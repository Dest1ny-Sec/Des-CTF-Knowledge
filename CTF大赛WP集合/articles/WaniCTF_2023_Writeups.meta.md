---
title: WaniCTF 2023 Writeups
contest: WaniCTF 2023
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [indexeddb_chrome, zip_path_traversal, http_range_2gb, aws_lambda_iam, image_magick_mvg, pngcrush_profile, exiftool_publisher_base64, usb_keyboard_parser, iso_9660]
attack_chain: extract1:indexedDB open testDB → objectStore.put({name:"FLAG{...}"}) / extract2:POST /file=x.zip multipart + target=flag 路径穿越 (含 PK 头) / 64bps:GET /2gb.txt Range: bytes=2147483648- 超 32 位偏移 / lapsus$:ImageMagick MVG SSRF+file:// 黑名单绕过 / aws:SecretUser IAM → aws iam get-policy-version → WaniLambdaGetFunc → lambda:GetFunction wani_function → S3 code / certified:POST /create file=../../../../../../proc/1/environ + target → image magick 错误回显 / chall.mp4 exiftool Publisher: flag_base64 / updog ISO 9660 + Usb_Keyboard_Parser.py pcap
key_payload: openRequest.onupgradeneeded = {objectStore.put({name:"FLAG{[redacted]}"})} / Range: bytes=2147483648- / aws iam get-policy-version --policy-arn arn:aws:iam::839865256996:policy/WaniLambdaGetFunc / exiftool Publisher : flag_base64:[redacted]
one_liner: WaniCTF 2023 全题型 WP，IndexedDB 浏览器数据 + zip 路径穿越 + HTTP Range 2GB 偏移 + AWS Lambda IAM 权限提升 + ImageMagick MVG SSRF + PNG tEXt profile + exiftool + USB HID。
lesson: HTTP Range 字节偏移 2147483648 触发整数溢出读 2GB 外内容；AWS IAM 用户即使 lambda:ListFunctions 被拒，也可通过 iam:GetPolicy 列举自己策略发现隐藏的 lambda:GetFunction 资源限制。
quality: high
---
