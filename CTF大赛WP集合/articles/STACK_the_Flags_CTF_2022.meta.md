---
title: STACK the Flags CTF 2022 - cursed_grimoires
contest: STACK the Flags
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [house-of-botcake, stdout-leak, fsop, mmap-then-edit, glibc-2.35]
attack_chain:
- 选 Create Grimoire 一次，edit 单字节写
- menu() 调 puts 触发 stdout write 路径
- malloc 1MB 大块跨过 mmap threshold
- mmap 区域位于 libc_base-0xf7ff0 处
- edit 改 stdout->_flags = 0x1800 (NO_WRITES 清除 + APPEND/CURRENTLY)
- edit 改 stdout->_IO_write_ptr 末字节为 0x50
- 调 menu 触发 puts，泄 _IO_stdfile_1_lock 算 libc_base
- chunk_addr = libc_base - 0xf7ff0 即 mmap 区域
- 改 stdout->vtable 至 _IO_wfile_jumps
- 改 _wide_data->_wide_vtable 伪造 _IO_wfile_overflow
- ret2libc / 调 system 弹 shell
- Full RELRO + Canary + NX + PIE 全开下利用 FSOP
key_payload: edit(stdout_offset+0x28, 0x50)  # _IO_write_ptr LSB
one_liner: STACK the Flags 2022 cursed_grimoires：菜单 1/2/3 二进制 + 1MB 大块跨 mmap 边界 + 单字节 edit 改 stdout。
lesson: Full RELRO + Canary + NX + PIE 全开下，FSOP via _IO_wfile_jumps 仍可作为终极利用面。
quality: high
---
# STACK the Flags CTF 2022 - cursed_grimoires

## 题目结构
- Full RELRO + Canary found + NX + PIE 全开
- glibc 2.35 (Ubuntu 22.04)
- 菜单：1. Create Grimoire (only once)  2. Edit Grimoire  3. Finish
- Edit 支持单字节任意写：`GRIMOIRE[v2] = (getchar() & 0xff)`

## 漏洞路径
1. `malloc(1_000_000)` 触发 mmap 路径，chunk_addr 落在 libc_base - 0xf7ff0
2. 通过 `edit()` 在 chunk 内偏移 0x0/0x28 改 `_IO_2_1_stdout_` 字段
3. `_flags` 设 0x1800（清 _IO_NO_WRITES，置 _IO_CURRENTLY_PUTTING + _IO_IS_APPENDING）
4. `_IO_write_ptr` 末字节设为 0x50，扩张可写区
5. 再次调 `menu()` 走 `puts()` → `_IO_new_file_xsputn` → `_IO_new_file_overflow` → `new_do_write` → `_IO_SYSWRITE` 触发 stdout 越界写
6. `r.recv(16)[5:]` 提取 `_IO_stdfile_1_lock` 地址 → libc_base
7. 改 `stdout->vtable = _IO_wfile_jumps`
8. 改 `_wide_data->_wide_vtable` 指向 fake vtable
9. fake `_IO_wfile_overflow` → 触发 magic → system("/bin/sh")

## 关键 IO_validate_vtable
- glibc 2.35 强制 vtable 必须在 `__libc_IO_vtables` 段
- 旁路：篡改 `_wide_data->_wide_vtable`，绕开 vtable 范围检查
