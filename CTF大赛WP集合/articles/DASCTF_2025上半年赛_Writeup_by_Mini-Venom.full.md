---
title: DASCTF 2025 上半年赛 Writeup by Mini-Venom
contest: DASCTF
year: 2025
difficulty: medium
vuln_type: misc_math
tags:
- obex
- bluetooth
- lsb-stego
- openssl
- rsa-key-recover
- sm4
- sm2
- xianyu-fs
attack_chain:
- 'BlueTrace: tshark 提 OBEX 图片'
- 像素 hex 拼接
- 'Webshell Plus: 提 RSA p,q 复私钥'
- openssl_decrypt AES-128
- TCP 流找 /etc/shadow
- hashcat 爆破 root 密码
- 'Excessive Security: ECDSA r 复用恢复 sk'
- 多项式 GCD 攻击
- 'xianyu_decrypt: SM4 解密'
key_payload: OBEX 流量 + RSA 私钥恢复 + ECDSA nonce 复用
one_liner: DASCTF 2025 上半年赛 Mini-Venom 战队 WP，OBEX/RSA 复私钥/ECDSA 复用/SM4 文件系统解密。
lesson: 蓝牙 OBEX 协议 tshark `-Y obex.header.value.byte_sequence` 抓图片；RSA 私钥只要 p,q 可直接 cryptography 重构。
quality: high
full_path: DASCTF_2025上半年赛_Writeup_by_Mini-Venom.full.md
meta_path: DASCTF_2025上半年赛_Writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'DASCTF 2025 上半年赛 Writeup by Mini-Venom。DASCTF 2025 上半年赛 Mini-Venom 战队 WP，OBEX/RSA 复私钥/ECDSA 复用/SM4 文件系统解密。。关键路径：BlueTrace: tshark 提 OBEX 图片 → 像素 hex 拼接 → Webshell Plus: 提 RSA p,q 复私钥。经验：蓝牙 OBEX 协议 ...'
category: crypto
subcategory: math
tools_used:
- hashcat
- tshark
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/258051.html
wp_author: Mini-Venom
reasoning_chain:
- BlueTrace：题目说文件被传入 PC → 触发点：蓝牙 OBEX 协议传图片
- 动作：tshark -r BlueTrace.pcapng -Y obex.header.value.byte_sequence -T fields -e obex.header.value.byte_sequence > 1.txt → 观察：抓到图片
- 假设：图像 RGB 通道全部相同 → 用 PIL 提取 r_list 像素 → hex 拼接 → DASCTF{...} flag
- Webshell Plus：流量是冰蝎 + openssl → 触发点：公开密钥可逆推 RSA 私钥
- 动作：从流量提 public key → 分解 n → 用 cryptography 重构 RSA private key → openssl_decrypt AES-128
- TCP 流找 /etc/shadow → hashcat 爆破 root 密码 → Excessive Security：ECDSA r 复用 → 多项式 GCD 攻击 → 恢复 sk
- xianyu_decrypt：SM4 解密文件系统 → 假设：鱼皮加密文件 + SM4 key 派生 → 还原 flag
failed_attempts:
- 试图不解 OBEX 流量直接搜图片字节 → 失败：图片被 OBEX 协议封装在 byte_sequence 字段
- 试图不解 RSA 私钥直接读密文 → 失败：必须先 p,q factor n
- 试图手工解 SM4 → 失败：SM4 复杂度比 AES 高，必须用 gmssl 库
key_observations:
- 蓝牙 OBEX 协议 tshark `-Y obex.header.value.byte_sequence` 抓图片是标准手法
- RSA 私钥只要 p,q 可直接 cryptography.hazmat.primitives.asymmetric.rsa 重构
- ECDSA nonce 复用 + 多项式 GCD 攻击可恢复 sk（r 重复则 k 重复）
- 冰蝎 webshell 用 openssl 加密时密钥派生逻辑在 server.php 但私钥可逆推
- RGB 通道全部相同的 PNG 可能藏文本，提取单通道拼十六进制
prerequisites:
- tshark OBEX 协议过滤（obex.header.value.byte_sequence）
- PIL 图像处理（PIL.Image.open/getpixel）
- cryptography.hazmat RSA private key 重构
- ECDSA 签名 + nonce 复用攻击
- SM4 国密算法（gmssl 库）
- hashcat 密码爆破
---
# DASCTF 2025上半年赛 Writeup by Mini-Venom

> 原文: https://www.ctfiot.com/258051.html
> ID: 258051

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

MISC

BlueTrace

题目说文件被传入PC中，去找找文件在哪，发现OBEX有图片行为

tshark提取

tshark -r BlueTrace.pcapng -Y obex.header.value.byte_sequence -T fields -e obex.header.value.byte_sequence > 1.txt

PC名称：INFERNITYのPC
fig:

得到个照片
fig:

分析颜色通道（RGB）值，发现都一样，那就提取，发现是隐藏了文本

from PIL import Image  

def check_rgb_uniformity(image_path):
img = Image.open(image_path).convert("RGB")  
width, height = img.size  
pixels = img.load()  

inconsistent_pixels = []  
r_list = []  
for y in range(height):  
for x in range(width):  
r, g, b = pixels[x, y]  
# print(f'{r}, {g}, {b}')  
# print(chr(r), end='')  
r_list.append(r)  
# if r != g or g != b:  
# inconsistent_pixels.append(((x, y), (r, g, b)))  

ifnot inconsistent_pixels:  
print(''.join(hex(r)[2:] for r in r_list))  
else:  
print(f"❌ 有 {len(inconsistent_pixels)} 个像素通道不一致，示例：")  

check_rgb_uniformity("flag.png")

fig:

DASCTF{0ba687ee-60e0-4697-8f4c-42e9b81d2dc6}

Webshell Plus

是冰蝎的流量，但是用了openssl
fig:
fig:

分析上面的马，我们需要去得到这当中的$p，才能得到后续交互的key
fig:

目前有的条件是有public key，但是解密需要私钥，我们可以去解这个公钥

提取n和e
fig:

分解
fig:

然后去构造private key

from Crypto.Util.number import inverse  
from cryptography.hazmat.primitives.asymmetric import rsa  
from cryptography.hazmat.primitives import serialization  

p = 7867691643586180987785626545986251727789183377275546449400690071916592141728452581896381132002349573632855071606614201168751151435679435299890592299985167
q = 7867691643586180987785626545986251727789183377275546449400690071916592141728452581896381132002349573632855071606614201168751151435679435299890592299985539
phi = (p - 1) * (q - 1)  
n = p * q  
e = 65537
d = inverse(e, phi)  
d_p = d % (p - 1)  
d_q = d % (q - 1)  
q_inv = pow(q, -1, p)  

private_key = rsa.RSAPrivateNumbers(  
p=p,  
q=q,  
d=d,  
dmp1=d_p,  
dmq1=d_q,  
iqmp=q_inv,  
public_numbers=rsa.RSAPublicNumbers(e, n)  
).private_key()  

pem = private_key.private_bytes(  
encoding=serialization.Encoding.PEM,  
format=serialization.PrivateFormat.PKCS8,  
encryption_algorithm=serialization.NoEncryption()  
)  
print(pem.decode())

然后后续解内容就行，发现其中TCP 32流中有/etc/shadow的结果，要的是root密码的md5，那就再去爆hashcat

<?php  
$key = 'd14d8ce94563e71a';  
$data = '  
myzZoRJB9iFwgtIPC0fDUeFaS+fdv0LH3s0SKFXJkWe+V0zA2TRsTsfK65Dn7HMfUZaD+teWivQy
Ajt320oY70by3v22VYG+fe9m+wVYkpscpuhYFu5u10Gk+/seD+6Swj65YvXjSJVI7fAC7wuUXCJE
Io5CkJyC78gv7bCBn3Xd2TKaHp8grtoz+a9geiFFyhPYpjo1G8KFXE4zkzesi/vA5C9TF55yANHI
LKvybGhwNnDqBA/EK1eB9oF99hwoH/JF0g/mXYCh+8pl6UtnXMWJibavqk+vW3daw2irj4BxUp5D
hiBfialxH2TkYD+PWCawQRPyySSxY/5dsQplP0uuMDuijkM7A5VRK8tzs/XV14Norr1RWEshvfBu
kQphvX1MZMXUTCf5Roqo9M6Sls2L5gK6z8rrnmSVNIOf8RzmAFnHOOtzbyO8wr/Fc5asNizVcPrC
L9Ul3EUVy+h4p3ow2cQfaLHfs0RVs5KSJdVwHrJcgH8gdv6bUeOXkDkiboauyFdgQTbYQYCZ6pGl
iiwbsgmU6M9QVGcXa27BxMPLZivnrIynGGVQT+b6HnOZT/jPgyz7TbzQDJH0YNynjdHFAgFkdngp
h75uql2jlggVzr9/IKsAgCPZL1SK8ZdZfryMN89/mn1nq/0E1eWzKwZSym/qeCckqpFLcBUsDNpf
bVkXdqyYZ5G1AYaAIp8OoUe+cEhoFnvay4/gVsn4Ol6qocOkwQ4pfv1dVWosaB2X8duzW7xTuZmU
rfRLwW+ybsW3pvc/1TmlJYKLKTxWFUeiEKxrscnWz2fkIbNjRwD6rDHbQXPLk/cnB0gq7EE4JTxk
ePqEJq+x5oR712jHqeMLeDtqtKiJX8NHZktaykEZlVTSu0ptknM1DDijOQtiQX5a6mpJgBSDIHxO
kVsG/ghCZ2DnGYQd5YM4TkQOzzn2IRczBKxG+pj3H2/tqoL3Dpbjwjh8+KGbPBvtxYE4isC2rv+i
J3OcfD/fA9u0QzZlVLAPot0HRkhQnjAprBSxC+nHMwv0oqX6/SsGoBsQjUeYQPsIbUEoXPQyfyiv
8jny08uEBgfY8nMcxMrEcM54BVVFCwY4b7TfOM5dFd90bHNmStc051bJsXal/0q6Q7VI8vaUUvbn
vZ+Z/2uOzHTa
';  
$json = openssl_decrypt($data, "AES128", $key);  
print openssl_error_string();  
$data = json_decode($json, true);  
$status = base64_decode($data['status']);  
$msg = base64_decode($data['msg']);  
echo 'status:'.$status.'  
msg:'.$msg;

然后md5

DASCTF{f3d279e1b58a1e25c092b018f035d406}

CRYPTO

Excessive Security

有

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
tshark -r BlueTrace.pcapng -Y obex.header.value.byte_sequence -T fields -e obex.header.value.byte_sequence > 1.txt
from PIL import Image  

def check_rgb_uniformity(image_path):
img = Image.open(image_path).convert("RGB")  
width, height = img.size  
pixels = img.load()  

inconsistent_pixels = []  
r_list = []  
for y in range(height):  
for x in range(width):  
r, g, b = pixels[x, y]  
# print(f'{r}, {g}, {b}')  
# print(chr(r), end='')  
r_list.append(r)  
# if r != g or g != b:  
# inconsistent_pixels.append(((x, y), (r, g, b)))  

ifnot inconsistent_pixels:  
print(''.join(hex(r)[2:] for r in r_list))  
else:  
print(f"❌ 有 {len(inconsistent_pixels)} 个像素通道不一致，示例：")  

check_rgb_uniformity("flag.png")
from Crypto.Util.number import inverse  
from cryptography.hazmat.primitives.asymmetric import rsa  
from cryptography.hazmat.primitives import serialization  

p = 7867691643586180987785626545986251727789183377275546449400690071916592141728452581896381132002349573632855071606614201168751151435679435299890592299985167
q = 7867691643586180987785626545986251727789183377275546449400690071916592141728452581896381132002349573632855071606614201168751151435679435299890592299985539
phi = (p - 1) * (q - 1)  
n = p * q  
e = 65537
d = inverse(e, phi)  
d_p = d % (p - 1)  
d_q = d % (q - 1)  
q_inv = pow(q, -1, p)  

private_key = rsa.RSAPrivateNumbers(  
p=p,  
q=q,  
d=d,  
dmp1=d_p,  
dmq1=d_q,  
iqmp=q_inv,  
public_numbers=rsa.RSAPublicNumbers(e, n)  
).private_key()  

pem = private_key.private_bytes(  
encoding=serialization.Encoding.PEM,  
format=serialization.PrivateFormat.PKCS8,  
encryption_algorithm=serialization.NoEncryption()  
)  
print(pem.decode())
<?php  
$key = 'd14d8ce94563e71a';  
$data = '  
myzZoRJB9iFwgtIPC0fDUeFaS+fdv0LH3s0SKFXJkWe+V0zA2TRsTsfK65Dn7HMfUZaD+teWivQy
Ajt320oY70by3v22VYG+fe9m+wVYkpscpuhYFu5u10Gk+/seD+6Swj65YvXjSJVI7fAC7wuUXCJE
Io5CkJyC78gv7bCBn3Xd2TKaHp8grtoz+a9geiFFyhPYpjo1G8KFXE4zkzesi/vA5C9TF55yANHI
LKvybGhwNnDqBA/EK1eB9oF99hwoH/JF0g/mXYCh+8pl6UtnXMWJibavqk+vW3daw2irj4BxUp5D
hiBfialxH2TkYD+PWCawQRPyySSxY/5dsQplP0uuMDuijkM7A5VRK8tzs/XV14Norr1RWEshvfBu
kQphvX1MZMXUTCf5Roqo9M6Sls2L5gK6z8rrnmSVNIOf8RzmAFnHOOtzbyO8wr/Fc5asNizVcPrC
L9Ul3EUVy+h4p3ow2cQfaLHfs0RVs5KSJdVwHrJcgH8gdv6bUeOXkDkiboauyFdgQTbYQYCZ6pGl
iiwbsgmU6M9QVGcXa27BxMPLZivnrIynGGVQT+b6HnOZT/jPgyz7TbzQDJH0YNynjdHFAgFkdngp
h75uql2jlggVzr9/IKsAgCPZL1SK8ZdZfryMN89/mn1nq/0E1eWzKwZSym/qeCckqpFLcBUsDNpf
bVkXdqyYZ5G1AYaAIp8OoUe+cEhoFnvay4/gVsn4Ol6qocOkwQ4pfv1dVWosaB2X8duzW7xTuZmU
rfRLwW+ybsW3pvc/1TmlJYKLKTxWFUeiEKxrscnWz2fkIbNjRwD6rDHbQXPLk/cnB0gq7EE4JTxk
ePqEJq+x5oR712jHqeMLeDtqtKiJX8NHZktaykEZlVTSu0ptknM1DDijOQtiQX5a6mpJgBSDIHxO
kVsG/ghCZ2DnGYQd5YM4TkQOzzn2IRczBKxG+pj3H2/tqoL3Dpbjwjh8+KGbPBvtxYE4isC2rv+i
J3OcfD/fA9u0QzZlVLAPot0HRkhQnjAprBSxC+nHMwv0oqX6/SsGoBsQjUeYQPsIbUEoXPQyfyiv
8jny08uEBgfY8nMcxMrEcM54BVVFCwY4b7TfOM5dFd90bHNmStc051bJsXal/0q6Q7VI8vaUUvbn
vZ+Z/2uOzHTa
';  
$json = openssl_decrypt($data, "AES128", $key);  
print openssl_error_string();  
$data = json_decode($json, true);  
$status = base64_decode($data['status']);  
$msg = base64_decode($data['msg']);  
echo 'status:'.$status.'  
msg:'.$msg;
from hashlib import sha256  
from random import randint  
from Crypto.Util.number import inverse, bytes_to_long, getPrime,long_to_bytes  
N = 98472559301398326519521704898800552100670435952553618641467704945731627783624140484670366845550939866842528582954361836035593755351584272693016822204234859506655433796327589389300744153263194916217158205372375670404000164793308078231134726345672236542974067442646354084915978240909130405000905936105602786257
c1 = 40127670364311180283394426274113033719543797673129006844648567069726278369353910517424074073714346881895826377902772771837790964432434997986229629267700081564740160692151350365553131535789070670584548053624970689607275665921674708650254889369926426966093575171344082441699295255661725211366819524902641461331
c2 = 4958767685161688254408001463637498631434015989118088175006720150146904021732816429444998309662995333252926794359370922113211567042198257249974382506057347524044728912256607992806670035884054654064021329936092742390064660715742236775795950389452053770118911570676738879382827738088237377423216124023239179385
(h1, s1, r1) = (68926494835039378729440404424793589316085902585443402029912033361291851069895, 70264613994433317101824708333691569351293428290775945022557096997867421112623, 95467825458659408375936425122753380788640181504557006906236884175684680903422)  
(h2, s2, r1) = (99816429822339421445908151468618514820067970997726274244928092260385418279182, 27386247988345867998752358066350183725137348277248603318763377237810993039608, 95467825458659408375936425122753380788640181504557006906236884175684680903422)  
(h3, s3, r2) = (100471089356874379799029324099340355602511511524623953182021635156113287196537, 108271537842404710192407976239166854351892165018292127464175836717873395489565, 13940715298251935708383205669373172931583958487449924842542107474174521484127)  
(h4, s4, r2) = (53552261622392134420510144174810499568173979993026285111445672642139328877380, 100312693542625967610858608130705401648902828203826044299984002070083890684220, 13940715298251935708383205669373172931583958487449924842542107474174521484127)  
e = 65537

n1 = 115792089237316195423570985008687907852837564279074904382605163141518161494337

A1 = (r1 * s2) % n1  
B1 = (-r1 * s1) % n1  
C1 = (s1 * h2 - s2 * h1) % n1  

A2 = (r2 * s4) % n1  
B2 = (-r2 * s3) % n1  
C2 = (s3 * h4 - s4 * h3) % n1  

D1 = (A1 * B2 - A2 * B1) % n1  
D1_inv = inverse_mod(D1, n1)  

D2 = (A2 * B1 - A1 * B2) % n1  
D2_inv = inverse_mod(D2, n1)  

x1 = (C1 * B2 - C2 * B1) * D1_inv % n1  
x2 = (A2 * C1 - A1 * C2) * D2_inv % n1  

def attack(c1, c2, a, b, e, n):
PR.<x>=PolynomialRing(Zmod(n))  
g1 = x^e - c1  
g2 = (a*x + b)^e - c2  

def gcd(g1, g2):
while g2:  
g1, g2 = g2, g1 % g2  
return g1.monic()  
print(gcd(g1, g2))  
return -gcd(g1, g2)[0]  

m1 = attack(c1, c2, x1, x2, e, N)  
flag = long_to_bytes(int(m1))  
print(flag)  

    #x + 98472559301398326519521704898800552100670435952553618641467704945731627783624140484670366845550939866842528582954361836035593755351584206749343906691680123993276208473999116876963410717148891366887303511134680635736354894959778972988838486751320350521474270271621998445045296093543008556372250828549972964948
NAME  
xianyu_decrypt  

FUNCTIONS  
decrypt_aes_ecb(enc_data: 'bytes', key: 'bytes') -> 'bytes'
decrypt_aes_ecb(bytes enc_data: bytes, bytes key: bytes) -> bytes  

load_and_decrypt_xianyu(xianyu_path: 'str') -> 'dict'
load_and_decrypt_xianyu(unicode xianyu_path: str) -> dict  

read_part1(data, offset)  
read_part1(data, offset)  

read_part2(data, offset)  
read_part2(data, offset)  

read_part3(data, offset)  
read_part3(data, offset)  

read_part4(data, offset, file_key, meta_length)  
read_part4(data, offset, file_key, meta_length)  

read_part5(data, offset, file_key)  
read_part5(data, offset, file_key)  

unpad(data: 'bytes') -> 'bytes'
unpad(bytes data: bytes) -> bytes  

DATA  
MASTER_KEY = b'XianYuAESKey0000'
XIANYU_HEADER = b'XIANYUFS'
__test__ = {}
import os  
import sys  
import json  
from xianyu_decrypt import (  
load_and_decrypt_xianyu,  
XIANYU_HEADER  
)  

def decrypt_auto(filepath, output_dir):
os.makedirs(output_dir, exist_ok=True)  
result = load_and_decrypt_xianyu(filepath)  

if isinstance(result, dict):  
for key, value in result.items():  
output_path = os.path.join(output_dir, f"{key}.bin"if isinstance(value, bytes) elsef"{key}.json")  
with open(output_path, 'wb'if isinstance(value, bytes) else'w') as f:  
f.write(value) if isinstance(value, bytes) else json.dump(value, f, indent=2)  
else:  
output_path = os.path.join(output_dir, "decrypted.bin")  
with open(output_path, 'wb') as f:  
f.write(result)  
return result  

if __name__ == "__main__":  
input_file = sys.argv[1]  
output_dir = sys.argv[2] if len(sys.argv) > 2else os.path.splitext(input_file)[0] + "_decrypted"
print(f"Decrypting {input_file} to {output_dir}...")  
decrypt_auto(input_file, output_dir)  
print("Decryption completed")
{  
"name": "u8004u800bAu68a6",  
"artist": "u5706u5934ud83dudc31",  
"fl4g": "(=u2180u03c9u2180=)u54c8~uff01uff01uff01u6211u542cu8bf4u5c31u5728u97f3u4e50u7684u201cu4fe1u606fu6587u4ef6u201du91ccuff01uff01",  
"flag": "DASCTF{fl5h_mus1c_miao_m1a0_mlaO}"  
}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]