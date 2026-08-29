---
title: 楚慧杯线下流量分析
contest: 楚慧杯
year: 2026
difficulty: easy
vuln_type: misc_unknown
tags: [流量取证, 冰蝎3, Behinder, 蚁剑, AntSword, WebShell, base64, AES-decrypt, JSON-parse, pcap-analysis]
attack_chain:
  - 过滤 HTTP 流量找到 .shE11.php（蚁剑特征）和 behind.php（冰蝎 3.x 特征）
  - 第一条 behind.php 流量找到冰蝎马绝对路径
  - 30 流解密：去掉开头两位 base64 编码，base64 解码蚁剑命令
  - 30 流中找到冰蝎马的绝对路径 + 16 进制编码字符（疑似 key）
  - 39 流解密冰蝎响应体：冰蝎 AES 加密 + 内层 base64 编码
  - JSON parse 解密后的数据：name/size/lastModified/perm/type 字段均 base64
  - base64 解码 ls 命令结果，找到 /tmp 扫描器
  - 找到黑客上传至 /tmp 目录的扫描器
key_payload: '16 进制 key 字符串 + 冰蝎 AES 解密 + base64 二层解码'
one_liner: 楚慧杯流量分析：识别冰蝎3 behind.php + 蚁剑 .shE11.php + AES 解密 + base64 二层解码找 key 和 flag。
lesson: 冰蝎3 与蚁剑的特征 URL 识别是流量取证基础；AES 加密 + base64 双层编码是常见 WebShell 通信模式。
quality: medium
---

# 楚慧杯线下流量分析

**来源**: ctfiot.com ID 306494
**难度**: 入门

## 流量识别

### 关键 URL
- `.shE11.php` - 蚁剑（AntSword）特征流量
- `behind.php` - 冰蝎 3.x 特征流量

## 解题步骤

### Step 1: 找冰蝎马绝对路径
打开第一条 `behind.php` 流量，路径字段包含冰蝎马绝对路径。

### Step 2: 找 key
设想冰蝎马通过蚁剑连接上传。蚁剑流量用 base64 编码：
- 找最后 base64 密文
- 去掉开头两位
- base64 解码 = 黑客执行的命令

30 流解密后找到冰蝎马绝对路径 + 16 进制编码字符（疑似 key）。

### Step 3: 解密冰蝎流量
- 拿 key 解密冰蝎响应体
- 内层还有 base64 编码
- 双重解码

### Step 4: 解码 JSON
```python
import sys, json, base64

raw = open(sys.argv[1], "r", encoding="utf-8").read()
data = json.loads(raw)
for idx, entry in enumerate(data, start=1):
    name = base64.b64decode(entry["name"]).decode()
    size_bytes = int(base64.b64decode(entry["size"]))
    last_modified = base64.b64decode(entry["lastModified"]).decode()
    perm = base64.b64decode(entry["perm"]).decode()
    ftype = base64.b64decode(entry["type"]).decode()
    print(f"{idx}. name={name}, type={ftype}, size={size_bytes} bytes, "
          f"lastModified={last_modified}, perm={perm}")
```

### Step 5: 39 流解出 flag
重复 base64 + AES 解密流程，第 39 流解出 flag。

## 黑客活动
- 通过蚁剑上传冰蝎马
- 利用冰蝎 3.x 执行命令
- 上传 /tmp 扫描器
- 持续渗透（ls / 找敏感文件）

## 评价
入门级流量取证，考察 WebShell 工具识别（蚁剑+冰蝎）+ AES 解密 + JSON 解析 + base64 多层编码。适合作为应急响应基础训练。
