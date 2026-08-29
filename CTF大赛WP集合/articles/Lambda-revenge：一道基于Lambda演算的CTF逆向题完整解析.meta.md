---
title: Lambda-revenge: XCTF 2022 Lambda 演算逆向题
contest: XCTF
year: 2022
difficulty: hard
vuln_type: reverse
tags: [Lambda 演算, Church 编码, 线性代数, 矩阵求逆, Church 数字, Church 布尔, 函数式编程]
attack_chain: |
  1. 题目: XCTF 2022 高难度逆向题，flag = XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}
  2. 数据结构: Exp (Lambda 表达式节点) + Closure (闭包) + Env (环境/变量绑定)
  3. 核心函数: val() (求值) + encode() (整数 → Church 数字) + churchBool() (布尔判断)
  4. flag 分 11 组，每组 3 字节 (33 字节 = 11×3)
  5. 每组有独立的验证表达式 chall[i]
  6. Church 编码基础:
     - λx.x (恒等函数)
     - λx.λy.x (K combinator，返回第一个参数 → True)
     - λx.λy.y (返回第二个参数 → False)
     - λf.λx.x (Church 数字 0)
     - λf.λx.f(x) (Church 数字 1)
     - λf.λx.f(f(x)) (Church 数字 2)
  7. 验证逻辑: 把整数编码成 Church 数字 + 矩阵和结果编码成 Church 数字的列表 (Pair 构造) + 验证结果是 Church 布尔值
  8. 求解思路: 写出每组 chall[i] 对应的 Church 表达式 → 还原为整数方程组 → 线性代数 (矩阵求逆) 求出原始 3 字节
key_payload: |
  # Church 数字:
  0 = λf.λx.x           # 不应用 f
  1 = λf.λx.f(x)        # f 应用 1 次
  2 = λf.λx.f(f(x))     # f 应用 2 次
  n = λf.λx.f^n(x)      # f 应用 n 次
  
  # Church 布尔:
  T = λx.λy.x           # True: 选第一个
  F = λx.λy.y           # False: 选第二个
  
  # Pair (True/False 选择器):
  pair = λa.λb.λs.s(a)(b)  # s = T 返回 a, s = F 返回 b
  
  # 攻击: 把 11 组 Church 表达式 → 还原为线性方程组 → 矩阵求逆
  # XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}
one_liner: XCTF 2022 Lambda-revenge: 把 flag 分 11 组 3 字节，编码成 Church 数字 + 矩阵 + Church 布尔值，逆向需要还原 Lambda 演算 + 线性代数。
lesson: |
  - Church 编码是函数式编程基础: λ 演算里数字/布尔/列表全是高阶函数
  - Church 数字: λf.λx.f^n(x) 表示 n
  - Church 布尔: T = λx.λy.x, F = λx.λy.y
  - Pair: λa.λb.λs.s(a)(b) 配合 T/F 取出 a 或 b
  - 还原 Church 表达式为整数方程: 关键是求值每个 Church 数字对应的"应用次数"
  - 11 组 3 字节 + 矩阵 = 11 套线性方程组，可用 numpy.linalg.solve 或 sympy.Matrix.solve 求逆
  - Lambda 演算逆向是 XCTF 高难度 Reverse 的标志
quality: high
---

# Lambda-revenge: XCTF 2022 Lambda 演算逆向题

> 来源: ctfiot.com 282968

## 题目概况

- **XCTF 2022** 高难度逆向题
- 涉及技术：**Lambda 演算**、**Church 编码**、**线性代数**、**逆向工程**
- Flag: `XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}`

## 数据结构

```c
typedef struct Exp Exp;
typedef struct Closure Closure;
typedef struct Env Env;

struct Closure {
    Exp *expr;       // 表达式
    Env *env;        // 环境
};
struct Env {
    // 变量绑定
};
```

## 核心函数

- `val()`: 求值函数
- `encode()`: 整数 → Church 数字
- `churchBool()`: Church 布尔值判断
- `main()`: flag 分 11 组，每组 3 字节，每组有独立验证表达式 `chall[i]`

## Church 编码基础

| 概念 | 编码 | 含义 |
|------|------|------|
| 恒等 | `λx.x` | 返回自身 |
| 常 K | `λx.λy.x` | True: 返回第一个 |
| 鸽 | `λx.λy.y` | False: 返回第二个 |
| 数字 0 | `λf.λx.x` | 不按按钮 |
| 数字 1 | `λf.λx.f(x)` | 按 1 次 |
| 数字 2 | `λf.λx.f(f(x))` | 按 2 次 |
| Pair | `λa.λb.λs.s(a)(b)` | T 取 a, F 取 b |

## 攻击链

1. **分析 chall[i]** — 写出每组 Church 表达式
2. **求值** — 把 Church 数字还原为"f 的应用次数"
3. **构造方程组** — 11 组 × 3 字节 = 33 字节，对应 11 套 3 元线性方程
4. **矩阵求逆** — `numpy.linalg.solve` 或 `sympy.Matrix.solve` 求出原始字节值
5. **拼 flag** — 把 11 组 3 字节拼成完整 flag

## flag 例子

`XCTF{M4tRI1|i||l|Il|I1X_A5_YC0mb}`

注意：M4tRI1 = Matrix，Y = Y-axis，C0mb = combination — 暗示用矩阵求逆（Matrix + Y axis + combination）。

## 评价

XCTF 2022 高难度逆向题，结合 **函数式编程理论**（Lambda 演算、Church 编码）和**线性代数**（矩阵求逆）。

**亮点：**
- 题目把 flag 编码成 Church 数字后隐藏在 lambda 表达式里
- 求解需要把 Church 表达式逐个求值，还原为整数
- 11 套线性方程组 → 矩阵求逆是核心
- 题目名字"Lambda-revenge"暗示"lambda + matrix 复仇"

**适用读者：** 函数式编程爱好者 / 线性代数研究者 / 高级逆向工程师
