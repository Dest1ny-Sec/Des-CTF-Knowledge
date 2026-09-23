---
title: Apiculture 2 - API 渗透测试 write-up
contest: Apiculture (养蜂业 API 挑战)
year: 2023
difficulty: medium
vuln_type:
- auth_bypass
- web_unknown
tags:
- API
- swagger.json
- /API/v2/
- OSINT
- DOCX-metadata
- sitemap.xml
- captcha-math
- 4-digit-PIN
- brute-force
- deprecated-API
attack_chain:
- /API/v4/swagger.json 暴露 /users/reset 邮件密码重置
- 降级到 /API/v2/swagger.json 旧版 API
- v2 三阶段重置：/users/reset1 拿 aes256Payload + 算术验证码
- v2 /users/reset2 提交答案 + payload 拿新 payload
- v2 /users/reset3 提交 payload + 4 位 SMS PIN 暴力 10000 次
- OSINT：sitemap.xml → marketing_legacy/giftcard.pdf → 父目录 DOCX/PPTX 元数据
- DOCX 作者 'Winny BÄRENJUNGEN' → LinkedIn 找 CEO 邮箱
- 重置 CEO 邮箱 winnybarenjungen@gmail.com 拿 flag
key_payload: 'POST /API/v2/users/reset3 { aes256Payload, sms4digits: 0000-9999 }'
one_liner: 旧版 API + DOCX 元数据 OSINT + 4 位 PIN 爆破
lesson: API 弃用版本不删是常见漏洞；DOCX/PPTX 元数据泄露作者；4 位 PIN 暴力无防是经典
quality: high
full_path: Apiculture_2_write-up-针对API的渗透测试.full.md
meta_path: Apiculture_2_write-up-针对API的渗透测试.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Apiculture 2 - API 渗透测试 write-up。旧版 API + DOCX 元数据 OSINT + 4 位 PIN 爆破。关键路径：/API/v4/swagger.json 暴露 /users/reset 邮件密码重置 → 降级到 /API/v2/swagger.json 旧版 API → v2 三阶段重置：/users/reset1 拿 aes256Payload + 算...
category: web
subcategory: logic
subcategories:
- logic
- web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/107150.html
reasoning_chain:
- '[触发点] /API/v4/swagger.json 暴露 /users/reset → 假设：v4 是新版要降级 / [动作] 试 /API/v2/swagger.json / [观察] v2 暴露 /users/reset1 + /users/reset2 + /users/reset3 三阶段重置 / [下一步] 走 v2 重置链'
- '[触发点] v2 重置三阶段：reset1 拿 aes256Payload + 算术验证码 / reset2 提交 + 拿 payload / reset3 提交 payload + 4 位 SMS PIN → 假设：4 位 PIN 可爆 / [动作] reset1 拿 payload → reset2 提交 → reset3 暴力 0000-9999 / [观察] 10000 次 PIN 爆破成功 / [下一步] OSINT 找目标邮箱'
- '[触发点] robot.txt → sitemap.xml → marketing_legacy/giftcard.pdf → 父目录 DOCX/PPTX → 假设：DOCX 作者元数据泄露 CEO 邮箱 / [动作] 看 DOCX 元数据 / [观察] 作者 ''Winny BÄRENJUNGEN'' / [下一步] LinkedIn 查 CEO'
- '[触发点] LinkedIn 找 CEO 邮箱 → 假设：winnybarenjungen@gmail.com 是 victim / [动作] 重置 CEO 邮箱密码 / [观察] 拿到新密码 / [下一步] 登录拿 flag'
failed_attempts:
- 试图在 v4 上重置 → 失败：v4 没有详细 reset 端点
- 试图用 6 位 PIN 爆破 → 失败：题目是 4 位
key_observations:
- API 弃用版本不删是常见漏洞
- DOCX/PPTX 元数据泄露作者
- 4 位 PIN 暴力无防是经典
- sitemap.xml + DOCX 元数据是 OSINT 经典组合
prerequisites:
- API 渗透（swagger.json / reset 端点）
- OSINT 基础（sitemap.xml / DOCX 元数据 / LinkedIn）
- 4 位 PIN 暴力爆破
- AES-256 payload 解密
---
# Apiculture 2 write-up-针对API的渗透测试

> 原文: https://www.ctfiot.com/107150.html
> ID: 107150

养蜂业挑战赛专门针对API攻击。第二层基本上看起来像是一个专门介绍蜂箱的网页：

在开发者工具中快速查看一下，会发现对/API/v4/products/ endpoint的调用：

这个端点确实允许获取蜂箱JSON。它还受到不当数据过滤漏洞的影响，因为它包含Angular前端未用于在浏览器中呈现网页的数据[即vendorID字段]：

不管怎么说，这个漏洞在那个挑战中不是很有用。一个最有趣的发现是注意到在/API/v4/swagger.json中有一个Swagger文件：

/API/v4/reset端点听起来很有趣，因为它可以允许更改其他人的密码：

基于此Swagger，/users/reset端点依赖于reset 1 ModelInput和resetModelOutput模式。因此，我们应该研究这些定义，看看这个有趣的终点所期望的是什么：

/users/reset端点基本上期望接收一个POST的电子邮件字符串，然后用另一个消息字符串进行响应。让我们检查：

此端点似乎不是很详细，无法用于标识有效邮箱：

不幸的是，密码重置过程依赖于发送到所有者邮箱的秘密链接。既然它们都不能被攻击，我们应该找到另一种方法。

这里的诀窍是注意到我们面对的是API的4月版本。而且可能存在较旧的版本，例如暂存或弃用的API。事实上，一些尝试很快就发现了v2的存在，其Swagger文件位于/API/v2/swagger.json：

与生产生态系统相反，在这个弃用的API上没有一个/users/reset端点。实际上有3个不同的重置端点：

/users/reset 1端点需要一个POST电子邮件字符串，并显然使用AES-256密码进行响应：

然后，/users/reset 2端点期望通过名为aes 256 PayloadFromReset 1的字符串变量接收此AES-256密码。它显然还期望challengeResponse变量为整数，并且它还将使用AES-256密码进行响应：

最后，/users/reset 3端点期望通过名为aes 256 PayloadFromReset 2的字符串变量接收此AES-256密码。它显然还期望接收一个名为sms 4digits的字符串变量，然后它将使用包含新密码的字符串消息进行响应：

因此，这个旧API上的密码重置功能只涉及一个4位数的PIN，可能是通过SMS发送给所有者的。闻起来很香！我们不能暴力破解一个基于UUID的秘密链接，但是我们可以攻击一个4位数的PIN……所以，如果两个版本的API都使用相同的数据库，那么我们有一个很好的方法来攻击prod中的帐户。这种情况确实与 2016年影响Facebook，除了这个/API/v2/reset端点还涉及验证码保护（我们很快就会看到）。

因此，我们需要确定一个受害者的选择，并使用他的电子邮件地址劫持他的帐户通过这个弃用的API。与生产接口相反，已弃用的API上的重置端点非常冗长，我们现在有一种方法来验证后端是否存在目标：

因此，我们现在应该集中精力寻找一个选择的目标。事实证明，robot.txt引用了sitemap.xml文件：

此站点地图允许在marketing_legacy目录中发现名为giftcard.pdf的文件：

PDF文件本身是无用的，但允许在父目录上进行目录索引，这允许发现其他Office文档：

DOCX和PPTX文件都包含显示CEO姓名的元数据：

一些快速的OSINT查询允许快速获得有关“Winny BÄRENJUNGEN”的信息：

在LinkedIn、Twitter、Youtube、Copaindavant和Viadeo上很容易找到这位首席执行官。我们可以很快发现，CEO的邮箱是winnybarenjungen@gmail.com：

现在我们已经确定了目标，让我们从/users/reset 1端点开始攻击被遗忘的API：

正如预期的那样，我们收到了一个aes256Payload（它很可能用于托管服务器端的秘密，以提供一些无状态的功能）以及一个验证码，通过challenge变量进行解析。

这个验证码是一个非常简单的数学难题，所以我们可以调用/users/reset 2端点，并向它提供我们的答案和从第一个端点接收的AES-256有效载荷：

不幸的是，这种手工制作的请求显然太慢了。因此，我们需要自动化该操作以更快：

这样效果更好，我们不会遇到任何过期的挑战问题：

因此，最后一步是使用/users/reset 3端点将AES-256密码与已发送到目标的4位数PIN沿着发布。让我们尝试为该PIN添加一个小的强制功能：

由于没有针对PIN的暴力破解的保护，我们最终可以在几秒钟内重置CEO的密码并获得我们的标志：

原文始发于微信公众号（闲聊知识铺）：Apiculture 2 write-up-针对API的渗透测试

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