---
title: 第五空间 2022/Web + Pwn 合集
contest: 第五空间
year: 2022
difficulty: medium
vuln_type:
- sqli
- phar
- deserialize
- rce
- pwn_unknown
tags:
- upload 类 phar 触发
- GIF89a 头绕过
- __wakeup file_get_contents
- 报错注入
- 弱口令爆破
- 命令注入
- 空格过滤 ${IFS}
- ret2libc
attack_chain:
- Web1: phar 反序列化读 /flag
  - upload 类：filename=__construct 设 /flag；__wakeup 读 file_get_contents(filename)
  - phar metadata 存这个对象，phar:// 触发 file_exists 走 __wakeup
- Web2: 登录框宽字节报错注入 admin%df'^(SUBSTRING(select(user()),1,1)<>0x61)#
  - 爆 user()、database() 等
  - 弱口令 admin admin123
  - 命令注入：127.0.0.1%0acd${IFS}ky*%0als%0atac${IFS}fl*
- Pwn: 经典 ret2libc
  - 0x400753 pop rdi; ret → puts@GOT → puts@PLT → main
  - 泄 libc 基址 → /bin/sh + system
key_payload: "$phar->setMetadata(new upload(filename='/flag'))"
one_liner: phar 反序列化读 /flag + 报错注入 + 命令注入 + ret2libc 三题合集
lesson: phar:// 是 file_exists/exif/finfo 等函数都触发的反序列化入口；${IFS} 绕过空格过滤
quality: high
---

# 第五空间 2022/Web + Pwn 合集

**phar 反序列化读 flag + 报错注入 + 命令注入 + ret2libc**

> 第五空间 · 2022 · medium · sqli/phar/deserialize/rce/pwn · quality=high
> 思路: Web1 phar 触发 __wakeup file_get_contents('/flag') → Web2 报错注入 + ${IFS} 命令注入 → Pwn ret2libc 泄 libc + system
> 套路: phar:// 是 file_exists/exif/finfo 等函数都触发的反序列化入口；${IFS} 绕过空格过滤

**关键 payload**:
```php
$phar->setMetadata(new upload(filename='/flag'))
```
