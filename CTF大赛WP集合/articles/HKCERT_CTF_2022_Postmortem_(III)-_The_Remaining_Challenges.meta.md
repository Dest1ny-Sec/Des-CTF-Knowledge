---
title: HKCERT CTF 2022 Postmortem (III): The Remaining Challenges
contest: HKCERT CTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [misc, z3-solver, mycraft, java, weighted-baked-model, getRotation, random-seed]
attack_chain:
  - 序列: ? 1 37 37 97 / ? 33
  - 序列: ? 1 85 85 97 / ? 85 / ? 2 2 26 97 / ? 24
  - z3求解: xs[0..m-1]整数数组
  - 约束: 严格递增+不重复+<q
  - sum[0]=xs[0], sum[i+1]=sum[i]+(i+2)*xs[i+1]
  - product[0]=xs[0], product[i+1]=product[i]*(i+2)*xs[i+1]
  - sum[m-1] % q == s, product[m-1] % q == p
  - Java getRotation: x*3129871 ^ z*116129781 ^ y
  - seed = (l*l*42317861 + l*11) >> 16
  - Random.nextLong() % 4
key_payload: z3.Solver + xorshift seed + weighted-baked-model
one_liner: HKCERT 2022 Misc：z3求解Minecraft mycraft+getRotation种子
lesson: Java Random种子可由x,y,z坐标异或重建
quality: high
---

# HKCERT CTF 2022 Postmortem (III): The Remaining Challenges

## 题目信息
- 比赛：HKCERT CTF 2022
- 作者：mystiz
- 类别：Misc

## 关键攻击链
### 1. 序列分析
```
? 1 37 37 97
? 33
? 1 85 85 97
? 85
? 2 2 26 97
? 24
```

### 2. z3 求解
```python
from z3 import *
import itertools
m, s, p, q = map(int, r.recvline().decode().split())
_s = Solver()
xs = [Int(f'x_{i}') for i in range(m)]
subss = [Int(f'ss_{i}') for i in range(m)]
subps = [Int(f'ps_{i}') for i in range(m)]

# 基础条件
for i in range(1, m):
    _s.add(xs[i-1] <= xs[i])
for i in range(0, m):
    _s.add(Not(xs[i] <= 0))
    _s.add(xs[i] < q)
for i, j in itertools.product(range(0, m), repeat=2):
    _s.add(Implies(i != j, xs[i] != xs[j]))

# s 和 p 约束
_s.add(subss[0] == xs[0])
_s.add(subps[0] == xs[0])
for i in range(m-1):
    _s.add(subss[i+1] == subss[i] + (i+2)*xs[i+1])
    _s.add(subps[i+1] == subps[i] * (i+2)*xs[i+1])
    _s.add(subss[m-1] % q == s)
    _s.add(subps[m-1] % q == p)

assert _s.check() == sat
md = _s.model()
x0s = [md.evaluate(xs[i]) for i in range(m)]
```

### 3. Java getRotation
```java
public static long getRotation(int x, int y, int z) {
    long l = (long)(x * 3129871) ^ (long)z * 116129781L ^ (long)y;
    l = l * l * 42317861L + l * 11L;
    long seed = l >> 16;
    Random random = new Random(seed);
    return Math.abs(random.nextLong()) % 4;
}
```

### 4. Go 实现
```go
func getRotation(x, y, z int) int32 {
    x2 := int(int32(x * 3129871))
    z2 := z * 116129781
    l := x2 ^ y ^ z2
    l = l * (l*42317861 + 11)
    seed := l >> 16
    seed ^= 0x5DEECE66D
    v := int32((seed*0xBB20B4600A69 + 0x40942DE6BA) >> 16)
    if v < 0 { v = -v }
    return v & 3
}
```

## 评分
- quality: high（z3 + Java Random 种子 + Minecraft mycraft 坐标）
