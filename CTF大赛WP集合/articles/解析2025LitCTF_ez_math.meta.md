---
title: 2025 LitCTF ez_math - 2×2 矩阵幂 Cayley-Hamilton 攻击
contest: LitCTF
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags: [matrix-power, Cayley-Hamilton, finite-field, quadratic-extension, GF-p2, quotient-ring, RSA-matrix, modular-inverse, characteristic-polynomial]
attack_chain:
  - 加密: A = [[flag, getPrime], [getPrime, getPrime]]; B = A^e mod p (e=65537, p 512-bit 素数)
  - 关键: flag 在 A[0][0]
  - Cayley-Hamilton: M² - (tr M)·M + (det M)·I = 0 → M^n = p_n·M - (det M)·p_{n-1}·I
  - 特征多项式: χ_A(x) = x² - (tr A)x + det A
  - 特征值: B 的特征值 = A 特征值的 e 次方
  - 在 GF(p²)* 中, gcd(e, p²-1) = 1 → 映射 x → x^e 是双射
  - 计算私钥: d = inverse_mod(e, p²-1)
  - 商环: R = F_p[X]/(X² - s1·X + s2), X 模拟 B 的特征值
  - 计算 X^d = β + α·X (商环中快速幂)
  - 恢复 A: A = α·B + β·I
  - flag = A[0][0] = LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
key_payload: 'A = α·B + β·I + 商环 mul + pow_poly + d = inverse_mod(e, p²-1)'
one_liner: LitCTF 2025 ez_math：2×2 矩阵 A^e mod p 的 Cayley-Hamilton 攻击，把高次幂降维到商环多项式求逆。
lesson: Cayley-Hamilton 定理 + 二次扩域是矩阵密码的通用解法；商环运算避开了复杂特征值计算。
quality: high
---

# 解析 2025 LitCTF ez_math - 2×2 矩阵幂 Cayley-Hamilton 攻击

**来源**: ctfiot.com ID 278432

## 题目代码
```python
from sage.all import *
from Crypto.Util.number import *
from uuid import uuid4

flag = b'LitCTF{' + str(uuid4()).encode() + b'}'
flag = bytes_to_long(flag)
len_flag = flag.bit_length()
e = 65537
p = getPrime(512)
P = GF(p)
A = [[flag, getPrime(len_flag)], [getPrime(len_flag), getPrime(len_flag)]]
A = matrix(P, A)
B = A ** e
print(f"e = {e}")
print(f"p = {p}")
print(f"B = {list(B)}".replace('(', '[').replace(')', ']'))
```

## 数学理论

### Cayley-Hamilton 定理
对 2×2 矩阵 M：
$$M^2 - (\text{tr } M) \cdot M + (\det M) \cdot I = 0$$
$$M^n = p_n \cdot M - (\det M) \cdot p_{n-1} \cdot I$$

### 特征多项式
- $\chi_A(x) = x^2 - (\text{tr } A)x + \det A$
- B 的特征值 $\mu_i = \lambda_i^e$

### 二次扩域 GF(p²)
- 阶为 $p^2 - 1$
- 当 $\gcd(e, p^2-1) = 1$ 时，$x \to x^e$ 是双射
- 私钥 $d = e^{-1} \pmod{p^2-1}$

## 商环运算

```python
def mul(u, v):
    a, b = u
    c, d = v
    # X² ≡ s1*X - s2
    const = (a * c - (b * d % mod) * s2) % mod
    xcoef = (a * d + b * c + (b * d % mod) * s1) % mod
    return (const, xcoef)

def pow_poly(base, exp):
    res = (1, 0)  # 1
    b = base
    e = exp
    while e > 0:
        if e & 1:
            res = mul(res, b)
        b = mul(b, b)
        e >>= 1
    return res
```

## 解密流程

```python
e = 65537
p = 8147594556101158967571180945694180896742294483544853070485096002084187305007965554901340220135102394516080775084644243545680089670612459698730714507241869
B = matrix(P, B_data)

# 1. 计算群阶和私钥
phi = p^2 - 1
d = inverse_mod(e, phi)

# 2. 在商环中计算 X^d
s1 = (B[0][0] + B[1][1]) % p  # tr(B)
s2 = (B[0][0] * B[1][1] - B[0][1] * B[1][0]) % p  # det(B)
beta, alpha = pow_poly((0, 1), d)  # X^d = beta + alpha*X

# 3. 恢复 A
A_recovered = alpha * B + beta * identity_matrix(2)

# 4. 提取 flag
flag = long_to_bytes(int(A_recovered[0, 0]))
print(flag)  # LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
```

## 关键技术
- **Cayley-Hamilton**：M² = (tr M)·M - (det M)·I
- **二次扩域**：特征值最多需要 GF(p²)
- **商环多项式求幂**：X^d 退化为 β + α·X
- **矩阵线性化**：A = α·B + β·I 把高次幂变一次线性组合

## 退化情况
- 若 B 是数量矩阵（与 I 成比例），商环退化为 1 维
- 本题不出现

## 评价
2025 LitCTF 密码学 ez_math 高质量题。考察 Cayley-Hamilton 定理 + 二次扩域 + 商环多项式。从矩阵密码到代数结构，是理论深度的极佳展示。flag：`LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}`
