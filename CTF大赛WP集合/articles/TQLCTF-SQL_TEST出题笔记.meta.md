---
title: TQLCTF/SQL_TEST 出题笔记
contest: TQLCTF
year: null
difficulty: medium
vuln_type:
- sqli
- phar
- deserialize
- rce
tags:
- mysqli_options
- MYSQLI_INIT_COMMAND
- time-based blind
- secure_file_priv
- INTO DUMPFILE
- Symfony
- Doctrine
- RedisProxy
- Dumper
- phar 触发链
attack_chain:
- 审 Symfony 控制器：/test 路由接受 key + value 两个 GET 参数
- mysqli_options($con, $key, $value) 任意调用（key 是数字 option，value 是 string）
- 关键 option: MYSQLI_INIT_COMMAND=3 → 发送 SQL 命令作为连接初始化
- 强制禁用 LOCAL INFILE，再用 MYSQLI_OPT_LOCAL_INFILE=0
- 但 MYSQLI_INIT_COMMAND 走的是 init_command 通道，不受 LOCAL INFILE 限制
- 用 time-based blind 注 secure_file_priv 路径（select if((select substr(@@global.secure_file_priv, i, 1)='x'), sleep(2), 1)）
- 得到 secure_file_priv 路径（如 /tmp/xxx/）
- 用 INTO DUMPFILE 把 phar 写入该路径（select 0x<hex> into dumpfile '/tmp/xxx/random.phar'）
- 用 phar://random.phar 触发 phar 反序列化
- Symfony Doctrine 反序列化链：RedisProxy.__call → Dumper.__invoke → system()
- 命令执行拿 flag
key_payload: "mysqli_options($con, MYSQLI_INIT_COMMAND, 'select 0x<phar_hex> into dumpfile \"/tmp/xxx/random.phar\"')"
one_liner: MYSQLI_INIT_COMMAND 注入 + secure_file_priv 盲注 + INTO DUMPFILE 写 phar + Doctrine 反序列化链 RCE
lesson: PHP mysqli_options 接受任意 option 编号 + 任意 string value；MYSQLI_INIT_COMMAND 通道不受 LOCAL INFILE 禁用影响；Symfony Doctrine 反序列化链通过 RedisProxy.__call 触发
quality: high
---

# TQLCTF/SQL_TEST 出题笔记

**MYSQLI_INIT_COMMAND 注入 + secure_file_priv 盲注 + INTO DUMPFILE 写 phar + Doctrine 反序列化链 RCE**

> TQLCTF · ? · medium · sqli/phar/deserialize/rce · quality=high
> 思路: 审 Symfony 控制器：/test 路由接受 key + value 两个 GET 参数 → mysqli_options($con, $key, $value) 任意调用（key 是数字 option，value 是 string） → 关键 option: MYSQLI_INIT_COMMAND=3 → 发送 SQL 命令作为连接初始化 → 强制禁用 LOCAL INFILE，再用 MYSQLI_OPT_LOCAL_INFILE=0 → 但 MYSQLI_INIT_COMMAND 走的是 init_command 通道，不受 LOCAL INFILE 限制 → 用 time-based blind 注 secure_file_priv 路径 → 用 INTO DUMPFILE 把 phar 写入该路径 → 用 phar://random.phar 触发 phar 反序列化 → Symfony Doctrine 反序列化链：RedisProxy.__call → Dumper.__invoke → system() → 命令执行拿 flag
> 套路: PHP mysqli_options 接受任意 option 编号 + 任意 string value；MYSQLI_INIT_COMMAND 通道不受 LOCAL INFILE 禁用影响；Symfony Doctrine 反序列化链通过 RedisProxy.__call 触发

**关键 payload**:
```php
mysqli_options($con, MYSQLI_INIT_COMMAND, 'select 0x<phar_hex> into dumpfile "/tmp/xxx/random.phar"')
```
