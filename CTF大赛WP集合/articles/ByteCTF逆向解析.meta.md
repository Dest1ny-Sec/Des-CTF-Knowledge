---
title: ByteCTF 逆向解析 - babyapk
contest: ByteCTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [Flutter babyapk, blutter解析, main.dart, simple.dart, m3N4B5V6函数, Rust FFI, z3约束求解, 32e750c8fb214562af22973fb5176b9c, 4个-位置, byte_18E46表, validate_hyphen_positions, app.so, Native Hook]
attack_chain:
  - Flutter APK, jadx 无法看, 用 blutter 解析 libapp.so
  - main.dart 调 m3N4B5V6() 函数
  - 找到 simple.dart 包含验证逻辑
  - IDA 搜 Simple/m3N4B5V6 找加密函数
  - Frida hook app.so 多个 native 函数 → 没反应, 怀疑长度检测
  - 改长度, HOOK 情况: 长度为 0x2d, {} 内为 36 位
  - 加密函数逆推, 4 轮 8 变量非线性约束
  - z3 解: 数组解都是可显字符 → 32e750c8fb214562af22973fb5176b9c
  - 长度 32 包含 4 个 -, 穷举 - 位置
  - byte_18E46 表查 byte → 验证 hyphen 位置
key_payload: 'blutter main.dart simple.dart / IDA 搜 Simple m3N4B5V6 / Frida hook app.so / z3 4 轮 8 变量约束 / 32e750c8... 32 字符 / 4 个 - 位置穷举 / byte_18E46 表'
one_liner: ByteCTF babyapk 逆向 — Flutter APK blutter 解析 + IDA 找 m3N4B5V6 + Frida hook app.so + z3 解 4 轮 8 变量非线性约束 + 32e750c8... + 4 个 - 位置穷举 + byte_18E46 表。
lesson: Flutter APK 逆向核心是 blutter 解析 libapp.so;Rust FFI 加密函数 IDA 找 cross-ref;z3 解非线性约束 + 穷举小集合是混合策略。
quality: high
---

# ByteCTF 逆向解析 - babyapk

## 速读
ByteCTF babyapk 逆向 — Flutter APK + Rust FFI + z3 + 4 个 - 位置。

## 步骤
1. jadx 不行, 用 blutter 解析 libapp.so
2. main.dart → 调 m3N4B5V6()
3. simple.dart 包含验证逻辑
4. IDA 搜 Simple 字符 → 找到加密函数
5. Frida hook app.so native 函数 → 没反应
6. 改长度测试, 发现长度 0x2d ({} 内 36 字符)
7. 加密函数逆推, 4 轮 8 变量约束

## z3 解约束
```python
from z3 import *
cmp = [0x0001EE59, 0x0000022A, 0x00001415, 0x00040714, ...]

for j in range(4):
    v58 = [BitVec(f'v58[{i}]', 32) for i in range(8)]
    s = Solver()
    for i in range(8):
        s.add(v58[i] >= 0, v58[i] <= 0x10FFFF)
    
    num2 = v58[2]; num3 = v58[3]; num0 = v58[0]; num1 = v58[1]
    num4 = v58[4]; num5 = v58[5]; num6 = v58[6]; num7 = v58[7]
    
    s.add(num7 + num1*num3*num5 - (num0+num6+num2*num4) == cmp[0+j*8])
    s.add(num3 - num4 - num0*num5 + num7*num1 + num2 + num6 == cmp[1+j*8])
    s.add(num0*num5 - (num4+num7*num1) + num2 + num6*num3 == cmp[2+j*8])
    # ... 4 轮共 8 约束
    
    if s.check() == sat:
        model = s.model()
        v58_values = [model[v58[i]].as_long() for i in range(8)]
        print(v58_values)
```

## 结果
- 32 字符: `32e750c8fb214562af22973fb5176b9c`
- 含 4 个 -, 穷举位置

## 验证
```python
byte_18E46 = [0x01, 0x01, 0x01, ...]  # 256 字节表

def validate_hyphen_positions(input_str):
    byte = byte_18E46
    input_bytes = [ord(c) for c in input_str]
    v2 = byte[input_bytes[0]]
    # 累加 byte 跳到 - 位置
    # ... 4 个 - 位置
```
