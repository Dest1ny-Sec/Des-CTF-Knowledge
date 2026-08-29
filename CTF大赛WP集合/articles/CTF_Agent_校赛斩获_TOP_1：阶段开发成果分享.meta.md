---
title: CTF Agent 校赛斩获 TOP 1：阶段开发成果分享
contest: CTF Agent
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags: [AI Agent, 三省六部制, 3核心大脑, 6子Agent, 异步记忆同步, GPT-5, sandbox, MCP工具集, 持久性, 幻觉避免, 难度判断, 全自动注册开靶机, AI爬虫]
attack_chain:
  - 校赛部署 CTF Agent 工作流, 接入 GPT-5 系列
  - 三省六部制: 3 个 agent 核心大脑 + 6 个子 agent
  - 4 个子 agent 异步同步记忆, 同时寻找解题方向
  - 1 个子 agent 做记忆上下文压缩
  - 1 个子 agent 做幻觉指出 + 全方向权重分析
  - 内置难度判断, 满级难度时启动完整流程
  - sandbox 策略, agent 缺工具时自动包管理器安装
  - 类 unix MCP 工具注册调用
  - 1 小时领先第二名 7000 分
  - 后续计划: 输入 URL 全自动注册 + 开靶机 + AI 爬虫 + API 检索 + 全自动判断
key_payload: '三省六部制 / 3 核心 + 6 子 Agent / 异步记忆同步 / GPT-5 / sandbox / MCP 类 unix / 难度判断 / 1小时领先7000分'
one_liner: CTF Agent 校赛 TOP1 经验 — 三省六部制 (3核心+6子 Agent) + 异步记忆同步 + GPT-5 + sandbox + MCP 工具集, 1 小时领先 7000 分拿下校赛。
lesson: AI Agent 解 CTF 是新方向;三省六部制 异步记忆同步 解决 Agent 同步/效率;MCP 工具注册调用是接口标准;sandbox 策略让 agent 自助。
quality: medium
---

# CTF Agent 校赛斩获 TOP 1：阶段开发成果分享

## 速读
CTF Agent 校赛 TOP1 经验分享 — 三省六部制 AI Agent 工作流。

## 三省六部制

### 3 个核心大脑
- 异步同步工作记忆 (轮次同步)
- 测试下来可增加记忆同步效率, 比同时同步快

### 6 个子 Agent
- 4 个直接寻找解题方向 (异步同步)
- 1 个记忆上下文压缩
- 1 个幻觉指出 + 全方向权重分析

## 难度判断
- 满级难度 → 启动完整三省六部制
- 低级难度 → 直接单 Agent

## 工具
- sandbox 策略: agent 缺工具时自动包管理器安装
- MCP 工具集: 类 unix 接口 + 工具注册 + 调用接口
- 持久性 Prompt 分化
- 工具调用: 借鉴 cc 思路

## 战绩
- 校赛 1 小时领先第二名 7000 分
- 最终 TOP1 (但 pwn 没打, 后停了)

## 后续计划
- 输入 CTF 网站 URL 全自动注册 + 开靶机
- AI 爬虫 + API 检索
- 全自动判断
