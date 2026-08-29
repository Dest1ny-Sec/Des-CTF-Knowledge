---
title: PBCTF 2021 中有意思的 ARM CPU 题
contest: PBCTF
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags: [ARM CPU, 嵌入式 PWN, 跨平台二进制, 模拟器]
attack_chain: |
  1. 题目: PBCTF 2021 ARM CPU 题
  2. ARM 架构: 32-bit ARM 指令集
  3. 跨平台二进制: ELF for ARM
  4. 需要 ARM 模拟器 (qemu-arm) 或真机
  5. 详细内容 (缺 writeup)
key_payload: |
  # ARM CPU 题运行方式:
  # qemu-arm ./pwn
  # 或真机 ARM 设备
one_liner: PBCTF 2021 ARM CPU 跨平台 PWN 题，需要 qemu-arm 模拟器或真机。
lesson: |
  - ARM 32 位指令集: bx/bl/push/pop
  - 跨平台 PWN 需要模拟器 (qemu-user / qemu-arm)
  - ARM 与 x86 调用约定不同: r0-r3 参数, r11=fp, r13=sp, r14=lr, r15=pc
  - PBCTF 是 Project Berlin CTF
quality: low
---

# PBCTF 2021 中有意思的 ARM CPU 题

> 来源: ctfiot.com 80201 (提及)

## 题目背景

PBCTF 2021 中有一道 ARM CPU 相关的 PWN 题，跨平台二进制。

## 攻击方式

```bash
# qemu-arm 模拟器
qemu-arm ./pwn

# 或真机 ARM 设备
./pwn
```

## 评价

PBCTF 2021 ARM CPU 题速查，文章内容较少。

适合研究 ARM 架构 + 嵌入式安全的研究者。
