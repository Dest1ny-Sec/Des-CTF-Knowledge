---
title: 2023 年春秋杯网络安全冬季联赛 RDG 部分 Writeup
contest: 春秋杯冬季联赛 2023
year: 2023
difficulty: easy
vuln_type: web_unknown
tags: [CodeIgniter_PHP, 文件上传, allowed_types_wildcard, 命令注入, Patient.php, RDG]
attack_chain:
  - application/controllers/Patient.php 文件上传功能
  - allowed_types='*' 未限制文件类型
  - 头像设置位置有命令注入
  - 修复：限制 allowed_types + 去掉自定义 binary
key_payload: 'allowed_types=*'
one_liner: RDG 漏洞定位：CodeIgniter 文件上传 allowed_types 通配 + 头像命令注入。
lesson: allowed_types='*' 是经典漏洞；用户头像二进制文件应固定为 file 工具。
quality: low
---

# 2023 年春秋杯网络安全冬季联赛 RDG 部分 Writeup

## 来源
- 原文：ctfiot.com/170482.html
- 比赛：春秋杯冬季联赛 RDG 部分

## 漏洞定位

### 漏洞 1：文件上传 allowed_types 通配
- `application/controllers/Patient.php`
- `allowed_types='*'` 未限制文件类型
- 可上传 PHP webshell

**修复**：添加文件名过滤规则
```php
$config['allowed_types'] = 'gif|jpg|png';
```

### 漏洞 2：头像设置命令注入
- 自定义 binary 路径
- 用户可控二进制文件路径触发命令注入

**修复**：去掉自定义 binary
```php
$bin_file = "file";
```

## 关键技巧
- **CodeIgniter 文件上传**：`$config['allowed_types']` 配置
- **命令注入检测**：grep 用户输入是否进 exec/system 调用
- **RDG（红队防御）**：从代码角度定位漏洞

## 适用场景
- PHP 文件上传漏洞
- 命令注入审计
- CodeIgniter 框架
