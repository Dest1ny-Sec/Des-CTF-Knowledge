---
title: 数据安全大赛 2024 数信杯 东部赛区
contest: 数据安全大赛
year: 2024
difficulty: medium
vuln_type:
- fmt_string
- pwn_unknown
- stego_image
- block_cipher
- stream_cipher
tags:
- 非栈上格式化字符串
- RBP 多级指针改返回地址
- %hn 写 short
- one_gadget
- base64 循环移位
- RC4 + XOR 双加密
- ftp 流量 STOR 计数
- Arnold 变换
- 套娃编码 Base64+Base32+hex
attack_chain:
- 题 1 非栈 fmt string：%11$p%13$p 泄 libc_start_main + 栈地址，%hn 写 short 分 2 次改 ret_addr 为 one_gadget
- 题 2 base64+循环移位：data[i] = (data[i]<<5)|(data[i]>>3) 然后 base64 解码
- 题 3 RC4+XOR：先 XOR k2 再 RC4(k1) 解密（key 动调可得）
- 数据分析 1：ftp 流量找 admin/admin123 登录，统计 STOR=101 → md5("101+key")
- 数据分析 2：分析 4 个表关联找越权访问 → md5 拼接
- 数据分析 3：搜 admin/admin@QWEzxc 密码 → md5
- 数据分析 5：SQL 注入流量 + shell.php 木马连接密码
- 套娃：100 张 PNG 拼图 + Arnold 变换还原二维码 + LSB 提取 + Base64+Base32+hex 三层编码
key_payload: "payload = \"%{}c%13$hn\".format(write_in - num_len + 5); payload2 = \"%{}c%39$hn\".format((one_gadget & 0xffff))"
one_liner: 8 道题合集：非栈 fmt string / base64 循环移位 / RC4+XOR / ftp STOR 计数 / SQL 流量 / 套娃编码 + Arnold
lesson: 非栈 fmt string 需 RBP 多级指针改 ret_addr；%hn 写 short 分多次绕过限制；流量取证要按"协议→认证→操作→数据"4 步定位
quality: high
---

# 数据安全大赛 2024 数信杯 东部赛区

**8 道题合集：非栈 fmt string + base64 循环移位 + RC4+XOR + ftp/STOR/SQL 流量 + Arnold 套娃**

> 数据安全大赛 · 2024 · medium · fmt_string/pwn/stego_image/cipher · quality=high
> 思路: 非栈 fmt string RBP 多级指针改 ret_addr → base64+循环移位 → RC4+XOR 双加密 → ftp 找认证+STOR 计数 → SQL 流量 → 100 PNG 拼图+Arnold 还原+LSB+3 层编码
> 套路: 非栈 fmt string 需 RBP 多级指针改 ret_addr；%hn 写 short 分多次绕过限制；流量取证要按"协议→认证→操作→数据"4 步定位

**关键 payload**:
```python
payload = "%{}c%13$hn".format(write_in - num_len + 5)
payload2 = "%{}c%39$hn".format((one_gadget & 0xffff))
```
