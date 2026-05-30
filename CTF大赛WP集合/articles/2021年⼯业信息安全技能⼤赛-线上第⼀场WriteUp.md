# 2021年⼯业信息安全技能⼤赛-线上第⼀场WriteUp

> 原文: https://www.ctfiot.com/1685.html
> ID: 1685

简单的梯形图

和利时V3.1.5B3及以上版本的组态软件AutoThink打开梯形图程序

解题思路

损坏的风机

解题思路

⼯控现场⾥异常的⽂件

解题思路

直接改EAX过掉反调试

过掉检测以后直接在调试窗口里就能看到flag

隐藏的⼯程

解题思路

密码：ICS

提取出来⼀个蓝凑云连接：

https://wwr.lanzoui.com/iIMaiqcpaxg 

是kingview 6.55⼯程⽂件

OPC协议分析

解题思路

流量里的两个主机 11 主机名是 ABC，21 主机名是 BCD，两台电脑都是 Windows，11 向 21 发请求。

⼯控安全异常取证分析

解题思路

解压出来两个⽂件，⼀个1122，⽂件挺⼤，另⼀个是 112233，1kb ⼀看就知道是个vmdk。

将 112233 改名为 Windows Server 2003 Web Edition-1.vmdk 

将 1122 改名为 Windows Server 2003 Web Edition-1-ﬂat.vmdk 

⽤ DiskGenius 打开，应该是个NTFS分区FDD，没有分区表的那种。

从名为 mp4.mp4 的⽂件中提取出⼀段 ascii 字符串。 

提取出字符串

HEX -> HEX -> B32 -> B32 -> B32 -> B64 -> B64 -> HEX -> B32 -> B64 -> B64

恶意文件分析

解题思路

无壳。进去类似一个shell

程序流程，输入32长度的哈希字符串，bytes.fromhex然后运行关键 crackme 函数。

findcrypt发现文件中有CRC32常量。

crackme函数中包含了一个硬编码的key，

从开源项目中可以检索到。

https://github.com/TurboPack/LockBox3/blob/master/run/ciphers/uTPLb_AES.pas

https://chromium.googlesource.com/chromiumos/platform/ec/+/refs/heads/stabilize-7797.B/test/tpm_test/crypto_test.xml

输入与硬编码的Key、加密结果作比较。16轮。

循环16次看ECX值即可dump出预期输入。拼起来可以得到：22d72a581f3a61e61e5b127e47ad8c0c

将这个值输入程序，得到flag

Fins协议通讯

解题思路11683 号数据包

U2FsdGVkX1/bWSZYUeFDeonQhK0AUHr9Tm7Ic20PRXxlPvlwG6a4fQ==

3DES解密

https://www.sojson.com/encrypt_triple_des.html

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1634876963.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876963.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634876964.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634876964.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1634876965.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634876965.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/4-1634876965.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/8-1634876965.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634876966.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/9-1634876966.png)