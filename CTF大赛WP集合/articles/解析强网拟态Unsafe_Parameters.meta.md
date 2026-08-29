---
title: 解析强网拟态 Unsafe Parameters - 共享私钥指数 RSA 攻击
contest: 强网拟态
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags: [RSA-shared-d, LLL, lattice-attack, multi-prime-RSA, AES-ECB, SHA3-512, Hidden-Number-Problem, HNP, three-prime, 425-bit-d]
attack_chain:
  - 5 组 RSA 共享一个 425 位素数 d 作为私钥
  - 每组 n = p*q*r (3 × 512-bit primes) + e_i = d^(-1) mod φ(n_i)
  - 关键: e_i × d ≈ k_i × n_i (近似关系)
  - 构造 6×6 格矩阵:
    [M, e_0, e_1, e_2, e_3, e_4]
    [0, -n_0, 0, 0, 0, 0]
    [0, 0, -n_1, 0, 0, 0]
    [0, 0, 0, -n_2, 0, 0]
    [0, 0, 0, 0, -n_3, 0]
    [0, 0, 0, 0, 0, -n_4]
  - M = 2^1024 平衡常数
  - LLL 规约 → 短向量第一行 = (M*d, d*e_0-k_0*n_0, ...)
  - d = abs(Mat_LLL[3][0]) // M
  - 验证 d 比特长度 425 + isPrime(d)
  - 用 d 分解每个 n (g^t mod n 与 gcd 与 n 找因子)
  - 每组 p*q*r = n, 用 e*d-1 = k*φ(n) 找到 2^s*t
  - sum = Σ(p+q+r) over 5 组
  - AES-ECB key = sha3_512(str(sum).encode()).digest()[:16]
  - 解密 flag = flag{9b31dd3e-aa6a-4c4d-b796-bff4e4dfe0cc}
key_payload: '5 组共享 d + LLL 6×6 矩阵 + d 分解 n × 5 + SHA3-512[:16] AES-ECB'
one_liner: 强网拟态 2025 Unsafe Parameters：5 组 RSA 共享 d 触发 LLL 攻击，构造 6×6 矩阵恢复 d 分解模数解 AES。
lesson: 多组 RSA 共享私钥是致命漏洞；e×d ≈ k×n 近似关系 + LLL 短向量是经典攻击。
quality: high
---

# 解析强网拟态 Unsafe Parameters - 共享私钥指数 RSA 攻击

**来源**: ctfiot.com ID 277005

## 题目
```python
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import sha3_512
from secret import *

def genParams():
    ns = []; es = []; ps = []
    d = getPrime(425)  # 共享私钥指数 d
    for _ in 'flag{':  # 5 次循环
        p, q, r = [getPrime(512) for _ in range(3)]
        ps.append((p, q, r))
        n = p * q * r   # 三素数 RSA, n 约 1536 bit
        totient = (p-1) * (q-1) * (r-1)
        es.append(inverse(d, totient))
        ns.append(n)
    return (ns, es), (d, ps)
```

## 攻击原理

### 数学关系
- $e_i \times d \equiv 1 \pmod{\phi(n_i)}$
- $e_i \times d = 1 + k_i \times \phi(n_i)$
- $e_i \times d \approx k_i \times n_i$ (因为 $\phi(n) \approx n$)

### 6×6 格矩阵
```
┌                                     ┐
│ M    e₀  e₁  e₂  e₃  e₄          │
│ 0   -n₀   0   0   0   0           │
│ 0    0  -n₁   0   0   0           │
│ 0    0    0  -n₂   0   0           │
│ 0    0    0   0  -n₃   0          │
│ 0    0    0   0   0  -n₄          │
└                                     ┘
```

短向量 v × Mat = (M×d, d×e₀ - k₀×n₀, ..., d×e₄ - k₄×n₄)

## 攻击脚本

```python
from sage.all import *
from Crypto.Util.number import *
import gmpy2

# 已知公开参数
ns = [...]  # 5 个模数
es = [...]  # 5 个公钥指数

# Step 1: LLL 恢复 d
M = 2**1024
a = [0] * 6
a[0] = [M, es[0], es[1], es[2], es[3], es[4]]
a[1] = [0, -ns[0], 0, 0, 0, 0]
a[2] = [0, 0, -ns[1], 0, 0, 0]
a[3] = [0, 0, 0, -ns[2], 0, 0]
a[4] = [0, 0, 0, 0, -ns[3], 0]
a[5] = [0, 0, 0, 0, 0, -ns[4]]

Mat = matrix(ZZ, a)
Mat_LLL = Mat.LLL()
d = abs(Mat_LLL[3][0]) // M
print(f"d 比特长度: {d.bit_length()}")  # 425
print(f"d 是素数: {isPrime(d)}")

# Step 2: 分解模数
def getpq(n, e, d):
    while True:
        k = e * d - 1
        g = randint(0, n)
        while k % 2 == 0:
            k = k // 2
        temp = gmpy2.powmod(g, k, n) - 1
        p = gmpy2.gcd(temp, n)
        if p > 1 and isPrime(p):
            return p

key = 0
for n, e in zip(ns, es):
    p = int(getpq(n, e, d))
    q = int(getpq(n // p, e, d))
    r = n // p // q
    key += p + q + r
print(f"所有素数之和: {key}")

# Step 3: AES-ECB 解密
from Crypto.Cipher import AES
from hashlib import sha3_512
key = sha3_512(str(key).encode()).digest()[:16]
ct = b'...'
flag = AES.new(key, AES.MODE_ECB).decrypt(ct)
print(flag.decode())
# flag = flag{9b31dd3e-aa6a-4c4d-b796-bff4e4dfe0cc}
```

## 关键技术
- **共享私钥攻击**：5 组 RSA 用同一个 d，违反密钥独立性原则
- **LLL 格基规约**：构造 6×6 矩阵，短向量 = (M×d, ...)
- **Hidden Number Problem (HNP)**：e×d ≈ k×n 近似关系
- **三素数 RSA**：n = p×q×r，1536 bit
- **AES-ECB**：key = SHA3-512(sum_p_q_r)[:16]
- **模数分解**：用 d 反推 φ(n) 的 2-adic 分解

## 安全教训
- 多组 RSA 必须使用独立密钥对
- 共享任何密钥材料都会引入漏洞
- LLL 算法是格密码学强大工具

## 评价
2025 强网拟态 FMS 之后又一高难度密码题。考察 LLL + 共享私钥攻击 + 三素数 RSA 分解 + AES-SHA3 组合。flag: `flag{9b31dd3e-aa6a-4c4d-b796-bff4e4dfe0cc}`。
