---
title: 2023 年国家基地"楚慧杯"网络安全实践能力竞赛初赛 WriteUp
contest: 楚慧杯 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [哈希扩展攻击, sqlmap盲注, 栈溢出, TEA, zip套娃, RSA_Boneh-Durfee, 天权信安]
attack_chain:
  - WEB: 哈希扩展攻击伪造 password123 + 文件名 SQL 注入 + sqlmap 一把梭
  - PWN ez_base: shift+f12 找 flag.txt 字符串 + 0x28 字节溢出 + 0x404911 跳转后门
  - RE Babyre: 32 轮 TEA 加密 + delta=0x9E3779B9 + 4 个 key
  - MISC ez_zip: 压缩包套娃，Python 脚本循环解压
  - 8 位二进制 → 字符串 → DASCTF flag
  - CRYPTO so-large-e: Boneh-Durfee LLL 攻击大 e RSA
  - 用 RSA-and-LLL-attacks 库解 d
key_payload: 'pay = b"a"*0x28 + p64(0x404911)'
one_liner: 楚慧杯初赛：哈希扩展+sqlmap+栈溢出 0x28+TEA+zip 套娃+Boneh-Durfee 大 e RSA。
lesson: 大 e RSA 用 Boneh-Durfee LLL 攻击；TEA delta=0x9E3779B9 + sum>>11 取 key；栈溢出字节数要逐个试。
quality: medium
---

# 2023 年国家基地"楚慧杯"网络安全实践能力竞赛初赛 WriteUp

## 来源
- 原文：ctfiot.com/151842.html
- 团队：天权信安网络安全团队（第三名）

## 5 道题详解

### WEB
- **未具体题名**（哈希扩展攻击 + SQL 注入）
  - 哈希扩展攻击：已知 hash 和长度，伪造 password123
  - 文件名 SQL 注入（成功/不成功回显不同）
  - 盲注 + sqlmap 一把梭

### PWN
1. **ez_base**（栈溢出 + 后门地址）
   - shift+f12 找 flag.txt 字符串
   - 0x28 字节垃圾数据 + 返回地址 0x404911
   - payload: `b'a' * 0x28 + p64(0x404911)`

### REVERSE
2. **Babyre**（TEA 32 轮）
   - delta=0x9E3779B9
   - 4 个 key: 0xDEADBEEF, 0x87654321, 0xFACEB00C, 0xCAFEBABE
   - sum >> 11 取 key 索引
   - 直接抄 decipher 函数

### MISC
3. **ez_zip**（zip 套娃）
   - Python 脚本循环解压 zip
   - 8 位二进制字符串 → chr 转换
   - 还原 flag: `DASCTF{10c58258ccf1e7c631e5911ed6acc4ed}`

### CRYPTO
4. **so-large-e**（大 e RSA + Boneh-Durfee LLL）
   - e 长度很大（> n/4）
   - https://github.com/Gao-Chuan/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage
   - 解 d = 663822343397699728953336968317794118491145998032244266550694156830036498673227937
   - pow(c, d, n) 还原 flag: `DASCTF{6f4fadce-5378-d17f-3c2d-2e064db4af19}`

## 关键技巧
- **哈希扩展攻击**：已知 hash 扩展任意长度
- **SQL 注入回显差异**：成功/不成功回显不同做盲注
- **栈溢出字节数**：0x28 逐字节试
- **TEA 变种**：sum>>11 索引 key
- **zip 套娃**：Python zipfile 循环解压
- **Boneh-Durfee**：大 e RSA 攻击

## 适用场景
- 哈希扩展攻击
- SQL 盲注
- 栈溢出入门
- TEA 32 轮
- 大 e RSA 攻击
