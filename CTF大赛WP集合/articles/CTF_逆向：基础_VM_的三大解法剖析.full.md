---
title: CTF 逆向：基础 VM 的三大解法剖析
contest: CTF Reverse
year: 2024
difficulty: medium
vuln_type: reverse
tags:
- VM字节码
- opcode 0x01/0x04/0x05 add/sub/xor
- target+value 操作数
- IDA get_wide_byte 提取
- z3 BitVec 8位约束
- Frida hook onEnter 计数
- encode/decode 对称
- flag_enc 32字节密文
attack_chain:
- 'VM 字节码: opcode 0x01 加 / 0x04 减 / 0x05 异或'
- '操作数: (target, value) - flag[target] += value / -= value / ^= value'
- '解法 1: IDA Python idc.get_wide_byte(start+i) 提取 0x7A31D0 起 16*25 字节'
- '解法 2: deopcode 倒序遍历 (3字节一组) 还原 flag'
- '解法 3: z3 BitVec 8位 + solver 约束每字节 == flag_enc'
- '解法 4: Frida hook vm.exe + 0x197F onEnter 计数, send(number) 到 Python'
- flag_enc = [0x65, 0xE2, ..., 0xFD] 32 字节
key_payload: '''VM opcode 0x01/0x04/0x05 / (target, value) 操作 / IDA get_wide_byte / z3 BitVec 8位 / deopcode 倒序 / Frida Interceptor.attach onEnter'''
one_liner: CTF VM 基础 — VM 字节码 0x01/0x04/0x05 (add/sub/xor) + IDA get_wide_byte 提取 + z3 BitVec 8 位约束 + deopcode 倒序遍历 + Frida hook onEnter 计数。
lesson: VM 逆向 3 大解法:① IDA 提取 opcode + 解释执行 / ② 倒序遍历反推 (因为加减异或操作可逆) / ③ z3 符号执行约束求解;VM 字节码通常 3 字节一组 (op, target, value)。
quality: high
full_path: CTF_逆向：基础_VM_的三大解法剖析.full.md
meta_path: CTF_逆向：基础_VM_的三大解法剖析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'CTF 逆向：基础 VM 的三大解法剖析。CTF VM 基础 — VM 字节码 0x01/0x04/0x05 (add/sub/xor) + IDA get_wide_byte 提取 + z3 BitVec 8 位约束 + deopcode 倒序遍历 + Frida hook onEnter 计数。。关键路径：VM 字节码: opcode 0x01 加 / 0x04 减 / 0x05 异或 ...'
category: reverse
subcategory: reverse
tools_used:
- IDA
- Python
- Z3
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/235951.html
reasoning_chain:
- 触发点：VM 字节码主循环 while(i<len) 解析 opcode → 假设：典型 switch-case VM 三类操作
- 动作：分析 opcode 0x00 nop / 0x01 add flag[target]+=value / 0x04 sub / 0x05 xor → 观察：每条指令 3 字节 (op, target, value)
- 假设：操作可逆 → 动作：解法 1 IDA get_wide_byte(0x7A31D0+i) 提取 16*25 字节 + Python 解释执行 → 观察：解出 flag
- 假设：加减异或可逆 → 动作：解法 2 deopcode 倒序遍历 opcode 应用 (sub→add, add→sub, xor→xor) 还原 flag 字节
- 假设：可以用 SAT 求解 → 动作：解法 3 z3 BitVec('flag[i]', 8) + 32 字节约束迭代 → 观察：s.check()=sat 得到 32 字符
- 假设：还能动态 hook → 动作：解法 4 Frida Interceptor.attach(vm.exe + 0x197F).onEnter 数 send(number) → Python 收集
- 观察：四种解法殊途同归 → 完成
failed_attempts:
- 试图用 IDA F5 反编译直接看逻辑 → 失败：opcode 是手工解释执行，F5 看不到 switch state machine
- 试图用 Python ctypes 模拟执行整个 VM → 失败：VM 解释器太复杂，opcode 操作更直接
- 试图猜默认 flag 长度 → 失败：flag_enc 是 32 字节硬编码
key_observations:
- VM 逆向 3 大解法：① IDA 提取 opcode + 解释执行 / ② 倒序遍历反推（可逆操作）/ ③ z3 符号执行约束
- VM 字节码通常 3 字节一组（op/target/value）
- 加减异或都是可逆操作，逆向可还原（除法不可逆）
- Frida onEnter 计数器能打印执行序列辅助理解
- 32 字节约束 + z3 BitVec 8 位单层 SAT 几分钟就能出
prerequisites:
- IDA Python 脚本（idc.get_wide_byte 提取内存）
- VM 字节码分析 + opcode 反汇编模式
- z3 BitVec + Solver 约束建模
- Frida Interceptor.attach + onEnter 回调
- Python 字节/列表/字符转换
---
# CTF 逆向：基础 VM 的三大解法剖析

> 原文: https://www.ctfiot.com/235951.html
> ID: 235951

1

VM核心原理速览

while(i<len(opcode)):
 if(opcode[i]==0x00):
 i+=1
 elif(opcode[i]==0x01):
 i+=2
 elif(opcode[i]==0x02):
 i+=3

2

三种解法

3

解题

import idaapi
import idc
start_address = 0x7A31D0
data_length = 16 * 25 # 略微多提取，一定要提取正确，不然后面很痛苦
# 将字节对象转换为十六进制字符串
with open("E:\CTF\code\python\CTF\dumpopcode.txt", "a") as f:
 for i in range(0,data_length):
 f.write(hex(idc.get_wide_byte(start_address+i)))
 f.write("n")

def encode(flag, opcode):
 encoded_flag = flag.copy()
 i = 1
 while i < len(opcode):
 op_type = opcode[i - 1]
 target = opcode[i]
 value = opcode[i + 1]
 if op_type == 1:
 writefile(f"flag[{target}] = flag[{target}] + {hex(value)};")
 i += 3
 elif op_type == 4:
 writefile(f"flag[{target}] = flag[{target}] - {hex(value)};")
 i += 3
 elif op_type == 5:
 writefile(f"flag[{target}] = flag[{target}] ^ {hex(value)};")
 i += 3
 else:
 break
 return encoded_flag

import z3
def getfile(file_path):
 opcode = []
 with open(file_path, 'r') as file:
 for line in file:
 opcode.append(int(line.strip(), 16))
 return opcode
def enopcode(opcode):
 read_opcode=[]
 i = 1
 while i<len(opcode):
 while True:
 while opcode[i - 1] == 1:
 read_opcode.append(opcode[i])
 read_opcode.append(1)
 read_opcode.append(opcode[i+1])
 i += 3
 if opcode[i - 1] != 4:
 break
 read_opcode.append(opcode[i])
 read_opcode.append(2)
 read_opcode.append(opcode[i+1])
 i += 3
 if opcode[i - 1] == 5:
 read_opcode.append(opcode[i])
 read_opcode.append(3)
 read_opcode.append(opcode[i+1])
 i += 3
 else:
 break
 return read_opcode
def deopcode(value,opcode,number):
 for i in range(len(opcode)-3,-1,-3):
 if opcode[i]==number:
 if opcode[i+1]==1:
 value-=opcode[i+2]
 print(f'flag[{number}]-={hex(opcode[i+2])}')
 elif opcode[i+1]==2:
 value+=opcode[i+2]
 print(f'flag[{number}]+={hex(opcode[i+2])}')
 elif opcode[i+1]==3:
 value^=opcode[i+2]
 print(f'flag[{number}]^={hex(opcode[i+2])}')
 return value&0xff
if __name__ == '__main__':
 oriopcode = getfile("E:\CTF\code\python\CTF\dumpopcode.txt")
 flag_enc = [
 0x65, 0xE2, 0x57, 0x60, 0xCE, 0x1E, 0xE1, 0x5C, 0x4B, 0x4B,
 0x23, 0x6D, 0x8C, 0xC2, 0xBC, 0x58, 0x84, 0x92, 0x7E, 0x8C,
 0x43, 0xDB, 0x15, 0x71, 0x97, 0x4A, 0xE3, 0xC4, 0x1F, 0x7C,
 0xC2, 0xFD
 ]
 opcode=enopcode(oriopcode)
 flag=[]
 for i in range(0,len(flag_enc)):
 flag.append(deopcode(flag_enc[i],opcode,i))
 print(''.join(chr(flag[i]) for i in range(len(flag))))

import z3

def getfile(file_path):
 opcode = []
 with open(file_path, 'r') as file:
 for line in file:
 opcode.append(int(line.strip(), 16))
 return opcode

def encode(flag, opcode):
 encoded_flag = flag.copy()
 i = 1
 while i < len(opcode):
 op_type = opcode[i - 1]
 target = opcode[i]
 value = opcode[i + 1]

 if op_type == 1:
 # 加法操作后截断为 8 位
 encoded_flag[target] = (encoded_flag[target] + value) & 0xFF
 print(f"flag[{target}] += {hex(value)}")
 i += 3
 elif op_type == 4:
 # 减法操作后截断为 8 位
 encoded_flag[target] = (encoded_flag[target] - value) & 0xFF
 print(f"flag[{target}] -= {hex(value)}")
 i += 3
 elif op_type == 5:
 # 异或操作后截断为 8 位
 encoded_flag[target] = (encoded_flag[target] ^ value) & 0xFF
 print(f"flag[{target}] ^= {hex(value)}")
 i += 3
 else:
 break # 未知操作类型退出循环
 return encoded_flag

if __name__ == '__main__':
 opcode = getfile("E:\CTF\code\python\CTF\dumpopcode.txt")
 flag_size = 32
 flag = [z3.BitVec(f'flag[{i}]', 8) for i in range(flag_size)] # 使用 8 位 BitVec
 flag_enc = [
 0x65, 0xE2, 0x57, 0x60, 0xCE, 0x1E, 0xE1, 0x5C, 0x4B, 0x4B,
 0x23, 0x6D, 0x8C, 0xC2, 0xBC, 0x58, 0x84, 0x92, 0x7E, 0x8C,
 0x43, 0xDB, 0x15, 0x71, 0x97, 0x4A, 0xE3, 0xC4, 0x1F, 0x7C,
 0xC2, 0xFD
 ]

 solver = z3.Solver()
 encoded_flag = encode(flag, opcode)

 # 添加约束：每个字节最终等于 flag_enc
 for j in range(len(flag_enc)):
 solver.add(encoded_flag[j] == flag_enc[j])
 for i in solver.assertions():
 print(i)
 if solver.check() == z3.sat:
 model = solver.model()
 result_flag = [model.evaluate(flag[i]).as_long() for i in range(flag_size)]
 print(result_flag)
 else:
 print("No solution found.")
# a=[98, 48, 98, 51, 101, 97, 97, 57, 55, 56, 51, 102, 54, 49, 57, 101, 49, 49, 98, 48, 97, 52, 48, 54, 52, 48, 50, 53, 48, 49, 56, 97]
# for i in a:
# print(chr(i),end='')

var number = 22;
function main() {
 var base = Module.findBaseAddress("vm.exe");
 if (base) {
 // console.log(base);
 Interceptor.attach(base.add(0x197F), {//循环的地方
 //opcode
 onEnter: function(args) {
 number += 1;
 }
 });
 Interceptor.attach(base.add(0x19A2), { //最好放在retn
 // Interceptor.attach(0x7FF755321965, { 直接给地址这样好像不行
 onEnter: function(args) {

 //console.log(number)
 send(number);
 var a = 0;
 for (var i = 0; i < 10000; i++) {
 a += 1;
 }
 var f = new NativeFunction(base.add(0x274A), 'void', ['int']); //exit函数地址,不是特别特别重要
 f(0);
 }
 });
 }
}

setImmediate(main);

import subprocess
import frida
import sys
import win32api
import win32con
import time

# 已知的 flag 部分
known_flag = b''

# 总 flag 长度
flaglen = 40
filename = r"E:
CTFproblemmatch2025二进制第一次测试二进制测试revm.exe"
exename = 'vm.exe'

# 根据已知部分创建初始 flag
flag = bytearray(known_flag + b' ' * (flaglen - len(known_flag)))

jscode = open("frida/hook.js", "rb").read().decode()
new_number = 0
result = 0

def brute(F):
 def on_message(message, data):
 global result
 if message['type'] == 'send':
 result = message['payload']
 # print(result)
 # else:
 # print(message)

 process = subprocess.Popen(filename, stdin=subprocess.PIPE,
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 universal_newlines=True)

 session = frida.attach(exename)
 script = session.create_script(jscode)
 script.on('message', on_message)
 script.load()
 print(f"r{F.decode()}", end='')
 process.stdin.write(F.decode())
 output, error = process.communicate()

 # time.sleep(20)

 # print(output)

 # print(f"number:{result}")
 process.terminate()
 return result

count = len(known_flag)
new_number = brute(flag)
t = time.time()
st = t
while count < flaglen:
 number = brute(flag)
 print(number)
 if number!= new_number:
 new_number = number
 count += 1
 else:
 flag[count] += 1
 if flag[count] > 127:
 flag[count] = ord('?')
 count += 1
print(f"总耗时{time.time() - st}")
print(flag.decode())

看雪ID：namename123

https://bbs.kanxue.com/user-home-997837.htm

*本文为看雪论坛优秀文章，由 namename123 原创，转载请注明来自看雪社区

# 往期推荐

1、Android逆向0基础入门：APK全面解析、动调与脱壳

2、Ghidra基于脚本的恶意软件分析

3、PE攻击之傀儡进程与重定位

4、通用 Linux kernel rootkit 开发导论

5、Web安全入门-网络资源的访问-隧道

6、PWN入门：GLibC堆请UAF

球分享

球点赞

球在看

点击阅读原文查看更多


```
while(i<len(opcode)):
 if(opcode[i]==0x00):
 i+=1
 elif(opcode[i]==0x01):
 i+=2
 elif(opcode[i]==0x02):
 i+=3
import idaapi
import idc
start_address = 0x7A31D0
data_length = 16 * 25 # 略微多提取，一定要提取正确，不然后面很痛苦
# 将字节对象转换为十六进制字符串
with open("E:\CTF\code\python\CTF\dumpopcode.txt", "a") as f:
 for i in range(0,data_length):
 f.write(hex(idc.get_wide_byte(start_address+i)))
 f.write("n")
def encode(flag, opcode):
 encoded_flag = flag.copy()
 i = 1
 while i < len(opcode):
 op_type = opcode[i - 1]
 target = opcode[i]
 value = opcode[i + 1]
 if op_type == 1:
 writefile(f"flag[{target}] = flag[{target}] + {hex(value)};")
 i += 3
 elif op_type == 4:
 writefile(f"flag[{target}] = flag[{target}] - {hex(value)};")
 i += 3
 elif op_type == 5:
 writefile(f"flag[{target}] = flag[{target}] ^ {hex(value)};")
 i += 3
 else:
 break
 return encoded_flag
import z3
def getfile(file_path):
 opcode = []
 with open(file_path, 'r') as file:
 for line in file:
 opcode.append(int(line.strip(), 16))
 return opcode
def enopcode(opcode):
 read_opcode=[]
 i = 1
 while i<len(opcode):
 while True:
 while opcode[i - 1] == 1:
 read_opcode.append(opcode[i])
 read_opcode.append(1)
 read_opcode.append(opcode[i+1])
 i += 3
 if opcode[i - 1] != 4:
 break
 read_opcode.append(opcode[i])
 read_opcode.append(2)
 read_opcode.append(opcode[i+1])
 i += 3
 if opcode[i - 1] == 5:
 read_opcode.append(opcode[i])
 read_opcode.append(3)
 read_opcode.append(opcode[i+1])
 i += 3
 else:
 break
 return read_opcode
def deopcode(value,opcode,number):
 for i in range(len(opcode)-3,-1,-3):
 if opcode[i]==number:
 if opcode[i+1]==1:
 value-=opcode[i+2]
 print(f'flag[{number}]-={hex(opcode[i+2])}')
 elif opcode[i+1]==2:
 value+=opcode[i+2]
 print(f'flag[{number}]+={hex(opcode[i+2])}')
 elif opcode[i+1]==3:
 value^=opcode[i+2]
 print(f'flag[{number}]^={hex(opcode[i+2])}')
 return value&0xff
if __name__ == '__main__':
 oriopcode = getfile("E:\CTF\code\python\CTF\dumpopcode.txt")
 flag_enc = [
 0x65, 0xE2, 0x57, 0x60, 0xCE, 0x1E, 0xE1, 0x5C, 0x4B, 0x4B,
 0x23, 0x6D, 0x8C, 0xC2, 0xBC, 0x58, 0x84, 0x92, 0x7E, 0x8C,
 0x43, 0xDB, 0x15, 0x71, 0x97, 0x4A, 0xE3, 0xC4, 0x1F, 0x7C,
 0xC2, 0xFD
 ]
 opcode=enopcode(oriopcode)
 flag=[]
 for i in range(0,len(flag_enc)):
 flag.append(deopcode(flag_enc[i],opcode,i))
 print(''.join(chr(flag[i]) for i in range(len(flag))))
import z3

def getfile(file_path):
 opcode = []
 with open(file_path, 'r') as file:
 for line in file:
 opcode.append(int(line.strip(), 16))
 return opcode

def encode(flag, opcode):
 encoded_flag = flag.copy()
 i = 1
 while i < len(opcode):
 op_type = opcode[i - 1]
 target = opcode[i]
 value = opcode[i + 1]

 if op_type == 1:
 # 加法操作后截断为 8 位
 encoded_flag[target] = (encoded_flag[target] + value) & 0xFF
 print(f"flag[{target}] += {hex(value)}")
 i += 3
 elif op_type == 4:
 # 减法操作后截断为 8 位
 encoded_flag[target] = (encoded_flag[target] - value) & 0xFF
 print(f"flag[{target}] -= {hex(value)}")
 i += 3
 elif op_type == 5:
 # 异或操作后截断为 8 位
 encoded_flag[target] = (encoded_flag[target] ^ value) & 0xFF
 print(f"flag[{target}] ^= {hex(value)}")
 i += 3
 else:
 break # 未知操作类型退出循环
 return encoded_flag

if __name__ == '__main__':
 opcode = getfile("E:\CTF\code\python\CTF\dumpopcode.txt")
 flag_size = 32
 flag = [z3.BitVec(f'flag[{i}]', 8) for i in range(flag_size)] # 使用 8 位 BitVec
 flag_enc = [
 0x65, 0xE2, 0x57, 0x60, 0xCE, 0x1E, 0xE1, 0x5C, 0x4B, 0x4B,
 0x23, 0x6D, 0x8C, 0xC2, 0xBC, 0x58, 0x84, 0x92, 0x7E, 0x8C,
 0x43, 0xDB, 0x15, 0x71, 0x97, 0x4A, 0xE3, 0xC4, 0x1F, 0x7C,
 0xC2, 0xFD
 ]

 solver = z3.Solver()
 encoded_flag = encode(flag, opcode)

 # 添加约束：每个字节最终等于 flag_enc
 for j in range(len(flag_enc)):
 solver.add(encoded_flag[j] == flag_enc[j])
 for i in solver.assertions():
 print(i)
 if solver.check() == z3.sat:
 model = solver.model()
 result_flag = [model.evaluate(flag[i]).as_long() for i in range(flag_size)]
 print(result_flag)
 else:
 print("No solution found.")
# a=[98, 48, 98, 51, 101, 97, 97, 57, 55, 56, 51, 102, 54, 49, 57, 101, 49, 49, 98, 48, 97, 52, 48, 54, 52, 48, 50, 53, 48, 49, 56, 97]
# for i in a:
# print(chr(i),end='')
var number = 22;
function main() {
 var base = Module.findBaseAddress("vm.exe");
 if (base) {
 // console.log(base);
 Interceptor.attach(base.add(0x197F), {//循环的地方
 //opcode
 onEnter: function(args) {
 number += 1;
 }
 });
 Interceptor.attach(base.add(0x19A2), { //最好放在retn
 // Interceptor.attach(0x7FF755321965, { 直接给地址这样好像不行
 onEnter: function(args) {

 //console.log(number)
 send(number);
 var a = 0;
 for (var i = 0; i < 10000; i++) {
 a += 1;
 }
 var f = new NativeFunction(base.add(0x274A), 'void', ['int']); //exit函数地址,不是特别特别重要
 f(0);
 }
 });
 }
}

setImmediate(main);
import subprocess
import frida
import sys
import win32api
import win32con
import time

# 已知的 flag 部分
known_flag = b''

# 总 flag 长度
flaglen = 40
filename = r"E:
CTFproblemmatch2025二进制第一次测试二进制测试revm.exe"
exename = 'vm.exe'

# 根据已知部分创建初始 flag
flag = bytearray(known_flag + b' ' * (flaglen - len(known_flag)))

jscode = open("frida/hook.js", "rb").read().decode()
new_number = 0
result = 0

def brute(F):
 def on_message(message, data):
 global result
 if message['type'] == 'send':
 result = message['payload']
 # print(result)
 # else:
 # print(message)

 process = subprocess.Popen(filename, stdin=subprocess.PIPE,
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 universal_newlines=True)

 session = frida.attach(exename)
 script = session.create_script(jscode)
 script.on('message', on_message)
 script.load()
 print(f"r{F.decode()}", end='')
 process.stdin.write(F.decode())
 output, error = process.communicate()

 # time.sleep(20)

 # print(output)

 # print(f"number:{result}")
 process.terminate()
 return result

count = len(known_flag)
new_number = brute(flag)
t = time.time()
st = t
while count < flaglen:
 number = brute(flag)
 print(number)
 if number!= new_number:
 new_number = number
 count += 1
 else:
 flag[count] += 1
 if flag[count] > 127:
 flag[count] = ord('?')
 count += 1
print(f"总耗时{time.time() - st}")
print(flag.decode())
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]