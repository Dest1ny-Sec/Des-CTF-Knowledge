---
title: 看雪·2023 KCTF 年度赛 - 热身题《失控的 AI》解析
contest: 看雪 KCTF 2023
year: 2023
difficulty: easy
vuln_type: [reverse, misc_math]
tags: [韦达定理, 二次方程, z3, factordb, 因式分解, x96dbg, 逆推]
attack_chain: ["x96dbg 跟踪程序到 v15/v16 比较处", "识别约束：v15+v16=117738, v15*v16=3457897337", "factordb / 韦达 / z3 多种解法得 56101 和 61637", "按 v15<=v16 顺序输入 56101-61637 拿 flag"]
key_payload: "56101-61637"
one_liner: 韦达定理逆推 + 多种解法的 reverse 入门题
lesson: 两个未知数 + 两组和积约束 → 一元二次方程根；z3 / factordb / 韦达三选一即可
quality: high
---

# 看雪·2023 KCTF 年度赛 - 热身题《失控的 AI》

原文 https://www.ctfiot.com/133666.html

## 题目
**输入两个整数**（格式 `%lld-%lld`），需要满足：
- `v15 > 0 && v16 > 0`
- `v15 <= v16`
- `v15 + v16 == 117738`
- `v15 * v16 == 3457897337`

## 4 种解法

### 解法一：韦达定理逆定理
设 v15、v16 是方程 `x² - 117738x + 3457897337 = 0` 的根
解得 `x = 56101` 或 `61637`
按 `v15 <= v16` 顺序：`56101-61637`

### 解法二：factordb 因式分解
- `A*B = 0xCE1B5379 = 3457897337`
- `A+B = 0x1CBEA = 117738`
- 查 factordb.com 得 `56101 × 61637`
- 输入 `56101-61637`

### 解法三：z3 求解
```python
from z3 import *
x, y = Int('x'), Int('y')
s = Solver()
s.add(x + y == 117738)
s.add(x * y == 3457897337)
s.add(x <= y)
s.add(x > 0, y > 0)
assert s.check() == sat
print(s.model())   # x=56101, y=61637
```

### 解法四：C++ 穷举
```cpp
for (long long a = 1; a <= 117738; ++a) {
    long long b = 117738 - a;
    if (a * b == 3457897337) { cout << a << "-" << b; break; }
}
```

## 教学价值
- reverse 入门题，逆向就是找关键比较
- "已知和+积求两数" 经典代数模型
- AI 写因式分解代码节省时间（作者也提到这一点）
- z3 / sympy / factordb 三大逆向工具

## 后续题目
第二题《CN 星际基地》Reverse 难度升级（已收录 7 队提交）
