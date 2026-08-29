---
title: 2022 年春秋杯冬季赛部分 WriteUp (天权信安)
contest: 2022 春秋杯冬季赛
year: 2022
difficulty: easy
vuln_type: [sqli, stego_image, reverse, web_unknown, misc_unknown]
tags: [春秋杯, 天权信安, PHP-下划线绕过, ftp-pcap, 零宽隐写, reindeer-game, Python-字节码, 位旋转, IDAPython]
attack_chain: ["Web ezphp: ?num=1_11 PHP 弱类型 + 数字下划线绕过", "Misc nan's analysis: Wireshark 导出 ftp 对象 → 图片末尾附加 shell.zip (零宽隐写)", "Misc reindeer game: 简单小游戏通关 → flag{82a2acb6-9803-4936-92db-f1431d90c6d1}", "Re easy_python: Python 字节码逆向 → LOAD_CONST 列表 + 位旋转 (x >> 5 | x << 3) & 0xff", "flag = [204,141,44,...] → flag{ddbae889-2895-44df-897d-2ae30df77b61}"]
key_payload: "flag = (flag[i] >> 5 | flag[i] << 3) & 255"
one_liner: 春秋杯 2022 冬季赛：PHP 下划线弱类型 + 零宽隐写 + Python 字节码
lesson: Python 字节码是 reverse 入门利器；PHP 下划线数字 (`1_11`) 是弱类型；零宽隐写是 misc 经典
quality: medium
---

# 2022 春秋杯冬季赛部分 WriteUp (天权信安)

原文 https://www.ctfiot.com/88076.html （天权信安）

## 战队
- 天权信安（2022 成立）
- 40+ 队员：科大 / 航空大 / 北航 / 地大 / 武大 / 华科 等
- 队员分布：绿盟 / 四叶草 / 长亭 / 安恒 / 联通 / 腾讯 / 华为 / 启明星辰

## Web

### ezphp
```
?num=1_11
```
- PHP 弱类型 + 数字下划线绕过
- `1_11` = 111

## Misc

### nan's analysis
- Wireshark 导出 FTP 对象
- 图片末尾附加 shell.zip 加密压缩包
- 零宽隐写

### reindeer game
- 小游戏难度简单
- 通关拿 flag
- `flag{82a2acb6-9803-4936-92db-f1431d90c6d1}`

## Reverse

### easy_python (Python 字节码)
```python
# Python 字节码 (3.x)
# LOAD_CONST 系列 → flag 列表
# FOR_ITER / BINARY_SUBSCR / BINARY_RSHIFT / BINARY_LSHIFT / BINARY_OR / BINARY_AND
flag = [204, 141, 44, 236, 111, 140, 140, 76, 44, 172, 7, 7, 39, 165, 70, 7,
        39, 166, 165, 134, 134, 140, 204, 165, 7, 39, 230, 140, 165, 70,
        44, 172, 102, 6, 140, 204, 230, 230, 76, 198, 38, 175]
for i in range(42):
    flag[i] = (flag[i] >> 5 | flag[i] << 3) & 255
for v in flag:
    print(chr(v), end="")
# flag{ddbae889-2895-44df-897d-2ae30df77b61}
```

## 教学价值
- **Python 字节码** 是 reverse 入门
- **`LOAD_CONST` 序列** 还原初始数组
- **`BINARY_RSHIFT / LSHIFT / OR / AND`** 还原算法
- **PHP 数字下划线** `1_11` = 111（弱类型）
- **零宽隐写** 字符宽度字符隐藏 flag

## 工具
- Wireshark
- Python dis 模块
- IDA + IDAPython
- WinHex / 010 Editor
- 在线零宽解码工具

## 关联
- 同系列还有 #48 2022 春秋杯冬季赛 WP By EDISEC（更多题目）
