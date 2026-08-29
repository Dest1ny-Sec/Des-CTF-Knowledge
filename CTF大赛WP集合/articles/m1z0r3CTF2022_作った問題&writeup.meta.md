---
title: m1z0r3CTF 2022 作った問題 & writeup
contest: m1z0r3CTF
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags: [lcg, rsa-chain, multi-prime, prime-256bit, custom-encrypt, secret-png, 16bit-prime]
attack_chain:
  - chall1: 未知 a, b, r, x (LCG)
  - 加密 = byte XOR LCG 输出
  - 已知明文头部 (PNG 头 8 字节) 推导 LCG
  - chall2: prime + 链式素数 + 16bit prime
  - 链式 q 拼接 next_prime
  - 小明文 + 已知 gen_p 爆破
  - chall3: getPrime(256) + 16bit 偏移 e
  - 16bit 偏移 ex + 2 字节 e 爆破
key_payload: LCG 已知明文恢复 + 链式 RSA + 16bit prime
one_liner: m1z0r3CTF 2022 三道密码学题：LCG 加密 + 链式 RSA + 16bit prime 拼接。
lesson: LCG 加密 + 已知明文攻击是经典题型；链式 prime RSA 的"prime 链"是近年新趋势。
quality: high
---

m1z0r3CTF 2022 日本出题人 wp，3 道 crypto 题（来源 ctfiot）。

**chall1: LCG 加密**

```python
from Crypto.Util.number import long_to_bytes
import random

secret = open("secret.png","rb").read()
a = random.randrange(256)  # 未知
b = random.randrange(256)
r = random.randrange(256)
x = random.randrange(256)

enc = 0
for s in secret:
    enc <<= 8
    x = (a*x + b) % r  # LCG
    enc += s ^ x
```

**破解**：
- PNG 文件头是固定 8 字节 `89 50 4E 47 0D 0A 1A 0A`
- 用 LCG 输出 `x1, x2, x3, ...` 与明文异或得到 `enc`
- 已知前 8 字节明文 → 列出 8 个方程组（4 未知数 + 8 方程）
- 暴力 256^4 空间搜索 a, b, r, x
- 找到后解密整张图

**chall2: 链式 RSA**

```python
def encrypt(st_len, go_len, prime, message):
    s = 0; l = 1; c = []
    while st_len <= go_len:
        while True:
            q = getPrime(st_len)
            qbin = bin(q)[2:]
            while len(qbin) < st_len: qbin = "0" + qbin
            next_prime = int(bin(prime)[2:] + qbin, 2)
            if isPrime(next_prime):
                N = prime * q
                m = bytes_to_long(message[s:s+l])
                e = 101
                if prime % e != 1 and q % e != 1:
                    c.append(pow(m, e, N))
                prime = next_prime
                break
        st_len *= 2; s += l; l *= 2
    return c, N
```

prime 链：每一轮 `next_prime = (prime 的二进制 + q 的二进制)`，用 next_prime * q 加密。`st_len` 翻倍 → prime 链越来越长。

**关键**：最后 N 已知（prime 链 + q 链拼接），gen_p 已知，c 已知。e=101 小 → 直接对小密文 CRT 求 d。

**chall3: 16bit prime + secret 偏移**

```python
ex = random.randrange(len(secret)-1)
e = bytes_to_long(secret[ex:ex+2])  # 16bit e
p = getPrime(256); q = getPrime(256)
n = p * q
# flag 每 3 字节一段加密
c.append(pow(m, e, n))
```

**攻击**：
- 16bit e 爆破（2^16 = 65536 种可能）
- 已知密文 + flag 前 3 字节（"m1z"）→ 验证 e 正确性
- `e=ord('m')*256+ord('1')` 等组合爆破

整篇适合作为"自定义 LCG + 链式 RSA + 16bit prime"教学。
