---
title: ICLESCTF 网络安全比赛 WP（Misc & Crypto）
contest: ICLESCTF
year: 2025
difficulty: easy
vuln_type: misc_unknown
tags: [gif-frame, news-base64, xor-index-cipher, RSA, LCG, data-stream-crack, 随波逐流]
attack_chain: interesting_web 4 个 GIF 快速滚动 + 随波逐流分帧查看得 flag/新闻网站 base64 编码解码/xor_index_cipher 写解密脚本/RSA 写解密脚本/破解数据流解密/LCG 写解密脚本
key_payload: GIF 分帧 + base64 解码 + 简单密码还原
one_liner: ICLESCTF 2025 网络安全比赛 Misc & Crypto 6 道题 WP，覆盖 GIF 分帧/base64 隐写/4 种密码学题。
lesson: GIF 快速滚动是帧动画；随波逐流是国内常用隐写分析工具；xor/RSA/LCG/数据流密码 4 类是基础密码学题。
quality: low
---

# ICLESCTF 网络安全比赛 WP（Misc & Crypto）

## 概览
ICLESCTF 2025 6 道题 WP，Misc 2 题 + Crypto 4 题。

## Misc

### 1. interesting_web
- 访问网站发现 4 个 GIF 快速滚动
- 拖入"随波逐流"分析，分帧查看
- 分帧后得 flag

### 2. 新闻网站
- 存在一张图片
- 拖入"随波逐流"分析
- 发现 base64 编码，解码得 flag

## Crypto

### 3. xor_index_cipher
- 写解密脚本还原

### 4. RSA
- 写解密脚本还原

### 5. 破解数据流
- 写解密脚本还原

### 6. LCG
- 写解密脚本还原

## 经验提炼
- GIF 快速滚动是帧动画，用"随波逐流"分帧
- 随波逐流是国内常用隐写分析工具（BinWalk、stegsolve 替代品）
- xor/RSA/LCG/数据流密码是基础密码学题四大类型
- 简短的 WP 通常是入门级比赛，关键在快速识别题目类型
