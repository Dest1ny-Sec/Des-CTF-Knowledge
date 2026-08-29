---
title: 2022 USTC Hackergame WriteUp 0x02
contest: 2022 USTC Hackergame (中科大)
year: 2022
difficulty: medium
vuln_type: [misc_math, reverse, web_unknown, crypto_unknown]
tags: [Hackergame, 15-puzzle, A-star, 数字华容道, 量子计算, 旅行商, RSA-教学, Z3, angr, IDA, LaTeX, APlayer]
attack_chain: ["15-puzzle: 数字华容道 + A* 求解 80 步内还原", "量子计算 1+1=?: 提示板扰动 → 反推", "旅行商 NP-hard: 小规模穷举 / 启发式", "RSA 教学: 课本 p,q,e → d = inverse(e, (p-1)*(q-1))", "IDA 静态分析: 找 main 函数 main_loop 状态机还原", "angr 符号执行: 找路径条件解迷宫 / 表达式", "Z3 SMT 求解: 线性方程组 / 不等式组", "LaTeX 渲染: 注入 RCE / 读取文件"]
key_payload: "flag{it_works_like_magic_e2a53e77e7}"
one_liner: USTC Hackergame 0x02 量子计算 + 拼图 + RSA + 旅行商 + LaTeX 渲染
lesson: USTC 信安赛题目趣味性强 + 知识面广；量子计算 / 旅行商 / LaTeX 都是冷门考点
quality: medium
---

# 2022 USTC Hackergame WriteUp 0x02

原文 https://www.ctfiot.com/71319.html

## flag 速览
```
flag{it_works_like_magic_e2a53e77e7}
```

## 题目概览

### 1. 15-puzzle 数字华容道
```python
class Board:
    def __init__(self):
        self.b = [[i*4+j for j in range(4)] for i in range(4)]
    def _blkpos(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] == 15:
                    return (i, j)
    def move(self, moves):
        for m in moves:
            i, j = self._blkpos()
            if m == 'L': self.b[i][j] = self.b[i][j-1]; self.b[i][j-1] = 15
            elif m == 'R': self.b[i][j] = self.b[i][j+1]; self.b[i][j+1] = 15
            elif m == 'U': ...
```
- A* 算法 + 曼哈顿距离启发 → 80 步内解出

### 2. 量子计算 1+1=?
- 提示板噪声
- 反推可能值

### 3. 旅行商 (TSP)
- 小规模数据穷举
- 或启发式最近邻 / 2-opt

### 4. RSA 教学
```python
p = 课本值
q = 课本值
e = 65537
d = pow(e, -1, (p-1)*(q-1))
m = pow(c, d, n)
```

### 5. 静态分析
- IDA 找 main 函数
- 还原 main_loop 状态机

### 6. angr 符号执行
```python
import angr
p = angr.Project('./binary', auto_load_libs=False)
sm = p.factory.simulation_manager(p.factory.entry_state())
sm.explore(find=lambda s: b'flag' in s.posix.dumps(s.stdout.fileno()))
```

### 7. Z3 求解
```python
from z3 import *
x, y, z = Ints('x y z')
s = Solver()
s.add(x + y == 10)
s.add(x * y == 24)
s.add(x > 0, y > 0)
print(s.check())
```

### 8. LaTeX 渲染 RCE
- 注入 `\write18{...}` 或 `\input{/etc/passwd}`

## 教学价值
- **Hackergame** 是中科大信安学院办的校内赛 → 现在也是国内公开赛
- 题目覆盖面广：math / physics / cs / security
- 入门用：**15-puzzle + A***, **RSA 课本**, **Z3**
- 进阶用：**angr 符号执行**, **LaTeX 注入**

## 工具
- angr (符号执行)
- Z3 (SMT solver)
- IDA Pro
- SageMath
- pwntools
