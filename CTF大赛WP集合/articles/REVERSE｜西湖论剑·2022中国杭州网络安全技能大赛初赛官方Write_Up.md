# REVERSE｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

> 原文: https://www.ctfiot.com/97742.html
> ID: 97742

2023年2月2日，第六届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国306所高校、485支战队、2733人集结线上初赛！

以下为本届西湖论剑大赛初赛REVERSE题目的Write Up

REVERSE

2022西湖论剑大赛官方WP

（一）

BabyRE

1、程序运行测试

2、IDA分析main函数，会发现只有一句GetLastError();

3、字符串列表能发现字符串“Input:”，通过交叉引用定位到是在sub_401170中被调用的

4、通过对sub_401170的交叉引用能够定位到这样一个数组

其中每个地址都包含一个函数和一个atexit();

5、分别在这6个地址和main函数设置断点，运行程序，发现执行顺序如下：

sub_401170

sub_401230

sub_4012B0

main

sub_401670

sub_4015C0

sub_4014E0

然后逐个函数分析。

sub_401170：

sub_401230：

sub_4012b0：将GetLastError在IAT中的地址替换成了sub_4019D0的地址。

sub_4019d0：

sub_401670：

sub_4015c0：

sub_4014e0：

6、解题思路：先通过base8和sha1爆破出flag的前6位，然后通过rc4爆破出flag的后6位，最后通过base8解密出flag中间的部分。

7、EXP

#include <stdio.h>
#include <windows.h>

typedef unsigned long ULONG;

void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len) //初始化函数
{
 int i = 0, j = 0;
 char k[256] = { 0 };
 unsigned char tmp = 0;
 for (i = 0; i < 256; i++) {
  s[i] = i;
  k[i] = key[i % Len];
 }
 for (i = 0; i < 256; i++) {
  j = (j + s[i] + k[i]) % 256;
  tmp = s[i];
  s[i] = s[j]; //交换s[i]和s[j]
  s[j] = tmp;
 }
}

void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len) //加解密
{
 int i = 0, j = 0, t = 0;
 unsigned long k = 0;
 unsigned char tmp;
 for (k = 0; k < Len; k++) {
  i = (i + 1) % 256;
  j = (j + s[i]) % 256;
  tmp = s[i];
  s[i] = s[j]; //交换s[x]和s[y]
  s[j] = tmp;
  t = (s[i] + s[j]) % 256;
  Data[k] ^= s[t];
 }
}

#define SHA1_ROTL(a,b) (SHA1_tmp=(a),((SHA1_tmp>>(32-b))&(0x7fffffff>>(31-b)))|(SHA1_tmp< 56) ? (128 - length % 64) : (64 - length % 64));
 if (!(pp = (char*)malloc((unsigned long)l))) return;
 for (i = 0; i < length; pp[i + 3 - 2 * (i % 4)] = str[i], i++);
 for (pp[i + 3 - 2 * (i % 4)] = 128, i++; i < l; pp[i + 3 - 2 * (i % 4)] = 0, i++);
 *((long*)(pp + l - 4)) = length << 3;
 *((long*)(pp + l - 8)) = length >> 29;
 for (ppend = pp + l; pp < ppend; pp += 64) {
  for (i = 0; i < 16; W[i] = ((long*)pp)[i], i++);
  for (i = 16; i < 80; W[i] = SHA1_ROTL((W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16]), 1), i++);
  A = H0, B = H1, C = H2, D = H3, E = H4;
  for (i = 0; i < 80; i++) {
   TEMP = SHA1_ROTL(A, 5) + SHA1_F(B, C, D, i) + E + W[i] + K[i];
   E = D, D = C, C = SHA1_ROTL(B, 30), B = A, A = TEMP;
  }
  H0 += A, H1 += B, H2 += C, H3 += D, H4 += E;
 }
 free(pp - l);
 sprintf(sha1, "%08x%08x%08x%08x%08x", H0, H1, H2, H3, H4);
}

unsigned char table[] = { '0', '1', '2', '3', '4', '5', '6', '7', 0 };

int Base8Encode(char* input, char* output)
{
 int index = 0;
 int length = strlen(input);

 for (int i = 0; i < length; i += 3)
 {
  output[index++] = table[input[i] >> 5];
  output[index++] = table[(input[i] >> 2) & 7];
  if (i + 1 == length)
  {
   output[index++] = table[(input[i] & 3) << 1];
   output[index++] = '=';
   output[index++] = '=';
   output[index++] = '=';
   output[index++] = '=';
   output[index++] = '=';
   break;
  }
  output[index++] = table[((input[i] & 3) << 1) + (input[i + 1] >> 7)];
  output[index++] = table[(input[i + 1] >> 4) & 7];
  output[index++] = table[(input[i + 1] >> 1) & 7];
  if (i + 2 == length)
  {
   output[index++] = table[(input[i + 1] & 1) << 2];
   output[index++] = '=';
   output[index++] = '=';
   break;
  }
  output[index++] = table[((input[i + 1] & 1) << 2) + (input[i + 2] >> 6)];
  output[index++] = table[(input[i + 2] >> 3) & 7];
  output[index++] = table[input[i + 2] & 7];
 }
 output[index] = 0;
 return 0;
}

int FindIndex(char* s, char c)
{
 if (c != '=')
 {
  return strchr(s, c) - s;
 }

 return 0;
}

int Base8Decode(char* input, char* output)
{
 int index = 0;
 int length = strlen(input);
 char table[] = { '0','1','2','3','4','5','6','7',0 };
 for (int i = 0; i < length; i += 8)
 {
  output[index++] =
   FindIndex(table, input[i]) << 5 |
   FindIndex(table, input[i + 1]) << 2 |
   FindIndex(table, input[i + 2]) >> 1;
  output[index++] =
   FindIndex(table, input[i + 2]) << 7 |
   FindIndex(table, input[i + 3]) << 4 |
   FindIndex(table, input[i + 4]) << 1 |
   FindIndex(table, input[i + 5]) >> 2;
  output[index++] =
   FindIndex(table, input[i + 5]) << 6 |
   FindIndex(table, input[i + 6]) << 3 |
   FindIndex(table, input[i + 7]);
 }
 return 0;
}

char check1[97] = "162304651523346214431471150310701503207116032063140334661543446114434066142304661563446615430464";
BYTE check2[41] = "67339fc92b4875b8c073c76994ef1ca4ce632d26";
BYTE check3[113] = {
 0x3F,0x95,0xBB,0xF2,0x57,0xF1,0x7A,0x5A,0x22,0x61,0x51,0x43,0xA2,0xFA,0x9B,0x6F,
 0x44,0x63,0xC0,0x08,0x12,0x65,0x5C,0x8A,0x8C,0x4C,0xED,0x5E,0xCA,0x76,0xB9,0x85,
 0xAF,0x05,0x38,0xED,0x42,0x3E,0x42,0xDF,0x5D,0xBE,0x05,0x8B,0x35,0x6D,0xF3,0x1C,
 0xCF,0xF8,0x6A,0x73,0x25,0xE4,0xB7,0xB9,0x36,0xFB,0x02,0x11,0xA0,0xF0,0x57,0xAB,
 0x21,0xC6,0xC7,0x46,0x99,0xBD,0x1E,0x61,0x5E,0xEE,0x55,0x18,0xEE,0x03,0x29,0x84,
 0x7F,0x94,0x5F,0xB4,0x6A,0x29,0xD8,0x6C,0xE4,0xC0,0x9D,0x6B,0xCC,0xD5,0x94,0x5C,
 0xDD,0xCC,0xD5,0x3D,0xC0,0xEF,0x0C,0x29,0xE5,0xB0,0x93,0xF1,0xB3,0xDE,0xB0,0x70 };

char plain[49];
char sha1_text[41];

char cipher1[128];
char cipher2[41];
BYTE cipher3[113];
int main()
{
 unsigned long long* p;
 
 memset(plain, '0', 48);
 
 Base8Decode(check1, plain+6);
 
 p = (unsigned long long*)plain;
 while(1)
 {
  Base8Encode(plain, cipher1);
  sha1(cipher1, 112, cipher2);

  if (memcmp(cipher2, check2, 40) == 0)
  {
   break;
  }
  (*p)++;
  for (int i = 0; i < 5; i++)
  {
   if (plain[i] == '9')
   {
    plain[i] = '0';
    plain[i + 1]++;
   }
  }
  
 }

 //memcpy(plain + 42, "807391", 6);
 p = (unsigned long long*)(plain+42);
 while (1)
 {
  BYTE sbox[256] = { 0 };
  Base8Encode(plain, cipher1);
  memcpy(cipher3, cipher1, 112);
  rc4_init(sbox, (BYTE*)(plain + 42), 6);
  rc4_crypt(sbox, cipher3, 112);

  if (memcmp(cipher3, check3, 112) == 0)
  {
   break;
  }
  (*p)++;
  for (int i = 0; i < 6; i++)
  {
   if (plain[42+i] == 0x40)
   {
    plain[42+i] = '0';
    plain[42+i+1]++;
    break;
   }
  }
 }

 puts(plain);

 return 0;
}

（二）

Berkeley

1、先用IDA分析，发现是ELF64文件，去除了符号，但存在一些特征表示可能是eBPF程序

2、bpf代码已经直接嵌入在文件中了，比较快的办法就是在数据段中找到ELF文件头

3、先将第一个字符转byte然后把后面的数据转换成数组，数组大小在引用它的函数中可以看到

4、使用shift+e提取出这部分数据，保存为bpf_bytecode.elf

5、使用LLVM-objdump -D bpf_bytecode.elf命令查看字节码，发现存在uprobe和uretprobe两个区段

其中uprobe段反汇编结果如下

uretprobe段反汇编结果如下

6、回到IDA继续分析，根据参数对BPF函数进行重命名，发现是监控了用户层的sub_63EA这个函数

当用户层进入sub_63EA时，会触发uprobe，当用户层从sub_63EA退出时，会触发uretprobe，用户层的代码逆出来是假的flag

7、为ghidra安装eBPF插件，打开bpf_bytecode.elf，分析LBB0_1和LBB0_2，可以进行反编译，更加利于分析

flag首先会被uprobe进行处理，然后映射到内存中，然后在uretprobe中进行二次处理，最后检查是否正确。

8、EXP

#include <stdio.h>
#include <windows.h>

unsigned char key[] = {
 0xC1,0xD1,0x02,0x61,0xD6,0xF7,0x13,0xA2,0x9B,0x20,0xD0,0x4A,0x8F,0x7F,0xEE,0xB9,
 0x00,0x63,0x34,0xB0,0x33,0xB7,0x8A,0x8B,0x94,0x60,0x2E,0x8E,0x21,0xFF,0x90,0x82,
 0xD5,0x87,0x96,0x78,0x22,0xB6,0x48,0x6C,0x45,0xC7,0x5A,0x16,0x80,0xFD,0xE4,0x8C,
 0xBF,0x01,0x1F,0x4B,0x79,0x24,0xA0,0xB4,0x23,0x4D,0x3B,0xC5,0x5D,0x6F,0x0D,0xC9,
 0xD4,0xCA,0x55,0xE0,0x39,0xAD,0x2B,0xCD,0x2C,0xEC,0xC2,0x6B,0x30,0xE6,0x0C,0xA8,
 0x9A,0x2F,0xF6,0xE8,0xBB,0x32,0x57,0xFB,0x0B,0x9D,0xF2,0x3F,0xB5,0xF9,0x59,0xE5,
 0x10,0xCF,0x51,0x41,0xE9,0x50,0xDF,0x26,0x74,0x58,0xCB,0x64,0x54,0x73,0xAB,0xF4,
 0xB2,0x9F,0x18,0xF8,0x4E,0xFE,0x08,0x1D,0x4F,0x49,0xD3,0xAC,0x38,0x12,0x77,0x11,
 0x69,0x07,0x1C,0x99,0xB3,0xE7,0x3D,0x05,0xD8,0xFC,0x70,0x46,0x93,0x09,0x65,0x89,
 0xB1,0xC6,0x52,0xFA,0xD2,0x0E,0xA9,0x17,0xE3,0x91,0xA1,0x68,0x5B,0x2A,0xF0,0xC3,
 0x42,0xCC,0x29,0xDE,0xDC,0x85,0x98,0x31,0x5C,0xBC,0x2D,0xEF,0x5E,0x7E,0xAF,0x67,
 0x62,0xA7,0x56,0x88,0xA4,0x43,0x40,0xE1,0x37,0x9E,0x36,0x76,0x71,0x84,0xBD,0x06,
 0x8D,0x47,0x7D,0x53,0xD7,0xC8,0xCE,0x15,0x92,0x95,0x4C,0x28,0x6D,0x75,0xEB,0x7C,
 0xF3,0xBE,0xAA,0xB8,0xED,0x03,0x3C,0x27,0x3E,0x19,0xDD,0xA6,0x66,0x25,0x1E,0xC4,
 0x6E,0xC0,0xE2,0xDB,0x3A,0xD9,0x81,0xA5,0x1B,0xF5,0x04,0xAE,0xBA,0xEA,0x97,0x83,
 0x35,0x44,0xA3,0x7A,0x1A,0xF1,0x86,0xDA,0x7B,0x14,0x72,0x9C,0x6A,0x0F,0x5F,0x0A, 0x00
};

unsigned char cipher[256] = {
  0xF3,0x27,0x47,0x1B,0x8F,0x09,0xFB,0x17,0x70,0x48,0xB0,0x53,0x32,0xDB,0xC0,0xB8
 ,0x63,0x2D,0x40,0x4B,0xF5,0x16,0xF0,0x35,0xE7,0xDF,0xEA,0xA2,0x9C,0x41,0xB3,0x25
 ,0xD7,0x0C,0x33,0x9C,0x7B,0x5A,0xCD,0x13,0xBB,0xEE,0x3E,0x0E,0xF2,0xCF,0x35,0xDA
 ,0xAF,0xA2,0x66,0x7D,0x38,0x37,0x67,0x1E,0x1F,0x6B,0x7B,0x30,0x0B,0x7A,0x02,0xA9
 ,0xC8,0x61,0x27,0x41,0xDB,0x01,0x22,0x31,0x6F,0xB6,0xD4,0x1B,0x04,0xD3,0x94,0xB8
 ,0x46,0xC7,0x24,0xCF,0xBD,0xAF,0x0B,0xDC,0x2E,0xBB,0xB2,0x71,0xF4,0x99,0x57,0x36
 ,0xD1,0x95,0x52,0x92,0xBA,0x6D,0xF3,0x30,0x50,0x59,0x9B,0xEA,0x2F,0x83,0xDC,0xF0
 ,0xDE,0x57,0xA1,0xAC,0xD2,0x51,0xA2,0x1D,0x59,0xA8,0x00,0xB6,0xE2,0x65,0x41,0x0C
 ,0x4F,0xEB,0xF0,0x2E,0x58,0x2A,0x1F,0xF4,0x95,0x72,0x88,0x7C,0xA9,0x0E,0xCB,0x3C
 ,0x42,0xB9,0xF3,0x49,0x9B,0x52,0x98,0x12,0xA3,0x17,0x51,0xC0,0x59,0x40,0x0A,0xBC
 ,0xE8,0x4C,0x04,0xFB,0x13,0x0A,0x17,0x3F,0xE6,0x36,0x97,0xDF,0xB3,0xE2,0x42,0x7F
 ,0xF8,0xCC,0x0E,0xD1,0x77,0xC4,0xA8,0x46,0x48,0xE3,0xF1,0x0A,0xEF,0x94,0x56,0x54
 ,0x5B,0xCA,0xBD,0xDD,0x7F,0x56,0x47,0xC2,0x99,0xFA,0x89,0xCC,0xE1,0xB9,0x3A,0x78
 ,0xE2,0x37,0x58,0x01,0x1B,0xC3,0x4B,0xE6,0x8C,0xF3,0xE5,0xB6,0x71,0x9E,0x63,0xAF
 ,0x11,0xCE,0x87,0xF6,0x6E,0xDE,0xC8,0xB1,0xD0,0x7A,0x15,0x6C,0x10,0x08,0x99,0x7B
 ,0x22,0x55,0x10,0x7A,0x82,0x73,0xFC,0x62,0xCB,0x34,0xA7,0xB7,0x62,0xFA,0x6B,0x9F };

unsigned int arr[8] = { 128,64,32,16,8,4,2,1 };
unsigned int output[256];
unsigned char flag[32];

//71c2ac98ac8d99a2e8a95111449a7393
int main()
{
 for (int i = 0; i < 32; i++)
 {
  for (int j = 32; j < 127; j++)
  {
   for (int k = 0; k < 8; k++)
   {
    unsigned char uc1 = j;
    unsigned char uc2 = ~(j + arr[k]);
    output[i * 8 + k] = key[uc1 ^ uc2];
    output[i * 8 + k] = key[output[i * 8 + k] ^ key[i * 8 + k]];
    if (output[i * 8 + k] != cipher[i * 8 + k])
    {
     goto next;
    }
   }
   flag[i] = j;
   break;
  next:
   j = j;
  }
 }

 puts((char*)flag);

 return 0;
}

（三）

Dual personality

1、查看程序运行效果（如果打不开，尝试使用Win10 x64系统作为运行平台）

2、IDA打开，发现main函数无法正常分析，中间有一段看似花指令的代码

3、从上往下分析，首先是输入flag，然后调用sub_401120

4、将地址0x4011d0中的代码dump下来，使用IDA分析为64位指令，就可以看到正确的代码

第一次切换到64位模式主要是为了修改地址0x407058中的值。

5、从main函数继续往下分析，中间有一个循环，对flag进行第一次加密

6、继续，下面发现一个call far，其实和jmp far是一个意思，切换到64位模式

代码中还参杂了一些花指令和反调试，就不一一枚举了

7、第二次切换到64位模式执行的地址是0x401200，同样dump下来使用IDA分析

8、然后第三次切换到64位模式

同样dump 0x401290的字节码，使用64位IDA分析，这个函数主要修改了0x407000保存的返回值，然后对0x407014开始 的数组中的常量进行处理，得到新的值。

注意：前两次切换到64位模式后，函数结束就重新切换到32位模式了，但是这次出来后仍然为64位模式，因此main函数之后的代码也都是64位的指令。

将这部分的代码进行dump和重分析得到结果如下：

9、EXP

#include <stdio.h>
#include <windows.h>

//6cc1e44811647d38a15017e389b3f704
unsigned char flag[] = "6cc1e44811647d38a15017e389b3f704";
int main()
{
 //复现加密过程
 DWORD delta = 0x5df966ae;

 delta += 0xdeadbeef;  //0x3CA7259D

 //1
 DWORD* pDwordFlag = (DWORD*)flag;
 for (int i = 0; i < 8; i++)
 {
  pDwordFlag[i] += delta;
  delta ^= pDwordFlag[i];
 }

 //2
 unsigned long long* pQwordFlag = (unsigned long long*)flag;
 *(pQwordFlag + 0) = (*(pQwordFlag + 0) << 12) | (*(pQwordFlag + 0) >> (64 - 12));
 *(pQwordFlag + 1) = (*(pQwordFlag + 1) << 34) | (*(pQwordFlag + 1) >> (64 - 34));
 *(pQwordFlag + 2) = (*(pQwordFlag + 2) << 56) | (*(pQwordFlag + 2) >> (64 - 56));
 *(pQwordFlag + 3) = (*(pQwordFlag + 3) << 14) | (*(pQwordFlag + 3) >> (64 - 14));

 //3
 DWORD key[] = { 0x9D, 0x44, 0x37, 0xB5 };
 key[0] &= key[1];
 key[1] |= key[2];
 key[2] ^= key[3];
 key[3] = ~key[3];

 printf("密文：");

 for (int i = 0; i < 32; i++)
 {
  flag[i] ^= key[i % 4];
  printf("0x%02X, ", flag[i]);
 }

 printf("n");

 //解密
 for (int i = 0; i < 32; i++)
 {
  flag[i] ^= key[i % 4];
 }

 pQwordFlag = (unsigned long long*)flag;
 *(pQwordFlag + 0) = (*(pQwordFlag + 0) >> 12) | (*(pQwordFlag + 0) << (64 - 12));
 *(pQwordFlag + 1) = (*(pQwordFlag + 1) >> 34) | (*(pQwordFlag + 1) << (64 - 34));
 *(pQwordFlag + 2) = (*(pQwordFlag + 2) >> 56) | (*(pQwordFlag + 2) << (64 - 56));
 *(pQwordFlag + 3) = (*(pQwordFlag + 3) >> 14) | (*(pQwordFlag + 3) << (64 - 14));

 delta = 0x5df966ae;

 delta += 0xdeadbeef;  //0x3CA7259D

 for (int i = 0; i < 8; i++)
 {
  DWORD tmp = pDwordFlag[i] ^ delta;
  pDwordFlag[i] -= delta;
  delta = tmp;
 }

 printf("flag:
DASCTF{%s}", flag);

 return 0;
}

（四）

EasyVT

1、一共两个附件，先分析Guest.exe

发现没有什么特别的地方，但是有很多VM相关的特权指令，在开启VT后，这些特权指令会触发VM-Exit Handler

2、分析EasyVT.sys

实现了一个最基础的VT，在执行VmLaunch之前会设置VMCS字段，在里面可以找到VM-Exit Handler的地址

跟进sub_4401c10

代码如下，有一系列switch case结构，用于处理不同的退出码，每个退出码对应的指令可以参Intel开发手册考卷3附录C。

然后对照Guest.exe中特权指令的执行顺序分析就可以了，实际上大多数Exit Handler都是在为tea算法和rc4算法设置各项值，通过对一个参数多次赋值以达到混淆的目的。

3、EXP

#include <stdio.h>
#include <windows.h>

void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len) //初始化函数
{
    int i = 0, j = 0;
    char k[256] = { 0 };
    unsigned char tmp = 0;
    for (i = 0; i < 256; i++) {
        s[i] = i;
        k[i] = key[i % Len];
    }
    for (i = 0; i < 256; i++) {
        j = (j + s[i] + k[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; //交换s[i]和s[j]
        s[j] = tmp;
    }
}

void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len) //加解密
{
    int i = 0, j = 0, t = 0;
    unsigned long k = 0;
    unsigned char tmp;
    for (k = 0; k < Len; k++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; //交换s[x]和s[y]
        s[j] = tmp;
        t = (s[i] + s[j]) % 256;
        Data[k] ^= s[t];
    }
}

//加密函数  
void TeaEncrypt(DWORD* v, DWORD* k) {
    DWORD v0 = v[1], v1 = v[0], sum = 0x20000000, i;           /* set up */
    DWORD delta = 0xc95d6abf;                     /* a key schedule constant */
    DWORD k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
    for (i = 0; i < 32; i++) {                       /* basic cycle start */
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
        v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
        sum -= delta;
    }                                              /* end cycle */
    v[1] = v0; v[0] = v1;
}
//解密函数  
void TeaDecrypt(DWORD* v, DWORD* k) {
    DWORD v0 = v[0], v1 = v[1], sum = 0x20000000, i;           /* set up */
    DWORD delta = 0xc95d6abf;                     /* a key schedule constant */
    DWORD k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */

    for (i = 0; i < 32; i++)
    {
        sum -= delta;
    }

    for (i = 0; i < 32; i++) {                         /* basic cycle start */
        sum += delta;
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
    }                                              /* end cycle */
    v[0] = v0; v[1] = v1;
}

int main()
{
    /*
    BYTE flag[100] = "81920c3758be43705ba154bb8f599846x00";

    int idx = 0;

    for (int i = 0; i < 4; i++)
    {
        BYTE rc4_sbox[256] = { 0 };
        BYTE rc4_text[8];
        rc4_text[0] = flag[i * 8 + 4];
        rc4_text[1] = flag[i * 8 + 5];
        rc4_text[2] = flag[i * 8 + 6];
        rc4_text[3] = flag[i * 8 + 7];
        rc4_text[4] = flag[i * 8 + 0];
        rc4_text[5] = flag[i * 8 + 1];
        rc4_text[6] = flag[i * 8 + 2];
        rc4_text[7] = flag[i * 8 + 3];

        BYTE rc4_key[17] = "04e52c7e31022b0b";
        rc4_init(rc4_sbox, rc4_key, 16);
        rc4_crypt(rc4_sbox, rc4_text, 8);

        DWORD *tea_text = (DWORD*)rc4_text;
        DWORD tea_key[4] = { 0x40506070, 0xc0d0e0f0, 0x8090a0b0, 0x00102030 };
        TeaEncrypt(tea_text, tea_key);
        printf("0x%x, 0x%x, ", tea_text[1], tea_text[0]);
    }

    */

    DWORD tea_cipher[] = { 0x5c073994, 0xd805cb3, 0x87dda586, 0x317fb8e, 0x6520ef29, 0x5a4987af, 0xeb2dc2a4, 0x38cf470e };
    DWORD tea_key[4] = { 0x40506070, 0xc0d0e0f0, 0x8090a0b0, 0x00102030 };
    BYTE rc4_key[17] = "04e52c7e31022b0b";
    BYTE plaintext[32];
    for (int i = 0; i < 4; i++)
    {
        TeaDecrypt(&tea_cipher[i * 2], tea_key);
        BYTE rc4_sbox[256] = { 0 };
        BYTE rc4_text[9] = { 0 };
        ((DWORD*)rc4_text)[0] = tea_cipher[i * 2 + 1];
        ((DWORD*)rc4_text)[1] = tea_cipher[i * 2];
        rc4_init(rc4_sbox, rc4_key, 16);
        rc4_crypt(rc4_sbox, rc4_text, 8);
        memcpy(plaintext + i * 8, rc4_text, 8);
    }

    for (int i = 0; i < 32; i += 8)
    {
        for (int j = 0; j < 4; j++)
        {
            printf("%c", plaintext[i + 4 + j]);
        }

        for (int j = 0; j < 4; j++)
        {
            printf("%c", plaintext[i + j]);
        }

    }

    return 0;
}

— 往期回顾 —

MISC｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

WEB｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up


```
    #include <stdio.h>
    #include <windows.h>

typedef unsigned long ULONG;

void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len) //初始化函数
{
 int i = 0, j = 0;
 char k[256] = { 0 };
 unsigned char tmp = 0;
 for (i = 0; i < 256; i++) {
  s[i] = i;
  k[i] = key[i % Len];
 }
 for (i = 0; i < 256; i++) {
  j = (j + s[i] + k[i]) % 256;
  tmp = s[i];
  s[i] = s[j]; //交换s[i]和s[j]
  s[j] = tmp;
 }
}

void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len) //加解密
{
 int i = 0, j = 0, t = 0;
 unsigned long k = 0;
 unsigned char tmp;
 for (k = 0; k < Len; k++) {
  i = (i + 1) % 256;
  j = (j + s[i]) % 256;
  tmp = s[i];
  s[i] = s[j]; //交换s[x]和s[y]
  s[j] = tmp;
  t = (s[i] + s[j]) % 256;
  Data[k] ^= s[t];
 }
}

    #define SHA1_ROTL(a,b) (SHA1_tmp=(a),((SHA1_tmp>>(32-b))&(0x7fffffff>>(31-b)))|(SHA1_tmp< 56) ? (128 - length % 64) : (64 - length % 64));
 if (!(pp = (char*)malloc((unsigned long)l))) return;
 for (i = 0; i < length; pp[i + 3 - 2 * (i % 4)] = str[i], i++);
 for (pp[i + 3 - 2 * (i % 4)] = 128, i++; i < l; pp[i + 3 - 2 * (i % 4)] = 0, i++);
 *((long*)(pp + l - 4)) = length << 3;
 *((long*)(pp + l - 8)) = length >> 29;
 for (ppend = pp + l; pp < ppend; pp += 64) {
  for (i = 0; i < 16; W[i] = ((long*)pp)[i], i++);
  for (i = 16; i < 80; W[i] = SHA1_ROTL((W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16]), 1), i++);
  A = H0, B = H1, C = H2, D = H3, E = H4;
  for (i = 0; i < 80; i++) {
   TEMP = SHA1_ROTL(A, 5) + SHA1_F(B, C, D, i) + E + W[i] + K[i];
   E = D, D = C, C = SHA1_ROTL(B, 30), B = A, A = TEMP;
  }
  H0 += A, H1 += B, H2 += C, H3 += D, H4 += E;
 }
 free(pp - l);
 sprintf(sha1, "%08x%08x%08x%08x%08x", H0, H1, H2, H3, H4);
}

unsigned char table[] = { '0', '1', '2', '3', '4', '5', '6', '7', 0 };

int Base8Encode(char* input, char* output)
{
 int index = 0;
 int length = strlen(input);

 for (int i = 0; i < length; i += 3)
 {
  output[index++] = table[input[i] >> 5];
  output[index++] = table[(input[i] >> 2) & 7];
  if (i + 1 == length)
  {
   output[index++] = table[(input[i] & 3) << 1];
   output[index++] = '=';
   output[index++] = '=';
   output[index++] = '=';
   output[index++] = '=';
   output[index++] = '=';
   break;
  }
  output[index++] = table[((input[i] & 3) << 1) + (input[i + 1] >> 7)];
  output[index++] = table[(input[i + 1] >> 4) & 7];
  output[index++] = table[(input[i + 1] >> 1) & 7];
  if (i + 2 == length)
  {
   output[index++] = table[(input[i + 1] & 1) << 2];
   output[index++] = '=';
   output[index++] = '=';
   break;
  }
  output[index++] = table[((input[i + 1] & 1) << 2) + (input[i + 2] >> 6)];
  output[index++] = table[(input[i + 2] >> 3) & 7];
  output[index++] = table[input[i + 2] & 7];
 }
 output[index] = 0;
 return 0;
}

int FindIndex(char* s, char c)
{
 if (c != '=')
 {
  return strchr(s, c) - s;
 }

 return 0;
}

int Base8Decode(char* input, char* output)
{
 int index = 0;
 int length = strlen(input);
 char table[] = { '0','1','2','3','4','5','6','7',0 };
 for (int i = 0; i < length; i += 8)
 {
  output[index++] =
   FindIndex(table, input[i]) << 5 |
   FindIndex(table, input[i + 1]) << 2 |
   FindIndex(table, input[i + 2]) >> 1;
  output[index++] =
   FindIndex(table, input[i + 2]) << 7 |
   FindIndex(table, input[i + 3]) << 4 |
   FindIndex(table, input[i + 4]) << 1 |
   FindIndex(table, input[i + 5]) >> 2;
  output[index++] =
   FindIndex(table, input[i + 5]) << 6 |
   FindIndex(table, input[i + 6]) << 3 |
   FindIndex(table, input[i + 7]);
 }
 return 0;
}

char check1[97] = "162304651523346214431471150310701503207116032063140334661543446114434066142304661563446615430464";
BYTE check2[41] = "67339fc92b4875b8c073c76994ef1ca4ce632d26";
BYTE check3[113] = {
 0x3F,0x95,0xBB,0xF2,0x57,0xF1,0x7A,0x5A,0x22,0x61,0x51,0x43,0xA2,0xFA,0x9B,0x6F,
 0x44,0x63,0xC0,0x08,0x12,0x65,0x5C,0x8A,0x8C,0x4C,0xED,0x5E,0xCA,0x76,0xB9,0x85,
 0xAF,0x05,0x38,0xED,0x42,0x3E,0x42,0xDF,0x5D,0xBE,0x05,0x8B,0x35,0x6D,0xF3,0x1C,
 0xCF,0xF8,0x6A,0x73,0x25,0xE4,0xB7,0xB9,0x36,0xFB,0x02,0x11,0xA0,0xF0,0x57,0xAB,
 0x21,0xC6,0xC7,0x46,0x99,0xBD,0x1E,0x61,0x5E,0xEE,0x55,0x18,0xEE,0x03,0x29,0x84,
 0x7F,0x94,0x5F,0xB4,0x6A,0x29,0xD8,0x6C,0xE4,0xC0,0x9D,0x6B,0xCC,0xD5,0x94,0x5C,
 0xDD,0xCC,0xD5,0x3D,0xC0,0xEF,0x0C,0x29,0xE5,0xB0,0x93,0xF1,0xB3,0xDE,0xB0,0x70 };

char plain[49];
char sha1_text[41];

char cipher1[128];
char cipher2[41];
BYTE cipher3[113];
int main()
{
 unsigned long long* p;
 
 memset(plain, '0', 48);
 
 Base8Decode(check1, plain+6);
 
 p = (unsigned long long*)plain;
 while(1)
 {
  Base8Encode(plain, cipher1);
  sha1(cipher1, 112, cipher2);

  if (memcmp(cipher2, check2, 40) == 0)
  {
   break;
  }
  (*p)++;
  for (int i = 0; i < 5; i++)
  {
   if (plain[i] == '9')
   {
    plain[i] = '0';
    plain[i + 1]++;
   }
  }
  
 }

 //memcpy(plain + 42, "807391", 6);
 p = (unsigned long long*)(plain+42);
 while (1)
 {
  BYTE sbox[256] = { 0 };
  Base8Encode(plain, cipher1);
  memcpy(cipher3, cipher1, 112);
  rc4_init(sbox, (BYTE*)(plain + 42), 6);
  rc4_crypt(sbox, cipher3, 112);

  if (memcmp(cipher3, check3, 112) == 0)
  {
   break;
  }
  (*p)++;
  for (int i = 0; i < 6; i++)
  {
   if (plain[42+i] == 0x40)
   {
    plain[42+i] = '0';
    plain[42+i+1]++;
    break;
   }
  }
 }

 puts(plain);

 return 0;
}
    #include <stdio.h>
    #include <windows.h>

unsigned char key[] = {
 0xC1,0xD1,0x02,0x61,0xD6,0xF7,0x13,0xA2,0x9B,0x20,0xD0,0x4A,0x8F,0x7F,0xEE,0xB9,
 0x00,0x63,0x34,0xB0,0x33,0xB7,0x8A,0x8B,0x94,0x60,0x2E,0x8E,0x21,0xFF,0x90,0x82,
 0xD5,0x87,0x96,0x78,0x22,0xB6,0x48,0x6C,0x45,0xC7,0x5A,0x16,0x80,0xFD,0xE4,0x8C,
 0xBF,0x01,0x1F,0x4B,0x79,0x24,0xA0,0xB4,0x23,0x4D,0x3B,0xC5,0x5D,0x6F,0x0D,0xC9,
 0xD4,0xCA,0x55,0xE0,0x39,0xAD,0x2B,0xCD,0x2C,0xEC,0xC2,0x6B,0x30,0xE6,0x0C,0xA8,
 0x9A,0x2F,0xF6,0xE8,0xBB,0x32,0x57,0xFB,0x0B,0x9D,0xF2,0x3F,0xB5,0xF9,0x59,0xE5,
 0x10,0xCF,0x51,0x41,0xE9,0x50,0xDF,0x26,0x74,0x58,0xCB,0x64,0x54,0x73,0xAB,0xF4,
 0xB2,0x9F,0x18,0xF8,0x4E,0xFE,0x08,0x1D,0x4F,0x49,0xD3,0xAC,0x38,0x12,0x77,0x11,
 0x69,0x07,0x1C,0x99,0xB3,0xE7,0x3D,0x05,0xD8,0xFC,0x70,0x46,0x93,0x09,0x65,0x89,
 0xB1,0xC6,0x52,0xFA,0xD2,0x0E,0xA9,0x17,0xE3,0x91,0xA1,0x68,0x5B,0x2A,0xF0,0xC3,
 0x42,0xCC,0x29,0xDE,0xDC,0x85,0x98,0x31,0x5C,0xBC,0x2D,0xEF,0x5E,0x7E,0xAF,0x67,
 0x62,0xA7,0x56,0x88,0xA4,0x43,0x40,0xE1,0x37,0x9E,0x36,0x76,0x71,0x84,0xBD,0x06,
 0x8D,0x47,0x7D,0x53,0xD7,0xC8,0xCE,0x15,0x92,0x95,0x4C,0x28,0x6D,0x75,0xEB,0x7C,
 0xF3,0xBE,0xAA,0xB8,0xED,0x03,0x3C,0x27,0x3E,0x19,0xDD,0xA6,0x66,0x25,0x1E,0xC4,
 0x6E,0xC0,0xE2,0xDB,0x3A,0xD9,0x81,0xA5,0x1B,0xF5,0x04,0xAE,0xBA,0xEA,0x97,0x83,
 0x35,0x44,0xA3,0x7A,0x1A,0xF1,0x86,0xDA,0x7B,0x14,0x72,0x9C,0x6A,0x0F,0x5F,0x0A, 0x00
};

unsigned char cipher[256] = {
  0xF3,0x27,0x47,0x1B,0x8F,0x09,0xFB,0x17,0x70,0x48,0xB0,0x53,0x32,0xDB,0xC0,0xB8
 ,0x63,0x2D,0x40,0x4B,0xF5,0x16,0xF0,0x35,0xE7,0xDF,0xEA,0xA2,0x9C,0x41,0xB3,0x25
 ,0xD7,0x0C,0x33,0x9C,0x7B,0x5A,0xCD,0x13,0xBB,0xEE,0x3E,0x0E,0xF2,0xCF,0x35,0xDA
 ,0xAF,0xA2,0x66,0x7D,0x38,0x37,0x67,0x1E,0x1F,0x6B,0x7B,0x30,0x0B,0x7A,0x02,0xA9
 ,0xC8,0x61,0x27,0x41,0xDB,0x01,0x22,0x31,0x6F,0xB6,0xD4,0x1B,0x04,0xD3,0x94,0xB8
 ,0x46,0xC7,0x24,0xCF,0xBD,0xAF,0x0B,0xDC,0x2E,0xBB,0xB2,0x71,0xF4,0x99,0x57,0x36
 ,0xD1,0x95,0x52,0x92,0xBA,0x6D,0xF3,0x30,0x50,0x59,0x9B,0xEA,0x2F,0x83,0xDC,0xF0
 ,0xDE,0x57,0xA1,0xAC,0xD2,0x51,0xA2,0x1D,0x59,0xA8,0x00,0xB6,0xE2,0x65,0x41,0x0C
 ,0x4F,0xEB,0xF0,0x2E,0x58,0x2A,0x1F,0xF4,0x95,0x72,0x88,0x7C,0xA9,0x0E,0xCB,0x3C
 ,0x42,0xB9,0xF3,0x49,0x9B,0x52,0x98,0x12,0xA3,0x17,0x51,0xC0,0x59,0x40,0x0A,0xBC
 ,0xE8,0x4C,0x04,0xFB,0x13,0x0A,0x17,0x3F,0xE6,0x36,0x97,0xDF,0xB3,0xE2,0x42,0x7F
 ,0xF8,0xCC,0x0E,0xD1,0x77,0xC4,0xA8,0x46,0x48,0xE3,0xF1,0x0A,0xEF,0x94,0x56,0x54
 ,0x5B,0xCA,0xBD,0xDD,0x7F,0x56,0x47,0xC2,0x99,0xFA,0x89,0xCC,0xE1,0xB9,0x3A,0x78
 ,0xE2,0x37,0x58,0x01,0x1B,0xC3,0x4B,0xE6,0x8C,0xF3,0xE5,0xB6,0x71,0x9E,0x63,0xAF
 ,0x11,0xCE,0x87,0xF6,0x6E,0xDE,0xC8,0xB1,0xD0,0x7A,0x15,0x6C,0x10,0x08,0x99,0x7B
 ,0x22,0x55,0x10,0x7A,0x82,0x73,0xFC,0x62,0xCB,0x34,0xA7,0xB7,0x62,0xFA,0x6B,0x9F };

unsigned int arr[8] = { 128,64,32,16,8,4,2,1 };
unsigned int output[256];
unsigned char flag[32];

//71c2ac98ac8d99a2e8a95111449a7393
int main()
{
 for (int i = 0; i < 32; i++)
 {
  for (int j = 32; j < 127; j++)
  {
   for (int k = 0; k < 8; k++)
   {
    unsigned char uc1 = j;
    unsigned char uc2 = ~(j + arr[k]);
    output[i * 8 + k] = key[uc1 ^ uc2];
    output[i * 8 + k] = key[output[i * 8 + k] ^ key[i * 8 + k]];
    if (output[i * 8 + k] != cipher[i * 8 + k])
    {
     goto next;
    }
   }
   flag[i] = j;
   break;
  next:
   j = j;
  }
 }

 puts((char*)flag);

 return 0;
}
    #include <stdio.h>
    #include <windows.h>

//6cc1e44811647d38a15017e389b3f704
unsigned char flag[] = "6cc1e44811647d38a15017e389b3f704";
int main()
{
 //复现加密过程
 DWORD delta = 0x5df966ae;

 delta += 0xdeadbeef;  //0x3CA7259D

 //1
 DWORD* pDwordFlag = (DWORD*)flag;
 for (int i = 0; i < 8; i++)
 {
  pDwordFlag[i] += delta;
  delta ^= pDwordFlag[i];
 }

 //2
 unsigned long long* pQwordFlag = (unsigned long long*)flag;
 *(pQwordFlag + 0) = (*(pQwordFlag + 0) << 12) | (*(pQwordFlag + 0) >> (64 - 12));
 *(pQwordFlag + 1) = (*(pQwordFlag + 1) << 34) | (*(pQwordFlag + 1) >> (64 - 34));
 *(pQwordFlag + 2) = (*(pQwordFlag + 2) << 56) | (*(pQwordFlag + 2) >> (64 - 56));
 *(pQwordFlag + 3) = (*(pQwordFlag + 3) << 14) | (*(pQwordFlag + 3) >> (64 - 14));

 //3
 DWORD key[] = { 0x9D, 0x44, 0x37, 0xB5 };
 key[0] &= key[1];
 key[1] |= key[2];
 key[2] ^= key[3];
 key[3] = ~key[3];

 printf("密文：");

 for (int i = 0; i < 32; i++)
 {
  flag[i] ^= key[i % 4];
  printf("0x%02X, ", flag[i]);
 }

 printf("n");

 //解密
 for (int i = 0; i < 32; i++)
 {
  flag[i] ^= key[i % 4];
 }

 pQwordFlag = (unsigned long long*)flag;
 *(pQwordFlag + 0) = (*(pQwordFlag + 0) >> 12) | (*(pQwordFlag + 0) << (64 - 12));
 *(pQwordFlag + 1) = (*(pQwordFlag + 1) >> 34) | (*(pQwordFlag + 1) << (64 - 34));
 *(pQwordFlag + 2) = (*(pQwordFlag + 2) >> 56) | (*(pQwordFlag + 2) << (64 - 56));
 *(pQwordFlag + 3) = (*(pQwordFlag + 3) >> 14) | (*(pQwordFlag + 3) << (64 - 14));

 delta = 0x5df966ae;

 delta += 0xdeadbeef;  //0x3CA7259D

 for (int i = 0; i < 8; i++)
 {
  DWORD tmp = pDwordFlag[i] ^ delta;
  pDwordFlag[i] -= delta;
  delta = tmp;
 }

 printf("flag:
DASCTF{%s}", flag);

 return 0;
}
    #include <stdio.h>
    #include <windows.h>

void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len) //初始化函数
{
    int i = 0, j = 0;
    char k[256] = { 0 };
    unsigned char tmp = 0;
    for (i = 0; i < 256; i++) {
        s[i] = i;
        k[i] = key[i % Len];
    }
    for (i = 0; i < 256; i++) {
        j = (j + s[i] + k[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; //交换s[i]和s[j]
        s[j] = tmp;
    }
}

void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len) //加解密
{
    int i = 0, j = 0, t = 0;
    unsigned long k = 0;
    unsigned char tmp;
    for (k = 0; k < Len; k++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; //交换s[x]和s[y]
        s[j] = tmp;
        t = (s[i] + s[j]) % 256;
        Data[k] ^= s[t];
    }
}

//加密函数  
void TeaEncrypt(DWORD* v, DWORD* k) {
    DWORD v0 = v[1], v1 = v[0], sum = 0x20000000, i;           /* set up */
    DWORD delta = 0xc95d6abf;                     /* a key schedule constant */
    DWORD k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
    for (i = 0; i < 32; i++) {                       /* basic cycle start */
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
        v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
        sum -= delta;
    }                                              /* end cycle */
    v[1] = v0; v[0] = v1;
}
//解密函数  
void TeaDecrypt(DWORD* v, DWORD* k) {
    DWORD v0 = v[0], v1 = v[1], sum = 0x20000000, i;           /* set up */
    DWORD delta = 0xc95d6abf;                     /* a key schedule constant */
    DWORD k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */

    for (i = 0; i < 32; i++)
    {
        sum -= delta;
    }

    for (i = 0; i < 32; i++) {                         /* basic cycle start */
        sum += delta;
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
    }                                              /* end cycle */
    v[0] = v0; v[1] = v1;
}

int main()
{
    /*
    BYTE flag[100] = "81920c3758be43705ba154bb8f599846x00";

    int idx = 0;

    for (int i = 0; i < 4; i++)
    {
        BYTE rc4_sbox[256] = { 0 };
        BYTE rc4_text[8];
        rc4_text[0] = flag[i * 8 + 4];
        rc4_text[1] = flag[i * 8 + 5];
        rc4_text[2] = flag[i * 8 + 6];
        rc4_text[3] = flag[i * 8 + 7];
        rc4_text[4] = flag[i * 8 + 0];
        rc4_text[5] = flag[i * 8 + 1];
        rc4_text[6] = flag[i * 8 + 2];
        rc4_text[7] = flag[i * 8 + 3];

        BYTE rc4_key[17] = "04e52c7e31022b0b";
        rc4_init(rc4_sbox, rc4_key, 16);
        rc4_crypt(rc4_sbox, rc4_text, 8);

        DWORD *tea_text = (DWORD*)rc4_text;
        DWORD tea_key[4] = { 0x40506070, 0xc0d0e0f0, 0x8090a0b0, 0x00102030 };
        TeaEncrypt(tea_text, tea_key);
        printf("0x%x, 0x%x, ", tea_text[1], tea_text[0]);
    }

    */

    DWORD tea_cipher[] = { 0x5c073994, 0xd805cb3, 0x87dda586, 0x317fb8e, 0x6520ef29, 0x5a4987af, 0xeb2dc2a4, 0x38cf470e };
    DWORD tea_key[4] = { 0x40506070, 0xc0d0e0f0, 0x8090a0b0, 0x00102030 };
    BYTE rc4_key[17] = "04e52c7e31022b0b";
    BYTE plaintext[32];
    for (int i = 0; i < 4; i++)
    {
        TeaDecrypt(&tea_cipher[i * 2], tea_key);
        BYTE rc4_sbox[256] = { 0 };
        BYTE rc4_text[9] = { 0 };
        ((DWORD*)rc4_text)[0] = tea_cipher[i * 2 + 1];
        ((DWORD*)rc4_text)[1] = tea_cipher[i * 2];
        rc4_init(rc4_sbox, rc4_key, 16);
        rc4_crypt(rc4_sbox, rc4_text, 8);
        memcpy(plaintext + i * 8, rc4_text, 8);
    }

    for (int i = 0; i < 32; i += 8)
    {
        for (int j = 0; j < 4; j++)
        {
            printf("%c", plaintext[i + 4 + j]);
        }

        for (int j = 0; j < 4; j++)
        {
            printf("%c", plaintext[i + j]);
        }

    }

    return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/10-1676352520.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1676352521.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676352521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676352521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1676352521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676352522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1676352522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1676352522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1676352522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1676352522.png)