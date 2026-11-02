---
title: 'FilmReader-镜像取证'
contest: '强网拟态防御 第九届'
contest_normalized: '强网拟态防御 第九届'
contest_year: 2025
year: 2025
category: 'misc'
subcategory: 'misc_other'
tags: []
attack_chain:
- '题目说明'
- '解题思路'
- 'x1ffffff'
- '解题过程'
- '从目录项空隙读出被删缓存'
- 'xF30A'
one_liner: '题目描述：镜像取证'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/iTgaxzumnH3cE4N5nH6VvQ'
last_verified: '2026-11-02'
flag_observed:
- 'flag{f1r57_c4ch3_15_4_dr4ft}'
- 'flag{n0_m0d3l_r34d5_7h15_d33p}'
- 'flag{r34d_h00k_d3crypt5_3v3ryth1ng}'
contest_normalized: "强网拟态"
---

FilmReader-镜像取证
题目描述：镜像取证
附件：shadowread.zip
核心思路：
flag.txt
是安慰奖。无参加载的模块把
read
拐到已删除的
.real_cache
，目录项空隙里 inode 和 extent 都还在，按模块自己的密钥派生和字节码虚拟机解密就是正稿。
1. 题目说明
题目给的是一块 512MiB 的 ext4 镜像
shadowread.img
（536870912 字节），卷标
shadowread
，块大小 4096。要恢复的是用户真正读到的 flag，不是磁盘上
flag.txt
直接变换出来的那一串。
镜像里和本题有关的明文材料有三份。
/home/ctf/note.txt
：
你看到的是影子。
cat 没有骗你,骗你的是 read。真的东西我搬走了,
磁盘上这份 flag.txt 是留给你们的安慰奖——
它确实能解出一面 flag,但那面是假的,别浪费提交次数。
原来的文件?删了,早就删了。
不过这块盘子记性不太好,删掉的东西,它自己还会念叨一阵子。
钥匙也删了——碎成四瓣,跟那几瓣缓存躺在一起。
哪瓣是真的?我的垫片记得,可惜它也跟着失忆了。
对了,那文件我一共写过两版——草稿和正稿我分得很清,希望你也是。
—— ph4nt0m
/var/log/auth.log
里这次会话实际执行的命令是：
2026-10-11T03:13:02+08:00 portal-srv sudo:      ctf : TTY=pts/0 ; PWD=/home/ctf ; USER=root ; COMMAND=/usr/bin/insmod /usr/local/bin/kcompat.ko
2026-10-11T03:13:44+08:00 portal-srv sudo:      ctf : TTY=pts/0 ; PWD=/home/ctf ; USER=root ; COMMAND=/bin/cat /home/ctf/flag.txt
2026-10-11T03:14:02+08:00 portal-srv sudo:      ctf : TTY=pts/0 ; PWD=/home/ctf ; USER=root ; COMMAND=/bin/rm /var/.cache/.kmod/.real_cache.bak
2026-10-11T03:14:20+08:00 portal-srv sudo:      ctf : TTY=pts/0 ; PWD=/home/ctf ; USER=root ; COMMAND=/bin/rm /var/.cache/.kmod/.real_cache
2026-10-11T03:14:35+08:00 portal-srv sudo:      ctf : TTY=pts/0 ; PWD=/home/ctf ; USER=root ; COMMAND=/bin/rm -f /var/.cache/.kmod/.s* /var/.cache/.kmod/.k*
insmod
没有模块参数。模块本体还在
/usr/local/bin/kcompat.ko
。
/home/ctf/flag.txt
仍是 40 字节，但
/var/.cache/.kmod/
下的缓存和四瓣钥匙已经从目录里删掉。
2. 解题思路
note 把三件事说死了：
cat
看到的内容被
read
掉了包，磁盘上的
flag.txt
能解出一面假 flag，真文件和四瓣钥匙都删了，而且真文件有草稿、正稿两版。
kcompat.ko
的 init 在拨码大于 2 时读取
.s1
、
.s2
、
.s3
的前 4 字节，用
.s2[0] & 3
决定
.k0
到
.k3
里的哪一瓣，拼成 16 字节后做 SHA-256，再把摘要迭代
0x1ffffff
次。摘要后 16 字节必须等于
.rodata
里的一份校验值。前 16 字节是虚拟机密钥，它的低 32 位再用来解开同一节里的 448 字节字节码。
read hook 只认文件名
flag.txt
。密钥派生成功后，它不再读
/home/ctf/flag.txt
，而是打开
/var/.cache/.kmod/.real_cache
，按 8 字节交给
.text+0x10
的栈虚拟机。未武装时的回退才是对
flag.txt
本身做减、循环右移、异或，那一串就是 note 里的安慰奖。
这些缓存文件的目录项已经被合并进前一项的
rec_len
，名字还留在空隙里，extent 也没有回收。日志超级块显示 journal 从 block 0 开始，没有另一份待回放的旧数据。直接按现存 inode 读出
.real_cache
再跑模块里的解密，得到的才是正稿。
.real_cache.bak
用同一把密钥解出草稿。
3. 解题过程
3.1 从目录项空隙读出被删缓存
ext4 删除目录项时通常不立刻清掉名字，而是把这项的空间并进前一个存活项的
rec_len
。inode 号和文件名仍按 4 字节对齐留在这块空隙里。这些 inode 的
i_block
仍是一棵深度为 0 的 extent 树，魔数
0xF30A
，逻辑块还指向原来的数据块。
对 journal 数据块做
debugfs logdump
，得到的都是：
Journal starts at block 0, transaction 7
journal 没有停在半截事务上，删掉的内容不需要从日志里重放。从根 inode 2 走目录，把空隙中的名字也当成子项，就能读回
/var/.cache/.kmod/
下的全部缓存：
路径
长度
/var/.cache/.kmod/.real_cache
32
/var/.cache/.kmod/.real_cache.bak
32
/var/.cache/.kmod/.s1
、
.s2
、
.s3
各 64
/var/.cache/.kmod/.k0
到
.k3
各 64
/home/ctf/flag.txt
40
同目录里还有
.s1.bak
、
.s1.old
、
.s2.bak
、
.s3.bak
。模块解码出来的路径没有这些后缀，它们不参与密钥派生。
3.2 确认默认拨码会改读
.real_cache
objdump
把模块里的重定位显示成
rip+0x0
，不能单靠那条指令看出比较的是哪个符号。
.data+0x9b8
处的有符号整数是 4，而
insmod
没有传参，加载后用的就是这个默认值。init 在该值大于 2 时才进入读缓存、做 SHA-256、核对摘要的路径。后面摘要核对成功，说明镜像上实际走的就是这条路径。
.rodata+0x130
起是一组用
0xc3
逐字节异或的 C 字符串，解码后是：
/var/.cache/.kmod/.k
/var/.cache/.kmod/.s3
/var/.cache/.kmod/.s2
/var/.cache/.kmod/.s1
/var/.cache/.kmod/.real_cache
/home/ctf/flag.txt
init 加载时把这些路径解回明文。read hook 在
.text+0xe10
。它先要求读取长度落在
1 .. 0x400000
，拨码大于 1，目标是普通文件，目录项名字正好是小端常数
0x7478742e67616c66
（
flag.txt
），名字长度 8。拨码不大于 2 时，钩子把文件还回去，调用原来的 read。
拨码大于 2 以后还要看 init 有没有把武装标志置 1。这个标志只在摘要校验通过、448 字节字节码就地解密完成之后才写成 1。置位后的分支不再读用户打开的
flag.txt
，而是
filp_open
上面那条
.real_cache
，把读到的内容按 8 字节送进虚拟机。因此
cat /home/ctf/flag.txt
显示的是
.real_cache
的明文，不是磁盘上那 40 字节。
3.3 用
.s2[0]
的低两位选出
.k2
拨码大于 2 时，init 对三条
.s*
路径各读 4 字节，放进栈上的 16 字节缓冲区：
rsp+0x10  第一份 4 字节
rsp+0x14  第二份 4 字节
rsp+0x18  第三份 4 字节
接着取
rsp+0x14
的第一个字节，
and 3
，加上
0x30
，接到
.k
路径末尾，再读这个路径的前 4 字节放到
rsp+0x1c
。
.s2
的首字节是
0xb6
，
0xb6 & 3 = 2
，所以第四份是
.k2
的前 4 字节。
.k0
、
.k1
、
.k3
不进入材料。
16 字节材料是：
3f9a2c71 b6567e02 d8c10f99 27e6a450
依次对应
.s1
、
.s2
、
.s3
、
.k2
的前 4 字节。init 先对这 16 字节做一次 SHA-256，再对得到的 32 字节摘要重复哈希
0x1ffffff
次（
r12d
初值
0x1ffffff
，每次
dec
后继续）。摘要为：
a65dc30a337a3faee5a58c868fc3e715e3b9cbcd45c9fcec9fd1f00a1f4a2371
校验使用后 16 字节
e3b9cbcd45c9fcec9fd1f00a1f4a2371
。
.rodata+0x3c0
的 16 字节逐字节异或
0xa6
之后与它相同，init 才会把前 16 字节
a65dc30a337a3faee5a58c868fc3e715
留作虚拟机密钥，并继续解密字节码。
3.4 按
mov ebx, eax
的零扩展解开字节码
字节码是
.rodata+0x200
起的
0x1c0
字节。密钥流是 64 位 LCG，乘数
0x5851f42d4c957f2d
，加数
0x14057b7ef767814f
。初态不能先把高 32 位或成
0x5a5a5a5a
再对整个 64 位异或：init 的指令是
mov    ebx, eax
movabs rax, 0x5a5a5a5a5a5a5a5a
xor    rbx, rax
mov ebx, eax
会把高 32 位清零。
eax
是摘要的低 32 位
0xa65dc30a
，异或之后的初态是
((0xa65dc30a ^ 0x5a5a5a5a) | (0x5a5a5a5a << 32))
高 32 位保持
0x5a5a5a5a
。若先或再异或，高半部会被清掉，虚拟机收到的就不是这 448 字节明文，缓存也不会被改写。
每个输出字节都先做一次
state = state * 0x5851f42d4c957f2d + 0x14057b7ef767814f
再取
state >> 56
与密文字节异或。循环上界是
0x1c0
，和这段字节码的长度一致。
3.5 用栈虚拟机解密正稿
虚拟机在
.text+0x10
。read hook 为每个 8 字节块准备 64 字节缓冲区：前 16 字节是摘要密钥，偏移 16 处放当前密文。调用约定就是
rdi
指向这块缓冲区。返回值是 0 时，钩子把偏移 16 的 8 字节写回用户缓冲区；剩余长度不足 8 的尾巴不进入虚拟机。
解释器的状态是：
累加器初值
0xffffffa5
。操作码等于
code[pc] ^ (acc & 0xff)
，每执行一条指令后
acc = (acc * 0x6d + 0x3b) & 0xffffffff
。
64 个 32 位栈槽。
0x01
压入立即数 dword，
0x02
压入立即数字节，
0x07
/
0x08
从缓冲区按字节或小端 dword 读取，
0x09
/
0x0a
按字节或 dword 写回。地址都
& 0x3f
，所以读写不出这 64 字节。
0x0b
到
0x13
是加、减、异或、与、或、左移、逻辑右移、循环右移和乘法，运算宽度 32 位。
0x1a
返回 0。步数超过
0x30d40
或程序计数器超过
0x1bf
则失败，钩子保留原密文。
同一段字节码、同一把 16 字节密钥解两份 32 字节缓存：
文件
明文
含义
.real_cache
flag{n0_m0d3l_r34d5_7h15_d33p}
钩子实际打开的正稿
.real_cache.bak
flag{f1r57_c4ch3_15_4_dr4ft}
先被删掉的草稿
正稿 30 字节，后面两个 NUL；草稿 28 字节，后面四个 NUL。两者都落在各自文件的 32 字节里。
3.6 把磁盘上的
flag.txt
解成安慰奖，但不提交
武装标志为 0 时，钩子仍会读原始文件，读到正数个字节后走
.text+0x11ea
。那里
ebx
从 3 开始，对每个下标
i
：
b = ror8((b - table[ebx % 20]) & 0xff, i)
b ^= table[i % 20]
ebx += 7
table
是
.rodata+0x100
的 20 字节
sh4d0w_1n_7h3_k3rn3l
。字节旋转只使用计数的低 3 位。默认拨码是 4 且摘要校验已经通过，这次
cat
不会走这条回退。把磁盘上的 40 字节
flag.txt
送进同一变换，得到
flag{r34d_h00k_d3crypt5_3v3ryth1ng}
这就是 note 说的安慰奖。它格式完整，但不是 read hook 交还给
cat
的那一串。
4. 完整解题脚本
依赖 Python 标准库。脚本自己解析 ext4 和 ELF，从镜像读出被删缓存与
kcompat.ko
，完成密钥派生、字节码解密和虚拟机解密。
0x1ffffff
次 SHA-256 是主要耗时。
#!/usr/bin/env python3
"""Recover the real flag from the shadowread ext4 image.
The module's default dial is high enough to ignore flag.txt and decrypt
/var/.cache/.kmod/.real_cache. Deleted cache inodes are still allocated, so
their bytes can be read without replaying the journal.
"""
import
argparse
import
hashlib
import
pathlib
import
struct
DEFAULT_IMAGE = pathlib.Path(
r"C:\Users\34645\Downloads\shadowread\shadowread.img"
)
class
Ext4
:
def
__init__
(self, blob: bytes)
->
None
:
self.blob = blob
superblock = blob[
1024
:
2048
]
self.block_size =
1024
<< struct.unpack_from(
"<I"
, superblock,
0x18
)[
0
]
self.inodes_per_group = struct.unpack_from(
"<I"
, superblock,
0x28
)[
0
]
self.inode_size = struct.unpack_from(
"<H"
, superblock,
0x58
)[
0
]
incompat = struct.unpack_from(
"<I"
, superblock,
0x60
)[
0
]
self.desc_size = struct.unpack_from(
"<H"
, superblock,
0xFE
)[
0
]
if
incompat &
0x80
else
32
self.volume = superblock[
0x78
:
0x88
].split(
b"\x00"
,
1
)[
0
].decode()
def
inode_raw
(self, number: int)
-> tuple[bytes, int]:
group = (number -
1
) // self.inodes_per_group
index = (number -
1
) % self.inodes_per_group
desc_off = self.block_size + group * self.desc_size
desc = self.blob[desc_off:desc_off + self.desc_size]
table = struct.unpack_from(
"<I"
, desc,
8
)[
0
]
if
self.desc_size >=
64
:
table |= struct.unpack_from(
"<I"
, desc,
40
)[
0
] <<
32
off = table * self.block_size + index * self.inode_size
raw = self.blob[off:off + self.inode_size]
size = struct.unpack_from(
"<I"
, raw,
4
)[
0
]
if
self.inode_size >=
0x70
:
size |= struct.unpack_from(
"<I"
, raw,
0x6C
)[
0
] <<
32
return
raw, size
def
read_inode
(self, number: int)
-> bytes:
raw, size = self.inode_raw(number)
magic, entries, _, depth, _ = struct.unpack_from(
"<HHHHI"
, raw,
0x28
)
if
magic !=
0xF30A
or
depth !=
0
:
raise
RuntimeError(
f"inode
{number}
: unexpected extent header
{magic:
#x
}
depth
{depth}
"
)
out = bytearray()
for
entry
in
range(entries):
logical, length, start_hi, start_lo = struct.unpack_from(
"<IHHI"
, raw,
0x34
+ entry *
12
)
del
logical
start = start_lo | (start_hi <<
32
)
for
block
in
range(length &
0x7FFF
):
at = (start + block) * self.block_size
out += self.blob[at:at + self.block_size]
if
len(out) >= size:
return
bytes(out[:size])
return
bytes(out[:size])
def
directory_entries
(data: bytes)
-> list[tuple[int, str, bool]]:
"""Return (inode, name, deleted). Deleted names survive inside an enlarged rec_len."""
found = []
position =
0
while
position +
8
<= len(data):
inode, rec_len, name_len, _ = struct.unpack_from(
"<IHBB"
, data, position)
if
rec_len <
8
or
position + rec_len > len(data):
break
if
inode
and
name_len:
found.append((inode, data[position +
8
:position +
8
+ name_len].decode(
"latin1"
),
False
))
slack = position + ((
8
+ name_len +
3
) & ~
3
)
end = position + rec_len
while
slack +
8
<= end:
hidden_inode, _, hidden_len, _ = struct.unpack_from(
"<IHBB"
, data, slack)
if
hidden_len ==
0
or
slack +
8
+ hidden_len > end
or
not
hidden_inode:
break
found.append((hidden_inode, data[slack +
8
:slack +
8
+ hidden_len].decode(
"latin1"
),
True
))
slack += (
8
+ hidden_len +
3
) & ~
3
position += rec_len
return
found
def
walk
(fs: Ext4)
-> dict[str, bytes]:
files: dict[str, bytes] = {}
def
visit
(inode: int, path: str)
->
None
:
raw, size = fs.inode_raw(inode)
mode = struct.unpack_from(
"<H"
, raw,
0
)[
0
]
body = fs.read_inode(inode)
if
mode &
0x4000
:
for
child, name, _deleted
in
directory_entries(body):
if
name
in
(
"."
,
".."
):
continue
visit(child,
f"
{path}
/
{name}
"
)
return
if
mode &
0x8000
:
files[path] = body
del
size
visit(
2
,
""
)
return
files
def
elf_section
(blob: bytes, wanted: str)
-> bytes:
shoff = struct.unpack_from(
"<Q"
, blob,
40
)[
0
]
shentsize = struct.unpack_from(
"<H"
, blob,
58
)[
0
]
shnum = struct.unpack_from(
"<H"
, blob,
60
)[
0
]
shstrndx = struct.unpack_from(
"<H"
, blob,
62
)[
0
]
def
header
(index: int)
-> tuple:
return
struct.unpack_from(
"<IIQQQQIIQQ"
, blob, shoff + index * shentsize)
names = blob[header(shstrndx)[
4
]:header(shstrndx)[
4
] + header(shstrndx)[
5
]]
for
index
in
range(shnum):
name_off, _, _, _, offset, size, *_ = header(index)
name = names[name_off:names.index(
b"\x00"
, name_off)].decode()
if
name == wanted:
return
blob[offset:offset + size]
raise
KeyError(wanted)
def
ror8
(value: int, count: int)
-> int:
count &=
7
value &=
0xFF
if
count ==
0
:
return
value
return
((value >> count) | (value << (
8
- count))) &
0xFF
def
consolation
(data: bytes, table: bytes)
-> bytes:
"""dial == 0: sub, rotate right, xor. This is the planted fake flag."""
state =
3
out = bytearray(data)
for
index, value
in
enumerate(out):
value = (value - table[state %
20
]) &
0xFF
value = ror8(value, index)
value ^= table[index %
20
]
out[index] = value
state +=
7
return
bytes(out)
def
derive_key
(material: bytes)
-> bytes:
digest = hashlib.sha256(material).digest()
for
_
in
range(
0x1FFFFFF
):
digest = hashlib.sha256(digest).digest()
return
digest
def
decrypt_bytecode
(blob: bytes, key_lo: int)
-> bytes:
# mov ebx, eax zeros the high half, then xor rbx, 0x5a5a5a5a5a5a5a5a.
state = ((key_lo &
0xFFFFFFFF
) ^
0x5A5A5A5A
) | (
0x5A5A5A5A
<<
32
)
multiplier =
0x5851F42D4C957F2D
increment =
0x14057B7EF767814F
mask = (
1
<<
64
) -
1
out = bytearray(blob)
for
index
in
range(len(out)):
state = (state * multiplier + increment) & mask
out[index] ^= (state >>
56
) &
0xFF
return
bytes(out)
def
run_vm
(code: bytes, memory: bytearray)
-> int:
acc =
0xFFFFFFA5
pc =
0
sp =
0
flag =
0
stack = [
0
] *
64
steps =
0
while
True
:
steps +=
1
if
steps >
0x30D40
or
pc >
0x1BF
:
return
-1
op = code[pc] ^ (acc &
0xFF
)
if
op ==
0x1
:
stack[sp] = struct.unpack_from(
"<I"
, code, pc +
1
)[
0
]
sp +=
1
pc +=
5
elif
op ==
0x2
:
stack[sp] = code[pc +
1
]
sp +=
1
pc +=
2
elif
op ==
0x3
:
sp -=
1
pc +=
1
elif
op ==
0x4
:
stack[sp] = stack[sp -
1
]
sp +=
1
pc +=
1
elif
op ==
0x5
:
stack[sp -
1
], stack[sp -
2
] = stack[sp -
2
], stack[sp -
1
]
pc +=
1
elif
op ==
0x6
:
stack[sp] = stack[sp -
2
]
sp +=
1
pc +=
1
elif
op ==
0x7
:
stack[sp -
1
] = memory[stack[sp -
1
] &
0x3F
]
pc +=
1
elif
op ==
0x8
:
stack[sp -
1
] = struct.unpack_from(
"<I"
, memory, stack[sp -
1
] &
0x3F
)[
0
]
pc +=
1
elif
op ==
0x9
:
memory[stack[sp -
2
] &
0x3F
] = stack[sp -
1
] &
0xFF
sp -=
2
pc +=
1
elif
op ==
0xA
:
struct.pack_into(
"<I"
, memory, stack[sp -
2
] &
0x3F
, stack[sp -
1
] &
0xFFFFFFFF
)
sp -=
2
pc +=
1
elif
0xB
<= op <=
0x13
:
left = stack[sp -
2
] &
0xFFFFFFFF
right = stack[sp -
1
] &
0xFFFFFFFF
count = right &
31
if
op ==
0xB
:
result = (left + right) &
0xFFFFFFFF
elif
op ==
0xC
:
result = (left - right) &
0xFFFFFFFF
elif
op ==
0xD
:
result = left ^ right
elif
op ==
0xE
:
result = left & right
elif
op ==
0xF
:
result = left | right
elif
op ==
0x10
:
result = (left << count) &
0xFFFFFFFF
elif
op ==
0x11
:
result = left >> count
elif
op ==
0x12
:
result = ((left >> count) | (left << ((
32
- count) &
31
))) &
0xFFFFFFFF
if
count
else
left
else
:
result = (left * right) &
0xFFFFFFFF
sp -=
1
stack[sp -
1
] = result
pc +=
1
elif
op
in
(
0x15
,
0x16
,
0x17
,
0x18
):
target = pc +
2
+ struct.unpack_from(
"b"
, code, pc +
1
)[
0
]
if
op ==
0x15
:
pc = target
elif
op ==
0x16
:
sp -=
1
pc = target
if
stack[sp] ==
0
else
pc +
2
elif
op ==
0x17
:
sp -=
1
pc = target
if
stack[sp] !=
0
else
pc +
2
else
:
flag = (flag -
1
) &
0xFF
pc = target
if
flag !=
0
else
pc +
2
elif
op ==
0x19
:
flag = code[pc +
1
]
pc +=
2
elif
op ==
0x1A
:
return
0
elif
op ==
0x1B
:
stack[sp] = flag
sp +=
1
pc +=
1
else
:
return
-1
acc = (acc *
0x6D
+
0x3B
) &
0xFFFFFFFF
def
vm_decrypt
(code: bytes, key: bytes, blob: bytes)
-> bytes:
out = bytearray(blob)
for
offset
in
range(
0
, len(out) -
7
,
8
):
memory = bytearray(
64
)
memory[:
16
] = key
memory[
16
:
24
] = out[offset:offset +
8
]
if
run_vm(code, memory) ==
0
:
out[offset:offset +
8
] = memory[
16
:
24
]
return
bytes(out)
def
main
()
->
None
:
parser = argparse.ArgumentParser()
parser.add_argument(
"--image"
, type=pathlib.Path, default=DEFAULT_IMAGE)
args = parser.parse_args()
fs = Ext4(args.image.read_bytes())
files = walk(fs)
print(
f"volume
{fs.volume}
block
{fs.block_size}
"
)
cache = {path: body
for
path, body
in
files.items()
if
"/.kmod/"
in
path
or
path.endswith(
"flag.txt"
)}
for
path
in
sorted(cache):
print(
f"file
{path}
{len(cache[path])}
"
)
rodata = elf_section(files[
"/usr/local/bin/kcompat.ko"
],
".rodata"
)
data = elf_section(files[
"/usr/local/bin/kcompat.ko"
],
".data"
)
dial = struct.unpack_from(
"<i"
, data,
0x9B8
)[
0
]
table = rodata[
0x100
:
0x115
]
paths = []
cursor =
0x130
while
cursor <
0x1F0
:
end = rodata.index(
b"\x00"
, cursor)
paths.append(bytes(byte ^
0xC3
for
byte
in
rodata[cursor:end]))
cursor = end +
1
while
cursor <
0x1F0
and
rodata[cursor] ==
0
:
cursor +=
1
print(
"dial"
, dial)
print(
"paths"
, [item.decode()
for
item
in
paths])
s1 = files[
"/var/.cache/.kmod/.s1"
]
s2 = files[
"/var/.cache/.kmod/.s2"
]
s3 = files[
"/var/.cache/.kmod/.s3"
]
shard = s2[
0
] &
3
key_file = files[
f"/var/.cache/.kmod/.k
{shard}
"
]
material = s1[:
4
] + s2[:
4
] + s3[:
4
] + key_file[:
4
]
digest = derive_key(material)
expect = bytes(byte ^
0xA6
for
byte
in
rodata[
0x3C0
:
0x3D0
])
print(
f"selector s2[0]&3 =
{shard}
"
)
print(
"material"
, material.hex())
print(
"digest"
, digest.hex())
print(
"check"
, digest[
16
:].hex(),
"match"
, digest[
16
:] == expect)
code = decrypt_bytecode(rodata[
0x200
:
0x3C0
], struct.unpack_from(
"<I"
, digest,
0
)[
0
])
key = digest[:
16
]
real = vm_decrypt(code, key, files[
"/var/.cache/.kmod/.real_cache"
])
draft = vm_decrypt(code, key, files[
"/var/.cache/.kmod/.real_cache.bak"
])
fake = consolation(files[
"/home/ctf/flag.txt"
], table)
print(
"real"
, real)
print(
"draft"
, draft)
print(
"consolation"
, fake)
if
__name__ ==
"__main__"
:
main()
函数
consolation
的注释把这条回退写成
dial == 0
。反汇编里它是武装标志未置位时的变换；默认拨码为 4 且校验通过时不会执行。脚本仍计算它，只为把安慰奖和正稿分开。
