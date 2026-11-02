---
title: 'Misc3-NeuronShuffle'
contest: '强网杯 2026 第十届'
contest_normalized: '强网杯 2026 第十届'
contest_year: 2026
year: 2026
category: 'crypto'
subcategory: 'crypto_other'
tags: []
attack_chain:
- '题目信息'
- '题目分析'
- '→48→40→32→16'
- '个较宽隐层的宽度正好是'
- '，这三个数后面会原样成为置换（打乱）的参数。'
- 'af6522bb081f48d0acf626'
one_liner: '1. 题目信息'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/onGfTPOi9N7Ak9UWWmMNoA'
last_verified: '2026-11-02'
flag_observed:
- 'flag{...}'
- 'flag{5c2aabdc937513bde1ba502f14cc51b6}'
contest_normalized: "强网杯"
subcategory_guess: "misc_misc"
---

Misc3-NeuronShuffle
1. 题目信息
项目
内容
分类
Misc
形态
附件题（离线分析，无远程服务）
附件
neuron_shuffle_8a803e935e33df360a9e1e1976d567c5.zip，55598字节
目标
无（离线附件）
Flag：flag{5c2aabdc937513bde1ba502f14cc51b6}
题面：本题含有少量人工神经元，运输过程中可能出现沉淀，使用前请充分摇匀；如出现头晕、眼花、脱发或开始质疑自我，均属正常现象。请勿停止做题，以免前功尽弃。本品最终解释权归脑子所有。 题面里“充分摇匀”和“沉淀”是直接提示：权重是一份被随机打乱了顺序的神经网络参数，解题的关键不是反推神经网络本身，而是还原打乱顺序所用的随机数。
2. 题目分析
附件结构
解压后的目录只有三个文件，没有源码工程也没有权重配置文件：
neuron_shuffle/
├── check.py      校验器，963字节
├── model_A.npz   可正常加载的权重，44982字节
└── model_B.bin   等长二进制，44982字节
model_A.npz
用
np.load(..., allow_pickle=False)
可以正常读出，包含8个数组：
数组
形状
作用
k0
(16,)
第2层偏置，16维
k1
(16,32)
第1层权重，32维输入→16维输出
k2
(40,48)
第2层权重，48维输入→40维输出
k3
(48,)
第1层偏置，48维
k4
(40,)
第3层偏置，40维
k5
(48,32)
第1层权重，32维输入→48维输出
k6
(32,40)
第3层权重，40维输入→32维输出
k7
(32,)
输出层偏置，32维
把偏置维度和权重形状对齐，可以还原出网络拓扑为
32→48→40→32→16
（权重按
(输出维, 输入维)
存放，也就是PyTorch的
Linear.weight
风格）：
k5
是32→48，
k3
是48维偏置，
k2
是48→40，
k4
是40维偏置，
k6
是40→32，
k7
是32维偏置，
k1
是32→16，
k0
是16维偏置。
目标主机实际读出的形状与
dtype
：
k3 (48,)     float64      k4 (40,)     float64
k6 (32, 40)  float64      k7 (32,)     float64
k1 (16, 32)  float64      k5 (48, 32)  float64
k2 (40, 48)  float64      k0 (16,)     float64
三个较宽隐层的宽度正好是
48
、
40
、
32
，这三个数后面会原样成为置换（打乱）的参数。
model_B.bin
是干扰项：长度44982字节，与
model_A.npz
完全等长；前16字节为
3268100616af6522bb081f48d0acf626
，形如一个16字节摘要；整个文件的字节分布接近均匀（每个字节值出现频率约200次），既不满足
zipfile.is_zipfile
，也不是zlib/lzma/bz2压缩流，按
float64
、
float32
在任何偏移切片都得不到量级合理的权重值。它是权重被“摇匀/加密”后的黑盒副本，无法直接解析。
解题不需要拆开
model_B.bin
：
model_A.npz
已经给出了同一批张量的数值，缺的只是“顺序”。题目真正的考点在
check.py
——它要的答案是一段索引排列。
check.py的校验逻辑
check.py
全文只有三十余行，核心是把用户输入规范化后做两级SHA-256：
V =
"cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
def
main
()
:
if
len(sys.argv) !=
2
:
sys.exit(__doc__)
src = Path(sys.argv[
1
])
try
:
text = src.read_text()
if
src.exists()
else
sys.argv[
1
]
except
OSError:
# inline answer string too long for a filename
text = sys.argv[
1
]
try
:
canon =
";"
.join(
","
.join(str(int(v))
for
v
in
s.split(
","
))
for
s
in
text.strip().split(
";"
))
except
Exception:
sys.exit(
"[-] wrong"
)
body = hashlib.sha256(canon.encode()).hexdigest()[:<端口>]
if
hashlib.sha256((
"ns::"
+ body).encode()).hexdigest() == V:
print(
f"[+] correct! flag = flag{{
{body}
}}"
)
else
:
sys.exit(
"[-] wrong"
)
几点关键设计：
输入形式宽松
：参数既可以是文件路径，也可以直接是答案字符串（Windows上超长字符串当路径会触发
OSError
，用
except OSError
兜底回退成字符串）。
规范化很严
：按
;
切三段、每段按
,
切、每项
int()
后重新拼接，因此前导零、空格、多余换行都会被吃掉；答案在文本层面唯一，必须真正生成正确的索引序列，随便加空格不会“碰巧”通过。
两级哈希
：先算
body = sha256(canon)[:<端口>]
（只取前32个十六进制字符，即128位），再算
sha256("ns::" + body)
与硬编码常量
V
比对。
flag就是
body
：
body
直接构成
flag{...}
的内容，所以二级哈希只是“防直接读flag”的外壳，真正要做的是
还原被哈希的原文
，而不是爆破摘要。
V
在附件里是明文常量，这给出了一个可判定的终点：只要构造出一段候选规范串，算两次哈希就能立刻判断对错，不需要提交到平台。
权重来自可预测的随机序列
对
model_A.npz
做统计：8个数组共
5384
个
float64
，去重后只剩
926
个不同的值。如果权重是逐层独立抽样得到的连续分布随机数，上千个值几乎不可能出现如此高的重复率，说明权重是
从一个候选值池按索引反复取用
的。
再用默认位生成器验证：
np.random.default_rng(20261101).normal(0, 0.6, 974)
产生的974个样本恰好覆盖模型全部926个唯一值，而且
k5
的第0行（32个值）与样本序列的前32个
逐位相同
：
k5[0][:5]  = [-1.07367412 -1.10126123  0.5885369   0.40113786  0.03993815]
samples[:5] = [-1.07367412 -1.10126123  0.5885369   0.40113786  0.03993815]
array_equal(k5[0], samples[:<端口>]) → True
这里的相等是
float64
的完全相等，不是近似相等。池长974是下界而非估计值：模型里最后被用到的那个值位于该序列下标973，取973个样本无法覆盖全部权重，取974个刚好覆盖。
由此得到三条可复用的结论：
权重由
default_rng
的
normal(0, 0.6, N)
生成，均值和标准差固定为
0
与
0.6
；
种子是整数，且
20261101
符合
YYYYMMDD
日期形式，说明种子就是日期；
序列是确定性的，只要种子对了，整个模型可以原位重建；反之种子空间极小，可以直接枚举。
3. 解题过程
提取浮点池与指纹行
先把模型压成一个一维浮点池（用于判断覆盖率），同时单独保存
k5
第0行（用于锁定序列起点）：
with
np.load(
'model_A.npz'
, allow_pickle=
False
)
as
model:
row = model[
'k5'
][
0
].copy()
values = np.unique(np.concatenate([model[name].ravel()
for
name
in
model.files]))
选择
k5[0]
作为“指纹行”有两个原因：它是模型里真实存在的一行，长度32足以排除偶然命中；它的值恰好等于序列的前32个样本并且保持顺序，等于把种子的起点也一起钉死了。如果只用“集合覆盖”判断，序列越长越容易误命中，命中后还要再回头验证顺序，多绕一步。
本步结果：
row
长度32，
values
长度926。
枚举日期种子并逐位比对
种子既然是日期，枚举窗口取题目发布前后的三个月即可：从
2026-10-01
开始连续92天（覆盖到
2026-12-31
）。对每个日期做两步比对：
day = start + timedelta(days=offset)
seed = int(day.strftime(
'%Y%m%d'
))
samples = np.random.default_rng(seed).normal(
0
,
0.6
,
974
)
if
np.array_equal(row, samples[:<端口>])
and
np.setdiff1d(values, samples).size ==
0
:
...
<code style="color: rgb(30, 107, 184);font-size: 14px;line-height: 1.8em;letter-spacing: 0e
