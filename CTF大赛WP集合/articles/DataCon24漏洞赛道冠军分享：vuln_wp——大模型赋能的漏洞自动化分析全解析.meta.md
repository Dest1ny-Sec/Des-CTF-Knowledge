---
title: DataCon24漏洞赛道冠军分享：vuln_wp——大模型赋能的漏洞自动化分析全解析
contest: DataCon 2024 漏洞分析赛道冠军
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [llm, rag, prompt-engineering, voting, race-condition, sql-injection, double-fetch, buff-overflow]
attack_chain:
  - 0817iotg战队完整框架
  - BeautifulSoup4解析HTML过滤图片
  - 提示工程多维度输出+两次LLM调用
  - 内置投票机制剔除低置信度结果
  - 扩展：版本/修复建议/POC/EXP/图像
  - 文件大小排序+类型过滤+按语言函数切分
  - 提示工程初步筛查+种子函数深度解析
  - 不同漏洞类型(race condition/SQLi/double-fetch/buff-overflow/cmd-injection)不同策略
  - RAG技术+多轮提示+结果投票
key_payload: RAG + 多次LLM调用 + 投票 + 漏洞类型策略
one_liner: DataCon24冠军 vuln_wp：LLM+RAG+投票+多类型漏洞策略
lesson: 漏洞分析LLM框架：HTML解析+提示工程+投票+RAG
quality: high
---

# DataCon24漏洞赛道冠军分享：vuln_wp——大模型赋能的漏洞自动化分析全解析

## 题目信息
- 比赛：DataCon 2024
- 方向：漏洞分析
- 冠军：0817iotg 战队
- 项目：vuln_wp
- 仓库：https://github.com/123f321/datacon24_vuln_wp

## 关键攻击链
### 1. 文章信息提取
- BeautifulSoup4 解析 HTML
- 精细化提示工程多维度输出
- 两次 LLM 调用分别判定
- 内置投票机制校验
- 扩展：版本/修复建议/POC/EXP/图像

### 2. 代码漏洞分析
- 文件大小排序+类型过滤
- 按编程语言函数级切分
- 提示工程初步筛查种子函数
- 深度解析：race condition / SQLi / double-fetch / buff_overflow / cmd_injection
- 复杂漏洞 RAG + 多轮提示 + 投票

### 3. 工程化
- Docker 压缩包快速部署
- 完整源码 + 测试数据
- 多种漏洞类型示例

## 评分
- quality: high（LLM + RAG + 投票 + 多漏洞类型策略完整框架，开源）
