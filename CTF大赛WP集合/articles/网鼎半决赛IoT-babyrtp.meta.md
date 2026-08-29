---
title: 网鼎半决赛IoT-babyrtp
contest: 网鼎半决赛 IoT
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [IoT-pwn, rtp-stream, ffmpeg, AES-encrypted-jpg, tshark-rtp-payload, IPv4-validation, HTTP-server-pwn, IP-cam, get-post, AES-decrypt]
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
---

## 题目列表

1道IoT:网鼎半决赛babyrtp

## 关键考点

### 固件分析
- binwalk提取固件
- 在usr文件夹发现服务端逻辑文件pwn

### HTTP server代码分析
- 实现简单HTTP服务器
  - socket()创建套接字
  - bind()绑定8080端口
  - listen()进入监听
  - accept()接受连接
  - handle_request()处理请求
- extract_url()提取url=参数,验证是否为IPv4地址
- 有效IPv4:返回s=url,继续if逻辑
- 无效:返回NULL

### rtp_aes_push
- 关键函数:rtp_aes_push for flag.jpg aes_key.bin [url] 5004
- 使用FFmpeg库进行RTP传输
- AES加密jpg文件后通过RTP流发送
- 推流命令:`while true; do ./rtp_aes_push flag.jpg aes_key.bin %s 5004; sleep 5; done`

### 攻击步骤
1. 准备服务端(伪造flag样例图)
2. 多次GET传参不成功,改POST传参
3. Wireshark/tshark截RTP传输流量
4. 对流量进行RTP解码
5. tshark提取rtp.payload:
   `tshark -r rtp.pcapng -Y rtp -T fields -e rtp.payload > out.txt`
6. AES解密(key=aes_key.bin)得flag.jpg

### 工具
- binwalk:固件提取
- Wireshark + tshark:流量分析
- FFmpeg:多媒体处理库(推流核心)
- Python + pycryptodome:AES解密

## 实战价值
- IoT固件题:binwalk+strings是入门基本功
- HTTP server常见url参数验证(IPv4检查)可绕
- RTP推流是IP camera/视频监控常见协议
- FFmpeg是多媒体处理库,推流核心
- Wireshark+tshark抓payload后用AES解密是RTP分析标准流程
