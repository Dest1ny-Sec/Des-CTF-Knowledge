---
title: Firebird Internal CTF 2023 Writeup
contest: Firebird Internal CTF 2023
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags:
- rsa
- partial-info
- padding-oracle
- rizo-duong
- side-channel
- 2048-bit
attack_chain:
- 引用 Gabrielle de Micheli, Nadia Heninger 2020 论文
- Recovering cryptographic keys from partial information
- Juliano Rizzo, Thai Duong 2010 "Practical Padding Oracle Attacks
- RSA 2048位 + 固定 seed(1337)
- t=[(key.p>>random.getrandbits(10))&1 ...]
- 已知 p/q 一些 LSB 信息
- 构造 _ps, _qs 候选位
- guess(n, _ps, _qs) 还原 p
- n%p==0, q=n//p, phi=(p-1)(q-1)
- d=pow(e,-1,phi_n), m=pow(c,d,n)
- Padding Oracle 攻击
- Hacker.__oracle(token) → authenticate
key_payload: 'random.seed(1337)  # 固定随机种子'
one_liner: Firebird CTF 2023：RSA partial info recovery+padding oracle
lesson: 固定seed RSA可预测；partial info论文+padding oracle组合
quality: high
full_path: Firebird_Internal_CTF_2023_Writeup.full.md
meta_path: Firebird_Internal_CTF_2023_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Firebird Internal CTF 2023 Writeup。Firebird CTF 2023：RSA partial info recovery+padding oracle。关键路径：引用 Gabrielle de Micheli, Nadia Heninger 2020 论文 → Recovering cryptographic keys from partial infor...
category: crypto
subcategory: rsa
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/95037.html
wp_author: example
reasoning_chain:
- 触发点：RSA 2048 + random.seed(1337) 固定 → 假设：seed 已知 → p/q 可预测
- 动作：分析 t = [(key.p>>random.getrandbits(10))&1 if random.getrandbits(1) else (key.q>>random.getrandbits(10))&1 for i in range(2048)]
- 假设：t 给 2048 个 p/q 某 bit 位信息 → 动作：基于 paper 'Recovering cryptographic keys from partial information'
- 假设：构造 _ps[b], _qs[b] 候选 bit 位 → 动作：调用 guess(n, _ps, _qs) → 观察：还原 p
- 动作：assert n%p==0; q=n//p; phi=(p-1)(q-1); d=pow(e,-1,phi); m=pow(c,d,n) → 观察：明文
- 第二关：Hacker.__oracle(token) 返回 Padding 是否正确 → 假设：Padding Oracle
- 动作：Hacker.__recover_block 16 字节迭代爆破 IV → 观察：每字节 256 次
- 假设：制造合法 token → 动作：register foo + signin foo 1024 次 → 观察：满足 token[30]!=1, token[31]^0x1^0x2<=token[31]
- 动作：r.sendline(f'hack {token}') → 观察：WHY? 触发 → 拿 username/password
failed_attempts:
- 试图用 sympy/numpy 求解 p 候选 → 失败：必须用 paper 提供的 guess 算法
- 试图爆破 2048-bit RSA 完整 p → 失败：必须借助 partial info
- 试图单次 signin 触发 token → 失败：必须 1024 次满足 token[31] 约束
key_observations:
- random.seed(1337) 固定 = 所有随机可预测
- RSA partial info paper 提供 guess(n, _ps, _qs) 算法核心
- Padding Oracle 攻击：每次爆破 1 字节 IV × 16 块
- AES-CBC PKCS#7 padding is incorrect 错误信息是 oracle 信号
- 合法 token 结构约束（boundary byte）是 CTF 常见过滤
prerequisites:
- RSA 数学基础（phi / mod inverse / discrete log）
- Crypto.PublicKey.RSA / random 模块
- AES-CBC + PKCS#7 padding 原理
- Padding Oracle 攻击原理
---
# Firebird Internal CTF 2023 Writeup

> 原文: https://www.ctfiot.com/95037.html
> ID: 95037

Gabrielle de Micheli, Nadia Heninger (2020) “Recovering cryptographic keys from partial information, by example”

https://hal.science/hal-03045663/document ↩︎

Juliano Rizzo, Thai Duong (2010) “Practical Padding Oracle Attacks”

https://www.usenix.org/legacy/event/woot10/tech/full_papers/Rizzo.pdf ↩︎


```
from Crypto.PublicKey import RSA
import random

random.seed(1337)

key = RSA.generate(2048)

t = [(key.p>>random.getrandbits(10))&1 if random.getrandbits(1) else (key.q>>random.getrandbits(10))&1 for i in range(2048)]
t = sum(t[i]<i) & 1
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
print(f'{flag = }')
class Hacker:
 def __init__(self, srv):
 # The function to check if the padding is correct
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

 for k in range(16):
 for i in range(256):
 iv[15-k] = i
 crafted_iv = xor(iv, bytes([k+1 for _ in range(16)]))
 if self.__oracle(crafted_iv + ciphertext_block): break
 return iv

 def __recover(self, ciphertext):
 return b''.join([
 xor(ciphertext[i-16:i],
 self.__recover_block(ciphertext[i:i+16]))
 for i in range(16, len(ciphertext), 16)
 ])

 def crack(self, token):
 token = bytes.fromhex(token)
 m = self.__recover(token)
 m = unpad(m, 16)
 m = parse_qs(m.decode())

 username, = m.get('username')
 password, = m.get('password')

 return username, password
000102030405060708090a0b0c0d0e0f 1d53a4e415b0893fc386fbea776b7198
> auth 204094b9bec1ea6b9473d345130699d2de1c31278bda8b9f4695bc8fac7116735f78bb7509cd5add82abcdca9bf7989d
?️ The token is correct for foo!
> auth 204094b9bec1ea6b9473d345130699d2de1c31278bda8b9f4695bc8fac7116735f78bb7509cd5add82abcdca9bf7989e
?️ Invalid token: Padding is incorrect..
from pwn import *

r = remote('carbon-chal.firebird.sh', 36013)

r.sendline(b'register foo xxxxxxxx\x02')
# username=foo&password=xxxxxxxx\x02

tokens = []
while len(tokens) == 0:
 # Create 1024 tokens at once to save time
 for _ in range(1024):
 r.sendline(b'signin foo xxxxxxxx\x02')

 for _ in range(1024):
 r.recvuntil(b'Signed in as foo with token ')
 token = bytes.fromhex(r.recvuntil(b'.')[:-1].decode())

 if token[30] != 1: continue
 if token[31]^0x1^0x2 > token[31]: continue
 tokens.append(token.hex())

token = tokens[0]
print(f'{token = }')
r.sendline(f'hack {token}'.encode())
r.recvuntil(b'WHY? ')

r.interactive()
f84bf7049cb55a0e1457d977e6cfbc0cc49ee1102da505e10aa3c32e619180446617ae2270cba3629b0851ae627236f19bb9cbfcadcd010eb923d170cbc2a7
import random
import re
from Crypto.Cipher import AES
from Crypto.Util import Counter
from operator import mul
from functools import reduce

# f i r e b i r d { }
known = bytes.fromhex('ffffffffffffffffff8080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080ff')
m = bytes.fromhex('66697265626972647b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007d')
c = bytes.fromhex('f84bf7049cb55a0e1457d977e6cfbc0cc49ee1102da505e10aa3c32e619180446617ae2270cba3629b0851ae627236f19bb9cbfcadcd010eb923d170cbc2a7')

def xor(a, b):
 return bytes([u^^v for u, v in zip(a, b)])

keystreams = []
for k in range(256):
 cipher = AES.new(bytes([k]) + b'\0'*15, AES.MODE_CTR, counter=Counter.new(128, initial_value=int(0)))
 keystreams.append(
 cipher.encrypt(b'\0'*len(c))
 )

A = []
b = []

# The number of entries I guessed that they are zeroes
# Suggested: sampled_zeroes + number_of_equations >= 256 (or add some more to avoid less false positives...)

number_of_equations = bin(int.from_bytes(known, 'big')).count('1')
sampled_zeroes = 256 - number_of_equations
assert sampled_zeroes <= 256-16
print(f'{sampled_zeroes + number_of_equations = }')

for i, (rc, mc, cc) in enumerate(zip(known, m, c)):
 for j in range(8):
 if (rc>>j) & 1 == 0: continue
 mb = (mc>>j) & 1
 cb = (cc>>j) & 1

 row = [(k[i]>>j) & 1 for k in keystreams]

 A.append(row)
 b.append(mb^^cb)

F = GF(2)
A = Matrix(F, A)
b = vector(F, b)

hit_frequency = reduce(mul, [(256-16-k)/(256-k) for k in range(sampled_zeroes)])
print(f'{number_of_equations = }')
print(f'{sampled_zeroes = }')
print(f'Expecting a hit every {int(1/hit_frequency)} times')

attempt = 0
while True:
 attempt += 1

 # The 128 entries "I" guessed it is non-zero
 v = sorted(random.sample(range(256), k=256-sampled_zeroes))

 _A = A[:, v]
 try:
 x0 = _A.solve_right(b)
 for dx in _A.right_kernel():
 flag = c
 set_bits_count = 0
 for i in range(256-sampled_zeroes):
 if x0[i] == dx[i]: continue
 set_bits_count += 1
 flag = xor(flag, keystreams[v[i]])

 flag = flag.decode()
 if not re.match(r'firebird\{\w+\}', flag): continue
 if set_bits_count > 16: continue

 print(f'[*] Flag recovered at attempt #{attempt}: {flag}')
 assert False, 'done!'

 
except KeyboardInterrupt:
 raise KeyboardInterrupt
 
except AssertionError as err:
 raise err
 
except:
 pass
```
