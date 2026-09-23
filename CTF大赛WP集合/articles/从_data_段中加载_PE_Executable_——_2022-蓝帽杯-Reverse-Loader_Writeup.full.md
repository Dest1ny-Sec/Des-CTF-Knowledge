---
title: 从data段中加载PE Executable——2022蓝帽杯Reverse Loader Writeup
contest: 蓝帽杯 2022 Reverse
year: 2022
difficulty: hard
vuln_type: reverse
tags:
- PE加载器
- 无文件PE
- IAT修复
- Base Relocation
- CRC32
- GetProcAddress
- PEB
- LDR
- InMemoryOrderModuleList
- Pell方程
- big num
- nim
attack_chain:
- VirtualProtect 把 .data 段设为 RWX 加载内嵌 PE dump
- 修改栈顶 rip 跳转到 code+0x34000 主逻辑
- gs:[0x60] 拿 PEB 指针 → PEB:[0x18] 拿 LDR 指针
- LDR:[0x20] 拿 InMemoryOrderModuleList 遍历已加载模块
- 解析 kernel32.dll 的 IMAGE_NT_HEADERS + IMAGE_DATA_DIRECTORY 拿 Export table
- 用 0xEDB88320 多项式 CRC32 校验函数名查 GetProcAddress
- lodsd 取下一个 checksum 循环查 LoadLibraryA
- 处理 Import Table IMAGE_IMPORT_DESCRIPTOR FirstThunk 填绝对地址
- 处理 Base Relocation Table 遍历每个要改写地址加上 code 基址
- 跳转 OEP 后是 nim 编译逻辑：input 解析 big num
- 约束 num1*num1-11*num2*num2 == 9 + big1 < num1 < big2
- sage 算 Pell 方程 x²-11y²=1 连分数收敛子
- 复合 (x1,y1)×(x2,y2) 找 num1 = 3x, num2 = 3y
key_payload: '''flag{%018d%018d}'' % (num1, num2)'
one_liner: 手写 PE Loader 从 .data 段加载无文件 PE，IAT 用 CRC32 查表 + Base Relocation；nim 关键逻辑是 Pell 方程 x²-11y²=1 求解。
lesson: 无文件 PE 加载 = VirtualProtect RWX + 手写 IAT (CRC 查函数名) + Base Relocation; Pell 方程 x²-Dy²=1 用连分数 convergents + 复合群无限解。
quality: high
full_path: 从_data_段中加载_PE_Executable_——_2022-蓝帽杯-Reverse-Loader_Writeup.full.md
meta_path: 从_data_段中加载_PE_Executable_——_2022-蓝帽杯-Reverse-Loader_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 从data段中加载PE Executable——2022蓝帽杯Reverse Loader Writeup。手写 PE Loader 从 .data 段加载无文件 PE，IAT 用 CRC32 查表 + Base Relocation；nim 关键逻辑是 Pell 方程 x²-11y²=1 求解。。关键路径：VirtualProtect 把 .data 段设为 RWX 加载内嵌 PE dum...
category: reverse
subcategory: reverse
tools_used:
- Sage
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/48420.html
reasoning_chain:
- 题目 Loader 从 .data 段加载 PE → 触发点：手写 PE Loader 机制
- VirtualProtect 把 .data 段设为 RWX + 修改栈顶 rip → code+0x34000
- 动作：gs:[0x60] 拿 PEB → PEB:[0x18] 拿 LDR → LDR:[0x20] 拿 InMemoryOrderModuleList
- 假设：遍历已加载模块 → 动作：解析 kernel32.dll 的 IMAGE_NT_HEADERS + IMAGE_DATA_DIRECTORY
- 0xEDB88320 多项式 → CRC32 校验函数名查 GetProcAddress → lodsd 取下一个 checksum
- 处理 Import Table IMAGE_IMPORT_DESCRIPTOR FirstThunk 填绝对地址
- 处理 Base Relocation Table 遍历每个要改写地址 + code 基址
- 跳转 OEP 后 nim 编译逻辑 → input 解析 big num
- 约束 num1*num1-11*num2*num2 == 9 + big1 < num1 < big2
- 动作：sage 算 Pell 方程 x²-11y²=1 连分数收敛子 → 复合 (x1,y1)×(x2,y2) 找 num1 = 3x, num2 = 3y
failed_attempts:
- 试图直接看 .data 段二进制 → 失败：反汇编需要 base relocation
- 试图用 Process Hacker 跟 LoadLibrary → 失败：手写 loader 不调系统
- 试图暴力搜索 Pell 解 → 失败：解太多需组合
key_observations:
- 无文件 PE 加载 = VirtualProtect RWX + 手写 IAT (CRC 查函数名) + Base Relocation
- Pell 方程 x²-Dy²=1 用连分数 convergents + 复合群无限解
- PEB_LDR_DATA.InMemoryOrderModuleList 是无 GetModuleHandle 的标准查询姿势
- CRC32 0xEDB88320 多项式是 CTF shellcode 函数名匹配常用方法
prerequisites:
- PE 文件结构（IMAGE_DOS_HEADER/NT_HEADERS/EXPORT/IMPORT/RELOCATION）
- Pell 方程数论基础
- Sage 数学工具使用
- Windows PEB/LDR 进程内部结构
---
# 从 data 段中加载 PE Executable —— 2022-蓝帽杯-Reverse-Loader Writeup

> 原文: https://www.ctfiot.com/48420.html
> ID: 48420

Brief

这题名为 Loader，其本质也是从 .data 段中加载了程序的主要逻辑并运行，使用了无文件 PE 文件加载的相关技术。

因为这道题没加反调试等 check，所以比赛时我只是略扫了一下 load 的部分，主要精力都放在关键逻辑上了。但其实这题 loader 部分的 assembly 写得很有意思，于是赛后我又着重分析了一下相关部分的代码。

题目整体可以分为两部分：

Loader 首先将 .data 段的权限设置为 RWX ，.data 中数据的是一个进程的 dump，Loader 随后效仿 Windows 加载器来修改 IAT 并对该部分代码进行重定位，随后跳转到其中的 main 函数

关键逻辑：由 nim 语言编译，将输入解析为 big num 再 check

首先，将 .data 段存放的 shellcode 记为 code 变量方便后续表示。

开头的 VirtualProtect 部分较为简单，直接略过。此时控制流来到 code 处，此处的逻辑也很简单，就是通过修改栈顶保存的 rip 让控制流来到 code+0x34000 处，我们直接从此处开始分析。

读取 gs:[0x60] 处的数据。如 Win32 Thread Information Block – Wikipedia 所述，该位置着指向当前进程 PEB 的指针。

读取 PEB:[0x18] 处的数据。偏移及字段的关系可以参考 PEB (geoffchappell.com) ，可知这里是获取的是 LDR 的指针。

进一步读取 LDR:[0x20] 处的数据。该结构体的细节可以参考 PEB_LDR_DATA (geoffchappell.com) ，可知这里获取的是 InMemoryOrderModuleList 的指针

将调用处后面的地址保存到 rsi 中，看来此处的数据并非花指令

访问 IMAGE_DOS_HEADER 的 e_lfanew 字段，该字段代表 IMAGE_NT_HEADERS 与文件头的偏移

访问 IMAGE_NT_HEADERS 的子结构体 IMAGE_OPTIONAL_HEADER 的 IMAGE_DATA_DIRECTORY 字段，对于 kernel32.dll ，该字段就是导出表的 offset

此时 rbx 指向 kernel32.dll 的导出表。后面大量使用的 0x20 偏移处的字段也就是其中的AddressOfNames 字段

首先注意到注意到其中使用了 0xEDB88320 这个 constant。上网搜索发现是一个 CRC 算法中的数字，该算法如下。

rbx+0x20 指向了 Export table 的 AddressOfNames。该字段是一个列表，每个成员是 Export function name 与 PE 文件的偏移，因此此时 rdi 指向了当前校验的函数名，eax 保存着 checksum

当 checksum 与 [rsi] 相等时执行后续代码，否则接着去校验后面的函数名

动调可以发现当 function name 为 GetProcAddress 时校验通过，此时 rdx 寄存器即为 GetProcAddress 的 index，再去访问 Export table 的 AddressOfFunctions 并处理偏移即可得到该函数的绝对地址

此时 rax 即 GetProcAddress 的地址，随后的 push 操作将其压入栈中，lodsd 在取值的同时会让 rsi+=4 ，即指向了下一个要定位的函数的 checksum

当再走完一遍上面的逻辑后，此时栈中已有 LoadLibraryA 和 GetProcAddress 的绝对地址

将 code 中的 IMAGE_NT_HEADERS 的地址保存到 rbp 寄存器中，并寻址到 IMAGE_NT_HEADERS+0x90 处的 Import Table。Import Table 由若干 IMAGE_IMPORT_DESCRIPTOR 构成，其 FirstThunk 字段指向了所有待导入的 API。

加载 dll 文件并获取其 IMAGE_IMPORT_DESCRIPTOR 的地址

通过循环来加载该 dll 中所有被使用到的 API

该 IMAGE_IMPORT_DESCRIPTOR 处理完后再加载其他需要的 dll

获取 Base Relocation Table 的绝对地址，存放到 rdi 中

遍历，对于每个要改写的地址，计算其绝对地址，随后将该地址的值改为 &code + offset

推荐阅读：

Shiro 历史漏洞分析

浅谈pyd文件逆向

CVE-2022-23222漏洞及利用分析

Mimikatz详细使用总结

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
InMemoryOrderModuleList` 是一个双向链表，链接了若干结构体，每个结构体都记录了加载进当前进程空间的一个模块。对于该进程，其链接的顺序是可执行文件，`ntdll.dll`，`kernel32.dll
for ( i = 0; i < len; i++ )
 {
   crc ^= ( input[ i ] );
   for ( k = 8; k; k-- )
   {
     crc = crc & 1 ? ( crc >> 1 ) ^ divisor : crc >> 1;
   }
 }

 return crc ^ 0xFFFFFFFF;
struct Data{
    int64_t f0;
    int64_t f1;
    // data
}
big1 = 0x100000000000000
big2 = 0x1000000000000000
num1 = # input 1
num2 = # input 2
assert(big1 < num1)
assert(num1 < big2)
assert(num1*num1-11*num2*num2 == 9)
sage ./pell.sage
# pell.sage
cf = continued_fraction(sqrt(11))
cs = cf.convergents()

for each in cs:
    x1, y1 = each.numer(), each.denom()
    if x1^2 - 11*y1^2 == 1:
        break

for each in cs[1:]:
    x2, y2 = each.numer(), each.denom()
    if x2^2 - 11*y2^2 == 1:
        break

D = 11
big1 = 0x100000000000000
big2 = 0x1000000000000000

while True:
    x = (x1 * x2 + D * y1 * y2)
    y = (x1 * y2 + x2 * y1)
    if big1 < x * 3 < big2:
        break

    x2, y2 = x1, y1
    x1, y1 = x, y

num1,num2 = x*3,y*3
print('flag{%018d%018d}' % (num1, num2))
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