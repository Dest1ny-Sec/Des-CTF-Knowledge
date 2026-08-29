---
title: 【WP】第七届"湖湘杯" leaker 设计思路与解析
contest: 湖湘杯
year: 2021
difficulty: medium
vuln_type: stego_image
tags: [digital-watermark, RGBA-alpha-LSB, 01-matrix-pattern, period-76-rows, 2x4-block-ASCII, leaker-source, frequency-anti-trim]
attack_chain: 1. Stegsolve 读 RGBA 模式 + Alpha 通道只有 255/254 → 最低位藏数据/2. 行重复周期 76 行 + 隔两行重复 → 缩小分析范围/3. 2x4 0 矩阵之间是相同信息 + 每隔 4 位为 0（ASCII 最高位）/4. 解读：1,3,5,7 行 + 2,4,6,8 列 + END 结束
key_payload: Alpha LSB 255/254  周期 76 行  2x4 矩阵 ASCII 编码
one_liner: 第七届湖湘杯 leaker 数字水印题，RGBA Alpha LSB 提取 01 矩阵 + 2x4 块 ASCII 编码还原。
lesson: 数字水印 = 抗修改隐写术，重复填充实现任意位置可读；RGBA Alpha 通道 255/254 区分是 LSB 隐写信号；2x4 0 矩阵作为分隔符是常见水印编码方式。
quality: high
---

# 【WP】第七届"湖湘杯" leaker 设计思路与解析

## 题目来源
- 出题人：NanoApe 师傅
- Idea 来源：互联网公司内部用于防泄密的数字水印

## 数字水印背景
"数字水印" 一词由 Andrew Tirkel 和 Charles Osborne 于 1992 年 12 月提出。

数字水印是一种隐蔽地嵌入到音频、视频或图像数据等信号的标记，用于验证数据真实性、完整性、标识所有者。

## 与隐写术区别
- **隐写术**: 人类感官上的不可感知性
- **数字水印**: 重心在鲁棒控制（抗修改）

## 水印应用
- 追踪溯源：水印嵌入每个分布点的数字信号
- 找到副本 → 检索水印 → 得知分发来源

## 解题步骤

### 1. Stegsolve 分析
- RGBA 模式图片
- Alpha 通道只有 255 和 254 两种取值
- 最低位藏数据

### 2. 01 矩阵提取
- 像素分布存在规律
- 单独提取得 01 矩阵
- 行重复周期 76 行（第 1 行 == 第 77 行）
- 隔两行重复一次
- 2x4 0 矩阵作为分隔符
- 矩阵内信息相同

### 3. ASCII 编码解读
- 第一行每隔 4 位为 0 → 猜测是 ASCII 最高位
- 每 2x4 矩阵代表一个字符的 ASCII 码
- 解读方法：
  ```
  1  3  5  7
  2  4  6  8
  END
  ```
- 按顺序读出 01 序列得明文

## 经验提炼
- 数字水印 = 抗修改隐写术，重复填充实现任意位置可读
- RGBA Alpha 通道 255/254 区分是 LSB 隐写信号
- 2x4 0 矩阵作为分隔符是常见水印编码方式
- 周期 76 行重复是冗余编码抗裁剪
- Stegsolve 是国内常用图像隐写分析工具
- 数字水印三要素：不可感知性 + 鲁棒性 + 容量
- 抗裁剪 = 重复填充 + 校验码
- leaker = 内部员工防泄密水印溯源场景
