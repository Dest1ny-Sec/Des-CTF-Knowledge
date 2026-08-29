---
title: Cyber Apocalypse 2023 硬件 CTF 题解
contest: Cyber Apocalypse 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [hardware, 逻辑分析仪, Gerber, UART, Verilog, hamming74, 数码管]
attack_chain:
  - Timed: 逻辑分析仪波形识别文字flag
  - Critical Flight: Gerber PCB viewer找隐藏字符串
  - Debug: UART波特率分析解码flag
  - HM74: Verilog 74汉明码纠错码统计分析
  - Secret-Code: 逻辑分析仪+Gerber通道映射还原数码管字符
  - hamming(7,4)码: p0,p1,p2校验+data_in3-0=4bit
key_payload: ham_out={p0,p1,data_in3,p2,data_in2,data_in1,data_in0}  # 7位
one_liner: 5道硬件题综合：波形图+Gerber+UART+Hamming+数码管逆向
lesson: 硬件CTF结合Verilog/逻辑分析仪/PCB viewer多工具
quality: high
---

# Cyber Apocalypse 2023 硬件 CTF 题解

## 题目信息
- 比赛：Cyber Apocalypse 2023
- 类别：硬件（Hardware）
- 涵盖：5 道硬件题

## 关键攻击链
### 1. Timed Transmission
- 逻辑分析仪波形图 → 文字组成 flag
- 示波器/逻辑分析仪截图识别高低电平持续时间

### 2. Critical Flight
- Gerber 文件（PCB 制造文件）
- viewer.digipcba.com / pcbway.com 渲染
- 找隐藏字符串拼接成 flag

### 3. Debug
- UART 串口通信波形
- 识别波特率（常见 9600/115200）
- 解码二进制 → ASCII

### 4. HM74（Hamming 7,4 码）
- Verilog 编码模块：
  ```verilog
  p0 = data_in[3] ^ data_in[2] ^ data_in[0]
  p1 = data_in[3] ^ data_in[1] ^ data_in[0]
  p2 = data_in[2] ^ data_in[1] ^ data_in[0]
  ham_out = {p0, p1, data_in[3], p2, data_in[2], data_in[1], data_in[0]}
  ```
- 输入 4 bit data，输出 7 bit（3 位校验 + 4 位数据）
- 解码时校验 p0/p1/p2 是否匹配，错误则纠错
- `bit_check()` 函数逐位检查

### 5. Secret-Code
- 逻辑分析仪记录 + Gerber PCB 文件
- 通道 ↔ 数码管段映射
- 还原数码管显示字符得 flag

## 评分
- quality: high（5 道硬件题工具齐全：Gerber viewer + 逻辑分析仪 + Verilog 仿真）
