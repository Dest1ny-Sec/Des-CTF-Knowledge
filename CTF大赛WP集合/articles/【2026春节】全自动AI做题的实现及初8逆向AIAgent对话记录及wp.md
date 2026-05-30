# 【2026春节】全自动AI做题的实现及初8逆向AIAgent对话记录及wp

> 原文: https://www.ctfiot.com/304188.html
> ID: 304188

作者论坛账号：Tokeii

使用多模型做题，不能仅依靠一个模型去

有总结反思系统，每次做完题目会反思整个做题过程下次遇到会怎么办

有一个点子系统(这里不过多介绍，可以在微信公众号搜索”点子系统应该前面可以看到我写的一篇文章”)

支持多 Agent 协作，不同类型题目

可以分给更合适的子 Agent。

编写常见工具的calling func调用，比如python代码执行，字符串搜索，web请求，等可以大幅度的去减少token的使用

支持上下文压缩和会话分支，避免聊长了以后越聊越乱，这个我是参考的字节开源的上下文OpenViking项目实现的。

打tag系统，在每次生成反思，总结，wp时会对内容进行打Tag工作，方便下次调用

Each step should be a TESTABLE hypothesis (e.g., ‘Test for SQL injection on /login param’), not vague (e.g., ‘Try web attacks’)

Include WHAT tool to use and WHAT to look for in each step

First step should always be information gathering (read source, analyze binary, fetch target)

Have at least one backup approach from a different attack angle

Skip approaches marked as ‘failed’ — they already proved unsuccessful

Prioritize ‘pending’ ideas — they haven’t been tried yet

Build your plan around untried approaches

Aclasses.dexfile (Java/Kotlin code)

A native librarylibhajimi.sofor multiple architectures

reset

[1. 用jadx反编译APK，分析Java/Kotlin层逻辑，找到验证入口和native方法调用 2. 用IDA分析libhajimi.so (x86_64)，找到JNI函数和核心验证逻辑 3. 分析加密/验证算法，提取密钥和常量 4. 编写脚本逆向算法，恢复flag 5. 提交flag]

update

1

in_progress

What have you accomplished so far?

Are you making progress toward the flag?Continue with your current approach if it shows promise.

true

50

D:
AIAICTFworkdir52pojiechu8jadx_outsources

hajimi|native|loadLibrary|System.load|check|verify|flag|52pojie

– 检查节奏

– 解密帧

– 验证并解密

– 更新经验值

– 开始会话

– 调试绕过

true

100

D:
AIAICTFworkdir52pojiechu8jadx_outsources

verifyAndDecrypt|decryptFrames|checkRhythm|updateExp|startSession|setDebugBypass

update

1

done

找到NativeBridge类，加载libhajimi.so，关键native方法：checkRhythm, updateExp, decryptFrames, verifyAndDecrypt, startSessionBytes, setDebugBypass。这是音乐节奏游戏，需要分析SO中的验证逻辑。

update

2

in_progress

D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so

{"filter": "Java_*", "count": 50}

What have you accomplished so far?

Are you making progress toward the flag?Continue with your current approach if it shows promise.

{"filter": "*JNI*", "count": 50}

{"filter": "*OnLoad*", "count": 50}

0x237c0

map[addr:
0x5CCA0 size:
192]

["0x16781", "0x158da", "0x15cb1", "0x14e3e", "0x156ca", "0x14d20", "0x16dd4", "0x15e04", "0x1559a", "0x155ab", "0x154c7", "0x16de2"]

map[func:[map[addr:
0x238a0 name:
startSessionBytes] map[addr:
0x23e50 name:
checkRhythm] map[addr:
0x23f60 name:
updateExp] map[addr:
0x24520 name:
decryptFrames] map[addr:
0x24850 name:
verifyAndDecrypt] map[addr:
0x24ca0 name:
setDebugBypass]]]

0x24850

0x24520

0x238a0

0x23e50

0x23f60

0x2DDC0

0x2DF40

0x2E680

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

The APK has ahjm_pack.binfile in assets with header “HJM1” (0x484A4D31)

The SO has 6 JNI methods registered dynamically

is clearly AES encryption – it uses S-box (byte_17430), MixColumns operations, 10 rounds – this is AES-128 in CTR mode (XOR with keystream)

derives a key using xxHash-like operations

is the main decryption function that processes the HJM1 format

They check*v11 != 827148872which is 0x31_4D_4A_48 = “HJM1” in little-endian

(offset 4) is the type: 1 or 2

For type 1: usessub_2DDC0(key derivation) +sub_2DF40(AES decryption)

For type 2: more complex verification involvingsub_2E680

Magic: HJM1

Type: 2

field[2]: 1

field[3]: 0x40 = 64

field[4]: 0x40 = 64

field[5]: 0x78 = 120

For type 2 (v26 == 2):

It checksbyte_5CFF8 || byte_5D140orv23 & 1(anti-cheat flags)

It needsv27 >= 999(exp >= 999)

It callssub_2E680which is… [thinking truncated, was 7414 chars] …pted data and the current exp value. For type 2 data, it needs exp >= 999.

Whena3 == 2(PERFECT hit) and conditions are met:

(increment perfect counter)

Ifv32 >= 0xC(12 perfects) andv37 >= 0x3E7(exp >= 999):

(flag set)

(key stored)

Each step should be a TESTABLE hypothesis (e.g., ‘Test for SQL injection on /login param’), not vague (e.g., ‘Try web attacks’)

Include WHAT tool to use and WHAT to look for in each step

First step should always be information gathering (read source, analyze binary, fetch target)

Have at least one backup approach from a different attack angle

Skip approaches marked as ‘failed’ — they already proved unsuccessful

Prioritize ‘pending’ ideas — they haven’t been tried yet

Build your plan around untried approaches

APK withlibhajimi.sonative library

class with methods: startSessionBytes, checkRhythm, updateExp, decryptFrames, verifyAndDecrypt, setDebugBypass

asset file with “HJM1” magic header (564 bytes)

The SO has AES-like encryption (S-box at byte_17430, key expansion, MixColumns operations in sub_2DF40)

is clearly AES-128 CTR mode encryption/decryption

handles the HJM1 format parsing and decryption

takes byte[] and String, processes HJM1 data

takes byte[] and long, also processes HJM1 data

Start a rhythm game session

Player hits notes, accumulating experience/score

When score is high enough, decryptFrames or verifyAndDecrypt is called to decrypt the flag

Magic: 0x314D4A48 = “HJM1” (827148872)

Type field at offset 4 must be 2

Several other fields at offsets 8, 12, 16

It reads the HJM1 data

Calls sub_24FC0 (anti-debug check?)

For type==1: uses sub_2DDC0 (key derivation) and sub_2DF40 (AES decrypt) with key=0x5A5A5A5D (999 ^ 0x5A5A5A5A)

For type==2: calls sub_2E680 with a key derived from game state

Checks HJM1 magic (827148872 = 0x314D4A48)

v23 = v11[1] (type field at offset 4)

If type == 1 and size > 0x34:

v24 = a4 (exp value) ^ 0x5A5A5A5A (if v21 is true, i.e., anti-debug passed)

sub_2DDC0(v24, v11+6, v11+10, v29) – ke… [thinking truncated, was 12175 chars] …y have IDA open. Let me just decompile the remaining key functions and then write a solution script.

setDebugBypass – how to enable debug mode

sub_2E570 – how the key is generated in debug mode

sub_2EB00 – key derivation used in sub_2E680

sub_24CB0 – hash function used throughout

setDebugBypass (0x24CA0) – small, should be quick

sub_2E570 – key generation for debug mode

sub_24CB0 – hash function (used everywhere)

sub_2EB00 – key derivation for type 2

sub_2DAF0 – another hash function used in startSession

是 HJM1 格式，type=2，包含 64×64 位图（512字节加密数据）

解密路径在sub_2E680，需要一个密钥

有setDebugBypass和sub_2E570可能提供简化路径

reset

[1. 反编译setDebugBypass和sub_2E570，理解debug bypass路径的密钥生成 2. 反编译sub_24CB0(哈希)和sub_2EB00(密钥派生)，理解完整解密链 3. 提取AES S-box和所有常量，编写Python解密脚本 4. 解密hjm_pack.bin得到64x64位图，识别flag（可能是QR码） 5. 提交flag]

update

1

in_progress

0x24ca0

0x2E570

0x2DAF0

0x24CB0

0x2EB00

0x2EC80

0x2DD50

0x2EFD0

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

= SipHash-2-4

= XXHash64

= AES-128 CTR mode encryption/decryption (with S-box atbyte_17430)

= Key derivation using SipHash + XXHash

= Main decryption function for type=2 frames

= Another key derivation function

= Fisher-Yates shuffle (permutation generation)

= Text rendering to bitmap (converts string to bitmap using font data atbyte_17540)

Offset 0: magic “HJM1” (0x314D4A48 = 827148872)

Offset 4: type (1 or 2)

Offset 8: field2 (number of frames/rows)

Offset 12: field3 (height)

Offset 16: field4 (width)

Offset 20: padding/reserved

Offset 24: key material (16 bytes for type=1, or used differently for type=2)

Offset 40: IV (12 bytes)

Offset 52: encrypted data

It checks magic, type=2, and fields

Callssub_2EB00(a2, qword_5CFE8, v3+6, &v42)to derive AES key

Then in a loop, derives per-block keys usingsub_24CB0(XXHash64)

Callssub_2DF40(AES CTR) to decrypt each 256-byte block

If field2 > 1, generates a permutation usingsub_2EC80and rearranges rows

For type=2, whenbyte_5D140(debug bypass) is set:

Callssub_2E570to generate key

XORs with 0xA5A5A5A5A5A5A5A5

Passes tosub_2E680

Native library (libhjm.so)

hjm_pack.bin (encrypted data)

Java code

[map[addr:
0x17430 size:
256] map[addr:
0x17530 size:16]]

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

bytes 0-3: magic “HJM1” (0x314D4A48 = 827148872)

bytes 4-7: type (1 or 2)

bytes 8-11: some field (frame count for type 2)

bytes 12-15: height (for type 2)

bytes 16-19: width (for type 2)

bytes 20-23: unused?

bytes 24-39: salt/nonce (16 bytes)

bytes 40-51: IV (12 bytes)

bytes 52+: encrypted data

Key comes fromsub_2E570which generates a deterministic key based onqword_5CFE8anddword_5CFD0

The key is XORed with0xA5A5A5A5A5A5A5A5

Key isa4 ^ 0x5A5A5A5A(when v21=1)

derives AES key from the key + salt + nonce

is AES-128-CTR decryption

It checks magic == 827148872 (HJM1) and type == 2

It reads frame_count = v3[2], height = v3[3], width = v3[4]

It callssub_2EB00(a2, qword_5CFE8, v3+6, &v42)to derive AES key

a2 is the key passed in (after XOR with 0xA5A5A5A5A5A5A5A5)

qword_5CFE8 is some state value

v3+6 is the salt (bytes 24-39 of the file)

v42 is the output key (16 bytes)

Then it decrypts in 256-byte chunks usingsub_2DF40(AES-128-CTR)

If frame_count > 1, it also does a permutation usingsub_2EC80

Whenbyte_5D140is true, it callssub_2E570(a1, v19, v20)to get the key

Then XORs with0xA5A5A5A5A5A5A5A5

Then callssub_2E680(v38, v34)where v34 is the XORed key

It uses `qw… [thinking truncated, was 17111 chars] …ind the relevant Java code.

Read hjm_pack.bin header to understand its structure

Look at the APK assets for other data files

Write a Python script that implements the full decryption chain

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

Callssub_2EB00(key, qword_5CFE8, salt, &derived_key)to derive AES key

Then decrypts using AES-CTR (sub_2DF40) with the derived key and IV

If frame_count > 1, also does a permutation unshuffle

Whenbyte_5D140(debug bypass) is set, callssub_2E570to generate key

Otherwise usesqword_5CFF0

The key is XORed with0xA5A5A5A5A5A5A5A5whenv21(debug flag) is true

– this is the session key

– derives AES key from (a2=key_param, qword_5CFE8, salt_from_file)

Thea2parameter is the key passed tosub_2E680

When debug bypass:
v33 = sub_2E570(a1, v19, v20)orv33 = qword_5CFF0

(when v23=1, i.e., debug mode active)

Then callssub_2E680(v38, v34)where v38 is the buffer containing the file data

Read hjm_pack.bin header

Try to understand the complete decryption without the complex state machine

Maybe the “debug bypass” path withbyte_5D140=1gives us a simpler path

InverifyAndDecrypt, for type=2:
v33 = sub_2E570(a1, v19, v20)

computes a key based onqword_5CFE8anddword_5CFD0

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

true

`Let me analyze the decryption flow for hjm_pack.bin (type=2) based on the decompiled code.

Checks magic=0x314D4A48, type=2

Gets field2 (f…[truncated]`

1

3

D:
AIAICTFworkdir52pojiechu8jadx_outsources

NativeBridge|hajimi|hjm_pack|startSession|debugBypass|setDebug

true

30

What have you accomplished so far?

Are you making progress toward the flag?Continue with your current approach if it shows promise.

4

true

`Progress assessment:

HJM1 file format: magic(4) + type(4) + frame_count(4) + height(4) + width(4) + ?(4) + salt(16) + iv(12) + encry…[truncated]`

I’ve fully reverse-engineered the native library structure:

2

D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2

.*

true

5

– 初始化会话

– 检查节奏

– 更新经验

– 解密帧

– 验证并解密

– 设置调试绕过

50

D:
AIAICTFworkdir52pojiechu8jadx_outsources

startSession|verifyAndDecrypt|decryptFrames|setDebugBypass|beatMap|hjm_pack

true

50

D:
AIAICTFworkdir52pojiechu8jadx_outsources

startSession|setDebugBypass|beatMap|checkRhythm|updateExp

true

true

50

D:
AIAICTFworkdir52pojiechu8jadx_outsources

startSession(|f1107a|C0082f|C0021h|f318b

startSession|beatMap|setDebug|decryptFrames|verifyAndDecrypt

true

30

D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0

D:
AIAICTFworkdir52pojiechu8jadx_outsources

.startSession(

true

30

30

D:
AIAICTFworkdir52pojiechu8jadx_outsources

startSession

true

reset

[1. 用Python重新实现native库的解密逻辑：SipHash + XXHash64 + AES-CTR 2. 确定初始状态：找到beatMap数据和startSession参数 3. 模拟debug bypass路径(sub_2E570)生成密钥 4. 解密hjm_pack.bin并渲染64x64位图 5. 提交flag]

30

D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0

C0082f|f1143e|f1141c|f1144f

true

What have you accomplished so far?

Are you making progress toward the flag?Continue with your current approach if it shows promise.

3

`CRITICAL FINDING: beatMap = {0, 250, 500, 750} (4 entries, interval 250ms)

beatMap = [0, 250, 500, 750] as int[] -> converted to bytes (little-endian int32s) = 16 bytes

startSession is called with (timestamp, beatMapBytes, interval=250)

In startSessionBytes:

dword_5CFD0 = count of beats = 4

dword_5CFD4 = interval = 250

qword_5CFD8 = timestamp

qword_5CFE0 = XXHash64(beatMapBytes, 16, 0x1A8CBC5B802E097C)

qword_5CFE8 = qword_5CFE0 (initi…`

false

3

update

2

done

beatMap=[0,250,500,750], interval=250, 密钥不依赖时间戳

Check the error messages carefully — is there a specific fix you’re missing?

If the current approach keeps failing for the same reason, consider adjusting your method

If the errors are different each time, you’re still making progress — keep iterating

Useideastool (action: list) to review alternative approaches if needed

update

1

in_progress

200

0x2E570

0x2EB00

200

0x2E680

400

0x24850

100

0x24850

100

200

D:
AIAICTFworkdir52pojiechu8bitmap_debug_key_raw_r13b0.png

Is this a QR code or any recognizable pattern? Describe what you see in detail.

0x2DAF0

200

true

`Let me carefully trace the SipHash implementation in sub_2DAF0.

1

3

What have you accomplished so far?

Are you making progress toward the flag?Continue with your current approach if it shows promise.

I’ve identified the APK’s native library decryption flow: SipHash-2-4 + XXHash64 + AES-CTR

I’ve computed the key derivation chain but the decrypted output doesn’t look like a valid QR code/bitmap

The “debug_key raw” variant has row0=all zeros which is promising but the rest is noise

My AES-CTR implementation (how the IV/nonce is constructed)

My understanding of sub_2DF40 (the actual decryption function)

The key derivation path I’m following

Key derivation chain computed (SipHash + XXHash64), 4 key variants tried

“debug_key raw” variant shows row0=all zeros (promising) but rest is noise

Likely issue: AES-CTR implementation details in sub_2DF40 or sub_24CB0

0x2DF40

300

The AES key is loaded from[rdx](16 bytes) – this is the key pointer

The counter/IV is loaded from[rcx](12 bytes) – this is the IV pointer

The counter is a simple incrementing 32-bit value in the first 4 bytes

0x2E680

= offset into output buffer

= chunk size (min(256, remaining))

= AES key (16 bytes, two 8-byte values from sub_24CB0)

= IV/nonce (12 bytes)

0x24CB0

0x24F86

20

data_ref

["0x5CFE0", "0x5CFE8", "0x5CFF0", "0x5CFF8", "0x5D140"]

0x249a0

50

At 0x249a7/0x249b0:
rax = qword_5CFE0(which is the XXHash64 of beatmap)

At 0x249c0-0x24a2b: A splitmix64-like transformation is applied to modifyrax

At 0x24a33:
qword_5CFE8 = rax(the modified value)

(the original xxhash)

(some game state)

(experience counter)

Then splitmix64 on rsi -> gives rcx, rdx

If result is non-zero (r13b=1):

(shift right double)

rcx = 0 << 32 = 0

rdx = 0

rsi = 0x1A8CBC5B802E097C ^ 0 ^ 0 = 0x1A8CBC5B802E097C

splitmix64(0x1A8CBC5B802E097C) -> some value

Then rax gets XORed with the splitmix result

cmp byte_5D00C, 1

jnz 0x24a30 (jump to xor r13d, r13d)

sub_24FC0 is called, returns some value

The return value updates dword_5D004 and dword_5D008

If dword_5D008 >= 4, byte_5D00C = 1

What have you accomplished so far?

Are you making progress toward the flag?Continue with your current approach if it shows promise.

0x24890

30

0x2E860

20

Each step should be a TESTABLE hypothesis (e.g., ‘Test for SQL injection on /login param’), not vague (e.g., ‘Try web attacks’)

Include WHAT tool to use and WHAT to look for in each step

First step should always be information gathering (read source, analyze binary, fetch target)

Have at least one backup approach from a different attack angle

Skip approaches marked as ‘failed’ — they already proved unsuccessful

Prioritize ‘pending’ ideas — they haven’t been tried yet

Build your plan around untried approaches

Char 0: P (████, █···█, █···█, ████, █, █, █)

Char 1: J (··███, ···█, ···█, ···█, ···█, █··█, ·██)

Char 2: 2 (·███, █···█, ····█, ···█, ··█, ·█, █████)

Char 3: 0 (·███, █···█, █··██, █·█·█, ██··█, █···█, ·███) – this is 0 with a slash

Char 4: 2 (same pattern as char 2)

Char 5: 6 (·███, █, █, ████, █···█, █···█, ·███)

Char 6: N (█···█, ██··█, █·█·█, █··██, █···█, █···█, █···█)

Char 7: B (████, █···█, █···█, ████, █···█, █···█, ████)

Char 8: L (█, █, █, █, █, █, █████)

Char 9: D (████, █···█, █···█, █···█, █···█, █···█, ████)

FLAG{HJMWAPJ2026NBLD}

：核心原生库，包含所有加解密逻辑

：HJM1 格式的加密位图文件（待解密目标）

Java 层代码经过混淆（f1.h、Q0.AbstractC0080d等），但通过 jadx 反编译可识别关键 JNI 调用

Java 层的NativeBridge类暴露了多个 JNI 方法：startSession、checkRhythm、updateExp、verifyAndDecrypt

数据硬编码为[0, 250, 500, 750]，interval = 250——这是一个节奏游戏的节拍数据

文件头为HJM1（0x314D4A48），后跟 salt（16字节）、IV（12字节）和 512 字节密文

原生库中存在一条 debug bypass 路径（sub_2E570），密钥生成完全基于数学运算，不依赖运行时状态

地址 0x24b8b 处检查byte_5D140（debugBypass 标志）

若 debug 模式开启，调用sub_2E570计算密钥，否则使用游戏过程中积累的qword_5CFF0

密钥经过可选的0xA5A5A5A5A5A5A5A5XOR 变换后传入sub_2E680进行 AES-CTR 解密

：先验证 SipHash-2-4 和 XXHash64 的正确性（通过标准测试向量），再实现完整派生链。初次解密结果为随机数据（51% 比特置位），说明某个环节有误。

：测试了 debug_key raw、debug_key ^ 0xA5、qfe8 raw、qfe8 ^ 0xA5 四种组合，均未得到有意义输出。

：由于纯 Python 实现可能在细节上出错，转而使用 Unicorn 引擎直接模拟原生库函数。遇到 SSE4.1 指令（pinsrb）不支持的问题，但成功模拟了不含 SSE4.1 的子函数。

：用 Unicorn 模拟sub_2EB00（密钥派生）和sub_24CB0（XXHash64 折叠），结合 PyCryptodome 的 AES-CTR 完成解密。

读取dword_5CFD0（节拍数 = 4）和qword_5CFE8

计算r14 = 0x1A8CBC5B802E097C ^ qfe8

对r14执行 splitmix64 变换

循环 4 次（对应 4 个节拍），每次用 SipHash-2-4 混合结果

最终输出 debug_key

当r13b = 0（密码未验证，即byte_5D00C != 1），cmovz生效，rsi = rax（原始 debug_key，不做 XOR）

当r13b = 1（密码已验证），保持rsi = debug_key ^ 0xA5A5A5A5A5A5A5A5

用0x1A8CBC5B802E097C ^ qfe8和0x802E097C1A8CBC5B ^ qfe8作为 SipHash 的两个密钥

对[debug_key, qfe8]这 16 字节数据执行 SipHash-2-4

输出 16 字节的密钥材料var_68

行 0-19：全零（空白）

行 20-26：第一行文本（7 像素高的字符）

行 27：空白分隔行

行 28-34：第二行文本

行 35：空白

行 36-42：闭合花括号}

行 43-63：全零（空白）

中的cmovz指令决定是否对 debug_key 做^ 0xA5A5A5A5A5A5A5A5，取决于r13b（密码验证状态）。在 debug bypass 场景下应使用原始 debug_key（不做 XOR）。

AES-CTR 的计数器是小端序（little-endian），PyCryptodome 默认使用大端序，需要显式指定little_endian=True。

解密后的位图不是 QR 码，而是像素字体渲染的文本，需要通过列分割和字形比对来识别字符。

由于文章过长，文中部分代码精简，可以点击左下角进入原文阅读。

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码隐藏代码Downloaded:
https://down.52pojie.cn/9Ax3NVYO.7zSaved to:D:
AIAICTFworkdir52pojiechu8chu8.7zSize:
2955939bytesContent-Type:
application/x-7z-compressed
复制代码隐藏代码$ 7z x D:
AIAICTFworkdir52pojiechu8chu8.7z -> D:
AIAICTFworkdir52pojiechu8extracted7-Zip 24.06 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-05-26Scanning the drive for archives:1 file, 2955939 bytes (2887 KiB)Extracting archive: D:
AIAICTFworkdir52pojiechu8chu8.7z--Path = D:
AIAICTFworkdir52pojiechu8chu8.7zType = 7zPhysical Size = 2955939Headers Size = 275Method = LZMA2:6m 7zAESSolid = -Blocks = 1Everything is OkSize: 4459647Compressed: 2955939Extracted 1 files: 【2026春节】解题领红包之八 {Android 中级题} 出题老师：正己.apk
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8extractedD:
AIAICTFworkdir52pojiechu8extracted【2026春节】解题领红包之八{Android中级题} 出题老师：正己.apk
复制代码隐藏代码$ copy"D:
AIAICTFworkdir52pojiechu8extracted【2026春节】解题领红包之八 {Android 中级题} 出题老师：正己.apk""D:
AIAICTFworkdir52pojiechu8chu8.apk"
复制代码隐藏代码
🤖 助手 - 第 5 轮 [14:00:46]
🔨 执行命令
复制代码隐藏代码$ file"D:
AIAICTFworkdir52pojiechu8chu8.apk"
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8chu8.apk: Zip archive data,atleastv0.0toextract,compression method=deflate
复制代码隐藏代码$mkdir"D:
AIAICTFworkdir52pojiechu8apk_unzipped"&&cd/d"D:
AIAICTFworkdir52pojiechu8"&& 7z x chu8.apk -oapk_unzipped -y 2>&1 |head-30
复制代码隐藏代码 Directory: D:
AIAICTFworkdir52pojiechu8[32;1mMode [0m[32;1m LastWriteTime[0m [32;1;3m Length[0m[32;1m Name[0m[32;1m---- [0m [32;1m -------------[0m [32;1m ------[0m [32;1m----[0md---- 2026/2/24 14:00 [44;1mapk_unzipped[0m[31;1mSet-Location: [31;1mA positional parameter cannot be found that accepts argument'D:
AIAICTFworkdir52pojiechu8'.[0m[exitcode:
exitstatus1]
复制代码隐藏代码$7z x D:
AIAICTFworkdir52pojiechu8chu8.apk -> D:
AIAICTFworkdir52pojiechu8apk_unzipped (fallback)7-Zip24.06(x64) : Copyright (c)1999-2024Igor Pavlov :
2024-05-26Scanningthe drive for archives:
1file,4459647bytes(4356KiB)Extractingarchive: D:
AIAICTFworkdir52pojiechu8chu8.apk--Path = D:
AIAICTFworkdir52pojiechu8chu8.apkType = zipPhysical Size =4459647Everything is OkFiles:
161Size: 5290531Compressed:
4459647Extracted50files:
AndroidManifest.xml DebugProbesKt.bin META-INF META-INFandroidx.activity_activity-compo... [truncated3011bytes]... META-INFandroidx.profileinstaller_profileinstaller.version META-INFandroidx.savedstate_savedstate-ktx.version META-INFandroidx.savedstate_savedstate.version META-INFandroidx.startup_startup-runtime.version META-INFandroidx.tracing_tracing.version META-INFandroidx.versionedparcelable_versionedparcelable.version META-INFcom META-INFcomandroid META-INFcomandroidbuild META-INFcomandroidbuildgradle META-INFcomandroidbuildgradleapp-metadata.properties META-INFkotlinx_coroutines_android.version META-INFkotlinx_coroutines_core.version ... (truncated)
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedclasses.dex
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedlibarm64-v8alibhajimi.soD:
AIAICTFworkdir52pojiechu8apk_unzippedlibarmeabi-v7alibhajimi.soD:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86libhajimi.soD:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so
复制代码隐藏代码$wherejadx 2>nul ||echo"jadx not found"
复制代码隐藏代码$ file"D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so"
复制代码隐藏代码
📋 命令输出[14:01:12]
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so: ELF64-bit LSBsharedobject, x86-64, version1(SYSV), dynamically linked, BuildID[sha1]=270f490cb71fbaa3b51330dd72f8d9bc7738ffe0, stripped
复制代码隐藏代码TodoList reset with5task(s):⬜1. 用jadx反编译APK，分析Java/Kotlin层逻辑，找到验证入口和native方法调用⬜2. 用IDA分析libhajimi.so (x86_64)，找到JNI函数和核心验证逻辑⬜3. 分析加密/验证算法，提取密钥和常量⬜4. 编写脚本逆向算法，恢复flag⬜5. 提交flag
复制代码隐藏代码Updatedtask#1. Current TodoList:🔄1. 用jadx反编译APK，分析Java/Kotlin层逻辑，找到验证入口和native方法调用⬜2. 用IDA分析libhajimi.so (x86_64)，找到JNI函数和核心验证逻辑⬜3. 分析加密/验证算法，提取密钥和常量⬜4. 编写脚本逆向算法，恢复flag⬜5. 提交flag
复制代码隐藏代码$ jadx -d"D:
AIAICTFworkdir52pojiechu8jadx_out""D:
AIAICTFworkdir52pojiechu8chu8.apk"--no-res 2>&1 |tail-10
复制代码隐藏代码[31;1mjadx: [31;1mThe term'jadx'is not recognized as a name of a cmdlet,function, script file, or executable program.[0m[31;1m[31;1mCheck the spelling of the name, orifa path was included, verify that the path is correct and try again.[0m[exitcode:
exitstatus1]
复制代码隐藏代码$dir"D:
AIAICTFTools"2>nul &&dir"D:
AIAICTFToolsjadx*"2>nul
复制代码隐藏代码 Directory: D:
AIAICTFTools[32;1mMode [0m[32;1m LastWriteTime[0m [32;1;3m Length[0m[32;1m Name[0m[32;1m---- [0m [32;1m -------------[0m [32;1m ------[0m [32;1m----[0md---- 2026/2/14 9:19 [44;1mIDA[0md---- 2026/2/19 14:46 [44;1mjadx[0md---- 2026/2/19 14:53 [44;1mphp[0m-a--- 2026/2/19 14:40 25926183 apktool_2.12.1.jar-a--- 2026/2/24 13:49 524288 [31;1mphp.zip[0m-a--- 2025/5/6 10:19 599040 [32;1mupx.exe[0m-a--- 2026/2/11 16:46 5927424 [32;1mwsrx.exe[0md---- 2026/2/19 14:46 [44;1mjadx[0m
复制代码隐藏代码$dir"D:
AIAICTFToolsjadx"2>nul
复制代码隐藏代码 Directory: D:
AIAICTFToolsjadx[32;1mMode [0m[32;1m LastWriteTime[0m [32;1;3m Length[0m[32;1m Name[0m[32;1m---- [0m [32;1m -------------[0m [32;1m ------[0m [32;1m----[0md---- 2026/2/19 14:46 [44;1mbin[0md---- 2026/2/19 14:46 [44;1mlib[0m----- 1980/2/1 0:00 11357 LICENSE----- 1980/2/1 0:00 17870 README.md
复制代码隐藏代码$"D:
AIAICTFToolsjadxbinjadx.bat"-d"D:
AIAICTFworkdir52pojiechu8jadx_out""D:
AIAICTFworkdir52pojiechu8chu8.apk"--no-res 2>&1 |tail-10
复制代码隐藏代码[31;1mParserError: [0m[31;1m[36;1mLine |[0m[31;1m[36;1m[36;1m 1 | [0m … ext.Encoding]::
UTF8; "D:
AIAICTFToolsjadxbinjadx.bat" [36;1m-d[0m "D:AI …[0m[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m | [31;1m ~~[0m[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m | [31;1mUnexpected token '-d' in expression or statement.[0m[exit code: exit status1]
复制代码隐藏代码$ cmd /c"D:
AIAICTFToolsjadxbinjadx.bat"-d"D:
AIAICTFworkdir52pojiechu8jadx_out""D:
AIAICTFworkdir52pojiechu8chu8.apk"--no-res 2>&1
复制代码隐藏代码INFO - loading ...INFO - processing ...INFO - progress:
0of1394(0%)INFO - progress:
242of1394(17%)INFO - progress:
451of1394(32%)INFO - progress:
706of1394(50%)INFO - progress:
936of1394(67%)INFO - progress:
1262of1394(90%)ERROR - finished with errors, count:16[exitcode:
exitstatus1]
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAAbstractC0154a.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAb.java。。。。
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.java:11:>import com.zj.wuaipojie2026_2.NativeBridge;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.java:57:> case NativeBridge.SCORE_GOOD/* 1 */:.....
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2MainActivity.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2R.java
复制代码隐藏代码packagecom.zj.wuaipojie2026_2;importf1.h;importjava.nio.ByteBuffer;importjava.nio.ByteOrder;/* JADX INFO: loaded from: classes.dex */publicfinalclassNativeBridge{ publicstaticfinalint$stable=0; publicstaticfinalintERR_CHEAT=-7; publicstaticfinalNativeBridgeINSTANCE=newNativeBridge(); publicstaticfinalintSCORE_GOOD=1; publicstaticfinalintSCORE_MISS=0; publicstaticfinalintSCORE_PERFECT=2; static{ System.loadLibrary("hajimi"); } privateNativeBridge(){ } privatefinalnativevoidstartSessionBytes(longj2,byte[] bArr,inti2); publicfinalnativeintcheckRhythm(longj2,inti2,longj3,inti3); publicfinalnativebyte[] decryptFrames(byte[] bArr,longj2); publicfinalnativevoidsetDebugBypass(booleanz2); publicfinalvoidstartSession(longj2,int[] iArr,inti2){ h.e(iArr,"beatMapMs"); ByteBufferbyteBufferOrder=ByteBuffer.allocate(iArr.length *4).order(ByteOrder.LITTLE_ENDIAN); for(inti3 : iArr) { byteBufferOrder.putInt(i3); } byte[] bArrArray = byteBufferOrder.array(); h.d(bArrArray,"array(...)"); startSessionBytes(j2, bArrArray, i2); } publicfinalnativelongupdateExp(inti2,inti3,longj2); publicfinalnativebyte[] verifyAndDecrypt(byte[] bArr, String str);}
复制代码隐藏代码packagecom.zj.wuaipojie2026_2;importA.e;importQ0.AbstractC0080d;importa.AbstractC0154a;importandroid.content.res.Resources;importandroid.os.Build;importandroid.os.Bundle;importandroid.view.View;importandroid.view.ViewGroup;importandroid.view.Window;importandroidx.activity.A;importandroidx.activity.B;importandroidx.activity.l;importandroidx.activity.m;importandroidx.activity.n;importandroidx.activity.o;importandroidx.activity.p;importandroidx.activity.q;importandroidx.compose.ui.platform.C0204f0;importandroidx.lifecycle.E;importf1.h;importh1.a;/* JADX INFO: loaded from: classes.dex */publicfinalclassMainActivityextendsl{ @Override// androidx.activity.l, w0.AbstractActivityC0756a, android.app.Activity publicfinalvoidonCreate(Bundle bundle){ super.onCreate(bundle); inti2=m.f1921a; Aa2=A.f1870j; Bb2=newB(0,0, a2); Bb3=newB(m.f1921a, m.f1922b, a2); ViewdecorView=getWindow().getDecorView(); h.d(decorView,"window.decorView"); Resourcesresources=decorView.getResources(); h.d(resources,"view.resources"); booleanzBooleanValue=((Boolean) a2.d0(resources)).booleanValue(); Resourcesresources2=decorView.getResources(); h.d(resources2,"view.resources"); booleanzBooleanValue2=((Boolean) a2.d0(resources2)).booleanValue(); inti3=Build.VERSION.SDK_INT; qpVar=i3 >=29?newp() : i3 >=26?newo() :
newn(); Windowwindow=getWindow(); h.d(window,"window"); pVar.a(b2, b3, window, decorView, zBooleanValue, zBooleanValue2); eeVar=AbstractC0080d.f1133b; ViewGroup.LayoutParamslayoutParams=AbstractC0154a.f1861a; ViewchildAt=((ViewGroup) getWindow().getDecorView().findViewById(android.R.id.content)).getChildAt(0); C0204f0c0204f0=childAtinstanceofC0204f0 ? (C0204f0) childAt :
null; if(c0204f0 !=null) { c0204f0.setParentCompositionContext(null); c0204f0.setContent(eVar); return; } C0204f0c0204f02=newC0204f0(this); c0204f02.setParentCompositionContext(null); c0204f02.setContent(eVar); ViewdecorView2=getWindow().getDecorView(); if(E.c(decorView2) ==null) { E.g(decorView2,this); } if(E.d(decorView2) ==null) { decorView2.setTag(R.id.view_tree_view_model_store_owner,this); } if(a.A(decorView2) ==null) { a.a0(decorView2,this); } setContentView(c0204f02, AbstractC0154a.f1861a); }}
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:23:> privatefinalnativevoidstartSessionBytes(longj2,byte[] bArr,inti2);。。。。
复制代码隐藏代码packageQ0;importcom.zj.wuaipojie2026_2.NativeBridge;importo1.InterfaceC0603z;/* JADX INFO: loaded from: classes.dex */publicfinalclassrextendsY0.iimplementse1.e { /* JADX INFO: renamed from: m, reason: collision with root package name */ publicfinal/* synthetic */byte[] f1186m; /* JADX INFO: renamed from: n, reason: collision with root package name */ publicfinal/* synthetic */O f1187n; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ publicr(byte[] bArr, O o2, W0.d dVar){ super(2, dVar); this.f1186m = bArr; this.f1187n = o2; } @Override// e1.e publicfinalObjectN(Object obj, Object obj2){ return((r) c((W0.d) obj2, (InterfaceC0603z) obj)).g(S0.k.f1286a); } @Override// Y0.a publicfinalW0.dc(W0.d dVar, Object obj){ returnnewr(this.f1186m,this.f1187n, dVar); } @Override// Y0.a publicfinalObjectg(Object obj)throwsThrowable { R.c.Y(obj); returnNativeBridge.INSTANCE.decryptFrames(this.f1186m,this.f1187n.f1107a); }}
复制代码隐藏代码packageQ0;importcom.zj.wuaipojie2026_2.NativeBridge;importjava.util.List;importo1.InterfaceC0603z;importt.InterfaceC0680W;/* JADX INFO: loaded from: classes.dex */publicfinalclasszextendsY0.iimplementse1.e { /* JADX INFO: renamed from: m, reason: collision with root package name */ publicfinal/* synthetic */byte[] f1217m; /* JADX INFO: renamed from: n, reason: collision with root package name */ publicfinal/* synthetic */InterfaceC0680W f1218n; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ publicz(byte[] bArr, InterfaceC0680W interfaceC0680W, W0.d dVar){ super(2, dVar); this.f1217m = bArr; this.f1218n = interfaceC0680W; } @Override// e1.e publicfinalObjectN(Object obj, Object obj2){ return((z) c((W0.d) obj2, (InterfaceC0603z) obj)).g(S0.k.f1286a); } @Override// Y0.a publicfinalW0.dc(W0.d dVar, Object obj){ returnnewz(this.f1217m,this.f1218n, dVar); } @Override// Y0.a publicfinalObjectg(Object obj)throwsThrowable { R.c.Y(obj); NativeBridgenativeBridge=NativeBridge.INSTANCE; Listlist=N.f1106a; returnnativeBridge.verifyAndDecrypt(this.f1217m, n1.k.j0((String)this.f1218n.getValue()).toString()); }}
复制代码隐藏代码packageQ0;importE0.C0021h;importandroid.os.SystemClock;importcom.zj.wuaipojie2026_2.NativeBridge;importt.C0691d0;/* JADX INFO: loaded from: classes.dex */publicfinal/* synthetic */classvextendsf1.fimplementse1.a { /* JADX INFO: renamed from: q, reason: collision with root package name */ publicfinal/* synthetic */intf1199q; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ public/* synthetic */v(inti2, Object obj, Class cls, String str, String str2,inti3,inti4) { super(i2, obj, cls, str, str2, i3); this.f1199q = i4; } @Override// e1.a publicfinalObjecto(){ inti2; O o2; switch(this.f1199q) { case0: C0082fc0082f=(C0082f)this.f3686j; if(!((O) c0082f.f1144f.getValue()).f1109c) { longjElapsedRealtimeNanos=SystemClock.elapsedRealtimeNanos(); longj2=(jElapsedRealtimeNanos - c0082f.f1143e) /1000000; C0021hc0021h=c0082f.f1141c; if(j2 <0) { c0021h.getClass(); i2 =0; }else{ c0021h.getClass(); inti3=(int) (j2 % ((long)1000)); int[] iArr = (int[]) c0021h.f318b; intlength=iArr.length; inti4=Integer.MAX_VALUE; inti5=0; for(inti6=0; i6 < length; i6++) { intiAbs=Math.abs(i3 - iArr[i6]); intiMin=Math.min(iAbs,1000- iAbs); if(iMin < i4) { i5 = i6; i4 = iMin; } } i2 = i5; } longj3=(((long) i2) <<32) ^ jElapsedRealtimeNanos; longj4=j3 ^ (j3 <<13); longj5=j4 ^ (j4 >>7); longj6=j5 ^ (j5 <<17); C0691d0c0691d0=c0082f.f1144f; inti7=((O) c0691d0.getValue()).f1107a >=50?1:0; NativeBridgenativeBridge=NativeBridge.INSTANCE; intiCheckRhythm=nativeBridge.checkRhythm(jElapsedRealtimeNanos, i2, j6, i7); longjUpdateExp=nativeBridge.updateExp(iCheckRhythm, i2, j6); if(jUpdateExp <0|| iCheckRhythm == -7) { o2 =newO(((O) c0691d0.getValue()).f1107a, Q.Cheat,true); }else{ Oo3=(O) c0691d0.getValue(); Qq2=iCheckRhythm !=0? iCheckRhythm !=1? iCheckRhythm !=2? Q.None : Q.Perfect : Q.Good : Q.Miss; o3.getClass(); o2 =newO(jUpdateExp, q2,false); } c0691d0.setValue(o2); } break; caseNativeBridge.SCORE_GOOD/* 1 */: ((androidx.activity.x)this.f3686j).d(); break; default: ((androidx.activity.x)this.f3686j).d(); break; } returnS0.k.f1286a; }}
复制代码隐藏代码Updatedtask#1. Current TodoList:✅1. 用jadx反编译APK，分析Java/Kotlin层逻辑，找到验证入口和native方法调用 → 找到NativeBridge类，加载libhajimi.so，关键native方法：checkRhythm, updateExp, decryptFrames, verifyAndDecrypt, startSessionBytes, setDebugBypass。这是音乐节奏游戏，需要分析SO中的验证逻辑。⬜2. 用IDA分析libhajimi.so (x86_64)，找到JNI函数和核心验证逻辑⬜3. 分析加密/验证算法，提取密钥和常量⬜4. 编写脚本逆向算法，恢复flag⬜5. 提交flag
复制代码隐藏代码Updatedtask#2. Current TodoList:✅1. 用jadx反编译APK，分析Java/Kotlin层逻辑，找到验证入口和native方法调用 → 找到NativeBridge类，加载libhajimi.so，关键native方法：checkRhythm, updateExp, decryptFrames, verifyAndDecrypt, startSessionBytes, setDebugBypass。这是音乐节奏游戏，需要分析SO中的验证逻辑。🔄2. 用IDA分析libhajimi.so (x86_64)，找到JNI函数和核心验证逻辑⬜3. 分析加密/验证算法，提取密钥和常量⬜4. 编写脚本逆向算法，恢复flag⬜5. 提交flag
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedD:
AIAICTFworkdir52pojiechu8apk_unzippedAndroidManifest.xmlD:
AIAICTFworkdir52pojiechu8apk_unzippedDebugProbesKt.binD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.activity_activity-compose.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.activity_activity-ktx.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.activity_activity.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.annotation_annotation-experimental.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.arch.core_core-runtime.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.autofill_autofill.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.animation_animation-core.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.animation_animation.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.foundation_foundation-layout.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.foundation_foundation.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.material3_material3.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.material_material-icons-core.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.material_material-ripple.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.runtime_runtime-saveable.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.runtime_runtime.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui-geometry.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui-graphics.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui-text.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui-tooling-preview.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui-unit.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui-util.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.compose.ui_ui.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.core_core-ktx.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.core_core.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.customview_customview-poolingcontainer.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.emoji2_emoji2.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.interpolator_interpolator.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-livedata-core.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-process.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-runtime-ktx.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-runtime.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-viewmodel-ktx.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-viewmodel-savedstate.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.lifecycle_lifecycle-viewmodel.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.profileinstaller_profileinstaller.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.savedstate_savedstate-ktx.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.savedstate_savedstate.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.startup_startup-runtime.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.tracing_tracing.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.versionedparcelable_versionedparcelable.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFcomD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFcomandroidD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFcomandroidbuildD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFcomandroidbuildgradleD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFcomandroidbuildgradleapp-metadata.propertiesD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFkotlinx_coroutines_android.version
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedDebugProbesKt.binD:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin
复制代码隐藏代码Nofiles found.
复制代码隐藏代码Nofiles found.
复制代码隐藏代码$ file"D:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin"
复制代码隐藏代码withopen(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin","rb")asf: data = f.read()print(f"Size:{len(data)}bytes")print(f"First 64 bytes hex:{data[:64].hex()}")print(f"First 64 bytes:{data[:64]}")print(f"Last 32 bytes hex:{data[-32:].hex()}")
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin:
data
复制代码隐藏代码Size:
564bytesFirst64byteshex: 484a4d3102000000010000004000000040000000780000000f1e2d3c4b5a69788796a5b4c3d2e1f0112233445566778899aabbcc9641cd80feda2af5fb95dd2cFirst64bytes:b'HJM1x02x00x00x00x01x00x00x00@x00x00x00@x00x00x00xx00x00x00x0fx1e-<KZixx87x96xa5xb4xc3xd2xe1xf0x11"3DUfwx88x99xaaxbbxccx96Axcdx80xfexda*xf5xfbx95xdd,'Last32byteshex: d4c4d122d0f243d6770260c018b66ed6db8a1b903acbaa215ca816690497ccc1
复制代码隐藏代码{"success":
true,"session": { "session_id":"2769f686", "input_path":"D:\AI\AICTF\workdir\52pojie\chu8\apk_unzipped\lib\x86_64\libhajimi.so", "filename":"libhajimi.so", "created_at":"2026-02-24T14:03:23.380456", "last_accessed":"2026-02-24T14:03:23.380456", "is_analyzing":
false, "metadata": {} },"message":"Binary opened successfully: libhajimi.so"}
复制代码隐藏代码[{ "data":[], "next_offset":
null}]
复制代码隐藏代码[{ "data":[ { "addr":"0x237c0", "name":"JNI_OnLoad", "size":"0x8e" } ], "next_offset":
null}]
复制代码隐藏代码[{ "data":[ { "addr":"0x237c0", "name":"JNI_OnLoad", "size":"0x8e" } ], "next_offset":
null}]
复制代码隐藏代码{"addr":"0x237c0","code":"__int64 __fastcall JNI_OnLoad(__int64 a1)n{n unsigned int v1; // ebxn __int64 v2; // raxn _QWORD v4[3]; // [rsp+0h] [rbp-18h] BYREFnn v4[1] = __readfsqword(0x28u); /*0x237ce*/n v4[0] = 0; /*0x237d3*/n v1 = -1; /*0x237e9*/n if ( !(*(unsigned int (__fastcall **)(__int64, _QWORD *, __int64))(*(_QWORD *)a1 + 48LL))(a1, v4, 65542) )n {n v2 = (*(__int64 (__fastcall **)(_QWORD, const char *))(*(_QWORD *)v4[0] + 48LL))( /*0x23800*/n v4[0],n "com/zj/wuaipojie2026_2/NativeBridge");n if ( v2 )n return (*(unsigned int (__fastcall **)(_QWORD, __int64, char **, __int64))(*(_QWORD *)v4[0] + 1720LL))(n v4[0],n v2,n off_5CCA0,n 6) != 0n ? -1n : 0x10006;n }n return v1; /*0x23843*/n}"}
复制代码隐藏代码[{ "addr":"0x5CCA0", "data":"0x81 0x67 0x1 0x0 0x0 0x0 0x0 0x0 0xda 0x58 0x1 0x0 0x0 0x0 0x0 0x0 0xa0 0x38 0x2 0x0 0x0 0x0 0x0 0x0 0xb1 0x5c 0x1 0x0 0x0 0x0 0x0 0x0 0x3e 0x4e 0x1 0x0 0x0 0x0 0x0 0x0 0x50 0x3e 0x2 0x0 0x0 0x0 0x0 0x0 0xca 0x56 0x1 0x0 0x0 0x0 0x0 0x0 0x20 0x4d 0x1 0x0 0x0 0x0 0x0 0x0 0x60 0x3f 0x2 0x0 0x0 0x0 0x0 0x0 0xd4 0x6d 0x1 0x0 0x0 0x0 0x0 0x0 0x4 0x5e 0x1 0x0 0x0 0x0 0x0 0x0 0x20 0x45 0x2 0x0 0x0 0x0 0x0 0x0 0x9a 0x55 0x1 0x0 0x0 0x0 0x0 0x0 0xab 0x55 0x1 0x0 0x0 0x0 0x0 0x0 0x50 0x48 0x2 0x0 0x0 0x0 0x0 0x0 0xc7 0x54 0x1 0x0 0x0 0x0 0x0 0x0 0xe2 0x6d 0x1 0x0 0x0 0x0 0x0 0x0 0xa0 0x4c 0x2 0x0 0x0 0x0 0x0 0x0 0x0 0x11 0x5 0x0 0x0 0x0 0x0 0x0 0x90 0x92 0x3 0x0 0x0 0x0 0x0 0x0 0xc0 0x93 0x3 0x0 0x0 0x0 0x0 0x0 0xae 0x67 0x1 0x0 0x0 0x0 0x0 0x0 0x10 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x8 0x0 0x0 0x0 0x0 0x0 0x0 0x0"}]
复制代码隐藏代码importstructdata =bytes([0x81,0x67,0x1,0x0,0x0,0x0,0x0,0x0,0xda,0x58,0x1,0x0,0x0,0x0,0x0,0x0,0xa0,0x38,0x2,0x0,0x0,0x0,0x0,0x0, 0xb1,0x5c,0x1,0x0,0x0,0x0,0x0,0x0,0x3e,0x4e,0x1,0x0,0x0,0x0,0x0,0x0,0x50,0x3e,0x2,0x0,0x0,0x0,0x0,0x0, 0xca,0x56,0x1,0x0,0x0,0x0,0x0,0x0,0x20,0x4d,0x1,0x0,0x0,0x0,0x0,0x0,0x60,0x3f,0x2,0x0,0x0,0x0,0x0,0x0, 0xd4,0x6d,0x1,0x0,0x0,0x0,0x0,0x0,0x04,0x5e,0x1,0x0,0x0,0x0,0x0,0x0,0x20,0x45,0x2,0x0,0x0,0x0,0x0,0x0, 0x9a,0x55,0x1,0x0,0x0,0x0,0x0,0x0,0xab,0x55,0x1,0x0,0x0,0x0,0x0,0x0,0x50,0x48,0x2,0x0,0x0,0x0,0x0,0x0, 0xc7,0x54,0x1,0x0,0x0,0x0,0x0,0x0,0xe2,0x6d,0x1,0x0,0x0,0x0,0x0,0x0,0xa0,0x4c,0x2,0x0,0x0,0x0,0x0,0x0])
# JNINativeMethod: { const char* name, const char* signature, void* fnPtr } - 3 pointers eachforiinrange(6): off = i *24 name_ptr = struct.unpack_from('<Q', data, off)[0] sig_ptr = struct.unpack_from('<Q', data, off+8)[0] fn_ptr = struct.unpack_from('<Q', data, off+16)[0] print(f"Method{i}: name=0x{name_ptr:x}, sig=0x{sig_ptr:x}, fn=0x{fn_ptr:x}")
复制代码隐藏代码Method0: name=0x16781, sig=0x158da, fn=0x238a0Method1: name=0x15cb1, sig=0x14e3e, fn=0x23e50Method2: name=0x156ca, sig=0x14d20, fn=0x23f60Method3: name=0x16dd4, sig=0x15e04, fn=0x24520Method4: name=0x1559a, sig=0x155ab, fn=0x24850Method5: name=0x154c7, sig=0x16de2, fn=0x24ca0
复制代码隐藏代码[{ "addr":"0x16781", "value":"startSessionBytes"},{ "addr":"0x158da", "value":"(J[BI)V"},{ "addr":"0x15cb1", "value":"checkRhythm"},{ "addr":"0x14e3e", "value":"(JIJI)I"},{ "addr":"0x156ca", "value":"updateExp"},{ "addr":"0x14d20", "value":"(IIJ)J"},{ "addr":"0x16dd4", "value":"decryptFrames"},{ "addr":"0x15e04", "value":"([BJ)[B"},{ "addr":"0x1559a", "value":"verifyAndDecrypt"},{ "addr":"0x155ab", "value":"([BLjava/lang/String;)[B"},{ "addr":"0x154c7", "value":"setDebugBypass"},{ "addr":"0x16de2", "value":"(Z)V"}]
复制代码隐藏代码{"func":[ { "addr":"0x238a0", "name":"startSessionBytes", "ok":
true, "error":
null, "dir":"vibe", "dir_error":
null }, { "addr":"0x23e50", "name":"checkRhythm", "ok":
true, "error":
null, "dir":"vibe", "dir_error":
null }, { "addr":"0x23f60", "name":"updateExp", "ok":
true, "error":
null, "dir":"vibe", "dir_error":
null }, { "addr":"0x24520", "name":"decryptFrames", "ok":
true, "error":
null, "dir":"vibe", "dir_error":
null }, { "addr":"0x24850", "name":"verifyAndDecrypt", "ok":
true, "error":
null, "dir":"vibe", "dir_error":
null }, { "addr":"0x24ca0", "name":"setDebugBypass", "ok":
true, "error":
null, "dir":"vibe", "dir_error":
null }]}
复制代码隐藏代码{"addr":"0x24850","code":"__int64 __fastcall verifyAndDecrypt(__int64 *a1, __int64 a2, __int64 a3, __int64 a4)n{n __int64 v5; // raxn int v8; // eaxn unsigned int v9; // ebpn unsigned __int64 v10; // rbxn char *v11; // r12n size_t v12; // rdxn char *v13; // rbxn __int64 v14; // raxn __int64 v15; // r15n __int64 v17; // raxn __int64 v18; // rcxn __int64 v19; // rsin __int64 v20; // rdxn __int64 v21; // raxn u...
复制代码隐藏代码{"addr":"0x24520","code":"__int64 __fastcall decryptFrames(__int64 a1, __int64 a2, __int64 a3, __int64 a4)n{n int v7; // eaxn __int64 v8; // rdxn unsigned int v9; // ebpn size_t v10; // r12n _DWORD *v11; // rbxn __int64 v12; // raxn __int64 v13; // r15n __int64 v15; // raxn __int64 v16; // rcxn __int64 v17; // rsin __in...
复制代码隐藏代码{"addr":"0x238a0","code":"unsigned __int64 __fastcall startSessionBytes(__int64 a1, __int64 a2, __int64 a3, __int64 a4, int a5)n{n int v9; // eaxn unsigned int v10; // ecxn unsigned int v11; // ecxn unsigned int v12; // ebxn __int64 v13; // r14n unsigned __int64 v14; // rcxn __int64 v15; // rsin __int64 v16; // rdin unsigned __int64 v17; // rdxn __int64 v....
复制代码隐藏代码{"addr":"0x23e50","code":"__int64 __fastcall checkRhythm(__int64 a1, __int64 a2, __int64 a3, int a4, __int64 a5, int a6)n{n __int64 result; // raxn unsigned __int64 v7; // rdxn unsigned __int64 v8; // rsin unsigned int v9; // eaxn int v10; // esin int v11; // eaxn int v12; // edin char v13; // r8n int v14; // ecxn int v15; // r10dnn result = 0; /*0x23...
复制代码隐藏代码{"addr":"0x23f60","code":"__int64 __fastcall updateExp(__int64 a1, __int64 a2, int a3, int a4, __int64 a5)n{n __int64 v5; // r15n __int64 v6; // rbpn __int64 v7; // r13n __int64 v8; // r14n __int64 v9; // rbxn unsigned __int64 v10; // r12n __int64 v11; // raxn unsigned __int64 v12; // rdxn unsigned __int64 v13; // raxn unsigned __int64 v14; // raxn unsigned __int64 v15; // rbxn unsigned __int64 v16; // rbxn unsigned __int64 v17; // rcxn __int64 v18; // r9n bool v19; // bpn __int64 v20; // rdxn unsigned int v21; // edin....
复制代码隐藏代码{"addr":"0x2DDC0","code":"unsigned __int64 __fastcall sub_2DDC0(__int64 a1, _QWORD *a2, __int64 a3, unsigned __int64 *a4)n{n __int64 v6; // raxn unsigned __int64 v7; // rsin unsigned __int64 v8; // r8n unsigned __int64 v9; // raxn __int64 v10; // rdxn __int64 v11; // raxn unsigned __int64 v12; // raxn unsig.........
复制代码隐藏代码{"addr":"0x2DF40","code":"unsigned __int64 __fastcall sub_2DF40(__int64 a1, unsigned __int64 a2, const __m128i *a3, _BYTE *a4)n{n int v4; // eaxn unsigned int v5; // edxn __int64 v6; // r14n __m128i inserted; // xmm0n __int64 v8; // rbxn int v9; // kr00_4n int v10; // ecxn __m128i v11; // xmm0n __m128i si128; // xmm1n __m128i v13; // xmm2n __int....
复制代码隐藏代码{"addr":"0x2E680","code":"__int64 __fastcall sub_2E680(_QWORD *a1, __int64 a2)n{n _QWORD *v2; // r12n _DWORD *v3; // r14n unsigned __int64 v4; // raxn __int64 v5; // rdxn __int64 v6; // rbpn int v7; // ecxn int v8; // edin unsigned int v9; // edin size_t v10; // rdin unsigned __int64 v11; // rbxn unsigned __int64 v12; // r13n void **v13; // r14n __int64 v14; // raxn __int64 v15; // r15n __int64 v16; // raxn uns...👤 用户 [14:04:36]
复制代码隐藏代码Offset 0:"HJM1"(magic)Offset 4:
type(uint32)-valueis2Offset 8:
field2(uint32)-valueis1Offset 12:
field3(uint32)-0x40=64Offset 16:
field4(uint32)-0x40=64Offset 20:
field5(uint32)-0x78=120Offset 24:
16bytes-key/IVmaterialOffset 40:
12bytes-morekeymaterialOffset 52:
encrypteddata
复制代码隐藏代码484a4d31 02000000 01000000 40000000 40000000 78000000
复制代码隐藏代码0f1e2d3c 4b5a6978 8796a5b4 c3d2e1f0
复制代码隐藏代码11223344 5566778899aabbcc
复制代码隐藏代码TodoList reset with5task(s):⬜1. 反编译setDebugBypass和sub_2E570，理解debugbypass路径的密钥生成⬜2. 反编译sub_24CB0(哈希)和sub_2EB00(密钥派生)，理解完整解密链⬜3. 提取AES S-box和所有常量，编写Python解密脚本⬜4. 解密hjm_pack.bin得到64x64位图，识别flag（可能是QR码）⬜5. 提交flag
复制代码隐藏代码Updated task#1. Current TodoList:🔄1. 反编译setDebugBypass和sub_2E570，理解debugbypass路径的密钥生成⬜2. 反编译sub_24CB0(哈希)和sub_2EB00(密钥派生)，理解完整解密链⬜3. 提取AES S-box和所有常量，编写Python解密脚本⬜4. 解密hjm_pack.bin得到64x64位图，识别flag（可能是QR码）⬜5. 提交flag
复制代码隐藏代码{"addr":"0x24ca0","code":"void __fastcall setDebugBypass(__int64 a1, __int64 a2, char a3)n{n byte_5D140 = a3 == 1; /*0x24ca3*/n}"}
复制代码隐藏代码{"addr":"0x2E570","code":"__int64 sub_2E570()n{n int v0; // ebpn int v1; // ebxn __int64 v2; // r14n unsigned __int64 v3; // rsin __int64 v4; // rcxn unsigned __int64 v5; // r15n __int64 v7; // [rsp+0h] [rbp-48h] BYREFn int v8; // [rsp+8h] [rbp-40h]n int v9; // [rsp+Ch] [rbp-3Ch]n int v10; // [rsp+10h] [rbp-38h]n int v11; // [rsp+14h] [rbp-34h]n unsigned __int64 v12; // [rsp+18h] [rbp-30h]nn v12 = __readfsqword(0x28u); /*0x2e585*/n v0 = dword_5CFD0; /*0x2e58a*/n v1 = 0; /*0x2e590*/n if ( dword_5CFD0 <= 0 ) /*0x2e594*/n return 0; /*0x2e650*/n v2 =... [truncated 1474 bytes] ...)))n ^ ((0xBF58476D1CE4E5B9LLn * (((qword_5CFE8 ^ 0x1A8CBC5B802E097CLL) - 0x61C8864680B583EBLL)n ^ (((qword_5CFE8 ^ 0x1A8CBC5B802E097CuLL) - 0x61C8864680B583EBLL) >> 30))) >> 27));n v4 = v3 ^ (v3 >> 31); /*0x2e5f2*/n v5 = qword_5CFE8 ^ 0x802E097C1A8CBC5BLL; /*0x2e5ff*/n do /*0x2e64c*/n {n v7 = v4; /*0x2e615*/n v8 = v1 % v0; /*0x2e619*/n v9 = 0; /*0x2e61d*/n v10 = v1; /*0x2e625*/n v11 = 2; /*0x2e629*/n v4 = sub_2DAF0(&v7, 24, v2, v5); /*0x2e644*/n ++v1; /*0x2e647*/n }n while ( v1 != 12 ); /*0x2e64c*/n return v4; /*0x2e665*/n}"}
复制代码隐藏代码{"addr":"0x2DAF0","code":"__int64 __fastcall sub_2DAF0(unsigned __int8 *a1, __int64 a2, __int64 a3, __int64 a4)n{n __int64 v4; // r9n __int64 v5; // r8n __int64 v6; // raxn __int64 v7; // rdxn unsigned __int64 v8; // r10n __int64 v9; // r11n __int64 v10; // r9n __int64 v11; // rbxn __int64 v12; // r8n __int64 v13; // rdxn __int64 v14; // raxn __int64 v15; // rdxn __int64 v16; // r9n __int64 v17; // raxn __int64 v18; // r8n __int64 v19; // rdxn __int64 v20; // r9n __int64 v21; // r8n __int64 v22; // raxn __int64 v23; // rdxn __int64 v24; // r9... [truncated 5807 bytes] ...^ __ROL8__(v55, 21); /*0x2dcea*/n v60 = v58 + v56; /*0x2dced*/n v61 = v60 ^ __ROL8__(v58, 13); /*0x2dcf4*/n v62 = v59 + __ROL8__(v57, 32); /*0x2dcfb*/n v63 = v62 ^ __ROL8__(v59, 16); /*0x2dd02*/n v64 = v63 + __ROL8__(v60, 32); /*0x2dd05*/n v65 = v61 + v62; /*0x2dd0c*/n v66 = v65 ^ __ROL8__(v61, 17); /*0x2dd13*/n v67 = v64 ^ __ROL8__(v63, 21); /*0x2dd1a*/n v68 = v67 + __ROL8__(v65, 32); /*0x2dd24*/n v69 = (v66 + v64) ^ __ROL8__(v66, 13); /*0x2dd32*/n return (v69 + v68) ^ __ROL8__(v68 ^ __ROL8__(v67, 16), 21) ^ __ROL8__(v69, 17) ^ __ROL8__(v69 + v68, 32); /*0x2dd49*/n}"}
复制代码隐藏代码{"addr":"0x24CB0","code":"unsigned __int64 __fastcall sub_24CB0(unsigned __int8 *a1, unsigned __int64 a2, unsigned __int64 a3)n{n unsigned __int64 v3; // r9n unsigned __int64 v4; // rbpn unsigned __int64 v5; // r13n unsigned __int64 v6; // r12n __int64 v7; // r15n __int64 v8; // r14n __int64 v9; // rbxn __int64 v10; // r11n unsigned __int64 v11; // r11n unsigned __int64 v12; // r11n unsigned __int64 v13; // rsin unsigned __int8 *v14; // r10n bool v15; // ccn unsigned __int64 v16; // rdin unsigned __int64 v17; // r10n __int64 v18; // r11n unsigned __in... [truncated 4974 bytes] ...t8 *)v16), 11))n ^ (0x27D4EB2F165667C5LL * *(unsigned __int8 *)(v16 + 1)),n 11))n ^ (0x27D4EB2F165667C5LL * *(unsigned __int8 *)(v16 + 2)),n 11))n ^ (0x27D4EB2F165667C5LL * *(unsigned __int8 *)(v16 + 3)),n 11);n v16 += 4LL; /*0x24f7d*/n }n while ( v16 < v3 ); /*0x24f84*/n }nLABEL_18:n v20 = 0x165667B19E3779F9LL /*0x24f86*/n * ((0xC2B2AE3D27D4EB4FLL * (v13 ^ (v13 >> 33))) ^ ((0xC2B2AE3D27D4EB4FLL * (v13 ^ (v13 >> 33))) >> 29));n return v20 ^ HIDWORD(v20); /*0x24fac*/n}"}
复制代码隐藏代码{"addr":"0x2EB00","code":"unsigned __int64 __fastcall sub_2EB00(__int64 a1, __int64 a2, _QWORD *a3, unsigned __int64 *a4)n{n __int64 v6; // raxn unsigned __int64 v7; // rsin unsigned __int64 v8; // r8n unsigned __int64 v9; // raxn __int64 v10; // rdxn __int64 v11; // raxn unsigned __int64 v12; // raxn unsigned __int64 v13; // rcxn _QWORD v15[5]; // [rsp+0h] [rbp-28h] BYREFnn v15[2] = __readfsqword(0x28u); /*0x2eb16*/n v15[0] = a1; /*0x2eb35*/n v15[1] = a2; /*0x2eb39*/n v6 = sub_2DAF0((unsigned __int8 *)v15, 16, a2 ^ 0x1A8CBC5B802E097CLL, a2 ^ 0x802E097C1A8CB... [truncated 2294 bytes] ...((0x85EBCA77C2B2AE63LL - 0x61C8864E7A143579LL * v11) >> 33))) >> 29));n v13 = 0x165667B19E3779F9LL /*0x2ec41*/n * ((0xC2B2AE3D27D4EB4FLLn * ((0x85EBCA77C2B2AE63LL - 0x61C8864E7A143579LL * v10)n ^ ((0x85EBCA77C2B2AE63LL - 0x61C8864E7A143579LL * v10) >> 33)))n ^ ((0xC2B2AE3D27D4EB4FLLn * ((0x85EBCA77C2B2AE63LL - 0x61C8864E7A143579LL * v10)n ^ ((0x85EBCA77C2B2AE63LL - 0x61C8864E7A143579LL * v10) >> 33))) >> 29));n *a4 = v12 ^ HIDWORD(v12); /*0x2ec4f*/n a4[1] = v13 ^ HIDWORD(v13); /*0x2ec52*/n return __readfsqword(0x28u); /*0x2ec66*/n}"}
复制代码隐藏代码{"addr":"0x2EC80","code":"__int64 __fastcall sub_2EC80(int a1, __int64 a2, __int64 *a3)n{n __int64 result; // raxn unsigned __int64 v6; // rcxn __int64 v7; // rdxn __m128i si128; // xmm0n __int64 v9; // rdin __m128i v10; // xmm1n __m128i v11; // xmm2n __int64 v12; // rdin unsigned __int64 v13; // rcxn unsigned __int64 v14; // rbxn __int64 v15; // r10n unsigned __int64 v16; // rdxnn result = *a3; /*0x2ec8f*/n v6 = (a3[1] - *a3) >> 2; /*0x2ec99*/n if ( v6 >= a1 ) /*0x2eca0*/n {n if ( v6 > a1 ) /*0x2ecaf*/n {n result += 4LL * a1; /*0x2ecb1*/... [truncated 2890 bytes] ...*)(v12 + 4 * v15) = *(_DWORD *)(v12 + 4 * v16); /*0x2edab*/n *(_DWORD *)(v12 + 4 * v16) = result; /*0x2edaf*/n --v13; /*0x2edb2*/n v14 -= 0x61C8864680B583EBLL; /*0x2edb5*/n }n while ( v13 > 2 ); /*0x2edbc*/n }n return result; /*0x2edbc*/n }n }n elsen {n v7 = 0; /*0x2eccb*/n }n do /*0x2ed39*/n {n *(_DWORD *)(result + 4 * v7) = v7; /*0x2ed30*/n ++v7; /*0x2ed33*/n }n while ( a1 != v7 ); /*0x2ed39*/n goto LABEL_12; /*0x2ed39*/n }n return result; /*0x2edbe*/n}"}
复制代码隐藏代码{"addr":"0x2DD50","code":"void __fastcall sub_2DD50(__int64 a1, signed __int64 a2)n{n char *v2; // raxn char *v3; // r15nn *(_OWORD *)a1 = 0; /*0x2dd58*/n *(_QWORD *)(a1 + 16) = 0; /*0x2dd5b*/n if ( a2 ) /*0x2dd66*/n {n if ( a2 < 0 ) /*0x2dd6b*/n sub_2EAF0(a1); /*0x2dd9f*/n v2 = (char *)operator new(a2); /*0x2dd73*/n *(_QWORD *)a1 = v2; /*0x2dd78*/n v3 = &v2[a2]; /*0x2dd7e*/n *(_QWORD *)(a1 + 16) = &v2[a2]; /*0x2dd81*/n memset(v2, 0, a2); /*0x2dd8d*/n *(_QWORD *)(a1 + 8) = v3; /*0x2dd92*/n }n}"}
复制代码隐藏代码{"addr":"0x2EFD0","code":"__int64 __fastcall sub_2EFD0(char *s, int a2, int a3, void *a4, size_t a5)n{n char *v5; // r13n char *v6; // rbpn size_t v7; // raxn size_t v8; // r12n size_t v9; // raxn size_t v10; // r15n size_t v11; // rbxn __int64 v12; // r9n __int64 v13; // r10n size_t v14; // rdin char *v15; // r14n char *v16; // rsin unsigned __int64 *v17; // r11n unsigned __int64 v18; // r12n __int64 v19; // raxn _BYTE *v20; // rcxn unsigned __int64 v21; // rdxn __int64 v22; // r8n __int128 v23; // xmm1n char v24; // aln unsigned __int64 v25;... [truncated 12861 bytes] .../*0x2f6fb*/n }n }n LODWORD(v6) = 0; /*0x2f334*/nLABEL_101:n if ( v27 ) /*0x2f70d*/n {n v49 = v27; /*0x2f70f*/n if ( v28 != v27 ) /*0x2f715*/n {n do /*0x2f726*/n {n v50 = v28 - 3; /*0x2f728*/n if ( (*(_BYTE *)(v28 - 3) & 1) != 0 ) /*0x2f730*/n operator delete(*(v28 - 1)); /*0x2f736*/n v28 = v50; /*0x2f720*/n }n while ( v50 != v27 ); /*0x2f726*/n v49 = (void **)ptr[0]; /*0x2f73d*/n }n ptr[1] = v27; /*0x2f745*/n operator delete(v49); /*0x2f74d*/n }n return (unsigned int)v6; /*0x2f767*/n}"}
复制代码隐藏代码sub_2EB00(a2, qword_5CFE8, v3 +6, &v42); // derive key from a2, qword_5CFE8, a... [thinking truncated, was5084chars] ...XHash64 of session dataqword_5CFE0 = v18;qword_5CFE8 = v18; // Initially set to same value
复制代码隐藏代码[ { "addr":"0x17430", "data":"0x63 0x7c 0x77 0x7b 0xf2 0x6b 0x6f 0xc5 0x30 0x1 0x67 0x2b 0xfe 0xd7 0xab 0x76 0xca 0x82 0xc9 0x7d 0xfa 0x59 0x47 0xf0 0xad 0xd4 0xa2 0xaf 0x9c 0xa4 0x72 0xc0 0xb7 0xfd 0x93 0x26 0x36 0x3f 0xf7 0xcc 0x34 0xa5 0xe5 0xf1 0x71 0xd8 0x31 0x15 0x4 0xc7 0x23 0xc3 0x18 0x96 0x5 0x9a 0x7 0x12 0x80 0xe2 0xeb 0x27 0xb2 0x75 0x9 0x83 0x2c 0x1a 0x1b 0x6e 0x5a 0xa0 0x52 0x3b 0xd6 0xb3 0x29 0xe3 0x2f 0x84 0x53 0xd1 0x0 0xed 0x20 0xfc 0xb1 0x5b 0x6a 0xcb 0xbe 0x39 0x4a 0x4c 0x58 0xcf 0xd0 0xef 0xaa 0xfb 0x43 0x4d 0x33 0x85 0x45 0xf9 0x2 0x7f 0x50 0x3c 0x9f 0xa8 0x51... [truncated 1429 bytes] ...xdb 0xe0 0x32 0x3a 0xa 0x49 0x6 0x24 0x5c 0xc2 0xd3 0xac 0x62 0x91 0x95 0xe4 0x79 0xe7 0xc8 0x37 0x6d 0x8d 0xd5 0x4e 0xa9 0x6c 0x56 0xf4 0xea 0x65 0x7a 0xae 0x8 0xba 0x78 0x25 0x2e 0x1c 0xa6 0xb4 0xc6 0xe8 0xdd 0x74 0x1f 0x4b 0xbd 0x8b 0x8a 0x70 0x3e 0xb5 0x66 0x48 0x3 0xf6 0xe 0x61 0x35 0x57 0xb9 0x86 0xc1 0x1d 0x9e 0xe1 0xf8 0x98 0x11 0x69 0xd9 0x8e 0x94 0x9b 0x1e 0x87 0xe9 0xce 0x55 0x28 0xdf 0x8c 0xa1 0x89 0xd 0xbf 0xe6 0x42 0x68 0x41 0x99 0x2d 0xf 0xb0 0x54 0xbb 0x16" }, { "addr":"0x17530", "data":"0x0 0x1 0x2 0x4 0x8 0x10 0x20 0x40 0x80 0x1b 0x36 0x0 0x0 0x0 0x0 0x0" }]
复制代码隐藏代码importstruct, os
# Read hjm_pack.bin headerwithopen(r"D:
AIAICTFworkdir52pojiechu8hjm_pack.bin","rb")asf: data = f.read()print(f"File size:{len(data)}bytes")print(f"Header hex:{...[truncated]
复制代码隐藏代码Traceback (most recent call last): File"C:
UsersWOYOUY~1AppDataLocalTempctf_agent_408345737.py", line6,in<module> with open(r"D:
AIAICTFworkdir52pojiechu8hjm_pack.bin","rb") as f: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^FileNotFoundError: [Errno2] No such file or directory:'D:\AI\AICTF\workdir\52pojie\chu8\hjm_pack.bin'[error:
exitstatus1]
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8D:
AIAICTFworkdir52pojiechu8apk_unzippedD:
AIAICTFworkdir52pojiechu8apk_unzippedAndroidManifest.xmlD:
AIAICTFworkdir52pojiechu8apk_unzippedDebugProbesKt.binD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.activity_activity-compose.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.activity_activity-ktx.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INFandroidx.activity_activity.versionD:
AIAICTFworkdir52pojiechu8apk_unzippedMETA-INF... [truncated7998bytes] ...libhajimi.so.namD:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so.tilD:
AIAICTFworkdir52pojiechu8apk_unzippedresD:
AIAICTFworkdir52pojiechu8apk_unzippedres-6.webpD:
AIAICTFworkdir52pojiechu8apk_unzippedres0K.xmlD:
AIAICTFworkdir52pojiechu8apk_unzippedres0Z.pngD:
AIAICTFworkdir52pojiechu8apk_unzippedres0w.xmlD:
AIAICTFworkdir52pojiechu8apk_unzippedres2K.9.pngD:
AIAICTFworkdir52pojiechu8apk_unzippedres4j.xmlD:
AIAICTFworkdir52pojiechu8apk_unzippedres5P.pngD:
AIAICTFworkdir52pojiechu8apk_unzippedres5c.png
复制代码隐藏代码importstructwithopen(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin","rb")asf: data = f.read()print(f"File size:{len(data)}bytes")print(f"Header hex:{data[:64].h...[truncated]
复制代码隐藏代码File size:
564bytesHeader hex:
484a4d3102000000010000004000000040000000780000000f1e2d3c4b5a69788796a5b4c3d2e1f0112233445566778899aabbcc9641cd80feda2af5fb95dd2cMagic:
0x314D4A48(HJM1)Type (offset 4):
2Field at offset 8:
1Field at offset 12:
64Field at offset 16:
64Bytes 20-23:
78000000Salt (offset 24-39):
0f1e2d3c4b5a69788796a5b4c3d2e1f0IV (offset 40-51):
112233445566778899aabbccEncrypteddata(offset52+):
512bytesFirst 32 bytes of encrypted:
9641cd80feda2af5fb95dd2c89bd91bc4013a0ed7c3df6e7a3d19b93bcc6542bExpectedbitmapsize(64x64@1bpp):
512bytesEncrypted data matches:
True
复制代码隐藏代码{"thoughtNumber":1,"totalThoughts":3,"nextThoughtNeeded":
true,"branches":[],"thoughtHistoryLength":5}
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedDebugProbesKt.binD:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin
复制代码隐藏代码Nofiles found.
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAAbstractC0154a.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAb.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAc.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAd.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAe.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAf.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAg.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAh.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesAi.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0C0155a.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0C0156b.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0a.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0b.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0c.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0d.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0e.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesA0f.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0AbstractC0254a.javaD:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0AbstractC0257d.java
复制代码隐藏代码$ findstr /s /i"NativeBridge|hajimi|hjm_pack|startSession|debugBypass|setDebug"D:
AIAICTFworkdir52pojiechu8jadx_outsources*.java 2>nul |head-50
复制代码隐藏代码[exitcode:
exitstatus1]
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.java:11:>importcom.zj.wuaipojie2026_2.NativeBridge;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.java:57:> caseNativeBridge.SCORE_GOOD/* 1 */:D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAa.java:66:> caseNativeBridge.SCORE_PERFECT/* 2 */:D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAb.java:17:>importcom.zj.wuaipojie2026_2.NativeBridge;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesAb.java:74:> caseNativeBridge.SCORE_GOOD/* 1 */:D:
AIAICTFworkdir52pojiechu8jadx_outso... [truncated3446bytes] ...52pojiechu8jadx_outsourcesF0u.java:
148:> caseNativeBridge.SCORE_PERFECT/* 2 */:D:
AIAICTFworkdir52pojiechu8jadx_outsourcesHd0.java:3:>importcom.zj.wuaipojie2026_2.NativeBridge;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesHd0.java:87:> caseNativeBridge.SCORE_GOOD/* 1 */:D:
AIAICTFworkdir52pojiechu8jadx_outsourcesHd0.java:91:> caseNativeBridge.SCORE_PERFECT/* 2 */:D:
AIAICTFworkdir52pojiechu8jadx_outsourcesHi.java:3:>importcom.zj.wuaipojie2026_2.NativeBridge;[30matches in11/289file(s)] [truncated at30matches]
复制代码隐藏代码{"thoughtNumber":2,"totalThoughts":4,"nextThoughtNeeded":
true,"branches":[],"thoughtHistoryLength":6}
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2MainActivity.java:1:>packagecom.zj.wuaipojie2026_2;D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2MainActivity.java:2:>D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2MainActivity.java:3:>importA.e;D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2MainActivity.java:4:>importQ0.AbstractC0080d;D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2MainActivity.java:5:>importa.AbstractC0154a;[5matchesin1/3file(s)] [truncated at5matches]
复制代码隐藏代码packagecom.zj.wuaipojie2026_2;importf1.h;importjava.nio.ByteBuffer;importjava.nio.ByteOrder;/* JADX INFO: loaded from: classes.dex */publicfinalclassNativeBridge{ publicstaticfinalint$stable=0; publicstaticfinalintERR_CHEAT=-7; publicstaticfinalNativeBridgeINSTANCE=newNativeBridge(); publicstaticfinalintSCORE_GOOD=1; publicstaticfinalintSCORE_MISS=0; publicstaticfinalintSCORE_PERFECT=2; static{ System.loadLibrary("hajimi"); } privateNativeBridge(){ } privatefinal... [truncated1458bytes] ...booleanz2); publicfinalvoidstartSession(longj2,int[] iArr,inti2){ h.e(iArr,"beatMapMs"); ByteBufferbyteBufferOrder=ByteBuffer.allocate(iArr.length *4).order(ByteOrder.LITTLE_ENDIAN); for(inti3 : iArr) { byteBufferOrder.putInt(i3); } byte[] bArrArray = byteBufferOrder.array(); h.d(bArrArray,"array(...)"); startSessionBytes(j2, bArrArray, i2); } publicfinalnativelongupdateExp(inti2,inti3,longj2); publicfinalnativebyte[] verifyAndDecrypt(byte[] bArr, String str);}
复制代码隐藏代码packagecom.zj.wuaipojie2026_2;importA.e;importQ0.AbstractC0080d;importa.AbstractC0154a;importandroid.content.res.Resources;importandroid.os.Build;importandroid.os.Bundle;importandroid.view.View;importandroid.view.ViewGroup;importandroid.view.Window;importandroidx.activity.A;importandroidx.activity.B;importandroidx.activity.l;importandroidx.activity.m;importandroidx.activity.n;importandroidx.activity.o;importandroidx.activity.p;importandroidx.activity.q;importandroidx.compose.ui.platform.C0204f0;importandroidx.lifecycle.E;importf1.h... [truncated2753bytes] ...ar); return; } C0204f0 c0204f02 = new C0204f0(this); c0204f02.setParentCompositionContext(null); c0204f02.setContent(eVar); View decorView2 = getWindow().getDecorView(); if(E.c(decorView2) ==null) { E.g(decorView2,this); } if(E.d(decorView2) ==null) { decorView2.setTag(R.id.view_tree_view_model_store_owner,this); } if(a.A(decorView2) ==null) { a.a0(decorView2,this); } setContentView(c0204f02, AbstractC0154a.f1861a); }}
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:23:> privatefinalnativevoidstartSessionBytes(longj2,byte[] bArr,inti2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:27:> publicfinalnativebyte[] decryptFrames(byte[] bArr,longj2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:29:> publicfinalnativevoidsetDebugBypass(booleanz2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:31:> publicfinal... [truncated1744bytes] ...3q.java:33:> InputStreaminputStreamOpen=this.f1185m.getAssets().open("hjm_pack.bin");D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0r.java:35:> returnNativeBridge.INSTANCE.decryptFrames(this.f1186m,this.f1187n.f1107a);D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0y.java:32:> InputStreaminputStreamOpen=this.f1216m.getAssets().open("hjm_pack.bin");D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0z.java:39:> returnnativeBridge.verifyAndDecrypt(this.f1217m, n1.k.j0((String)this.f1218n.getValue()).toString());[11matches in5/2191file(s)]
复制代码隐藏代码packageQ0;importandroid.content.Context;importjava.io.InputStream;importo1.InterfaceC0603z;/* JADX INFO: renamed from: Q0.q, reason: case insensitive filesystem *//* JADX INFO: loaded from: classes.dex */publicfinalclassC0093qextendsY0.iimplementse1.e { /* JADX INFO: renamed from: m, reason: collision with root package name */ publicfinal/* synthetic */Context f1185m; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ publicC0093q(Context context, W0.d dVar){ super(2, dVar); this.f1185m = context; } @Override// e1.e publicfinalObjectN(Object obj, Object obj2){ return((C0093q) c((W0.d) obj2, (InterfaceC0603z) obj)).g(S0.k.f1286a); } @Override// Y0.a publicfinalW0.dc(W0.d dVar, Object obj){ returnnewC0093q(this.f1185m, dVar); } @Override// Y0.a publicfinalObjectg(Object obj)throwsThrowable { R.c.Y(obj); InputStreaminputStreamOpen=this.f1185m.getAssets().open("hjm_pack.bin"); try{ f1.h.b(inputStreamOpen); byte[] bArrJ = b0.g.J(inputStreamOpen); c0.d.p(inputStreamOpen,null); returnbArrJ; }finally{ } }}
复制代码隐藏代码packageQ0;importcom.zj.wuaipojie2026_2.NativeBridge;importjava.util.List;importo1.InterfaceC0603z;importt.InterfaceC0680W;/* JADX INFO: loaded from: classes.dex */publicfinalclasszextendsY0.iimplementse1.e { /* JADX INFO: renamed from: m, reason: collision with root package name */ publicfinal/* synthetic */byte[] f1217m; /* JADX INFO: renamed from: n, reason: collision with root package name */ publicfinal/* synthetic */InterfaceC0680W f1218n; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ publicz(byte[] bArr, InterfaceC0680W interfaceC0680W, W0.d dVar){ super(2, dVar); this.f1217m = bArr; this.f1218n = interfaceC0680W; } @Override// e1.e publicfinalObjectN(Object obj, Object obj2){ return((z) c((W0.d) obj2, (InterfaceC0603z) obj)).g(S0.k.f1286a); } @Override// Y0.a publicfinalW0.dc(W0.d dVar, Object obj){ returnnewz(this.f1217m,this.f1218n, dVar); } @Override// Y0.a publicfinalObjectg(Object obj)throwsThrowable { R.c.Y(obj); NativeBridgenativeBridge=NativeBridge.INSTANCE; Listlist=N.f1106a; returnnativeBridge.verifyAndDecrypt(this.f1217m, n1.k.j0((String)this.f1218n.getValue()).toString()); }}
复制代码隐藏代码packageQ0;importcom.zj.wuaipojie2026_2.NativeBridge;importo1.InterfaceC0603z;/* JADX INFO: loaded from: classes.dex */publicfinalclassrextendsY0.iimplementse1.e { /* JADX INFO: renamed from: m, reason: collision with root package name */ publicfinal/* synthetic */byte[] f1186m; /* JADX INFO: renamed from: n, reason: collision with root package name */ publicfinal/* synthetic */O f1187n; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ publicr(byte[] bArr, O o2, W0.d dVar){ super(2, dVar); this.f1186m = bArr; this.f1187n = o2; } @Override// e1.e publicfinalObjectN(Object obj, Object obj2){ return((r) c((W0.d) obj2, (InterfaceC0603z) obj)).g(S0.k.f1286a); } @Override// Y0.a publicfinalW0.dc(W0.d dVar, Object obj){ returnnewr(this.f1186m,this.f1187n, dVar); } @Override// Y0.a publicfinalObjectg(Object obj)throwsThrowable { R.c.Y(obj); returnNativeBridge.INSTANCE.decryptFrames(this.f1186m,this.f1187n.f1107a); }}
复制代码隐藏代码packageQ0;importandroid.content.Context;importjava.io.InputStream;importo1.InterfaceC0603z;/* JADX INFO: loaded from: classes.dex */publicfinalclassyextendsY0.iimplementse1.e { /* JADX INFO: renamed from: m, reason: collision with root package name */ publicfinal/* synthetic */Context f1216m; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ publicy(Context context, W0.d dVar){ super(2, dVar); this.f1216m = context; } @Override// e1.e publicfinalObjectN(Object obj, Object obj2){ return((y) c((W0.d) obj2, (InterfaceC0603z) obj)).g(S0.k.f1286a); } @Override// Y0.a publicfinalW0.dc(W0.d dVar, Object obj){ returnnewy(this.f1216m, dVar); } @Override// Y0.a publicfinalObjectg(Object obj)throwsThrowable { R.c.Y(obj); InputStreaminputStreamOpen=this.f1216m.getAssets().open("hjm_pack.bin"); try{ f1.h.b(inputStreamOpen); byte[] bArrJ = b0.g.J(inputStreamOpen); c0.d.p(inputStreamOpen,null); returnbArrJ; }finally{ } }}
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:23:> privatefinalnativevoidstartSessionBytes(longj2,byte[] bArr,inti2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:25:> publicfinalnativeintcheckRhythm(longj2,inti2,longj3,inti3);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:29:> publicfinalnativevoidsetDebugBypass(booleanz2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:31:> publi... [truncated1427bytes] ...ourcescomzjwuaipojie2026_2NativeBridge.java:39:> startSessionBytes(j2, bArrArray, i2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:42:> publicfinalnativelongupdateExp(inti2,inti3,longj2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0v.java:58:> intiCheckRhythm=nativeBridge.checkRhythm(jElapsedRealtimeNanos, i2, j6, i7);D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0v.java:59:> longjUpdateExp=nativeBridge.updateExp(iCheckRhythm, i2, j6);[9matches in2/2191file(s)]
复制代码隐藏代码packageQ0;importE0.C0021h;importandroid.os.SystemClock;importcom.zj.wuaipojie2026_2.NativeBridge;importt.C0691d0;/* JADX INFO: loaded from: classes.dex */publicfinal/* synthetic */classvextendsf1.fimplementse1.a { /* JADX INFO: renamed from: q, reason: collision with root package name */ publicfinal/* synthetic */intf1199q; /* JADX WARN: 'super' call moved to the top of the method (can break code semantics) */ public/* synthetic */v(inti2, Object obj, Class cls, String str, String str2,inti3,inti4) { super(i2, obj, cls, s... [truncated3492bytes] ...q2 = iCheckRhythm !=0? iCheckRhythm !=1? iCheckRhythm !=2? Q.None : Q.Perfect : Q.Good : Q.Miss; o3.getClass(); o2 =newO(jUpdateExp, q2,false); } c0691d0.setValue(o2); } break; caseNativeBridge.SCORE_GOOD/* 1 */: ((androidx.activity.x)this.f3686j).d(); break; default: ((androidx.activity.x)this.f3686j).d(); break; } returnS0.k.f1286a; }}
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0C0256c.java:3:>import E0.C0021h;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0C0256c.java:13:>publicfinal class C0256c extendsC0021h{D:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0C0256c.java:19:> @Override // E0.C0021hD:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0C0256c.java:42:> @Override // E0.C0021hD:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0d.java:3:>import E0.C0021h;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesB0d.java:38:> publicd(C0021hc0021h) {D:
AIAICTFworkdir52pojiechu8ja... [truncated6009bytes] ...hu8jadx_outsourcesE0C0021h.java:
419:> publicC0021h(AndroidComposeView androidComposeView) {D:
AIAICTFworkdir52pojiechu8jadx_outsourcesE0C0021h.java:
427:> c0021h= newC0021h(7, androidComposeView);D:
AIAICTFworkdir52pojiechu8jadx_outsourcesE0C0021h.java:
429:> this.f318b =c0021h;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesE0C0021h.java:
432:> publicC0021h(Matcher matcher, Stringstr) {D:
AIAICTFworkdir52pojiechu8jadx_outsourcesE0C0021h.java:
434:> this.f318b = matcher;[50matchesin3/127file(s)] [truncatedat50matches]
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0r.java:35:> returnNativeBridge.INSTANCE.decryptFrames(this.f1186m,this.f1187n.f1107a);D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0z.java:39:> returnnativeBridge.verifyAndDecrypt(this.f1217m, n1.k.j0((String)this.f1218n.getValue()).toString());[2matchesin2/63file(s)]
复制代码隐藏代码[0 matches in 0/2191 file(s)]
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:23:> privatefinalnativevoidstartSessionBytes(longj2,byte[] bArr,inti2);D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:31:> publicfinalvoidstartSession(longj2,int[] iArr,inti2){D:
AIAICTFworkdir52pojiechu8jadx_outsourcescomzjwuaipojie2026_2NativeBridge.java:39:> startSessionBytes(j2, bArrArray, i2);[3matches in1/2191file(s)]
复制代码隐藏代码TodoList reset with5task(s):⬜1. 用Python重新实现native库的解密逻辑：SipHash + XXHash64 + AES-CTR⬜2. 确定初始状态：找到beatMap数据和startSession参数⬜3. 模拟debugbypass路径(sub_2E570)生成密钥⬜4. 解密hjm_pack.bin并渲染64x64位图⬜5. 提交flag
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0C0082f.java:12:>publicfinalclassC0082f{D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0C0082f.java:21:> publicfinalC0021h f1141c;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0C0082f.java:27:> publiclongf1143e;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0C0082f.java:30:> publicfinalC0691d0 f1144f;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0C0082f.java:32:> publicC0082f(Context context){D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0C0082f.java:37:> this.f1141c =newC0021h... [truncated2179bytes] ...longj3, O o2, k0.l lVar, k0.l lVar2,int[] iArr, C0082f c0082f,longj4,longj5, InterfaceC0680W interfaceC0680W, InterfaceC0680W interfaceC0680W2,inti2, C0311D c0311d, InterfaceC0680W interfaceC0680W3) {D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0x.java:
181:> C0082fc0082f=this.f1208p;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0x.java:
182:> longj4=c0082f.f1143e;D:
AIAICTFworkdir52pojiechu8jadx_outsourcesq0x.java:
261:> vvVar=newv(0, c0082f, C0082f.class,"onFeedTap","onFeedTap()V",0,0);[17matches in3/63file(s)]
复制代码隐藏代码packageQ0;importE0.C0021h;importandroid.content.Context;importandroid.media.MediaPlayer;importt.AbstractC0713v;importt.C0677T;importt.C0691d0;/* JADX INFO: renamed from: Q0.f, reason: case insensitive filesystem *//* JADX INFO: loaded from: classes.dex */publicfinalclassC0082f{ /* JADX INFO: renamed from: a, reason: collision with root package name */ publicfinalContext f1139a; /* JADX INFO: renamed from: b, reason: collision with root package name */ publicfinalint[] f1140b; /* JADX INFO: renamed from: c, reason: collision with root package name */ publicfinalC0021h f1141c; /* JADX INFO: renamed from: d, reason: collision with root package name */ publicMediaPlayer f1142d; /* JADX INFO: renamed from: e, reason: collision with root package name */ publiclongf1143e; /* JADX INFO: renamed from: f, reason: collision with root package name */ publicfinalC0691d0 f1144f; publicC0082f(Context context){ f1.h.e(context,"context"); this.f1139a = context; int[] iArr = {0,250,500,750}; this.f1140b = iArr; this.f1141c =newC0021h(4, iArr); this.f1144f = AbstractC0713v.E(newO(0L, Q.None,false), C0677T.f6486m); }}
复制代码隐藏代码{"thoughtNumber":3,"totalThoughts":3,"nextThoughtNeeded":
false,"branches":[],"thoughtHistoryLength":7}
复制代码隐藏代码Updated task#2. Current TodoList:⬜1. 用Python重新实现native库的解密逻辑：SipHash + XXHash64 + AES-CTR✅2. 确定初始状态：找到beatMap数据和startSession参数→beatMap=[0,250,500,750],interval=250, 密钥不依赖时间戳⬜3. 模拟debugbypass路径(sub_2E570)生成密钥⬜4. 解密hjm_pack.bin并渲染64x64位图⬜5. 提交flag
复制代码隐藏代码Updated task#1. Current TodoList:🔄1. 用Python重新实现native库的解密逻辑：SipHash + XXHash64 + AES-CTR✅2. 确定初始状态：找到beatMap数据和startSession参数→beatMap=[0,250,500,750],interval=250, 密钥不依赖时间戳⬜3. 模拟debugbypass路径(sub_2E570)生成密钥⬜4. 解密hjm_pack.bin并渲染64x64位图⬜5. 提交flag
复制代码隐藏代码{"addr":"0x2E570","asm": { "name":"sub_2E570", "start_ea":"0x2e570", "lines":"sub_2E570 (.text @ 0x2e570):
n2e570 push rbpn2e571 push r15n2e573 push r14n2e575 push r12n2e577 push rbxn2e578 sub rsp, 20hn2e57c mov rax, fs:
28hn2e585 mov [rsp+48h+var_30], raxn2e58a mov ebp, cs:
dword_5CFD0n2e590 xor ebx, ebxn2e592 test ebp, ebpn2e594 jle loc_2E650n2e59a mov rax, cs:
qword_5CFE8n2e5a1 mov r14, 1A8CBC5B802E097Chn2e5ab xor r14, raxn2e5ae mov rcx, 9E3779B97F4A7C15hn2e5b8 add rcx, r14n2e5... [truncated 2915 bytes] ... "offset": "0x10", "size": "0x4", "type": "_DWORD" }, { "name": "var_34", "offset": "0x14", "size": "0x4", "type": "_DWORD" }, { "name": "var_30", "offset": "0x18", "size": "0x8", "type": "_QWORD" }, { "name": "__return_address", "offset": "0x48", "size": "0x8", "type": "_UNKNOWN*" } ], "return_type": "__int64", "arguments": [] }, "instruction_count": 65, "total_instructions": null, "cursor": { "done": true }}
复制代码隐藏代码{"addr":"0x2EB00","asm": { "name":"sub_2EB00", "start_ea":"0x2eb00", "lines":"sub_2EB00 (.text @ 0x2eb00):
n2eb00 push r14n2eb02 push rbxn2eb03 sub rsp, 18hn2eb07 mov rbx, rcxn2eb0a mov r14, rdxn2eb0d mov rax, fs:
28hn2eb16 mov [rsp+28h+var_18], raxn2eb1b mov rdx, 1A8CBC5B802E097Chn2eb25 xor rdx, rsin2eb28 mov rcx, 802E097C1A8CBC5Bhn2eb32 xor rcx, rsin2eb35 mov [rsp+28h+var_28], rdin2eb39 mov [rsp+28h+var_20], rsin2eb3e mov rdi, rspn2eb41 mov esi, 10hn2eb46 call sub_2DAF0n2eb4b mo... [truncated 3453 bytes] ...":"_QWORD" }, { "name":"__return_address", "offset":"0x28", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"unsigned __int64", "arguments": [ { "name":"arg0", "type":"__int64" }, { "name":"arg1", "type":"__int64" }, { "name":"arg2", "type":"_QWORD *" }, { "name":"arg3", "type":"unsigned __int64 *" } ] },"instruction_count":89,"total_instructions": null,"cursor": { "done":
true }}
复制代码隐藏代码{"addr":"0x2E680","asm": { "name":"sub_2E680", "start_ea":"0x2e680", "lines":"sub_2E680 (.text @ 0x2e680):
n2e680 push rbpn2e681 push r15n2e683 push r14n2e685 push r13n2e687 push r12n2e689 push rbxn2e68a sub rsp, 0B8hn2e691 mov rax, fs:
28hn2e69a mov [rsp+0E8h+var_38], raxn2e6a2 test rsi, rsin2e6a5 jz loc_2EA89n2e6ab mov r12, rdin2e6ae mov r14, [rdi]n2e6b1 mov rax, [rdi+8]n2e6b5 sub rax, r14n2e6b8 cmp rax, 34h ; '4'n2e6bc jb loc_2EA89n2e6c2 cmp dword ptr [r14], 314D4A48hn... [truncated 10360 bytes] ... "size": "0x10", "type": "_OWORD" }, { "name": "var_38", "offset": "0xb0", "size": "0x8", "type": "_QWORD" }, { "name": "__return_address", "offset": "0xe8", "size": "0x8", "type": "_UNKNOWN*" } ], "return_type": "__int64", "arguments": [ { "name": "arg0", "type": "_QWORD*" }, { "name": "arg1", "type": "__int64" } ] }, "instruction_count": 250, "total_instructions": null, "cursor": { "done": true }}
复制代码隐藏代码importstructfromCrypto.CipherimportAESdefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefu32(x):
returnx &0xFFFFFFFFdefrol64(x, n):
returnu64((x << n) | (x >> (64- n)))
# SipHash-2-4defsip...[truncated]
复制代码隐藏代码qword_5CFE0 = qword_5CFE8 =0x810a3647628f0212sub_2E570 result (debug_key) =0xd2c13a26769ce7e0v34 (key to sub_2E680) =0x77649f83d3394245Salt:
0f1e2d3c4b5a69788796a5b4c3d2e1f0IV:
112233445566778899aabbccEncrypted size:
512SipHash resultinsub_2EB00 =0x0ea9de92c914b094key_part0 =0xf456e2c7ee0af52ckey_part1 =0x18ff86584363a443var_68 (derived key material): 2cf50aeec7e256f443a463435886ff18
复制代码隐藏代码importstructfromCrypto.CipherimportAESdefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefu32(x):
returnx &0xFFFFFFFFdefrol64(x, n):
returnu64((x << n) | (x >> (64- n)))defxxhash64(data, se...[truncated]
复制代码隐藏代码foldedqword_5CFE8=0xe3853455Chunk 0:
key=32d64809c01fd6eec54ddff78e80aa78,nonce=112233440052f26b99aabbcc,first_dec=805e6a74557f1cdaaa356dc35ebd35afChunk 1:
key=8610330511564bbe75b9fff53f5b6851,nonce=102233440052f26b99aabbcc,first_dec=4d9d53f018fbfb7d0e8b33a72b8fbad8Decrypted512bytesFirst 32 bytes:
805e6a74557f1cdaaa356dc35ebd35aff827c44616a2b4f525b1e38e9e70d0edLast 32 bytes:
9733382e37cc3934c373ba95401066edddc2132e3ea1be30ab63387055f97b8aBits set:
2124/4096(51%)
复制代码隐藏代码{"addr":"0x24850","asm": { "name":"verifyAndDecrypt", "start_ea":"0x24850", "lines":"verifyAndDecrypt (.text @ 0x24850):
n24850 push rbpn24851 push r15n24853 push r14n24855 push r13n24857 push r12n24859 push rbxn2485a sub rsp, 58hn2485e mov r14, rdin24861 mov rax, fs:
28hn2486a mov [rsp+88h+var_38], raxn2486f mov rax, [rdi]n24872 test rdx, rdxn24875 jz loc_24937n2487b mov r15, rcxn2487e test rcx, rcxn24881 jz loc_24937n24887 mov r13, rdxn2488a mov rdi, r14n2488d mov r... [truncated 4522 bytes] ...0x8", "type":"_QWORD" }, { "name":"__return_address", "offset":"0x88", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"__int64", "arguments": [ { "name":"arg0", "type":"__int64 *" }, { "name":"arg1", "type":"__int64" }, { "name":"arg2", "type":"__int64" }, { "name":"arg3", "type":"__int64" } ] },"instruction_count":
100,"total_instructions": null,"cursor": { "next":
100 }}
复制代码隐藏代码{"addr":"0x24850","asm": { "name":"verifyAndDecrypt", "start_ea":"0x24850", "lines":"verifyAndDecrypt (.text @ 0x24850):
n249be jnz short loc_24A30n249c0 shl rcx, 20hn249c4 movsxd rdx, edxn249c7 mov rsi, 1A8CBC5B802E097Chn249d1 xor rsi, rcxn249d4 xor rsi, rdxn249d7 mov rcx, 9E3779B97F4A7C15hn249e1 add rcx, rsin249e4 mov rdx, rcxn249e7 shr rdx, 1Ehn249eb xor rdx, rcxn249ee mov rcx, 0BF58476D1CE4E5B9hn249f8 imul rcx, rdxn249fc mov rdx, rcxn249ff shr rdx, 1Bhn24a03 xor rdx, rcxn24a06... [truncated 7164 bytes] ...x8", "type":"_QWORD" }, { "name":"__return_address", "offset":"0x88", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"__int64", "arguments": [ { "name":"arg0", "type":"__int64 *" }, { "name":"arg1", "type":"__int64" }, { "name":"arg2", "type":"__int64" }, { "name":"arg3", "type":"__int64" } ] },"instruction_count":
184,"total_instructions": null,"cursor": { "done":
true }}
复制代码隐藏代码24b8b:al= byte_5D140 (debugBypass flag)24b92:
testal,al24b94:
setnzcl24b97:
orcl, byte_5CFF824b9d:
orcl,r13b24ba0:
testcl,124ba3:
jz24bb4 (fail)24ba5: ...24ba9:
testal,al (testdebugBypass again)24bab:
jz24bda (ifNOTdebug, use qword_5CFF0)24bad:
callsub_2E570 (if debug, compute key)24bb2:
jmp24be124bda:
movrax, qword_5CFF0 (use game-earned key)24be1:
movrsi,0xA5A5A5A5A5A5A5A524beb:
xorrsi,rax24bee:
testr13b,r13b (r13b= password verification passed?)24bf1:
cmovzrsi,rax (if passwordNOTverified, DON'T XOR)24bf5: lea rdi, [rsp+var_70]24bfa: call sub_2E680
复制代码隐藏代码importstructfromCrypto.CipherimportAESfromPILimportImagedefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefu32(x):
returnx &0xFFFFFFFFdefrol64(x, n):
returnu64((x << n) | (x >> (64- n)))...[truncated]
复制代码隐藏代码debug_key ^0xA5(r13b=1):
bits=2124/4096(51%), row0=805e6a74557f1cda Savedbitmap_debug_key_^_0xA5_r13b1.pngdebug_key raw (r13b=0):
bits=1959/4096(47%), row0=0000000000000000 Savedbitmap_debug_key_raw_r13b0.pngqfe8 ^0xA5(game path):
bits=2090/4096(51%), row0=a70cb53fdecafaae Savedbitmap_qfe8_^_0xA5_game_path.pngqfe8 raw:
bits=2053/4096(50%), row0=2a9a67989b338d3f Savedbitmap_qfe8_raw.png
复制代码隐藏代码Thisis**nota valid, scannable QR code nor a standard machine-readable pattern**likea barcode, Data Matrix, etc. Here's a detailed breakdown of what this is:1. **Overall Type**: Itisa dense, high-contrast monochrome black-and-white chaotic texture, specifically a distorted, overlapping"soup"ofstylized, warped small characters/symbols.2. **Detailed Elements**: The frameisfilledwithtightly packed, deformed, overlapping small glyphs: they resemble squashed, curved, angular lowercase letters, modified punctuation,orabstract tiny shapes, all mashed togetherwithno consistent spacing, alignment,ororder.3. **LackofFunctional PatternStructure**: Unlike QR codes, which have astrictsquare grid, clear corner finder markers,anduniform square modules, this has zero consistent grid, no reference pointsforscanning,andno organizedstructure. It has no scannableormachine-readablefunction.4. **Visual Effect**: It looksliketextrun through an extreme warp/distortion filter, turning readable charactersintoan unreadable, dense, chaotic texture that fills the entire image space.
复制代码隐藏代码importstructfromPILimportImage
# Read the decrypted data for the "debug_key raw" variant
# Let me regenerate it quicklydefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefu32(x):
returnx &0xFFFFFF...[truncated]
复制代码隐藏代码Imagesize: (64,64)Imagemode:1█ ██ █ █ █ ████ █ ██ ████ ████████ █ █ ████ ██ ██ █ ████████ █████ ██ █ ███ █ █ █ █ ██████ █████ █ ███████ █ █ ██ █ █ ██ █ ███ █ ██ ██ ██ █ █ ████ █ ███ ██ █ █ �...[truncated 8112 bytes]...████ ████ █████ ██ ███ ██ █ ███ ██ █ █ ██ █ █ █ █ █ █ ██ █ ██ ████ ███ █ ██ █ █ █ ██ ██ █ ███ █ █████ █ █ ███ █ █ █ █ ██ █ ██ ████ █ ███ ███ ███ ██ ██ ███ ████ ██ ██ ███ █ ███ ██ ███ █ ██ █ ██ ████ █ █ █ █ ███ ███ █ █ █ █ ███ █
复制代码隐藏代码{"addr":"0x2DAF0","asm": { "name":"sub_2DAF0", "start_ea":"0x2daf0", "lines":"sub_2DAF0 (.text @ 0x2daf0):
n2daf0 push rbxn2daf1 mov r9, 736F6D6570736575hn2dafb xor r9, rdxn2dafe mov r8, 646F72616E646F6Dhn2db08 xor r8, rcxn2db0b mov rax, 6C7967656E657261hn2db15 xor rax, rdxn2db18 mov rdx, 7465646279746573hn2db22 xor rdx, rcxn2db25 mov r10, rsin2db28 and r10, 0FFFFFFFFFFFFFFF8hn2db2c jz loc_2DBB6n2db32 lea rcx, [rdi+r10]n2db36 xor r11d, r11dn2db39 nop dword ptr [rax+00000000h]n2db40 ... [truncated 5389 bytes] ...4a retn", "stack_frame": [ { "name":"__return_address", "offset":"0x8", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"__int64", "arguments": [ { "name":"arg0", "type":"unsigned __int8 *" }, { "name":"arg1", "type":"__int64" }, { "name":"arg2", "type":"__int64" }, { "name":"arg3", "type":"__int64" } ] },"instruction_count":
168,"total_instructions": null,"cursor": { "done":
true }}
复制代码隐藏代码{"thoughtNumber":1,"totalThoughts":3,"nextThoughtNeeded":
true,"branches":[],"thoughtHistoryLength":8}
复制代码隐藏代码{"addr":"0x2DF40","asm": { "name":"sub_2DF40", "start_ea":"0x2df40", "lines":"sub_2DF40 (.text @ 0x2df40):
n2df40 push rbpn2df41 push r15n2df43 push r14n2df45 push r13n2df47 push r12n2df49 push rbxn2df4a sub rsp, 108hn2df51 mov [rsp+138h+var_118], rdin2df56 mov rax, fs:
28hn2df5f mov [rsp+138h+var_38], raxn2df67 movdqu xmm0, xmmword ptr [rdx]n2df6b movdqa [rsp+138h+var_E8], xmm0n2df71 mov eax, 1n2df76 mov edx, 0Fhn2df7b mov r14d, 10hn2df81 lea rbp, byte_17430n2df88 lea rdi, byte_17530... [truncated 13870 bytes] ...WORD" }, { "name":"__return_address", "offset":"0x138", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"unsigned __int64", "arguments": [ { "name":"arg0", "type":"__int64" }, { "name":"arg1", "type":"unsigned __int64" }, { "name":"arg2", "type":"const __m128i *" }, { "name":"arg3", "type":"_BYTE *" } ] },"instruction_count":
300,"total_instructions": null,"cursor": { "next":
300 }}
复制代码隐藏代码{"addr":"0x2E680","code":"__int64 __fastcall sub_2E680(_QWORD *a1, __int64 a2)n{n _QWORD *v2; // r12n _DWORD *v3; // r14n unsigned __int64 v4; // raxn __int64 v5; // rdxn __int64 v6; // rbpn int v7; // ecxn int v8; // edin unsigned int v9; // edin size_t v10; // rdin unsigned __int64 v11; // rbxn unsigned __int64 v12; // r13n void **v13; // r14n __int64 v14; // raxn __int64 v15; // r15n __int64 v16; // raxn unsigned __int64 v17; // rbpn void **v18; // r13n _QWORD *v19; // r14n void *v20; // r12n void *v21; // raxn __int64 v22; // raxn __int6... [truncated 7703 bytes] ... ptr[1] = ptr[0]; /*0x2ea54*/n operator delete(ptr[0]); /*0x2ea59*/n }n return (unsigned int)v6; /*0x2ea5e*/n }n }n if ( !src[0] || (src[1] = src[0], operator delete(src[0]), (v25 = ptr[0]) != 0) ) /*0x2ea7d*/n {n ptr[1] = v25; /*0x2ea7f*/n operator delete(v25); /*0x2ea84*/n }n goto LABEL_27; /*0x2ea84*/n }n }n }n }n }n }n return (unsigned int)v6; /*0x2eaa0*/n}"}
复制代码隐藏代码{"addr":"0x24CB0","code":"unsigned __int64 __fastcall sub_24CB0(unsigned __int8 *a1, unsigned __int64 a2, unsigned __int64 a3)n{n unsigned __int64 v3; // r9n unsigned __int64 v4; // rbpn unsigned __int64 v5; // r13n unsigned __int64 v6; // r12n __int64 v7; // r15n __int64 v8; // r14n __int64 v9; // rbxn __int64 v10; // r11n unsigned __int64 v11; // r11n unsigned __int64 v12; // r11n unsigned __int64 v13; // rsin unsigned __int8 *v14; // r10n bool v15; // ccn unsigned __int64 v16; // rdin unsigned __int64 v17; // r10n __int64 v18; // r11n unsigned __in... [truncated 4974 bytes] ...t8 *)v16), 11))n ^ (0x27D4EB2F165667C5LL * *(unsigned __int8 *)(v16 + 1)),n 11))n ^ (0x27D4EB2F165667C5LL * *(unsigned __int8 *)(v16 + 2)),n 11))n ^ (0x27D4EB2F165667C5LL * *(unsigned __int8 *)(v16 + 3)),n 11);n v16 += 4LL; /*0x24f7d*/n }n while ( v16 < v3 ); /*0x24f84*/n }nLABEL_18:n v20 = 0x165667B19E3779F9LL /*0x24f86*/n * ((0xC2B2AE3D27D4EB4FLL * (v13 ^ (v13 >> 33))) ^ ((0xC2B2AE3D27D4EB4FLL * (v13 ^ (v13 >> 33))) >> 29));n return v20 ^ HIDWORD(v20); /*0x24fac*/n}"}
复制代码隐藏代码v20 = (void*)sub_24CB0(src,32,4951); // ptr[0] = 8 bytes but only low 32 meaningful?v21 = (void*)sub_24CB0(src,32,9320); // ptr[1]ptr[0] = v20;ptr[1] = v21;
复制代码隐藏代码{"addr":"0x24F86","asm": { "name":"sub_24CB0", "start_ea":"0x24f86", "lines":"sub_24CB0 (.text @ 0x24f86):
n24f86 mov rcx, rsin24f89 shr rcx, 21hn24f8d xor rcx, rsin24f90 imul rcx, raxn24f94 mov rsi, rcxn24f97 shr rsi, 1Dhn24f9b xor rsi, rcxn24f9e imul rsi, rdxn24fa2 mov rax, rsin24fa5 shr rax, 20hn24fa9 xor rax, rsin24fac pop rbxn24fad pop r12n24faf pop r13n24fb1 pop r14n24fb3 pop r15n24fb5 pop rbpn24fb6 retn", "stack_frame": [ { "name":"__return_address", "offset":"0x30", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"unsigned __int64", "arguments": [ { "name":"arg0", "type":"unsigned __int8 *" }, { "name":"arg1", "type":"unsigned __int64" }, { "name":"arg2", "type":"unsigned __int64" } ] },"instruction_count":18,"total_instructions": null,"cursor": { "done":
true }}
复制代码隐藏代码rax=rsirax>>=32 (rax= high32 ofrsi,zero-extended)rax^=rsi (rax=rsi^ (rsi>>32))
复制代码隐藏代码importstructdefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefrol64(x, n):
returnu64((x << n) | (x >> (64- n)))defxxhash64(data, seed): PRIME1, PRIME2, PRIME3, PRIME4, PRIME5 =0x9E3779B185EB...[truncated]
复制代码隐藏代码My XXHash64: 0x4a688cc8e32bcc0bLibXXHash64:
0x4a688cc8e32bcc0bMatch:
True32-bytetest:My:
0xcbf59c5116ff32b4Lib:
0xcbf59c5116ff32b4Match:
TrueBeatmap hash:My:
0x810a3647628f0212Lib:
0x810a3647628f0212Match:
True
复制代码隐藏代码importstruct, xxhashdefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefsub_24CB0(data, seed): """XXHash64 with final fold: result ^ (result >> 32)""" h = xxhash.xxh64(data, seed=seed).intdigest() returnu64(h ^ (h >>32))
# Now let me also check: in sub_2E680, the 'src' buffer passed to sub_24CB0 is 32 bytes:# [0:16] = var_68 (key material from sub_2EB00)
# [16:20] = r15d (chunk counter as u32)
# [20:24] = r13d (low 32 of qword_5CFE8)
# [24:32] = var_E0 ^ r13 (where var_E0 = chunk_idx * 0x100000000)
# Wait, looking at the decompiled code more carefully:# v44.m128i_i64[0] = __PAIR64__(v12, v15) -> this is (v12 << 32) | v15
# v44.m128i_i64[1] = v12 ^ v31
# v12 = qword_5CFE8 (r13 in asm)
# v15 = chunk counter (r15 in asm, starts at 0)
# v31 = var_E0 (starts at 0, increments by 0x100000000)
# So the 32-byte src buffer is:# [0:16] = var_68 (from sub_2EB00)
# [16:24] = __PAIR64__(qword_5CFE8, chunk_counter) = (qfe8 << 32) | counter
# [24:32] = qfe8 ^ var_E0
# Wait, __PAIR64__(v12, v15) means high=v12, low=v15
# So bytes 16-23 = v15 (low 32) | v12 (high 32) as a 64-bit LE value
# That means: struct.pack('<Q', (v12 << 32) | (v15 & 0xFFFFFFFF))
# Which is: struct.pack(' offset 0 of var_48 = r15d (low 32)
# mov dword ptr [rsp+var_48+4], r13d -> offset 4 of var_48 = r13d (high 32)
# So var_48[0:8] = (r13 << 32) | r15 = __PAIR64__(r13, r15)
# And at 0x2e807:# mov rax, var_E0
# xor rax, r13
# mov qword ptr [rsp+var_48+8], rax -> var_48[8:16] = var_E0 ^ r13
# So the full 32-byte buffer for sub_24CB0 is:# src[0:16] = var_68 (key from sub_2EB00)
# src[16:20] = r15d (chunk counter, 32-bit)
# src[20:24] = r13d (low 32 of qfe8)
# src[24:32] = var_E0 ^ r13 (64-bit)
# This matches what I had before. Good.# Now let me check the IV construction more carefully.# From the decompiled code, the IV (src in the call to sub_2DF40) is built as:# 1. src[0:8] = *v13 (first 8 bytes of IV from file, at offset 0x28 = 40)
# 2. src[8:12] = *(v13 + 8) (next 4 bytes of IV from file)
# 3. Then XOR first 8 bytes with counter info
# The XOR mask is built from xmm0:# byte 0: r15 & 0xFF
# byte 1: (r15 >> 8) & 0xFF
# byte 2: (r15 >> 16) & 0xFF
# byte 3: (r15 >> 24) & 0xFF
# byte 4: folded & 0xFF
# byte 5: (folded >> 8) & 0xFF
# byte 6: (folded >> 16) & 0xFF
# byte 7: (folded >> 24) & 0xFF
# Where folded = qfe8 ^ (qfe8 >> 32)
# Then: src[0:8] ^= xmm0[0:8]# So the 12-byte IV passed to sub_2DF40 is:# [0:8] = file_iv[0:8] ^ pack('> 8)
# bl = var_133 ^ (counter >> 16)
# r12b = var_134 ^ (counter >> 24)
# So the counter is XORed with the LAST 4 bytes of the first round key.# This is NOT standard AES-CTR!# In standard AES-CTR, you'd have a 16-byte counter block that gets encrypted.# Here, the "counter block" is:# [first_round_key[0:12] ^ IV[0:12]] + [first_round_key[12:16] ^ counter_bytes]# And this gets fed through the AES rounds (starting from round 1, not round 0).# Actually wait - let me re-read. The key expansion at the top of sub_2DF40:# var_E8 is loaded with the key (16 bytes from [rdx])
# Then key expansion happens (the loop at 0x2df8f-0x2e018)
# This expands to 11 round keys (176 bytes = 0xB0)
# Then the first round key (var_E8[0:16]) is XORed with the IV:# var_125 = var_E8[0] ^ IV[0]# var_129 = var_E8[1] ^ IV[1] (wait, the naming is confusing)
# Actually the var names are at negative offsets. Let me map them:# var_125 is at offset 0x13, var_126 at 0x12, etc.# var_E8 is at offset 0x50
# The XOR at 0x2e02d: al = var_E8[0] ^ rcx[0], stored to var_125
# This creates a modified first block that combines the round key with the IV.# Then in the AES encryption loop, this modified block goes through SubBytes + MixColumns
# for 9 rounds, then a final SubBytes, then XOR with the last round key.# So the encryption is: AES_encrypt(round_key_0 ^ IV_extended)
# where IV_extended = [IV(12 bytes) + counter(4 bytes)]# This IS standard AES-CTR! The first step of AES is AddRoundKey (XOR with round key 0),# and here they pre-compute that XOR with the IV.# So the full picture:# counter_block = IV(12 bytes) || counter(4 bytes, big-endian? little-endian?)
# keystream = AES_encrypt(key, counter_block)
# plaintext = ciphertext ^ keystream
# The counter format: looking at the XOR at 0x2e136:# r9b = var_131 ^ cl (cl = counter & 0xFF)
# This means byte 12 of the block = round_key[12] ^ (counter & 0xFF)
# Which means the counter is in LITTLE-ENDIAN format in bytes 12-15
# But in standard AES-CTR (like NIST), the counter is big-endian.# PyCryptodome's AES.MODE_CTR with nonce uses big-endian counter by default.# So I need to use little-endian counter!print("Key insight: AES-CTR with 12-byte nonce and 4-byte LITTLE-ENDIAN counter")print("The nonce is: file_IV[0:8] ^ counter_info || file_IV[8:12]")print("Counter starts at 0 and increments for each 16-byte block within a 256-byte chunk")
复制代码隐藏代码Keyinsight:
AES-CTR with12-bytenonceand4-byteLITTLE-ENDIAN counterThe nonce is: file_IV[0:8] ^ counter_info||file_IV[8:12]Counter startsat0andincrements for each16-byteblockwithin a256-bytechunk
复制代码隐藏代码importstruct, xxhashfromCrypto.CipherimportAESfromCrypto.UtilimportCounterfromPILimportImagedefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefu32(x):
returnx &0xFFFFFFFFdefrol64(x, n):
returnu64((x << n) | (x >> (64- n)))defsiphash_2_4(data, k0, k1): v0 = u64(k0 ^0x736f6d6570736575) v1 = u64(k1 ^0x646f72616e646f6d) v2 = u64(k0 ^0x6c7967656e657261) v3 = u64(k1 ^0x7465646279746573) length =len(data); blocks = length //8 foriinrange(blocks): m = struct.unpack_from('<Q', data, i*8)[0] v3 ^= m for_inrange(2): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) v0 ^= m last =bytearray(8) rem = length %8; start = blocks *8 foriinrange(rem): last[i] = data[start+i] last[7] = length &0xFF m = struct.unpack('<Q',bytes(last))[0] v3 ^= m for_inrange(2): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) v0 ^= m v2 ^=0xFF for_inrange(4): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) returnu64(v0^v1^v2^v3)defsplitmix64(state): state = u64(state +0x9E3779B97F4A7C15) z = state z = u64((z ^ (z >>30)) *0xBF58476D1CE4E5B9) z = u64((z ^ (z >>27)) *0x94D049BB133111EB) returnstate, z ^ (z >>31)defsub_24CB0(data, seed): h = xxhash.xxh64(data, seed=seed).intdigest() returnu64(h ^ (h >>32))defderive_key_sub_2EB00(key_val, qfe8, salt): eb_k0 = u64(qfe8 ^0x1A8CBC5B802E097C) eb_k1 = u64(qfe8 ^0x802E097C1A8CBC5B) eb_buf = struct.pack('<QQ', key_val, qfe8) sip = siphash_2_4(eb_buf, eb_k0, eb_k1) salt_q0, salt_q1 = struct.unpack_from('<QQ', salt,0) PRIME1,PRIME2,PRIME4 =0x9E3779B185EBCA87,0xC2B2AE3D27D4EB4F,0x85EBCA77C2B2AE63 PRIME3_xxh, r10 =0x165667B19E3779F9,0x27D4EB2F165726CC s1 = u64(salt_q1*PRIME2); s1=rol64(s1,31); s1=u64(s1*PRIME1) s0 = u64(salt_q0*PRIME2); s0=rol64(s0,31); s0=u64(s0*PRIME1) sa = u64(sip*PRIME2); sa=rol64(sa,31); sa=u64(sa*PRIME1) rax2 = sa ^ r10 rax2=rol64(rax2,27); rax2=u64(rax2*PRIME1); rax2=u64(rax2+PRIME4) rax2^=s0; rax2=rol64(rax2,27); rax2=u64(rax2*PRIME1); rax2=u64(rax2+PRIME4) rax2^=s1; rax2=rol64(rax2,27); rax2=u64(rax2*PRIME1); rax2=u64(rax2+PRIME4) rax2^=rax2>>33; rax2=u64(rax2*PRIME2); rax2^=rax2>>29; rax2=u64(rax2*PRIME3_xxh); rax2^=rax2>>32 rdx = u64(r10+0x1EF) ^ sa rdx=rol64(rdx,27); rdx=u64(rdx*PRIME1); rdx=u64(rdx+PRIME4) rdx^=s0; rdx=rol64(rdx,27); rdx=u64(rdx*PRIME1); rdx=u64(rdx+PRIME4) rdx^=s1; rdx=rol64(rdx,27); rdx=u64(rdx*PRIME1); rdx=u64(rdx+PRIME4) rdx^=rdx>>33; rdx=u64(rdx*PRIME2); rdx^=rdx>>29; rdx=u64(rdx*PRIME3_xxh); rdx^=rdx>>32 returnrax2, rdxdefaes_ctr_decrypt_le(key, nonce_12, data): """AES-128-CTR with 12-byte nonce and 4-byte little-endian counter""" result =bytearray() counter =0 foriinrange(0,len(data),16): block = nonce_12 + struct.pack('>32)) total =len(encrypted) num_chunks = (total +255) //256 decrypted =bytearray(total) var_E0 =0 forciinrange(num_chunks): cs_ = ci *256 csz =min(256, total - cs_) # Build 32-byte buffer for sub_24CB0 src = var_68 # 16 bytes src += struct.pack('> bit_idx) &1 img.putpixel((x, y), pixel) img.save(rf"D:
AIAICTFworkdir52pojiechu8bitmap_le_{name}.png") bits =sum(bin(b).count('1')forbindecrypted) print(f"{name}: bits={bits}/{total*8}({bits*100//(total*8)}%), first16={decrypted[:16].hex()}") # Also try with standard big-endian CTR decrypted2 =bytearray(total) var_E0 =0 forciinrange(num_chunks): cs_ = ci *256 csz =min(256, total - cs_) src = var_68 + struct.pack('> (64- n)))defsiphash_2_4(data, k0, k1): v0 = u64(k0 ^0x736f6d6570736575) v1 = u64(k1 ^0x646f72616e646f6d) v2 = u64(k0 ^0x6c7967656e657261) v3 = u64(k1 ^0x7465646279746573) length =len(data); blocks = length //8 foriinrange(blocks): m = struct.unpack_from('<Q', data, i*8)[0] v3 ^= m for_inrange(2): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) v0 ^= m last =bytearray(8) rem = length %8; start = blocks *8 foriinrange(rem): last[i] = data[start+i] last[7] = length &0xFF m = struct.unpack('<Q',bytes(last))[0] v3 ^= m for_inrange(2): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) v0 ^= m v2 ^=0xFF for_inrange(4): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) returnu64(v0^v1^v2^v3)
# Standard SipHash-2-4 test vectors from the paper
# Key: 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
# k0 = 0x0706050403020100, k1 = 0x0f0e0d0c0b0a0908k0 =0x0706050403020100k1 =0x0f0e0d0c0b0a0908
# Test vector for empty message: expected 0x726fdb47dd0e0e31result_empty = siphash_2_4(b"", k0, k1)print(f"SipHash(empty): 0x{result_empty:
016x}(expected: 0x726fdb47dd0e0e31)")
# Test vector for message = 00: expected 0x74f839c593dc67fdresult_0 = siphash_2_4(bytes([0]), k0, k1)print(f"SipHash([0]): 0x{result_0:
016x}(expected: 0x74f839c593dc67fd)")
# Test vector for message = 00 01: expected 0x0d6c8009d9a94f5aresult_01 = siphash_2_4(bytes([0,1]), k0, k1)print(f"SipHash([0,1]): 0x{result_01:
016x}(expected: 0x0d6c8009d9a94f5a)")
# Test vector for message = 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0eresult_15 = siphash_2_4(bytes(range(15)), k0, k1)print(f"SipHash([0..14]): 0x{result_15:
016x}(expected: 0xa129ca6149be45e5)")
复制代码隐藏代码SipHash(empty):
0x726fdb47dd0e0e31(expected:
0x726fdb47dd0e0e31)SipHash([0]): 0x74f839c593dc67fd(expected:
0x74f839c593dc67fd)SipHash([0,1]):
0x0d6c8009d9a94f5a(expected:
0x0d6c8009d9a94f5a)SipHash([0..14]):
0xa129ca6149be45e5(expected:
0xa129ca6149be45e5)
复制代码隐藏代码
# SipHash is verified correct. Let me now trace through sub_2E570 step by step
# to make sure the debug key computation is right.importstructdefu64(x):
returnx &0xFFFFFFFFFFFFFFFFdefrol64(x, n):
returnu64((x << n) | (x >> (64- n)))defsiphash_2_4(data, k0, k1): v0 = u64(k0 ^0x736f6d6570736575) v1 = u64(k1 ^0x646f72616e646f6d) v2 = u64(k0 ^0x6c7967656e657261) v3 = u64(k1 ^0x7465646279746573) length =len(data); blocks = length //8 foriinrange(blocks): m = struct.unpack_from('<Q', data, i*8)[0] v3 ^= m for_inrange(2): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) v0 ^= m last =bytearray(8) rem = length %8; start = blocks *8 foriinrange(rem): last[i] = data[start+i] last[7] = length &0xFF m = struct.unpack('<Q',bytes(last))[0] v3 ^= m for_inrange(2): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) v0 ^= m v2 ^=0xFF for_inrange(4): v0=u64(v0+v1); v1=rol64(v1,13); v1^=v0; v0=rol64(v0,32) v2=u64(v2+v3); v3=rol64(v3,16); v3^=v2 v0=u64(v0+v3); v3=rol64(v3,21); v3^=v0 v2=u64(v2+v1); v1=rol64(v1,17); v1^=v2; v2=rol64(v2,32) returnu64(v0^v1^v2^v3)defsplitmix64(state): state = u64(state +0x9E3779B97F4A7C15) z = state z = u64((z ^ (z >>30)) *0xBF58476D1CE4E5B9) z = u64((z ^ (z >>27)) *0x94D049BB133111EB) returnstate, z ^ (z >>31)
# sub_2E570 trace:# ebp = dword_5CFD0 (number of beats = 4)
# rax = qword_5CFE8
# r14 = 0x1A8CBC5B802E097C ^ rax
# splitmix64(r14) -> rcx
# r15 = 0x802E097C1A8CBC5B ^ raximportxxhashbeatmap = struct.pack('<4I',0,250,500,750)qfe8 = xxhash.xxh64(beatmap, seed=0x1A8CBC5B802E097C).intdigest()print(f"qfe8 = 0x{qfe8:
016x}")rax = qfe8r14 = u64(0x1A8CBC5B802E097C^ rax)print(f"r14 = 0x{r14:
016x}")
# splitmix64rcx_state = u64(r14 +0x9E3779B97F4A7C15)print(f"rcx after add = 0x{rcx_state:
016x}")rdx = rcx_staterdx = u64((rdx ^ (rdx >>0x1E)) *0xBF58476D1CE4E5B9)print(f"after first mix = 0x{rdx:
016x}")rdx2 = rdxrdx2 = u64((rdx2 ^ (rdx2 >>0x1B)) *0x94D049BB133111EB)print(f"after second mix = 0x{rdx2:
016x}")rsi = rdx2rcx_val = rsircx_final = rcx_val ^ (rcx_val >>0x1F)print(f"splitmix64 result = 0x{rcx_final:
016x}")
# Verify with my function_, sm_result = splitmix64(r14)print(f"splitmix64 verify = 0x{sm_result:
016x}")print(f"Match:{rcx_final == sm_result}")r15 = u64(0x802E097C1A8CBC5B^ rax)print(f"r15 = 0x{r15:
016x}")
# Loop 12 timesebp =4
# dword_5CFD0rcx = rcx_finalforiinrange(12): # Build 24-byte buffer on stack: # [0:8] = rcx (var_48) # [8:12] = i % ebp (var_40, as signed int) # [12:16] = 0 (var_3C) # [16:20] = i (var_38, as unsigned int) # [20:24] = 2 (var_34, as unsigned int) # sub_2DAF0(rdi=stack_buf, rsi=0x18, rdx=r14, rcx=r15) buf = struct.pack('<q', rcxifrcx <2**63elsercx -2**64) # as signed? No, just raw bytes buf = struct.pack('<Q', rcx) buf += struct.pack('Letmetakea different approach. Insteadoftryingtoperfectly replicate the native code,letmeuse Unicorntoemulate the critical functions directly:### 🐍 执行 Python 脚本```python#Letmecheckwhereqword_5CFE8iswritten (notjust read)
# Looking at the xrefs,letmecheck0x23a6aand0x246eeimport struct
# First,letmere-examine the initialization. qword_5CFE0andqword_5CFE8
# might besetinthe startSessionfunction.#Letmelook at thefunctionthat sets these values.# Actually,letmetrya completely different approach.# Insteadofreimplementing everything,letmeuse unicorntoemulate the native code.# First,letmeread the .so filewithopen(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhjm.so","rb")asf: so_data = f.read()print(f"SO file size: {len(so_data)} bytes")
# Check ELF headermagic = so_data[:4]print(f"Magic: {magic}")ei_class = so_data[4] #1=32bit,2=64bitprint(f"Class: {'64-bit' if ei_class == 2 else '32-bit'}")#Getsection headerstofind .textimport structe_shoff = struct.unpack_from('<Q', so_data, 0x28)[0]e_shentsize = struct.unpack_from('<H', so_data, 0x3A)[0]e_shnum = struct.unpack_from('<H', so_data, 0x3C)[0]e_shstrndx = struct.unpack_from('<H', so_data, 0x3E)[0]print(f"Section headers at: 0x{e_shoff:x}, count: {e_shnum}, size: {e_shentsize}")#Getprogram headersforloadinge_phoff = struct.unpack_from('<Q', so_data, 0x20)[0]e_phentsize = struct.unpack_from('<H', so_data, 0x36)[0]e_phnum = struct.unpack_from('<H', so_data, 0x38)[0]print(f"nProgram headers at: 0x{e_phoff:x}, count: {e_phnum}")foriinrange(e_phnum): off= e_phoff + i * e_phentsize p_type = struct.unpack_from(' with open(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhjm.so", "rb") as f: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^FileNotFoundError: [Errno 2] No such file or directory: 'D:\AI\AICTF\workdir\52pojie\chu8\apk_unzipped\lib\x86_64\libhjm.so'[error: exit status 1]
复制代码隐藏代码Nofiles found.
复制代码隐藏代码D:
AIAICTFworkdir52pojiechu8apk_unzippedlibarm64-v8alibhajimi.soD:
AIAICTFworkdir52pojiechu8apk_unzippedlibarmeabi-v7alibhajimi.soD:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86libhajimi.soD:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so
复制代码隐藏代码importstructwithopen(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so","rb")asf: so_data = f.read()
# Get program headers for loadinge_phoff = struct.unpack_from('<Q', so_data,0x20)[0]e_phentsize = struct.unpack_from('<H', so_data,0x36)[0]e_phnum = struct.unpack_from('<H', so_data,0x38)[0]segments = []foriinrange(e_phnum): off = e_phoff + i * e_phentsize p_type = struct.unpack_from(' setnz cl -> cl=1
# or cl, byte_5CFF8 -> cl |= byte_5CFF8
# or cl, r13b -> cl |= r13b
# test cl, 1 -> jz fail (won't jump since cl=1)
# test al, al -> jz 24bda (won't jump since al=1)
# call sub_2E570 -> rax = debug_key
# rsi = 0xA5A5A5A5A5A5A5A5
# xor rsi, rax -> rsi = debug_key ^ 0xA5A5A5A5A5A5A5A5
# test r13b, r13b -> cmovz rsi, rax
# If r13b=0: rsi = rax (raw debug_key)
# If r13b=1: rsi = debug_key ^ 0xA5A5A5A5A5A5A5A5
# r13b is set at 0x24a1e or 0x24a30
# At 0x24a30: xor r13d, r13d (r13b=0) when byte_5D00C != 1
# byte_5D00C is set to 1 at 0x249a0 when dword_5D008 >= 4
# dword_5D008 is the experience counter. For debug bypass, it might be 0.# So byte_5D00C = 0, and we go to 0x24a30: r13b = 0
# Therefore: rsi = rax = debug_key (NO XOR)
# BUT WAIT: at 0x249a0, byte_5D00C is set to 1 BEFORE the splitmix64 code.# The flow is:# 0x24898: cmp dword_5D008, 4
# 0x2489f: jge 0x249a0 (if exp >= 4, set byte_5D00C=1, then do splitmix)
# 0x248a5: ... (if exp < 4, different path)
# For debug bypass with exp=0: we DON'T go to 0x249a0.# Instead we go through the other path. Let me check what happens.# Actually, let me just check: what is byte_5D00C initially? It's in BSS, so 0.# And dword_5D008 is also 0.# So at 0x24898: 0 < 4, so we DON'T jump to 0x249a0.# We continue at 0x248a5.# Let me look at 0x248a5:
print("nNow checking the flow when exp < 4...")
复制代码隐藏代码qfe8 = 0x810a3647628f0212debug_key = 0xd2c13a26769ce7e0Now checking the flow when exp < 4...
复制代码隐藏代码{"addr":"0x24890","asm": { "name":"verifyAndDecrypt", "start_ea":"0x24890", "lines":"verifyAndDecrypt (.text @ 0x24890):
n24890 call qword ptr [rax+558h]n24896 test eax, eaxn24898 jle loc_24934n2489e mov ebp, eaxn248a0 mov ebx, eaxn248a2 mov rdi, rbx; sizen248a5 call __Znwm; operator new(ulong)n248aa mov [rsp+88h+var_70], raxn248af lea r12, [rax+rbx]n248b3 mov [rsp+88h+var_60], r12n248b8 mov rdi, rax; sn248bb xor esi, esi; cn248bd mov [rsp+88h+var_78], rbxn248c2 mov rdx, rbx; nn248c5 mov rbx, raxn248c8 call _memsetn248cd mov [rsp+88h+var_68], r12n248d2 mov rax, [r14]n248d5 mov rdi, r14n248d8 mov rsi, r13n248db xor edx, edxn248dd mov ecx, ebpn248df mov r8, rbxn248e2 call qword ptr [rax+640h]n248e8 cmp ebp, 33h ; '3'n248eb jbe short loc_248F5n248ed cmp dword ptr [rbx], 314D4A48hn248f3 jz short loc_24967n248f5 mov rax, [r14]n248f8 mov rdi, r14", "stack_frame": [ { "name":"var_80", "offset":"0x8", "size":"0x4", "type":"_DWORD" }, { "name":"var_7C", "offset":"0xc", "size":"0x4", "type":"_DWORD" }, { "name":"var_78", "offset":"0x10", "size":"0x8", "type":"_QWORD" }, { "name":"var_70", "offset":"0x18", "size":"0x8", "type":"_QWORD" }, { "name":"var_68", "offset":"0x20", "size":"0x8", "type":"_QWORD" }, { "name":"var_60", "offset":"0x28", "size":"0x8", "type":"_QWORD" }, { "name":"s2", "offset":"0x30", "size":"0x8", "type":"void *" }, { "name":"var_50", "offset":"0x38", "size":"0x8", "type":"_QWORD" }, { "name":"var_38", "offset":"0x50", "size":"0x8", "type":"_QWORD" }, { "name":"__return_address", "offset":"0x88", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"__int64", "arguments": [ { "name":"arg0", "type":"__int64 *" }, { "name":"arg1", "type":"__int64" }, { "name":"arg2", "type":"__int64" }, { "name":"arg3", "type":"__int64" } ] },"instruction_count":30,"total_instructions": null,"cursor": { "next":30 }}
复制代码隐藏代码fromunicornimport*fromunicorn.x86_constimport*importstruct, xxhashwithopen(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedlibx86_64libhajimi.so","rb")asf: so_data = f.read()BASE =0x10000000STACK_BASE =0x7FFF0000; STACK_SIZE =0x200000HEAP =0x20000000; FS_BASE =0x30000000; RET_ADDR =0x40000000mu = Uc(UC_ARCH_X86, UC_MODE_64)mapped =set()segs = [(0x0,0x0,0x56570,0x56570),(0x57570,0x56570,0x4728,0x4728),(0x5cca0,0x5aca0,0xe8,0xfc0)]forva,fo,fs,msinsegs: s=(BASE+va)&~0xFFF; e=((BASE+va+ms)+0xFFF)&~0xFFF forpginrange(s,e,0x1000): ifpgnotinmapped: mu.mem_map(pg,0x1000); mapped.add(pg) mu.mem_write(BASE+va, so_data[fo:fo+fs])mu.mem_map(STACK_BASE, STACK_SIZE)mu.mem_map(HEAP,0x200000)mu.mem_map(FS_BASE,0x1000)mu.mem_write(FS_BASE+0x28, struct.pack('<Q',0xDEADBEEFCAFEBABE))mu.msr_write(0xC0000100, FS_BASE)mu.mem_map(RET_ADDR,0x1000)mu.mem_write(RET_ADDR,b'xcc')
# Read hjm_pack.binwithopen(r"D:
AIAICTFworkdir52pojiechu8apk_unzippedassetshjm_pack.bin","rb")asf: hjm_data = f.read()
# Set up globalsbeatmap = struct.pack('<4I',0,250,500,750)qfe8 = xxhash.xxh64(beatmap, seed=0x1A8CBC5B802E097C).intdigest()mu.mem_write(BASE +0x5CFD0, struct.pack('= 0x34 bytes and start with magic 0x314D4A48
# Set up the file data in heapFILE_DATA = HEAP +0x10000mu.mem_write(FILE_DATA, hjm_data)
# Set up the a1 structure (two pointers: start, end)A1_STRUCT = HEAP +0x20000mu.mem_write(A1_STRUCT, struct.pack('<QQ', FILE_DATA, FILE_DATA +len(hjm_data)))
# The key value - try debug_key (raw, no XOR)debug_key =0xd2c13a26769ce7e0
# Hook operator new and operator delete to provide heap memoryNEW_HEAP = HEAP +0x30000new_offset = [0]defhook_code(uc, address, size, user_data): pass
# We need to handle calls to operator new, operator delete, memcpy, memset
# Let me patch the PLT entries to return immediately
# Find PLT entries - let me just hook specific addresses
# sub_2E680 calls:# - sub_2EB00 (key derivation)
# - sub_24CB0 (xxhash fold)
# - sub_2DF40 (AES-CTR)
# - operator new, operator delete, memcpy, memset (via PLT)
# Let me check what external calls sub_2E680 makesprint("Testing emulation of sub_2E680...")
# Set up callrsp = STACK_BASE + STACK_SIZE -0x2000mu.mem_write(rsp, struct.pack('<Q', RET_ADDR))mu.reg_write(UC_X86_REG_RSP, rsp)mu.reg_write(UC_X86_REG_RDI, A1_STRUCT)mu.reg_write(UC_X86_REG_RSI, debug_key)
# Hook to intercept PLT callscall_log = []defhook_mem_invalid(uc, access, address, size, value, user_data): rip = uc.reg_read(UC_X86_REG_RIP) call_log.append(f"Invalid mem access at RIP=0x{rip:x}, addr=0x{address:x}, access={access}") returnFalsemu.hook_add(UC_HOOK_MEM_UNMAPPED, hook_mem_invalid)try: mu.emu_start(BASE +0x2E680, RET_ADDR, timeout=10000000, count=50000) rip = mu.reg_read(UC_X86_REG_RIP) ifrip == RET_ADDR: result = mu.reg_read(UC_X86_REG_RAX) print(f"sub_2E680 returned: 0x{result:x}") else: print(f"Stopped at RIP=0x{rip:x}")exceptUcErrorase: rip = mu.reg_read(UC_X86_REG_RIP) print(f"Error at RIP=0x{rip:x}:{e}") ifcall_log: forlincall_log[-5:]:
print(f" {l}")
复制代码隐藏代码Testing emulation ofsub_2E680...ErroratRIP=0x1002e86f: Invalidinstruction(UC_ERR_INSN_INVALID)
复制代码隐藏代码{"addr":"0x2E860","asm": { "name":"sub_2E680", "start_ea":"0x2e860", "lines":"sub_2E680 (.text @ 0x2e860):
n2e861 mov rax, [r14]n2e864 mov ecx, r15dn2e867 shr ecx, 8n2e86a movd xmm0, r15dn2e86f pinsrb xmm0, ecx, 1n2e875 mov ecx, r15dn2e878 shr ecx, 10hn2e87b pinsrb xmm0, ecx, 2n2e881 mov ecx, r15dn2e884 shr ecx, 18hn2e887 pinsrb xmm0, ecx, 3n2e88d mov [rsp+0E8h+src], raxn2e895 movzx ecx, byte ptr [rsp+0E8h+var_A8]n2e89a pinsrb xmm0, ecx, 4n2e8a0 movzx ecx, byte ptr [rsp+0E8h+var_B0]n2e8a5 pinsrb xmm0, ecx, 5n2e8ab mov ecx, [r14+8]n2e8af mov dword ptr [rsp+0E8h+src+8], ecxn2e8b6 movzx ecx, byte ptr [rsp+0E8h+var_B8]n2e8bb pinsrb xmm0, ecx, 6", "stack_frame": [ { "name":"var_E8", "offset":"0x0", "size":"0x8", "type":"_QWORD" }, { "name":"var_E0", "offset":"0x8", "size":"0x8", "type":"_QWORD" }, { "name":"n", "offset":"0x10", "size":"0x8", "type":"size_t" }, { "name":"var_D0", "offset":"0x18", "size":"0x8", "type":"_QWORD" }, { "name":"var_C8", "offset":"0x20", "size":"0x8", "type":"_QWORD" }, { "name":"var_C0", "offset":"0x28", "size":"0x8", "type":"_QWORD" }, { "name":"var_B8", "offset":"0x30", "size":"0x8", "type":"_QWORD" }, { "name":"var_B0", "offset":"0x38", "size":"0x8", "type":"_QWORD" }, { "name":"var_A8", "offset":"0x40", "size":"0x8", "type":"_QWORD" }, { "name":"var_A0", "offset":"0x48", "size":"0x8", "type":"_QWORD" }, { "name":"var_98", "offset":"0x50", "size":"0x8", "type":"_QWORD" }, { "name":"var_90", "offset":"0x58", "size":"0x8", "type":"_QWORD" }, { "name":"ptr", "offset":"0x60", "size":"0x10", "type":"void *[2]" }, { "name":"var_78", "offset":"0x70", "size":"0x8", "type":"_QWORD" }, { "name":"var_68", "offset":"0x80", "size":"0x10", "type":"_OWORD" }, { "name":"src", "offset":"0x90", "size":"0x10", "type":"void *[2]" }, { "name":"var_48", "offset":"0xa0", "size":"0x10", "type":"_OWORD" }, { "name":"var_38", "offset":"0xb0", "size":"0x8", "type":"_QWORD" }, { "name":"__return_address", "offset":"0xe8", "size":"0x8", "type":"_UNKNOWN *" } ], "return_type":"__int64", "arguments": [ { "name":"arg0", "type":"_QWORD *" }, { "name":"arg1", "type":"__int64" } ] },"instruction_count":20,"total_instructions": null,"cursor": { "next":20 }}
复制代码隐藏代码
# The pinsrb at 0x2e86f is the issue. Let me look at what it's doing:# It's building an XMM0 register byte-by-byte from r15d (chunk counter) and
# the folded qfe8 value. Then XORing with the IV.## xmm0[0] = r15d & 0xFF
# xmm0[1] = (r15d >> 8) & 0xFF
# xmm0[2] = (r15d >> 16) & 0xFF
# xmm0[3] = (r15d >> 24) & 0xFF
# xmm0[4] = var_A8 byte (from folded qfe8)
# xmm0[5] = var_B0 byte
# xmm0[6] = var_B8 byte
# xmm0[7] = var_C0 byte## So xmm0[0:4] = r15d (chunk counter as LE bytes)
# xmm0[4:8] = folded qfe8 as LE bytes## This is exactly what I had: struct.pack(' var_68mu = make_emu()mu.mem_write(HEAP +0x2000, salt)mu.mem_write(HEAP +0x3000,b'x00'*16)call_func(mu,0x2EB00, rdi=debug_key, rsi=qfe8, rdx=HEAP+0x2000, rcx=HEAP+0x3000)var_68 =bytes(mu.mem_read(HEAP +0x3000,16))print(f"var_68 ={var_68.hex()}")
# Step 2: For each chunk, compute AES key via sub_24CB0folded = (qfe8 ^ (qfe8 >>32)) &0xFFFFFFFFtotal =len(encrypted)num_chunks = (total +255) //256decrypted =bytearray(total)var_E0 =0forciinrange(num_chunks): # Build 32-byte src buffer src = var_68 # 16 bytes src += struct.pack('> (7- x%8)) &1), ("LSB_first",lambday,x: (data[y*8+ x//8] >> (x%8)) &1), ("MSB_inv",lambday,x:1- ((data[y*8+ x//8] >> (7- x%8)) &1)), ("LSB_inv",lambday,x:1- ((data[y*8+ x//8] >> (x%8)) &1)),]: img = Image.new('1', (64,64)) foryinrange(64): forxinrange(64): img.putpixel((x, y), get_pixel(y, x)) fn =rf"D:
AIAICTFworkdir52pojiechu8qr_{name}.png" img_scaled = img.resize((640,640), Image.NEAREST) img_scaled.save(fn)
# Print ASCII art for MSB_inv (white=space, black=█)print("MSB_inv (inverted, likely QR):")foryinrange(64): row ="" forxinrange(64): bit = (data[y*8+ x//8] >> (7- x%8)) &1 row +=" "ifbitelse"█" print(row)
复制代码隐藏代码MSB_inv(inverted, likely QR):██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ █ ██████ ███ ████ ██ ███ ███ █ ███ █ ███ ██ ██████ █████ █████ ███ █ ███ ███ ███ ███ ████ ██ █ █ ███ █ ███ █████ ██ █████ ███ █ ███████ ███ ████ ██ █ █ █ ███ █ ███ █████ █████ █████ █ █ ██ ████ ███ ████ ██ ███ █ █ █ █ █████ █████ █████ ███ █ ███ ███ ███ ███ ████ ██ ███ █ █ █ █ ███ █████ █████ █████ ███ █ ███ ███ ███ ███ █ ██ ██ ███ █ █ █ ███ █████ █████ █ ███ ██ ████ ██ ███ ██ ███ ███ █ ███ █ ███ █████████████████████████████████████████████████████████████████████ ████ ██ ███ ███ ███ ██ ███ █ ██ █████ ██████ ███ ████ ██ ███ █ ███ █ ███ █ █████ ██ █ ███ █ █████ ███ █████ ███ ████ ██████ █ ██ █████ █ █████ █ █ █ ███ █ █████ ███ █████ █████ █████ ██ █ █ ████ ██ ██ ██ █ ██ █████ ███ █████ ████████ ████ ███ ██ ███ ███ ███ █ ███ █ ███ █ █████ ███ █████ █████ ██ ███ ████ ███ ██ ████ ███ █ ███ █ ███ █ █████ ███ █████ ██████ ███ ██ ██ ██ ██ ███ █ ██ █ ██████████████████████████████████████████████████████████████████████████████████████████████████ ███████████████████████████████████████████████████████████████ ███████████████████████████████████████████████████████████████ ████████████████████████████████████████████████████████████████ ██████████████████████████████████████████████████████████████ ███████████████████████████████████████████████████████████████ ██████████████████████████████████████████████████████████████ ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
复制代码隐藏代码
# The bitmap shows QR-like patterns in rows 20-35 (bytes 160-280 roughly)
# But rows 0-19 and 36-63 are all white (all 1s when inverted = all 0s in data)
# This means the data IS mostly zeros with a QR code in the middle.# But the QR code seems incomplete/corrupted.# Wait - looking more carefully, the QR code IS there but it's only in the middle portion.# The rest being all zeros is correct - it's a 64x64 image with a QR code centered in it.# The QR code appears to be roughly 44x16 pixels, which is unusual.# Actually, looking at the pattern more carefully:# Rows 20-35 have the QR-like pattern (16 rows)
# Rows 36-42 have a few scattered bits
# This looks like a valid QR code that's been placed in the center of a 64x64 canvas
# Let me try to scan itimportstructwithopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()
# Count non-zero bytes per rowforyinrange(64): row_data = data[y*8:(y+1)*8] ifany(b !=0forbinrow_data): bits =''.join(str((row_data[x//8] >> (7-x%8)) &1)forxinrange(64)) print(f"Row{y:2d}:{bits}")
复制代码隐藏代码Row 20:
0011111010000001110001110000110010001000111010001010001001110000Row 21:
0010000010000010001010001000100010001000010011011010001010001000Row 22:
0011110010000010001010000000100011111000010010101010001010001000Row 23:
0010000010000011111010111001000010001000010010001010101011111000Row 24:
0010000010000010001010001000100010001000010010001010101010001000Row 25:
0010000010000010001010001000100010001010010010001011011010001000Row 26:
0010000011111010001001110000110010001001100010001010001010001000Row 28:
0011110000111001110001110001110001110010001011110010000011110000Row 29:
0010001000010010001010001010001010000011001010001010000010001000Row 30:
0010001000010000001010011000001010000010101010001010000010001000Row 31:
0011110000010000010010101000010011110010011011110010000010001000Row 32:
0010000000010000100011001000100010001010001010001010000010001000Row 33:
0010000010010001000010001001000010001010001010001010000010001000Row 34:
0010000001100011111001110011111001110010001011110011111011110000Row 36:
0000000000000000000000000000001100000000000000000000000000000000Row 37:
0000000000000000000000000000000100000000000000000000000000000000Row 38:
0000000000000000000000000000000100000000000000000000000000000000Row 39:
0000000000000000000000000000000010000000000000000000000000000000Row 40:
0000000000000000000000000000000100000000000000000000000000000000Row 41:
0000000000000000000000000000000100000000000000000000000000000000Row 42:
0000000000000000000000000000001100000000000000000000000000000000
复制代码隐藏代码
# The bitmap has text rendered in it. Let me try to read it.# Each character appears to be about 8 pixels wide and 7 pixels tall (rows 20-26, 28-34)
# There's a gap at row 27 (separator between two lines of text)
# Let me extract the two text blocks and try OCR or visual analysisfromPILimportImagewithopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()
# Create a clean image of just the text area, scaled upimg = Image.new('L', (64,64),255)foryinrange(64): forxinrange(64): bit = (data[y*8+ x//8] >> (7- x%8)) &1 ifbit: img.putpixel((x, y),0) # black for 1-bits
# Scale up 10x for readabilityimg_big = img.resize((640,640), Image.NEAREST)img_big.save(r"D:
AIAICTFworkdir52pojiechu8text_bitmap.png")
# Crop just the text area (rows 20-34, all 64 columns)img_text = img.crop((0,20,64,35))img_text_big = img_text.resize((640,150), Image.NEAREST)img_text_big.save(r"D:
AIAICTFworkdir52pojiechu8text_cropped.png")
# Also the vertical line in rows 36-42print("Vertical line area (rows 36-42):")foryinrange(36,43): row_data = data[y*8:(y+1)*8] bits =''.join('█'if(row_data[x//8] >> (7-x%8)) &1else' 'forxinrange(64)) print(f" {bits}")print("nText area rows 20-26 (line 1):")foryinrange(20,27): row_data = data[y*8:(y+1)*8] bits =''.join('█'if(row_data[x//8] >> (7-x%8)) &1else' 'forxinrange(64)) print(f" {bits}")print("nText area rows 28-34 (line 2):")foryinrange(28,35): row_data = data[y*8:(y+1)*8] bits =''.join('█'if(row_data[x//8] >> (7-x%8)) &1else' 'forxinrange(64)) print(f" {bits}")
复制代码隐藏代码Verticallinearea(rows36-42): ██ █ █ █ █ █ ██ Textarearows20-26(line1): █████ █ ███ ███ ██ █ █ ███ █ █ █ █ ███ █ █ █ █ █ █ █ █ █ █ ██ ██ █ █ █ █ ████ █ █ █ █ █ █████ █ █ █ █ █ █ █ █ █ █ █████ █ ███ █ █ █ █ █ █ █ █ █ █████ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ ██ ██ █ █ █ █████ █ █ ███ ██ █ █ ██ █ █ █ █ █ █ Textarearows28-34(line2): ████ ███ ███ ███ ███ ███ █ █ ████ █ ████ █ █ █ █ █ █ █ █ █ █ ██ █ █ █ █ █ █ █ █ █ █ █ ██ █ █ █ █ █ █ █ █ █ █ ████ █ █ █ █ █ █ ████ █ ██ ████ █ █ █ █ █ █ ██ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ ██ █████ ███ █████ ███ █ █ ████ █████ ████
复制代码隐藏代码
# Let me carefully read each character from the bitmap
# Line 1 (rows 20-26): Each char is ~5-6 pixels wide with 1px spacing
# Let me extract columns for each characterwithopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()
# Print line 1 with column numbersprint("Line 1 (rows 20-26):")print("Col: ", end="")forxinrange(64): print(x %10, end="")print()foryinrange(20,27): row_data = data[y*8:(y+1)*8] print(f"R{y}: ", end="") forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 print('█'ifbitelse' ', end="") print()print("nLine 2 (rows 28-34):")print("Col: ", end="")forxinrange(64): print(x %10, end="")print()foryinrange(28,35): row_data = data[y*8:(y+1)*8] print(f"R{y}: ", end="") forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 print('█'ifbitelse' ', end="") print()
复制代码隐藏代码Line 1 (rows 20-26):
Col: 0123456789012345678901234567890123456789012345678901234567890123R20: █████ █ ███ ███ ██ █ █ ███ █ █ █ █ ███ R21: █ █ █ █ █ █ █ █ █ █ ██ ██ █ █ █ █ R22: ████ █ █ █ █ █ █████ █ █ █ █ █ █ █ █ R23: █ █ █████ █ ███ █ █ █ █ █ █ █ █ █ █████ R24: █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ R25: █ █ █ █ █ █ █ █ █ █ █ █ █ ██ ██ █ █ R26: █ █████ █ █ ███ ██ █ █ ██ █ █ █ █ █ █ Line 2 (rows 28-34):
Col: 0123456789012345678901234567890123456789012345678901234567890123R28: ████ ███ ███ ███ ███ ███ █ █ ████ █ ████ R29: █ █ █ █ █ █ █ █ █ █ ██ █ █ █ █ █ █ R30: █ █ █ █ █ ██ █ █ █ █ █ █ █ █ █ █ R31: ████ █ █ █ █ █ █ ████ █ ██ ████ █ █ █ R32: █ █ █ ██ █ █ █ █ █ █ █ █ █ █ █ R33: █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ R34: █ ██ █████ ███ █████ ███ █ █ ████ █████ ████
复制代码隐藏代码
# Let me carefully identify each character by column ranges
# Line 1 characters (cols 2-57 approximately):# Looking at the pixel patterns:# Cols 2-6: F (█████, █, ████, █, █, █, █)
# Cols 8-12: L (█, █, █, █, █, █, █████)
# Cols 14-18: A (███, █ █, █ █, █████, █ █, █ █, █ █) -> wait
# Actually let me look at it differently
# Col 2-6:# R20: █████ -> F
# R21: █# R22: ████# R23: █# R24: █# R25: █# R26: █# Col 8-12:# R20: █ -> L
# R21: █# R22: █# R23: █# R24: █# R25: █# R26: █████# Col 14-18:# R20: ███ -> A
# R21: █ █# R22: █ █# R23: █████# R24: █ █# R25: █ █# R26: █ █# Col 20-24:# R20: ███ -> G
# R21: █ █# R22: █# R23: █ ███# R24: █ █# R25: █ █# R26: ███# Col 26-29:# R20: ██ -> {# R21: █# R22: █# R23: █# R24: █# R25: █# R26: ██# Col 31-35:# R20: █ █ -> H
# R21: █ █# R22: █████# R23: █ █# R24: █ █# R25: █ █# R26: █ █# Col 37-39:# R20: ███ -> I? No...# R21: █# R22: █# R23: █# R24: █# R25: █ █ -> wait, that's J? No...# R26: ██# Hmm, let me look at this more carefully with exact column positionsforyinrange(20,27): row_data = data[y*8:(y+1)*8] s ="" forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")print()foryinrange(28,35): row_data = data[y*8:(y+1)*8] s ="" forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")
复制代码隐藏代码Traceback (most recent call last): File"C:
UsersWOYOUY~1AppDataLocalTempctf_agent_2198965434.py", line78,in<module> row_data = data[y*8:(y+1)*8] ^^^^NameError: name'data'is not defined[error:
exitstatus1]
复制代码隐藏代码withopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()print("Line 1:")foryinrange(20,27): row_data = data[y*8:(y+1)*8] s ="" forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")print("nLine 2:")foryinrange(28,35): row_data = data[y*8:(y+1)*8] s ="" forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")
# Now let me try OCR on the scaled image
复制代码隐藏代码Line 1:
R20:··█████·█······███···███····██··█···█···███·█···█·█···█··███····R21:··█·····█·····█···█·█···█···█···█···█····█··██·██·█···█·█···█···R22:··████··█·····█···█·█·······█···█████····█··█·█·█·█···█·█···█···R23:··█·····█·····█████·█·███··█····█···█····█··█···█·█·█·█·█████···R24:··█·····█·····█···█·█···█···█···█···█····█··█···█·█·█·█·█···█···R25:··█·····█·····█···█·█···█···█···█···█·█··█··█···█·██·██·█···█···R26:··█·····█████·█···█··███····██··█···█··██···█···█·█···█·█···█···Line 2:
R28:··████····███··███···███···███···███··█···█·████··█·····████····R29:··█···█····█··█···█·█···█·█···█·█·····██··█·█···█·█·····█···█···R30:··█···█····█······█·█··██·····█·█·····█·█·█·█···█·█·····█···█···R31:··████·····█·····█··█·█·█····█··████··█··██·████··█·····█···█···R32:··█········█····█···██··█···█···█···█·█···█·█···█·█·····█···█···R33:··█·····█··█···█····█···█··█····█···█·█···█·█···█·█·····█···█···R34:··█······██···█████··███··█████··███··█···█·████··█████·████····
复制代码隐藏代码
# Line 1 character analysis (7 rows high, reading column by column):# Cols 2-6: F L A G { H I M W A (reading the pixel font)
# Let me segment by looking for blank columns (all dots)line1_rows = []line2_rows = []withopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()foryinrange(20,27): row = [] forxinrange(64): bit = (data[y*8+ x//8] >> (7- x%8)) &1 row.append(bit) line1_rows.append(row)foryinrange(28,35): row = [] forxinrange(64): bit = (data[y*8+ x//8] >> (7- x%8)) &1 row.append(bit) line2_rows.append(row)
# Find character boundaries by looking for blank columnsdeffind_chars(rows): chars = [] in_char =False start =0 forxinrange(64): col_has_pixel =any(rows[y][x]foryinrange(len(rows))) ifcol_has_pixelandnotin_char: start = x in_char =True elifnotcol_has_pixelandin_char: chars.append((start, x)) in_char =False ifin_char: chars.append((start,64)) returncharschars1 = find_chars(line1_rows)chars2 = find_chars(line2_rows)print("Line 1 characters:")fori, (s, e)inenumerate(chars1): print(f" Char{i}: cols{s}-{e}(width{e-s})") foryinrange(7): row =''.join('█'ifline1_rows[y][x]else'·'forxinrange(s, e)) print(f" {row}") print()print("nLine 2 characters:")fori, (s, e)inenumerate(chars2): print(f" Char{i}: cols{s}-{e}(width{e-s})") foryinrange(7): row =''.join('█'ifline2_rows[y][x]else'·'forxinrange(s, e)) print(f" {row}") print()
复制代码隐藏代码Line 1 characters:
Char 0:
cols2-7(width5) █████ █···· ████· █···· █···· █···· █····Char 1:
cols8-13(width5) █···· █···· █···· █···· █···· █···· █████Char 2:
cols14-19(width5) ·███· █···█ █···█ █████ █···█ █···█ █···█Char 3:
cols20-25(width5) ·███· █···█ █···· █·███ █···█ █···█ ·███·Char 4:
cols27-30(width3) ·██ ·█· ·█· █·· ·█· ·█· ·██Char 5:
cols32-37(width5) █···█ █···█ █████ █···█ █···█ █···█ █···█Char 6:
cols38-43(width5) ··███ ···█· ···█· ···█· ···█· █··█· ·██··Char 7:
cols44-49(width5) █···█ ██·██ █·█·█ █···█ █···█ █···█ █···█Char 8:
cols50-55(width5) █···█ █···█ █···█ █·█·█ █·█·█ ██·██ █···█Char 9:
cols56-61(width5) ·███· █···█ █···█ █████ █···█ █···█ █···█Line 2 characters:
Char 0:
cols2-7(width5) ████· █···█ █···█ ████· █···· █···· █····Char 1:
cols8-13(width5) ··███ ···█· ···█· ···█· ···█· █··█· ·██··Char 2:
cols14-19(width5) ·███· █···█ ····█ ···█· ··█·· ·█··· █████Char 3:
cols20-25(width5) ·███· █···█ █··██ █·█·█ ██··█ █···█ ·███·Char 4:
cols26-31(width5) ·███· █···█ ····█ ···█· ··█·· ·█··· █████Char 5:
cols32-37(width5) ·███· █···· █···· ████· █···█ █···█ ·███·Char 6:
cols38-43(width5) █···█ ██··█ █·█·█ █··██ █···█ █···█ █···█Char 7:
cols44-49(width5) ████· █···█ █···█ ████· █···█ █···█ ████·Char 8:
cols50-55(width5) █···· █···· █···· █···· █···· █···· █████Char 9:
cols56-61(width5) ████· █···█ █···█ █···█ █···█ █···█ ████·
复制代码隐藏代码
# Let me also check if there's a closing brace }# The vertical line in rows 36-42 might be the closing bracewithopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()print("Rows 36-42 (potential closing brace):")foryinrange(36,43): row_data = data[y*8:(y+1)*8] s ="" forxinrange(28,36): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")
# That vertical pattern at cols 30-31:# R36: ██# R37: ·█# R38: ·█# R39: ··█ (shifted right = this is })
# R40: ·█# R41: ·█# R42: ██# This is indeed a closing brace }print("nFull flag: FLAG{HJMWAPJ2026NBLD}")
复制代码隐藏代码Rows 36-42 (potential closing brace):
R36:··██····R37:···█····R38:···█····R39:····█···R40:···█····R41:···█····R42:··██····Full flag:
FLAG{HJMWAPJ2026NBLD}
复制代码隐藏代码已捕获 flag，已在界面弹窗中提供复制与人工确认入口（正确/错误）。
复制代码隐藏代码importstruct, xxhashbeatmap = struct.pack('<4I',0,250,500,750)qfe8 = xxhash.xxh64(beatmap, seed=0x1A8CBC5B802E097C).intdigest()
# qfe8 = 0x810a3647628f0212
复制代码隐藏代码defsplitmix64(state): state = u64(state +0x9E3779B97F4A7C15) z = state z = u64((z ^ (z >>30)) *0xBF58476D1CE4E5B9) z = u64((z ^ (z >>27)) *0x94D049BB133111EB) returnstate, z ^ (z >>31)
# r14 = 0x1A8CBC5B802E097C ^ qfe8r14 = u64(0x1A8CBC5B802E097C^ qfe8)state, sm_result = splitmix64(r14)
# 循环4次 SipHash 混合...debug_key =0xd2c13a26769ce7e0
复制代码隐藏代码24be1: mov rsi, 0xA5A5A5A5A5A5A5A524beb: xor rsi, rax ; rsi = debug_key ^ 0xA5...24bee: test r13b, r13b ; r13b = 密码验证是否通过24bf1: cmovz rsi, rax ; 若密码未验证，不做 XOR24bf5: call sub_2E680 ; 传入最终密钥进行解密
复制代码隐藏代码withopen("hjm_pack.bin","rb")asf: hjm = f.read()
# HJM1 文件格式：# [0:4] = magic "HJM1" (0x314D4A48)
# [4:8] = version/flags
# [8:16] = encrypted data size (8 bytes LE)
# [16:24] = reserved
# [24:40] = salt (16 bytes)
# [40:52] = IV/nonce (12 bytes)
# [52:] = encrypted data (512 bytes = 64x64 bitmap, 1 bit/pixel)salt = hjm[24:40] # 0f1e2d3c4b5a69788796a5b4c3d2e1f0iv = hjm[40:52] # 112233445566778899aabbccciphertext = hjm[52:52+512]
复制代码隐藏代码fromunicornimport*fromunicorn.x86_constimport*# 加载 libhajimi.so 到 Unicornwithopen("libhajimi.so","rb")asf: so_data = f.read()BASE =0x10000000mu = Uc(UC_ARCH_X86, UC_MODE_64)
# 映射 ELF 段segs = [ (0x0,0x0,0x56570,0x56570), (0x57570,0x56570,0x4728,0x4728), (0x5cca0,0x5aca0,0xe8,0xfc0)]forva, fo, fs, msinsegs: s = (BASE + va) & ~0xFFF e = ((BASE + va + ms) +0xFFF) & ~0xFFF mu.mem_map(s, e - s) mu.mem_write(BASE + va, so_data[fo:fo+fs])
# 设置栈、堆、FS段STACK_BASE =0x7FFF0000; STACK_SIZE =0x200000mu.mem_map(STACK_BASE, STACK_SIZE)mu.mem_map(0x20000000,0x200000) # heapmu.mem_map(0x30000000,0x1000) # FS basemu.mem_write(0x30000000+0x28, struct.pack('<Q',0xDEADBEEFCAFEBABE))mu.msr_write(0xC0000100,0x30000000)
# 调用 sub_2EB00(rdi=debug_key, rsi=qfe8, rdx=out_buf, rcx=out_size)
# ... 设置参数并执行
复制代码隐藏代码var_68 = 7f721557831c2dbd7f70756f448aee26 q0 = 0xbd2d1c835715727f q1 = 0x26ee8a446f75707f
复制代码隐藏代码
# src[0:16] = var_68 (来自 sub_2EB00 的密钥材料)
# src[16:20] = chunk_counter (uint32 LE)
# src[20:24] = qfe8 的低 32 位
# src[24:32] = qfe8 ^ (chunk_idx * 0x100000000)
复制代码隐藏代码defsub_24CB0(data, seed): """XXHash64 with final fold: result ^ (result >> 32)""" h = xxhash.xxh64(data, seed=seed).intdigest() returnu64(h ^ (h >>32))
# AES key = [sub_24CB0(src, 4951), sub_24CB0(src, 9320)]h1 = sub_24CB0(src_buf,4951) # 低 8 字节h2 = sub_24CB0(src_buf,9320) # 高 8 字节aes_key = struct.pack('<QQ', h1, h2) # 16 字节 AES-128 密钥
复制代码隐藏代码Chunk 0: key = 16d6d0d72e99938d72d9bcd5616451ef nonce = 112233440052f26b99aabbcc
复制代码隐藏代码folded_qfe8 = u32(qfe8 ^ (qfe8 >>32)) # 0xe3853455
# nonce[0:4] = IV[0:4] ^ struct.pack('> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")print("nLine 2:")foryinrange(28,35): row_data = data[y*8:(y+1)*8] s ="" forxinrange(64): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")
复制代码隐藏代码line1_rows = []withopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()foryinrange(20,27): row = [] forxinrange(64): bit = (data[y*8+ x//8] >> (7- x%8)) &1 row.append(bit) line1_rows.append(row)deffind_chars(rows): chars = [] in_char =False start =0 forxinrange(64): col_has_pixel =any(rows[y][x]foryinrange(len(rows))) ifcol_has_pixelandnotin_char: start = x in_char =True elifnotcol_has_pixelandin_char: chars.append((start, x)) in_char =False ifin_char: chars.append((start,64)) returncharschars1 = find_chars(line1_rows)fori, (s, e)inenumerate(chars1): print(f" Char{i}: cols{s}-{e}(width{e-s})") foryinrange(7): row =''.join('█'ifline1_rows[y][x]else'·'forxinrange(s, e)) print(f" {row}")
复制代码隐藏代码withopen(r"D:
AIAICTFworkdir52pojiechu8decrypted_emu.bin","rb")asf: data = f.read()print("Rows 36-42 (potential closing brace):")foryinrange(36,43): row_data = data[y*8:(y+1)*8] s ="" forxinrange(28,36): bit = (row_data[x//8] >> (7- x%8)) &1 s +='█'ifbitelse'·' print(f"R{y}:{s}")
# 输出：# R36: ··██····# R37: ···█····# R38: ···█····# R39: ····█··· ← 向右缩进，确认是 }# R40: ···█····# R41: ···█····# R42: ··██····
复制代码隐藏代码FLAG{HJMWAPJ2026NBLD}
复制代码隐藏代码beatMap[0,250,500,750] →XXHash64(seed=0x1A8CBC5B802E097C) → qfe8 → splitmix64 + SipHash-2-4循环 → debug_key →SipHash-2-4(debug_key, qfe8) → var_68 (16字节密钥材料) →XXHash64_fold(var_68 || counter, seed=4951/9320) → AES-128密钥 → AES-CTR 解密 →64×64位图 → 像素字体文本
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004480-wxsync-2026-04-ce75b82704451ee41e1cef8b4b976949.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004483-wxsync-2026-04-5600ac0fa03aab87e3955858bc69e8b7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004485-wxsync-2026-04-79bc96637431cea68e43f75dd2af325f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004487-wxsync-2026-04-12778f575a20a98daeabc6871da3be42.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004489-wxsync-2026-04-e4edb22671d542f13af146f9ca0f4d15.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004490-wxsync-2026-04-7709be872643dd052fedc9d43cf407b2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775004492-wxsync-2026-04-1804e4342d379920a56040d0850e3f0e.webp)