---
title: 第七届 强网杯 全国网络安全挑战赛 Web Writeup
contest: 第七届强网杯
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [强网杯Web, xcache read-only protection, mmap RO/RW, /tmp/clean_b3, xc_php_find_unlocked hook, 函数指针patch, mprotect]
attack_chain: xcache只读保护→同文件mmap两次(ro_addr/rw_addr 0x4000000间隔)→hook xc_php_find_unlocked返回fake值→用函数指针后3位地址找libphp基址→把远程函数指针全部替换成本地函数指针
key_payload: "xcache read only protection;mmap两次0x4000000间隔;ro_addr=0x7fb5ed09c000;rw_addr=0x7fb5ed09c000+0x4000000;xc_php_find_unlocked强制返回fake;函数指针后3位;clean_b3文件"
one_liner: 第七届强网杯Web：xcache只读保护+mmap两次+xc_php_find_unlocked hook+函数指针patch
lesson: xcache启用read-only protection时同文件被mmap两次（ro+rw），攻击者需patch映射到rw区域
quality: high
---

# 第七届 强网杯 全国网络安全挑战赛 Web Writeup

**赛事**：第七届强网杯 Web方向

**核心挑战**：xcache read-only protection

**题目核心思路**：

**Step 1：理解xcache只读保护**
- 远程启用xcache read-only protection
- 同一个文件被mmap了**两次**：
  - 只读 (PROT_READ) 映射：`ro_addr = 0x7fb5ed09c000`
  - 读写 (PROT_READ|PROT_WRITE) 映射：`rw_addr = 0x7fb5ed09c000 + 0x4000000`
  - 大小都是 0x4000000

```c
void mymmap() {
    int file1 = open("/tmp/clean_b3", O_RDONLY);
    size_t ro_addr = 0x7fb5ed09c000;
    size_t rw_addr = 0x7fb5ed09c000 + 0x4000000;
    size_t ro_size = 0x4000000;
    int mmap1_result = mmap(ro_addr, ro_size, PROT_READ, MAP_PRIVATE | MAP_FIXED, file1, 0);
    int mmap2_result = mmap(rw_addr, ro_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_FIXED, file1, 0);
}
```

**Step 2：hook xc_php_find_unlocked**
- 在 xc_php_find_unlocked 函数中：
  - 第一次调用时，强制返回 fake 值（已 mmap 的地址）
  - 后续调用不处理
```c
if (is_replaced_1 == 0) {
    is_replaced_1 = 1;
    mymmap();
    char* ptr = 0x7fb5f10bc1e8;
    return ptr;
}
```

**Step 3：找mmap基址**
```python
from pwn import *
filename = "clean_b3"
with open(filename, "rb") as f:
    f.seek(0x20230)
    ptr = u64(f.read(8))  # mmap地址
    f.seek(0x20290)
    ptr2 = u64(f.read(8))  # sanity check
delta = 0x20290
root = ptr - delta
real_rw_root = root + 0x4000000  # rw基址
```

**Step 4：函数指针patch**
- 用函数指针后3位地址找libphp基址
- 把mmap文件里远程函数指针全部替换成本地函数指针
```python
remote_regex = br'.{3}\xff\xb5\x7f\x00\x00'  # 远程函数指针
local_regex = br'.{3}\xf6\xff\x7f\x00\x00'  # 本地函数指针
# 替换映射
```

**关键技术**：
- xcache read-only protection工作原理
- mmap两次映射 ro+rw（0x4000000间隔）
- xc_php_find_unlocked hook点选择
- 函数指针后3位匹配libphp基址
- clean_b3文件分析与patch

**质量评估**：高（xcache深度利用 + mmap机制 + 函数指针patch）
