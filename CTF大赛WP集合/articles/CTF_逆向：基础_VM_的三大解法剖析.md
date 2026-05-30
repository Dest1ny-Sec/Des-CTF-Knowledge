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
filename = r"E:CTFproblemmatch2025二进制第一次测试二进制测试revm.exe"
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
```



```
import idaapi
import idc
start_address = 0x7A31D0
data_length = 16 * 25 # 略微多提取，一定要提取正确，不然后面很痛苦
# 将字节对象转换为十六进制字符串
with open("E:\CTF\code\python\CTF\dumpopcode.txt", "a") as f:
 for i in range(0,data_length):
 f.write(hex(idc.get_wide_byte(start_address+i)))
 f.write("n")
```



```
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
```



```
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
```



```
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
```



```
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
```



```
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
filename = r"E:CTFproblemmatch2025二进制第一次测试二进制测试revm.exe"
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-6f62b76ef398386534b11122f58cbe08.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-7a1cf5d8fa0250842fce760e6e30b095.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-cd6256d3912ff34f839b2456c8430ee1.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-eeb7500f7e03bc00ad6548be2104a2ca.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c6ce9fcadacfd79119760ee44d0d99fc.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c299832ba8799518f31b6c1234f5bbc4.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-0cc0be049b057ef4324c7d332157af89.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-df9c66aad7afae3c9c7483b817164875.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-2edc6175d9d5ef32a7dac91b48086f30.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-71612baea187590d75a96ee2368782fc.webp)