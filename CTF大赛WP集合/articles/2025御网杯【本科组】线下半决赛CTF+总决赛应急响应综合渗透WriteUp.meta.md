---
title: 2025 御网杯【本科组】线下半决赛 CTF+总决赛应急响应综合渗透 WriteUp
contest: 2025 御网杯
year: 2025
difficulty: easy
vuln_type: [stego_image, sqli, web_unknown, misc_math]
tags: [御网杯 2025 本科组 线下半决赛, USB 键盘流量 <DEL> 删除, 压缩包密码爆破 882401, exe 实际是压缩包改后缀解压, 全局搜索 flag+hex 解码 666c61677b, 工业流量分析 按时间排序 STOP, 0k4o rot13, Base32+Base64+Ascii85 混合解码 3 次, 工业控制 s7comm, IEC 60870-5 104]
attack_chain:
  - 键盘流量: iloveyou<DEL>...flag{}inKJ<DEL>...op97ya<DEL>...bc6g9 → 删 DEL 前内容 → flag{inop97bc6g9}
  - 压缩包密码爆破: 882401 解压 + 文档清除格式
  - exe 实际是压缩包: 16 进制头 50 4B 改后缀解压 → 流量包 → 全局搜 flag 编码 → 666c6167... → flag{DGswTfgy1GD236fs2sfF2dskLng}
  - 工业流量分析: 按时间排序，最先 STOP 的包 → flag{ac6417423bb3000c}
  - 0k4o 0k46 ... rot13 → Base32→Base64→Ascii85 → flag{hnctfqwer54321}
key_payload: "USB 键盘流量 <DEL> 8 次 = 8 个删除字符"
one_liner: 2025 御网杯本科组线下半决赛 Misc+Crypto 多题：USB 键盘流量+压缩包爆破+exe 改后缀+工业流量+rot13+Base 混合解码。
lesson: USB 键盘流量 `<DEL>` 是 Backspace 退格键，要计算删除字符数还原真实输入；exe 改后缀解压是流量包杂项最常见套路；Base32→Base64→Ascii85 混合解码是 CTF crypto 经典链。
quality: medium
---

# 2025 御网杯【本科组】线下半决赛 CTF+总决赛应急响应综合渗透 WriteUp

## Misc 4 题

### Q1 键盘流量

```
iloveyou<DEL><DEL><DEL><DEL><DEL><DEL><DEL><DEL>flag{}inKJ<DEL><DEL>op97ya<DEL><DEL>bc6g9
```

`<DEL>` 是 Backspace，每次删前一个字符。  
- `iloveyou` 后 8 个 `<DEL>` 删 8 个字符 → 留 `flag{}in`
- `KJ` 后 2 个 `<DEL>` 删 `KJ` → 留 `op97`
- `ya` 后 2 个 `<DEL>` 删 `ya` → 留 `bc6g9`

**flag{inop97bc6g9}**

### Q2 文件隐写 + 压缩包密码爆破

密码 `882401` → 解压后文档"清除格式"得 flag。
**flag{12axzaq1sz}**

### Q3 exe 实际是压缩包

exe 16 进制头 `50 4B 03 04` (PK ZIP) → 改后缀 `.zip` 解压出 pcapng 流量包。  
全局搜关键字 flag + 16 进制编码：
```
666c61677b44477377546667793147443233366673327366463264736b4c6e677d
```
hex 解：`flag{DGswTfgy1GD236fs2sfF2dskLng}`

### Q4 工业流量分析

按时间排序，最先 STOP 的包。  
**flag{ac6417423bb3000c}**

## Crypto 2 题

### Q1 0k4o rot13 + Base 混合

```
0k4o 0k46 0k4p 0k54 0k51 0k33 0k33 0k43 0k4o 0k35 ...
```

1. **rot13** 转换：把 `0k4o` 拆成 `0k` + `4o` → 字符 `o` 是字母，rot13 → `b`；4 是数字，保留。  
2. **Base32 解码** → bytes
3. **Base64 解码** → bytes
4. **Ascii85 解码** → 明文

**flag{hnctfqwer54321}**

### Q2 zip 内 CRC + 爆破
压缩包内多个文件 CRC 相同 → 字典攻击。
