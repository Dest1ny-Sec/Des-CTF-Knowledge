---
title: 【WP】第二届"红明谷"杯数据安全大赛题目解析（三）
contest: 红明谷
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [RTPS-protocol, RSA-AES-pcap, on-off-board-key, pycryptor, USB-keystroke, ROS-traffic, blind-stack-overflow, USB-hid-table]
attack_chain: 1. 神秘电波：Wireshark 过滤 RTPS 协议 + onboard/offboard key 切换 RSA 加密三元素 (n, e, c) + AES 解密 /2. 重要系统：tshark 提取 USB capdata + normalKeys/shiftKeys 字典映射 + <DEL> 处理还原 player:guest
key_payload: USB HID normalKeys/shiftKeys 0x04-0x1d 字典  RTPS onboard/offboard 切换
one_liner: 第二届红明谷杯题解（三），RTPS 协议 RSA/AES 流量分析 + USB 键盘流量盲打还原。
lesson: RTPS 协议是 ROS/DDS 中间件的实时通信协议；USB 键盘流量通过 HID Usage ID 0x04-0x1d 映射到字母；正常/Shift 键切换大小写和符号。
quality: high
---

# 【WP】第二届"红明谷"杯数据安全大赛题目解析（三）

## 概览
第二届红明谷杯数据安全大赛题解（第三部分），覆盖 RTPS 协议 + USB 键盘流量分析。

## 神秘电波

### 约法 X 章
1. RTPS 流量包分析
2. RSA 和 AES 解密

### 致知力行
- 打开流量包，大量 TLS 数据无有用信息
- WireShark 统计分析：充斥大量 RTPS 包
- 过滤 RTPS 协议封包
- 发现 onboard/offboard 切换：
  - `{"key": "ZG3a44ipuXxUQsMD", "mode": "offboard"}`
  - `{"key": "QM+LQwfNhRIHXKkS", "mode": "onboard"}`
  - onboard 时给 RSA 三元组 (n, e, c)

### 附件源码
- `XXXX_enc.py`: 使用 pycryptor 加密，密码 (nJ3Ypqh61zkDxYHV) 隐藏在流量包中
- 需要提取所有 Onboard 状态的 Key 进行爆破
- `XXXX_decode.py`: 强混淆但从函数名可知使用 RSA 加密

## 重要系统

### 约法 X 章
1. USB 和 ROS 流量分析
2. 攻击流量分析
3. 栈溢出流量盲打

### 致知力行
```bash
tshark -r important.pcap -T fields -e usb.capdata > importantUSB.txt
```

### USB HID 键盘映射
```python
normalKeys = {
    "04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g",
    "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n",
    "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u",
    "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z",
    "1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6",
    "24":"7","25":"8","26":"9","27":"0",
    "28":"<RET>","29":"<ESC>","2a":"<DEL>","2b":"t","2c":"<SPACE>",
    "2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>",
    "33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>",
    "3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>",
    "40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"
}

shiftKeys = {
    "04":"A", ..., "1d":"Z",
    "1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^",
    "24":"&","25":"*","26":"(","27":")",
    ...
}
```

### 还原脚本
```python
output = []
keys = open('importantUSB.txt','r')
for line in keys:
    try:
        for i in range(0, len(line) + len(line)/2, 3):
            line = line[:i+2] + ':' + line[i+2:]
        if line[0]!='0' or (line[1]!='0' and line[1]!='2') or ...:
            continue
        if line[6:8] in normalKeys.keys():
            output += [[normalKeys[line[6:8]]], [shiftKeys[line[6:8]]]][line[1]=='2']
    except:
        pass
keys.close()
```

### 处理 <DEL> 删除
```python
for i in range(len(output)):
    try:
        a = output.index('<DEL>')
        del output[a]
        del output[a-1]
    except:
        break
```

## 经验提炼
- RTPS 协议是 ROS/DDS 中间件的实时通信协议
- USB 键盘流量通过 HID Usage ID 0x04-0x1d 映射到字母
- 正常/Shift 键切换大小写和符号（line[1] == '2' 表示 Shift）
- pycryptor 是 Python 字节码加密工具，密钥可爆破
- onboard/offboard 是车辆远程控制模式切换术语
- Wireshark 统计功能可快速识别协议组成
- USB HID Usage ID 是 USB 标准化的键盘码
- <DEL> 处理要同时删除按键和前一个字符
- tshark `-T fields -e usb.capdata` 是 USB 数据提取标准命令
