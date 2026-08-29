---
title: 看雪 2022 KCTF 春季赛 第11题 虫洞末世 ydmp 原点磨盘
contest: KCTF春季赛
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [KCTF, custom-cipher, floating-point-error, GCD, factor, brute-force, mathematical-puzzle, single-team, ydmp]
attack_chain:
  - flag = lrY1314cXy2920as
  - 数字映射 ascii+175, 字符映射 ascii+100
  - 平方组合: p = lists[2i]² * lists[2i+1] + i² (i = 项数)
  - 奇偶判定: 奇数 +2, 偶数 +1
  - 磨盘公倍数: 在第 3 式项数同乘的基础上分别相加得到 2.式的公倍数 Q
  - Q 作除得到最终值
  - 验证: 开放首末最终值 + 6 项的两两比值 doom 后的值
  - sage gcd(m0, m1) = 32, factor 拆解 m0 m1 为素因子
  - 暴力 96^4 = 8,419,072 组合 (i,l,j,m) 找 (197,215) (208,214)
  - 浮点运算 + doom 误差扩大 → 整数比较容差
key_payload: 'p = lists[2i]² * lists[2i+1] + i² + 平方公倍数 + 浮点 doom 误差'
one_liner: ydmp 原点磨盘密码：平方+公倍数+浮点误差+暴力 96^4 组合，4 元变量 sage 因子分解 + GCD 求唯一解。
lesson: 自定义数学密码的破解依赖 gcd/factor + 暴力枚举；浮点误差处理是工程关键。
quality: medium
---

# 看雪 2022 KCTF 春季赛 | 第11题 虫洞末世 ydmp <<原点磨盘>>

**来源**: ctfiot.com ID 44295
**出题方**: 【一个人的浪漫】
**答案**: `lrY1314cXy2920as`
**攻破战队**: 7 队

## 题目设计

### 1. 字符映射
- 数字 (ascii 48-57): +175
- 字符 (其他): +100
- 例: 'l' → ord('l') + 100 = 208

### 2. 平方组合 (2.式)
- p = lists[2i]² * lists[2i+1] + i²
- i 是项数（从 0 开始）

### 3. 奇偶处理
- 奇数 +2
- 偶数 +1

### 4. 磨盘公倍数
- 在 3.式项数同乘的基础上相加
- 生成 2.式的公倍数 Q
- Q 作除得到最终值

### 5. 校验
- 开放首末最终值
- 6 项两两比值经 doom 函数后的值
- doom 专门扩大浮点误差

## 解题思路

### Step 1: 字符集构造
```python
s = set()
for i in string.printable:
    p = ord(i)
    if 48 <= p <= 57:
        p += 175
    else:
        p += 100
    s.add(p)
```

### Step 2: GCD + Factor
```sage
sage: gcd(m0, m1)
32
sage: factor(m0)
2^6 * 3^3 * 19 * 19301 * 5651461 * 18765679 * 452548673
sage: factor(m1)
2^5 * 13 * 29 * 181 * 353 * 641 * 929 * 270532579 * 400359419
```

### Step 3: 构造所有公因子组合
```sage
mtf = [2, 3, 19, 19301, 5651461, 18765679, 452548673]
m0f = []
for i in range(7*4*2^5):
    k = bin(i)[2:].zfill(10)
    l = [int(k[:3], 2), int(k[3:5], 2), int(k[5], 2), int(k[6], 2), 
         int(k[7], 2), int(k[8], 2), int(k[9], 2)]
    tmp = 1
    for u, v in zip(mtf, l):
        tmp *= u^v
    m0f.append(tmp)
```

### Step 4: 求交点
```sage
xa = {(m0/i + i) for i in m0f}
xb = {(m1/i + i) for i in m1f}
xa & xb
# {14109109473780244}
```

### Step 5: 暴力 4 元变量
```python
for i in s:
    for l in s:
        for j in s:
            for m in s:
                if (i**2 * l + 7**2) / (j**2 * m) == k0/k1:
                    print((i, l), (j, m))
# (197, 215) (208, 214)
```

### Step 6: 浮点容差匹配
```python
for i in s:
    for l in s:
        for j in s:
            for m in s:
                if int(((Qi / (i**2 * l + 1)) / (Qi / (j**2 * m + 36))) * 10**16) == x:
                    print((i, l), (j, m))
# (189, 224) (225, 223)
```

## 评价
看雪 2022 KCTF 春季赛压轴题，考察自定义数学密码 + 浮点误差 + 暴力枚举 + GCD/factor 因子分解。Sage 数学工具 + Python 暴力相结合，是典型的数学密码 CTF 风格。
