# [HITCTF 2022]re3 – debug_maze详细Writeup

> 原文: https://www.ctfiot.com/87278.html
> ID: 87278

HITCTF2022{4311254395e7d3cf0b372d95b58325674d6117}

一

前言

HITCTF的reverse方向总体都不难，由于是WIn32并且没有考察ollvm，主要考察方向有shellcode、动态加载、字符串混淆、花指令、驱动IO控制等一系列偏向于RW的技巧和知识点。这些知识点出现在很多流行恶意代码中，例如ransomware。

笔者稍微有一点恶意代码分析的经验，对本题目在比赛时已经还原的八九不离十，然而在最后一分钟判断奇偶时出现头昏行为把A、C判断为奇数导致没有提交flag。最后遗憾的没有苟到前十。但是题目本身已经吃透了，在这里把本题目的flag获取过程详细的给出，供参考。

一如既往，本Writeup会延续以前Writeup的风格，将按照解题的思路和顺序，对题目的考察点详细解释，可用于新手入门，但是会显得比较冗长。已经有基础的师傅可以略看，因为大部分时间我都在解释我如何看到这一点和解释我的解题思路。

二

FISRT GLANCE

拿到题目，例行对题目进行格式和壳检查。拖入die，可以发现题目为32位控制台程序，未加壳。

因此拖入IDA32进行初始观察。IDA32在载入之中没有遇到麻烦，打开main函数首先看到IsDebuggerPresent。

熟悉反调试的师傅可能会对这个IsDebuggerPresent进行跳patch过操作，但是我们先不急，先对整个题目做整体检查。

先看到第一个函数，其中包含了字符串give me your flag: here???和%s，似乎这个是要求输入的提示符。于是在这里我们打开程序：

可以看到提示字符串并不符合，这可能是个假输出，或者就是在哪里对字符串进行了修改。另外，我们注意到在退出程序的时候程序有延迟，并不是丝滑的点击关闭按钮程序就退出了，而是程序需要等一两秒才退出。这引起了我们的怀疑，记在小本本上。

回到IDA，这一函数的返回值是9，赋给了dword_426388。

继续向下看，观察到两个函数，这个函数使用了刚才被赋值的dword_426388：

这个函数中包含了两个可疑的部分。图中标出了。分别是对参数的偏移和解引用。这种操作一般代表这个参数是一个结构体指针。但是目前还没有确认这是什么指针，先记在小本本上。接下来是一个SM3的常量。SM3是中华人民共和国政府采用的一种密码散列函数标准，由国家密码管理局于2010年12月17日发布。本质上SM3是一种密码散列函数，可以粗浅的理解为一种类似于SHA-2的算法。

于是这个函数sub_4011F0就是我们一会儿要关注的一个点。我们接着继续查看main函数，在尾部看到最后一个函数sub_401320在这里我们看到了老朋友sub_4011F0，证实了上面的猜测。

接下来，我们注意到下面的switch块中存在两个常量。熟悉Windows开发的同学应该对这两个异常的十六进制值比较熟悉，它们分别是断点和拒绝访问错误。为什么题目在这里安置了这两个异常作为if的条件并且在其中安插了很像debug_maze题目名中maze所指的迷宫的操作呢？我们也把这个东西记在小本本上。

至此，main函数分析结束。

别急，到这里有经验的师傅还会检查TLS函数。TLS 回调函数的调用运行要先于 EP 代码的执行。它是各线程独立的数据存储空间，可修改进程的全局/静态数据。换句话说，TLS将在OEP之前执行。按下Ctrl+E，查看entry point，果然在其中看到了TLS函数的身影。

打开TLS函数，其中果然出现了被修改的痕迹。

这里也出现了IsDebuggerPresent函数的调用，但是简单的看一看逻辑就会发现，这里的F5结果中第25行的判断要求不存在调试器方才执行里面的代码。这就比较奇怪了。查看里面的函数，注意到函数sub_401D40经常被调用，于是我们跟踪进去，查看其逻辑。

sub_401D40调用了sub_401D40，前者（以29行为例）传入了unk_4258B8的地址。

这个地址看上去像是一个字符串。但是我们还未知道字符串的内容是什么。后一个函数接收两个参数，而传递给他的参数第一个为&unk_4258B8 + 1，第二个参数为这个字符串的第一个字符。跟踪到函数内可以看到函数的逻辑是异或加密。

int __cdecl sub_401D10(_BYTE *a1, char a2){ int result; // eax do { *a1++ ^= a2; result = (unsigned __int8)*a1; } while ( *a1 ); return result;}

分析上述函数的逻辑，得知这是将字符串的第1字节往后与第0字节异或，得到新的字符串再填入原来的空间。对unk_4258B8进行这样的操作：

From Hex, XOR – CyberChefXOR({‘option’:’Hex’,’string’:’0x7f’},’Standard’,false)&input=N0YgMTggMTYgMDkgMUEgNUYgMTIgMUEgNUYgMDYgMTAgMEEgMEQgNUYgMTkgMTMgMUUgMTggNDUgN0YgMDAgMDAgMDAgMDA)

很好，我们看到了程序的输出字符串，这个函数改名为dec_xored。后面紧跟的函数sub_4016C0就是printf函数（根据里面的va_start标志），同样的，sub_401730是scanf。另一个函数sub_401D70，经过类似的简要分析知道他是一个加密函数。用于在解密字符串后以任意密钥加密字符串，来防止内存搜索。

类似的，函数更名为enc_xored。

接下来分为两个部分，第一部分校验输入的合法性。

其中调用了函数_loaddll。字面意义上看，这似乎是一个调用动态链接库的函数。跟踪查看函数中调用了ExitProcess，因此可以知道这个函数和退出进程有关。我们暂时不管他。

第二部分是将输入变换之后填充到内存地址中。

其中要求变换后的各字节都为奇数，这是一个重要的提示，记在小本本上。

这里我们遇到了两个变量：byte_42639B和Str1。他们有什么关系呢？根据内存布局图。

他们似乎是互不相干的两个变量。细心的同学在分析scanf函数时就已经发现，Str的大小应该是1024字节。

结合分析，第二部分的for分析后注释如下。这一段是将输入的字符，例如1234转换为十六进制值0x1234并检查是否为奇数。

在完成这对两个字符的操作之后，如果为偶数，则进入错误环节。

经过刚才我们这一通操作，我们总结了下述要点：

三

地址转换机构：sub_4011F0

首先注意到这个函数返回的值在后续都被按照函数的方式被调用。

因此这很可能是一个类似于GetProcAddress函数的地址转换机构。但是如果我们按照dword_426388 := 9的初始值执行分析，就会发现总是会出发访问异常。验证这一函数的结构体的方法，是使用vs对应的编译一个程序出来。

注意到这个是异常0xC0000005，会不会是后续的函数的处理条件呢？我们跟踪到函数sub_401320中查看发现。

在其函数中也存在这一函数，而上下文中并不存在跳转，并且在TLS到OEP中都不存在自修改trick，因此我们可以认定，这个代码很可能出错了。但是运行时并没有出现这一错误，调试器也没有遇到这一问题，Windows也没有遇到这一问题，那么只有可能是我们的复现出错了。

有人问有没有可能是某处的SEH或者VEH（一种异常处理机制）？答案是否定的。先观察我们漏掉的“系统函数”_CRT_INIT，只有在.text:
004017B4处调用的_CRT_INIT中初始化了SEH链。在.text:
00D3396F中调用了一个sub_40F960，这个函数是一个数组调用函数（CALL_LIST）即对调用输入的参数。在其第一个参数unk_41E128的第二个offset sub_401000中调用了sub_403150，对byte_426B90进行了大量的赋值。这个变量也在刚才我们说到的异常分析函数中出现了。

而在start中，只有sub_4040B5中调用了SetUnhandledExceptionFilter。

其参数为0，代表传递给系统默认的错误处理句柄。稍有VS工程逆向经验的师傅都清楚，start中的诸多操作都很干净，这些异常是为了防止栈溢出的操作。感兴趣的同学可以自己编译一个vs项目做实验，笔者使用VS2022任意编译的项目的起始代码和题目的代码相差无几。下面给出笔者编译的代码（包含了vs自动生成的符号表）：

注意刚才我们怀疑的部分：

是完全一样的。这意味着这刚才我们遇到的错误并不是题目刻意引发的，而是我们的分析错误。

那么究竟是哪里出错了呢？我们注意到复现版本的代码中引用了变量dword_426388，这个变量在sub_401170中被修改过。

观察IDA似乎只有一行短短的return 9i。于是我们试图从汇编中找答案。

返回值被存储在eax里，而这个返回值本应该是一个if选择结构，这里因为可以执行编译前运算，IDA自动把不会触发的分支省略了，即右半边的loc_4011D1。这里的汇编代码如下：

.text:
004011BD 58 pop eax.text:
004011BE 58 pop eax.text:
004011BF 33 C0 xor eax, eax.text:
004011C1 83 F0 03 xor eax, 3.text:
004011C4 E8 00 00 00 00 call $+5.text:
004011C9 F7 E0 mul eax.text:
004011CB 83 F8 51 cmp eax, 51h ; 'Q'.text:
004011CE 74 01 jz short loc_4011D1.text:
004011D0 C3 retn.text:
004011D1 ; ---------------------------------------------------------------------------.text:
004011D1.text:
004011D1 loc_4011D1: ; CODE XREF: sub_401170+5E↑j.text:
004011D1 83 E8 21 sub eax, 21h ; '!'.text:
004011D4 64 8B 00 mov eax, fs:[eax].text:
004011D7 8B 40 0C mov eax, [eax+0Ch].text:
004011DA 8B 40 0C mov eax, [eax+0Ch].text:
004011DD 8B 00 mov eax, [eax].text:
004011DF 8B 00 mov eax, [eax].text:
004011E1 8B 40 18 mov eax, [eax+18h].text:
004011E4 5D pop ebp.text:
004011E5 C3 retn

其中出现了一个指令：call $+5，这是一个经典的反分析trick。在《恶意代码分析实战》第15章“对抗反汇编”第15.4.3节“滥用返回指针”中详细解释了这一花指令的原理。

对于我们这里的花指令，call $+5会执行mul eax两次，一次由call跳转，然后call结束时返回到mul eax顺序执行，因此正确的执行结果是eax == 51h，满足jz的条件，从而通过PEB获取了kernel32.dll基址。

知道了上述的关键信息，我们再返回看刚才的地址转换机构的前半部分就很明朗了。

后面部分的是SM3加密，这个加密我们可以轻易地知道这段代码实现了GetProcAddress的机制，也就是通过将函数的名称做数字签名，依次与传入的第二个参数进行比较，从而简介获取函数地址。有兴趣的师傅可以自己手动实现一个SM3代码，这里给出一个参考：

SMx/sm3.c at master · NEWPLAN/SMx (github.com)

（https://github.com/NEWPLAN/SMx/blob/master/SM3/Windows/SM3/src/sm3.c）

我的方法是通过绕过IsDebuggerPresent的方法动态调试，或者叫任意执行到这个函数，然后看eax对应的函数结构判断函数。通过判断，能够轻易地给出各种函数的名称，换句话说，导入表。下面给出一个示例：

四

子母进程调试及异常处理

通过上文的分析，我们将所有API转换，并给予相应的常量、名称和结构，能够大致梳理出题目的思路：

题目在未被调试的环境下创建了子进程，并使用DEBUG_ONLY_THIS_PROCESS | DEBUG_PROCESS启动。这样会使子进程进入被调试状态，将其事件全部发送给父进程，父进程接收子进程线程的异常，处理并观察flag的正确性，最终给出输出。

上图给的是地址转换之后的API以及对应的函数结构。可以看到其基本流程为：

而对应的两个异常，也和main函数的初始节中的一大堆奇怪的调试错误对上号。我们观察主函数中需要调试器（即子进程）中执行的汇编代码：

.text:
00D31A38 60 pusha.text:
00D31A39 B9 01 00 00 00 mov ecx, 1.text:
00D31A3E C1 E1 03 shl ecx, 3.text:
00D31A41 B8 02 00 00 00 mov eax, 2.text:
00D31A46 BB 09 00 00 00 mov ebx, 9.text:
00D31A4B 33 D2 xor edx, edx.text:
00D31A4D 8B 12 mov edx, [edx].text:
00D31A4F B9 01 00 00 00 mov ecx, 1.text:
00D31A54 D1 E1 shl ecx, 1.text:
00D31A56 B8 04 00 00 00 mov eax, 4.text:
00D31A5B CC int 3 ; Trap to Debugger.text:
00D31A5C B9 01 00 00 00 mov ecx, 1.text:
00D31A61 C1 E1 02 shl ecx, 2.text:
00D31A64 B8 00 00 00 00 mov eax, 0.text:
00D31A69 CC int 3 ; Trap to Debugger.text:
00D31A6A B9 01 00 00 00 mov ecx, 1.text:
00D31A6F D1 E1 shl ecx, 1.text:
00D31A71 B8 00 00 00 00 mov eax, 0.text:
00D31A76 BB FF FF FF FF mov ebx, 0FFFFFFFFh.text:
00D31A7B 33 D2 xor edx, edx.text:
00D31A7D 8B 12 mov edx, [edx].text:
00D31A7F B9 01 00 00 00 mov ecx, 1.text:
00D31A84 C1 E1 04 shl ecx, 4.text:
00D31A87 B8 00 00 00 00 mov eax, 0.text:
00D31A8C BB 06 00 00 00 mov ebx, 6.text:
00D31A91 CC int 3 ; Trap to Debugger.text:
00D31A92 B9 01 00 00 00 mov ecx, 1.text:
00D31A97 B8 00 00 00 00 mov eax, 0.text:
00D31A9C BB 05 00 00 00 mov ebx, 5.text:
00D31AA1 33 D2 xor edx, edx.text:
00D31AA3 8B 12 mov edx, [edx].text:
00D31AA5 B9 01 00 00 00 mov ecx, 1.text:
00D31AAA C1 E1 03 shl ecx, 3.text:
00D31AAD B8 01 00 00 00 mov eax, 1.text:
00D31AB2 BB 00 00 00 00 mov ebx, 0.text:
00D31AB7 33 D2 xor edx, edx.text:
00D31AB9 8B 12 mov edx, [edx].text:
00D31ABB B9 01 00 00 00 mov ecx, 1.text:
00D31AC0 C1 E1 04 shl ecx, 4.text:
00D31AC3 B8 01 00 00 00 mov eax, 1.text:
00D31AC8 BB 02 00 00 00 mov ebx, 2.text:
00D31ACD 33 D2 xor edx, edx.text:
00D31ACF 8B 12 mov edx, [edx].text:
00D31AD1 B9 01 00 00 00 mov ecx, 1.text:
00D31AD6 B8 02 00 00 00 mov eax, 2.text:
00D31ADB CC int 3 ; Trap to Debugger.text:
00D31ADC B9 01 00 00 00 mov ecx, 1.text:
00D31AE1 D1 E1 shl ecx, 1.text:
00D31AE3 B8 04 00 00 00 mov eax, 4.text:
00D31AE8 BB FF FF FF FF mov ebx, 0FFFFFFFFh.text:
00D31AED 33 D2 xor edx, edx.text:
00D31AEF 8B 12 mov edx, [edx].text:
00D31AF1 B9 01 00 00 00 mov ecx, 1.text:
00D31AF6 C1 E1 05 shl ecx, 5.text:
00D31AF9 B8 0F 00 00 00 mov eax, 0Fh.text:
00D31AFE 33 D2 xor edx, edx.text:
00D31B00 8B 12 mov edx, [edx].text:
00D31B02 B9 01 00 00 00 mov ecx, 1.text:
00D31B07 B8 00 00 00 00 mov eax, 0.text:
00D31B0C BB 06 00 00 00 mov ebx, 6.text:
00D31B11 33 D2 xor edx, edx.text:
00D31B13 8B 12 mov edx, [edx].text:
00D31B15 B9 01 00 00 00 mov ecx, 1.text:
00D31B1A D1 E1 shl ecx, 1.text:
00D31B1C B8 00 00 00 00 mov eax, 0.text:
00D31B21 BB 01 00 00 00 mov ebx, 1.text:
00D31B26 33 D2 xor edx, edx.text:
00D31B28 8B 12 mov edx, [edx].text:
00D31B2A B9 01 00 00 00 mov ecx, 1.text:
00D31B2F C1 E1 03 shl ecx, 3.text:
00D31B32 B8 01 00 00 00 mov eax, 1.text:
00D31B37 BB 00 00 00 00 mov ebx, 0.text:
00D31B3C 33 D2 xor edx, edx.text:
00D31B3E 8B 12 mov edx, [edx].text:
00D31B40 B9 01 00 00 00 mov ecx, 1.text:
00D31B45 C1 E1 04 shl ecx, 4.text:
00D31B48 B8 01 00 00 00 mov eax, 1.text:
00D31B4D BB 02 00 00 00 mov ebx, 2.text:
00D31B52 33 D2 xor edx, edx.text:
00D31B54 8B 12 mov edx, [edx].text:
00D31B56 B9 01 00 00 00 mov ecx, 1.text:
00D31B5B B8 02 00 00 00 mov eax, 2.text:
00D31B60 CC int 3 ; Trap to Debugger.text:
00D31B61 B9 01 00 00 00 mov ecx, 1.text:
00D31B66 D1 E1 shl ecx, 1.text:
00D31B68 B8 05 00 00 00 mov eax, 5.text:
00D31B6D BB 01 00 00 00 mov ebx, 1.text:
00D31B72 33 D2 xor edx, edx.text:
00D31B74 8B 12 mov edx, [edx].text:
00D31B76 B9 01 00 00 00 mov ecx, 1.text:
00D31B7B C1 E1 05 shl ecx, 5.text:
00D31B7E B8 08 00 00 00 mov eax, 8.text:
00D31B83 33 D2 xor edx, edx.text:
00D31B85 8B 12 mov edx, [edx].text:
00D31B87 B9 01 00 00 00 mov ecx, 1.text:
00D31B8C B8 00 00 00 00 mov eax, 0.text:
00D31B91 BB 06 00 00 00 mov ebx, 6.text:
00D31B96 33 D2 xor edx, edx.text:
00D31B98 8B 12 mov edx, [edx].text:
00D31B9A B9 01 00 00 00 mov ecx, 1.text:
00D31B9F D1 E1 shl ecx, 1.text:
00D31BA1 B8 00 00 00 00 mov eax, 0.text:
00D31BA6 BB FF FF FF FF mov ebx, 0FFFFFFFFh.text:
00D31BAB 33 D2 xor edx, edx.text:
00D31BAD 8B 12 mov edx, [edx].text:
00D31BAF B9 01 00 00 00 mov ecx, 1.text:
00D31BB4 C1 E1 03 shl ecx, 3.text:
00D31BB7 B8 01 00 00 00 mov eax, 1.text:
00D31BBC BB 00 00 00 00 mov ebx, 0.text:
00D31BC1 33 D2 xor edx, edx.text:
00D31BC3 8B 12 mov edx, [edx].text:
00D31BC5 B9 01 00 00 00 mov ecx, 1.text:
00D31BCA C1 E1 04 shl ecx, 4.text:
00D31BCD B8 01 00 00 00 mov eax, 1.text:
00D31BD2 BB 02 00 00 00 mov ebx, 2.text:
00D31BD7 33 D2 xor edx, edx.text:
00D31BD9 8B 12 mov edx, [edx].text:
00D31BDB B9 01 00 00 00 mov ecx, 1.text:
00D31BE0 B8 02 00 00 00 mov eax, 2.text:
00D31BE5 CC int 3 ; Trap to Debugger.text:
00D31BE6 B9 01 00 00 00 mov ecx, 1.text:
00D31BEB D1 E1 shl ecx, 1.text:
00D31BED B8 04 00 00 00 mov eax, 4.text:
00D31BF2 BB 01 00 00 00 mov ebx, 1.text:
00D31BF7 33 D2 xor edx, edx.text:
00D31BF9 8B 12 mov edx, [edx].text:
00D31BFB B9 01 00 00 00 mov ecx, 1.text:
00D31C00 C1 E1 05 shl ecx, 5.text:
00D31C03 B8 01 00 00 00 mov eax, 1.text:
00D31C08 33 D2 xor edx, edx.text:
00D31C0A 8B 12 mov edx, [edx].text:
00D31C0C B9 01 00 00 00 mov ecx, 1.text:
00D31C11 C1 E1 05 shl ecx, 5.text:
00D31C14 CC int 3 ; Trap to Debugger.text:
00D31C15 B9 01 00 00 00 mov ecx, 1.text:
00D31C1A D1 E1 shl ecx, 1.text:
00D31C1C B8 09 00 00 00 mov eax, 9.text:
00D31C21 BB 01 00 00 00 mov ebx, 1.text:
00D31C26 33 D2 xor edx, edx.text:
00D31C28 8B 12 mov edx, [edx].text:
00D31C2A B9 01 00 00 00 mov ecx, 1.text:
00D31C2F C1 E1 03 shl ecx, 3.text:
00D31C32 CC int 3 ; Trap to Debugger.text:
00D31C33 61 popa

可以发现，这些代码中正好只操作了三个寄存器：eax/ebx/ecx。根据这些代码写一个小脚本模拟执行，来对应异常处理的vm指令。

ins=['mov','ecx','1','shl','ecx','3','mov','eax','2','mov','ebx','9','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','1','mov','eax','4','int','3','mov','ecx','1','shl','ecx','2','mov','eax','0','int','3','mov','ecx','1','shl','ecx','1','mov','eax','0','mov','ebx','-1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','0','mov','ebx','6','int','3','mov','ecx','1','mov','eax','0','mov','ebx','5','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','mov','eax','1','mov','ebx','0','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','1','mov','ebx','2','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','2','int','3','mov','ecx','1','shl','ecx','1','mov','eax','4','mov','ebx','-1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','mov','eax','15','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','0','mov','ebx','6','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','1','mov','eax','0','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','mov','eax','1','mov','ebx','0','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','1','mov','ebx','2','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','2','int','3','mov','ecx','1','shl','ecx','1','mov','eax','5','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','mov','eax','8','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','0','mov','ebx','6','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','1','mov','eax','0','mov','ebx','-1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','mov','eax','1','mov','ebx','0','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','1','mov','ebx','2','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','2','int','3','mov','ecx','1','shl','ecx','1','mov','eax','4','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','mov','eax','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','int','3','mov','ecx','1','shl','ecx','1','mov','eax','9','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','int','3','popa',]def ROL(i,index): tmp = bin(i)[2:].rjust(8, "0") for _ in range(index): tmp = tmp[1:] + tmp[0] return int(tmp, 2) CONTEXT = { 'eax' : 0, 'ebx' : 0, 'ecx' : 0, 'edx' : 0}round = 0eip = 0while True: #print(str(CONTEXT['eax']) +','+ str(CONTEXT['ebx']) +','+ str(CONTEXT['ecx']) +','+ str(CONTEXT['edx'] )) if(ins[eip] == 'mov'): if(ins[eip+2][0] =='['): #print('0xC0000005' +','+ str(CONTEXT['eax']) +','+ str(CONTEXT['ebx']) +','+ str(CONTEXT['ecx']) +','+ str(CONTEXT['edx'] )+ ',' ) if(CONTEXT['ecx'] == 1): print('sub_D33570('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 1 elif(CONTEXT['ecx'] == 2): print('sub_D335B0('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 4): print('sub_D335E0('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 8): print('sub_D33610('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 16): print('sub_D33640('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 32): print('sub_D33680('+str(CONTEXT['eax'])+');') #do 2 else: #if(ins[eip+1] == 'eax' or ins[eip+1] == 'ebx' or ins[eip+1] == 'ecx' or ins[eip+1] == 'edx') CONTEXT[ins[eip+1]] = int(ins[eip+2]) elif(ins[eip] == 'shl'): CONTEXT[ins[eip+1]] = CONTEXT[ins[eip+1]] << int(ins[eip+2]) elif(ins[eip] == 'xor'): CONTEXT[ins[eip+1]] = CONTEXT[ins[eip+1]] ^ CONTEXT[ins[eip+2]] elif(ins[eip] == 'int'): eip = eip -1 #print('0x80000003' +','+ str(CONTEXT['eax']) +','+ str(CONTEXT['ebx']) +','+ str(CONTEXT['ecx']) +','+ str(CONTEXT['edx'] )+ ',' ) if(CONTEXT['ecx'] == 1): print('sub_D336A0('+str(CONTEXT['eax'])+');') elif(CONTEXT['ecx'] == 2): print('sub_D336D0('+str(CONTEXT['eax'])+');') elif(CONTEXT['ecx'] == 4): print('sub_D33720('+str(CONTEXT['eax'])+');') elif(CONTEXT['ecx'] == 8): print('CorrectOutput();') elif(CONTEXT['ecx'] == 16): print('sub_D33800('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') elif(CONTEXT['ecx'] == 32): print('WrongOutput();') #do elif(ins[eip] == 'popa'): eip = -3 round = round + 1 if(round == 19):
break #break #do eip = eip + 3

sub_D33610(2, 9);sub_D336D0(4);sub_D33720(0);sub_D335B0(0, -1);sub_D33800(0, 6);sub_D33570(0, 5);sub_D33610(1, 0);sub_D33640(1, 2);sub_D336A0(2);sub_D335B0(4, -1);sub_D33680(15);sub_D33570(0, 6);sub_D335B0(0, 1);sub_D33610(1, 0);sub_D33640(1, 2);sub_D336A0(2);sub_D335B0(5, 1);sub_D33680(8);sub_D33570(0, 6);sub_D335B0(0, -1);sub_D33610(1, 0);sub_D33640(1, 2);sub_D336A0(2);sub_D335B0(4, 1);sub_D33680(1);WrongOutput();sub_D335B0(9, 1);CorrectOutput();

五

VM

得到了执行流，接下来的工作就是对执行流进行逆向。首先，执行流所使用的函数有几种。

EXCEPTION_BREAKPOINTcase 1u:
sub_D336A0(_eax);case 2u:
sub_D336D0(_eax);case 4u:
sub_D33720(_eax);case 8u:
_CorrectOutput();case 0x10u:
sub_D33800(_eax, _ebx);case 0x20u:
_WrongOutput(); EXCEPTION_ACCESS_VIOLATIONcase 1u:
sub_D33570(_eax, _ebx);case 2u:
sub_D335B0(_eax, _ebx);case 4u:
sub_D335E0(_eax, _ebx);case 8u:
sub_D33610(_eax, _ebx);case 0x10u:
cmp(_eax, _ebx);case 0x20u:
sub_D33680(_eax);

以及其操作的变量有dword_427B90、byte_427BBC、dword_427BC0。其中dword_427B90具有初始值。

这些“原子”操作的逆向很简单，其对应的指令如下：

EXCEPTION_BREAKPOINTcase 1u:
jnz(_eax);case 2u:
push(_eax);case 4u:
pop(_eax);case 8u:
_CorrectOutput();case 0x10u:
mul(_eax, _ebx);case 0x20u:
_WrongOutput(); EXCEPTION_ACCESS_VIOLATIONcase 1u:
add(_eax, _ebx);case 2u:
addn(_eax, _ebx); //直接访存case 4u:
store(_eax, _ebx);case 8u:
load(_eax, _ebx);case 0x10u:
cmp(_eax, _ebx);case 0x20u:
jmp(_eax);

修改这些函数名，再次运行上面的脚本：

load(2, 9);push(4);pop(0);addn(0, -1);mul(0, 6);add(0, 5);load(1, 0);cmp(1, 2);jnz(2);addn(4, -1);jmp(15);add(0, 6);addn(0, 1);load(1, 0);cmp(1, 2);jnz(2);addn(5, 1);jmp(8);add(0, 6);addn(0, -1);load(1, 0);cmp(1, 2);jnz(2);addn(4, 1);jmp(1);WrongOutput();addn(9, 1);CorrectOutput();

分析上面的执行流，可以知道这个执行流的逻辑极其简单。其从byte_426B90中读取数据并寻找这个数据，判断迷宫。换句话说可以认为，输入的数据首先要在byte_426B90的范围内，如果数据和迷宫的字节相同，则往那个方向走一步。如果没有就报错，如果走错了也报错。byte_426B90的初始化是一个迷宫。走迷宫的规则在TLS函数里，其规则很简单，只需要依据奇数走迷宫即可。

而我们被处理的输入，在.text:
00401346的memmove(&unk_426C58, &Str1, 0x13u);被放置在unk_426C58中，这个变量其实是byte_426B90的第0xC8位置。（0xC8同时也是dword_427B90[9]的值）。迷宫有dword_427B90[6] = 12行，初始位置坐标为(5,0)（dword_427B90[4] = 5;dword_427B90[5] = 0;)

六

SOLVE!

知道上面这些所有的信息，打开我们最初找到的初始化部分sub_401000，把数据导出并按照12行排列，走迷宫喽！

reverse3.exe是题目。
reverse3.exe.idb为笔者自己分析的IDA数据库文件，版本IDA75。

看雪ID：Hedione

https://bbs.pediy.com/user-home-923183.htm

*本文由看雪论坛 Hedione 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
前言
二
FISRT GLANCE
int __cdecl sub_401D10(_BYTE *a1, char a2){ int result; // eax do { *a1++ ^= a2; result = (unsigned __int8)*a1; } while ( *a1 ); return result;}
三
地址转换机构：sub_4011F0
.text:
004011BD 58 pop eax.text:
004011BE 58 pop eax.text:
004011BF 33 C0 xor eax, eax.text:
004011C1 83 F0 03 xor eax, 3.text:
004011C4 E8 00 00 00 00 call $+5.text:
004011C9 F7 E0 mul eax.text:
004011CB 83 F8 51 cmp eax, 51h ; 'Q'.text:
004011CE 74 01 jz short loc_4011D1.text:
004011D0 C3 retn.text:
004011D1 ; ---------------------------------------------------------------------------.text:
004011D1.text:
004011D1 loc_4011D1: ; CODE XREF: sub_401170+5E↑j.text:
004011D1 83 E8 21 sub eax, 21h ; '!'.text:
004011D4 64 8B 00 mov eax, fs:[eax].text:
004011D7 8B 40 0C mov eax, [eax+0Ch].text:
004011DA 8B 40 0C mov eax, [eax+0Ch].text:
004011DD 8B 00 mov eax, [eax].text:
004011DF 8B 00 mov eax, [eax].text:
004011E1 8B 40 18 mov eax, [eax+18h].text:
004011E4 5D pop ebp.text:
004011E5 C3 retn
四
子母进程调试及异常处理
.text:
00D31A38 60 pusha.text:
00D31A39 B9 01 00 00 00 mov ecx, 1.text:
00D31A3E C1 E1 03 shl ecx, 3.text:
00D31A41 B8 02 00 00 00 mov eax, 2.text:
00D31A46 BB 09 00 00 00 mov ebx, 9.text:
00D31A4B 33 D2 xor edx, edx.text:
00D31A4D 8B 12 mov edx, [edx].text:
00D31A4F B9 01 00 00 00 mov ecx, 1.text:
00D31A54 D1 E1 shl ecx, 1.text:
00D31A56 B8 04 00 00 00 mov eax, 4.text:
00D31A5B CC int 3 ; Trap to Debugger.text:
00D31A5C B9 01 00 00 00 mov ecx, 1.text:
00D31A61 C1 E1 02 shl ecx, 2.text:
00D31A64 B8 00 00 00 00 mov eax, 0.text:
00D31A69 CC int 3 ; Trap to Debugger.text:
00D31A6A B9 01 00 00 00 mov ecx, 1.text:
00D31A6F D1 E1 shl ecx, 1.text:
00D31A71 B8 00 00 00 00 mov eax, 0.text:
00D31A76 BB FF FF FF FF mov ebx, 0FFFFFFFFh.text:
00D31A7B 33 D2 xor edx, edx.text:
00D31A7D 8B 12 mov edx, [edx].text:
00D31A7F B9 01 00 00 00 mov ecx, 1.text:
00D31A84 C1 E1 04 shl ecx, 4.text:
00D31A87 B8 00 00 00 00 mov eax, 0.text:
00D31A8C BB 06 00 00 00 mov ebx, 6.text:
00D31A91 CC int 3 ; Trap to Debugger.text:
00D31A92 B9 01 00 00 00 mov ecx, 1.text:
00D31A97 B8 00 00 00 00 mov eax, 0.text:
00D31A9C BB 05 00 00 00 mov ebx, 5.text:
00D31AA1 33 D2 xor edx, edx.text:
00D31AA3 8B 12 mov edx, [edx].text:
00D31AA5 B9 01 00 00 00 mov ecx, 1.text:
00D31AAA C1 E1 03 shl ecx, 3.text:
00D31AAD B8 01 00 00 00 mov eax, 1.text:
00D31AB2 BB 00 00 00 00 mov ebx, 0.text:
00D31AB7 33 D2 xor edx, edx.text:
00D31AB9 8B 12 mov edx, [edx].text:
00D31ABB B9 01 00 00 00 mov ecx, 1.text:
00D31AC0 C1 E1 04 shl ecx, 4.text:
00D31AC3 B8 01 00 00 00 mov eax, 1.text:
00D31AC8 BB 02 00 00 00 mov ebx, 2.text:
00D31ACD 33 D2 xor edx, edx.text:
00D31ACF 8B 12 mov edx, [edx].text:
00D31AD1 B9 01 00 00 00 mov ecx, 1.text:
00D31AD6 B8 02 00 00 00 mov eax, 2.text:
00D31ADB CC int 3 ; Trap to Debugger.text:
00D31ADC B9 01 00 00 00 mov ecx, 1.text:
00D31AE1 D1 E1 shl ecx, 1.text:
00D31AE3 B8 04 00 00 00 mov eax, 4.text:
00D31AE8 BB FF FF FF FF mov ebx, 0FFFFFFFFh.text:
00D31AED 33 D2 xor edx, edx.text:
00D31AEF 8B 12 mov edx, [edx].text:
00D31AF1 B9 01 00 00 00 mov ecx, 1.text:
00D31AF6 C1 E1 05 shl ecx, 5.text:
00D31AF9 B8 0F 00 00 00 mov eax, 0Fh.text:
00D31AFE 33 D2 xor edx, edx.text:
00D31B00 8B 12 mov edx, [edx].text:
00D31B02 B9 01 00 00 00 mov ecx, 1.text:
00D31B07 B8 00 00 00 00 mov eax, 0.text:
00D31B0C BB 06 00 00 00 mov ebx, 6.text:
00D31B11 33 D2 xor edx, edx.text:
00D31B13 8B 12 mov edx, [edx].text:
00D31B15 B9 01 00 00 00 mov ecx, 1.text:
00D31B1A D1 E1 shl ecx, 1.text:
00D31B1C B8 00 00 00 00 mov eax, 0.text:
00D31B21 BB 01 00 00 00 mov ebx, 1.text:
00D31B26 33 D2 xor edx, edx.text:
00D31B28 8B 12 mov edx, [edx].text:
00D31B2A B9 01 00 00 00 mov ecx, 1.text:
00D31B2F C1 E1 03 shl ecx, 3.text:
00D31B32 B8 01 00 00 00 mov eax, 1.text:
00D31B37 BB 00 00 00 00 mov ebx, 0.text:
00D31B3C 33 D2 xor edx, edx.text:
00D31B3E 8B 12 mov edx, [edx].text:
00D31B40 B9 01 00 00 00 mov ecx, 1.text:
00D31B45 C1 E1 04 shl ecx, 4.text:
00D31B48 B8 01 00 00 00 mov eax, 1.text:
00D31B4D BB 02 00 00 00 mov ebx, 2.text:
00D31B52 33 D2 xor edx, edx.text:
00D31B54 8B 12 mov edx, [edx].text:
00D31B56 B9 01 00 00 00 mov ecx, 1.text:
00D31B5B B8 02 00 00 00 mov eax, 2.text:
00D31B60 CC int 3 ; Trap to Debugger.text:
00D31B61 B9 01 00 00 00 mov ecx, 1.text:
00D31B66 D1 E1 shl ecx, 1.text:
00D31B68 B8 05 00 00 00 mov eax, 5.text:
00D31B6D BB 01 00 00 00 mov ebx, 1.text:
00D31B72 33 D2 xor edx, edx.text:
00D31B74 8B 12 mov edx, [edx].text:
00D31B76 B9 01 00 00 00 mov ecx, 1.text:
00D31B7B C1 E1 05 shl ecx, 5.text:
00D31B7E B8 08 00 00 00 mov eax, 8.text:
00D31B83 33 D2 xor edx, edx.text:
00D31B85 8B 12 mov edx, [edx].text:
00D31B87 B9 01 00 00 00 mov ecx, 1.text:
00D31B8C B8 00 00 00 00 mov eax, 0.text:
00D31B91 BB 06 00 00 00 mov ebx, 6.text:
00D31B96 33 D2 xor edx, edx.text:
00D31B98 8B 12 mov edx, [edx].text:
00D31B9A B9 01 00 00 00 mov ecx, 1.text:
00D31B9F D1 E1 shl ecx, 1.text:
00D31BA1 B8 00 00 00 00 mov eax, 0.text:
00D31BA6 BB FF FF FF FF mov ebx, 0FFFFFFFFh.text:
00D31BAB 33 D2 xor edx, edx.text:
00D31BAD 8B 12 mov edx, [edx].text:
00D31BAF B9 01 00 00 00 mov ecx, 1.text:
00D31BB4 C1 E1 03 shl ecx, 3.text:
00D31BB7 B8 01 00 00 00 mov eax, 1.text:
00D31BBC BB 00 00 00 00 mov ebx, 0.text:
00D31BC1 33 D2 xor edx, edx.text:
00D31BC3 8B 12 mov edx, [edx].text:
00D31BC5 B9 01 00 00 00 mov ecx, 1.text:
00D31BCA C1 E1 04 shl ecx, 4.text:
00D31BCD B8 01 00 00 00 mov eax, 1.text:
00D31BD2 BB 02 00 00 00 mov ebx, 2.text:
00D31BD7 33 D2 xor edx, edx.text:
00D31BD9 8B 12 mov edx, [edx].text:
00D31BDB B9 01 00 00 00 mov ecx, 1.text:
00D31BE0 B8 02 00 00 00 mov eax, 2.text:
00D31BE5 CC int 3 ; Trap to Debugger.text:
00D31BE6 B9 01 00 00 00 mov ecx, 1.text:
00D31BEB D1 E1 shl ecx, 1.text:
00D31BED B8 04 00 00 00 mov eax, 4.text:
00D31BF2 BB 01 00 00 00 mov ebx, 1.text:
00D31BF7 33 D2 xor edx, edx.text:
00D31BF9 8B 12 mov edx, [edx].text:
00D31BFB B9 01 00 00 00 mov ecx, 1.text:
00D31C00 C1 E1 05 shl ecx, 5.text:
00D31C03 B8 01 00 00 00 mov eax, 1.text:
00D31C08 33 D2 xor edx, edx.text:
00D31C0A 8B 12 mov edx, [edx].text:
00D31C0C B9 01 00 00 00 mov ecx, 1.text:
00D31C11 C1 E1 05 shl ecx, 5.text:
00D31C14 CC int 3 ; Trap to Debugger.text:
00D31C15 B9 01 00 00 00 mov ecx, 1.text:
00D31C1A D1 E1 shl ecx, 1.text:
00D31C1C B8 09 00 00 00 mov eax, 9.text:
00D31C21 BB 01 00 00 00 mov ebx, 1.text:
00D31C26 33 D2 xor edx, edx.text:
00D31C28 8B 12 mov edx, [edx].text:
00D31C2A B9 01 00 00 00 mov ecx, 1.text:
00D31C2F C1 E1 03 shl ecx, 3.text:
00D31C32 CC int 3 ; Trap to Debugger.text:
00D31C33 61 popa
ins=['mov','ecx','1','shl','ecx','3','mov','eax','2','mov','ebx','9','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','1','mov','eax','4','int','3','mov','ecx','1','shl','ecx','2','mov','eax','0','int','3','mov','ecx','1','shl','ecx','1','mov','eax','0','mov','ebx','-1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','0','mov','ebx','6','int','3','mov','ecx','1','mov','eax','0','mov','ebx','5','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','mov','eax','1','mov','ebx','0','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','1','mov','ebx','2','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','2','int','3','mov','ecx','1','shl','ecx','1','mov','eax','4','mov','ebx','-1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','mov','eax','15','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','0','mov','ebx','6','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','1','mov','eax','0','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','mov','eax','1','mov','ebx','0','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','1','mov','ebx','2','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','2','int','3','mov','ecx','1','shl','ecx','1','mov','eax','5','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','mov','eax','8','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','0','mov','ebx','6','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','1','mov','eax','0','mov','ebx','-1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','mov','eax','1','mov','ebx','0','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','4','mov','eax','1','mov','ebx','2','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','mov','eax','2','int','3','mov','ecx','1','shl','ecx','1','mov','eax','4','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','mov','eax','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','5','int','3','mov','ecx','1','shl','ecx','1','mov','eax','9','mov','ebx','1','xor','edx','edx','mov','edx','[edx]','mov','ecx','1','shl','ecx','3','int','3','popa',]def ROL(i,index): tmp = bin(i)[2:].rjust(8, "0") for _ in range(index): tmp = tmp[1:] + tmp[0] return int(tmp, 2) CONTEXT = { 'eax' : 0, 'ebx' : 0, 'ecx' : 0, 'edx' : 0}round = 0eip = 0while True: #print(str(CONTEXT['eax']) +','+ str(CONTEXT['ebx']) +','+ str(CONTEXT['ecx']) +','+ str(CONTEXT['edx'] )) if(ins[eip] == 'mov'): if(ins[eip+2][0] =='['): #print('0xC0000005' +','+ str(CONTEXT['eax']) +','+ str(CONTEXT['ebx']) +','+ str(CONTEXT['ecx']) +','+ str(CONTEXT['edx'] )+ ',' ) if(CONTEXT['ecx'] == 1): print('sub_D33570('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 1 elif(CONTEXT['ecx'] == 2): print('sub_D335B0('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 4): print('sub_D335E0('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 8): print('sub_D33610('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 16): print('sub_D33640('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') #do 2 elif(CONTEXT['ecx'] == 32): print('sub_D33680('+str(CONTEXT['eax'])+');') #do 2 else: #if(ins[eip+1] == 'eax' or ins[eip+1] == 'ebx' or ins[eip+1] == 'ecx' or ins[eip+1] == 'edx') CONTEXT[ins[eip+1]] = int(ins[eip+2]) elif(ins[eip] == 'shl'): CONTEXT[ins[eip+1]] = CONTEXT[ins[eip+1]] << int(ins[eip+2]) elif(ins[eip] == 'xor'): CONTEXT[ins[eip+1]] = CONTEXT[ins[eip+1]] ^ CONTEXT[ins[eip+2]] elif(ins[eip] == 'int'): eip = eip -1 #print('0x80000003' +','+ str(CONTEXT['eax']) +','+ str(CONTEXT['ebx']) +','+ str(CONTEXT['ecx']) +','+ str(CONTEXT['edx'] )+ ',' ) if(CONTEXT['ecx'] == 1): print('sub_D336A0('+str(CONTEXT['eax'])+');') elif(CONTEXT['ecx'] == 2): print('sub_D336D0('+str(CONTEXT['eax'])+');') elif(CONTEXT['ecx'] == 4): print('sub_D33720('+str(CONTEXT['eax'])+');') elif(CONTEXT['ecx'] == 8): print('CorrectOutput();') elif(CONTEXT['ecx'] == 16): print('sub_D33800('+str(CONTEXT['eax'])+', '+str(CONTEXT['ebx'])+');') elif(CONTEXT['ecx'] == 32): print('WrongOutput();') #do elif(ins[eip] == 'popa'): eip = -3 round = round + 1 if(round == 19):
break #break #do eip = eip + 3
sub_D33610(2, 9);sub_D336D0(4);sub_D33720(0);sub_D335B0(0, -1);sub_D33800(0, 6);sub_D33570(0, 5);sub_D33610(1, 0);sub_D33640(1, 2);sub_D336A0(2);sub_D335B0(4, -1);sub_D33680(15);sub_D33570(0, 6);sub_D335B0(0, 1);sub_D33610(1, 0);sub_D33640(1, 2);sub_D336A0(2);sub_D335B0(5, 1);sub_D33680(8);sub_D33570(0, 6);sub_D335B0(0, -1);sub_D33610(1, 0);sub_D33640(1, 2);sub_D336A0(2);sub_D335B0(4, 1);sub_D33680(1);WrongOutput();sub_D335B0(9, 1);CorrectOutput();
五
VM
EXCEPTION_BREAKPOINTcase 1u:
sub_D336A0(_eax);case 2u:
sub_D336D0(_eax);case 4u:
sub_D33720(_eax);case 8u:
_CorrectOutput();case 0x10u:
sub_D33800(_eax, _ebx);case 0x20u:
_WrongOutput(); EXCEPTION_ACCESS_VIOLATIONcase 1u:
sub_D33570(_eax, _ebx);case 2u:
sub_D335B0(_eax, _ebx);case 4u:
sub_D335E0(_eax, _ebx);case 8u:
sub_D33610(_eax, _ebx);case 0x10u:
cmp(_eax, _ebx);case 0x20u:
sub_D33680(_eax);
EXCEPTION_BREAKPOINTcase 1u:
jnz(_eax);case 2u:
push(_eax);case 4u:
pop(_eax);case 8u:
_CorrectOutput();case 0x10u:
mul(_eax, _ebx);case 0x20u:
_WrongOutput(); EXCEPTION_ACCESS_VIOLATIONcase 1u:
add(_eax, _ebx);case 2u:
addn(_eax, _ebx); //直接访存case 4u:
store(_eax, _ebx);case 8u:
load(_eax, _ebx);case 0x10u:
cmp(_eax, _ebx);case 0x20u:
jmp(_eax);
load(2, 9);push(4);pop(0);addn(0, -1);mul(0, 6);add(0, 5);load(1, 0);cmp(1, 2);jnz(2);addn(4, -1);jmp(15);add(0, 6);addn(0, 1);load(1, 0);cmp(1, 2);jnz(2);addn(5, 1);jmp(8);add(0, 6);addn(0, -1);load(1, 0);cmp(1, 2);jnz(2);addn(4, 1);jmp(1);WrongOutput();addn(9, 1);CorrectOutput();
六
SOLVE!
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/10-1671714688.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1671714688.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1671714689.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671714690.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1671714690.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1671714691.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671714692.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1671714693.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1671714693.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/10-1671714693.png)