---
title: 【2024御网杯】线下半决赛 Misc WriteUp
contest: 御网杯
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [0-width-stego, xlsx-zip-mislabel, PNG-file-append, pyc-Rot13-base64, RTMP-pcap-extract, tcpflow, ffmpeg-frames]
attack_chain: simple_analysis 0 宽度隐写 330k 在线工具秒解/kitty 附件 xlsx 实为 zip 包（50 4B 03 04 14 00）→解压得 kitty.xml 实为 PNG（89 50 4E 47）/aixin Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU 经 Rot13→Rot16→Base64→Reverse 多层解码/直播流量 pcapng 过滤 _ws.col.info == "Video Data" + tcpflow -T %T_%A%C%c.rtmp -r rtmp.pcapng 拆流 → rtmp2flv.py 转 flv → ffmpeg -vf "fps=1" frame%04d.png 抽帧
key_payload: Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU  ROT13 16 次 → base64 → reverse
one_liner: 御网杯 2024 高职组半决赛 4 题 Misc 复盘，0 宽隐写 + 文件套娃 + 多层编解码 + RTMP 抽帧。
lesson: 0 宽度 Unicode 隐写用 330k 工具秒解；xlsx/png/zip 等格式头互转是常见套娃；RTMP 流量过滤 Video Data 后用 tcpflow 抽 + rtmp2flv + ffmpeg 三步抽帧是经典工作流。
quality: medium
---

# 【2024御网杯】线下半决赛 Misc WriteUp

## 概览
2024 御网杯高职组线下半决赛（B12 抽签号）4 题 Misc 复盘。

## simple_analysis
- 题目看起来空白，但 Windows 11 记事本打开可见特殊字符
- 解法：0 宽度 Unicode 隐写，工具 https://330k.github.io/misc_tools/unicode_steganography.html 即可秒解
- 比赛环境下没网的话，可下载离线工具 https://gitcode.com/open-source-toolkit/fe9fb/overview

## kitty
- 附件 xlsx 打开报错，010 Editor 看文件头是 50 4B 03 04 14 00（ZIP）
- 解压得 kitty.xml，再 010 看发现是 PNG 头（89 50 4E 47）
- 改后缀为 .png，发现文件末尾有附加数据但 flag 已经直接显示
- 出题人可能是想考 ZIP 修复，但非预期直接文件附加

## aixin
- pyc 文件，但附件给的是字符串：`Mx12ItE2XjqgYEBDADA0WGEhXQI2W2I4JNIiWEJEA05So2nrlQIU`
- 解法：Rot13 → Rot16 → Base64 → Reverse 多层套娃解码
- 比赛时直接用"赛博厨子"在线工具解开，本地起个 http_server 也行

## 直播流量
- pcapng 文件，OBS 直播 RTMP 抓包
- 过滤 `_ws.col.info == "Video Data"`
- 提取：`tcpflow -T %T_%A%C%c.rtmp -r rtmp.pcapng`
  - `%T` 时间戳、`%A` 源地址、`%C` 目的端口、`%c` 会话号
- 转码：`./rtmp2flv.py *.rtmp` → `ffmpeg -i *.flv -vf "fps=1" frame%04d.png` 抽帧
- 在帧画面中找 flag

## 经验提炼
- 0 宽度 Unicode 隐写工具首推 330k
- xlsx/docx/jar 等 OOXML 格式本质是 ZIP，文件头 50 4B 03 04
- PNG/JPG/GIF 等图片格式可直接改后缀查看
- 字符串多编码套娃常见组合：Rot13+Base64+Reverse
- RTMP 流量分析三件套：wireshark 过滤 → tcpflow 抽流 → rtmp2flv 转码 → ffmpeg 抽帧
