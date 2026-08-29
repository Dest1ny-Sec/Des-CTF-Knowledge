---
title: SECCON CTF 2023 Quals/Upsolves
contest: SECCON CTF
year: 2023
difficulty: medium
vuln_type:
- jwt
- xss
- rce
tags:
- JWT alg 注入
- constructor prototype
- 弱 secret
- notevil eval
- CSP 绕过
- XSS 拿 cookie
- 简单计算器 XSS
attack_chain:
- bad-jwt 题目：JWT 验证函数 createSignature 用 algorithms[header.alg.toLowerCase()]()
- 攻击：把 alg 改成 "constructor" → algorithms.constructor 是 Object constructor → 拼出恒等签名
- 伪签名："eyJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ=="（拼接 header+payload 不加点）
- 验证：calculated_signature == expected_signature 恒等 → 通过
- 设 session 携带伪造 JWT 拿到 admin
- simplecalc 题目：CSP `default-src ${js_url} 'unsafe-eval'`，url 来自 req.hostname
- 攻击：控制 Host 头让 js_url 指向攻击者服务器，返回恶意 JS
- eval(params.get('expr')) 可执行任意 JS
- 用 XSS 拿管理员 cookie 访问 /flag
- 上报链接触发 admin 访问 → 收集 flag
key_payload: "header = {\"alg\": \"constructor\", \"typ\": \"JWT\"}; payload = {\"isAdmin\": true}; token = base64(header) + '.' + base64(payload) + '.' + base64(header+payload)"
one_liner: JWT alg 注入 prototype pollution + CSP Host 头污染 XSS 拿 flag
lesson: JWT 库用字典查算法时 alg 字段可被注入到 Object 原型链；CSP 中 default-src 接受 Host 头参数可被污染
quality: high
---

# SECCON CTF 2023 Quals/Upsolves

**JWT alg 注入 prototype pollution + CSP Host 头污染 XSS**

> SECCON CTF · 2023 · medium · jwt/xss/rce · quality=high
> 思路: bad-jwt: JWT 验证 createSignature 用 algorithms[header.alg.toLowerCase()](), alg=constructor → prototype pollution 恒等签名 → 伪造 isAdmin → simplecalc: CSP `default-src ${js_url} 'unsafe-eval'` url 来自 req.hostname → 污染 Host 头让 js_url 指向攻击者 → eval(expr) 拿 admin cookie
> 套路: JWT 库用字典查算法时 alg 字段可被注入到 Object 原型链；CSP 中 default-src 接受 Host 头参数可被污染

**关键 payload**:
```javascript
header = {"alg": "constructor", "typ": "JWT"}
payload = {"isAdmin": true}
token = base64(header) + '.' + base64(payload) + '.' + base64(header+payload)
```
