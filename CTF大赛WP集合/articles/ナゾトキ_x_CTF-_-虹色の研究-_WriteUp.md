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
```



```
┌──(kali㉿kali)-[~/work/nazotoki_7color/1st_red]
└─$ strings 1_Reversing | grep -E "((nazo)|(777)|(flag))"
flag.txt
t mind. I'm looking for the 777.
flag
```



```
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
```



```
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
```



```
┌──(kali㉿kali)-[~/work/nazotoki_7color/1st_yellow]
└─$ binwalk -e 3_Forensics.png 

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
0 0x0 PNG image, 1000 x 1333, 8-bit/color RGB, interlaced
78 0x4E Zlib compressed data, best compression
2127564 0x2076CC PNG image, 115 x 20, 8-bit/color RGB, interlaced
2127642 0x20771A Zlib compressed data, best compression
```



```
┌──(kali㉿kali)-[~/work/nazotoki_7color/1st_yellow]
└─$ split -b 2127564 3_Forensics.png --additional-suffix .png
```



```
Line-based text data: text/html (10 lines)
 <!DOCTYPE html>\r\n
 <html lang="ja">\r\n
 <head>\r\n
 <meta charset="UTF-8">\r\n
 <title>青</title>\r\n
 </head>\r\n
 <body>\r\n
 <a href="secret/flag.html">secret</a>\r\n
 </body>\r\n
 </html>\r\n
```



```
Hypertext Transfer Protocol
 HTTP/1.1 401 Unauthorized\r\n
 :
 WWW-Authenticate: Basic realm="Restricted Content"\r\n
 :
```



```
(リクエスト)
Hypertext Transfer Protocol
 GET /secret/flag.html HTTP/1.1\r\n
 :
 Authorization: Basic bmF6b3Rva2lDVEY6T0FVVEg=\r\n
 Credentials: ※ここの文字をフラグ形式にするとよい※
 :
```



```
(レスポンス)
<!DOCTYPE html>\r\n
<html lang="ja">\r\n
<head>\r\n
 <meta charset="UTF-8">\r\n
 <meta name="viewport" content="width=device-width, initial-scale=1.0">\r\n
 <title>blue</title>\r\n
</head>\r\n
<body>\r\n
 The basic flag is in the password on this page.\r\n
</body>\r\n
</html>\r\n
```



```
{
 "answer": "Number not found"
}
```
