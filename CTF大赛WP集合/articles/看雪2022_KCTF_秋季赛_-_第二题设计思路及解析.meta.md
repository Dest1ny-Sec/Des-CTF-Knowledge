---
title: 看雪2022 KCTF 秋季赛 | 第二题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: medium
vuln_type: reverse
tags: [62进制, 大数计算, 数论, 自定义大数库, BigNumMul/BigNumDiv, gmpy2.invert]
attack_chain: 14位key按-拆2部分→62进制转大数sn1/sn2→num=10^19初始大数→循环0x200000次对sn1+sn2累加→模num结果与原数相差1时flag增加1→BigNumMul/BigNumDiv干扰计算31次时增加4→注册成功
key_payload: "sbase=0-9A-Za-z;num=10^19 cnt=32;31*x=1 mod n;31*y=n-1 mod n;x=gmpy2.invert(31,n);key=ZSxZerX4xb4-jyvP7x12lI7"
one_liner: KCTF2022秋Q2《盗贼作乱》：62进制key+大数+31*x=1mod n数论+BigNumMul/Div干扰计算
lesson: 大数模逆用gmpy2.invert；自定义大数库的隐藏干扰点（第31次触发）
quality: high
---

# 看雪2022 KCTF 秋季赛 | 第二题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q2《盗贼作乱》

**难度**：围观3000+人

**题目设计**：
- 14位key按`-`切2部分，62进制转大数sn1/sn2
- 初始大数 num = (b62)IRtzloZ6iuB = 10^19
- 要求 sn1<num, sn2<num, sn1<sn2
- 循环0x200000次对sn1/sn2累加，模num结果与原数相差1时flag++
- flag==10时注册成功
- **BigNumMul/BigNumDiv干扰计算**：flag>0时第31次循环再flag+=4

**算法原型**：
- num范围内数n，自我累加cnt次后，模num结果与原数相差1
- 累加cnt-1次结果应为 num*x+1 或 num*x-1
- n<num → n*(cnt-1) < num*(cnt-1) → x<=cnt-1
- 检测范围(1,cnt)中的x

**EXP**：
```python
sbase = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def baseConv(a):
    s = ''
    l = len(sbase)
    while a > 0:
        s += sbase[a % l]
        a //= l
    return s

def calc(num, cnt):
    for x in range(1, cnt):
        if (num * x + 1) % (cnt - 1) == 0:
            n = (num * x + 1) // (cnt - 1)
            print(n, x, "+1", baseConv(n))
        if (num * x - 1) % (cnt - 1) == 0:
            n = (num * x - 1) // (cnt - 1)
            print(n, x, "-1", baseConv(n))

calc(10**19, 32)
# 3870967741935483871 12 +1 ZSxZerX4xb4
# 6129032258064516129 19 -1 jyvP7x12lI7
```

**关键解算**（31次循环触发+4）：
```python
import gmpy2
n = 10**19
# 31*x = 1 (mod n)
x = gmpy2.invert(31, n)
# 31*y = n-1 (mod n)
for i in range(100):
    if (i*n - 1) % 31 == 0:
        break
y = (i*n - 1) // 31
print(baseConv(x) + '-' + baseConv(y))
# ZSxZerX4xb4-jyvP7x12lI7
```

**key**：`ZSxZerX4xb4-jyvP7x12lI7`

**核心技巧**：
- 大数模逆 `gmpy2.invert(a, n)`
- 62进制自定义字母表
- 自定义大数库的隐藏干扰点分析（BigNumMul/Div第31次）

**质量评估**：高（gmpy2.invert解法 + key完整）
