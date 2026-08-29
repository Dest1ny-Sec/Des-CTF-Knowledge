---
title: 2025 RCTF writeup by Arr3stY0u（GMP MT19937 LSB 格攻击 + seed2 缩放）
contest: 2025 RCTF
year: 2025
difficulty: hard
vuln_type: [crypto_unknown, lattice, mt19937]
tags: [RCTF GMP MT19937, gmp_urandomb_ui 取低 31 位, WARM_UP = 2000 twist, mti = 2000 % 624 = 128, LSB 观测, twist 线性递推, temper 移位+按位与/异或, LSB 取出 1 位, 矩阵元素数=624 LSB 完整观测, 模数 LLL 还原 seed, 用户 secret 字节缩放, 二次幂模映射]
attack_chain:
  - 用户 secret=int.from_bytes(secret, 'big') 缩放成 seed
  - 二次幂模映射 seed2 = seed^2 mod N
  - seed2 位填入 MT mt[] 状态：bit31 是 mt[0] 最高位
  - WARM_UP=2000 调用 __gmp_mt_recalc_buffer (twist)
  - mti = 2000 % 624 = 128
  - 标准 MT19937 twist+temper（32 位）取 gmp_urandomb_ui(self.gmp_state, 31) 低 31 位
  - 取最低 1 位 LSB 作为 1 比特随机整数返回
  - 624 LSB 完整观测 → 矩阵 F2 上 LLL → 还原 seed2 → 还原 secret
key_payload: "mti = 2000 % 624 = 128; gmp_urandomb_ui 取低 31 位"
one_liner: 2025 RCTF 高级 crypto：GMP MT19937 自实现 + WARM_UP 2000 + 二次幂模映射 + LSB 1 比特输出，624 LSB 完整观测后用 F2 上 LLL 反推 seed2 → 还原 secret。
lesson: GMP 内置 MT19937 是 gmpy2 / pycryptodome 测试向量的常见来源；自定义 WARM_UP + temper 后取 LSB 是抗直接 MT crack 套路，但只要能取 624 个连续 LSB，F2 上 LLL 仍可还原。
quality: high
---

# 2025 RCTF writeup by Arr3stY0u（GMP MT19937 LSB 格攻击）

## 题目结构

```python
# 用户 seed = int.from_bytes(secret, 'big') 缩放
# seed2 = seed^2 mod N
# seed2 位填入 MT mt[]：
#   bit31 = mt[0] 的最高位（其余 31 位为 0）
#   剩余位按 32 位小端拆成 mt[1..623]
WARM_UP = 2000
# 调用 __gmp_mt_recalc_buffer (twist) 2000 次
mti = WARM_UP % 624 = 128
# twist + temper（标准 MT19937 32 位）后
# gmp_urandomb_ui(self.gmp_state, 31) 取低 31 位
# 作为 31 比特随机整数返回
# 但攻击者只取 LSB（最低 1 位）
```

## 攻击思路

如果我们让矩阵的元素个数为 624，则可在一次交互中完整观测 warm-up 后 MT 的连续 624 个 LSB。

- **twist** 本质是线性递推；
- **temper** 由移位 + 按位与/异或构成；
- **取 LSB** = 取最低 1 位。

记 $a_i$ 为 mt[0] 的 bit 变量（bit31），$b_j$ 为观测到的 LSB 序列。  
整体 $a_i \to b_j$ 是由 "seed2 → mt[] → twist/temper → LSB" 组成的**线性变换矩阵** $A$（F2 上）。  
种子 s 上界远小于 N → 视作整数 → 模数 N；多项式次数 m → F2 上 LLL → 还原 seed2 → 还原 secret。

## 关键观察

- WARM_UP=2000 是固定常量 → mti=128 固定  
- 取 LSB 而非全 31 位输出是抗攻击设计，但 624 个 LSB 仍可解  
- 二次幂模映射 seed2 = seed^2 mod N 把 seed 域压到 N，但 N=2^32（mt 大小）量级时仍是可解的

## 解题要点

1. **观测 624 LSB** → 建立 F2 上线性方程组
2. **F2 LLL / 高斯消元** → 还原 mt[0..623] 全部 32 位
3. **mt[0] bit31 = seed2 的 bit31** → 还原 seed2
4. **二次幂模开方** → 还原 seed
5. **seed = int(secret) 缩放回** → 还原 secret 字节
