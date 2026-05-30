# 【WP】第二届“红明谷”杯数据安全大赛题目解析（二）

> 原文: https://www.ctfiot.com/32512.html
> ID: 32512

SM2

题目知识点：

Biased nonce attack

观察代码发现 nonce 有一定 bias，前 6 bits 永远是 0，构造格子解 HNP 得到密钥，解密得到 flag。

poc链接：https://raw.githubusercontent.com/chunqiugame/cqb_writeups/master/2022hmgb/sm2_poc.sage

MissingFile

00 楔子

本意是为了考察选手对于MTF的一些认知，以及对于微软里面常见的一个API CryptProtectData加密获得的数据，也就是常说的 DPAPI Blob的一些了解程度的考察。但是为了方便出题（其实是自己折磨自己了），用了各种办法将数据读入内存，反而导致flag的泄露（疑似是flag也被存在了内存中，还没有被抹去），导致出现了非预期解，给各位师傅道歉了。

01 致知力行

题目描述: 某日Akira检查自己电脑时，发现机器好像中毒了！Akira试着抢救，但被病毒发现，只剩下了一份快照，这份快照能帮Akira找到病毒留下的秘密吗？

题目描述中提到了机器中毒，其实就是指这台电脑 已经被攻击过，暗示memory之中会残留一些攻击者利用过的数据。通常情况下，内存中残留的数据不足以进行数据恢复，但是在某些特定情况下，数据已被加载到内存中时，便有获取某一些特定数据的机会，这一题就是模拟此场景。同时提到了被病毒发现，其实这里是想表达病毒进行了自我数据删除，所以有数据残留。

加密数据发现

对于这类内存分析题，首先通过volatility调查当前内存的版本。

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群

Q群:
703460426


```
Biased nonce attack
.volatility_2.6_win64_standalone.exe -f memory imageinfo
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 filescan
UsersNewGuestDesktopHacker
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 mftparser > mtfparser.txt
DPAPI：
全称Data Protection Application Programming Interface

DPAPI blob：
一段密文，可使用Master Key对其解密

Master Key：
64字节，用于解密DPAPI blob，使用用户登录密码、SID和16字节随机数加密后保存在Master Key file中

Master Key file：
二进制文件，可使用用户登录密码对其解密，获得Master Key

这部分内容选自：https://3gstudent.github.io/%E6%B8%97%E9%80%8F%E6%8A%80%E5%B7%A7-%E5%88%A9%E7%94%A8Masterkey%E7%A6%BB%E7%BA%BF%E5%AF%BC%E5%87%BAChrome%E6%B5%8F%E8%A7%88%E5%99%A8%E4%B8%AD%E4%BF%9D%E5%AD%98%E7%9A%84%E5%AF%86%E7%A0%81
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 hivelist
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 hashdump
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 getsids
dpapi::
masterkey /in:"master.key" /sid:S-1-5-21-206512979-2006505507-2644814589-1001 /password:
123456
dpapi::
blob /in:
dump_S3cret /masterkey:
092c4220064c30bc7f8b15d2d48957c4926af0632149b9c08cd87f34fc43aa1204d775bdc6ab429a0d4d0826fb80b08250b125d92913e2f7578cf778073bfe38
flag{Hide_Behind_Windows}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/2-1648169389.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/2-1648169390.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/7-1648169390.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/4-1648169391.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/6-1648169392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/9-1648169392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/0-1648169392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/7-1648169393.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/0-1648169393.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/3-1648169394.png)