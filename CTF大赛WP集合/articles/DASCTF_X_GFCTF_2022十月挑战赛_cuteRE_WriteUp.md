# DASCTF X GFCTF 2022十月挑战赛 cuteRE WriteUp

> 原文: https://www.ctfiot.com/72634.html
> ID: 72634

记录一下自己的做题记录，主要是利用动态分析的方式，获取关键数据信息。

一

信息搜集

64位程序，未加壳。

使用IDA寻找程序主函数。

程序的main函数主要分成3个部分：

如下图所示，程序获取用户输入后，先判断长度是否为32位，后将32位数据按奇偶，分成2部分。

主要由sub_405700、sub_4059F0、sub_406270和sub_400C10函数组成，稍后再分析其相关功能。

将生成的密文与程序内的密文比较，相同则满足程序的逻辑。

二

函数功能猜测

sub_405700(参数 byte_609450)
函数中包含BASE编码表，同时存在base关键字，猜测使用了Base64编码。

sub_4059F0（参数 unk_609350、byte_6090A0:’swpu’、4）
函数内容比较复杂，同时控制流还经过混淆，可以使用deflat去处控制流混淆。

sub_406270（参数 unk_609350、s2:
用户输入的部分数据、数据长度），根据代码中的rc4字符，猜测为rc4加密功能。

sub_400C10（参数 v35：用户输入的数据、v33：处理后的结果、长度）根据后面的strcmp函数，经过处理后的值为xlt0+V9PtVBKt0lEukZYug==，猜测该功能为Base64编码。

三

解密密文数据

密文1：
xlt0+V9PtVBKt0lEukZYug==

密文2：
“x72xA7xE5xB1xBFxD1x3AxC9x7Ex5Dx83xA8x21x4Fx70x90”

尝试使用base64解密密文1，和使用RC4,密钥’swpu’解密密文2，解密失败，猜测加密的相关参数可能在程序运行过程中被修改了。

我们回到sub_400C10((int64)v35, (int64)v33, *v30)
根据我们的猜测，该函数为Base64加密函数，同时sub_405700函数中，保存了Base64的相关信息，猜测sub_405700为加密的初始函数，sub_405700函数的输入参数为byte_609450，我们动态运行程序，查看执行完成后byte_609450地址的值。

发现该地址生成了一个新的base表，使用该表对密文进行解密，得到明文’DST{Wo7Xj5Ad8Nx8’。

base64_table = 'ghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef' def btoa(): # base64编码函数 s = input("input string to encode:n") n = len(s) % 3 x = '' asc = [] for i in range(len(s)): asc.append(ord(s[i])) # 取各字符ascii值 x += '{:
08b}'.format(asc[i]) # 将各字符ascii值转为二进制 if n: x += '0' * 2 * (3 - n) # 长度非3倍的结尾补零 i = 0 out = '' while i < len(x): out += base64_table[int(x[i:i + 6], 2)] i += 6 if n: out += '=' * (3 - n) # 补上'='使编码后长度为4倍 print(out) def atob(): # base64解码函数 s = input("input string to decode:n") b64 = [] x = '' for i in range(len(s)): if s[i] == '=': b64.append(0) else: for j in range(64): if (s[i] == base64_table[j]): b64.append(j) break x += '{:
06b}'.format(b64[i]) print(x) i = 0 out = '' while i < len(x): if int(x[i:i + 8], 2): out += chr(int(x[i:i + 8], 2)) i += 8 print(out) def main(): m = input('Input 1/2 to encode/decode:n') if m == '1': btoa() elif m == '2': atob() else: print('Error! Please restart the process!') main()

回到sub_406270函数，输入参数为unk_609350，该参数关联sub_4059F0函数，该函数利用byte_6090A0生成了unk_609350，动态运行后，查看byte_6090A0的地址，该地址的值为szv~。

使用该密钥对密文2进行解密，获得明文：
ACFg0Gw1Jo5Ix9C}

# RC4from Crypto.Util.number import bytes_to_long, long_to_bytes key = "szv~"msg = "x72xA7xE5xB1xBFxD1x3AxC9x7Ex5Dx83xA8x21x4Fx70x90"key = list(key)
# KSAS = [i for i in range(256)]j = 0for i in range(256): j = (j + S[i] + ord(key[i % len(key)])) % 256 S[i], S[j] = S[j], S[i]# PRGAi = 0j = 0keystream = []for k in range(len(msg)): i = (i + 1) % 256 j = (j + S[i]) % 256 S[i], S[j] = S[j], S[i] keystream.append(S[(S[i] + S[j]) % 256]) enc = "".join(map(chr, [(ord(msg[i]) ^ keystream[i]) for i in range(len(keystream))]))print(enc)

将二者按奇偶排列，即可获得flag。
DASCTF{gW0oG7wX1jJ5oA5dI8xN9xC8}

看雪ID：HU_Moon

https://bbs.pediy.com/user-home-920107.htm

*本文由看雪论坛 HU_Moon 原创，转载请注明来自看雪社区

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
一
信息搜集
二
函数功能猜测
三
解密密文数据
base64_table = 'ghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef' def btoa(): # base64编码函数 s = input("input string to encode:n") n = len(s) % 3 x = '' asc = [] for i in range(len(s)): asc.append(ord(s[i])) # 取各字符ascii值 x += '{:
08b}'.format(asc[i]) # 将各字符ascii值转为二进制 if n: x += '0' * 2 * (3 - n) # 长度非3倍的结尾补零 i = 0 out = '' while i < len(x): out += base64_table[int(x[i:i + 6], 2)] i += 6 if n: out += '=' * (3 - n) # 补上'='使编码后长度为4倍 print(out) def atob(): # base64解码函数 s = input("input string to decode:n") b64 = [] x = '' for i in range(len(s)): if s[i] == '=': b64.append(0) else: for j in range(64): if (s[i] == base64_table[j]): b64.append(j) break x += '{:
06b}'.format(b64[i]) print(x) i = 0 out = '' while i < len(x): if int(x[i:i + 8], 2): out += chr(int(x[i:i + 8], 2)) i += 8 print(out) def main(): m = input('Input 1/2 to encode/decode:n') if m == '1': btoa() elif m == '2': atob() else: print('Error! Please restart the process!') main()
# RC4from Crypto.Util.number import bytes_to_long, long_to_bytes key = "szv~"msg = "x72xA7xE5xB1xBFxD1x3AxC9x7Ex5Dx83xA8x21x4Fx70x90"key = list(key)
# KSAS = [i for i in range(256)]j = 0for i in range(256): j = (j + S[i] + ord(key[i % len(key)])) % 256 S[i], S[j] = S[j], S[i]# PRGAi = 0j = 0keystream = []for k in range(len(msg)): i = (i + 1) % 256 j = (j + S[i]) % 256 S[i], S[j] = S[j], S[i] keystream.append(S[(S[i] + S[j]) % 256]) enc = "".join(map(chr, [(ord(msg[i]) ^ keystream[i]) for i in range(len(keystream))]))print(enc)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668126689.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1668126690.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668126690.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668126691.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668126692.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668126692.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668126692.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668126692.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1668126693.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668126693.png)