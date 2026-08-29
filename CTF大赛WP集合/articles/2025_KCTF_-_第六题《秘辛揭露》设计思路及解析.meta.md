---
title: 2025 KCTF 第六题《秘辛揭露》设计思路及解析（易语言重载混淆+RC4 KSA 流密码）
contest: 2025 KCTF
year: 2025
difficulty: hard
vuln_type: [reverse]
tags: [KCTF 2025 第六题 秘辛揭露, 易语言内核特征检测, 重载与编译混淆, IDA 反编译器崩溃, 自定义调用约定, tools/link.ini obj 静态编译, sub_123540D0 xor 0BADF00D+0CAFEBABE, RC4 KSA 流密码, 32 位 4 字节一组异或, 水泊梁山战队 zZhouQing 0xchang 寞叶_]
attack_chain:
  - 易语言 tools/link.ini 配置后静态编译生成 obj 拖入 IDA
  - 识别易语言符号 → 反编译自定义调用约定
  - 函数 sub_123540D0：xor edx, 0BADF00D / xor ecx, 0CAFEBABE / xor eax, eax / or ecx, edx / setnz al / retn
  - 32 位 4 字节一组分 8 组，4B 0C 54 0F 32 00 02 35 异或
  - 内部 RC4 KSA 调度算法 + 复杂位运算（xor/and/<<</>>）
  - 动态调试 sub_123532A6 call sub_12353BC0 截获 xor 操作
key_payload: "xor edx, 0BADF00D; xor ecx, 0CAFEBABE; or ecx, edx; setnz al"
one_liner: 2025 KCTF 第六题 秘辛揭露：易语言内核特征检测 + 重载编译混淆 + RC4 KSA 流密码；自定义调用约定+ IDA 崩溃点+ 动态调试。
lesson: 易语言逆向需要 tools/link.ini 重新编译生成 obj → IDA 看易语言符号；水泊梁山战队（zZhouQing/0xchang/寞叶_）出题，2024 也出过 KCTF 水泊梁山反混淆题。
quality: high
---

# 2025 KCTF 第六题《秘辛揭露》设计思路及解析

## KCTF 评委团队点评

> 题目结合易语言内核特征检测、重载与编译混淆，既考验选手对易语言底层实现的逆向功底，又通过 IDA 反编译器崩溃点与自定义调用约定增加干扰，成功解题需耐心动态调试、算法逆向和脚本编写，适合中高阶 CTF 选手挑战。

## 设计思路

出题战队：水泊梁山（zZhouQing、0xchang、寞叶_）

修改好 `tools/link.ini` 文件后，再次静态编译，此时程序的生成目录下会产生 obj 文件，将其拖入 IDA 即可开始分析易语言的符号。

## 赛题解析

```asm
.text:123540D0 sub_123540D0    proc near
.text:123540D0                 xor     edx, 0BADF00Dh
.text:123540D6                 xor     ecx, 0CAFEBABEh
.text:123540DC                 xor     eax, eax
.text:123540DE                 or      ecx, edx
.text:123540E0                 setnz   al
.text:123540E3                 retn
.text:123540E3 sub_123540D0    endp

00 1D 3B 29 70 12 69 B7 6C 0F 4D 5C 9F 5B 6C 1B
B5 47 A2 28 C0 F8 DC E0 7A F8 D6 28 F6 F8 93 B3
```

## 自定义调用约定函数

- `sub_123540D0`：xor/and/&lt;&lt;/&gt;&gt; 运算  
- `sub_12353BC0`：`fmod` 浮点数取模运算  
- 上述运算会通过 `sub_12353BC0` 传入函数指针和参数主动调用

## 输入

- `a1`：指向长度为 32 字节的明文或密文数据  
- `a2`：指向另一块数据，可能是密钥 (Key) 或初始化向量 (IV)

## 算法流程

1. **初始化** (Key/IV Setup)：利用输入 `a2` 和内部固定的常量，通过一个极其复杂的、类似 RC4 KSA 的调度算法，生成一个内部状态（S 盒）  
2. **密钥流生成** (Keystream Generation)：基于初始化后的内部状态，生成用于加密/解密的伪随机密钥流  
3. **加解密** (Encryption/Decryption)：将输入 `a1` 的数据与生成的密钥流，通过一系列复杂的位运算（异或、与、移位）进行结合，生成最终的输出

## 调试技巧

断在 `0x123532A6 call sub_12353BC0`，这里是 **xor 操作**，会对 32 位输入四位一组分为八组，每组第一个字节共八个，跟参数二的八位字节 `4B 0C 54 0F 32 00 02 35` 依次异或。
