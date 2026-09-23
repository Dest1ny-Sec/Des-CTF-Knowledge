---
title: Apiculture 1 write-up - 针对 API 的渗透测试
contest: Apiculture
year: 2022
difficulty: easy
vuln_type: web_unknown
tags:
- API penetration
- vendorID leakage
- swagger.json
- /api/products
- /api/vendors/{id} IDOR
- /api/flags/ Basic Auth
- SHA1 弱密码
- 57332 admin
- abeille密码
attack_chain:
- /api/products/ 端点泄露未使用 vendorID 字段
- 看到所有产品 vendorID=57336
- /api/swagger.json 发现 /api/flags/ (Basic Auth 保护)
- /api/vendors/57336 拿到 SHA1 密码哈希
- 谷歌 SHA1 哈希得弱密码
- 但 57336 用户无法访问 /api/flags/
- 'IDOR: /api/vendors/57332 试错发现 admin'
- 57332 同样是 SHA1 弱密码 (abeille)
- 用 admin 身份 + abeille 登录 /api/flags/ 拿 flag
key_payload: '''/api/products vendorID 57336 泄露 / /api/swagger.json 找 /api/flags/ / /api/vendors/57336 SHA1 弱密码 / IDOR 试错找 57332 admin / SHA1 弱密码 abeille / Basic Auth 登录'''
one_liner: Apiculture 1 API 渗透 — /api/products 泄露 vendorID + /api/swagger.json 找 /api/flags/ + /api/vendors/{id} IDOR 试 57332 admin + SHA1 弱密码 abeille 登录拿 flag。
lesson: 'API 渗透标准链: 端点泄露字段 → swagger.json 找受保护端点 → IDOR 试错 admin → 弱密码爆破;vendorID 是常见 IDOR 字段。'
quality: medium
full_path: Apiculture_1_write-up-针对API的渗透测试.full.md
meta_path: Apiculture_1_write-up-针对API的渗透测试.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Apiculture 1 write-up - 针对 API 的渗透测试。Apiculture 1 API 渗透 — /api/products 泄露 vendorID + /api/swagger.json 找 /api/flags/ + /api/vendors/{id} IDOR 试 57332 admin + SHA1 弱密码 abeille 登录拿 flag。。关键路径：/api/...
category: web
subcategory: web_other
time_required: quick
difficulty_score: 2
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/107011.html
reasoning_chain:
- '[触发点] 浏览器开发者工具看 /API/products/ 调用 → 假设：响应含未使用 vendorID 字段泄露 / [动作] 直接看 /API/products/ 端点返回 JSON / [观察] 所有产品 vendorID=57336 / [下一步] 找 /api/swagger.json'
- '[触发点] 想到开发人员常留 API 文档 → 假设：/api/swagger.json 暴露受保护端点 / [动作] 访问 /api/swagger.json / [观察] 发现 /api/flags/ Basic Auth 保护端点 / [下一步] 试 /api/vendors/57336'
- '[触发点] /api/vendors/{id} 端点 → 假设：57336 用户可访问并泄露 SHA1 哈希 / [动作] 访问 /api/vendors/57336 / [观察] 拿到 SHA1 弱密码哈希 / [下一步] Google SHA1 反查'
- '[触发点] 谷歌 SHA1 哈希 → 假设：弱密码易反查 → 假设：57336 用户不能访问 /api/flags/ / [动作] IDOR 试 /api/vendors/57332 发现 admin / [观察] 57332 也是 SHA1 弱密码 (abeille) / [下一步] 用 admin + abeille 拿 /api/flags/ flag'
failed_attempts:
- 试图直接登录 /api/flags/ → 失败：缺有效凭证
- 试图猜 admin 密码 → 失败：SHA1 弱密码需用 google 反查
key_observations:
- API 渗透标准链：端点泄露字段 → swagger.json 找受保护端点 → IDOR 试错 admin → 弱密码爆破
- vendorID 是常见 IDOR 字段
- SHA1 弱密码易通过谷歌反查
- Basic Auth 保护可被 IDOR + 弱密码组合绕过
prerequisites:
- API 渗透基础（端点泄露 / swagger.json）
- IDOR 漏洞测试
- SHA1 哈希反查
- Basic Auth 认证机制
---
# Apiculture 1 write-up-针对API的渗透测试

> 原文: https://www.ctfiot.com/107011.html
> ID: 107011

养蜂业挑战赛专门针对API攻击。这基本上是一个蜂蜜成瘾者网站：

为了解决第一个挑战，我们应该注意对/API/products/ API的调用：

此端点向Angular前端提供信息，以便页面可以在浏览器中呈现……但它受到不当数据过滤漏洞的影响，因为它会显示网页中未使用的数据[即vendorID字段]。我们确实可以发现所有产品都是由同一个供应商发布的，其ID为57336：

然后，我们应该尝试发现其他端点。幸运的是，开发人员在/api/swagger.json中保留了他的API的详细描述：

/API/flags/ endpoint听起来特别有趣…但它受到Basic Auth的保护：

让我们看看/API/vendors/端点。当我们提供通过最初的不当数据过滤漏洞泄露的供应商ID时，它会显示有趣的信息：

因此，我们知道供应商是一个简单的用户，我们有他的密码哈希。这个SHA1哈希可以快速破解，或者简单地在谷歌上搜索以获得该供应商的弱密码：

然而，它不允许访问受限的/API/flags/ endpoint……但是我们可以利用不安全的直接对象引用漏洞来获取其他供应商的信息：

经过几次尝试后，我们发现供应商57332是管理员：

而且他的弱密码也可以很容易地被谷歌到：

我们现在可以使用www.example.com用户和abeille密码以Antonio Rodrigo NOGUEIRA的身份登录arn@gmail.br：

最后欣赏我们的Flag：

原文始发于微信公众号（闲聊知识铺）：Apiculture 1 write-up-针对API的渗透测试

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