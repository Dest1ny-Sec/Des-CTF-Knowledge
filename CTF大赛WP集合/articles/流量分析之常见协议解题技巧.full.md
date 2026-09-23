---
title: 流量分析之常见协议解题技巧
contest: 流量分析专题
year: 2022
difficulty: easy
vuln_type: forensic_traffic
tags:
- Wireshark
- USB HID
- tshark
- 数据包筛选
- 关键字搜索
- 文件还原
- 流量分析
attack_chain: tshark提取USB capdata→normalKeys/shiftKeys字典映射→WIFI/工控/蓝牙协议分类
key_payload: tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt;normalKeys+shiftKeys字典;n[2:4]00跳过;n[0:2]==02大写
one_liner: CTF流量分析常见协议技巧：tshark提取+HID字典映射+WIFI/工控/蓝牙协议
lesson: USB HID键盘流量用normalKeys/shiftKeys字典映射；n[0:2]==02判定Shift
quality: medium
full_path: 流量分析之常见协议解题技巧.full.md
meta_path: 流量分析之常见协议解题技巧.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 流量分析之常见协议解题技巧。CTF流量分析常见协议技巧：tshark提取+HID字典映射+WIFI/工控/蓝牙协议。经验：USB HID键盘流量用normalKeys/shiftKeys字典映射；n[0:2]==02判定Shift
category: forensic
subcategory: network_forensics
tools_used:
- Wireshark
- tshark
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/86477.html
reasoning_chain:
- WP 列 7 节：题型简介/Wireshark 技巧/筛选/关键字/还原/文件提取/题型讲解 → 触发点：USB HID 流量是高频考点
- 动作：tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt → 提取 8 字节键盘数据
- 假设：第 0 字节是 modifier（02=Shift, 00=无），第 2 字节是 keycode → 观察：建立 normalKeys/shiftKeys 双字典
- 'normalKeys: 04=''a''..1d=''z'', 1e-27=''0-9'', 2c='' '', shiftKeys 对应大写'
- 动作：Python 循环 usbdata.txt → 跳过 n[2:4]=='00'（无按键）→ 映射 keycode→字符
- 观察：还原出 HID 键盘敲入字符串 → 题型：WIFI/工控协议/蓝牙协议
- 'WIFI: eapol 4 次握手 → 抓 WPA 握手 → aircrack-ng 跑字典'
- '工控: MMS/IEC61850/Modbus S7comm → tshark -Y 过滤字段 → 还原 SCADA 指令'
failed_attempts:
- 试图用 Wireshark GUI 复制 capdata → 失败：大量包手动复制不可能
- 试图硬编码 1-255 全 keycode 字典 → 失败：HID 0x00-0x03 是 modifier，不参与映射
- 试图不看 modifier 直接映射 → 失败：Shift 状态决定大小写
key_observations:
- USB HID 8 字节格式：byte0=modifier, byte1=reserved, byte2-7=keycode
- n[0:2]=='02' 表示 Shift 按下，对应 shiftKeys 字典
- n[2:4]=='00' 表示无按键，必须跳过
- WPA 4 次握手靠 eapol 帧识别 + aircrack-ng 跑字典
prerequisites:
- tshark 命令行使用（-r / -Y / -T fields / -e）
- USB HID 键盘协议（boot protocol）
- Wireshark 协议过滤语法
- Python 字符串处理（bytes + dict 映射）
---
# 流量分析之常见协议解题技巧

> 原文: https://www.ctfiot.com/86477.html
> ID: 86477

‍01

CTF 流量分析题型简介 ‍‍‍‍‍‍‍‍‍

02‍

wireshark 工具使用技巧

03‍

数据包筛选

04‍

关键字搜索‍‍‍‍‍‍‍‍‍‍

05‍

数据包还原‍‍‍‍‍‍‍‍‍

06‍

数据文件提取‍‍‍‍‍‍‍‍‍

07‍

相关题型讲解

# -*- coding: cp936 -*-
import os
os.system("tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt")
normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

nums = []
keys = open('usbdata.txt')
for line in keys:
    #print(line)
    if len(line)!=17: 
         continue
    nums.append(line[0:2]+line[4:6])
    #print(nums)
keys.close()
output = ""
for n in nums:
    if n[2:4] == "00" :
        continue

    if n[2:4] in normalKeys:
        if n[0:2]=="02": 
            output += shiftKeys [n[2:4]]
        else :
            output += normalKeys [n[2:4]]
    else:
        output += '[unknown]'
print('output :' + output)

08‍

WIFI 流量题目

09‍

工控协议流量题

10

蓝牙协议流量题目


```
# -*- coding: cp936 -*-
import os
os.system("tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt")
normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":""","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

nums = []
keys = open('usbdata.txt')
for line in keys:
    #print(line)
    if len(line)!=17: 
         continue
    nums.append(line[0:2]+line[4:6])
    #print(nums)
keys.close()
output = ""
for n in nums:
    if n[2:4] == "00" :
        continue

    if n[2:4] in normalKeys:
        if n[0:2]=="02": 
            output += shiftKeys [n[2:4]]
        else :
            output += normalKeys [n[2:4]]
    else:
        output += '[unknown]'
print('output :' + output)
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