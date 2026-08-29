---
title: Buuctf 解题思路
contest: Buuctf
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [DialogFunc Win32, GetDlgItemTextA 8字符, 字符串比较, sub_4010F0 快排, sub_401000 base64 编码, byte_407830 表, APK jadx, dd2940c04462b4dd7c450528835cca15 XOR, qword 减法, easy strcmp]
attack_chain:
  - 刮开有奖: DialogFunc 接受 8 字符, 内部数组 v9-v19 存 90,74,83,69,67,97,78,72,51,110,103 (ZJSECaNH3ng)
  - sub_4010F0 快排: 改 v9-v19 顺序
  - sub_401000 base64 编码: 拿排序后字符串
  - 比较条件: String == v9+34 && v21 == v13 && 4*v22-141 == 3*v11 && v23/4 == 2*(v16/9) && !strcmp(v6, "ak1w") && !strcmp(v7, "V1Ax")
  - 简单注册器: APK jadx, MainActivity 32 字符注册码 + dd2940c04462b4dd7c450528835cca15 改 + reverse
  - easy strcmp: qword 减法恢复 3 个 8 字节字符串拼接 flag
key_payload: 'DialogFunc 8 字符 / sub_4010F0 快排 v9-v19 / sub_401000 base64 编码 / dd2940c04462b4dd7c450528835cca15 XOR + reverse / qword_201060 3 个 8字节减法'
one_liner: Buuctf 3 题合集 — 刮开有奖 DialogFunc 8 字符 + 快排 + base64 编码比较 + 简单注册器 APK 32 字符 + dd2940c0... XOR + reverse + easy strcmp qword 减法还原。
lesson: 字符串比较题多步:输入字符串 → 数组排序 → base64 编码 → 多重比较;APK 注册码常用 char[] + char 运算 + reverse;qword 减法是反编译快速 strcmp 还原的常见手段。
quality: medium
---

# Buuctf 解题思路

## 速读
Buuctf 多题合集 (长白山攻防实验室) — 刮开有奖 + 简单注册器 + easy strcmp。

## 1. 刮开有奖 (DialogFunc)

```c
BOOL DialogFunc(HWND hDlg, UINT a4, WPARAM a5, LPARAM a6) {
    if (a4 != 273 || (_WORD)a5 != 1001) return 0;
    GetDlgItemTextA(hDlg, 1000, &String, 0xFFFF);
    if (strlen(&String) == 8) {
        v9 = 90; v10 = 74; v11 = 83; v12 = 69; v13 = 67; v14 = 97;
        v15 = 78; v16 = 72; v17 = 51; v18 = 110; v19 = 103;  // ZJSECaNH3ng
        sub_4010F0(&v9, 0, 10);  // 快排
        // 多重比较
        if (String == v9 + 34 && v21 == v13 
            && 4*v22 - 141 == 3*v11 
            && v23/4 == 2*(v16/9) 
            && !strcmp(v6, "ak1w") 
            && !strcmp(v7, "V1Ax")) {
            MessageBoxA(hDlg, "U g3t 1T!", "@_@", 0);
        }
    }
}
```

## 2. 简单注册器 (APK jadx)
```java
if (xx.length() != 32 || xx.charAt(31) != 'a' || xx.charAt(1) != 'b' 
    || (xx.charAt(0) + xx.charAt(2)) - 48 != 56) {
    flag = 0;
}
if (flag == 1) {
    char[] x = "dd2940c04462b4dd7c450528835cca15".toCharArray();
    x[2] = (char)((x[2] + x[3]) - 50);
    x[4] = (char)((x[2] + x[5]) - 48);
    x[30] = (char)((x[31] + x[9]) - 48);
    x[14] = (char)((x[27] + x[28]) - 97);
    for (int i = 0; i < 16; i++) {  // reverse
        char a = x[31 - i];
        x[31 - i] = x[i];
        x[i] = a;
    }
    // flag{x}
}
```

## 3. easy strcmp (Zer0pts 2020)
```c
if (!strcmp(a2[1], "zer0pts{********CENSORED********}")) puts("Correct!");

// sub_6EA: 减法还原
for (j = 0; j < v4; ++j) 
    *(_QWORD *)(8*j + a1) -= qword_201060[j];
// qword_201060 = [0, 0x410A4335494A0942, 0x0B0EF2F50BE619F0, 0x4F0A3A064A35282B]
```

```python
import binascii
word_1 = [0x410A4335494A0942]
word_2 = [0x0B0EF2F50BE619F0]
word_3 = [0x4F0A3A064A35282B]
# 拼接还原
```
