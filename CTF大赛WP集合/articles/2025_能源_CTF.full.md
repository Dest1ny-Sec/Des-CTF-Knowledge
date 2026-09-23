---
title: 2025 能源 CTF（RSA hint 线性同余 + HNP 隐数问题格攻击）
contest: 2025 能源 CTF
year: 2025
difficulty: hard
vuln_type:
- crypto_rsa
- lattice
tags:
- 能源 CTF 2025
- RSA hint + 233*k == 233*k*p 线性同余
- p | hint 隐变量
- HNP 隐数问题格
- c=a*m+b mod p 30 组
- m < p
- enc = pow(m
- flag
- p)
- p 512-bit
- a 512-bit
- b 400-bit
- target_vector_length=400
- K=2^400
- Sage LLL
attack_chain:
- 'Q1: hint + 233*k == 233*k*p → p | hint → p = gcd(hint, p) → 试 233*k 直到整除 hint'
- 'Q2: HNP 30 组 (a_i, c_i) + 隐变量 m, b_i 400 bit'
- '构造 Lattice H:'
- length=30, target_vector_length=400, K=2^400
- LLL 还原 m
- enc = pow(m, flag, p) → flag = discrete_log(enc, m, p) 或 pow(enc, inverse(flag_int, p-1), p) == m
key_payload: Lattice HNP + LLL 还原 m
one_liner: 2025 能源 CTF：Q1 RSA hint p 线性同余 + Q2 HNP 隐数问题格攻击（30 组 512-bit a + 400-bit b + 隐 m）。
lesson: hint + 233*k == 233*k*p 是 RSA 隐 p 套路 → p = gcd(hint, ...) 试 233*k；HNP 30 组 (a, c) 隐变量 m + 小 b (400-bit) → Sage 构造 5-row lattice + LLL 还原 m。
quality: high
full_path: 2025_能源_CTF.full.md
meta_path: 2025_能源_CTF.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: '2025 能源 CTF（RSA hint 线性同余 + HNP 隐数问题格攻击）。2025 能源 CTF：Q1 RSA hint p 线性同余 + Q2 HNP 隐数问题格攻击（30 组 512-bit a + 400-bit b + 隐 m）。。关键路径：Q1: hint + 233*k == 233*k*p → p | hint → p = gcd(hint, p) → 试 233*k ...'
category: crypto
subcategory: rsa
subcategories:
- rsa
- lattice
tools_used:
- Sage
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/243032.html
reasoning_chain:
- 触发点：hint + 233*k == 233*k*p 同余式 → 假设：p 整除 hint（p | hint）→ 动作：把等式改写 233*k*(p-1) = hint
- 观察：k 未知 → 假设：爆破 233*k 当作因子 → 动作：gcd(hint, 233*k) 整除时，p = hint/(233*k) + 1 → 验证 512-bit 质数
- 下一步：拿到 p,q → d=inverse(65537,(p-1)(q-1)) → m=pow(c,d,n) 解 Q1
- 触发点：Q2 给 30 组 (a_i, c_i) + b_i 只 400-bit + 隐 m 512-bit → 假设：经典 HNP 隐数问题 → 动作：构造 32-row lattice（30 行 p 对角 + 末行 c + 倒数行 K/p）
- 观察：target_vector_length=400, K=2^400 → 假设：b 维度补齐则 LLL 能找到短向量 → 动作：M.LLL() 选 LLL[i] 末位 K 行还原 m0=(cc[0]-L[i][0])/aa[0] % p
- 触发点：enc = pow(m, flag_int, p) → 假设：flag 是离散对数指数 → 动作：big_div = 7938574420107972329924249635772221961795521132311900945710547973
- 观察：psub.bit_length() 较小 → 假设：big_div | (p-1) → 动作：enc_sub = pow(enc, big_div, p); m_sub = pow(m, big_div, p)
- 下一步：Sage discrete_log(Mod(enc_sub,p), Mod(m_sub,p), ord=psub) + 循环 psub 加到 ASCII 含 flag 子串输出
failed_attempts:
- 试图直接 sqrt(GCD(hint, k)) → 失败：hint 内的 233*k 因子未直接暴露
- 试图对 m 用 Pohlig-Hellman 解离散对数 → 失败：p-1 没有光滑因子，big_div 是攻击给出的子群大小
- 试图用现成 lattice 库 baby-step giant-step → 失败：HNP 不是普通 DLP，需要 LLL 还原短向量
key_observations:
- RSA hint 线性同余 + 233 倍数 → p 整除 hint 是常见隐 p 套路
- HNP（Hidden Number Problem）30 组 (a,c) + 隐 m + 小 b 是 lattice LLL 经典攻击面
- target_vector_length 与 K=2^N 是 LLL 还原隐变量的归一化参数
- enc = pow(m, flag, p) 时离散对数要先分解 p-1 找光滑子群
- Sage 的 discrete_log 函数在 ord 已知情况下是 Pohlig-Hellman 自动化
prerequisites:
- Sage 数学工具使用（matrix / LLL / discrete_log）
- RSA 模数分解（费马小定理 / p 整除 hint 套路）
- Hidden Number Problem lattice 还原原理
- 离散对数 + Pohlig-Hellman 算法
---
# 2025 能源 CTF

> 原文: https://www.ctfiot.com/243032.html
> ID: 243032


```
from Crypto.Util.number import *
import hint

flag=b'xxx'
e=65537
p=getPrime(512)
q=getPrime(512)
n=p*q
m=bytes_to_long(flag)
c=pow(m,e,n)
k=getPrime(1024)
assert hint + 233 * k == 233 * k * p
print(n)
print(c)
print(hint)

# n = 
# c =
# hint =
from Crypto.Util.number import *
from secrets import flag

assert len(flag) == 38

p = getPrime(512)
m = getPrime(512)
while m > p:
    m = getPrime(512)

aa = []
cc = []
bb = []
for i in range(30):
    a = getPrime(512)
    b = getPrime(400)
    c = (a * m + b) % p
    aa.append(a)
    cc.append(c)
    bb.append(b)

enc = pow(m,flag,p)
print(f'p = {p}')
print(f'aa = {aa}')
print(f'cc = {cc}')
print(f'enc = {enc}')

# p = 0x83b05d231fd40ff8ca26b4fb8136dc920754c14412960ce2ec700457861d48fe74f3958fc3a153f77a23fb850ecf0ac1e9722c71b6cc8a104b372cc17bf1528f
# aa = []
# cc = []
# enc =
p = 
aa = []
cc = []

# Lattice of HNP 

# [p 0 ....       ]
# [0 p ....       ]
# [    ....       ]
# [a a .... K/p   ]
# [c c ....     K ]

length = len(aa)
target_verctor_length = 400
K = 2**target_verctor_length

a = []
for i in range(length):
    b = []
    for j in range(length):
        if i == j:
            b.append(p)
        else:
            b.append(0)
    b.append(0)
    b.append(0)
    a.append(b)

b = []
for i in range(length):
    b.append(aa[i])
b.append(K/p)
b.append(0)
a.append(b)

b = []
for i in range(length):
    b.append(cc[i])
b.append(0)
b.append(K)
a.append(b)

M = Matrix(QQ,a)
L = M.LLL()

for i in range(L.ncols()):
    if L[i][-1] == 2** target_verctor_length:
        m0 = (cc[0] - abs(L[i][0]))/aa[0] % p
        m1 = (cc[1] - abs(L[i][1]))/aa[1] % p
        assert m0 == m1
        print(f"m = {m}")
        break
big_div = 7938574420107972329924249635772221961795521132311900945710547973
psub = (p-1)// big_div
print(psub.bit_length())
m = m0
big_div = 7938574420107972329924249635772221961795521132311900945710547973
psub = (p-1)// big_div
print(psub.bit_length())

enc_sub = pow(enc,big_div,p)
m_sub = pow(m,big_div,p)

flag_sub = discrete_log(Mod(enc_sub,p),Mod(m_sub,p),ord = psub)
for i in range(2**5):
    flag_sub += psub
    ifb'flag'in long_to_bytes(flag_sub):
        print(long_to_bytes(flag_sub))

# flag{70b1b709ce431682addb581596320007}
from Crypto.Util.number import *
from gmpy2 import *
import os

flag = b'xxx'
p = next_prime(bytes_to_long(os.urandom(128)))
q = next_prime(bytes_to_long(os.urandom(128)))
r = next_prime(q)
n = p * q * r
e = 0x10001
print(f"n = {n}")
print(f"c = {pow(bytes_to_long(flag), e, n)}")
print(f"gift1 = {p % (2**10)}")
print(f"gift2 = {(p >> 20) % 2 ** 800}")

# n = 
# c = 
# gift1 = 
# gift2 =
R.<x> = Zmod(n)[]

for i in range(2^10):
 f = x * 2^820 + gift2 * 2^20 + i * 2^10 + gift1
 ans = f.monic().small_roots(X=2^(1024-820),beta=0.33)
 if len(ans) != 0:
  p = int(f(ans[0]))
        print("[+]",p)
  break
print(long_to_bytes(pow(c,inverse(0x10001,p-1),p)))
from secret import flag
from Crypto.Util.number import getPrime

flag = bin(int.from_bytes(flag, 'big'))[2:]

private_key = []
g = getPrime(10)
private_key.append(g)
for i in range(len(flag) - 1):
    g = g * 2
    private_key.append(g)

a = getPrime(20)
b = getPrime(len(flag) + 20)
public_key = []
for i in private_key:
    public_key.append((a * i) % b)
print(public_key)

c = 0
for i in range(len(flag)):
    c += int(str(flag)[i])*public_key[i]
print(c)
a = 797627
g = 967
b = public_key[-2] * 2 - public_key[-1]
c = c * inverse(a,b) % b

private_key = []
private_key.append(g)
for i in range(len(public_key) - 1):
    g = g * 2
    private_key.append(g)

flag = ""
for each in private_key[::-1]:
    if c >= each:
        flag = '1' + flag
        c -= each
    else:
        flag = '0' + flag
assert c == 0
print(long_to_bytes(int(flag,2)))
```


---
## 附图

[图片已移除]
[图片已移除]