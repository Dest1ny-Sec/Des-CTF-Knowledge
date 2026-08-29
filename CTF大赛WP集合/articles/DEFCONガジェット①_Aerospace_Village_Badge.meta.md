---
title: DEFCON ガジェット① Aerospace Village Badge
contest: DEFCON
year: 2023
difficulty: easy
vuln_type: misc_unknown
tags: [badge, hardware, wifi, base64, moongoku, ipv4, sao]
attack_chain:
  - 看 Badge 边缘的刻印 MVNtYWxsU3RlcA==
  - Base64 解码得 1SmallStep
  - 当 Wifi 密码连 WrightStuff AP
  - 看另一侧"First moonwalk data as ipv4"
  - 解 IPv4 数据包
  - 莱特兄弟 / James Webb SAO
key_payload: 物理 Base64 刻印 + Wifi 密码
one_liner: DEFCON Aerospace Village Badge 硬件解谜，刻印 Base64 当 Wifi 密码。
lesson: 硬件 Badge 谜题第一步永远看边缘/背面刻印 + 物理连接器。
quality: high
---

DEFCON Aerospace Village Badge 硬件解谜，作者日本 CTFer（双语中日翻译）。

**Badge 介绍**
- The Wright Stuff（莱特兄弟），$80/12000 日元
- SAO（Simple Add-On）插槽：JWT = James Webb 太空望远镜
- 焊接后完成（去 Soldering Village）

**谜题 1：Wifi 密码**
看徽章边缘，刻印 `MVNtYWxsU3RlcA==`（两个 == 提示 Base64）。解码得 `1SmallStep`，作为 WrightStuff AP 的 Wifi 密码连接。

**谜题 2：First moonwalk data as ipv4**
另一侧有 "First moonwalk data as ipv4" 提示，需将 moonwalk 步态数据编码为 IPv4 流量包。深入分析需配合 Badge 上其他传感器（红外/温度等）。

**DEFCON Village 介绍**
DEFCON 现场有各种 Village：航天/医疗/锁具/车辆/焊接等，主题 CTF + 研讨会 + 讲座 + 售卖 Badge（捐款形式）。Badge 多有谜题/功能（SAO 可加挂载板），Wright Stuff Badge 是莱特兄弟跨卫星造型，触摸金属改变 LED 颜色。

整篇 WP 适合作为"硬件 + 现实世界 OSINT"类 CTF 题的入门参考。
