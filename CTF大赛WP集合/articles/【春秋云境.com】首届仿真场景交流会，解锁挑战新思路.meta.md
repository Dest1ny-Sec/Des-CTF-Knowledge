---
title: 【春秋云境.com】首届仿真场景交流会，解锁挑战新思路
contest: 春秋云境 2022 网鼎杯决赛
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [春秋云境, 内网渗透, Jenkins, Gitlab, Oracle, Windows提权, CVE-2022-26923, 永恒之蓝, XR Shop]
attack_chain:
  - Privilege 靶场: XR Shop 内网渗透 4 个 flag
  - 步骤 1: web 路径备份源码审计 → Jenkins 漏洞 → 拿下 Jenkins
  - 步骤 2: Jenkins 信息收集发现 Gitlab → 发现 Oracle 数据库信息
  - 步骤 3: 攻击 Oracle → XR-0923 主机 → 账号登录
  - 步骤 4: Windows 提权 → 域内 ACE 特权滥用 → 域控
  - 第二靶场 (网鼎杯 2022 决赛复盘): 4 个 flag
  - 步骤 1: 端口扫描 → WordPress 80 端口 → 后台弱口令 → getshell
  - 步骤 2: 内网信息收集 → 永恒之蓝主机 → metasploit 利用
  - 步骤 3: 提取账号密码 → 拿下域内机器 → 敏感 ACE
  - 步骤 4: CVE-2022-26923 域控提权
key_payload: 'Jenkins+Gitlab+Oracle+XR-0923+域控 CVE-2022-26923'
one_liner: 春秋云境仿真场景 2 个靶场复盘：XR Shop 4 flag 内网渗透 + 网鼎杯 2022 复盘 WordPress+永恒之蓝+CVE-2022-26923。
lesson: 内网渗透标准流程: 端口扫描 → Web 弱口令 → 内网信息收集 (Jenkins/Gitlab) → 数据库 (Oracle/MSSQL) → 提权 → 横向 → 域控；CVE-2022-26923 是 ADCS 域控提权。
quality: medium
---

# 【春秋云境.com】首届仿真场景交流会，解锁挑战新思路

## 概览
- **来源**: ctfiot 167308 (春秋云境)
- **类型**: 内网渗透仿真靶场
- **难度**: ⭐⭐⭐

## Privilege 靶场 (XR Shop)
- 4 个 flag
- 步骤:
  1. web 备份源码审计 → Jenkins 系统攻击
  2. Jenkins 信息收集 → 发现 Gitlab
  3. Gitlab 发现 Oracle 数据库信息
  4. 攻击 Oracle → 登录 XR-0923
  5. Windows 提权 → 域内 ACE 特权滥用
  6. 拿下域控

## 第二靶场 (2022 网鼎杯决赛复盘)
- 4 个 flag
- 步骤:
  1. 端口扫描 → WordPress 80 端口
  2. 后台弱口令 → getshell
  3. 内网信息收集 → 永恒之蓝主机
  4. metasploit-framework 利用
  5. 提取账号密码 → 域内其他机器
  6. 敏感 ACE → 拿下域内另一台
  7. **CVE-2022-26923** 域控提权

## CVE-2022-26923 (ADCS 域控提权)
- Active Directory 证书服务权限提升
- 允许低权限用户将机器账户的 dNSHostName 属性设置为 DC
- 申请 DC 证书 → 身份验证
- 影响: Windows Server 2012-2022

## 教学
- 内网渗透标准流程: 端口扫描 → Web → 数据库 → 提权 → 横向 → 域控
- Jenkins+Gitlab 是企业内网常见高价值目标
- Oracle 数据库 TNS 协议攻击
- Windows 提权: PrintNightmare, HiveNightmare, ADCS
- 春秋云境提供仿真场景练手
