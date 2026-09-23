---
title: 【工控Writeup】2022 河南工业互联网安全大赛复赛
contest: 河南工业互联网
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags:
- MMS-protocol
- modbus-ICS
- fileOpen-fileRead
- base64-image-flag
- hex-shift
- function-code-17-109-65-1-3-67
- 工业互联网
attack_chain: 1. MMS 流量过滤 fileOpen 操作 4 次拿标识符 /2. 找 fileRead 操作提取 base64 图片 /3. 异或/移位 666i5250... + 61673255... 偏移 6 /4. modbus 流量 function_code 序列 17,109,65,1,1,3,3,67 /5. 提取发送方 frame_id + func_code 找异常
key_payload: flag{ICS-mms104}  flag{RP2U5myhBI5m}  modbus function 17 109 65 1 1 3 3 67
one_liner: 2022 河南工业互联网安全大赛复赛 3 题 WP，MMS fileOpen 读图 + hex 移位爆破 + modbus 异常检测。
lesson: MMS (Manufacturing Message Specification) 是工业自动化协议；modbus function code 序列分析是工控异常检测；hex 移位爆破是常见编码。
quality: high
full_path: 【工控Writeup】2022河南工业互联网安全大赛复赛.full.md
meta_path: 【工控Writeup】2022河南工业互联网安全大赛复赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【工控Writeup】2022 河南工业互联网安全大赛复赛。2022 河南工业互联网安全大赛复赛 3 题 WP，MMS fileOpen 读图 + hex 移位爆破 + modbus 异常检测。。经验：MMS (Manufacturing Message Specification) 是工业自动化协议；modbus fu...
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/78419.html
reasoning_chain:
- 'pcap 流量过滤 mms → 触发点: 看到 fileOpen 操作 4 次'
- '假设: fileOpen 后会有 fileRead 拿数据 → 动作: 过滤 fileOpen 响应包拿标识符'
- '观察: 一包 wireshark 没解析 → 手动看下一包发现 base64 图片 → 还原 flag{ICS-mms104}'
- '题目二 mms item 字段出现 666i5250356j4249 → 假设: hex 字母被移位了'
- '动作: 遍历 1-16 偏移, 把字母按 ascii 减 → 观察: 偏移 6 时 ''flag''/''RP2U5'' 出来'
- '题目三 modbus func_code 17,109,65,1,1,3,3,67 循环 → 假设: 异常包就是偏离序列的帧'
- '动作: tshark 提取 ip.src==172.31.14.123 全部 func_code → 比对序列 → 1642 多 1 → 1648 改 1 → flag{1642+5485}'
failed_attempts:
- '题目二尝试偏移 4 → 失败: 不能让 i/j 移到 e/f 这种 hex 合法字符'
- '题目三先提交 flag{1642} 单值 → 失败: 必须配对偏移的发送+返回'
- '题目三只看 func_code → 失败: 后面发现异常其实在 modbus.data 内容层'
key_observations:
- MMS 协议的 fileOpen+fileRead 可被滥用成任意文件读取通道
- modbus function_code 序列异常检测 = 工控异常流量的经典指纹
- hex 字符串字母被 ascii 减移位是 ICS 流量混淆常见手法
- tshark 命令行比 GUI 稳, 多字段过滤用 -T fields -e
prerequisites:
- MMS / IEC 61850 工控协议基础 (fileOpen / fileRead)
- Modbus TCP 协议 (function_code + reference_num + data)
- tshark 命令行过滤语法
- Wireshark 协议解析失败时的手动十六进制排查
---
# 【工控Writeup】2022河南工业互联网安全大赛复赛

> 原文: https://www.ctfiot.com/78419.html
> ID: 78419

HNGK-流量分析

打开过滤mms，然后直接搜索flag发现有个列目录的返回结果。

再往下找有个fileOpen的操作。

继续往后找也是上面这俩个操作，那么就过滤一下fileOpen的操作去拿打开后的标识符然后看看用哪了。有4次打开操作。

那就过滤出这几个的返回包，拿到标识符。

不过有个返回包没解析出来，先不管，看看能不能用过滤出来的三个标识符找到其fileFead操作。

成功找到，那就看看这个请求的响应是什么。结果没过滤出来东西。

猜测是wireshark没解析成功，那就去掉过滤看看下一个包是什么，这个流量包里的请求和响应都是挨在一起的。

似乎是因为长度没解析对。反正看见base64格式的图片了，先提取出来。发现图片内容就是flag。

flag{ICS-mms104}

HNGK-MMS拿到流量包后发现打不开，扔到010发现其实是个压缩包，于是再解压一次。

遍历一遍mms，发现有两条请求的item比较奇怪。

而66正好是f的ascii。

所以猜测可能是有位移，但是十六进制的字母必然不可能有ij这种东西，所以猜测可能是先把字母往小移，但是不知道具体偏移是多少，那就一个一个试过去，然后移完之后解一下hex看看能出来啥。

先从偏移为4开始，因为至少要4才能让ij移到ef这种合理的hex。

import string
flag = bytearray(b"666i5250356j4249"b"616732557968356j")for i in range(len(flag)):    if flag[i] in string.ascii_lowercase.encode():        flag[i] -= 4print(flag)print(bytes.fromhex(flag.decode()))

但是好像没啥规律，继续尝试到偏移为6的时候发现fl和ag。

尝试将前后半段每两字节拼接，得到flagRP2U5myhBI5m，拼上括号提交发现正确。

flag{RP2U5myhBI5m}

HNGK-modbus

这题筛选modbus之后发现function是有规律循环的：17, 109, 65, 1, 1, 3, 3, 67。

于是尝试提取发送方所有的func_code和帧id，然后跑一轮看看有没有多了或者少了的。

tshark -r .modbus.pcap -Y "modbus && ip.src==172.31.14.123" -T fields -e "frame.number" -T fields -e "modbus.func_code" > data.txt

发现1648帧多了个1。

data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if i[1] != base[p % len(base)]:        print(i)    p += 1

过去看了下发现确实是多了个1，不过上下对比一下发现实际上多出来的是1642数据包，因为这个1541在其他地方没出现过。

而1642数据包在提取结果里是539条，直接忽略这条再跑一遍看看还有没有异常的。

data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if p == 539:        continue    if i[1] != base[p % len(base)]:        print(i)    p += 1

直接跑完没有异常。

尝试提交flag{1642}或者flag{1642+1643}但是都不对。

于是怀疑可能数据包异常点不是func而是其内容。

那么只能挨个func的数据筛选过去看看有没有异常了。

先把17给发送和返回过滤一遍：(modbus.func_code == 17) && !(!modbus.data) && !(modbus.data == 06:00:00)。

发现没有异常的，那就再看109的：((modbus.func_code == 109) && !(modbus.data == 54)) && !(modbus.data == 00)。

发现也没有，再看65的：((modbus.func_code == 65) && !(modbus.data == a8:b9:09:00:0c:01:06:02:06:03:06:04:06:05:06:06:06:07:06:00:06)) && !(modbus.data == 02:fe:00)。

还是没有，再看1的：((((modbus.func_code == 1) && !(modbus.reference_num == 0)) && !(modbus.reference_num == 1536)) && !(frame[63] == 00)) && !(frame[63] == fe)。

发现两对数据包有异常，比之前找的多了一对，所以实际上异常是多了一个和改了一个。

尝试提交flag{1642+5485}，发现正确。

flag{1642+5485}

HNGK-奇怪的工控协议

看了下协议分布，最主要的modbus，不过iec60870_104和iec60870_asdu也不算少。

在modbus里面翻了半天也没看到啥有用的东西，然后去iec60870_104翻了下直接发现了flag。

flag{sort__104}

点击在看，关注我们

END


```
import string
flag = bytearray(b"666i5250356j4249"b"616732557968356j")for i in range(len(flag)):    if flag[i] in string.ascii_lowercase.encode():        flag[i] -= 4print(flag)print(bytes.fromhex(flag.decode()))
tshark -r .modbus.pcap -Y "modbus && ip.src==172.31.14.123" -T fields -e "frame.number" -T fields -e "modbus.func_code" > data.txt
data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if i[1] != base[p % len(base)]:        print(i)    p += 1
data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if p == 539:        continue    if i[1] != base[p % len(base)]:        print(i)    p += 1
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