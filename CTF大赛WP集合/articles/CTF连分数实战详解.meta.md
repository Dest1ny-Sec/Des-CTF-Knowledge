---
title: CTF连分数实战详解
contest: 公众号文章
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags: [crypto, rsa, 连分数, wiener, pell, 渐进分数]
attack_chain:
  - 连分数展开e/N得到渐进分数列表
  - 遍历每个收敛k/d验证k*e-1能否被d整除
  - 若能则得到私钥d分解N=p*q
  - 扩展攻击d<N^0.25用2t+8bits搜索
  - Pell方程x^2-Dy^2=1连分数求最小特解
key_payload: def transform(x,y): res=[]; while y: res.append(x//y); x,y=y,x%y
one_liner: 连分数攻击小d RSA，含Wiener扩展+Verheul-Tilborg+Pell方程
lesson: 小解密指数RSA用连分数逼近k/d，d<N^0.292时仍可破
quality: high
---

# CTF连分数实战详解

## 题目信息
- 来源：公众号「别忘了星标我」
- 主题：连分数方法攻击 RSA
- 引用论文：Wiener 1990、Verheul-van Tilborg 1997、eprint 2008/459、2015/399

## 关键攻击链
1. **Wiener 攻击**：当 `d < N^0.25` 时，k/d 是 e/N 的渐进分数，欧几里得算法求所有收敛，验证 `k*e ≡ 1 (mod d)` 来分解 N
2. **连分数展开**：`transform(x,y)` 辗转相除法，sagemath 用 `continued_fraction(45/38)` 得 `[1;5,2,3]`
3. **Verheul-Tilborg 扩展**：d 比 N^0.25 长几位，2t+8 bits 暴力搜索部分收敛
4. **Prime Power RSA**：双模 N1/N2 时 k/(N1*N2) 渐进分数验证
5. **Pell 方程**：`x^2 - D*y^2 = 1` 用连分数求最小特解
6. **完整代码**：`sub_fraction(45,38) → [(1,1),(6,5),(13,11),(45,38)]`

## 关键技术点
- 连分数展开：欧几里得算法的变体
- 渐进分数（convergent）：k_n/d_n 形式
- 模 N 分解：`(k*e-1) % d == 0` 验证
- Pell 方程：连分数求最小解

## 评分
- quality: high（理论+代码+论文引用齐全，覆盖 Wiener 及其 3 种扩展）
