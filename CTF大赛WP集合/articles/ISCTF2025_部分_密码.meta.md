---
title: ISCTF 2025 部分密码题
contest: ISCTF
year: 2025
difficulty: medium
vuln_type: crypto_oracle
tags: [variant Caesar, 幂塔 2^2^t, RSA p+q, LLL 格, 三角函数]
attack_chain: |
  1. Ez_Caesar (variant Caesar): shift 初值 2，加密每字符后 shift += 3 → KXKET{Tubsdx_re_hg_zytc_hxq_vnjma} 反向解密得 ISCTF{Caesar_is_so_easy_and_funny}
  2. Power tower: m = ISCTF{...}, n=p (256-bit prime), t=63-bit prime, l = pow(2, pow(2, t), n), c = m ^ l
     → 攻击: factorint(n) → φ(n) → 扩展欧拉定理 2^(2^t) mod n = pow(2, pow(2, t, φ(n)), n) → m = c ^ l
  3. easy_RSA: 给出 N + ct1=pow(msg, e, N) + ct2=pow(msg, p+q, N) → 因为 p+q 已知可从 ct2 拿到 m^(p+q)，但 p+q 需要 leak
     → 利用 RSA 原根 + (p+q) 可对 φ(N) 简化: m^(p+q) mod N = m^(p+q mod φ(N)) mod N → ct2 = pow(msg, p+q, N) → 直接求 p+q = log_m(ct2) mod φ(N) (当 e=65537 时存在 CRT 解)
  4. LLL 格三角函数: enc = a*cos(x) + b*sin(x) (a, b 是 flag 拆两段) → 构造 matrix M = [[1,0,0,round(cos_x*scale)], [0,1,0,round(sin_x*scale)], [0,0,1,round(enc*scale)]] → LLL 短向量找 (a, b) → flag_part1 + flag_part2
key_payload: |
  # Ez_Caesar 解密:
  def variant_caesar_decrypt(text):
      decrypted, shift = '', 2
      for c in text:
          if c.isalpha():
              base = ord('A') if c.isupper() else ord('a')
              decrypted += chr((ord(c) - base - shift) % 26 + base)
              shift += 3
          else:
              decrypted += c
      return decrypted
  print(variant_caesar_decrypt("KXKET{Tubsdx_re_hg_zytc_hxq_vnjma}"))
  # => ISCTF{Caesar_is_so_easy_and_funny}
  
  # Power tower 欧拉:
  t = 6039738711082505929
  n = 107502945843251244337535082460697583639357473016005252008262865481138355040617
  c = 114092817888610184061306568177474033648737936326143099257250807529088213565247
  factors = factorint(n)
  phi_n = 1
  for p, k in factors.items():
      phi_n *= (p**(k-1)) * (p-1)
  l = pow(2, pow(2, t, phi_n), n)
  flag = long_to_bytes(c ^ l)
one_liner: ISCTF 2025 4 道密码 (变种凯撒 / 幂塔欧拉 / RSA p+q leak / LLL 三角函数) 速查。
lesson: |
  - 变种凯撒 + 动态 shift 是入门套路，shift += 3 时已知明密文对可推
  - 幂塔 2^(2^t) mod n 必须先 factor(n) 求 φ(n)，再用扩展欧拉定理 pow(2, pow(2, t, φ(n)), n)
  - ct2=pow(msg, p+q, N) 是 RSA 变种，p+q 是关键 leak，结合 ct1 标准 RSA 可联立
  - LLL 求 a*cos(x)+b*sin(x) 中 a/b 用 round(coeff*2^400) 缩放 + matrix LLL 找短向量
quality: medium
---

# ISCTF 2025 部分密码题

> 来源: ctfiot.com 286515

## 1. Ez_Caesar (变种凯撒)

加密时 shift 初始为 2，每加密一个字母后 `shift += 3`：

```python
def variant_caesar_encrypt(text):
    encrypted, shift = '', 2
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            encrypted += chr((ord(c) - base + shift) % 26 + base)
            shift += 3
        else:
            encrypted += c
    return encrypted
```

密文 `KXKET{Tubsdx_re_hg_zytc_hxq_vnjma}` → 反向解密 `shift -= 3` → `ISCTF{Caesar_is_so_easy_and_funny}`

## 2. Power tower

```python
m = b'ISCTF{...}'
n = getPrime(256); t = getPrime(63)
l = pow(2, pow(2, t), n)
c = m ^ l
```

攻击：先 `factorint(n)` 求 φ(n)，再用扩展欧拉定理：

```python
phi_n = 1
for p, k in factorint(n).items():
    phi_n *= (p**(k-1)) * (p-1)
l = pow(2, pow(2, t, phi_n), n)
flag = long_to_bytes(c ^ l)
```

## 3. easy_RSA (ct2 leak p+q)

```python
N, e = p*q, 65537
ct1 = pow(msg, e, N)
ct2 = pow(msg, p+q, N)  # 关键 leak：指数 p+q
```

利用 `pow(msg, p+q, N) = pow(msg, p+q mod φ(N), N)`，结合 ct1 标准 RSA 可联立：
- 由 ct1 = msg^e mod N → msg = pow(ct1, d, N)
- 代入 ct2 验证：ct2 = pow(msg, p+q, N)
- 求 p+q：解离散对数 m^(p+q) = ct2 mod N → 当 gcd(p+q, φ(N))=1 时 p+q = log_m(ct2) mod φ(N)

## 4. LLL 格三角函数

`enc = a*cos(x) + b*sin(x)`，a/b 是 flag 拆两段：

```python
R = RealField(1000)
x_r = R(x); cos_x = cos(x_r); sin_x = sin(x_r)
scale = 2^400
M = matrix(ZZ, [
    [1, 0, 0, round(cos_x * scale)],
    [0, 1, 0, round(sin_x * scale)],
    [0, 0, 1, round(enc * scale)]
])
L = M.LLL()
for row in L:
    if abs(row[2]) == 1:
        a, b = abs(row[0]), abs(row[1])
        if abs(a*cos_x + b*sin_x - enc) < 1e10:
            flag = long_to_bytes(a) + long_to_bytes(b)
            break
```

## 评价

4 道密码合集 (变种凯撒 / 幂塔 / RSA p+q leak / LLL 三角函数)，覆盖了 ISCTF 2025 密码入门到中等难度。代码片段完整可直接跑，但每题只有"攻击 + payload"没有"思路推导"，适合作为已知技巧速查。
