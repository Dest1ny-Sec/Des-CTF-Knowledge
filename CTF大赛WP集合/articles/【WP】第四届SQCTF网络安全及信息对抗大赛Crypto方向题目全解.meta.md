---
title: 【WP】第四届 SQCTF 网络安全及信息对抗大赛 Crypto 方向题目全解
contest: SQCTF
year: 2025
difficulty: mixed
vuln_type: crypto_rsa
tags: [Fermat-attack, RSA-close-prime, CRT, ECC-discrete-log, dp-dp1-leak, gcd-iroot, side-channel-template-attack, RSA-common-modulus, rotor-machine]
attack_chain: 1. RSA Fermat 攻击 (p-q 接近) /2. RSA CRT 多个 (n, c) 组合 /3. e 小 + iroot 求明文 /4. ECC 离散对数 + c1*k - c2 还原 /5. dp + e 爆破求 p q /6. 侧信道模板攻击 euclidean 距离 /7. RSA 公模攻击 gcdext(e1, e2) 求逆 /8. 14 转子密码机爆破
key_payload: Fermat attack + CRT + ECC + dp leak + side channel + common modulus + 转子密码机
one_liner: 第四届 SQCTF Crypto 方向 8 大题全解，覆盖 RSA/ECC/侧信道/经典密码学全栈。
lesson: Fermat 攻击适用 p q 接近；CRT 适用多组 (n, c)；ECC 加法公式；dp 泄漏 + e 爆破；侧信道模板用欧氏距离分类；RSA 公模攻击用扩展欧几里得；14 转子密码机 + 密文定位爆破。
quality: high
---

# 【WP】第四届 SQCTF 网络安全及信息对抗大赛 Crypto 方向题目全解

## 概览
第四届 SQCTF 网络安全及信息对抗大赛 Crypto 方向 8 大题全解，覆盖 RSA/ECC/侧信道/经典密码学。

## 题 1: RSA Fermat 攻击
```python
import math
import gmpy2
from Crypto.Util.number import long_to_bytes

def fermat_attack(n):
    a = math.isqrt(n)
    b2 = a*a - n
    b = math.isqrt(n)
    count = 0
    while b*b != b2:
        a = a + 1
        b2 = a*a - n
        b = math.isqrt(b2)
        count += 1
    p = a + b
    q = a - b
    assert n == p*q
    return p, q

n = 7349515423675898192...
e = 65537
c = 3514741378432598036...
p, q = fermat_attack(n)
phi_n = (p-1) * (q-1)
d = gmpy2.invert(e, phi_n)
m = pow(c, d, n)
print(long_to_bytes(m))
```

## 题 2: RSA CRT（中国剩余定理）
```python
import gmpy2
from functools import reduce
from Crypto.Util.number import bytes_to_long, long_to_bytes

def CRT(c, n):
    sum = 0
    N = reduce(lambda x, y: x*y, n)
    for n_i, c_i in zip(n, c):
        N_i = N // n_i
        t_i = gmpy2.invert(N_i, n_i)
        sum += c_i * N_i * t_i
    return sum % N
```

## 题 3: e 小 + iroot 求明文
```python
for e in range(1, 10):
    m, r = gmpy2.iroot(x, e)
    if r == True:
        print(long_to_bytes(m))
```

## 题 4: ECC 离散对数
```python
a = 1234577
b = 3213242
n = 7654319
E = EllipticCurve(GF(n), [0, 0, 0, a, b])
base = E([5234568, 2287747])
pub = E([2366653, 1424308])
c1 = E([5081741, 6744615])
c2 = E([610619, 6218])
X = base
for i in range(1, n):
    if X == pub:
        secret = i
        break
    else:
        X = X + base
m = c2 - (c1 * secret)
```

## 题 5: dp 泄漏 + e 爆破
```python
for x in range(1, e):
    if (e * dp) % x == 1:
        p = (e * dp - 1) // x + 1
        if n % p != 0:
            continue
        q = n // p
        phi = (p-1) * (q-1)
        d = gmpy2.invert(e, phi)
        m = pow(c, d, n)
        print(long_to_bytes(m))
```

## 题 6: 侧信道模板攻击
```python
import numpy as np
from scipy.spatial.distance import euclidean

traces = np.load('energy_traces_with_flag.npy')
template_trace_0 = np.load('template_trace_0.npy')
template_trace_1 = np.load('template_trace_1.npy')

def recover_private_key(traces, template_trace_0, template_trace_1):
    private_key = []
    for trace in traces:
        dist_0 = euclidean(trace, template_trace_0)
        dist_1 = euclidean(trace, template_trace_1)
        private_key.append(0 if dist_0 < dist_1 else 1)
    return private_key

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    text = ''.join([chr(int(char, 2)) for char in chars])
    return text
```

## 题 7: RSA 公模攻击
```python
import gmpy2
from Crypto.Util.number import long_to_bytes
n = 1365050356023361235...
c1 = 3366500968116867439...
c2 = 7412517103990148893...
e1 = 4217054819
e2 = 2800068527

_, s1, s2 = gmpy2.gcdext(e1, e2)
m = pow(c1, s1, n) * pow(c2, s2, n) % n
print(long_to_bytes(m))
```

## 题 8: 14 转子密码机
```python
txt = '''1: <QWXZRJYVKSLPDTMACFNOGIEBHU <
2: <BXZPMTQOIRVHKLSAFUDGJYCEWN <
3: <LKJHGFDSAQZWXECRVBYTNUIMOP <
...
14: < KOLPQAZWSXEDCRFVTGBYHNUJM <'''

x = []
for line in txt.strip().split('\n'):
    x.append(line[4:31].strip().replace('<', ''))

key = '4,2,11,8,9,12,3,6,10,14,1,5,7,13'
key = [int(i) for i in key.split(',')]

mi = 'UNEHJPBIUOMAVZ'
flag = []
for m, n in zip(key, mi):
    flag.append(x[m-1][x[m-1].index(n):] + x[m-1][:x[m-1].index(n)])

for i in range(26):
    for j in flag:
        print(j[i], end='')
    print()
```

## 经验提炼
- Fermat 攻击适用 p q 接近（差值小）
- CRT 适用多组 (n, c) 模互素合并
- ECC 加法公式：同点 p = (3x² + a) / 2y，异点 p = (y2-y1) / (x2-x1)
- dp 泄漏 + e 爆破：1 < x < e, (e*dp) % x == 1
- 侧信道模板攻击：欧氏距离分类比特位
- RSA 公模攻击：gcd(e1, e2) = 1，用 gcdext 求 s1, s2
- 14 转子密码机 + 密文定位爆破
- SciPy euclidean 距离用于模板匹配
- gmpy2.iroot 求整数 n 次方根
- Fermat 攻击复杂度 O(p-q)，差值越大越慢
