---
title: '任务3｜crypto-3：OTA许可封装的双缺陷与两条攻击路径'
contest: '2026中国工业互联网安全大赛-线上预选赛'
contest_normalized: '2026中国工业互联网安全大赛-线上预选赛'
contest_year: 2026
year: 2026
category: 'crypto'
subcategory: 'crypto_other'
tags: []
attack_chain:
- '基本情况'
- '关键突破'
- '利用/还原思路'
- '复现脚本'
- '), int(k['
- '< g < n1)'
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{Sh4r3d_Pr1m3_0v3r_0TA_26}'
---

任务3｜crypto-3：OTA许可封装的双缺陷与两条攻击路径
附件
：任务3.zip（crtpto-3.zip内的firmware_manifest.json、sealed_blobs.json）
1. 基本情况
附件含firmware_manifest.json（站内RSA密钥台账）与sealed_blobs.json（退役样机OTA客户端缓存导出的9条封装记录）。台账描述PRT-3000保护测控装置的三批固件包：FW-2026Q3-A为在役批次（current，PUB-A1/A2/A3），FW-2026Q2-B因e=3且无填充被吊销（revoked），FW-2026Q1-Z为历史归档（superseded，仅PUB-Z1），另有研发测试台密钥PUB-C1（status=test）。封装方案为raw RSA，签名与许可载荷复用同一批密钥，每条记录是raw RSA输出的大端整数。目标是恢复在役批次的许可载荷flag。
2. 关键突破
把台账所有模数两两求gcd，命中三对：PUB-A1与PUB-B1、PUB-A1与PUB-Z1、PUB-B1与PUB-Z1，公共因子是512位素数。也就是说A1、B1、Z1跨批次、跨产线烧录站复用了同一p；PUB-A1的n为1023位，可直接分解为两个512位因子。
A批次自身还有第二类缺陷：PUB-A1/A2/A3的指数均为e=3，记录1至3承载同一许可载荷，且三个模数两两互素。用中国剩余定理合并三条同余式后模数M约3070位；因明文很短，合并结果就是m³本身，取整数三次根即还原。
台账把e=3无填充写在B批次的吊销理由里，但A批次同样如此，还叠加共享素因子，形成两条独立可解路径，可互相印证。
干扰项：记录9对应PUB-C1，e=3且密文远小于模数，直接开立方得NRWF-OTA-LIC/FW-TEST
#factory
-test-blob-v1，是诱饵；PUB-B4指数为65537，不参与广播且属已吊销批次，均与目标无关。
3. 利用/还原思路
解析两份JSON，建立key_id到(n,e)、批次到密钥列表、key_id到sealed整数的映射。
定位FW-2026Q3-A，取其密钥列表[PUB-A1,PUB-A2,PUB-A3]。
路径一：对n(A1)与台账全部n求gcd，命中PUB-B1得512位p；令q=n//p，φ=(p−1)(q−1)，d=3⁻¹modφ，m=cᵈmodn。
路径二：确认三把e均为3、三模数两两互素；用CRT合并cᵢ≡m³(modnᵢ)，M=n₁n₂n₃约3070位。
因m³<M，对合并值取整数三次根，并校验root³等于合并值。
两条路径载荷逐字节一致；再对记录9开立方确认诱饵，最后正则提取flag。
4. 复现脚本
import
json, re
from
math
import
gcd, prod
from
Crypto.Util.number
import
inverse
man = json.load(open(
"firmware_manifest.json"
, encoding=
"utf-8"
))
keys = {k[
"key_id"
]: (int(k[
"n"
],
16
), int(k[
"e"
]))
for
k
in
man[
"public_keys"
]}
sealed = {r[
"key_id"
]: int(r[
"sealed"
],
16
)
for
r
in
json.load(open(
"sealed_blobs.json"
, encoding=
"utf-8"
))[
"records"
]}
a = [b
for
b
in
man[
"batches"
]
if
b[
"batch_id"
] ==
"FW-2026Q3-A"
][
0
][
"key_ids"
]
n1, e1 = keys[a[
0
]]
p = next(g
for
k, (n, _)
in
keys.items()
if
k != a[
0
]
for
g
in
[gcd(n1, n)]
if
1
< g < n1)
v1 = pow(sealed[a[
0
]], inverse(e1, (p -
1
) * (n1 // p -
1
)), n1)
M = prod(keys[k][
0
]
for
k
in
a)
acc = sum(sealed[k] * (M // keys[k][
0
]) * inverse(M // keys[k][
0
], keys[k][
0
])
for
k
in
a) % M
def
iroot
(v, k)
:
if
v <
2
:
return
v
x =
1
<< ((v.bit_length() + k -
1
) // k)
while
True
:
y = ((k -
1
) * x + v // x ** (k -
1
)) // k
if
y >= x:
break
x = y
while
x ** k > v: x -=
1
while
(x +
1
) ** k <= v: x +=
1
return
x
v2 = iroot(acc,
3
)
assert
v1 == v2
m = v1.to_bytes((v1.bit_length() +
7
) //
8
,
"big"
)
print(m.decode())
print(re.search(r
b"flag\x5c{[^}]*\x5c}"
, m).group().decode())
5. 运行结果
path1: gcd(n[A1], n[PUB-B1]) = 512 bit prime
path2: CRT modulus = 3070 bit, e = 3
path1 payload: b'NRWF-OTA-LIC/FW-2026Q3-A
#flag
{Sh4r3d_Pr1m3_0v3r_0TA_26}'
path2 payload: b'NRWF-OTA-LIC/FW-2026Q3-A
#flag
{Sh4r3d_Pr1m3_0v3r_0TA_26}'
flag: flag{Sh4r3d_Pr1m3_0v3r_0TA_26}
6. 小结
共享素因子与e=3无填充叠加在同一批密钥上，两条路径互证；raw RSA必须改OAEP并逐把独立生成。
最终flag
flag{Sh4r3d_Pr1m3_0v3r_0TA_26}
