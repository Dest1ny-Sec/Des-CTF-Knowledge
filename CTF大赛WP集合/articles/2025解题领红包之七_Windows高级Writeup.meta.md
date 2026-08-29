---
title: 2025 解题领红包之七 - Windows 高级 Writeup
contest: 解题领红包
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags: [ECC椭圆曲线, point_add, 加密d-1轮, 解密d-1轮, 108字符6字符组, ParseInt, 时间戳异或, abs64平方, UID, 比较Str1!=Str2, 复杂条件, 排行榜第五]
attack_chain:
  - 入口 sub_1400017A0: 输入 UID (范围 1..0x5F5E0FE)
  - UID ^= 60 * (time(0)/60) / 10
  - Str2 = abs64(UID*UID) sprintf 16 字符
  - 输入 Key 长度必须 108
  - Key 每 6 字符一组, ParseInt 3 个 2 字符为 100*v9 + 10*v10 + v11
  - 共 18 个整数组成 IntArray[0..17]
  - 椭圆曲线加密: 用 (a, d, Gx, Gy, p) 跑 d-1 次 point_add 得 (x, y) = (v12, v13)
  - 从 IntArray 取 de_a = [16], de_p = [17] (用户提供 a, p)
  - 用 de_a, de_p 解密 d-1 次得 (x1, y1)
  - 循环 16 次: Str1[i] = (IntArray[i] - 10*y1 - v20) / x1 (mod? 步长 10202)
  - 比较 Str1 != Str2
  - 步长 10202 × 16 = 163232
  - Str2 由 abs64(UID^2) 决定, UID 又被时间戳影响
key_payload: '108字符→18 数组 / ECC 加密-解密 d-1 轮 / de_a, de_p 用户控制 / 步长 10202 16 次 / Str1 != Str2 校验'
one_liner: 解题领红包 Windows 高级 — UID+时间戳异或得 Str2 + 108 字符 Key 转 18 数组 + ECC 加解密 d-1 轮 + 复杂字符算式比较。
lesson: 比较 Str1 != Str2 即失败, 需让两边相等; UID^2 决定 Str2, 但 UID 也被 time(0) 量化异或, 所以爆破时间窗口 + 构造 Key 是双难。
quality: medium
---

# 2025 解题领红包之七 - Windows 高级 Writeup

## 速读
作者 Command (排行榜第五) — 复杂 ECC + 时间戳条件校验, 实际无法提交。

## 校验链路
1. UID (1..0x5F5E0FE) → `UID ^= 60 * (time(0)/60) / 10` → 平方 → Str2
2. Key 必须 108 字符
3. Key 每 6 字符解析为 3 个 2 字符数字 → 18 个整数
4. 用内置 (a, Gx, Gy, d, p) 跑 ECC 加 d-1 次加密
5. 从 IntArray[16], IntArray[17] 读 de_a, de_p
6. 用 de_a, de_p 解密 d-1 次
7. 循环 16 次 (步长 10202, 总 163232) 算 Str1[i] = (IntArray[i] - 10*y1 - v20) / x1
8. `strncmp(Str1, Str2, 0x10) != 0` → Correct else Error

## 难点
- d != 1 总是成立
- de_a, de_p 完全由用户控制 (IntArray[16], [17])
- 步长 10202 是固定递增
- Str2 由时间相关 UID 决定, 不可预测

## 评价
题目极其复杂但因时间窗口限制 + 解析约束太多, 实战无法提交; 仍是有教学价值的 ECC 综合题。
