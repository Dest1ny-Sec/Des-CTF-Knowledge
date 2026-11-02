---
title: '失陷主机流量分析 (capture.pcap)'
contest: '强网拟态防御 第九届'
contest_normalized: '强网拟态防御 第九届'
contest_year: 2025
year: 2025
category: 'misc'
subcategory: 'misc_other'
tags: []
attack_chain:
- '题目说明'
- ',954,555'
- '）的外传流量，还原攻击者传出的真实数据并获取'
- '解题思路'
- 'xa9b2c3d4'
- 'x1337'
one_liner: '题目描述：'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/iTgaxzumnH3cE4N5nH6VvQ'
last_verified: '2026-11-02'
flag_observed:
- 'flag{...}'
- 'flag{fake_patched_s0rry}'
- 'flag{tw0_c4ts_0ne_tr4p}'
contest_normalized: "强网拟态"
subcategory_guess: "traffic_analysis"
---

失陷主机流量分析 (capture.pcap)
题目描述：
我们从一台失陷主机上抓到了一段流量：capture.pcap。抓包抓到一半主机断电了。
附件：capture.zip
核心思路
：通过以太网帧与 IPv4 头部长度字段修复损坏的 PCAP 文件头及包记录头，从 HTTP、DNS、ICMP 流量中搜集 12 条文档碎片，结合测试服务交互流量逆向还原 MSB 比特流打包的 KV-VM 虚拟机指令集（
rev.B
与
rev.C
），依次解密并执行
KV
与
PX
两个 ICMP 隐蔽通道中的自修改字节码，拼接得到完整 Flag。
1. 题目说明
题目给出如下背景描述与流量文件
capture.pcap
（大小
5,954,555
字节，SHA-256 为
ef38842f4026e501f6a712cbeaa9ea19c5d6ab376108f71e03eed90a0feff8f4
）：
我们从一台失陷主机上抓到了一段流量：capture.pcap。抓包抓到一半主机断电了。
目标是修复并分析
capture.pcap
中失陷主机（
10.0.0.5
）的外传流量，还原攻击者传出的真实数据并获取
flag{...}
格式的 Flag。
2. 解题思路
修复损坏的 PCAP 结构
：检查文件头发现 Magic Number 被篡改为
0xa9b2c3d4
、LinkType 被篡改为
0x1337
，且第 47、53、59、67、75、83 号数据包的
incl_len
/
orig_len
字段被篡改导致后续数据包错位。利用二层以太网帧类型（IPv4 头部
Total Length + 14
、ARP 固定
42
字节）重新计算每个数据包的真实长度，即可无损恢复全部 4561 个数据包。
提取并还原 12 条文档碎片
：遍历修复后的 HTTP、DNS TXT（含单字节异或混淆）和 ICMP Echo Reply 流量，找齐编号为
1/12
至
12/12
的提示信息与
/kv-vm-manual.txt
文档，明确 ICMP 隧道的包结构、密钥链算法以及 KV-VM v3 虚拟机的比特流指令格式。
根据测试机流量逆向 5-bit 指令集
：流量中包含失陷主机对
10.0.0.99:31337
（
rev.B
）和
10.0.0.99:31338
（
rev.C
）发送的
RUN <hex>
测试指令及返回结果。对比测试输入与输出，还原全部 19 条 5-bit 操作码，并定位
rev.C
相较
rev.B
重定义的 3 条指令行为（
RORI
、
POP
空栈返回 0、
JMPR
乘 16）。
两阶段字节码解密与虚拟机执行
：
第一阶段：用初始密钥
解密并校验
KV
通道分片，重组出 251 字节的
rev.B
字节码，送入虚拟机运行得到前半段 Flag
flag{tw0_c4t
以及第二阶段参数
PX rev.C k=9f3cb712aa55d04e
。
第二阶段：提取 ICMP 中
PX
通道的 5 个分片（42 字节），用密钥
9f3cb712aa55d04e
循环异或解密后送入
rev.C
虚拟机运行，得到后半段 Flag
s_0ne_tr4p}
。
3. 解题过程
3.1 修复 PCAP 全局文件头与包长度字段
关键观察：
直接用 Wireshark 打开
capture.pcap
会报错。读取文件前 24 字节全局头并按小端序解析包头时，解析到第 48 号包（偏移
7082
）出现长度异常（
incl_len = 3997706
）：
Header (24 bytes): d4c3b2a9 0200 0400 00000000 00000000 ffff0000 37130000
Pkt 47: offset=7001, incl_len=65, orig_len=65
Pkt 48: offset=7082, incl_len=3997706, orig_len=3997696, first16=00000200000000050200000000990800
可以看到：
全局头前 4 字节为
d4 c3 b2 a9
（
0xa9b2c3d4
），标准微秒级 PCAP Magic 应为
d4 c3 b2 a1
（
0xa1b2c3d4
）；末尾 4 字节 LinkType 为
37 13 00 00
（
0x1337
），标准 Ethernet 应为
01 00 00 00
（
1
）。
在第 48 号包的
first16
中，以太网帧头
020000000005 020000000099 0800
向后偏移了 2 字节。查看第 47 号包（偏移
7017
）的 IPv4 头部，其
Total Length
字段为
0x0035
（53 字节），加上 14 字节以太网帧头，实际帧长应为
字节，而第 47 号包头中的
incl_len
却写成了
65
。
原理与操作：
PCAP 文件中的每个数据包均为标准以太网帧（
0x0800
IPv4 或
0x0806
ARP）。对于 IPv4 数据包，真实帧长恒等于
；对于 ARP 数据包，真实帧长恒为 42 字节。据此扫描全文件并对比
incl_len
与真实帧长：
import
struct
with
open(
"capture.pcap"
,
"rb"
)
as
f:
data = bytearray(f.read())
data[
0
:
4
] = struct.pack(
"<I"
,
0xA1B2C3D4
)
data[
20
:
24
] = struct.pack(
"<I"
,
1
)
offset =
24
pkt_idx =
0
while
offset +
16
<= len(data):
ts_sec, ts_usec, incl_len, orig_len = struct.unpack(
"<IIII"
, data[offset:offset+
16
])
pkt_start = offset +
16
eth_type = struct.unpack(
">H"
, data[pkt_start+
12
:pkt_start+
14
])[
0
]
real_len =
14
+ struct.unpack(
">H"
, data[pkt_start+
16
:pkt_start+
18
])[
0
]
if
eth_type ==
0x0800
else
42
if
incl_len != real_len:
print(
f"Mismatch at Pkt
{pkt_idx}
(offset
{offset}
): header=
{incl_len}
, real=
{real_len}
"
)
data[offset+
8
:offset+
16
] = struct.pack(
"<II"
, real_len, real_len)
offset = pkt_start + real_len
pkt_idx +=
1
print(
f"Total packets:
{pkt_idx}
, final offset:
{offset}
/
{len(data)}
"
)
本步结果：
共定位并修复 6 处包长篡改，最终偏移恰好等于文件总大小
5954555
字节，完整恢复 4561 个数据包：
Mismatch at Pkt 47 (offset 7001): header=65, real=67
Mismatch at Pkt 53 (offset 7491): header=64, real=71
Mismatch at Pkt 59 (offset 7983): header=64, real=71
Mismatch at Pkt 67 (offset 8639): header=71, real=75
Mismatch at Pkt 75 (offset 9337): header=86, real=83
Mismatch at Pkt 83 (offset 10035): header=76, real=83
Total packets: 4561, final offset: 5954555/5954555
3.2 提取 12 条分析笔记与虚拟机参考手册
关键观察：
对修复后的流量按协议分类后（排除末尾用于填充体积的 UDP
8.8.8.8:443
与 TCP
1.1.1.1:443
流量），在 HTTP（
10.0.0.80:80
）、DNS（
10.0.0.53:53
）和 ICMP（
10.0.0.99
）中发现编号为
X/12
的分片提示（其中 Pkt 39 的 DNS 响应经过了
0x42
单字节异或混淆）。
原理与操作：
遍历全部数据包，提取包含
/12
的明文及单字节异或 payload，同时导出 HTTP 响应中的
/kv-vm-manual.txt
。
本步结果：
按序号
1/12
至
12/12
整理出的完整提示如下：
编号
来源位置
内容
1/12
Pkt 33 (
doc1.darknet-corp.net
TXT)
field notes 1/12 :: he exfils over ICMP echo. exactly ONE channel is his. the rest are chaff. mostly.
2/12
Pkt 35 (
doc2.darknet-corp.net
TXT)
2/12 :: payload: 'KV' u8 seq | u8 len | u8 cksum | data. reassemble by seq asc.
3/12
Pkt 10 (
/cat1.jpg
HTTP 响应头)
3/12 :: data[i]=plain[i]^((K_seq+i)&0xFF). cksum=sum(plain)&0xFF. drop bad cksum; first valid per seq wins.
4/12
Pkt 37 (
doc4.darknet-corp.net
TXT)
4/12 :: key chain rev.B: K_0=0xA6, K_(n+1)=(K_n*31+7)&0xFF
5/12
Pkt 12 (
/cat2.jpg
JPEG COM 注释段)
5/12 :: note: rev.B keychain doc had a typo. K_0=0xA5. burn rev.B.
6/12
Pkt 210 (ICMP Echo Reply)
6/12 :: the reassembled bytes are firmware v3 bytecode.
7/12
Pkt 39 (
doc7.darknet-corp.net
TXT ^
0x42
)
7/12 :: v3 packs instructions MSB-first, no byte alignment: opcode 5b, reg 4b, imm 8b, addr 16b (bit addr).
8/12
Pkt 12 (
/cat2.jpg
HTTP 响应头)
8/12 :: data space is byte-addressed. pc is a bit address. jumps take bit addrs; JMPR jumps R*8.
9/12
Pkt 16 (
/favicon.ico
HTTP 404 正文)
9/12 :: there is no opcode list. the box at 10.0.0.99:31337 answers test programs. query: RUN <hex>
10/12
Pkt 41 (
doc10.darknet-corp.net
TXT)
10/12 :: 16 regs R0-RF, mod 256, 256-deep stack. pop on empty faults.
11/12
Pkt 14 (
/kv-vm-manual.txt
HTTP 响应头)
11/12 :: pages lie. cats lie. chaff channels lie. trust checksums.
12/12
Pkt 43 (
doc12.darknet-corp.net
TXT)
12/12 :: if your disassembly turns to garbage, congratulations. keep going.
同时，Pkt 14 正文给出了旧版固件 v2.4 的指令助记符列表（
/kv-vm-manual.txt
）：
KV-VM REFERENCE MANUAL -- firmware v2.4
=======================================
16 registers R0-RF, mod 256. operands follow the opcode byte.
0x00 HALT        0x2C LOADI r,imm   0x4A MOVR rd,rs    0xB4 LOADC rD,[rA]
0x58 STOREC [rA],rV  0x37 PUSH r    0x91 POP r         0x61 EMIT r
0x83 ADDI r,imm  0x6E SUBI r,imm    0x0F XORI r,imm    0xA2 ANDI r,imm
0x1D ROLI r,imm  0xC9 XORR rd,rs    0x53 ADDR rd,rs    0xD7 JMP a16le
0x19 JNZ r,a16le 0xEB JZ r,a16le
加上笔记
8/12
提到的
JMPR r
，固件 v3 共有 19 条指令，操作码由 8-bit 改为 5-bit，按 MSB-first 紧凑比特流排列（无字节对齐）。
3.3 逆向 KV-VM v3 指令集（
rev.B
与
rev.C
）
关键观察：
在 TCP 流量中存在两个测试会话：
10.0.0.5:52300 <-> 10.0.0.99:31337
：发送了 21 条
RUN <hex>
测试指令，覆盖全部
rev.B
指令。
10.0.0.5:52400 <-> 10.0.0.99:31338
：服务端首先返回 Banner：
rev.C test box. 3 opcodes redefined vs rev.B. no manual. RUN <hex>
随后客户端发送了 9 条测试指令。
原理与操作：
将
31337
会话中的十六进制指令转为 MSB-first 二进制比特流。以第一条测试
RUN 3820c83e
OUT 41
（共 32 bits）为例：
00111 0000 01000001 | 10010 0000 | 11111 | 0 (padding)
LOADI R0,  0x41     | EMIT  R0   | HALT  |
由此直接确定
00111
为
LOADI r, imm
（
）、
10010
为
EMIT r
（
）、
11111
为
HALT
（
）。同理逐一拆解其余 20 条
31337
测试用例，再对比
31338
（
rev.C
）的 9 条测试用例：
在
31338
中，
RUN 3840e000641f
（
LOADI R0, 0x81; 11000 R0, 0x01; EMIT R0; HALT
）输出
OUT c0
，
RUN 3810e000a41f
（
LOADI R0, 0x21; 11000 R0, 0x02; EMIT R0; HALT
）输出
OUT 48
。可見
11000
在
rev.B
中为循环左移
ROLI
，而在
rev.C
中重定义为**循环右移
RORI
**。
在
31338
中，
RUN b0483e
（
POP R0; EMIT R0; HALT
）输出
OUT 00
，而在
31337
中
RUN b07c
返回
ERR stack underflow (POP on empty)
。可见
10110
（
POP
）在
rev.C
中**空栈弹出时不再报错，而是返回
0
**。
在
31338
中，
RUN 3b8121c038abc87e
（
LOADI R7, 0x02; JMPR R7
后在 bit 32 处存放
LOADI R0, 0x57; EMIT R0; HALT
）输出
OUT 57
；
LOADI R7, 0x03; JMPR R7
跳转到 bit 48 输出
OUT 59
。可见
01000
（
JMPR r
）在
rev.B
中跳转目标为
，而在
rev.C
中重定义为 **
**。
本步结果：
完整还原的 KV-VM v3 指令集如下表所示：
5-bit Opcode
助记符
格式与比特长度
rev.B
语义
rev.C
差异
00001
(
0x01
)
STOREC [rA], rV
op(5) + rA(4) + rV(4)
= 13b
mem[R[rA]] = R[rV]
相同
00011
(
0x03
)
ADDI r, imm
op(5) + r(4) + imm(8)
= 17b
R[r] = (R[r] + imm) & 0xFF
相同
00110
(
0x06
)
ADDR rd, rs
op(5) + rd(4) + rs(4)
= 13b
R[rd] = (R[rd] + R[rs]) & 0xFF
相同
00111
(
0x07
)
LOADI r, imm
op(5) + r(4) + imm(8)
= 17b
R[r] = imm
相同
01000
(
0x08
)
JMPR r
op(5) + r(4)
= 9b
pc = R[r] * 8
pc = R[r] * 16
01001
(
0x09
)
MOVR rd, rs
op(5) + rd(4) + rs(4)
= 13b
R[rd] = R[rs]
相同
01010
(
0x0A
)
JMP a16
op(5) + addr(16)
= 21b
pc = addr
相同
01011
(
0x0B
)
XORI r, imm
op(5) + r(4) + imm(8)
= 17b
R[r] ^= imm
相同
01101
(
0x0D
)
PUSH r
op(5) + r(4)
= 9b
stack.push(R[r])
相同
01110
(
0x0E
)
ANDI r, imm
op(5) + r(4) + imm(8)
= 17b
R[r] &= imm
相同
10000
(
0x10
)
JZ r, a16
op(5) + r(4) + addr(16)
= 25b
若
R[r] == 0
则
pc = addr
相同
10001
(
0x11
)
XORR rd, rs
op(5) + rd(4) + rs(4)
= 13b
R[rd] ^= R[rs]
相同
10010
(
0x12
)
EMIT r
op(5) + r(4)
= 9b
输出字节
R[r]
相同
10100
(
0x14
)
LOADC rD, [rA]
op(5) + rD(4) + rA(4)
= 13b
R[rD] = mem[R[rA]]
相同
10101
(
0x15
)
SUBI r, imm
op(5) + r(4) + imm(8)
= 17b
R[r] = (R[r] - imm) & 0xFF
相同
10110
(
0x16
)
POP r
op(5) + r(4)
= 9b
空栈报错，否则
R[r] = stack.pop()
空栈时
R[r] = 0
11000
(
0x18
)
ROLI
/
RORI
op(5) + r(4) + imm(8)
= 17b
循环左移
imm & 7
位
循环右移
imm & 7
位
11100
(
0x1C
)
JNZ r, a16
op(5) + r(4) + addr(16)
= 25b
若
R[r] != 0
则
pc = addr
相同
11111
(
0x1F
)
HALT
op(5)
= 5b
停机
相同
3.4 解密并执行第一阶段
KV
通道字节码（
rev.B
）
关键观察：
ICMP 流量中共包含 39 个以
KV
开头的 Echo Request 数据包（Pkt 209 至 Pkt 285）。根据笔记
2/12
~
5/12
，其格式为
'KV' | u8 seq | u8 len | u8 cksum | data
，使用初始密钥
，递推公式为：
第
seq
号分片中第
字节的解密公式为：
原理与操作：
对 39 个
KV
分片执行解密并验证
。其中来自
10.0.0.13
的 3 个伪造包（Pkt 213、227、243）校验和失败被自动丢弃，来自
10.0.0.5
的 36 个包全部通过校验（包含 4 个重传包），去重并按
seq = 0..31
升序拼接，得到 251 字节的
rev.B
固件字节码。
将该 251 字节送入
rev.B
虚拟机运行：
第一阶段循环（
pc = 0..447
）原地解密偏移
59..178
（
0x3b..0xb2
）的代码（这解释了笔记
12/12
中“反汇编变成乱码说明找对了方向”的自修改特性）。
第二阶段（
pc = 552..747
）计算前 59 字节的校验和并与
0x16
异或比对，防止字节码被篡改（若被篡改则跳转到
pc = 1088
输出假 Flag
flag{fake_patched_s0rry}
）。
第三阶段（
pc = 768..1029
）解密偏移
179..250
（
0xb3..0xfa
）的区域并跳转至
0xb3 * 8 = 1432
。
第四阶段（
pc = 1432..1671
）将偏移
0xd2..0xfa
的 41 字节数据循环左移 3 位、异或
0x5a
及地址偏移后压栈再逆序弹出输出。
本步结果：
rev.B
虚拟机运行 3319 步后在
pc = 1671
处正常停机，输出 41 字节明文：
flag{tw0_c4t
PX rev.C k=9f3cb712aa55d04e
输出给出了前半段 Flag
flag{tw0_c4t
，并指出下一阶段位于 ICMP 的
PX
通道，需使用密钥
k = 9f3cb712aa55d04e
解密并在
rev.C
虚拟机中运行。
3.5 解密并执行第二阶段
PX
通道字节码（
rev.C
）
关键观察：
在 ICMP 流量前段（Pkt 117、119、121、123、125）存在 5 个以
PX
开头的 Echo Request 数据包（由
10.0.0.14
和
10.0.0.5
交替发送，对应前半段 Flag 中的
tw0_c4ts
）：
pkt=117 src=10.0.0.14 seq=0 len=10 cksum=0x50 enc=2d2087dc8b32f1bd270e
pkt=119 src=10.0.0.5  seq=1 len=10 cksum=0x30 enc=ab120bc19c6cf61f7713
pkt=121 src=10.0.0.5  seq=2 len=10 cksum=0x0e enc=0650160eaa2ca91aa952
pkt=123 src=10.0.0.14 seq=3 len=10 cksum=0x37 enc=10feaff6916921ac04b9
pkt=125 src=10.0.0.5  seq=4 len=2  cksum=0x3b enc=80bb
原理与操作：
将
PX
的 5 个分片按
seq = 0..4
顺序拼接得到 42 字节密文
enc_all
，使用第一阶段获得的 8 字节密钥
k = bytes.fromhex("9f3cb712aa55d04e")
进行循环异或解密：
解密得到 42 字节的
rev.C
字节码：
b21c30ce216721f3b8321c00a1944c226923c001ac05c64035101e080307c0b030ca267b8bf9d4f71f87
其首指令为
b2...
（
10110 0100
，即
POP R4
，依赖
rev.C
空栈弹出返回
0
的特性），并结合
JMPR
（乘 16）与
RORI
（循环右移）解密内置数据后逐字节
EMIT
。
本步结果：
送入
rev.C
虚拟机运行 106 步后在
pc = 237
停机，输出后半段 Flag：
s_0ne_tr4p}
将两阶段输出拼接，即得最终完整 Flag
flag{tw0_c4ts_0ne_tr4p}
。
4. 完整解题脚本
将以下脚本保存为
solve.py
，放置在与
capture.pcap
同一目录下（或通过命令行参数传入
capture.pcap
路径）即可直接运行：
import
struct
import
sys
def
parse_and_repair_pcap
(path)
:
with
open(path,
"rb"
)
as
f:
data = f.read()
offset =
24
packets = []
while
offset +
16
<= len(data):
ts_sec, ts_usec, incl_len, orig_len = struct.unpack(
"<IIII"
, data[offset:offset+
16
])
pkt_start = offset +
16
eth_type = struct.unpack(
">H"
, data[pkt_start+
12
:pkt_start+
14
])[
0
]
# 根据二层协议与 IPv4 Total Length 计算真实帧长，绕过损坏的 incl_len
if
eth_type ==
0x0800
:
ip_len = struct.unpack(
">H"
, data[pkt_start+
16
:pkt_start+
18
])[
0
]
real_len =
14
+ ip_len
elif
eth_type ==
0x0806
:
real_len =
42
else
:
real_len = incl_len
packets.append(data[pkt_start:pkt_start+real_len])
offset = pkt_start + real_len
return
packets
def
run_kv_vm
(code_bytes, rev=
"B"
)
:
mem = bytearray(code_bytes) + bytearray(
256
)
regs = [
0
] *
16
stack = []
out = bytearray()
pc =
0
def
get_bits
(pos, n)
:
val =
0
for
i
in
range(n):
val = (val <<
1
) | ((mem[(pos + i) >>
3
] >> (
7
- ((pos + i) &
7
))) &
1
)
return
val
while
True
:
op = get_bits(pc,
5
)
if
op ==
0b11111
:
# HALT
break
elif
op ==
0b00111
:
# LOADI r, imm
regs[get_bits(pc +
5
,
4
)] = get_bits(pc +
9
,
8
)
pc +=
17
elif
op ==
0b10010
:
# EMIT r
out.append(regs[get_bits(pc +
5
,
4
)])
pc +=
9
elif
op ==
0b00011
:
# ADDI r, imm
r = get_bits(pc +
5
,
4
)
regs[r] = (regs[r] + get_bits(pc +
9
,
8
)) &
0xFF
pc +=
17
elif
op ==
0b10101
:
# SUBI r, imm
r = get_bits(pc +
5
,
4
)
regs[r] = (regs[r] - get_bits(pc +
9
,
8
)) &
0xFF
pc +=
17
elif
op ==
0b01011
:
# XORI r, imm
r = get_bits(pc +
5
,
4
)
regs[r] = (regs[r] ^ get_bits(pc +
9
,
8
)) &
0xFF
pc +=
17
elif
op ==
0b01110
:
# ANDI r, imm
r = get_bits(pc +
5
,
4
)
regs[r] = (regs[r] & get_bits(pc +
9
,
8
)) &
0xFF
pc +=
17
elif
op ==
0b11000
:
# ROLI (rev.B) / RORI (rev.C)
r = get_bits(pc +
5
,
4
)
imm = get_bits(pc +
9
,
8
) &
7
v = regs[r]
if
rev ==
"B"
:
regs[r] = ((v << imm) | (v >> (
8
- imm))) &
0xFF
else
:
regs[r] = ((v >> imm) | (v << (
8
- imm))) &
0xFF
pc +=
17
elif
op ==
0b01001
:
# MOVR rd, rs
regs[get_bits(pc +
5
,
4
)] = regs[get_bits(pc +
9
,
4
)]
pc +=
13
elif
op ==
0b10001
:
# XORR rd, rs
rd = get_bits(pc +
5
,
4
)
regs[rd] ^= regs[get_bits(pc +
9
,
4
)]
pc +=
13
elif
op ==
0b00110
:
# ADDR rd, rs
rd = get_bits(pc +
5
,
4
)
regs[rd] = (regs[rd] + regs[get_bits(pc +
9
,
4
)]) &
0xFF
pc +=
13
elif
op ==
0b01101
:
# PUSH r
stack.append(regs[get_bits(pc +
5
,
4
)])
pc +=
9
elif
op ==
0b10110
:
# POP r
r = get_bits(pc +
5
,
4
)
if
not
stack:
if
rev ==
"B"
:
raise
RuntimeError(
"Stack underflow"
)
regs[r] =
0
else
:
regs[r] = stack.pop()
pc +=
9
elif
op ==
0b00001
:
# STOREC [rA], rV
mem[regs[get_bits(pc +
5
,
4
)]] = regs[get_bits(pc +
9
,
4
)]
pc +=
13
elif
op ==
0b10100
:
# LOADC rD, [rA]
regs[get_bits(pc +
5
,
4
)] = mem[regs[get_bits(pc +
9
,
4
)]]
pc +=
13
elif
op ==
0b01010
:
# JMP addr16
pc = get_bits(pc +
5
,
16
)
elif
op ==
0b11100
:
# JNZ r, addr16
r = get_bits(pc +
5
,
4
)
a = get_bits(pc +
9
,
16
)
pc = a
if
regs[r] !=
0
else
pc +
25
elif
op ==
0b10000
:
# JZ r, addr16
r = get_bits(pc +
5
,
4
)
a = get_bits(pc +
9
,
16
)
pc = a
if
regs[r] ==
0
else
pc +
25
elif
op ==
0b01000
:
# JMPR r
pc = regs[get_bits(pc +
5
,
4
)] * (
8
if
rev ==
"B"
else
16
)
else
:
raise
RuntimeError(
f"Unknown opcode
{op:
05
b}
at pc=
{pc}
"
)
return
bytes(out)
def
main
()
:
pcap_path = sys.argv[
1
]
if
len(sys.argv) >
1
else
"capture.pcap"
packets = parse_and_repair_pcap(pcap_path)
print(
f"[*] Parsed
{len(packets)}
packets from
{pcap_path}
"
)
# 1. 提取 KV 与 PX 两个 ICMP Echo Request 通道载荷
kv_pkts = []
px_pkts = []
for
pkt
in
packets:
if
struct.unpack(
">H"
, pkt[
12
:
14
])[
0
] ==
0x0800
and
pkt[
23
] ==
1
:
ihl = (pkt[
14
] &
0x0F
) *
4
icmp = pkt[
14
+ ihl:]
if
icmp[
0
] ==
8
:
# Echo Request
payload = icmp[
8
:]
if
payload.startswith(
b"KV"
):
seq, length, cksum = payload[
2
], payload[
3
], payload[
4
]
kv_pkts.append((seq, length, cksum, payload[
5
:
5
+length]))
elif
payload.startswith(
b"PX"
):
seq = int.from_bytes(payload[
2
:
4
],
"big"
)
length, cksum = payload[
4
], payload[
5
]
px_pkts.append((seq, length, cksum, payload[
6
:
6
+length]))
# 2. 解密并重组 KV 通道 (K_0 = 0xA5)
K = [
0xA5
]
for
_
in
range(
256
):
K.append((K[
-1
] *
31
+
7
) &
0xFF
)
kv_by_seq = {}
for
seq, length, cksum, enc
in
kv_pkts:
plain = bytes(enc[i] ^ ((K[seq] + i) &
0xFF
)
for
i
in
range(length))
if
(sum(plain) &
0xFF
) == cksum
and
seq
not
in
kv_by_seq:
kv_by_seq[seq] = plain
kv_rom =
b""
.join(kv_by_seq[s]
for
s
in
sorted(kv_by_seq))
print(
f"[*] Reassembled KV bytecode:
{len(kv_rom)}
bytes (seqs 0..
{max(kv_by_seq)}
)"
)
kv_out = run_kv_vm(kv_rom, rev=
"B"
).decode()
print(
"[*] Stage 1 (KV rev.B) output:"
)
print(kv_out.strip())
lines = kv_out.strip().splitlines()
flag_part1 = lines[
0
]
px_key = bytes.fromhex(lines[
1
].split(
"k="
)[
1
])
# 3. 使用第一阶段输出的密钥解密 PX 通道并在 rev.C 虚拟机上执行
px_enc =
b""
.join(enc
for
_, _, _, enc
in
sorted(px_pkts, key=
lambda
x: x[
0
]))
px_rom = bytes(px_enc[i] ^ px_key[i % len(px_key)]
for
i
in
range(len(px_enc)))
print(
f"[*] Reassembled PX bytecode:
{len(px_rom)}
bytes"
)
flag_part2 = run_kv_vm(px_rom, rev=
"C"
).decode()
print(
"[*] Stage 2 (PX rev.C) output:"
)
print(flag_part2)
print(
f"\n[+] Flag:
{flag_part1}
{flag_part2}
"
)
if
__name__ ==
"__main__"
:
main()
