---
title: OSINTUK CTF – 星座行动 Writeup (UK 都市传说 OSINT)
contest: OSINTUK
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags: [UK OSINT, 都市传说, 星座杀手, Google Maps, 维吉尼亚密码, 虚无密码, 报纸隐写]
attack_chain: |
  1. Developed in Darkness (曼彻斯特 Albert Square):
     - 宝丽来照片 → 反向图片搜 → Albert Square
     - 曼彻斯特市中心著名地标
  2. The Last Meal (Big John's 外卖):
     - A41 公路 + Big John's → 谷歌地球搜 "Big John's in West Brom"
     - 找快餐店邮政编码
  3. Remote Access (toyota island):
     - A50 + A38 + Willington B5008 + Nottingham A50
     - 沿 A50 找发电站 → toyota island
  4. Ghost Writer (报纸):
     - 报纸文章篡改，关键地点被删除
     - 1931 万圣节 (漫画背面)
     - AI 识别地点
  5. Character Witness (虚无密码):
     - 手写纸条是重复字符
     - 加密方法简单但隐蔽
     - 虚无密码解码 → 地点
  6. The Big Picture (最终决战):
     - 之前的作案地点可能构成序列
     - 预测凶手下一步行动
key_payload: |
  # Developed in Darkness: 曼彻斯特 Albert Square
  # The Last Meal: A41 + Big John's in West Brom
  # Remote Access: A50 + A38 + 发电站 = toyota island
  # Ghost Writer: 报纸 + 1931 万圣节
  # Character Witness: 虚无密码
  # The Big Picture: 序列分析
one_liner: OSINTUK 星座行动: 5 道 UK 都市传说主题 OSINT (Albert Square + Big John's + toyota island + 报纸 + 虚无密码)。
lesson: |
  - OSINTUK 都市传说主题: "星座杀手" 跨城连环作案
  - Google Maps 是 UK OSINT 核心工具 (Street View 全景 + 街道名)
  - 报纸 + 1931 万圣节是历史 OSINT
  - 虚无密码 (Null cipher) 是手写纸条常用编码
  - 地点序列分析是 OSINT 高级技巧
quality: high
---

# OSINTUK CTF – 星座行动 Writeup

> 来源: ctfiot.com 295078

## "星座杀手" 都市传说

> "星座杀手" 跨城连环作案，每张照片都是下一步行动的线索。

## 5 道 OSINT 速查

### Developed in Darkness
- 宝丽来照片 → 反向图片搜 → **曼彻斯特 Albert Square**
- 曼彻斯特市中心著名地标

### The Last Meal
- A41 公路 + Big John's → 谷歌地球搜 "Big John's in West Brom"
- 找快餐店 **邮政编码**

### Remote Access
```bash
# 方位标识:
Birmingham – A38 (S)
Willington – B5008
Nottingham – A50 (E)
Uttoxeter – A50 (W)
# 沿 A50 找发电站 → toyota island
```

### Ghost Writer
- 报纸文章篡改，关键地点被删除
- 漫画背面 "1931 万圣节"
- AI 识别地点

### Character Witness
- 手写纸条是重复字符
- **虚无密码** (Null cipher) 解码 → 地点

### The Big Picture
- 之前的作案地点可能构成序列
- 预测凶手下一步行动

## 评价

OSINTUK 星座行动 5 道 UK 都市传说主题 OSINT：
- **Google Maps Street View** 街道全景
- **谷歌双引号搜索** 报纸 + 第 8 页
- **A50/A38/B5008** 英国公路网 OSINT
- **1931 万圣节** 历史事件 OSINT
- **虚无密码** 手写纸条解码

适用读者：UK OSINT / 都市传说 / 历史地理
