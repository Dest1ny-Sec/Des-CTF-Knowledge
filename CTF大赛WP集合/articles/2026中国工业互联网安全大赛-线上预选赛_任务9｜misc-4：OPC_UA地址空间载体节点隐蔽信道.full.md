---
title: '任务9｜misc-4：OPC UA地址空间载体节点隐蔽信道'
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
- '00 c8 02'
- '越界序号，尾随节点异或后不是合法base64字符。必须按声明槽数截断，否则解码混入多余字节失败。'
- '利用/还原思路'
- '00 c8 02'
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{0PCUA_M1rr0r_Trace_D3c0y}'
- 'flag{0PCUA_N0d3Id_C0v3rt_2026}'
- 'flag{0PCUA_Sn4psh0t_L34k_2026}'
subcategory_guess: "misc_misc"
---

任务9｜misc-4：OPC UA地址空间载体节点隐蔽信道
附件
：任务9.zip（misc-4.zip内的plant_nodeset.xml、plant_opcua.pcap）
1. 基本情况
车间OPC UA采集系统的地址空间导出文件plant_nodeset.xml与MES侧镜像流量plant_opcua.pcap一并留存，题面称攻击者用自定义方法把内部缓存写进地址空间。XML含ns=0至ns=3四个命名空间，ns=3下7个自定义方法的Description字段带有base64编码的JSON元数据。流量中10.40.9.77:53999一条短会话调用了三个诊断方法，入参依次为109、58、145。目标是交叉两份材料还原节点上的隐蔽通道，取出状态为active那条通道的flag。
2. 关键突破
元数据给出三条通道：Dump对应
Diag.Cache.Slot
、active；Trace对应
Diag.Cache.Mirror
、disabled；Snapshot对应
Diag.Snapshot.Entry
、deprecated。三者都声明40个槽位，只有active真正启用，按状态选载体即可排除干扰。
流量侧三次Call分别落在
Diagnostics.Internal
的Dump、Trace与
Diagnostics.Legacy
的Snapshot上，入参109、58、145没有回显，说明数据被写回地址空间。载体槽位BrowseName形如
Diag.Cache.Slot.00
，把槽位NodeId的低字节按槽序号升序拼接再异或方法入参，得到的字节串恰好是合法base64；入参就是该通道的单字节异或密钥，key=109即解出active通道的flag。
报文解析不能依赖固定偏移：MSG帧为type(3字节)+size(4字节小端)，body前16字节是通道、令牌、序号、请求号，随后是服务NodeId；CallRequest为FourByte编码
01 00 c8 02
，即ns=0、标识712。RequestHeader的AuditEntryId是变长String，长度一变偏移就漂移，稳妥做法是在body内扫描0x03型String NodeId，前两个命中即ObjectId与MethodId，再读4字节MethodsToCall数量，Variant类型码7为Int32入参。
槽位还有陷阱：
Diag.Cache.Slot
实挂58个节点，比声明的40个多出
0A
至
0H
后缀与
40
至
49
越界序号，尾随节点异或后不是合法base64字符。必须按声明槽数截断，否则解码混入多余字节失败。
3. 利用/还原思路
解析XML，遍历UAMethod，对Description做base64解码并解析JSON，建立“方法短名→载体/状态/槽数”映射。
遍历UAVariable，按载体名前缀收集数字槽标签，得到“槽序号→NodeId数值”字典。
按五元组归并pcap的TCP流并重组，切出MSG帧，保留body[16:20]为
01 00 c8 02
的Call报文。
扫描body内0x03型String NodeId，第二个为MethodId，其后4字节计数、1字节类型码、4字节Int32即密钥，得109、58、145。
对每个载体取声明槽数内的槽位，NodeId低字节按序异或密钥，补
=
后base64解码，取status为active者。
4. 复现脚本
import
base64, json
import
xml.etree.ElementTree
as
ET
NS =
"{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}"
root = ET.parse(
"plant_nodeset.xml"
).getroot()
# ... pcap 头解析、TCP 重组与三次 Call 入参提取略, 结果为 109/58/145
KEYS = {
"Dump"
:
109
,
"Trace"
:
58
,
"Snapshot"
:
145
}
methods = {}
for
n
in
root.iter(NS +
"UAMethod"
):
d = n.find(NS +
"Description"
)
if
d
is
not
None
and
d.text
and
"<"
not
in
d.text:
methods[n.get(
"BrowseName"
).split(
"."
)[
-1
]] = json.loads(base64.b64decode(d.text))
for
short, meta
in
sorted(methods.items()):
pre, slots = meta[
"carrier"
] +
"."
, {}
for
n
in
root.iter(NS +
"UAVariable"
):
name = (n.get(
"BrowseName"
)
or
""
).split(
":"
)[
-1
]
if
name.startswith(pre)
and
name[len(pre):].isdigit():
slots[int(name[len(pre):])] = int(n.get(
"NodeId"
).split(
";"
)[
-1
].split(
"="
)[
-1
])
order = [i
for
i
in
sorted(slots)
if
i < meta[
"slots"
]]
# 截掉声明槽数以外的尾随节点
raw = bytes((slots[i] &
0xFF
) ^ KEYS[short]
for
i
in
order)
print(meta[
"status"
], meta[
"carrier"
], base64.b64decode(raw +
b"="
* (-len(raw) %
4
)).decode())
5. 运行结果
[*] 调用Dump(109)、Trace(58)、Snapshot(145)
[active    ] Diag.Cache.Slot      key=109 -> flag{0PCUA_N0d3Id_C0v3rt_2026}
[deprecated] Diag.Snapshot.Entry  key=145 -> flag{0PCUA_Sn4psh0t_L34k_2026}
[disabled  ] Diag.Cache.Mirror    key=58  -> flag{0PCUA_M1rr0r_Trace_D3c0y}
flag{0PCUA_N0d3Id_C0v3rt_2026}
6. 小结
隐蔽信道藏在协议元数据里：入参当异或密钥、NodeId低字节当密文，比直接改字段值更难被字段级校验发现。
最终flag
flag{0PCUA_N0d3Id_C0v3rt_2026}
