---
title: 解析一道清朝老题 - McEliece
contest: Hack.lu CTF 2017 / 后量子 crypto
year: 2025 (现代解析)
difficulty: hard
vuln_type: [crypto_rsa, lattice]
tags: [McEliece, GRS, Reed-Solomon, 范德蒙德, Sidelnikov-Shestakov, Berlekamp-Welch, GF(2^8), 后量子, 编码密码]
attack_chain: ["公开 publickey.sobj 64×128 矩阵 over GF(2^8)", "公开 ciphertext.sobj 128 维向量", "识别 GRS 码（生成矩阵每列是范德蒙向量）", "Sidelnikov-Shestakov 攻击：枚举 255 个 ratio 恢复支撑向量 α", "用 GRS 对偶码也是 GRS 性质恢复列乘子 v", "Berlekamp-Welch 解码器解出 m·S", "左乘 S^-1 还原明文 m", "flag: flag{ReedSolomonCodesAreNoGoodIdeaForMcElieceIfYouWantTopCrypto}"]
key_payload: "G[i,j] = v_j * α_j^i  (i=0..k-1, j=0..n-1) — 范德蒙德结构"
one_liner: Sidelnikov-Shestakov 攻击 McEliece GRS 码 255 ratio 枚举
lesson: McEliece 安全只对二元 Goppa 码；GRS / Reed-Solomon 实现的 McEliece 是 1992 年就被破的；后量子选码要慎重
quality: high
---

# 解析一道清朝老题 - McEliece

原文 https://www.ctfiot.com/282175.html

## 题目
- `publickey.sobj`: 64×128 矩阵 over GF(2^8)
- `ciphertext.sobj`: 128 维向量 over GF(2^8)
- 经典后量子密码学 CTF 挑战

## McEliece 密码系统
```
选择 [n, k, d] 线性纠错码 C，有高效解码 D
选择 k×k 可逆矩阵 S 和 n×n 置换矩阵 P
公钥 G' = S·G·P
私钥 (S, G, P, D)
随机选权重 t 错误向量 e
密文 c = m·G' + e
解密：c' = c·P^-1 = m·S·G + e·P^-1
       D(c') = m·S
       m = (m·S)·S^-1
```

## 漏洞：GRS 码被 Sidelnikov-Shestakov 攻破

GRS 码生成矩阵形如 `G[i,j] = v_j · α_j^i`，列之间存在多项式关系（范德蒙德结构），对偶码也是 GRS。

### 攻击步骤
1. **设 a[0]=0, a[1]=1**（无损一般性）
2. **枚举 255 个 ratio** 恢复支撑向量 α
   ```python
   for ratio in F.list()[1:]:
       a = [0]*n
       a[1] = 1
       succ = True
       # 恢复支撑向量
       for i in range(k, n):
           tar = gpe[0][i] / gpe[1][i] / ratio
           res = 0
           for x in F.list():
               if x != 0 and (x - a[1]) / (x - a[0]) == tar:
                   if res != 0: succ = False; break
                   res = x
           if res == 0: succ = False
           if not succ: break
           a[i] = res
       if not succ: continue
   ```
3. **恢复剩余 α 元素 + 列乘子 v**
4. **重构 GRS 码 + Berlekamp-Welch 解码器**
5. **还原明文**

### Sage 解码
```python
C = codes.GeneralizedReedSolomonCode(a, k, cols)
E = codes.encoders.GRSEvaluationVectorEncoder(C)
D = codes.decoders.GRSBerlekampWelchDecoder(C)
g = E.generator_matrix()
tmp = D.decode_to_message(cmsg)
msg = vector(tmp) * h.inverse()
print(bytes([int(str(x)) for x in msg]))
```

## flag
```
flag{ReedSolomonCodesAreNoGoodIdeaForMcElieceIfYouWantTopCrypto}
```
明文向量：`(102, 108, 97, 103, 123, 82, 101, 101, 100, 83, 111, 108, ...)` = `flag{ReedS...`

## 复杂度
- 枚举 255 个 ratio
- 每个 ratio 需要 n 次查找 + 验证
- **秒级完成** （SageMath）

## 安全对比
| 码类型 | 是否安全 |
|--------|---------|
| GRS / Reed-Solomon | ❌ 1992 Sidelnikov-Shestakov 攻破 |
| 经典 Goppa 码 | ✅ 40 年无本质弱点 |
| 二元 Goppa 码 | ✅ NIST 后量子标准候选（n≥2000, t≥50, m≥11） |

## 教学价值
- McEliece 是 1978 年最早的非 RSA 公钥方案之一
- 安全性完全依赖底层纠错码选择
- GRS / RS 实现 = 自杀
- 二元 Goppa 才是 NIST 选定的"安全"实现
- SageMath 的 `codes.GeneralizedReedSolomonCode` + `GRSBerlekampWelchDecoder` 是 CTF 工具
- 1992 Sidelnikov-Shestakov 论文 + 2009 IACR ePrint 452 详细代数攻击

## 参考文献
- Sidelnikov V.M., Shestakov S.O. (1992) — On insecurity of cryptosystems based on generalized Reed-Solomon codes
- IACR ePrint 2009/452 — Algebraic Cryptanalysis of McEliece Variants with Compact Keys
- NIST Post-Quantum Cryptography Standardization Project
- Hack.lu CTF 2017 — McEliece Challenge
