---
title: 【WP】NewStar CTF 2025 Week1&Week2 之 WEB 方向题解
contest: NewStarCTF
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [token-calc, expression-regex, requests-Session, cookie-maintain, /start_challenge, /verify_token, multiply-xor]
attack_chain: POST /start_challenge 拿 expression token 表达式 + hint + multiplier + xor_value + 新 session/正则提取 num1*num2^0x... 计算 token/POST /verify_token 提交 token/保持 session cookie 跨请求
key_payload: expression = "token = (1234 * 5678) ^ 0xDEADBEEF"  token = (1234*5678) ^ 0xDEADBEEF
one_liner: NewStar CTF 2025 Week1&Week2 Web 入门题，token 计算 + Session 维持 + 正则表达式。
lesson: requests.Session() 自动维持 cookie；正则 re.search 提取表达式数字和异或值；token = (num1*num2) ^ xor_val 是基础算术 XOR；Web 入门题通常用 icook 维持 session。
quality: medium
---

# 【WP】NewStar CTF 2025 Week1&Week2 之 WEB 方向题解

## 概览
NewStar CTF 2025 Week1 & Week2 Web 方向题解，基于 token 计算 + Session 维持。

## 解题流程

### 第一步：start_challenge
```python
import requests
import re

base_url = "https://eci-2ze5w79g3ev2py8ceky2.cloudeci1.ichunqiu.com:5000"
session = requests.Session()
session.cookies.update({
    "Hm_lvt_2d0601bd28de7d49818249cf35d95943": "1756542647",
    "session": ".eJx..."
})

start_response = session.post(f"{base_url}/start_challenge", headers=headers, data="")
response_data = start_response.json()
# 解析 expression / hint / multiplier / xor_value
```

### 第二步：计算 token
```python
def calculate_token(expression):
    match = re.search(r'token = \((\d+) \* (\d+)\) \^ (0x[0-9a-f]+)', expression)
    if match:
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        xor_val = int(match.group(3), 16)
        product = num1 * num2
        token = product ^ xor_val
        return token
    raise ValueError("无法解析表达式")
```

### 第三步：verify_token
```python
verify_data = {"token": token}
verify_response = session.post(f"{base_url}/verify_token", headers=headers, json=verify_data)
```

## 关键点
- `expression` 格式：`token = (1234 * 5678) ^ 0xDEADBEEF`
- `token = (num1 * num2) ^ xor_value`
- `requests.Session()` 自动维持 cookie
- 新 session 在 start_challenge 响应中返回
- `application/json` Content-Type 接收 JSON 响应

## 经验提炼
- requests.Session() 自动维持 cookie
- 正则 re.search 提取表达式数字和异或值
- token = (num1*num2) ^ xor_val 是基础算术 XOR
- Web 入门题通常用 cookie 维持 session
- `re.search(r'token = \((\d+) \* (\d+)\) \^ (0x[0-9a-f]+)', expression)` 表达式匹配
- `re.search` vs `re.match`：search 找任意位置，match 从头开始
- `int(x, 16)` 解析十六进制
- `session.cookies.set('session', new_session)` 手动更新 cookie
