---
title: 暗魂CTF平台-工控-协议分析-writeup
contest: 暗魂CTF
year: 2024
difficulty: easy
vuln_type: forensic_traffic
tags:
- 工控CTF
- Modbus协议
- S7comm协议
- OMRON协议
- Wireshark
- TCP流
- 字节交换
attack_chain: modbus协议过滤追踪第一条http流→flag1=We1c0meToZXB2023→tcp流追踪16进制拼接→flag2=EnergyRevolution→s7comm.header.errcod !== 0x00过滤异常→OMRON omron.command==0x0102→每两字节swap_bytes交换位置解码flag3
key_payload: wireshark filter modbus;s7comm.header.errcod !== 0x00;omron.command==0x0102;swap_bytes(每两字节交换)
one_liner: 暗魂CTF工控协议分析三题：modbus+s7comm异常过滤+omron字节交换解码
lesson: 工控CTF核心Wireshark过滤器：modbus/s7comm/omron；OMRON密文常需每两字节swap
quality: medium
full_path: 暗魂CTF平台-工控-协议分析-writeup.full.md
meta_path: 暗魂CTF平台-工控-协议分析-writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 暗魂CTF平台-工控-协议分析-writeup。暗魂CTF工控协议分析三题：modbus+s7comm异常过滤+omron字节交换解码。经验：工控CTF核心Wireshark过滤器：modbus/s7comm/omron；OMRON密文常需每两字节swap
category: forensic
subcategory: network_forensics
tools_used:
- Wireshark
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/198479.html
reasoning_chain:
- modbus 题：黑客通过 modbus 协议向同伙发秘密信息 → 触发点：modbus 协议过滤
- 动作：wireshark filter 'modbus' → 追踪第一条 http 流 → 观察：flag{We1c0meToZXB2023}
- 异常流量题：描述说找异常 → 触发点：tcp 流追踪
- 动作：filter 'tcp' → 追踪第一个 tcp 流 → 假设：会话里有拼接的 16 进制
- 观察：每个流都泄露一段 hex → 动作：3 处 hex 拼接 + 解码 → flag{EnergyRevolution}
- S7Error 题：西门子设备资源异常 → 触发点：s7comm 协议
- 假设：Ack_Data Header 中 errcod=0x00 是正常 → 动作：filter 's7comm.header.errcod !== 0x00'
- 观察：异常包 → 下一步：OMRON 题
- OMRON 题：filter 'omron.command == 0x0102' → 触发点：每两字节 swap_bytes 交换位置
- 动作：swap_bytes(hex_str) 写 Python 函数 → 输出 f94ScF/rv0jUS2+fs04MH+xChkzBMy4dI7R7BucEM1CkzcyJU1Au3XnHhave fun:)
- 再次 swap → a51e47f646375ab6 → 完成
failed_attempts:
- OMRON 直接读 hex 字符串不解码 → 失败：必须每两字节 swap
- s7comm 全过滤 → 失败：必须过滤 errcod !== 0x00 的异常包
key_observations:
- 工控 CTF 三大协议 filter：modbus / s7comm / omron
- S7comm Ack_Data 异常过滤用 s7comm.header.errcod !== 0x00
- OMRON 密文常需每两字节 swap_bytes 解码
- 工控流量题大多先 Wireshark 过滤再 TCP 流追踪
prerequisites:
- Modbus / S7comm / OMRON 工控协议基础
- Wireshark 显示过滤器 + TCP 流追踪
- 16 进制拼接与解码
- 字节交换（swap_bytes）函数编写
---
# 暗魂CTF平台-工控-协议分析-writeup

> 原文: https://www.ctfiot.com/198479.html
> ID: 198479

点击蓝字

关注我们

微信搜一搜

暗魂攻防实验室

协议分析

modbus

描述：

黑客通过modbus协议向他的同伙发送了一条秘密信息，通过流量设备我们抓取到了相关的流量包，你能根据流量包找到这条信息么?

exp:

过滤一下 modbus ，追踪第一条数据的 http 流，就能发现 flag

flag为：flag{We1c0meToZXB2023}

异常的流量

描述：

请对提供的流量进行分析，发现可能存在的异常，找出flag，提交格式：flag{xxx}。

exp：

在过滤器中过滤一下 tcp ，追踪一下第一个 tcp 流，选择一下会话往下翻就能发现一串 16 进制，一共有 3 处拼接起来就行，然后我看了一下，我基本每个 tcp 流都会泄露这个串 16 进制，然后进行解码，用 flag{} 包裹就行

flag： flag{EnergyRevolution}

S7Error

描述：

某工厂的工程师发现有一台西门子设备存在资源异常，请分析并找出异常流量的数据包编号。

exp：

过滤器过滤 s7comm，大概了解一下 s7comm 协议，分析 Header 部分，可以看到 Ack_Data 的 Header 中大部分 Error code 是 0x00，说明这种流应该是没有异常的，那我过滤一下不等于 0x00 就行了

Ack_Data：带有返回数据，例如指令是查询内容，返回的就有要查询的东西

s7comm.header.errcod !== 0x00

[工控CTF之协议分析7——OMRON_omron协议-CSDN博客](https://blog.csdn.net/song123sh/article/details/128388409)

omron.command == 0x0102

9fS4Fcr/0vUj2Sf+0sM4+HCxkhBzyMd47I7RuBEc1MkCczJy1UuAX3Hnahevf nu):

def swap_bytes(hex_str): result = []for i inrange(0, len(hex_str), 4): byte1 = hex_str[i:i+2] byte2 = hex_str[i+2:i+4] result.append(byte2 + byte1)return''.join(result)
input_hex ="396653344663722f3076556a3253662b30734d342b4843786b68427a794d64343749375275424563314d6b43637a4a79315575415833486e"output_hex = swap_bytes(input_hex)print(output_hex)
f94ScF/rv0jUS2+fs04MH+xChkzBMy4dI7R7BucEM1CkzcyJU1Au3XnHhave fun:)

5ae1746f6473a56b35616531373436663634373361353662
跟上面一样每两个字节交换一次位置
a51e47f646375ab6

联系微信客服

扫码联系

暗魂攻防实验室

微信搜一搜

暗魂攻防实验室


```
s7comm.header.errcod !== 0x00
[工控CTF之协议分析7——OMRON_omron协议-CSDN博客](https://blog.csdn.net/song123sh/article/details/128388409)
omron.command == 0x0102
9fS4Fcr/0vUj2Sf+0sM4+HCxkhBzyMd47I7RuBEc1MkCczJy1UuAX3Hnahevf nu):
def swap_bytes(hex_str): result = []for i inrange(0, len(hex_str), 4): byte1 = hex_str[i:i+2] byte2 = hex_str[i+2:i+4] result.append(byte2 + byte1)return''.join(result)
input_hex ="396653344663722f3076556a3253662b30734d342b4843786b68427a794d64343749375275424563314d6b43637a4a79315575415833486e"output_hex = swap_bytes(input_hex)print(output_hex)
f94ScF/rv0jUS2+fs04MH+xChkzBMy4dI7R7BucEM1CkzcyJU1Au3XnHhave fun:)
5ae1746f6473a56b35616531373436663634373361353662
跟上面一样每两个字节交换一次位置
a51e47f646375ab6
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