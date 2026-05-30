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
