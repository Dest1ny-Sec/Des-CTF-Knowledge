---
title: 2022 年第三届电信和互联网行业职业技能竞赛 WriteUp
contest: 2022 电信/互联网行业职业技能竞赛
year: 2022
difficulty: medium
vuln_type: [sqli, deserialize, reverse, crypto_rsa, web_unknown, misc_unknown]
tags: [职业技能竞赛, xor-0x70, flag-reverse, SilentEye, binwalk, crc-collision, ddddocr, SQL-异或注入, 费马小定理, 临时密钥重用]
attack_chain: ["PWN: 内联库函数, 调试器找 flag (无原文代码)", "Reverse: 输入反转 + XOR 0x70 → 反转后 xor 0x70 还原", "MISC 1: 1 进入 calc, print(eval(line)) 直接拿 key", "MISC 2: __import__('os').popen('cat flag').read()", "MISC 3: binwalk jpg → zip → CRC 碰撞密码 ohhhh_you_found_me → 解压 → base64 → 图片 SilentEye → flag", "WEB func.php: ddddocr 识别验证码 + 异或 SQL 注入 1'^(ascii(substr(database(),{0},1))={1})^'1, 过滤 select, 改查 code 字段", "WEB EzPop: POP 链构造", "WEB 超级马里奥: js 藏 flag 路径", "Crypto: 爆破 X0=4/5 → 恢复 key → 解密第一段 → 作 key 解密第二段", "Crypto old_rsa: 费马小定理分解 modulus = s, p,q 关系 n/s 开根, 解 rsa"]
key_payload: "1'^(ascii(substr(database(),{0},1))={1})^'1"
one_liner: 2022 电信职业技能赛：xor 0x70 + binwalk + CRC 碰撞 + ddddocr SQL 异或 + RSA
lesson: 异或 SQL 注入绕过关键字是经典；CRC 碰撞短文件名密码是 misc 入门；费马小定理分解 RSA
quality: high
---

# 2022 第三届电信/互联网行业职业技能竞赛 WriteUp

原文 https://www.ctfiot.com/61661.html

## Pwn
- 内联库函数, 调试器找 flag

## Reverse
```python
# 输入 123123123
# 反转成 321321321
# XOR 0x70
# 找 buffer 地址 0xb966f0
flag_bytes = bytes([b ^ 0x70 for b in buffer])
```
- 输入反转 + XOR 0x70

## Misc

### calc 拿 key
```python
# 1. 没有 key 长度限制
# 输入 1 → print(eval(line)) → 拿 key 实际值
```

### 命令执行
```python
__import__('os').popen('cat flag').read()
```

### jpg + zip
```bash
1. binwalk 分离 jpg → zip
2. CRC 碰撞 → 密码 ohhhh_you_found_me
3. 解压 → base64 → SilentEye → flag
```

## Web

### func.php SQL 注入
- ddddocr 识别验证码
- 异或注入：`1'^(ascii(substr(database(),{0},1))={1})^'1`
- 绕过 select 过滤
- 试 code 字段得 flag

### EzPop
- POP 链构造

### 超级马里奥
- js 藏 flag 路径 → 访问解码

## Crypto

### 临时密钥重用
- 爆破 X0 = 4 或 5
- 恢复 key
- 解密第一段 → 作 key 解密第二段
- 拿完整 flag

### old_rsa
- 费马小定理分解 modulus = s
- p,q 关系 → n/s 开根
- 解 RSA

## 教学价值
- **异或 SQL 注入** 绕过关键字是 CTF 经典
- **CRC 碰撞** 短文件密码是 misc 入门
- **binwalk** 分离文件
- **SilentEye** 音频隐写
- **ddddocr** 验证码 OCR
- **费马小定理** 分解 RSA
- **临时密钥重用** 解多段密文

## 工具
- binwalk
- ddddocr
- SilentEye
- crc32 碰撞脚本
- IDA / x64dbg

## 关联
- 电信职业技能赛 = 信安员国赛
- 涵盖全面：PWN / Reverse / MISC / WEB / CRYPTO
