---
title: N1CTF24 PHP Master Writeup
contest: N1CTF 2024
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [PHP_8.3_FPM, 单进程pm, frame_pointer, dl加载, O0_gcc, N1CTF_PHP_Master]
attack_chain:
  - 编译 PHP 8.3 FPM：CFLAGS="-O0 -g -fno-omit-frame-pointer" LIBS='-ldl'
  - ./configure --prefix=/opt/php-8.3 --enable-fpm --with-fpm-user=www-data --with-fpm-group=www-data --with-zlib
  - pm = static + pm.max_children = 1
  - 关闭多进程避免 fork 复杂化
key_payload: 'CFLAGS="-O0 -g -fno-omit-frame-pointer"'
one_liner: N1CTF24 PHP Master：PHP 8.3 FPM 单进程 pwn 编译配置。
lesson: PHP-FPM pwn 题编译保留 frame pointer + O0 优化；pm = static + max_children=1 避免多进程。
quality: medium
---

# N1CTF24 PHP Master Writeup

## 来源
- 原文：ctfiot.com/213627.html
- 比赛：N1CTF 2024

## 编译配置

### CFLAGS
```bash
CFLAGS="-O0 -g -fno-omit-frame-pointer"
LIBS='-ldl'
./configure \
  --prefix=/opt/php-8.3 \
  --enable-fpm \
  --with-fpm-user=www-data \
  --with-fpm-group=www-data \
  --with-zlib
```

### php-fpm.conf
```ini
pm = static
pm.max_children = 1
```

## 关键技巧
- **O0 优化**：不优化，便于逆向和堆栈分析
- **fno-omit-frame-pointer**：保留 RBP 寄存器用于栈帧回溯
- **-ldl 链接**：dlopen/dlsym 支持运行时加载扩展
- **pm = static**：单进程 pwn，无需处理 fork 后多进程状态

## 适用场景
- PHP-FPM 漏洞利用
- 高版本 PHP 8.x pwn
- 编译环境配置
