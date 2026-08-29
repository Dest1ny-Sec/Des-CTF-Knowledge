---
title: MBSD Cybersecurity Challenges 2023 参加記 (IPFactory 战队)
contest: MBSD Cybersecurity 2023
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [Web 爬虫, 漏洞扫描, 自动化诊断, 团队参加, IPFactory 学校, delikitchup]
attack_chain: |
  1. 比赛性质: 不是传统 CTF 夺旗，而是"网络安全诊断"竞赛
  2. 阶段 1: 创建一个爬虫，掌握 Web 应用规模（URL 数量、表单、API 等）
  3. 阶段 2: 用爬虫在云环境生产站点扫描 MBSD{flag} 标识
  4. 评分标准: 检测率（找到 flag 数量）+ 不访问非指定域 + 不访问被禁页面
  5. 允许修改第一次提交的工具源码（但要重新提交）
  6. 诊断结果按运营指定格式输出
  7. 终审: 东京线下展示 + 演示文稿
  8. 团队: IPFactory 学校 (日本) 4 名一年级学生组成 "delikitchup" 队
     - hatomato / Chisenon / sango / ERUTONE
  9. 历届 IPFactory 战队成绩: 之前有前辈拿过冠军
key_payload: |
  # 比赛时间表:
  # - 团队报名/题目分发: 2023-07-19 ~ 2023-11-13 (4 个月)
  # - 解释材料+工具提交: 2023-11-13
  # - 一次审查结果: 2023-11-20
  # - 性能审查: 2023-11-27 ~ 2023-12-01
  # - 最终审查: 2023-12-15 东京线下
  
  # 比赛要求:
  # - 创建 Web 爬虫
  # - 提交工具、源码、安装步骤、操作说明
  # - 性能审查时用工具找 MBSD{flag} 格式
  # - 检测率高 + 不访问非指定域 + 不访问被禁页面
one_liner: MBSD Cybersecurity Challenges 2023 — 日本 IPFactory 学校 4 名大一学生 "delikitchup" 队的 Web 爬虫 + 漏洞扫描参加记。
lesson: |
  - MBSD 是日本知名的"网络安全诊断"竞赛，与传统 CTF 不同
  - 重点是 Web 爬虫 + 漏洞扫描的"工程能力"，不是 single-flag 解题
  - 比赛分两阶段: 工具开发 (4 个月) + 性能审查 + 最终审查
  - 性能评分标准: flag 检测率 (MBSD{...} 格式) + 合规性 (不访问非指定域)
  - IPFactory 是日本信息科学专门学校的安全研究社团
  - "delikitchup" = delicious + ketchup (前辈赢过 IPFactory 队名)
quality: low
---

# MBSD Cybersecurity Challenges 2023 参加記

> 来源: ctfiot.com 153514 - IPFactory Advent Calendar 2023 第 20 天

## 比赛概况

- **比赛名**: MBSD Cybersecurity Challenges 2023 (MBSD 网络安全挑战)
- **比赛性质**: 与传统 CTF 不同，是"网络安全诊断"竞赛
- **主办**: MBSD (日本三井物産セキュアディレクション株式会社)
- **时间**: 2023-07-19 ~ 2023-12-15 (5 个月)

## 比赛内容

### 一次审查

创建一个 Web 爬虫，掌握 Web 应用规模（URL 数量、表单、API 等）。提交：
- 工具
- 源代码
- 安装步骤
- 操作说明（开发工程师视角）

### 性能审查

- 在云环境生产站点扫描 `MBSD{flag}` 格式的标识
- 评分标准：检测率 + 合规性
- 不允许访问非指定域 → 减分
- 不允许访问被禁页面 → 减分
- 工具获取的 flag 仅输出
- 第一次提交的工具源码可修改（修改后重新提交）
- 诊断结果按运营指定格式输出

### 最终审查

- 东京线下
- 演示文稿
- 介绍性能审查成绩

## 团队介绍

**IPFactory** (日本信息科学专门学校) — 4 名一年级学生：
- **hatomato** (鸠本)
- **Chisenon** (奇塞农)
- **sango** (三哥)
- **ERUTONE** (埃鲁通)

**队名**: `delikitchup` (delicious + ketchup) — 命名者 sango 独断决定。

> 上一次是 IPFactory 大四学生（入学时已经是校友）赢过，这次新人想积累经验。

## 评价

MBSD Cybersecurity Challenges 是日本知名的"实战化"安全竞赛，**与夺旗 CTF 不同**：
- 重点是**工程能力**（写爬虫、写扫描器）
- 比赛周期长（5 个月）
- 评分标准是**检测率 + 合规性**，不是单 flag 解答

适合**网络安全服务方向**的团队而非 CTF 战队。中文圈对应"补天杯"或"企业 SRC 漏洞挖掘"性质的竞赛。
