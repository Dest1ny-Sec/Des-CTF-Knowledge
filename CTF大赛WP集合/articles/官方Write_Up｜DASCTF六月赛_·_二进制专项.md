# 官方Write Up｜DASCTF六月赛 · 二进制专项

> 原文: https://www.ctfiot.com/118808.html
> ID: 118808

6月4日，DASCTF二进制专项赛于BUU平台顺利开赛。

本场竞赛特别邀请了国内知名战队的二进制优秀选手为赛事保驾护航。特此发布官方WP供大家复盘学习～

（点击文末“阅读原文”获得完整版WP）

REVERSE

unsym的解题思路

首先逆向分析go语言程序

使用Finger插件恢复部分比较关键的函数 从而看一看出来调用了一些大整数运算的函数

根据字符串把握程序大致的流程

根据关键点e=0x10001 可以推测该算法使用了RSA加密来校验输入的Key

使用Yafu分解大整数N 并且求出正确的Key

利用Key解密对应的文件即可 然后根据PE结构的特点修复PE结构

ez_exe的解题思路

解题步骤

首先识别程序是一个Python打包而成的exe文件

使用pycdc或者是在线网站 将exe文件解包为python程序源码

代码审计 然后根据python程序的key解密出bin2文件

逆向bin2文件 解密XXTea算法即可

babyRe的解题思路

首先动态调试 恢复几个API的符号

发现是一个线程注入的技术 注入的代码是从资源中解密出的shellcode

分析线程的shellcode 发现不能正确执行 (反调试的存在)

绕过反调试后 解密出shellcode 发现其实是个RC4加密

dump RC4加密

然后进行解密即可 放入ida x64分析即可

shellcode中存在大量的花指令 需要一一去除

careful的解题思路

解题步骤

动态调试 设置断点在 ds:gethostbyname 处

进入gethostbyname 内部其实存在了内联HOOK  hook了这个API函数 修改了传入的参数 然后调用真正的API

选手需要更进一步步入进入该内联函数分析

高级分析技巧:使用Wireshark 工具直接分析DNS域名解析协议

cap的解题思路

解题步骤

逆向分析程序

发现程序是一个截屏软件 并且会把截屏的图片进行加密

逆向加密的算法 写出exp进行解密

W

P

完整版链接

请师傅们点击【阅读原文】查看六月赛DASCTF【WP】完整版

往期精选

校企党建共建｜安恒信息与浙江经济职业技术学院达成战略合作

2023-04-14

安恒培训｜五月认证培训计划来袭！热门课程火热报名中～

2023-04-13

第六届西湖论剑·中国杭州网络安全技能大赛圆满收官！

2023-03-21


```
from Crypto.Util.number import *

p1 = getPrime(115)
p2 = getPrime(115)
print(p1)
print(p2)
print(p1*p2)
p=21154904887215748949280410616478423
q=37636318457745167234140808130156739
n=796192737278561537484199099160091818919833721026691718207595201542597
#print(pow(123,65535,n))
print(hex(p))
print(hex(q))
print(hex(n))
n = int("1d884d54d21694ccd120f145c8344b729b301e782c69a8f3073325b9c5",16)
print(n)
p = 37636318457745167234140808130156739
q = 21154904887215748949280410616478423
c = int("fad53ce897d2c26f8cad910417fbdd1f0f9a18f6c1748faca10299dc8",16)
e = 65537
phi = (p-1)*(q-1)
import gmpy2 
d = gmpy2.invert(e,phi)
m = pow(c,d,n)
print(long_to_bytes(m))

k1=[ord(i) for i in "you get the right key!"]
k2=[ord(i) for i in "VGhpc19pc19hX2Zha2Vfa2"]
for i,j in zip(k1,k2):
    print(i^j,end=',')
print()
from Crypto.Cipher import AES

key = b"E@sy_RSA_enc7ypt"
aes=AES.new(key,AES.MODE_CBC)
c = open("encrypted.bin","rb").read()
print(c)
m = aes.decrypt(c)
open("dec.dump","wb").write(m)

"""
    
    factor(796192737278561537484199099160091818919833721026691718207595201542597)

fac: factoring 796192737278561537484199099160091818919833721026691718207595201542597
fac: using pretesting plan: normal
fac: no tune info: using qs/gnfs crossover of 95 digits
div: primes less than 10000
fmt: 1000000 iterations
rho: x^2 + 3, starting 1000 iterations on C69
rho: x^2 + 2, starting 1000 iterations on C69
rho: x^2 + 1, starting 1000 iterations on C69
pm1: starting B1 = 150K, B2 = gmp-ecm default on C69
ecm: 30/30 curves on C69, B1=2K, B2=gmp-ecm default
ecm: 74/74 curves on C69, B1=11K, B2=gmp-ecm default
ecm: 44/44 curves on C69, B1=50K, B2=gmp-ecm default, ETA: 0 sec

starting SIQS on c69: 796192737278561537484199099160091818919833721026691718207595201542597

==== sieving in progress (1 thread):   11184 relations needed ====
====           Press ctrl-c to abort and save state           ====
10251 rels found: 4935 full + 5316 from 53214 partial, (1908.05 rels/sec)

SIQS elapsed time = 33.3969 seconds.
Total factoring time = 42.4275 seconds

***factors found***

P35 = 37636318457745167234140808130156739
P35 = 21154904887215748949280410616478423

ans = 1
"""
```



```
#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.11

import ctypes
from time import *
from ctypes import *
from ctypes import wintypes
from hashlib import md5

class _STARTUPINFO(Structure):
    _fields_ = [
        ('cb', c_ulong),
        ('lpReserved', c_char_p),
        ('lpDesktop', c_char_p),
        ('lpTitle', c_char_p),
        ('dwX', c_ulong),
        ('dwY', c_ulong),
        ('dwXSize', c_ulong),
        ('dwYSize', c_ulong),
        ('dwXCountChars', c_ulong),
        ('dwYCountChars', c_ulong),
        ('dwFillAttribute', c_ulong),
        ('dwFlags', c_ulong),
        ('wShowWindow', c_ushort),
        ('cbReserved2', c_ushort),
        ('lpReserved2', c_char_p),
        ('hStdInput', c_ulong),
        ('hStdOutput', c_ulong),
        ('hStdError', c_ulong)]

class _PROCESS_INFORMATION(Structure):
    _fields_ = [
        ('hProcess', c_void_p),
        ('hThread', c_void_p),
        ('dwProcessId', c_ulong),
        ('dwThreadId', c_ulong)]

StartupInfo = _STARTUPINFO()
ProcessInfo = _PROCESS_INFORMATION()
key1 = bytes(md5(b'bin1bin1bin1').hexdigest().encode())
file = open('bin1', 'rb').read()
arr = range(len(file))()
open('bin1', 'wb').write(bytes(arr))
sleep(0)
bet = ctypes.windll.kernel32.CreateProcessA(b'bin1', ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), byref(StartupInfo), byref(ProcessInfo))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ProcessInfo.hProcess), ctypes.c_int(-1))
open('bin1', 'wb').write(file)
```



```
import  marshal
f = open("ez_py.pyc","rb").read()
for i in range(0xff):
    tmp = f[i:]
    try:
        Pyobj = marshal.loads(tmp)
        import dis
        dis.dis(Pyobj)
        #break
    except:
        pass
```



```
arr=[key1[i%len(key1)]^file[i] for i in range(len(file))]
```



```
import ctypes
from time import *
from ctypes import *
from ctypes import wintypes
from hashlib import md5

key1 = bytes(md5(b"bin2bin2bin2").hexdigest().encode())
file = open("bin2","rb").read()
#这里仿照逆向出来的python源码 将bin2*3 的md5值作为秘钥key去解密key2
arr=[key1[i%len(key1)]^file[i] for i in range(len(file))]
open("dump","wb").write(bytes(arr))
#print(bytes(arr))
sleep(0)
```



```
#include <stdio.h>
#include <stdio.h>  
#include <stdint.h>  
#define DELTA 0x7937b99e  
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))  
 #include <Windows.h>
void btea(uint32_t *v, int n, uint32_t const key[4])  
{  
    uint32_t y, z, sum;  
    unsigned p, rounds, e;  
    if (n > 1)            /* Coding Part */  
    {  
        rounds =  52/n;  
        sum = 0;  
        z = v[n-1];  
        do  
        {  
            sum += DELTA;  
            e = (sum >> 2) & 3;  
            for (p=0; p<n-1; p++)  
            {  
                y = v[p+1];  
                z = v[p] += MX;  
            }  
            y = v[0];  
            z = v[n-1] += MX;  
        }  
        while (--rounds);  
    }  
    else if (n < -1)      /* Decoding Part */  
    {  
        n = -n;  
        rounds =  52/n;  
        sum = rounds*DELTA;  
        y = v[0];  
        do   
        {  
            e = (sum >> 2) & 3;  
            for (p=n-1; p>0; p--)  
            {  
                z = v[p-1];  
                y = v[p] -= MX;  
            }  
            z = v[n-1];  
            y = v[0] -= MX;  
            sum -= DELTA;  
        }  
        while (--rounds);  
    }  
}
int main()
{
 
 unsigned int key[]={0x4b5f,0xdead,0x11ed,0xb3cc};

 for(int i=0;i<11;i++)
 {
  //printf("0x%x,",cin1[i]);
 }
 //btea(cin1,-11,key);
 
 //puts("---");
 int enc[11]={0xcc45699d,0x683d5352,0xb8bb71a0,0xd3817ad,0x7547e79e,0x4bdd8c7c,0x95e25a81,0xc4525103,0x7049b46f,0x5417f77c,0x65567138};
 btea(enc,-11,key);
 printf("%s",enc);

 return 0;
}
```



```
f = open("COD101.bin","rb").read()
key=[24, 87, 104, 100]
arr = []
for i,j in enumerate(f):
    arr.append(key[i%4]^j)
open("dump","wb").write(bytes(arr))
```



```
#include <stdio.h>
int size1 = 0x100;

void __stdcall  rc4(char* data)
{
 unsigned char sbox[257] = { 0 };
 unsigned int i, j, k;
 int tmp;
 char key[] = { 93 ,66,98,41,3,54,71,65,21,54 };
 int len = 0;
 char* p = data;

 while (*p)
 {
  len++;
  p++;
 }
 //printf("len:%dn", len);
 for (i = 0; i < size1; i++) {
  sbox[i] = i;
 }

 j = k = 0;
 for (i = 0; i < size1; i++) {
  tmp = sbox[i];
  j = (2 * j + tmp + key[k]) % size1;
  sbox[i] = sbox[j];
  sbox[j] = tmp;
  if (++k >= 10)
   k = 0;
 }
 j = k = 0;
 int R;
 for (i = 0; i < len; i++) {
  j = (j + k) % size1;
  k = (k + sbox[j]) % size1;

  tmp = sbox[j];
  sbox[j] = sbox[k];
  sbox[k] = tmp;

  R = sbox[(sbox[j] + sbox[k] + k) % size1];
  data[i] -= (i % 13);
  data[i] ^= R ;
  
 }

}

int main()
{
 char enc[]={ 0xF7, 0x2E, 0x34, 0xF0, 0x72, 0xCF, 0x5E, 0x0A, 0xBB, 0xEC, 
  0xB1, 0x2B, 0x70, 0x88, 0x88, 0xED, 0x46, 0x38, 0xDB, 0xDA, 
  0x6C, 0xBD, 0xD4, 0x06, 0x77, 0xF2, 0xCF, 0x56, 0x88, 0xC6, 
  0x31, 0xD2, 0xB7, 0x5A, 0xC1, 0x42, 0xB0, 0xF4, 0x48, 0x37, 
  0xF5, 0x2C, 0xF5, 0x58};
 rc4(enc);
 printf("%s",enc);
 }
```



```
Just_An_APIH00k11.com
from hashlib import *
m = md5(b"Just_An_APIH00k11.com").hexdigest()
print("DASCTF{%s}"%m)
```



```
DASCTF{3d0bd550-edbe-11ed-b2a3-f1d90bff20c4}

def dec(buf,len,order):
    key=[ord(i) for i in "enc_by_dasctf"]
    arr=[]
    for i in range(len):
        arr.append(buf[i]^key[(i+order)%13])
    return bytes(arr)
f = open("cap.bin","rb")
buf1=f.read(14)
buf2=f.read(40)
buf3=f.read()

out1=dec(buf1,14,1)
out2=dec(buf2,40,2)
out3=dec(buf3,len(buf3),3)

outbuf=out1+out2+out3
open("out.bmp","wb").write(outbuf)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1685946496.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1685946496.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1685946496.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1685946497.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1685946497.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/9-1685946498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1685946498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1685946498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/7-1685946499.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1685946500.png)