---
title: Mini Shai-Hulud 蠕虫式投毒事件分析 (TanStack/Mistral/Squawk/OpenSearch/Guardrails AI/UiPath)
contest: 事件分析
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags: [供应链投毒, npm 投毒, PyPI 投毒, GitHub Actions, OIDC token, ATT&CK T1195.002]
attack_chain: |
  1. 事件: 2026-05-12 凌晨 3 点墨菲安全检测到 TanStack 42 个 @tanstack/* npm 包被投毒 (GitHub Actions 攻击)
  2. 受害范围: TanStack 42 包 84 版本 + Mistral AI 多个 SDK + Squawk + OpenSearch + Guardrails AI + UiPath
  3. 攻击链 (TanStack):
     - pull_request_target 工作流在 fork PR 上执行了不可信代码
     - 攻击者通过 GitHub Actions cache poisoning 把恶意内容写进主分支发布流程恢复的缓存
     - 发布流程有写权限, 恶意代码从 runner 进程内存中提取 OIDC token, 向 npm registry 发起发布请求
     - 看起来仍来自可信的 GitHub Actions/OIDC 发布链路
  4. 典型注入点 1 (package.json):
     "optionalDependencies": {"@tanstack/setup": "github:tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c"}
  5. 典型注入点 2 (@tanstack/setup 生命周期脚本): 触发后下载并执行远程 Python artifact
  6. ATT&CK T1195.002 (Compromise Software Supply Chain) + T1552.001 (Credentials In Files) + T1041 (Exfiltration Over C2)
  7. 防御建议:
     - 检查包名 + 版本 + 锁文件, 不要按 namespace 粗暴判断
     - 限制 pull_request_target 触发条件 (拒绝 first-time contributor)
     - 限制发布流程权限 (仅 main branch push 触发)
     - 检查 GitHub Actions cache 内容 (缓存完整性校验)
key_payload: |
  # 受影响样本 (2026-05):
  # npm: 42 @tanstack/* 包 + @mistralai/mistralai* + @squawk/mcp + @opensearch-project/opensearch + @uipath/*
  # PyPI: mistralai@2.4.6 + guardrails-ai@0.10.1
  
  # 攻击链:
  # 1. pull_request_target 工作流在 fork PR 上执行不可信代码
  # 2. GitHub Actions cache poisoning
  # 3. 从 runner 内存提取 OIDC token
  # 4. 用 OIDC token 向 npm registry 发起发布请求
  
  # 注入 1 (package.json):
  "optionalDependencies": {
    "@tanstack/setup": "github:tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c"
  }
  
  # 注入 2 (@tanstack/setup 生命周期脚本):
  # install/postinstall 触发后下载并执行远程 Python artifact
  
  # 防御:
  # - 限制 pull_request_target 拒绝 first-time contributor
  # - 限制发布流程权限
  # - 检查 GitHub Actions cache 内容
  # - 检查锁文件
one_liner: 2026-05 Mini Shai-Hulud 蠕虫式供应链投毒事件分析: TanStack + Mistral + Squawk + OpenSearch + Guardrails AI + UiPath 多生态被投毒。
lesson: |
  - GitHub Actions cache poisoning 是新型供应链攻击面
  - OIDC token 提权让攻击看起来来自可信发布链路
  - 不要按 namespace 粗暴判断 (TanStack 受害 ≠ 所有 @tanstack/* 包)
  - pull_request_target 触发条件需要严格限制 (first-time contributor 拒绝)
  - 跨生态攻击: npm + PyPI 同步影响
  - 墨菲安全持续监测供应链投毒
quality: medium
---

# Mini Shai-Hulud 蠕虫式投毒事件分析

> 来源: ctfiot.com 307839 - 墨菲安全

## 事件概述

2026-05-12 凌晨 3 点，墨菲安全检测到 **TanStack 42 个 @tanstack/* npm 包被投毒**。恶意包在安装阶段执行约 2.3 MB 的混淆载荷，窃取 CI/CD、云平台和开发机凭据，并尝试利用拿到的发布权限继续污染维护者名下的其他包。

## 影响范围

| 生态 | 受影响样本 | 说明 |
|------|------------|------|
| npm / TanStack | @tanstack/react-router, router-core, router-cli, vue-router 等 42 包 84 版本 | 周下载量超千万级 |
| npm / Mistral AI | @mistralai/mistralai, mistralai-azure, mistralai-gcp | AI SDK 进入攻击面 |
| PyPI / Mistral AI | mistralai@2.4.6 | 跨 Python 生态 |
| npm / Squawk | @squawk/mcp, weather, flightplan | 航空数据 + MCP 包 |
| npm / OpenSearch | @opensearch-project/opensearch 3.5.3, 3.6.2, 3.7.0, 3.8.0 | 搜索基础设施 |
| PyPI / Guardrails AI | guardrails-ai@0.10.1 | import 时触发 |
| npm / UiPath | 多个 @uipath/* 包 | 企业自动化 |

> @tanstack/query*, table*, form*, virtual*, store **未受影响** — 排查时按具体包名+版本+锁文件，不要按 namespace 粗暴判断。

## 攻击链

1. **`pull_request_target` 工作流在 fork PR 上执行不可信代码**
2. **GitHub Actions cache poisoning**：把恶意内容写进会被主分支发布流程恢复的缓存
3. **发布流程有写权限**，从 runner 进程内存中提取 OIDC token，直接向 npm registry 发起发布请求
4. **结果**：恶意版本看起来仍来自可信的 GitHub Actions/OIDC 发布链路

## 典型注入点 1：package.json

```json
"optionalDependencies": {
  "@tanstack/setup": "github:tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c"
}
```

URL 看起来指向 TanStack/router，但对应 commit 实际来自 fork 网络中的孤立提交。

## 典型注入点 2：@tanstack/setup 生命周期脚本

postinstall 触发后下载并执行远程 Python artifact。

## 评价

2026-05 重大供应链投毒事件，亮点是：
- **GitHub Actions cache poisoning** 是新型攻击面
- **OIDC token 提权** 让攻击看起来来自可信发布链路
- **跨生态同时感染** (npm + PyPI)
- 周下载量超千万级，影响面巨大

适用读者：DevSecOps 工程师 / 供应链安全研究员 / 蓝队应急响应
