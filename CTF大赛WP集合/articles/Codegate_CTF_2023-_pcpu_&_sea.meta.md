---
title: Codegate CTF 2023: pcpu & sea
contest: Codegate CTF 2023
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags: [pwn, register-uaf, signed-cmp, AES-CBC, rop, libc-2.31, splice]
attack_chain:
  - pcpu: reg_list sleep(1)竞态UAF + alloc_list(3)复用释放buffer
  - 0x10000 list OOB read_reg_idx泄露其他寄存器
  - sea: signed/unsigned类型混淆 char last_byte+memcpy扩展长度
  - dec()栈溢出leak canary/libc/pie
  - AES-CBC+ROP execve(/bin/sh)
key_payload: prog=[alloc_list(0),alloc_list(1),copy_reg(0,1),write_reg0_idx(0,10),alloc_list(3),dump_regs()]
one_liner: Codegate 2023两道pwn：pcpu寄存器竞态UAF+sea signed混淆AES-CBC
lesson: sleep(1)竞态+register复用可OOB；signed/unsigned混淆可扩大memcpy长度
quality: high
---

# Codegate CTF 2023: pcpu & sea

## 题目信息
- 比赛：Codegate CTF 2023
- 题目：pcpu（寄存器 VM）+ sea（AES 加解密）
- 涉及库：libc-2.31

## 关键攻击链
### pcpu
1. `struct reg_list { uint64_t is_free; union { uint64_t rand_digit; uint8_t list[0x10000]; } }`
2. 0x16F0 函数：`v17 = (reg_list *)*registers; sleep(1u); v17->list[ptr->third_byte] = ptr->high_byte`
3. 利用：
   - `alloc_list(0)`, `alloc_list(1)` 双 buffer
   - `copy_reg(0,1)` 转移 x1→x0，x0 被释放
   - `write_reg0_idx(0,10)` 写已释放 buffer
   - `alloc_list(3)` 新分配复用释放内存
   - 78 次 `read_reg_idx(2,3,i)` + `dump_regs()` OOB 读出 flag

### sea
1. `(char)last_byte <= 16` signed 比较，`last_byte` 为负可绕过
2. `while (last_byte > i)` unsigned 比较，负数当成大正数
3. `v12 = len - (char)last_byte` signed 减法，负数让 v12 变大
4. `qmemcpy(dst, src, v12)` 复制超过原长度数据
5. 解法：`enc(b"A"*0x10 + b'\x80'*0x80)` → 加密栈数据 → leak canary/libc/pie
6. AES-CBC 构造 ropchain：`rdi=/bin/sh, rsi=0, rdx=0 → execve`

## 评分
- quality: high（两道 PWN 一道寄存器竞态 UAF + 一道符号混淆，给出完整 exp）
