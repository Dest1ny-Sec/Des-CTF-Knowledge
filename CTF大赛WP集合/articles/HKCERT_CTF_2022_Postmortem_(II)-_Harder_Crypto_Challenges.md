# HKCERT CTF 2022 Postmortem (II): Harder Crypto Challenges

> 原文: https://www.ctfiot.com/87575.html
> ID: 87575


```
Microsoft Windows [Version 10.0.19044.2006]
(c) Microsoft Corporation. All rights reserved.

C:\Users\mystiz>aes.bat [**REDACTED_KEY**] 68656c6c6f20776f726c6421
2740f489df8449453fd87f075a648e94

C:\Users\mystiz>aes.bat [**REDACTED_KEY**] [**REDACTED_FLAG**]
9a3538b25faf70f2654e7816df540acedb753d319f76311d95a4ad5e797fff3e13f7dcbde563baf8f7ac62580196b5ca911789fedade0fd6fb40642413d521992311f9bc01d127db4bbcf257ee5deb8fcd49b23aadd12f52fa7829e7e281373f
```



```
:EncryptBlock
 set block_id=%1

 call :LoadState %block_id%

 set round_key=0
 call :AddRoundKey %round_key%

 for /l %%r in (1, 1, 9) do (
 set round_key=%%r
 call :SubBytes
 call :ShiftRows
 call :MixColumns
 call :AddRoundKey %round_key%
 )

 set round_key=10
 call :SubBytes
 call :ShiftRows
 call :AddRoundKey %round_key%
 
 call :SaveState %block_id%
exit /b 0
```



```
:AddRoundKey
 set round_id=%1
 for /l %%i in (0, 1, 15) do (
 set /a j=16*%round_id%+%%i
 set /a STATE[%%i]="STATE[%%i]^KEY[%j%]"
 )
exit /b 0
```



```
hkcert22{pr09r4mm1ng_in_b47ch_1s_s0_d1fficul7_4nd_why_d03s_th1n9s_1n_br4ck3t_run5_in_p4ral13l}
```



```
:AddRoundKey
 set round_id=%1
 for /l %%i in (0, 1, 15) do (
 set /a j=16*%round_id%+%%i
 set /a STATE[%%i]="STATE[%%i]^KEY[%j%]"
 )
exit /b 0
```



```
:EncryptBlock
 set block_id=%1

 call :LoadState %block_id%

 set round_key=0
 call :AddRoundKey %round_key%

 for /l %%r in (1, 1, 9) do (
 set round_key=%%r
 call :SubBytes
 call :ShiftRows
 call :MixColumns
 call :AddRoundKey %round_key%
 )

 set round_key=10
 call :SubBytes
 call :ShiftRows
 call :AddRoundKey %round_key%
 
 call :SaveState %block_id%
exit /b 0
```



```
package main

import (
	"fmt"
	"math/rand"
	"os"
)

func main() {
	rand.Seed(1337)

	flag, err := os.ReadFile("flag.enc")
	if err != nil {
 fmt.Println("cannot open flag.enc")
 os.Exit(1)
	}

	for i, j := uint64(0), 0; j < len(flag); i++ {
 rand.Uint64()
 if i == uint64(1)<<j {
 x := byte(rand.Uint64())
 fmt.Print(string(flag[j] ^ x))
 j += 1
 }
	}
	fmt.Println()
}
```



```
// https://cs.opensource.google/go/go/+/refs/tags/go1.19:src/math/rand/rng.go

// Copyright 2009 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package rand

/*
 * Uniform distribution
 *
 * algorithm by
 * DP Mitchell and JA Reeds
 */

const (
	rngLen = 607
	rngTap = 273
	rngMax = 1 << 63
	rngMask = rngMax - 1
	int32max = (1 << 31) - 1
)

var (
	// rngCooked used for seeding. See gen_cooked.go for details.
	rngCooked [rngLen]int64 = [...]int64{
 -4181792142133755926, -4576982950128230565, 1395769623340756751, 5333664234075297259,
 // ...600 numbers snipped...
 8382142935188824023, 9103922860780351547, 4152330101494654406,
	}
)

type rngSource struct {
	tap int // index into vec
	feed int // index into vec
	vec [rngLen]int64 // current feedback register
}

// seed rng x[n+1] = 48271 * x[n] mod (2**31 - 1)
func seedrand(x int32) int32 {
	const (
 A = 48271
 Q = 44488
 R = 3399
	)

	hi := x / Q
	lo := x % Q
	x = A*lo - R*hi
	if x < 0 {
 x += int32max
	}
	return x
}

// Seed uses the provided seed value to initialize the generator to a deterministic state.
func (rng *rngSource) Seed(seed int64) {
	rng.tap = 0
	rng.feed = rngLen - rngTap

	seed = seed % int32max
	if seed < 0 {
 seed += int32max
	}
	if seed == 0 {
 seed = 89482311
	}

	x := int32(seed)
	for i := -20; i < rngLen; i++ {
 x = seedrand(x)
 if i >= 0 {
 var u int64
 u = int64(x) << 40
 x = seedrand(x)
 u ^= int64(x) << 20
 x = seedrand(x)
 u ^= int64(x)
 u ^= rngCooked[i]
 rng.vec[i] = u
 }
	}
}

// Uint64 returns a non-negative pseudo-random 64-bit integer as an uint64.
func (rng *rngSource) Uint64() uint64 {
	rng.tap--
	if rng.tap < 0 {
 rng.tap += rngLen
	}

	rng.feed--
	if rng.feed < 0 {
 rng.feed += rngLen
	}

	x := rng.vec[rng.feed] + rng.vec[rng.tap]
	rng.vec[rng.feed] = x
	return uint64(x)
}
```



```
func main() {
	rand.Seed(1337)

	flag, err := os.ReadFile("flag.enc")
	if err != nil {
 fmt.Println("cannot open flag.enc")
 os.Exit(1)
	}

	for i, j := uint64(0), 0; j < len(flag); i++ {
 rand.Uint64()
 if i == uint64(1)<<j {
 x := byte(rand.Uint64())
 fmt.Print(string(flag[j] ^ x))
 j += 1
 }
	}
	fmt.Println()
}
```



```
RNGCOOKED = [
 -4181792142133755926, -4576982950128230565, 1395769623340756751, 5333664234075297259,
 # ...Snipped. Please copy directly from Golang's source code 
 8382142935188824023, 9103922860780351547, 4152330101494654406
]
RNGLEN = 607
RNGTAP = 273

class GoRng:
 def __init__(self, seed):
 self.tap = 0
 self.feed = RNGLEN - RNGTAP

 self.vec = vector(Zmod(2^8), [0 for _ in range(RNGLEN)])

 seed %= (1<<31) - 1
 if seed == 0: seed = 89482311

 x = seed
 for i in range(-20, 0):
 x = self.__seedrand(x)

 for i in range(RNGLEN):
 x = self.__seedrand(x)
 u = x<<40
 x = self.__seedrand(x)
 u ^^= x<<20
 x = self.__seedrand(x)
 u ^^= x
 u ^^= RNGCOOKED[i]
 self.vec[i] = u

 def __seedrand(self, x):
 A, Q, R = 48271, 44488, 3399
 hi = x // Q
 lo = x % Q
 x = A*lo - R*hi
 return x % ((1<<31) - 1)

rng = GoRng(1337)

T = Matrix(Zmod(2^8), 607, 607)

for i in range(606):
 T[i, i+1] = 1
T[606, 0] = 1
T[606, 334] = 1

S = T

a = vector(Zmod(2^8), list(rng.vec[333::-1]) + list(rng.vec[:333:-1]))

# Skip the first two randoms
a = T^2 * a

with open('flag.enc', 'rb') as f: flag = f.read()
output = []
for i, f in enumerate(flag):
 a = T*a
 output.append(int(a[-1]) ^^ f)
 a = S*a
 S = S*S
 print(bytes(output))
```



```
message ServerRoundInitMessage {
 bytes nonce = 1; // server's nonce
}

message ClientRoundInitMessage {
 bytes hash = 1; // MD5 digest of ClientMoveMessage
 bytes nonce = 2; // client's nonce
}

message ServerMoveMessage {
 Move move = 1;
}

message ClientMoveMessage {
 bytes nonce_server = 1;
 bytes nonce_client = 2;
 Move move = 3;
}

message ServerRoundFinalMessage {
 Player winner = 1;
};
```



```
// ServerRoundInitMessage
{"nonce": "15f0...5273"}
```



```
// ClientMoveMessage
{"nonce_server": "15f0...5273", "nonce_client": "d7b5...1ff1", "move": "scissors"}
```



```
// ClientRoundInitMessage
{"hash": "03e0...a148", "nonce": "d7b5...1ff1"}
```



```
// ServerMoveMessage
{"move": "rock"}
```



```
// ClientMoveMessage
{"nonce_server": "15f0...5273", "nonce_client": "d7b5...1ff1", "move": "scissors"}
```



```
// ServerRoundFinalMessage
{"winner": "server"}
```



```
# Inside hashclash/scripts/demo
echo -n "hello world." > prefix.txt
../poc_no.sh prefix.txt
MD5 differential path toolbox
Copyright (C) 2009 Marc Stevens
http://homepages.cwi.nl/~stevens/
(trimmed)
Found collision!
468115c46b73eac261b6d9f5284b68e3 collision1.bin
468115c46b73eac261b6d9f5284b68e3 collision2.bin
31dda9646624a15c6078582c9af60cf597949a18 collision1.bin
87fbd7c43d1ed226d13a478f0b89f55a744864d9 collision2.bin
4 -rw-rw-r-- 1 mystiz mystiz 128 Dec 18 14:48 collision1.bin
4 -rw-rw-r-- 1 mystiz mystiz 128 Dec 18 14:48 collision2.bin
hd collision1.bin 
00000000 68 65 6c 6c 6f 20 77 6f 72 6c 64 2e 12 d9 a6 74 |hello world....t|
00000010 d7 a8 55 aa c5 66 63 f8 58 98 89 71 e8 b2 49 52 |..U..fc.X..q..IR|
00000020 f9 e0 de f1 a0 62 e4 0d ba a9 57 b1 96 ed 91 eb |.....b....W.....|
00000030 1c b7 69 1d 36 89 e7 1a a2 41 a4 fd 7f bb 98 1f |..i.6....A......|
00000040 f7 72 24 73 6b 78 6b 20 14 db d0 a2 36 66 2a bc |.r$skxk ....6f*.|
00000050 36 fe cb 1e 32 1b 35 5b b7 ce d7 1b 0f e5 3f 98 |6...2.5[......?.|
00000060 1b 8b ed ab 73 14 fb f7 57 d2 2d ed c9 45 8a 1c |....s...W.-..E..|
00000070 2c f0 ab 4e fb 47 96 81 75 4c 25 34 ad ec 01 db |,..N.G..uL%4....|
00000080
hd collision2.bin
00000000 68 65 6c 6c 6f 20 77 6f 72 6d 64 2e 12 d9 a6 74 |hello wormd....t|
00000010 d7 a8 55 aa c5 66 63 f8 58 98 89 71 e8 b2 49 52 |..U..fc.X..q..IR|
00000020 f9 e0 de f1 a0 62 e4 0d ba a9 57 b1 96 ed 91 eb |.....b....W.....|
00000030 1c b7 69 1d 36 89 e7 1a a2 41 a4 fd 7f bb 98 1f |..i.6....A......|
00000040 f7 72 24 73 6b 78 6b 20 14 da d0 a2 36 66 2a bc |.r$skxk ....6f*.|
00000050 36 fe cb 1e 32 1b 35 5b b7 ce d7 1b 0f e5 3f 98 |6...2.5[......?.|
00000060 1b 8b ed ab 73 14 fb f7 57 d2 2d ed c9 45 8a 1c |....s...W.-..E..|
00000070 2c f0 ab 4e fb 47 96 81 75 4c 25 34 ad ec 01 db |,..N.G..uL%4....|
00000080
md5sum collision*.bin
468115c46b73eac261b6d9f5284b68e3 collision1.bin
468115c46b73eac261b6d9f5284b68e3 collision2.bin
```



```
[byte 1] [byte 2] [byte 3]
11000000 10100000 00010000
*( 64) *( 32) ( 16)
```



```
00000101 01101000 01100101 01101100 01101100 01101111
******** -- an unsigned integer 5
 ******** ******** ******** ******** ******** -- 5-byte buffer "hello"
```



```
enum Move {
 ROCK = 0;
 PAPER = 1;
 SCISSORS = 2;
}

message ClientMoveMessage {
 bytes nonce_server = 1;
 bytes nonce_client = 2;
 Move move = 3;
}
```



```
0a 05 68 65 6c 6c 6f
** -- an unsigned integer 10 = 8*1 + 2
 field number = 1 (nonce_server)
 wire type = 2 (LEN)
 ** -- an unsigned integer 5 (the length)
 ** ** ** ** ** -- 5-byte buffer "hello"
```



```
nonce_server: 1a0ab7c21d1c0200ffe48b8e0e37d369 (hex-encoded)
nonce_client: 152b631ddef3cd401dc0b730739460a8 (hex-encoded)
move: SCISSORS
```



```
19 01 0a 05 04 05 06 07 08
** -- an unsigned integer 0x19 = 8*3 + 1
 field number = 3 (move)
 wire type = 1 (I64)
 ** ** ** ** ** ** ** ** -- the 64-bit integer 0x0807060504050a01
```



```
18 01 0a 05 04 05 06 07 08
** -- an unsigned integer 0x18 = 8*3 + 0
 field number = 3 (move)
 wire type = 0 (VARINT)
 ** -- an unsigned integer 1
 ** -- an unsigned integer 0x0a = 8*1 + 2
 field number = 1 (nonce_server)
 wire type = 2 (LEN)
 ** -- an unsigned integer 5 (the length)
 ** ** ** ** ** -- 5-byte buffer "04 05 06 07 08"
```



```
nonce_server: 0405060708 (hex-encoded)
move: PAPER
```



```
1a 07 00 00 00 00 00 00 00 18 01 0a 05 04 05 06 07 08 1a 6c
```



```
1a 07 00 00 00 00 00 00 00 18 01 0a 05 04 05 06 07 08 1a 6c 11 e1 00 b5 d6 e0 e8 59 d2 1a ba f6
45 c7 64 92 91 43 f4 6c 46 11 cd 78 ac 72 d5 49 7f dd ec 8b 6f 18 a7 9f 5e 55 1a 49 90 0b 29 6e
23 8b 8e 23 06 62 2a 07 ec be 56 14 39 02 91 60 ce c6 60 be 16 35 74 a3 b5 78 11 21 3b e6 2d d8
2a bb cc aa 9b 55 89 bc 43 a8 cc 5c 97 0f 92 25 f6 72 0b 99 0f 47 2e e0 71 15 4e 97 85 e0 23 86
```



```
1a 07 00 00 00 00 00 00 00 19 01 0a 05 04 05 06 07 08 1a 6c 11 e1 00 b5 d6 e0 e8 59 d2 1a ba f6
45 c7 64 92 91 43 f4 6c 46 11 cd 78 ac 72 d5 49 7f dd ec 8b 6f 18 a7 9f 5e 55 1a 49 90 0b 29 6e
23 8b 8e 23 06 62 2a 07 ec bd 56 14 39 02 91 60 ce c6 60 be 16 35 74 a3 b5 78 11 21 3b e6 2d d8
2a bb cc aa 9b 55 89 bc 43 a8 cc 5c 97 0f 92 25 f6 72 0b 99 0f 47 2e e0 71 15 4e 97 85 e0 23 86
```



```
move = bytes.fromhex('00 00 00 00 00 00 00') # bytes
move = 1 # enum, equivalent to "PAPER"
nonce_client = bytes.fromhex('04 05 06 07 08') # bytes
move = bytes.fromhex('11 e1 00 ... e0 23 86') # bytes
```



```
nonce_server: 0405060708 (hex-encoded)
move: PAPER
```



```
move = bytes.fromhex('00 00 00 00 00 00 00') # bytes
move = 0x08_07_06_05_04_05_0a_01 # fixed64
move = bytes.fromhex('11 e1 00 ... e0 23 86') # bytes
```



```
1a 07 00 00 00 00 00 00 00 18 01 0a 05 04 05 06 07 08 1a 6c 11 e1 00 b5 d6 e0 e8 59 d2 1a ba f6
45 c7 64 92 91 43 f4 6c 46 11 cd 78 ac 72 d5 49 7f dd ec 8b 6f 18 a7 9f 5e 55 1a 49 90 0b 29 6e
23 8b 8e 23 06 62 2a 07 ec be 56 14 39 02 91 60 ce c6 60 be 16 35 74 a3 b5 78 11 21 3b e6 2d d8
2a bb cc aa 9b 55 89 bc 43 a8 cc 5c 97 0f 92 25 f6 72 0b 99 0f 47 2e e0 71 15 4e 97 85 e0 23 86

1a 07 00 00 00 00 00 00 00 18 02 0a 05 04 05 06 07 08 1a 6c
```



```
1a 07 00 00 00 00 00 00 00 18 01 0a 05 04 05 06 07 08 1a 6c 11 e1 00 b5 d6 e0 e8 59 d2 1a ba f6
45 c7 64 92 91 43 f4 6c 46 11 cd 78 ac 72 d5 49 7f dd ec 8b 6f 18 a7 9f 5e 55 1a 49 90 0b 29 6e
23 8b 8e 23 06 62 2a 07 ec be 56 14 39 02 91 60 ce c6 60 be 16 35 74 a3 b5 78 11 21 3b e6 2d d8
2a bb cc aa 9b 55 89 bc 43 a8 cc 5c 97 0f 92 25 f6 72 0b 99 0f 47 2e e0 71 15 4e 97 85 e0 23 86

1a 07 00 00 00 00 00 00 00 18 02 0a 05 04 05 06 07 08 1a 6c 37 41 76 c6 67 9c 61 22 b6 c0 7c e8
47 80 c9 13 9b 01 66 db 88 46 2e 6a cc fe ea d5 5a 12 ff f1 4d a6 c4 9d ef c4 cb 40 62 b4 90 cf
92 3f 36 ec 96 0f c9 54 43 00 e5 a9 3e 4d df f8 99 92 77 54 1a 27 64 00 79 f2 52 2c 48 39 6f b9
a6 ef 7d c3 07 4d 40 c3 8b d5 73 42 37 3f 6d e1 b5 50 67 87 ed 32 cd 23 75 f5 15 05 51 75 51 70
```



```
1a 07 00 00 00 00 00 00 00 18 01 0a 05 04 05 06 07 08 1a 6c 11 e1 00 b5 d6 e0 e8 59 d2 1a ba f6
45 c7 64 92 91 43 f4 6c 46 11 cd 78 ac 72 d5 49 7f dd ec 8b 6f 18 a7 9f 5e 55 1a 49 90 0b 29 6e
23 8b 8e 23 06 62 2a 07 ec be 56 14 39 02 91 60 ce c6 60 be 16 35 74 a3 b5 78 11 21 3b e6 2d d8
2a bb cc aa 9b 55 89 bc 43 a8 cc 5c 97 0f 92 25 f6 72 0b 99 0f 47 2e e0 71 15 4e 97 85 e0 23 86

1a 07 00 00 00 00 00 00 00 19 02 0a 05 04 05 06 07 08 1a 6c 37 41 76 c6 67 9c 61 22 b6 c0 7c e8
47 80 c9 13 9b 01 66 db 88 46 2e 6a cc fe ea d5 5a 12 ff f1 4d a6 c4 9d ef c4 cb 40 62 b4 90 cf
92 3f 36 ec 96 0f c9 54 43 ff e4 a9 3e 4d df f8 99 92 77 54 1a 27 64 00 79 f2 52 2c 48 39 6f b9
a6 ef 7d c3 07 4d 40 c3 8b d5 73 42 37 3f 6d e1 b5 50 67 87 ed 32 cd 23 75 f5 15 05 51 75 51 70
```



```
move = bytes.fromhex('00 00 00 00 00 00 00') # bytes
move = 1 # enum, equivalent to "PAPER"
nonce_client = bytes.fromhex('04 05 06 07 08') # bytes
move = bytes.fromhex('11 e1 00 ... e0 23 86') # bytes

move = bytes.fromhex('00 00 00 00 00 00 00') # bytes
move = 2 # enum, equivalent to "SCISSORS"
nonce_client = bytes.fromhex('04 05 06 07 08') # bytes
move = bytes.fromhex('37 41 76 ... 75 51 70') # bytes

# As a result:
move = 2 # SCISSORS
nonce_client = bytes.fromhex('04 05 06 07 08')
```



```
move = bytes.fromhex('00 00 00 00 00 00 00') # bytes
move = 1 # enum, equivalent to "PAPER"
nonce_client = bytes.fromhex('04 05 06 07 08') # bytes
move = bytes.fromhex('11 e1 00 ... e0 23 86') # bytes

move = bytes.fromhex('00 00 00 00 00 00 00') # bytes
move = 0x08_07_06_05_04_05_0a_02 # fixed64
move = bytes.fromhex('37 41 76 ... 75 51 70') # bytes

# As a result:
move = 1 # PAPER
nonce_client = bytes.fromhex('04 05 06 07 08')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/img_63aae782cacc2.png)