---
title: DIVER OSINT CTF 2024 writeup
contest: DIVER
year: 2024
difficulty: medium
vuln_type: misc_math
tags: [osint, gmail, google-maps, twitter, openstreetmap, flightradar, address]
attack_chain:
  - ad_directiare: gmail osint + Google Maps 评论找午餐价 4400
  - osprey1: 推特搜"屋久島 オスプレイ コールサイン"得 12-0065_GUNDAM22
  - osprey2: 推文定位 16:46 武士健身中心 OpenStreetMap Way 810021666
  - chiban: 饺子满洲+サンディ双葉店+地番検索くん → 筆界未定地-6
  - italy: 飞行数据网站搜 10/27 → I-LIDI Alidaunia 13:45:46 1600
key_payload: Gmail/Google Maps + 推特 + OpenStreetMap + FlightRadar24
one_liner: DIVER OSINT CTF 2024 复盘，日文 + 中文双语 WP 5 题。
lesson: OSINT 题的关键工具是 Gmail/Google Maps/推特/OpenStreetMap/FlightRadar24 五件套。
quality: high
---

DIVER OSINT CTF 2024 (2024/06/08-09) 5 题 WP，作者日本 CTFer。

**ad_directiare** — 名片上人物在东京出差时吃的午餐价格。Gmail osint + Google Maps 评论：`Diver24{4400}`。first blood。

**osprey1** — 2023/11/29 美国鱼鹰 V-22 在日本屋久岛坠毁。机号 + 坠机时呼号。推特搜"屋久島 オスプレイ コールサイン"找 Miliota 推文：`Diver24{12-0065_GUNDAM22}`。

**osprey2** — 2024/02/15 美军基地追悼式典 16:46:37 在哪里举行？OpenStreetMap Way 号码。推文推断武士健身中心外操场 OSM 搜：`Diver24{810021666}`。最后一分钟才交，osprey3 来不及。

**chiban** — 图像中央道路地番。饺子（饺子满洲，关东）+ サンディ（关东，Mr. 关西）双招牌 → サンディ双葉店 → 地番検索くん：`Diver24{筆界未定地-6}`。

**italy** — 2023/10/27 新潟大学校园上空的意大利直升机。所有者名 + 时刻 (JST) + 气压高度。FlightRadar24 查 10/27 历史：意大利黄色直升机 I-LIDI。UTC 转 JST：`Diver24{Alidaunia_13:45:46_1600}`。

**OSINT 五件套**：
1. Gmail/Google Maps 评论
2. 推特 (Twitter) 搜索
3. OpenStreetMap Way 编号
4. FlightRadar24
5. 地番検索くん

适合作为"日式 OSINT 入门"教材。
