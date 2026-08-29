---
title: HDCTF 2023 WP
contest: HDCTF 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [stego, zsteg, base64, zip-crc, rockyou, bkcrack, 分卷压缩, png-height, wav]
attack_chain:
  - hardMisc: zsteg得到数据解base64
  - flag: HDCTF{wE1c0w3_10_HDctf_M15c}
  - ExtremeMisc: IDAT.png文件尾分离zip
  - Dic.zip用rockyou字典爆破
  - Reverse.piz字节倒序: int((('%02x'%i)[::-1],16)).to_bytes(1,'little')
  - bkcrack明文攻击
  - MasterMisc: 分卷压缩爆破
  - topic.png后有png+wav+png
  - 改png高度得第二段flag
  - flag: NSSCTF{e67d8104-7536-4433-bfff-96759901c405}
key_payload: HDCTF{wE1c0w3_10_HDctf_M15c}
one_liner: HDCTF 2023 3道MISC：zsteg+zip CRC爆破+分卷flag
lesson: zip CRC爆破+明文攻击(bkcrack)组合解分段压缩
quality: high
---

# HDCTF 2023 WP

## 题目信息
- 比赛：HDCTF 2023
- 队伍：rank 10
- 类别：MISC

## 关键攻击链
### 1. hardMisc
- `zsteg` 得到数据
- 解 base64
- flag: `HDCTF{wE1c0w3_10_HDctf_M15c}`

### 2. ExtremeMisc
- IDAT.png 文件尾分离 zip
- Dic.zip 用 rockyou.txt 字典爆破
- Reverse.piz 字节倒序：
  ```python
  zip = open('Reverse.piz', 'rb').read()
  zip_reverse = open('reverse.zip', 'wb')
  zip_reverse.write(b''.join([(int(('%02x'%i)[::-1], 16)).to_bytes(1, 'little') for i in zip]))
  ```
- 爆破密码 + bkcrack 明文攻击（比 archpr 快）

### 3. MasterMisc
- 带密码的分卷压缩
- bandizip 高版本密码爆破
- 三部分 flag：
  - topic.png 后有 png + wav + 第二 png
  - 改第二 png 高度得第二段
  - 第一段：`NSSCTF{e67d8104`
  - 完整：`NSSCTF{e67d8104-7536-4433-bfff-96759901c405}`

## 评分
- quality: high（zsteg + zip CRC + bkcrack + 分卷压缩完整）
