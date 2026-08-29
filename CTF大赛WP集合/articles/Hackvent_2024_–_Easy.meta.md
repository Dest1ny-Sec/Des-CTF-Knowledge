---
title: Hackvent 2024 – Easy
contest: Hackvent 2024
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [misc, gifsicle, change-color, ean8, barcode, python-check-digit, png-extract]
attack_chain:
  - gifsicle --change-color 234 "#000000" --change-color 235 "#ffffff" 04ab...gif > mod.gif
  - 解压help.zip得到9个example*.png
  - 162x191 1-bit grayscale PNG
  - EAN-8 校验位计算:
  - odd_sum = sum(odd positions * 3)
  - even_sum = sum(even positions)
  - check_digit = (10 - (odd+even)%10) % 10
  - 拼接flag
key_payload: gifsicle --change-color 234 "#000000" --change-color 235 "#ffffff"
one_liner: Hackvent 2024 Easy：gifsicle改色+EAN-8条形码校验位
lesson: gifsicle改透明色+EAN-8校验位算法
quality: medium
---

# Hackvent_2024_–_Easy

## 题目信息
- 比赛：Hackvent 2024
- 难度：Easy

## 关键攻击链
### 1. GIF 颜色处理
```bash
gifsicle --change-color 234 "#000000" --change-color 235 "#ffffff" 04ab832f-50dd-4dea-a834-e0a34fa625b5.gif > 04ab832f-50dd-4dea-a834-e0a34fa625b5-mod.gif
```
- 颜色 234 → 黑色
- 颜色 235 → 白色

### 2. 解压 help.zip
```bash
unzip help.zip
# example1.png ~ example9.png
```

### 3. PNG 特征
```
example1.png: 162 x 200, 1-bit grayscale
example2.png: 162 x 100, 1-bit grayscale
example3-9.png: 162 x 191, 1-bit grayscale
```

### 4. EAN-8 校验位
```python
def calculate_check_digit(ean8):
    odd_sum = sum(int(ean8[i]) * 3 for i in range(0, 7, 2))   # 奇数位
    even_sum = sum(int(ean8[i]) for i in range(1, 6, 2))         # 偶数位
    total_sum = odd_sum + even_sum
    check_digit = (10 - (total_sum % 10)) % 10
    return check_digit
```

## 评分
- quality: medium（gifsicle 改色 + EAN-8 校验位计算）
