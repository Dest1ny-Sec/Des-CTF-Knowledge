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
key_payload: 'new PDO("uri:phar://phar.phar/mysql:host=localhost;dbname=test", $user, $pass)'
one_liner: PDO dsn_from_uri 触发 phar 反序列化拿 shell
lesson: PHP PDO 的 pgsqlCopyFromFile、dsn_from_uri 等内部函数可作为 phar 反序列化触发点
quality: medium
---

# 春秋杯 2022/sql_debug

**PDO dsn_from_uri 触发 phar 反序列化拿 shell**

> 春秋杯 · 2022 · medium · deserialize/phar/rce · quality=medium
> 思路: Nette 框架 install.php 可改数据库配置 → 数据库用 PDO 连接 → 找 PDO 内部 phar 触发点 → 发现 pdo pgsqlCopyFromFile 函数可触发 phar → 搜 PHP 源码找 phar 反序列化入口函数 dsn_from_uri → 构造 PDO dsn="uri:phar://phar.phar/..." 触发 phar 反序列化 → 挖 Nette POP 链子写入 install.lock → 打 Phar 拿 shell
> 套路: PHP PDO 的 pgsqlCopyFromFile、dsn_from_uri 等内部函数可作为 phar 反序列化触发点

**关键 payload**:
```php
new PDO("uri:phar://phar.phar/mysql:host=localhost;dbname=test", $user, $pass)
```
