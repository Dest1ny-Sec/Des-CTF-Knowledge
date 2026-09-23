---
title: 42 个 TanStack 包遭供应链劫持：6 分钟植入 84 个恶意版本
contest: 供应链安全
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags:
- 供应链劫持
- TanStack
- pull_request_target
- Pwn Request
- GitHub Actions缓存中毒
- OIDC令牌内存提取
- T1199
- T1071.001
- T1003.003
- T1090.003
- T1552
- T1070.004
- git-tanstack.com拼写
- P2P加密
- GitHub API死信
attack_chain:
- '初始访问: pull_request_target "Pwn Request" 模式 (T1199)'
- '持久化: GitHub Actions 缓存中毒 (T1090.003)'
- '凭证窃取: OIDC 令牌从进程内存提取 (T1003.003)'
- '远程控制: 远程 dispatch 行为 (T1071.001)'
- '拼写错误域名: git-tanstack[.]com (c 替换)'
- '会话信使网络: P2P 加密流量伪装'
- 'GitHub API 死信: 令牌上传至新建仓库'
- 数据隐匿于合法流量
- 6 分钟植入 84 个恶意版本到 42 个 @tanstack/* 包
- 1200 万次/周下载量
key_payload: '''Pwn Request / Actions 缓存 / OIDC 内存提取 / git-tanstack.com / P2P 信使 / 84 恶意版本 6 分钟 / 1200万次/周'''
one_liner: TanStack 供应链劫持复盘 — Pwn Request + Actions 缓存中毒 + OIDC 内存提取 + P2P 信使 + 6分钟植入 84 个恶意版本，覆盖 npm+PyPI 多平台。
lesson: pull_request_target 是 CI 致命弱点（PR 触发可信工作流可读 secrets）；GitHub Actions 缓存是横向扩散温床；OIDC token 写内存不安全。
quality: medium
full_path: 42个TanStack包遭供应链劫持：6分钟植入84个恶意版本.full.md
meta_path: 42个TanStack包遭供应链劫持：6分钟植入84个恶意版本.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '42 个 TanStack 包遭供应链劫持：6 分钟植入 84 个恶意版本。TanStack 供应链劫持复盘 — Pwn Request + Actions 缓存中毒 + OIDC 内存提取 + P2P 信使 + 6分钟植入 84 个恶意版本，覆盖 npm+PyPI 多平台。。关键路径：初始访问: pull_request_target "Pwn Request" 模式 (T1199) ...'
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/307893.html
reasoning_chain:
- npm 包名 '@tanstack/*' 6 分钟内发布 84 个恶意版本 + 1200 万周下载 → 触发点：典型供应链劫持
- 假设：不是包作者被黑而是发布管道劫持 → 动作：审计 CI workflow 文件 pull_request_target 触发器
- 观察：恶意 PR 可访问 secrets.OIDC_TOKEN → 下一步：定位 Actions 缓存中毒入口
- GitHub Actions 缓存键 hashFiles('**/pnpm-lock.yaml') 在 PR 中可控 → 触发点：缓存中毒横向扩散
- 假设：缓存中毒后下游 job 读恶意 .npmrc → 动作：grep .npmrc 看到指向 git-tanstack.com (拼写)
- 观察：git-tanstack[.]com c 替换冒充 tanstack.com → 下一步：定位 host exec 通过 OIDC
- 假设：PR 触发时 OIDC token 写入进程内存 → 动作：strings /proc/PID/mem 提取 GITHUB_TOKEN
- 观察：拿到 OIDC 后 push 到新 repo 做 GitHub API 死信 + P2P 信使分发 → 完成 84 个恶意版本
failed_attempts:
- 试图靠包作者 npm 账户被盗 → 失败：发布 token 来自 GitHub OIDC 不是 npm
- 试图审计 JS 代码 → 失败：恶意代码是 postinstall 注入运行时 fetch 拉第二阶段
key_observations:
- pull_request_target + Actions 缓存中毒是 npm/PyPI 横向扩散双杀组合
- git-tanstack[.]com c 字母替换是典型 typosquatting 在 CI 层
- OIDC token 写内存是事实，多 CI runner 中存在 strings 提取风险
- P2P 加密信使伪装合法应用层流量规避 NDR
- GitHub API 死信 (新仓库) 是凭证外带常见通道
prerequisites:
- GitHub Actions CI 模型 (pull_request_target vs pull_request)
- OIDC token 生命周期与内存驻留
- MITRE ATT&CK T1199/T1090.003/T1003.003 对应供应链/凭证攻击
---
# 42个TanStack包遭供应链劫持：6分钟植入84个恶意版本

> 原文: https://www.ctfiot.com/307893.html
> ID: 307893

攻击阶段

技术手段

对应 MITRE ATT&CK

初始访问

pull_request_target “Pwn Request” 模式

T1199 (供应链攻陷)

持久化

GitHub Actions 缓存中毒

T1090.003 (多跳通道)

凭证窃取

OIDC 令牌进程内存提取

T1003.003 (系统/服务凭证)

远程控制

远程 dispatch 行为

T1071.001 (应用层协议)

时间

攻击目标

攻击向量

2026年4月

SAP 相关包

npm 包名仿冒

2026年5月上旬

Checkmarx, Bitwarden, Lightning, Intercom, Trivy

供应链攻陷

2026年5月11日

TanStack (核心攻击)

发布管道劫持

2026年5月中旬

UiPath, Mistral AI, OpenSearch, PyPI

横向扩散

平台

受影响包

下载量/影响力

npm

42 @tanstack/* 包 (84 个恶意版本)

1200 万次/周

npm

OpenSearch 相关包

企业级用户

PyPI

mistralai v2.4.6

ML 开发者生态

PyPI

guardrails-ai v0.10.1

LLM 应用开发

npm

UiPath 相关包

RPA 开发者

通道

技术实现

情报关联

拼写错误域名

git-tanstack[.]com

标记为 critical

会话信使网络

P2P 加密流量伪装

规避网络检测

GitHub API 死信

令牌上传至新建仓库

数据隐匿于合法流量

Technique ID

Technique Name

备注

T1199

Supply Chain Compromise

核心攻击向量

T1071.001

Application Layer Protocol: Web Protocols

C2 通信

T1003.003

OS Credential Dumping: Proc Filesystem

OIDC 令牌提取

T1090.003

Multi-Stage Channels

P2P 数据外泄

T1552

Unsecured Credentials

目标凭证类型

T1070.004

File Deletion

破坏性 payload