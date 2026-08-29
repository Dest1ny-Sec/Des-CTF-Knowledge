---
title: Backdoor CTF 2023 Writeup
contest: Backdoor CTF
year: 2023
difficulty: easy
vuln_type: misc_unknown
tags: [exiftool Artist, flag{7h3_r34l_ctf_15_7h3_fr13nd5_w3_m4k3_al0ng}, jadx smali, open_sesame MainActivity, it4chi n4ut1lus sh4dy sl4y3r, valid_password 7字节, XOR循环校验, Character.isDigit, sl4y3r]
attack_chain:
  - friend.jpeg exiftool Artist: flag{7h3_r34l_ctf_15_7h3_fr13nd5_w3_m4k3_al0ng}
  - open_sesame.apk jadx 反编译 smali
  - MainActivity.valid_password = [0x34, 0x6c, 0x31, 0x62, 0x61, 0x62, 0x61] = "4l1baba"
  - it4chi: char → int[] 数组
  - n4ut1lus: 比较 int[] 长度和元素
  - sh4dy: 保留数字字符 (Character.isDigit)
  - sl4y3r: 字符串处理
  - flag: charAt 循环 XOR
  - 登录: 输入 user + 密码
key_payload: 'exiftool Artist flag / valid_password 0x34 0x6c 0x31 0x62 0x61 0x62 0x61 = "4l1baba" / it4chi+n4ut1lus+sh4dy+sl4y3r / XOR 循环'
one_liner: Backdoor CTF 2023 — exiftool Artist 字段直接读 flag + open_sesame APK smali 分析 it4chi/n4ut1lus/sh4dy/sl4y3r/flag 函数 + valid_password 0x34 0x6c 0x31 0x62 0x61 0x62 0x61 = "4l1baba"。
lesson: JPEG EXIF Artist 字段常被用来藏 flag;smali 读 valid_password 数组转 ASCII 是 APK 入门基础;函数名混淆 it4chi/n4ut1lus/sh4dy/sl4y3r 提示四元素 (海龟汤)。
quality: medium
---

# Backdoor CTF 2023 Writeup

## 速读
Backdoor CTF 2023 — JPEG exiftool + APK smali 入门。

## 1. JPEG exiftool
```bash
$ exiftool friend.jpeg
Artist : flag{7h3_r34l_ctf_15_7h3_fr13nd5_w3_m4k3_al0ng}
```

## 2. APK smali (open_sesame)
- `MainActivity` extends `AppCompatActivity`
- `valid_password = [0x34, 0x6c, 0x31, 0x62, 0x61, 0x62, 0x61]` = "4l1baba"

## 函数列表
| 函数 | 作用 |
|------|------|
| `it4chi(String)` | char → int[] 转换 |
| `n4ut1lus(String)` | 验证 int[] 长度和元素 |
| `sh4dy(String)` | `Character.isDigit` 保留数字字符 |
| `sl4y3r(String)` | 字符串处理 |
| `flag(String, String)` | charAt 循环 XOR |

## flag
- `flag{7h3_r34l_ctf_15_7h3_fr13nd5_w3_m4k3_al0ng}` (TMNT 海龟汤彩蛋)
