---
title: 山石CTF 2024 招新赛/REVERSE&WEB 篇
contest: 山石CTF
year: 2024
difficulty: easy
vuln_type:
- reverse
tags:
- C++ 字符变换
- 循环移位
- 位交换
- 保留符号未脱
- UPX 脱壳
- 字符串常量比较
- 招新赛
attack_chain:
- easycpp2: 程序未脱符号，直接看 main 函数
- 读入 usr_input 字符串
- rand() % 7 + 1 得到 rotate_count
- func1 对每字符：func1_1 循环右移 rotate_count 位，func1_2 交换第 1 位和第 rotate_count 位
- 跟 24 字节 data 数组逐字节比较，全等输出 "Correct!"
- 解密：swap_bits 还原 + circular_left_shift 解出 ayyctf{you_get_rand_num}
- 后续题：UPX 脱壳 (l_info corrupted) → 改用 F8 手动步过 OEP 跳板 → dump 内存
- 字符串比较：strlen 后 FUN_401830 变换后跟 "02CD290D5ACE1A83" 比较
key_payload: "def swap_bits(byte, n): bit1 = byte & 1; bitN = (byte >> (n-1)) & 1; if bit1 != bitN: byte ^= 1; byte ^= (1 << (n-1)); return byte"
one_liner: C++ 保留符号无脱 → 看 main 还原 循环右移 + 位交换 加密
lesson: 招新赛题往往不脱符号；C++ 字符变换题常见循环移位+位操作复合；UPX l_info corrupted 时手脱 F8 步过 OEP
quality: medium
---

# 山石CTF 2024 招新赛/REVERSE&WEB 篇

**C++ 保留符号 + 循环右移 + 位交换还原**

> 山石CTF · 2024 · easy · reverse · quality=medium
> 思路: easycpp2: 程序未脱符号 → 直接看 main → func1: func1_1 循环右移 rotate_count 位，func1_2 交换第 1 位和第 rotate_count 位 → 跟 24 字节 data 数组比较 → 解密：swap_bits 还原 + circular_left_shift → 后续题：UPX 脱壳失败改手脱
> 套路: 招新赛题往往不脱符号；C++ 字符变换题常见循环移位+位操作复合；UPX l_info corrupted 时手脱 F8 步过 OEP

**关键 payload**:
```python
def swap_bits(byte, n):
    bit1 = byte & 1
    bitN = (byte >> (n-1)) & 1
    if bit1 != bitN:
        byte ^= 1
        byte ^= (1 << (n-1))
    return byte
```
