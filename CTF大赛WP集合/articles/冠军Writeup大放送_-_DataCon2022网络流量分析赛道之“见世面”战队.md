# 冠军Writeup大放送 | DataCon2022网络流量分析赛道之“见世面”战队

> 原文: https://www.ctfiot.com/91160.html
> ID: 91160

由奇安信集团、清华大学网络研究院、蚂蚁集团、腾讯安全大数据实验室、Coremail论客主办的DataCon2022大数据安全分析竞赛线上赛和决赛已圆满落幕，五大赛道第一名也已各归其主。赛后，DataCon组委会后台收到很多关于“求大佬Writeup”的私信，今天，大家期待的冠军Writeup闪亮登场啦！

首先要分享的是网络流量分析赛道排名第一的见世面战队writeup。见世面战队是由广州大学网络空间安全学院方滨兴院士班的五位小伙伴组建而成，分别为曾东阳、顾家乐、张哲维、孙一航、徐颖慧，指导老师为李树栋老师。

广州大学方滨兴院士班简称“方班”，自2017年成立以来，斩获各类比赛大奖，方班loom战队曾荣获2019首届DataCon大数据安全分析竞赛（恶意代码行为分析方向）冠军，方班IStar战队和loom战队又在2020第二届DataCon（DNS恶意域名分析和恶意代码分析赛道）荣获奖项。

见世面战队成员们研究方向广泛，热爱大数据和网络安全。秉持“多参与，增阅历，见世面”的原则，团队共同学习，积极参与比赛，学习先进思想技术，立志为网络与信息安全贡献力量。

第1章 挖矿流量检测

图1.1自行抓取的挖矿流量包

图1.3安全流量过滤代码

图1.7抓取TLS通讯包

图1.9分析“ChangeCIPherSpec”的TLS包

图1.10分析pcap文件

图1.13“ChangeCIPherSpec”流量包限制条件

图1.20特征包识别过滤结果

black_ssl3.pcap:
自行获取的加密挖矿流量包
black_ssl3.pcap_Flow.csv:
CICFlowMeter对black_ssl3.pcap的处理结果cryptomining.pcap_Flow.csv:
CICFlowMeter对赛方提供的cryptomining.pcap处理结果
full.csv:
cryptomining.pcap用wireshark导出的全部流量包信息
full_http2.csv:
用于排除干扰的http与h2协议http的包信息
mining_check_finish.py:
代码文件，其中check_stream函数为主要处理函数

第2章 智能蜜罐环境构建-Level1

图2.1解析请求代码

图2.8替换数据类型代码

图2.18poc测试图

图2.19poc测试结果图

datacon_l1_sever.py:
构建的服务器，用于接收请求报文并返回正确的响应。datacon_l1_poc_sent.py:
请求重发器，用于测试构造的代码是否正确。

第3章 智能蜜罐环境构建-Level2

图3.1字符串转换代码

图3.5正则匹配代码

datacon_l2_server_clean.py:
构建的Level2服务器，用于接收请求并返回响应。datacon_l2_poc_sent.py:
Level2的请求重发器，用于测试服务器是否能够正确响应。

参考文献

[1]Xti9er、七夜、pav1.(2021,November18).虚拟货币挖矿检测与防御.腾讯安全应急响应心.https://security.tencent.com/index.php/blog/msg/208

[2]Charm1y.(2019,February7).Suricata下的挖矿行为检测.FREEBUF.https://www.freebuf.com/articles/network/195171.html

[3]Mubie,haoyuma.(2021).MaliciousMiningBehaviorDetectionSystemofEncryptedDigitalCurrencyBasedonMachineLearning.SafetyTechnologiesandFaultTolerantMethodsforEngineering2021.https://doi.org/10.1155/2021/2983605

[4]Madneai.(2020,May8).流量分析的瑞士军刀：Zeek.FREEBUF.https://www.freebuf.com/sectool/235587.html

[5]Jayus.(2020,June19).网络安全数据集流量特征提取工具Cicflowmeter.安全客.https://www.anquanke.com/post/id/207835

[6]Lebron-jian.(2019,May11).Python机器学习笔记：异常点检测算法——OneClassSVM.博客园.https://www.cnblogs.com/wj-1314/p/10701708.html

[7]Lebron-jian.(2019,April13).Python机器学习笔记：异常点检测算法——IsolationForest.博客园.https://www.cnblogs.com/wj-1314/p/10461816.html

[8]Ahlashkari.(2020,June18).CICFlowMeter.Github.

https://github.com/ahlashkari/CICFlowMeter

[9]Nebutech.(2022,September2).NBMiner.Github.

https://github.com/NebuTech/NBMiner

[10]Chaitin.(2022,October31).Xray.Github.https://github.com/chaitin/xray

[11]Chaitin.(2022,October31).Xray.Xray安全评估工具文档.

https://docs.xray.cool/#/guide/poc

[12]Python官方.(2019,October14).Http.Server—HTTP服务器.Python.Org.https://docs.Python.org/zh-cn/3.8/library/http.server.html#http.server.HTTPServer

[13]Md-irohas.(2019,November13).Tcppc.GitHub.https://github.com/md-irohas/tcppc-go

[14]hktalent.(2022,July27).Scan4all.GitHub.

https://github.com/hktalent/scan4all/tree/main/pocs_yml/ymlFiles

添加DataCon小助手微信
微信号：DataConofficial
获取更多大数据安全知识
进群还有超多活动、福利
DataCon定制服饰、背包等精彩好礼
等你来拿！

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673403310.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673403310.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1673403311.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1673403311.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673403312.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673403312.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673403313.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673403313.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673403314.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673403314.jpeg)