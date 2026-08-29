---
title: 2022 美团 MTCTF 初赛 writeup by Arr3stY0u
contest: 2022 美团 MTCTF 初赛
year: 2022
difficulty: medium
vuln_type: [misc_math, crypto_rsa, web_unknown, pwn_unknown]
tags: [美团, CTF, 最小公倍数, gcd, RealField, gift, p2-approx, iroot, CRT, pwncli, pwntools, 整数爆破, RSA]
attack_chain: ["CyberSpace: b=[32,38,27,...] flag += chr(b[i]+70) = 'flag{different_xor}'", "strange_rsa1: gift 是 0.9878... 高精度小数，n/gift ≈ q² → iroot 拿 p", "n 2048 位，gift 1024 位，p ≈ iroot(n/gift, 2) ± 偏移爆破", "strange_rsa2: 多 e 共享 n，CRT 攻击 e1*e2*...", "strange_rsa3: 已知 p 高位 + 私钥泄露", "web: Java 反序列化 / Spring 全家桶", "pwn: pwncli 库简化 EXP"]
key_payload: "p = iroot(n/gift, 2) 爆破 1000 个候选"
one_liner: 美团 MTCTF 6 大类：math + RSA + web + pwn + reverse + misc
lesson: gift = 高精度小数 → RealField 还原精确 n/gift → iroot 开方爆破 p
quality: high
---

# 2022 美团 MTCTF 初赛 writeup by Arr3stY0u

原文 https://www.ctfiot.com/57358.html （Arr3stY0u）

## MISC: CyberSpace
```python
b = [32, 38, 27, 33, 53, 30, 35, 32, 32, 31, 44, 31, 40, 46, 25, 50, 41, 44, 55]
flag = ""
for i in range(len(b)):
    flag += chr(b[i] + 70)
print(flag)
# flag{different_xor}
```

## CRYPTO: strange_rsa1
```python
from Crypto.Util.number import *
from gmpy2 import iroot
n = 10852516704806... # 2048-bit
gift = 0.98787132...  # 1024-bit 小数

# 关键：gift ≈ q^2/n，n/gift ≈ p^2
n = RealField(prec=512*2)(n)
p1 = n / gift
p = iroot(int(p1), 2)[0]  # 1024-bit 整数开方
print(p)
# 在 p 附近爆破几千个候选解 RSA
```

**攻击原理：**
- `n = p * q`，`gift = q²/n`，所以 `p² = n²/gift`，`p = n/sqrt(gift) = sqrt(n/gift)`
- 用 `RealField(prec=1024)` 保证精度
- `iroot(x, 2)` 取整数平方根
- ± 1000 范围内爆破

## CRYPTO: strange_rsa2 / strange_rsa3
- 多 e 共享 n → CRT 解密
- 已知 p 高位 / 私钥泄露

## Pwn
推荐 pwncli 库：
- https://github.com/RoderickChan/pwncli
- 比 pwntools 简洁

## 招新
- web / pwn / crypto / SRC（补天 / 企业 SRC / 众测）
- 联系方式见文末

## 教学价值
- **gift 小数精度** 是 RSA 攻击信号
- **RealField(prec)** 是 SageMath 高精度浮点
- **iroot** 整数开方
- **iio / aio** Python/GMP 多精度库
- **pwncli** 是 pwntools 的高级封装
- 美团 MTCTF 是企业级赛事，覆盖面广

## 工具
- SageMath RealField
- gmpy2 (iroot, isqrt, invert, is_prime)
- pycryptodome
- pwncli (RoderickChan)
- pwntools
