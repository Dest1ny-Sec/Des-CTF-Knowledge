---
title: 冠军Writeup大放送 | DataCon2022网络流量分析赛道之"见世面"战队
contest: DataCon2022 网络流量分析
year: 2022
difficulty: medium
vuln_type: forensic_traffic
tags: [DataCon, 流量分析, 挖矿检测, 智能蜜罐, CICFlowMeter, TLS ChangeCIPherSpec, OneClassSVM, IsolationForest, Suricata, Zeek]
attack_chain:
  - 广州大学方班 (方滨兴院士班) 见世面战队 5 人
  - 第1章 挖矿流量检测: black_ssl3.pcap 自抓加密挖矿流量
  - CICFlowMeter 处理 cryptomining.pcap → 流量特征提取
  - TLS ChangeCIPherSpec 包分析: 加密挖矿特征
  - mining_check_finish.py check_stream 函数
  - 机器学习: OneClassSVM / IsolationForest 异常检测
  - 第2章 智能蜜罐 Level1: 请求重发器 datacon_l1_poc_sent.py
  - 第3章 智能蜜罐 Level2: 字符串转换+正则匹配 datacon_l2_server_clean.py
  - 工具: Suricata / Zeek / NBMiner / Xray / scan4all
  - 方班 loom 战队 2019 首届 DataCon 冠军 + 2020 复赛奖项
key_payload: 'CICFlowMeter + TLS ChangeCIPherSpec + OneClassSVM + 智能蜜罐请求重发器'
one_liner: DataCon2022 流量分析冠军 见世面：挖矿流量检测 (TLS ChangeCIPherSpec) + 智能蜜罐构建 Level1/2。
lesson: 加密挖矿流量检测靠 TLS ChangeCIPherSpec 包特征 + CICFlowMeter 流量特征 + OneClassSVM 异常检测；智能蜜罐靠请求重发器测试响应差异。
quality: medium
---

# 冠军Writeup大放送 | DataCon2022网络流量分析赛道之"见世面"战队

## 概览
- **来源**: ctfiot 91160
- **赛事**: DataCon2022 流量分析赛道冠军
- **战队**: 广州大学方班 见世面 (曾东阳/顾家乐/张哲维/孙一航/徐颖慧, 指导李树栋)
- **难度**: ⭐⭐⭐

## 三大任务

### 第1章 挖矿流量检测
- 自行抓取 black_ssl3.pcap 加密挖矿流量
- CICFlowMeter 处理 cryptomining.pcap → 流量特征
- full.csv (Wireshark 导出) + full_http2.csv (排除干扰)
- **关键发现**: TLS ChangeCIPherSpec 包特征
- mining_check_finish.py: check_stream() 主处理函数

### 第2章 智能蜜罐环境构建-Level1
- datacon_l1_server.py: 接收请求返回正确响应
- datacon_l1_poc_sent.py: 请求重发器

### 第3章 智能蜜罐环境构建-Level2
- 字符串转换 + 正则匹配
- datacon_l2_server_clean.py: 接收请求响应
- datacon_l2_poc_sent.py: Level2 请求重发器

## 工具链
- CICFlowMeter (Ahlashkari GitHub)
- Zeek (网络分析)
- Suricata (IDS)
- NBMiner (挖矿工具样本)
- Xray (安全评估)
- OneClassSVM / IsolationForest (异常检测)
- scan4all (hktalent 综合扫描)

## 教学
- 加密挖矿流量: TLS ChangeCIPherSpec 包 + TLS 指纹
- 智能蜜罐: 请求重放检测响应差异
- 方班是 DataCon 流量分析老牌强队
