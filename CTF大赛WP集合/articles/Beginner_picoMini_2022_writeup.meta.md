---
title: Beginner picoMini 2022 writeup
contest: picoCTF
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags: [picoCTF Beginner, run_s4n1ty_run, s4n1ty_c4t, str_xor enkidu, 4个level, md5 hash, 691d密码, 4ec9密码, print_flag, serpentine, fixme缩进]
attack_chain:
  - runme.py: 直接 print flag{picoCTF{run_s4n1ty_run}}
  - nc saturn.picoctf.net 57688: picoCTF{s4n1ty_c4t}
  - convertme.py: 十进制 → 二进制, XOR 'enkidu' 解密
  - code.py: picoCTF{c0d3b00k_455157_8100c7c1}
  - fixme1.py: 缩进错误
  - fixme2.py: if flag = "" 应为 ==
  - level1.py: 密码 691d → str_xor 解密
  - level2.py: chr(0x34)+chr(0x65)+chr(0x63)+chr(0x39) = "4ec9"
  - md5 多轮: Joan of Arc, Clint Eastwood, grave robbers
  - serpentine: 选 b 调 print_flag
  - level3.py: 密码 1ea2
  - level4.py: 100 个候选密码 md5 匹配
key_payload: 'str_xor enkidu / md5 hash / 691d 4ec9 1ea2 密码 / print_flag / 100 候选 md5 匹配'
one_liner: picoCTF Beginner picoMini 2022 全 12 题 — runme + nc + convertme + code + fixme1/2 + 4 个 level (str_xor + md5 + print_flag) + serpentine + 100 候选 md5 匹配。
lesson: picoCTF 入门是综合小练习合集:Python 脚本分析、密码学 (XOR/md5)、代码修复 (缩进/语法)、二进制 (print_flag 函数)。
quality: medium
---

# Beginner picoMini 2022 writeup

## 速读
picoCTF 2022 Beginner picoMini 全 12 题入门合集。

## 题目列表

### 1. runme.py
```python
flag = 'picoCTF{run_s4n1ty_run}'
print(flag)
```

### 2. nc saturn.picoctf.net 57688
```
picoCTF{s4n1ty_c4t}
```

### 3. convertme.py
- 输入十进制转二进制
- 26 → 11010
- `str_xor(flag_enc, 'enkidu')` → `picoCTF{4ll_y0ur_b4535_e2a58836}`

### 4. code.py
```
picoCTF{c0d3b00k_455157_8100c7c1}
```

### 5. fixme1.py
- 缩进错误 → `picoCTF{1nd3nt1ty_cr1515_09ee727a}`

### 6. fixme2.py
- `if flag = ""` → 改 `==`
- `picoCTF{3qu4l1ty_n0t_4551gnm3nt_4863e11b}`

### 7. level1.py
- 密码: `691d`
- `picoCTF{545h_r1ng1ng_56891419}`

### 8. level2.py
- 密码: `chr(0x34)+chr(0x65)+chr(0x63)+chr(0x39) = "4ec9"`
- `picoCTF{tr45h_51ng1ng_9701e681}`

### 9. MD5 模式
- `Joan of Arc` → 19ba425a542946fcf13228d9ddd53139
- `Clint Eastwood` → b84954cb41831fa842dd69f6e1836b6e
- `grave robbers` → bf48d2ac4e5d0532912c8e8e0998645f
- `picoCTF{4ppl1c4710n_r3c31v3d_674c1de2}`

### 10. serpentine.py
- 选 `b` → `picoCTF{7h3_r04d_l355_7r4v3l3d_8e47d128}`

### 11. level3.py
- 密码: `1ea2`
- `picoCTF{m45h_fl1ng1ng_6f98a49f}`

### 12. level4.py
- 100 候选密码 md5 匹配
- `hash_pw` 拿 md5 比对
