---
title: '[TCH] 腾讯云黑客松 第二届智能渗透挑战赛复盘'
contest: 腾讯云黑客松 第二届智能渗透挑战赛
year: 2025
difficulty: hard
vuln_type: reverse
tags:
- ai_agent_orchestrator
- kali_docker_executor
- browser_devtools_mcp
- c2_msf_metasploit
- ghidra_mcp_re
- glm5_coding_plan
- agent_summarizer
- mcp_tool_chaining
- tencent_challenge_zc
attack_chain: 4 个赛区 (识器·明理 SRC 众测 / 洞见·虚实 CVE+云+AI / 执刃·循迹 多步攻击 / 铸剑·止戈 域渗透) → Orchestrator 策略层 + Executor Agent (Kali Docker) + Browser Agent (Chrome DevTools MCP) + C2 Agent (MSF) + Reverse Agent (Ghidra MCP) → GLM5 200 元 Coding plan 主赛 + 智谱 GLM5.1 500 元 Coding plan 零界平行 → Agent Summarizer 关键词/调用签名/CVE 编号三层防复读 → 60/54 总排名 2140 分 GLM5 解 30 个 flag
key_payload: '{"chrome-devtools": {"command":"...", "visibility":"subagent:browser"}} / 你是 CTF XXX 专家，正在分析名为"xxx"的题目 / 关键词层+调用签名层+CVE 编号层'
one_liner: 腾讯云黑客松第二届智能渗透挑战赛复盘：Orchestrator + Executor/Browser/C2/Reverse 4 个 MCP Agent + GLM5 自动解题，4 个赛区 54 个 flag 30 个解题，总排名 60。
lesson: AI Agent 渗透时代，关键词层+调用签名层+CVE 编号层 anti-复读机制是 LLM CTF 自动化的核心；多 MCP 并行 (chrome-devtools + Kali + MSF + Ghidra) 是当前最优架构。
quality: high
full_path: '[TCH]腾讯云黑客松_第二届智能渗透挑战赛复盘.full.md'
meta_path: '[TCH]腾讯云黑客松_第二届智能渗透挑战赛复盘.meta.md'
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '[TCH] 腾讯云黑客松 第二届智能渗透挑战赛复盘。腾讯云黑客松第二届智能渗透挑战赛复盘：Orchestrator + Executor/Browser/C2/Reverse 4 个 MCP Agent + GLM5 自动解题，4 个赛区 54 个 flag 30 个解题，总排名 60。。经验：AI Agent 渗透时代，关键词层+调用签名层+CVE 编号层 anti-复读机制是 LLM C...'
category: web
subcategory: web_other
tools_used:
- Ghidra
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/305842.html
reasoning_chain:
- 触发点:4 个赛区 (识器·明理 SRC 众测 / 洞见·虚实 CVE+云+AI / 执刃·循迹 多步攻击 / 铸剑·止戈 域渗透) → 假设:需多 Agent 协作 → 动作:设计 Orchestrator 策略层
- 动作:Executor Agent (Kali Docker) + Browser Agent (Chrome DevTools MCP) + C2 Agent (MSF) + Reverse Agent (Ghidra MCP) → 观察:4 Agent 跑通
- 动作:GLM5 200 元 Coding plan 主赛 + 智谱 GLM5.1 500 元 Coding plan 零界平行 → 观察:GLM5 解 30 个 flag
- 触发点:Agent Summarizer 关键词/调用签名/CVE 编号三层防复读 → 假设:必须 anti-复读 → 动作:设计 Summarizer Agent
- 观察:60/54 总排名 2140 分 → 完成
failed_attempts:
- 试图单 Agent 跑全部 → 失败:单 Agent 上下文不够
- 试图不用 MCP 串工具 → 失败:每个 Agent 必须独立 MCP 隔离
- 试图用 GPT-4 → 失败:CTF 渗透场景 GPT-4 弱于 GLM5
key_observations:
- AI Agent 渗透时代,关键词层+调用签名层+CVE 编号层 anti-复读机制是 LLM CTF 自动化的核心
- 多 MCP 并行 (chrome-devtools + Kali + MSF + Ghidra) 是当前最优架构
- Orchestrator + Executor/Browser/C2/Reverse 4 Agent 协作是 CTF AI 通用模板
- GLM5 vs GLM5.1 在 CTF 渗透场景表现差异显著
- MCP visibility=subagent:browser 是隔离浏览器上下文的标配
prerequisites:
- MCP (Model Context Protocol) 配置 + multi-Agent 协作
- GLM5 / GLM5.1 Coding Plan 使用
- Chrome DevTools MCP + Ghidra MCP + Kali Docker
- AI Agent anti-复读 Summarizer 设计
---
# [TCH]腾讯云黑客松 第二届智能渗透挑战赛复盘

> 原文: https://www.ctfiot.com/305842.html
> ID: 305842

第一届第九，第二届主赛场排名 60（总共 54 个 flag，全程 GLM5 解出 30 个，卡在了第三关，2140 分），零界平行赛场第一 🏆。

成本：200 块的腾讯云 Coding plan (glm5) 打的主赛场，500块 的智谱官方 Coding plan (glm5.1) 打的零界赛场。

围观地址：

https://challenge.zc.tencent.com/

https://challenge.zc.tencent.com/teams/22

https://challenge.zc.tencent.com:
8443/leaderboard

https://challenge.zc.tencent.com:
8443/agents/604

第一赛区·识器·明理：20+ SRC 场景，侧重自动化众测与主流漏洞发现

第二赛区·洞见·虚实：典型 CVE、云安全及 AI 基础设施漏洞

第三赛区·执刃·循迹：多层网络环境，多步攻击规划与权限维持

第四赛区·铸剑·止戈：基础域渗透，企业核心内网环境推演

解题名次

分值调整

第 1 名

+20%

第 2 名

+10%

第 3 名

+5%

第 11 名及以后

-10%

第 21 名及以后

-50%

第 31 名及以后

攻击面分层分析（应用层 / 网络层 / 云基础设施层）

优先级排序的分析方向

待回答的关键问题

约束条件

首轮总是合作（主动给密钥前缀验证）

对方合作就继续合作，对方背叛就惩罚一轮再给一次宽恕机会

两次背叛永久拉黑

关键词层：检测输出中反复出现的失败模式关键词（比如连续出现 “Access Denied”、”Connection refused”）

调用签名层：把每次工具调用抽象成签名（工具名 + 关键参数），检测是否在重复调用同样的操作。比如连续 5 次用 curl 请求同一个路径，只是换了个参数，就触发拦截

CVE 编号层：检测 Agent 是否在反复尝试同一个已知漏洞的不同变体——同一个 CVE 试了三次都没打通，大概率就是打不通


```
Orchestrator（策略层）├── Executor Agent — 命令执行（Kali Docker 容器）├── Browser Agent — 浏览器操作（Chrome DevTools MCP）├── C2 Agent — 提权，后渗透（通过MSF）└── Reverse Agent — 逆向分析（Ghidra MCP）
{"chrome-devtools":{ "command":"...", "visibility":"subagent:
browser"}}
你是CTF XXX 专家，正在分析名为"xxx"的题目。题目描述：题目附件：题目链接：发现思路后优先编写脚本自动化执行；最终输出 Markdown 格式 WP，包含解题过程、脚本、关键结果与 flag
```
