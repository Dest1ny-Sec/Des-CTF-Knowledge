# corCTF 2024：位运算虚拟机及gpu hash爆破

> 原文: https://www.ctfiot.com/197191.html
> ID: 197191

FizzBuzz101 was innocently writing a new, top-secret compiler when his computer was Crowdstriked. Worse, the recovery key is behind a hasher that he wrote and compiled himself, and he can’t remember how the bits work! Can you help him get his life’s work back?

FizzBuzz101 正在无辜地编写一个新的绝密编译器，这时他的电脑遭到了 Crowdstriked。更糟糕的是，恢复密钥在他自己编写和编译的哈希器后面，他不记得这些位是如何工作的！你能帮他找回他一生的工作吗？

一

初步分析

0x1290~0xED853有一坨mov byte导致main函数f5不了

0x1290~0x136F：mov byte ptr [rax+x], 1，x范围是120h到13Fh

0x1370~0x16EF：mov byte ptr [rax+x], 0，x范围是0FA0h到101Fh

0x16F0~0x1E6E：or运算

mov cl, [rax+0FA0h]
or cl, [rax+100h]
mov [rax+0], cl

0x1E6F~0x566E：mov byte ptr [rax+x], y，赋值0或1

0x566F~0x57EE：and运算

0x57EF~0x59CE：xor运算

0x59CF~0x5BAE：and运算

…

一直持续到0xED853。

猜测是把变量按位拆分到字节。

二

main函数逻辑

main函数的[0x1290,0xED854)部分的扣掉了，然后ida f5（这题rva=va=foa）。

main的逻辑大体如下：

对输入有几个字节的校验。

把输入[7:18]按位拆分到字节（小端字节序，大端位序），填充到v3[0x940:0x998]。

然后就是text[0x1290:0xED854]这段代码的位运算，都是操作v3的。

最后按大端位序，v3[0:128]32字节为一组，每字节对应一位，v3中低字节对应32位整型高位，32字节转换为一个32位整型；按从低到高分4组，组成4个DWORD。

后两个DWORD需要=0x19C603BA,0x14353CE4。

__int64 __fastcall main(int a1, char **a2, char **a3)
{
 // ...
 puts("Welcome!nPlease enter the flag here: ");
 v3 = calloc(1uLL, (size_t)byte_186A0);
 v22 = __ctype_b_loc();
 while ( 1 )
 {
 memset(s, 0, 1000);
 fgets(s, 999, stdin);
 v4 = strcspn(s, "n");
 s[v4] = 0;
 if ( !memcmp("corctf{", s, 7uLL) && v4 > 1 && s[v4 - 1] == '}' && s[8] == s[17] && s[9] == s[11] )
 {
 v5 = s[7];
 if ( s[7] == s[16] + 1 && s[14] == s[16] + 4 )
 {
 v6 = &s[8];
 v7 = v3 + 0x940;
 v8 = *v22;
 if ( ((*v22)[s[7]] & 8) != 0 )
 {
 while ( 1 )
 {
 v9 = v7;
 v10 = 7;
 do
 {
 v11 = v5 >> v10--;
 *v9 = v11;
 *v9++ &= 1u;
 }
 while ( v10 != -1 ); // 输入按位拆分
 v7 += 8;
 if ( &s[18] == v6 ) // 遍历范围是s[7]~s[17]
 break;
 v5 = *v6++; // v5是遍历s[7]~s[17] (s[0]~s[6]="corctf{")
 if ( (v8[(char)v5] & 8) == 0 )
 goto LABEL_14;
 }
 v3[0x998] = 1;
 for ( i = 0LL; i != 64; ++i )
 v3[i + 0xB00] = ((0x8000000000000000LL >> i) & 0x5800000000000000LL) != 0;
 memset(v3 + 0x120, 1, 32uLL); // // [0x1290,0xED854)部分的代码
 memset(v3 + 0xFA0, 1, 128uLL); // // [0x1290,0xED854)部分的代码
 v13 = v3;
 v14 = 0;
 v15 = 0;
 for ( j = 0LL; ; v14 = *(_DWORD *)&v24[4 * (v15 >> 5) - 16] )
 {
 v16 = 0LL;
 v17 = v15 >> 5;
 do
 {
 v18 = (char)v13[v16];
 v19 = 0x80000000 >> v16++;
 v14 |= v19 * v18;
 }
 while ( v16 != 32 );
 v15 += 32;
 v13 += 32;
 *(_DWORD *)&v24[4 * v17 - 16] = v14;
 if ( v15 == 128 )
 break;
 }
 if ( *((_QWORD *)&j + 1) == 0x14353CE419C603BALL )
 break;
 }
 }
 }
LABEL_14:
 puts("Try again: ");
 }
 puts("Nice!n");
 // ...
}

三

分析位运算虚拟机

合并了连续写入位的结果（见附件asm.txt）。

[0x1290,0xED854)部分的代码，位运算模拟32位整型运算，这里截取其中一段运算，只截取了处理低8位的，完整就是一个32位的加法（8位一字节，小端字节序，字节里面大端位序）。

字节数组B40和B41是寄存器。

def f():
 global d
 d[0xA7] = d[0x87] ^ d[0x7]
 d[0xB40] = d[0x87] & d[0x7]
 d[0xB41] = d[0x86] ^ d[0x6]
 d[0xA6] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x86] & d[0x6]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x85] ^ d[0x5]
 d[0xA5] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x85] & d[0x5]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x84] ^ d[0x4]
 d[0xA4] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x84] & d[0x4]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x83] ^ d[0x3]
 d[0xA3] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x83] & d[0x3]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x82] ^ d[0x2]
 d[0xA2] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x82] & d[0x2]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x81] ^ d[0x1]
 d[0xA1] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x81] & d[0x1]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x80] ^ d[0x0]
 d[0xA0] = d[0xB41] ^ d[0xB40]

四

反编译

每连续32个对非寄存器字节（非d_B40,d_B41）的写入，是模拟32位整型运算一次。

运算类型包括常量赋值 以及 加法、与、或、异或、循环位移5种运算。

常量赋值直接模拟，然后取数据出来即可。

5种运算识别：往数组中插入随机数据，32次写入非寄存器字节后，取出结果，判断是上述哪种运算的结果，即可得到该组位运算模拟的32位整型运算。

然后重新编译，扔ida里看发现是hash算法，需要爆破。

__ctype_b_loc()是特征表，&8检查的是字符是否为数字和大小写字母。

输入除flag wrap外11个字符，实际上只需要确定7个字符，且a[9]的范围少了12种字符的可能，(s[7]~s[17],s是带wrap的完整flag,a是去掉wrap)。

s[8]==s[17] a[1]=a[10]

s[9]==s[11] a[2]=a[4]

s[7]==s[16]+1 a[0]=a[9]+1

s[14]==s[16]+4 a[7]=a[9]+4

反编译结果 c语言可编译版本 见附件asm2.c。

五

gpu爆破

用python numba包调用cuda爆破（笔记本2060 7分半能跑完完整爆破）。

需要注意的是，位运算虚拟机内部是按8位一字节，小端字节序，字节内大端位序来模拟32位整型运算的。

而最后校验从虚拟中取数据时，是按32位大端位序来取的（字节序反了）。

所以反编译的代码在最后比较要反转输出或者比较目标。

爆破脚本见附件c.py（点击阅读原文，文末获取）。

爆破的坑：尽量把逻辑都扔进核函数里，减少数据交换；还有尽量别用数组，在本题中非常慢，拆成一个个单独的变量就快很多。

看雪ID：wx_御史神风

https://bbs.kanxue.com/user-home-907036.htm

*本文为看雪论坛优秀文章，由 wx_御史神风 原创，转载请注明来自看雪社区

# 往期推荐

1、Alt-Tab Terminator注册算法逆向

2、恶意木马历险记

3、VMP源码分析：反调试与绕过方法

4、Chrome V8 issue 1486342浅析

5、Cython逆向-语言特性分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
初步分析
```



```
mov cl, [rax+0FA0h]
or cl, [rax+100h]
mov [rax+0], cl
```



```
二
main函数逻辑
```



```
__int64 __fastcall main(int a1, char **a2, char **a3)
{
 // ...
 puts("Welcome!nPlease enter the flag here: ");
 v3 = calloc(1uLL, (size_t)byte_186A0);
 v22 = __ctype_b_loc();
 while ( 1 )
 {
 memset(s, 0, 1000);
 fgets(s, 999, stdin);
 v4 = strcspn(s, "n");
 s[v4] = 0;
 if ( !memcmp("corctf{", s, 7uLL) && v4 > 1 && s[v4 - 1] == '}' && s[8] == s[17] && s[9] == s[11] )
 {
 v5 = s[7];
 if ( s[7] == s[16] + 1 && s[14] == s[16] + 4 )
 {
 v6 = &s[8];
 v7 = v3 + 0x940;
 v8 = *v22;
 if ( ((*v22)[s[7]] & 8) != 0 )
 {
 while ( 1 )
 {
 v9 = v7;
 v10 = 7;
 do
 {
 v11 = v5 >> v10--;
 *v9 = v11;
 *v9++ &= 1u;
 }
 while ( v10 != -1 ); // 输入按位拆分
 v7 += 8;
 if ( &s[18] == v6 ) // 遍历范围是s[7]~s[17]
 break;
 v5 = *v6++; // v5是遍历s[7]~s[17] (s[0]~s[6]="corctf{")
 if ( (v8[(char)v5] & 8) == 0 )
 goto LABEL_14;
 }
 v3[0x998] = 1;
 for ( i = 0LL; i != 64; ++i )
 v3[i + 0xB00] = ((0x8000000000000000LL >> i) & 0x5800000000000000LL) != 0;
 memset(v3 + 0x120, 1, 32uLL); // // [0x1290,0xED854)部分的代码
 memset(v3 + 0xFA0, 1, 128uLL); // // [0x1290,0xED854)部分的代码
 v13 = v3;
 v14 = 0;
 v15 = 0;
 for ( j = 0LL; ; v14 = *(_DWORD *)&v24[4 * (v15 >> 5) - 16] )
 {
 v16 = 0LL;
 v17 = v15 >> 5;
 do
 {
 v18 = (char)v13[v16];
 v19 = 0x80000000 >> v16++;
 v14 |= v19 * v18;
 }
 while ( v16 != 32 );
 v15 += 32;
 v13 += 32;
 *(_DWORD *)&v24[4 * v17 - 16] = v14;
 if ( v15 == 128 )
 break;
 }
 if ( *((_QWORD *)&j + 1) == 0x14353CE419C603BALL )
 break;
 }
 }
 }
LABEL_14:
 puts("Try again: ");
 }
 puts("Nice!n");
 // ...
}
```



```
三
分析位运算虚拟机
```



```
def f():
 global d
 d[0xA7] = d[0x87] ^ d[0x7]
 d[0xB40] = d[0x87] & d[0x7]
 d[0xB41] = d[0x86] ^ d[0x6]
 d[0xA6] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x86] & d[0x6]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x85] ^ d[0x5]
 d[0xA5] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x85] & d[0x5]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x84] ^ d[0x4]
 d[0xA4] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x84] & d[0x4]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x83] ^ d[0x3]
 d[0xA3] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x83] & d[0x3]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x82] ^ d[0x2]
 d[0xA2] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x82] & d[0x2]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x81] ^ d[0x1]
 d[0xA1] = d[0xB41] ^ d[0xB40]
 d[0xB40] = d[0xB41] & d[0xB40]
 d[0xB41] = d[0x81] & d[0x1]
 d[0xB40] = d[0xB41] | d[0xB40]
 d[0xB41] = d[0x80] ^ d[0x0]
 d[0xA0] = d[0xB41] ^ d[0xB40]
```



```
四
反编译
```



```
五
gpu爆破
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1722648275.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1722648280.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722648281.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1722648282.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1722648282.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1722648283.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1722648283.gif)