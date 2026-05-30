# 网鼎半决赛IoT-babyrtp

> 原文: https://www.ctfiot.com/218450.html
> ID: 218450

网鼎半决之后意难平，协工作室小伙伴共同研究了这道半决赛的rtp双端推流的题目。（由于是赛后复现，没有当时的环境，文中有不足之处望师傅们指正）

0x01 逻辑梳理

首先拿到附件之后，经典bin文件，先走binwalk提取一下固件内容，于usr文件夹中发现服务端逻辑文件

然后对pwn文件进行分析，这段代码实现了一个简单的 HTTP 服务器，通过socket创建套接字，bind绑定到一个端口（8080），然后通过listen进入监听状态，等待客户端连接。每当有连接到达时，服务器通过accept接受连接，并调用handle_request函数处理请求。

根据逻辑，我们跟进到handle_request函数，此处即是当接收客户端的请求时，函数extract_url会提取url参数的内容进行判断，然后返回赋值到s变量控制下面逻辑的走向

继续跟进到extract_url函数中看如何进行的提取判断操作，查找字符串"url="。提取其后面的内容作为 URL，然后检查提取到的 URL 是否是有效的 IPv4 地址。如果是有效的 IPv4 地址，则返回该 URL，否则释放内存并返回NULL。

分析到此处之后再返回到主逻辑中复盘，当s返回值有效时继续走向下面的if中的逻辑

跟进到push_stream函数之后会发现，此处使用rtp_aes_push对于flag内容进行了操作

转而现在继续分析rtp_aes_push文件中的内容

send_rtp_stream函数的实现，用于通过 RTP 流发送一个加密的 jpg 文件。使用了 FFmpeg 库进行 RTP 传输流的设置和编码，并且在传输过程中对数据进行了 AES 加密。（FFmpeg 是一个开源的多媒体处理库，用于录制、转换、流式传输和播放音视频文件。它支持几乎所有的音视频格式，是视频和音频处理领域的一个重要工具）

那么分析到现在逻辑已经理得比较清晰了，首先需要有一个正确的url传参，然后进入到if逻辑中，使程序流走到push_stream，进而执行while true; do ./rtp_aes_push flag.jpg aes_key.bin %s 5004; sleep 5; done的样例命令，然后运行rtp_aes_push启动rtp服务的传输。

0x02 实操模拟

首先于一台机器中伪造一个flag样例图用于此题复现，同时这台机器作为服务端启动

然后尝试get传输接收rtp流的客户端ip，发现走到了错误的逻辑

多次尝试之后使用了post传参，发现推流成功到这一步之后就只差临门一脚了，如何截获rtp传输的数据（此处传输的即是加密之后的flag.jpg内容)，即成为了解题的关键，我们此处选择使用wireshark截获rtp传输的流量，然后对流量中的数据进行分析，很明显的发现了rtp传输的流量

这里需要注意的是需要对流量进行rtp解码

解码之后发现正常的rtp流量

然后使用tshark对于rtp数据载荷进行提取（因为是分包发送，人话就是把这几个流的内容拼起来），tshark -r "rtp.pcapng" -Y rtp -T fields -e rtp.payload > out.txt，然后得到传输的AES密文。最后直接使用key进行AES的解密即可得到flag

原文始发于微信公众号（RwebSec）：网鼎半决赛IoT-babyrtp

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/8-1733360763.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1733360763.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/2-1733360764.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1733360764.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1733360765.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733360765.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1733360766.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/8-1733360766.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/2-1733360767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1733360767.png)