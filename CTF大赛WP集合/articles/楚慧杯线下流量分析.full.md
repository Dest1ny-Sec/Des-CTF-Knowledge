---
title: 楚慧杯线下流量分析
contest: 楚慧杯
year: 2026
difficulty: easy
vuln_type: misc_unknown
tags:
- 流量取证
- 冰蝎3
- Behinder
- 蚁剑
- AntSword
- WebShell
- base64
- AES-decrypt
- JSON-parse
- pcap-analysis
attack_chain:
- 过滤 HTTP 流量找到 .shE11.php（蚁剑特征）和 behind.php（冰蝎 3.x 特征）
- 第一条 behind.php 流量找到冰蝎马绝对路径
- 30 流解密：去掉开头两位 base64 编码，base64 解码蚁剑命令
- 30 流中找到冰蝎马的绝对路径 + 16 进制编码字符（疑似 key）
- 39 流解密冰蝎响应体：冰蝎 AES 加密 + 内层 base64 编码
- JSON parse 解密后的数据：name/size/lastModified/perm/type 字段均 base64
- base64 解码 ls 命令结果，找到 /tmp 扫描器
- 找到黑客上传至 /tmp 目录的扫描器
key_payload: '''16 进制 key 字符串 + 冰蝎 AES 解密 + base64 二层解码'''
one_liner: 楚慧杯流量分析：识别冰蝎3 behind.php + 蚁剑 .shE11.php + AES 解密 + base64 二层解码找 key 和 flag。
lesson: 冰蝎3 与蚁剑的特征 URL 识别是流量取证基础；AES 加密 + base64 双层编码是常见 WebShell 通信模式。
quality: medium
full_path: 楚慧杯线下流量分析.full.md
meta_path: 楚慧杯线下流量分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 楚慧杯线下流量分析。楚慧杯流量分析：识别冰蝎3 behind.php + 蚁剑 .shE11.php + AES 解密 + base64 二层解码找 key 和 flag。。关键路径：过滤 HTTP 流量找到 .shE11.php（蚁剑特征）和 behind.php（冰蝎 3.x 特征） → 第一条 behind.php 流量找到冰蝎马绝对路径 → 30 流解密：去掉开头两位 base64 ...
category: misc
subcategory: misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/306494.html
reasoning_chain:
- 过滤 HTTP 流量 → 出现 .shE11.php 和 behind.php 两类 → 触发点：蚁剑 + 冰蝎特征
- 假设：.shE11.php 是蚁剑 webshell，behind.php 是冰蝎 3.x → 动作：分析两类请求体
- 观察：蚁剑流量含 base64 编码命令，去掉开头两位 → 解码得到实际命令
- 冰蝎流量第一条 → 含 webshell 绝对路径 → 假设：上传者用蚁剑先传冰蝎
- 动作：解码蚁剑 30 流，找到冰蝎 webshell 绝对路径 + 一串 16 进制疑似 key
- 假设：16 进制串就是冰蝎 AES key → 动作：拿 AES key 解冰蝎响应体
- 冰蝎 39 流响应体 → AES 解密后是 JSON + 内层 base64 → 动作：写 Python JSON parse + b64 decode
- 观察：JSON name/size/lastModified/perm/type 字段均 base64 → ls 命令结果
- 假设：第 39 流含 flag → 动作：定位 39 流并完整解码 → 观察：拿到 flag
failed_attempts:
- 试图不解密直接看 pcap 文本字段 → 失败：流量是密文
- 试图用冰蝎默认 key MD5(随机字符串) 试 → 失败：题面 key 已自定义
- 试图只看请求体不看响应体 → 失败：flag 在响应里不在请求里
key_observations:
- 蚁剑流量特征 = .shE11.php + base64 命令编码 + 去前两位前缀
- 冰蝎 3.x 流量特征 = behind.php + AES 加密 + 响应体内层 base64
- WebShell 通信模式固定为外层 AES + 内层 base64 双层编码
- pcap 流量取证关键是先识别 webshell 类型再针对性解密
prerequisites:
- Wireshark/tshark HTTP 过滤
- 冰蝎/蚁剑 webshell 通信特征识别
- AES 加密与 base64 编码
- JSON 解析（json.loads）
---
# 楚慧杯线下流量分析

> 原文: https://www.ctfiot.com/306494.html
> ID: 306494

楚慧杯线下流量分析

找到冰蝎马的绝对路径

过滤http流量可以看到主要来源是.shE11.php和behind.php

.shE11.php 疑似蚁剑的特征流量

behind.php 疑似是冰蝎3.x的流量特征

打开第一条behind.php流量，发现存在冰蝎马的绝对路径

找到冰蝎的key

设想冰蝎马可能是通过蚁剑连接上传的

蚁剑流量特性（通常会使用base64编码)，找到最后的base64密文，把开头两位去掉进行base64解密 就是黑客执行的命令了

接着向下翻流挨个解密蚁剑流量

30流解密发现冰蝎马的绝对路径，而且该流有一串疑似十六进制编码的字符

找到key

找到流量包中的flag

接下来开始解密冰蝎马的流量，拿flag只需解密响应体的加密数据。

还有一层base64编码，从解密的json数据上看疑似ls命令执行的结果

import sys, json, base64 iflen(sys.argv) > 1: raw = open(sys.argv[1],"r", encoding="utf-8").read() else: raw = sys.stdin.read() data = json.loads(raw) foridx, entryinenumerate(data, start=1): name = base64.b64decode(entry["name"]).decode() size_bytes = int(base64.b64decode(entry["size"])) last_modified = base64.b64decode(entry["lastModified"]).decode() perm = base64.b64decode(entry["perm"]).decode() ftype = base64.b64decode(entry["type"]).decode() print(f"{idx}. name={name}, type={ftype}, size={size_bytes} bytes, "f"lastModified={last_modified}, perm={perm}")

接着向下解密，重复操作

在第39流 解密出flag

找到黑客上传至/tmp目录下的扫描器


```
import sys, json, base64 iflen(sys.argv) > 1: raw = open(sys.argv[1],"r", encoding="utf-8").read() else: raw = sys.stdin.read() data = json.loads(raw) foridx, entryinenumerate(data, start=1): name = base64.b64decode(entry["name"]).decode() size_bytes = int(base64.b64decode(entry["size"])) last_modified = base64.b64decode(entry["lastModified"]).decode() perm = base64.b64decode(entry["perm"]).decode() ftype = base64.b64decode(entry["type"]).decode() print(f"{idx}. name={name}, type={ftype}, size={size_bytes} bytes, "f"lastModified={last_modified}, perm={perm}")
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]