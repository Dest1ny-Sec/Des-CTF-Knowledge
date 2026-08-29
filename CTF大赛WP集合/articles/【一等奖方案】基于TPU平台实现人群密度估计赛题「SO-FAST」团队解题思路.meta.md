---
title: 【一等奖方案】基于TPU平台实现人群密度估计赛题「SO-FAST」团队解题思路
contest: 2022 CCF BDCI SO-FAST TPU 密度估计
year: 2022
difficulty: hard
vuln_type: misc_math
tags: [CCF BDCI, TPU, CSRNet, INT8量化, 4N Batch, 推理加速, 算能BM1684, 人群密度估计, A/B榜第一]
attack_chain:
  - 第十届 CCF 大数据与计算智能大赛
  - 队伍: SO-FAST (宋礼/柯嵩宇/包锴楠) 京东/上交/西南交大
  - 任务: CSRNet 在 TPU (算能 BM1684) 平台部署
  - Step 1: 模型选择 CSRNet (FP32 vs INT8 对比)
  - Step 2: INT8 量化 (FP32 精度高但慢, INT8 平衡)
  - Step 3: 量化图片选择 (NWPU-Crowd 第 178 张, 大规模人群+广色差)
  - Step 4: 推理加速 1: 图片尺寸变换 (1 vs 4 张, 0.5s/张)
  - Step 4: 推理加速 2: 4N Batch (INT8+INT32 关系, 4 张一次 0.27s)
  - Step 5: BM1684 平台部署实测
  - 综合评分 score = (250-MAE)*0.2 + (500-RMSE)*0.1 + (0.4-NAE)*200 + (2-time)*100
  - A 榜 229.73 第一, B 榜 263.78 第一
key_payload: 'CSRNet + INT8 + 4N Batch + 2x2 图片划分 + BM1684 部署第一'
one_liner: 2022 CCF BDCI TPU 密度估计冠军 SO-FAST：CSRNet + INT8 量化 + 4N Batch + 2×2 图片划分 + 推理加速。
lesson: TPU 部署 5 步流程: 模型选择→INT8 量化→量化图片筛选→推理加速 (尺寸+4N Batch)→部署实测; 4N Batch 利用 INT8+INT32 关系 4 张一次推理降一半时间。
quality: high
---

# 【一等奖方案】基于TPU平台实现人群密度估计赛题「SO-FAST」团队解题思路

## 概览
- **来源**: ctfiot 124006
- **赛事**: 2022 CCF BDCI TPU 密度估计冠军
- **战队**: SO-FAST (宋礼 京东 / 柯嵩宇 上交 / 包锴楠 西南交大)
- **难度**: ⭐⭐⭐⭐

## 5 步实施方案

### Step 1: 预训练模型评估
- 测试多个预训练模型, 选择 CSRNet

### Step 2: 模型量化
- FP32 vs INT8 对比
- FP32 精度高但推理慢
- **INT8 量化**: 平衡精度+速度

### Step 3: 量化数据集筛选
- NWPU-Crowd 第 178 张图 (大规模人群+广色差)
- 提升量化后精度

### Step 4: 推理加速
**优化 1: 图片尺寸变换**
- 1 张图: 推理精度 14.9 分, 时间 1.07s
- 4 张图 (2×2): 精度 7.11 分, 时间 0.5s
- 总体 +50 分

**优化 2: 4N Batch 模式**
- INT8 + INT32 关系
- 4 张图一次推理
- 0.51s → 0.27s (降一半)

### Step 5: 部署实测
- 算能 BM1684 TPU 平台
- A 榜 229.73 第一
- B 榜 263.78 第一

## 综合评分公式
```
score = (250 - MAE) * 0.2
      + (500 - RMSE) * 0.1
      + (0.4 - NAE) * 200
      + (2 - time) * 100
```

## 工具
- 算能 Sophon Toolkit
- CSRNet (CVPR 2018) 预训练
- 量化工具链
- BM1684 TPU

## 教学
- TPU 部署 5 步流程: 选模型→量化→筛选数据→加速→部署
- 4N Batch 利用 INT8+INT32 数据类型关系, 4 张图一次推理
- 量化数据集筛选比传统随机选取精度提升明显
