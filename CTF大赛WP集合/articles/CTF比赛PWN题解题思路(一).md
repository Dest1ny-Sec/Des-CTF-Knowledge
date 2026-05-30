# CTF比赛PWN题解题思路(一)

> 原文: https://www.ctfiot.com/201125.html
> ID: 201125

题目一

运行程序如下，输入1，提示no username

用IDA对程序进行逆向，需要输入admin才能继续

程序漏洞点是在输入用户名的地方存在栈溢出

方法一

使用gdb进行调试，在main函数处设置断点

单步调试（ni）到func函数处，进行步入(si)

单步调试到名字输入的位置

输入足够长度的字符串

计算引起溢出的字符串长度，有两种方法，第一种包括admin所以长度为56

将返回地址覆盖成程序中我们想让其返回的地址，这里我们通过IDA查找危险函数

这里有危险的shell函数，地址为0x405D36, 因为小端存储，因此我们需要写入365D40，字符串为6]@

最终payload为admin+51个字符+6]@，成功获得shell

方法二

根据变量长度计算空间大小，再加上8比特，编写脚本

题目二

首先查看伪代码，栈空间建议使用gdb进行调试，伪代码查看可能不准确

程序最终的判断是v7和v5相等即可得到shell，v7是程序里的，v5是我们的输入，然后这里data可以输入0xc0个字节，这里可以覆盖v7的地址空间。

因此本题的解题思路是输入data，覆盖掉v7，然后输入已知的数据，获得shell。

编写脚本获得shell

题目三

查看伪代码 gets处存在栈溢出，必须首先输入设定的字符串

但是溢出后的返回地址，程序里面并没有明显的shell，但是有bin/sh字符串和system函数可以利用

获取RDI地址

编写脚本获得shell

题目四

类似于题目三，不同点在于没有/bin/sh字符，需要使用gets函数写入

使用gdb调试，vmmap命令获得可写的地址空间

编写脚本写入/bin/sh

获得shell

原文始发于微信公众号（小话安全）：CTF比赛PWN题解题思路(一)

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1724501973.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1724501973.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1724501974.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1724501974.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1724501975.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1724501976.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1724501977.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1724501977.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1724501978.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1724501978.png)