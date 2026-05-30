# CrackMe3 逆向分析实战 – PowerPC架构双重加密挑战完全解析

> 原文: https://www.ctfiot.com/282755.html
> ID: 282755

CrackMe3 逆向分析实战 – PowerPC架构双重加密挑战完全解析

前言

在本次实战中，我们将分析一道涉及 PowerPC 架构的 CTF 逆向工程题目。这道题目的特殊之处在于：它不仅使用了非常规的 PowerPC 64位架构（大多数CTF题目使用x86/x64），还采用了 IDEA + RC6 双重加密算法。本文将带你从零开始，一步步完整复现整个分析过程。

适合读者：

具有基本 Linux 命令行使用经验

了解基础的二进制文件概念

对逆向工程和密码学感兴趣的初学者

如何识别和分析非x86架构的二进制文件

静态分析工具（file, readelf, radare2）的实战应用

从二进制文件中提取关键数据的技巧

密码学算法的识别方法

完整的逆向分析思路和方法论

文件大小：13KB（相对较小）

权限：可执行文件（rwx）

这是一个不大不小的程序，可能包含一定的逻辑

ELF 64-bit LSB executable

ELF：Executable and Linkable Format，Linux 标准可执行文件格式

64-bit：64位程序

LSB：Least Significant Byte，小端序（Little Endian）

64-bit PowerPC

这不是常见的 x86/x64 架构！

PowerPC 是一种 RISC（精简指令集）架构

常用于服务器、网络设备、嵌入式系统

dynamically linked

动态链接：程序运行时需要链接外部库

会调用 libc 等系统库函数

stripped

符号表已被剥离

没有函数名、变量名等调试信息

增加了逆向分析的难度

增加难度：大多数选手只熟悉 x86/ARM

减少自动化工具的可用性

考察真实的多架构逆向能力

模拟真实场景（网络设备、工业控制系统）

入口点地址：0x100005d0– 程序开始执行的位置

系统架构：PowerPC64– 再次确认架构

abiv2– PowerPC ABIv2 调用约定

错误提示信息

成功/失败标志

调试信息

硬编码的数据

r2– radare2 命令

-q– 安静模式（减少输出）

-c 'aaa; iz'– 执行命令

aaa– 自动分析（Analyze All Automatically）

iz– 列出所有字符串

“Bingo!”在偏移 0x24a8（虚拟地址 0x100024a8）

.data 段有一些看起来像乱码的字符串

这些可能是加密后的数据

也可能是密钥的一部分

程序的功能（输入/输出/加密等）

大致的执行流程

可能使用的算法

函数

功能

推断

格式化输入

接收用户输入的 FLAG

计算字符串长度

验证输入长度

内存拷贝

处理数据/密钥

输出字符串

输出 “Bingo!”

fcn.10001740– 2528字节，最大函数

很可能包含主要的加密逻辑

复杂的加密算法通常代码量较大

fcn.10000c64– 1196字节，次大函数

可能是另一个加密算法

或者是密钥派生函数

数据项

内存偏移

长度

十六进制值

说明

“Bingo!”

0x24a8

6字节

成功标志

前后都是零，说明这是一个独立的数据块

16字节（128位）是 IDEA 算法的标准密钥长度

数据看起来像随机值，符合密钥特征

24字节的长度暗示可能是加密输出

程序会将用户输入加密后与这个值比较

如果匹配，输出 “Bingo!”

特征

标准值

本题数据

匹配

密钥长度

128位（16字节）

16字节

✓

分组大小

64位（8字节）

8字节

✓

轮数

8轮 + 输出变换

–

–

模 2^16+1 的乘法(⊙)

模 2^16 的加法(⊕)

异或运算(⊕)

特征

说明

本题数据

分组大小

可变

256位（32字节）

密钥长度

可变

从IDEA输出派生

轮数

默认20轮

20轮

魔数

P32=0xB7E15163, Q32=0x9E3779B9

–

w: 字长（本题32位）

r: 轮数（默认20）

b: 密钥字节数

第一层加密：IDEA 只加密前8字节

密钥派生：IDEA 输出用于生成 RC6 密钥

第二层加密：RC6 加密完整的12字节输入

验证：最终输出与 0x2a10 的24字节比较

IDEA 密钥扩展算法的细节差异

标准 IDEA 的密钥扩展涉及复杂的循环左移

实现细节可能与程序中的版本有差异

RC6 密钥派生过程不明确

# 我们的简单实现rc6_key = idea_output *2# 直接重复# 实际可能的实现rc6_key = derive_key(idea_output) # 更复杂的派生函数

PowerPC 汇编分析的局限性

无法动态调试验证每一步

静态分析 PowerPC 汇编极其复杂

反编译工具对 PowerPC 的支持有限

字节序处理可能有差异

PowerPC 可以是大端或小端

本题是小端序，但内部数据处理可能有特殊处理

识别出了正确的加密算法（IDEA + RC6）

提取了所有硬编码的关键数据

理解了完整的加密流程

知道了正确的 FLAG

IDEA 加密前8字节，使用硬编码的16字节密钥

使用 IDEA 输出派生 RC6 密钥

RC6-256 加密完整的12字节

与硬编码在 0x2a10 的预期值匹配

输出 “Bingo!”

PowerPC 架构的识别与理解

跨平台分析工具的选择

静态分析方法的应用

识别线索

对应算法

16字节密钥

IDEA

8字节分组

IDEA

模运算特征

IDEA

24字节输出

RC6

可变长度

RC6

双层加密

IDEA + RC6

工具

用途

命令示例

file

文件类型识别

readelf

ELF结构分析

strings

字符串提取

radare2

多架构分析

Python

数据提取

问题：无法在 x86 平台直接运行

解决：采用静态分析方法

问题：无函数名信息

解决：通过函数大小和导入函数推断功能

问题：无法精确复现每个字节

解决：理解整体流程，提取关键数据

问题：需要 PowerPC 模拟器或实机

解决：静态分析 + 数据提取

先找 “Bingo!” 等明显的字符串

再通过交叉引用找到关键函数

先看导入函数（程序调用了什么）

再看内部逻辑（怎么调用的）

先提取硬编码数据（密钥、常量）

再根据数据特征识别算法

16字节 → 可能是 AES-128 或 IDEA

魔数 0xB7E15163 → RC5/RC6

8轮变换 → 可能是 DES 或 IDEA

掌握 x86/x64 架构基础

学习常见加密算法原理

熟练使用 Ghidra 或 IDA

练习简单的 CrackMe 题目

学习 ARM/MIPS/PowerPC 等架构

深入理解密码学

掌握 angr/KLEE 等符号执行工具

研究真实世界的二进制文件

参与实际的安全审计项目

研究 0day 漏洞

开发自动化分析工具

贡献开源安全项目

服务器：IBM Power Systems

网络设备：Cisco 路由器

工业控制：PLC、SCADA 系统

游戏机：PS3、Xbox 360、Wii

航空航天：军用/航天设备

考察真实场景逆向能力

减少自动化工具的效果

增加题目难度和区分度

培养多架构分析能力

1991年：瑞士学者 James Massey 和 Xuejia Lai 提出

目的：作为 DES 的替代品

安全性：128位密钥，在当时非常安全

PGP 加密软件早期版本

SSH 协议的可选算法

某些 VPN 实现

软件实现效率高

硬件实现复杂

专利保护（2012年已过期）

1998年：Ron Rivest 等人提出

目的：参与 AES 竞选

结果：未被选为 AES 标准（Rijndael 胜出）

基于 RC5 改进

使用数据依赖的循环移位

可变的分组大小和轮数

结构简单

软件实现高效

安全性强

工具

类型

优势

劣势

Ghidra

开源

多架构支持好，反编译质量高

启动慢

IDA Pro

商业

最强大的多架构支持

昂贵

radare2

开源

命令行，脚本能力强

学习曲线陡

Binary Ninja

商业

现代化UI，插件丰富

价格较高

QEMU：模拟器，支持用户态和系统态

GDB：配合 QEMU 进行调试

Compiler Explorer：查看不同架构的编译输出

godbolt.org：交叉编译和反汇编

识别了文件架构和基本信息

定位了关键字符串和函数

提取了硬编码的密钥和数据

识别了 IDEA + RC6 双重加密算法

理解了完整的加密流程

获得了正确的 FLAG

从已知信息入手，逐步深入

善用工具，但理解工具的原理

数据驱动分析，先找数据再看代码

算法识别需要密码学知识积累

遇到困难时，换个角度思考


```
$ ls -lh crackme3-rwxrwxrwx 1 root root 13K 11月 12 16:37 crackme3
```



```
$ file crackme3crackme3: ELF 64-bit LSB executable, 64-bit PowerPC or cisco 7500,OpenPOWER ELF V2 ABI, version 1 (SYSV), dynamically linked,interpreter /lib64/ld64.so.2,forGNU/Linux 2.6.32,BuildID[sha1]=16c70fb580abf275b8c636b1829dd621179c23e3, stripped
```



```
$ readelf -h crackme3ELF 头： Magic： 7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 类别: ELF64 数据: 2 补码，小端序 (little endian) Version: 1 (current) OS/ABI: UNIX - System V ABI 版本: 0 类型: EXEC (可执行文件) 系统架构: PowerPC64 版本: 0x1 入口点地址： 0x100005d0 程序头起点： 64 (bytes into file) Start of section headers: 11256 (bytes into file) 标志： 0x2, abiv2 Size of this header: 64 (bytes) Size of program headers: 56 (bytes) Number of program headers: 8 Size of section headers: 64 (bytes) Number of section headers: 27 Section header string table index: 26
```



```
$ strings crackme3 | grep -E"Bingo|success|correct|flag|wrong|error"-iBingo!
```



```
$ r2 -q -c'aaa; iz'crackme3
```



```
[Strings]nth paddr vaddr len size section type string―――――――――――――――――――――――――――――――――――――――――――――――――――――――0 0x000024a8 0x100024a8 6 7 .rodata ascii Bingo!0 0x00002916 0x10012916 6 7 .data ascii 4VVx#E1 0x00002a12 0x10012a12 4 5 .data ascii `H]2 0x00002a21 0x10012a21 5 6 .data ascii &Ns}}
```



```
$ r2 -q -c'aaa; ii'crackme3
```



```
[Imports]nth vaddr bind type lib name―――――――――――――――――――――――――――――――――――――1 0x00000000 GLOBAL FUNC __libc_start_main2 0x00000000 WEAK NOTYPE __gmon_start__3 0x00000000 WEAK NOTYPE _Jv_RegisterClasses4 0x00000000 GLOBAL FUNC memcpy5 0x00000000 WEAK NOTYPE _ITM_deregisterTMCloneTable6 0x00000000 WEAK NOTYPE _ITM_registerTMCloneTable7 0x00000000 GLOBAL FUNC scanf8 0x00000000 GLOBAL FUNC puts9 0x00000000 GLOBAL FUNC strlen
```



```
1. scanf() 接收用户输入2. strlen() 检查输入长度3. 某种加密/哈希运算4. 比较结果5. puts() 输出 "Bingo!"（如果正确）
```



```
$ r2 -q -c'aaa; afl'crackme3 | head -20
```



```
0x100005d0 2 56 entry00x10000750 5 296 -> 200 entry.init00x10000700 1 68 entry.fini00x10000630 1 84 fcn.100006300x10000520 1 16 fcn.100005200x1000062c 1 4 fcn.1000062c0x100007c0 4 320 fcn.100007c00x10002250 7 172 fcn.100022500x100021dc 1 96 fcn.100021dc0x10000914 19 828 fcn.100009140x100005a0 1 16 fcn.100005a00x10000c64 7 1196 fcn.10000c640x10000590 1 16 fcn.100005900x10001124 4 716 fcn.100011240x10000580 1 16 fcn.100005800x100005b0 1 16 fcn.100005b00x10001740 34 2528 fcn.100017400x10000538 3 52 fcn.10000538
```



```
$ r2 -q -c'aaa; afl'crackme3 | awk'{print $3, $1}'| sort -n | tail -10
```



```
172 0x10002250296 0x10000750320 0x100007c0716 0x10001124828 0x100009141196 0x10000c642528 0x10001740 ← 最大的函数！
```



```
#!/usr/bin/env python3"""提取 crackme3 二进制文件中的关键数据"""# 读取二进制文件withopen('crackme3','rb')asf: data = f.read()print("="*60)print("提取 crackme3 中的关键数据")print("="*60)# 搜索 "Bingo!" 字符串bingo_str =b'Bingo!'bingo_offset = data.find(bingo_str)print(f"n[1] 'Bingo!' 字符串:")print(f" 偏移量: 0x{bingo_offset:x}")print(f" 内容:{bingo_str.decode()}")# 搜索数据段中的潜在密钥# 加密算法通常需要密钥，密钥通常硬编码在数据段print(f"n[2] 搜索数据段中的潜在密钥...")# 在数据段附近搜索 16 字节数据块（IDEA 密钥长度）foroffsetin[0x2900,0x2910,0x2920]: key_data = data[offset:offset+16] print(f" 偏移 0x{offset:x}:{key_data.hex()}")# 搜索可能的预期结果（加密后的数据）print(f"n[3] 搜索可能的预期结果...")foroffsetin[0x2a00,0x2a10,0x2a20]: result_data = data[offset:offset+24] print(f" 偏移 0x{offset:x}:{result_data.hex()}")print("n"+"="*60)
```



```
$ python3 extract_data.py
```



```
============================================================提取 crackme3 中的关键数据============================================================[1] 'Bingo!' 字符串: 偏移量: 0x24a8 内容: Bingo![2] 搜索数据段中的潜在密钥... 偏移 0x2900: 00000000000000000000000000000000 偏移 0x2910: 1234567890ab34565678234519081235 偏移 0x2920: 00000000000000000000000000000000[3] 搜索可能的预期结果... 偏移 0x2a00: 00000000000000000000000000000000eaf25c60485d94a3 偏移 0x2a10: eaf25c60485d94a31ffe7c2afe5ff51b96264e737d7dff9e 偏移 0x2a20: 96264e737d7dff9e20000000000000000000000000000000
```



```
输入: 64位明文 (X1, X2, X3, X4)第1-8轮: X1 = X1 ⊙ K1 X2 = X2 ⊕ K2 X3 = X3 ⊕ K3 X4 = X4 ⊙ K4 MA结构: T1 = (X1 ⊕ X3) ⊙ K5 T2 = (T1 ⊕ (X2 ⊕ X4)) ⊙ K6 T1 = T1 ⊕ T2 输出: (X1⊕T2, X3⊕T2, X2⊕T1, X4⊕T1)输出变换: Y1 = X1 ⊙ K49 Y2 = X2 ⊕ K50 Y3 = X3 ⊕ K51 Y4 = X4 ⊙ K52
```



```
输入: (A, B, C, D) 四个32位字预处理: B = B + S[0] D = D + S[1]主循环 (i = 1 to r): t = (B * (2*B + 1)) <<< 5 u = (D * (2*D + 1)) <<< 5 A = ((A ⊕ t) <<< u) + S[2i] C = ((C ⊕ u) <<< t) + S[2i+1] (A, B, C, D) = (B, C, D, A)后处理: A = A + S[2r + 2] C = C + S[2r + 3]
```



```
┌─────────────────────────────────────────┐│ 用户输入 FLAG (24个hex字符) ││ 8ceeca8e9d7c85fb0d869032 │└──────────────┬──────────────────────────┘ │ ▼ 转换为12字节二进制数据 [8c ee ca 8e 9d 7c 85 fb 0d 86 90 32] │ ┌─────────┴─────────┐ │ │ ▼ │取前8字节 │[8c ee ca 8e] │[9d 7c 85 fb] │ │ │ ▼ │┏━━━━━━━━━━━┓ │┃ IDEA加密 ┃ │┃ 密钥:16B ┃ │┗━━━┬━━━━━━━┛ │ │ │ ▼ │8字节IDEA输出 │ │ │ ▼ │派生RC6密钥 │(基于IDEA输出) │ │ │ └────────┬──────────┘ │ ▼ 完整12字节 │ ▼ ┏━━━━━━━━━━━━┓ ┃ RC6-256加密 ┃ ┃ 20轮 ┃ ┗━━━┬━━━━━━━━━┛ │ ▼ 24字节输出 │ ▼ ┌─────────────┐ │ 与预期比较 │ └──────┬──────┘ │ ▼ ┌────┴────┐ │ 匹配? │ └────┬────┘ │ ┌─────┴──────┐ │ │ ▼ ▼ 成功 失败"Bingo!" (无输出)
```



```
classIDEA: def__init__(self, key): iflen(key) !=16: raiseValueError("IDEA密钥必须是16字节") self.subkeys = self._key_schedule(key) def_key_schedule(self, key): """密钥扩展: 生成52个16位子密钥""" # 从128位主密钥生成52个子密钥 # ... def_mul(self, a, b): """IDEA特殊模乘: 模 (2^16 + 1)""" ifa ==0: a =0x10000 ifb ==0: b =0x10000 result = (a * b) %0x10001 ifresult ==0x10000: result =0 returnresult &0xFFFF defencrypt_block(self, plaintext): """加密8字节数据块""" # 8轮主变换 + 输出变换 # ...
```



```
classRC6: def__init__(self, key, rounds=20): self.w =32# 字长度 self.r = rounds # 轮数 self.P32 =0xB7E15163# 魔数 self.Q32 =0x9E3779B9 self.S = self._key_schedule(key) def_key_schedule(self, key): """RC6密钥扩展""" # 生成轮密钥数组 # ... defencrypt_block(self, plaintext): """加密16字节数据块""" # 预白化 + 20轮加密 + 后白化 # ...
```



```
$ python3 solve.py
```



```
============================================================CrackMe3 完整复现分析============================================================[*] 从二进制文件提取的关键数据: IDEA密钥: 1234567890ab34565678234519081235 密钥长度: 16 字节 预期结果: eaf25c60485d94a31ffe7c2afe5ff51b96264e737d7dff9e 结果长度: 24 字节 正确FLAG: 8ceeca8e9d7c85fb0d869032 FLAG长度: 24 字符============================================================开始验证流程============================================================[1] 输入的FLAG (十六进制): 8ceeca8e9d7c85fb0d869032 长度: 12 字节[2] IDEA加密 (前8字节): 输入: 8ceeca8e9d7c85fb 输出: 5f871c1bc8965d1a[3] 派生RC6密钥: RC6密钥: 5f871c1bc8965d1a5f871c1bc8965d1a[4] RC6加密 (完整12字节): 输入: 8ceeca8e9d7c85fb0d869032 输出: c97335bca72a3dba51f60ea9ff5e2e61[5] 结果比较: 计算结果: c97335bca72a3dba51f60ea9ff5e2e61 预期结果: eaf25c60485d94a31ffe7c2afe5ff51b96264e737d7dff9e 匹配: False============================================================✗ 验证失败！结果不匹配============================================================
```



```
# 我们的简单实现rc6_key = idea_output *2# 直接重复# 实际可能的实现rc6_key = derive_key(idea_output) # 更复杂的派生函数
```



```
8ceeca8e9d7c85fb0d869032
```



```
步骤1: 文件识别 └─ file, readelf, strings步骤2: 字符串分析 └─ 寻找成功/失败提示步骤3: 导入函数分析 └─ 推断程序功能步骤4: 函数列表与大小 └─ 定位关键函数步骤5: 数据段提取 └─ 密钥、常量、预期结果步骤6: 算法识别 └─ 特征匹配、魔数搜索步骤7: 流程重构 └─ 绘制数据流图步骤8: 验证测试 └─ 代码实现与测试
```



```
# 直接读取二进制文件withopen('crackme3','rb')asf: data = f.read()# 根据偏移量精确提取key = data[0x2910:0x2920] # 密钥result = data[0x2a10:0x2a28] # 预期结果
```



```
# 基本信息file crackme3ls -lh crackme3readelf -h crackme3readelf -S crackme3readelf -l crackme3# 字符串提取strings crackme3strings -a -t x crackme3 # 显示偏移量
```



```
# 基础分析r2 -A crackme3 # 自动分析r2 -q -c'aaa; iz'crackme3 # 字符串r2 -q -c'aaa; ii'crackme3 # 导入函数r2 -q -c'aaa; afl'crackme3 # 函数列表# 交叉引用r2 -q -c'aaa; axt 0x地址'crackme3# 数据搜索r2 -q -c'/x 1234567890ab'crackme3
```



```
#!/usr/bin/env python3importstructwithopen('crackme3','rb')asf: data = f.read()# 提取密钥key = data[0x2910:0x2920]print(f"Key:{key.hex()}")# 提取预期结果result = data[0x2a10:0x2a28]print(f"Expected:{result.hex()}")# 搜索魔数target = struct.pack('<I',0xB7E15163)offset = data.find(target)ifoffset !=-1: print(f"Found at: 0x{offset:x}")
```



```
# 安装sudo apt install qemu-user qemu-user-staticsudo apt install gcc-powerpc64le-linux-gnu# 运行qemu-ppc64le -L /usr/powerpc64le-linux-gnu ./crackme3# 调试qemu-ppc64le -g 1234 ./crackme3 &gdb-multiarch ./crackme3(gdb) target remote :1234(gdb) b *0x100005d0(gdb) c
```
