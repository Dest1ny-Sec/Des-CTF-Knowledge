---
title: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（一）
contest: VSEC
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [Block-Harbor, VSEC-HarborBay, Mach-E-UDS-simulation, CAN-interface, Arbitration-ID, license-plate-VIN, MAC-address-geolocation, OSINT]
attack_chain: 1. VSEC 平台 → HarborBay → Mach-E UDS Challenge Simulation/2. CAN 接口名/3. 周期 CAN 帧 Arbitration ID/4. CAN 帧 data 字段字节数 + 值/5. 帧发送频率 Hz/6. Block Harbor 成立时间 2014 年/7. 车牌 DCR 660 密歇根州查 VIN + 品牌型号 + 制造地 + 进口时间/8. MAC 2A:38:5C:91:E5:27 查 2022-12-08 位置
key_payload: Mach-E UDS Challenge  CAN 接口名  帧格式  车牌 DCR 660  MAC 2A:38:5C:91:E5:27
one_liner: VSEC 车联网安全 CTF 挑战赛（一），Mach-E UDS 模拟器 + Block Harbor 背景 + 车牌 + MAC 地理定位。
lesson: Block Harbor 是汽车网络安全公司，VSEC 是其平台；Mach-E 是福特野马电动车；CAN 仲裁 ID + data 字段是基础协议；车牌反查 VIN 是 OSINT 经典题。
quality: medium
---

# 【WriteUP】VSEC 车联网安全 CTF 挑战赛（一）

## 概览
Block Harbor 组织的车联网安全 CTF 挑战赛 VSEC，50 个汽车挑战，5000 美元奖金。

## 题目 1: CAN 接口名
- 在 VSEC → HarborBay → Mach-E UDS Challenge Simulation → 启动终端
- 查 CAN 接口名称

## 题目 2-5: CAN 帧分析
- Arbitration ID
- data 字段字节数
- data 字段值（格式 XXYY）
- 发送频率（Hz）

## 题目 6: 密码
- 提示"如果是您的实际密码，扣 100 万分"

## 题目 7: Block Harbor 成立时间
- 搜官网介绍：2014 年成立

## 题目 8-11: 车牌 OSINT（DCR 660）
- 注册地：密歇根州
- 查 VIN
- 品牌和型号（格式：year-make-model）
- 制造地（格式：City, Country）
- 进口时间（格式：dd-mm-yyyy）

## 题目 12: MAC 地址地理定位
- MAC: `2A:38:5C:91:E5:27`
- 追踪 2022-12-08 位置
- 纬度和经度，精确到小数点后两位（格式：XX.XX,XX.XX）

## 经验提炼
- Block Harbor 是汽车网络安全公司，VSEC 是其平台
- Mach-E 是福特野马电动车
- CAN 仲裁 ID + data 字段是基础协议
- 车牌反查 VIN 是 OSINT 经典题
- 密歇根州车牌可查 NHTSA 数据库
- MAC 地址地理定位用 WiFi 探针数据库
- CAN 周期帧通常用于状态广播
- 50 个汽车挑战覆盖车联网攻击面
- 100K 美元奖金池反映行业重视
- VSEC 平台提供 HarborBay 仿真环境
