# 之江杯-WriteUp

> 原文: https://www.ctfiot.com/269337.html
> ID: 269337

恭喜Venom在此次挑战赛中获得第一名的好成绩！

给各位大佬递茶

下面一起来看看WriteUp~

CTF

S7Comm 攻击协议分析

可得flag

梯形图2

内存取证分析

密码为空

发现有个notepad的进程。打开了flag。txt，还有个flag.rar

提取两个文件。发现flag。txt是加密的。压缩包也是加密的

附件直接string可得flag

IC卡分析

两个文件不同的点

金额是两个字节存储，按4字节为一组，前俩字节是数据，后俩字节是校验，校验方式为异或

比如0x7896 ^ 0x0000

后续的数据如下

7B 00 00 00 A6 FF FF FF 30 00 00 00

75 00 00 00 A0 FF FF FF 34 00 00 00

72 00 00 00 9A FF FF FF 5F 00 00 00

31 00 00 00 96 FF FF FF 6B 00 00 00

65 00 00 00 A0 FF FF FF 6D 00 00 00

79 00 00 00 A0 FF FF FF 73 00 00 00

69 00 00 00 8C FF FF FF 74 00 00 00

65 00 00 00 8D FF FF FF 7D 00 00 00

4字节一组。类似7B 00 00 00直接取值，即为0x7b，类似A6 FF FF FF的进行ff异或，即为0xa6^0xff

上位机通讯异常分析

S7协议恶意攻击分析

有个发到PLC的STOP包

异常的流量分析

strings 时发现有张图片，打开可得flag

梯形图分析1

工控组态分析

力控直接加载项目

modbus

tcp.stream eq 1

317772337d

1wr3}

666c61677b => flag{

3138676854 => 18ghT

317772337d => 1wr3}

注册表分析

工控现场的恶意扫描

简单Modbus协议分析

病毒文件恢复

https://lesuobingdu.360.cn/

上传信息直接在线解密

异常的工程文件

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org

本篇文章来源于微信公众号: ChaMd5安全团队

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144917-wxsync-2025-09-19304c29d1777d39ccb7b04e465b68b3.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144918-wxsync-2025-09-ac6eeec6a9b2ab238dffcac4814b2e28.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144920-wxsync-2025-09-8472b69ed014430f1db353406af9a3f1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144922-wxsync-2025-09-1e8e4c164dfea7af1ea048217ce25470.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144925-wxsync-2025-09-f69e5e2c83d9e56aeb7fe584405b7068.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144927-wxsync-2025-09-d77dd12d4fb62b130fc36acfbaff30f6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144929-wxsync-2025-09-94f41031fda6be9fa0e63810cb6786d3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144931-wxsync-2025-09-6bfe0e32fcd2c1b66effa65548557fea.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144932-wxsync-2025-09-100dfd79704f55ba370f8cf94c8a49d8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757144934-wxsync-2025-09-c055b8e935ad73bc906b01a62273c501.png)