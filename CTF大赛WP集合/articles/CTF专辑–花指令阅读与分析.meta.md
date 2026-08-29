---
title: CTF 专辑 – 花指令阅读与分析
contest: CTF Reverse
year: 2024
difficulty: medium
vuln_type: reverse
tags: [花指令, JunkCode, 等价替换, 抵消型, jmp db型, 间接赋值, IDA LinearSweep, Recursive Traversal, OllyDbg, 算数拆分, 栈平衡, call+5取eip]
attack_chain:
  - JunkCode: mov eax,eax; jmp rva=0; xor eax,0
  - 算数拆分: add eax,5 → add eax,2; add eax,1; inc eax; inc eax
  - shl eax,5 → shl eax,3; shl eax,1; shl eax,1
  - 等价解释: push 0x11111 ≡ sub esp,4; mov [esp],0x11111
  - retn 0x5 ≡ mov eip,[esp]; add esp,4+5
  - enter 8,0 ≡ push ebp; mov ebp,esp; sub esp,8
  - 抵消型: push-pop / add-sub / inc-dec / xor-xor
  - jmp db 型: EB 03 55 E8 AA → EB 03 jmp 跳过 55 E8 AA 数据
  - 条件跳转 jmp db: jz label0; jnz label1; label0: db 0E8h
  - 间接赋值: b=a, c=b → c=a (用于构造花指令)
  - IDA Linear Sweep 逐行反汇编, Recursive Traversal 按代码顺序
key_payload: 'JunkCode 算数拆分 / 等价解释 push pop retn / 抵消型 push-pop add-sub / jmp db EB 03 / 间接赋值 / IDA LinearSweep vs Recursive Traversal'
one_liner: 花指令阅读与分析 — JunkCode 算数拆分 + push/pop/retn 等价解释 + 抵消型 (add-sub/xor-xor) + jmp db 型 (EB 03 跳 55 E8 AA) + 间接赋值 + IDA LinearSweep vs Recursive Traversal 反汇编算法差异。
lesson: 花指令分 4 类:① 垃圾代码 ② 等价替换 ③ 抵消型 ④ jmp db 型;IDA LinearSweep 逐行 vs Recursive Traversal 按执行顺序;call+5 拿 eip 是经典 trick。
quality: high
---

# CTF 专辑 – 花指令阅读与分析

## 速读
花指令阅读与分析完整教程 — 4 类花指令 + 2 种反汇编算法。

## 4 类花指令

### ① JunkCode (垃圾代码)
```asm
mov eax, eax
xchg esp, esp
jmp rva=0
xor eax, 0
```

### ② 等价替换
| 原始 | 等价 |
|------|------|
| `push 0x11111` | `sub esp, 4; mov [esp], 0x11111` |
| `pop eax` | `mov eax, [esp]; add esp, 4` |
| `retn 0x5` | `mov eip, [esp]; add esp, 9` |
| `enter 8, 0` | `push ebp; mov ebp, esp; sub esp, 8` |
| `add eax, 5` | `add eax, 2; add eax, 1; inc eax; inc eax` |
| `shl eax, 5` | `shl eax, 3; shl eax, 1; shl eax, 1` |
| `and esp, 0xfffffff0` | (栈对齐) |

### ③ 抵消型
- `push eax; pop eax` (栈平衡)
- `add eax, 2; sub eax, 2` (运算抵消)
- `inc eax; dec eax` (加减 1)
- `xor eax, 2; xor eax, 2` (异或相同)
- `not eax; not eax` (取反两次)

### ④ jmp db 型
```asm
; 无条件跳转
004710D5  EB 03        jmp short 004710DA
004710D7  55           push ebp       ; IDA LinearSweep 误以为 0x55 是 push ebp 指令
004710D8  E8           db E8h
004710D9  AA           db AAh
004710DA  83 C0 02     add eax, 0x2

; 条件跳转
start:
    xor eax, eax
    test eax, eax
    jz label0
    jnz label1
label0:
    db 0E8h
label1:
    xor eax, 3
    add eax, 3
```

## 间接赋值
```c
b = a
c = b
// 即 c = a
```

## IDA 反汇编算法

| 算法 | 特点 |
|------|------|
| Linear Sweep | 逐行反汇编, 不区分代码/数据, 易被 jmp db 干扰 |
| Recursive Traversal | 按执行顺序, 遇到分支记录地址, 抗花指令 |

## call+5 取 eip
```asm
call $+5  ; 跳到下一行
pop eax   ; eax = 当前 call+5 后的地址
; eip = [esp] - 5 (call 指令自身长度)
```
