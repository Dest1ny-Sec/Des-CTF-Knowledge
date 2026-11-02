---
title: '任务7｜misc-2：5View私有容器中的Modbus隐蔽信道'
contest: '2026中国工业互联网安全大赛-线上预选赛'
contest_normalized: '2026中国工业互联网安全大赛-线上预选赛'
contest_year: 2026
year: 2026
category: 'misc'
subcategory: 'misc_other'
tags: []
attack_chain:
- '基本情况'
- '关键突破'
- '利用/还原思路'
- '复现脚本'
- 'blob = open(CAP,'
- ':pos +'
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{y0u_jus4_hav3_the_c0de}'
subcategory_guess: "misc_misc"
---

任务7｜misc-2：5View私有容器中的Modbus隐蔽信道
附件
：任务7.zip（misc-2.zip内的modbus.pcap）
1. 基本情况
附件modbus.pcap以5View私有格式封装，文件头魔数为AAAA AAAA，既非标准pcap的D4 C3 B2 A1，也非pcapng的0A 0D 0D 0A，直接交给dpkt或scapy会报头部非法。提示说明这是Modbus通信，机密标识符被写入寄存器。抓包共751826字节、7700条记录，绝大多数是成对读操作，真正的写操作只有一处。目标是从流量中还原被刻意倒置的内容。
2. 关键突破
容器为连续记录：每条前面是36字节记录头，固定以EE EE 33 33开头，偏移16处的4字节小端整数等于其后以太帧长度，按36+帧长顺序步进即可。首条记录前还有一段私有文件头，从首个魔数起按此规则可遍历全部7700条，尾部无额外对齐。不宜全文搜索魔数切分，因为以太帧载荷内部也可能出现同样字节，会造成记录边界错位。
协议层按以太类型08 00、IPv4协议号6、IP首部长度与TCP数据偏移逐层取出载荷，目的端口502即Modbus。统计功能码可见1、2、3、4各有351条，对应读线圈、读离散输入、读保持寄存器、读输入寄存器；功能码0x10（写多个保持寄存器）只有1条，正是目标报文。
该报文起始寄存器为1、寄存器数25、字节数50，恰为25×2，说明数据未被截断。Modbus的0x10请求在7字节MBAP头之后依次为功能码1字节、起始地址2字节、数量2字节、字节数1字节、数据，故pdu[7]为功能码，pdu[8:12]可按两个大端16位读出，pdu[12]为字节数。50字节以0x00开头，是寄存器对齐填充；末尾一连串“.”用于占满剩余寄存器空间，二者都不是密文。去掉后得到以“==”开头的字符串，而合法Base64的等号只应在末尾，说明整串被倒序。反转后解码，结果以“}”开头、以“galf”结尾，明文同样被倒置，再反转一次即得flag。两层倒置叠加，正是题面所说的刻意混淆。
3. 利用/还原思路
读入整个文件，以EE EE 33 33定位第一条记录起点，跳过文件私有前缀。
循环校验记录头，读取偏移16处的4字节小端作为帧长，切出以太帧后步进36+帧长。
逐层解析：以太类型须为08 00，IPv4协议号须为6，按IHL与TCP数据偏移取载荷，并以IP总长度截断，避免把以太网填充算进去。
保留目的端口502且长度足够的报文，按功能码0x10筛选；在MBAP头后按功能码、起始地址、数量、字节数、数据的顺序读取pdu[8:12]与pdu[12]。
去除前导0x00与尾部“.”，反转后Base64解码，再反转得到明文。
4. 复现脚本
import
base64, struct
CAP, MAGIC, HL =
"modbus.pcap"
,
b"\x5cxee\x5cxee\x5cx33\x5cx33"
,
36
blob = open(CAP,
"rb"
).read()
pos, frames = blob.find(MAGIC), []
while
pos !=
-1
and
pos + HL <= len(blob):
n = struct.unpack(
"<I"
, blob[pos +
16
:pos +
20
])[
0
]
frames.append(blob[pos + HL:pos + HL + n])
pos += HL + n
for
f
in
frames:
if
len(f) <
34
or
f[
12
:
14
] !=
b"\x5cx08\x5cx00"
:
continue
ip = f[
14
:]
if
ip[
0
] >>
4
!=
4
or
ip[
9
] !=
6
:
continue
ihl = (ip[
0
] &
15
) *
4
seg = ip[ihl:struct.unpack(
">H"
, ip[
2
:
4
])[
0
]]
if
len(seg) <
20
or
struct.unpack(
">H"
, seg[
2
:
4
])[
0
] !=
502
:
continue
pdu = seg[(seg[
12
] >>
4
) *
4
:]
if
len(pdu) <
13
or
pdu[
7
] !=
0x10
:
continue
ref, qty = struct.unpack(
">HH"
, pdu[
8
:
12
])
raw = pdu[
13
:
13
+ pdu[
12
]]
cipher = raw.lstrip(
b"\x5cx00"
).rstrip(
b"."
)
print(ref, qty, base64.b64decode(cipher[::
-1
])[::
-1
].decode())
5. 运行结果
[*] 容器魔数 aaaaaaaa，体积 751826 字节，记录数 7700
[*] 功能码 0x01/0x02/0x03/0x04 各351条，0x10仅1条
[*] 起始寄存器 1，寄存器数 25，字节数 50
[*] 反转Base64得 }ed0c_eht_3vah_4suj_u0y{galf
[+] flag{y0u_jus4_hav3_the_c0de}
6. 小结
私有容器按长度字段步进比搜魔数可靠，海量读操作只是掩蔽，唯一的写寄存器报文就是隐蔽信道。
最终flag
flag{y0u_jus4_hav3_the_c0de}
