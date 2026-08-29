---
title: 2025 第一届"网谷杯" Writeup（外链 PDF）
contest: 网谷杯
year: 2025
difficulty: easy
vuln_type: misc_unknown
tags: [招新广告, ChaMd5Venom, 团队战绩, PDF外链]
attack_chain:
  - 全文为 ChaMd5 安全团队 2017-2024 战绩列表
  - 真实 WP 内容指向外部 PDF：github.com/ChaMd5Team/Venom-WP/blob/main/2025-第一届网谷杯-WriteUp.pdf
  - 招新 IOT/Car/工控/样本分析 多方向
key_payload: 'admin@chamd5.org 招新邮箱'
one_liner: 纯粹的 ChaMd5 团队宣传页 — 列出 SRC/CTF/工控/IoT/AI/车联网/区块链 历年战绩，正文 WP 全部走外链 PDF。
lesson: 此类"WP"实质是团队软文 + 招新引流；结构化收录时只能标 misc_unknown，无法提取真正的技术细节。
quality: low
---

# 2025 第一届"网谷杯" Writeup

## 速读
本文为 ChaMd5 安全团队 Venom 战队在 ctfiot 发布的招新 + 战绩汇总。

## 实际内容
- 团队安全厂商漏洞致谢列表（2017-2024）
- CTF/工控/IoT/AI/车联网/区块链 多赛道奖项
- 团队书籍出版信息
- 真实 WP 全部外链 GitHub PDF

## 评价
"WP" 名称挂羊头卖狗肉 — 100% 招新广告，正文没有任何技术分析。
