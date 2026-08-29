---
title: Cyberdefenders 蓝队-恶意软件流量分析 2
contest: Cyberdefenders 蓝队
year: 2022
difficulty: easy
vuln_type: forensic_memory
tags: [wireshark过滤, _path字段, sort_duration, 蓝队流量分析, malware, packet_total]
attack_chain:
  - wireshark 过滤 http && ip.src==37.143.15.180 && ip.dst==172.16.165.132 && tcp.srcport==51439 && tcp.dstport==49398
  - _path=="files" | sort -r duration 找最长时间传输
  - _path=="http" f.txt 过滤 http 流量
  - _path=="ssl" 看 SSL 流量
  - packettotal.com 病毒分析
key_payload: 'ip.src==37.143.15.180, ip.dst==172.16.165.132'
one_liner: 蓝队恶意软件流量分析入门：wireshark _path 过滤 + sort + packettotal。
lesson: _path 字段过滤比 ip/port 灵活；最长 duration 文件最可疑；packettotal 是免费样本分析平台。
quality: low
---

# Cyberdefenders 蓝队-恶意软件流量分析 2

## 来源
- 原文：ctfiot.com/84130.html
- 平台：Cyberdefenders 蓝队 CTF

## 关键 Wireshark 过滤语法
```bash
# 1. 源 IP 到目标 IP 的 HTTP 流量
http && ip.src==37.143.15.180 && ip.dst==172.16.165.132 && tcp.srcport==51439 && tcp.dstport==49398

# 2. 按 duration 排序找最长时间传输
_path=="files" | sort -r duration

# 3. HTTP 流量到文件
_path=="http" f.txt

# 4. SSL 流量
_path=="ssl"
```

## 工具
- **packettotal.com**：免费在线样本分析
- **Wireshark**：流量包分析
- **tshark**：命令行过滤

## 关键技巧
- **`_path` 字段过滤**：比单纯 ip/port 灵活
- **`sort -r duration`**：找最长时间传输的文件最可疑
- **packettotal**：免费样本哈希查询

## 适用场景
- 蓝队流量分析入门
- 恶意软件样本识别
- Wireshark 高级过滤
