---
title: inctf Forensic 复现 | Memlabs（下）
contest: inctf
year: 2019
difficulty: medium
vuln_type: forensic_memory
tags: [memory-forensics, volatility, mega-drive-key, strings, lab6]
attack_chain:
  - Lab6: 内存中搜 "Mega Drive Key"
  - strings 提相关 key
  - 后续还原
key_payload: strings 搜特殊字符串
one_liner: inctf Memlabs Lab 4-6 复现（下），volatility + strings 提取 Mega Drive Key。
lesson: 内存取证常用 `strings` + 关键字符串作为快速定位线索。
quality: medium
---

inctf Memlabs Lab 4-6 复现（下半部分，来源 ctfiot）。

**Lab6 关键步骤**：
> The names were not readable. They were composed of alphabets and numbers but I wasn't able to make out what exactly it was.
> 
> `strings Lab6.raw | grep "Mega Drive Key"`

在内存文件中用 strings 搜特殊字符串 "Mega Drive Key" 定位关键数据。

**内存取证常用 strings 关键词**：
- "Mega Drive Key"
- "flag{", "CTF{", "idek{" 等 flag 格式
- "password", "secret", "token"
- 文件路径 / 进程名

适合作为内存取证"线索搜索"工具集锦。
