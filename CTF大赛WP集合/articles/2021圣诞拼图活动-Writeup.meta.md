---
title: 2021 圣诞拼图活动 Writeup
contest: 2021 圣诞活动
year: 2021
difficulty: easy
vuln_type: [misc_unknown, stego_image]
tags: [拼图, A-star, 数字华容道, 4x4, 16-puzzle, 自动求解, 启发式搜索, MinBinHeapq]
attack_chain: ["题目给 4x4 拼图（16 块），一块全黑，其余 15 块打乱", "随机滑动 64 步，理论上 ≤64 步可还原", "原图块对应序列: 5, 1, 6, 8, 2, 11, 7, 13, 15, 14, 3, 4, 10, 16, 12, 0", "A* 算法 + MinBinHeapq 优先队列 + 曼哈顿距离启发", "求解 72 步（>64 步时重置）", "输出方向: RRDDRDLULURRULDLDLUURRRDLLDRULDDRULUURDRULLDRRDLLLDRURULLDDRULURRDLDRURU", "步数超出时多刷几张图重试"]
key_payload: "5, 1, 6, 8, 2, 11, 7, 13, 15, 14, 3, 4, 10, 16, 12, 0"
one_liner: 16-puzzle 数字华容道 A* 自动求解
lesson: N-puzzle 是经典 AI 搜索问题；曼哈顿距离是 admissible heuristic
quality: medium
---

# 2021 圣诞拼图活动 Writeup

原文 https://www.ctfiot.com/19654.html

## 题目
- 随机生成图片，分成 4x4 = 16 块
- 一块全黑，15 块打乱
- 滑动 64 步，理论上 ≤64 步可还原
- 时间限制（< 80 步）

## 解法
### Step 1: 拼图 → 数字华容道
- 编号 1-15 + 黑块 0
- 找一张好拼的图保存

### Step 2: 序列转换
原图块对应还原后图片的序列：
```
5, 1, 6, 8, 2, 11, 7, 13, 15, 14, 3, 4, 10, 16, 12, 0
```

### Step 3: A* 自动求解
```python
# main.py
from State import Node, MinBinHeapq, Step
import time
from copy import deepcopy

class Solution():
    def __init__(self, puzzle):
        self.number = 16
        self.map = puzzle
        self.white = -1
        # 0=上 1=下 2=左 3=右
        self.direction = [[-1,0], [1,0], [0,-1], [0,1]]
        self.step_direction = [0, 1, 2, 3]
```

**算法：**
- 状态 = 4x4 矩阵
- 启发 = 曼哈顿距离
- 优先队列 (MinBinHeapq)
- 邻居 = 4 方向滑动黑块

### Step 4: 输出
```
RRDDRDLULURRULDLDLUURRRDLLDRULDDRULUURDRULLDRRDLLLDRURULLDDRULURRDLDRURU
所需步数：72
共搜索状态数：3927
搜索完成，共用时：2.6 秒
```

> 72 > 64（理论值），多刷几次拼图直到拿到好解

## 教学价值
- **N-puzzle** 是经典 AI 搜索问题
- **A* 算法 + admissible heuristic**（曼哈顿距离）是最优解
- **IDDFS / BFS** 适用于小状态空间（16! = 2e13 不可能）
- **MinBinHeapq** = Python heapq
- 数字华容道 = 15-puzzle 简化版
- 工程实战：多刷图、状态缓存、剪枝

## 选手成绩
- f11st: 246934 ms 第一
- crystal: 880427 ms
- gorgeousdays: 3104518 ms
- solazola: 3553183 ms

## 工具
- Python heapq
- A* 算法模板
- 拼图工具 / Photoshop
- 录像软件记录手动操作
