---
title: 用 GPT-5.4 单挑 NCTF 团队赛，成功解出91.7%的题目
contest: NCTF 2026
year: 2026
difficulty: mixed
vuln_type: misc_unknown
tags: [GPT-5.4, AI解题, Codex Agent, Trae, NCTF 2026, AI取代初级安全]
attack_chain: 搬运题目附件给AI→AI自主在沙盒搭建环境→objdump/Androguard/gdb自动逆向→失败重试+AI自我反思→22/24题
key_payload: "Codex + GPT-5.4;Trae + GPT-5.4;objdump;baksmali;Androguard;webhook.site"
one_liner: GPT-5.4单挑NCTF 2026团队赛：24题解22道（91.7%）排名34/915
lesson: AI解题能力已超越大部分初级安全研究员；CTF出题方需做"抗AI"设计
quality: low
---

# 用 GPT-5.4 单挑 NCTF 团队赛，成功解出91.7%的题目

**赛事**：NCTF 2026（南京邮电大学）

**成绩**：24道题解出22道（91.7%），排名34/915

**实验设置**：
- 工具：Codex + GPT-5.4 / Trae + GPT-5.4
- 作者不写一行代码、不做任何手动分析
- 不装IDA/JADX等反编译工具
- 不装任何MCP、不给技术指导

**三步工作流**：
1. **搬运**：把题目描述、附件原封不动扔给AI
2. **装死**：绝对不给任何"试试看XX算法"提示
3. **重试**：失败时回复三类："重试"、"换个思路再试下"、"这么简单你都做不出来？再想想"

**AI自主行为**：
- 自动搭建本地漏洞环境
- objdump反汇编、baksmali/Androguard APK逆向
- 自动gdb调试 + 改exp
- 失败中自我反思、自我迭代
- 网上找webhook.site接收XSS flag

**对比结论**：
- 国产大模型（GLM/Qwen/Kimi）打不过GPT-5.4
- 同一GPT-5.4下，Codex > Trae（Agent工程能力差异）

**行业冲击**：
- 91.7%解题率证明"只会搬运题目"的人能拿好名次
- 大量初级安全研究员、渗透测试员饭碗受冲击
- 出题方对AI能力评估不足
- 传统"套壳题"、"标准算法变种题"在GPT-5.4面前犹如裸奔

**质量评估**：低（个人感想文章，无技术细节）
