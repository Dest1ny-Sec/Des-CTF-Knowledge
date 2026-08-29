---
title: 【WP】破阵阁・网安淬锋公开赛题目全解
contest: 破阵阁
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [intruder-bruteforce, sqlmap-dump, path-traversal, JWT-alg-none, nacos-command-injection, crontab-crash-tomcat, sqlmap-search-param, Joomla-3.7-CVE-2017-8917]
attack_chain: 1. 最简单签到 intruder id 遍历 47/2. 游戏营销 api.php 成绩提交接口/3. 最简单 Web id sql 注入 sqlmap dump/4. 安全牛 ERP 目录穿越 flag.html/5. 身份鉴权 JWT alg=none 绕签名/6. 诡异命令执行 第 250 个流 nacos 注入/7. webshell 被删除 grep -r "flag{" 整盘搜/8. 暗影迷踪 crontab -r 清空 + 删除 /var/crash/tomcat/9. 激进的开发者 search sql 注入 superadmin/1Qaz2Wsx + 文件上传/10. 小小的挑战 Joomla 3.7 CVE-2017-8917 SQL 注入
key_payload:  flag uuids  intruder id=47  sqlmap search  superadmin/1Qaz2Wsx
one_liner: 破阵阁・网安淬锋公开赛 10 道题全解 WP，涵盖 SQL 注入/路径穿越/JWT alg=none/命令注入/Webshell 还原/渗透。
lesson: JWT alg=none 是经典签名绕过；Joomla 3.7.0 CVE-2017-8917 SQL 注入；nacos 注入看 Wireshark 第 250 流；crontab -r + 删 crash 是应急响应清痕迹。
quality: high
---

# 【WP】破阵阁・网安淬锋公开赛题目全解

## 概览
破阵阁・网安淬锋公开赛 10 道题全解 WP，涵盖 MISC/WEB/Forensics/Pentest。

## MISC

### 最简单签到
- intruder 遍历 id，在 47 找到 flag
- `flag{18d6d685-9161-471e-a92e-1c472ffa846a}`

### 游戏营销
- 发现成绩提交接口 `api.php`
- `flag{9dab6a2b-3e7d-4fdf-bb42-a76f325b3b38}`

## WEB

### 最简单的 Web 安全入门
- id 存在 SQL 注入
- sqlmap 直接 dump
- `flag{8b258afe-ddb5-4459-a66d-2682596a6db0}`

### 安全牛的 ERP
- 提示在 flag.html
- 目录穿越
- `flag{e9142efc-dc83-47cf-a9f6-3fedbd5c3dec}`

### 贼牛掰的身份鉴权
- 签名 key 不知道
- 加密改成 `alg=none` 即可
- `flag{023b3d64-b9a6-4fdd-82c7-136579868f83}`

## Forensics

### 诡异的命令执行
- 在第 250 个流中发现 nacos 注入执行结果
- `flag{531c8909-7678-4f86-96fd-cc67a7576b36}`

### webshell 被删除了
- 全局查找 flag
- `grep -r "flag{" /`
- `flag{e9bef616-d5c0-41e1-82f4-52208e6877bf}`

### 暗影迷踪
- `crontab -r` 清空计划任务
- 删除 `/var/crash/tomcat` 目录
- `flag{80b61d65-0675-481c-8e69-ec8f380a31de}`

## Pentest

### 激进的开发者
- `search` 参数存在 SQL 注入
- 得到用户 `superadmin` / 密码 `1Qaz2Wsx`
- 登录发现文件上传
- 上传一句话木马
- 直接连接后门
- `flag{e3fd4235-5576-45ff-98b1-ea58fe285391}`

### 小小的挑战（赛后复盘）
- 扫目录发现 `/administrator` 和 `/README.txt`
- 识别为 Joomla! 3.7
- CVE-2017-8917 SQL 注入
- https://developer.aliyun.com/article/1099637
- 175.27.169.122:port

## 经验提炼
- JWT `alg=none` 是经典签名绕过
- Joomla 3.7.0 CVE-2017-8917 SQL 注入
- nacos 注入看 Wireshark 第 250 流
- `crontab -r` + 删 crash 是应急响应清痕迹
- intruder 遍历 id 是 Burp Suite 入门用法
- `api.php` 暴露成绩提交接口是开发人员常见失误
- sqlmap `--dump` 自动导出所有表
- ERP 系统 flag.html 提示路径是入门级目录穿越
- `grep -r` 整盘搜索 flag 是取证基础操作
- 文件上传 + 一句话木马是 Web 渗透经典三件套
- `1Qaz2Wsx` 是常见弱密码（qwerty 键盘左手）
