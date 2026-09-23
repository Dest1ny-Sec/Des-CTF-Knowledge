---
title: Ichunqiu 云境 —— Tsclient Writeup
contest: Ichunqiu 云境
year: 2022
difficulty: hard
vuln_type: web_unknown
tags:
- MSSQL
- Potato 提权
- incognito
- Tsclient
- 镜像劫持
- krbrelayup
- 约束委派
attack_chain: '|'
key_payload: '|'
one_liner: MSSQL 弱口令 → Potato 提权 → incognito 模拟 token 拿 \tsclientC 凭据 → 镜像劫持/krbrelayup 提权 → DCSync 带走 DC。
lesson: '|'
quality: high
full_path: Ichunqiu云境_——_Tsclient_Writeup.full.md
meta_path: Ichunqiu云境_——_Tsclient_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Ichunqiu 云境 —— Tsclient Writeup。MSSQL 弱口令 → Potato 提权 → incognito 模拟 token 拿 \tsclientC 凭据 → 镜像劫持/krbrelayup 提权 → DCSync 带走 DC。。经验：|
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/85253.html
reasoning_chain:
- 入口 MSSQL 弱口令 → 触发点：sa 空口令 / 默认口令
- 动作：MSSQL shell xp_cmdshell → 观察：当前机器不在域内
- 假设：提权到 system → 动作：GetClsid.ps1 暴力枚举 Potato Clsid → 观察：拿到有效 Clsid + 命令执行
- 动作：导出 SAM/SYSTEM/Security → 假设：解 Administrator NTLM
- 观察：administrator 2caf35bb4c5059a3d50599844e2b9b1f → 动作：psexec 139 横向（外网不开 445）
- 假设：找到 RDP 登录的 john 用户 → 动作：msf incognito 模块模拟 john token
- 动作：net use 看到 tsclientC 共享 → 假设：rdp 残留
- 动作：cat tsclientC\credential.txt → 观察：xiaorang.lab\Aldrich / Ald@rLMWuy7Z!#
- 假设：横向 172.22.8.46 → 动作：smbpasswd.py 远程改过期密码 → 111qqq...
- 假设：xiaorang.lab\Aldrich 是普通用户 → 动作：镜像劫持 magnify.exe → 提权 system
- 动作：mimikatz 抓 win2016$ 机器账户 → 假设：处于 Domain Admins 组 → DCSync DC01 → 完成
failed_attempts:
- f-secure lab 等其他 impersonate token 工具 → 失败：只有 MSF incognito 能用
- CrackMapExec 默认 RDP 模块 → 失败：扫不出有效 RDP
- 约束委派走非标准路径 → 失败：要先有 service ticket
key_observations:
- MSSQL 弱口令 + xp_cmdshell 是经典入口链
- MSF incognito 是模拟 token 的最稳定工具
- tsclient 共享是 RDP 残留凭据常见位置
- 镜像劫持 magnify.exe + 可写 Image File Execution Options 是经典提权
- 机器账户在 Domain Admins 组 → 直接 DCSync
prerequisites:
- MSSQL 提权（xp_cmdshell）+ JuicyPotato
- MSF incognito token 模拟 + 镜像劫持（IFEO）
- 约束委派（S4U2Self / S4U2Proxy）
---
# Ichunqiu云境 —— Tsclient Writeup

> 原文: https://www.ctfiot.com/85253.html
> ID: 85253

Ichunqiu云境 —— Tsclient Writeup

Author:小离-xiaoli

0x1 Info

• Tag: MSSQL，Privilege Escalation，Kerberos，域渗透，RDP

0x2 Recon

1. Target external ip 47.92.82.196

2. nmap

3. MSSQL 弱口令爆破，爆破出有效凭据，权限为服务账户权限（MSSQLSERVER） sa:
1qaz!QAZ

0x3 入口点 MSSQL – 172.22.8.18

• 前言，该机器不在域内

1. 直接MSSQL shell（这里做完了忘记截图了..）

2. 提权，这里直接获取Clsid暴力怼potato（前面几个clsid是用不了的）

修改GetClsid.ps1，添加执行potato

Potato和GetClsid.ps1

执行GetClsid.ps1

获取到有效clsid以及命令执行结果

3. 导出SAM，SYSTEM，Security

解出凭据，用administrator + psexec 139横向（外网没有开445）就能获取到 flag01 administrator 2caf35bb4c5059a3d50599844e2b9b1f

4. qwinsta和端口连接看到有机器rdp过来

5. 这边使用administrator psexec后上msf（system权限），使用incognito模块，模拟至john（本人实测，只有msf的incognito能完成后续操作，f-secure lab等其他的模拟令牌工具没成功）

6. 使用john的token执行 net use 看到 \tsclientC 共享

7. 直接获取 \tsclientC 下面的 credential.txt，同时提示 hijack image (镜像劫持) xiaorang.labAldrich:
Ald@rLMWuy7Z!#

• 快进，略过搭建代理过程

1. CME 扫描 172.22.8.0/24，有三个机器提示密码过期了

2. 测试一下 DC01 88端口是否开启（测是否域控），DC01为域控

3. smbpasswd.py 远程修改一下过期密码，改成111qqq…

4. ldapshell.py 验证，登录域成功

5. CME 枚举 RDP，显示能登录进入 172.22.8.46（用CME官方的RDP模块不会扫出有效RDP凭据，这边自己写了一个基于xfreerdp的CME模块） XiaoliChan/CrackMapExec-Extension

0x4 域渗透 – 入口 – 172.22.8.46

1. 登录进入，查看到 xiaorang.labAldrich 不是这台机器的管理员，只是普通用户

• 提权，两种方法

Priv-ESC1：镜像劫持提权（常规）

Get-ACL查看到任何用户都可以对注册表 “HKLM:
SOFTWAREMicrosoftWindows NTCurrentVersionImage File Execution Options” 进行写入，创建操作

创建一个劫持magnify.exe（放大镜）的注册表，执行CMD.exe

锁定用户

点击放大镜

提权至system

Priv-ESC2：krbrelayup提权

域普通权限用户在域内机器，直接带走（非常规，推荐）

5. 快进mimikatz，获取到当前机器的机器账户 win2016$

xiaorang.labWIN2016$ 4ba974f170ab0fe1a8a1eb0ed8f6fe1a

0x5 域渗透 – DC Takeover

• 两种方法

1. 观察 WIN2016$ 的组关系，发现处于 Domain Admins 组，直接使用 Dcsync 带走 DC01 （过程略）

2. 约束委派（非常规）

Bloodhound收集域信息，分析，发现存在约束委派

使用 getST.py 进行约束委派攻击

带走 DC01

0x6 Outro

• 个人比较手残，不懂C，incognito那个部分，按照作者解释来说，常规是要自己写一个impersonate token的工具（还是没脱离MSF.. TAT）

原文始发于微信公众号（Gcow安全团队）：Ichunqiu云境 —— Tsclient Writeup

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