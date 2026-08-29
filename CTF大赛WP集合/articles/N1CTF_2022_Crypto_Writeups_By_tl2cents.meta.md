---
title: N1CTF 2022 Crypto Writeups By tl2cents (RSA 变种)
contest: N1CTF
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [RSA 变种, enc(m, k) = (m*r^s, m*r^t) 字节级爆破, xgcd 求逆]
attack_chain: |
  1. 题目: N1CTF 2022 Crypto — RSA 变种
  2. keygen: p, q (512-bit) → n=pq, phi=(p-1)(q-1)
     - a = getrandbits(1024), b = phi + 1 - a
     - s = getrandbits(1024), t = -s*a * inverse(b, phi) % phi
     - pubkey = (s, t, n), privkey = (a, b, n)
  3. 加密 enc(m, k):
     - r = getrandbits(1024)
     - return (m * pow(r, s, n) % n, m * pow(r, t, n) % n)
  4. flag = pow(bytes_to_long(flag), 0x10001, pubkey[2])
  5. 每个 byte m 加密: c1, c2 = enc(m, pubkey)
  6. 攻击: 字节级爆破 m (0-255)
     - xgcd(s, t) 求 (g, x, y) 让 s*x + t*y = g
     - z = pow(c1, x, n); w = pow(c2, y, n)
     - mm = pow(m, -(x+y), n)
     - r_ = mm * z * w % n
     - 验证 c1_ = (m * pow(r_, s//g, n)) % n == c1
  7. 还原 encflag
key_payload: |
  def xgcd(a, b):
      x0, y0, x1, y1 = 0, 1, 1, 0
      while a != 0:
          q, a, b = b // a, b % a, a
          x0, x1 = x1, x0 - x1 * q
          y0, y1 = y1, y0 - y1 * q
      return b, x0, y0
  
  encflag = b""
  r_list = []
  for c1, c2 in tqdm(enc):
      if c1 == 0 and c2 == 0:
          encflag += bytes([0])
          r_list.append(-1)
          continue
      for m in range(256):
          g, x, y = xgcd(s, t)
          z = pow(c1, x, n)
          w = pow(c2, y, n)
          mm = pow(m, -(x+y), n)
          r_ = mm * z * w % n
          c1_ = (m * pow(r_, s // g, n)) % n
          c2_ = (m * pow(r_, t // g, n)) % n
          if c1_ == c1 and c2_ == c2:
              encflag += bytes([m])
              r_list.append(r_)
              break
  print(encflag)
one_liner: N1CTF 2022 Crypto: RSA 变种 (pubkey=(s, t, n), enc(m)=(m*r^s, m*r^t)), 字节级爆破 m (0-255) + xgcd 求 r。
lesson: |
  - RSA 变种: pubkey=(s, t, n), enc(m)=(m*r^s, m*r^t)
  - 字节级爆破 m (0-255) 恢复明文
  - xgcd(s, t) 求 (g, x, y) 让 s*x + t*y = g
  - 恢复 r = pow(m, -(x+y)) * pow(c1, x) * pow(c2, y) mod n
  - 验证 r^((s+t)//g) 一致
  - N1CTF 是 N1 战队主办的国际赛
quality: high
---

# N1CTF 2022 Crypto Writeups By tl2cents

> 来源: ctfiot.com 76390

## 题目

```python
def keygen():
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    phi = (p-1)*(q-1)
    while True:
        a = getrandbits(1024)
        b = phi + 1 - a
        s = getrandbits(1024)
        t = -s * a * inverse(b, phi) % phi
        if GCD(b, phi) == 1:
            break
    return (s, t, n), (a, b, n)

def enc(m, k):
    s, t, n = k
    r = getrandbits(1024)
    return m * pow(r, s, n) % n, m * pow(r, t, n) % n

pubkey, privkey = keygen()
flag = pow(bytes_to_long(flag), 0x10001, pubkey[2])
c = []
for m in long_to_bytes(flag):
    c1, c2 = enc(m, pubkey)
    c.append((c1, c2))
```

## 攻击

```python
def xgcd(a, b):
    x0, y0, x1, y1 = 0, 1, 1, 0
    while a != 0:
        q, a, b = b // a, b % a, a
        x0, x1 = x1, x0 - x1 * q
        y0, y1 = y1, y0 - y1 * q
    return b, x0, y0

encflag = b""
r_list = []
for c1, c2 in tqdm(enc):
    if c1 == 0 and c2 == 0:
        encflag += bytes([0])
        r_list.append(-1)
        continue
    for m in range(256):
        g, x, y = xgcd(s, t)
        z = pow(c1, x, n)
        w = pow(c2, y, n)
        mm = pow(m, -(x+y), n)
        r_ = mm * z * w % n
        c1_ = (m * pow(r_, s // g, n)) % n
        c2_ = (m * pow(r_, t // g, n)) % n
        if c1_ == c1 and c2_ == c2:
            encflag += bytes([m])
            r_list.append(r_)
            break
print(encflag)
```

## 评价

N1CTF 2022 Crypto 高质量 RSA 变种题目：
- 巧妙设计 `b = phi + 1 - a` 让 `s + t` 关系特定
- 字节级爆破 (0-255) 利用 flag 编码冗余
- xgcd 求 r 是经典技巧

适用读者：密码学 / RSA 研究者
