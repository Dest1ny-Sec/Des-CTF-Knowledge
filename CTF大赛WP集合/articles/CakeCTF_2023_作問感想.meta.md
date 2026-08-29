---
title: CakeCTF 2023 作問感想
contest: CakeCTF 2023 (出题人感想)
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags: [crypto, pwn, 签名前置, RSA-CRT, 矩阵幂, 出题人感想, 双语]
attack_chain:
  - simple signature: x/u仅在公钥中，私钥无关联任意设值解
  - Cake Puzzle: 15-puzzle简单reversing+solver
  - janken vs yoshiking 2: GL5(Fp)矩阵幂+det() Pohlig-Hellman DLP
  - decryptyou: RSA-CRT Garner算法u=p mod q可pwn破坏但m≤p时不响
  - Iron Door: 高难度crypto
key_payload: det(M^r) = det(M)^r 在Fp上做Pohlig-Hellman
one_liner: CakeCTF 2023出题人感想，5题涵盖签名+15拼图+矩阵DLP+RSA-CRT
lesson: 矩阵离散对数可用det()降到Fp上DLP；RSA-CRT Garner中临时变量u可被pwn
quality: high
---

# CakeCTF 2023 作問感想

## 题目信息
- 比赛：CakeCTF 2023
- 作者：yoshiking（官方出题人感想文）
- 涵盖：simple signature / Cake Puzzle / janken vs yoshiking 2 / decryptyou / Iron Door
- 形式：日文 + 中文双语

## 关键攻击链
1. **[crypto/warmup] simple signature**（88 解）：公钥中 x, u_?, ?_? 只在公钥用，私钥无数学关联 → 任意设值匹配
2. **[rev] Cake Puzzle**（56 解）：15 拼图 reversing + solver 即可解
3. **[crypto] janken vs yoshiking 2**（43 解）：
   - yoshiking 选 5×5 随机矩阵 M（Fp 上），算 M^r
   - r mod 3 是 yoshiking 出拳
   - p smooth，GL5(Fp) 不便直接求
   - **关键 trick**：`det(M^r) = det(M)^r`，Fp 上 Pohlig-Hellman 解 DLP
4. **[crypto/pwn] decryptyou**（13 解）：
   - zer0pts CTF 2022 signme 续作，RSA-CRT 解密可 pwn 破坏 `u = p mod q`
   - Garner 算法 `m = ((m_p - m_q) * u mod p) + m_q mod n`
   - **关键 trick**：若 m ≤ p，则 m_p = m_q，Garner 中 `(m_p - m_q)*u mod p = 0`，u 被破坏也不影响
5. **[crypto] Iron Door**（8 解）：高难度题

## 评分
- quality: high（出题人亲自讲思路 + 数学 trick 详细，双语内容）
