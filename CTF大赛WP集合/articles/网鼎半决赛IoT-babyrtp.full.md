---
title: 网鼎半决赛IoT-babyrtp
contest: 网鼎半决赛 IoT
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags:
- IoT-pwn
- rtp-stream
- ffmpeg
- AES-encrypted-jpg
- tshark-rtp-payload
- IPv4-validation
- HTTP-server-pwn
- IP-cam
- get-post
- AES-decrypt
attack_chain:
- binwalk提取固件,分析pwn文件(usr文件夹)
- 实现简单HTTP服务器:socket+bind(8080)+listen+accept+handle_request
- handle_request调extract_url提取url=参数内容
- extract_url检查"url="后内容是否为有效IPv4地址
- 有效URL:返回s(IPv4地址),继续走if逻辑
- 关键:push_stream使用rtp_aes_push for flag.jpg aes_key.bin [url] 5004
- 推流命令:while true; do ./rtp_aes_push flag.jpg aes_key.bin [url] 5004; sleep 5; done
- GET传参不能进入逻辑,改用POST传参
- Wireshark/tshark截获RTP流,rtp.payload提取密文
- AES解密(key=aes_key.bin)得flag.jpg
key_payload: AES(key=aes_key.bin).decrypt(rtp_payload)
one_liner: 网鼎半决赛IoT-babyrtp IoT固件RTP推流题,binwalk提取固件+HTTP server+url=参数IPv4验证+rtp_aes_push循环推流+Wireshark截RTP+AES解密flag.jpg。
lesson: IoT固件题要从bin开始,用binwalk提取文件系统;HTTP server常见url参数验证;rtp推流是IP camera常见协议,ffmpeg是核心库;AES加密的图片用tshark抓payload后解密。
quality: medium
full_path: 网鼎半决赛IoT-babyrtp.full.md
meta_path: 网鼎半决赛IoT-babyrtp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 网鼎半决赛IoT-babyrtp。网鼎半决赛IoT-babyrtp IoT固件RTP推流题,binwalk提取固件+HTTP server+url=参数IPv4验证+rtp_aes_push循环推流+Wireshark截RTP+AES解密flag.jpg。。关键路径：binwalk提取固件,分析pwn文件(usr文件夹) → 实现简单HTTP服务器:socket+bind(8080)+lis...
category: misc
subcategory: misc_other
tools_used:
- Wireshark
- tshark
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/218450.html
reasoning_chain:
- 触发点：bin 文件 → 假设：binwalk 提取固件 → 动作：binwalk -e
- 观察：usr 文件夹有 pwn 文件 → 下一步：分析 pwn 逻辑
- 动作：分析 handle_request → extract_url 检查 'url=' 后 IPv4 验证 → 假设：必须 IPv4 格式
- 动作：传 url=192.168.x.x 触发 push_stream → rtp_aes_push 推流
- 触发点：while true; do ./rtp_aes_push flag.jpg aes_key.bin %s 5004; sleep 5 → 假设：rtp_aes_push 用 AES 加密
- 动作：post 触发推流 → 观察：成功推送 RTP 流
- 动作：wireshark 截 RTP 流量 → tshark -Y rtp -T fields -e rtp.payload > out.txt
- 假设：AES key 已知道 → 动作：AES 解密 out.txt → 观察：得到 flag.jpg
failed_attempts:
- binwalk 不指定 -e → 失败：未解压
- GET url= 传 IPv4 → 失败：路由走错分支
- wireshark 不过滤 rtp → 失败：分包数据散乱
key_observations:
- binwalk 是 IoT 固件分析首选工具
- RTP 推流用 AES 加密时 key 通常与代码/配置一起给出
- tshark -e rtp.payload 提取 RTP 载荷是录制 RTP 标准命令
- extract_url IPv4 验证：url 参数必须是 IPv4 格式
prerequisites:
- binwalk 固件分析
- RTP/RTCP 协议
- wireshark/tshark RTP 解码
- AES 解密基础
---
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