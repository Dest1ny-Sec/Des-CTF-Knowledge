---
title: 【工控Writeup】2022 河南工业互联网安全大赛复赛
contest: 河南工业互联网
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [MMS-protocol, modbus-ICS, fileOpen-fileRead, base64-image-flag, hex-shift, function-code-17-109-65-1-3-67, 工业互联网]
attack_chain: 1. MMS 流量过滤 fileOpen 操作 4 次拿标识符 /2. 找 fileRead 操作提取 base64 图片 /3. 异或/移位 666i5250... + 61673255... 偏移 6 /4. modbus 流量 function_code 序列 17,109,65,1,1,3,3,67 /5. 提取发送方 frame_id + func_code 找异常
key_payload: flag{ICS-mms104}  flag{RP2U5myhBI5m}  modbus function 17 109 65 1 1 3 3 67
one_liner: 2022 河南工业互联网安全大赛复赛 3 题 WP，MMS fileOpen 读图 + hex 移位爆破 + modbus 异常检测。
lesson: MMS (Manufacturing Message Specification) 是工业自动化协议；modbus function code 序列分析是工控异常检测；hex 移位爆破是常见编码。
quality: high
---

# 【工控Writeup】2022 河南工业互联网安全大赛复赛

## 概览
2022 河南工业互联网安全大赛复赛 3 题 WP，MMS + modbus 流量分析。

## HNGK-流量分析
- 过滤 mms
- 找 flag 字符串
- 找 fileOpen 操作
- 4 次打开操作拿标识符
- 找 fileRead 请求
- base64 提取图片
- flag: **`flag{ICS-mms104}`**

## HNGK-MMS
- 流量包打不开，扔 010 发现是压缩包
- 遍历 mms 找异常请求 item
- 异或/移位爆破 hex 字符串

### 爆破脚本
```python
import string
flag = bytearray(b"666i5250356j4249" b"616732557968356j")
for i in range(len(flag)):
    if flag[i] in string.ascii_lowercase.encode():
        flag[i] -= 4
print(flag)
print(bytes.fromhex(flag.decode()))
```

- 偏移 4 无规律，偏移 6 出 fl+ag
- 拼接 `flagRP2U5myhBI5m` 得 **`flag{RP2U5myhBI5m}`**

## HNGK-modbus
- 过滤 modbus
- function_code 序列: `17, 109, 65, 1, 1, 3, 3, 67` 有规律循环
- 提取发送方所有 func_code + frame_id
- 找异常/缺失

## 经验提炼
- MMS (Manufacturing Message Specification) 是工业自动化协议
- modbus function code 序列分析是工控异常检测
- hex 移位爆破是常见编码
- MMS fileOpen / fileRead 是文件操作服务
- 4 次 fileOpen 拿 fileHandle 标识符
- 工业互联网 = 工业 + 互联网 = ICS + IT
- base64 图片可能含 flag
- 偏移爆破：从 4 开始试，找 fl+ag
- 河南工业互联网 = 河南省工信厅主办
- modbus function code 1=读线圈 3=读保持寄存器
