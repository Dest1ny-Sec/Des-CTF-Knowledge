---
title: DataCon2024解题报告WriteUp—软件供应链安全赛道
contest: DataCon 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [supply-chain, npm, pypi, llm, mphunter, guarddog, obs, typosquatting]
attack_chain:
  - 第一章：赛题介绍
  - 第二章：总体思路
  - 第三章：解题详述
  - MPHunter：恶意PyPI包聚类
  - npm软件包文件结构分析
  - LLM对NodeJS代码威胁评分
  - OBS（Obfuscation）代码检测
  - PyPI恶意包相似性匹配
  - 基于多源规则拓展匹配
  - 第四章：未标注新恶意包样本
  - LLM 增强数据集 Maltracker
  - guarddog规则+LLM辅助
  - 高度相似依赖识别
key_payload: LLM 评分NodeJS代码+多源规则匹配+相似性聚类
one_liner: DataCon2024软件供应链：npm/PyPI恶意包检测+LLM辅助+MPHunter
lesson: LLM辅助+规则匹配+相似性聚类是供应链安全3大武器
quality: high
---

# DataCon2024解题报告WriteUp—软件供应链安全赛道

## 题目信息
- 比赛：DataCon 2024
- 方向：软件供应链安全
- 冠军：中科院软件研究所 SecureNexusLab 战队

## 关键攻击链
### 总体思路
- **MPHunter** 流程图
- npm 软件包文件结构分析
- LLM 对 NodeJS 代码威胁评分
- OBS（Obfuscation）代码检测
- PyPI 恶意包相似性匹配
- 基于多源规则拓展匹配

### LLM 增强
- `Maltracker: A fine-grained npm malware tracker copiloted by llm-enhanced dataset`
- 使用 LLM 评分子段威胁分数

### 关键工具/论文
- guarddog（DataDog 开源）
- 通义千问 LLM
- JS-deobfuscator
- VirusTotal 查询
- Maltracker 数据集
- ASE 2023 论文：Hunting Malicious PyPI Packages with Code Clustering
- 2024 Typosquatting npm campaign
- Tea-NPM Rubbish（奇安信天问）

### 关键识别模式
- 高度相似依赖（typosquatting）
- 无意义依赖包列表
- 恶意代码片段风险评估
- 收集恶意规则 + 拓展匹配

## 评分
- quality: high（MPHunter 框架 + LLM 评分 + 相似性聚类 + 13 篇参考文献）
