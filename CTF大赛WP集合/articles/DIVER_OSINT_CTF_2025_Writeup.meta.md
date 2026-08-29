---
title: DIVER OSINT CTF 2025 Writeup
contest: DIVER
year: 2025
difficulty: medium
vuln_type: misc_math
tags: [osint, ndl, opendata, japan-internment, flightradar, google-earth, sentinel-2, korea-hotel, elevator-db]
attack_chain:
  - internment: 藤井富太郎木曜島真珠採り → ヘイ収容所 → Rushworth Camp 4
  - 澳大利亚开放数据库 + 官方记录
  - hole: 山西大同市 CM 拍摄
  - Sentinel-2 2024-08-27 卫星图找 霊丘県
  - elevator: 客室内 + 窗外景色 → 韩国東横イン
  - 特征外灯定位
  - 韩国电梯故障数据库
key_payload: メタ読み（metadata reading）+ Sentinel-2 卫星图
one_liner: DIVER OSINT CTF 2025 复盘，作者 CLACKER 前田。
lesson: 当 solve 数少的 hard 题，通过"问题描述的 solve 数"反推真实难度（メタ読み）。
quality: high
---

DIVER OSINT CTF 2025 Writeup，作者 CLACKER 前田（双语 WP）。

**internment (hard/48solve)**
- 著名木曜島真珠採りダイバー藤井富太郎，二战强制収容
- 释放的収容所 + 释放年月日
- 国会図書館 id.ndl.go.jp/auth/ndlna/001236886 → ヘイ収容所
- 英语搜索后切到澳大利亚开放数据库
- Hay 转 Ru（4 号）→ Release
- `Diver25{1946-12-10_4_Rushworth_Victoria}`

**hole (medium/72solve)**
- 这个洞在哪里？
- 山西大同市拍摄 CM；Google Earth 找不到同风景跑道
- 探索大同市域南东方向
- 2024-08-27 Sentinel-2 卫星图发现 霊丘県近边
- 精确位置定位 1 败，团队双 check 通过

**elevator (hard/12solve)**
- 某酒店客房 + 窗景（2024 拍摄），2 件故障记录的电梯
- 故障日 + 注册号
- 国内足場崩落事故排查无果
- 瓦屋根 → 日本为前提，但韩国有 13 家东横イン
- solve 数少的 hard 题"メタ読み"反推 → 韩国东横イン
- 特征外灯定位
- 韩国电梯故障数据库查 2 件记录
- `Diver25{20240101_20240601_1234567}`

**メタ読み（meta-reading）** 是本题反复强调的方法：题目描述里透露的"难度/solve 数"信息用作解题线索，hard 题但 solve 数少 = 方向偏了 / 是 niche 话题。
