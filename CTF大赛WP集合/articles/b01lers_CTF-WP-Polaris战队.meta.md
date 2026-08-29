---
title: b01lers CTF WP - Polaris 战队
contest: b01lersCTF
year: 2024
difficulty: medium
vuln_type: crypto_rsa
tags: [coppersmith, certificate, lop, knapsack, ntru, lattice]
attack_chain:
  - 解析 X.509 证书公钥
  - Coppersmith 小根
  - p=2,q=3 / p=3,q=2 爆破
  - 还原 RSA 私钥
  - 解密 flag
key_payload: t0 证书爆破 + Coppersmith small_roots
one_liner: b01lers CTF 多题 WP 合集，Polaris 战队对证书类 RSA 与格密码题给出系统化爆破思路。
lesson: RSA 弱密钥(e 极小、p 邻近、证书 t0 已知)攻击面比单纯 e*d 完整攻击更多；CTF 出题常借 X.509 包装弱密钥。
quality: high
---

b01lers CTF 2024 Polaris 战队 WP 集合，重点题 Majestic Lop：题目给一份 X.509 证书
+ 密文 flag，要求破 RSA。证书里 t0 timestamp 字段有限，p 较小(Coppersmith 适用)
且 p=2,q=3 或 p=3,q=2 这种极小因子组合。

作者给出系统化攻击流程：
1. openssl 解析证书 → 提取 N, e
2. factor_db / yafu 试分解
3. 失败则试 p=2 或 p=3 的极小子因子
4. 再失败用 e 与 N 的关系推 Coppersmith bound
5. 都失败退到 Wiener / Boneh-Durfee 连分数

合集还涉及 knapsack 低密度攻击(LLL)、NTRU 私钥恢复、ECC 离散对数等格密码
应用题，每道题都给了 SageMath 完整脚本与解题思路。Polaris 战队在赛后公开的
WP 比 b01lers 官方 writeup 更详细。

适合作为 Crypto 方向 CTFer 的"小抄合订本"：每类弱密钥一把梭的脚本都备好。
