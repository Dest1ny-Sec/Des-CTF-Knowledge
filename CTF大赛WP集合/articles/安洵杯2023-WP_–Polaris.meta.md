---
title: 安洵杯2023 WriteUp - Polaris战队(全方向10+题)
contest: 安洵杯2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [PHP代码注入, 反序列化, 嵌套Luck, 1位翻转p_bit, 1024bit, 32位爆破, CBC_Padding_Oracle, SROP, ORW, 侧信道爆破flag, mprotect_RWX, 仿射替换, RC4, 魔改Base64, 魔改TEA, shld双精度左移, 魔改SM4, S盒T盒]
attack_chain: Web1 lambda_36:include+eval一句话 → Web2 Luck嵌套You→Luck→Luck→md5=phpinfo → Cr1 010101:p1 1024位中1个1被改0,遍历p1中0位改1试isPrime → Cr2 POA:CBC_Padding_Oracle从尾到头逐字节爆破 → Cr3 Rabin:e1=2/e2=5/x=8,Rabin解密c1,RSA解c2 → Misc1 SSTV:Misc2 jpg末尾hex+pngcheck+jphide → Pwn1 side-channel:SROP+mprotect+orw+bss shellcode+side-channel爆破flag(单字符cmp卡住) → Pwn2 seccomp:SROP+open/read/write ./flag → Re1 mobliego:查表替换 → Re2:RC4+魔改Base64按位还原 → Re3 牢大:TEA解密delta=0x9E3779B9 → Re4 你好PE:patch nop+shld双精度左移逆运算 → Re5 蓝色小鲸鱼:魔改SM4按字节查找T表
key_payload: SROP(rax=10 mprotect)+ORW+side-channel爆破 + 仿射表替换 + shld逆运算 + 魔改SM4 S盒T盒
one_liner: Polaris安洵杯2023全方向10+题WEB/MISC/CRYPTO/PWN/REVERSE综合。
lesson: 1位翻转密文用1024次isPrime爆破;Padding Oracle从尾到头逐字节cmp;侧信道爆破:用SROP+orw+cmp卡死循环卡时长(每字符1秒);SROP+leave_ret栈迁移+SROP+open/read/write;PE patch nop绕过反调试+shld双精度左移;魔改SM4 S盒T盒按字节索引。
quality: high
---
