---
title: 【出题人推荐】Datacon24 漏洞赛道冠军分享 vuln_wp 大模型赋能的漏洞自动化分析全解析
contest: DataCon
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [大模型-AI, BeautifulSoup4-HTML-parse, 多轮LLM调用, 投票机制, RAG检索增强, 函数级别切分, race-condition, SQLi, double-fetch, buff-overflow, command-injection]
attack_chain: 1. BeautifulSoup4 解析 HTML 过滤图片/2. 多轮大模型调用 + 投票机制降低误报/3. 文件大小排序 + 类型过滤 + 函数级别切分/4. 提示工程初筛种子函数/5. 不同漏洞类型 (race condition / SQLi / double-fetch / buff overflow / command injection) 不同分析策略/6. RAG + 多轮提示 + 结果投票
key_payload: 0817iotg  datacon24_vuln_wp  multi-LLM-call + voting
one_liner: DataCon 2024 漏洞分析赛道冠军（武大 0817 IOTG）大模型赋能漏洞自动化分析全套方案。
lesson: 大模型 + 投票机制 + RAG + 多轮提示是 AI 漏洞挖掘黄金组合；BeautifulSoup 解析 + 函数级切分 + 类型过滤是预处理三件套；多漏洞类型差异化策略。
quality: high
---

# 【出题人推荐】Datacon24 漏洞赛道冠军分享

## 团队
武汉大学 0817 IOTG 战队，DataCon 2024 漏洞分析赛道冠军。

## 项目地址
- https://github.com/123f321/datacon24_vuln_wp
- https://www.datacon.org.cn/competition/competitions/91/introduction

## 项目目标
利用大模型深度语义理解能力实现自动化、智能化的漏洞检测与信息提取。

## 核心特性

### 1. 多阶段处理流程
- BeautifulSoup4 解析 HTML，过滤图片等无关内容
- 精细化提示工程，信息拆分成多个输出维度
- 两次大模型调用分别判定
- 内置投票机制，自动剔除不合理或低置信度结果
- 扩展功能：版本信息、修复建议、POC/EXP 代码、图像内容

### 2. 代码分析
- 文件大小排序 + 类型过滤
- 依据编程语言函数级别切分
- 提示工程初筛种子函数
- 深度解析，针对不同漏洞类型差异化分析：
  - race condition
  - SQL injection
  - double-fetch
  - buff overflow
  - command injection

### 3. 高级特性
- RAG 技术结合多轮提示与结果投票
- 多次调用大模型降低输出不确定性
- Docker 压缩包部署
- 模块化设计

## 经验提炼
- 大模型 + 投票机制 + RAG + 多轮提示是 AI 漏洞挖掘黄金组合
- BeautifulSoup 解析 + 函数级切分 + 类型过滤是预处理三件套
- 多漏洞类型差异化策略
- 多轮 LLM 调用降低单一模型偏差
- 投票机制对抗 LLM 不确定性
- RAG 注入专业漏洞知识库
- 函数级切分避免上下文超限
- DataCon 是奇安信主办的国内顶级 CTF
- 0817 IOTG 是武大物联网安全团队
- 自动化漏洞分析是 AI 安全重要方向
