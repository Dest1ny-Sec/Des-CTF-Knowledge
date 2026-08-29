---
title: 强网杯2025 PolyEncryption - Vibe Reing的胜利 (看雪SleepAlone)
contest: 强网杯2025
year: 2025
difficulty: hard
vuln_type: reverse
tags: [PolyEncryption, dotnet, polyencrypt.dll, saw.py, Hack.java, AI辅助, 白盒AES, S-box, ShiftRows, MixColumns, AddRoundKey, 22轮, Sbox+MixCols交错, dotnet反编译, AES密钥编排, SleepAlone]
attack_chain: 静态分析dotnet polyencrypt.dll → 找到saw.py/Hack.java关键模块 → AI推理数据流(明文abe74e3a9c375b3428bf31d1f8fa49c1→逆序处理→小端→AES风格加密) → Patch saw.py/Hack.java绕过混淆/反调试 → Debug docker日志敲定细节 → 纯Python实现PolyEnc 22轮(奇数轮SubBytes+MixColumns,偶数轮ShiftRows+AddRoundKey) → 加解密验证 → 解密flag.enc
key_payload: 22轮 PolyEnc(奇数SubBytes+MixColumns,偶数ShiftRows+AddRoundKey) + 密钥级联(A'=A^sbox(rol(D,8))^round_key) + 逆MixColumns[0x0E,0x0B,0x0D,0x09]
one_liner: 强网杯2025 PolyEncryption:AI辅助+dotnet反编译+saw.py Hack.java patch+22轮AES风格PolyEnc纯Python实现。
lesson: AI辅助逆向+手动验证+patch关键模块;dotnet polyencrypt.dll分析策略:先看saw.py/Hack.java逻辑再Patch;PolyEnc 22轮用奇数轮SubBytes+MixColumns+偶数轮ShiftRows+AddRoundKey;密钥级联s[1]=A^sbox(rol(D,8))^round_key;逆MixColumns矩阵[0x0E,0x0B,0x0D,0x009];逆向流程:Round 22→Round 1(偶数→逆AddRoundKey+逆ShiftRows;奇数→逆MixColumns+逆SubBytes)。
quality: high
---
