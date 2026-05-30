# 【WriteUP·中篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛

> 原文: https://www.ctfiot.com/186393.html
> ID: 186393

一个带有智能汽车远程控制的APP应用程序，能够通过它来发动汽车

（1）获取链接

（2）获取IPA

（3）简单的命令执行：双写加%0截断：ip=1.1.1.1%0acacatt flflagag.php

（6）由ssid：wifi和密码：root12222，生成PSK，用于解密空口wifi包内容（使用如下网址生成PSK https://www.wireshark.org/tools/wpa-psk.html）

（9）分析发现为压缩包文件，尝试打开，存在口令，此处为弱口令“123”解压出文件如下

（10）Winhex分析发现存在base64（url：https://www.qqxiuzi.cn/bianma/base64.htm）编码并再次16进制转字符串（url：https://www.sojson.com/hexadecimal.html），解码得flag

（6）flag{f7sgu2lsagbgfa90f63dc8b6e0e2Kg2lVW}

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1717846649.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/9-1717846650.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/10-1717846650.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1717846651.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/9-1717846651.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/7-1717846653.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1717846653.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1717846654.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/3-1717846656.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1717846657.png)