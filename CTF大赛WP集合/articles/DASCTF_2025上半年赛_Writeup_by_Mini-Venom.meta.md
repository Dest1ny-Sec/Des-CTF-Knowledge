---
title: DASCTF 2025 上半年赛 Writeup by Mini-Venom
contest: DASCTF
year: 2025
difficulty: medium
vuln_type: misc_math
tags: [obex, bluetooth, lsb-stego, openssl, rsa-key-recover, sm4, sm2, xianyu-fs]
attack_chain:
  - BlueTrace: tshark 提 OBEX 图片
  - 像素 hex 拼接
  - Webshell Plus: 提 RSA p,q 复私钥
  - openssl_decrypt AES-128
  - TCP 流找 /etc/shadow
  - hashcat 爆破 root 密码
  - Excessive Security: ECDSA r 复用恢复 sk
  - 多项式 GCD 攻击
  - xianyu_decrypt: SM4 解密
key_payload: OBEX 流量 + RSA 私钥恢复 + ECDSA nonce 复用
one_liner: DASCTF 2025 上半年赛 Mini-Venom 战队 WP，OBEX/RSA 复私钥/ECDSA 复用/SM4 文件系统解密。
lesson: 蓝牙 OBEX 协议 tshark `-Y obex.header.value.byte_sequence` 抓图片；RSA 私钥只要 p,q 可直接 cryptography 重构。
quality: high
---

DASCTF 2025 上半年赛 Mini-Venom 战队（ChaMd5）WP 集合。

**MISC: BlueTrace**
tshark 抓 pcapng 蓝牙 OBEX 流量：
```bash
tshark -r BlueTrace.pcapng -Y obex.header.value.byte_sequence -T fields -e obex.header.value.byte_sequence > 1.txt
```
得到 PC 名 `INFERNITYのPC` + 一张图片。Python PIL 提取像素 RGB 全相同 → 每像素 R 转 hex 拼接 → flag = `DASCTF{0ba687ee-60e0-4697-8f4c-42e9b81d2dc6}`。

**MISC: Webshell Plus**
冰蝎 webshell 但用 OpenSSL 加密。提 n=7867691643586180987785626545986251727789183377275546449400690071916592141728452581896381132002349573632855071606614201168751151435679435299890592299985167、e=65537；factor 找 p, q；用 `cryptography.hazmat.primitives.asymmetric.rsa` 构 RSAPrivateNumbers 复私钥 → openssl_decrypt AES-128 解密。TCP 32 流里找 `/etc/shadow` 结果，hashcat 爆破 root 密码 md5。

**CRYPTO: Excessive Security**
ECDSA 签名 (h1, s1, r1)/(h2, s2, r1) r 复用 → 联立方程：
- A1 = (r1 * s2) % n1
- B1 = (-r1 * s1) % n1
- C1 = (s1 * h2 - s2 * h1) % n1
- D1 = (A1 * B2 - A2 * B1) % n1
- x1 = (C1 * B2 - C2 * B1) * D1^(-1) % n1
- x2 = (A2 * C1 - A1 * C2) * D2^(-1) % n1
恢复 nonce x1, x2 → 恢复 d。

**Excessive Security: xianyu 闲鱼文件**
`xianyu_decrypt.load_and_decrypt_xianyu()` 解密自定义 XIANYUFS 文件格式；MASTER_KEY = `XianYuAESKey0000`；read_part1~5 + unpad 解析；解出 json：
```json
{"name": "梦梦A姬", "artist": "圆头🐱", "fl4g": "..."}
flag = "DASCTF{fl5h_mus1c_miao_m1a0_mlaO}"
```
