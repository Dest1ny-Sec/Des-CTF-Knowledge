---
title: PWN 赛题解析
contest: 看雪论坛 ctfiot 系列
year: 2024
difficulty: medium
vuln_type: rop
tags: [pwn, ret2libc, shellcode, seccomp, sandbox-bypass, fmt-string, 栈迁移, orw]
attack_chain:
  - 一 stdout 题：read 0x60 越界写覆盖 rbp/rip
  - 跳 vuln 函数循环 20 次填满 stdout 缓冲区
  - 泄 read@got 计算 libc 偏移
  - 构造 pop_rdi+rsi+rdx 调 execve
  - 二 Shuffled_Execution 题：seccomp 沙箱禁 execve 系
  - 写入 orw shellcode (openat+mmap+writev)
  - 三 SavethePrincess：rand 派生密钥 + 偏序密码爆破
  - 泄 canary/libc/stack 三件套
  - 栈迁移到 mprotect rwx 区域执行 shellcode
  - 四 spiiill：自定义 VM 字节码解释器
  - 越界 PC 控制跳 system 执行 sh
key_payload: payload1='a'*0x58+p64(vuln); payload4=p64(0xa)+p64(0xc)+p64(0xfffffffffffffc02)+'sh\x00'
one_liner: 4 道 PWN 题合集，涵盖 ret2libc 泄地址循环填充、seccomp 下 openat+mmap+writev orw、fmt-string 泄三件套栈迁移、自定义 VM 解释器 PC 劫持。
lesson: ASLR 开启时只能绕过 libc/stack/canary；seccomp 沙箱禁 execve 时必须用 openat+mmap+writev 替代；自定义 VM 程序 PC 越界即可劫持控制流。
quality: high
---
