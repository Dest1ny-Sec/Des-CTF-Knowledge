---
title: 2024 阿里CTF WriteUp By Mini-Venom（Pwn + AI 推特情感分类）
contest: 2024 阿里CTF
year: 2024
difficulty: medium
vuln_type: [pwn_unknown, misc_math, web_unknown]
tags: [招新广告战队, n1[15]=4 n1[0]=0, malloc 0x20 show 指针, mid edit 栈溢出, sub_20F7 v3[264] BYREF overflow, sklearn TfidfVectorizer + LinearSVC, Twitter airline sentiment 数据集, kaggle crowdflower]
attack_chain:
  - Pwn sub_20F7: v3[264] BYREF + 0x118 rsp offset → rbp-0x110 → 264+0x10 字节可填，溢出到 rbp-8 canary
  - 中间 edit 触发 off-by-null 修改 n1[15]=4 偏移绕过
  - AI: kaggle Twitter airline sentiment dataset + sklearn tfidf + LinearSVC 训练
  - 准确率不高但几次试出
key_payload: "n1[0] = 0; n1[15] = 4"
one_liner: 阿里 CTF Mini-Venom 招新广告：Pwn sub_20F7 栈溢出 264 字节 + mid edit off-by-null + AI 用 Twitter 情感数据集 sklearn LinearSVC 试答案。
lesson: Mini-Venom 招新广告常带"试错型"AI 题（情感分类、对抗样本）作为引流入口，准确率不用太高，多试几次；栈溢出 264 字节可填但 rbp-8 是 canary，需先 leak 才能 ROP。
quality: low
---

# 2024 阿里CTF WriteUp By Mini-Venom

## Pwn

```c
__int64 sub_20F7() {
    int i;            // [rsp+8h]  [rbp-118h]
    int v2;           // [rsp+Ch]  [rbp-114h]
    char v3[264];     // [rsp+10h] [rbp-110h] BYREF overflow
    unsigned __int64 v4;  // [rsp+118h] [rbp-8h]
    ...
}
```
`v3[264]` 距 rbp-0x110，v4 是 canary 在 rbp-8。  
`n1[0]=0; n1[15]=4` 触发 off-by-null 绕过某 size 检查，mid edit 时溢出覆盖返回地址。  
需要先 leak canary 再 ROP。

## AI 情感分类

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

# 数据集：kaggle crowdflower/twitter-airline-sentiment
```
"准确率不高，反正试了几次也出了" — 走试错路线，对抗样本式 AI 题。
