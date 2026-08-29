---
title: Open xINT CTF 2024 Writeup (日文 OSINT)
contest: xINT CTF
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [OSINT, whois, TLDpedia, 注册商查询, 国外店铺电话]
attack_chain: |
  1. whois (100pts):
     - 题目: gov.ru 的纳税人番号是什么?
     - Domaintools 查询无果
     - TLDpedia 找 .ru 注册商 whois 页面
     - 直接在注册商页面搜
     - 朋友说直接 whois 命令一撃可解
  2. all grean (100pts):
     - 题目: 这家店的电话号码是什么? (国番号, 无连字符)
     - 外国店, Google Lens 失败
     - 细部观察找线索
  3. 比赛概况:
     - 6 题 1200 点 (官方显示 1500 点)
     - 排名 17 (按 1200 算 25 名)
     - 日本 + 国际 OSINT 玩家
key_payload: |
  # whois gov.ru 税号:
  whois gov.ru
  # 或访问 TLDpedia 找 .ru 注册商 whois 页面
  
  # 国外店铺电话:
  # 细部观察 + Google 搜索
one_liner: Open xINT CTF 2024 日文 OSINT 速查: whois gov.ru 税号 + 国外店铺电话。
lesson: |
  - whois 命令一撃可解 .ru 域名税号
  - TLDpedia 是 TLD 注册商查询工具
  - OSINT 比赛需要熟练使用 whois/Domaintools
  - 日文 CTF 比赛也是 OSINT 的重要组成部分
  - xINT CTF 是日本 xINT 系列 OSINT 比赛
quality: medium
---

# Open xINT CTF 2024 Writeup

> 来源: ctfiot.com 215623

## 比赛背景

- 参与次数: 第 2 次 (继 TsukuCTF 2023 后)
- 6 题 1200 点 → 排名 17
- 日本 + 国际 OSINT 玩家

## whois (100pts)

```bash
# 题目: gov.ru 的纳税人番号是什么?
whois gov.ru
# 或访问 TLDpedia 找 .ru 注册商 whois 页面
```

> 后来朋友说 whois 命令一撃可解

## all grean (100pts)

```bash
# 题目: 这家店的电话号码是什么? (国番号, 无连字符)
# 外国店, Google Lens 失败
# 细部观察 + Google 搜索
```

## 评价

Open xINT CTF 2024 日文 OSINT 速查：
- **whois gov.ru** 税号查询
- **TLDpedia** 注册商查询
- **国外店铺电话** OSINT

xINT CTF 是日本 OSINT 比赛，国际化程度较高。

适用读者：OSINT 入门 / 国外信息查询
