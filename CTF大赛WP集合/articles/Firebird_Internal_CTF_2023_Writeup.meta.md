---
title: Firebird Internal CTF 2023 Writeup
contest: Firebird Internal CTF 2023
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags: [rsa, partial-info, padding-oracle, rizo-duong, side-channel, 2048-bit]
attack_chain:
  - 引用 Gabrielle de Micheli, Nadia Heninger 2020 论文
  - "Recovering cryptographic keys from partial information"
  - Juliano Rizzo, Thai Duong 2010 "Practical Padding Oracle Attacks"
  - RSA 2048位 + 固定 seed(1337)
  - t=[(key.p>>random.getrandbits(10))&1 ...]
  - 已知 p/q 一些 LSB 信息
  - 构造 _ps, _qs 候选位
  - guess(n, _ps, _qs) 还原 p
  - n%p==0, q=n//p, phi=(p-1)(q-1)
  - d=pow(e,-1,phi_n), m=pow(c,d,n)
  - Padding Oracle 攻击
  - Hacker.__oracle(token) → authenticate
key_payload: random.seed(1337)  # 固定随机种子
one_liner: Firebird CTF 2023：RSA partial info recovery+padding oracle
lesson: 固定seed RSA可预测；partial info论文+padding oracle组合
quality: high
---

# Firebird Internal CTF 2023 Writeup

## 题目信息
- 比赛：Firebird Internal CTF 2023
- 类别：Crypto

## 关键攻击链
### 1. 理论基础
- Gabrielle de Micheli, Nadia Heninger (2020) "Recovering cryptographic keys from partial information"
- Juliano, Thai Duong (2010) "Practical Padding Oracle Attacks"

### 2. RSA 固定种子
```python
from Crypto.PublicKey import RSA
import random
random.seed(1337)
key = RSA.generate(2048)
t = [(key.p >> random.getrandbits(10)) & 1 if random.getrandbits(1) else (key.q >> random.getrandbits(10)) & 1 for i in range(2048)]
```

### 3. partial bit 还原
```python
if id == 0:
    assert _ps[b] in [[v], [0, 1]]
    _ps[b] = [v]
else:
    assert _qs[b] in [[v], [0, 1]]
    _qs[b] = [v]

p = guess(n, _ps, _qs)
assert n % p == 0
q = n // p
phi_n = (p-1) * (q-1)
d = pow(e, -1, phi_n)
m = pow(c, d, n)
flag = int(m).to_bytes(2048//8, 'big').lstrip(b'\0')
```

### 4. Padding Oracle 攻击
```python
class Hacker:
    def __init__(self, srv):
        self.srv = srv
    
    def __oracle(self, token):
        try:
            self.srv.authenticate(token.hex())
            return True
        except Exception as err:
            return str(err) not in [
                'Padding is incorrect.',
                'PKCS#7 padding is incorrect.'
            ]
    
    def __recover_block(self, ciphertext_block):
        iv = bytearray(16)
        ...
```

## 评分
- quality: high（partial info + padding oracle + 论文级理论）
