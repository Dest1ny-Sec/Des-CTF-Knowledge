---
title: 强网杯2024 solve2-apk 赛题解析 - TEA+Twofish+RS_MDS
contest: 强网杯2024
year: 2024
difficulty: hard
vuln_type: reverse
tags: [Android_Apk, JNI, TEA解密, Twofish, RS_MDS_Encode, Reed_Solomon, GF(256), 字节序转换, 异或拼接, key_material, AES_S-box, Aar0n]
attack_chain: C++还原:TEA 32轮 delta=0x9e3779b9 sum=0xC6EF3720 4 key → switchEndian字节序转换 → 字符串拼接part1 → Java:RS_MDS_Encode用Reed-Solomon(12,8) over GF(256)产生AES S-box → Twofish(key=000102030405060708090a0b0c0d0e0f).decrypt(data1) → 异或data2^enc1^enc2=part2 → flag{iT3N0t7H@tH@E6D0YOV7hInkS0}
key_payload: TEA+switchEndian + Twofish+RS_MDS_Encode + 异或拼接
one_liner: 强网杯2024 solve2 apk:TEA+字节序+Twofish RS_MDS_Encode(Reed-Solomon)+异或拼接三段flag。
lesson: APK逆向需结合Java层RS_MDS_Encode(GF(256) Reed-Solomon)+C++层TEA+switchEndian字节序;Twofish密钥=000102030405060708090a0b0c0d0e0f;flag分段拼接part1+part2;RS_MDS_Encode 4字节rem+4字节rem+2次循环。
quality: high
---
