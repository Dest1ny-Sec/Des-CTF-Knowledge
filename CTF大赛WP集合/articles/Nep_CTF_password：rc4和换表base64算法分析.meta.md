---
title: Nep CTF password RC4 + 换表 base64 算法分析 (Android JNI)
contest: Nep CTF
year: 2023
difficulty: hard
vuln_type: reverse
tags: [Android APK, JNI verify, 自定义 base64 字符表, RC4, v28/v30 算法还原]
attack_chain: |
  1. 题目: Nep CTF password — Android 客户端
  2. Java 层:
     - verify(String str) == 0  (so 文件)
     - file(byte[] bArr, String str) == true (比较 iArr2 = {139,210,217,93,149,255,126,95,41,86,18,185,239,236,139,208,69})
  3. JNI verify:
     - Java_com_nepnep_app_MainActivity_verify
     - 输入字符串 → 处理 → 与 "3g6L2PWL2PXFmR+7ise7iq==" 比较
     - 处理使用 sub_77C 和 sub_8A4
  4. 自定义 base64 字符表: "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ"
     - 标准 base64 字符表: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
     - 区别: 大小写反转 + 字母表 vs 数字 + 符号
  5. 反推 v30: v30[i] = index_in_custom_table(s1[i])
  6. v12 = (v30[i] - v5 + 64) % 64, v5 是 v8 计数
  7. 还原出原始明文 (再经 RC4 加密还原 Java 层)
key_payload: |
  # 自定义 base64 字符表:
  aAb_str = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  # 反推 v30 (v30[i] = index in aAb_str):
  s1 = "3g6L2PWL2PXFmR+7ise7iq=="
  s1_one = "3g6L2PWL2PXFmR+7ise7iq"
  v30 = []
  for one in s1_one:
      v30.append(get_aAb_str_len(one))  # v30 = [29, 6, 32, 49, 28, 53, 60, 49, 28, 53, 61, 43, 12, 55, 36, 33, 8, 18, 4, 33, 8, 16]
  
  # v12 算法反推:
  v7 = 16
  v5 = 0
  while v7 >= 1:
      if v7 < 3:
          s1_arr[v5] = aAb_str[v30[v5]]
          s1_arr[v5 + 1] = aAb_str[v30[v5 + 1]]
          v9 = "="
          s1_arr[v5 + 2] = "="
          v8 = v5 + 3
      else:
          v8 = v5 + 3
          v9 = "="
      v5 = v8
one_liner: Nep CTF password: Android JNI verify + 自定义 base64 字符表 (小写字母+数字+大写字母+符号) + RC4 加密, v30 数组反推算法。
lesson: |
  - Android 客户端: Java 层 verify + file + JNI 层 custom base64
  - 自定义 base64 字符表 vs 标准 base64: 字符表顺序和大小写反转
  - v30 = index_in_custom_table, v12 算法反推
  - iArr2 17 字节比较是已知明文攻击
  - RC4 在 java 层加密 → JNI 层 base64 编码 → 比对硬编码 "3g6L2PWL2PXFmR+7ise7iq=="
  - 完整还原算法需要: 反推 base64 + 解 RC4
quality: high
---

# Nep CTF password RC4 + 换表 base64 算法分析

> 来源: ctfiot.com 167920

## 题目背景

- Android APK
- Java 层: `verify(String str) == 0` + `file(byte[] bArr, String str) == true`
- JNI 层: `Java_com_nepnep_app_MainActivity_verify`

## 自定义 base64 字符表

```python
aAb_str = "abcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# 标准: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
# 区别: 大小写反转 + 字母表 vs 数字 + 符号
```

## 已知密文

```c
// JNI 函数处理后比较
"3g6L2PWL2PXFmR+7ise7iq=="
```

## iArr2 比较

```java
iArr2 = {139, 210, 217, 93, 149, 255, 126, 95, 41, 86, 18, 185, 239, 236, 139, 208, 69}
```

## v30 反推

```python
def get_aAb_str_len(ab_str):
    for i, ab in enumerate(aAb_str):
        if ab == ab_str:
            return i

s1 = "3g6L2PWL2PXFmR+7ise7iq=="
s1_one = "3g6L2PWL2PXFmR+7ise7iq"
v30 = [get_aAb_str_len(c) for c in s1_one]
# v30 = [29, 6, 32, 49, 28, 53, 60, 49, 28, 53, 61, 43, 12, 55, 36, 33, 8, 18, 4, 33, 8, 16]
```

## 评价

Nep CTF password Android 客户端逆向 + 自定义 base64 + RC4 综合题：
- **自定义字符表** base64 是国赛常见 trick
- **v30 数组** 是反推核心
- **Java 层 RC4** + JNI 层 base64 双层加密
- **iArr2 17 字节** 比较是已知明文攻击

适用读者：Android 逆向 / JNI / 自定义算法
