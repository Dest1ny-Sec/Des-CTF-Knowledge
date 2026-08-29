---
title: 磐石CTF2025 Pwn赛题user解析：解密0xfbad1880背后的IO_FILE结构体利用技术
contest: 磐石CTF2025
year: 2025
difficulty: medium
vuln_type: heap_exploit
tags: [IO_FILE结构体, 0xfbad1880, _IO_2_1_stdout_, _flags字段, _IO_write_base/ptr, glibc 2.31, 负数idx, 任意地址写]
attack_chain: heap[-8] = _IO_2_1_stdout_→edit修改stdout结构体→_flags=0xfbad1880+_IO_write_base改低地址→泄露libc地址→其他漏洞(如tcache)任意地址写
key_payload: "heap[-8]=_IO_2_1_stdout_;_flags=0xfbad1880;_IO_write_base低地址;stdout距离heap 0x40字节;heap数组5个chunk 0x50/0x40;delete/edit负数idx"
one_liner: 磐石CTF2025 user：glibc 2.31菜单题无show+IO_FILE结构体伪造+stdout泄露libc
lesson: 堆bss数组距stdout固定0x40字节可用edit(-8)修改stdout；_flags=0xfbad1880触发写缓冲
quality: high
---

# 磐石CTF2025 Pwn赛题user解析：解密0xfbad1880背后的IO_FILE结构体利用技术

**赛事**：磐石CTF2025 - user

**难度**：92人解题

**知识点**：IO_FILE结构体伪造 + stdout泄露libc + glibc 2.31任意地址写

**逆向分析**：

**add()**：
- bss段全局变量heap[5]存chunk指针
- 空闲位置申请0x50 chunk，读0x40数据

**delete()**：
- 输入idx，若 heap[idx] != NULL 则 free()
- **只判断 idx > 4，没考虑负数**

**edit()**：
- 修改 heap[idx] 最多0x40数据
- 同样**没判断负数**

**show()**：
- 没有输出功能
- 仅 puts("output not available")

**漏洞**：
- 无show功能
- delete/edit 接受负数idx
- bss段heap数组与标准IO距离固定0x40字节
- **edit(-8) 修改 _IO_2_1_stdout_**

**IO_FILE结构体**：
- stdout是 _IO_FILE 结构体
- 维护输出缓冲：
  - `_IO_write_base`：写缓冲区起始
  - `_IO_write_ptr`：已写入末尾
  - `_IO_write_end`：写缓冲区结束
- `_flags` 字段常为 `0xfbad1800`（带magic）
- `0xfbad1880` 是另一个变体

**stdout泄露libc原理**：
- 修改 `_flags = 0xfbad1880`（包含 _IO_CURRENTLY_PUTTING）
- 修改 `_IO_write_base` 为低地址（如 _IO_2_1_stderr_ 某字段）
- 修改 `_IO_write_ptr` 大于 `_IO_write_base`
- 调用 puts() → 从 _IO_write_base 写到 _IO_write_ptr → 泄露libc地址

**内存布局**：
```
heap数组 [5个指针] = 0x40字节
↓
[0x40字节间隔]
↓
_IO_2_1_stdout_ 结构体
```
- `edit(-8)` 修改 stdout
- 修改0x40字节可覆盖stdout前0x40字节

**利用链**：
1. edit(-8) 修改stdout结构体
2. 触发puts/输出 → 泄露libc地址
3. 利用其他漏洞（如tcache/任意地址写）打 system("/bin/sh")

**关键技术**：
- bss段数组与标准IO的固定距离
- 负数idx可越界访问
- IO_FILE结构体_flags=0xfbad1880
- _IO_write_base/ptr控制输出范围
- glibc 2.31堆利用

**质量评估**：高（IO_FILE结构体详解 + stdout泄露原理 + 利用链）
