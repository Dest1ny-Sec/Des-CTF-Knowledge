---
title: 暗魂CTF平台-工控-协议分析-writeup
contest: 暗魂CTF
year: 2024
difficulty: easy
vuln_type: forensic_traffic
tags: [工控CTF, Modbus协议, S7comm协议, OMRON协议, Wireshark, TCP流, 字节交换]
attack_chain: modbus协议过滤追踪第一条http流→flag1=We1c0meToZXB2023→tcp流追踪16进制拼接→flag2=EnergyRevolution→s7comm.header.errcod !== 0x00过滤异常→OMRON omron.command==0x0102→每两字节swap_bytes交换位置解码flag3
key_payload: "wireshark filter modbus;s7comm.header.errcod !== 0x00;omron.command==0x0102;swap_bytes(每两字节交换)"
one_liner: 暗魂CTF工控协议分析三题：modbus+s7comm异常过滤+omron字节交换解码
lesson: 工控CTF核心Wireshark过滤器：modbus/s7comm/omron；OMRON密文常需每两字节swap
quality: medium
---

# 暗魂CTF平台-工控-协议分析-writeup

**赛事**：暗魂CTF平台（暗魂攻防实验室，2024）

**三题详解**：

**1. modbus协议（基础题）**
- 描述：黑客通过modbus向同伙发秘密信息
- 解：Wireshark过滤 `modbus`，追踪第一条HTTP流
- flag: `flag{We1c0meToZXB2023}`

**2. 异常的流量（TCP流16进制）**
- 描述：分析异常流量
- 解：Wireshark过滤 `tcp`，追踪第一个TCP流
- 选会话往下翻 → 一串16进制（3处拼接）
- 每个TCP流都会泄露部分16进制
- 拼接后解码
- flag: `flag{EnergyRevolution}`

**3. S7Error + OMRON协议（异常错误码过滤+字节交换）**
- S7comm：`s7comm.header.errcod !== 0x00` 过滤异常Ack_Data
- Ack_Data带返回数据，error code 0x00为正常
- 找出非0x00的错误包编号
- OMRON：`omron.command == 0x0102` 过滤
- 解密关键：每两字节交换位置
  ```python
  def swap_bytes(hex_str):
      result = []
      for i in range(0, len(hex_str), 4):
          byte1 = hex_str[i:i+2]
          byte2 = hex_str[i+2:i+4]
          result.append(byte2 + byte1)
      return ''.join(result)
  ```
- 输入hex: `396653344663722f3076556a3253662b30734d342b4843786b68427a794d64343749375275424563314d6b43637a4a79315575415833486e`
- swap后: `f94ScF/rv0jUS2+fs04MH+xChkzBMy4dI7R7BucEM1CkzcyJU1Au3XnH`
- 解码: `have fun:)`
- 第二段: `5ae1746f6473a56b35616531373436663634373361353662` → `a51e47f646375ab6`

**关键技术**：
- Wireshark过滤器：`modbus` / `s7comm.header.errcod !== 0x00` / `omron.command == 0x0102`
- TCP流追踪16进制拼接
- OMRON密文常需每两字节swap

**质量评估**：中（payload具体，flag完整，缺完整第三题完整flag）
