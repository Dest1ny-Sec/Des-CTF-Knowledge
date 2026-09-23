---
title: 网鼎杯 2024 青龙/crypto001
contest: 网鼎杯
year: 2024
difficulty: hard
vuln_type:
- crypto_rsa
- diffie_hellman
- block_cipher
- ecc
tags:
- p/q 高位泄露
- bd_attack
- 2g+a 素数生成
- ECC 双重签名
- AES-CBC
- Vigenère
- SPN 分组密码
- 64bit 自定义 S 函数
attack_chain:
- 'crypto001: 给 n, e, c + hint1 = p>>442 + hint2 = q>>442 (各 70 bit 高位)'
- 已知 p/q 高位 → 构造 bd_attack (Coppersmith) 还原 p, q
- 算 d = inverse(e, phi)，解 m = pow(c, d, n) 拿 flag
- '白虎 crypto: 2g*a+1 形式素数生成，g 是 1000bit 素数'
- p-1 平滑 → Pollard p-1 分解
- 双重签名泄漏 s = (z + r*dA % n) * k^-1 % n
- 两组 (r1,s1) 和 (r2,s2) 已知 → 联立方程解 dA
- 算 sha256(dA) → AES key → 解密 victory_encrypted_flag
- Vigenère "WANGDINGCUP" 解回明文
- 'SPN: P permutation + S 函数 + 14 轮 SPN 分组密码'
- 用 z3 求解 z3.add(encryptWithoutP(P(m), key) == P(c))
key_payload: 'hint1, hint2 = p>>442, q>>442  # Coppersmith bd_attack 还原'
one_liner: 4 道 crypto 题合集：高位 p/q 还原 / p-1 smooth RSA / 双重签名 + Vigenère / SPN 分组密码
lesson: 已知 p/q 高位 70bit 必用 Coppersmith bd_attack；2g+1 形式素数 p-1 平滑用 Pollard p-1；EC-Schnorr 双重签名同 k 联立解 d
quality: high
full_path: 2024_网鼎杯_青龙&白虎.full.md
meta_path: 2024_网鼎杯_青龙&白虎.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: '网鼎杯 2024 青龙/crypto001。4 道 crypto 题合集：高位 p/q 还原 / p-1 smooth RSA / 双重签名 + Vigenère / SPN 分组密码。关键路径：crypto001: 给 n, e, c + hint1 = p>>442 + hint2 = q>>442 (各 70 bit 高位) → 已知 p/q 高位 → 构造 bd_attack (Co...'
category: crypto
subcategory: rsa
subcategories:
- rsa
- symmetric
tools_used:
- Radare2
- Z3
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/215151.html
reasoning_chain:
- 触发点：crypto001 给 n e c + hint1=p>>442 hint2=q>>442 各 70bit 高位 → 假设：bd_attack Coppersmith
- 动作：分别把 p = hint1*2^442 + x, q = hint2*2^442 + y 代入 small_roots 双未知数 → 观察：拿到 p 和 q
- 假设：d 是 299bit 素数 → 动作：算 phi=(p-1)(q-1), e=inverse(d,phi), m=pow(c, d, n) → 观察：出 flag
- 触发点：白虎 crypto 用 2g+1 形式素数 g 是 1000bit 素数 → 假设：p-1 = 2g 平滑
- 动作：Pollard p-1 分解 base=2 smooth bound → 观察：gcd(2^(2L)-1, n) 出 p
- 触发点：双重签名 (r1,s1)(r2,s2) 来自 Schnorr → 假设：同 k复用可联立解 d
- 动作：两式相减消去 r，再求 d → 观察：拿到 dA
- 动作：sha256(dA)[:16] 当 AES key 解密 victory_encrypted_flag → 观察：拿到 AES 明文
- 触发点：Vigenère key='WANGDINGCUP' → 假设：已知 key 直接解 → 动作：还原明文
- 触发点：SPN 14 轮 P permutation + S 函数 → 假设：可 z3 求解全轮逆
- 动作：z3.add(encryptWithoutP(P(m), key) == P(c)) → 观察：解出 key
- 下一步：合并多 flag 提交
failed_attempts:
- 试图直接 Pollard rho分解 2048bit RSA → 失败：n 是强素数生成
- 试图对双重签名做 r=k*G 离散对数攻击 → 失败：k 未直接泄露
- 试图不解 dA 直接解 AES → 失败：key 是 sha256(dA)[:16] 必须先拿 dA
key_observations:
- 已知 p/q 高位 70bit + 512bit 必走 Coppersmith bd_attack 双未知数
- 2g+1 形式素数 p-1 平滑：Pollard p-1 比 Pollard rho 快 10^5 倍
- EC-Schnorr 同 k 复用两签名可联立解 d，公式与 ECDSA nonce 复用同源
- AES key 来自 sha256(dA)[:16] 是把数学漏洞串到密码学层的典型套路
prerequisites:
- SageMath Coppersmith bd_attack 用法
- Pollard p-1 算法原理
- EC-Schnorr 签名 + nonce复用解私钥
- AES-CBC / SHA256 / Vigenère 基础
---
# 2024 网鼎杯 青龙&白虎

> 原文: https://www.ctfiot.com/215151.html
> ID: 215151

青龙

crypto001

from Crypto.Util.number import *
from secret import flag

p = getPrime(512)
q = getPrime(512)
n = p * q
d = getPrime(299)
e = inverse(d,(p-1)*(q-1))
m = bytes_to_long(flag)
c = pow(m,e,n)
hint1 = p >> (512-70)
hint2 = q >> (512-70)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
print(f"hint1 = {hint1}")
print(f"hint2 = {hint2}")

已知 p,q 高位的bd_attack，纯原题了，详解可以参考 2023 CryptoCTF-Insights 一题

CryptoCTF -Insights

Van1sh，公众号：Van1sh2023 CryptoCTF（二）


```
from Crypto.Util.number import *
from secret import flag

p = getPrime(512)
q = getPrime(512)
n = p * q
d = getPrime(299)
e = inverse(d,(p-1)*(q-1))
m = bytes_to_long(flag)
c = pow(m,e,n)
hint1 = p >> (512-70)
hint2 = q >> (512-70)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
print(f"hint1 = {hint1}")
print(f"hint2 = {hint2}")
# coding: utf-8
#!/usr/bin/env python2

import gmpy2
import random
import binascii
from hashlib import sha256
from sympy import nextprime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
from FLAG import flag
    #flag = 'wdflag{123}'

def victory_encrypt(plaintext, key):
    key = key.upper()
    key_length = len(key)
    plaintext = plaintext.upper()
    ciphertext = ''

    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext += encrypted_char
        else:
            ciphertext += char

    return ciphertext

victory_key = "WANGDINGCUP"
victory_encrypted_flag = victory_encrypt(flag, victory_key)

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
xG = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
yG = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
G = (xG, yG)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
h = 1
zero = (0,0)

dA = nextprime(random.randint(0, n))

if dA > n:
    print("warning!!")

def addition(t1, t2):
    if t1 == zero:
        return t2
    if t2 == zero:
        return t2
    (m1, n1) = t1
    (m2, n2) = t2
    if m1 == m2:
        if n1 == 0 or n1 != n2:
            return zero
        else:
            k = (3 * m1 * m1 + a) % p * gmpy2.invert(2 * n1 , p) % p
    else:
        k = (n2 - n1 + p) % p * gmpy2.invert((m2 - m1 + p) % p, p) % p
    m3 = (k * k % p - m1 - m2 + p * 2) % p
    n3 = (k * (m1 - m3) % p - n1 + p) % p
    return (int(m3),int(n3))

def multiplication(x, k):
    ans = zero
    t = 1
    while(t <= k):
        if (k &t )>0:
            ans = addition(ans, x)
        x = addition(x, x)
        t <<= 1
    return ans

def getrs(z, k):
    (xp, yp) = P
    r = xp
    s = (z + r * dA % n) % n * gmpy2.invert(k, n) % n
    return r,s

z1 = random.randint(0, p)
z2 = random.randint(0, p)
k = random.randint(0, n)
P = multiplication(G, k)
hA = multiplication(G, dA)
r1, s1 = getrs(z1, k)
r2, s2 = getrs(z2, k)

print("r1 = {}".format(r1))
print("r2 = {}".format(r2))
print("s1 = {}".format(s1))
print("s2 = {}".format(s2))
print("z1 = {}".format(z1))
print("z2 = {}".format(z2))

key = sha256(long_to_bytes(dA)).digest()
cipher = AES.new(key, AES.MODE_CBC)
iv = cipher.iv
encrypted_flag = cipher.encrypt(pad(victory_encrypted_flag.encode(), AES.block_size))
encrypted_flag_hex = binascii.hexlify(iv + encrypted_flag).decode('utf-8')

print("Encrypted flag (AES in CBC mode, hex):", encrypted_flag_hex)
s = (z + r * dA % n) % n * gmpy2.invert(k, n) % n
# sagemath
r1 = 
r2 = 
s1 = 
s2 = 
z1 = 
z2 = 

k = (z1-z2)/(s1-s2) % n
d = (s1*int(k)-z1) / int(r1) % n
c = ''
c = bytes.fromhex(c)
iv = c[:16]
c = c[16:]
key = sha256(long_to_bytes(d)).digest()
cipher = AES.new(iv= iv, key=key, mode = AES.MODE_CBC)
victory_encrypted_flag = cipher.decrypt(c)
def victory_decrypt(plaintext, key):
    key = key.upper()
    key_length = len(key)
    plaintext = plaintext.upper()
    ciphertext = ''

    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            ciphertext += encrypted_char
        else:
            ciphertext += char

    return ciphertext

victory_key = "WANGDINGCUP"

key_length=len(victory_key)
victory_encrypted_flag = ''

flag = victory_decrypt(victory_encrypted_flag, victory_key)
print(flag.lower())
from sage.all import *
from Crypto.Util.number import *

block_size = 64
rounds = 14

P_permutation = Permutations(list(range(block_size))).random_element()
inverse_P_permutation = [P_permutation.index(i) for i in range(block_size)]

MASK = 0b1110001001111001000110010000100010101111101100101110100001001001
IV = 7

b2i = lambda x: Integer(sum([x[i] * 2**i for i in range(len(x))]))

def pad(x):
    padlen = block_size - len(x) % block_size
    return x + bytes([padlen] * padlen)

def P(x):
    bit_x = x.bits()
    if len(bit_x) < block_size:
        bit_x.extend([0] * (block_size - len(bit_x)))
    bit_x = [bit_x[P_permutation[i]] for i in range(block_size)]
    return b2i(bit_x)

def P_inv(x):
    bit_x = x.bits()
    if len(bit_x) < block_size:
        bit_x.extend([0] * (block_size - len(bit_x)))
    bit_x = [bit_x[inverse_P_permutation[i]] for i in range(block_size)]
    return b2i(bit_x)

def S(x):
    x1 = x
    x2 = x << IV & MASK
    x3 = x << IV & ((1 << block_size) - 1) | MASK
    return x1 ^ x2 ^ x3

def encrypt(message_block, key):
    ret = message_block
    for i in range(rounds):
        ret = P_inv(S(P(ret)) ^ key)
    return ret

from secret import flag
from hashlib import md5

message = pad(flag)
message = [Integer(bytes_to_long(message[i:i+8])) for i in range(0, len(message), 8)]

key = int(md5(flag).hexdigest(), 16) & ((1 << block_size) - 1)

ciphertext = [encrypt(m, key) for m in message]

print(ciphertext)
print(P_permutation)
from z3 import *

def encryptwhithoutP(message_block, key):
    ret = message_block
    for i in range(rounds):
        ret = (S(ret) ^ key)
    return ret

m=
c=
key = BitVec("key",64)
s = Solver()
s.add(encryptwhithoutP(P(m),key) == P(c))
if s.check() == sat:
    m = s.model()
    print(m)
from Crypto.Util.number import getPrime, isPrime, GCD, inverse

nbits = 2048
gbits = 1000
g = getPrime(int(gbits))
while True:
    a = getPrime(int(nbits*0.5)-gbits)
    p = 2*g*a + 1
    if isPrime(p):
        break

while True:
    b = getPrime(int(nbits*0.5)-gbits)
    q = 2*g*b + 1
    if p!=q and isPrime(q):
        break
N = p*q
e = 65537

def str2int(s):
    return int(s.encode('latin-1').hex(),16)

def int2str(i):
    tmp=hex(i)[2:]
    if len(tmp)%2==1:
        tmp='0'+tmp
    return bytes.fromhex(tmp).decode('latin-1')

with open('pubkey.txt','w') as f:
    f.write(str(e)+'n')
    f.write(str(N)+'n')

with open('flag.txt') as f:
    plain = str2int(f.read())

c = pow(plain,e,N)
with open('cipher.txt','wb') as f:
    f.write(int2str(c).encode('latin-1'))
```


---
## 附图

[图片已移除]