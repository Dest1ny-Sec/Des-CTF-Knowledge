---
title: 【BuildCTF】Web 方向 AK 全解 WP
contest: BuildCTF
year: 2024
difficulty: medium
vuln_type: ssti
tags:
- ID-bruteforce
- robots.txt
- htaccess-upload
- HTTP-headers
- Flask-SSTI
- replace-length
- ffifdyop-MD5
- Character.toUpperCase-trick
- JWT-forge
- app.js
- JWT_SECRET_KEY
- WAF-bypass
attack_chain: find-the-id 爆破数字 207/Tflock robots.txt + ctfer 登录态保持爆破 admin/Babyupload .htaccess 上传 + 木马 env 命令执行/ez!http 填 headers Date 点分隔格式/我写的网站被rce了 读文件命令执行/LovePopChain 反序列化链 post rce/RedFlag Flask ssti/Why_so_serials replace 长度变化构造反序列化 + joker 扩充/ez_md5 ffifdyop MD5 注入 → 爆破 3e41f780146b6c246cd49dd296a3da28 → 1145146803531 + 数组弱等于/eazyl0gin 字符ı→I ſ→S 登录绕 + 012346 md5/刮刮乐 cmd + Referer + 注释 /dev/null/sub admin + JWT_SECRET_KEY 伪造 token + 命令执行闭合/Cookie_Factory app.js 暴露 flag/ez_waf WAF 绕
key_payload: admin token 伪造 + JWT_SECRET_KEY  + ffifdyop  MD5 注入 + ı/ſ 字符 case-folding
one_liner: BuildCTF 2024 Web 方向 AK 全解，13 道题覆盖 ID 爆破/htaccess/headers/SSTI/反序列化/JWT/字符 case-folding 漏洞。
lesson: Character.toUpperCase() 中 'ı'→'I' 'ſ'→'S' 是 Java 经典 Unicode case-folding 漏洞；ffifdyop 经 MD5 后得 'or' 触发 SQL 注入绕过；JWT_SECRET_KEY 泄漏直接伪造 token。
quality: high
full_path: 【BuildCTF】Web方向AK全解WP.full.md
meta_path: 【BuildCTF】Web方向AK全解WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【BuildCTF】Web 方向 AK 全解 WP。BuildCTF 2024 Web 方向 AK 全解，13 道题覆盖 ID 爆破/htaccess/headers/SSTI/反序列化/JWT/字符 case-folding 漏洞。。经验：Character.toUpperCase() 中 'ı'→'I' 'ſ'→'S' 是 Java 经典 Unicode ...
category: web
subcategory: web_other
tools_used:
- Flask
- Java
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/212857.html
reasoning_chain:
- find-the-id → 爆破数字 207 → 触发点：暴力 ID 枚举
- Tflock → robots.txt + ctfer 登录态保持 + admin 字典爆破
- Babyupload → .htaccess 上传 + 木马 env 命令执行 → 触发点：上传限制绕
- LovePopChain → 反序列化链 post rce → 触发点：PHP pop chain
- RedFlag → Flask SSTI → 假设：模板注入 → 动作：{{config}} → flag
- Why_so_serials → replace 长度变化构造反序列化 + joker 扩充 → 假设：长度检查绕过
- ez_md5 → ffifdyop MD5 注入 → 触发点：MD5 后 latin1 含 'or'
- 动作：爆破 3e41f780146b6c246cd49dd296a3da28 → 1145146803531 + 数组弱等于
- eazyl0gin → 字符 ı→I ſ→S 登录绕 → 触发点：Java Character.toUpperCase Unicode case-folding
- 刮刮乐 → cmd + Referer + JWT_SECRET_KEY 伪造 token + 命令执行闭合
- Cookie_Factory / ez_waf → app.js 暴露 flag + WAF 绕收尾
failed_attempts:
- 试图直接 admin 登录 → 失败：必须先 ctfer 登录保持爆破
- 试图用普通 md5 注入 → 失败：必须用 ffifdyop 触发 raw md5
key_observations:
- Character.toUpperCase() 中 'ı'→'I' 'ſ'→'S' 是 Java 经典 Unicode case-folding 漏洞
- ffifdyop 经 MD5 后得 'or' 触发 SQL 注入绕过
- JWT_SECRET_KEY 泄漏直接伪造 token
- 反序列化链 + replace 长度变化构造是 PHP pop 链关键
prerequisites:
- PHP 反序列化 pop chain 构造
- Flask SSTI 模板注入
- MD5 注入（ffifdyop raw）
- Java Unicode case-folding 漏洞
---
# 【BuildCTF】Web方向AK全解WP

> 原文: https://www.ctfiot.com/212857.html
> ID: 212857

【find-the-id】

爆破数字，207时得到flag

【Tflock】

扫目录发现robots.txt

获得一个账号ctfer:
123456

获得admin密码字典

在每次爆破admin密码前发送一个ctfer登录成功的请求

admin爆破成功

登录获得flag

【Babyupload】

上传.htaccess

再上传木马执行env命令即可

【ez!http】

按要求填写http headers即可

Date不用按标准格式填写，用点分隔就行

【我写的网站被rce了？】

读文件时候可以命令执行即可

【LovePopChain】

写反序列化链子，然后post传参rce即可

【RedFlag】

Flask ssti

https://www.freebuf.com/articles/web/323728.html

【Why_so_serials?】

利用replace长度的变化构造反序列化字符串，利用joker扩充把原来最后面的内容按长度挤出去就行了

【ez_md5】

md5 sql注入，输入ffifdyop加密得到’闭合构造sql注入

进入下一关/LnPkcKqy_levl2.php

提示了robots看到

爆破一下3e41f780146b6c246cd49dd296a3da28得到1145146803531

Md5弱等于，直接传数组即可

【eazyl0gin】

node在处理大小时候有漏洞

在Character.toUpperCase()函数中，字符ı会转变为I，字符ſ会变为S。

在Character.toLowerCase()函数中，字符İ会转变为i，字符K会转变为k。

密码md5解密得到012346

故使用BUıLDCTF和012346登录

【刮刮乐】

提示传入cmd并且修改Referer头

没有回显可能后面拼接了/dev/null，注释掉后面就行了

【sub】

注册admin

利用JWT_SECRET_KEY伪造token

可以读到文件之后构造命令执行闭合

【Cookie_Factory】

扫目录发现app.js

打开即可获得flag

【ez_waf】

前面添加8000个1绕过waf上传一句话木马

获取flag

【打包给你】

原题：https://blog.csdn.net/qq_46548764/article/details/141602431

上传文件后，后端会存储用户的文件并将其打包并提供压缩包下载功能，漏洞触发点，关键在于：

vps打开nc -lvvp 8080 监听

上传这三个文件并下载，触发tar命令的反弹shell

【fake_signin】

看到补签功能只有一次，但是存在如果30天同时并发可以达到同时补签30天的情况

再次刷新签到页面，发现30天都是已签到状态了，flag也出来了

原文始发于微信公众号（智佳网络安全）：【BuildCTF】Web方向AK全解WP

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]