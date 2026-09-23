---
title: 【2024御网杯】线下半决赛 Misc WriteUp
contest: 御网杯
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags:
- 0-width-stego
- xlsx-zip-mislabel
- PNG-file-append
- pyc-Rot13-base64
- RTMP-pcap-extract
- tcpflow
- ffmpeg-frames
attack_chain: simple_analysis 0 宽度隐写 330k 在线工具秒解/kitty 附件 xlsx 实为 zip 包（50 4B 03 04 14 00）→解压得 kitty.xml 实为 PNG（89 50 4E 47）/aixin Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU 经 Rot13→Rot16→Base64→Reverse 多层解码/直播流量 pcapng 过滤 _ws.col.info == "Video Data" + tcpflow -T %T_%A%C%c.rtmp -r rtmp.pcapng 拆流 → rtmp2flv.py 转 flv → ffmpeg -vf "fps=1" frame%04d.png 抽帧
key_payload: Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU  ROT13 16 次 → base64 → reverse
one_liner: 御网杯 2024 高职组半决赛 4 题 Misc 复盘，0 宽隐写 + 文件套娃 + 多层编解码 + RTMP 抽帧。
lesson: 0 宽度 Unicode 隐写用 330k 工具秒解；xlsx/png/zip 等格式头互转是常见套娃；RTMP 流量过滤 Video Data 后用 tcpflow 抽 + rtmp2flv + ffmpeg 三步抽帧是经典工作流。
quality: medium
full_path: 【2024御网杯】线下半决赛Misc_WriteUp.full.md
meta_path: 【2024御网杯】线下半决赛Misc_WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【2024御网杯】线下半决赛 Misc WriteUp。御网杯 2024 高职组半决赛 4 题 Misc 复盘，0 宽隐写 + 文件套娃 + 多层编解码 + RTMP 抽帧。。经验：0 宽度 Unicode 隐写用 330k 工具秒解；xlsx/png/zip 等格式头互转是常见套娃；RTMP 流量过...
category: misc
subcategory: misc_other
tools_used:
- C
- Python
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/212477.html
reasoning_chain:
- Q1 simple_analysis：Windows 11 记事本打开看特殊字符 → 触发点：0 宽度 Unicode 隐写
- 动作：打开 330k.github.io/misc_tools/unicode_steganography.html → 观察：在线解出 flag
- Q2 kitty：xlsx 附件打开报错 → 010 Editor 看头 50 4B 03 04 14 00 → 触发点：xlsx 实为 zip 包
- 动作：解压得 kitty.xml，但 kitty.xml 头 89 50 4E 47 是 PNG → 观察：套娃（zip 套 PNG）
- Q3 aixin：Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU → 触发点：pyc 反编译非预期更快
- 动作：ROT13 16 次 → Base64 → Reverse 多层解码 → 观察：解出 flag
- Q4 直播流量：pcapng 过滤 _ws.col.info == "Video Data" → 触发点：RTMP Video Data 流
- 动作：tcpflow -T %T_%A%C%c.rtmp -r rtmp.pcapng 拆流 → rtmp2flv.py 转 flv → ffmpeg -vf "fps=1" frame%04d.png 抽帧 → 完成
failed_attempts:
- Q2 试图直接解 kitty.xml → 失败：套娃多层
- Q3 试图用 PyInstaller 反编译 → 失败：非预期更快（ROT13×16+Base64+Reverse）
- Q4 试图用 Wireshark 抽帧 → 失败：tcpflow + rtmp2flv + ffmpeg 三步更稳
key_observations:
- 0 宽度 Unicode 隐写用 330k 工具秒解
- xlsx/png/zip 等格式头互转是常见套娃
- RTMP 流量过滤 Video Data 后用 tcpflow 抽 + rtmp2flv + ffmpeg 三步抽帧是经典工作流
- 多层编码（ROT13/Base64/Reverse）是 pyc 套题的标配
prerequisites:
- 330k Unicode 隐写工具使用
- 010 Editor 看文件头
- ROT13/Base64/Reverse 多次解码
- tcpflow / rtmp2flv / ffmpeg 命令行工具
---
# 【2024御网杯】线下半决赛Misc WriteUp

> 原文: https://www.ctfiot.com/212477.html
> ID: 212477

前言

本文章编写为2024御网杯高职组线下半决赛WriteUp，线下半决赛抽签号为B12，一点之前一直是第一，赛后听到很多大佬说没工具，大部分自己都是线上的工具，线下没网。但是，线下也有相应的解法，问题不大。

Misc

simple_analysis

这道题看上去好像什么都没有，但是其实在Windows 11的记事本打开会看到特殊字符：

直接0宽度隐写秒了，签到题难度。工具地址：https://330k.github.io/misc_tools/unicode_steganography.html

❝

但是此时问题出现了，我们常用的0宽都是线上在线使用的，怎么办呢？

您看这是什么呢？https://gitcode.com/open-source-toolkit/fe9fb/overview

kitty

附件是一个xlsx文件

但是打开提示报错

我们尝试使用010 Editor看看

发现是压缩包，文件头为我们熟悉的50 4B 03 04 14 00

继续解压，得到了kitty.xml

为了避免上当受骗，我们还是来看下010

果然，小骗子！！

从文件头看出来，这是一个PNG文件

但是文件末尾有一个文件附加，但是文件头不太对。这里肯定不是50 4B 03 04 14 00，虽然flag已经出来了，但是如果是作为这道题的出题人，这题其实应该算是非预期解了。

先改个后缀名吧

感觉这里应该是直接文件附加了

但是50 4B 03 04后面就直接是0000了，所以我觉得这里应该是考察ZIP修复的，但是没想到flag就直接在后面摆着。

aixin

一个pyc文件，比赛过程中我看我前面还有侧边的小兄弟们都在费劲巴拉的去用Pyinstaller啥的去反编译pyc。

但是我想说的是，，预期解虽然是这样，，但是有没有可能，，非预期解更快啊？

Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU

你猜猜这是什么呢？

非预期秒了，没难度。

ROT13改16，Base64，Reverse，纯套题。

什么？你跟我说你本地没有赛博厨子？？👩🏻‍🍳要不开心了！这玩意就是个开源的，你本地开个http_server都能给打开。

直播流量

我记得这是哪里的原题来着

OBS流量信息

过滤所有Video data

_ws.col.info == "Video Data"

导出特定数据

tcpflow -T %T_%A%C%c.rtmp -r rtmp.pcapng

❝

这里%T_%A%C%c.rtmp可不是乱起名字，是因为

%T：表示时间戳（timestamp），通常是捕获的时间。

%A：表示源地址（source address）。

%C：表示目的地址（destination address）的端口号（如果适用）。

%c：表示会话编号（session number），用于区分同一时间内的不同会话。

.rtmp：是文件扩展名，表示输出文件是RTMP流。


```
Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU
_ws.col.info == "Video Data"
tcpflow -T %T_%A%C%c.rtmp -r rtmp.pcapng
./rtmp2flv.py *.rtmp
ffmpeg -i *.flv -vf "fps=1" frame%04d.png
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