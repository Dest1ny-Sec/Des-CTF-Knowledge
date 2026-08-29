---
title: 基于 TPU 平台实现人群密度估计 CCF BDCI 2022 二等奖方案
contest: CCF-BDCI
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [TPU, crowd-density-estimation, VGG, CSRNet, MCNN, grid-search, INT8-quantization, BMODEL, MAE-RMSE-NAE, CCF-BDCI]
attack_chain:
  - 4 个预训练模型 CANNet/CSRNet/MCNN/VGG，FP32 vs INT8 BModel
  - 测试 FP32 vs INT8 在 (576,768)~(2048,2048) 输入的得分
  - CANNet 权重无法加载，跳过
  - 选 VGG（综合分 186.74/177.64）> MCNN > CSRNet
  - 网格搜索: 模型输入 [112×112, 144×144, 144×192, 224×224, 288×384, 576×768] + Batch Size [1,2,4,8,16] + 缩放 [224~2048]
  - 结论: Batch Size 影响小，固定 = 1
  - 选小图片尺寸 (288×384 ~ 768×768) + 小模型输入 (144×192) + Batch=1
  - INT8 量化 (200 张训练图 lmdb 校准) 分数反而低 → 放弃 INT8
  - 最终: FP32 BModel + 缩放 (288×384, 768×768) + 模型输入 144×192 + Batch=1
  - B 榜第二
key_payload: 'VGG FP32 + 缩放 (288×384, 768×768) + 模型输入 144×192 + B 榜 #2'
one_liner: 2022 CCF BDCI TPU 人群密度估计：4 模型网格搜索 + INT8 量化对比 + 选 VGG FP32 144×192 拿 B 榜第二。
lesson: 网格搜索是模型选择标准方法；FP32 vs INT8 量化在精度敏感任务中 INT8 不一定更好。
quality: high
---

# 基于 TPU 平台实现人群密度估计 CCF BDCI 2022 二等奖方案

**来源**: ctfiot.com ID 123438
**赛题地址**: https://www.datafountain.cn/competitions/583
**团队**: 深藏blue（天翼云科技周伟伟、黄宇生、林瑞玉）

## 任务
- 人群密度估计 + 计数（计算机视觉）
- 4 个预训练模型: CANNet / CSRNet / MCNN / VGG
- TPU 推理平台，FP32 / INT8 BModel
- 评价指标: MAE + RMSE + NAE (精度) + TIME (速度)

## 4 模型对比（FP32/INT8 同条件）

| 模型 | FP32 | INT8 |
|------|------|------|
| CANNet | / | / |
| CSRNet | 68.34 | 65.19 |
| MCNN | 169.76 | 161.49 |
| VGG | 186.74 | 177.64 |

→ 选 **VGG**

## 网格搜索
- 模型输入: [112×112, 144×144, 144×192, 224×224, 288×384, 576×768]
- Batch Size: [1, 2, 4, 8, 16]
- 图片缩放范围: [minH, minW, maxH, maxW] = [224,224,768,768] / [288,384,1024,1024] / [288,384,2048,2048] / [432,576,1536,1536] / [576,768,2048,2048]

## 结论
- Batch Size 影响小（Batch 推理耗时与单张几乎线性）→ 固定 = 1
- 模型输入一定，图片尺寸增加 → 精度↑但小图数量增加 → 速度分降低更快
- 较小模型输入对精度影响小
- **最终**: 缩放 (288×384, 768×768) + 模型输入 144×192 + Batch=1 + FP32

## 量化实验
- 准备 lmdb 校准数据集（200 张训练图）
- INT8 量化后综合分降低 → **放弃 INT8**

## 数据分析
- 图片宽度 500-5000，高度 ≤ 4000
- 宽高比 1.5
- 大图分割推理（避免下采样导致特征丢失）
- 不缩放至统一尺寸，缩放到区间 (288×384, 768×768)

## 评价
2022 CCF BDCI TPU 平台工程实践：模型选择 + 网格搜索 + 量化对比，最终 B 榜第二。是嵌入式 AI 部署经典案例。
