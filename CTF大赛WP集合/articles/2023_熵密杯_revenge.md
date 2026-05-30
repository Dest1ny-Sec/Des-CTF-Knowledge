# 2023 熵密杯 revenge

> 原文: https://www.ctfiot.com/133267.html
> ID: 133267

咱们书接上回（没想到还能接上），在前边说我们注意到了 Gitea 中的改动，出题人对 openssl 项目中的 crypto/rand/drbg_lib.c 文件中一个生成随机数的函数进行了修改，将原本生成32字节随机数写死了。

当时猜测的是数字签名系统计算 msg1 签名，生成临时密钥的时候调用了这个函数。事实上，服务端在生成私钥时调用了该函数！

我们看到数字签名系统调试数据包中服务端使用的公钥（No.66）

随后进行本地测试，验证上面的随机数是否为服务端私钥

注意到和流量包中的公钥是相等的，于是我们就可以用服务端的私钥和客户端的公钥计算预主密钥，然后导入  wireshark 进行会话解密。

整个流量包中有两次会话的协商，我们先在第一个 Client Key Exchange 中抓取客户端的第一个公钥（No.69）

然后计算它们的协商密钥

得到 7ff739dbe782d963e54e3242d83b3a01a6535aed3579f6a514a664b363915903

另外找到 Client Hello 里的随机数（No.64）

预主密钥的格式为 PMS_CLIENT_RANDOM[空格]Random[空格]sharekey

于是第一个预主密钥为

同理我们在 No.3334 可以找到另一个 Random，在 No.3341 可以找到另一个客户端的公钥

最终预主密钥文件为

随后【编辑】->【首选项】->【TLS】

导入后我们即可看到解密后的流量。

追踪一下 HTTP 流即可看到签名系统的 用户名密码 以及 flag3

另外 socks 代理的用户名和密码可以在 No.19 的数据包中找到

进入数字签名系统后，

我们需要计算新消息的签名。

首先 SM2 签名理论上是不会有什么问题的，并且前面一题的考点已经是私钥泄露了，那么这里应该是没法直接获取私钥的。在签名中，与私钥同等重要的，就是临时密钥了。在上一篇文章中我们猜测这里可能是临时密钥重用。不过那需要至少已知两条签名我们才能恢复私钥，所以这个思路应该可以否定了。不过，我们在第二关还获取到了一份数字签名系统签名验签源码：sign-verify.c，那么切入点显然会在这了。

在其中的 Sign 函数中，我们注意到

看到  time_parse 和 derive_from_time 函数

乱七八糟的，但是总而言之，随机数 k 和消息中的时间相关。

那么思路就很显然了：我们可以计算签名 msg1 时使用的临时密钥 k，有了 k 也就能恢复签名用的私钥 sk，从而也就能给 msg2 签名了。

由于 c 的大数计算可麻烦，这里还是先用它的代码把临时密钥 k 打印出来先

编译指令：gcc tmpk.c -L. -l crypto -l ssl -o tmpk （把 tmpk.c 放在 openssl 目录下）

得到 D2D569D2A7250B2B27DF909C9AFC1FD9E0A555AEC4BFB5D80CD71F70ADACF414

已知临时密钥 
 ，根据签名值我们可以获取 

 ，而计算私钥 sk 的公式为

注意到这里有一个坑点，签名里的 r 和 s 用 FlipEndian 处理过，字节序变化了，所以我们在计算的时候也要相应处理

得到私钥 104515905597970870556286963199400550747760654012576876144731059595513283165045

验证一下

和公钥一致！

所以我们可以构造私钥文件 pri_pub/priSM2.key （ hex(bytes_to_long(long_to_bytes(sk::-1]))）

然后把main函数修改一下

运行得到 msg2 的签名


```
uint8_t rand0_32[32] = {0x67, 0xc6, 0x69, 0x73, 0x51, 0xff, 0x4a, 0xec, 0x29, 0xcd, 0xba, 0xab, 0xf2, 0xfb, 0xe3, 0x46, 0x7c, 0xc2, 0x54, 0xf8, 0x1b, 0xe8, 0xe7, 0x8d, 0x76, 0x5a, 0x2e, 0x63, 0x33, 0x9f, 0xc9, 0x9a};

    for(int i=0;i<outlen;i++){
        out[i] = rand0_32[i % 32];
    }
```



```
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

rand0 = [0x67, 0xc6, 0x69, 0x73, 0x51, 0xff, 0x4a, 0xec, 0x29, 0xcd, 0xba, 0xab, 0xf2, 0xfb, 0xe3, 0x46, 0x7c, 0xc2, 0x54, 0xf8, 0x1b, 0xe8, 0xe7, 0x8d, 0x76, 0x5a, 0x2e, 0x63, 0x33, 0x9f, 0xc9, 0x9a]

sk = "".join(hex(i)[2:].rjust(2,'0') for i in rand0)
print(sk)

privatekey=X25519PrivateKey.from_private_bytes(bytes.fromhex(sk))
print((privatekey.public_key()._raw_public_bytes().hex()))
```



```
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey,X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

rand0 = [0x67, 0xc6, 0x69, 0x73, 0x51, 0xff, 0x4a, 0xec, 0x29, 0xcd, 0xba, 0xab, 0xf2, 0xfb, 0xe3, 0x46, 0x7c, 0xc2, 0x54, 0xf8, 0x1b, 0xe8, 0xe7, 0x8d, 0x76, 0x5a, 0x2e, 0x63, 0x33, 0x9f, 0xc9, 0x9a]

sk = "".join(hex(i)[2:].rjust(2,'0') for i in rand0)
# print(sk)

privatekey=X25519PrivateKey.from_private_bytes(bytes.fromhex(sk))
# print((privatekey.public_key()._raw_public_bytes().hex()))

publickey=X25519PublicKey.from_public_bytes(bytes.fromhex('a0022027e0390ead7d82e1e74ae2d2f045fbf72896b9846d7f28bfa184280e3e'))

result=privatekey.exchange(publickey)
print(result.hex())
```



```
PMS_CLIENT_RANDOM 9d8f92cc2ac8f33293da5169d49c82794c660fc937bd0c1b05f5e062e491da85 7ff739dbe782d963e54e3242d83b3a01a6535aed3579f6a514a664b363915903
```



```
PMS_CLIENT_RANDOM 9d8f92cc2ac8f33293da5169d49c82794c660fc937bd0c1b05f5e062e491da85 7ff739dbe782d963e54e3242d83b3a01a6535aed3579f6a514a664b363915903
PMS_CLIENT_RANDOM b5dbfb40bc4c2b1a46bbc594fc89a56c17fe7db891beb7c111691516bd3117d1 4c8c1680018a8dd48749d642b6a6df5cc2104cb98842b82b0d748430108b8f61
```



```
//Generate Random Number
 unsigned char randomScalar[32];
 unsigned int i_time=0;
 time_parse(message, &i_time);
 if(derive_from_time(i_time,randomScalar,32))
  goto err;
 BN_bin2bn(randomScalar, 32, k);
```



```
int time_parse(char *str_time, unsigned int *i_time){
 struct tm s_time;

 /* strptime(str_time,"%Y年%m月%d日%H:%M:%S",&s_time);
 s_time.tm_isdst = -1;
 *i_time = mktime(&s_time);  */

 int year, month, day, hour, minute,second;
 sscanf(str_time,"%d-%d-%d %d:%d:%d", &year, &month, &day, &hour, &minute, &second);
 s_time.tm_year= year-1900;
 s_time.tm_mon= month-1;
 s_time.tm_mday= day;
 s_time.tm_hour= hour;
 s_time.tm_min= minute;
 s_time.tm_sec= second;
 s_time.tm_isdst= -1;

 *i_time = mktime(&s_time);
 return 0;
}

int derive_from_time(unsigned int seed, unsigned char *randomScalar, int length) {
    if (randomScalar == NULL || length <= 0) {
        return 1; // Invalid input
    }

    unsigned int currentSeed = seed;
    int generatedLength = 0;

    while (generatedLength < length) {
        unsigned char shaOutput[SHA256_DIGEST_LENGTH];
        SHA256((const unsigned char *)&currentSeed, sizeof(currentSeed), shaOutput);
        int remainingLength = length - generatedLength;
        int copyLength = remainingLength < SHA256_DIGEST_LENGTH ? remainingLength : SHA256_DIGEST_LENGTH;
        memcpy(randomScalar + generatedLength, shaOutput, copyLength);
        generatedLength += copyLength;
        currentSeed++;
    }
    return 0; // Success
}
```



```
//Generate Random Number
 unsigned char randomScalar[32];
 unsigned int i_time=0;
 time_parse(message, &i_time);
 if(derive_from_time(i_time,randomScalar,32))
  goto err;
 BN_bin2bn(randomScalar, 32, k);
 BN_print_fp(stdout, k); 
 printf("n");
```



```
from Crypto.Util.number import *
r = 0x37AF670C4742BD0C8D7CF68FCEBFE61885AA630695D50A15DF279CD64327466F
r = bytes_to_long(long_to_bytes(r)[::-1])
s = 0x6701CFB5F356887B9441323FDC08FBA900E1050109FD95F024DC9C178CEBE7A4
s = bytes_to_long(long_to_bytes(s)[::-1])
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
k = 0xD2D569D2A7250B2B27DF909C9AFC1FD9E0A555AEC4BFB5D80CD71F70ADACF414
print((k-s)*inverse(s+r,n)%n)
```



```
753bffd7cd2353cbe72702159162f8da8f7118d8b4944fe74ddbf7e2fee711e7
```



```
int main()
{
 unsigned char pub[64];
 unsigned char pri[64];
 unsigned char message1[128] = "2023-8-10 09:11:13, A transfers 50000.00 to B.";
 unsigned char message2[128] = "2023-8-10 11:31:01, B transfers 50000.00 to A.";
 unsigned char digest[32];
 unsigned char sig1[64];
 unsigned char sig2[64];
 int ret;

 printf("msg1:t%sn",message2);
 ret = Sign_Prifile(message2, sig1);
 user_printf_hex("sig1:t",sig1,64);
 ret = Verify_Pubfile(message2, sig1);
 printf("verify:t%dn",ret);

 return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742840.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/9-1693742841.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1693742842.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/7-1693742842.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1693742843.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/5-1693742844.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/6-1693742845.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/2-1693742846.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/3-1693742847.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742847.png)