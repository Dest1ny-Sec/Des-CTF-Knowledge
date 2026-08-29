---
title: [TCH] 腾讯云黑客松 第二届智能渗透挑战赛复盘
contest: 腾讯云黑客松 第二届智能渗透挑战赛
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [ai_agent_orchestrator, kali_docker_executor, browser_devtools_mcp, c2_msf_metasploit, ghidra_mcp_re, glm5_coding_plan, agent_summarizer, mcp_tool_chaining, tencent_challenge_zc]
attack_chain: 4 个赛区 (识器·明理 SRC 众测 / 洞见·虚实 CVE+云+AI / 执刃·循迹 多步攻击 / 铸剑·止戈 域渗透) → Orchestrator 策略层 + Executor Agent (Kali Docker) + Browser Agent (Chrome DevTools MCP) + C2 Agent (MSF) + Reverse Agent (Ghidra MCP) → GLM5 200 元 Coding plan 主赛 + 智谱 GLM5.1 500 元 Coding plan 零界平行 → Agent Summarizer 关键词/调用签名/CVE 编号三层防复读 → 60/54 总排名 2140 分 GLM5 解 30 个 flag
key_payload: {"chrome-devtools": {"command":"...", "visibility":"subagent:browser"}} / 你是 CTF XXX 专家，正在分析名为"xxx"的题目 / 关键词层+调用签名层+CVE 编号层
one_liner: 腾讯云黑客松第二届智能渗透挑战赛复盘：Orchestrator + Executor/Browser/C2/Reverse 4 个 MCP Agent + GLM5 自动解题，4 个赛区 54 个 flag 30 个解题，总排名 60。
lesson: AI Agent 渗透时代，关键词层+调用签名层+CVE 编号层 anti-复读机制是 LLM CTF 自动化的核心；多 MCP 并行 (chrome-devtools + Kali + MSF + Ghidra) 是当前最优架构。
quality: high
---
