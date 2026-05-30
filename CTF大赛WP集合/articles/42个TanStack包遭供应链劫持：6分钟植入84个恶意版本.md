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