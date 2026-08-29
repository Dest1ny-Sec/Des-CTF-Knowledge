---
title: Wbaes：一次白盒密码逆向的实战之旅 (WHCTF 2017)
contest: WHCTF 2017 (Wani Hack)
year: 2017
difficulty: hard
vuln_type: block_cipher
tags: [white_box_aes, movfuscation, dfa_differential_fault_analysis, deadpool, phoenixaes, look_up_table, sigaction_anti_debug, t_box_aes, sigaction_stripped_elf, hxp_dfa]
attack_chain: file ELF 32 位 9.3 MB stripped + sigaction 反调试 + MOV 混淆 → DFA 注入尝试全部 NoFault（编译器优化防故障）→ 提取字符串 "Here is flag{%s}" → 已知 AES 实现（白盒 T-Box）→ 测试密钥 whctf&flappypig! 试解 16 字节密文块 → 遍历全文件 9770792 字节找 16 字节连续块可打印字符 ≥12 → 命中 0x003a8162 偏移解出 Whc7f&Fl@ppyp1g! → ./Wbaes "Whc7f&Fl@ppyp1g!" 输出 flag
key_payload: key = b'whctf&flappypig!' / ciphertext = 13cb006c2994de6da1b81ba399206290 / plaintext = Whc7f&Fl@ppyp1g! / 全文件遍历 16 字节 AES-ECB 解密筛可打印字符
one_liner: WHCTF 2017 Wbaes 9.3 MB MOV 混淆白盒 AES，DFA 失败后改用"已知密钥 + 文件全字节扫描可解 16 字节块"绕过白盒保护，flag: Whc7f&Fl@ppyp1g!。
lesson: 白盒 AES 攻击中"密钥已知 + 文件全字节扫描"是最直接的捷径；MOVfuscation 让 DFA 难以注入时，应该转向"字符串+猜测+文件扫描"的混合策略。
quality: high
---
