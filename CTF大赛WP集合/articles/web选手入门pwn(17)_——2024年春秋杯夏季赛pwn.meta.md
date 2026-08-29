---
title: web选手入门pwn(17) 2024春秋杯夏季赛pwn
contest: 春秋杯
year: 2024
difficulty: easy
vuln_type: rop
tags: [ret2libc, stack-overflow, ret2vuln-loop, 整数溢出, prng爆破]
attack_chain: 题目1循环ret2vuln+extend堆喷对齐栈帧触发printf泄libc+ret2libc / 题目2password=base64(this is password)登录+length=-1整数下溢触发gets→覆盖saved RBP+返回地址
key_payload: 题目2 length=-1 整数下溢 + payload A*104 + p64(pop_rdi_ret) + p64(binsh) + p64(system) 覆盖PRNG栈槽
one_liner: 春秋杯两题入门ROP，覆盖ret2vuln循环喷射+整数下溢gets覆盖的经典入门路径。
lesson: length字段使用int32比较但调用gets时无符号，length=-1溢出为最大正值绕过长度检查；ret2vuln+extend操作本质是栈空间对齐+控制字刷新printf参数。
quality: high
---

# web选手入门pwn(17) 2024 春秋杯夏季赛 pwn

## 概览
两题常规入门 PWN 复盘，覆盖 ret2vuln 循环喷射 + 整数下溢 gets 覆盖两个典型路径。

## 题目1: 简单栈溢出循环利用
- 漏洞：vuln 函数 `read(0, buf, n)` 中 n 由外部输入但 read 调用 buf 长度固定
- 利用：
  - `payload = A*88 + p64(vuln)` 第一次触发回到 vuln 循环
  - 第二次 `B*40 + p64(pop_rdi) + p64(got_puts) + p64(puts_plt) + p64(vuln)` 泄 puts GOT → libc
  - 通过 `extend` 函数（21 次）让栈布局对齐以满足 printf/puts 调用
  - 第三次发 system(/bin/sh) payload 完成 ROP
- 关键 gadget：`pop_rdi_ret = 0x4013d3`，`pop_rsi_r15_ret = 0x4013d1`，`pop_rdx_r12_ret = 0x11c1e1 (libc)`
- 收获：extend 函数实际上是在栈上做"对齐喷"，让多次 read 后 printf 时栈能命中之前填入的 canary 段

## 题目2: 整数下溢 + gets 覆盖
- 登录：`dGhpcyBpcyBwYXNzd29yZA==`（base64 of "this is password"），由原文直接给出
- 漏洞：choice 3 输入 `length: -1` → 内层 length 字段是有符号 int 但传给 `gets(buf)` 的实际可用空间按无符号理解 = 0xFFFFFFFF
- 利用：
  - length=-1 触发 gets 无界读，覆盖栈上 saved RBP / saved RIP / PRNG 状态
  - 第一次 `payload = A*72` 覆盖至 printf 后续要读的栈区域，让 printf 误读邻近地址 → 泄 text base（text_1297 = u64(recv[-9:-3]+b"\x00\x00") - 0x1297）
  - 第二次 `payload = A*104 + pop_rdi(puts_got) + puts_plt + bio_fun` 泄 libc
  - 第三次 `payload = A*104 + ret + pop_rdi(binsh) + system` 收壳
- 收获：长度字段用 int 32 但 read/gets 是 size_t 的代码经常出现 `-1 → MAX` 整数下溢漏洞
