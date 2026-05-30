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
 return template.replace("{{res}}", s.join('<br/>'));
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
 return template.replace("{{res}}", s.join('<br/>'));
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1635298566.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1635298566.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1635298566.jpeg)