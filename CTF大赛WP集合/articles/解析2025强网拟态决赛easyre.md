# 解析2025强网拟态决赛easyre

> 原文: https://www.ctfiot.com/286199.html
> ID: 286199

Signal异常处理与TEA加密算法的逆向分析实战

前言

本文将详细分析一道综合性逆向工程题目，该题目巧妙地将Signal异常处理机制与TEA加密算法结合，展现了现代恶意软件中常见的反分析技巧。通过本文的学习，读者将掌握如何识别和分析基于异常处理的控制流混淆，以及如何识别和破解TEA加密算法。

题目初步分析

文件基本信息

首先对题目文件进行基本信息识别：

file main.exe

输出结果：

main.exe: PE32+ executable (console) x86-64 (stripped to external PDB), for MS Windows, 10 sections

这是一个64位Windows可执行文件，已剥离调试符号，增加了分析难度。

字符串信息分析

使用radare2提取程序中的字符串信息：

r2 -q -c"aaa; iz"main.exe

从输出中可以提取到以下关键字符串：

“Input flag: ” – 程序会要求用户输入

“Wrong flag! Try again.” – 输入错误的提示

“Success! You got the flag.” – 输入正确的提示

“Wrong length! Hint: 32 chars.” – 提示flag长度为32个字符

SIGSEGV (信号值11) – 访问违例，通常由非法内存访问引起

SIGILL – 非法指令

SIGFPE – 浮点异常

SIGINT – 中断信号（如Ctrl+C）

注册异常处理函数：使用signal(SIGSEGV, handler)注册SIGSEGV信号的处理函数

设置恢复点：调用setjmp保存当前的执行上下文

触发异常：通过mov dword [0], eax向地址0写入，必然触发访问违例

异常处理：操作系统捕获异常后，调用注册的处理函数

恢复执行：处理函数通过longjmp跳转回setjmp保存的位置继续执行

控制流混淆：正常的控制流被异常处理打断，静态分析工具难以跟踪执行路径

代码隐藏：关键逻辑隐藏在异常处理函数中，而不在主执行流中

反调试：未配置正确异常处理的调试器会认为程序崩溃，实际上程序正常运行

动态行为：只有在运行时才能观察到完整的执行流程

分组长度：64位（两个32位整数）

密钥长度：128位（四个32位整数）

轮数：32轮

结构：Feistel网络

代码量：极其简洁，适合嵌入式系统

delta = 0x9E3779B9（黄金分割比例 * 2^32）

解密时使用delta的补码：0x61C88647

sum初值 = delta * 32 = 0xC6EF3720

特征常量0x61C88647：这是TEA的delta值的补码

特征常量0xC6EF3720：delta * 32的值，用于32轮迭代

位运算模式：典型的”左移4位”、”右移5位”、”异或”组合

Feistel结构：两个32位变量交替运算

位移运算（扩散）

密钥混合（混淆）

累加运算（非线性）

XOR运算（可逆性）

sum的初始值：解密时从delta * 32开始，而不是从0开始

delta的选择：使用0x61C88647确保sum在32轮后正确递增回0

运算顺序：先处理v1，再处理v0（与加密顺序相反）

减法操作：使用减法代替加法（逆运算）

sum的变化方向：每轮加delta（与加密时减delta相反）

密钥：从异常处理函数中提取并计算

密文：从程序数据段提取

算法：标准TEA解密

小端序（Little-Endian）：低位字节存储在低地址，x86/x64架构使用

大端序（Big-Endian）：高位字节存储在低地址，网络字节序

‘f’ (ASCII 0x66) 在最低字节

‘l’ (ASCII 0x6C) 在次低字节

‘a’ (ASCII 0x61) 在次高字节

‘g’ (ASCII 0x67) 在最高字节

检查导入表，确认signal函数的导入

定位signal函数的调用位置

识别异常触发点（向地址0写入）

找到异常处理函数的地址

反汇编异常处理函数代码

识别密钥读取位置

理解密钥变换逻辑（XOR和SUB运算）

提取原始密钥数据

计算变换后的实际密钥

分析校验函数调用的加密函数

寻找特征常量（0x61C88647, 0xC6EF3720）

识别位运算模式（左移4、右移5、异或）

确认32轮迭代循环

确定为TEA加密算法

通过比较逻辑找到密文存储位置

使用工具提取密文数据

转换为适合编程语言处理的格式

实现标准TEA解密算法

注意sum和delta的初始值

注意运算顺序和方向

对8个32位整数（4组64位数据）进行解密

理解x86/x64的小端序存储方式

将十六进制转换为ASCII字符

对每4字节的字符串进行反转

拼接得到完整flag

0x9E3779B9– 原始delta值（加密时使用）

0x61C88647– delta的补码（解密时使用）

0xC6EF3720– delta * 32（解密时sum的初始值）

一个左移4位（shl x, 4）

一个右移5位（shr x, 5）

多个add指令

一个或多个xor指令

循环计数器初始化为32

或者sum从0累加到delta * 32

从低地址开始存储低位字节（小端序）

从低地址开始存储高位字节（大端序）

‘f’ = 0x66

‘l’ = 0x6C

‘a’ = 0x61

‘g’ = 0x67

IDA Pro– 功能最强大，支持多种架构

Ghidra– NSA开源，免费且功能强大

radare2– 命令行工具，适合自动化分析

Binary Ninja– 现代化UI，中间语言表示清晰

x64dbg– Windows平台最佳选择

GDB– Linux标准调试器

WinDbg– Windows内核级调试

LLDB– macOS和iOS调试

010 Editor– 十六进制编辑器，支持模板

CyberChef– 在线数据处理工具

Python– 编写自动化脚本

从main函数或入口点开始

识别主要功能模块

逐步深入细节

绘制控制流图

从字符串和导入函数入手

找到关键功能点

向上追踪调用链

理解整体逻辑

识别加密算法特征常量

识别标准库函数模式

识别反调试/反分析技巧

使用工具辅助识别

S-box常量（固定的256字节表）

10/12/14轮（取决于密钥长度）

MixColumns和SubBytes操作

Delta常量0x9E3779B9

32或64轮

简单的位运算组合

256字节的S盒

KSA（密钥调度算法）和PRGA（伪随机生成算法）

两个索引变量i和j

4个初始魔数：0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

64轮运算

特定的位运算函数F, G, H, I

5个初始常量

80轮运算

循环左移操作

8个初始哈希值

64轮运算

特定的常量表（64个32位常量）

Signal/SEH异常处理

VEH（Vectored Exception Handling）

故意触发异常并利用处理流程

GetTickCount() 检测运行时间

rdtsc 指令检测CPU周期

时间差异检测调试器存在

IsDebuggerPresent() API

PEB结构中的BeingDebugged标志

检测调试器特征进程/窗口

CRC/MD5校验自身代码

检测断点（INT3指令，0xCC）

检测代码段是否被修改

参加在线CTF平台（CTFtime, pwnable.kr）

练习各类reverse题目

学习官方WriteUp

与社区交流经验

阅读开源软件源码

对比源码和二进制

理解编译器优化

学习代码结构

编写IDA/Ghidra插件

开发自动化分析脚本

制作符号化工具

构建分析框架

关注安全研究博客

阅读学术论文

参与安全会议

跟踪最新漏洞

初步信息收集– 使用基本工具获取文件信息和字符串

控制流分析– 识别异常处理机制和执行流程

算法识别– 通过特征常量和代码模式识别TEA算法

数据提取– 提取密钥和密文数据

逆向实现– 编写解密程序

数据处理– 正确处理字节序问题

使用异常处理隐藏密钥变换逻辑，增加分析难度

选择TEA这种轻量级算法，代码简洁但具有一定强度

涉及字节序处理，考察对底层数据表示的理解

Signal异常处理机制的原理和识别方法

TEA加密算法的特征和解密实现

字节序问题的本质和处理方法

系统化的逆向分析思路

Wheeler, D. J., & Needham, R. M. (1994). TEA, a Tiny Encryption Algorithm

TEA, XTEA, and XXTEA加密算法的改进历史

Block Cipher Techniques（分组密码技术）

Windows SEH (Structured Exception Handling) Documentation

Signal Handling in POSIX Systems

Exception Handling in x86/x64 Architecture

Practical Malware Analysis（恶意软件分析实战）

Reversing: Secrets of Reverse Engineering（逆向工程权威指南）

The IDA Pro Book（IDA Pro权威指南）

CTFtime.org – CTF比赛信息和WriteUp

GitHub – 各类逆向工程工具和脚本

StackOverflow – 技术问题交流平台


```
file main.exe
```



```
main.exe: PE32+ executable (console) x86-64 (stripped to external PDB), for MS Windows, 10 sections
```



```
r2 -q -c"aaa; iz"main.exe
```



```
r2 -q -c"aaa; ii~signal"main.exe
```



```
32 0x140011390 NONE FUNC msvcrt.dll signal
```



```
r2 -q -c"aaa; axt 0x14000b082"main.exe
```



```
; 注册signal处理函数0x1400097be lea rdx, [0x140001720] ; 异常处理函数地址0x1400097c5 mov ecx, 0xb ; 信号值11 (SIGSEGV)0x1400097ca call signal ; 调用signal注册; 设置setjmp保存点0x1400097d2 lea rcx, [0x140010080]0x1400097d9 call _setjmp0x1400097de test eax, eax0x1400097e0 jne 0x1400097ed; 故意触发访问违例0x1400097e2 xor eax, eax0x1400097e4 mov dword [0], eax ; 向地址0写入，触发SIGSEGV0x1400097eb ud2 ; 未定义指令（备用触发方式）; 异常处理后返回点0x1400097ed lea rcx, [用户输入]0x1400097f1 call fcn.140001850 ; 调用校验函数
```



```
r2 -q -c"aaa; pd 100 @ 0x140001720"main.exe
```



```
; 从固定地址读取原始密钥0x140001724 mov eax, [0x14000a040] ; key[0] = 0x123456780x14000172a mov ecx, [0x14000a048] ; key[2] = 0xfedcba980x140001730 mov edx, [0x14000a04c] ; key[3] = 0x765432100x140001745 mov eax, [0x14000a044] ; key[1] = 0x9abcdef0; 对密钥进行变换0x140001736 xor eax, 0xdeadbeef ; key[0] ^= 0xdeadbeef0x14000173b sub ecx, 0x11223344 ; key[2] -= 0x112233440x14000174b xor edx, 0xccddeeff ; key[3] ^= 0xccddeeff0x140001765 sub eax, 0x789abcdf ; key[1] -= 0x789abcdf; 将变换后的密钥保存回内存0x14000177a movaps [0x14000a040], xmm0; 使用longjmp返回到setjmp位置0x140001781 call longjmp
```



```
r2 -q -c"aaa; pxw 16 @ 0x14000a040"main.exe
```



```
0x14000a040 0x12345678 0x9abcdef0 0xfedcba98 0x76543210
```



```
# 原始密钥值key1 =0x12345678key2 =0x9abcdef0key3 =0xfedcba98key4 =0x76543210# 按照异常处理函数中的变换逻辑计算k0 = key1 ^0xdeadbeef # 0xCC99E897k1 = key2 -0x789abcdf # 0x22222211k2 = key3 -0x11223344 # 0xEDBA8754k3 = key4 ^0xccddeeff # 0xBA89DCEF
```



```
k[0] = 0xCC99E897 (3432638615)k[1] = 0x22222211 (572662289)k[2] = 0xEDBA8754 (3988424532)k[3] = 0xBA89DCEF (3129597167)
```



```
r2 -q -c"aaa; pd 100 @ 0x140001790"main.exe
```



```
; TEA算法的delta常量（补码形式）0x1400017d5 sub r9d, 0x61c88647 ; delta = 0x61C886470x140001812 cmp r9d, 0xc6ef3720 ; sum = delta * 32; TEA核心运算逻辑0x1400017dc shl eax, 4 ; v << 40x1400017df shr r12d, 5 ; v >> 50x1400017e3 add r12d, r8d ; 加上密钥0x1400017e6 add eax, ebx ; 累加0x1400017e8 xor eax, r12d ; 异或运算
```



```
v0 += ((v1 <<4) + k[0]) ^ (v1 + sum) ^ ((v1 >>5) + k[1]);v1 += ((v0 <<4) + k[2]) ^ (v0 + sum) ^ ((v0 >>5) + k[3]);sum -= delta;
```



```
voiddecrypt(uint32_t* v,uint32_t* k){ uint32_tv0 = v[0], v1 = v[1]; uint32_tsum =0xC6EF3720; // delta * 32 uint32_tdelta =0x61C88647; for(inti =0; i <32; i++) { v1 -= ((v0 <<4) + k[2]) ^ (v0 + sum) ^ ((v0 >>5) + k[3]); v0 -= ((v1 <<4) + k[0]) ^ (v1 + sum) ^ ((v1 >>5) + k[1]); sum += delta; } v[0] = v0; v[1] = v1;}
```



```
0x140001883 lea rdx, [0x14000a020] ; 密文数据地址0x1400018a2 cmp dword [rax], ebx ; 比较加密结果与密文
```



```
r2 -q -c"aaa; pxw 32 @ 0x14000a020"main.exe
```



```
0x14000a020 0xe1c22986 0xd39eddc5 0xdfa1484d 0x10d4e53c0x14000a030 0xc49a3be4 0x77dbf48a 0xe5ebae29 0xe99fec5c
```



```
uint32_tciphertext[8] = { 0xe1c22986,0xd39eddc5,0xdfa1484d,0x10d4e53c, 0xc49a3be4,0x77dbf48a,0xe5ebae29,0xe99fec5c};
```



```
#include<stdint.h>#include<stdio.h>voiddecrypt(uint32_t* v,uint32_t* k){ uint32_tv0 = v[0], v1 = v[1]; uint32_tsum =0xC6EF3720; // delta * 32 uint32_tdelta =0x61C88647; for(inti =0; i <32; i++) { v1 -= ((v0 <<4) + k[2]) ^ (v0 + sum) ^ ((v0 >>5) + k[3]); v0 -= ((v1 <<4) + k[0]) ^ (v1 + sum) ^ ((v1 >>5) + k[1]); sum += delta; } v[0] = v0; v[1] = v1; printf(" %x %x", v0, v1);}intmain(){ // 从程序中提取的密文 uint32_tv[8] = { 0xe1c22986,0xd39eddc5,0xdfa1484d,0x10d4e53c, 0xc49a3be4,0x77dbf48a,0xe5ebae29,0xe99fec5c }; // 计算得到的密钥 uint32_tk[4] = {0xCC99E897,0x22222211,0xEDBA8754,0xBA89DCEF}; printf("Decrypting TEA...n"); // TEA每次处理64位（两个32位整数） for(inti =0; i <8; i +=2) { decrypt(&v[i], k); } printf("n"); return0;}
```



```
gcc decrypt_tea.c -o decrypt_tea./decrypt_tea
```



```
Decrypting TEA...67616c66 6731737b 5f6c346e 646e3468 5f72336c 745f7331 6b633172 7d212179
```



```
32位整数：0x67616c66内存布局（小端序）： 地址增长方向 -> [66] [6c] [61] [67] f l a g
```



```
#!/usr/bin/env python3importbinascii# 从TEA解密得到的十六进制字符串hex_values ="67616c66 6731737b 5f6c346e 646e3468 5f72336c 745f7331 6b633172 7d212179"hex_list = hex_values.split(" ")print("Converting to ASCII with byte reversal:")flag =""forhex_strinhex_list: # 将十六进制转为字节，解码为ASCII，然后反转字符串 decoded = binascii.a2b_hex(hex_str).decode() reversed_str = decoded[::-1] flag += reversed_str print(f"{hex_str}->{decoded}->{reversed_str}")print(f"nFinal flag:{flag}")
```



```
python3 extract_flag.py
```



```
Converting to ASCII with byte reversal:67616c66 -> galf -> flag6731737b -> g1s{ -> {s1g5f6c346e -> _l4n -> n4l_646e3468 -> dn4h -> h4nd5f72336c -> _r3l -> l3r_745f7331 -> t_s1 -> 1s_t6b633172 -> kc1r -> r1ck7d212179 -> }!!y -> y!!}Final flag: flag{s1gn4l_h4ndl3r_1s_tr1cky!!}
```



```
signal() - 注册信号处理函数_setjmp() - 保存执行上下文longjmp() - 恢复执行上下文
```



```
mov dword [0], eax ; 向空指针写入mov dword [0xffffffff], eax ; 向非法地址写入div ecx ; 除零（当ecx为0时）ud2 ; 未定义指令
```



```
setjmp -> 触发异常 -> 异常处理 -> longjmp -> 继续执行
```



```
((v <<4) + k[i]) ^ (v + sum) ^ ((v >>5) + k[j])
```



```
地址： 0x1000 0x1001 0x1002 0x1003数据： 78 56 34 12
```



```
地址： 0x1000 0x1001 0x1002 0x1003数据： 12 34 56 78
```



```
# 方法1：使用切片反转text ="galf"flag = text[::-1] # "flag"# 方法2：使用struct模块importstructnum =0x67616c66bytes_data = struct.pack('<I', num) # 小端序打包text = bytes_data.decode()[::-1] # 解码并反转# 方法3：使用binascii模块importbinasciihex_str ="67616c66"decoded = binascii.a2b_hex(hex_str).decode() # "galf"flag = decoded[::-1] # "flag"
```
