---
title: 【春秋云境.com】首届仿真场景交流会，解锁挑战新思路
contest: 春秋云境 2022 网鼎杯决赛
year: 2024
difficulty: medium
vuln_type: web_unknown
tags:
- 春秋云境
- 内网渗透
- Jenkins
- Gitlab
- Oracle
- Windows提权
- CVE-2022-26923
- 永恒之蓝
- XR Shop
attack_chain:
- 'Privilege 靶场: XR Shop 内网渗透 4 个 flag'
- '步骤 1: web 路径备份源码审计 → Jenkins 漏洞 → 拿下 Jenkins'
- '步骤 2: Jenkins 信息收集发现 Gitlab → 发现 Oracle 数据库信息'
- '步骤 3: 攻击 Oracle → XR-0923 主机 → 账号登录'
- '步骤 4: Windows 提权 → 域内 ACE 特权滥用 → 域控'
- '第二靶场 (网鼎杯 2022 决赛复盘): 4 个 flag'
- '步骤 1: 端口扫描 → WordPress 80 端口 → 后台弱口令 → getshell'
- '步骤 2: 内网信息收集 → 永恒之蓝主机 → metasploit 利用'
- '步骤 3: 提取账号密码 → 拿下域内机器 → 敏感 ACE'
- '步骤 4: CVE-2022-26923 域控提权'
key_payload: '''Jenkins+Gitlab+Oracle+XR-0923+域控 CVE-2022-26923'''
one_liner: 春秋云境仿真场景 2 个靶场复盘：XR Shop 4 flag 内网渗透 + 网鼎杯 2022 复盘 WordPress+永恒之蓝+CVE-2022-26923。
lesson: '内网渗透标准流程: 端口扫描 → Web 弱口令 → 内网信息收集 (Jenkins/Gitlab) → 数据库 (Oracle/MSSQL) → 提权 → 横向 → 域控；CVE-2022-26923 是 ADCS 域控提权。'
quality: medium
full_path: 【春秋云境.com】首届仿真场景交流会，解锁挑战新思路.full.md
meta_path: 【春秋云境.com】首届仿真场景交流会，解锁挑战新思路.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '【春秋云境.com】首届仿真场景交流会，解锁挑战新思路。春秋云境仿真场景 2 个靶场复盘：XR Shop 4 flag 内网渗透 + 网鼎杯 2022 复盘 WordPress+永恒之蓝+CVE-2022-26923。。关键路径：Privilege 靶场: XR Shop 内网渗透 4 个 flag → 步骤 1: web 路径备份源码审计 → Jenkins 漏洞 → 拿下 Jenkins...'
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/167308.html
reasoning_chain:
- '靶场 Privilege: XR Shop → 触发点: 公网 web + 内网渗透综合'
- '假设: 备份源码可能有漏洞 → 动作: 扫 web 路径找 .zip/.bak 备份'
- '观察: Jenkins 备份源码 → 审计后 RCE Jenkins → 拿第一台机 shell'
- '假设: 内网有 gitlab + oracle → 动作: 信息收集发现 gitlab + Oracle 数据库连接信息'
- 攻击 oracle → 登入 XR-0923 账号 → Windows 提权 → 拿域内主机
- 敏感 ACE → 横向移动拿第二台域机 → CVE-2022-26923 → 拿域控
failed_attempts:
- '试图直接拿 flag → 失败: 是靶场综合题, 必须走完整渗透链路才能拿 flag'
key_observations:
- 靶场综合题 = 备份源码审计 + Jenkins RCE + 信息收集 + 数据库利用 + 域渗透
- '内网渗透路径: web 入口 → 备份源码 → 中间件漏洞 → 信息收集 → 数据库 → 域内 → 域控'
- Windows 特权滥用 (敏感 ACE) 是横向移动的关键, ACL 审计是核心
- CVE-2022-26923 是 AD CS 提权到域控的高危漏洞, 必须及时打补丁
prerequisites:
- Jenkins/GitLab RCE 与备份源码审计
- Oracle 数据库利用 + 默认/弱口令字典
- Windows AD 域渗透 (ACL/ACE/PKI 提权)
- 内网代理转发 (frp/nps/socks)
---
# 【春秋云境.com】首届仿真场景交流会，解锁挑战新思路

> 原文: https://www.ctfiot.com/167308.html
> ID: 167308

春秋云境.com自上线以来，便吸引了业界广泛的瞩目，数以万计的爱好者们在此平台不断磨砺技能、精进技艺。春秋云境.com融合了大量真实网络安全案件、大型攻防演练等实战场景，将独特剧情与技术要点巧妙融合，为初学者打造了一个充满挑战与趣味的实战平台。同时，我们也十分注重用户的互动交流体验，期待与您一同探讨、进步。为此，我们精心挑选了两个用户反馈最为集中的场景进行深入探讨，以期为大家提供更专业、实用的解题思路。

Privilege

web信息收集、命令执行、Oracle Getshell

在这个靶场中，您将扮演一名资深黑客，被雇佣来评估虚构公司 XR Shop 的网络安全。您需要通过渗透测试逐个击破公司暴露在公网的应用，并通过后渗透技巧深入 XR Shop 的内部网络，寻找潜在的弱点和漏洞，并通过滥用 Windows 特权获取管理员权限，最终并获取隐藏在其内部的核心机密。

解题思路

对web路径的备份源码进行探测，并对备份源码进行简单的审计，发现可能存在有漏洞的地方，进而在对Jenkins系统展开攻击。拿下Jenkins之后

对其展开信息收集便可发现Gitlab，

在到gitlab中发现存在有ORACLE数据库相关信息，

转而在攻击ORACLE。在通过信息收集发现的账号登录XR-0923，

最后在经过Windows系统提权即可拿下XR-0923，最后在发现域内存在特权滥用

最终拿下域控

该靶场为 2022 第三届网鼎杯决赛内网靶场复盘。完成该挑战可以帮助玩家了解内网渗透中的代理转发、内网扫描、信息收集、特权提升以及横向移动技术方法，加强对域环境核心认证机制的理解，以及掌握域环境渗透中一些有趣的技术要点。该靶场共有 4 个 flag，分布于不同的靶机。

解题思路

对给定的IP进行端口探测，发现存在有一个wordpress网站位于80端口，对其进行信息收集能够发现其后台存在有弱口令，进入后台即可成功getshell

待getshell之后对内网进行信息收集可以发现到一台机器存在有永恒之蓝，使用metasploit-framework即可成功利用

在对永恒之蓝这台主机进行信息收集后便可以发现其中存在有大量的账号与密码

紧接着在这些账号密码的帮助之下便可拿下域内的另一台机器，在域内信息收集之后发现存在有较为敏感的ACE,

在利用这条敏感的ACE帮助之下即可拿下除域控外的另一台机器，

最终在利用CVE-2022–26923成功拿下域控。

我们深知在练习的过程中，您可能会遇到一些疑问或思考。同时我们特地邀请了春秋云境.com的技术专家在微信群【春秋云境.com🪐大本营】进行深入交流，共同探讨解题思路和网络安全实战技巧！

这是一场集结智慧与热情的盛会，是一次技术与实战深度对话的机遇。我们诚挚邀请您体验这场技术盛宴，与技术专家们共同感受实战魅力！

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]