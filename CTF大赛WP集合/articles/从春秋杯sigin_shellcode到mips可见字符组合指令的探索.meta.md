---
title: 从春秋杯 sigin_shellcode 到 mips 可见字符组合指令的探索
contest: 春秋杯
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [MIPS-shellcode, printable-ASCII, R-type-I-type-J-type, opcode-fuzz, syscall-restriction, heterogeneous-PWN, sigin]
attack_chain:
  - MIPS 32 寄存器 ($0-$31) + HI/LO 特殊寄存器
  - 指令 32 位: R 型 (opcode=0) + I 型 (opcode+rs+rt+imm16) + J 型 (opcode+imm26)
  - 可见字符范围 [0x21, 0x7e]
  - R 型 opcode 必须是 0 → 不可见字符 → 不可用
  - J 型 fuzz 只剩 jalx (但需 microMIPS/MIPS16e 支持)
  - I 型可用: beqzl/beqz/bnezl/bnel/blezl/bgtzl/andi/slti
  - 没有 syscall 指令可用
  - 通用 MIPS 可见字符 shellcode 几乎不可能
  - sigin_shellcode 是异构 pwn 题, 让选手探索可见字符 MIPS shellcode
key_payload: 'mips 可见字符 shellcode 不存在 (无 syscall) + R/I/J 型指令 fuzz'
one_liner: 春秋杯 sigin_shellcode：探索 MIPS 可见字符组合指令，R 型 opcode=0 不可用 + J 型只有 jalx + 没有 syscall。
lesson: 通用 MIPS 可见字符 shellcode 几乎不可能（无 syscall 指令），异构 pwn 题设计思路。
quality: medium
---

# 从春秋杯 sigin_shellcode 到 mips 可见字符组合指令的探索

**来源**: ctfiot.com ID 119807
**作者**: 出题人 (2023 春秋杯春季赛)
**赛事**: 春秋杯春季赛 sigin_shellcode (异构 pwn)

## 出题想法
- 很多 shellcode 题目但从未见过通用的可见字符 mips_shellcode
- 借出题探索"为何通用可见字符 mips_shellcode 并不存在"

## MIPS 寄存器
- 32 个: `$0-$31` (别名 $zero, $at, $v0-$v1, $a0-$a3, $t0-$t9, $s0-$s7, $t8-$t9, $gp, $sp, $fp, $ra)
- 特殊: HI, LO (乘法除法结果)

## MIPS 指令格式
- **R 型**: opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + funct(6) = 32 bit
  - opcode 必须是 0 → 不可见字符 → **R 型完全不可用**
- **I 型**: opcode(6) + rs(5) + rt(5) + immediate(16)
- **J 型**: opcode(6) + address(26)

## 可见字符范围
- ASCII 可见字符 (不含空格): `[0x21, 0x7E]`

## 可用指令 fuzz
```python
import string
visible = [ord(c) for c in string.printable.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')]
# 范围: 0x21-0x7E
```

### I 型可用
- `beqzl` / `beqz` (rs == 0)
- `bnezl` / `bnel`
- `blezl` / `bgtzl`
- `andi` / `slti` (用于置零)

### J 型可用
- `jalx` (但需 microMIPS/MIPS16e 支持)

## 关键限制
- **没有 syscall 指令** → 通用 MIPS 可见字符 shellcode 几乎不可能
- 即使 andi/slti 能给 a0/a1 置零，仍无法完成系统调用

## 评价
2023 春秋杯春季赛 sigin_shellcode 异构 pwn 题。考察：
- MIPS 32 位指令编码
- 可见字符约束的指令可用性分析
- 异构 pwn (MIPS) shellcode 编写限制
- 出题探索 "为何不存在通用 MIPS 可见字符 shellcode"

是 MIPS 体系结构 + shellcode 约束研究的优秀案例。
