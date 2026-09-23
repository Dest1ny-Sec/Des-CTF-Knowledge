---
title: 2024 网鼎杯 朱雀 & 玄武
contest: 网鼎杯
year: 2024
difficulty: hard
vuln_type:
- lattice
- crypto_rsa
- secret_sharing
tags:
- 已知 p 高位 256/512 Coppersmith
- 多层 RSA 套娃
- p1q1=2024*p1
- n22=p^2+q^2 解方程
- Shamir 秘密共享 kernel 攻击
attack_chain: '朱雀 crypto002: 已知 p 高 256bit → Coppersmith X=2^248 beta=0.49 epsilon=0.014 → 爆破 7 比特 p / crypto003: 3 层 RSA 套娃 - Layer1: n1=p1*q1 q1=next_prime(2024*p1) → n1//2024 开根还原 p1 / Layer2: n2=p2*q2, n22=p2^2+q2^2 → 解二元二次方程 (p2+q2)^2 = n22+2n2, (p2-q2)^2 = n22-2n2 / Layer3: p3/q3 共享 1024 高位 → 已知 p3 高位攻击 / 两式 m1=p1*m^2+p2*m+p3, m2=q1*m^2+q2*m+q3 → 解联立方程 / 玄武 Shamir: 10000 份 shares 每份 64 个 polynomial coefs + value, n_players=64, threshold=128 > 实际自由度 32 → 拆 32 维 kernel (C2 = matrix of high coefs) → 累积 C1*kernel 拼出完整矩阵 → 求解'
key_payload: f = (p>>248)<<248 + x ; f.small_roots(X=2^248, beta=0.49, epsilon=0.014) ; n1 // 2024 开根 = p1 ; m^2 = p1*m1 - p2*m + p3 / p1 ; ShamirSS(coefs, value) 64 个 coefs, 10000 组
one_liner: Coppersmith 已知 p 高位 + 多层 RSA 套娃 + Shamir kernel 攻击。
lesson: Shamir 秘密共享若 threshold > 自由度，攻击者可取 C2 矩阵求 kernel 还原 C1 拼出完整方程组。
quality: high
full_path: 2024_网鼎杯_朱雀&玄武.full.md
meta_path: 2024_网鼎杯_朱雀&玄武.meta.md
images_removed: true
images_removed_count: 3
schema_version: v3.0.0-P0
summary: 2024 网鼎杯 朱雀 & 玄武。Coppersmith 已知 p 高位 + 多层 RSA 套娃 + Shamir kernel 攻击。。经验：Shamir 秘密共享若 threshold > 自由度，攻击者可取 C2 矩阵求 kernel 还原 C1 拼出完整方...
category: crypto
subcategory: lattice
subcategories:
- lattice
- rsa
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 3
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/217506.html
reasoning_chain:
- 触发点：crypto002 给1024bit RSA 模数 n + 已知 p 高 256bit → 假设：标准 Coppersmith 已知高位攻击
- 动作：在 Sage 用 f = (p>>248)<<248 + x + small_roots(X=2^248, beta=0.49, epsilon=0.014)
- 观察：sage 一跑要 9 秒，248bit 解不出 → 假设：必须爆破最高 8bit 补齐未知位
- 动作：循环爆破前缀 8bit + small_roots →观察：每组 9s × 256 = 38 分钟出 p
- 触发点：crypto003 三层 RSA 套娃 Layer1 n1=p1*q1 q1=next_prime(2024*p1) → 假设：n1/2024≈p1*q1/2024≈p1²开根
- 动作：iroot(n1/2024) ≈ p1 → 观察：误差 ≤ next_prime 距离 → 直接 next_prime 得 p1
- 假设：Layer2 n2=p2*q2, n22=p2²+q2² → 动作：(p2+q2)²=n22+2n2, (p2-q2)²=n22-2n2 → 解出 p2+q2 和 p2-q2
- 触发点：Layer3 给 m1=p1*m²+p2*m+p3 m2=q1*m²+q2*m+q3 共享 p3/q3 高位 → 假设：可联立求 m
- 动作：m² = (p1*m1-p2*m+p3)/p1 代入 m2 → 解二次方程 → 观察：出 m
- 触发点：玄武 Shamir 10000 份 shares 64 个 coefs 阈值 128 > 自由度 32 → 假设：C2 矩阵可求 kernel
- 动作：构造 C2 = matrix of high coefs, 求 kernel, 累积 C1*kernel 拼出完整方程组 → 观察：解出全部64 个低 coefs
- 下一步：把 shares value 与 poly 求值比较，差分还原 flag
failed_attempts:
- 试图直接 small_roots(X=2^248, beta=0.49) 出 p → 失败：248bit 边界 Coppersmith epsilon 不够
- 试图对 n1 直接 factor → 失败：n1 是真 RSA 模数无结构弱点
- 试图直接解联立二元二次方程组 n22=p²+q² n=pq → 失败：消元后开方有符号歧义
key_observations:
- 已知 p 高位 256/512 是2024 网鼎杯 crypto002 经典套路：必须爆破补齐未知高位
- Coppersmith 的 epsilon 是关键参数：epsilon越大越快但要求小根，0.014跑 9s 出
- next_prime(2024*p1) 这种弱关联结构可直接 next_prime(iroot(n/2024)) 还原
- p²+q² 与 p*q 联立可在 O(1) 内解 p 和 q（对称性消元）
- Shamir 阈值 > 自由度 = 攻击者可取高 coefs 矩阵求 kernel 还原低 coefs
prerequisites:
- SageMath small_roots 用法（Coppersmith 已知高位攻击）
- RSA 多项式/二次方程解法
- 线性代数 GF(p) 矩阵 kernel 求法
- Shamir 秘密共享原理
---
# 2024 网鼎杯 朱雀&玄武

> 原文: https://www.ctfiot.com/217506.html
> ID: 217506

朱雀

crypto002

各位朱雀组参赛选手请注意，平台新增“CRYPTO02”赛题提示：
提示信息如下：请根据提示信息进一步完成解题。

（1）RSA模数 n：

0x00b8cb1cca99b6ac41876c18845732a5cbfc875df346ee9002ce608508b5fcf6b60a5ac7722a2d64ef74e1443a338e70a73e63a303f3ac9adf198595699f6e9f30c009d219c7d98c4ec84203610834029c79567efc08f66b4bc3f564bfb571546a06b7e48fb35bb9ccea9a2cd44349f829242078dfa64d525927bfd55d099c024f

（2）素数 p 的高位：

0xe700568ff506bd5892af92592125e06cbe9bd45dfeafe931a333c13463023d4f0000000000000000000000000000000000000000000000000000000000000000

（3）加密指数 e：

0x10001

（4）加密消息文件：flag.enc，你需要读取并解密此文件。

你的任务是通过给定的信息恢复素数 p，计算私钥 d，并解密加密消息以获得 flag。

这题就没啥弯弯绕绕的了，就是一个已知 p 高位攻击，已知的比特是 256 位的，只有一半，直接 copper 是 copper 不出的，需要爆破一下。

爆破之前，可以先在本地测一下，什么样的参数，多少位能出，这样能够节省一些时间。

from Crypto.Util.number import *
import time
p = getPrime(512)
q = getPrime(512)
n = p * q

s = time.time()
R.<x> = Zmod(n)[]

f = (p>>248)<<248
f += x
f.small_roots(X=2^248,beta = 0.49,epsilon = 0.014)
print(time.time()-s)

我这里测的用 epsilon = 0.014 能出 248 比特，用 win 下的 sagemath 虚拟机一个要跑 9 秒左右，总共爆破 8 比特，需要大概 38 分钟。可以考虑一下多进程。

crypto003

#!/usr/bin/env python3

import random
from sympy import nextprime
from gmpy2 import is_prime
from Crypto.Util.number import getPrime, bytes_to_long
from Secret import flag

m = bytes_to_long(flag)

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 2999

f = open("out.txt", 'w')

p1 = getPrime(1024)
q1 = nextprime(2024 * p1)
n1 = p1 * q1
f.write("n1 = {0}n".format(n1))

p2 = getPrime(1024)
q2 = 1
while q2 < p2:
    q2 = getPrime(1024)
n2 = p2 * q2
n22 = p2 * p2 + q2 * q2
f.write("n2 = {0}n".format(n2))
f.write("n22 = {0}n".format(n22))

r = random.getrandbits(1024)
p3 = r
while not is_prime(p3):
    p3 += random.getrandbits(400)
q3 = r
while q3 < p3:
    q3 += random.getrandbits(500)
while not is_prime(p3):
    q3 += random.getrandbits(500)
n3 = p3 * q3
f.write("n3 = {0}n".format(n3))

m1 = p1 * m * m + p2 * m + p3
m2 = q1 * m * m + q2 * m + q3
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)

f.write("n = {0}n".format(n))
f.write("c1 = {0}n".format(c1))
f.write("c2 = {0}n".format(c2))

一共套了三层，

p1 = getPrime(1024)
q1 = nextprime(2024 * p1)
n1 = p1 * q1

第一层直接给 n1//2024 开根就好了。

p2 = getPrime(1024)
q2 = 1
while q2 < p2:
    q2 = getPrime(1024)
n2 = p2 * q2
n22 = p2 * p2 + q2 * q2
f.write("n2 = {0}n".format(n2))
f.write("n22 = {0}n".format(n22))

第二层就是解一个二元二次方程，也没啥。

r = random.getrandbits(1024)
p3 = r
while not is_prime(p3):
    p3 += random.getrandbits(400)
q3 = r
while q3 < p3:
    q3 += random.getrandbits(500)
while not is_prime(p3):
    q3 += random.getrandbits(500)
n3 = p3 * q3
f.write("n3 = {0}n".format(n3))

第三层有 bug，两行都是 while not is_prime(p3):，这就导致 q3 根本不是素数（除非一发入魂了，那是真的没话讲），不过似乎也不太影响解题。

本地生成了一组数据测一下，大概高 528 比特是一样的。直接对 n 开根得到 p 的高位，然后直接已知 p 高位攻击（故技重施）。

于是根据大小关系，我们能获得 p1,p2,p3,q1,q2,q3

我们还有两条式子

github上有一个 crypto-attacks 项目，里面有一个 fast_polynomial_gcd

Van1sh，公众号：Van1sh2023 SEECTF（see you again~）


```
各位朱雀组参赛选手请注意，平台新增“CRYPTO02”赛题提示：
提示信息如下：请根据提示信息进一步完成解题。

（1）RSA模数 n：

0x00b8cb1cca99b6ac41876c18845732a5cbfc875df346ee9002ce608508b5fcf6b60a5ac7722a2d64ef74e1443a338e70a73e63a303f3ac9adf198595699f6e9f30c009d219c7d98c4ec84203610834029c79567efc08f66b4bc3f564bfb571546a06b7e48fb35bb9ccea9a2cd44349f829242078dfa64d525927bfd55d099c024f

（2）素数 p 的高位：

0xe700568ff506bd5892af92592125e06cbe9bd45dfeafe931a333c13463023d4f0000000000000000000000000000000000000000000000000000000000000000

（3）加密指数 e：

0x10001

（4）加密消息文件：flag.enc，你需要读取并解密此文件。

你的任务是通过给定的信息恢复素数 p，计算私钥 d，并解密加密消息以获得 flag。
from Crypto.Util.number import *
import time
p = getPrime(512)
q = getPrime(512)
n = p * q

s = time.time()
R.<x> = Zmod(n)[]

f = (p>>248)<<248
f += x
f.small_roots(X=2^248,beta = 0.49,epsilon = 0.014)
print(time.time()-s)
#!/usr/bin/env python3

import random
from sympy import nextprime
from gmpy2 import is_prime
from Crypto.Util.number import getPrime, bytes_to_long
from Secret import flag

m = bytes_to_long(flag)

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 2999

f = open("out.txt", 'w')

p1 = getPrime(1024)
q1 = nextprime(2024 * p1)
n1 = p1 * q1
f.write("n1 = {0}n".format(n1))

p2 = getPrime(1024)
q2 = 1
while q2 < p2:
    q2 = getPrime(1024)
n2 = p2 * q2
n22 = p2 * p2 + q2 * q2
f.write("n2 = {0}n".format(n2))
f.write("n22 = {0}n".format(n22))

r = random.getrandbits(1024)
p3 = r
while not is_prime(p3):
    p3 += random.getrandbits(400)
q3 = r
while q3 < p3:
    q3 += random.getrandbits(500)
while not is_prime(p3):
    q3 += random.getrandbits(500)
n3 = p3 * q3
f.write("n3 = {0}n".format(n3))

m1 = p1 * m * m + p2 * m + p3
m2 = q1 * m * m + q2 * m + q3
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)

f.write("n = {0}n".format(n))
f.write("c1 = {0}n".format(c1))
f.write("c2 = {0}n".format(c2))
p1 = getPrime(1024)
q1 = nextprime(2024 * p1)
n1 = p1 * q1
p2 = getPrime(1024)
q2 = 1
while q2 < p2:
    q2 = getPrime(1024)
n2 = p2 * q2
n22 = p2 * p2 + q2 * q2
f.write("n2 = {0}n".format(n2))
f.write("n22 = {0}n".format(n22))
r = random.getrandbits(1024)
p3 = r
while not is_prime(p3):
    p3 += random.getrandbits(400)
q3 = r
while q3 < p3:
    q3 += random.getrandbits(500)
while not is_prime(p3):
    q3 += random.getrandbits(500)
n3 = p3 * q3
f.write("n3 = {0}n".format(n3))
# SageMath version 10.0, Release Date: 2023-05-20

from sage.all import *
from Crypto.Util.number import *

from secret import flag
flag = flag.lstrip(b"wdflag{").rstrip(b"}")

class ShamirSS:
    def __init__(self, coefs, value):
        self.coefs = coefs
        self.value = value

class ShamirProtocol:
    def __init__(self, n_players, threshold, modulus):
        self.n_players = n_players
        self.threshold = threshold
        
        assert isPrime(modulus), "Modulus must be a prime number"
        self.modulus = modulus
        
        
    def input_share(self, values):
        coefs = [
            [getRandomRange(1, self.modulus) for _ in range(self.threshold)]
            for _ in range(self.n_players)
        ]

        randoms = values + [getRandomRange(1, self.modulus) for _ in range(self.threshold - len(values))]

        values = [
            sum([r * c for r, c in zip(randoms, coef)]) % self.modulus
            for coef in coefs
        ]
        shares = [ShamirSS(coef, value) for coef, value in zip(coefs, values)]
        return shares
    
protocol = ShamirProtocol(len(flag), len(flag) * 2, 257)
values = list(flag)

import os
os.mkdir("shares")

for i in range(10000):
    shares = protocol.input_share(values)
    save(shares, f"shares/share_{i}.sobj")
class ShamirSS:
    def __init__(self, coefs, value):
        self.coefs = coefs
        self.value = value
from tqdm import *
p=257
NEWV = []
FLAG = True
index=0
for i in trange(10000):
    s = load('share_%d.sobj'%i)
    C1 = matrix(GF(p),[ss.coefs[:32] for ss in s])
    C2 = matrix(GF(p),[ss.coefs[32:] for ss in s])
    V = vector(GF(p),[ss.value for ss in s])
    if C2.rank()<32:
        Ck = C2.left_kernel().basis()
        CK = Matrix(GF(p),Ck)
        newC1 = CK * C1 
        newV = CK * V
        if FLAG:
            NEWC1 = newC1
            NEWV.append(newV)
            FLAG = False
            continue
        NEWC1 = NEWC1.stack(newC1)
        NEWV.append(newV)
        index += 1
NEWV = [i[0] for i in NEWV]
NEWV = vector(GF(p),NEWV)
FLAG =  (NEWC1.solve_right(NEWV))
print(''.join(chr(i) for i in FLAG))

# sage: print(''.join(chr(i) for i in FLAG))
# 197de281fd12e95eba04e7b84539fc8c
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]