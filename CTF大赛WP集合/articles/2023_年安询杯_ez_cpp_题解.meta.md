---
title: 2023 年安询杯 ez_cpp 题解
contest: 安询杯 2023
year: 2023
difficulty: medium
vuln_type: reverse
tags: [数组硬编码, ROT13, XOR差分, 半字节交换, 爆破]
attack_chain:
  - Enc1: ROT13-like 字符偏移 (v3 > 90 时 +13 否则 -13，v3+13 > 122 时回 -13)
  - Enc2: 32 字节查 v6 表 ^=4/9/6 或 +=2/5
  - Enc3: arr[i] ^= 1; arr[i] = dec3(arr[i])
  - dec3(a1) 是 8-bit reverse 字节反转
  - 给定 arr 数组 32 个 uint（含 32-bit 负数）
  - 反向 Enc3 → Enc2 → Enc1 还原明文
key_payload: 'arr[] = {0x22, 0x0FFFFFFA2, 0x72, 0x0FFFFFFE6, 0x52, 0x0FFFFFF8C, ...}'
one_liner: 32 字节 ROT13 + 查表 XOR/ADD + 半字节反转 三层加密逆向。
lesson: 半字节反转 dec3(v) = ((v>>0)&1)<<7 + ... 是经典 8-bit reverse；查表操作要反向回推。
quality: medium
---

# 2023 年安询杯 ez_cpp 题解

## 来源
- 原文：ctfiot.com/119444.html

## 三层加密结构

### Enc1（ROT13 字符偏移）
```cpp
for (int v3 = 0; v3 < 128; v3++) {
    if ((v3 - 61) <= 0x3Eu) {
        if (v3 > 90) {
            if (v3 + 13 <= 122) tmp_result = v3 + 13;
            else tmp_result = v3 - 13;
        } else {
            if (v3 + 13 <= 90) tmp_result = v3 + 13;
            else tmp_result = v3 - 13;
        }
    }
    if (tmp_result == arr[i] && check(v3)) {
        // 找到原始字符 v3
    }
}
```
- 91-122 字母 (a-z) → 103-122 + 13 越界 → 减 13
- 65-90 字母 (A-Z) → 78-103 越界 → 减 13
- 实为 ROT13 字符偏移

### Enc2（32 字节查表）
```cpp
int v6[] = {0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0};
for (int i = 0; i < 32; i++) {
    if (i <= 16) {
        if (v6[i]) {
            if (v6[i] - 1 == 0) arr[i] ^= 9;
        } else {
            arr[i] += 2;
        }
    } else {
        if (v6[i]) {
            if (v6[i] - 1 == 0) arr[i] ^= 6;
        } else {
            arr[i] += 5;
        }
    }
}
```
- 前 16 字节：v6=0 加 2，v6=1 XOR 9
- 后 16 字节：v6=0 加 5，v6=1 XOR 6
- 逆向就是反向减 + XOR

### Enc3（半字节反转 + 整体 XOR 1）
```cpp
unsigned int dec3(unsigned int a1) {
    a1--;
    unsigned int v2 = 0;
    for (int v3 = 0; v3 < 8; v3++)
        v2 |= ((a1 >> v3) & 1) << (7 - v3);
    return v2;
}
// Enc3: arr[i] ^= 1; arr[i] = dec3(arr[i]);
```
- 先 XOR 1，再 8-bit reverse
- 逆向：8-bit reverse (dec3) → XOR 1

## 还原流程
1. 反向 Enc3：8-bit reverse → XOR 1
2. 反向 Enc2：v6=0 减 2 / 减 5，v6=1 XOR 9 / XOR 6
3. 反向 Enc1：ROT13 字符还原

## 关键技巧
- **ROT13 变种**：91-122 + 13 越界时回退，是常见 char 偏移
- **查表 v6 数组**：32 字节 v6 用 0/1 区分加法与 XOR
- **半字节反转**：8-bit 倒序是经典加密

## 适用场景
- C++ 简单加密逆向
- 多层数组变换
- 看雪论坛中级 RE
