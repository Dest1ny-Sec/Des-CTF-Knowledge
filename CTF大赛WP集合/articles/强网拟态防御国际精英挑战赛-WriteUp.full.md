---
title: 强网拟态防御/zerocalc
contest: 强网拟态
year: 2021
difficulty: medium
vuln_type:
- ssti
- ssrf
- rce
tags:
- notevil patched eval
- cookieSession key 可控
- cookie pollution
- readFile
- /etc/passwd 泄露
- /flag 随机名
attack_chain:
- 题目给 notevil（patched 过的 eval）但还接受额外 utils 参数
- 注入：readFile('/etc/passwd') 直接读 /etc/passwd（notevil 不挡 fs.readFile）
- cookieSession 用 Math.random().toString(16) 作 secret（弱但难爆破）
- 注入读 /proc/self/environ 或 /proc/1/environ 找 secret
- 用 secret 伪造 session 注入 cookieSession 污染
- 注入 hi.unshift(`${e} = ${ret}`) 让历史记录显示任意内容
- flag 路径随机：find / -name 'flag*' 2>/dev/null 遍历目录
- 读 flag 文件
key_payload: e = "readFile('/etc/passwd')"
one_liner: notevil 注入 readFile 读 /etc/passwd + 找 cookieSession secret 伪造 session
lesson: '"patched" 库接受额外参数时仍可注入；cookieSession secret 用弱熵 Math.random 易被读 /proc 还原'
quality: high
full_path: 强网拟态防御国际精英挑战赛-WriteUp.full.md
meta_path: 强网拟态防御国际精英挑战赛-WriteUp.meta.md
images_removed: true
images_removed_count: 3
schema_version: v3.0.0-P0
summary: 强网拟态防御/zerocalc。notevil 注入 readFile 读 /etc/passwd + 找 cookieSession secret 伪造 session。关键路径：题目给 notevil（patched 过的 eval）但还接受额外 utils 参数 → 注入：readFile('/etc/passwd') 直接读 /etc/passwd（notevil 不挡 fs.rea...
category: web
subcategory: ssti
subcategories:
- ssti
- ssrf
- rce
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 3
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/2601.html
reasoning_chain:
- 强网拟态防御/zerocalc：notevil patched eval + cookieSession 密钥污染 → 触发点：notevil 不挡 fs.readFile 但挡 evaluation 字符串
- 题目给 notevil（patched 过的 eval）但还接受额外 utils 参数 → 假设：注入 readFile('/etc/passwd') → 动作：构造表达式 'e = readFile("/etc/passwd")'
- 观察：读到 /etc/passwd 内部账户信息
- 假设：cookieSession secret 用 Math.random().toString(16) → 弱熵但难爆破 → 改为读 /proc/self/environ 或 /proc/1/environ 找 secret
- 用 secret 伪造 session 注入 cookieSession 污染 → 假设：注入 admin 字段
- 假设：hi.unshift(`e = ${ret}`) 让历史记录显示任意内容 → 进一步注入假 log
- flag 路径随机：find / -name 'flag*' 2>/dev/null → 遍历 → 读 flag 文件
failed_attempts:
- 试图直接 Math.random 爆破 secret → 失败：范围太大
- 读取 /etc/passwd 找密码 → 失败：只列用户
- 注入 ?e= 直接拿 process.env → 失败：notevil 拦 env
key_observations:
- '''patched'' 库接受额外参数时仍可注入：notevil 挡 evaluation 但不挡 fs.readFile'
- cookieSession secret 用弱熵 Math.random 易被读 /proc 还原
- 环境变量 /proc/1/environ 是 secret 高频存放处
- find / -name 'flag*' 是 fs 路径不确定时的标准答案
prerequisites:
- Node.js notevil 库与 patched eval 限制
- cookieSession 弱密钥攻击
- Linux /proc/self/environ 读取技巧
- SSTI / Code Injection 注入基础
---
# 强网拟态防御国际精英挑战赛-WriteUp

> 原文: https://www.ctfiot.com/2601.html
> ID: 2601

早安~各位打工人
以及本次比赛的超长WriteUp
决定给大家放个pdf
欢迎各位点击链接自取~
https://github.com/ChaMd5Team/Venom-WP/blob/main/2021-%E5%BC%BA%E7%BD%91%E6%8B%9F%E6%80%81%E9%98%B2%E5%BE%A1%E5%9B%BD%E9%99%85%E7%B2%BE%E8%8B%B1%E6%8C%91%E6%88%98%E8%B5%9B-WriteUp.pdf

Venom的小伙伴们辛苦啦，以及欢迎各路大神加入我们！

 Web

zerocalc

readFile('/etc/passwd')可以读文件
const express = require("express");
const path = require("path");
const fs = require("fs");
const notevil = require("./notevil"); // patched something...
const crypto = require("crypto");
const cookieSession = require("cookie-session");
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieSession({
 name: 'session',
 keys: [Math.random().toString(16)],
}));
//flag in root directory but name is randomized
const utils = {
 async md5(s) {
 return new Promise((resolve, reject) => {
 resolve(crypto.createHash("md5").update(s).digest("hex"));
 });
 },
 async readFile(n) {
 return new Promise((resolve, reject) => {
 fs.readFile(n, (err, data) => {
 if (err) {
 reject(err);
 } else {
 resolve(data);
 } });
 });
 },
}
const template = fs.readFileSync("./static/index.html").toString();
function render(s) {
 return template.replace("{{res}}", s.join('
'));
}
app.use("/", async (req, res) => {
 const e = req.body.e;
 const his = req.session.his || [];
 if (e) {
 try {
 const ret = (await notevil(e, utils)).toString();
 his.unshift(`${e} = ${ret}`);
 if (his.length > 10) {
 his.pop();
 }
 } catch (error) {
 console.log(error);
 his.add(`${e} = wrong?`);
 }
 req.session.his = his;
 }
 res.send(render(his));
});
app.use((err, res) => {
 console.log(err);
 res.redirect('/');
});
app.listen(process.env.PORT || 8888);

end

ChaMd5 ctf组 长期招新

尤其是crypto+reverse+pwn+合约的大佬

欢迎联系admin@chamd5.org


```
readFile('/etc/passwd')可以读文件
const express = require("express");
const path = require("path");
const fs = require("fs");
const notevil = require("./notevil"); // patched something...
const crypto = require("crypto");
const cookieSession = require("cookie-session");
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieSession({
 name: 'session',
 keys: [Math.random().toString(16)],
}));
//flag in root directory but name is randomized
const utils = {
 async md5(s) {
 return new Promise((resolve, reject) => {
 resolve(crypto.createHash("md5").update(s).digest("hex"));
 });
 },
 async readFile(n) {
 return new Promise((resolve, reject) => {
 fs.readFile(n, (err, data) => {
 if (err) {
 reject(err);
 } else {
 resolve(data);
 } });
 });
 },
}
const template = fs.readFileSync("./static/index.html").toString();
function render(s) {
 return template.replace("{{res}}", s.join('
'));
}
app.use("/", async (req, res) => {
 const e = req.body.e;
 const his = req.session.his || [];
 if (e) {
 try {
 const ret = (await notevil(e, utils)).toString();
 his.unshift(`${e} = ${ret}`);
 if (his.length > 10) {
 his.pop();
 }
 } catch (error) {
 console.log(error);
 his.add(`${e} = wrong?`);
 }
 req.session.his = his;
 }
 res.send(render(his));
});
app.use((err, res) => {
 console.log(err);
 res.redirect('/');
});
app.listen(process.env.PORT || 8888);
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]