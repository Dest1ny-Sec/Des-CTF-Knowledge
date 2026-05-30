# 解析第九届 XCTF Tch3s

> 原文: https://www.ctfiot.com/278232.html
> ID: 278232

CTF密码学挑战：Tch3s 时序攻击详解

题目概述

本文将深入分析一道CTF密码学题目，该题目涉及时序攻击（Timing Attack）和伪随机数生成器（PRNG）的弱点。题目提供了两个文件：

Tch3s：一个ELF可执行文件

output：程序的输出文件，包含加密的flag和测试数据

程序首先输出加密后的flag（十六进制格式）

然后进行多轮测试，每次：

生成随机的16字节明文

加密该明文并输出密文

解密密文验证正确性

记录加密和解密所需的时间（纳秒）

初始化随机数生成器：使用srand(time(NULL))

生成加密密钥：通过16次rand() % 256调用生成16字节的密钥

加密flag：使用生成的密钥对flag进行加密并输出

测试循环：进行多次测试，每次生成随机明文进行加密解密测试

种子空间有限：time(NULL)返回的是Unix时间戳（自1970年1月1日以来的秒数），虽然数值很大，但在特定时间范围内的可能值是有限的。

可预测性：如果我们知道程序大致的运行时间，就可以在一个很小的时间窗口内暴力搜索所有可能的种子。

确定性：相同的种子会产生完全相同的随机数序列。如果我们找到了正确的种子，就能重现所有的随机数，包括用于生成密钥的随机数。

遍历可能的时间戳作为种子

对每个种子：

调用srand(seed)

跳过前16次rand()调用（密钥生成）

生成16个随机数

检查是否与第一个测试明文匹配

找到匹配的种子后，就能重现密钥

我们遍历可能的时间戳范围（约4000万个值）

对于每个候选种子，我们模拟程序的行为：先跳过16次rand()调用，然后生成16个随机数

将生成的随机数与output文件中的第一个测试明文进行比对

如果完全匹配，说明找到了正确的种子

这个动态库使用LD_PRELOAD技术来劫持程序对srand的调用

当程序调用srand(time(NULL))时，我们的函数会被调用

我们从环境变量SRAND中读取预设的种子值，并用它替换原始的种子

这样就能让程序使用我们找到的种子，而不是当前时间

加密函数地址：0x30ba（相对地址）

解密函数地址：0x31a1（相对地址）

环境准备：设置环境变量，使用我们找到的种子

断点设置：在加密函数入口处设置断点

内存修改：

当程序执行到加密函数时，$rdi指向明文缓冲区，$rsi指向密文缓冲区，$rdx指向密钥

我们将output中的加密flag写入$rdi（作为”假明文”）

注意字节序：十六进制字符串B789EB60在内存中以小端序存储为60 EB 89 B7，对应整数0x60eb89b7

调用解密函数：直接调用程序中的解密函数，传入相同的三个参数

查看结果：解密后的明文（即flag）会写入$rsi指向的缓冲区

识别弱PRNG：程序使用srand(time(NULL))作为随机数种子

种子空间分析：时间戳的可能范围有限，可以暴力搜索

侧信道信息泄露：程序输出的测试数据泄露了随机数序列

种子恢复：通过匹配已知的随机数序列来找到种子

密钥重建：使用恢复的种子重新生成密钥

密文解密：利用程序自身的解密函数完成解密

完全确定性：给定相同的种子，产生完全相同的序列

可预测性：知道几个连续的输出值，理论上可以推断出种子

周期性：序列会周期性重复

熵不足：time(NULL)的精度是秒级，1秒内的所有调用得到相同的值

可预测范围：我们通常能估计程序的运行时间范围

搜索空间小：即使搜索几年的时间跨度，也只有约1亿个可能值，现代计算机可以在几分钟内完成

差分功耗分析（DPA）

缓存时序攻击

推断密钥信息

使用恒定时间算法（Constant-time algorithms）

避免分支依赖于密钥数据

小心缓存和内存访问模式

Debian OpenSSL漏洞（2008）：由于错误的补丁，OpenSSL的PRNG熵源被严重削弱，导致只有32768种可能的密钥。

Android Bitcoin钱包漏洞（2013）：Android的SecureRandom实现有缺陷，导致生成的ECDSA签名可预测，比特币被盗。

PlayStation 3签名密钥泄露（2010）：Sony在ECDSA签名时重复使用了相同的随机数k，导致私钥可被计算出来。

密码学实现的重要性：即使加密算法本身是安全的，糟糕的实现也会导致系统完全崩溃。

随机性的关键作用：密码学系统的安全性高度依赖于高质量的随机数。

侧信道攻击的威胁：看似无害的信息泄露（如测试数据输出）可能成为攻击的突破口。

实战技能的综合运用：

二进制分析与逆向工程

C编程与系统调用

动态分析与调试技术

密码学原理与攻击技术

“时序攻击”的警示：虽然本题主要利用的是PRNG弱点，但题目名称提醒我们时序信息也可能是攻击向量。


```
file Tch3s
Tch3s: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, stripped
exportFLAG="flag{test_flag_for_analysis}"./Tch3s | head -n 20
encrypted flag: BCB00E4069532EC83DA17A2F407858D83A4E557C1E8E2A332AB14B0C637470CETest 1 plaintext: 8EE8CCC42881517FA1100B36B29E547ATest 1 encrypted: 1D2EE01F5596812A6A39FAEAFA745293, costs: 27800.000000 nsTest 1 decrypted: 8EE8CCC42881517FA1100B36B29E547A, costs: 28936.000000 nsTest 2 plaintext: 5E2C0A8B0A5188C71F3F487FF85E1C6ATest 2 encrypted: 7DC18F60A6E5413DB22A3E179B374E7F, costs: 29187.000000 nsTest 2 decrypted: 5E2C0A8B0A5188C71F3F487FF85E1C6A, costs: 29861.000000 ns...
head -n 20 output
encrypted flag: B789EB607A91D08888E2C4C4E4D9573FF5333E4783390B91EDB9D2B4FD2A5FC0Test 1 plaintext: 720B4455C91B6A024135343386B6679DTest 1 encrypted: C9BBC42200F90090C6A51602B63D0979, costs: 24497.000000 nsTest 1 decrypted: 720B4455C91B6A024135343386B6679D, costs: 22873.000000 ns...
    #include<stdbool.h>#include<stdint.h>#include<stdio.h>#include<stdlib.h>// 从output文件中获取的第一个test plaintextuint8_tseq[] = {0x72,0x0B,0x44,0x55,0xC9,0x1B,0x6A,0x02, 0x41,0x35,0x34,0x33,0x86,0xB6,0x67,0x9D};intmain(){// 时间戳应该是最近的，大约在2024-2025年之间// 1730000000 对应 2024年10月27日// 1770000000 对应 2026年2月3日for(intseed =1730000000; seed <1770000000; seed++) { if(seed %1000000==0) { printf("Progress: %d\n", seed); } srand(seed); boolgood =true; // 跳过key生成（前16次rand调用） for(inti =0; i <16; i++) rand(); // 检查生成的随机数序列是否匹配第一个test plaintext for(inti =0; i <sizeof(seq) /sizeof(seq[0]); i++) { unsignedinttemp = (unsignedint)rand() %256; if(temp != seq[i]) { good =false; break; } } if(good) { printf("Found seed: %d\n", seed); // 验证并输出key printf("Key bytes: "); srand(seed); for(inti =0; i <16; i++) { printf("%02X ", (unsignedint)rand() %256); } printf("\n"); break; } }return0;}
gcc crack_seed.c -o crack_seed./crack_seed
Progress: 1730000000Progress: 1731000000...Progress: 1753000000Found seed: 1753843495Key bytes: 17 A7 C5 6D 2D DE 47 FD BD CE B6 80 60 B9 16 9C
    #include<dlfcn.h>#include<stdio.h>#include<stdlib.h>typedefvoid(*srand_t)(unsignedintseed);srand_treal_srand;voidsrand(unsignedintseed){fprintf(stderr,"called srand(%d)\n", seed);if(!real_srand) { real_srand = dlsym(RTLD_NEXT,"srand"); }char*s = getenv("SRAND");intreal_seed =0;if(s) { sscanf(s,"%d", &real_seed); fprintf(stderr,"real seed is(%d)\n", real_seed); real_srand(real_seed); }else{ real_srand(seed); }}
gcc -shared -fPIC hook_srand.c -o hook_srand.so -ldl
exportFLAG="flag{test}"exportSRAND=1753843495LD_PRELOAD=./hook_srand.so ./Tch3s | head -n 10
called srand(1761836786)real seed is(1753843495)encrypted flag: D355DF17F209B90CFFFEA6DA1692780DTest 1 plaintext: 720B4455C91B6A024135343386B6679DTest 1 encrypted: C9BBC42200F90090C6A51602B63D0979, costs: 27116.000000 nsTest 1 decrypted: 720B4455C91B6A024135343386B6679D, costs: 25238.000000 ns
# 设置环境变量set environment FLAG=flag{test_flag_for_testing_12345}set environment SRAND=1753843495set environment LD_PRELOAD=./hook_srand.sofile ./Tch3s
# 在加密函数入口打断点b *0x5555555570barun
# 解密第一部分: B789EB607A91D08888E2C4C4E4D9573F
# 注意字节序转换（小端序）set *((int *)$rdi) = 0x60eb89b7set *((int *)$rdi+1) = 0x88d0917aset *((int *)$rdi+2) = 0xc4c4e288set *((int *)$rdi+3) = 0x3f57d9e4
# 调用解密函数p ((void (*)(void*,void*,void*))0x5555555571a1)($rdi,$rsi,$rdx)x/s $rsirun
# 解密第二部分: F5333E4783390B91EDB9D2B4FD2A5FC0set *((int *)$rdi) = 0x473e33f5set *((int *)$rdi+1) = 0x910b3983set *((int *)$rdi+2) = 0xb4d2b9edset *((int *)$rdi+3) = 0xc05f2afd
# 调用解密函数p ((void (*)(void*,void*,void*))0x5555555571a1)($rdi,$rsi,$rdx)x/s $rsiquit
gdb -batch -x decrypt_exact.gdb
Breakpoint 1, 0x00005555555570ba in ?? ()0x55555555b2e0:	"flag{tim1ng_a7t@"Breakpoint 1, 0x00005555555570ba in ?? ()0x55555555b2e0:	"ck_1s_dangerous}"
X[n+1] = (a * X[n] + c) mod m
Test 1 encrypted: ..., costs: 24497.000000 nsTest 1 decrypted: ..., costs: 22873.000000 ns
    #include<stdbool.h>#include<stdint.h>#include<stdio.h>#include<stdlib.h>uint8_tseq[] = {0x72,0x0B,0x44,0x55,0xC9,0x1B,0x6A,0x02, 0x41,0x35,0x34,0x33,0x86,0xB6,0x67,0x9D};intmain(){for(intseed =1730000000; seed <1770000000; seed++) { if(seed %1000000==0) { printf("Progress: %d\n", seed); } srand(seed); boolgood =true; for(inti =0; i <16; i++) rand(); for(inti =0; i <sizeof(seq) /sizeof(seq[0]); i++) { unsignedinttemp = (unsignedint)rand() %256; if(temp != seq[i]) { good =false; break; } } if(good) { printf("Found seed: %d\n", seed); srand(seed); printf("Key: "); for(inti =0; i <16; i++) { printf("%02X ", (unsignedint)rand() %256); } printf("\n"); break; } }return0;}
    #include<dlfcn.h>#include<stdio.h>#include<stdlib.h>typedefvoid(*srand_t)(unsignedintseed);srand_treal_srand;voidsrand(unsignedintseed){fprintf(stderr,"called srand(%d)\n", seed);if(!real_srand) { real_srand = dlsym(RTLD_NEXT,"srand"); }char*s = getenv("SRAND");intreal_seed =0;if(s) { sscanf(s,"%d", &real_seed); fprintf(stderr,"real seed is(%d)\n", real_seed); real_srand(real_seed); }else{ real_srand(seed); }}
gcc crack_seed.c -o crack_seedgcc -shared -fPIC hook_srand.c -o hook_srand.so -ldl
```
