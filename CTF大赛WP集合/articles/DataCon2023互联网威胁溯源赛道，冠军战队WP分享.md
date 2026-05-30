# DataCon2023互联网威胁溯源赛道，冠军战队WP分享

> 原文: https://www.ctfiot.com/150471.html
> ID: 150471

由中国通信学会数据安全委员会指导，奇安信集团、清华大学网络研究院、北京市大数据中心、蚂蚁集团、腾讯安全大数据实验室、Coremail广东盈世、赛尔网络主办的DataCon大数据安全分析竞赛最终排名已揭晓。

清华大学TrickorTech战队、武汉大学N0nE429战队、中国科学院信息工程研究所404NOTFOUND战队、中国科学院信息工程研究所Hematopoiesisbshjdkvhbj战队、社会联合跃哥我真不会啊战队分别获得AI安全赛道、软件安全赛道、邮件安全赛道、互联网威胁溯源赛道、漏洞分析赛道冠军。

本期Hematopoiesisbshjdkvhbj战队为大家分享互联网威胁溯源赛道解题思路。

题目一：形形色色的DDoS

0-20s时间段：流量包集中发送

>20s时间段：每间隔20s会发送固定数量的流量包

会话：502个会话

节点：503台（502台其他主机+1台受害主机）

包含MON_GETLIST字段

响应包按照每 6 个 IP 进行分割，最多有 100 个响应包

NTP Flood攻击：100个源IP

UDP Flood攻击：100个源IP

SYN Flood攻击：200个源IP

慢速http header泛洪攻击：50个源IP

慢速http payload泛洪攻击：50个源IP

题目二：威胁情报的关联分析

题目三：藏于幕后的僵网C2

D-?)3L&U]XIUIVIS)*#$:07]XWSITSISTIX_V)*#$:7*53]XVUSX)$2:30,$]UWUVWUVX

JXNT-C2:1.2.3.4NODE_IP:
104.54.45.183NODE_PORT:
13241NEW_TIME:
20230231

F-?)3L&U]XIUIVIS)*#$:07]XWQIXQRIUWUIXXR)*#$:7*53]VVVVV)$2:30,$]UWUVWUVX

JXNT-C2:1.2.3.4NODE_IP:
106.167.202.117NODE_PORT:
33333NEW_TIME:
20230231

D-?)3L&U]XW`IXXIXUIUS`)*#$:07]WIWIWIW)*#$:7*53]VVVVV)$2:30,$]UWUVW`WX

JXNT-C2:
109.11.12.249NODE_IP:0.0.0.0NODE_PORT:
33333NEW_TIME:
20230901

题目四：消失的窃密流量

（1）很多文件中会多次出现全0的段落；
（2）16字节正好是AES分组长度（128比特）；
（3）分组密码的ECB模式会导致相同原文加密出相同的密文。

（1）ntp反射放大攻击的源ip：由反射放大攻击原理可知，这些ip都是ntp server的ip，与攻击无关。
（2）udp flood和syn flood攻击的源ip：由这两种攻击的原理可知，攻击流程中只需要源ip向被攻击ip发包，不需要接收被攻击ip响应，所以源ip可以任意伪造。我们无法确认这些源ip是否是伪造的。
（3）两种http慢速攻击的源ip：虽然只有单向流量，但可以确认完成了tcp握手，源ip无法伪装，因此这些ip是僵尸机的真实ip。可以算被控主机的ip，共计100个。（4）唯一外向流量的目的ip（93.33.5.89）：在4.2.1的分析中，我们怀疑这是个跳板机。一般来说，攻击者使用跳板机是为了隐藏自己的ip不被发现，不会使用自己的主机做跳板机，所以这个ip也是被控主机的ip。
（5）最长流的源ip（131.141.22.15）：看起来是正常的通信对象。
（6）被DDoS主机（83.250.118.40）：按照4.2.1的分析，koko就是运行在这个主机上的，毫无疑问属于被控制的主机，所以这个ip也是被控主机的ip。

（1）所有的目的ip：因为是蜜罐日志，所以这些ip都不是真实主机，忽略。
（2）大多数源ip和下载ip：除了表2-1中的ip，无法直接证明与本次攻击相关，忽略。
（3）106.167.202.117和104.54.45.183：根据第三题的逆向过程可知，这两个ip是P2P僵尸网络节点，且在日志中有对蜜罐进行过ssh爆破攻击，因此极大可能运行了koba的被控主机。
（4）101.147.195.126、195.220.160.50和66.65.23.150：缺乏明确信息，可能是攻击者自己使用的传播源和下载站，应该不是被控主机。

"username": "root", "password": "tsgoingon""username": "admin", "password": "admin123",

五、总结

六、附录

ptrace(PTRACE_TRACEME, 0, 0, 0);

参考文献

[1]https://blog.csdn.net/qq_32350719/article/details/88662306

[2]https://www.cloudflare.com/zh-cn/learning/ddos/ddos-low-and-slow-attack/

[3]https://github.com/mpgn/CVE-2019-7238

[4] https://github.com/ruCyberPoison/-Mirai-Iot-BotNet

[5] https://github.com/cq674350529/deflat

【推荐阅读】


```
D-?)3L&U]XIUIVIS)*#$:07]XWSITSISTIX_V)*#$:7*53]XVUSX)$2:30,$]UWUVWUVX
JXNT-C2:1.2.3.4NODE_IP:
104.54.45.183NODE_PORT:
13241NEW_TIME:
20230231
F-?)3L&U]XIUIVIS)*#$:07]XWQIXQRIUWUIXXR)*#$:7*53]VVVVV)$2:30,$]UWUVWUVX
JXNT-C2:1.2.3.4NODE_IP:
106.167.202.117NODE_PORT:
33333NEW_TIME:
20230231
D-?)3L&U]XW`IXXIXUIUS`)*#$:07]WIWIWIW)*#$:7*53]VVVVV)$2:30,$]UWUVW`WX
JXNT-C2:
109.11.12.249NODE_IP:0.0.0.0NODE_PORT:
33333NEW_TIME:
20230901
"username": "root", "password": "tsgoingon""username": "admin", "password": "admin123",
ptrace(PTRACE_TRACEME, 0, 0, 0);
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1702114276.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1702114277.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/5-1702114278.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1702114279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/5-1702114280.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702114281.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1702114282.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1702114283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702114284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702114285.png)