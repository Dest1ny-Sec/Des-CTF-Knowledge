---
title: 2025 KCTF 第九题《智斗邪首》设计思路及解析（斐波那契变种+高精度倒数）
contest: 2025 KCTF
year: 2025
difficulty: medium
vuln_type: [misc_math]
tags: [KCTF 2025 第九题 智斗邪首, 斐波那契数列变种, 超长小数, 倒数变换, Python Decimal 高精度, sys.set_int_max_str_digits, 字符串压缩算法, 2024*2039=4126936, 2025*2040=4131000, htg 出题 心学战队]
attack_chain:
  - Python Decimal 调高精度 getcontext().prec=int(prec)
  - sys.set_int_max_str_digits(int(arg2)) 允许超长整数打印
  - 计算 Decimal(1) / Decimal(n) 的倒数
  - 斐波那契变种构造超长整数（千万位级）
  - 字符串压缩算法处理超大整数
  - 多层输入校验+混淆
key_payload: "getcontext().prec = int(prec); Decimal(1) / Decimal(n)"
one_liner: 2025 KCTF 第九题 智斗邪首：斐波那契变种+Decimal 高精度倒数+压缩编码+多层输入校验，考验数学建模和工程实现。
lesson: Python 处理超长整数时 `sys.set_int_max_str_digits(0)` 必加，否则 str(int) 报 ValueError；斐波那契变种构造"特殊数字"是密码学/数学 CTF 高频套路。
quality: high
---

# 2025 KCTF 第九题《智斗邪首》设计思路及解析

## KCTF 评委团队点评

> 这道 CTF 题以斐波那契数列变种为数学核心，通过构造超长小数和倒数变换，将逆向问题转化为高精度计算挑战。题目创新性地采用字符串压缩算法处理超大整数，并嵌入 Python 解决精度问题，增加了多层输入校验和混淆机制。难点在于识破数学构造、处理压缩编码及实现精确倒数计算，考验选手的数学建模和工程实现能力。

## 设计思路

出题人：htg（心学战队）

### 主要框架

```python
from decimal import Decimal, getcontext
import os
import sys

def reciprocal(n, prec):
    getcontext().prec = int(prec)
    result = Decimal(1) / Decimal(n)
    return result

def main(arg1, arg2):
    sys.set_int_max_str_digits(int(arg2))  # 关键！允许超长整数打印
    reciprocal_value = reciprocal(arg1, arg2)
    print(reciprocal_value)

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    main(arg1, arg2)

# 2024*2039=4126936
# 2025*2040=4131000
```

## 解题关键

1. **斐波那契变种构造**超长小数（千万位级）
2. **倒数变换** Decimal(1) / Decimal(n) 高精度
3. **字符串压缩算法**处理超大整数（不然 str() 直接报错）
4. **多层输入校验**+混淆（避免直出）
5. **`sys.set_int_max_str_digits()`** 必加，否则 str 大整数 raise ValueError
6. **2024*2039=4126936** / **2025*2040=4131000** 是提示年份相关
