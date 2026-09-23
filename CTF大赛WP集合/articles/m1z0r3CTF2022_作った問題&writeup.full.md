---
title: m1z0r3CTF 2022 作った問題 & writeup
contest: m1z0r3CTF
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags:
- lcg
- rsa-chain
- multi-prime
- prime-256bit
- custom-encrypt
- secret-png
- 16bit-prime
attack_chain:
- 'chall1: 未知 a, b, r, x (LCG)'
- 加密 = byte XOR LCG 输出
- 已知明文头部 (PNG 头 8 字节) 推导 LCG
- 'chall2: prime + 链式素数 + 16bit prime'
- 链式 q 拼接 next_prime
- 小明文 + 已知 gen_p 爆破
- 'chall3: getPrime(256) + 16bit 偏移 e'
- 16bit 偏移 ex + 2 字节 e 爆破
key_payload: LCG 已知明文恢复 + 链式 RSA + 16bit prime
one_liner: m1z0r3CTF 2022 三道密码学题：LCG 加密 + 链式 RSA + 16bit prime 拼接。
lesson: LCG 加密 + 已知明文攻击是经典题型；链式 prime RSA 的"prime 链"是近年新趋势。
quality: high
full_path: m1z0r3CTF2022_作った問題&writeup.full.md
meta_path: m1z0r3CTF2022_作った問題&writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'm1z0r3CTF 2022 作った問題 & writeup。m1z0r3CTF 2022 三道密码学题：LCG 加密 + 链式 RSA + 16bit prime 拼接。。关键路径：chall1: 未知 a, b, r, x (LCG) → 加密 = byte XOR LCG 输出 → 已知明文头部 (PNG 头 8 字节) 推导 LCG。经验：LCG 加密 + 已知明文攻击是经典题型；链...'
category: crypto
subcategory: rsa
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/84177.html
reasoning_chain:
- 触发点：3 题 + tag 'lcg' / 'rsa-chain' / 'multi-prime' / '16bit-prime' → 假设：LCG + 链式 RSA + 16bit prime
- chall1：加密 = byte XOR LCG 输出 → 假设：未知 a, b, r, x → 动作：已知明文头部 (PNG 头 8 字节) 推导 LCG
- 触发点：x = (a*x+b)%r 加密 PNG 头 → 假设：PNG 头 8 字节已知 → 动作：z3 解 4 未知数
- 动作：构建等式 → 观察：唯一解 → 还原 LCG → 解密 PNG
- chall2：链式素数 + 16bit prime → 触发点：encrypt 函数用 next_prime(prime + q) → 假设：每串 q 可拼 prime
- 动作：16bit q 暴力枚举 → 假设：找到下一个素数 → 观察：拼 prime 链 → 还原 N
- chall3：getPrime(256) + 16bit 偏移 e → 假设：e = (gen_p+offset) 16bit → 动作：枚举 offset + 2 字节 e 爆破
- 下一步：用 p, q, e 算 d 解密 → flag
failed_attempts:
- chall1 试图不解 LCG 直接暴力 → 失败：x 输出空间太大，必须先解 LCG 参数
- chall2 试图不枚举 q 直接分解 N → 失败：q 太短但 prime 链必须正确拼接
- chall3 试图不爆破 e → 失败：e 受 16bit 偏移限制
key_observations:
- LCG 加密 + 已知明文攻击是经典题型，已知 8 字节 PNG 头足够解 4 未知数
- 链式 prime RSA 的'prime 链'是近年新趋势（q 拼接到 prime 形成新素数）
- 16bit 偏移 e + 2 字节爆破 = 36bit 搜索空间，CPU 爆破足够
- PNG 文件头 8 字节是 0x89504E470D0A1A0A 标准签名
prerequisites:
- 线性同余生成器（LCG）参数恢复
- RSA 数论（phi / 模幂 / d = e^-1 mod phi）
- z3 约束求解器
- PNG 文件格式与签名
---
# m1z0r3CTF2022 作った問題&writeup

> 原文: https://www.ctfiot.com/84177.html
> ID: 84177


```
    #chall1.py
from Crypto.Util.number import long_to_bytes
import random

secret = open("secret.png","rb").read()

a = random.randrange(256)
b = random.randrange(256)
r = random.randrange(256)
x = random.randrange(256)

enc = 0
for s in secret:
 enc <<= 8
 x = (a*x+b)%r
 enc += s^x

f = open("encrypted_data.dat","wb")
f.write(long_to_bytes(enc))
from Crypto.Util.number import *

def encrypt(st_len,go_len,prime,message):
 s = 0
 l = 1
 c = []
 while st_len <= go_len:
 while True:
 q = getPrime(st_len)
 qbin = bin(q)[2:]
 while len(qbin) < st_len: qbin = "0" + qbin
 next_prime = int(bin(prime)[2:] + qbin,2)
 if isPrime(next_prime):
 N = prime * q
 m = bytes_to_long(message[s:s+l])
 e = 101
 if prime%e != 1 and q%e != 1:
 c.append(pow(m,e,N))
 prime = next_prime
 break
 st_len *= 2
 s += l
 l *= 2
 assert len(message) == s
 return c,N

flag = open("flag.txt","rb").read()
gen_p = getPrime(16)
c,N = encrypt(gen_p.bit_length(),256,gen_p,flag)
print(c)
# [923347949, 7382279973222128877, 122962146306170765837908848551223454567, 3549519152212014068083700234235160186300219130505299139696292306205464039799, 1527384673643022720120101064151977796913895264858932377772580237410767118686969106391529500139242897405662607203540127567551879700554668904837212450683883]
print(N)
# 6159034900797898425838526763919325877394844976323736393192254250464963575156530328240421294138007406960476709427205843365628191563244980986067184889098833
import random
from Crypto.Util.number import *

secret = open("secret.png","rb").read()
flag = open("flag.txt","rb").read().strip()
assert len(flag)%3 == 0
ex = random.randrange(len(secret)-1)
e = bytes_to_long(secret[ex:ex+2])
p = getPrime(256)
q = getPrime(256)
n = p*q
c = []
for i in range(0,len(flag),3):
 m = bytes_to_long(flag[i:i+3])
 c.append(pow(m,e,n))
print(c)
# [6298113965475853786056847106208713300642945466885637995557170104494725950616074542425506023987217363886529665397919957618261581053133941027535155746435321, 135028125411958273916880824261545147614327725922209748340303390558194571689687977032589044265126382565916547879777234892642296715526896605761082569309957, 1321747274929612152457518915168588918356514442679554382787182364164828302372180029740168631933681540647333144180952171045221159999310072594994307374026397, 2918560933591924342981380338403848413183651470512194619662681532592047008257668515013412096463534685052633599782673614961906361066771670231196673146753898, 5775447489821919812656223325306418654099675333689382733144673190079859607549709791366025032709099098614570746711061453405145141567455154943434221193937600, 1274850466517264624838781305598541289691584629758963818109637778738466734330749252973718909288129468236472225834841856001947077472220670167226069634313329, 1303782230905842229285244210919421873678385109856332605169575017604438212677510463647334165086069519414714376999894517045356733235945921910952902514007317]
"m1z"^e - 対応した暗号文
"0r3"^e - 対応した暗号文
・16bitの素数pとflag(とその他諸々)を引数とする
・暗号化?回目
1. pと同じ大きさの素数qを生成する
2. binaryでpとqを繋ぎ合わせた値が素数であれば3に、そうでないなら1に進む
3. e = 101, N = pqとしてRSAで暗号化
4. 暗号化するmはflagの先頭2^(?−1)文字。一度暗号化した文字は暗号化しない。
5. pが256bitとなれば暗号化終わり。
6. p = pとqを繋ぎ合わせた値
7. 暗号化?回目終了、1へ。
・最後のNと暗号文のリストを公開
```
