---
title: 【BuildCTF】Web 方向 AK 全解 WP
contest: BuildCTF
year: 2024
difficulty: mixed
vuln_type: web_unknown
tags: [ID-bruteforce, robots.txt, htaccess-upload, HTTP-headers, Flask-SSTI, replace-length, ffifdyop-MD5, Character.toUpperCase-trick, JWT-forge, app.js, JWT_SECRET_KEY, WAF-bypass]
attack_chain: find-the-id 爆破数字 207/Tflock robots.txt + ctfer 登录态保持爆破 admin/Babyupload .htaccess 上传 + 木马 env 命令执行/ez!http 填 headers Date 点分隔格式/我写的网站被rce了 读文件命令执行/LovePopChain 反序列化链 post rce/RedFlag Flask ssti/Why_so_serials replace 长度变化构造反序列化 + joker 扩充/ez_md5 ffifdyop MD5 注入 → 爆破 3e41f780146b6c246cd49dd296a3da28 → 1145146803531 + 数组弱等于/eazyl0gin 字符ı→I ſ→S 登录绕 + 012346 md5/刮刮乐 cmd + Referer + 注释 /dev/null/sub admin + JWT_SECRET_KEY 伪造 token + 命令执行闭合/Cookie_Factory app.js 暴露 flag/ez_waf WAF 绕
key_payload: admin token 伪造 + JWT_SECRET_KEY  + ffifdyop  MD5 注入 + ı/ſ 字符 case-folding
one_liner: BuildCTF 2024 Web 方向 AK 全解，13 道题覆盖 ID 爆破/htaccess/headers/SSTI/反序列化/JWT/字符 case-folding 漏洞。
lesson: Character.toUpperCase() 中 'ı'→'I' 'ſ'→'S' 是 Java 经典 Unicode case-folding 漏洞；ffifdyop 经 MD5 后得 'or' 触发 SQL 注入绕过；JWT_SECRET_KEY 泄漏直接伪造 token。
quality: high
---

# 【BuildCTF】Web 方向 AK 全解 WP

## 概览
BuildCTF 2024 Web 方向 AK（All Kill）13 道题全解。

## 题目1: find-the-id
- 爆破数字，207 时得到 flag

## 题目2: Tflock
- 扫目录发现 `robots.txt`
- 获得账号 `ctfer:123456` 和 admin 密码字典
- 每次爆破 admin 密码前先发 ctfer 登录成功请求（保持会话态）
- admin 爆破成功后登录得 flag

## 题目3: Babyupload
- 上传 `.htaccess` 改 Apache 配置
- 再上传木马执行 env 命令

## 题目4: ez!http
- 按要求填写 HTTP headers
- Date 不用标准格式，用点分隔即可

## 题目5: 我写的网站被 rce 了
- 读文件时可触发命令执行

## 题目6: LovePopChain
- 写反序列化链 post 传参 rce

## 题目7: RedFlag
- Flask SSTI，参考 https://www.freebuf.com/articles/web/323728.html

## 题目8: Why_so_serials
- `replace` 长度变化构造反序列化字符串
- `joker` 扩充把原最后内容按长度挤出去

## 题目9: ez_md5
- MD5 SQL 注入：输入 `ffifdyop` MD5 后得 `'or'` 闭合触发注入
- 进入下一关 `/LnPkcKqy_levl2.php`
- 提示 robots.txt，爆破 `3e41f780146b6c246cd49dd296a3da28` 得 `1145146803531`
- MD5 弱等于直接传数组

## 题目10: eazyl0gin
- Node.js `Character.toUpperCase()` 漏洞：
  - `'ı'` → `'I'`
  - `'ſ'` → `'S'`
  - `Character.toLowerCase()` 中 `'İ'` → `'i'`，`'K'` → `'k'`
- 密码 MD5 解密得 `012346`
- 用 `BUıLDCTF` + `012346` 登录

## 题目11: 刮刮乐
- 提示传入 `cmd` + 修改 `Referer` 头
- 没回显可能后面拼接 `/dev/null`，注释掉后面即可

## 题目12: sub
- 注册 admin
- 泄漏 `JWT_SECRET_KEY` 伪造 token
- 读文件后构造命令执行闭合

## 题目13: Cookie_Factory
- 扫目录发现 `app.js`
- 直接暴露 flag

## 题目14: ez_waf
- WAF 绕（具体手法未详述）

## 经验提炼
- `Character.toUpperCase()` 中 `'ı'`→`'I'`、`'ſ'`→`'S'` 是 Java 经典 Unicode case-folding 漏洞
- `ffifdyop` 经 MD5 后得 `'or'`，触发 SQL 注入绕过
- `JWT_SECRET_KEY` 泄漏直接伪造 token
- `replace` 长度变化 + `joker` 扩展是反序列化字符串逃逸经典手法
- 读 robots.txt + 保持 ctfer 会话态爆破 admin 是常见后台爆破套路
- Date header 不强制 RFC 1123 格式
- `.htaccess` 可改 Apache 配置绕过上传限制
