# Nep CTF password：rc4和换表base64算法分析

> 原文: https://www.ctfiot.com/167920.html
> ID: 167920

一

背景

这题考查的主要对base64底层算法的了解，如果不了解他的实现原理，破解它还是相当有难度的。它在so层主要考察了base64算法的实现流程，在java层考察了rc4加密算法，接下来我们详细分析算法还原的过程。

二

代码分析

打开APP先简单试玩下，发现首页有输入key和密码两个输入框，把代码拖入到jadx中。我们从代码找到首页代码。

从代码中可以看出，他有2块验证，verify(String str) == 0 ，file(byte[] bArr, String str) == true。第一个验证肯定是在so文件进行了加密，第二个在是一个加密比较，满足 iArr2 = {139, 210, 217, 93, 149, 255, 126, 95, 41, 86, 18, 185, 239, 236, 139, 208, 69}的元素比较，就可以得到明文。

将APK解压，找到目标文件，拖入到IDA中。在导出表中我们很容易发现目标函数Java_com_nepnep_app_MainActivity_verify。

代码逻辑：

1.初始化变量和数组：首先，代码声明了一些变量和数组，其中包括字符串指针 a3_val、整数变量 a3_len、循环计数变量 v7 和 v8，以及一些用于存储中间结果的数组 v28 和 v30。

2.获取系统寄存器的值：通过 _ReadStatusReg 函数，代码从系统寄存器中获取一个值，并将其存储在变量 v33 中。

3.获取字符串的 UTF-8 表示：通过 JNI 函数 GetStringUTFChars 和 GetStringUTFLength，代码获取了从 Java 传递进来的字符串 a3 的 UTF-8 表示，并将其分别存储在 a3_val 和 a3_len 中。

4.字符串处理：代码接下来对字符串进行了一系列的处理。首先，它初始化了一个用于存储结果的数组 s，并通过两个函数调用 sub_77C 和 sub_8A4 对字符串进行了进一步的处理。

5.循环处理字符串的每个字符：代码通过循环处理字符串的每个字符，按照一定的规则进行转换，并将结果存储在数组 v28 中。这个循环分为两个阶段：首先处理每个三个字符的块，然后处理剩余的字符。

6.释放字符串的 UTF-8 表示：在处理完字符串后，通过 JNI 函数 ReleaseStringUTFChars，释放从 Java 获取的字符串的 UTF-8 表示。

7.比较字符串：最后，代码使用 strcmp 比较处理后的字符串是否与硬编码的字符串 “3g6L2PWL2PXFmR+7ise7iq==” 相匹配。如果匹配，函数返回 1LL，否则返回 0LL。

从逆向的思维来考虑：既然要满足 v28 = 3g6L2PWL2PXFmR+7ise7iq==的逻辑，我们就反向推算生成的算法。

aAbcdefghijklmn : “abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ”

看着像base64用到的对应表字符串，但是顺序好像也不对。先来反推 v28的值。以第一个值为例：3
v28[0] =3
aAbcdefghijklmn[v30[0]] = 3
v30[0] = 29
那么：
v30[1] = 6
v30[2] = 32
.
.
.
以此类似我们用python还原他的算法：

aAb_str = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ" # aAbcdefghijklmn 的定义

def get_aAb_str_len(ab_str):
 i = 0
 for ab in aAb_str:
 if ab == ab_str:
 return i
 i = i + 1

# 反向求解出 v12 的值
s1 = "3g6L2PWL2PXFmR+7ise7iq=="
s1_one = "3g6L2PWL2PXFmR+7ise7iq"
if __name__ == '__main__':
 v30= []
 v5 = 0
 for one in s1_one:
 # aAbcdefghijklmn[v30[v5]] = one
 get_len = get_aAb_str_len(one)
 v30.append(get_len)
 # print(get_len)
 print("v30",v30)

v30 = [29, 6, 32, 49, 28, 53, 60, 49, 28, 53, 61, 43, 12, 55, 36, 33, 8, 18, 4, 33, 8, 16]

再还原他的算法，我们再将v30带入其中，验证：

aAb_str = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ" # aAbcdefghijklmn 的定义
s1 = "3g6L2PWL2PXFmR+7ise7iq=="
v30 = [29, 6, 32, 49, 28, 53, 60, 49, 28, 53, 61, 43, 12, 55, 36, 33, 8, 18, 4, 33, 8, 16]
print("v30 ",v30)
v7 = 16
v5 = 0
s1_arr = [""] * (len(s1))
while v7 >= 1:
 if v7 < 3:
 s1_arr[v5] = aAb_str[v30[v5]]
 s1_arr[v5 + 1] = aAb_str[v30[v5 + 1]]
 print("s1_arr[v5 + 1] ", s1_arr[v5 + 1], v5 + 1, v30[v5 + 1])
 if v7 == 1:
 v9 = "="
 s1_arr[v5 + 2] = "="
 v8 = v5 + 3
 else:
 print(" s1_arr[v5 + 2] ", s1_arr[v5 + 2], v5 + 2)
 v8 = v5 + 3
 v9 = "="
 v5 = v8
 else:
 s1_arr[v5] = aAb_str[v30[v5]]
 s1_arr[v5 + 1] = aAb_str[v30[v5 + 1]]
 s1_arr[v5 + 2] = aAb_str[v30[v5 + 2]]
 v8 = v5 + 3
 v5 = v5 + 4
 v9 = aAb_str[v30[v8]]
 print("v8 = ", v8)
 s1_arr[v8] = v9
 print(s1_arr)
 print("v7 : ", v7)
 v7 = v7 - 3
 print("v7 : ", v7)
print("s1_arr ", s1_arr)
print(v30)

s1_arr = [‘3’, ‘g’, ‘6’, ‘L’, ‘2’, ‘P’, ‘W’, ‘L’, ‘2’, ‘P’, ‘X’, ‘F’, ‘m’, ‘R’, ‘+’, ‘7’, ‘i’, ‘s’, ‘e’, ‘7’, ‘i’, ‘q’, ‘=’, ‘=’]

到此：
v30=[29, 6, 32, 49, 28, 53, 60, 49, 28, 53, 61, 43, 12, 55, 36, 33, 8, 18, 4, 33, 8, 16]

现在关键是这2个函数：
sub_77C(a3_val, (__int64)s, a3_len % 3);
sub_8A4(s, (__int64)v30);

先来看：sub_77C

这段代码的作用是将输入字符串中的每个字符进行一系列位运算和转换，然后将处理后的结果按照 8 字节对齐的方式存储在指定的内存地址中。同时，根据额外情况，可能还需要在存储结果的内存地址后面追加两个或四个字节的数值。

frida hook sub_77C

function hook_so() {
 Java.perform(function () {

 var syms_addr = Process.getModuleByName("libart.so").enumerateSymbols();
 var GetStringUTFChars_addr = NULL;
 for (var index = 0; index < syms_addr.length; index++) {
 const sym_addr = syms_addr[index];
 if (sym_addr.name.indexOf("Check") == -1 && sym_addr.name.indexOf("GetStringUTFChars") >= 0) {
 GetStringUTFChars_addr = sym_addr.address;
 }
 }

 Interceptor.attach(GetStringUTFChars_addr, {
 onEnter: function (args) {
 // console.log("GetStringUTFChars_addr args : ", ptr(args[1]).readCString())
 }, onLeave: function (retval) {
 // console.log("GetStringUTFChars_addr retval ", hexdump(retval))
 }
 })

 var module_addr = Module.findBaseAddress("libnative-lib.so");
 console.log("module_addr ", module_addr);
 var sub_8A4 = module_addr.add(0x8A4);
 var sub_77C = module_addr.add(0x77C);
 console.log("sub_92C ", sub_77C)
 var v127 = NULL
 Interceptor.attach(sub_77C, {
 onEnter: function (args) {
 console.log("sub_77C arg[0", args[0].readCString(), hexdump(args[0]))
 console.log("sub_77C arg[1", args[1].readCString(), hexdump(args[1]))
 // console.log("sub_77C arg[2",args[2].readCString(),hexdump(args[2]))
 // console.log("arg[2", args[2])
 v127 = args[1]
 }, onLeave: function (retval) {
 console.log("retval ", v127.readCString())
 console.log("retval ", hexdump(v127))
 //011000010110001001100011011100100110010101110111011101110110010100
 }
 })

 var v12 = NULL
 Interceptor.attach(sub_8A4, {
 onEnter: function (args) {
 console.log("sub_8A4 arg[0", args[0].readCString(), hexdump(args[0]))
 v12 = args[1]
 console.log("sub_8A4 v12 args[1] = ", args[1])
 }, onLeave: function (retval) {
 console.log("sub_8A4 retval v12 = ", v12)
 console.log("sub_8A4 retval v12 s = ", ptr(v12).readByteArray(64))
 console.log("sub_8A4retval ", v12.readCString())
 console.log("sub_8A4 retval ", hexdump(v12))
 }
 })
 })
}

输入字串，最终得到的是一个二进制的字符。

说明 输入的字符串 经过sub_77C() 转成了二进制。

再来看看sub_8A4(s, (__int64)v30)

根据目前的线索：s是二进制字符，v30也知道。推到出s就破案了。

代码逻辑：

1.初始化变量：声明了几个变量，其中包括整数变量 v4、循环计数变量 i、结果变量 result、字符指针 v7、整数变量 v8，以及字符变量 v9。

2.循环处理字符串中的每个块：
（1）进入一个无限循环，循环变量 i 从 0 开始递增。
（2）获取字符串 s 的长度，将结果存储在 result 中。
（3）如果 i 大于等于字符串长度除以 6 的结果，说明已经处理完字符串，跳出循环。
（4）计算 v7，指向字符串 s 中当前块的起始位置。
（5）计算 v8，将 v4 按照 2 字节对齐的方式，即将最低位清零。
（6）v4 每次递增 6，表示处理一个块的六个字符。
（7） 对于每个字符块，执行一系列位运算：将当前字符块的第一个字符与 *(_BYTE *)(a2 + i) 相加，并将结果存储在 *(_BYTE *)(a2+ i) 中。将第二个字符与 v8 相加，并将结果存储在 *(_BYTE *)(a2 + i) 中。

分析到这我来看下base64：

Base64编码过程：(1). 将原数据每三个字节作为一组，一共是24个二进制位；(2). 将这24个二进制位分为四组，每个组有6个二进制；(3). 在每组前面加两个00扩展成32个二进制位，即四个字节；(4). 根据下图中的Base64索引表，得到扩展后的每个字节对应的符号：

从上面分析的种种迹象表明，sub_77C、sub_8A4应该就是字符串经过base64编码的过程，v30是base64的索引。既然如此，我们对着正常编码表映射出v30的对应的编码：dGgxc18xc19rM3khISEhIQ==
进行解密：key = th1s_1s_k3y!!!!!

总结 : key 加密流程就是：base64编码后，和自定义的编码表换位。如果熟悉base64编码的底层原理，应该是一眼就能看穿其中的道理。

从这段代码我们可以分析出来：
iArr = iArr2

接下来我们用分别还原这2个函数：en1(iArr, str, str.length());en2(iArr, bArr, bArr.length);

en1

def Rc4_init(S, K): # S盒初始化置换,K为密钥
 j = 0
 k = []
 for i in range(256):
 S.append(256 - i)
 k.append(K[i % len(K)])
 for i in range(256):
 j = (j + S[i] + ord(k[i])) % 256
 S[i], S[j] = S[j], S[i] # 交换S[i],S[j]

en2

def rc4_Decrypt1(S, D):
 i = j = 0
 result = ''
 for a in D:
 i = (i + 1) % 256
 j = (j + S[i]) % 256
 S[i], S[j] = S[j], S[i]
 t = (S[i] + S[j]) % 256
 k = chr(a ^ S[(S[i] + S[j]) % 256])
 result += k
 return result

三

完整的算法还原

综合所有的分析，我们写出完整的算法：

import base64
import binascii

s1 = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ"
s2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ

data = "3g6L2PWL2PXFmR+7ise7iq=="

data_y = "dGgxc18xc19rM3khISEhIQ=="

print(str.maketrans(s1, s2))
print(data.translate(str.maketrans(s1, s2)).encode('utf-8'))
key = str(base64.b64decode(data.translate(str.maketrans(s1, s2)).encode('utf-8')), encoding="utf-8")
print(" key = ",key)

def Rc4_init(S, K): # S盒初始化置换,K为密钥
 j = 0
 k = []
 for i in range(256):
 S.append(256 - i)
 k.append(K[i % len(K)])
 for i in range(256):
 j = (j + S[i] + ord(k[i])) % 256
 S[i], S[j] = S[j], S[i] # 交换S[i],S[j]

def rc4_Decrypt1(S, D):
 i = j = 0
 result = ''
 for a in D:
 i = (i + 1) % 256
 j = (j + S[i]) % 256
 S[i], S[j] = S[j], S[i]
 t = (S[i] + S[j]) % 256
 k = chr(a ^ S[(S[i] + S[j]) % 256])
 result += k
 return result

bb = [139, 210, 217, 93, 149, 255, 126, 95, 41, 86, 18, 185, 239, 236, 139, 208, 69]
print("key: " + key)
s = []
Rc4_init(s, key)
z = rc4_Decrypt1(s, bb)
print("Decrypt:" + z)

明文：Y0uG3tTheP4ssw0rd

验证：

看雪ID：西贝巴巴

https://bbs.kanxue.com/user-home-961239.htm

*本文为看雪论坛优秀文章，由 西贝巴巴 原创，转载请注明来自看雪社区

# 往期推荐

1、摘除MiniFilter回调的正确姿势

2、bpf在android逆向中的辅助效果

3、NDK集成OLLVM模块流程记录

4、【NKCTF】babyHeap-Off by one&Tcache Attack

5、Qemu源码浅析之v0.1.6

6、堆利用学习：the house of einherjar

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
背景
```



```
二
代码分析
```



```
aAb_str = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ" # aAbcdefghijklmn 的定义

def get_aAb_str_len(ab_str):
 i = 0
 for ab in aAb_str:
 if ab == ab_str:
 return i
 i = i + 1

# 反向求解出 v12 的值
s1 = "3g6L2PWL2PXFmR+7ise7iq=="
s1_one = "3g6L2PWL2PXFmR+7ise7iq"
if __name__ == '__main__':
 v30= []
 v5 = 0
 for one in s1_one:
 # aAbcdefghijklmn[v30[v5]] = one
 get_len = get_aAb_str_len(one)
 v30.append(get_len)
 # print(get_len)
 print("v30",v30)
```



```
aAb_str = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ" # aAbcdefghijklmn 的定义
s1 = "3g6L2PWL2PXFmR+7ise7iq=="
v30 = [29, 6, 32, 49, 28, 53, 60, 49, 28, 53, 61, 43, 12, 55, 36, 33, 8, 18, 4, 33, 8, 16]
print("v30 ",v30)
v7 = 16
v5 = 0
s1_arr = [""] * (len(s1))
while v7 >= 1:
 if v7 < 3:
 s1_arr[v5] = aAb_str[v30[v5]]
 s1_arr[v5 + 1] = aAb_str[v30[v5 + 1]]
 print("s1_arr[v5 + 1] ", s1_arr[v5 + 1], v5 + 1, v30[v5 + 1])
 if v7 == 1:
 v9 = "="
 s1_arr[v5 + 2] = "="
 v8 = v5 + 3
 else:
 print(" s1_arr[v5 + 2] ", s1_arr[v5 + 2], v5 + 2)
 v8 = v5 + 3
 v9 = "="
 v5 = v8
 else:
 s1_arr[v5] = aAb_str[v30[v5]]
 s1_arr[v5 + 1] = aAb_str[v30[v5 + 1]]
 s1_arr[v5 + 2] = aAb_str[v30[v5 + 2]]
 v8 = v5 + 3
 v5 = v5 + 4
 v9 = aAb_str[v30[v8]]
 print("v8 = ", v8)
 s1_arr[v8] = v9
 print(s1_arr)
 print("v7 : ", v7)
 v7 = v7 - 3
 print("v7 : ", v7)
print("s1_arr ", s1_arr)
print(v30)
```



```
function hook_so() {
 Java.perform(function () {

 var syms_addr = Process.getModuleByName("libart.so").enumerateSymbols();
 var GetStringUTFChars_addr = NULL;
 for (var index = 0; index < syms_addr.length; index++) {
 const sym_addr = syms_addr[index];
 if (sym_addr.name.indexOf("Check") == -1 && sym_addr.name.indexOf("GetStringUTFChars") >= 0) {
 GetStringUTFChars_addr = sym_addr.address;
 }
 }

 Interceptor.attach(GetStringUTFChars_addr, {
 onEnter: function (args) {
 // console.log("GetStringUTFChars_addr args : ", ptr(args[1]).readCString())
 }, onLeave: function (retval) {
 // console.log("GetStringUTFChars_addr retval ", hexdump(retval))
 }
 })

 var module_addr = Module.findBaseAddress("libnative-lib.so");
 console.log("module_addr ", module_addr);
 var sub_8A4 = module_addr.add(0x8A4);
 var sub_77C = module_addr.add(0x77C);
 console.log("sub_92C ", sub_77C)
 var v127 = NULL
 Interceptor.attach(sub_77C, {
 onEnter: function (args) {
 console.log("sub_77C arg[0", args[0].readCString(), hexdump(args[0]))
 console.log("sub_77C arg[1", args[1].readCString(), hexdump(args[1]))
 // console.log("sub_77C arg[2",args[2].readCString(),hexdump(args[2]))
 // console.log("arg[2", args[2])
 v127 = args[1]
 }, onLeave: function (retval) {
 console.log("retval ", v127.readCString())
 console.log("retval ", hexdump(v127))
 //011000010110001001100011011100100110010101110111011101110110010100
 }
 })

 var v12 = NULL
 Interceptor.attach(sub_8A4, {
 onEnter: function (args) {
 console.log("sub_8A4 arg[0", args[0].readCString(), hexdump(args[0]))
 v12 = args[1]
 console.log("sub_8A4 v12 args[1] = ", args[1])
 }, onLeave: function (retval) {
 console.log("sub_8A4 retval v12 = ", v12)
 console.log("sub_8A4 retval v12 s = ", ptr(v12).readByteArray(64))
 console.log("sub_8A4retval ", v12.readCString())
 console.log("sub_8A4 retval ", hexdump(v12))
 }
 })
 })
}
```



```
def Rc4_init(S, K): # S盒初始化置换,K为密钥
 j = 0
 k = []
 for i in range(256):
 S.append(256 - i)
 k.append(K[i % len(K)])
 for i in range(256):
 j = (j + S[i] + ord(k[i])) % 256
 S[i], S[j] = S[j], S[i] # 交换S[i],S[j]
```



```
def rc4_Decrypt1(S, D):
 i = j = 0
 result = ''
 for a in D:
 i = (i + 1) % 256
 j = (j + S[i]) % 256
 S[i], S[j] = S[j], S[i]
 t = (S[i] + S[j]) % 256
 k = chr(a ^ S[(S[i] + S[j]) % 256])
 result += k
 return result
```



```
三
完整的算法还原
```



```
import base64
import binascii

s1 = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ"
s2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ

data = "3g6L2PWL2PXFmR+7ise7iq=="

data_y = "dGgxc18xc19rM3khISEhIQ=="

print(str.maketrans(s1, s2))
print(data.translate(str.maketrans(s1, s2)).encode('utf-8'))
key = str(base64.b64decode(data.translate(str.maketrans(s1, s2)).encode('utf-8')), encoding="utf-8")
print(" key = ",key)

def Rc4_init(S, K): # S盒初始化置换,K为密钥
 j = 0
 k = []
 for i in range(256):
 S.append(256 - i)
 k.append(K[i % len(K)])
 for i in range(256):
 j = (j + S[i] + ord(k[i])) % 256
 S[i], S[j] = S[j], S[i] # 交换S[i],S[j]

def rc4_Decrypt1(S, D):
 i = j = 0
 result = ''
 for a in D:
 i = (i + 1) % 256
 j = (j + S[i]) % 256
 S[i], S[j] = S[j], S[i]
 t = (S[i] + S[j]) % 256
 k = chr(a ^ S[(S[i] + S[j]) % 256])
 result += k
 return result

bb = [139, 210, 217, 93, 149, 255, 126, 95, 41, 86, 18, 185, 239, 236, 139, 208, 69]
print("key: " + key)
s = []
Rc4_init(s, key)
z = rc4_Decrypt1(s, bb)
print("Decrypt:" + z)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1710763692.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1710763693.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1710763693.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1710763694.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1710763694.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1710763694.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1710763695.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1710763695.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/8-1710763695.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1710763696.jpeg)