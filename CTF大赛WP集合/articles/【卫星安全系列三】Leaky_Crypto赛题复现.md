# 【卫星安全系列三】Leaky Crypto赛题复现

> 原文: https://www.ctfiot.com/151037.html
> ID: 151037

一道卫星上AES侧信道攻击的题目，主要利用AES T-表的Cache缓存碰撞实施攻击。

题目描述

题目文件：

https://github.com/ADDVulcan/ADDVulcan/tree/master/Payload%20Modules/Leaky%20Crypto

题目有两个文件，Readme.txt文件是题目描述，大概意思是题目使用AES-128的ECB模式和前6字节为97ca6080f575的密钥加密了flag，密文是：

7972c157dad7b858596ecdb798877cc4ed4b03d6822295954e69b7ecebb704af08c054a03a374f8bdaa18ff16ba09be2b6b25f1ef73ef80111646de84cd3af2514501e056889e95c680f7d199b6531e9dd6ee599aeb23835327e6e853a9a40a9f405bd1443e014363ea46631582b97c3d3f83f4e1101da2557f9b03808a61968

test.txt文件是题目附件，其中给了100000个明文和其对应的加密时间，如：

2c86f81fdc568d631c9dd0a075ec2a35,10776
5e7b2322d8a2dabd86884d42de3748c8,10704
3ebac48a8c3b0a3b552c385eafc7f99a,10776
54f865a9cc7a3a1bcf68bad09d0b699a,10704
... ...

在Readme.txt文件中还有一点提示，最有用的是解这题需要用到侧信道攻击（Side Channel Attacks）。

搜集一下关于AES侧信道的资料，可以翻到有一种对AES的T-表进行侧信道攻击，恰好可以用来攻击这道题目。

AES、T-Table和缓存碰撞

在了解攻击前，需要知道一点前置知识。

AES的详细流程非常复杂，这里不多说，建议先去参考教科书或CTF Wiki学习学习。

简要来说的话，AES主要有以下4个操作：

轮密钥加，AddRoundKey

字节替换，SubBytes

行移位，ShiftRows

列混淆，MixColumns

如果在

生成时

的输入恰好是

，就会触发一次Cache Hits，CPU只需直接拿缓存中的对应数据。

如果在

生成时

的输入不是

，就会触发一次Cache Misses，CPU需要从更远的内存中获取这个数据，然后（可能会）用这个数据覆盖缓存中对应位置的数据。

：

：


```
https://github.com/ADDVulcan/ADDVulcan/tree/master/Payload%20Modules/Leaky%20Crypto
7972c157dad7b858596ecdb798877cc4ed4b03d6822295954e69b7ecebb704af08c054a03a374f8bdaa18ff16ba09be2b6b25f1ef73ef80111646de84cd3af2514501e056889e95c680f7d199b6531e9dd6ee599aeb23835327e6e853a9a40a9f405bd1443e014363ea46631582b97c3d3f83f4e1101da2557f9b03808a61968
2c86f81fdc568d631c9dd0a075ec2a35,10776
5e7b2322d8a2dabd86884d42de3748c8,10704
3ebac48a8c3b0a3b552c385eafc7f99a,10776
54f865a9cc7a3a1bcf68bad09d0b699a,10704
... ...
P -> AddRoundKey ->
SubBytes -> ShiftRows -> MixColumns -> AddRoundKey ->
... (9 Rounds) ...
SubBytes -> ShiftRows -> MixColumns -> AddRoundKey ->
SubBytes -> ShiftRows -> MixColumns -> C
ShiftRows -> SubBytes -> MixColumns -> AddRoundKey
轮密钥加 -> 查T-表 -> 轮密钥加 ...
THRESHOLD = 10

with open('./test.txt', 'r') as f:
    raw_data = f.read()

data = []
for d in raw_data.split('n')[:-1]:
    tmp = d.split(',')
    tmp[0] = bytes.fromhex(tmp[0])
    tmp[1] = int(tmp[1])
    data += [tmp]

key = bytes.fromhex('97ca6080f575')

def mean(l):
    assert isinstance(l, list)
    return sum(l) / len(l)

def check(i, j, ki, kj):
    col = []
    ncol = []

    for di in range(len(data)):
        p, t = data[di]
        if p[i] ^ ki == p[j] ^ kj:
            col += [t]
        else:
            ncol += [t]
    r = mean(ncol) - mean(col)
    if r < THRESHOLD:
        return None
    return r

def test(i, j):
    ki = key[i]
    for kj in range(256):
        r = check(i, j, ki, kj)
        if r:
            print((i, j), hex(kj), r)

if __name__ == '__main__':
    test(4, 8)

'''
(4, 8) 0xe4 24.571021646042936
(4, 8) 0xe5 20.58349909921526
(4, 8) 0xe6 23.138921452926297
(4, 8) 0xe7 24.225824547616867
'''
0 ->  4 ->  8 ;
12 ->  5 ->  9 -> 13 ;
 1 -> 10 -> 14 ->  2 ;
 6 -> 15 ->  3 ->  7 ;
11 ;
4 ->  8 ;
 5 -> 12 ;
 5 ->  9 -> 13 ;
 1 -> 10 ;
 2 -> 14 ;
 3 ->  7 ;
 3 -> 15 ->  6 ;
THRESHOLD = 10

with open('./test.txt', 'r') as f:
    raw_data = f.read()

data = []
for d in raw_data.split('n')[:-1]:
    tmp = d.split(',')
    tmp[0] = bytes.fromhex(tmp[0])
    tmp[1] = int(tmp[1])
    data += [tmp]

key = bytes.fromhex('97ca6080f575')

key = [set([ki]) for ki in key] + [set() for _ in range(16 - len(key))]
print(key)

def mean(l):
    assert isinstance(l, list)
    return sum(l) / len(l)

def check(i, j, ki, kj):
    col = []
    ncol = []

    for di in range(len(data)):
        p, t = data[di]
        if p[i] ^ ki == p[j] ^ kj:
            col += [t]
        else:
            ncol += [t]
    r = mean(ncol) - mean(col)
    if r < THRESHOLD:
        return None
    return r

def hack(chains):
    for chi in chains:
        print(chi)
        i, j = chi
        for ki in list(key[i]):
            for kj in range(256):
                r = check(i, j, ki, kj)
                if r:
                    print((i, j), hex(kj), r)
                    if j > 5:
                        key[j].add(kj)
        print(key)
        print()

chains = [
    (0, 4), (4, 8),
    (5, 9), (9, 13), (5, 12),
    (1, 10), (2, 14), (10, 14),
    (3, 7), (3, 15), (15, 6)
]

    #hack(chains)
key = [{151}, {202}, {96}, {128}, {245}, {117}, {228, 229, 230, 231}, {68, 69, 70, 71}, {228, 229, 230, 231}, {84, 85, 86, 87}, {244, 245, 246, 247}, set(), {188, 189, 190, 191}, {20, 21, 22, 23}, {104, 105, 106, 107}, {92, 93, 94, 95}]
print(key)
print()

import itertools
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tqdm import tqdm
from math import prod

c = bytes.fromhex('7972c157dad7b858596ecdb798877cc4ed4b03d6822295954e69b7ecebb704af08c054a03a374f8bdaa18ff16ba09be2b6b25f1ef73ef80111646de84cd3af2514501e056889e95c680f7d199b6531e9dd6ee599aeb23835327e6e853a9a40a9f405bd1443e014363ea46631582b97c3d3f83f4e1101da2557f9b03808a61968')
key = [list(ki) if ki else list(range(256)) for ki in key]
print(key)
print()

for k16 in tqdm(itertools.product(*key), total=prod([len(ki) for ki in key])):
    k = bytes(k16)
    aes = AES.new(k, AES.MODE_ECB)
    p = aes.decrypt(c)
    try:
        p = unpad(p, 16)
    
except:
        continue
    if b'flag' in p:
        print(k.hex())
        print(p)
        print()

'''
 66%|████████████████████████████▏              | 43992636/67108864 [18:25<09:26, 40781.32it/s]
97ca6080f575e646e557f755bf15685e
b'flag{uniform54349juliet:
GL2aGs7ys8ygcW0kFBPLbwEdjLbwNltiPdX_ANqtOFbUpEh_ciY8tWZd4y2VblkUhOl-PxXJdJYK86pIHmmwcw0}'
'''
```
