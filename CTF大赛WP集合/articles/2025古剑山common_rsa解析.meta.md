---
title: 2025 古剑山 common_rsa 解析（RSA 共模攻击+扩展欧几里得）
contest: 2025 古剑山
year: 2025
difficulty: medium
vuln_type: [crypto_rsa, lattice]
tags: [古剑山 2025 common_rsa 物不知数, RSA 共模攻击 同一 m 不同 e, c1=m^e1 mod N, c2=m^e2 mod N, gcd(e1, e2)=1, 扩展欧几里得 s*e1+t*e2=1, m=c1^s * c2^t mod N, c1_inv=invert(c1, N) c1^(-1)^334, part1+part2 mod N, gmpy2.gcdext]
attack_chain:
  - 同 N 同 m 不同 e1, e2，e1=35422 e2=1033
  - 扩展欧几里得 gcd(e1, e2)=1, s=-334, t=11453
  - s*e1 + t*e2 = -334*35422 + 11453*1033 = 1
  - c1^s = c1^(-334) = (c1^(-1))^334
  - c1_inv = gmpy2.invert(c1, N)
  - m = (c1_inv)^|s| * c2^t mod N = (c1^(-1))^334 * c2^11453 mod N
  - flag = bytes.fromhex(hex(m)[2:])
key_payload: "m = (c1_inv)^|s| * c2^t mod N"
one_liner: 2025 古剑山 common_rsa 物不知数：同 N 同 m 不同 e1=35422, e2=1033 共模攻击，扩展欧几里得求 s, t，c1^(-1)^334 * c2^11453 mod N 还原 m。
lesson: RSA 共模攻击 = 同 N 同 m 不同 e，扩展欧几里得求 s*e1 + t*e2 = 1，m = c1^s * c2^t mod N；s 为负数时取模逆元 invert(c1, N)。
quality: high
---

# 2025 古剑山 common_rsa 解析（物不知数）

## 题目背景

```
N = 162178605357818616394571566923155907889899677780239882906511996614607940884142045197452389471499799373787832649318837814454679970724845203557871078001956378966434166323827984964942729898095347038272003371167123553368531662277059263517900162297903110415768403265100411543878859321181606008503516896600638590699
e1 = 35422
c1 = 153249315480380808558746807096025628082875635601515291525075274335055878390662930254941118045696231628008256877302589689883059616503108946971165183674522403835250738176157466145855833767128209866527507862726083268576304163200171600023472544755768741118904892489037291247455823396160705615280802805803254323033
e2 = 1033
c2 = 5823189490163315770684717059899864988806118565674660089157163486577056500243194221873916232616081138765317598078910078375360361118674333149663483360677725162911935082290640547407140413703664960164356579153623498735889314476063673352676918268911309402784919521792079943937126634436658784515914270266106683548
```

## 攻击原理

### 同 N 同 m 不同 e

```
c1 = m^e1 mod N
c2 = m^e2 mod N
```

### 扩展欧几里得

```python
def extended_gcd(a, b):
    if b == 0: return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y
```

求 `s*e1 + t*e2 = 1`：
```python
gcd, s, t = gmpy2.gcdext(e1, e2)
# gcd(e1, e2) = 1
# s = -334, t = 11453
# 验证: -334 * 35422 + 11453 * 1033 = -11830948 + 11830949 = 1
```

### 还原 m

```
c1^s * c2^t mod N
= (m^e1)^s * (m^e2)^t mod N
= m^(e1*s) * m^(e2*t) mod N
= m^(e1*s + e2*t) mod N
= m^1 mod N
= m mod N
```

s = -334（负数）→ 取 `c1_inv = gmpy2.invert(c1, N)`：

```python
import gmpy2
c1_inv = gmpy2.invert(c1, N)
part1 = pow(c1_inv, abs(s), N)  # (c1^-1)^334 mod N
part2 = pow(c2, t, N)            # c2^11453 mod N
m = (part1 * part2) % N
flag = bytes.fromhex(hex(m)[2:])
print(flag.decode('ascii'))
```

## 完整解

```python
import gmpy2
N = ...
e1 = 35422; e2 = 1033
c1 = ...; c2 = ...
gcd, s, t = gmpy2.gcdext(e1, e2)
c1_inv = gmpy2.invert(c1, N)
part1 = pow(c1_inv, abs(s), N)
part2 = pow(c2, t, N)
m = (part1 * part2) % N
flag = bytes.fromhex(hex(m)[2:])
print(flag.decode('ascii'))
```
