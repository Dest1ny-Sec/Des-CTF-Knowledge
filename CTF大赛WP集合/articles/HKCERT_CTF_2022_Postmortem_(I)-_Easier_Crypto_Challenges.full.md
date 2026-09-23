---
title: 'HKCERT CTF 2022 Postmortem (I): Easier Crypto Challenges'
contest: HKCERT CTF 2022
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags:
- crypto
- dlp
- cookie-flipping
- cbc
- base64
- negative-e
- gcd
- mystiz
attack_chain:
- 'DLP: p=1444...g=2 h=679...求 x'
- 'Cookie flipping: JSON {"username":"mystiz","x":13,"y":5}'
- 改为"mystiz_
- 'flag: hkcert22{cu7_4nd_p45t3_1ik3_4_3ng1n3er}'
- CBC bit flipping attack
- 'Negative e RSA: e=-1/-2/-3'
- m0="The secret token is "+padding+" and it is encrypted with e = N.
- gcd(n1, n2, n3) 还原N
- pow(256, -33, n) * (pow(c1, -1, n) - m1) % n 还原secret
key_payload: 'gcd(c2*(m2*c1+1-m1*c1)^2 - c1^2, c3*(m3*c1+1-m1*c1)^3 - c1^3)  # 求N'
one_liner: HKCERT 2022 Easy Crypto：DLP+Cookie翻转+负指数RSA恢复N
lesson: 负指数e=-1/-2/-3加密可构造已知消息恢复模数N
quality: high
full_path: HKCERT_CTF_2022_Postmortem_(I)-_Easier_Crypto_Challenges.full.md
meta_path: HKCERT_CTF_2022_Postmortem_(I)-_Easier_Crypto_Challenges.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'HKCERT CTF 2022 Postmortem (I): Easier Crypto Challenges。HKCERT 2022 Easy Crypto：DLP+Cookie翻转+负指数RSA恢复N。关键路径：DLP: p=1444...g=2 h=679...求 x → Cookie flipping: JSON {"username":"mystiz","x":13,...'
category: crypto
subcategory: rsa
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/87576.html
reasoning_chain:
- 触发点：DLP 三元组 (p,g,h)=(1444...,2,679...) → 假设：p-1 平滑可 Pohlig-Hellman 解 x → 动作：Sage discrete_log(h, g, p)
- 观察：x=小整数 → 下一步：用 x 当 AES key 解密游戏 token
- 触发点：cookie 是 JSON {username,mystiz;x:13;y:5;...} + 加密 base64 → 假设：CBC bit flipping 改 username 一位即可拿 flag → 动作：翻转密文第 16 字节把 'mystiz' 改成 'mystiz_'
- 观察：服务端 cookie 解密后 username='mystiz_' → flag hkcert22{cu7_4nd_p45t3_1ik3_4_3ng1n3er}
- 触发点：RSA 题目给出 e=-1/-2/-3 + 已知 m0='The secret token is ' + 128-byte secret + ' and it is encrypted with e = N.' → 假设：可构造 µ1=已知 m 但 secret 段填 0
- 动作：encrypt(-1/-2/-3) 三次得 c1/c2/c3 → 推导 n = gcd(c2*(µ2*c1+1-µ1*c1)^2 - c1^2, c3*(µ3*c1+1-µ1*c1)^3 - c1^3) → 观察：拿到 n
- 下一步：secret = pow(256, -33, n) * (pow(c1, -1, n) - µ1) % n → 动作：r.sendline(secret) → 观察：拿到 flag
failed_attempts:
- 试图直接对 e=-1 算 pow(c1, -1, n) → 失败：未知 n，无法直接求逆元
- 试图单独用 e=-2 / e=-3 推导 secret → 失败：必须先恢复 n
key_observations:
- 负指数 e=-1/-2/-3 + 已知消息前缀可构造仿射方程组，gcd 三次结果得到 n 是经典 RSA 还原套路
- CBC bit flipping 第 i 块只影响第 i+1 块明文，翻转 1 字节可改 username
- Pohlig-Hellman 对 p-1 平滑椭圆曲线群 / 加法群都有效，discrete_log 是 CTF 入门必会
- DLP + bit flipping + RSA 三题共用 hkcert22{cu7_4nd_p45t3_1ik3_4_3ng1n3er} 标志属于系列化题目设计
prerequisites:
- Sage discrete_log + Pohlig-Hellman 算法
- AES-CBC bit flipping 攻击
- RSA 负指数 + GCD 还原模数技巧
- Python Crypto.Util.number + pwntools
---
# HKCERT CTF 2022 Postmortem (I): Easier Crypto Challenges

> 原文: https://www.ctfiot.com/87576.html
> ID: 87576


```
p = 1444779821068309665607966047026245709114363505560724292470220924533941341173119282750461450104319554545087521581252757303050671443847680075401505584975539
g = 2
h = 679175474187312157096793918495021788380347146757928688295980599009809870413272456661249570962293053504169610388075260415234004679602069004959459298631976
def gcd(a, b):
 while b != 0:
 a, b = b, a % b
 return a
{"username":"mystiz","x":13,"y":5,"inventory":[],"onMapItems":[{"item":0,"x":3,"y":4},{"item":0,"x":3,"y":4},{"item":1,"x":4,"y":5},{"item":1,"x":5,"y":5},{"item":1,"x":6,"y":5},{"item":0,"x":15,"y":1}]}
document.cookie
document.cookie="game-token=bar"
fff21bf4a7d27a027502b1e1a253b35f071efbc3642eea3269d634e6c984feebf89e4736ab5b
a5b4ef81b78a57a889ba4cf06024a9c302947c9a620592c23a76476e8424c54f1f47216f45d9
03c1baa4d2bd6f06d268a81b9d30326c80f521249fdba79cf386395248f82a0236c0771ae421
0d738aa474035eda8131cc3f384ac551a93538d21903eb1b717741df7e1b7ac7350304f0d7f6
db588f809cf319706f0a09ededf7547fab175c8e132a832c878303dd6064ba98361cf4f9784a
0699
{"username":"mystiz_","x":13,"y":5,"inventory":[],"onMapItems":[{"item":0,"x":3,"y":4},{"item":1,"x":4,"y":5},{"item":1,"x":5,"y":5},{"item":1,"x":6,"y":5},{"item":0,"x":15,"y":1}]}
Message: {"username":"mys{"username":"mys
Ciphertext: fff21bf4a7d27a027502b1e1a253b35f fff21bf4a7d27a027502b1e1a253b35f
fff21bf4a7d27a027502b1e1a253b35ffb2333bf9573b1d240840aefb4f78b1e071efbc3642e
ea3269d634e6c984feebf89e4736ab5ba5b4ef81b78a57a889ba4cf06024a9c302947c9a6205
92c23a76476e8424c54f1f47216f45d903c1baa4d2bd6f06d268a81b9d30326c80f521249fdb
a79cf386395248f82a0236c0771ae4210d738aa474035eda8131cc3f384ac551a93538d21903
eb1b717741df7e1b7ac7350304f0d7f6db588f809cf319706f0a09ededf7547fab175c8e132a
832c878303dd6064ba98361cf4f9784a0699
{"username":"mystiz_","x":13,"y":5,"inventory":[0,0,0,0,0,0,0,0 ],"onMapItems":[{"item":0,"x":3,"y":4},{"item":1,"x":4,"y":5},{"item":1,"x":5,"y":5},{"item":1,"x":6,"y":5},{"item":0,"x":15,"y":1}]}
hkcert22{cu7_4nd_p45t3_1ik3_4_3ng1n3er}
Plaintext: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Ciphertext: 4czfHjwa9rl+Xds/1EbFuJioVRnYL0ym86UZ2WDMQPgBKGT5AN3Cqe7OShpvkxIt
Plaintext: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Ciphertext: 4czIHjwaYd8F1St/xEb7rJioV0+RLnygf6UGZWDMQPuBClqKAX35Te9ONhsv2mkp
Plaintext: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Ciphertext: 4czIHjwaYd8F1St/xEb7rJioV0+RLnygfWUGZ6DMQPuBClqKAX35Te9ONhsv2mkp
The secret token is [SECRET] and it is encrypted with e = [E].
# m0 = "The secret token is "
m0 = 0x5468652073656372657420746f6b656e2069732
# m1 = " and it is encrypted with e = "
m1 = 0x20616e6420697420697320656e6372797074656420776974682065203d20
# m2 = "."
m2 = 0x2e
from math import gcd
from pwn import *

r = remote('chal.hkcert22.pwnable.hk', 28101)

def encrypt(e):
 r.sendline(str(e).encode())
 r.recvuntil(b'c = ')
 c = int(r.recvline().decode(), 16)
 return c

c1, c2, c3 = encrypt(-1), encrypt(-2), encrypt(-3)

µ1 = b'The secret token is ' + b'\0'*128 + b' and it is encrypted with e = -1.'
µ2 = b'The secret token is ' + b'\0'*128 + b' and it is encrypted with e = -2.'
µ3 = b'The secret token is ' + b'\0'*128 + b' and it is encrypted with e = -3.'

µ1, µ2, µ3 = [int.from_bytes(µ, 'big') for µ in [µ1, µ2, µ3]]

n = gcd(
 c2 * (µ2 * c1 + 1 - µ1 * c1)**2 - c1**2,
 c3 * (µ3 * c1 + 1 - µ1 * c1)**3 - c1**3
)
log.info(f'{n = }')

# Eliminate small factors
for k in range(2, 1000):
 while n % k == 0:
 n //= k

secret = pow(256, -33, n) * (pow(c1, -1, n) - µ1) % n
assert secret < 256**128
secret = int.to_bytes(secret, 128, 'big')
log.info(f'{secret = }')
r.sendline(secret)

r.interactive()
```
