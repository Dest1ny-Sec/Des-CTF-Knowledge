---
title: CTF学习交流群 第五期writeup大放送
contest: 群赛出题
year: 2017
difficulty: easy
vuln_type: misc_unknown
tags: [misc, apk-reverse, web, 招新, 群活动]
attack_chain:
  - misc题作者天河出题
  - apk题作者天河用flag_en数组chr(i-1)解码
  - web题作者Adolph出PDF附件文档
  - 答案d0c0r10n_th3_w0rld
key_payload: flag_en=[0x65,0x31,0x60,...]; s+=chr(i-1)
one_liner: CTF群第5期三题writeup合集，misc+apk+web
lesson: 群活动writeup合集典型格式，答案+招新广告+游戏宣传
quality: low
---

# CTF学习交流群 第五期writeup大放送

## 题目信息
- 群号 473831530（已关闭入群）
- 出题人：kkkkkkkkx（misc）、大土豆（apk）、Adolph（web）
- 后续：第6期 BrainOverFlow 招新活动

## 关键攻击链
1. misc题仅给到作者+wp作者署名，无具体解法
2. apk题：flag_en 14 字节数组，每个字节 -1 后转字符
3. web题：直接附 PDF 出题文档，春节期间环境仍有效
4. 招新广告 + BrainOverFlow 冬季仙境 DLC 宣传

## 关键技术点
- 简单字节减法：chr(i-1)
- APK DEX 静态分析
- Web 题目环境化（PDF 出题）

## 评分
- quality: low（招新广告多，实际解法少，2/3 题仅给答案流水账）
