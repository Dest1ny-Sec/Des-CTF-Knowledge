---
title: 流量分析之常见协议解题技巧
contest: 流量分析专题
year: 2022
difficulty: easy
vuln_type: forensic_traffic
tags: [Wireshark, USB HID, tshark, 数据包筛选, 关键字搜索, 文件还原, 流量分析]
attack_chain: tshark提取USB capdata→normalKeys/shiftKeys字典映射→WIFI/工控/蓝牙协议分类
key_payload: "tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt;normalKeys+shiftKeys字典;n[2:4]00跳过;n[0:2]==02大写"
one_liner: CTF流量分析常见协议技巧：tshark提取+HID字典映射+WIFI/工控/蓝牙协议
lesson: USB HID键盘流量用normalKeys/shiftKeys字典映射；n[0:2]==02判定Shift
quality: medium
---

# 流量分析之常见协议解题技巧

**主题**：CTF流量分析常见协议解题技巧

**核心内容**：
1. CTF流量分析题型简介
2. Wireshark工具使用技巧
3. 数据包筛选
4. 关键字搜索
5. 数据包还原
6. 数据文件提取
7. **USB HID键盘流量解析**（常用）
8. WIFI流量题目
9. 工控协议流量题
10. 蓝牙协议流量题

**USB HID解析Python脚本**：
```python
import os
os.system("tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt")
normalKeys = {
    "04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g",
    "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n",
    "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u",
    "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z", "1e":"1", "1f":"2",
    "20":"3", "21":"4", "22":"5", "23":"6", "24":"7", "25":"8", "26":"9",
    "27":"0", "28":"<RET>", "29":"<ESC>", "2a":"<DEL>", "2b":"t",
    "2c":"<SPACE>", "2d":"-", "2e":"=", "2f":"[", "30":"]", "31":"\\",
    "32":"<NON>", "33":";", "34":"'", "35":"<GA>", "36":",", "37":".",
    "38":"/", "39":"<CAP>"
    # ... F1-F12 keys
}

shiftKeys = {  # 大写版
    "04":"A", "05":"B", ... "2f":"{", "30":"}", "31":"|", "33":"\"", "34":":", "36":"<", "37":">", "38":"?"
}

nums = []
keys = open('usbdata.txt')
for line in keys:
    if len(line) != 17: continue
    nums.append(line[0:2] + line[4:6])
keys.close()

output = ""
for n in nums:
    if n[2:4] == "00": continue
    if n[2:4] in normalKeys:
        if n[0:2] == "02":
            output += shiftKeys[n[2:4]]  # Shift+字母
        else:
            output += normalKeys[n[2:4]]
    else:
        output += '[unknown]'
print('output :' + output)
```

**关键技术**：
- tshark提取capdata：`tshark -r test.pcapng -T fields -e usb.capdata`
- HID键盘长度17字节，第3字节=00跳过
- n[0:2]==02表示Shift按下，用shiftKeys
- WIFI/工控/蓝牙各有专用协议解析

**质量评估**：中（核心USB脚本完整，其他协议简略）
