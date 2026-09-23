---
title: 2024 西湖论剑 Qrohttre（Windows 调试器实现父子进程同步 + SMC）
contest: 2024 西湖论剑
year: 2024
difficulty: hard
vuln_type:
- reverse
- misc_unknown
tags:
- Qrohttre 父子进程同步调试
- DEBUG_PROCESS CreateProcessA
- 0xCC 断点同步用户输入
- TF 单步异常
- f_OnBreakPoint_4070A0 + f_OnSingleStep_407530
- f_OnAccessViolation_406710
- ZwSetInformationThread ThreadHideFromDebugger 0x11 反调试
- 双段 SMC 自解密
- CE dump 40B991-40DDB4 内存 patch 回 QrohttreSub.exe
- WriteProcessMemory 回写垃圾
attack_chain:
- 主进程 CreateProcessA DEBUG_PROCESS 创建子进程
- 子进程入口点 INT3（0xCC）断点
- '主进程 f_OnBreakPoint_4070A0: 同步用户输入到子进程 + 设置 TF 单步标志'
- 子进程单步异常 → 主进程 f_OnSingleStep_407530 解密下一条指令 + 上条指令写垃圾
- ZwSetInformationThread(ThreadHideFromDebugger) 反调试
- 找到第二段 SMC 起始位置 0x40B991，patch 掉 WriteProcessMemory 回写
- CE dump 子进程 40B991-40DDB4 解密代码
- patch 到 QrohttreSub.exe 静态分析
- 触发访问越权异常 (读写操作数未完全解密)，分发 f_OnAccessViolation_406710 还原地址
key_payload: CreateProcessA(..., DEBUG_PROCESS, ...); f_OnSingleStep_407530
one_liner: Qrohttre 主进程用 Win32 DEBUG_PROCESS 调试子进程，TF 单步 + 双段 SMC 自解密 + 0xCC 断点同步用户输入；patch WriteProcessMemory + CE dump + 父子进程双 IDA patch 是分析套路。
lesson: Win32 调试 API（DEBUG_PROCESS + TF 单步 + 0xCC 断点）实现父子进程同步通信是 Windows 高级逆向题，patch 掉 WriteProcessMemory 回写 + CE dump 是核心套路；反调试 ThreadHideFromDebugger 用 ZwSetInformationThread(0x11) 设线程。
quality: high
full_path: 2024西湖论剑_Qrohttre：一道windows调试实现同步题.full.md
meta_path: 2024西湖论剑_Qrohttre：一道windows调试实现同步题.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 西湖论剑 Qrohttre（Windows 调试器实现父子进程同步 + SMC）。Qrohttre 主进程用 Win32 DEBUG_PROCESS 调试子进程，TF 单步 + 双段 SMC 自解密 + 0xCC 断点同步用户输入；patch WriteProcessMemory + CE dump + 父子进程双 IDA patch 是分析套路。。关键路径：主进程 CreateP...
category: reverse
subcategory: reverse
subcategories:
- reverse
- misc_other
tools_used:
- IDA
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/172527.html
reasoning_chain:
- '[触发点] 主进程用 CreateProcessA(..., DEBUG_PROCESS, ...) → 假设：父子进程同步调试通信 → [动作] IDA 静态分析 f_main_40DE18 看 GetStartupInfoA → [观察] 主进程调试子进程 → [下一步] 分析调试事件分发'
- '[触发点] f_OnException_406FA0 分发 BP/SingleStep/AccessViolation → 假设：TF 单步 + 0xCC 断点触发 → [动作] IDA 看 f_OnBreakPoint_4070A0 同步输入 → [观察] 父子进程数据通过 0x414008/0x41400C 同步 → [下一步] 分析 SMC'
- '[触发点] 0xCC 断点 + 子进程 40B991-40DDB4 自解密 → 假设：WriteProcessMemory 回写加密段 → [动作] patch 第二个 WriteProcessMemory 回写 + CE dump 40B991-40DDB4 → [观察] 得到解密后代码 → [下一步] IDA patch 到 QrohttreSub.exe'
- '[触发点] 反调试 ThreadHideFromDebugger (ZwSetInformationThread 0x11) → 假设：父进程阻止被调试 → [动作] IDA 跳过 ZwSetInformationThread 调用 → [观察] 父进程可被调试'
- '[触发点] 48 段子进程代码 + f_main_40DE18 比较 dword_414490 == arr414010 → 假设：z3 还原 48 个 v414008 → [动作] Python z3 solver + 30<=v414008[i]<=127 → [观察] DASCTF{cTkBnLT6gA8H_sX7Q2VMBMAtl9PZvojBPnSTH7J7aNHeStxN}'
failed_attempts:
- 试图用 WinDbg 跟子进程 → 失败：父进程 ThreadHideFromDebugger 阻止调试
- 试图直接看 IDA 反编译 40B991 → 失败：操作数是错的，需 dump 出解密后代码
- 试图读 idx 映射关系 → 失败：直接读 eax 在 0x40730B 断点处更简单
key_observations:
- Win32 调试 API（DEBUG_PROCESS + TF 单步 + 0xCC 断点）实现父子进程同步通信是 Windows 高级逆向题
- patch 掉 WriteProcessMemory 回写 + CE dump 是核心套路
- 反调试 ThreadHideFromDebugger 用 ZwSetInformationThread(0x11) 设线程
- 父子进程数据通过共享内存区（414008/41400C）同步
prerequisites:
- Win32 调试 API（CreateProcessA DEBUG_PROCESS / ContinueDebugEvent / DEBUG_EVENT）
- SMC 自解密 + WriteProcessMemory
- z3 solver 还原非线性约束
- 反调试 ZwSetInformationThread / ThreadHideFromDebugger
---
# 2024西湖论剑 Qrohttre：一道windows调试实现同步题

> 原文: https://www.ctfiot.com/172527.html
> ID: 172527

一

第一段smc

字符串搜输出内容，有个假的校验，下断点断不下来。断scanf跟踪，返回到40DFDE，动态静态代码不一致，smc。

解密代码：

加密段是0x40DE77~0x40e2bb。

二

利用调试技术实现进程同步通信

主进程以调试模式创建子进程，子进程执行相同的程序：

GetModuleFileNameA(0, Filename, 0x104u);GetStartupInfoA(&StartupInfo);v9 = CreateProcessA(Filename, 0, 0, 0, 1, DEBUG_PROCESS, 0, 0, &StartupInfo, &ProcessInformation);

主进程等待调试事件。

子进程创建，发生调试事件控制权回到主进程，主进程 在子进程入口点设置0xCC断点。

主进程获取用户输入。主进程恢复子进程运行，继续等待调试事件。

子进程运行至入口点，0xCC断点控制权回到主进程。

f_OnException_406FA0 函数负责分发异常调试事件（处理了断点、单步、访问越权三种不同的异常调试事件）。

0xCC触发的断点异常，分发给f_OnBreakPoint_4070A0函数处理。该函数将用户输入数据同步到子进程，并设置TF位触发单步异常。

主进程 恢复子进程运行，继续等待调试事件。

子进程执行代码，由于TF位被设置，触发单步异常控制权回到主进程，分发给f_OnSingleStep_407530函数处理。

该函数会一直设置TF位，故相当于主进程以单步的方式调试子进程。

该函数中还包括一个反调试，导致主进程无法被继续调试。

#define ThreadHideFromDebugger 0x11ZwSetInformationThread(GetCurrentThread(), ThreadHideFromDebugger, 0, 0);

f_OnSingleStep_407530是主进程步进调试子进程的代码。当检测到子进程运行到第二段SMC时，解码起始16字节的代码。

完成起始16字节代码解密后，子进程每执行一条指令之前，主进程就解密一次后续代码，并往子进程上一条指令填充垃圾数据。

按图片所示，patch掉第二个写回垃圾指令的WriteProcessMemory，然后在图中位置设置断点。执行到断点时（把下面那条Write也执行了）用ark找到子进程pid，用CE dump子进程40B991-40DDB4的解密后的代码。（此处解密不完全，5.1有补充）

加密段是40B991-40DDB4，复制一份程序改名为QrohttreSub.exe，方便分析子进程，ida里把CE dump出来的解密后代码patch到QrohttreSub.exe中。

patch完后，ida识别出QrohttreSub.exe的main函数位于0040B8F0。

通过单步陷阱处理函数（f_OnSingleStep_407530）解密的代码，从40B991开始的指令，操作数是不正确的，还未完全解密。

子进程执行错误操作数的读写指令，触发访问权限异常，控制权再次回到主进程，分发给f_OnAccessViolation_406710。

该函数会读取指令读写的地址（该函数默认指令第2~5字节为读写的地址）。

根据读写地址不同进行处理（详见5.2）。

完整解密过程是：先单步异常，解密指令；再触发内存访问越权，解密操作数

因此4.3图中的断点位置，是解密最后一条指令，恰好最后几条指令是jmp和nop，不会触发内存访问越权，估得到的是正确的解密指令和操作数的代码

经过调试验证，只有读内存的地址是不正确会触发访问越权，然后被修正。

读内存A04DDB2C的指令会被改成读414008。

其余读其他地址指令由sub_4072E0处理，读的地址改为41400C，且父子进程41400C处的数据会被同步修改。

三

读写数据的完整过程

现在可以得出子进程40B991处代码的实际执行过程。这是子进程40B991处完整解密后的部分代码（操作数也解密了）。

表面完全解密后的代码是：（注意v414008[0]相当于是*(v414008+4*0)，而不是*(414008+4*0)）

// 子进程数据int* v414008; // &v414008 = 414008int* v41400C; // &v41400C = 41400C*v41400C = func(v414008[0], v414008[5], v414008[3], ...);

解密操作数前的代码，其中key和A04DDB2C的位置都位于非法地址：

int* vA04DDB2C; // &vA04DDB2C = A04DDB2Cint* key; // &key = valid addressint temp = func(A04DDB2C[0], A04DDB2C[5], A04DDB2C[3], ...);*key = temp;

第一次解密操作数，将A04DDB2C替换成414008：

int* v414008; // &v414008 = 414008int* key; // &key = valid addressint temp = func(v414008[0], v414008[5], v414008[3], ...);*key = temp;

第二次解密操作数，将key替换成41400C，且修改了子进程内存数据：

int* v414008; // &v414008 = 414008int* v41400C; // &v41400C = 41400Cint temp = func(v414008[0], v414008[5], v414008[3], ...);v41400C = 0x414490 + 4*map[key]; // 主进程sub_4072E0修改了子进程41400C处的数据*v41400C = temp;

至此才是正确的执行内容。

四

还原与解密

一共有48段上面这样这样的代码，func很好处理，直接复制然后z3就行。

根据key的不同修改v41400C的值的映射有点麻烦，因为解密指令后得到的错误地址就是key，第二次解密操作数后key就被修改成41400C了。

这里不去获取映射了，直接获取映射后的结果，映射后v41400C的值会被设为4 * idx + 0x414490，代码是按顺序执行的，ida或者x32dbg主进程在40730B处下个断点即可，直接读eax，获取其相对414490的偏移。

读出idx：

idx = [5, 7, 3, 6, 1, 0, 9, 4, 2, 8, 14, 17, 13, 19, 12, 16, 11, 18, 10, 15, 23, 29, 20, 27, 22, 26, 21, 25, 28, 24, 33, 38, 31, 32, 39, 37, 30, 36, 34, 35, 47, 45, 40, 46, 42, 44, 43, 41]

用v414490[idx[i]]依次替换掉sub_40B991中的*v41400C。

回到主进程的f_main_40DE18，最后有一个比较：

ReadProcessMemory(hProcess, &dword_414490, &dword_414490, 0xC0u, 0);
if ( !memcmp(&dword_414490, arr414010, 0xC0u) )
    f_print("Right, the flag is DASCTF{%48s}n", (char)&d_input);
  else
    f_print("Wrong flagn", v3);

读出414010处的48*4字节内容，令其一一等于v414490数组，用z3解出v414008。

from z3 import *

arr414010 = [10055, 1165166, 4294965955, 28964355, 2005, 11801, 4294956681, 5157, 6788, 4294954770, 5381, 6008, 4294962473, 4294962309, 12710, 4294960983, 4294960907, 4294958038, 381186, 4294248290, 7421, 106, 5891, 3564, 338599, 11442, 4294960088, 4941, 1000466, 4294958069, 7857, 557652, 4294953719, 4294957570, 633437, 1639, 4294953318, 4294967085, 4294469914, 4294966863, 11488, 9153, 4294959608, 7942, 5848, 6812, 6688, 4294504346]

v414008 = [BitVec('v414008_{}'.format(i), 32) for i in range(48)]
v414490 = [0 for i in range(48)]

def sub_40B991():
    v414490[5] = (v414008[0] + v414008[5] + v414008[3] - v414008[7]) ^ (v414008[2] * v414008[4] + v414008[6] + v414008[1])
    v414490[7] = (v414008[7] * v414008[0]) ^ (v414008[4] + v414008[5] + v414008[2] - v414008[1]) ^ v414008[6] ^ v414008[3]
    pass # 省略后续部分
    
sub_40B991()

s = Solver()
for i in range(48):
    s.add(v414008[i] >= 30)
    s.add(v414008[i] <= 127)
for i in range(48):
    s.add(v414490[i] == arr414010[i])

if s.check() == sat:
    m = s.model()
    flag = ''
    for i in range(48):
        flag += chr(m[v414008[i]].as_long())
    print('DASCTF{{{}}}'.format(flag))
else:
    print('unsat')
# DASCTF{cTkBnLT6gA8H_sX7Q2VMBMAtl9PZvojBPnSTH7J7aNHeStxN}

看雪ID：wx_御史神风

https://bbs.kanxue.com/user-home-907036.htm

*本文为看雪论坛优秀文章，由 wx_御史神风 原创，转载请注明来自看雪社区

# 往期推荐

1、一次.net cpu爆高分析-windbg sos基本命令使用及分析思路

2、虚假交友APP(信息窃取)逆向分析

3、常见的固件加解密方式与D-Link固件解密实战分析

4、.NET 恶意软件 101：分析 .NET 可执行文件结构

5、CVE-2024-0015复现 (DubheCTF DayDream)

6、Unity的et热更新分析和补丁

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
第一段smc
二
利用调试技术实现进程同步通信
GetModuleFileNameA(0, Filename, 0x104u);GetStartupInfoA(&StartupInfo);v9 = CreateProcessA(Filename, 0, 0, 0, 1, DEBUG_PROCESS, 0, 0, &StartupInfo, &ProcessInformation);
    #define ThreadHideFromDebugger 0x11ZwSetInformationThread(GetCurrentThread(), ThreadHideFromDebugger, 0, 0);
三
读写数据的完整过程
// 子进程数据int* v414008; // &v414008 = 414008int* v41400C; // &v41400C = 41400C*v41400C = func(v414008[0], v414008[5], v414008[3], ...);
int* vA04DDB2C; // &vA04DDB2C = A04DDB2Cint* key; // &key = valid addressint temp = func(A04DDB2C[0], A04DDB2C[5], A04DDB2C[3], ...);*key = temp;
int* v414008; // &v414008 = 414008int* key; // &key = valid addressint temp = func(v414008[0], v414008[5], v414008[3], ...);*key = temp;
int* v414008; // &v414008 = 414008int* v41400C; // &v41400C = 41400Cint temp = func(v414008[0], v414008[5], v414008[3], ...);v41400C = 0x414490 + 4*map[key]; // 主进程sub_4072E0修改了子进程41400C处的数据*v41400C = temp;
四
还原与解密
idx = [5, 7, 3, 6, 1, 0, 9, 4, 2, 8, 14, 17, 13, 19, 12, 16, 11, 18, 10, 15, 23, 29, 20, 27, 22, 26, 21, 25, 28, 24, 33, 38, 31, 32, 39, 37, 30, 36, 34, 35, 47, 45, 40, 46, 42, 44, 43, 41]
ReadProcessMemory(hProcess, &dword_414490, &dword_414490, 0xC0u, 0);
if ( !memcmp(&dword_414490, arr414010, 0xC0u) )
    f_print("Right, the flag is DASCTF{%48s}n", (char)&d_input);
  else
    f_print("Wrong flagn", v3);
from z3 import *

arr414010 = [10055, 1165166, 4294965955, 28964355, 2005, 11801, 4294956681, 5157, 6788, 4294954770, 5381, 6008, 4294962473, 4294962309, 12710, 4294960983, 4294960907, 4294958038, 381186, 4294248290, 7421, 106, 5891, 3564, 338599, 11442, 4294960088, 4941, 1000466, 4294958069, 7857, 557652, 4294953719, 4294957570, 633437, 1639, 4294953318, 4294967085, 4294469914, 4294966863, 11488, 9153, 4294959608, 7942, 5848, 6812, 6688, 4294504346]

v414008 = [BitVec('v414008_{}'.format(i), 32) for i in range(48)]
v414490 = [0 for i in range(48)]

def sub_40B991():
    v414490[5] = (v414008[0] + v414008[5] + v414008[3] - v414008[7]) ^ (v414008[2] * v414008[4] + v414008[6] + v414008[1])
    v414490[7] = (v414008[7] * v414008[0]) ^ (v414008[4] + v414008[5] + v414008[2] - v414008[1]) ^ v414008[6] ^ v414008[3]
    pass # 省略后续部分
    
sub_40B991()

s = Solver()
for i in range(48):
    s.add(v414008[i] >= 30)
    s.add(v414008[i] <= 127)
for i in range(48):
    s.add(v414490[i] == arr414010[i])

if s.check() == sat:
    m = s.model()
    flag = ''
    for i in range(48):
        flag += chr(m[v414008[i]].as_long())
    print('DASCTF{{{}}}'.format(flag))
else:
    print('unsat')
# DASCTF{cTkBnLT6gA8H_sX7Q2VMBMAtl9PZvojBPnSTH7J7aNHeStxN}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]