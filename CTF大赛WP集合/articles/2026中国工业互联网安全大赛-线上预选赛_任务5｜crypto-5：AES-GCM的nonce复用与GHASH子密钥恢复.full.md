---
title: '任务5｜crypto-5：AES-GCM的nonce复用与GHASH子密钥恢复'
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
- '份许可各用所属通道的H派生密钥，只采纳台账中current的ch1。'
- '复现脚本'
- ') ^ (R'
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{GCM_N0nc3_R3u53_1s_F0rb1dd3n_26}'
subcategory_guess: "symmetric"
---

任务5｜crypto-5：AES-GCM的nonce复用与GHASH子密钥恢复
附件
：任务5.zip（crypto-5.zip内的gcm_capture.json、sealed_license.json、telemetry_policy.json）
1. 基本情况
遥测上行链路以AES-128-GCM保护32字节定长帧，密钥128位、nonce12字节、标签16字节。台账telemetry_policy.json规定nonce由4字节大端frame_ctr与8字节大端dev_epoch拼接，AAD为16字节链路标识，明文以
NRWF-T2 SEQ=
开头。日志共24帧，分属ch1至ch3，另附三份封存许可，其中仅ch1为current。目标是从抓包与台账恢复当前通道的许可凭据。
2. 关键突破
三处nonce完全碰撞：ch1的seq5/7/9（frame_ctr=0x2A）、ch2的13/15/18（0x5C）、ch3的11/14/17（0x9A）；另有0x37出现在seq21/24，但dev_epoch不同，nonce未复用，属干扰项。同nonce各帧的CTR密钥流相同，密文异或只在偏移15、26、28三处非零，对应SEQ与温度数字。
标签满足tag=GHASH(H,AAD,C)⊕E_K(J0)，同nonce下E_K(J0)为同一常数，两帧相减即消去。本题帧结构为1块AAD、2块密文、1块长度，展开后AAD块与长度块也两两相同，只剩ΔC1·H^3⊕ΔC2·H^2⊕ΔT=0，H的一次项系数恒为0。同组三帧可取两条这样的差式，在GF(2^128)上做多项式辗转相除；两式共有根H，公因式为首一一次式x⊕H，其常数项直接就是H，无需开方，也不受二次项退化影响，第三个差式还能回代核验。
3. 利用/还原思路
按GCM位序实现GF(2^128)：乘x为右移一位、末位为1时异或0xE1<<120，乘法单位元是1<<127。
按nonce分组，保留帧数大于1的组，统计密文差异字节，确认差异只落在可变字段。
以每组首帧为基准，与其余两帧构造系数向量[ΔT,0,ΔC2,ΔC1]。
对两条三次式做poly_gcd并首一化，结果为一次式时取常数项为H，回代残差应为0。
以H的16字节大端为IKM，salt取NRWF-TELEM-LIC-v2，info取ch加通道号，HKDF-SHA256派生32字节密钥。
以AES-256-CTR解封，计数器块自16字节iv起按128位大端递增，复算HMAC-SHA256(key,iv||ct)[:16]与tag比对。
三份许可各用所属通道的H派生密钥，只采纳台账中current的ch1。
4. 复现脚本
import
json
R, ONE =
0xE1
<<
120
,
1
<<
127
def
up1
(v)
:
return
(v >>
1
) ^ (R
if
v &
1
else
0
)
def
mul
(a, b)
:
z, v =
0
, a
for
i
in
range(
128
):
z ^= v
if
b >> (
127
- i) &
1
else
0
v = up1(v)
return
z
def
inv
(a)
:
r, e = ONE, (
1
<<
128
) -
2
while
e:
if
e &
1
:
r = mul(r, a)
a, e = mul(a, a), e >>
1
return
r
def
pdiv
(p, q)
:
p, q = list(p), list(q)
while
len(p) >
1
and
p[
-1
] ==
0
: p.pop()
while
len(q) >
1
and
q[
-1
] ==
0
: q.pop()
if
len(p) < len(q):
return
[
0
], p
quo = [
0
] * (len(p) - len(q) +
1
)
for
i
in
range(len(quo) -
1
,
-1
,
-1
):
f = mul(p[i + len(q) -
1
], inv(q[
-1
]))
quo[i] = f
for
j, c
in
enumerate(q):
p[i + j] ^= mul(f, c)
while
len(p) >
1
and
p[
-1
] ==
0
: p.pop()
return
quo, p
def
pgcd
(p, q)
:
while
len(q) >
1
or
q[
0
]:
p, q = q, pdiv(p, q)[
1
]
lead = inv(p[
-1
])
return
[mul(c, lead)
for
c
in
p]
G = {}
for
f
in
json.load(open(
"gcm_capture.json"
, encoding=
"utf-8"
))[
"frames"
]:
G.setdefault(f[
"nonce"
], []).append(f)
def
diff
(a, b)
:
A, B = bytes.fromhex(a[
"ciphertext"
]), bytes.fromhex(b[
"ciphertext"
])
return
[int(a[
"tag"
],
16
) ^ int(b[
"tag"
],
16
),
0
,
int.from_bytes(A[
16
:],
"big"
) ^ int.from_bytes(B[
16
:],
"big"
),
int.from_bytes(A[:
16
],
"big"
) ^ int.from_bytes(B[:
16
],
"big"
)]
for
g
in
G.values():
if
len(g) >
2
:
H = pgcd(diff(g[
0
], g[
1
]), diff(g[
0
], g[
2
]))[
0
]
print(g[
0
][
"ch_id"
],
"%032x"
% H)
5. 运行结果
[+] ch1 两次差式公共根唯一：H=effec68ba41d511d7422c6f2661d3e7a，回代残差 全零
[lic_7f2a] ch=1 status=current  HMAC-SHA256(iv||ct)[:16] 一致
[=] flag{GCM_N0nc3_R3u53_1s_F0rb1dd3n_26}
6. 小结
nonce复用让标签差消去E_K(J0)，H便从认证密钥降为可解的多项式根；再把H当作KDF输入，等于把认证子密钥借给了业务侧。
最终flag
flag{GCM_N0nc3_R3u53_1s_F0rb1dd3n_26}
