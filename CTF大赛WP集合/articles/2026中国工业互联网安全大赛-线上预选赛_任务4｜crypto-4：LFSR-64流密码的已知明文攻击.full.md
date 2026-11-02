---
title: '任务4｜crypto-4：LFSR-64流密码的已知明文攻击'
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
- '), int(prof['
- 'mix ='
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{N4rr0wb4nd_LFSR_St4t3_26}'
subcategory_guess: "archive"
---

任务4｜crypto-4：LFSR-64流密码的已知明文攻击
附件
：任务4.zip（crypto-4.zip内的radio_capture.log、radio_policy.json）
1. 基本情况
radio_capture.log为36帧，每行含时间戳、通道、方向、ctr、长度与载荷；radio_policy.json登记算法档NRWF-RADIO-V2的poly、output_mask、state_mix与state_init，以及三通道的ctr_salt、status和下行通道CH9。算法为64位LFSR逐位生成密钥流。目标是恢复status=current通道的密钥并解出flag。
2. 关键突破
反馈位为parity(state&poly)，输出位为parity(state&output_mask)，state_mix是rol64，均为GF(2)线性映射；只有state_init的raw=key⊕((ctr_salt·ctr)mod2^64)带异或常数。链路因此仿射：密钥流=Φ(rol64(key⊕(ctr_salt·ctr),13))，Φ与帧无关。
每帧前8字节恒为A5 5A、通道号与NRWF-，即64位已知密钥流，组成64阶线性方程组；求出Φ⁻¹后一次矩阵向量乘即可定出密钥，不必搜索2^64空间。参数poly=0xd80000000000001b、output_mask=0x8020000000000001、rol=13。
CH2两帧ctr同为0x0014，前13字节一致、自偏移13起分叉：初始状态相同则密钥流相同，异或后只剩明文差异（WTG09/V=08.0/P=1205与WTG07/V=05.7/P=0790）。可见ctr明文携带并直接参与派生，回收即密钥流复用。CH9以A5 5A 00开头、紧跟可读ASCII，为plaintext通道，不含flag。
3. 利用/还原思路
从台账取current档poly、output_mask与rol位数，并读ctr_salt、status。
位发生器每步先取parity(state&output_mask)输出，再算反馈、右移、反馈位置第63位；64位按lsb-first打包。
令state=rol64(1<<i,13)，i=0…63，各取64位得Φ的64个列向量，转置成行。
取一帧，前8字节密文异或明文头得观测密钥流，再异或常数Φ(rol64(ctr_salt·ctr,13))，解64阶方程组得候选密钥。
其余帧回代明文头全中才采纳；整帧异或密钥流得明文，偏移8为类型0x10，偏移9起为遥测或flag。
只采纳status=current的CH1；CH2、CH3分别为rotated、revoked。
4. 复现脚本
import
json, re
pol = json.load(open(
"radio_policy.json"
, encoding=
"utf-8"
))
prof = next(p
for
p
in
pol[
"crypto_profiles"
]
if
p[
"status"
] ==
"current"
)
POLY, OMASK = int(prof[
"poly"
],
16
), int(prof[
"output_mask"
],
16
)
ROT = int(re.search(
r"rol64\x5c(raw,\x5cs*(\x5cd+)\x5c)"
, prof[
"state_mix"
]).group(
1
))
par =
lambda
v: bin(v).count(
"1"
) &
1
mix =
lambda
r: ((r << ROT) | (r >> (
64
- ROT))) &
0xFFFFFFFFFFFFFFFF
def
bits
(s)
:
while
1
:
yield
par(s & OMASK)
s = (s >>
1
) | (par(s & POLY) <<
63
)
word =
lambda
s: sum(b << i
for
i, b
in
zip(range(
64
), bits(s)))
rows = [sum(((word(mix(
1
<< i)) >> j) &
1
) << i
for
i
in
range(
64
))
for
j
in
range(
64
)]
pool = [{
"ctr"
: int(x[
3
][
4
:],
16
),
"b"
: bytes.fromhex(x[
5
])}
for
x
in
map(str.split, open(
"radio_capture.log"
, encoding=
"utf-8"
))
if
len(x) ==
6
and
x[
1
] ==
"CH1"
and
x[
2
] ==
"UL"
]
salt = int(next(c[
"ctr_salt"
]
for
c
in
pol[
"channels"
]
if
c[
"ch_id"
] ==
1
),
16
)
hdr = bytes([
0xA5
,
0x5A
,
1
]) +
b"NRWF-"
ks =
lambda
f: sum((f[
"b"
][i] ^ hdr[i]) << (
8
* i)
for
i
in
range(
8
))
rhs = ks(pool[
0
]) ^ word(mix((salt * pool[
0
][
"ctr"
]) &
0xFFFFFFFFFFFFFFFF
))
aug = [rows[i] | (((rhs >> i) &
1
) <<
64
)
for
i
in
range(
64
)]
for
c
in
range(
64
):
r = next(r
for
r
in
range(c,
64
)
if
aug[r] >> c &
1
)
aug[c], aug[r] = aug[r], aug[c]
aug = [a ^ aug[c]
if
k != c
and
a >> c &
1
else
a
for
k, a
in
enumerate(aug)]
key = sum(((aug[i] >>
64
) &
1
) << i
for
i
in
range(
64
))
assert
all(word(mix(key ^ ((salt * f[
"ctr"
]) &
0xFFFFFFFFFFFFFFFF
))) == ks(f)
for
f
in
pool)
for
f
in
pool:
g = bits(mix(key ^ ((salt * f[
"ctr"
]) &
0xFFFFFFFFFFFFFFFF
)))
pt = bytes(c ^ sum(next(g) << j
for
j
in
range(
8
))
for
c
in
f[
"b"
])
if
b"flag{"
in
pt:
print(
"key=%
#018x
"
% key, pt[
9
:].decode(
"latin1"
).rstrip())
5. 运行结果
key=0x6b1f4a9c2d8e7305 flag{N4rr0wb4nd_LFSR_St4t3_26}
flag{N4rr0wb4nd_LFSR_St4t3_26}
6. 小结
线性密钥流叠加固定明文头等于泄露密钥；64位LFSR状态偏短，ctr更不得复用。
最终flag
flag{N4rr0wb4nd_LFSR_St4t3_26}
