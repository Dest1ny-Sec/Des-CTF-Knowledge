---
title: 2021年工业信息安全技能大赛线上第一场 WriteUp
contest: 工业信息安全技能大赛
year: 2021
difficulty: easy
vuln_type: misc_unknown
tags: [ICS, 梯形图, AutoThink, Fins协议, OPC, VMDK取证, AES, 3DES, 反调试]
attack_chain:
  - 用 AutoThink 打开梯形图程序还原逻辑
  - 改 EAX 绕过 crackme 反调试
  - 用 OPC/Fins 协议字段定位工控流量关键包
  - 重组 vmdk+flat.vmdk 拿 NTFS 镜像做取证
  - 从 mp4.mp4 提取十六进制字符串连环解码
  - 跑 AES-16 轮拿到硬编码 key 的预期输入
  - 用 3DES 解密 Fins 协议 U2FsdGVkX1 密文
key_payload: '3DES密文: U2FsdGVkX1/bWSZYUeFDeonQhK0AUHr9Tm7Ic20PRXxlPvlwG6a4fQ=='
one_liner: 工控+取证综合 7 题，AutoThink/Fins/OPC/VMDK/AES/3DES 一锅炖。
lesson: 工业流量重在协议字段定位（OPC/Fins 主机名/数据点），取证重在 vmdk 配对。
quality: low
---

# 2021年工业信息安全技能大赛线上第一场 WriteUp

## 来源
- 原文：ctfiot.com/1685.html
- 作者：ctfiot 编辑
- 收录：ChaMd5 Venom 系列

## 题目列表
1. **简单的梯形图** - 和利时 AutoThink V3.1.5B3 打开 PLC 梯形图
2. **损坏的风机** - 工控风机故障分析
3. **工控现场里异常的文件** - 取证定位异常
4. **隐藏的工程** - kingview 6.55 工程文件提取（密码 ICS，蓝凑云）
5. **OPC 协议分析** - 11(主机名 ABC) → 21(主机名 BCD) 流量分析
6. **工控安全异常取证分析** - 1122(flat.vmdk) + 112233(vmdk) → NTFS
7. **恶意文件分析** - crackme 无壳，CRC32 + uTPLb_AES.pas 硬编码 key
8. **Fins 协议通讯** - 11683 号包 U2FsdGVkX1/... 3DES 解密

## 关键技巧
- **VMDK 配对**：必须 `-flat.vmdk`(数据) + `.vmdk`(描述) 同时提供，缺一 DiskGenius 打不开
- **AES 16 轮预期输入**：crackme 函数循环 16 次后 ECX 值即正确输入，拼起来 `22d72a581f3a61e61e5b127e47ad8c0c`
- **反调试绕过**：调试器断点后改 EAX 寄存器跳过 PEB.BeingDebugged 检测
- **连环编码**：HEX→HEX→B32→B32→B32→B64→B64→HEX→B32→B64→B64 串糖葫芦

## 适用场景
- 工控协议（OPC/Fins）入门
- VMDK 磁盘取证初探
- AES/3DES 简单 CTF 密码题
