---
title: HackTheBox Stocker WriteUp
contest: HackTheBox Stocker
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [htb, pentest, nmap, nginx, ffuf, vhost-fuzz, subdomain, dev]
attack_chain:
  - nmap: 22/80端口, nginx 1.18.0
  - ffuf 子域名爆破
  - 字典: /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt
  - ffuf -w ... -H "Host: FUZZ.stocker.htb" -u http://10.10.11.196 -fs 178
  - 发现 dev.stocker.htb 子域
  - 访问 dev.stocker.htb 获取管理面板
  - SSH登录angoose
  - sudo -l 提权
key_payload: dev.stocker.htb
one_liner: HTB Stocker：ffuf vhost爆破dev.stocker.htb子域
lesson: Vhost爆破是发现子域名隐藏功能的高效方法
quality: high
---

# HackTheBox Stocker WriteUp

## 题目信息
- 平台：HackTheBox
- 题目：Stocker
- 类别：Pentest 实战

## 关键攻击链
### 1. 端口扫描
```bash
sudo nmap -Pn -n -v --reason -sS -p- -sC --min-rate=1000 -A 10.10.11.196 -oN nmap.log
# 22/tcp open ssh OpenSSH 8.2p1
# 80/tcp open http nginx 1.18.0 (Ubuntu)
```

### 2. Vhost 子域名爆破
```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt \
  -H "Host: FUZZ.stocker.htb" \
  -u http://10.10.11.196 -fs 178

# 结果:
dev [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 164ms]
```

### 3. SSH 登录
```bash
ssh angoose@10.10.11.196
angoose@stocker:~$ whoami
angoose
angoose@stocker:~$ ls -l
-rw-r----- 1 root angoose 33 Jun 24 09:29 user.txt
angoose@stocker:~$ sudo -l
```

## 评分
- quality: high（Vhost 爆破 + dev.stocker.htb 子域 + SSH 登录）
