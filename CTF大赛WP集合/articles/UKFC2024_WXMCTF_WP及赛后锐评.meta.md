---
title: UKFC2024 WXMCTF WP及赛后锐评
contest: WXMCTF 2024 (UKFC2024)
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [string_decode, hex_extract, sha512_bruteforce, pikalang, ret2win, ret2libc, fmt_string, ret2shellcode, format_loss]
attack_chain: grep 文件批量读出二进制 → ASCII 还原 "Eightfold Battle Formation" → Wireshark 导出 16 进制流重组文件 → sha512 等值爆破 number → 32-bit ret2win/ret2libc/64-bit fmt-string+heap leak+environ+stack leak → pikalang esolang 解释执行
key_payload: wxmctf{Eightfold_Battle_Formation} / wxmctf{4nd_h1s_n4me_1s!!!!!!!} / b'a'*0x28+p32(backdoor) / payload = b'1'*0x20+p64(addr)
one_liner: 严重格式损失的 WXMCTF 题目集锦，但能拼出八阵图/JC/JWT 加密 Python 谜题 + 三档 pwn + 皮卡丘语言。
lesson: 当原文是 .docx 转 .md 时代码块缩进会全丢，整理 WP 时必须用 `code block fence` 包裹原始可读内容。
quality: low
---
