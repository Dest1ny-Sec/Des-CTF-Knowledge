---
title: 四川省信息安全技术大赛 AWD部分WriteUp
contest: 四川省信息安全技术大赛 AWD
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [AWD, PHP代码审计, Python Flask SSTI, webshell查杀, seay, D盾, 河马, 流量分析, render_template_string, 批量攻击]
attack_chain:
  - 初始 7w 分, 15 分钟一轮, 一轮 100 分, 最终 22w+ 分
  - PHP 题: 整站 tar 备份 + D盾/河马 webshell 查杀 + seay 代码审计
  - 命令执行: manage_comment_del.php + Manage_rce.php 删代码修复
  - 任意 SQL: manage_sql.php TRUE→FALSE 修复
  - 文件上传: user_upload.php 加白名单
  - Python 题: Flask blog + render_template_string SSTI
  - 加固: 花括号过滤
  - 攻击: 找 /auth/reset 路由 + render_template_string 漏洞
  - 回显 flag 在 HTML 注释里
  - 批量脚本每轮打 4000+ 分
key_payload: 'PHP 命令执行/SQL/上传 + Python Flask SSTI render_template_string + 批量 flag 脚本'
one_liner: 四川省信安 AWD 复盘: PHP 命令执行/SQL/上传修复 + Python Flask SSTI 批量攻击每轮 4000+ 分。
lesson: AWD 修复策略: 1) 删漏洞代码/修 TRUE→FALSE/加白名单; 2) webshell 查杀; 3) 备份源代码; 4) 改弱口令; 5) 看日志找他人攻击 payload; 6) 批量攻击脚本。
quality: medium
---

# 四川省信息安全技术大赛 AWD部分WriteUp

## 概览
- **来源**: ctfiot 76769 (Polo)
- **赛事**: 四川省信息安全技术大赛 AWD
- **难度**: ⭐⭐⭐

## 战绩
- 初始 7w 分, 15 分钟一轮, 1 flag = 100 分
- 最终 22w+ 分 (第二名 11w 时我们 14w)

## PHP 题

### 加固流程
1. tar 整站备份源代码
2. D盾/河马 webshell 查杀
3. seay 自动代码审计
4. 删 db.sql (敏感数据)
5. 检查 uploads 目录
6. 数据库备份 + 改后台密码 (弱口令 123456 / admin)
7. 删除魔改 WAF 路径 (担心主办方 check)

### 漏洞点
- **命令执行**: `manage_comment_del.php` + `Manage_rce.php` → 删代码修复
- **任意 SQL**: `manage_sql.php` `TRUE→FALSE`
- **任意文件上传**: `user_upload.php` 加白名单

## Python 题 (Flask)

### 漏洞点
- Flask blog + `render_template_string` SSTI
- 路由 `/auth/reset` 触发

### 加固
```python
# 过滤花括号
if '{' in input or '}' in input:
    return "Forbidden"
```

### 利用
- 找日志中其他队 payload (ssti {{...}})
- burp 看 render 后 HTML 注释
- flag 在注释里
- 写脚本批量打 → 每轮 4000+ 分

## 教学
- AWD 流程: 备份 → 查杀 → 审计 → 修复 → 攻击
- Python Flask 找漏洞: 全局搜 `render_template_string`
- 看日志学 payload 是关键加速器
- 批量脚本比手动快 10 倍
