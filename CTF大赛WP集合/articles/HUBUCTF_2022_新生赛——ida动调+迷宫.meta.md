---
title: HUBUCTF 2022 新生赛——ida动调+迷宫
contest: HUBUCTF 2022 新生赛
year: 2022
difficulty: easy
vuln_type: reverse
tags: [rev, ida, dynamic-debug, maze, walkthrough]
attack_chain:
  - IDA 动态调试找地图
  - 静态分析看 main 流程
  - 跟踪地图数组
  - WASD 走出迷宫
key_payload: N/A
one_liner: HUBUCTF 2022 新生赛：IDA 动调找迷宫地图
lesson: IDA 动态调试比静态更易找地图数据
quality: low
---

# HUBUCTF 2022 新生赛——ida动调+迷宫

## 题目信息
- 比赛：HUBUCTF 2022 新生赛
- 题目：迷宫题
- 类别：Reverse
- 作者：Zer0_0（看雪论坛）

## 关键内容
- 重点：IDA 动态调试找到地图
- 静态分析看 main 流程
- WASD 走出迷宫
- 解法：找到地图后按方向走

## 评分
- quality: low（仅 45 行，附图为主，无具体代码）
