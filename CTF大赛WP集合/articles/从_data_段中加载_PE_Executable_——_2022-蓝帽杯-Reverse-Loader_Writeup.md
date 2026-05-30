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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/3-1657851692.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/8-1657851693.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/2-1657851694.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/3-1657851694.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/6-1657851695.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/6-1657851695.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/2-1657851696.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/9-1657851696.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/9-1657851697.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/07/5-1657851697.png)