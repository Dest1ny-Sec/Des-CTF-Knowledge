# N1CTF24 PHP Master Writeup

> 原文: https://www.ctfiot.com/213627.html
> ID: 213627


```
1
CFLAGS="-O0 -g -fno-omit-frame-pointer" LIBS='-ldl' ./configure --prefix=/opt/php-8.3 --enable-fpm --with-fpm-user=www-data --with-fpm-group=www-data --with-zlib
1
2
pm = static
pm.max_children = 1
```
