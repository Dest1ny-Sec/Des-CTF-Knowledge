---
title: DASCTF六月赛·二进制专项官方WP
contest: DASCTF六月赛·二进制专项
year: 2023
difficulty: hard
vuln_type: reverse
tags: [Go逆向, Finger插件, RSA_e=0x10001, Yafu分解, pycdc解包, XXTEA, 线程注入, RC4, 花指令去除, gethostbyname内联HOOK, Wireshark_DNS, 截屏加密, 易语言, _STARTUPINFO, CreateProcess]
attack_chain: unsym:Go逆向+Finger恢复大整数函数+e=0x10001确认RSA+Yafu分解N得p1*p2+Key解密文件+修复PE结构 → ez_exe:pycdc解包+key解密bin2+XXTEA逆运算 → babyRe:动态调试恢复API符号+线程注入资源shellcode+反调试+RC4解密+IDA64分析+去花指令 → careful:gethostbyname内联HOOK步入分析+Wireshark DNS协议分析 → cap:逆向截屏软件加密算法+写exp解密
key_payload: Finger插件 + e=0x10001 + Yafu分解69位整数 + pycdc + XXTEA + RC4 + DNS内联HOOK
one_liner: DASCTF六月赛二进制专项5题官方WP:Go RSA/pycdc XXTEA/线程注入RC4/gethostbyname内联HOOK/截屏加密。
lesson: Go逆向用Finger插件恢复关键函数;e=0x10001直接推测RSA;Yafu分解N得p1*p2=796192737278561537484199099160091818919833721026691718207595201542597→35位+35位素数;pycdc解包exe;线程注入资源shellcode绕过反调试;gethostbyname内联HOOK可Wireshark旁路DNS协议。
quality: high
---
