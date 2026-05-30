# m0leCon CTF 2025 Teaser re Embedded encryption RISCV 对称密码

> 原文: https://www.ctfiot.com/206641.html
> ID: 206641

RISCV 32位，看起来是固件的代码。

一

架构、硬件相关API

大部分架构、硬件相关函数看名字猜功能。

metal_gpio_get_input_pin函数百度一下，是从针脚读数据：

__inline__ int metal_gpio_get_input_pin(struct metal_gpio *gpio, int pin)
// Get the value of the GPIO pin.

ida中F5的结果（美化了一下，应该是虚函数调用）如下，其返回值类型不是int而是bool：

bool __fastcall metal_gpio_get_input_pin(int device, char pin)
{
 return device && (device->func(device) & (1 << pin)) != 0;
}

调用了随机数相关的api：srand和rand，实现和我电脑上的编译器调的库不一样，这两个API的实现也在ELF中给出来了，后续直接复制ida f5的结果出来用就行。

二

初始化

有一个数组长度是1604，ida里设成1608显示的效果好一点。

数组初始化内容如下：

data[0:32) (32字节) = 0, 1, 2, 3, ... , 31
data[32:65) (32+1字节) = "ptm{REDACTEDREDACTEDREDACTEDRED}x00"
data[68:324) (256字节) = 0, 1, 2, 3, ... , 255

三

过程分析

这里以最开始的一段打乱IP置换表的代码为例，ida里f5出来是这个样子的：

v12 = &var644[(unsigned __int8)v10 + 1604];
v13 = &var644[(unsigned __int8)v11 + 1604];
v14 = *(v12 - 1604) + *(v13 - 1604);
*(v12 - 1604) = v14;
v15 = *(v13 - 1604);
*(v13 - 1604) = v14 - v15;
*(v12 - 1604) = v15 + *(v12 - 1604) - v14;

实际上v12=var644 + v10 + 1604，这是以栈顶指针的去索引数组，可能是编译器的锅，搞出来的代码有点混乱，后续的*(v12 - 1604)等价于var644[v10]：

v14 = var644[v10] + var644[v11];
var644[v10] = v14;
v15 = var644[v11];
var644[v11] = v14 - v15;
var644[v10] = v15 + var644[v10] - v14;

这段代码简单分析一下会发现，最后是把var644[v10]和var644[v11]进行了一下交换。

按上述方法分析整个main函数，发现unsigned char var644[1604]逻辑上可以分成四个数组：

_BYTE m32[32]; // &var644[0:32]
_BYTE input[33]; // &var644[32:64]
_BYTE m256[256]; // &var644[68:324]
_DWORD output[256]; // &var644[580:1604]

其中m32是IP置换表、m256是P盒映射表，input、output是缓冲区。

简单说一下，IP置换就是交换数组中元素的位置，P盒运算就是一个一对一的映射。

四

加密过程

main流程总结：

◆流程1：重复1337次

◆流程2：j: 0 -> 31

◆将output视作16×16的矩阵

◆输出

将output每行加起来，然后输出

◆输出

将output每列加起来，然后输出

流程1是个比较常规的对称密码加密过程，不再详细叙述。

加密所用的表、数据取自随机函数生成器，相当于密钥是个随机数种子。

seed取自metal_gpio_get_input_pin，是个1位的值。

流程2，实际是把input最后一轮的结果，映射到output上。

整个过程等价于output[input[j]] = 1 << (31-j)。

然后将output当成二维方阵，输出行列和。

五

流程2 解密

首先从行列和还原output。

易得知，output矩阵中不同两个元素不会在相同的位同时为1，即若a!=b则output[a]&output[b]==0为真。

因此，若行和为0x101，行和第0位和第8位为1，表示该行中一个元素第0位为1，一个元素第8位为1，这两个元素可以相同。即该行存在0x100、0x1或0x101，其余为0。

同理列和也可以如此分解。

记录下第0位为1的元素所在的行和列，即可知道output矩阵中该位置第0位为1。

def get_bit_idx(x):
 i = 0
 res = []
 while x:
 if x & 1:
 res.append(i)
 i += 1
 x >>= 1
 return res

rows = [0]*32
cols = [0]*32
for r in range(16):
 res = get_bit_idx(row_sums[r])
 for a in res:
 rows[a] = r
for c in range(16):
 res = get_bit_idx(col_sums[c])
 for a in res:
 cols[a] = c
 
output = [0]*256
for i in range(32):
 output[rows[i]*16 + cols[i]] |= 1 << i

然后由output还原最后一轮的input。

加密过程分析得到的output[input[j]] = 1 << (31-j)

因此若(output[i] & (1 << j)) != 0，则input[31-j] = i

inputs = [0]*32
for i in range(256):
 res = get_bit_idx(output[i])
 for j in res:
 j = 31 - j
 inputs[j] = i
print(inputs)

六

流程1 对称密码 解密

首先seed只能是0或1，跑两次即可。

接着是对称密码解密，IP置换、P盒运算、异或运算都是可逆的。

其中IP置换的置换表、P盒运算的映射表、异或运算的值都是由rand随机获取的。

所以需要先缓存1337轮的置换表、映射表、异或数据，然后执行这三种操作的逆运算即可。

_BYTE m32s[1337 + 1][32]; // &var644[0]
_BYTE m256s[1337 + 1][256]; // &var644[68]
_BYTE xors[1337][32];
void decrypt(unsigned int seed, _BYTE* last_input) {
 _BYTE input[33] = { 0, };
 _DWORD output[256] = { 0, }; // &var644[580]

 memcpy(input, last_input, 32);

 int i, j;

 _BYTE rm256[256];

 // cache rand result
 srand(seed);
 for (i = 0; i != 32; ++i)
 m32s[0][i] = i;
 for (i = 0; i != 256; ++i)
 m256s[0][i] = i;
 for (j = 0; j < ROUNDS; j++) {
 for (i = 0; i < 1000; i++) {
 _BYTE a = (int)rand() % 32;
 _BYTE b = (int)rand() % 32;
 if (a != b)
 {
 _BYTE temp;
 temp = m32s[j][a];
 m32s[j][a] = m32s[j][b];
 m32s[j][b] = temp;
 }
 };
 for (i = 0; i < 10000; i++) {
 _BYTE a = rand();
 _BYTE b = rand();
 if (a != b)
 {
 _BYTE temp;
 temp = m256s[j][a];
 m256s[j][a] = m256s[j][b];
 m256s[j][b] = temp;
 }
 };
 for (i = 0; i != 32; ++i)
 xors[j][i] = rand();
 // copy to next round
 for (i = 0; i != 32; ++i)
 m32s[j+1][i] = m32s[j][i];
 for (i = 0; i != 256; ++i)
 m256s[j+1][i] = m256s[j][i];
 }

 for (j = ROUNDS - 1; j >= 0; j--) {
 // rbox
 for (i = 0; i < 256; i++)
 rm256[m256s[j][i]] = i;
 // decrypt
 for (i = 0; i != 32; ++i)
 input[i] ^= xors[j][i];
 for (i = 0; i != 32; ++i)
 input[i] = rm256[input[i]];
 for (i = 0; i != 32; ++i)
 output[m32s[j][i]] = input[i];
 for (i = 0; i != 32; ++i)
 input[m32s[j][i]] = output[i];
 };

 // print input 
 printf("input = ");
 for (i = 0; i < 33; i++)
 printf("%u, ", input[i]);
 putchar(10);
 printf("input = %sn", input);
}

int main(int argc, const char** argv, const char** envp)
{
 _BYTE last_input_flag[33] = { 47, 238, 122, 29, 149, 143, 143, 247, 59, 106, 136, 53, 69, 229, 45, 255, 13, 10, 226, 239, 237, 247, 7, 100, 159, 65, 44, 193, 159, 106, 155, 236, 0 };
 decrypt(0, last_input_flag);
 decrypt(1, last_input_flag);
 return 0;
}

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
架构、硬件相关API
```



```
__inline__ int metal_gpio_get_input_pin(struct metal_gpio *gpio, int pin)
// Get the value of the GPIO pin.
```



```
bool __fastcall metal_gpio_get_input_pin(int device, char pin)
{
 return device && (device->func(device) & (1 << pin)) != 0;
}
```



```
二
初始化
```



```
data[0:32) (32字节) = 0, 1, 2, 3, ... , 31
data[32:65) (32+1字节) = "ptm{REDACTEDREDACTEDREDACTEDRED}x00"
data[68:324) (256字节) = 0, 1, 2, 3, ... , 255
```



```
三
过程分析
```



```
v12 = &var644[(unsigned __int8)v10 + 1604];
v13 = &var644[(unsigned __int8)v11 + 1604];
v14 = *(v12 - 1604) + *(v13 - 1604);
*(v12 - 1604) = v14;
v15 = *(v13 - 1604);
*(v13 - 1604) = v14 - v15;
*(v12 - 1604) = v15 + *(v12 - 1604) - v14;
```



```
v14 = var644[v10] + var644[v11];
var644[v10] = v14;
v15 = var644[v11];
var644[v11] = v14 - v15;
var644[v10] = v15 + var644[v10] - v14;
```



```
_BYTE m32[32]; // &var644[0:32]
_BYTE input[33]; // &var644[32:64]
_BYTE m256[256]; // &var644[68:324]
_DWORD output[256]; // &var644[580:1604]
```



```
四
加密过程
```



```
五
流程2 解密
```



```
def get_bit_idx(x):
 i = 0
 res = []
 while x:
 if x & 1:
 res.append(i)
 i += 1
 x >>= 1
 return res

rows = [0]*32
cols = [0]*32
for r in range(16):
 res = get_bit_idx(row_sums[r])
 for a in res:
 rows[a] = r
for c in range(16):
 res = get_bit_idx(col_sums[c])
 for a in res:
 cols[a] = c
 
output = [0]*256
for i in range(32):
 output[rows[i]*16 + cols[i]] |= 1 << i
```



```
inputs = [0]*32
for i in range(256):
 res = get_bit_idx(output[i])
 for j in res:
 j = 31 - j
 inputs[j] = i
print(inputs)
```



```
六
流程1 对称密码 解密
```



```
_BYTE m32s[1337 + 1][32]; // &var644[0]
_BYTE m256s[1337 + 1][256]; // &var644[68]
_BYTE xors[1337][32];
void decrypt(unsigned int seed, _BYTE* last_input) {
 _BYTE input[33] = { 0, };
 _DWORD output[256] = { 0, }; // &var644[580]

 memcpy(input, last_input, 32);

 int i, j;

 _BYTE rm256[256];

 // cache rand result
 srand(seed);
 for (i = 0; i != 32; ++i)
 m32s[0][i] = i;
 for (i = 0; i != 256; ++i)
 m256s[0][i] = i;
 for (j = 0; j < ROUNDS; j++) {
 for (i = 0; i < 1000; i++) {
 _BYTE a = (int)rand() % 32;
 _BYTE b = (int)rand() % 32;
 if (a != b)
 {
 _BYTE temp;
 temp = m32s[j][a];
 m32s[j][a] = m32s[j][b];
 m32s[j][b] = temp;
 }
 };
 for (i = 0; i < 10000; i++) {
 _BYTE a = rand();
 _BYTE b = rand();
 if (a != b)
 {
 _BYTE temp;
 temp = m256s[j][a];
 m256s[j][a] = m256s[j][b];
 m256s[j][b] = temp;
 }
 };
 for (i = 0; i != 32; ++i)
 xors[j][i] = rand();
 // copy to next round
 for (i = 0; i != 32; ++i)
 m32s[j+1][i] = m32s[j][i];
 for (i = 0; i != 256; ++i)
 m256s[j+1][i] = m256s[j][i];
 }

 for (j = ROUNDS - 1; j >= 0; j--) {
 // rbox
 for (i = 0; i < 256; i++)
 rm256[m256s[j][i]] = i;
 // decrypt
 for (i = 0; i != 32; ++i)
 input[i] ^= xors[j][i];
 for (i = 0; i != 32; ++i)
 input[i] = rm256[input[i]];
 for (i = 0; i != 32; ++i)
 output[m32s[j][i]] = input[i];
 for (i = 0; i != 32; ++i)
 input[m32s[j][i]] = output[i];
 };

 // print input 
 printf("input = ");
 for (i = 0; i < 33; i++)
 printf("%u, ", input[i]);
 putchar(10);
 printf("input = %sn", input);
}

int main(int argc, const char** argv, const char** envp)
{
 _BYTE last_input_flag[33] = { 47, 238, 122, 29, 149, 143, 143, 247, 59, 106, 136, 53, 69, 229, 45, 255, 13, 10, 226, 239, 237, 247, 7, 100, 159, 65, 44, 193, 159, 106, 155, 236, 0 };
 decrypt(0, last_input_flag);
 decrypt(1, last_input_flag);
 return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1727178873.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727178874.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1727178875.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/10-1727178875.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/9-1727178876.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1727178877.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727178877.gif)