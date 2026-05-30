# DASCTF 2023 7月 逆向题解

> 原文: https://www.ctfiot.com/134546.html
> ID: 134546

一

controlflow

S = [3279, 3264, 3324, 3288, 3363, 3345, 3528, 3453, 3498, 3627, 3708, 3675,
 3753, 3786, 3930, 3930, 4017, 4173, 4245, 4476, 4989, 4851, 5166, 5148, 4659,
 4743, 4596, 5976, 5217, 4650, 6018, 6135, 6417, 6477, 6672, 6891, 7056, 7398,
 7650, 7890]

for i in range(0, 20, 2):
 tmp = S[11 + i]
 S[11 + i] = S[10 + i]
 S[10 + i] = tmp

for i in range(40):
 assert(S[i] % 3 == 0)
 S[i] //= 3
 S[i] += i

for i in range(20):
 S[10 + i] ^= i * (i + 1)

for i in range(40):
 S[i] -= i * i
 S[i] ^= 0x401

F = ''.join(chr(s) for s in S)
print(F)

二

webserver

dataP = [
 [33211, 36113, 28786, 44634, 30174, 39163, 34923, 44333, 33574, 23555],
 [35015, 42724, 34160, 49166, 35770, 45984, 39754, 51672, 38323, 27511],
 [31334, 34214, 28014, 41090, 29258, 37905, 33777, 39812, 29442, 22225],
 [30853, 35330, 30393, 41247, 30439, 39434, 31587, 46815, 35205, 20689]
]

dataQ = [
 [23, 13, 4, 48, 41, 41, 42, 33, 30, 3],
 [69, 1, 13, 45, 41, 64, 8, 80, 15, 42],
 [56, 19, 62, 70, 23, 63, 30, 68, 17, 56],
 [92, 12, 16, 64, 31, 3, 17, 71, 58, 9],
 [64, 83, 71, 52, 99, 89, 76, 68, 1, 99],
 [16, 16, 52, 43, 0, 44, 50, 32, 50, 31],
 [20, 63, 2, 99, 0, 57, 79, 43, 71, 19],
 [80, 92, 93, 58, 84, 74, 81, 45, 55, 21],
 [ 1, 99, 30, 28, 56, 1, 12, 77, 92, 4],
 [37, 67, 60, 54, 51, 79, 38, 87, 48, 16]
]

import sympy as sp

P = sp.Matrix(dataP)
Q = sp.Matrix(dataQ)
Q_ = Q.inv()
F = P * Q_
print(''.join(chr(f) for f in F))

三

TCP

for ( i = 0; i <= 3; ++i )
 *(_QWORD *)&g_buf[8 * i] = rand();
 for ( j = 0; j <= 15; ++j )
 g_buf[j + 32] = rand();

__int128 f(__int128 m, __int128 a, __int128 b) {
 __int128 x = a;
 __int128 y = 0;
 while (b != 0) {
 if (b & 1)
 y = __modti3(x + y, m);
 else
 x = __modti3(2 * x, m);
 b >>= 1;
 }
 return y
}

void decrypt(char *key, char *src, int len, char *ret)
{
 int i, j, k;
 if ( len > 15 )
 {
 for ( i = 0; i < len; ++i )
 ret[i] = src[i];
 for ( j = len - 16; j >= 0; --j )
 tea_decrypt(key, (unsigned __int64 *)&ret[j]);
 }
 else
 {
 for ( k = 0; k < len; ++k )
 ret[k] = key[k + 32] ^ src[k];
 }
}

from pwn import *
from Crypto.Util.number import *

n = unpack(bytes.fromhex('5fcef0e867349fc68f40763a6b0bde01'), 128)
e = unpack(bytes.fromhex('01000100000000000000000000000000'), 128)
print(f'n = {n}, n_hex = {hex(n)}')
print(f'e = {e}, e_hex = {hex(e)}')

p = 1152921504606848051
assert(isPrime(p))
q = 2152921504606847269
assert(isPrime(q))
assert(p * q == n)

phi = inverse(e, (p - 1) * (q - 1))
print(f'phi = {phi}')

buf60h = bytes.fromhex('7a3202cc78acb66216341041b18ea201a3eb93301b27a2b6e77cb244d2e02c0082cd6369f3a7c1d2a1dd9b561c98510017c911f2ac5ec565e2d9b9016df34900661212d889172b99954d25018b5d43012e81783c2d8cebedeb053ccd651de400')
buf48h = b''
for i in range(6):
 number = unpack(buf60h[i*16 : (i+1)*16], 128)
 number = pow(number, phi, n)
 buf48h += pack(number, 64, endianness='big')
 print(f'numbers[{i}] = {hex(number)}')
print(f'buf48h = {buf48h}')
assert(len(buf48h) == 48)

msg = bytes.fromhex('16cb56c17a19fb2ddcdb8472d52d1d6b1693164a13316a33be05bc1c4a2029b9efbf96dc917da5056d3ee46c2b0815cb56c17b19fb2de6db847211fd382bc3eb739037f7dfa4b0ca553f4dc67f81b71b7f9215cb56c17819fb2dd6db84727c8526cc3d6383bbcf0159590648586e7dd08b49cc1ee7f519ec206592254842b7f33d25646640ab16cb56c17a19fb2de5db8472c008ba6c15334f76485d8c17082f4468addbb3a62d20e754105d1014cb56c17a19fb2dfedb847215cb56c17219fb2dbdd984723419b3ea63306ff1224173d834b1f9c436332f39ec2aa102bb7747859d50793674b05a56f14ee29491895944cbf1f6846a9831f8dd5666202c4b0d558a690239b1dece4322fe535c0742cc2f37378577b999eaab713d853643bc379dac7f7f471ef2240b8898fac4431149aa27a65507db39a9111dea802a803506fbd4a2d558068974f993dcab4587a5620db6909a951dcf8bb65d4f8e92ac8300fd049bb3218199705babb255e7daef40a28c1d7e3f74cb1d44687be127258aafc4dbdaf09266daa68605e250aa244c179d759d22e90ed3d8a9bf155fae86c721ed8ee5603c4613ac47e5a80079b909727277fff31d20529b3c022e3b1a3616d639ca036586ef17d3dc9bdf1eeec5859f0022514f29b240f30c818e7fdd478f36779978c08885b2266e3cf599d0a4c27bca4615720a08e13916ec4a6ef5c943ddb25566e620726f56c5160913564d683badcc7204ec8e7080221de325a431a0680e9e108e427c7bc3807b86c78820bc9c2340709da352d953aea805a04b53f2d88f7b8fae50e5ba2de55615bc9b2e526167226e75f5c8827593281f23a65e5098e0e8e2623ee4f892bac76e6987a05832bc0b84215bb74ed83786bd55265e61ba5702170fda63e01a44d6b8a6f1740a6c03803095e5176bde18ee873dcd6380de9f325f1c436c11e3250cebceceb319a49a4e3f2f62cfd137b602e27f3974a113df414287da48afd9e8c7ef0bdb4d345313b52d662202f543f426f8271432a20186b1dc7f70d4123def1c3745c1ffe7f4017ff60e0b7486f0e8db90889a36072583ddb26dbd37778115cb56c17e19fb2d5edb847263424fb4921f224eb2d445183f9bc6541d1ac77072a6e616e6826cbbebe96af229e79620462869e51686d4d523f782b2e5b43a769403bf62f1b87512013f95d068dc04beb337f8741b471386a7746ebc7b9c7a9568ed9b590936cdc533f6f943e3a37966362b62092ce5a3c53a95b33d0ff1ac2c5800b67b8cc40d614b8df74d4114d4bb7104b545ac7d0b9eb606578fd63561578740ce7eeaa189baacd436ae15cb56c17f19fb2d5edb8472ecc4942bbc4e2bbec5c4adb791a7096298f6347c4a277364cea894234bdcf69811f31ce644bae10edc0de4ccc200a44fa0e2faa4d2eb3b28dcecc3a468efdbfa7de2728b27dfafd1a5df4803a7986cfa768fb1f9751ba1a7d47c9a6928978810d76dceb819738f4684637d3ddd2cc41e2a4585a366d4a46b32db59508f34bf5c654be7b5c86e24cca5d1013738c32ba9b6083e76e0f93c80fe712261841e546315cb56c17c19fb2d5edb847260fd338fdcecb096e26a56603082a58f5b1fb0ffb7fc8faac33589ec52ed02256aba88b2c2836433a5d146c6efe784d47da7a7ffc4256f3dce73314c0171f89e9a4f6a95f59e8460d2b65fe178daba5faf8d34d99e32a50aefbbb7ed9c9507765958870dd2e1836fe608215ca753a7125f3cb86ac32d1149cf2a144b873fc7a96914d376ed2fe88d36a609596a68d8bb76e71d1b81a8db3618271f002ff6fb5815cb56c17d19fb2d5edb8472b72d657abc1a3c2133fa45fd834d28fce3b5bdd8f111bfa61386a306aa74598ea6e5022f4aac8d9acd442c44465eb334c26d060dfc8f4f59c13f3225a5ea111f9e3e9ef4c75f40b85c43dbdd5d30970cde507cd96fa6a88970e23c1dc1cb9a1eab2f4cc16444226aff6c49dd13e030240ea32267a1699b5b8c83d05c1cc257f5028d649e2b58d96a1f59fcd42f027179e7400f2c64c3063ae1f9c496ec019eba12cb56c17219fa2dfedb847213cb56c17919fb2dfedb847211cb56c17a19fb2dfedb8472')
tea_key = [
 unpack(buf48h[i*8 : (i+1)*8], 64)
 for i in range(4)
]
xor_key = buf48h[32:48]
for i in range(4):
 print(f'tea_key[i] = {tea_key[i]}, hex_tea_key[i] = {hex(tea_key[i])}')
print(f'xor_key = {xor_key}')

def tea_decrypt(d):
 v0 = unpack(d[0:8], 64)
 v1 = unpack(d[8:16], 64)
 s = 0x13c6ef3720
 LIMIT = 0xffff_ffff_ffff_ffff
 for i in range(32):
 tmp = ((v0 + s) ^ ((v0 << 4) + tea_key[2]) ^ ((v0 >> 5) + tea_key[3])) & LIMIT
 v1 = (v1 - tmp) & LIMIT
 tmp = ((v1 + s) ^ ((v1 << 4) + tea_key[0]) ^ ((v1 >> 5) + tea_key[1])) & LIMIT
 v0 = (v0 - tmp) & LIMIT
 s = (s - 0x9e3779b9) & LIMIT
 return pack(v0, 64) + pack(v1, 64)

def decrypt(m):
 l = len(m)
 if l > 15:
 b = bytearray(m)
 for i in range(l-16, -1, -1):
 b[i:(i+16)] = tea_decrypt(b[i:(i+16)])
 return bytes(b)
 else:
 return bytes(m[i] ^ xor_key[i] for i in range(len(m)))

buf = bytearray(400 * 10)
idx = 0

while True:
 instr = decrypt(msg[idx:
idx+12])
 idx += 12
 a0 = unpack(instr[0:4], 32)
 a1 = unpack(instr[4:8], 32)
 a2 = unpack(instr[8:12], 32)
 if a0 == 1:
 print(decrypt(msg[idx:
idx+a2]))
 idx += a2
 elif a0 == 2:
 data = decrypt(msg[idx:
idx+a2])
 idx += a2
 buf[400*a1:
400*a1+a2] = data
 print(f'stored data at segment {a1}')
 elif a0 == 3:
 print(f'input data at segment {a1}')
 elif a0 == 4:
 print(f'show data at segment {a1}')
 elif a0 == 5:
 print(f'execute data at segment {a1 & 0xffff}')
 else:
 print('ended')
 break

with open('program', 'wb') as f:
 f.write(buf)

from ida_bytes import get_bytes
from struct import *

seg4 = get_bytes(400 * 4, 160)
seg5 = get_bytes(400 * 5, 160)
seg6 = get_bytes(400 * 6, 160)
seg7 = get_bytes(400 * 7, 160)

flag = ''
buf = bytearray(160)
for i in range(0, 160, 4):
 buf[i:i+2] = seg7[i:i+2]
 buf[i+2:i+4] = seg6[i:i+2]
 p = unpack('>= 1;
 }
 return y
}
void decrypt(char *key, char *src, int len, char *ret)
{
 int i, j, k;
 if ( len > 15 )
 {
 for ( i = 0; i < len; ++i )
 ret[i] = src[i];
 for ( j = len - 16; j >= 0; --j )
 tea_decrypt(key, (unsigned __int64 *)&ret[j]);
 }
 else
 {
 for ( k = 0; k < len; ++k )
 ret[k] = key[k + 32] ^ src[k];
 }
}
from pwn import *
from Crypto.Util.number import *

n = unpack(bytes.fromhex('5fcef0e867349fc68f40763a6b0bde01'), 128)
e = unpack(bytes.fromhex('01000100000000000000000000000000'), 128)
print(f'n = {n}, n_hex = {hex(n)}')
print(f'e = {e}, e_hex = {hex(e)}')

p = 1152921504606848051
assert(isPrime(p))
q = 2152921504606847269
assert(isPrime(q))
assert(p * q == n)

phi = inverse(e, (p - 1) * (q - 1))
print(f'phi = {phi}')

buf60h = bytes.fromhex('7a3202cc78acb66216341041b18ea201a3eb93301b27a2b6e77cb244d2e02c0082cd6369f3a7c1d2a1dd9b561c98510017c911f2ac5ec565e2d9b9016df34900661212d889172b99954d25018b5d43012e81783c2d8cebedeb053ccd651de400')
buf48h = b''
for i in range(6):
 number = unpack(buf60h[i*16 : (i+1)*16], 128)
 number = pow(number, phi, n)
 buf48h += pack(number, 64, endianness='big')
 print(f'numbers[{i}] = {hex(number)}')
print(f'buf48h = {buf48h}')
assert(len(buf48h) == 48)

msg = bytes.fromhex('16cb56c17a19fb2ddcdb8472d52d1d6b1693164a13316a33be05bc1c4a2029b9efbf96dc917da5056d3ee46c2b0815cb56c17b19fb2de6db847211fd382bc3eb739037f7dfa4b0ca553f4dc67f81b71b7f9215cb56c17819fb2dd6db84727c8526cc3d6383bbcf0159590648586e7dd08b49cc1ee7f519ec206592254842b7f33d25646640ab16cb56c17a19fb2de5db8472c008ba6c15334f76485d8c17082f4468addbb3a62d20e754105d1014cb56c17a19fb2dfedb847215cb56c17219fb2dbdd984723419b3ea63306ff1224173d834b1f9c436332f39ec2aa102bb7747859d50793674b05a56f14ee29491895944cbf1f6846a9831f8dd5666202c4b0d558a690239b1dece4322fe535c0742cc2f37378577b999eaab713d853643bc379dac7f7f471ef2240b8898fac4431149aa27a65507db39a9111dea802a803506fbd4a2d558068974f993dcab4587a5620db6909a951dcf8bb65d4f8e92ac8300fd049bb3218199705babb255e7daef40a28c1d7e3f74cb1d44687be127258aafc4dbdaf09266daa68605e250aa244c179d759d22e90ed3d8a9bf155fae86c721ed8ee5603c4613ac47e5a80079b909727277fff31d20529b3c022e3b1a3616d639ca036586ef17d3dc9bdf1eeec5859f0022514f29b240f30c818e7fdd478f36779978c08885b2266e3cf599d0a4c27bca4615720a08e13916ec4a6ef5c943ddb25566e620726f56c5160913564d683badcc7204ec8e7080221de325a431a0680e9e108e427c7bc3807b86c78820bc9c2340709da352d953aea805a04b53f2d88f7b8fae50e5ba2de55615bc9b2e526167226e75f5c8827593281f23a65e5098e0e8e2623ee4f892bac76e6987a05832bc0b84215bb74ed83786bd55265e61ba5702170fda63e01a44d6b8a6f1740a6c03803095e5176bde18ee873dcd6380de9f325f1c436c11e3250cebceceb319a49a4e3f2f62cfd137b602e27f3974a113df414287da48afd9e8c7ef0bdb4d345313b52d662202f543f426f8271432a20186b1dc7f70d4123def1c3745c1ffe7f4017ff60e0b7486f0e8db90889a36072583ddb26dbd37778115cb56c17e19fb2d5edb847263424fb4921f224eb2d445183f9bc6541d1ac77072a6e616e6826cbbebe96af229e79620462869e51686d4d523f782b2e5b43a769403bf62f1b87512013f95d068dc04beb337f8741b471386a7746ebc7b9c7a9568ed9b590936cdc533f6f943e3a37966362b62092ce5a3c53a95b33d0ff1ac2c5800b67b8cc40d614b8df74d4114d4bb7104b545ac7d0b9eb606578fd63561578740ce7eeaa189baacd436ae15cb56c17f19fb2d5edb8472ecc4942bbc4e2bbec5c4adb791a7096298f6347c4a277364cea894234bdcf69811f31ce644bae10edc0de4ccc200a44fa0e2faa4d2eb3b28dcecc3a468efdbfa7de2728b27dfafd1a5df4803a7986cfa768fb1f9751ba1a7d47c9a6928978810d76dceb819738f4684637d3ddd2cc41e2a4585a366d4a46b32db59508f34bf5c654be7b5c86e24cca5d1013738c32ba9b6083e76e0f93c80fe712261841e546315cb56c17c19fb2d5edb847260fd338fdcecb096e26a56603082a58f5b1fb0ffb7fc8faac33589ec52ed02256aba88b2c2836433a5d146c6efe784d47da7a7ffc4256f3dce73314c0171f89e9a4f6a95f59e8460d2b65fe178daba5faf8d34d99e32a50aefbbb7ed9c9507765958870dd2e1836fe608215ca753a7125f3cb86ac32d1149cf2a144b873fc7a96914d376ed2fe88d36a609596a68d8bb76e71d1b81a8db3618271f002ff6fb5815cb56c17d19fb2d5edb8472b72d657abc1a3c2133fa45fd834d28fce3b5bdd8f111bfa61386a306aa74598ea6e5022f4aac8d9acd442c44465eb334c26d060dfc8f4f59c13f3225a5ea111f9e3e9ef4c75f40b85c43dbdd5d30970cde507cd96fa6a88970e23c1dc1cb9a1eab2f4cc16444226aff6c49dd13e030240ea32267a1699b5b8c83d05c1cc257f5028d649e2b58d96a1f59fcd42f027179e7400f2c64c3063ae1f9c496ec019eba12cb56c17219fa2dfedb847213cb56c17919fb2dfedb847211cb56c17a19fb2dfedb8472')
tea_key = [
 unpack(buf48h[i*8 : (i+1)*8], 64)
 for i in range(4)
]
xor_key = buf48h[32:48]
for i in range(4):
 print(f'tea_key[i] = {tea_key[i]}, hex_tea_key[i] = {hex(tea_key[i])}')
print(f'xor_key = {xor_key}')

def tea_decrypt(d):
 v0 = unpack(d[0:8], 64)
 v1 = unpack(d[8:16], 64)
 s = 0x13c6ef3720
 LIMIT = 0xffff_ffff_ffff_ffff
 for i in range(32):
 tmp = ((v0 + s) ^ ((v0 << 4) + tea_key[2]) ^ ((v0 >> 5) + tea_key[3])) & LIMIT
 v1 = (v1 - tmp) & LIMIT
 tmp = ((v1 + s) ^ ((v1 << 4) + tea_key[0]) ^ ((v1 >> 5) + tea_key[1])) & LIMIT
 v0 = (v0 - tmp) & LIMIT
 s = (s - 0x9e3779b9) & LIMIT
 return pack(v0, 64) + pack(v1, 64)

def decrypt(m):
 l = len(m)
 if l > 15:
 b = bytearray(m)
 for i in range(l-16, -1, -1):
 b[i:(i+16)] = tea_decrypt(b[i:(i+16)])
 return bytes(b)
 else:
 return bytes(m[i] ^ xor_key[i] for i in range(len(m)))

buf = bytearray(400 * 10)
idx = 0

while True:
 instr = decrypt(msg[idx:
idx+12])
 idx += 12
 a0 = unpack(instr[0:4], 32)
 a1 = unpack(instr[4:8], 32)
 a2 = unpack(instr[8:12], 32)
 if a0 == 1:
 print(decrypt(msg[idx:
idx+a2]))
 idx += a2
 elif a0 == 2:
 data = decrypt(msg[idx:
idx+a2])
 idx += a2
 buf[400*a1:
400*a1+a2] = data
 print(f'stored data at segment {a1}')
 elif a0 == 3:
 print(f'input data at segment {a1}')
 elif a0 == 4:
 print(f'show data at segment {a1}')
 elif a0 == 5:
 print(f'execute data at segment {a1 & 0xffff}')
 else:
 print('ended')
 break

with open('program', 'wb') as f:
 f.write(buf)
from ida_bytes import get_bytes
from struct import *

seg4 = get_bytes(400 * 4, 160)
seg5 = get_bytes(400 * 5, 160)
seg6 = get_bytes(400 * 6, 160)
seg7 = get_bytes(400 * 7, 160)

flag = ''
buf = bytearray(160)
for i in range(0, 160, 4):
 buf[i:i+2] = seg7[i:i+2]
 buf[i+2:i+4] = seg6[i:i+2]
 p = unpack('<I', buf[i:i+4])[0]
 q = unpack('<I', seg5[i:i+4])[0]
 r = unpack('<I', seg4[i:i+4])[0]
 buf[i:i+4] = pack('<I', ((p - q) & 0xffff_ffff) ^ r)
 flag += chr(buf[i])

print(flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/3-1694259507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/10-1694259507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/6-1694259507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/9-1694259508.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694259509.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1694259509.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1694259509.gif)