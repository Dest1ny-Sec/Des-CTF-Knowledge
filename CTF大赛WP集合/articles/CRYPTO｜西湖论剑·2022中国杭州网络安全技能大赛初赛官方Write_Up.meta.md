---
title: CRYPTO｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up
contest: 西湖论剑
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [MyCurveErrorLearn ECHNP, MyErrorLearn MIHNP, MyErrorLearnTwice LLL对角阵, LockByLock Pollard kangaroo, MyOracle MT19937 LSB, 椭圆曲线HNP, 模逆HNP, Coppersmith, Pollard kangaroo e范围爆破, MT19937 state恢复]
attack_chain:
  - MyCurveErrorLearn: ECHNP(DH) 椭圆曲线 Hidden Number Problem, 输入 0 得 t=0, t 与 oracle 输出多项式关系
  - LockByLock: secureProcedure 嵌套加密, A 加密 c1, B 加密 c1 得 c2, A 解 c2 得 c3
  - 两次输入得中间值, Pollard's kangaroo 在 e 范围内求解
  - MyErrorLearn: MIHNP 模逆 HNP, 二元 Coppersmith 解多项式
  - MyErrorLearnTwice: d 组输出, LLL 求对角阵 + 最短格向量恢复 e
  - MyOracle: 模是偶数时泄露 r LSB, 构造矩阵恢复 MT19937 全部 state
key_payload: 'ECHNP(DH) / LockByLock kangaroo / MIHNP Coppersmith / MIHNP LLL 对角阵 / MT19937 LSB state 恢复'
one_liner: 西湖论剑 2022 CRYPTO 官方 WP — MyCurveErrorLearn ECHNP 椭圆 HNP + LockByLock Pollard kangaroo + MyErrorLearn MIHNP Coppersmith + MyErrorLearnTwice LLL 对角阵 + MyOracle MT19937 LSB state 恢复。
lesson: HNP (Hidden Number Problem) 是密码学隐藏数问题模板;ECHNP/MIHNP/LWE 都基于 LLL;Pollard kangaroo 适合已知 e 范围;MT19937 LSB oracle 是 RNG 恢复经典。
quality: high
---

# CRYPTO｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up

## 速读
西湖论剑 2022 CRYPTO 官方 5 题 — 椭圆曲线 HNP + 模逆 HNP + MT19937 state 恢复。

## Crypto 题目

### (一) MyCurveErrorLearn
- ECHNP(DH): 椭圆曲线 Hidden Number Problem
- 输入 0, oracle 输出 t 与未知 P 的关系
- 多项式还原 P

### (二) LockByLock
- secureProcedure 嵌套加密
- A 加密 flag → c1, B 加密 c1 → c2, A 解 c2 → c3
- 两次输入得中间值
- Pollard's kangaroo 在 e 范围内求解
- secureProcedure + 共模攻击

### (三) MyErrorLearn
- MIHNP: Modular Inversion Hidden Number Problem
- d 对 (a, b) 中恢复 s
- 二元 Coppersmith 解多项式

### (四) MyErrorLearnTwice
- d 组输出, MIHNP LLL 升级
- 构造对角阵, 求最短格向量恢复 e

### (五) MyOracle
- 模是偶数 → 泄露 r LSB
- 构造矩阵恢复 MT19937 全部 state (cryptography-wiki MT19937 矩阵构造)
- 预测随机数
