# 解析2025强网拟态Icall

> 原文: https://www.ctfiot.com/277428.html
> ID: 277428

Icall – 多层加密与反调试的攻防对抗

前言

本文详细记录了一道名为”Icall”的CTF逆向题目的完整分析过程。作为一道综合性逆向题目，它涉及反调试技术、自定义RC4流密码、仿射密码等多项技术，非常适合学习现代逆向工程的思路和方法。

题目提示：Icall call where?

目标：通过逆向分析获取隐藏的flag

一、初步侦察 – 了解目标

1.1 文件基本信息

首先对目标文件进行基础信息收集：

file Icall

输出结果：

Icall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV),dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,for GNU/Linux 3.2.0, stripped

关键信息解读：

ELF 64-bit：Linux平台64位可执行文件

stripped：符号表已被移除，增加了分析难度，函数名、变量名等信息不可见

dynamically linked：使用动态链接，会调用外部库函数

.init_array：初始化函数数组，在main之前执行

.data：数据段，可能包含密文

.rodata：只读数据段，可能包含S-box

pthread_create：创建线程

prctl：进程控制，常用于反调试

getpid+kill：可能用于自杀式反调试

0x401120

0x401130← 这是我们的重点

主线程在init阶段创建一个子线程

子线程调用prctl(PR_SET_PTRACER, ...)设置跟踪权限

读取/proc/self/status文件检查TracerPid字段

如果TracerPid不为0，说明正在被调试，程序调用kill自杀

return命令会让函数立即返回，跳过所有反调试检测代码

这比修改二进制文件更灵活，且不会破坏程序完整性

第一次：参数为0x0C(12)

第二次：参数为0x1E(30)

第三次：参数为0x2A(42)

轮次

循环次数

十六进制

第1轮

12

0x0C

第2轮

30

0x1E

第3轮

42

0x2A

字符类型

基准

模数(m)

乘数(a)

加数(b)

逆元(a⁻¹)

数字 0-9

‘0’

10

7

11

3

大写 A-Z

‘A’

26

17

11

15

小写 a-z

‘a’

26

17

11

15

r0uNd_Rc4：多轮（Round）RC4加密

Aff1ne：仿射（Affine）密码

Enc1yp7：加密（Encrypt）的1337写法

使用pthread_create在主线程启动前创建监控线程

监控线程通过prctl和读取/proc/self/status检测调试状态

检测到调试器时使用kill终止进程

方法1（推荐）：GDB的return命令直接跳过函数

方法2：Hook系统调用（LD_PRELOAD）

方法3：修改二进制文件，NOP掉检测代码

反调试函数通常在.init_array段注册

多线程反调试比单线程更难绕过

动态绕过比静态patch更灵活

查找256字节数组（S-box）

寻找典型的交换操作

观察模256运算

识别XOR操作

自定义S-box初始值

多轮PRGA生成单个密钥流字节

CFB模式的链式XOR

三轮独立加密

多轮PRGA大幅增强了密钥流的随机性

CFB模式消除了相同明文的模式特征

三轮加密增加了暴力破解的复杂度

模运算

乘法逆元（扩展欧几里得算法）

同余方程

快速识别仿射变换（imul+add+idiv）

验证互质性（gcd(a, m) = 1）

计算乘法逆元

作为预处理层增加分析难度

保持字符类型不变（数字仍是数字）

与强加密算法结合使用

文件信息收集（file, readelf, strings）

段结构分析

反汇编关键函数

提取硬编码数据

运行程序观察行为

GDB设置断点跟踪执行流

观察寄存器和内存变化

Hook关键函数

结合静态和动态信息

识别算法特征

编写验证脚本

迭代优化理解

使用内核级反调试（ptrace自身）

添加时间检测（RDTSC指令）

检测虚拟机环境

实现代码完整性校验

使用真正的密钥派生函数（PBKDF2）

添加HMAC完整性保护

实现白盒加密

使用更复杂的分组密码

控制流平坦化

虚假控制流注入

字符串加密

虚拟机保护（VMProtect）

工具

用途

命令示例

file

文件类型识别

readelf

ELF文件分析

objdump

反汇编

strings

字符串提取

GDB

动态调试

Python

脚本编写

《Practical Reverse Engineering》

《The IDA Pro Book》

《Reversing: Secrets of Reverse Engineering》

《Applied Cryptography》- Bruce Schneier

《Cryptography Engineering》

RFC 4345 (RC4)

CrackMe网站

CTFtime – CTF竞赛平台

GitHub上的逆向工程工具集


```
file Icall
Icall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV),dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,for GNU/Linux 3.2.0, stripped
readelf -h Icall
入口点地址：0x401040
readelf -S Icall | grep -E"Name|init_array|data|rodata"
strings Icall | head -30
pthread_createpthread_detachprctlgetpidkill
readelf -x .init_array Icall
".init_array"节的十六进制输出： 0x00405dd0 20114000 00000000 30114000 00000000
objdump -d Icall | grep"401130:"-A 50
401130: push %rbp401131: mov %rsp,%rbp401134: sub $0x40,%rsp...401173: movabs $0x401290,%r8 # 线程函数地址...40118b: call *%r8 # pthread_create调用
objdump -d Icall | grep"401290:"-A 80
4012ce: mov $0x4,%edi # PR_SET_TRACER4012e9: call *%r9 # prctl调用
set pagination offset confirm off
# 在反调试函数入口设置断点b *0x401130run <<< "test_input"# 直接返回，不执行反调试代码return
# 继续执行到mainb *0x402000continuequit
gdb -x bypass_antidebug.gdb Icall
objdump -d Icall | grep -A 30"^0000000000401040"
401061: mov $0x402000,%rdi # main函数地址401068: call *0x4f6a(%rip) # __libc_start_main
objdump -d Icall | grep"402000:"-A 200 | head -250
1. 函数序言（保存栈帧）2. 调用scanf/fgets读取用户输入3. 调用strlen计算输入长度4. 多次调用同一个函数（疑似加密函数）5. 调用memcmp比较结果6. 根据比较结果输出成功/失败信息
readelf -x .data Icall
406020 f788c329 36646329 c77f1cab 71e00349 ...)6dc)....q..I406030 73cb0aaf 0c87848e 5a64c7ac 2a670000 s.......Zd..*g..
enc = [0xF7,0x88,0xC3,0x29,0x36,0x64,0x63,0x29,0xC7,0x7F, 0x1C,0xAB,0x71,0xE0,0x03,0x49,0x73,0xCB,0x0A,0xAF, 0x0C,0x87,0x84,0x8E,0x5A,0x64,0xC7,0xAC,0x2A,0x67]
# 绕过反调试b *0x401130runreturn
# 在可能的加密调用处断点b *0x402073b *0x402102b *0x40219bcontinue
# 访问256字节数组mov (%rax,%rcx,1),%dl # S[i]mov (%rax,%rdx,1),%r8b # S[j]
xchg %dl,%r8b # swap(S[i], S[j])
add %dl,%r8b # t = S[i] + S[j]movzbl %r8b,%edxmov (%rax,%rdx,1),%cl # K = S[t]
xor %cl,%bl # plaintext ^ keystream
s_box = [ 0xCD,0xE1,0x65,0xC6,0xB3,0x05,0x63,0x50,0x07,0x36, 0x0B,0x10,0x87,0x49,0x40,0x0F,0xF0,0xB5,0xE9,0xD2, # ... 共256个字节 0x62,0xA3,0x79,0x4C,0xFE,0xFF]
defget_keystream_byte(n_rounds): for_inrange(n_rounds): # 重复n次 i = (i +1) %256 j = (j + s_box[i]) %256 s_box[i], s_box[j] = s_box[j], s_box[i] k = s_box[(s_box[i] + s_box[j]) %256] returnk # 只返回最后一次的结果
# 第一个字节特殊处理C[0] = P[0] ^ S_box[0] ^ K[0]# 后续字节形成链式依赖foriinrange(1, len(P)): C[i] = P[i] ^ C[i-1] ^ K[i]
输入： AAAA AAAA ...RC4前： LLLL LLLL ... # 字符已经改变！
# 判断字符类型cmp $'0',%aljl .not_digitcmp $'9',%aljg .not_digit
# 对数字进行变换movzbl %al,%eaxsub $0x30,%eax # x = c - '0'imul $0x7,%eax,%edx # y = 7 * xadd $0xb,%edx # y = y + 11mov $0xa,%ecxcdqidiv %ecx # y = y % 10add $0x30,%edx # result = y + '0'
E(x) = (a * x + b) mod m
D(y) = a^(-1) * (y - b) mod m
# 对于数字：7 * 3 = 21 ≡ 1 (mod 10) ✓# 对于字母：17 * 15 = 255 ≡ 1 (mod 26) ✓
原始flag → [仿射变换] → [RC4轮1(0x0C)] → [RC4轮2(0x1E)] → [RC4轮3(0x2A)] → 密文
密文 → [RC4轮3逆(0x2A)] → [RC4轮2逆(0x1E)] → [RC4轮1逆(0x0C)] → [仿射逆变换] → 原始flag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-# 密文数据（从0x406020提取）new_enc = [0xF7,0x88,0xC3,0x29,0x36,0x64,0x63,0x29,0xC7,0x7F, 0x1C,0xAB,0x71,0xE0,0x03,0x49,0x73,0xCB,0x0A,0xAF, 0x0C,0x87,0x84,0x8E,0x5A,0x64,0xC7,0xAC,0x2A,0x67]defget_key(a4): """ 生成RC4密钥流 参数a4: PRGA循环次数 """ # 自定义S-box初始值（256字节） s_box = [ 0xCD,0xE1,0x65,0xC6,0xB3,0x05,0x63,0x50,0x07,0x36, 0x0B,0x10,0x87,0x49,0x40,0x0F,0xF0,0xB5,0xE9,0xD2, 0x14,0x15,0x16,0x17,0xED,0xDB,0x77,0xE4,0x1C,0x57, 0xC7,0x6D,0x66,0xA9,0xB2,0x3E,0x24,0xCB,0xDC,0xC0, 0xA8,0x29,0xFD,0xF6,0x76,0x2D,0x92,0x8F,0xF9,0x68, 0xEE,0x64,0x34,0x7C,0x71,0xCA,0xB1,0x52,0x3A,0x98, 0xE7,0x4D,0x5D,0x03,0x82,0x37,0x9B,0x91,0x6F,0x55, 0xE8,0xEA,0x43,0x74,0x0D,0x38,0x4B,0xFC,0x67,0x0E, 0x47,0x94,0x7E,0x78,0x54,0x61,0xB9,0xB6,0x33,0x09, 0xDD,0x5B,0x26,0x7A,0x83,0x7B,0x3F,0xF5,0x02,0xD6, 0xDA,0xD1,0xA0,0x80,0x4E,0xAE,0x6A,0x6B,0x8E,0xCC, 0x39,0x44,0x5A,0x48,0x72,0xC4,0x20,0x13,0x2C,0x8B, 0xE0,0x32,0x7F,0x89,0x19,0x0A,0x1F,0x22,0x31,0x04, 0xDF,0xE6,0xA2,0x85,0x86,0x30,0x06,0x12,0xBE,0x51, 0x8D,0x8C,0xD5,0x2B,0x90,0x18,0xB8,0x0C,0xD4,0x95, 0x96,0x9A,0xD9,0x9C,0x2F,0xEF,0x99,0xE3,0x9E,0xB0, 0x70,0xAD,0xB7,0x1E,0x28,0x45,0xF3,0xCE,0x27,0x69, 0xAA,0xF2,0xE5,0xA5,0xD3,0xE2,0xAF,0x9D,0x35,0x3D, 0xB4,0xAB,0xC8,0xA4,0x9F,0x6E,0xBA,0x2A,0xBC,0x84, 0x97,0x08,0xA7,0xD7,0xC2,0x2E,0x6C,0x81,0x4A,0x5F, 0xA1,0xC9,0xFA,0x21,0x73,0x00,0xC3,0x11,0x58,0x60, 0x56,0x4F,0x1A,0xFB,0x1B,0x01,0xA6,0x88,0x59,0xD0, 0x5C,0xC1,0x3C,0xAC,0xC5,0x7D,0xF1,0x41,0xBB,0x8A, 0x75,0xDE,0x42,0xEC,0x93,0xEB,0xBD,0x3B,0x53,0x46, 0xBF,0x1D,0x5E,0xD8,0xF4,0xCF,0x23,0xF7,0xF8,0x25, 0x62,0xA3,0x79,0x4C,0xFE,0xFF ] xor = [] i =0 j =0 v7 =0 # 对每个字节生成密钥流 forbyte_posinrange(30): # 执行a4次PRGA循环 for_inrange(a4): i = (i +1) %256 j = (j + s_box[i]) %256 # 交换S[i]和S[j] s_box[i], s_box[j] = s_box[j], s_box[i] # 生成密钥流字节 t_idx = (s_box[i] + s_box[j]) %256 v7 = s_box[t_idx] xor.append(v7) returnxor
# 三轮解密（逆序：从0x2A开始）rounds = [0x2a,0x1e,0xc]print("="*60)print("开始RC4三轮解密")print("="*60)forround_numinrange(3): print(f"n【第{round_num +1}轮解密】") print(f" 循环次数:{rounds[round_num]}(0x{rounds[round_num]:
02x})") # 生成本轮密钥流 xor = get_key(rounds[round_num]) print(f" 第一个密钥流字节: 0x{xor[0]:
02x}") # 逆向链式XOR：从后往前解密 foriinrange(len(new_enc) -1,-1,-1): ifi !=0: # C[i] = P[i] ^ C[i-1] ^ K[i] # 解密：P[i] = C[i] ^ C[i-1] ^ K[i] new_enc[i] = new_enc[i] ^ new_enc[i -1] ^ xor[i] else: # 第一个字节特殊处理 new_enc[i] = new_enc[i] ^0xCD^ xor[i] print(f" 解密后前10字节:{bytes(new_enc[:10])}")print("n"+"="*60)print("RC4解密完成！")print("="*60)print(f"n仿射密文:{bytes(new_enc)}")print(f"十六进制:{bytes(new_enc).hex()}")
==============================================================开始RC4三轮解密==============================================================【第1轮解密】 循环次数: 42 (0x2a) 第一个密钥流字节: 0x83 解密后前10字节: b'x08x9ex11Vx1c'【第2轮解密】 循环次数: 30 (0x1e) 第一个密钥流字节: 0x97 解密后前10字节: b'=6Gx08x1d'【第3轮解密】 循环次数: 12 (0x0c) 第一个密钥流字节: 0x5b 解密后前10字节: b'uklb{a1vYg'==============================================================RC4解密完成！==============================================================仿射密文: b'uklb{a1vYg_Az9_Luu8ynNyz8xm0!}'十六进制: 756b6c627b61317659675f417a395f4c757538796e4e797a38786d30217d
#!/usr/bin/env python3
# -*- coding: utf-8 -*-defdecrypt_char(c): """ 解密单个字符 使用仿射密码的逆变换 """ if'0'<= c <='9': # 数字：a=7, b=11, m=10, a^(-1)=3 base, mod, inv = ord('0'),10,3 elif'A'<= c <='Z': # 大写字母：a=17, b=11, m=26, a^(-1)=15 base, mod, inv = ord('A'),26,15 elif'a'<= c <='z': # 小写字母：a=17, b=11, m=26, a^(-1)=15 base, mod, inv = ord('a'),26,15 else: # 非字母数字字符不变（如花括号、感叹号） returnc # 解密公式：x = a^(-1) * (y - b) mod m y = ord(c) - base x = (inv * (y -11)) % mod returnchr(x + base)defdecrypt_string(s): """解密整个字符串""" return''.join(decrypt_char(c)forcins)if__name__ =="__main__": # 从RC4解密得到的仿射密文 shifted_flag ="uklb{a1vYg_Az9_Luu8ynNyz8xm0!}" print("="*60) print("仿射密码解密") print("="*60) print(f"n输入（仿射密文）：{shifted_flag}") # 解密 final_flag = decrypt_string(shifted_flag) print(f"n输出（最终flag）：{final_flag}") print("n"+"="*60) print("解密成功！") print("="*60)
==============================================================仿射密码解密==============================================================输入（仿射密文）：uklb{a1vYg_Az9_Luu8ynNyz8xm0!}输出（最终flag）：flag{r0uNd_Rc4_Aff1neEnc1yp7!}==============================================================解密成功！==============================================================
flag{r0uNd_Rc4_Aff1neEnc1yp7!}
```
