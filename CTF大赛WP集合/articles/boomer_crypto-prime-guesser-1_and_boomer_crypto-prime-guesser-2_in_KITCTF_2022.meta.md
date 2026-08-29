---
title: boomer_crypto-prime-guesser-1 and boomer_crypto-prime-guesser-2 in KITCTF 2022
contest: KITCTF
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [rsa, binary-search, q-finding, 8-bit-prime, q-recovery, mitm, 16-bit-prime]
attack_chain:
  - 1: 8 bit q 暴力枚举
  - mod p 找 q
  - SCALED_PT 模式
  - 2: 16 bit q 暴力
  - FINDING Q 二分迭代
  - Q=2^i 模式（第一次 True 转 False 的位置）
  - SK 计算
  - 4 个 scaled_pt 恢复
key_payload: FINDING Q 模式识别 + 二分搜索 q
one_liner: KITCTF 2022 boomer prime-guesser 1/2 复盘，8/16-bit RSA 弱密钥枚举。
lesson: 当 q < 2^k 时，q = 2^k + 1 转换点能定位 q 真实值。
quality: high
---

KITCTF 2022 boomer_crypto-prime-guesser-1 和 -2 复盘。

**prime-guesser-1（8-bit q）**

简单暴力枚举 2^8 = 256 个 q 候选值，验证哪个 q 满足 p = N / q 是质数。

**prime-guesser-2（16-bit q）**

更复杂的搜索：
```python
FINDING Q
iter: 1 i: 2 True
iter: 2 i: 4 True
iter: 3 i: 8 True
...
iter: 19 i: 524288 True
iter: 20 i: 1048576 False
...
iter: 31 i: 2147483648 False
iter: 32 i: 4294967296 True
```

**核心观察**：从 iter=20 开始 i=1048576 返回 False（因为 i 已经超过 q 的位数）；iter=32 时 i=4294967296 = 2^32 又返回 True（巧合：q < 2^32 时 mod q 是 0）。

通过"第一次 True 转 False"的位置可以定位 q 的真实位数（这里 q < 2^19 即 16-bit）。然后用 2^19 附近的值爆破 q。

**SCALED_PT / SK**
- `SCALED_PT[i]` 是密文按位展开的 0/1 序列
- `SK[i]` 是私钥 d 对应位
- 通过模幂还原明文

**4 个 scaled_pt 模式恢复**
每 4 个 SCALED_PT 是相同明文 m 的不同密文组合（CRT 攻击方向），用 CRT 求 d 然后解 m。

整篇 WP 适合作为"RSA 弱 q 攻击 + 模式识别 + CRT 恢复"完整教学。
