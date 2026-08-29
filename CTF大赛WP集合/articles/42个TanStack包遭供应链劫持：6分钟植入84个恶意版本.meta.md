---
title: 42 个 TanStack 包遭供应链劫持：6 分钟植入 84 个恶意版本
contest: 供应链安全
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags: [供应链劫持, TanStack, pull_request_target, Pwn Request, GitHub Actions缓存中毒, OIDC令牌内存提取, T1199, T1071.001, T1003.003, T1090.003, T1552, T1070.004, git-tanstack.com拼写, P2P加密, GitHub API死信]
attack_chain:
  - 初始访问: pull_request_target "Pwn Request" 模式 (T1199)
  - 持久化: GitHub Actions 缓存中毒 (T1090.003)
  - 凭证窃取: OIDC 令牌从进程内存提取 (T1003.003)
  - 远程控制: 远程 dispatch 行为 (T1071.001)
  - 拼写错误域名: git-tanstack[.]com (c 替换)
  - 会话信使网络: P2P 加密流量伪装
  - GitHub API 死信: 令牌上传至新建仓库
  - 数据隐匿于合法流量
  - 6 分钟植入 84 个恶意版本到 42 个 @tanstack/* 包
  - 1200 万次/周下载量
key_payload: 'Pwn Request / Actions 缓存 / OIDC 内存提取 / git-tanstack.com / P2P 信使 / 84 恶意版本 6 分钟 / 1200万次/周'
one_liner: TanStack 供应链劫持复盘 — Pwn Request + Actions 缓存中毒 + OIDC 内存提取 + P2P 信使 + 6分钟植入 84 个恶意版本，覆盖 npm+PyPI 多平台。
lesson: pull_request_target 是 CI 致命弱点（PR 触发可信工作流可读 secrets）；GitHub Actions 缓存是横向扩散温床；OIDC token 写内存不安全。
quality: medium
---

# 42 个 TanStack 包遭供应链劫持：6 分钟植入 84 个恶意版本

## 速读
2026 年 4-5 月大规模供应链攻击事件复盘 — TanStack 是核心受害者。

## MITRE ATT&CK 对应
| T-ID | Name | 用途 |
|------|------|------|
| T1199 | Supply Chain Compromise | 核心攻击向量 |
| T1071.001 | App Layer Protocol | C2 通信 |
| T1003.003 | OS Credential Dumping: Proc FS | OIDC 令牌提取 |
| T1090.003 | Multi-Stage Channels | P2P 数据外泄 |
| T1552 | Unsecured Credentials | 目标凭证类型 |
| T1070.004 | File Deletion | 破坏性 payload |

## 攻击时间线
- 2026-04: SAP 相关 npm 包名仿冒
- 2026-05 上旬: Checkmarx, Bitwarden, Lightning, Intercom, Trivy 供应链攻陷
- 2026-05-11: **TanStack 核心攻击** (发布管道劫持)
- 2026-05 中旬: UiPath, Mistral AI, OpenSearch, PyPI 横向扩散

## 受影响
- **npm**: 42 个 @tanstack/* 包 (84 个恶意版本, 1200万次/周)
- **PyPI**: mistralai v2.4.6, guardrails-ai v0.10.1
- **npm**: UiPath, OpenSearch 相关

## 通道技术
- 拼写错误域名: `git-tanstack[.]com` (替换 c)
- 会话信使网络 (P2P 加密流量)
- GitHub API 死信 (令牌上传至新建仓库)
