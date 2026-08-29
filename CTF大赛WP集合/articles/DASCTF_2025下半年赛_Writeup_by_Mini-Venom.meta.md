---
title: DASCTF 2025 下半年赛 Writeup by Mini-Venom
contest: DASCTF
year: 2025
difficulty: low
vuln_type: misc_unknown
tags: [招新, pdf-only, 团队介绍, ChaMd5]
attack_chain:
  - 文档说"请联系 admin@chamd5.org"
  - PDF 链接 https://github.com/ChaMd5Team/Venom-WP
  - 实际内容是团队获奖历史
key_payload: 无 (仅招新文)
one_liner: DASCTF 2025 下半年赛 Mini-Venom 战队招新小广告 + 团队历年获奖汇总。
lesson: 部分"WP"实际是团队招新宣传，没有真实技术内容，应该标 low 质量。
quality: low
---

DASCTF 2025 下半年赛 Mini-Venom 战队（ChaMd5）"WP"——实际主要是团队招新广告 + 历年获奖历史。

**唯一技术内容**：

整篇 95% 是招新 + 历年战绩列表。战队 `ChaMd5 Venom` 长期招 IOT+工控+样本分析成员，邮箱 `admin@chamd5.org`。

唯一技术链接：https://github.com/ChaMd5Team/Venom-WP/blob/main/2025-DASCTF下半年赛Write_Up.pdf（PDF 而非 markdown）。

**战队历史获奖**（节选）：
- 2025 DASCTF 下半年赛 第四名
- 2025 CCF 智能汽车大赛 三等奖
- 2025 LLM 指令遵循攻防赛 第一名
- 2024 DASCTF 暑假挑战赛 第一名
- 2024 ByteAI 安全挑战赛 第十名
- 2024 Block Harbor VicOne Automotive CTF 第六名
- 2023 DataCon 漏洞分析赛道第三
- 2020 之江杯 工控第一名
- 2019 360SRC IoT 第四名
- 2018 赛博地球杯 工控第二名

适合作为参考战队历史档案，不含具体技术 WP。
