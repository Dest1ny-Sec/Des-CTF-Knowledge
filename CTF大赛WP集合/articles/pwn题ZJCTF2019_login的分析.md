# pwn题ZJCTF2019 login的分析

> 原文: https://www.ctfiot.com/89970.html
> ID: 89970

由于对汇编了解甚少，本不复杂的一题让我学到了很多。

文件一开始需要登录，需要用户名和密码。

先checksec，存在canary。

主函数如下，一眼可以得到密码，下面会慢慢分析。

首先是16行的Admin的构造函数，调用了User的构造函数。

User构建的结构体，包含0x401170处的get_password函数的指针，传入的用户名与密码，它们的上限大小都是0x50。

Admin结构体与User的区别在于指针改为了0x401150，但还是get_password指针。

感觉这个Admin结构体意义不明，但数据结构的构思和我们关系不大就是了
后续可能存在函数指针的利用。

接着看主函数25行的User::read_name，读取输入的0x49个字符，然后赋值给bss段的login+1处，login是一个全局User结构体，实现了名字读入。

接着到了本题的重点，指针v3(实际只被寄存器暂存)存储函数指针main::{lambda(void)#1}::operator,然后经过password_checker得到二级指针v7。

查看password_checker,3*8的数组v2中，在v2处存储了a1(主函数的v3）指针。

看汇编语言更为直观，rax存储了[rbp-0x18]处的地址。

接着是read_password函数，与read_name函数基本一致。

get_password函数很简单。

在看最后的password_checker()前，我们用正确密码测试文件，显示段错误。

查看password_checker,login与admin的密码比较后，来了个奇葩的有毒打印，接着前面的二级函数终于被调用了。

我们需要知道报错原因，gdb调试发现正好是二级指针调用出错。

此外题目中有现成后门。

因此这题的漏洞基本算是送到脸上了，但对汇编不了解的我硬是做了两天。

经过上面的初步分析，我们知道程序在password_checker中调用一个二级指针失败而段错误终止，考虑到canary的存在，srop不可能短期实现。即使我们无法利用这个二级指针getshell，它的存在也会让程序终止。由于存在后门函数，只要能改变这个二级指针，这题就getshell了。

在网上多位师傅博客的参考下，我学会了用汇编溯源的技巧。c语言代码虽然易懂，但最硬核与直接的还是汇编。

调试前我们要明白一个概念：对于一个函数内调用的函数，他们的栈是平行的：由于push rbp; mov rbp, rsp;sub rsp, x子函数的ebp相同，esp根据位移不同而不同。

因此，子函数的栈空间会存在反复利用的情况；如果父函数中出现了子函数栈空间的指针变量，下一次调用子函数时，这个指针变量指向的值就有可能改变！

回到调试，我们观察main函数的汇编，指针存于[rbp-0x130]，它来自于password_checker的rax。

此处与我们初步调试的结果相同，rax的来源是[rbp-0x18]的地址（我原来不明白lea的意思……想了很久）。在最终二级指针调用时，会获得rbp-0x18的值，再获得[rbp-0x18]内的地址。我们可以覆盖后面子函数中[rbp-0x18]的值。

from pwn import *context.log_level = 'debug' io = process('./login')#io = remote('node4.buuoj.cn',25895)#pause()#gdb.attach(io, 'b *0x400b42') io.sendlineafter('username: ', 'admin')payload = b'2jctf_pa5sw0rdx00'.ljust(0x48, b'x61') + p64(0x400e88)io.sendafter('password', payload)io.interactive()

看雪ID：N1co5in3

https://bbs.pediy.com/user-home-945391.htm

*本文由看雪论坛 N1co5in3 原创，转载请注明来自看雪社区

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
from pwn import *context.log_level = 'debug' io = process('./login')#io = remote('node4.buuoj.cn',25895)#pause()#gdb.attach(io, 'b *0x400b42') io.sendlineafter('username: ', 'admin')payload = b'2jctf_pa5sw0rdx00'.ljust(0x48, b'x61') + p64(0x400e88)io.sendafter('password', payload)io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672840567.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672840568.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1672840568.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1672840569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1672840570.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672840570.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672840571.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1672840571.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672840572.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1672840572.png)