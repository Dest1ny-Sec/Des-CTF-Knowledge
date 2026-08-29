---
title: Ichunqiu 云境 - Delegation Writeup
contest: 春秋云境 (ichunqiu)
year: 2022
difficulty: medium
vuln_type: [auth_bypass, misc_unknown]
tags: [AD, Active-Directory, NTLM, hash, delegation, SPN, kerberoast, 内网, 域控]
attack_chain: ["环境三台机器 fileserver/DC01/win19 + 域 xiaorang.lab", "admin/123456 登录", "导出 Administrator NTLM hash aad3b435b51404ee:aad3b435b51404ee + ba21c629d9fd56aff10c3e826323e6ab", "MACHINE.ACC hash 917234367460f3f2817aa4439f97e636", "Delegation 攻击链"]
key_payload: "Administrator::aad3b435b51404eeaad3b435b51404ee:ba21c629d9fd56aff10c3e826323e6ab:::"
one_liner: AD 域 Delegation 攻击 + NTLM hash 抓取
lesson: Active Directory 域渗透中 NTLM 哈希传递（PTH）+ 委派攻击是常见链；aad3b435... 是空 LM hash 标志
quality: medium
---

# Ichunqiu 云境 - Delegation Writeup

原文 https://www.ctfiot.com/84759.html

## 环境
- `172.22.4.19  fileserver.xiaorang.lab`
- `172.22.4.7   DC01.xiaorang.lab`（域控）
- `172.22.4.45  win19.xiaorang.lab`
- 域 `xiaorang.lab`
- 初始账号 `admin / 123456`

## 抓到的哈希
```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:ba21c629d9fd56aff10c3e826323e6ab:::
$MACHINE.ACC:aad3b435b51404eeaad3b435b51404ee:917234367460f3f2817aa4439f97e636
```

注：`aad3b435b51404ee` 是空 LM hash 标志（pass-the-hash 兼容性）。

## 知识点
- **Pass-the-Hash (PtH)**：用 NTLM hash 直接认证，不需要明文
- **Delegation 攻击**：
  - Unconstrained Delegation：服务可被委派到任意机器 → 抓 TGT
  - Constrained Delegation：服务只能委派到指定 SPN → S4U2Self/S4U2Proxy
  - Resource-Based Constrained Delegation (RBCD)：基于资源的约束委派
- **Kerberoasting**：请求 SPN 的 TGS，离线爆破
- **NTLM Relay**：中继 NTLM 认证到其他服务

## 春秋云境 / ATT&CK 链
1. 拿到 web shell / webshell
2. mimikatz / SharpChrome 抓浏览器密码
3. secretsdump 导出 SAM
4. PtH 到其他机器
5. 找 SPN / RBCD 配置错误
6. 拿到域控

## 教学价值
- 国内"春秋云境"、"ATT&CK 实战"系列都模拟 AD 域环境
- 哈希 `aad3b435...` 出现意味着 LM hash 已禁用，留 NTLM
- Delegation 是域渗透高级技术，从 2018 年起成为比赛热门
