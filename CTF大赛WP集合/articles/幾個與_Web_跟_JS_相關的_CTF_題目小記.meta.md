---
title: 几个Web+JS相关CTF题目小记 - Node原型链污染
contest: 多个CTF题目精选(JS+Web)
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [Node.js, 原型链污染, prototype_pollution, Proxy, Fastify, innerHTML, SVG_onload, unhandledrejection, npm_preinstall, prototype.shell, prototype.path, Object.prototype.data]
attack_chain: Node JSON深合并Object.entries原型链污染(Object.prototype.data.path.shell) → npm preinstall脚本读取prototype.path触发RCE → Proxy get()拦截flag访问 → Fastify x-token=hash(user.id)未授权 → innerHTML+SVG onload执行JS → window.addEventListener('unhandledrejection',e.reason.stack)泄露path
key_payload: Object.prototype.data = {exports:{"./pwn.js"},name:'./usage.js'} + prototype.shell + prototype.path
one_liner: 5题Web+JS小记:Node原型链污染触发npm preinstall RCE/Proxy拦截/Fastify x-token/innerHTML SVG onload/unhandledrejection。
lesson: Node深合并Object.entries递归赋值是经典原型链污染漏洞;Object.prototype.data.path.shell可被npm preinstall利用;SVG onload可在innerHTML中执行JS;Proxy get()陷阱;window.addEventListener('unhandledrejection')泄露错误堆栈信息。
quality: medium
---
