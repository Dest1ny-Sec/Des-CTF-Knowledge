# SigMachine CTF逆向题深度解析:从零到一的完整解题之旅

> 原文: https://www.ctfiot.com/283400.html
> ID: 283400

SigMachine CTF逆向题深度解析:从零到一的完整解题之旅

引言

本文将带你深入分析一道综合性的CTF逆向题目SigMachine。这道题融合了ELF文件格式、Linux信号处理、自定义加密算法、OLLVM混淆等多种技术,是学习二进制安全和逆向工程的绝佳案例。

我们将从最基础的文件分析开始,一步步深入,揭开这道题目背后的技术原理。即使你是逆向新手,也能跟随本文的节奏,理解每一个技术细节。

第一章:初次接触 – 文件信息收集

1.1 文件类型识别

拿到任何二进制文件,第一步永远是了解它的基本信息。我们使用Linux系统自带的file命令:

$ file sigmachinesigmachine: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked,forGNU/Linux 3.2.0, stripped

让我们逐个解读这些信息:

1. ELF 64-bit LSB executable

ELF: Executable and Linkable Format,Linux系统的可执行文件格式

64-bit: 64位程序,需要64位处理器和操作系统

LSB: Least Significant Byte,小端序存储(低位字节在前)

executable: 可执行文件

目标架构是x86-64(AMD64),即常见的PC处理器架构

所有需要的库函数都被编译进了这个文件

文件体积会很大(本题678KB)

好处:不依赖系统库,可以独立运行

坏处:给逆向分析增加了难度,因为代码量巨大

所有调试符号(函数名、变量名)都被移除

逆向时看到的都是地址,如sub_401990而非有意义的函数名

这是对逆向工程的第一道防线

地址0x47c093: “wrong!”

地址0x47c09a: “right!”

地址0x47c0a1: “password: “

初始化全局变量

注册信号处理器

设置程序运行环境

每行16字节,每个地址占8字节(64位)

ELF使用小端序,需要字节反转

原始数据

反转后

函数地址

700a4000 00000000

0x00000000 00400a70

0x400a70

50194000 00000000

0x00000000 00401950

0x401950

90194000 00000000

0x00000000 00401990

0x401990

f0194000 00000000

0x00000000 004019f0

0x4019f0

501a4000 00000000

0x00000000 00401a50

0x401a50

b01a4000 00000000

0x00000000 00401ab0

0x401ab0

f0044000 00000000

0x00000000 004004f0

0x4004f0

注册反调试机制

修改关键数据结构

设置信号处理陷阱

第一个参数(edi寄存器): 信号编号

第二个参数(rsi寄存器): 信号处理函数的地址

调用地址0x407360: 这是signal()函数的地址

信号编号

十六进制

Linux标准信号名

正常用途

本题重定向为

2

0x2

SIGINT

中断信号(Ctrl+C)

加法运算(ADD)

3

0x3

SIGQUIT

退出信号

减法运算(SUB)

4

0x4

SIGILL

非法指令

乘法运算(MUL)

5

0x5

SIGTRAP

调试断点

除法运算(DIV)

6

0x6

SIGABRT

程序终止

取模运算(MOD)

7

0x7

SIGBUS

总线错误

按位取反(NOT)

8

0x8

SIGFPE

浮点异常

异或运算(XOR)

10

0xa

SIGUSR1

用户信号1

或运算(OR)

11

0xb

SIGSEGV

段错误

与运算(AND)

12

0xc

SIGUSR2

用户信号2

左移运算(SHL)

13

0xd

SIGPIPE

管道破裂

右移运算(SHR)

混淆执行流:调试器很难跟踪信号的跳转

隐藏运算逻辑:代码中看不到+、-、*等明显的运算符

增加分析难度:需要理解Linux信号机制才能分析

密文长度:114字节

字符集:仅包含 D, E, G, J, L, M, Q, T, U, V, W, X 这12个字母

长度关系:114 = 38 × 3

TABLE3有8个字符 → 可以表示3位二进制(2³=8)

TABLE2有4个字符 → 可以表示2位二进制(2²=4)

3位 + 2位 + 3位 = 8位 = 1字节

位数

取值范围

对应表

表长度

3位

0-7

TABLE3

8字符

2位

0-3

TABLE2

4字符

3位

0-7

TABLE3

8字符

高3位和低3位共享同一个异或累积值xor_3

低3位的编码依赖于当前字符的高3位编码结果

这形成了字节内部的依赖关系

前后依赖:第N个字符的加密结果影响第N+1个字符

雪崩效应:明文的微小变化会导致后续所有密文改变

抵抗攻击:相同的明文字符在不同位置产生不同密文

控制流平坦化 (Control Flow Flattening)

虚假控制流 (Bogus Control Flow)

指令替换 (Instruction Substitution)

原本清晰的if-else结构变成了复杂的switch-case

程序流程变成了状态机,难以理解

IDA/Ghidra的反编译结果会非常混乱

忽略混淆,专注数据流

不纠结于控制流,关注数据的读写

追踪全局变量OPERAND[]和TMP[]的使用

识别关键模式

找到raise()系统调用

定位.rodata段的数据访问

动态分析辅助

使用GDB观察内存变化

记录输入输出关系

符号执行

使用angr等工具自动求解

让工具处理复杂的控制流

无法混淆数据

TABLE3、TABLE2这些常量表无法隐藏

目标密文必须存储在程序中

无法隐藏系统调用

signal()、raise()等调用仍然可见

可以通过strace追踪

增加代码体积

混淆后的代码通常是原代码的3-10倍

运行速度也会下降

技术

作用

学到的知识

理解程序结构

.init_array段、.rodata段、小端序

初始化机制

main之前的代码执行

运算隐藏

signal()、raise()、信号处理函数

数据编码

移位、与、或、异或

自定义加密

字节拆分与组合

增强安全性

前后依赖、雪崩效应

代码保护

控制流平坦化

工具

用途

替代方案

识别文件类型

–

提取字符串

查看ELF结构

反汇编

IDA Pro, Ghidra

脚本编写

Ruby, Perl

+ 程序

验证flag

–

《程序员的自我修养:链接、装载与库》- 深入理解ELF

《逆向工程权威指南》- 系统学习逆向

《深入理解计算机系统》(CSAPP) – 计算机基础

CTFtime.org – CTF比赛信息

Reverse Engineering Stack Exchange – 问答社区

LiveOverflow YouTube频道 – 视频教程

XCTF攻防世界 – 中文题库

pwnable.kr – 韩国平台

Crackmes.one – 破解练习

耐心观察– 从大量信息中提取关键线索

逻辑推理– 从现象推导原理

动手验证– 理论必须经过实践检验

系统思考– 将各个技术点串联成完整画面

ELF文件格式知识– 理解程序结构

操作系统机制– 利用信号系统

密码学思想– 位拆分和异或链

代码混淆技术– OLLVM增加难度

ELF格式规范:https://refspecs.linuxfoundation.org/elf/elf.pdf

Linux信号手册:man 7 signal

System V ABI:https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf

objdump手册:man objdump

readelf手册:man readelf

GDB文档:https://sourceware.org/gdb/documentation/

OLLVM项目:https://github.com/obfuscator-llvm/obfuscator

Reverse Engineering for Beginners:https://beginners.re/

CTF Wiki:https://ctf-wiki.org/

《程序员的自我修养:链接、装载与库》俞甲子等著

《深入理解计算机系统》(CSAPP) Randal E. Bryant

《逆向工程权威指南》Dennis Yurichev

《加密与解密》段钢著

术语

英文

解释

逆向工程

Reverse Engineering

从程序分析其设计和实现

静态分析

Static Analysis

不运行程序的分析

动态分析

Dynamic Analysis

运行程序时的分析

ELF

Executable and Linkable Format

Linux可执行文件格式

符号表

Symbol Table

函数名、变量名等调试信息

小端序

Little Endian

低位字节在前的存储方式

大端序

Big Endian

高位字节在前的存储方式

信号

Signal

Unix/Linux进程间通信机制

构造函数

Constructor

main之前执行的初始化函数

位运算

Bitwise Operation

对二进制位的操作

异或

XOR (Exclusive OR)

相同为0,不同为1的运算

混淆

Obfuscation

增加代码理解难度的技术

控制流

Control Flow

程序执行的路径

数据流

Data Flow

数据在程序中的传递


```
$ file sigmachinesigmachine: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked,forGNU/Linux 3.2.0, stripped
```



```
$ chmod +x sigmachine$ ./sigmachinepassword: hellowrong!
```



```
$ strings -tx sigmachine | grep -E"password|wrong|right" 7c093 wrong! 7c09a right! 7c0a1 password:
```



```
$ readelf -x .init_array sigmachine".init_array"节的十六进制输出: 0x006a0138 700a4000 00000000 50194000 00000000 p.@.....P.@..... 0x006a0148 90194000 00000000 f0194000 00000000 ..@.......@..... 0x006a0158 501a4000 00000000 b01a4000 00000000 P.@.......@..... 0x006a0168 f0044000 00000000 ..@.....
```



```
原始: 700a4000 00000000反转: 00000000 00400a70结果: 0x400a70
```



```
$ objdump -d sigmachine -M intel | grep -A 10"^0000000000401990"
```



```
401990:	push rbp401991:	mov rbp,rsp401994:	sub rsp,0x20401998:	mov edi,0x2 # 第一个参数: 信号编号240199d:	movabs rsi,0x400aa0 # 第二个参数: 处理函数地址4019a7:	call 0x407360 # 调用signal()函数4019ac:	mov edi,0x3 # 信号编号34019b1:	movabs rsi,0x400b60 # 处理函数地址4019bf:	call 0x407360 # 调用signal()
```



```
$ objdump -d sigmachine | grep -B 3"call.*407360"| grep"mov.*$0x"401998: bf 02 00 00 00 mov $0x2,%edi4019ac: bf 03 00 00 00 mov $0x3,%edi4019c4: bf 04 00 00 00 mov $0x4,%edi4019f8: bf 05 00 00 00 mov $0x5,%edi401a0c: bf 06 00 00 00 mov $0x6,%edi401a24: bf 07 00 00 00 mov $0x7,%edi401a58: bf 08 00 00 00 mov $0x8,%edi401a6c: bf 0a 00 00 00 mov $0xa,%edi401a84: bf 0b 00 00 00 mov $0xb,%edi401ab8: bf 0c 00 00 00 mov $0xc,%edi401acc: bf 0d 00 00 00 mov $0xd,%edi
```



```
result = a + b;
```



```
// 步骤1: 将操作数存入全局数组OPERAND[0] = a;OPERAND[1] = b;// 步骤2: 触发信号2(ADD信号)raise(2);// 步骤3: 信号处理函数自动被调用// (在信号处理函数内部: TMP[0] = OPERAND[0] + OPERAND[1])// 步骤4: 从全局数组读取结果result = TMP[0];
```



```
$ readelf -x .rodata sigmachine | grep -A 10"0x0047c010"
```



```
0x0047c010 58564544 554c4a54 47574d51 00000000 XVEDULJTGWMQ....0x0047c020 44474c4a 57455657 58445755 544d554a DGLJWEVWXDWUTMUJ0x0047c030 474c4a57 54555744 45574558 474c4a47 GLJWTUWDEWEXGLJG0x0047c040 54554754 55575554 474a4c57 4458574c TUGTUWUTGJLWDXWL0x0047c050 5557554a 514c5557 554c574c 54574544 UWUJQLUWULWLTWED0x0047c060 51545557 54554d4c 554d5554 4d564551 QTUWTUMLUMUTMVEQ0x0047c070 4c4a5755 4c574c54 4d4a5447 544c4d58 LJWULWLTMJTGTLMX0x0047c080 564d5658 4745444d 58564745 56515555 VMVXGEDMXVGEVQUU0x0047c090 4d4a0077 726f6e67 21007269 67687421 MJ.wrong!.right!
```



```
58 56 45 44 55 4c 4a 54X V E D U L J T
```



```
47 57 4d 51G W M Q
```



```
data = bytes.fromhex('''44474c4a 57455657 58445755 544d554a474c4a57 54555744 45574558 474c4a4754554754 55575554 474a4c57 4458574c5557554a 514c5557 554c574c 5457454451545557 54554d4c 554d5554 4d5645514c4a5755 4c574c54 4d4a5447 544c4d58564d5658 4745444d 58564745 565155554d4a'''.replace(' ','').replace('n',''))print(data.decode('ascii'))
```



```
DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ
```



```
字节: 0b 01100110 (字符'f' = 0x66) ↓拆分: 011 | 00 | 110 ↓ ↓ ↓ 高3位 中2位 低3位
```



```
byte_val =0x66# 'f'的ASCII码# 二进制: 0b01100110# 提取高3位 (bit 5-7)high_3 = (byte_val >>5) &0b111# 0b01100110 >> 5 = 0b00000011 = 3# 提取中2位 (bit 3-4)mid_2 = (byte_val >>3) &0b11# 0b01100110 >> 3 = 0b00001100# 0b00001100 & 0b11 = 0b00 = 0# 提取低3位 (bit 0-2)low_3 = byte_val &0b111# 0b01100110 & 0b111 = 0b110 = 6
```



```
xor_3 =0# 3位数据的异或累积值xor_2 =0# 2位数据的异或累积值# 对高3位编码enc_high = high_3 ^ xor_3 # 3 ^ 0 = 3# 对中2位编码enc_mid = mid_2 ^ xor_2 # 0 ^ 0 = 0# 对低3位编码(注意:这里用enc_high而非xor_3!)enc_low = low_3 ^ enc_high# 6 ^ 3 = 5
```



```
TABLE3 ="XVEDULJT"TABLE2 ="GWMQ"cipher_0 = TABLE3[enc_high] # TABLE3[3] = 'D'cipher_1 = TABLE2[enc_mid] # TABLE2[0] = 'G'cipher_2 = TABLE3[enc_low] # TABLE3[5] = 'L'print(cipher_0 + cipher_1 + cipher_2) # "DGL"
```



```
xor_3 = enc_high # 更新为3xor_2 = enc_mid # 更新为0xor_3 = enc_low # 再次更新为5(覆盖之前的值)
```



```
#!/usr/bin/env python3TABLE3 ="XVEDULJT"TABLE2 ="GWMQ"defencrypt(plaintext): """加密函数""" result ="" xor_3 =0# 3位异或累积值 xor_2 =0# 2位异或累积值 fori, charinenumerate(plaintext): byte_val = ord(char) # 位拆分 high_3 = (byte_val >>5) &0b111 mid_2 = (byte_val >>3) &0b11 low_3 = byte_val &0b111 # 异或编码 enc_high = high_3 ^ xor_3 enc_mid = mid_2 ^ xor_2 enc_low = low_3 ^ enc_high # 关键:用enc_high # 查表替换 cipher_char_0 = TABLE3[enc_high] cipher_char_1 = TABLE2[enc_mid] cipher_char_2 = TABLE3[enc_low] result += cipher_char_0 + cipher_char_1 + cipher_char_2 # 更新异或值 xor_3 = enc_high xor_2 = enc_mid xor_3 = enc_low # 再次更新 # 调试输出 print(f"[{i:02d}] '{char}' (0x{byte_val:02x}) → " f"拆分:({high_3},{mid_2},{low_3}) → " f"编码:({enc_high},{enc_mid},{enc_low}) → " f"密文:{cipher_char_0}{cipher_char_1}{cipher_char_2}") returnresult# 测试plaintext ="flag{Sig Machine S0 E4sy for Y0U 233}n"encrypted = encrypt(plaintext)TARGET ="DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ"print(f"n加密结果:{encrypted}")print(f"目标密文:{TARGET}")print(f"匹配结果:{encrypted == TARGET}")
```



```
[00] 'f' (0x66) → 拆分:(3,0,6) → 编码:(3,0,5) → 密文:DGL[01] 'l' (0x6c) → 拆分:(3,1,4) → 编码:(6,1,2) → 密文:JWE[02] 'a' (0x61) → 拆分:(3,0,1) → 编码:(1,1,0) → 密文:VWX[03] 'g' (0x67) → 拆分:(3,0,7) → 编码:(3,1,4) → 密文:DWU... (省略中间输出)加密结果: DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ目标密文: DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ匹配结果: True
```



```
# 第一个'a': xor_3=0, xor_2=0# 加密后: VWX# 更新: xor_3=0# 第二个'a': xor_3=0, xor_2=1 (注意xor_2已经变化)# 加密后: VGX (与第一个不同!)
```



```
明文字节 → [位拆分] → [异或编码] → [查表] → 密文
```



```
密文 → [反查表] → [异或解码] → [位组合] → 明文字节
```



```
如果: c = a ^ b那么: a = c ^ b (异或同一个值可以恢复原值)证明: c ^ b = (a ^ b) ^ b = a ^ (b ^ b) = a ^ 0 = a
```



```
#!/usr/bin/env python3# -*- coding: utf-8 -*-TABLE3 ="XVEDULJT"TABLE2 ="GWMQ"# 目标密文(从程序中提取)AIM ="DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ"print(f"密文长度:{len(AIM)}")print(f"应解密出:{len(AIM) //3}个字符n")result =""xor_3 =0# 异或累积值,初始为0xor_2 =0foriinrange(len(AIM) //3): # 步骤1: 提取3个密文字符 cipher_char_0 = AIM[i *3+0] # 对应高3位 cipher_char_1 = AIM[i *3+1] # 对应中2位 cipher_char_2 = AIM[i *3+2] # 对应低3位 # 步骤2: 反查表(得到加密时的编码值) encrypted_high_3 = TABLE3.index(cipher_char_0) encrypted_mid_2 = TABLE2.index(cipher_char_1) encrypted_low_3 = TABLE3.index(cipher_char_2) # 步骤3: 异或解码(恢复原始位值) # 因为加密时: encrypted_value = original_value ^ xor_prev # 所以解密时: original_value = encrypted_value ^ xor_prev high_3 = encrypted_high_3 ^ xor_3 mid_2 = encrypted_mid_2 ^ xor_2 low_3 = encrypted_low_3 ^ encrypted_high_3 # 注意:用encrypted_high_3 # 步骤4: 更新异或值(必须与加密时完全相同!) xor_3 = encrypted_high_3 xor_2 = encrypted_mid_2 xor_3 = encrypted_low_3 # 再次更新 # 步骤5: 位组合(将3-2-3位重新拼成8位字节) # # 目标格式: 0b HHHMM LLL # ↑ ↑ ↑ # 高3 中2 低3 # original_byte = ((high_3 <<5) &0b11100000) | ((mid_2 <<3) &0b00011000) | (low_3 &0b00000111) result += chr(original_byte) # 调试输出 print(f"[{i:02d}] 密文:{cipher_char_0}{cipher_char_1}{cipher_char_2}→ " f"查表:({encrypted_high_3},{encrypted_mid_2},{encrypted_low_3}) → " f"解码:({high_3},{mid_2},{low_3}) → " f"字节:0x{original_byte:02x}→ 字符:'{chr(original_byte)}'")print(f"n{'='*60}")print(f"解密结果:{result}")print(f"{'='*60}")print(f"nFlag:{result.strip()}")
```



```
$ python3 decrypt.py
```



```
密文长度: 114应解密出: 38 个字符[00] 密文:DGL → 查表:(3,0,5) → 解码:(3,0,6) → 字节:0x66 → 字符:'f'[01] 密文:JWE → 查表:(6,1,2) → 解码:(3,1,4) → 字节:0x6c → 字符:'l'[02] 密文:VWX → 查表:(1,1,0) → 解码:(3,0,1) → 字节:0x61 → 字符:'a'[03] 密文:DWU → 查表:(3,1,4) → 解码:(3,0,7) → 字节:0x67 → 字符:'g'[04] 密文:TMU → 查表:(7,2,4) → 解码:(3,3,3) → 字节:0x7b → 字符:'{'[05] 密文:JGL → 查表:(6,0,5) → 解码:(2,2,3) → 字节:0x53 → 字符:'S'[06] 密文:JWT → 查表:(6,1,7) → 解码:(3,1,1) → 字节:0x69 → 字符:'i'[07] 密文:UWD → 查表:(4,1,3) → 解码:(3,0,7) → 字节:0x67 → 字符:'g'[08] 密文:EWE → 查表:(2,1,2) → 解码:(1,0,0) → 字节:0x20 → 字符:' '[09] 密文:XGL → 查表:(0,0,5) → 解码:(2,1,5) → 字节:0x4d → 字符:'M'[10] 密文:JGT → 查表:(6,0,7) → 解码:(3,0,1) → 字节:0x61 → 字符:'a'[11] 密文:UGT → 查表:(4,0,7) → 解码:(3,0,3) → 字节:0x63 → 字符:'c'[12] 密文:UWU → 查表:(4,1,4) → 解码:(3,1,0) → 字节:0x68 → 字符:'h'[13] 密文:TGJ → 查表:(7,0,6) → 解码:(3,1,1) → 字节:0x69 → 字符:'i'[14] 密文:LWD → 查表:(5,1,3) → 解码:(3,1,6) → 字节:0x6e → 字符:'n'[15] 密文:XWL → 查表:(0,1,5) → 解码:(3,0,5) → 字节:0x65 → 字符:'e'[16] 密文:UWU → 查表:(4,1,4) → 解码:(1,0,0) → 字节:0x20 → 字符:' '[17] 密文:JQL → 查表:(6,3,5) → 解码:(2,2,3) → 字节:0x53 → 字符:'S'[18] 密文:UWU → 查表:(4,1,4) → 解码:(1,2,0) → 字节:0x30 → 字符:'0'[19] 密文:LWL → 查表:(5,1,5) → 解码:(1,0,0) → 字节:0x20 → 字符:' '[20] 密文:TWE → 查表:(7,1,2) → 解码:(2,0,5) → 字节:0x45 → 字符:'E'[21] 密文:DQT → 查表:(3,3,7) → 解码:(1,2,4) → 字节:0x34 → 字符:'4'[22] 密文:UWT → 查表:(4,1,7) → 解码:(3,2,3) → 字节:0x73 → 字符:'s'[23] 密文:UML → 查表:(4,2,5) → 解码:(3,3,1) → 字节:0x79 → 字符:'y'[24] 密文:UMU → 查表:(4,2,4) → 解码:(1,0,0) → 字节:0x20 → 字符:' '[25] 密文:TMV → 查表:(7,2,1) → 解码:(3,0,6) → 字节:0x66 → 字符:'f'[26] 密文:EQL → 查表:(2,3,5) → 解码:(3,1,7) → 字节:0x6f → 字符:'o'[27] 密文:JWU → 查表:(6,1,4) → 解码:(3,2,2) → 字节:0x72 → 字符:'r'[28] 密文:LWL → 查表:(5,1,5) → 解码:(1,0,0) → 字节:0x20 → 字符:' '[29] 密文:TMJ → 查表:(7,2,6) → 解码:(2,3,1) → 字节:0x59 → 字符:'Y'[30] 密文:TGT → 查表:(7,0,7) → 解码:(1,2,0) → 字节:0x30 → 字符:'0'[31] 密文:LMX → 查表:(5,2,0) → 解码:(2,2,5) → 字节:0x55 → 字符:'U'[32] 密文:VMV → 查表:(1,2,1) → 解码:(1,0,0) → 字节:0x20 → 字符:' '[33] 密文:XGE → 查表:(0,0,2) → 解码:(1,2,2) → 字节:0x32 → 字符:'2'[34] 密文:DMX → 查表:(3,2,0) → 解码:(1,2,3) → 字节:0x33 → 字符:'3'[35] 密文:VGE → 查表:(1,0,2) → 解码:(1,2,3) → 字节:0x33 → 字符:'3'[36] 密文:VQU → 查表:(1,3,4) → 解码:(3,3,5) → 字节:0x7d → 字符:'}'[37] 密文:UMJ → 查表:(4,2,6) → 解码:(0,1,2) → 字节:0x0a → 字符:''============================================================解密结果: flag{Sig Machine S0 E4sy for Y0U 233}============================================================Flag: flag{Sig Machine S0 E4sy for Y0U 233}
```



```
$echo"flag{Sig Machine S0 E4sy for Y0U 233}"| ./sigmachinepassword: right!
```



```
voidcheck_password(char*input){ if(strlen(input) !=38) { printf("wrong!n"); return; } if(encrypt(input) == target) { printf("right!n"); }else{ printf("wrong!n"); }}
```



```
voidcheck_password(char*input){ intstate =0; // 状态变量 while(1) { switch(state) { case0: // 初始状态 if(strlen(input) !=38) { state =1; // 跳转到错误处理 }else{ state =2; // 跳转到加密验证 } break; case1: // 错误处理 printf("wrong!n"); state =99; // 跳转到退出 break; case2: // 加密验证 if(encrypt(input) == target) { state =3; // 跳转到成功 }else{ state =1; // 跳转到错误 } break; case3: // 成功处理 printf("right!n"); state =99; break; case99: // 退出 return; } }}
```



```
1. 文件分析 ↓2. 字符串提取 ↓3. Constructor识别 ↓4. 信号处理分析 ↓5. 数据段提取 ↓6. 算法逆向 ↓7. 脚本编写 ↓8. Flag验证
```



```
$ objdump -d sigmachine | grep"call.*signal"| wc -l11
```



```
$ readelf -x .init_array sigmachine | grep -c"00000000"7
```



```
importstringwithopen('sigmachine','rb')asf: content = f.read() printable = set(string.printable) # 分析字符分布...
```



```
$ strace -e signal,rt_sigaction ./sigmachine 2>&1 | grep rt_sigactionrt_sigaction(SIGINT, {...}, NULL, 8) = 0rt_sigaction(SIGQUIT, {...}, NULL, 8) = 0... (共11个)
```



```
#include<signal.h>#include<stdio.h>void(*orig_handler)(int);void(*my_signal(intsignum,void(*handler)(int)))(int) { printf("[HOOK] Registering signal %dn", signum); // 调用原始signal函数...}
```



```
importangr# 加载二进制文件proj = angr.Project('./sigmachine', auto_load_libs=False)# 创建符号输入flag = proj.loader.main_object.get_symbol('flag_buffer')state = proj.factory.entry_state(stdin=angr.SimPacket('flag'))# 设置约束state.solver.add(state.regs.rax ==0x47c09a) # "right!"地址# 符号执行simgr = proj.factory.simulation_manager(state)simgr.explore(find=0x47c09a)# 输出结果ifsimgr.found: print(simgr.found[0].posix.dumps(0))
```



```
#!/usr/bin/env python3"""SigMachine加密算法实现与验证用于验证我们对加密算法的理解"""TABLE3 ="XVEDULJT"TABLE2 ="GWMQ"defencrypt(plaintext): """ 实现3-2-3位拆分加密算法 参数: plaintext: 明文字符串 返回: 加密后的密文字符串 """ result ="" xor_3 =0 xor_2 =0 forcharinplaintext: byte_val = ord(char) # 位拆分 high_3 = (byte_val >>5) &0b111 mid_2 = (byte_val >>3) &0b11 low_3 = byte_val &0b111 # 异或编码 enc_high = high_3 ^ xor_3 enc_mid = mid_2 ^ xor_2 enc_low = low_3 ^ enc_high # 查表替换 result += TABLE3[enc_high] + TABLE2[enc_mid] + TABLE3[enc_low] # 更新异或值 xor_3 = enc_high xor_2 = enc_mid xor_3 = enc_low returnresultif__name__ =="__main__": # 测试 plaintext ="flag{Sig Machine S0 E4sy for Y0U 233}n" encrypted = encrypt(plaintext) target ="DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ" print(f"明文:{plaintext}") print(f"密文:{encrypted}") print(f"目标:{target}") print(f"匹配:{encrypted == target}")
```



```
#!/usr/bin/env python3"""SigMachine解密脚本从密文恢复明文flag"""TABLE3 ="XVEDULJT"TABLE2 ="GWMQ"CIPHERTEXT ="DGLJWEVWXDWUTMUJGLJWTUWDEWEXGLJGTUGTUWUTGJLWDXWLUWUJQLUWULWLTWEDQTUWTUMLUMUTMVEQLJWULWLTMJTGTLMXVMVXGEDMXVGEVQUUMJ"defdecrypt(ciphertext): """ 解密函数 参数: ciphertext: 密文字符串(长度必须是3的倍数) 返回: 解密后的明文字符串 """ iflen(ciphertext) %3!=0: raiseValueError("密文长度必须是3的倍数") result ="" xor_3 =0 xor_2 =0 foriinrange(len(ciphertext) //3): # 提取3个密文字符 cipher_char_0 = ciphertext[i *3+0] cipher_char_1 = ciphertext[i *3+1] cipher_char_2 = ciphertext[i *3+2] # 反查表 encrypted_high_3 = TABLE3.index(cipher_char_0) encrypted_mid_2 = TABLE2.index(cipher_char_1) encrypted_low_3 = TABLE3.index(cipher_char_2) # 异或解码 high_3 = encrypted_high_3 ^ xor_3 mid_2 = encrypted_mid_2 ^ xor_2 low_3 = encrypted_low_3 ^ encrypted_high_3 # 更新异或值 xor_3 = encrypted_high_3 xor_2 = encrypted_mid_2 xor_3 = encrypted_low_3 # 位组合 original_byte = ((high_3 <<5) &0b11100000) | ((mid_2 <<3) &0b00011000) | (low_3 &0b00000111) result += chr(original_byte) returnresultif__name__ =="__main__": print("SigMachine解密工具") print("="*60) print(f"密文长度:{len(CIPHERTEXT)}") print(f"明文长度:{len(CIPHERTEXT) //3}") print("="*60) plaintext = decrypt(CIPHERTEXT) print(f"n解密结果:n{plaintext}") print(f"nFlag:{plaintext.strip()}")
```



```
#!/usr/bin/env python3"""批量测试加密/解密的正确性"""fromencryptimportencryptfromdecryptimportdecrypttest_cases = [ "flag{test}", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789", "Hello, World!n", "The quick brown fox jumps over the lazy dog",]print("批量测试加密/解密算法")print("="*70)fori, plaintextinenumerate(test_cases,1): print(f"n测试用例{i}:") print(f"原文:{repr(plaintext)}") # 加密 ciphertext = encrypt(plaintext) print(f"密文:{ciphertext}") # 解密 recovered = decrypt(ciphertext) print(f"解密:{repr(recovered)}") # 验证 match = plaintext == recovered print(f"匹配:{'✓ 成功'ifmatchelse'✗ 失败'}") ifnotmatch: print(f"错误: 原文与解密结果不匹配!") breakprint("n"+"="*70)print("所有测试完成!")
```



```
# ===== 文件分析 =====file <binary> # 识别文件类型strings <binary> # 提取字符串strings -tx <binary> # 显示字符串地址# ===== ELF分析 =====readelf -h <binary> # 查看ELF头readelf -S <binary> # 查看段表readelf -x .rodata <binary> # 查看rodata段readelf -x .init_array <binary> # 查看constructor# ===== 反汇编 =====objdump -d <binary> # 反汇编全部代码objdump -d -M intel <binary> # Intel语法objdump -s -j .rodata <binary> # 查看rodata数据# ===== 动态调试 =====gdb <binary> # 启动GDBstrace <binary> # 追踪系统调用ltrace <binary> # 追踪库函数调用# ===== 运行测试 =====echo"test"| ./<binary> # 管道输入./<binary> <<<"test" # Here字符串python -c"print('test')"| ./<binary> # Python生成输入# ===== 数据提取 =====xxd <binary> | grep"pattern" # 十六进制查看hexdump -C <binary> # 十六进制+ASCIIrabin2 -z <binary> # radare2提取字符串
```
