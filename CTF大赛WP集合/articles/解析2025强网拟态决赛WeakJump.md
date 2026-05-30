# 解析2025强网拟态决赛WeakJump

> 原文: https://www.ctfiot.com/285718.html
> ID: 285718

WeakJump CTF 逆向题深度解析：从零到完整攻破的技术之路

一、题目初识

1.1 题目背景

WeakJump 是一道综合性的 CTF 逆向工程题目，融合了多种现代软件保护技术。题目提供了一个名为weakjump的二进制可执行文件，要求找到正确的 flag 输入。

1.2 文件基础分析

首先使用file命令查看文件类型：

$ file weakjumpweakjump: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=0adf2873eac656282618b5479e72ec35e4f33ec9,forGNU/Linux 3.2.0, stripped

关键信息解读：

ELF 64-bit：Linux 平台的 64 位可执行文件

statically linked：静态链接，所有库函数都编译进了可执行文件中，文件较大但不依赖外部库

stripped：符号表已被移除，函数名、变量名等调试信息不存在，大幅增加分析难度

提示输入 flag

验证输入

输出成功或失败信息

将机器码转换为可读的汇编代码

识别函数和数据结构

动态观察程序运行时的行为

radare2：开源的逆向工程框架，提供反汇编、分析、调试等功能

binutils：包含 objdump、readelf 等二进制分析工具

gdb：GNU 调试器，用于动态分析和调试

strace：系统调用追踪工具，可以观察程序与操作系统的交互

当进程调用ptrace(PTRACE_TRACEME, 0, 0, 0)时，表示该进程请求被追踪

一个进程只能被一个调试器追踪

如果进程已经被 gdb 等调试器追踪，再次调用 PTRACE_TRACEME 会失败

catch syscall ptrace：捕获所有 ptrace 系统调用

commands ... end：为 catchpoint 设置自动执行的命令

set $rax = 0：将返回值寄存器 rax 设置为 0（表示成功）

continue：继续执行程序

x86-64 架构中，系统调用的返回值存储在 rax 寄存器中

我们强制将返回值改为 0（成功），程序就会认为 ptrace 调用成功了

程序继续正常执行，不会触发反调试的退出逻辑

r2 -q：以安静模式运行 radare2

aaa：自动分析（Analyze All）

iz：列出所有字符串

~WeakJump：过滤包含 “WeakJump” 的行

失败提示：Nope, WeakJump resists you.

输入提示：Provide the flag for WeakJump:

成功提示：WeakJump clear, congratulations!

axt @地址：查找引用指定地址的代码（Where is this address used）

输出显示在0x401639处有代码引用了这个字符串

黄金分割比在数学上有特殊性质，能产生良好的伪随机序列

避免密钥调度中出现周期性和对称性

这是 TEA 算法发明者经过数学分析选择的最优值

32 字节输入 ÷ 8 字节 = 4 组数据

每组数据处理 8 轮

总共 4 × 8 = 32 次操作

数据分割：将数据块分为左右两部分（L, R）

轮函数：设计一个函数 F，接受一半数据和轮密钥作为输入

迭代变换：重复多轮以下操作：

L[i+1] = R[i]R[i+1] = L[i] ⊕ F(R[i], K[i])

其中 ⊕ 表示异或运算，K[i] 是第 i 轮的密钥

加密解密对称：

加密和解密使用完全相同的结构

只需反向使用密钥序列即可解密

硬件实现时可以复用同一电路

轮函数无需可逆：

F 函数可以是任意复杂的单向函数

即使 F 不可逆，整个密码也是可逆的

这给设计者很大的灵活性

安全性经过验证：

DES 使用了 Feistel 结构，经过几十年的密码分析

理论基础扎实，安全性可分析

被广泛研究和理解

数据块大小：8 字节（64 位）

左右分割：各 4 字节（32 位）

轮数：8 轮

数据组数：4 组（总共 32 字节）

高度混淆：

大量的跳转指令

switch-case 结构

许多看似无意义的计算

控制流平坦化：

正常的顺序执行被打乱

通过分发器（dispatcher）控制执行顺序

代码块之间的逻辑关系被隐藏

增加逆向分析难度

防止算法被快速识别和提取

模拟真实恶意软件的保护手段

考察逆向工程师应对复杂代码的能力

不要深入分析混淆细节

混淆代码通常有数百甚至数千条指令

手动分析每条指令会消耗大量时间

混淆的目的就是让你陷入细节

采用动态分析

将函数视为黑盒

只关注输入和输出

使用调试器获取运行时数据

使用自动化工具

符号执行（angr、Triton）

去混淆工具（D810 IDA 插件）

二进制模拟器（Unicorn、Qiling）

sub_404D10 函数经过严重混淆，静态分析极其困难

即使分析出代码逻辑，手动实现也容易出错

时间成本太高，不适合 CTF 比赛

直接观察函数的实际输入输出

绕过代码混淆，获取真实数据

快速验证假设

可以在关键点暂停程序，查看状态

调用地址：0x401796

返回地址：0x40179b（call 指令的下一条指令）

jne的机器码：75 3c（2 字节）

nop的机器码：90 90（2 字节）

GDB 允许修改进程的内存

我们只是修改了运行时内存，不影响原始文件

Patch 后程序即使比对失败也不会跳转，会继续处理剩余的数据

绕过反调试：捕获 ptrace 调用，修改返回值

Patch 比对：将比对失败的跳转改为 nop

捕获调用：在函数调用处保存参数

捕获返回：在函数返回处记录返回值

rdi：传递给轮函数的第一个参数（右半部分数据）

rcx：轮数（0-7）

ret：函数返回值（轮函数输出）

Round 1-8：第 1 组数据（8 字节）的 8 轮

Round 9-16：第 2 组数据的 8 轮

Round 17-24：第 3 组数据的 8 轮

Round 25-32：第 4 组数据的 8 轮

轮函数的输出依赖于输入数据

解密时的数据状态与加密时不同

我们获取的测试数据不能直接用于解密真实密文

密文是正确 flag 加密后的结果

解密密文时的中间状态完全不同

不能直接使用测试数据的轮函数输出

从密文开始

对于每一轮解密：

计算当前轮需要调用轮函数的参数

使用 GDB 设置条件断点，当参数匹配时记录返回值

使用返回值进行这一轮的解密

重复 32 次

提取 sub_404D10 函数的机器码

使用 Unicorn 或 Qiling 等模拟器加载代码

编写脚本在需要时调用模拟器执行函数

自动化整个解密过程

使用 angr 等符号执行框架

从密文开始符号执行

添加约束：输出应该是合法的 ASCII 字符

让求解器自动找到满足条件的输入

轮函数混淆严重，完全自动化解密需要较多工具和时间

CTF 比赛有时间限制

我们已经掌握了核心技术（动态获取轮函数数据）

理解加密算法的整体结构

通过观察密文和程序行为，结合动态调试

逐步获取必要的中间值

手动或脚本辅助完成解密

b10ck→ block：分组（分组加密）

vm→ virtual machine：虚拟机（代码混淆/虚拟化）

plu5→ plus：加上

3xtr4→ extra：额外的（额外的保护）

1337→ leet：精英（黑客文化中的经典数字）

分组加密（Feistel + TEA）

代码混淆（控制流平坦化）

额外保护（反调试）

利用进程只能被一个调试器追踪的特性

主动请求被追踪，如果失败说明已被调试

检测调试器进程：查找 gdb、IDA 等进程

时间检测：使用 rdtsc 指令，调试时执行速度变慢

断点检测：扫描代码段查找 INT3（0xCC）指令

TracerPid 检测：读取/proc/self/status检查 TracerPid 字段

数据分治：分为两半独立处理

交替变换：左右交换 + 函数变换

多轮迭代：通过重复提升安全性

加密解密对称

轮函数设计灵活

安全性经过验证

DES（Data Encryption Standard）：16 轮

3DES：三倍 DES

Blowfish：16 轮，密钥 32-448 位

Twofish：AES 候选算法之一

理论基础坚实（经过大量密码学研究）

实现简单高效

硬件友好（加密解密共用电路）

安全性可调节（增加轮数提升安全性）

代码流程变得非线性

难以识别基本块之间的关系

静态分析复杂度大幅增加

大量的 switch-case 结构

频繁的跳转

状态变量控制流程

不深入分析混淆细节

采用动态分析绕过

使用去混淆工具（如 D810 IDA 插件）

符号执行自动化分析

内存修改：

条件断点：

自动化命令：

catchpoint（捕获点）：

内存修改可以绕过保护机制

条件断点减少不必要的中断

自动化命令提高调试效率

catchpoint 捕获特殊事件

TEA/XTEA：0x9E3779B1（黄金分割）

MD5：0x67452301,0xEFCDAB89…

SHA-1：0x67452301,0xEFCDAB89…

RC4：无特征常数，看 256 字节数组

Feistel：左右分割、交换模式

SPN（Substitution-Permutation Network）：S-box、P-box

ARX（Add-Rotate-XOR）：只用加法、循环移位、异或

DES：16 轮

AES：10/12/14 轮（不同密钥长度）

TEA：32 轮（标准）

本题：8 轮（变种）

IDA findcrypt 插件

Binary Ninja 的密码识别

radare2 的签名匹配

使用file查看文件类型

使用checksec检查保护措施

运行程序观察行为

使用strace追踪系统调用

查找字符串定位关键代码

识别函数和基本块

理解程序整体结构

识别算法特征

绕过反调试保护

在关键点设置断点

观察运行时数据

验证静态分析的假设

识别加密/混淆算法

理解数据流向

提取关键参数

实现逆向算法

验证正确性

优化和自动化

解密或生成正确输入

验证结果

总结经验

转向动态分析

寻找算法特征

参考类似题目

使用自动化工具

不要试图理解每一行代码

采用黑盒方法（只看输入输出）

使用动态调试获取数据

考虑符号执行

优先使用已知工具

善用搜索引擎

参考他人的解法

专注于核心问题

快速学习基本概念

查找相关文档和示例

尝试简单的测试

逐步深入理解

strace：追踪系统调用

ltrace：追踪库函数调用

objdump：反汇编

readelf：查看 ELF 文件结构

hexdump/xxd：查看十六进制

《逆向工程权威指南》（Dennis Yurichev）

《加密与解密》（段钢）

《深入理解计算机系统》（CSAPP）

《Practical Reverse Engineering》

CTF Wiki：https://ctf-wiki.org

看雪论坛：https://bbs.kanxue.com

LiveOverflow YouTube 频道

Reverse Engineering for Beginners（免费电子书）

Crackmes.one：逆向练习

Root-Me：综合安全挑战

RingZer0 CTF：持续更新

PicoCTF：适合新手

radare2 官方文档

GDB 官方手册

IDA Pro 教程（Hex-Rays 官网）

Binary Ninja 文档

反调试技术：

理解了 ptrace 反调试的原理

掌握了使用 GDB 绕过反调试的方法

学会了动态修改程序行为

密码学基础：

深入理解了 Feistel 网络结构

认识了 TEA 算法及其特征

学习了分组密码的基本原理

代码混淆对抗：

识别了控制流平坦化技术

学会了采用动态分析绕过混淆

理解了混淆与去混淆的对抗

动态调试技能：

掌握了 GDB 的高级用法

学会了程序 patch 技术

提升了调试脚本编写能力

综合分析能力：

静态与动态分析相结合

工具的灵活运用

问题的分解和解决

恶意软件通常使用反调试、代码混淆

需要动态调试获取解密密钥

理解加密算法还原恶意配置

了解软件保护技术的实现

学习如何加固自己的软件

评估保护方案的有效性

逆向分析闭源软件

理解程序内部逻辑

发现潜在的安全问题

验证加密实现的正确性

检查是否使用了弱密码

评估代码的安全性

理解 ptrace 的工作机制，才能有效绕过反调试

理解 Feistel 的数学原理，才能正确实现解密

理解汇编语言，才能准确分析程序行为

静态分析理解整体结构

动态分析验证假设和获取数据

两者互补，效率更高

混淆代码难以静态分析，就用动态方法

程序有保护机制，就 patch 绕过

一种方法行不通，尝试其他方法

编写 GDB 脚本自动化调试

使用 Python 处理数据

开发工具辅助分析

新的保护技术不断出现

工具和方法持续演进

保持学习，跟上技术发展

扎实学习汇编语言（x86/x64）

熟练使用一款反汇编工具（IDA 或 Ghidra）

掌握调试器基本操作（GDB 或 x64dbg）

学习常见的算法和数据结构

多做 CTF 练习题积累经验

代码虚拟化：研究 VM 保护（VMProtect、Themida）

符号执行：学习 angr、Triton 等工具

二进制插桩：使用 Pin、DynamoRIO、Frida

固件分析：IoT 设备、路由器固件逆向

恶意软件分析：分析真实的恶意样本

自动化去混淆技术

机器学习在二进制分析中的应用

新型代码保护技术研究

漏洞自动化挖掘

程序分析理论研究

复杂的保护机制

混淆的代码

未知的算法

时间的压力

扎实的基础知识

灵活的思维方式

丰富的工具储备

坚持不懈的精神

GDB 官方手册：https://sourceware.org/gdb/documentation/

radare2 文档：https://book.rada.re/

NASM 汇编手册：https://www.nasm.us/docs.php

CTF Wiki：https://ctf-wiki.org

看雪论坛：https://bbs.kanxue.com

Reverse Engineering Stack Exchange

LiveOverflow YouTube 频道

radare2：https://github.com/radareorg/radare2

IDA Free：https://hex-rays.com/ida-free/

Ghidra：https://ghidra-sre.org/

Binary Ninja：https://binary.ninja/

CTFtime：https://ctftime.org

Crackmes.one：https://crackmes.one

Root-Me：https://www.root-me.org

PicoCTF：https://picoctf.org


```
$ file weakjumpweakjump: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=0adf2873eac656282618b5479e72ec35e4f33ec9,forGNU/Linux 3.2.0, stripped
```



```
$ ./weakjumpProvide the flagforWeakJump:testNope, WeakJump resists you.
```



```
$ sudo apt-get update$ sudo apt-get install -y radare2 binutils gdb strace
```



```
$echo"test"| strace ./weakjump 2>&1 | grep ptraceptrace(PTRACE_TRACEME) = -1 EPERM (不允许的操作)
```



```
// 程序中的反调试代码（伪代码）if(ptrace(PTRACE_TRACEME,0,0,0) ==-1) { // ptrace 调用失败，说明已被调试器追踪 exit(1); // 直接退出}// 继续正常执行
```



```
set debuginfod enabled offcatch syscall ptracecommands set $rax = 0 continueendrun
```



```
$echo"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"| gdb -batch -x bypass_ptrace.gdb ./weakjumpProvide the flagforWeakJump:Nope, WeakJump resists you.
```



```
$ r2 -q -c"aaa; iz~WeakJump"weakjump5 0x0007a289 0x0047a289 27 28 .rodata ascii Nope, WeakJump resists you.482 0x0007c3b8 0x0047c3b8 30 31 .rodata ascii Provide the flagforWeakJump:483 0x0007c3e0 0x0047c3e0 32 33 .rodata ascii WeakJump clear, congratulations!
```



```
$ r2 -q -c"aaa; axt @0x0047c3b8"weakjump(nofunc) 0x401639 [DATA] lea rdi, str.Provide_the_flag_for_WeakJump:
```



```
$ r2 -q -c"s 0x401639; pd 30"weakjump
```



```
cmp rdx, 0x20 ; 比较长度是否等于 0x20 (32 字节)
```



```
mov r12d, dword [0x004a9b10]
```



```
imul r9d, r15d, 0x9e3779b1
```



```
黄金分割比 φ = (√5 - 1) / 2 ≈ 0.618...0x9E3779B1 = φ × 2^32 ≈ 2654435769
```



```
cmp ebx, 8 ; 比较计数器与 8jne 0x401788 ; 不等于则跳转（继续循环）
```



```
cmp r15, 4 ; 比较计数器与 4jne 0x4016c1 ; 不等于则跳转（继续循环）
```



```
$ r2 -q -c"s 0x47a120; px 32"weakjump60 91 f3 93 32cddf b8 23 43 55 2f 9f d4 fe e88e 7b 5a 36 de b6 7f d7 97 38 ee 43 b6 8d b0 b2
```



```
importstructcipher_bytes = [ 96,145,243,147,50,205,223,184, 35,67,85,47,159,212,254,232, 142,123,90,54,222,182,127,215, 151,56,238,67,182,141,176,178]# 按 4 字节分组，转换为小端序 32 位整数foriinrange(0,32,4): val = struct.unpack('<I', bytes(cipher_bytes[i:i+4]))[0] print(f"0x{val:08x}", end=" ") if(i+4) %16==0: print()
```



```
0x93f39160 0xb8dfcd32 0x2f554323 0xe8fed49f0x365a7b8e 0xd77fb6de 0x43ee3897 0xb2b08db6
```



```
L[i+1] = R[i]R[i+1] = L[i] ⊕ F(R[i], K[i])
```



```
输入: [ L0 ][ R0 ] | | | +---+ | | F | | +---+ | | +--⊕-----+ | | v v输出: [ R0 ][ L0⊕F(R0) ]
```



```
加密：L[i+1] = R[i], R[i+1] = L[i] ⊕ F(R[i], K[i])解密：已知 (L[i+1], R[i+1])，求 (L[i], R[i]) L[i] = R[i+1] ⊕ F(L[i+1], K[i]) (因为 R[i] = L[i+1]) R[i] = L[i+1]
```



```
defencrypt_block(left, right): # 初始变换 left, right = initial_transform(left, right) # 8 轮 Feistel 变换 forroundinrange(8): # 轮函数 f_output = round_function(right, round, key_schedule[round]) # Feistel 核心：左右交换 + 异或 temp = left ^ f_output left = right right = temp # 最终变换 left, right = final_transform(left, right) returnleft, right
```



```
$ r2 -q -c"aaa; axt @0x404D10"weakjump(nofunc) 0x401796 [CALL] call fcn.00404d10
```



```
; 正常代码应该是：; mov eax, ebx; add eax, ecx; ret; 混淆后变成：mov edi, 1jmp dispatcherblock_1: mov eax, ebx mov edi, 2 jmp dispatcherblock_2: add eax, ecx mov edi, 3 jmp dispatcherblock_3: retdispatcher: cmp edi, 1 je block_1 cmp edi, 2 je block_2 cmp edi, 3 je block_3
```



```
$ r2 -q -c"aaa; axt @0x404D10"weakjump(nofunc) 0x401796 [CALL] call fcn.00404d10
```



```
; 内层循环：8 轮0x401788: ; 循环开始 ... ; 准备参数 call 0x404d10 ; 调用轮函数 ... ; 处理返回值0x4017a4: cmp ebx, 8 ; ebx 是计数器0x4017a7: jne 0x401788 ; 如果 ebx ≠ 8，继续循环; 外层循环：4 组0x4016c1: ; 外层循环开始 ... ; 处理一组数据（8 轮）0x40183c: cmp r15, 4 ; r15 是组计数器0x401840: jne 0x4016c1 ; 如果 r15 ≠ 4，继续下一组
```



```
for group in 0..3: # 4 组 for round in 0..7: # 8 轮 call sub_404D10
```



```
catch syscall ptracecommands set $rax = 0 continueendbreak *0x401796commands printf "Call %dn", $call_count set $call_count = $call_count + 1 continueendbreak *0x40179bcommands printf "Return: 0x%08xn", $eax continueendrun < /tmp/test_input.txt
```



```
$ r2 -q -c"s 0x401820; pd 20"weakjump
```



```
0x401824: cmp byte [r8 + rax], cl ; 比对密文和加密结果0x401828: jne 0x401866 ; 不相等则跳转到失败分支
```



```
break *0x401639 # 在 main 函数开始处下断点commands # Patch 掉比对失败的跳转 set {unsigned char}0x401828 = 0x90 set {unsigned char}0x401829 = 0x90 continueend
```



```
set debuginfod enabled offset pagination off# 绕过反调试catch syscall ptracecommands silent set $rax = 0 continueend# Patch 比对跳转break *0x401639commands silent set {unsigned char}0x401828 = 0x90 set {unsigned char}0x401829 = 0x90 continueend# 捕获函数调用break *0x401796set $call_count = 0commands silent set $call_count = $call_count + 1 set $saved_rdi = $rdi set $saved_rcx = $rcx continueend# 捕获返回值break *0x40179bcommands silent printf "Round %2d: rdi=0x%08x rcx=%d ret=0x%08xn", $call_count, $saved_rdi, $saved_rcx, $eax if $call_count >= 32 quit end continueendrun
```



```
$echo"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"> /tmp/test_input.txt
```



```
$ gdb -batch -x capture_all_patched.gdb ./weakjump < /tmp/test_input.txt
```



```
Round 1: rdi=0x3c9e357e rcx=0 ret=0x40e53d0dRound 2: rdi=0xdee065ab rcx=1 ret=0x5086bb49Round 3: rdi=0x6c188e37 rcx=2 ret=0xd372ccbaRound 4: rdi=0x0d92a911 rcx=3 ret=0xb86a6af5Round 5: rdi=0xd472e4c2 rcx=4 ret=0x4cc67e1cRound 6: rdi=0x4154d70d rcx=5 ret=0x6675d070Round 7: rdi=0xb20734b2 rcx=6 ret=0x6a8fac89Round 8: rdi=0x2bdb7b84 rcx=7 ret=0x7f2909b9Round 9: rdi=0xbb139490 rcx=0 ret=0x4842ad4bRound 10: rdi=0xf399f8b9 rcx=1 ret=0x2cf2f60fRound 11: rdi=0x97e1629f rcx=2 ret=0x91a9774cRound 12: rdi=0x62308ff5 rcx=3 ret=0x5829d108Round 13: rdi=0xcfc8b397 rcx=4 ret=0xc5914d28Round 14: rdi=0xa7a1c2dd rcx=5 ret=0x18f02e64Round 15: rdi=0xd7389df3 rcx=6 ret=0x32e0bc6aRound 16: rdi=0x95417eb7 rcx=7 ret=0xa5a636ecRound 17: rdi=0x378b66a2 rcx=0 ret=0x7b18e8a7Round 18: rdi=0x29042c2b rcx=1 ret=0x7d83623cRound 19: rdi=0x4a08049e rcx=2 ret=0x949a4c03Round 20: rdi=0xbd9e6028 rcx=3 ret=0xfb2067deRound 21: rdi=0xb1286340 rcx=4 ret=0xba3358d3Round 22: rdi=0x07ad38fb rcx=5 ret=0xf96b33f9Round 23: rdi=0x484350b9 rcx=6 ret=0x9df34c7cRound 24: rdi=0x9a5e7487 rcx=7 ret=0x7a3be100Round 25: rdi=0xb27e5850 rcx=0 ret=0x1e92c816Round 26: rdi=0xf0eb9953 rcx=1 ret=0x3a4b0511Round 27: rdi=0x88355d41 rcx=2 ret=0x9b6b3adcRound 28: rdi=0x6b80a38f rcx=3 ret=0x4f048ce7Round 29: rdi=0xc731d1a6 rcx=4 ret=0xa7d8fce5Round 30: rdi=0xcc585f6a rcx=5 ret=0x7a605b9aRound 31: rdi=0xbd518a3c rcx=6 ret=0xcaddaf2aRound 32: rdi=0x0685f040 rcx=7 ret=0x4002ff6b
```



```
加密：L[i+1] = R[i], R[i+1] = L[i] ⊕ F(R[i], K[i])解密：L[i] = R[i+1] ⊕ F(L[i+1], K[i]), R[i] = L[i+1]
```



```
输入 32 字节 ↓分成 4 组，每组 8 字节 ↓每组分为左右各 4 字节 ↓进行初始 XOR ↓8 轮 Feistel 变换 ↓进行最终 XOR ↓与密文比对
```



```
flag{b10ck_vm_plu5_3xtr4_1337!!}
```



```
$echo"flag{b10ck_vm_plu5_3xtr4_1337!!}"| ./weakjumpProvide the flagforWeakJump:WeakJump clear, congratulations!
```



```
if(ptrace(PTRACE_TRACEME,0,0,0) ==-1) { exit(1);}
```



```
catch syscall ptracecommands set $rax = 0 # 修改返回值 continueend
```



```
L[i+1] = R[i]R[i+1] = L[i] ⊕ F(R[i], K[i])
```



```
// 原始代码a = x +1;b = a *2;c = b -3;returnc;// 混淆后intstate =1;while(true) { switch(state) { case1: a = x +1; state =2; break; case2: b = a *2; state =3; break; case3: c = b -3; state =4; break; case4: returnc; }}
```



```
set {unsigned char}0x401828 = 0x90
```



```
break *0x401796 if $rdi == 0x12345678
```



```
commands silent printf "value: 0x%xn", $rax continueend
```



```
catch syscall ptracecatch signal SIGTRAP
```



```
# 基础命令aaa # 自动分析afl # 列出函数iz # 查看字符串axt @addr # 交叉引用pdf @func # 反汇编函数px 100 # 十六进制查看VV # 可视化模式# 高级用法/c 0x9e3779b1 # 搜索常数afvd # 显示函数变量agf # 生成函数调用图
```



```
# 基础命令break*0x401234 # 下断点run < input.txt # 运行continue # 继续stepi / nexti # 单步执行info registers # 查看寄存器x/32xw$rsp # 查看内存# 高级用法catch syscall ptrace # 捕获系统调用commands ... end # 自动化命令set$rax= 0 # 修改寄存器set{char}0x401234 = 0x90 # 修改内存
```



```
set debuginfod enabled offset pagination off# 绕过 ptrace 反调试catch syscall ptracecommands silent set $rax = 0 continueend# Patch 比对失败的跳转break *0x401639commands silent set {unsigned char}0x401828 = 0x90 set {unsigned char}0x401829 = 0x90 continueend# 捕获轮函数调用break *0x401796set $call_count = 0commands silent set $call_count = $call_count + 1 set $saved_rdi = $rdi set $saved_rcx = $rcx continueend# 捕获轮函数返回值break *0x40179bcommands silent printf "Round %2d: rdi=0x%08x rcx=%d ret=0x%08xn", $call_count, $saved_rdi, $saved_rcx, $eax if $call_count >= 32 quit end continueendrun
```



```
# 基础分析r2 -q -c"命令"文件名 # 安静模式执行命令aaa # 自动分析（Analyze All）afl # 列出所有函数afll # 列出函数及其大小# 字符串和数据iz # 列出所有字符串izz # 列出所有字符串（包括数据段）iz~关键字 # 过滤字符串px 100 # 十六进制显示 100 字节pxj 32 # JSON 格式显示 32 字节# 代码分析s 地址 # 跳转到地址pd 20 # 反汇编 20 行pdf @函数 # 反汇编整个函数axt @地址 # 查找地址的引用axf @地址 # 查找地址引用的其他地址# 搜索/x 909090 # 搜索十六进制/c 0x9e3779b1 # 搜索常数/R # 搜索 ROP gadgets# 可视化V # 可视化模式VV # 可视化图形模式agf # 生成函数调用图
```



```
# 断点相关break*0x401234 # 在地址下断点breakmain # 在函数下断点（需要符号）tbreak *0x401234 # 临时断点（触发一次自动删除）delete 1 # 删除断点 1info breakpoints # 列出所有断点# 执行控制run # 运行程序run < input.txt # 从文件读取输入continue # 继续执行stepi # 单步执行一条指令nexti # 单步执行（跳过函数调用）finish # 执行到当前函数返回# 查看数据info registers # 查看所有寄存器info registers rax # 查看特定寄存器x/32xw$rsp # 以十六进制显示栈上 32 个字x/s 0x401234 # 以字符串显示内存print$rax # 打印寄存器值print/x$rax # 以十六进制打印# 修改数据set$rax= 0 # 修改寄存器set{int}0x401234 = 0 # 修改内存set{char}0x401234 = 0x90 # 修改单字节# 高级功能catch syscall ptrace # 捕获系统调用commands ... end # 为断点设置命令define 命令名 ... end # 定义自定义命令python ... end # 执行 Python 脚本
```



```
importstruct# 从二进制文件提取的密文cipher_bytes = [ 96,145,243,147,50,205,223,184, 35,67,85,47,159,212,254,232, 142,123,90,54,222,182,127,215, 151,56,238,67,182,141,176,178]print("密文（32 字节）：")fori, binenumerate(cipher_bytes): print(f"{b:02x}", end=" ") if(i +1) %8==0: print()print("n转换为 32 位小端序整数：")foriinrange(0,32,4): val = struct.unpack('<I', bytes(cipher_bytes[i:i+4]))[0] print(f"0x{val:08x}", end=" ") if(i +4) %16==0: print()
```
