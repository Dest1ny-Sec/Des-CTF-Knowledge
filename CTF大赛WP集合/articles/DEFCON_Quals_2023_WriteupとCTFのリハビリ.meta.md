---
title: DEFCON Quals 2023 Writeup と CTF のリハビリ
contest: DEFCON
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags: [glibc-2.37, glibc-2.35, tcache-double-free, cyclic-0x208, house-of]
attack_chain:
  - cyclic(0x208) 输入 create
  - 11 次 delete(1) 触发 unsorted bin
  - create("") 切割 unsorted bin
  - 多次 create 触发 tcache
  - libc 2.37 mmap_threshold 调整
  - tcache double free 攻击
key_payload: cyclic 0x208 + 11 次 delete 触发 unsorted bin
one_liner: DEFCON 2023 Quals open-house PWN 题复盘，日文 WP。
lesson: 11 次 delete(1) 同一个 index 触发 tcache 重复 + unsorted bin 残留。
quality: high
---

DEFCON 2023 Quals open-house PWN 复盘，作者日本 CTFer。

**题目信息**
ELF 32-bit LSB PIE 启用、No canary、NX enabled、No RELRO、stripped。

**菜单**：c(create) / v(view) / m(modify/replace) / d(delete) / q(quit)

**利用**：
```python
create(cyclic(0x208))
for i in range(11):
    delete(1)
create("")
create("")
create("")
create("")
```

`cyclic(0x208)` 输入后栈/堆块 0x208 字节填满；连续 11 次 delete(1) 触发 tcache (0x110 size 7 个) + 1 个进 unsorted bin (glibc-2.32+)；`create("")` 切割 unsorted bin 拿 libc 地址。

**坑点**：
- glibc 2.37 mmap_threshold 默认 128KB，多次 create 后大块会改用 mmap
- delete 同一 index 11 次会触发 double-free 检测 → 改用 create+delete 循环

详细利用链涉及 tcache_perthread_struct 攻击 + house of apple 2 + 栈劫持 + ROP to system。
