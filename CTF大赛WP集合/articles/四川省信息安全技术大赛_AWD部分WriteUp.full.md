---
title: 四川省信息安全技术大赛 AWD部分WriteUp
contest: 四川省信息安全技术大赛 AWD
year: 2022
difficulty: medium
vuln_type: web_unknown
tags:
- AWD
- PHP代码审计
- Python Flask SSTI
- webshell查杀
- seay
- D盾
- 河马
- 流量分析
- render_template_string
- 批量攻击
attack_chain:
- 初始 7w 分, 15 分钟一轮, 一轮 100 分, 最终 22w+ 分
- 'PHP 题: 整站 tar 备份 + D盾/河马 webshell 查杀 + seay 代码审计'
- '命令执行: manage_comment_del.php + Manage_rce.php 删代码修复'
- '任意 SQL: manage_sql.php TRUE→FALSE 修复'
- '文件上传: user_upload.php 加白名单'
- 'Python 题: Flask blog + render_template_string SSTI'
- '加固: 花括号过滤'
- '攻击: 找 /auth/reset 路由 + render_template_string 漏洞'
- 回显 flag 在 HTML 注释里
- 批量脚本每轮打 4000+ 分
key_payload: '''PHP 命令执行/SQL/上传 + Python Flask SSTI render_template_string + 批量 flag 脚本'''
one_liner: '四川省信安 AWD 复盘: PHP 命令执行/SQL/上传修复 + Python Flask SSTI 批量攻击每轮 4000+ 分。'
lesson: 'AWD 修复策略: 1) 删漏洞代码/修 TRUE→FALSE/加白名单; 2) webshell 查杀; 3) 备份源代码; 4) 改弱口令; 5) 看日志找他人攻击 payload; 6) 批量攻击脚本。'
quality: medium
full_path: 四川省信息安全技术大赛_AWD部分WriteUp.full.md
meta_path: 四川省信息安全技术大赛_AWD部分WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '四川省信息安全技术大赛 AWD部分WriteUp。四川省信安 AWD 复盘: PHP 命令执行/SQL/上传修复 + Python Flask SSTI 批量攻击每轮 4000+ 分。。关键路径：初始 7w 分, 15 分钟一轮, 一轮 100 分, 最终 22w+ 分 → PHP 题: 整站 tar 备份 + D盾/河马 webshell 查杀 + seay 代码审计 → 命令执行: ma...'
category: web
subcategory: web_other
tools_used:
- Flask
- PHP
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/76769.html
reasoning_chain:
- '四川 AWD 复盘, 初始 7w 分, 15 分钟一轮 → 触发点: AWD 攻防同时进行 → 假设: 1) 修自己的洞, 2) 打别人得 flag'
- 'PHP 题: manage_comment_del.php + Manage_rce.php 命令执行 → 假设: 删代码修复 + D盾/河马查杀 → 动作: 整站 tar 备份 + seay 代码审计'
- 'manage_sql.php TRUE→FALSE 修复 → 任意 SQL 关闭 → 假设: 改查询逻辑 → 动作: 文件替换 / sed in-place'
- 'user_upload.php 文件上传 → 加白名单修复 → 触发点: 上传白名单 png/jpg → 动作: 修 mimetype 检查'
- 'Python 题 Flask blog + render_template_string SSTI → 触发点: 加固花括号过滤 → 假设: 攻击者找 render_template_string'
- '动作: 找 /auth/reset 路由 + render_template_string 漏洞 → 观察: 回显 flag 在 HTML 注释里 → 批量脚本每轮打 4000+ 分'
failed_attempts:
- '试图用复杂过滤绕过 → 失败: AWD 修洞比赛速度优先'
- '试图单挑打 → 失败: 必须批量脚本'
key_observations:
- 'AWD 修复策略: 删漏洞代码/修 TRUE→FALSE/加白名单'
- webshell 查杀 (D盾/河马) + 备份源代码 + 改弱口令 + 看日志
- 'Flask render_template_string SSTI 加固: 花括号过滤 {{ }}'
- 'AWD 节奏: 一轮 100 分, 必须批量脚本 (4000+ 分/轮)'
prerequisites:
- PHP 代码审计 (seay)
- Flask SSTI 原理 (render_template_string)
- D盾/河马 webshell 查杀
- 批量脚本编写 (Python 多线程 requests)
---
# 四川省信息安全技术大赛 AWD部分WriteUp

> 原文: https://www.ctfiot.com/76769.html
> ID: 76769

写在前面

有一年多没打过awd了，这次awd的题目正好遇到了会的，一道PHP一道python还有一个java，队伍里面正好有个java佬，直接起飞。

初始分七万，15分钟一轮，一个flag一百分，最后打了22w多分，我们14w分的时候第二名才11w，具体最后差我们多少不太清楚。

题外话：敢欺负我师弟？无所谓，我会出手。（

我主要做的php和python题，所以就说下这两道题怎么做的

PHP

由于前30分钟是加固时间，所以可以不慌不忙的把php修好。

php这道题拿到手SSH上去之后首先做的就是对网站进行整站备份，为了加快scp/sftp传输速度，直接tar压缩整站。

源代码搞下来之后用D盾、河马进行webshell查杀，使用seay进行自动代码审计，一共找到了两三个读flag点，一个文件上传点。

在复原的时候还是尽量按照AWD赛时的思路去还原，争取还原选手赛时最真实的思路。

备份下源代码之后我们尝试开启waf的流量记录功能或者weblogger，但是我们自己魔改后的waf开不起来，并且担心主办方check原版waf的路径，所以最后没有开waf。

weblogger部署之后站点无法正常访问，遂放弃，本次AWD PHP题所有的漏洞点均为人工审计得出。

接下来先随意看一下目录有没有隐藏文件或者敏感文件，在根目录发现db.sql，直接删掉

接下来根据经验去查看uploads目录是否有可疑文件

在检查完之后还需要做的就是连接数据库进行备份，这里我疏忽了忘记了备份，不过问题不大，应该是没有人能成功打进来我们的靶机进行提权或者破坏，不过无法确定，因为这次的平台没有给每道题的状态，如靶机是否down，每轮是否被check等，呵呵。

进入数据库之后要做的就是修改网站后台密码，这也是常识了，一般来说网站后台密码是弱口令，试了下123456还是admin来着就进去了。

这里改密码出了点问题，我以为密码是MD5之后的值 但是我md5之后的结果和网站存储的结果不太一样，所以后面我改掉之后自己的网站也没有再上去了，只要保证别人登不进去后台就可以，我自己需要的话可以在改回去默认的密码。

网站后台改完基本上数据库也OK了，接下来进行代码审计

命令执行与任意SQL执行

manage_comment_del.php

这个点有命令执行，但是我无法执行命令，因为当时加固阶段网站被waf搞down了，所以我直接修了

这里的修复方式同理，不再赘述。

Manage_rce.php

修复方式也很简单 直接把对应的代码删掉

manage_sql.php

这题给??整乐了，看到SQL注入都不load_file是吧，说句题外话，在打网站后台漏洞的时候我根本没打过rce，直接打SQL语句这个点，过了很久了大部分人还没修，乐。

把TRUE改成FALSE就可以修复了。

任意文件上传

user_upload.php

没啥过滤，修复方法如下

PHP题基本就到这里了，后面或许出了新洞，没有再审计了，一直在干flask内存马。

Python

python这题给了一个blog系统，是flask写的，那么我首先想到的就是模板注入。

代码看了半天也没啥收获，其实这里我的思路有点问题，我忘记直接去搜render_template_string了。直接搜的话可以在加固阶段直接定位到漏洞点。在加固阶段这题也没看出来啥，代码太多了，上去网站功能也很多，前两个小时就没怎么管这道题。

后面我们java和php题都搞完了之后发现有扣分，估计就是python题出问题了，好巧不巧根目录给了web日志

那么就可以充分发挥流量人的特长，看日志。

日志中有大量扫描器等垃圾流量，试了试不太行，最后发现扣分的时候一直有向/auth/reset路由发送请求，遂进入代码查看

看最后的渲染方法是什么，flask人狂喜，已经可以定位漏洞点就在这里了，我首先做的是修复，其次是批量攻击

这题修也非常简单，我直接把花括号过滤了,传了花括号直接返回

下面需要做的就是对这题进行利用，知道这个漏洞点之后我自己试了一下，但是并没有回显SSTI打过去的payload，比较奇怪，我以为是自己payload的问题，遂写了几句话看一下别人payload

最后看到payload就是最简单的ssti payload，由于备份没有存所以展示不了了。可以去看hackbar最简单的那个。

既然确定了是在这里利用漏洞，那么回显的flag在哪里？

我从burp直接看了render后的结果，然后翻了一下源代码发现回显结果是以注释的形式体现，所以这题也就解出来了，最后写脚本批量交，每一轮能打四千多分。

原文始发于Polo：四川省信息安全技术大赛 AWD部分WriteUp

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