---
title: Coppersmith's Attack
contest: 公众号文章
year: 2020
difficulty: medium
vuln_type: crypto_rsa
tags: [crypto, rsa, coppersmith, small-e, 部分p泄露, sagemath, sha256前缀]
attack_chain:
  - 第1题: e=3, c<m^3 直接 gmpy2.iroot(c,3) 开立方
  - 第2题: e=65537, p高128位已知 用Coppersmith f=x+p4
  - PR.<x>=PolynomialRing(Zmod(n)) f=x+p4
  - x0=f.small_roots(X=2^kbits, beta=0.4)[0]求小根
  - 第0题: SHA256前缀爆破找 skr
key_payload: f.small_roots(X=2^kbits, beta=0.4)[0]  # sagemath
one_liner: Coppersmith攻击小e+部分p泄露+SHA256前缀爆破综合
lesson: 已知p高位时用Coppersmith在Zmod(n)上多项式小根求低位
quality: medium
---

# Coppersmith's Attack

## 题目信息
- 来源：ctfiot 转载 PoC||GTFO 风格文章
- 涵盖：3 个挑战，难度递进

## 关键攻击链
### 挑战 0：SHA256 前缀爆破
- `skr[0:5].encode('hex') = 88d6b371c4`
- `sha256(skr) = 235b85c0695a9d824064d887285b462c6e5bf11eb1521b24fcb72b320aa13ed1`
- 解：`for i in range(10000,20000000): payload=long_to_bytes(tar)+long_to_bytes(i); sha256(payload)==...`

### 挑战 1：e=3 直接开立方
- `c = pow(m, 3, n)`，且 `m^3 < n`
- `m = gmpy2.iroot(c, 3)[0]` 直接开立方

### 挑战 2：已知 p 高 128 位
- p 1024 位，已知高 896 位 `(p>>128)<<128 = p4`
- kbits = 1024 - 896 = 128 位未知
- Sagemath：
  ```python
  PR.<x> = PolynomialRing(Zmod(n))
  f = x + p4
  x0 = f.small_roots(X=2^kbits, beta=0.4)[0]
  ```

### 挑战 3：类似 1 但需额外处理
- e=3 但 m 大或 n 有特殊结构

## 关键技术点
- Coppersmith 小根定理：已知 p 高位多项式 `f(x) = x + p4` 模 n，X=2^kbits，beta=0.4
- sagemath `small_roots` 实现
- gmpy2 `iroot` 大整数开方

## 评分
- quality: medium（概念清晰 + sagemath 代码示例，但内容较零散）
