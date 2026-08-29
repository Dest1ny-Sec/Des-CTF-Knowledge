---
title: HKCERT CTF 2022 Postmortem (I): Easier Crypto Challenges
contest: HKCERT CTF 2022
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags: [crypto, dlp, cookie-flipping, cbc, base64, negative-e, gcd, mystiz]
attack_chain:
  - DLP: p=1444...g=2 h=679...求 x
  - Cookie flipping: JSON {"username":"mystiz","x":13,"y":5}
  - 改为"mystiz_"
  - flag: hkcert22{cu7_4nd_p45t3_1ik3_4_3ng1n3er}
  - CBC bit flipping attack
  - Negative e RSA: e=-1/-2/-3
  - m0="The secret token is "+padding+" and it is encrypted with e = N."
  - gcd(n1, n2, n3) 还原N
  - pow(256, -33, n) * (pow(c1, -1, n) - m1) % n 还原secret
key_payload: gcd(c2*(m2*c1+1-m1*c1)^2 - c1^2, c3*(m3*c1+1-m1*c1)^3 - c1^3)  # 求N
one_liner: HKCERT 2022 Easy Crypto：DLP+Cookie翻转+负指数RSA恢复N
lesson: 负指数e=-1/-2/-3加密可构造已知消息恢复模数N
quality: high
---

# HKCERT CTF 2022 Postmortem (I): Easier Crypto Challenges

## 题目信息
- 比赛：HKCERT CTF 2022
- 作者：mystiz
- 类别：Crypto（Easier）

## 关键攻击链
### 1. DLP
```python
p = 1444779821068309665607966047026245709114363505560724292470220924533941341173119282750461450104319554545087521581252757303050671443847680075401505584975539
g = 2
h = 679175474187312157096793918495021788380347146757928688295980599009809870413272456661249570962293053504169610388075260415234004679602069004959459298631976
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
# 求 x: h = g^x mod p
```

### 2. Cookie 翻转
```json
{"username":"mystiz","x":13,"y":5,"inventory":[],"onMapItems":[...]}
```
- 改为 `"mystiz_"` 拿到 flag
- flag: `hkcert22{cu7_4nd_p45t3_1ik3_4_3ng1n3er}`

### 3. CBC Bit Flipping
- 字符串 Padding Oracle 攻击
- 翻转 base64 字符

### 4. 负指数 RSA
```python
# m0 = "The secret token is "
# m1 = " and it is encrypted with e = "
# m2 = "."
r = remote('chal.hkcert22.pwnable.hk', 28101)
c1, c2, c3 = encrypt(-1), encrypt(-2), encrypt(-3)
# e = -1: c = m^(-1) mod n
# e = -2: c = m^(-2) mod n
# e = -3: c = m^(-3) mod n
m1 = int.from_bytes(b'The secret token is ' + b'\0'*128 + b' and it is encrypted with e = -1.', 'big')
m2 = ... (e = -2)
m3 = ... (e = -3)
n = gcd(
    c2 * (m2 * c1 + 1 - m1 * c1)**2 - c1**2,
    c3 * (m3 * c1 + 1 - m1 * c1)**3 - c1**3
)
# 消除小因子
for k in range(2, 1000):
    while n % k == 0:
        n //= k
secret = pow(256, -33, n) * (pow(c1, -1, n) - m1) % n
```

## 评分
- quality: high（DLP + Cookie 翻转 + 负指数 RSA gcd 恢复 N）
