---
title: HackPack（LLM挑战）Writeup
contest: HackPack CTF (LLM挑战)
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [llm, prompt-injection, yellowdog, pixel-bot, ssti, jinja2, ssrf, google-store]
attack_chain:
  - YellowDog-1: 描述黄狗LLM服务
  - carolina89 编号不可点击
  - 修改数据包编号为carolina89获flag
  - pixel-bot: 概括Google商店
  - 限制google域名
  - bot访问+分析返回结果
  - SSRF或LLM prompt injection
  - YellowDog LLM安全问题
key_payload: 改carolina89编号; prompt injection绕过google限制
one_liner: HackPack LLM挑战：YellowDog编号枚举+pixel-bot prompt injection
lesson: LLM应用安全常结合prompt injection+IDOR+SSRF
quality: medium
---

# HackPack（LLM挑战）Writeup

## 题目信息
- 比赛：HackPack CTF
- 类别：LLM 安全

## 关键攻击链
### YellowDog-1
- 描述黄狗图片 LLM 服务
- 多数图片可点击获取描述
- 编号 carolina89 的图片不可点击
- 修改请求中编号为 carolina89
- 获得 flag

### pixel-bot
- 概括 Google Store 列表
- 限制只能访问 google.com 域名
- bot 访问 + 分析返回结果
- 通过 prompt injection 绕过限制
- 引导 bot 泄露 flag

## 评分
- quality: medium（LLM + IDOR + prompt injection + SSRF 综合）
