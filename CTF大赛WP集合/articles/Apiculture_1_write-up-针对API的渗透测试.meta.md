---
title: Apiculture 1 write-up - 针对 API 的渗透测试
contest: Apiculture
year: 2022
difficulty: easy
vuln_type: web_unknown
tags: [API penetration, vendorID leakage, swagger.json, /api/products, /api/vendors/{id} IDOR, /api/flags/ Basic Auth, SHA1 弱密码, 57332 admin, abeille密码]
attack_chain:
  - /api/products/ 端点泄露未使用 vendorID 字段
  - 看到所有产品 vendorID=57336
  - /api/swagger.json 发现 /api/flags/ (Basic Auth 保护)
  - /api/vendors/57336 拿到 SHA1 密码哈希
  - 谷歌 SHA1 哈希得弱密码
  - 但 57336 用户无法访问 /api/flags/
  - IDOR: /api/vendors/57332 试错发现 admin
  - 57332 同样是 SHA1 弱密码 (abeille)
  - 用 admin 身份 + abeille 登录 /api/flags/ 拿 flag
key_payload: '/api/products vendorID 57336 泄露 / /api/swagger.json 找 /api/flags/ / /api/vendors/57336 SHA1 弱密码 / IDOR 试错找 57332 admin / SHA1 弱密码 abeille / Basic Auth 登录'
one_liner: Apiculture 1 API 渗透 — /api/products 泄露 vendorID + /api/swagger.json 找 /api/flags/ + /api/vendors/{id} IDOR 试 57332 admin + SHA1 弱密码 abeille 登录拿 flag。
lesson: API 渗透标准链: 端点泄露字段 → swagger.json 找受保护端点 → IDOR 试错 admin → 弱密码爆破;vendorID 是常见 IDOR 字段。
quality: medium
---

# Apiculture 1 write-up - 针对 API 的渗透测试

## 速读
Apiculture 蜂蜜成瘾者网站 API 渗透第一关。

## 步骤

### 1. /api/products/ 泄露 vendorID
- 端点向 Angular 前端提供产品信息
- 受不当数据过滤影响, 显示未使用字段 `vendorID`
- 看到所有产品都是同一供应商发布, ID=57336

### 2. /api/swagger.json 找端点
- 开发者保留 API 详细描述
- `/api/flags/` 端点: **Basic Auth 保护**

### 3. /api/vendors/57336 拿密码
- 端点暴露供应商信息
- 拿到 SHA1 密码哈希
- 谷歌搜索得弱密码

### 4. IDOR 找 admin
- 57336 密码无法访问 /api/flags/
- 试错: /api/vendors/57332 是 admin
- 弱密码也是 SHA1 (abeille)

### 5. 登录拿 flag
- 用户: `arn@gmail.br` (Antonio Rodrigo NOGUEIRA)
- 密码: `abeille`
- /api/flags/ 拿 flag

## 关键 takeaway
- 端点字段泄露 (vendorID) 是 IDOR 入口
- swagger.json 暴露未授权端点
- SHA1 弱密码可谷歌搜
