# D3CTF2023 REVERSE

> 原文: https://www.ctfiot.com/133171.html
> ID: 133171

一

D3SKY

无壳32位

首先在TLS函数发现修改了一个RC4的密钥，稍微审计可知，同时在main函数可知我们的输入是37位，所以这边初始化的74位其实就是存放了我们的输入37位和密文37位，整理下可知：

unsigned int sub_3B1050()
{
 unsigned int v0; // eax

 if ( !IsDebuggerPresent() )
 Str[5] = 49;
 v0 = strlen("YunZhiJun");
 RC4_INIT(&Sbox, "YunZhiJun", v0);
 return RC4(&Sbox, st_input, 74u);
}

来到主函数并不是很长，不过是道VM题，而这题比较特殊是 与非 VM，也就是说所有的操作都是靠

op[p2] = ~(op[p0] & op[p1]);

这条语句进行运行。

int __cdecl main(int argc, const char **argv, const char **envp)
{
 int v4; // [esp+0h] [ebp-24h]
 int v5; // [esp+Ch] [ebp-18h]
 unsigned __int16 p2; // [esp+14h] [ebp-10h]
 unsigned __int16 p0; // [esp+18h] [ebp-Ch]
 unsigned __int16 p1; // [esp+1Ch] [ebp-8h]
 unsigned __int16 i; // [esp+20h] [ebp-4h]

 v5 = 0;
 puts("Welcome to D^3CTF~");
 while ( op[0] != 0xFFFF )
 {
 if ( op[2] == 1 )
 {
 op[2] = 0;
 printf("%c", op[3]);
 }
 if ( op[7] == 1 )
 {
 op[7] = 0;
 scanf("%c", &op[8]);
 v4 = v5++;
 if ( v4 == 37 && op[8] != 0x7E )
 {
 puts("Wrong!");
 return 0;
 }
 }
 if ( op[19] )
 {
 puts("Wrong!");
 return 0;
 }
 i = op[0];

 RC4(&Sbox, &op[op[0]], 3u);
 p0 = op[i];
 p1 = op[i + 1];
 p2 = op[i + 2];

 op[0] = i + 3;
 RC4(&Sbox, &op[i], 3u);
 op[p2] = ~(op[p0] & op[p1]);
 }
 puts("Right! Your flag is antd3ctf{your input}");
 return 0;
}

那么稍微审计可知比较重要的几点：

那么既然是VM题，先打印出所有的opcode看看效果， 那么这里有两个方法。

第一种 利用条件断点

在字节码在加密回去前的地方下个断点，把其语句打印出来。

op_addr = 0x5B4018
ebp = idc.get_reg_value('ebp')
p0 = ida_bytes.get_word(ebp - 0xC)
p1 = ida_bytes.get_word(ebp - 0x8)
p2 = ida_bytes.get_word(ebp - 0x10)

op_p0 = ida_bytes.get_word(op_addr + p0 * 2)
op_p1 = ida_bytes.get_word(op_addr + p1 * 2)
print('op[%d] = ~(op[%d] & op[%d]) ' % (p2, p0, p1), '(op[%d] = ~(%d & %d))' % (p2, op_p0, op_p1) )

但由于前面还有个input有很多语句，我们只需要关心我们输入后程序进行了什么操作所以在判断输入长度也下个条件断点。

op_addr = 0x5B4018
ebp = idc.get_reg_value('ebp')
v4 = ida_bytes.get_word(ebp - 0x24) 
if (v4 == 36):
 print('----------------------------END INPUT------------------------------')

测试输入 123456781234567812345678123456781234~

随后让程序跑起来直接输入即可跑出opcode，不难发现我们的输入49 50 51 52都被引用到，第一个密文36也被引用到随后程序就跑出wrong，同时也可以知道op[2772]就是存放我们输入的起始位置了。

...
op[11] = ~(op[20] & op[20]) (op[11] = ~(1 & 1))
op[7] = ~(op[11] & op[11]) (op[7] = ~(65534 & 65534))
---------------------END INPUT----------------------
op[7] = ~(op[8] & op[8]) (op[7] = ~(126 & 126))
op[2808] = ~(op[7] & op[7]) (op[2808] = ~(65409 & 65409))
op[11] = ~(op[2772] & op[2772]) (op[11] = ~(49 & 49))
op[11] = ~(op[11] & op[2773]) (op[11] = ~(65486 & 50))
op[12] = ~(op[2773] & op[2773]) (op[12] = ~(50 & 50))
op[12] = ~(op[12] & op[2772]) (op[12] = ~(65485 & 49))
op[17] = ~(op[11] & op[12]) (op[17] = ~(65533 & 65534))
op[11] = ~(op[2774] & op[2774]) (op[11] = ~(51 & 51))
op[11] = ~(op[11] & op[2775]) (op[11] = ~(65484 & 52))
op[12] = ~(op[2775] & op[2775]) (op[12] = ~(52 & 52))
op[12] = ~(op[12] & op[2774]) (op[12] = ~(65483 & 51))
op[18] = ~(op[11] & op[12]) (op[18] = ~(65531 & 65532))
op[11] = ~(op[17] & op[17]) (op[11] = ~(3 & 3))
op[11] = ~(op[11] & op[18]) (op[11] = ~(65532 & 7))
op[12] = ~(op[18] & op[18]) (op[12] = ~(7 & 7))
op[12] = ~(op[12] & op[17]) (op[12] = ~(65528 & 3))
op[18] = ~(op[11] & op[12]) (op[18] = ~(65531 & 65535))
op[11] = ~(op[2809] & op[2809]) (op[11] = ~(36 & 36))
op[11] = ~(op[11] & op[18]) (op[11] = ~(65499 & 4))
op[12] = ~(op[18] & op[18]) (op[12] = ~(4 & 4))
op[12] = ~(op[12] & op[2809]) (op[12] = ~(65531 & 36))
op[19] = ~(op[11] & op[12]) (op[19] = ~(65535 & 65503))

第二种 ctrl cv

还有种方便的方法就是直接复制ida的代码即可，在我们需要输出的地方直接打印即可，其中注意下导入 defs.h 的ida库。

（完整代码请点击文末阅读原文查看）

#include <cstdio>
#include <cstring>
#include "defs.h"
#include <cstdlib>
#define _CRT_SECURE_NO_WARNINGS

那么再经过稍微的调试与审计，不难发现我们的每段比较密文都是这种形式。

# op[17] = in[0] ^ in[1]
op[11] = ~(data[0] & data[0])
op[11] = ~(op[11] & data[1])
op[12] = ~(data[1] & data[1])
op[12] = ~(op[12] & data[0])
op[17] = ~(op[11] & op[12])

# op[18] = in[2] ^ in[3]
op[11] = ~(data[2] & data[2])
op[11] = ~(op[11] & data[3])
op[12] = ~(data[3] & data[3])
op[12] = ~(op[12] & data[2])
op[18] = ~(op[11] & op[12])

# op[18] = op[17] ^ op[18]
op[11] = ~(op[17] & op[17])
op[11] = ~(op[11] & op[18])
op[12] = ~(op[18] & op[18])
op[12] = ~(op[12] & op[17])
op[18] = ~(op[11] & op[12])

# check
op[11] = ~(data[37] & data[37]) # data[37]也就是我们的密文第一位
op[11] = ~(op[11] & op[18])
op[12] = ~(op[18] & op[18])
op[12] = ~(op[12] & data[37])
op[19] = ~(op[11] & op[12])

随后直接Z3即可，当然看了云之君师傅博客直接逆也可以。

from z3 import *

enc = [0x0024, 0x000B, 0x006D, 0x000F, 0x0003, 0x0032, 0x0042, 0x001D, 0x002B, 0x0043, 0x0078, 0x0043, 0x0073, 0x0030, 0x002B, 0x004E, 0x0063, 0x0048, 0x0077, 0x002E, 0x0032, 0x0039, 0x001A, 0x0012, 0x0071, 0x007A, 0x0042, 0x0017, 0x0045, 0x0072, 0x0056, 0x000C, 0x005C, 0x004A, 0x0062, 0x0053, 0x0033]
sol = Solver()
input = [BitVec('input%d' % i, 8) for i in range(37)]

sol.add(input[36] == ord('~'))

for i in range(37):
 sol.add((input[i] ^ input[(i + 1) % 37] ^ input[(i + 2) % 37] ^ input[(i + 3) % 37]) == enc[i])

assert sat == sol.check()
ans = sol.model()
for i in range(37):
 print(chr(ans[input[i]].as_long()), end = "")
# A_Sin91e_InS7rUcti0N_ViRTua1_M4chin3~

二

D3RC4

无壳64位

首先点入main函数是会得到一个fake flag，不过也已经经过RC4异或了一次我们的输入，随后出题人在_fini_array还有起个函数，也就是本题的关键了

那么先普及点前置知识。

fork函数的返回值

◆-1：创建失败，在父进程中返回-1

◆0：创建成功，当前进程是子进程

◆其他：创建成功，在父进程中返回子进程的pid(进程 ID)

pipe管道

#include <unistd.h>
int pipe (int fd[2]);
 //返回:成功返回0，出错返回-1

◆fd参数返回两个文件描述符，fd[0]指向管道的读端，fd[1]指向管道的写端，fd[1]的输出是fd[0]的输入

◆当要父进程要读值，父进程关闭fd[1]（写端），子进程关闭fd[0]（读端），因为管道是单向的，管道是用环形队列实现的

那么简单来说就是写的时候关读端fd[0]，起写端fd[1]，另一端反之。

该函数为程序退出后要执行的函数。

unsigned __int64 father()
{
 int v1; // eax
 __WAIT_STATUS stat_loc; // [rsp+4h] [rbp-2Ch] BYREF
 int i; // [rsp+Ch] [rbp-24h]
 int j; // [rsp+10h] [rbp-20h]
 int k; // [rsp+14h] [rbp-1Ch]
 __pid_t p; // [rsp+18h] [rbp-18h]
 int v7; // [rsp+1Ch] [rbp-14h]
 int ffd[2]; // [rsp+20h] [rbp-10h] BYREF
 unsigned __int64 v9; // [rsp+28h] [rbp-8h]

 v9 = __readfsqword(0x28u);
 if ( pipe(ffd) == -1 )
 exit(1);
 p = fork();
 if ( p < 0 )
 exit(1);

 if ( p ) // 父进程
 {
 close(ffd[0]);
 v7 = 2;
 HIDWORD(stat_loc.__iptr) = 3;
 while ( SHIDWORD(stat_loc.__iptr) < len ) // 主进程写数据
 {
 if ( SHIDWORD(stat_loc.__iptr) % v7 ) // 奇数
 write(ffd[1], &stat_loc.__iptr + 4, 4uLL);
 else // 偶数，执行十六次
 ++p1;
 ++HIDWORD(stat_loc.__iptr);
 }

 close(ffd[1]); // 关闭写端开始读子进程的数据放入密钥
 close(fd0[1]);
 while ( read(fd0[0], &stat_loc.__iptr + 4, 4uLL) )
 {
 v1 = p2++;
 aWe1c0m3T0D3ctf[v1] = BYTE4(stat_loc.__iptr);// 修改了Key
 }

 close(fd0[0]); // 关闭读端，再起一个子进程
 wait(&stat_loc);

 if ( LODWORD(stat_loc.__uptr) )
 {
 puts(s);
 exit(1);
 }

 p = fork();
 if ( p < 0 )
 exit(1);

 if ( !p ) // 子进程
 {
 init_key(Sbox, aWe1c0m3T0D3ctf, p2);
 for ( i = 0; i < p1; ++i )
 RC4(Sbox, len, xor_key);
 for ( j = 0; j < len; j += 2 )
 {
 in1[j] = (in1[j] + in1[j + 1]) ^ xor_key[j];
 in1[j + 1] = xor_key[j + 1] ^ (in1[j] - in1[j + 1]);
 }
 for ( k = 0; k < len; ++k )
 {
 if ( in1[k] != enc[k] )
 exit(1);
 }
 exit(0);
 }

 wait(&stat_loc); // 父进程调用wait等待子进程退出
 if ( LODWORD(stat_loc.__uptr) ) // 根据子进程返回值输出，就是最后的check了
 puts(s);
 else
 puts(aGqk9lLwyvj);
 exit(0);
 }
 child(ffd);
 return v9 - __readfsqword(0x28u);
}

总结下该函数所执行的操作：

unsigned __int64 __fastcall child(int *ffd)
{
 int v2; // eax
 int buf; // [rsp+18h] [rbp-28h] BYREF
 __WAIT_STATUS stat_loc; // [rsp+1Ch] [rbp-24h] BYREF
 int i; // [rsp+24h] [rbp-1Ch]
 int j; // [rsp+28h] [rbp-18h]
 __pid_t v7; // [rsp+2Ch] [rbp-14h]
 int lfd[2]; // [rsp+30h] [rbp-10h] BYREF
 unsigned __int64 v9; // [rsp+38h] [rbp-8h]

 v9 = __readfsqword(0x28u);
 close(ffd[1]);
 if ( !read(*ffd, &buf, 4uLL) ) // 读不到数据就退
 exit(1);
 if ( pipe(lfd) == -1 )
 exit(1);

 v7 = fork();
 if ( v7 < 0 )
 exit(1);

 if ( v7 ) // 子父进程
 {
 close(lfd[0]);
 close(fd0[0]);

 write(fd0[1], &buf, 4uLL); // 写入的就是从ffd管道读到的值，也就是Buf[0]，随后写入key
 close(fd0[1]);

 while ( read(*ffd, &stat_loc.__iptr + 4, 4uLL) )// 向上读入 其父进程 传入的值
 {
 if ( SHIDWORD(stat_loc.__iptr) % buf ) // 余第一项，注意每次都不一样，随后向下递归写入取值
 write(lfd[1], &stat_loc.__iptr + 4, 4uLL);
 else
 ++p1;
 }
 close(lfd[1]);
 wait(&stat_loc);

 v2 = p2++; // 注意fork后的子进程和父进程不共有这些值，所以随便改也没事
 aWe1c0m3T0D3ctf[v2] = Sbox[buf];
 init_key(Sbox, aWe1c0m3T0D3ctf, p2);
 for ( i = 0; i < 256 - p1; ++i )
 {
 RC4(Sbox, len, xor_key);
 for ( j = 0; j < len; j += 2 )
 {
 in1[j] = (in1[j] + in1[j + 1]) ^ xor_key[j];
 in1[j + 1] = xor_key[j + 1] ^ (in1[j] - in1[j + 1]);
 }
 }
 exit(0);
 }
 child(lfd);
 return v9 - __readfsqword(0x28u);
}

再总结下Child函数：

子父进程处理Fahter函数传来的值再传递给自己的子进程（也就是 2.）

子子进程处理子父进程的值（也就是 1. ）

那么稍微屡屡就知道我们的key到底做了什么修改。

def get_key(arr):
 if len(arr) <= 0:
 return
 global key
 key.append(arr[0])

 new_arr = []
 for i in range(1, len(arr)):
 if arr[i] % arr[0] != 0:
 new_arr.append(arr[i])

 get_key(new_arr)

arr = []
global key
key = bytearray(b'We1c0m3_t0_d^3ctf')
for i in range(3, 36):
 if i % 2 != 0: 
 arr.append(i)
get_key(arr)
print(key)

# b'We1c0m3_t0_d^3ctfx03x05x07x0brx11x13x17x1dx1f'

那么得到key了之后这题也就没有什么难点了。

还有个神奇的方法，我一直没意识到，赛后问了P1umH0师傅，其实直接attach上就能拿到key了。

按理来说在这下断点是应该断的住的，毕竟我们的输入与key的修改没有任何关系，而我每次跑到这就自动退了，而且key也没成功修改，属于是玄学问题。

if ( LODWORD(stat_loc.__uptr) )
 {
 puts(s);
 exit(1);
 }

那么这题也可以用Z3直接做了，跟着程序写完所有加密直接就可以出。

from z3 import *

def init_key(Sbox, key, p2):
 v4 = 0
 for i in range(256):
 v4 = (Sbox[i] + v4 + key[i % p2]) % 256
 Sbox[i], Sbox[v4] = Sbox[v4], Sbox[i]

def RC4(Sbox, l):
 v7 = -1
 v5 = 0
 v6 = 0
 xor_key = [0] * 104
 while (l):
 v5 = (v5 + 1) % 256
 v6 = (v6 + Sbox[v5]) % 256
 Sbox[v6], Sbox[v5] = Sbox[v5], Sbox[v6]
 v7 += 1
 xor_key[v7] = Sbox[(Sbox[v5] + Sbox[v6]) % 256]
 l -= 1
 return xor_key

def Encrypt(input):
 global Sbox
 Sbox = [0] * 256
 for i in range(256):
 Sbox[i] = i
 enc = [0xF7, 0x5F, 0xE7, 0xB0, 0x9A, 0xB4, 0xE0, 0xE7, 0x9E, 0x05, 
 0xFE, 0xD8, 0x35, 0x5C, 0x72, 0xE0, 0x86, 0xDE, 0x73, 0x9F, 
 0x9A, 0xF6, 0x0D, 0xDC, 0xC8, 0x4F, 0xC2, 0xA4, 0x7A, 0xB5, 
 0xE3, 0xCD, 0x60, 0x9D, 0x04, 0x1F]

 sol = Solver()
 # main decryption
 p1 = 17
 p2 = 17 
 l = len(input)
 key = b'We1c0m3_t0_d^3ctf'
 init_key(Sbox, key, p2)
# print(Sbox)
 xor_key = RC4(Sbox, l)
# print(xor_key)
 in1 = [0] * 36
 for i in range(l):
 in1[i] = input[i] ^ xor_key[i]
 

 key = b'We1c0m3_t0_d^3ctfx03x05x07x0brx11x13x17x1dx1f'
 # father-child decryption
 init_key(Sbox, key, len(key))
 for i in range(p1):
 xor_key = RC4(Sbox, l)
 print(xor_key)
 for j in range(0, l, 2):
 in1[j] = (in1[j] + in1[j + 1]) ^ xor_key[j]
 in1[j + 1] = xor_key[j + 1] ^ (in1[j] - in1[j + 1])
 for i in range(l):
 sol.add(in1[i] == enc[i])
 
 assert sat == sol.check()
 ans = sol.model()
 for i in range(l):
 print(chr(ans[input[i]].as_long()), end = "")

input = [BitVec('input%d' % i, 8) for i in range(36)]
Encrypt(input)
# getting_primes_with_pipes_is_awesome

三

D3RECOVER

无壳64位

那么本题为抽象的pyd逆向，第一个文件是没有符号的，第二个文件是有符号的，出题人也就是想让我们用Bindiff来合并一下，于是可以直接恢复第一个文件的符号方便逆向。

于是直接搜索check向上引用不难发现 _pyx_pf_14d3recover_ver2_2check 就是我们的加密函数。

那么通过调试与化简可得以下逻辑：

for ( i = 0LL; i <= 31; ++i )
 _Pyx_PyByteArray_Append(v9, input ^ 0x23u)
for ( j = 0LL; j <= 29; ++j )
{
 input_t1 = input[index]
 input_t1 = input[index + 2]
 PyNumber_Add(input_t1, input_t2)
 Pyx_PyInt_AndObjC(index, num_0xFF, 0xFFLL, 0LL, 0LL)
 _Pyx_PyInt_XorObjC(input_t2, num_0x54, 0x54LL, 0LL, 0LL)
}

那么调试拿到enc直接用Z3就出了。

from z3 import *

enc = [0xd3,0xc7,0xce,0xca,0x3f,0x84,0xdb,0xb3,0xb6,0xb9,0x80,0xea,0xd0,0xcd,0x72,0xfc,0xd8,0x30,0x95,0xdb,0xe2,0xd8,0x92,0x08,0xc1,0xc6,0xc5,0xf4,0x07,0xec,0x02,0x5e]
enc1 = [0x76,0x7c,0x72,0x78,0x7e,0x64,0x72,0x78,0x76,0x7c,0x72,0x78,0x7e,0x64,0x72,0x78,0x76,0x7c,0x72,0x78,0x7e,0x64,0x72,0x78,0x76,0x7c,0x72,0x78,0x7e,0x64,0x14,0x1b]
input = [BitVec("input%d" % i, 8) for i in range(32)]
sol = Solver()
in1 = [0] * 32
for i in range(32):
 in1[i] = input[i] ^ 0x23

for i in range(30):
 in1[i] = ((in1[i] + in1[i + 2]) & 0xFF) ^ 0x54

for i in range(32):
 sol.add(enc[i] == in1[i])

while sat == sol.check():
 ans = sol.model()
 for i in range(32):
 print(chr(ans[input[i]].as_long()), end = "")
 sol.add(Or([input[i] != ans[input[i]] for i in range(32)]) )
# flag{y0U_RE_Ma5t3r_0f_R3vocery!}

四

D3SYSCALL

无壳64位

这题VM也比较特别，是利用内核模块动态修改了系统调用实现的VM，这题由syscall所进行的VM进行过程。

64位下的syscall是通过不同的rax的值进行不同的系统调用

简单来说这题就是注册了几个自己的操作，不同操作由不同的eax代表，随后syscall到相应操作进行VM操作。

那么出题人师傅在官解里解释的很详细了

https://github.com/4nsw3r123/d3syscall

有了这个概念，那么现在从逆向的角度去看待这题。

首先我们可以在这个区域看到运行于主函数之前的函数

随后直接调试可以看到在tmp目录起了个my_module，随后去 kallsyms(符号表，它包含了内核中所有的符号信息) 获取sys_call_table(系统调用表) ，随后将sys_call_module传入my_module。

那么在看my_module前先看下main函数

进到该函数可以发现清一色的syscall

那么至此我们了解了主程序在 init 起了个 my_module 注册了自己的系统调用，随后程序syscall到自己注册的系统调用进行加密，那么事情就很简单了，只要我们搞懂每次的调用所对应的操作就能解出本题。

该文件直接动调取出，IDA打开看到 init_module 函数，主要就是解析这几个函数，也就是syscall所对应的操作。

*(sys_table + 2680) = mov; // v4[0x14F]
 v4[0x150] = ALU;
 v4[0x151] = push;
 v4[0x152] = pop;
 v4[0x153] = reset;
 v4[0x154] = check;

拿 mov 举例

__int64 __fastcall mov(_QWORD *a1)
{
 __int64 rdi0; // rax
 unsigned __int64 rdx0; // r12
 unsigned __int64 rsi0; // rbx

 _fentry__(a1);
 rdi0 = a1[14]; // 我是通过传参顺序命名好所传入的变量
 rdx0 = a1[12];
 rsi0 = a1[13];
 if ( rdi0 )
 {
 if ( rdi0 == 1 )
 {
 if ( rsi0 > 3 )
 _ubsan_handle_out_of_bounds(&off_1800, a1[13]);// 像这种 out 就是越界了而程序正常执行是不会发生的
 tmp_reg[rsi0] = rdx0; // 我们只需要关注实际操作，如这条
 }
 }
 else
 {
 if ( rdx0 > 3 )
 _ubsan_handle_out_of_bounds(&off_1840, a1[12]);
 if ( rsi0 > 3 )
 _ubsan_handle_out_of_bounds(&off_1820, rsi0);
 tmp_reg[rsi0] = tmp_reg[rdx0];
 }
 if ( rsi0 > 3 )
 _ubsan_handle_out_of_bounds(&off_17E0, rsi0);
 return tmp_reg[rsi0];
}

写出对应的代码

def mov(rdx, rsi, rdi):
 if rdi == 1:
 print('tmp_reg[%x] = %x' %(rsi, rdx))
 else:
 print('tmp_reg[%x] = tmp_reg[%x]' %(rsi, rdx))

那么到这一步，我们只需要逐个翻译每个 rax 所对应的操作，再从主程序取得所有参数就能将程序所有的操作打印出来。

那么出题人还提供了个很方便的思路就是 strace 可以打印出所有的syscall，这样可以快速拿到所有参数。

那么翻译出整个流程直接通过Z3或者逆向直接解密即可。

def mov(rdx, rsi, rdi):
 if rdi == 1:
 print('tmp_reg[%x] = %x' %(rsi, rdx))
 else:
 print('tmp_reg[%x] = tmp_reg[%x]' %(rsi, rdx))

def alu(rdx, rsi, rdi):
 if rdi == 3:
 print('tmp_reg[%x] = tmp_reg[%x] ^ tmp_reg[%x]' % (rsi, rdx, rsi))
 elif rdi == 4:
 print('tmp_reg[%x] = tmp_reg[%x] << tmp_reg[%x]' % (rsi, rsi, rdx))
 elif rdi == 5:
 print('tmp_reg[%x] = tmp_reg[%x] >> tmp_reg[%x]' % (rsi, rsi, rdx))
 elif rdi == 1:
 print('tmp_reg[%x] = tmp_reg[%x] - tmp_reg[%x]' % (rsi, rsi, rdx))
 elif rdi == 2:
 print('tmp_reg[%x] = tmp_reg[%x] * tmp_reg[%x]' % (rsi, rdx, rsi))
 else:
 print('tmp_reg[%x] = tmp_reg[%x] + tmp_reg[%x]' % (rsi, rdx, rsi))

def push(rsi, rdi):
 if rdi == 1:
 print('mem[tmp_reg[5] + 1] = %x' % (rsi))
 else:
 print('mem[tmp_reg[5] + 1] = tmp_reg[%x]' % (rsi))

def pop(rsi):
 print('tmp_reg[5] = tmp_reg[5] - 1')
 print('tmp_reg[%x] = mem[tmp_reg[5]]' % (rsi))

def reset():
 print('init_reg[0] = 0')
 print('init_reg[1] = 0')
 print('init_reg[2] = 0')
 print('init_reg[3] = 0')

def check():
 print('check mem == enc')

def syscall(op):
 if op[0] == 0x14F:
 mov(op[3], op[2], op[1])
 elif op[0] == 0x150:
 alu(op[3], op[2], op[1])
 elif op[0] == 0x151:
 push(op[2], op[1])
 elif op[0] == 0x152:
 pop(op[2])
 elif op[0] == 0x153:
 reset()
 elif op[0] == 0x154:
 check()

opcode = [[0x14f, 0x1, 0, 0x3837363534333231],
[0x14f, 0x1, 0x1, 0x3837363534333231],
[0x151, 0, 0x1, 0x3837363534333231],
[0x14f, 0, 0x2, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x4, 0x2, 0x1],
[0x14f, 0x1, 0x1, 0x51e7647e],
[0x150, 0, 0x2, 0x1],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x2, 0x3, 0x1],
[0x14f, 0x1, 0x1, 0xe0b4140a],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0xe6978f27],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0x1, 0x2, 0x3],
[0x150, 0, 0x1, 0x2],
[0x151, 0, 0x1, 0x2],
[0x151, 0, 0, 0x2],
[0x14f, 0, 0x2, 0x1],
[0x14f, 0x1, 0, 0x6],
[0x150, 0x4, 0x2, 0],
[0x14f, 0x1, 0, 0x53a35337],
[0x150, 0, 0x2, 0],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5],
[0x150, 0x2, 0x3, 0],
[0x14f, 0x1, 0, 0x9840294d],
[0x150, 0, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5eae4751],
[0x150, 0x1, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0, 0x2, 0x3],
[0x150, 0, 0, 0x2],
[0x151, 0, 0, 0x2],
[0x153, 0, 0, 0x2],
[0x14f, 0x1, 0, 0x3837363534333231],
[0x14f, 0x1, 0x1, 0x3837363534333231],
[0x151, 0, 0x1, 0x3837363534333231],
[0x14f, 0, 0x2, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x4, 0x2, 0x1],
[0x14f, 0x1, 0x1, 0x51e7647e],
[0x150, 0, 0x2, 0x1],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x2, 0x3, 0x1],
[0x14f, 0x1, 0x1, 0xe0b4140a],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0xe6978f27],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0x1, 0x2, 0x3],
[0x150, 0, 0x1, 0x2],
[0x151, 0, 0x1, 0x2],
[0x151, 0, 0, 0x2],
[0x14f, 0, 0x2, 0x1],
[0x14f, 0x1, 0, 0x6],
[0x150, 0x4, 0x2, 0],
[0x14f, 0x1, 0, 0x53a35337],
[0x150, 0, 0x2, 0],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5],
[0x150, 0x2, 0x3, 0],
[0x14f, 0x1, 0, 0x9840294d],
[0x150, 0, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5eae4751],
[0x150, 0x1, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0, 0x2, 0x3],
[0x150, 0, 0, 0x2],
[0x151, 0, 0, 0x2],
[0x153, 0, 0, 0x2],
[0x14f, 0x1, 0, 0x34333231],
[0x14f, 0x1, 0x1, 0],
[0x151, 0, 0x1, 0],
[0x14f, 0, 0x2, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x4, 0x2, 0x1],
[0x14f, 0x1, 0x1, 0x51e7647e],
[0x150, 0, 0x2, 0x1],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x2, 0x3, 0x1],
[0x14f, 0x1, 0x1, 0xe0b4140a],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0xe6978f27],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0x1, 0x2, 0x3],
[0x150, 0, 0x1, 0x2],
[0x151, 0, 0x1, 0x2],
[0x151, 0, 0, 0x2],
[0x14f, 0, 0x2, 0x1],
[0x14f, 0x1, 0, 0x6],
[0x150, 0x4, 0x2, 0],
[0x14f, 0x1, 0, 0x53a35337],
[0x150, 0, 0x2, 0],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5],
[0x150, 0x2, 0x3, 0],
[0x14f, 0x1, 0, 0x9840294d],
[0x150, 0, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5eae4751],
[0x150, 0x1, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0, 0x2, 0x3],
[0x150, 0, 0, 0x2],
[0x151, 0, 0, 0x2],
[0x153, 0, 0, 0x2],
[0x154, 0, 0, 0x2]]

for op in opcode:
 syscall(op)

def encrypt(p1, p2, cnt):
 enc = [0xB0800699CB89CC89, 0x4764FD523FA00B19, 0x396A7E6DF099D700, 0xB115D56BCDEAF50A, 0x2521513C985791F4, 0xB03C06AF93AD0BE]
 p2 += ((p1 << 3) + 0x51e7647e) ^ (p1 * 3 + 0xe0b4140a) ^ (p1 + 0xe6978f27)
 p1 += ((p2 << 6) + 0x53a35337) ^ (5 * p2 + 0x9840294d) ^ (p2 - 0x5eae4751)
 sol.add(p1 == enc[cnt + 1])
 sol.add(p2 == enc[cnt])

from z3 import *

input = [BitVec('input%d' % i, 64) for i in range(6)]
sol = Solver()
for i in range(0, 6, 2):
 encrypt(input[i], input[i + 1], i)
assert sat == sol.check()
ans = sol.model()
for i in range(6):
 print(int.to_bytes(ans[input[i]].as_long(), 8, 'little').decode(),end='')
# d3ctf{cef9b994-2547-4844-ac0d-a097b75806a0}

五

D3Tetris

无壳

拿到一个 apk 与一个流量包，打开流量包不难，数据不多，根据数据不难判断是个 Protocol 包。

解包得到数据

Java层进行了混淆，很难看，于是想到有流量包那也许可以通过 ip 搜到关键函数，发现只有一条。

不难判断这就是程序关键点。

翻阅那长长的一条可以发现一个混淆的 native 函数。

第一个函数是类构造时候就会调用，第二个应该是分数到了 900000 会调用的函数。

于是来到 so 层看这两个函数的源码，不过代码不好看，到处翻阅不难发现 oO0OooOo0oO 该函数中有 AES 加密与 RC4 加密，那么具体加密什么数据与密钥我们直接开始动调。

调试机开启

crosshatch:/ # ./data/local/tmp/7ad64
IDA Android 64-bit remote debug server(ST) v7.7.27. Hex-Rays (c) 2004-2022
Listening on 0.0.0.0:23946...

转发默认端口并以调试模式开启该 apk

adb forward tcp:23946 tcp:23946
adb shell am start -D -n com.jetgame.tetris/.MainActivity

随后 ida 设置

这里是为了加载每个 so 的时候断一下以防跑飞。

随后直接 attach 上该进程，随后按下 F9，再 JDWP 继续运行该程序（这里设置的是进程 PID）。

jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=18367

安卓调试原理可参考

https://bbs.kanxue.com/thread-266378.htm#msg_header_h1_0

随后 IDA 调试可以发现会闪退，原因是有有个检测，而这个检测就在 init_array 段的第一个函数，所以我们去 init_array 段先下个断点，ctrl + s 来到该段，点入再进入第一个函数第一行汇编下断点。

按几下 F9 即可跑到我们下断点（中间可能会问你 same or not same，直接 same 即可），而开启反调试的代码就在我们当前函数的最后一句。

而我们只需要不启动这个线程即可，在这里直接 ctrl + n 到 xxxx8E84 或修改 eip 即可。

随后在旁边的 modules 里搜索该模块找到我们要分析的函数在开头下个断点，再按几下 F9 即可。

稍许调试就可以找到第一处关键点，就是我们这题的目标找到 boot_id，这里就是取出自己手机的 boot_id。

随后继续调试可以发现对我们的 bootid 进行了 AES 加密，其实 key 是固定的，而 iv 是根据 ANDROID_ID，再然后就是 RC4 加密，密钥直接调试就可以拿到了。

那么分析到这就可以整理一下目前的信息

也可以通过 hook + 抓包的方式来对比流量包里的数据，同样可以确定流量包里的有我们要的密文与 iv。

那么另一种获取的方法就是通过 Frida，通过刚刚的调试可以发现 init_array 的第一个函数就是反调试反检测函数，那么我们只需要在程序启动的时候 hook 绕过该检测函数，再去 hook 我们目标函数获取参数即可。

可参考：DetectFrida/app/src/main/c/native-lib.c at master · darvincisec/DetectFrida · GitHub

Hook init_array 需要知道在 so 文件的加载过程，系统会自动调用 init、init_array 和 JNI_OnLoad 函数，其中 init 和 init_array 是在 dlopen 函数执行过程中调用， JNI_Onload 是在 dlopen 函数执行之后调用的，但我们想 Hook init，只 Hook dlopen 是做不到的，在 dlopen 的 onEnter 函数中， so 文件还没加载，无法 Hook init，在 onLeave 函数时，init 又加载完毕。

所以想要 Hook init 或是 init_array，需要在 dlopen 函数内部找一个 Hook 点，该函数必须满足两点：

于是 linker 中的 call_constructors 满足这些需求，该函数用于调用 so 文件中的 init 和 init_array，并且该函数在 linker 的符号表中，不需要通过偏移来计算函数地址。

于是在 linker 中找到该函数地址后，直接把我们想 hook 的函数写上即可。

function hook_call_constructors() {
 var _symbols = Process.getModuleByName('linker64').enumerateSymbols();
 var call_constructors_addr = null;
 
 for (let index = 0; index < _symbols.length; index++) {
 var _symbol = _symbols[index];
 if (_symbol.name.indexOf('call_constructors') != -1) {
 call_constructors_addr = _symbol.address;
 break;
 }
 }
 
 var detach_listener = Interceptor.attach(call_constructors_addr, {
 onEnter: function(args) {
 console.log('[*] now you can hook init_array');
 replace_init_array();
 hook_native_1();
 hook_native_2();
 hook_sub_189EC();
 hook_sub_17FB8();
 detach_listener.detach();
 }
 });
 }

完整代码

function HookLibWithCallbackOnEnter(name, callback) {
 var android_dlopen_ext =
 Module.findExportByName('libdl.so', 'android_dlopen_ext');
 var detach_listener_II = Interceptor.attach(android_dlopen_ext, {
 onEnter: function(args) {
 var cur = args[0].readCString();
 console.log('[+] android_dlopen_ext called, name: ' + cur);
 if (cur.indexOf(name) != -1) {
 console.log('[+] Hook Lib success, name:', name);
 callback();
 detach_listener_II.detach()
 }
 }
 });
 }
 
 function LogModule(module) {
 console.log('Module name: ' + module.name);
 console.log('Module base: ' + module.base);
 console.log('Module size: ' + module.size);
 }
 
 function TraverseModules(mode, {name = '', name_array = []}) {
 if (mode == 'all') {
 var modules = Process.enumerateModules();
 for (var i = 0; i < modules.length; i++) {
 var module = modules[i];
 // LogModule(module);
 }
 return modules;
 } else if (mode == 'single') {
 var module = Process.getModuleByName(name);
 LogModule(module);
 return module;
 } else if (mode == 'multiple') {
 var modules = Process.enumerateModules();
 var target_modules = [];
 for (var i = 0; i < modules.length; i++) {
 var module = modules[i];
 if (name_array.indexOf(module.name) != -1) {
 LogModule(module);
 target_modules.push(module);
 }
 }
 return target_modules;
 }
 }
 
 function replace_init_array() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var sub_13900 = libnative.base.add(0x13900);
 Interceptor.replace(sub_13900, new NativeCallback(function() {
 console.log('[*] anti-cheat had been removed');
 }, 'void', []));
 }
 
 function hook_native_1() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var loc_14BEC = libnative.base.add(0x14BEC);
 Interceptor.attach(loc_14BEC, {
 onEnter: function(args) {
 console.log('[*] loc_14BEC (native_1) called');
 }
 });
 }
 
 function hook_native_2() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var loc_15F8C = libnative.base.add(0x15F8C);
 Interceptor.attach(loc_15F8C, {
 onEnter: function(args) {
 console.log('[*] loc_15F8C (native_2) called');
 }, onLeave: function (retval) {
 console.log(retval.readCString())
 }
 });
 }
 
 function hook_sub_189EC() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var sub_189EC = libnative.base.add(0x189EC);
 Interceptor.attach(sub_189EC, {
 onEnter: function(args) {
 console.log('[*] sub_189EC (AES) called');
 console.log(args[0].readByteArray(64));
 console.log(args[1].readCString());
 console.log(args[2]);
 console.log(args[3].readCString());
 console.log(args[4].readCString());
 }
 });
 }
 
 function hook_sub_17FB8() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var sub_17FB8 = libnative.base.add(0x17FB8);
 Interceptor.attach(sub_17FB8, {
 onEnter: function(args) {
 console.log('[*] sub_17FB8 (RC4_INIT) called');
 console.log(args[1].readCString());
 }
 });
 }
 
 function hook_call_constructors() {
 var _symbols = Process.getModuleByName('linker64').enumerateSymbols();
 var call_constructors_addr = null;
 
 for (let index = 0; index < _symbols.length; index++) {
 var _symbol = _symbols[index];
 if (_symbol.name.indexOf('call_constructors') != -1) {
 call_constructors_addr = _symbol.address;
 break;
 }
 }
 
 var detach_listener = Interceptor.attach(call_constructors_addr, {
 onEnter: function(args) {
 console.log('[*] now you can hook init_array');
 replace_init_array();
 hook_native_1();
 hook_native_2();
 hook_sub_189EC();
 hook_sub_17FB8();
 detach_listener.detach();
 }
 });
 }
 
 function HookNativeOnEnter() {
 hook_call_constructors()
 }
 
 
 function main() {
 HookLibWithCallbackOnEnter('libnative.so', HookNativeOnEnter);
 }
 
 main();

// frida -U -f com.jetgame.tetris --no-pause -l terits.js

那么所需的数据都有了，就可以解密了，根据密钥长度与 AES 主函数可以确定是 AES-256 CBC，而该 AES 修改了一些地方。

__int64 __fastcall round(__int64 w, _BYTE *p, unsigned __int8 *a3, _BYTE *ww)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 v84 = *(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 v7 = p[4]; // 状态矩阵
 v8 = p[8];
 v9 = p[12];
 v10 = *ww ^ *p;
 v11 = p[1];
 v12 = p[5];
 v13 = p[9];
 v14 = p[13];
 v15 = p[2];
 v16 = p[6];
 v17 = p[10];
 v18 = p[14];
 v19 = p[3];
 v20 = p[7];
 v21 = p[11];
 v22 = p[15];
 v68 = v10;
 v23 = 1;
 v24 = 16;
 v25 = ww[4] ^ v7; // 轮密钥加
 v69 = v25;
 v26 = ww[8] ^ v8;
 v70 = v26;
 v27 = ww[12] ^ v9;
 v71 = v27;
 v28 = ww[1] ^ v11;
 v72 = v28;
 v29 = ww[5] ^ v12;
 v73 = v29;
 v30 = ww[9] ^ v13;
 v74 = v30;
 v31 = ww[13] ^ v14;
 v75 = v31;
 v32 = ww[2] ^ v15;
 v76 = v32;
 v33 = ww[6] ^ v16;
 v77 = v33;
 v34 = ww[10] ^ v17;
 v78 = v34;
 v79 = ww[14] ^ v18;
 v80 = ww[3] ^ v19;
 v81 = ww[7] ^ v20;
 v82 = ww[11] ^ v21;
 for ( i = ww[15] ^ v22; ; i ^= v51[15] )
 {
 v35 = byte_75EF53F395[(v25 & 0xF0) + (v25 & 0xF)];// 字节代换
 v36 = byte_75EF53F395[(v26 & 0xF0) + (v26 & 0xF)];
 v37 = byte_75EF53F395[(v27 & 0xF0) + (v27 & 0xF)];
 v38 = byte_75EF53F395[(v28 & 0xF0) + (v28 & 0xF)];
 v39 = byte_75EF53F395[(v29 & 0xF0) + (v29 & 0xF)];
 v40 = byte_75EF53F395[(v30 & 0xF0) + (v30 & 0xF)];
 v41 = byte_75EF53F395[(v31 & 0xF0) + (v31 & 0xF)];
 v42 = byte_75EF53F395[(v32 & 0xF0) + (v32 & 0xF)];
 v43 = byte_75EF53F395[(v33 & 0xF0) + (v33 & 0xF)];
 v44 = *(w + 4) - 1;
 v45 = byte_75EF53F395[(v34 & 0xF0) + (v34 & 0xF)];
 v68 = byte_75EF53F395[(v10 & 0xF0) + (v10 & 0xF)];
 v69 = v35;
 v70 = v36;
 v71 = v37;
 v72 = v38;
 v73 = v39;
 v74 = v40;
 v75 = v41;
 v46 = byte_75EF53F395[(v79 & 0xF0) + (v79 & 0xF)];
 v47 = byte_75EF53F395[(v80 & 0xF0) + (v80 & 0xF)];
 v48 = byte_75EF53F395[(v81 & 0xF0) + (v81 & 0xF)];
 v49 = byte_75EF53F395[(v82 & 0xF0) + (v82 & 0xF)];
 v50 = byte_75EF53F395[(i & 0xF0) + (i & 0xF)];
 v76 = v42;
 v77 = v43;
 v78 = v45;
 v79 = v46;
 v80 = v47;
 v81 = v48;
 v82 = v49;
 i = v50;
 if ( v23 > v44 )
 break;
 mixColumns(v45, &v68); // 列混合
 shiftRows(w, &v68); // 行移位，这两个变了位置
 v51 = &ww[v24];
 v10 = *v51 ^ v68;
 v68 = v10;
 v25 = v51[4] ^ v69;
 v69 = v25;
 v26 = v51[8] ^ v70;
 v70 = v26;
 ++v23;
 v27 = v51[12] ^ v71;
 v71 = v27;
 v24 += 16;
 v28 = v51[1] ^ v72;
 v72 = v28;
 v29 = v51[5] ^ v73;
 v73 = v29;
 v30 = v51[9] ^ v74;
 v74 = v30;
 v31 = v51[13] ^ v75;
 v75 = v31;
 v32 = v51[2] ^ v76;
 v76 = v32;
 v33 = v51[6] ^ v77;
 v77 = v33;
 v34 = v51[10] ^ v78;
 v78 = v34;
 v79 ^= v51[14];
 v80 ^= v51[3];
 v81 ^= v51[7];
 v82 ^= v51[11];
 }
 shiftRows(w, &v68); // 新出的行移位
 v52 = &ww[16 * *(w + 4)]; // 轮密钥加
 v68 ^= *v52;
 v69 ^= v52[4];
 v53 = v69;
 v70 ^= v52[8];
 v54 = v70;
 v71 ^= v52[12];
 v55 = v71;
 v72 ^= v52[1];
 v56 = v72;
 v73 ^= v52[5];
 v57 = v73;
 v74 ^= v52[9];
 v58 = v74;
 v75 ^= v52[13];
 v59 = v75;
 v76 ^= v52[2];
 v60 = v76;
 result = v52[6] ^ v77;
 v77 ^= v52[6];
 v78 ^= v52[10];
 v62 = v78;
 v79 ^= v52[14];
 v63 = v79;
 v80 ^= v52[3];
 v64 = v80;
 v81 ^= v52[7];
 v65 = v81;
 v82 ^= v52[11];
 v66 = v82;
 v67 = i;
 LOBYTE(v52) = v52[15];
 *a3 = v68;
 a3[4] = v53;
 a3[8] = v54;
 a3[12] = v55;
 a3[1] = v56;
 a3[5] = v57;
 a3[9] = v58;
 a3[13] = v59;
 a3[2] = v60;
 a3[6] = result;
 a3[10] = v62;
 a3[14] = v63;
 a3[3] = v64;
 a3[7] = v65;
 a3[11] = v66;
 a3[15] = v52 ^ v67;
 return result;
}

拿别的师傅整理好的，这是所有修改的地方

ASE模板：https://github.com/kokke/tiny-AES-c

static const uint8_t sbox[256] = { 144, 122, 80, 239, 240, 156, 47, 125, 160, 52, 35, 202, 79, 33, 102, 107, 61, 224, 194, 179, 252, 105, 8, 255, 127, 22, 72, 213, 235, 89, 216, 12, 243, 228, 168, 234, 185, 129, 1, 40, 19, 184, 108, 203, 220, 138, 39, 25, 210, 164, 211, 153, 73, 87, 135, 223, 45, 74, 193, 88, 180, 104, 222, 199, 148, 123, 170, 226, 140, 83, 173, 30, 4, 197, 24, 0, 237, 241, 121, 67, 81, 176, 132, 90, 238, 151, 136, 38, 182, 115, 157, 91, 254, 229, 84, 244, 177, 6, 63, 188, 49, 96, 161, 133, 201, 248, 198, 231, 174, 195, 130, 159, 251, 206, 253, 50, 141, 46, 65, 191, 55, 183, 236, 119, 2, 128, 59, 118, 146, 20, 208, 76, 56, 137, 28, 70, 43, 11, 196, 114, 14, 205, 98, 16, 111, 9, 143, 124, 212, 215, 109, 247, 155, 172, 32, 18, 100, 221, 204, 250, 112, 249, 53, 29, 154, 82, 245, 13, 175, 186, 166, 48, 41, 139, 126, 192, 131, 149, 97, 68, 163, 34, 117, 94, 167, 85, 42, 145, 242, 66, 162, 86, 181, 95, 219, 54, 71, 190, 134, 165, 64, 21, 93, 142, 189, 200, 26, 209, 60, 7, 17, 51, 187, 110, 158, 150, 58, 218, 57,92, 44, 31, 23, 230, 37, 106, 10, 62, 147, 233, 116, 101, 171, 77, 207, 232, 120, 15, 178, 225, 246, 113, 3, 169, 27, 214, 99, 78, 217, 36, 152, 103, 69, 5, 227, 75 };
static const uint8_t rsbox[256] = { 75, 38, 124, 242, 72, 253, 97, 209, 22, 145, 226, 137, 31, 167, 140, 237, 143, 210, 155, 40, 129, 201, 25, 222, 74, 47, 206, 244, 134, 163, 71, 221, 154, 13, 181, 10, 249, 224, 87, 46, 39, 172, 186, 136, 220, 56, 117, 6, 171, 100, 115, 211, 9, 162, 195, 120, 132, 218, 216, 126, 208, 16, 227, 98, 200, 118, 189, 79, 179, 252, 135, 196, 26, 52, 57, 255, 131, 233, 247, 12, 2, 80, 165, 69, 94, 185, 191, 53, 59, 29, 83, 91, 219, 202, 183, 193, 101, 178, 142, 246, 156, 231, 14, 251, 61, 21, 225, 15, 42, 150, 213, 144, 160, 241, 139, 89, 230, 182, 127, 123, 236, 78, 1, 65, 147, 7, 174, 24, 125, 37, 110, 176, 82, 103, 198, 54, 86, 133, 45, 173, 68, 116, 203, 146, 0, 187, 128, 228, 64, 177, 215, 85, 250, 51, 164, 152, 5, 90, 214, 111, 8, 102, 190, 180, 49, 199, 170, 184, 34, 243, 66, 232, 153, 70, 108, 168, 81, 96, 238, 19, 60, 192, 88, 121, 41, 36, 169, 212, 99, 204, 197, 119, 175, 58, 18, 109, 138, 73, 106, 63, 205, 104, 11, 43, 158, 141, 113, 234, 130, 207, 48, 50, 148, 27, 245, 149, 30, 248, 217, 194, 44, 157, 62, 55, 17, 239, 67, 254, 33, 93, 223, 107, 235, 229, 35, 28, 122, 76, 84, 3, 4, 77, 188, 32, 95, 166, 240, 151, 105, 161, 159, 112, 20, 114, 92, 23 };

static void Cipher(state_t* state, const uint8_t* RoundKey)
{
 uint8_t round = 0;

 // Add the First round key to the state before starting the rounds.
 AddRoundKey(0, state, RoundKey);
 
 for (round = 1; ; ++round)
 {
 SubBytes(state);
 if (round == Nr) {
 break;
 }
 // These two change the order
 MixColumns(state);
 ShiftRows(state);
 
 AddRoundKey(round, state, RoundKey);
 }
 // Add round key to last round
 ShiftRows(state);
 AddRoundKey(Nr, state, RoundKey);
}

static void InvCipher(state_t* state, const uint8_t* RoundKey)
{
 uint8_t round = 0;

 // Add the First round key to the state before starting the rounds.
 AddRoundKey(Nr, state, RoundKey);
 InvShiftRows(state);
 
 for (round = (Nr - 1); ; --round)
 {
 InvSubBytes(state);
 AddRoundKey(round, state, RoundKey);
 if (round == 0) {
 break;
 }
 InvShiftRows(state);
 InvMixColumns(state);
 }
}

ase.h 文件修改成 AES256

main.c

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define CBC 1

#include "aes.h" 

int main() {
 uint8_t plaintxt[48] = { 166, 98, 46, 98, 247, 122, 195, 92, 107, 245, 116, 68, 109, 138, 246, 178, 164, 132, 68, 240, 247, 142, 161, 208, 221, 9, 198, 98, 39, 8, 116, 233 };
 uint8_t rc4_key[32] = { 0xe5,0xc5,0xc8,0x6f,0xd4,0x04,0x84,0x75,0x0f,0x46,0xcd,0xca,0x65,0x7d,0x9a,0x7c,0x37,0x04,0x3c,0x56,0xec,0x4c,0x9a,0xe2,0xb8,0x31,0xa3,0x81,0x88,0x25,0x8b,0x10 };
 for (int i = 0; i < 32; i++) {
 plaintxt[i] ^= rc4_key[i];
 }
 uint8_t key[32] = "A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!";
 uint8_t iv[16] = "3d354e98963a69b2";

 struct AES_ctx ctx;

 AES_init_ctx_iv(&ctx, key, iv);
 AES_CBC_decrypt_buffer(&ctx, plaintxt, 32);
 
 puts(plaintxt);

 return 0;
}

Get Flag!

官方题解搜Q群：532023069

http://lu1u.bxsteam.tk/2023/05/02/d3ctf-re/#d3Hell

https://mp.weixin.qq.com/s?__biz=Mzg4MjcxMTAwMQ==&mid=2247486967&idx=1&sn=ad55ddd11c6bfa17843270625f5f92fc&chksm=cf53cd41f8244457c2db68626c91f2e4564d756b903222f3a913e89f211d475418864c5041bc&mpshare=1&scene=23&srcid=0501bEUrW8ydbpm175TL5FFn&sharer_sharetime=1682949687637&sharer_shareid=6eea79ff6da57fc6752ab0bc570bf392#rd

https://fq6p9pyo5tt.feishu.cn/docx/InUFdQUKdozf8yx5IhGcf5zInSe

视频版：
https://www.bilibili.com/video/BV13P41117B6/?spm_id_from=333.999.0.0
https://www.bilibili.com/video/BV1Mh41157fr/?spm_id_from=333.999.0.0

看雪ID：P.Z

https://bbs.kanxue.com/user-home-930234.htm

*本文为看雪论坛精华文章，由 P.Z 原创，转载请注明来自看雪社区

# 往期推荐

1、在 Windows下搭建LLVM 使用环境

2、深入学习smali语法

3、安卓加固脱壳分享

4、Flutter 逆向初探

5、一个简单实践理解栈空间转移

6、记一次某盾手游加固的脱壳与修复

球分享

球点赞

球在看


```
一
D3SKY
```



```
unsigned int sub_3B1050()
{
 unsigned int v0; // eax

 if ( !IsDebuggerPresent() )
 Str[5] = 49;
 v0 = strlen("YunZhiJun");
 RC4_INIT(&Sbox, "YunZhiJun", v0);
 return RC4(&Sbox, st_input, 74u);
}
```



```
int __cdecl main(int argc, const char **argv, const char **envp)
{
 int v4; // [esp+0h] [ebp-24h]
 int v5; // [esp+Ch] [ebp-18h]
 unsigned __int16 p2; // [esp+14h] [ebp-10h]
 unsigned __int16 p0; // [esp+18h] [ebp-Ch]
 unsigned __int16 p1; // [esp+1Ch] [ebp-8h]
 unsigned __int16 i; // [esp+20h] [ebp-4h]

 v5 = 0;
 puts("Welcome to D^3CTF~");
 while ( op[0] != 0xFFFF )
 {
 if ( op[2] == 1 )
 {
 op[2] = 0;
 printf("%c", op[3]);
 }
 if ( op[7] == 1 )
 {
 op[7] = 0;
 scanf("%c", &op[8]);
 v4 = v5++;
 if ( v4 == 37 && op[8] != 0x7E )
 {
 puts("Wrong!");
 return 0;
 }
 }
 if ( op[19] )
 {
 puts("Wrong!");
 return 0;
 }
 i = op[0];

 RC4(&Sbox, &op[op[0]], 3u);
 p0 = op[i];
 p1 = op[i + 1];
 p2 = op[i + 2];

 op[0] = i + 3;
 RC4(&Sbox, &op[i], 3u);
 op[p2] = ~(op[p0] & op[p1]);
 }
 puts("Right! Your flag is antd3ctf{your input}");
 return 0;
}
```



```
op_addr = 0x5B4018
ebp = idc.get_reg_value('ebp')
p0 = ida_bytes.get_word(ebp - 0xC)
p1 = ida_bytes.get_word(ebp - 0x8)
p2 = ida_bytes.get_word(ebp - 0x10)

op_p0 = ida_bytes.get_word(op_addr + p0 * 2)
op_p1 = ida_bytes.get_word(op_addr + p1 * 2)
print('op[%d] = ~(op[%d] & op[%d]) ' % (p2, p0, p1), '(op[%d] = ~(%d & %d))' % (p2, op_p0, op_p1) )
```



```
op_addr = 0x5B4018
ebp = idc.get_reg_value('ebp')
v4 = ida_bytes.get_word(ebp - 0x24) 
if (v4 == 36):
 print('----------------------------END INPUT------------------------------')
```



```
...
op[11] = ~(op[20] & op[20]) (op[11] = ~(1 & 1))
op[7] = ~(op[11] & op[11]) (op[7] = ~(65534 & 65534))
---------------------END INPUT----------------------
op[7] = ~(op[8] & op[8]) (op[7] = ~(126 & 126))
op[2808] = ~(op[7] & op[7]) (op[2808] = ~(65409 & 65409))
op[11] = ~(op[2772] & op[2772]) (op[11] = ~(49 & 49))
op[11] = ~(op[11] & op[2773]) (op[11] = ~(65486 & 50))
op[12] = ~(op[2773] & op[2773]) (op[12] = ~(50 & 50))
op[12] = ~(op[12] & op[2772]) (op[12] = ~(65485 & 49))
op[17] = ~(op[11] & op[12]) (op[17] = ~(65533 & 65534))
op[11] = ~(op[2774] & op[2774]) (op[11] = ~(51 & 51))
op[11] = ~(op[11] & op[2775]) (op[11] = ~(65484 & 52))
op[12] = ~(op[2775] & op[2775]) (op[12] = ~(52 & 52))
op[12] = ~(op[12] & op[2774]) (op[12] = ~(65483 & 51))
op[18] = ~(op[11] & op[12]) (op[18] = ~(65531 & 65532))
op[11] = ~(op[17] & op[17]) (op[11] = ~(3 & 3))
op[11] = ~(op[11] & op[18]) (op[11] = ~(65532 & 7))
op[12] = ~(op[18] & op[18]) (op[12] = ~(7 & 7))
op[12] = ~(op[12] & op[17]) (op[12] = ~(65528 & 3))
op[18] = ~(op[11] & op[12]) (op[18] = ~(65531 & 65535))
op[11] = ~(op[2809] & op[2809]) (op[11] = ~(36 & 36))
op[11] = ~(op[11] & op[18]) (op[11] = ~(65499 & 4))
op[12] = ~(op[18] & op[18]) (op[12] = ~(4 & 4))
op[12] = ~(op[12] & op[2809]) (op[12] = ~(65531 & 36))
op[19] = ~(op[11] & op[12]) (op[19] = ~(65535 & 65503))
```



```
#include <cstdio>
#include <cstring>
#include "defs.h"
#include <cstdlib>
#define _CRT_SECURE_NO_WARNINGS
```



```
# op[17] = in[0] ^ in[1]
op[11] = ~(data[0] & data[0])
op[11] = ~(op[11] & data[1])
op[12] = ~(data[1] & data[1])
op[12] = ~(op[12] & data[0])
op[17] = ~(op[11] & op[12])

# op[18] = in[2] ^ in[3]
op[11] = ~(data[2] & data[2])
op[11] = ~(op[11] & data[3])
op[12] = ~(data[3] & data[3])
op[12] = ~(op[12] & data[2])
op[18] = ~(op[11] & op[12])

# op[18] = op[17] ^ op[18]
op[11] = ~(op[17] & op[17])
op[11] = ~(op[11] & op[18])
op[12] = ~(op[18] & op[18])
op[12] = ~(op[12] & op[17])
op[18] = ~(op[11] & op[12])

# check
op[11] = ~(data[37] & data[37]) # data[37]也就是我们的密文第一位
op[11] = ~(op[11] & op[18])
op[12] = ~(op[18] & op[18])
op[12] = ~(op[12] & data[37])
op[19] = ~(op[11] & op[12])
```



```
from z3 import *

enc = [0x0024, 0x000B, 0x006D, 0x000F, 0x0003, 0x0032, 0x0042, 0x001D, 0x002B, 0x0043, 0x0078, 0x0043, 0x0073, 0x0030, 0x002B, 0x004E, 0x0063, 0x0048, 0x0077, 0x002E, 0x0032, 0x0039, 0x001A, 0x0012, 0x0071, 0x007A, 0x0042, 0x0017, 0x0045, 0x0072, 0x0056, 0x000C, 0x005C, 0x004A, 0x0062, 0x0053, 0x0033]
sol = Solver()
input = [BitVec('input%d' % i, 8) for i in range(37)]

sol.add(input[36] == ord('~'))

for i in range(37):
 sol.add((input[i] ^ input[(i + 1) % 37] ^ input[(i + 2) % 37] ^ input[(i + 3) % 37]) == enc[i])

assert sat == sol.check()
ans = sol.model()
for i in range(37):
 print(chr(ans[input[i]].as_long()), end = "")
# A_Sin91e_InS7rUcti0N_ViRTua1_M4chin3~
```



```
二
D3RC4
```



```
#include <unistd.h>
int pipe (int fd[2]);
 //返回:成功返回0，出错返回-1
```



```
unsigned __int64 father()
{
 int v1; // eax
 __WAIT_STATUS stat_loc; // [rsp+4h] [rbp-2Ch] BYREF
 int i; // [rsp+Ch] [rbp-24h]
 int j; // [rsp+10h] [rbp-20h]
 int k; // [rsp+14h] [rbp-1Ch]
 __pid_t p; // [rsp+18h] [rbp-18h]
 int v7; // [rsp+1Ch] [rbp-14h]
 int ffd[2]; // [rsp+20h] [rbp-10h] BYREF
 unsigned __int64 v9; // [rsp+28h] [rbp-8h]

 v9 = __readfsqword(0x28u);
 if ( pipe(ffd) == -1 )
 exit(1);
 p = fork();
 if ( p < 0 )
 exit(1);

 if ( p ) // 父进程
 {
 close(ffd[0]);
 v7 = 2;
 HIDWORD(stat_loc.__iptr) = 3;
 while ( SHIDWORD(stat_loc.__iptr) < len ) // 主进程写数据
 {
 if ( SHIDWORD(stat_loc.__iptr) % v7 ) // 奇数
 write(ffd[1], &stat_loc.__iptr + 4, 4uLL);
 else // 偶数，执行十六次
 ++p1;
 ++HIDWORD(stat_loc.__iptr);
 }

 close(ffd[1]); // 关闭写端开始读子进程的数据放入密钥
 close(fd0[1]);
 while ( read(fd0[0], &stat_loc.__iptr + 4, 4uLL) )
 {
 v1 = p2++;
 aWe1c0m3T0D3ctf[v1] = BYTE4(stat_loc.__iptr);// 修改了Key
 }

 close(fd0[0]); // 关闭读端，再起一个子进程
 wait(&stat_loc);

 if ( LODWORD(stat_loc.__uptr) )
 {
 puts(s);
 exit(1);
 }

 p = fork();
 if ( p < 0 )
 exit(1);

 if ( !p ) // 子进程
 {
 init_key(Sbox, aWe1c0m3T0D3ctf, p2);
 for ( i = 0; i < p1; ++i )
 RC4(Sbox, len, xor_key);
 for ( j = 0; j < len; j += 2 )
 {
 in1[j] = (in1[j] + in1[j + 1]) ^ xor_key[j];
 in1[j + 1] = xor_key[j + 1] ^ (in1[j] - in1[j + 1]);
 }
 for ( k = 0; k < len; ++k )
 {
 if ( in1[k] != enc[k] )
 exit(1);
 }
 exit(0);
 }

 wait(&stat_loc); // 父进程调用wait等待子进程退出
 if ( LODWORD(stat_loc.__uptr) ) // 根据子进程返回值输出，就是最后的check了
 puts(s);
 else
 puts(aGqk9lLwyvj);
 exit(0);
 }
 child(ffd);
 return v9 - __readfsqword(0x28u);
}
```



```
unsigned __int64 __fastcall child(int *ffd)
{
 int v2; // eax
 int buf; // [rsp+18h] [rbp-28h] BYREF
 __WAIT_STATUS stat_loc; // [rsp+1Ch] [rbp-24h] BYREF
 int i; // [rsp+24h] [rbp-1Ch]
 int j; // [rsp+28h] [rbp-18h]
 __pid_t v7; // [rsp+2Ch] [rbp-14h]
 int lfd[2]; // [rsp+30h] [rbp-10h] BYREF
 unsigned __int64 v9; // [rsp+38h] [rbp-8h]

 v9 = __readfsqword(0x28u);
 close(ffd[1]);
 if ( !read(*ffd, &buf, 4uLL) ) // 读不到数据就退
 exit(1);
 if ( pipe(lfd) == -1 )
 exit(1);

 v7 = fork();
 if ( v7 < 0 )
 exit(1);

 if ( v7 ) // 子父进程
 {
 close(lfd[0]);
 close(fd0[0]);

 write(fd0[1], &buf, 4uLL); // 写入的就是从ffd管道读到的值，也就是Buf[0]，随后写入key
 close(fd0[1]);

 while ( read(*ffd, &stat_loc.__iptr + 4, 4uLL) )// 向上读入 其父进程 传入的值
 {
 if ( SHIDWORD(stat_loc.__iptr) % buf ) // 余第一项，注意每次都不一样，随后向下递归写入取值
 write(lfd[1], &stat_loc.__iptr + 4, 4uLL);
 else
 ++p1;
 }
 close(lfd[1]);
 wait(&stat_loc);

 v2 = p2++; // 注意fork后的子进程和父进程不共有这些值，所以随便改也没事
 aWe1c0m3T0D3ctf[v2] = Sbox[buf];
 init_key(Sbox, aWe1c0m3T0D3ctf, p2);
 for ( i = 0; i < 256 - p1; ++i )
 {
 RC4(Sbox, len, xor_key);
 for ( j = 0; j < len; j += 2 )
 {
 in1[j] = (in1[j] + in1[j + 1]) ^ xor_key[j];
 in1[j + 1] = xor_key[j + 1] ^ (in1[j] - in1[j + 1]);
 }
 }
 exit(0);
 }
 child(lfd);
 return v9 - __readfsqword(0x28u);
}
```



```
def get_key(arr):
 if len(arr) <= 0:
 return
 global key
 key.append(arr[0])

 new_arr = []
 for i in range(1, len(arr)):
 if arr[i] % arr[0] != 0:
 new_arr.append(arr[i])

 get_key(new_arr)

arr = []
global key
key = bytearray(b'We1c0m3_t0_d^3ctf')
for i in range(3, 36):
 if i % 2 != 0: 
 arr.append(i)
get_key(arr)
print(key)

# b'We1c0m3_t0_d^3ctfx03x05x07x0brx11x13x17x1dx1f'
```



```
if ( LODWORD(stat_loc.__uptr) )
 {
 puts(s);
 exit(1);
 }
```



```
from z3 import *

def init_key(Sbox, key, p2):
 v4 = 0
 for i in range(256):
 v4 = (Sbox[i] + v4 + key[i % p2]) % 256
 Sbox[i], Sbox[v4] = Sbox[v4], Sbox[i]

def RC4(Sbox, l):
 v7 = -1
 v5 = 0
 v6 = 0
 xor_key = [0] * 104
 while (l):
 v5 = (v5 + 1) % 256
 v6 = (v6 + Sbox[v5]) % 256
 Sbox[v6], Sbox[v5] = Sbox[v5], Sbox[v6]
 v7 += 1
 xor_key[v7] = Sbox[(Sbox[v5] + Sbox[v6]) % 256]
 l -= 1
 return xor_key

def Encrypt(input):
 global Sbox
 Sbox = [0] * 256
 for i in range(256):
 Sbox[i] = i
 enc = [0xF7, 0x5F, 0xE7, 0xB0, 0x9A, 0xB4, 0xE0, 0xE7, 0x9E, 0x05, 
 0xFE, 0xD8, 0x35, 0x5C, 0x72, 0xE0, 0x86, 0xDE, 0x73, 0x9F, 
 0x9A, 0xF6, 0x0D, 0xDC, 0xC8, 0x4F, 0xC2, 0xA4, 0x7A, 0xB5, 
 0xE3, 0xCD, 0x60, 0x9D, 0x04, 0x1F]

 sol = Solver()
 # main decryption
 p1 = 17
 p2 = 17 
 l = len(input)
 key = b'We1c0m3_t0_d^3ctf'
 init_key(Sbox, key, p2)
# print(Sbox)
 xor_key = RC4(Sbox, l)
# print(xor_key)
 in1 = [0] * 36
 for i in range(l):
 in1[i] = input[i] ^ xor_key[i]
 

 key = b'We1c0m3_t0_d^3ctfx03x05x07x0brx11x13x17x1dx1f'
 # father-child decryption
 init_key(Sbox, key, len(key))
 for i in range(p1):
 xor_key = RC4(Sbox, l)
 print(xor_key)
 for j in range(0, l, 2):
 in1[j] = (in1[j] + in1[j + 1]) ^ xor_key[j]
 in1[j + 1] = xor_key[j + 1] ^ (in1[j] - in1[j + 1])
 for i in range(l):
 sol.add(in1[i] == enc[i])
 
 assert sat == sol.check()
 ans = sol.model()
 for i in range(l):
 print(chr(ans[input[i]].as_long()), end = "")

input = [BitVec('input%d' % i, 8) for i in range(36)]
Encrypt(input)
# getting_primes_with_pipes_is_awesome
```



```
三
D3RECOVER
```



```
for ( i = 0LL; i <= 31; ++i )
 _Pyx_PyByteArray_Append(v9, input ^ 0x23u)
for ( j = 0LL; j <= 29; ++j )
{
 input_t1 = input[index]
 input_t1 = input[index + 2]
 PyNumber_Add(input_t1, input_t2)
 Pyx_PyInt_AndObjC(index, num_0xFF, 0xFFLL, 0LL, 0LL)
 _Pyx_PyInt_XorObjC(input_t2, num_0x54, 0x54LL, 0LL, 0LL)
}
```



```
from z3 import *

enc = [0xd3,0xc7,0xce,0xca,0x3f,0x84,0xdb,0xb3,0xb6,0xb9,0x80,0xea,0xd0,0xcd,0x72,0xfc,0xd8,0x30,0x95,0xdb,0xe2,0xd8,0x92,0x08,0xc1,0xc6,0xc5,0xf4,0x07,0xec,0x02,0x5e]
enc1 = [0x76,0x7c,0x72,0x78,0x7e,0x64,0x72,0x78,0x76,0x7c,0x72,0x78,0x7e,0x64,0x72,0x78,0x76,0x7c,0x72,0x78,0x7e,0x64,0x72,0x78,0x76,0x7c,0x72,0x78,0x7e,0x64,0x14,0x1b]
input = [BitVec("input%d" % i, 8) for i in range(32)]
sol = Solver()
in1 = [0] * 32
for i in range(32):
 in1[i] = input[i] ^ 0x23

for i in range(30):
 in1[i] = ((in1[i] + in1[i + 2]) & 0xFF) ^ 0x54

for i in range(32):
 sol.add(enc[i] == in1[i])

while sat == sol.check():
 ans = sol.model()
 for i in range(32):
 print(chr(ans[input[i]].as_long()), end = "")
 sol.add(Or([input[i] != ans[input[i]] for i in range(32)]) )
# flag{y0U_RE_Ma5t3r_0f_R3vocery!}
```



```
四
D3SYSCALL
```



```
*(sys_table + 2680) = mov; // v4[0x14F]
 v4[0x150] = ALU;
 v4[0x151] = push;
 v4[0x152] = pop;
 v4[0x153] = reset;
 v4[0x154] = check;
```



```
__int64 __fastcall mov(_QWORD *a1)
{
 __int64 rdi0; // rax
 unsigned __int64 rdx0; // r12
 unsigned __int64 rsi0; // rbx

 _fentry__(a1);
 rdi0 = a1[14]; // 我是通过传参顺序命名好所传入的变量
 rdx0 = a1[12];
 rsi0 = a1[13];
 if ( rdi0 )
 {
 if ( rdi0 == 1 )
 {
 if ( rsi0 > 3 )
 _ubsan_handle_out_of_bounds(&off_1800, a1[13]);// 像这种 out 就是越界了而程序正常执行是不会发生的
 tmp_reg[rsi0] = rdx0; // 我们只需要关注实际操作，如这条
 }
 }
 else
 {
 if ( rdx0 > 3 )
 _ubsan_handle_out_of_bounds(&off_1840, a1[12]);
 if ( rsi0 > 3 )
 _ubsan_handle_out_of_bounds(&off_1820, rsi0);
 tmp_reg[rsi0] = tmp_reg[rdx0];
 }
 if ( rsi0 > 3 )
 _ubsan_handle_out_of_bounds(&off_17E0, rsi0);
 return tmp_reg[rsi0];
}
```



```
def mov(rdx, rsi, rdi):
 if rdi == 1:
 print('tmp_reg[%x] = %x' %(rsi, rdx))
 else:
 print('tmp_reg[%x] = tmp_reg[%x]' %(rsi, rdx))
```



```
def mov(rdx, rsi, rdi):
 if rdi == 1:
 print('tmp_reg[%x] = %x' %(rsi, rdx))
 else:
 print('tmp_reg[%x] = tmp_reg[%x]' %(rsi, rdx))

def alu(rdx, rsi, rdi):
 if rdi == 3:
 print('tmp_reg[%x] = tmp_reg[%x] ^ tmp_reg[%x]' % (rsi, rdx, rsi))
 elif rdi == 4:
 print('tmp_reg[%x] = tmp_reg[%x] << tmp_reg[%x]' % (rsi, rsi, rdx))
 elif rdi == 5:
 print('tmp_reg[%x] = tmp_reg[%x] >> tmp_reg[%x]' % (rsi, rsi, rdx))
 elif rdi == 1:
 print('tmp_reg[%x] = tmp_reg[%x] - tmp_reg[%x]' % (rsi, rsi, rdx))
 elif rdi == 2:
 print('tmp_reg[%x] = tmp_reg[%x] * tmp_reg[%x]' % (rsi, rdx, rsi))
 else:
 print('tmp_reg[%x] = tmp_reg[%x] + tmp_reg[%x]' % (rsi, rdx, rsi))

def push(rsi, rdi):
 if rdi == 1:
 print('mem[tmp_reg[5] + 1] = %x' % (rsi))
 else:
 print('mem[tmp_reg[5] + 1] = tmp_reg[%x]' % (rsi))

def pop(rsi):
 print('tmp_reg[5] = tmp_reg[5] - 1')
 print('tmp_reg[%x] = mem[tmp_reg[5]]' % (rsi))

def reset():
 print('init_reg[0] = 0')
 print('init_reg[1] = 0')
 print('init_reg[2] = 0')
 print('init_reg[3] = 0')

def check():
 print('check mem == enc')

def syscall(op):
 if op[0] == 0x14F:
 mov(op[3], op[2], op[1])
 elif op[0] == 0x150:
 alu(op[3], op[2], op[1])
 elif op[0] == 0x151:
 push(op[2], op[1])
 elif op[0] == 0x152:
 pop(op[2])
 elif op[0] == 0x153:
 reset()
 elif op[0] == 0x154:
 check()

opcode = [[0x14f, 0x1, 0, 0x3837363534333231],
[0x14f, 0x1, 0x1, 0x3837363534333231],
[0x151, 0, 0x1, 0x3837363534333231],
[0x14f, 0, 0x2, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x4, 0x2, 0x1],
[0x14f, 0x1, 0x1, 0x51e7647e],
[0x150, 0, 0x2, 0x1],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x2, 0x3, 0x1],
[0x14f, 0x1, 0x1, 0xe0b4140a],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0xe6978f27],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0x1, 0x2, 0x3],
[0x150, 0, 0x1, 0x2],
[0x151, 0, 0x1, 0x2],
[0x151, 0, 0, 0x2],
[0x14f, 0, 0x2, 0x1],
[0x14f, 0x1, 0, 0x6],
[0x150, 0x4, 0x2, 0],
[0x14f, 0x1, 0, 0x53a35337],
[0x150, 0, 0x2, 0],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5],
[0x150, 0x2, 0x3, 0],
[0x14f, 0x1, 0, 0x9840294d],
[0x150, 0, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5eae4751],
[0x150, 0x1, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0, 0x2, 0x3],
[0x150, 0, 0, 0x2],
[0x151, 0, 0, 0x2],
[0x153, 0, 0, 0x2],
[0x14f, 0x1, 0, 0x3837363534333231],
[0x14f, 0x1, 0x1, 0x3837363534333231],
[0x151, 0, 0x1, 0x3837363534333231],
[0x14f, 0, 0x2, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x4, 0x2, 0x1],
[0x14f, 0x1, 0x1, 0x51e7647e],
[0x150, 0, 0x2, 0x1],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x2, 0x3, 0x1],
[0x14f, 0x1, 0x1, 0xe0b4140a],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0xe6978f27],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0x1, 0x2, 0x3],
[0x150, 0, 0x1, 0x2],
[0x151, 0, 0x1, 0x2],
[0x151, 0, 0, 0x2],
[0x14f, 0, 0x2, 0x1],
[0x14f, 0x1, 0, 0x6],
[0x150, 0x4, 0x2, 0],
[0x14f, 0x1, 0, 0x53a35337],
[0x150, 0, 0x2, 0],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5],
[0x150, 0x2, 0x3, 0],
[0x14f, 0x1, 0, 0x9840294d],
[0x150, 0, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5eae4751],
[0x150, 0x1, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0, 0x2, 0x3],
[0x150, 0, 0, 0x2],
[0x151, 0, 0, 0x2],
[0x153, 0, 0, 0x2],
[0x14f, 0x1, 0, 0x34333231],
[0x14f, 0x1, 0x1, 0],
[0x151, 0, 0x1, 0],
[0x14f, 0, 0x2, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x4, 0x2, 0x1],
[0x14f, 0x1, 0x1, 0x51e7647e],
[0x150, 0, 0x2, 0x1],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0x3],
[0x150, 0x2, 0x3, 0x1],
[0x14f, 0x1, 0x1, 0xe0b4140a],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0],
[0x14f, 0x1, 0x1, 0xe6978f27],
[0x150, 0, 0x3, 0x1],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0x1, 0x2, 0x3],
[0x150, 0, 0x1, 0x2],
[0x151, 0, 0x1, 0x2],
[0x151, 0, 0, 0x2],
[0x14f, 0, 0x2, 0x1],
[0x14f, 0x1, 0, 0x6],
[0x150, 0x4, 0x2, 0],
[0x14f, 0x1, 0, 0x53a35337],
[0x150, 0, 0x2, 0],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5],
[0x150, 0x2, 0x3, 0],
[0x14f, 0x1, 0, 0x9840294d],
[0x150, 0, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x14f, 0, 0x3, 0x1],
[0x14f, 0x1, 0, 0x5eae4751],
[0x150, 0x1, 0x3, 0],
[0x150, 0x3, 0x2, 0x3],
[0x152, 0, 0x2, 0x3],
[0x150, 0, 0, 0x2],
[0x151, 0, 0, 0x2],
[0x153, 0, 0, 0x2],
[0x154, 0, 0, 0x2]]

for op in opcode:
 syscall(op)

def encrypt(p1, p2, cnt):
 enc = [0xB0800699CB89CC89, 0x4764FD523FA00B19, 0x396A7E6DF099D700, 0xB115D56BCDEAF50A, 0x2521513C985791F4, 0xB03C06AF93AD0BE]
 p2 += ((p1 << 3) + 0x51e7647e) ^ (p1 * 3 + 0xe0b4140a) ^ (p1 + 0xe6978f27)
 p1 += ((p2 << 6) + 0x53a35337) ^ (5 * p2 + 0x9840294d) ^ (p2 - 0x5eae4751)
 sol.add(p1 == enc[cnt + 1])
 sol.add(p2 == enc[cnt])

from z3 import *

input = [BitVec('input%d' % i, 64) for i in range(6)]
sol = Solver()
for i in range(0, 6, 2):
 encrypt(input[i], input[i + 1], i)
assert sat == sol.check()
ans = sol.model()
for i in range(6):
 print(int.to_bytes(ans[input[i]].as_long(), 8, 'little').decode(),end='')
# d3ctf{cef9b994-2547-4844-ac0d-a097b75806a0}
```



```
五
D3Tetris
```



```
crosshatch:/ # ./data/local/tmp/7ad64
IDA Android 64-bit remote debug server(ST) v7.7.27. Hex-Rays (c) 2004-2022
Listening on 0.0.0.0:23946...
```



```
adb forward tcp:23946 tcp:23946
adb shell am start -D -n com.jetgame.tetris/.MainActivity
```



```
jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=18367
```



```
function hook_call_constructors() {
 var _symbols = Process.getModuleByName('linker64').enumerateSymbols();
 var call_constructors_addr = null;
 
 for (let index = 0; index < _symbols.length; index++) {
 var _symbol = _symbols[index];
 if (_symbol.name.indexOf('call_constructors') != -1) {
 call_constructors_addr = _symbol.address;
 break;
 }
 }
 
 var detach_listener = Interceptor.attach(call_constructors_addr, {
 onEnter: function(args) {
 console.log('[*] now you can hook init_array');
 replace_init_array();
 hook_native_1();
 hook_native_2();
 hook_sub_189EC();
 hook_sub_17FB8();
 detach_listener.detach();
 }
 });
 }
```



```
function HookLibWithCallbackOnEnter(name, callback) {
 var android_dlopen_ext =
 Module.findExportByName('libdl.so', 'android_dlopen_ext');
 var detach_listener_II = Interceptor.attach(android_dlopen_ext, {
 onEnter: function(args) {
 var cur = args[0].readCString();
 console.log('[+] android_dlopen_ext called, name: ' + cur);
 if (cur.indexOf(name) != -1) {
 console.log('[+] Hook Lib success, name:', name);
 callback();
 detach_listener_II.detach()
 }
 }
 });
 }
 
 function LogModule(module) {
 console.log('Module name: ' + module.name);
 console.log('Module base: ' + module.base);
 console.log('Module size: ' + module.size);
 }
 
 function TraverseModules(mode, {name = '', name_array = []}) {
 if (mode == 'all') {
 var modules = Process.enumerateModules();
 for (var i = 0; i < modules.length; i++) {
 var module = modules[i];
 // LogModule(module);
 }
 return modules;
 } else if (mode == 'single') {
 var module = Process.getModuleByName(name);
 LogModule(module);
 return module;
 } else if (mode == 'multiple') {
 var modules = Process.enumerateModules();
 var target_modules = [];
 for (var i = 0; i < modules.length; i++) {
 var module = modules[i];
 if (name_array.indexOf(module.name) != -1) {
 LogModule(module);
 target_modules.push(module);
 }
 }
 return target_modules;
 }
 }
 
 function replace_init_array() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var sub_13900 = libnative.base.add(0x13900);
 Interceptor.replace(sub_13900, new NativeCallback(function() {
 console.log('[*] anti-cheat had been removed');
 }, 'void', []));
 }
 
 function hook_native_1() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var loc_14BEC = libnative.base.add(0x14BEC);
 Interceptor.attach(loc_14BEC, {
 onEnter: function(args) {
 console.log('[*] loc_14BEC (native_1) called');
 }
 });
 }
 
 function hook_native_2() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var loc_15F8C = libnative.base.add(0x15F8C);
 Interceptor.attach(loc_15F8C, {
 onEnter: function(args) {
 console.log('[*] loc_15F8C (native_2) called');
 }, onLeave: function (retval) {
 console.log(retval.readCString())
 }
 });
 }
 
 function hook_sub_189EC() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var sub_189EC = libnative.base.add(0x189EC);
 Interceptor.attach(sub_189EC, {
 onEnter: function(args) {
 console.log('[*] sub_189EC (AES) called');
 console.log(args[0].readByteArray(64));
 console.log(args[1].readCString());
 console.log(args[2]);
 console.log(args[3].readCString());
 console.log(args[4].readCString());
 }
 });
 }
 
 function hook_sub_17FB8() {
 var libnative = TraverseModules('single', {name: 'libnative.so'});
 var sub_17FB8 = libnative.base.add(0x17FB8);
 Interceptor.attach(sub_17FB8, {
 onEnter: function(args) {
 console.log('[*] sub_17FB8 (RC4_INIT) called');
 console.log(args[1].readCString());
 }
 });
 }
 
 function hook_call_constructors() {
 var _symbols = Process.getModuleByName('linker64').enumerateSymbols();
 var call_constructors_addr = null;
 
 for (let index = 0; index < _symbols.length; index++) {
 var _symbol = _symbols[index];
 if (_symbol.name.indexOf('call_constructors') != -1) {
 call_constructors_addr = _symbol.address;
 break;
 }
 }
 
 var detach_listener = Interceptor.attach(call_constructors_addr, {
 onEnter: function(args) {
 console.log('[*] now you can hook init_array');
 replace_init_array();
 hook_native_1();
 hook_native_2();
 hook_sub_189EC();
 hook_sub_17FB8();
 detach_listener.detach();
 }
 });
 }
 
 function HookNativeOnEnter() {
 hook_call_constructors()
 }
 
 
 function main() {
 HookLibWithCallbackOnEnter('libnative.so', HookNativeOnEnter);
 }
 
 main();

// frida -U -f com.jetgame.tetris --no-pause -l terits.js
```



```
__int64 __fastcall round(__int64 w, _BYTE *p, unsigned __int8 *a3, _BYTE *ww)
{
 // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

 v84 = *(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 v7 = p[4]; // 状态矩阵
 v8 = p[8];
 v9 = p[12];
 v10 = *ww ^ *p;
 v11 = p[1];
 v12 = p[5];
 v13 = p[9];
 v14 = p[13];
 v15 = p[2];
 v16 = p[6];
 v17 = p[10];
 v18 = p[14];
 v19 = p[3];
 v20 = p[7];
 v21 = p[11];
 v22 = p[15];
 v68 = v10;
 v23 = 1;
 v24 = 16;
 v25 = ww[4] ^ v7; // 轮密钥加
 v69 = v25;
 v26 = ww[8] ^ v8;
 v70 = v26;
 v27 = ww[12] ^ v9;
 v71 = v27;
 v28 = ww[1] ^ v11;
 v72 = v28;
 v29 = ww[5] ^ v12;
 v73 = v29;
 v30 = ww[9] ^ v13;
 v74 = v30;
 v31 = ww[13] ^ v14;
 v75 = v31;
 v32 = ww[2] ^ v15;
 v76 = v32;
 v33 = ww[6] ^ v16;
 v77 = v33;
 v34 = ww[10] ^ v17;
 v78 = v34;
 v79 = ww[14] ^ v18;
 v80 = ww[3] ^ v19;
 v81 = ww[7] ^ v20;
 v82 = ww[11] ^ v21;
 for ( i = ww[15] ^ v22; ; i ^= v51[15] )
 {
 v35 = byte_75EF53F395[(v25 & 0xF0) + (v25 & 0xF)];// 字节代换
 v36 = byte_75EF53F395[(v26 & 0xF0) + (v26 & 0xF)];
 v37 = byte_75EF53F395[(v27 & 0xF0) + (v27 & 0xF)];
 v38 = byte_75EF53F395[(v28 & 0xF0) + (v28 & 0xF)];
 v39 = byte_75EF53F395[(v29 & 0xF0) + (v29 & 0xF)];
 v40 = byte_75EF53F395[(v30 & 0xF0) + (v30 & 0xF)];
 v41 = byte_75EF53F395[(v31 & 0xF0) + (v31 & 0xF)];
 v42 = byte_75EF53F395[(v32 & 0xF0) + (v32 & 0xF)];
 v43 = byte_75EF53F395[(v33 & 0xF0) + (v33 & 0xF)];
 v44 = *(w + 4) - 1;
 v45 = byte_75EF53F395[(v34 & 0xF0) + (v34 & 0xF)];
 v68 = byte_75EF53F395[(v10 & 0xF0) + (v10 & 0xF)];
 v69 = v35;
 v70 = v36;
 v71 = v37;
 v72 = v38;
 v73 = v39;
 v74 = v40;
 v75 = v41;
 v46 = byte_75EF53F395[(v79 & 0xF0) + (v79 & 0xF)];
 v47 = byte_75EF53F395[(v80 & 0xF0) + (v80 & 0xF)];
 v48 = byte_75EF53F395[(v81 & 0xF0) + (v81 & 0xF)];
 v49 = byte_75EF53F395[(v82 & 0xF0) + (v82 & 0xF)];
 v50 = byte_75EF53F395[(i & 0xF0) + (i & 0xF)];
 v76 = v42;
 v77 = v43;
 v78 = v45;
 v79 = v46;
 v80 = v47;
 v81 = v48;
 v82 = v49;
 i = v50;
 if ( v23 > v44 )
 break;
 mixColumns(v45, &v68); // 列混合
 shiftRows(w, &v68); // 行移位，这两个变了位置
 v51 = &ww[v24];
 v10 = *v51 ^ v68;
 v68 = v10;
 v25 = v51[4] ^ v69;
 v69 = v25;
 v26 = v51[8] ^ v70;
 v70 = v26;
 ++v23;
 v27 = v51[12] ^ v71;
 v71 = v27;
 v24 += 16;
 v28 = v51[1] ^ v72;
 v72 = v28;
 v29 = v51[5] ^ v73;
 v73 = v29;
 v30 = v51[9] ^ v74;
 v74 = v30;
 v31 = v51[13] ^ v75;
 v75 = v31;
 v32 = v51[2] ^ v76;
 v76 = v32;
 v33 = v51[6] ^ v77;
 v77 = v33;
 v34 = v51[10] ^ v78;
 v78 = v34;
 v79 ^= v51[14];
 v80 ^= v51[3];
 v81 ^= v51[7];
 v82 ^= v51[11];
 }
 shiftRows(w, &v68); // 新出的行移位
 v52 = &ww[16 * *(w + 4)]; // 轮密钥加
 v68 ^= *v52;
 v69 ^= v52[4];
 v53 = v69;
 v70 ^= v52[8];
 v54 = v70;
 v71 ^= v52[12];
 v55 = v71;
 v72 ^= v52[1];
 v56 = v72;
 v73 ^= v52[5];
 v57 = v73;
 v74 ^= v52[9];
 v58 = v74;
 v75 ^= v52[13];
 v59 = v75;
 v76 ^= v52[2];
 v60 = v76;
 result = v52[6] ^ v77;
 v77 ^= v52[6];
 v78 ^= v52[10];
 v62 = v78;
 v79 ^= v52[14];
 v63 = v79;
 v80 ^= v52[3];
 v64 = v80;
 v81 ^= v52[7];
 v65 = v81;
 v82 ^= v52[11];
 v66 = v82;
 v67 = i;
 LOBYTE(v52) = v52[15];
 *a3 = v68;
 a3[4] = v53;
 a3[8] = v54;
 a3[12] = v55;
 a3[1] = v56;
 a3[5] = v57;
 a3[9] = v58;
 a3[13] = v59;
 a3[2] = v60;
 a3[6] = result;
 a3[10] = v62;
 a3[14] = v63;
 a3[3] = v64;
 a3[7] = v65;
 a3[11] = v66;
 a3[15] = v52 ^ v67;
 return result;
}
```



```
static const uint8_t sbox[256] = { 144, 122, 80, 239, 240, 156, 47, 125, 160, 52, 35, 202, 79, 33, 102, 107, 61, 224, 194, 179, 252, 105, 8, 255, 127, 22, 72, 213, 235, 89, 216, 12, 243, 228, 168, 234, 185, 129, 1, 40, 19, 184, 108, 203, 220, 138, 39, 25, 210, 164, 211, 153, 73, 87, 135, 223, 45, 74, 193, 88, 180, 104, 222, 199, 148, 123, 170, 226, 140, 83, 173, 30, 4, 197, 24, 0, 237, 241, 121, 67, 81, 176, 132, 90, 238, 151, 136, 38, 182, 115, 157, 91, 254, 229, 84, 244, 177, 6, 63, 188, 49, 96, 161, 133, 201, 248, 198, 231, 174, 195, 130, 159, 251, 206, 253, 50, 141, 46, 65, 191, 55, 183, 236, 119, 2, 128, 59, 118, 146, 20, 208, 76, 56, 137, 28, 70, 43, 11, 196, 114, 14, 205, 98, 16, 111, 9, 143, 124, 212, 215, 109, 247, 155, 172, 32, 18, 100, 221, 204, 250, 112, 249, 53, 29, 154, 82, 245, 13, 175, 186, 166, 48, 41, 139, 126, 192, 131, 149, 97, 68, 163, 34, 117, 94, 167, 85, 42, 145, 242, 66, 162, 86, 181, 95, 219, 54, 71, 190, 134, 165, 64, 21, 93, 142, 189, 200, 26, 209, 60, 7, 17, 51, 187, 110, 158, 150, 58, 218, 57,92, 44, 31, 23, 230, 37, 106, 10, 62, 147, 233, 116, 101, 171, 77, 207, 232, 120, 15, 178, 225, 246, 113, 3, 169, 27, 214, 99, 78, 217, 36, 152, 103, 69, 5, 227, 75 };
static const uint8_t rsbox[256] = { 75, 38, 124, 242, 72, 253, 97, 209, 22, 145, 226, 137, 31, 167, 140, 237, 143, 210, 155, 40, 129, 201, 25, 222, 74, 47, 206, 244, 134, 163, 71, 221, 154, 13, 181, 10, 249, 224, 87, 46, 39, 172, 186, 136, 220, 56, 117, 6, 171, 100, 115, 211, 9, 162, 195, 120, 132, 218, 216, 126, 208, 16, 227, 98, 200, 118, 189, 79, 179, 252, 135, 196, 26, 52, 57, 255, 131, 233, 247, 12, 2, 80, 165, 69, 94, 185, 191, 53, 59, 29, 83, 91, 219, 202, 183, 193, 101, 178, 142, 246, 156, 231, 14, 251, 61, 21, 225, 15, 42, 150, 213, 144, 160, 241, 139, 89, 230, 182, 127, 123, 236, 78, 1, 65, 147, 7, 174, 24, 125, 37, 110, 176, 82, 103, 198, 54, 86, 133, 45, 173, 68, 116, 203, 146, 0, 187, 128, 228, 64, 177, 215, 85, 250, 51, 164, 152, 5, 90, 214, 111, 8, 102, 190, 180, 49, 199, 170, 184, 34, 243, 66, 232, 153, 70, 108, 168, 81, 96, 238, 19, 60, 192, 88, 121, 41, 36, 169, 212, 99, 204, 197, 119, 175, 58, 18, 109, 138, 73, 106, 63, 205, 104, 11, 43, 158, 141, 113, 234, 130, 207, 48, 50, 148, 27, 245, 149, 30, 248, 217, 194, 44, 157, 62, 55, 17, 239, 67, 254, 33, 93, 223, 107, 235, 229, 35, 28, 122, 76, 84, 3, 4, 77, 188, 32, 95, 166, 240, 151, 105, 161, 159, 112, 20, 114, 92, 23 };

static void Cipher(state_t* state, const uint8_t* RoundKey)
{
 uint8_t round = 0;

 // Add the First round key to the state before starting the rounds.
 AddRoundKey(0, state, RoundKey);
 
 for (round = 1; ; ++round)
 {
 SubBytes(state);
 if (round == Nr) {
 break;
 }
 // These two change the order
 MixColumns(state);
 ShiftRows(state);
 
 AddRoundKey(round, state, RoundKey);
 }
 // Add round key to last round
 ShiftRows(state);
 AddRoundKey(Nr, state, RoundKey);
}

static void InvCipher(state_t* state, const uint8_t* RoundKey)
{
 uint8_t round = 0;

 // Add the First round key to the state before starting the rounds.
 AddRoundKey(Nr, state, RoundKey);
 InvShiftRows(state);
 
 for (round = (Nr - 1); ; --round)
 {
 InvSubBytes(state);
 AddRoundKey(round, state, RoundKey);
 if (round == 0) {
 break;
 }
 InvShiftRows(state);
 InvMixColumns(state);
 }
}
```



```
#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define CBC 1

#include "aes.h" 

int main() {
 uint8_t plaintxt[48] = { 166, 98, 46, 98, 247, 122, 195, 92, 107, 245, 116, 68, 109, 138, 246, 178, 164, 132, 68, 240, 247, 142, 161, 208, 221, 9, 198, 98, 39, 8, 116, 233 };
 uint8_t rc4_key[32] = { 0xe5,0xc5,0xc8,0x6f,0xd4,0x04,0x84,0x75,0x0f,0x46,0xcd,0xca,0x65,0x7d,0x9a,0x7c,0x37,0x04,0x3c,0x56,0xec,0x4c,0x9a,0xe2,0xb8,0x31,0xa3,0x81,0x88,0x25,0x8b,0x10 };
 for (int i = 0; i < 32; i++) {
 plaintxt[i] ^= rc4_key[i];
 }
 uint8_t key[32] = "A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!";
 uint8_t iv[16] = "3d354e98963a69b2";

 struct AES_ctx ctx;

 AES_init_ctx_iv(&ctx, key, iv);
 AES_CBC_decrypt_buffer(&ctx, plaintxt, 32);
 
 puts(plaintxt);

 return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/5-1693568806.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/10-1693568807.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/7-1693568808.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/5-1693568808.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/10-1693568809.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693568810.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1693568810.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693568810.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/5-1693568811.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/9-1693568812.png)