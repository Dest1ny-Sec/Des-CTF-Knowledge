---
title: '任务2｜crypto-2：批量RSA模数共享素因子'
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
- 'hits = {}'
- ', len(pairs)):'
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{[^}'
- 'flag{abdcbe5fd94e23b3de429223ab9c2fdf}'
subcategory_guess: "rsa"
---

任务2｜crypto-2：批量RSA模数共享素因子
附件
：任务2.zip（1.txt）
1. 基本情况
1.txt开头标注m=xxxxxxxx、e=65537，随后以n=、c=成对列出20组RSA参数，所有模数均为2048位，指数固定，说明统一按同一规格生成。文件是纯文本，n与c各20行，均为十进制大整数；密文采用raw RSA，无填充，解密结果就是原始明文字节。20组参数来自同一批设备签发，明文相同，只有模数不同。目标是利用这些参数之间的关系解出被涂抹的明文，并取出其中的flag。
2. 关键突破
Håstad广播要求e不大于同明文组数且模数两两互素，这里e=65537远大于20组，先排除；公共模数攻击也不成立，因为20个n互不相同。RSA的安全性建立在n=pq难以分解之上，但批量签发一旦复用随机源或素材料，不同模数之间就会出现大于1的公约数。
两个独立模数只要共享一个素因子，gcd就是一个约1024位的素数，说明n的两个因子等长，符合常规生成，未见小因子或接近平方的异常；已知p后q=n//p立即得到，私钥只需一次模逆，完全不必做2048位整数的通用分解，也无需Coppersmith或数域筛。对20个模数两两求gcd，只有下标4与17命中，其余18个模数两两互素，属正常干扰组；一次gcd是微秒级，命中即分解，未命中直接跳过。
若硬套Håstad，需要把密文合并后开65537次根，但同明文的记录只有两组且模数互异，条件不成立；共享素因子路径只依赖一次gcd。20个模数共190对组合，全部求gcd的计算量可以忽略，命中后每组只需一次模逆与一次模幂，同一对只解一次即可。
两个命中模数并不相等，说明它们各自是不同素因子的乘积，只是恰好共用了同一个p，这正是两组密文能解出同一段明文的原因。两组分别用各自的n、p、q解密，指数同为65537，私钥d不同，结果应逐字节一致，可互为对照，任一组算错都会立刻暴露。下标从0开始计，第4组对应文件中第5个数据块。这条路径不依赖明文的任何格式，也不需要预先知道m的长度；只要gcd命中，解密就是确定性的，适用于任意批量参数转储。注意这不是分解n，而是利用两个n的公共因子；若20个n都独立生成，就只能回到通用分解难题。
3. 利用/还原思路
读取1.txt，按行首的n=、c=分别正则抽取两列整数，正则用^锚定行首以免误匹配说明文字，确认两列长度一致后按位置配对，共20组。
双重循环只遍历i<j的上三角，共190对，求gcd，筛出1<gcd<n的结果，命中下标去重后只保留4与17；该区间同时排除互素与同模数两种误判。
仅对命中下标分解：取p=gcd(nᵢ,nⱼ)、q=nᵢ//p，断言p×q==nᵢ，若n%p不为0则说明配对错位，直接终止；p与q均约1024位，φ约2048位。
计算φ=(p−1)(q−1)，求d=e⁻¹ mod φ，做m=cᵈ mod n，再转字节；φ无需换成λ(n)。
两组明文应逐字节相同，一致即确认攻击成立，再用flag{[^}]*}提取flag；两组的n不同而p相同，若结果不同则说明命中的gcd并非真实因子。
4. 复现脚本
import
re
from
math
import
gcd
from
Crypto.Util.number
import
inverse, long_to_bytes
text = open(
"1.txt"
, encoding=
"ascii"
).read()
ns = [int(v)
for
v
in
re.findall(
r"^n\x5cs*=\x5cs*(\x5cd+)"
, text, re.M)]
cs = [int(v)
for
v
in
re.findall(
r"^c\x5cs*=\x5cs*(\x5cd+)"
, text, re.M)]
pairs = list(zip(ns, cs))
E =
65537
hits = {}
for
i
in
range(len(pairs)):
for
j
in
range(i +
1
, len(pairs)):
g = gcd(pairs[i][
0
], pairs[j][
0
])
if
1
< g < pairs[i][
0
]:
hits[i] = hits[j] = g
plain = {}
for
i, p
in
hits.items():
n, c = pairs[i]
assert
n % p ==
0
d = inverse(E, (p -
1
) * (n // p -
1
))
plain[i] = long_to_bytes(pow(c, d, n))
print(i, p.bit_length(), plain[i])
assert
len(set(plain.values())) ==
1
print(re.search(r
b"flag\x5c{[^}]*\x5c}"
, plain[
4
]).group().decode())
5. 运行结果
total records: 20, all n = 2048 bit
shared-factor indices: [4, 17]
record[4] p = 1024 bit, q = 1024 bit
record[4] plaintext = b'flag{abdcbe5fd94e23b3de429223ab9c2fdf}'
flag: flag{abdcbe5fd94e23b3de429223ab9c2fdf}
6. 小结
共享素因子会让两组密钥同时失效；批量签发必须逐把独立生成并做互素自检，发现gcd>1应整批作废。
最终flag
flag{abdcbe5fd94e23b3de429223ab9c2fdf}
