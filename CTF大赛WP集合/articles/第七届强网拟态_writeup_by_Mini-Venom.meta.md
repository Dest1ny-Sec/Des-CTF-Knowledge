---
title: 第七届强网拟态 writeup by Mini-Venom
contest: 第七届强网拟态
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [强网拟态, pwn模板, ret2libc_orw, 栈溢出, Mini-Venom EXP模板, signin栈溢出]
attack_chain: pwn题栈溢出→ret2libc_orw→system(/bin/sh)或ORW读flag
key_payload: "pwntools模板;栈溢出;ret2libc_orw;fopen NULL;Mini-Venom"
one_liner: 第七届强网拟态Pwn：signin栈溢出+ret2libc_orw+Mini-Venom EXP模板
lesson: pwnlib模板l32/l64/uu32/uu64可重复使用；ret2libc_orw是栈溢出通用解
quality: low
---

# 第七届强网拟态 writeup by Mini-Venom

**赛事**：第七届强网拟态（2024）

**性质**：Mini-Venom Pwn方向writeup

**signin题**：
- 纯在栈溢出
- 打 ret2libc_orw 即可
- system(/bin/sh) 或 ORW 读flag

**Mini-Venom标准pwn模板**：
```python
from pwn import *
from struct import pack
from ctypes import *
import base64

def debug(c=0):
    if c: gdb.attach(p, c)
    else: gdb.attach(p); pause()

def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/sh\x00'))

s = lambda data: p.send(data)
sa = lambda text, data: p.sendafter(text, data)
sl = lambda data: p.sendline(data)
sla = lambda text, data: p.sendlineafter(text, data)
r = lambda num=4096: p.recv(num)
rl = lambda text: p.recvuntil(text)
pr = lambda num=4096: print(p.recv(num))
inter = lambda: p.interactive()

l32 = lambda: u32(p.recvuntil(b'\xf7')[-4:].ljust(4, b'\x00'))
l64 = lambda: u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
uu32 = lambda: u32(p.recv(4).ljust(4, b'\x00'))
uu64 = lambda: u64(p.recv(6).ljust(8, b'\x00'))
int16 = lambda data: int(data, 16)
lg = lambda s, num: p.success('%s -> 0x%x' % (s, num))
```

**质量评估**：低（仅含模板和signin题）
