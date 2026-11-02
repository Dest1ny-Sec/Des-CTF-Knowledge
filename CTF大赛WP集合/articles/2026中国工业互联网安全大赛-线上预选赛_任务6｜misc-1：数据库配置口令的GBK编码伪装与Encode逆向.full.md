---
title: '任务6｜misc-1：数据库配置口令的GBK编码伪装与Encode逆向'
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
- 'return'
- 'while'
one_liner: '附件'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w'
last_verified: '2026-11-02'
flag_observed:
- 'flag{2025_DLB_Crypt}'
subcategory_guess: "reverse"
---

任务6｜misc-1：数据库配置口令的GBK编码伪装与Encode逆向
附件
：任务6.zip（db_config.sys、encode.png）
1. 基本情况
附件两份文件的后缀均与实际类型不符。db_config.sys仅256字节，文件头为5B 64 62 20即ASCII的“[db ”，实为CRLF行尾的INI数据库配置；encode.png魔数为FF D8 FF E0，实为1149×425的JPEG截图，画面是IDA反编译的Encode函数。配置中service_1指向mdb、user_name为D5000、db_name为ems，只有user_password的值是一串生僻汉字，落盘42字节。目标是由这段汉字还原明文口令，再套flag格式。
2. 关键突破
Encode的原型为int __cdecl Encode(char *SoursePasswd, char *TargetPasswd)，以i从0遍历源串，每字节写出两个字节：TargetPasswd[2i]=((SoursePasswd[i]>>4)+0x80)^0x6C，TargetPasswd[2i+1]=((SoursePasswd[i]&0x0F)+0x80)^0x6E，循环后在2i处写0。一个明文字节被拆成高低半字节，密文长度恰为两倍且无损。
值域决定了伪装必然成立。半字节n加0x80等价于0x80|n，高四位恒为8；异或0x6C或0x6E（高四位均为6）后高四位固定为0xE，低四位是n与常量低四位的异或，仍为0至15的排列。因此两个密文字节都严格落在0xE0至0xEF，恰被GBK双字节区覆盖，任意ASCII口令都能变成合法汉字串。实测14字节只取到部分值，不能把实测区间当成理论值域。
落盘链路是把密文字节按GBK解码成汉字，再以UTF-8写入配置。42字节正好是14个三字节UTF-8序列，对应GBK下28字节，两种编码的长度严格保持3:2。逆向时须先按UTF-8宽度切出每个字符，再回查GBK双字节，不能直接对整串解码。
3. 利用/还原思路
读文件头判型：db_config.sys无常见魔数，但首字节为“[”且可整段UTF-8解码，判为INI；encode.png以FF D8 FF E0开头，判为JPEG。
在原始字节流定位
user_password=
，向后取到第一个0x0D，得42字节，字段值起始偏移73，全程不做解码。
手工走UTF-8：首字节高4位为1110则宽度3，取两个10xxxxxx续字节拼码点，共14个字符，宽度集合为{3}。
遍历GBK首字节0x81至0xFE、尾字节0x40至0xFE并跳过0x7F，只保留解出单字符的组合，建立21791项字符到双字节的索引。
逐字查表得(t0,t1)，按hi=(t0^0x6C)-0x80、lo=(t1^0x6E)-0x80还原，检查均在0至15内，拼(hi<<4)|lo。首字“鞬”U+956C的GBK为EF EC，算得0x32即字符“2”。
正向复算：对还原出的口令重跑Encode，再GBK解码、UTF-8编码，所得42字节须与文件字段逐字节相同且CRC32同为95aca49d。
明文为2025_DLB_Crypt，即flag{2025_DLB_Crypt}。
4. 复现脚本
import
binascii
FIELD =
b"user_password="
def
field
(blob, key)
:
s = blob.find(key) + len(key)
e = s
while
blob[e]
not
in
(
0x0D
,
0x0A
):
e +=
1
return
s, blob[s:e]
def
walk
(buf)
:
i =
0
while
i < len(buf):
b0 = buf[i]
w =
3
if
b0 >>
4
==
0xE
else
2
if
b0 >>
5
==
0x6
else
1
cp = b0 & (
0x0F
if
w ==
3
else
0x1F
if
w ==
2
else
0x7F
)
for
k
in
range(
1
, w):
cp = cp <<
6
| buf[i + k] &
0x3F
yield
cp
i += w
def
gbk_index
()
:
idx = {}
for
h
in
range(
0x81
,
0xFF
):
for
l
in
range(
0x40
,
0xFF
):
if
l ==
0x7F
:
continue
try
:
ch = bytes([h, l]).decode(
"gbk"
)
except
UnicodeDecodeError:
continue
if
len(ch) ==
1
:
idx[ch] = (h, l)
return
idx
blob = open(
"db_config.sys"
,
"rb"
).read()
off, raw = field(blob, FIELD)
idx = gbk_index()
plain = bytes(((idx[chr(c)][
0
] ^
0x6C
) -
0x80
) <<
4
|
((idx[chr(c)][
1
] ^
0x6E
) -
0x80
)
for
c
in
walk(raw))
back =
b""
.join(bytes([((b >>
4
) +
0x80
) ^
0x6C
,
((b &
15
) +
0x80
) ^
0x6E
]).decode(
"gbk"
).encode()
for
b
in
plain)
print(off, len(raw), len(idx), binascii.crc32(raw) == binascii.crc32(back), plain)
5. 运行结果
[*] user_password 位于偏移 73，占 42 字节
[*] GBK双字节索引 21791 项；UTF-8分段 14 个字符，宽度集合 [3]
[+] 还原明文口令：2025_DLB_Crypt
[+] 回环 CRC32 95aca49d 校验通过
[=] flag{2025_DLB_Crypt}
6. 小结
后缀伪装只误导第一步，真正难点是密文字节先被GBK解释、再以UTF-8落盘；半字节混淆本身不构成加密。
最终flag
flag{2025_DLB_Crypt}
