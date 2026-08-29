---
title: pem 类文件解析及 2022 蓝帽杯 crypto 详解
contest: 蓝帽杯
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags: [pem, rsa, openssl, asn1, der, public-key, private-key, pfx]
attack_chain:
  - PEM 文件 base64 + 头尾标记
  - 解析 n/e/d/p/q/u 6 个参数
  - RSA.construct 重建密钥
  - 已知 p, q 算 phi 求 d
  - 用公钥加密 + 私钥解密
key_payload: PEM 解析 + RSA 参数构造
one_liner: 2022 蓝帽杯 PEM 文件 RSA 密码学详解。
lesson: PEM 文件本质是 base64 编码的 ASN.1 DER 序列，含 6 个 RSA 参数。
quality: medium
---

PEM 文件解析 + 2022 蓝帽杯 crypto 详解（来源 ctfiot）。

**PEM 文件基础**

PEM = Privacy-Enhanced Mail，常用于数字证书。文件形式：
- base64 编码的二进制
- 头尾标记：
  - 公钥：`-----BEGIN PUBLIC KEY-----` / `-----END PUBLIC KEY-----`
  - 私钥：`-----BEGIN RSA PRIVATE KEY-----` / `-----END RSA PRIVATE KEY-----`
  - 证书：`-----BEGIN CERTIFICATE-----` / `-----END CERTIFICATE-----`

**生成 RSA 密钥（Python）**
```python
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

# 公钥
p, q = getPrime(512), getPrime(512)
n = p * q
e = 0x10001
pub = RSA.construct((n, e))
with open('out.pem', 'wb') as f:
    f.write(pub.exportKey('PEM'))

# 私钥
d = inverse(e, (p-1)*(q-1))
priv = RSA.construct((n, e, d, p, q))
with open('priv.pem', 'wb') as f:
    f.write(priv.exportKey('PEM'))

# 自动生成
key = RSA.generate(1024)  # bits >= 1024
with open('out.pem', 'wb') as f:
    f.write(key.exportKey('PEM'))
```

**PEM 包含的 6 个参数**：
- n：模数
- e：公钥指数
- d：私钥指数
- p, q：大素数
- u = p^(-1) mod q（CRT 优化用）

**openssl 命令**
```bash
# 从 PEM 提取参数
openssl rsa -in private.pem -text -noout
# 解析出 n, e, d, p, q
```

**CTF 应用**：
1. 给定 PEM 私钥 → 提取 n, e, d
2. 给定密文 → `pow(c, d, n)` 解密
3. 给定 PEM 公钥 → 提取 n, e，弱密钥分解 p, q

适合作为"PEM 文件 + RSA 参数提取"教学案例。
