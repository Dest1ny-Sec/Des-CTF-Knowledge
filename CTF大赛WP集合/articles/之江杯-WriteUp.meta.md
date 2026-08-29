---
title: 之江杯-WriteUp
contest: 之江杯 / ChaMd5 Venom
year: 2024
difficulty: easy
vuln_type: forensic_memory
tags: [S7Comm, 工控, 梯形图, 内存取证, IC卡, Modbus, 360解密, 注册表分析, 招新广告]
attack_chain:
  - S7Comm 攻击协议: 直接分析 pcap 过滤 S7Comm
  - 梯形图 2: 力控/西门子工具打开
  - 内存取证: notepad 进程打开 flag.txt + flag.rar (密码)
  - 提取 rar 用 string 找密码或 ARCHPR
  - IC 卡: 4 字节一组，前 2 字节数据 + 后 2 字节 XOR 校验
  - 比如 0x7896 0x0000 → 0x78 'x' + 0x96
  - 上位机通讯: 异常的工程文件 (modbus tcp.stream eq 1)
  - 病毒文件 360 在线解密: lesuobingdu.360.cn
  - 注册表分析: 找 Run 键值后门
  - 多题均为字符串提取 + 工具加载 + 简单编码
key_payload: 'flag{18ghT1wr3} + 666c61677b...313878...317772337d'
one_liner: 之江杯工控多题 writeup，覆盖 S7Comm/Modbus/IC 卡/内存取证/注册表，最后招新广告。
lesson: 工控 CTF 偏工具流 (力控/西门子博图/Wireshark/Volatility/ARCHPR/lesuobingdu.360.cn)，IC 卡 4 字节分组 + XOR 校验是金融卡基础编码。
quality: low
---

# 之江杯-WriteUp

## 概览
- **来源**: ctfiot 269337
- **赛事**: 之江杯 / ChaMd5 Venom 战队
- **难度**: ⭐⭐ (多题流，招新广告结尾)

## 题目列表
1. **S7Comm 攻击协议分析** - pcap 过滤 S7Comm
2. **梯形图 2** - 力控/西门子工具加载
3. **内存取证** - notepad 进程打开 flag.txt + flag.rar
4. **字符串提取** - strings file 找 flag
5. **IC 卡分析** - 4 字节分组 + 2 字节数据 + 2 字节 XOR 校验
6. **上位机通讯异常** - pcap 字符串扫图片
7. **梯形图 1** - 力控加载
8. **工控组态分析** - 力控直接加载
9. **Modbus 协议** - `tcp.stream eq 1` + hex 提取
10. **注册表分析** - 找 Run 启动项
11. **工控恶意扫描** - pcap 分析
12. **Modbus 简单分析** - 字符串 + 协议
13. **病毒文件恢复** - 360 在线解密
14. **异常工程文件** - 提取 flag

## IC 卡核心编码
```python
# 4 字节一组：前 2 字节数据 + 后 2 字节 XOR 校验
data_groups = [
    b'\x7B\x00\x00\x00',  # 0x7b = '{'
    b'\xA6\xFF\xFF\xFF',  # 0xa6^0xff = 0x59
    b'\x30\x00\x00\x00',  # 0x30 = '0'
    ...
]
flag = b''
for g in data_groups:
    if g[2:] == b'\x00\x00':
        flag += bytes([g[0]])  # 直接取值
    else:
        flag += bytes([g[0] ^ 0xff])  # XOR
```

## Modbus 解码
```
tcp.stream eq 1
317772337d → 1wr3}
666c61677b → flag{
3138676854 → 18ghT
```

## 结尾招新
- ChaMd5 Venom 长期招新 (IOT + 工控 + 样本分析)
- 联系 admin@chamd5.org

## 教学意义
- 招新广告型 WP，仅作目录索引
