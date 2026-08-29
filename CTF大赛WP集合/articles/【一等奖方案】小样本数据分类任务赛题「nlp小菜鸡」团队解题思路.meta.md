---
title: 小样本专利数据分类 CCF BDCI 2022 一等奖方案
contest: CCF-BDCI
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [NLP, few-shot, patent-classification, Nezha, ERNIE-Gram, Bert-for-patents, AWP, SWA, multi-sample-dropout, pseudo-label, model-ensemble, CCF-BDCI]
attack_chain:
  - 数据：958 条专利训练 + 20839 测试 + 20890 复赛，36 类脱敏标签，长尾分布
  - 短文本（title+assignee+abstract 拼接 ≤ 657 字符）
  - 5 个模型 Nezha / Ernie-Gram-zh / Ernie-3.0-xbase-zh / Bert-for-patents / Chinese-RoBERTa-wwm-ext-large
  - 阶段 1：通用预训练 → 阶段 2：领域预训练（用测试集增量 MLM）→ 阶段 3：领域微调
  - Bert-for-patents 翻译为英文后 5 段输入（title+assignee+head+body+tail）
  - 优化：AWP Embedding+model 双扰动 + SWA 局部最优集成 + Multi-Sample Dropout
  - 集成：加权平均（Ernie-gram/xbase 权重小）+ 二阶段伪标签（先训练集训练模型集成生成第一阶段伪标签）
  - 第二阶段伪标签：训练集 + 初赛 70% 伪标签 + 复赛 70% 伪标签训练 Nezha 10 折集成
  - 最终 5 折 Ernie-Gram-zh + 伪标签数据训练
  - 复赛 macro F1 = 0.61387745 排名第一
key_payload: 'macro F1 = 0.61387745 第一名, 模型 < 2GB'
one_liner: 5 个中文+英文预训练模型集成 + 领域预训练 + AWP/SWA + 伪标签，小样本专利分类 CCF BDCI 2022 一等奖。
lesson: 小样本学习的关键是数据增强（伪标签）+ 模型多样性（5 个不同架构）+ 鲁棒性优化（AWP+SWA+MSD）。
quality: high
---

# 第十届 CCF 大数据与计算智能大赛 2022 (CCF BDCI) - 小样本数据分类任务 - nlp小菜鸡 团队 一等奖

**赛题地址**: https://datafountain.cn/competitions/582
**团队**: nlp小菜鸡（华南师大朱金乘 + 北京交大包刚林 + 指导老师穆丽伟）

## 摘要
- 任务：专利数据 36 类分类，958 训练 / 20839 初赛测试 / 20890 复赛测试
- 评价指标：macro F1
- 三阶段范式：通用预训练 → 领域预训练 → 领域微调
- 模型集成：5 个预训练模型加权平均 + 二阶段伪标签
- 最终：5 折 Ernie-Gram-zh + 伪标签训练
- 复赛 0.61387745 第一

## 数据分析
- title+assignee+abstract 拼接长度 ≤ 657（短文本）
- 标签分布长尾（部分类仅 4-5 条）
- 标签语义未知（脱敏）
- 难点：数据少 + 标签不均衡 + 标签语义未知 + 提交次数有限

## 5 个模型架构
### 1. Nezha-large
- 华为诺亚方舟 Bert 改进版
- 用初赛测试集领域增量预训练
- Nezha + Multi-Sample Dropout + Linear
- 单模型 macro F1 = 0.61

### 2. Chinese-RoBERTa-wwm-ext-large
- Whole Word Masking + 取消 NSP + max_len=512
- 基础结构 + AWP + SWA
- 单模型 0.595

### 3. Bert-for-patents
- Google 在 1 亿+专利上训练
- 数据翻译为英文，5 段输入（title/assignee/head/body/tail）
- Bert-for-patents + MultiDropout + Linear + SWA
- 单模型 0.605

### 4. Ernie-gram-zh
- 百度 n-gram 显式掩码 MLM
- Ernie-gram-zh + GRU + Multi-Sample Dropout + Linear + SWA
- 单模型 0.597

### 5. Ernie-3.0-xbase-zh
- 文心 Ernie 3.0
- 同 Ernie-gram 结构 + SWA
- 单模型 0.599

## 优化技术
1. **领域预训练**：用比赛测试集无监督数据，Nezha-large-wwm 增量 MLM 预训练
2. **AWP 对抗训练**：Embedding 层 + model 双扰动
3. **SWA**：保存多个局部最优点集成
4. **加权平均融合**：Ernie-gram/xbase 权重小
5. **二阶段伪标签**：第一阶段集成模型生成，第二阶段 Nezha 10 折生成

## 其他尝试（未融合）
- Prompt 模型（标签语义未知）
- 文本增强（随机替换/交换/删除/回译）
- TTA（测试时增强）

## 参考
- [1] NEZHA: Neural Contextualized Representation for Chinese Language Understanding
- [2] ERNIE-Gram: Pre-Training with Explicitly N-Gram Masked Language Modeling
- [3] ERNIE 3.0: Large-scale knowledge enhanced pre-training
- [4] RoBERTa: A Robustly Optimized BERT Pretraining Approach
- [5] Adversarial Distributional Training for Robust Deep Learning
- [6] Automatic Brain Tumor Segmentation using CNNs with TTA
- [7] Pre-train, prompt, and predict: A systematic survey of prompting methods

## 评价
NLP 小样本学习的标杆方案。核心是"模型多样性 + 鲁棒性增强 + 伪标签数据扩展"三板斧。模型 < 2GB 易落地生产。
