---
title: 2025"领航杯"网安赛项教师组决赛 WP（上）- Crypto 修栅栏/RSA + Misc DNS/FTP + Web locallogin
contest: 2025 领航杯网安赛项
year: 2025
difficulty: medium
vuln_type:
- crypto_rsa
- web_unknown
- sqli
- ssrf
- auth_bypass
tags:
- 领航杯 2025 教师组 决赛
- Crypto 修栅栏 rail fence cipher
- CnHongKe base64 拼接
- DNS 二级域名组成有意义语句
- FTP 流量 flag.zip + sk.pem + secret.enc
- X-Forwarded-For 127.0.0.1 绕过 IP 检测
- base64 编码 cookie 替换 user→admin
- sqlmap 盲注
attack_chain:
- Crypto 修栅栏：三个一组替换，从上往下从左往右拼接 → CnHongKe base64 → 解码
- Crypto RSA：直接参考 Python 脚本运行
- DNS 流量：二级域名组成有意义语句 → flag
- FTP 流量：flag.zip + sk.pem + secret.enc → 还原密文
- 'Web locallogin: user/userpass 登录 + X-Forwarded-For: 127.0.0.1 绕 IP 检测'
- cookie base64 编码 user→admin 替换
- 'Web sql: sqlmap 脚本爆破'
key_payload: 'X-Forwarded-For: 127.0.0.1 绕 IP 检测'
one_liner: 2025 领航杯教师组决赛上：Crypto 修栅栏+RSA + Misc DNS/FTP + Web locallogin XFF+cookie 替换+sqlmap。
lesson: 修栅栏密码 = 三组字符按行拼接 → base64 编码；X-Forwarded-For 绕 IP 检测是经典 Web 套路；base64 编码 cookie 替换 user 字段是 admin 鉴权绕过常考点。
quality: medium
full_path: 2025“领航杯”网安赛项教师组决赛WP（上）.full.md
meta_path: 2025“领航杯”网安赛项教师组决赛WP（上）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2025"领航杯"网安赛项教师组决赛 WP（上）- Crypto 修栅栏/RSA + Misc DNS/FTP + Web locallogin。2025 领航杯教师组决赛上：Crypto 修栅栏+RSA + Misc DNS/FTP + Web locallogin XFF+cookie 替换+sqlmap。。关键路径：Crypto 修栅栏：三个一组替换，从上往下从左往右拼接 → Cn...
category: crypto
subcategory: rsa
subcategories:
- rsa
- web_other
- sql_injection
- ssrf
- logic
tools_used:
- Python
- sqlmap
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/277888.html
reasoning_chain:
- 触发点：Crypto 修栅栏密码 三组字符 → 假设：从上往下从左往右拼接 → 动作：py 把字符按行拼 base64
- 观察：CnHongKe → base64 解码 → 拿到 flag → 下一步：Crypto RSA 直接跑脚本
- 触发点：DNS 流量全是 DNS query → 假设：二级域名组成有意义语句 → 动作：tshark DNS qry name 列提取
- 观察：拼字符串得 flag → 下一步：FTP 流量看到 flag.zip + sk.pem + secret.enc
- 下一步：PKI 解密 flag.zip 得到密文
- '触发点：Web locallogin 后端校验 X-Forwarded-For 白名单 → 假设：127.0.0.1 绕 IP → 动作：登录后抓包加 X-Forwarded-For: 127.0.0.1'
- 观察：cookie base64 编码 user 字段 → 假设：改 user→admin 重编 base64 → 动作：替换 cookie 提权
- 下一步：sqlmap tamper 对有 waf 的接口做盲注爆破
failed_attempts:
- 试图直接猜 admin 密码 → 失败：locallogin 默认锁 IP 必须 XFF 绕
- 试图用混杂密钥解 flag.zip → 失败：必须 sk.pem + secret.enc 配套
- 试图手动解 DNS 流量所有 qry → 失败：二级域名巨多，靠脚本拼接
key_observations:
- 修栅栏密码 = 多组字符串按行从上往下从左往右拼接 → base64
- 'X-Forwarded-For: 127.0.0.1 是 IP 白名单绕过的经典头'
- base64 编码 cookie 的 user 字段替换是 admin 鉴权绕过常考点
- DNS 二级域名 = 流量分析中隐写信息载体
- FTP sk.pem + secret.enc = PKI 解密常用组合
prerequisites:
- tshark DNS 字段提取（qry.name）
- PKI 公钥加密 + openssl 解密
- XFF 头注入 + cookie base64 编码替换
- sqlmap tamper 脚本使用
---
# 2025“领航杯”网安赛项教师组决赛WP（上）

> 原文: https://www.ctfiot.com/277888.html
> ID: 277888

点击上方蓝字关注我们

郑重说明

数字人才创研院秉承探究学习与交流知识‍‍的原则，所有发布的技术文章仅供参考，目的在于助力你获得更多知识；与此同时，让我们共同遵守《网络安全法》，未经授权请勿利用文章中的技术内容对任何计算机系统进行非授权操作，否则对他人或单位而造成的直接或间接后果或损失，均由使用者本人负责。

 公众号发表的文章如有涉及您的侵权，烦请私信联系告知，我们会立即删除并对您表达最诚挚的歉意！感谢您的理解！‍

Purpose of recommendation

推荐观点

赛事的开展不仅给广大参赛选手提供了网络安全实战平台，同时也搭建了发现人才和共同交流的平台。竞技赛场，你追我赶，参赛选手以竞赛活动为契机，以赛促学、以赛促训，畅享不一样“饕餮盛宴”的竞赛。通过比赛，教学相长，大大增强了我省在全国对应赛项中的竞争力。

知己知彼，百战百胜，小编分享官方WP，旨在让大家了解赛事赛题的难度变化与知识范畴，发现团队薄弱之处，提升团队技术能力。

推荐指数：★★★★★

01-1

Crypto-修栅栏

1.三个一组进行替换，从上往下，从左往右进行拼接，发现了CnHongKe的base64编码

2.分开与拼接，如下图所示

3.直接使用base64解码即可得到答案

01-2

Crypto-RSA

直接上参考的Python脚本，运行即可

02-1

Misc-dns流量分析

1. 打开发现都是dns流量

2. 观察发现传输的二级域名可以组成有意义语句

3. 整合发现flag

02-2

Misc-keyfile

1.分析流量发现里面存在FTP流量，优先查看里面传输的文件。

2.发现里面存在flag.zip，但保存出来是加密的，此时结合sk.pem以及secret.enc解密数据，得到密文数据。

03-1

Web-locallogin

1. 使用user/userpass登录

2. 登录后抓包，在http头增加X-Forwarded-For: 127.0.0.1绕过ip检测

3. 查看cookie值，发现其为base64加密；将user替换为admin再进行base64编码替换即可

03-2

Web-sql

1. 编写脚本，参考代码如下：

如果喜欢，敬请关注，后期内容更精彩！

END

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