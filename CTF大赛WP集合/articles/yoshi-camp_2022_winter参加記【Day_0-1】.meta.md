---
title: yoshi-camp 2022 winter 参加記【Day 0-1】
contest: yoshi-camp
year: 2022
difficulty: easy
vuln_type: misc_math
tags: [hash-collision, integer-encoding, flag, sat]
attack_chain: H('A') 哈希 = 287496 / H('\xf0') = 多项式 6*z2 + 30*z2... / int.to_bytes(0b..., 64, 'big') 解码出 yochicamp{uouo_fish_life}
key_payload: int.to_bytes(0b1111001011011110110001101101000011010010110001101100001011011010111000001111011011101010110111101110101011011110101111101100110011010010111001101101000010111110110110001101001011001100110010101111101, 64, "big")
one_liner: yoshicamp 2022 winter 简单题，直接给出哈希值→位串→ASCII 字符串 flag。
lesson: 位串→int.to_bytes(64, 'big') 是从比特流到 ASCII flag 的标准转换；多项式哈希 H(x) = 6*z + 30*z 类表达用 z 变量符号化"未知数"。
quality: low
---

# yoshi-camp 2022 winter 参加記【Day 0-1】

## 概览
极简 WP，只有一个示例块演示哈希→位串→flag 的转换路径。

## 关键公式
- H('A') = 287496
- H('\xf0') = 3125053620820126733577185655687010464159146*z2 + 30208777635867085880652267524806729714750758
- 解码：`int.to_bytes(0b..., 64, "big")` → 64 字节大端串 → `\x00...yochicamp{uouo_fish_life}`

## 经验提炼
- 哈希题如果直接给出位串（如 `0b11110010...`），几乎总是 `int.to_bytes(bit_len, 'big')` 解码
- 64 字节（512 bit）长度对应常见 SHA-512 摘要长度
- yoshicamp 是日本 Yoshíer 联合 CTF，多用 SAT / z3 类符号化思路
