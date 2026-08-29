---
title: 0xGame 2025/Crypto WriteUp Week1
contest: 0xGame
year: 2025
difficulty: easy
vuln_type:
- crypto_rsa
- diffie_hellman
- block_cipher
- vigenere
- web_qrcode
tags:
- 新人向
- factordb
- Vigenère 标准
- Vigenère 魔改乘法
- GB2312
- 三进制 base
- iroot(7) 整数根
- POW 爆破
- DH s=1 退化
attack_chain:
- 子题 1 流量登录：扫 QR 码填 6 位验证码
- 子题 2 DH 退化：设 Bob 公钥 B=1 → s=pow(1,a,p)=1 → 直接用 s=1 派生 AES key
- 子题 3 RSA factordb：n 256-bit 太小，直接 factordb 分解 p,q
- 子题 4 Vigenère 标准：已知 key "Welcome-2025-0xGame"，解密
- 子题 5 Vigenère 魔改乘法：((char_index + bias) * char_index) mod len → 逐位解二次同余
- 子题 6 flag 切 4 段：b64 + hex + 三进制 a/w/q + iroot(7) → 拼回 flag (gb2312)
- 子题 7 POW + 2025 位 RSA：4 字符前缀爆破 + d=inverse(e, n-1)
key_payload: "B = 1; s = 1  // DH 退化攻击"
one_liner: 7 个新人向 crypto 子题合集（DH s=1 / factordb / Vigenère 两种 / GB2312 三进制 iroot / POW + 2025 位 RSA）
lesson: DH 协议 s 值退化时（公钥=1）直接 s=1；factordb 是小指数 RSA 标准武器；Vigenère 乘法变种需逐位解二次同余；多段编码拼接时按段确认长度和编码
quality: high
---

# 0xGame 2025/Crypto WriteUp Week1

**7 个新人向 crypto 子题合集**

> 0xGame · 2025 · easy · crypto multi · quality=high
> 思路: 子题 1 流量登录：扫 QR 码填 6 位验证码 → 子题 2 DH 退化：设 Bob 公钥 B=1 → s=pow(1,a,p)=1 → 直接用 s=1 派生 AES key → 子题 3 RSA factordb：n 256-bit 太小，直接 factordb 分解 p,q → 子题 4 Vigenère 标准：已知 key "Welcome-2025-0xGame"，解密 → 子题 5 Vigenère 魔改乘法：((char_index + bias) * char_index) mod len → 逐位解二次同余 → 子题 6 flag 切 4 段：b64 + hex + 三进制 a/w/q + iroot(7) → 拼回 flag (gb2312) → 子题 7 POW + 2025 位 RSA：4 字符前缀爆破 + d=inverse(e, n-1)
> 套路: DH 协议 s 值退化时（公钥=1）直接 s=1；factordb 是小指数 RSA 标准武器；Vigenère 乘法变种需逐位解二次同余；多段编码拼接时按段确认长度和编码

**关键 payload**:
```python
B = 1
s = 1  # DH 退化攻击
```
