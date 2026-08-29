---
title: PWN - 西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up
contest: 西湖论剑 2022 中国杭州网络安全技能大赛 初赛
year: 2023
difficulty: high
vuln_type: rop
tags: [pwn, z3-solver, babycalc, jit, message-board, fmt-string, 栈迁移, orw]
attack_chain:
  - 一 babycalc：read 末尾置 0 单字节溢出覆盖 rbp LSB
  - 任意偏移写 1 字节改 retaddr 为 leave;ret 触发栈迁移
  - 栈迁移到可控数据区布置 ret*21 + pop_rdi+got+puts+start 泄 libc
  - 输入 16 字节 z3 方程答案 (0x13 0x24 0x35 ... 0x03)
  - 计算 one_gadget 0xf1247 二次栈迁移
  - 二 jit：自研 IR (mov/and/or/xor/call) → mmap 编译为机器码
  - var2idx 整数溢出：variba=32 时 -8*32=0 绕过 fatal 检查
  - 用 jop 链 + movabs rsi 写入 6 字节 shellcode (push /sh; pop rax; shl 32; push /bin; or; syscall 0x3b)
  - 利用 ASLR 改写 retaddr 后 12 位跳 shellcode
  - 三 Message Board：seccomp 禁 execve 59 号系统调用
  - fmt-string 泄 libc + 栈溢出 0x10 控 rbp+ret
  - 跳 mov [rbp] rsi gadget 任意地址写 0xC0 (orw rop)
  - 二次 leave;ret 栈迁移到 bss 区域执行 open+read+puts 链
key_payload: jit sc="\x68/sh\x00" + "\x58\x48\xc1\xe0\x20" + "\x68/bin" + "\x5f\x48\x09\xf8" + "\x50\x48\x89\xe7" + "\x48\x31\xf6\x48\x31\xd2" + "\x6a\x3b\x58\x0f\x05"
one_liner: 西湖论剑 2022 三道 PWN 官方 WP：babycalc 单字节溢出+栈迁移、jit 自研 IR 编译器整数溢出、Message Board seccomp 沙箱下 orw+栈迁移双跳。
lesson: read 末尾 NUL 字节可单字节溢出改 rbp；自研 JIT 必须审计 var2idx 等边界检查；seccomp 禁 execve 必走 open+read+puts orw；fmt-string 泄 libc 后栈迁移到 bss 是经典二段跳。
quality: high
---
