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
