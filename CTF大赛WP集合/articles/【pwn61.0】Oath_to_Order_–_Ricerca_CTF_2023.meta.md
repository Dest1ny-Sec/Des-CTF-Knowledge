---
title: 【pwn61.0】Oath to Order - Ricerca CTF 2023
contest: RicercaCTF
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags: [aligned_alloc, size-0-bug, getstr-overflow, fastbin-free, libc-leak, malloc-algorithm, fuzzer-find-vuln]
attack_chain: 1. NOTE_LEN=10 NOTE_SIZE=300 不可 free/edit/create(idx, align, size, data) 多次写同 index 重新 alloc/2. aligned_alloc(align, size) + size=0 时 getstr(buf, 0) while(--size) 不进入循环任意长输入 → 堆溢出/3. align=0xF0 + size=0x20 aligned_alloc split 3 块 1+3 释放 + 残留 main_arena libc 指针/4. Fuzz 找 size=0 漏洞
key_payload: aligned_alloc(0xF0, 0) + getstr size=0 任意长输入  fastbin 残留 libc 指针 0x7f1773219ce0
one_liner: Ricerca CTF 2023 Oath to Order 高级堆题，aligned_alloc size=0 整数零化触发任意长输入 + fastbin 残留 libc 指针泄地址。
lesson: aligned_alloc(align, size) 内部走 __int_memalign → __int_malloc(size + align) split 3 块机制；size=0 时 getstr while(--size) 直接退出，可写任意长数据；fastbin 残留指针是经典 libc 泄方法。
quality: high
---

# 【pwn61.0】Oath to Order - Ricerca CTF 2023

## 题目分析

### 限制
- 最多 NOTE_LEN(10) 个 note
- 每个 note 最多 NOTE_SIZE(300) 字节
- **不可 free 分配的 note**
- **不可 edit 分配的 note**
- 可指定 index 写入，**每次写入都重新 allocation**
- 分配方式 `aligned_alloc(align, size)`，align 可小于 NOTE_SIZE

### 关键点
- notes 通过 `aligned_alloc` 分配（不同寻常）
- 这是本题的核心 trick

## 漏洞发现

### Fuzzer 流程
- 作者写 fuzzer 跑程序，回家时崩溃
- 崩溃条件：`align == 0x100` 且 `size == 0`

### getstr 漏洞
```c
void getstr(char *buf, unsigned size) {
    while (--size) {
        if (read(STDIN_FILENO, buf, sizeof(char)) != sizeof(char))
            exit(1);
        else if (*buf == '\n')
            break;
        buf++;
    }
    *buf = '\0';
}
```
- 当 `size == 0` 时，`--size` 溢出为 0xFFFFFFFF
- 循环继续，可输入任意长度数据
- 直到 '\n' 退出

## aligned_alloc 机制

### 简化流程
1. 如果 `align < MALLOC_ALIGNMENT`（多数为 0x10），直接调 `__libc_malloc()`
2. 如果 `align` 不是 2 的幂，向上取整到下一个 2 的幂（违反 POSIX，但 glibc 行为）
3. 调 `__int_memalign()`，其中 `__int_malloc()` 分配 `size + align` 字节（worst case）
4. 找到对齐位置，**split 块为 3 块**
5. 第 1 块和第 3 块被 free
6. 返回第 2 块（用户数据）

## Heap Puzzle: 通过 free fastbin 泄 libc base

### Stage 1: aligned_alloc(0xF0, 0)
```python
create(0, 0xF0, 0, b"A"*0x10 + p64(0xF0) + p32(0x40))
```

### 堆布局
```
# Chunk A (fastbin, last_remainder)
0x5581b77ee000: 0x0000000000000000  0x00000000000000f1
0x5581b77ee010: 0x00007f1773219ce0  0x00007f1773219ce0  # main_arena 指针！
0x5581b77ee020: 0x0000000000000000  0x0000000000000000
...
0x5581b77ee080: 0x0000000000000000  0x0000000000000000
```

- size=0 时 aligned_alloc 分配最小 0x20 块
- 第 1 块 + 第 3 块被 free
- 残留 main_arena libc 指针 `0x00007f1773219ce0`

## 经验提炼
- `aligned_alloc(align, size)` 内部走 `__int_memalign` → `__int_malloc(size + align)` split 3 块机制
- size=0 时 getstr `while(--size)` 直接退出，可写任意长数据
- fastbin 残留指针是经典 libc 泄方法
- 不可 free/edit 是约束，让攻击面更窄
- 多次写入同 index 重新 alloc 是关键，残留旧块
- Fuzzer 自动发现 `align==0x100 size==0` 崩溃条件
- main_arena + 96 是 unsorted bin 头
- 0x7f 开头地址是 64 位指针高字节（libc/mmap 区）
