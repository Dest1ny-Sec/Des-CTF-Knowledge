---
title: OSINTUK CTF – 幽灵行动 Writeup (UK OSINT 系列)
contest: OSINTUK
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [OSINT, what3words, Google Maps Street View, 谷歌双引号搜索, 凯撒 + 维吉尼亚]
attack_chain: |
  1. The Artifact (隐写 + 找位置):
     - 反向图片搜 MAG218 看起来是迪拜, 但答案是伦敦
     - exiftool 看元数据: "red herring" (red 鱼) 提示隐写
     - 图片实际隐写 what3words 三个词: then.number.known
  2. The Getaway (Google Maps 全景):
     - 2017.9 时间点, 谷歌地图全景图
     - 酒店大厅内部能看到门口 + 一辆 TX (伦敦黑色出租车)
     - 放大车牌清晰可见 → 推断地址
  3. The Odometer (里程表):
     - 数字累加 / 拼车数据 → OSINT
     - 还原行程
  4. The Key Source (Hackney Today 报纸):
     - 谷歌双引号搜 "Hackney Today" → 第 8 页
     - 关键句 "what goes around comes around"
     - flag: osintuk{WHAT_GOES_AROUND_COMES_AROUND}
  5. The Final Transmission (凯撒 + 维吉尼亚):
     - 凯撒密码基础 + 维吉尼亚密钥 4
     - AI 跑出最终 flag
key_payload: |
  # The Artifact what3words:
  # exiftool → "red herring" → 隐写
  # what3words: then.number.known
  
  # The Getaway (TX 车牌):
  # 2017.9 + Google Maps Street View 找黑色 TX 车牌
  
  # The Key Source:
  # site:googlesearch "Hackney Today" → 第 8 页
  # flag: osintuk{WHAT_GOES_AROUND_COMES_AROUND}
  
  # The Final Transmission:
  # 凯撒基础 + 维吉尼亚 (key=4)
one_liner: OSINTUK 幽灵行动: 4 道 UK OSINT (what3words 隐写 + Google Maps TX 车牌 + 报纸 + 凯撒+维吉尼亚)。
lesson: |
  - **what3words** 隐写: 全球位置编码系统 (3 词 → 3m×3m 精度)
  - exiftool 找 "red herring" 提示是 隐写
  - Google Maps Street View 历史全景 + 黑色 TX 车牌 = 伦敦出租
  - "Hackney Today" 报纸谷歌双引号搜 + 第 8 页
  - 凯撒 + 维吉尼亚 (key=4) 是古典密码入门
  - OSINTUK 是英国 OSINT 比赛
quality: high
---

# OSINTUK CTF – 幽灵行动 Writeup

> 来源: ctfiot.com 290898

## The Artifact

反向图片搜 MAG218 看起来是迪拜，但答案是伦敦：
- 尝试 MAG218 附近的伦敦酒店品牌
- 寻找迪拜风格 + 2017 年前建成 + 金融城属性

**exiftool 元数据：**
- "what am i" 谜语 → `red herring`（红色鲱鱼）= 转移视线提示

**关键洞察：** 隐写 → what3words `then.number.known`

## The Getaway

2017.9 时间点 + 谷歌地图全景图：
- 酒店大厅内部能看到门口外面
- 一辆符合特征的 TX（伦敦黑色出租车）
- 放大车牌清晰可见

## The Odometer

数字累加 / 拼车数据 OSINT 还原行程。

## The Key Source

```bash
site:google.com "Hackney Today"
# 第 8 页: "what goes around comes around"
```

**flag**: `osintuk{WHAT_GOES_AROUND_COMES_AROUND}`

## The Final Transmission

凯撒基础 + 维吉尼亚（key=4）古典密码破解。

## 评价

OSINTUK 幽灵行动 5 道 UK OSINT：
- **what3words** 隐写（3 词编码 3m×3m 精度位置）
- **Google Maps Street View** 历史全景 + 黑色 TX 车牌
- **报纸** "Hackney Today" 谷歌双引号搜索
- **凯撒 + 维吉尼亚** 古典密码

OSINTUK 是英国 OSINT 比赛，每道都需要"工具熟练度 + 推理能力"。

适用读者：OSINT 入门 / 英国地理 / 古典密码
