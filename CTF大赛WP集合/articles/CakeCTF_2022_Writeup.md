# CakeCTF 2022 Writeup

> 原文: https://www.ctfiot.com/49056.html
> ID: 49056

yoshikingさん, theoremoonさん, ptr-yudaiさん主催のCakeCTF 2022に参加させていただきました。やっぱりCTFは楽しい！と思える良問の数々で、すごく面白かったです。主催の皆さん、ありがとうございました！?

[welcome] Welcome (676 solves)

[warmup / rev] nimrev (246 solves)

[rev] luau (64 solves)

[forensics / rev] zundamon (20 solves)

[survey] Survey (226 solves)

[welcome] Welcome (676 solves)

Get the flag in Discord

問題文に書かれている通り、DiscordからFlagが得られる。

Flag: CakeCTF{p13a53_tast3_0ur_5p3cia1_cak35}

[warmup / rev] nimrev (246 solves)

Have you ever analysed programs written in languages other than C/C++?

NimMainModule 関数に目を通すと、eqStrings が呼び出されている場所を見つけることができる。

.text:000000000000AFB8 mov rdx, [rbp+flag]
.text:000000000000AFBC mov rax, [rbp+input]
.text:000000000000AFC0 mov rsi, rdx
.text:000000000000AFC3 mov rdi, rax
.text:000000000000AFC6 call eqStrings

入力とそのまま比較していることから、Flagが eqStrings に渡されていると推測することができる。ブレークポイントを設置して引数の内容を確認することでFlagが得られる。

gdb-peda$ x/24c 0x7ffff7d0f0e0
0x7ffff7d0f0e0: 0x43 0x61 0x6b 0x65 0x43 0x54 0x46 0x7b
0x7ffff7d0f0e8: 0x73 0x30 0x6d 0x33 0x74 0x31 0x6d 0x33
0x7ffff7d0f0f0: 0x73 0x5f 0x6e 0x30 0x74 0x5f 0x43 0x7d

Flag: CakeCTF{s0m3t1m3s_n0t_C}

[rev] luau (64 solves)

Aloha! This is a luau for reverse engineerers!

LuaソースコードとLua 5.3のバイトコードが配布されている。

libflag.lua: Lua bytecode, version 5.3
main.lua: ASCII text

Luaソースコードを確認してみると、libflag.checkFlag という関数が呼び出されており、引数として入力内容と "CakeCTF 2022" という文字列が渡されていることがわかる。Luaバイトコードのデコンパイラがないか探してみると、luadecというものが見つかったので、手元でビルドした上で試してみた。

# luadecをビルドする
$ git clone https://github.com/viruscamp/luadec
$ cd luadec
$ git submodule update --init lua-5.3
$ cd lua-5.3
$ make linux
$ cd ../luadec
$ make LUAVER=5.3

# luadecを実行する
$ ./luadec ./libflag.lua
cannot find blockend > 5 , pc = 4, f->sizecode = 5
cannot find blockend > 110 , pc = 109, f->sizecode = 110
-- Decompiled using luadec 2.2 rev: 895d923 for Lua 5.3 from https://github.com/viruscamp/luadec
-- Command line: ./libflag.lua

Segmentation fault (core dumped)

見ての通り、正常にデコンパイルすることができなかったので、逆アセンブル機能を試してみた。

$ ./luadec -dis ./libflag.lua
cannot find blockend > 5 , pc = 4, f->sizecode = 5
cannot find blockend > 110 , pc = 109, f->sizecode = 110
; Disassembled using luadec 2.2 rev: 895d923 for Lua 5.3 from https://github.com/viruscamp/luadec
; Command line: -dis ./libflag.lua

; Function: 0
; Defined at line: 0
; #Upvalues: 1
; #Parameters: 0
; Is_vararg: 2
; Max Stack Size: 2

 0 [-]: CLOSURE R0 0 ; R0 := closure(Function #0_0)
 1 [-]: NEWTABLE R1 0 1 ; R1 := {} (size = 0,1)
 2 [-]: SETTABLE R1 K0 R0 ; R1["checkFlag"] := R0
 3 [-]: RETURN R1 2 ; return R1
 4 [-]: RETURN R0 1 ; return

; Function: 0_0
; Defined at line: 1
; #Upvalues: 1
; #Parameters: 2
; Is_vararg: 0
; Max Stack Size: 41

 0 [-]: NEWTABLE R2 26 0 ; R2 := {} (size = 26,0)
 1 [-]: LOADK R3 K0 ; R3 := 62
 2 [-]: LOADK R4 K1 ; R4 := 85
 3 [-]: LOADK R5 K2 ; R5 := 25
 4 [-]: LOADK R6 K3 ; R6 := 84
**長いので省略**

エラーは先ほどと変わらず表示されているが、正常に逆アセンブルできているように見えたので、構わず解析を進めることにした。表示されたコードを最初から読んでいくと、まず最初に数値をR3~R40に代入し、それをR2というリストに格納していることがわかる。

 1 [-]: LOADK R3 K0 ; R3 := 62
 2 [-]: LOADK R4 K1 ; R4 := 85
 3 [-]: LOADK R5 K2 ; R5 := 25
.
.
.
 36 [-]: LOADK R38 K30 ; R38 := 89
 37 [-]: LOADK R39 K31 ; R39 := 34
 38 [-]: LOADK R40 K31 ; R40 := 34
 39 [-]: SETLIST R2 38 1 ; R2[0] to R2[37] := R3 to R40 ; R(a)[(c-1)*FPF+i] := R(a+i), 1 <= i <= b, a=2, b=38, c=1, FPF=50

次にR0（第一引数）とR2の長さが等しいか確認する処理があり、更にその次にR0およびR1（第二引数）をバイトのリストに変換する処理が記述されていた。

 59 [-]: SETTABLE R3 R8 R9 ; R3[R8] := R9
...
 72 [-]: SETTABLE R4 R8 R9 ; R4[R8] := R9

その後、R3およびR4の順序を逆順に並び替える処理、そしてR3とR4でXORデコードを行っている処理が記述されていた。

 82 [-]: GETTABLE R13 R3 R8 ; R13 := R3[R8]
 83 [-]: GETTABLE R14 R3 R12 ; R14 := R3[R12]
 84 [-]: SETTABLE R3 R8 R14 ; R3[R8] := R14
 85 [-]: SETTABLE R3 R12 R13 ; R3[R12] := R13
...
 92 [-]: GETTABLE R9 R3 R8 ; R9 := R3[R8]
 93 [-]: SUB R10 R8 K32 ; R10 := R8 - 1
 94 [-]: LEN R11 R4 ; R11 := #R4
 95 [-]: MOD R10 R10 R11 ; R10 := R10 % R11
 96 [-]: ADD R10 K32 R10 ; R10 := 1 + R10
 97 [-]: GETTABLE R10 R4 R10 ; R10 := R4[R10]
 98 [-]: BXOR R9 R9 R10 ; R9 := R9 ~ R10

以下が上記で判明した内容をもとに作成したソルバです。

#!/usr/bin/env python3

r2 = [62, 85, 25, 84, 47, 56, 118, 71, 109, 0, 90, 71, 115, 9, 30, 58, 32, 101, 40, 20, 66, 111, 3, 92, 119, 22, 90, 11, 119, 35, 61, 102, 102, 115, 87, 89, 34, 34]
r4 = bytearray(b"CakeCTF 2022")

flag = ''
for i in range(len(r2)):
 flag += chr(r2[i] ^ r4[i % len(r4)])

print(flag[::-1])

Flag: CakeCTF{w4n1w4n1_p4n1c_uh0uh0_g0ll1r4}

3番目に解いたのでダメかな、と思いきやPrizeを貰えることになって、すごく嬉しかったです！*1

[forensics / rev] zundamon (20 solves)

I found a suspicious process named "zundamon" running on my computer. Can you investigate the communication logs to confirm that no information has been leaked?

This program may harm your computer. Do not run it outside sandbox.

実行ファイル (ELF) とpcapngファイルが配布されている。

evidence.pcapng: pcapng capture file - version 1.0
zundamon: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7e0fd4acc0c6f7aed55b6aab42ccd63a2c7ee871, for GNU/Linux 3.2.0, not stripped

zundamon という実行ファイルを解析すると、/dev/input/ 下のデバイスファイルを読み取り、その内容を 164.70.70.9 宛てに送信するような機能を持っていることがわかる。

.text:0000000000001568 mov rcx, cs:cmp ; cmp
.text:000000000000156F lea rdx, is_char ; selector
.text:0000000000001576 lea rdi, dir ; "/dev/input"
.text:000000000000157D mov rax, fs:28h
.text:0000000000001586 mov [rsp+2048h+var_30], rax
.text:000000000000158E xor eax, eax
.text:0000000000001590 lea rsi, [rsp+2048h+namelist] ; namelist
.text:0000000000001595 call _scandir
...
.text:0000000000001737 lea rdi, cp ; "164.70.70.9"
.text:000000000000173E mov [rsp+38h+var_38], 0EB180002h
.text:0000000000001745 call _inet_addr
...
.text:0000000000001AB8 mov rsi, r14 ; buf
.text:0000000000001ABB mov edx, 3072 ; nbytes
.text:0000000000001AC0 mov edi, r12d ; fd
.text:0000000000001AC3 call _read
...
.text:00000000000019EB mov edx, 2 ; n
.text:00000000000019F0 mov rsi, r12 ; buf
.text:00000000000019F3 mov edi, ebp ; fd
.text:00000000000019F5 call _write

Wiresharkを用いてペイロードを抽出した上で、内容を読みやすくするスクリプトを作成し実行しました。

#!/usr/bin/env python3

import struct

KNOWN_VAR = [b'PING', b'+PONG', b'RPUSH', b'd8:f2:ca:ce:44:8d', b'*3', b'$5', b'$17', b'$3', b'*1', b'$4']

payload = bytes.fromhex(open('zundamon/payload.raw', 'r').read())
payload = payload.split(b'\r\n')
dat = []
for elem in payload:
 if elem != b'' and elem not in KNOWN_VAR and elem[0] != 58:
 dat.append(chr(elem[0]).encode())

dat = b''.join(dat)

# 長くなったので、一部省略しています
# 完全版: https://gist.github.com/mopisec/be346d276bbc7b83be9a7c69a681bbcd

for i in range(0, len(payload), EVENT_SIZE):
 print(get_key_from_value(key_dict, struct.unpack(EVENT_FORMAT, dat[i:i+EVENT_SIZE])[0]))

$ python3 ./nanoda_solve.py
KEY_LEFTCTRL
KEY_LEFTCTRL
...
KEY_LEFTSHIFT
KEY_C
KEY_A
KEY_A
KEY_K
KEY_K
KEY_E
KEY_E
KEY_LEFTSHIFT
KEY_C
KEY_C
KEY_T
KEY_T
KEY_F
KEY_F
KEY_RIGHTBRACE
...

Flag: CakeCTF{b3_C4r3fuL_0f_M4l1c10us_k3yL0gg3r}

とても面白い問題でした、なのだ！?

[survey] Survey (226 solves)

Surveyを提出することでFlagが得られる。

Flag: CakeCTF{ar3_y0u_5ati5fi3d_with_thi5_y3ar5_cak3?}


```
Get the flag in Discord
```



```
Have you ever analysed programs written in languages other than C/C++?
```



```
.text:000000000000AFB8 mov rdx, [rbp+flag]
.text:000000000000AFBC mov rax, [rbp+input]
.text:000000000000AFC0 mov rsi, rdx
.text:000000000000AFC3 mov rdi, rax
.text:000000000000AFC6 call eqStrings
```



```
gdb-peda$ x/24c 0x7ffff7d0f0e0
0x7ffff7d0f0e0: 0x43 0x61 0x6b 0x65 0x43 0x54 0x46 0x7b
0x7ffff7d0f0e8: 0x73 0x30 0x6d 0x33 0x74 0x31 0x6d 0x33
0x7ffff7d0f0f0: 0x73 0x5f 0x6e 0x30 0x74 0x5f 0x43 0x7d
```



```
Aloha! This is a luau for reverse engineerers!
```



```
libflag.lua: Lua bytecode, version 5.3
main.lua: ASCII text
```



```
# luadecをビルドする
$ git clone https://github.com/viruscamp/luadec
$ cd luadec
$ git submodule update --init lua-5.3
$ cd lua-5.3
$ make linux
$ cd ../luadec
$ make LUAVER=5.3

# luadecを実行する
$ ./luadec ./libflag.lua
cannot find blockend > 5 , pc = 4, f->sizecode = 5
cannot find blockend > 110 , pc = 109, f->sizecode = 110
-- Decompiled using luadec 2.2 rev: 895d923 for Lua 5.3 from https://github.com/viruscamp/luadec
-- Command line: ./libflag.lua

Segmentation fault (core dumped)
```



```
$ ./luadec -dis ./libflag.lua
cannot find blockend > 5 , pc = 4, f->sizecode = 5
cannot find blockend > 110 , pc = 109, f->sizecode = 110
; Disassembled using luadec 2.2 rev: 895d923 for Lua 5.3 from https://github.com/viruscamp/luadec
; Command line: -dis ./libflag.lua

; Function: 0
; Defined at line: 0
; #Upvalues: 1
; #Parameters: 0
; Is_vararg: 2
; Max Stack Size: 2

 0 [-]: CLOSURE R0 0 ; R0 := closure(Function #0_0)
 1 [-]: NEWTABLE R1 0 1 ; R1 := {} (size = 0,1)
 2 [-]: SETTABLE R1 K0 R0 ; R1["checkFlag"] := R0
 3 [-]: RETURN R1 2 ; return R1
 4 [-]: RETURN R0 1 ; return

; Function: 0_0
; Defined at line: 1
; #Upvalues: 1
; #Parameters: 2
; Is_vararg: 0
; Max Stack Size: 41

 0 [-]: NEWTABLE R2 26 0 ; R2 := {} (size = 26,0)
 1 [-]: LOADK R3 K0 ; R3 := 62
 2 [-]: LOADK R4 K1 ; R4 := 85
 3 [-]: LOADK R5 K2 ; R5 := 25
 4 [-]: LOADK R6 K3 ; R6 := 84
**長いので省略**
```



```
1 [-]: LOADK R3 K0 ; R3 := 62
 2 [-]: LOADK R4 K1 ; R4 := 85
 3 [-]: LOADK R5 K2 ; R5 := 25
.
.
.
 36 [-]: LOADK R38 K30 ; R38 := 89
 37 [-]: LOADK R39 K31 ; R39 := 34
 38 [-]: LOADK R40 K31 ; R40 := 34
 39 [-]: SETLIST R2 38 1 ; R2[0] to R2[37] := R3 to R40 ; R(a)[(c-1)*FPF+i] := R(a+i), 1 <= i <= b, a=2, b=38, c=1, FPF=50
```



```
59 [-]: SETTABLE R3 R8 R9 ; R3[R8] := R9
...
 72 [-]: SETTABLE R4 R8 R9 ; R4[R8] := R9
```



```
82 [-]: GETTABLE R13 R3 R8 ; R13 := R3[R8]
 83 [-]: GETTABLE R14 R3 R12 ; R14 := R3[R12]
 84 [-]: SETTABLE R3 R8 R14 ; R3[R8] := R14
 85 [-]: SETTABLE R3 R12 R13 ; R3[R12] := R13
...
 92 [-]: GETTABLE R9 R3 R8 ; R9 := R3[R8]
 93 [-]: SUB R10 R8 K32 ; R10 := R8 - 1
 94 [-]: LEN R11 R4 ; R11 := #R4
 95 [-]: MOD R10 R10 R11 ; R10 := R10 % R11
 96 [-]: ADD R10 K32 R10 ; R10 := 1 + R10
 97 [-]: GETTABLE R10 R4 R10 ; R10 := R4[R10]
 98 [-]: BXOR R9 R9 R10 ; R9 := R9 ~ R10
```



```
#!/usr/bin/env python3

r2 = [62, 85, 25, 84, 47, 56, 118, 71, 109, 0, 90, 71, 115, 9, 30, 58, 32, 101, 40, 20, 66, 111, 3, 92, 119, 22, 90, 11, 119, 35, 61, 102, 102, 115, 87, 89, 34, 34]
r4 = bytearray(b"CakeCTF 2022")

flag = ''
for i in range(len(r2)):
 flag += chr(r2[i] ^ r4[i % len(r4)])

print(flag[::-1])
```



```
I found a suspicious process named "zundamon" running on my computer. Can you investigate the communication logs to confirm that no information has been leaked?

This program may harm your computer. Do not run it outside sandbox.
```



```
evidence.pcapng: pcapng capture file - version 1.0
zundamon: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7e0fd4acc0c6f7aed55b6aab42ccd63a2c7ee871, for GNU/Linux 3.2.0, not stripped
```



```
.text:0000000000001568 mov rcx, cs:cmp ; cmp
.text:000000000000156F lea rdx, is_char ; selector
.text:0000000000001576 lea rdi, dir ; "/dev/input"
.text:000000000000157D mov rax, fs:28h
.text:0000000000001586 mov [rsp+2048h+var_30], rax
.text:000000000000158E xor eax, eax
.text:0000000000001590 lea rsi, [rsp+2048h+namelist] ; namelist
.text:0000000000001595 call _scandir
...
.text:0000000000001737 lea rdi, cp ; "164.70.70.9"
.text:000000000000173E mov [rsp+38h+var_38], 0EB180002h
.text:0000000000001745 call _inet_addr
...
.text:0000000000001AB8 mov rsi, r14 ; buf
.text:0000000000001ABB mov edx, 3072 ; nbytes
.text:0000000000001AC0 mov edi, r12d ; fd
.text:0000000000001AC3 call _read
...
.text:00000000000019EB mov edx, 2 ; n
.text:00000000000019F0 mov rsi, r12 ; buf
.text:00000000000019F3 mov edi, ebp ; fd
.text:00000000000019F5 call _write
```



```
#!/usr/bin/env python3

import struct

KNOWN_VAR = [b'PING', b'+PONG', b'RPUSH', b'd8:f2:ca:ce:44:8d', b'*3', b'$5', b'$17', b'$3', b'*1', b'$4']

payload = bytes.fromhex(open('zundamon/payload.raw', 'r').read())
payload = payload.split(b'\r\n')
dat = []
for elem in payload:
 if elem != b'' and elem not in KNOWN_VAR and elem[0] != 58:
 dat.append(chr(elem[0]).encode())

dat = b''.join(dat)

# 長くなったので、一部省略しています
# 完全版: https://gist.github.com/mopisec/be346d276bbc7b83be9a7c69a681bbcd

for i in range(0, len(payload), EVENT_SIZE):
 print(get_key_from_value(key_dict, struct.unpack(EVENT_FORMAT, dat[i:i+EVENT_SIZE])[0]))
```



```
$ python3 ./nanoda_solve.py
KEY_LEFTCTRL
KEY_LEFTCTRL
...
KEY_LEFTSHIFT
KEY_C
KEY_A
KEY_A
KEY_K
KEY_K
KEY_E
KEY_E
KEY_LEFTSHIFT
KEY_C
KEY_C
KEY_T
KEY_T
KEY_F
KEY_F
KEY_RIGHTBRACE
...
```
