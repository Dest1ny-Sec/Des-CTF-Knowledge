---
title: 2025 强网杯 ezran - MT19937 状态恢复攻击
contest: 强网杯
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags: [MT19937, PRNG-state-recovery, GF-2-linear, shuffle-reverse, Fisher-Yates, gf2bv, Mersenne-Twister, gaussian-elimination, getrandbits]
attack_chain:
  - 题目: MT19937 PRNG 生成 3108 次 (r1, r2)
  - r1 = getrandbits(8), r2 = getrandbits(16)
  - x = (pow(r1, 2*i, 257) & 0xff) ^ r2 → 2 字节大端 gift
  - 总输出 3108 × 2 = 6216 字节
  - flag 用 Python shuffle() 打乱 2025 次
  - 关键: r2 高 8 位 ^ observed = (pow(r1, 2*i, 257) & 0xff) = 0-255
  - 约束: (r2 >> 8) ^ observed ∈ [0, 255]
  - 内部状态 624 个 32 位整数 (19968 bit)
  - 用 gf2bv 库构造线性系统 lin = LinearSystem([32] * 624)
  - 高斯消元法 GF(2) 求解多个解
  - 第一个状态最高位为 1: mt[0] ^ 0x80000000
  - Fisher-Yates 逆: 记录每次交换 (i, j), 反向应用
  - 验证: gg == gift → flag
key_payload: 'getrandbits(8) + getrandbits(16) + gift[2i:2i+2][0] + LinearSystem(624) + Fisher-Yates 逆'
one_liner: 2025 强网杯 ezran：MT19937 624 状态 GF(2) 线性方程组恢复 + Fisher-Yates 洗牌逆向。
lesson: MT19937 内部状态 19968 bit 可通过足够样本 (3108) 恢复；GF(2) 线性代数 + 高斯消元是标准攻击。
quality: high
---

# 解析 2025 强网杯 ezran - MT19937 状态恢复攻击

**来源**: ctfiot.com ID 275603

## 题目分析
- `r1 = getrandbits(8)` (8 位)
- `r2 = getrandbits(16)` (16 位)
- `x = (pow(r1, 2*i, 257) & 0xff) ^ r2`
- `gift += long_to_bytes(x, 2)` (大端)
- 循环 3108 次 → 6216 字节
- `flag` 用 `shuffle()` 打乱 2025 次

## 信息泄漏
- `r2 >> 8 ^ observed = pow(r1, 2*i, 257) & 0xff`
- `r2 >> 8` 的范围是 0-255
- 通过 `gift[2i:2i+2][0]` 提取 `x` 的高 8 位

## 攻击链

### Step 1: 提取约束
```python
from gf2bv import LinearSystem
import random

gift = ...  # 6216 字节
out = [gift[2*i:2*i+2][0] for i in range(len(gift) // 2)]  # 3108 个高 8 位
```

### Step 2: 构造线性系统
```python
lin = LinearSystem([32] * 624)
mt = lin.gens()  # 624 个 32 位符号变量

rng = random.Random()
zeros = []

# 第一个状态最高位为 1
zeros.append(mt[0] ^ int(0x80000000))

# 约束: (r2 >> 8) ^ observed ∈ [0, 255]
for o in out:
    rng.getrandbits(8)  # 模拟 r1
    zeros.append(rng.getrandbits(16) >> 8 ^ int(o))
```

### Step 3: 求解 GF(2) 线性方程组
```python
for sol in lin.solve_all(zeros):
    # sol 是 MT19937 内部状态 624 个 32 位整数
    # 重建 random.Random 实例
    rng_state = (3, tuple(sol + [624]), None)
    rng = random.Random()
    rng.setstate(rng_state)
    
    # 重放 2025 次 shuffle 逆向
    # ... 验证 gift
```

### Step 4: Fisher-Yates 逆
```python
# 记录 shuffle 时的 (i, j) 交换
sw = []
rng = random.Random(seed)
arr = list(range(n))
for i in range(n-1, 0, -1):
    j = rng.randint(0, i)
    sw.append((i, j))
    arr[i], arr[j] = arr[j], arr[i]

# 逆: 反向应用
for i, j in reversed(sw):
    arr[i], arr[j] = arr[j], arr[i]
```

## 关键技术
- **MT19937 内部状态**: 624 个 32 位整数 = 19968 bit
- **GF(2) 线性代数**: 状态转移在 GF(2) 上是线性的
- **gf2bv 库**: https://github.com/orisano/gf2bv 自动化线性系统求解
- **高斯消元**: 求多个解后验证
- **Fisher-Yates 洗牌**: 记录 (i, j) 交换 + 反向应用

## 评价
2025 强网杯 ezran 高质量密码学 PRNG 攻击题。考察：
- MT19937 算法细节
- GF(2) 线性代数
- 信息泄漏分析 (r2 高 8 位 + 0-255 范围约束)
- Fisher-Yates 逆算法

是 PRNG 状态恢复经典教学案例。
