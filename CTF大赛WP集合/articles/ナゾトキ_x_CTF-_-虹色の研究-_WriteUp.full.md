---
title: ナゾトキ x CTF? - 虹色の研究 - WriteUp
contest: ナゾトキ
year: 2023
difficulty: easy
vuln_type: reverse
tags:
- 虹色の研究
- MineNumber-7
- reversing
- decompile
- ASCII-sum
- '0x309'
- 7 color
- 日语
attack_chain: 1. nc 12345 启动 MineNumber Search Engine /2. 输入名字生成 MineNumber /3. strings + grep flag/4. 反编译：local_58 字符串 ASCII 求和 /5. 输入名字 ASCII 和 = 0x309 (777) 触发 flag
key_payload: local_64 == 0x309  name ASCII sum = 777  flag.txt
one_liner: ナゾトキ x CTF 虹色の研究（日语 CTF 入门题），MineNumber=777 触发 flag 字符串输出。
lesson: 日语 CTF 入场题；ASCII 字符求和触发 flag 是入门级；strings + grep 找 flag 字符串；反编译看比较常量 0x309。
quality: medium
full_path: ナゾトキ_x_CTF-_-虹色の研究-_WriteUp.full.md
meta_path: ナゾトキ_x_CTF-_-虹色の研究-_WriteUp.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: ナゾトキ x CTF? - 虹色の研究 - WriteUp。ナゾトキ x CTF 虹色の研究（日语 CTF 入门题），MineNumber=777 触发 flag 字符串输出。。经验：日语 CTF 入场题；ASCII 字符求和触发 flag 是入门级；strings + grep 找 flag 字符串；...
category: reverse
subcategory: reverse
tools_used:
- netcat
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/117900.html
reasoning_chain:
- 'nc xxx:12345 → MineNumber Search Engine → 触发点: 输入名字生成 MineNumber'
- 'strings 1_Reversing | grep -E ''flag|777|nazo'' → 观察: flag.txt + ''looking for the 777'''
- '假设: MineNumber=777 触发 flag → 反编译: while 循环对 name 字符 ASCII 求和'
- '动作: 让 local_64 == 0x309 (777) → 输入名字 ASCII 和 = 777 → flag 输出'
- '黄题: binwalk -e 3_Forensics.png → 假设: 嵌图 + 隐写'
- '观察: binwalk 拆出 115x20 PNG + HTML 含 secret/flag.html'
- '动作: 401 Unauthorized + Basic Auth bmF6b3Rva2lDVEY6T0FVVEg= → base64 解 → ''nazotokiCTF:OAUTH'''
- '青题: Vigenere 密码解 FWTS ZSEHVQ... → key=''VIGENERE'' → 明文是日语提示'
failed_attempts:
- '试图直接 strings 找完整 flag → 失败: 只是字符串提示, 真 flag 在 sum=777 触发里'
- 'binwalk 默认不解压 → 失败: 加 -e 才拆分嵌套 PNG'
key_observations:
- 日语 CTF = 字符串题 + 古典密码 (Vigenere) + binwalk 隐写
- ASCII 字符求和触发 = 入门级条件分支, 反编译看比较常量 0x309
- binwalk -e 是拆嵌图/嵌压缩包的标准动作
- Vigenere key='VIGENERE' 这种自指 key 是入门题常见梗
prerequisites:
- strings/grep 反编译前字符串搜索
- ASCII 累加条件分支逆向
- binwalk 嵌图/嵌压缩包分离
- Vigenere 古典密码手工/脚本解密
---
# ナゾトキ x CTF? -虹色の研究- WriteUp

> 原文: https://www.ctfiot.com/117900.html
> ID: 117900


```
┌──(kali㉿kali)-[~]
└─$ nc xxx.xxx.xxx.xxx 12345
************************
MineNumber Search Engine
************************
Enter your name:
DonGury
Your MineNumber is : 712
Don’t mind. I'm looking for the 777.
┌──(kali㉿kali)-[~/work/nazotoki_7color/1st_red]
└─$ strings 1_Reversing | grep -E "((nazo)|(777)|(flag))"
flag.txt
t mind. I'm looking for the 777.
flag
// デコンパイルしたコード
while ((local_60 < 0x40 && (local_58[(int)local_60] != 10))) {
 local_64 = local_64 + (int)local_58[(int)local_60];
 local_60 = local_60 + 1;
}
printf("Your MineNumber is : %d\n",(ulong)local_64);
if (local_64 == 0x309) {
 puts(flag);
 puts("You are the luckiest!");
}
# ヴェジェネル暗号で暗号化された文字列を復号するサンプルコード
enc_code = "FWTS ZSEHVQ TS XSKEZ PG WHMU HZAA.WHMU XJPG WRX LWZZ OH AS ICVSA HRWL."
key = "VIGENERE"

A_ASCII = ord('A')
ALFABET_NUM = ord('Z') - (A_ASCII - 1)

dec_code = ""
i_key = 0

for i in range(0,len(enc_code)):
 if enc_code[i] == " " or enc_code[i] == ".":
 dec_code = dec_code + enc_code[i]
 next
 else:
 tmp_num = ord(enc_code[i]) - (ord(key[i_key]) - A_ASCII)
 if tmp_num < A_ASCII:
 tmp_num = tmp_num + ALFABET_NUM

 dec_code = dec_code + chr(tmp_num)

 i_key = i_key + 1
 if i_key >= len(key):
 i_key = 0

print(dec_code)
┌──(kali㉿kali)-[~/work/nazotoki_7color/1st_yellow]
└─$ binwalk -e 3_Forensics.png

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
0 0x0 PNG image, 1000 x 1333, 8-bit/color RGB, interlaced
78 0x4E Zlib compressed data, best compression
2127564 0x2076CC PNG image, 115 x 20, 8-bit/color RGB, interlaced
2127642 0x20771A Zlib compressed data, best compression
┌──(kali㉿kali)-[~/work/nazotoki_7color/1st_yellow]
└─$ split -b 2127564 3_Forensics.png --additional-suffix .png
Line-based text data: text/html (10 lines)
 <!DOCTYPE html>\r\n
 <html lang="ja">\r\n
 <head>\r\n
 <meta charset="UTF-8">\r\n
 <title>青</title>\r\n
 </head>\r\n
 \r\n
 [secret](secret/flag.html)\r\n
 \r\n
 </html>\r\n
Hypertext Transfer Protocol
 HTTP/1.1 401 Unauthorized\r\n
 :
 WWW-Authenticate: Basic realm="Restricted Content"\r\n
 :
(リクエスト)
Hypertext Transfer Protocol
 GET /secret/flag.html HTTP/1.1\r\n
 :
 Authorization: Basic bmF6b3Rva2lDVEY6T0FVVEg=\r\n
 Credentials: ※ここの文字をフラグ形式にするとよい※
 :
(レスポンス)
<!DOCTYPE html>\r\n
<html lang="ja">\r\n
<head>\r\n
 <meta charset="UTF-8">\r\n
 <meta name="viewport" content="width=device-width, initial-scale=1.0">\r\n
 <title>blue</title>\r\n
</head>\r\n
\r\n
 The basic flag is in the password on this page.\r\n
\r\n
</html>\r\n
{
 "answer": "Number not found"
}
```
