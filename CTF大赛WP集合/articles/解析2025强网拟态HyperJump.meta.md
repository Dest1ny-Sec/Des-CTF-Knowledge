---
title: 解析2025强网拟态HyperJump
contest: 强网拟态 2025 HyperJump
year: 2025
difficulty: hard
vuln_type: reverse
tags: [custom-vm, password-verify, char-by-char, r15-index, ROP-style-attack, brute-force, O-n-m-complexity, SSE-instructions, movd, punpckldq, PIE-stripped]
attack_chain:
- 自定义VM程序,口令验证机制
- 题目提示:"最复杂的迷宫也有它的规律"
- 64位ELF+PIE+stripped
- 反反调试:修改ptrace返回值/Patch掉反调试代码
- 关键特征:查找表访问+XOR/ROL/ROR位运算+SSE指令(movd/punpckldq)
- 最终比较:计算结果与0x5420+r15处预期值比较
- r15:验证到第几个字符的索引
- 24字符逐位验证,某字符错误立即返回
- 攻击:patch程序,让返回码=r15当前索引值
- "mov eax, 0x1" (5字节:b8 01 00 00 00) → "mov eax, r15d" (3字节:44 89 f8) + 2字节NOP
- 枚举每位置所有可能字符(0-9 a-z A-Z符号),观察返回码
- 返回码最大者=该位置正确字符
- 复杂度:O(n*m)=24*95=2280次
key_payload: mov eax, r15d (3字节patch)
one_liner: 强网拟态2025 HyperJump自定义VM口令验证,24字符逐位+查找表+XOR/ROL/ROR+SSE指令+patch返回码为r15索引(3字节patch替代5字节mov eax, 0x1)+贪心爆破。
lesson: 自定义VM口令验证的爆破关键:让程序返回"已验证字符数"作为侧信道;r15作为索引寄存器的patch技术(短指令+NOP)是密码学CTF常用技巧。
quality: high
---

## 题目列表

1道Reverse:HyperJump自定义VM口令验证

## 关键考点

### 题目特征
- 64位ELF+PIE+stripped
- 自定义VM+口令验证
- 题目提示:"最复杂的迷宫也有它的规律"

### 反反调试
- 修改ptrace返回值
- Patch掉反调试代码
- 纯静态分析

### 关键指令
- 查找表访问:从预设数据表读取值
- 多种位运算:XOR/ROL/ROR
- SIMD指令:SSE(movd/punpckldq)

### 验证逻辑
- r15:当前验证到第几个字符
- 24字符逐位验证,某字符错误立即返回
- 最终比较:计算结果与0x5420+r15处预期值比较
- 全部通过则打印成功消息,返回0
- 失败则打印"Nope, try again.",返回1

### Patch技术(短指令+NOP)
- 原始:`mov eax, 0x1` (5字节: b8 01 00 00 00)
- Patch:`mov eax, r15d` (3字节: 44 89 f8) + 2字节NOP
- 让程序返回"当前验证字符索引"作为侧信道

### 攻击算法(贪心)
- 枚举每位置所有可能字符(0-9 a-z A-Z符号)
- 观察返回码(r15值)
- 返回码最大者=该位置正确字符
- 重复24次找到完整flag

### 复杂度
- 时间复杂度:O(n*m)=24*95=2280次
- 实际情况:验证可能跳跃,可能更快

### 返回码示例
- 第1个字符'f'正确 → 返回码从0变为1
- 前2个字符"fl"正确 → 返回码变为3
- 前4个字符"flag"正确 → 返回码为4
- 前5个字符"flag{"正确 → 返回码为5

## 实战价值
- 自定义VM口令验证的爆破关键:让程序返回"已验证字符数"作为侧信道
- r15作为索引寄存器的patch技术(短指令+NOP)是密码学CTF常用技巧
- 贪心算法+穷举是逐位爆破的标准方法
- 静态分析中位数编码的熟悉(REX前缀+ModR/M字节)是必备基础
- "程序自检测代码段hash"是防patch的标准防御
