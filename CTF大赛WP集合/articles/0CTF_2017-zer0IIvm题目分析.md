# 0CTF 2017-zer0IIvm题目分析

> 原文: https://www.ctfiot.com/44501.html
> ID: 44501

【原理】

分析llvm的混淆插件，定位到主要函数flatten()，通过交叉引用快速定位prng_seed。通过硬编码的crc32来爆破出key的前三位

AES_PRECOMP_TE[i](x) = MixColumns(SBox(x) << 8*i)

scramble32是XorKey、SubBytes、MixColumn后跟另一个XorKey的 4 轮迭代

通过泄漏的key前三位来逐个爆破aes的key

【工具】

ida,python sage,python aes,gdb

【步骤】

在这个题中，我们拿到了一个用于 llvm 的混淆插件和一个混淆的二进制文件。该插件接受一个 16 字节的种子作为参数并将其用于内部 PRNG。我们的目标是分析二进制文件并从中恢复种子。

main函数：

.text:
4004C0 main:           ; DATA XREF: _start+1D

.text:
4004C0     push rbp

.text:
4004C1     mov  rbp, rsp

.text:
4004C4     sub  rsp, 4038Ch

.text:
4004CB     mov  dword ptr [rbp-4], 0

.text:
4004D2     mov  dword ptr [rbp-8], 46544330h

.text:
4004D9     mov  dword ptr [rbp-0Ch], 4E52BCE7h

.text:
4004E0

.text:
4004E0 main_switch:       ; CODE XREF: .text:
loc_7635AC

.text:
4004E0     mov  eax, [rbp-0Ch]

.text:
4004E3     mov  ecx, eax

.text:
4004E5     sub  ecx, 8000DEEAh

.text:
4004EB     mov  [rbp-10h], eax

.text:
4004EE     mov  [rbp-14h], ecx

.text:
4004F1     jz   loc_728049

.text:
4004F7     jmp  $+5

.text:
4004FC

.text:
4004FC loc_4004FC:        ; CODE XREF: .text:
00000000004004F7

.text:
4004FC     mov  eax, [rbp-10h]

.text:
4004FF     sub  eax, 8001EACAh

.text:
400504     mov  [rbp-18h], eax

.text:
400507     jz   loc_73E38A

.text:
40050D     jmp  $+5

.text:
400512

.text:
400512 loc_400512:        ; CODE XREF: .text:
000000000040050D

.text:
400512     mov  eax, [rbp-10h]

.text:
400515     sub  eax, 8003CC64h

.text:
40051A     mov  [rbp-1Ch], eax

.text:
40051D     jz   loc_5C0C95

.text:
400523     jmp  $+5

…

对应伪代码：

state = 0x4E52BCE7

main_switch:

switch(state) {

case 0x8000DEEA: goto loc_728049;

case 0x8001EACA: goto loc_73E38A;

case 0x8003CC64: goto loc_5C0C95;

…

}

loc_xxxxxx:

// do something

state = 0x8003CC64

goto main_switch

没得到什么比较有用的信息，来先看看混淆插件。

lib0opsPass.so

函数列表可以发现一个相当大的函数 Oops::
OopsFlattening::
flatten(). 通过cross-references可以迅速定位相关函数

调用 prng_seed 初始化PRNG

Oops::
CryptoUtils::
prng_seed(cryptoutils, &seed_string);

用PRNG生成16字节

memset(&key, 0, 0x20uLL);

LODWORD(cryptoutils_) = llvm::
ManagedStatic<Oops::
CryptoUtils>::
operator->(&Oops::
Oopscryptoutils, 0LL);

Oops::
CryptoUtils::
get_bytes(cryptoutils_, &key, 16);

if ( crc32(‘FTC0’, &key, 3) != 0xF9E319A6 )

…

hardcoded crc32 check可以很容易得到前三个字节: 179, 197, 140.

key 用来混淆plains数组:

LODWORD(plains0) = plains[0];

LODWORD(v35) = llvm::
ManagedStatic<Oops::
CryptoUtils>::
operator->(&Oops::
Oopscryptoutils, v33);

v36 = plains0;

v37 = Oops::
CryptoUtils::
scramble32(v35, plains0, &key);

…

v60 = counter++;

plainsCUR = plains[v60];

LODWORD(v62) = llvm::
ManagedStatic<Oops::
CryptoUtils>::
operator->(&Oops::
Oopscryptoutils, v59);

v63 = Oops::
CryptoUtils::
scramble32(v62, plainsCUR, &key);

IDA得知数组大概大小:

.data:
2345E0 ; _DWORD plains[65806]

.data:
2345E0 plains          dd 0F6172961h, 0CB973739h, 904F3728h, 0DB7194B9h, 81E0B166h

…

gdb script :

$ cat >cmd

set confirm off

set pagination off

break *0x04004e3

commands

p/x $eax

cont

end

run

$ gdb -x cmd -n ./0llvm </dev/null >log

$ head -30 log

GNU gdb (Ubuntu 7.11.1-0ubuntu1~16.04) 7.11.1

…

Reading symbols from ./0llvm…(no debugging symbols found)…done.

Breakpoint 1 at 0x4004e3

Breakpoint 1, 0x00000000004004e3 in main ()

$1 = 0x4e52bce7

Breakpoint 1, 0x00000000004004e3 in main ()

$2 = 0x3ac545da

Breakpoint 1, 0x00000000004004e3 in main ()

$3 = 0xff97c58e

Breakpoint 1, 0x00000000004004e3 in main ()

$4 = 0xe83342dd

$ tail log

Breakpoint 1, 0x00000000004004e3 in main ()

$65789 = 0xf1dbf041

Breakpoint 1, 0x00000000004004e3 in main ()

$65790 = 0xdb9a21b8

Breakpoint 1, 0x00000000004004e3 in main ()

$65791 = 0xb02b5689

[Inferior 1 (process 10622) exited with code 027]

(gdb) quit

Recovering key

__int64 __fastcall Oops::
CryptoUtils::
scramble32(

Oops::
CryptoUtils *this, unsigned int x, const char *key)

{

int v3; // ST20_4@1

int v4; // ST24_4@1

int v5; // ST20_4@1

v3 = AES_PRECOMP_TE3[(x ^ key[3])] ^

AES_PRECOMP_TE2[(BYTE1(x) ^ key[2])] ^

AES_PRECOMP_TE1[((x >> 16) ^ key[1])] ^

AES_PRECOMP_TE0[(BYTE3(x) ^ *key)];

v4 = AES_PRECOMP_TE3[(v3 ^ key[7])] ^

AES_PRECOMP_TE2[(BYTE1(v3) ^ key[6])] ^

AES_PRECOMP_TE1[((v3 >> 16) ^ key[5])] ^

AES_PRECOMP_TE0[(BYTE3(v3) ^ key[4])];

v5 = AES_PRECOMP_TE3[(v4 ^ key[11])] ^

AES_PRECOMP_TE2[(BYTE1(v4) ^ key[10])] ^

AES_PRECOMP_TE1[((v4 >> 16) ^ key[9])] ^

AES_PRECOMP_TE0[(BYTE3(v4) ^ key[8])];

return AES_PRECOMP_TE3[(v5 ^ key[15])] ^

AES_PRECOMP_TE2[(BYTE1(v5) ^ key[14])] ^

AES_PRECOMP_TE1[((v5 >> 16) ^ key[13])] ^

AES_PRECOMP_TE0[(BYTE3(v5) ^ key[12])] ^

((key[2] << 8) | (key[1] << 16) | (*key << 24) | key[3]);

}

aes 块. 得到S盒:

from aes import AES

A = AES()

for i in xrange(4):

for x, t in enumerate(AES_PRECOMP_TE[i]):

t = [BYTE3(t), BYTE2(t), BYTE1(t), BYTE0(t)]

t2 = A.mixColumn(list(t), isInv=True)

print t2

print

$ python precomp.py

[99, 0, 0, 0]

[124, 0, 0, 0]

[119, 0, 0, 0]

[123, 0, 0, 0]

[242, 0, 0, 0]

[107, 0, 0, 0]

…

AES_PRECOMP_TE[i](x) = MixColumns(SBox(x) << 8*i)

X1 = (x1, a, b, c)

X2 = (x2, a, b, c)

X3 = (x3, a, b, c)

(X1 ⊕⊕ X2, X1 ⊕⊕ X3)

Recovering Seed

key生成算法：

// in Oops::
CryptoUtils::
encrypt(Oops::
CryptoUtils *this, unsigned __int8 *dst, unsigned __int8 *nonce, unsigned __int8 *seed)

memset(dst, 0, 0x10uLL);

v5 = *(nonce_ + 1);

*buf = *nonce_;

*buf2 = v5;

for ( i = 0; i <= 15; ++i ) {

seedbyte = seed_[i];

for ( j = 0; j <= 7; ++j ) {

if ( seedbyte & 1 ) {

for ( k = 0; k <= 15; ++k )

dst[k] ^= buf[k];

}

seedbyte = seedbyte >> 1;

for ( l = 0; l <= 15; ++l )

buf[l] = TABLE[buf[l]];

}

}

TABLE是8位非线性S盒. Nonce is constant and hardcoded (note that it is increased by 1 before calling encrypt, as a big-endian number, see Oops::
CryptoUtils::
inc_ctr):

// in  Oops::
CryptoUtils::
prng_seed(struct CryptoUtils *cryptoutils, __int64 a2)

noncebuf = cryptoutils->nonce;

*noncebuf = 0xD7C59B4DFFD1E010LL;

*(noncebuf + 1) = 0x20C7C17B250E019ALL;

虽然TABLE是非线性的, 但是buf是独立更新的。buf 和 seed 却是线性相关的, 所以可以由下列脚本恢复seed:

from sage.all import *

from struct import pack, unpack

def tobin(x, n):

return tuple(map(int, bin(x).lstrip(“0b”).rjust(n, “0”)))

def frombin(v):

return int(“”.join(map(str, v)), 2 )

def tobinvec(v):

return sum( [tobin(c, 8) for c in v], () )

PRNG_OUT = [179, 197, 140, 9, 31, 61, 9, 48, 214, 74, 172, 159, 200, 11, 185, 236]

TABLE = [0x0ED,0x67,0x7F,0x0F6,0x0C7,0x9A,0x24,0x12,0x0BA,0x83,0x49,0x0DB,0x13,0x0BF,0x61,0x0B0,0x0FF,0x69,0x80,0x0EC,0x0DE,0x4,0x63,0x0C4,0x96,0x73,0x1B,0x6E,0x0A6,0x9E,0x87,0x4B,0x0FC,0x10,0x2A,0x0C3,0x5C,0x2E,0x36,0x0B2,0x0DF,0x0E3,0x90,0x0FE,0x1A,0x0F,0x1C,0x84,0x1,0x15,0x3A,0x85,0x0A5,0x57,0x3F,0x6D,0x0F5,0x4A,0x0A,0x0D6,0x9F,0x64,0x0B5,0x0F7,0x8F,0x99,0x68,0x4D,0x17,0x0F9,0x0EE,0x0F0,0x3,0x6,0x4C,0x0BD,0x58,0x33,0x0A9,0x0DC,0x3C,0x0A3,0x3B,0x0D1,0x0BB,0x28,0x0F4,0x0B9,0x0CF,0x47,0x0A0,0x6A,0x0C2,0x19,0x0B,0x97,0x81,0x35,0x91,0x7C,0x5D,0x7A,0x48,0x2B,0x41,0x0D9,0x0CB,0x6F,0x56,0x8D,0x5A,0x0C5,0x3E,0x0D8,0x0C0,0x60,0x1F,0x9,0x0CA,0x7B,0x25,0x0E7,0x0AE,0x0F2,0x77,0x0FA,0x3D,0x50,0x0E2,0x4F,0x0C9,0x2C,0x53,0x45,0x0C1,0x0E9,0x46,0x0D,0x70,0x8A,0x0A1,0x0D5,0x94,0x92,0x88,0x95,0x9D,0x26,0x9B,0x0E4,0x5,0x44,0x11,0x2D,0x7,0x1E,0x0A4,0x38,0x0E1,0x0A8,0x52,0x89,0x0AF,0x40,0x72,0x0E5,0x0B4,0x7E,0x51,0x6C,0x0FB,0x76,0x62,0x0D4,0x8,0x9C,0x54,0x5B,0x75,0x29,0x0C6,0x66,0x0DA,0x0FD,0x14,0x86,0x78,0x16,0x0B6,0x8B,0x39,0x0E6,0x0B7,0x1D,0x0D3,0x18,0x0A7,0x30,0x0E8,0x23,0x37,0x7D,0x82,0x0BE,0x34,0x0C,0x55,0x0D0,0x0EF,0x0,0x0CD,0x0AC,0x0A2,0x4E,0x0B3,0x0AB,0x31,0x8E,0x21,0x0E0,0x22,0x74,0x5E,0x8C,0x32,0x0F8,0x0EB,0x2F,0x79,0x0F1,0x42,0x0C8,0x0DD,0x0CE,0x65,0x27,0x5F,0x20,0x0B8,0x0AA,0x0AD,0x71,0x6B,0x0D2,0x0EA,0x0BC,0x0E,0x0CC,0x98,0x2,0x59,0x43,0x0B1,0x93,0x0D7,0x0F3,]

# note 0x20… -> 0x21

nonce = pack(“<QQ”, 0xD7C59B4DFFD1E010, 0x21C7C17B250E019A)

cols = [map(ord, nonce)]

for i in xrange(127):

v = [TABLE[c] for c in cols[-1]]

cols.append(v)

cols = [vector(GF(2), tobinvec(v)) for v in cols]

target = vector(GF(2), tobinvec(PRNG_OUT))

m = matrix(GF(2), 128, len(cols))

for x, c in enumerate(cols):

m.set_column(x, c)

try:

sol = m.solve_right(target)

except ValueError:

print “NO SOLUTION”

quit()

print “SOL”, sol

res = “”

for i in xrange(0, 128, 8):

res += chr(frombin(sol[i:i+8][::-1]))

print “flag{%s}” % res

【考点】

1、C++逆向分析

2、llvm反混淆原理

3、AES密钥爆破

原文始发于微信公众号（山石网科安全技术研究院）：0CTF 2017-zer0IIvm题目分析

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/06/8-1654581159.png)