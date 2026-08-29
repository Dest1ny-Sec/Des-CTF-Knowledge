---
title: 【云境】ThermalPower 工控仿真场景
contest: 云境
year: 2024
difficulty: easy
vuln_type: web_unknown
tags: [工控仿真, AES-CBC-key-base64, JSESSIONID-CUSTOMSESSID-cookie-replay, ThermalPower, ICS-scenario]
attack_chain: 1. AES CBC key=QZYysgMYhG6/CzIJlVpR2g== (Base64) /2. Cookie: JSESSIONID + CUSTOMSESSID 8A365128F3FD7662310296AD67463C26 /3. 抓包重放 chenhua/chenhua@0813 登录 /4. flag01 33565d1e-04e9-4efb-b1b9-f70641ae489c /5. flag02 63cd8cd5-151f-4f29-bdc7-f80312888158
key_payload: AES key QZYysgMYhG6/CzIJlVpR2g==  chenhua/chenhua@0813  flag 33565d1e
one_liner: 云境 ThermalPower 工控仿真场景，AES-CBC 加密 + JSESSIONID 重放 + 弱口令登录拿 flag。
lesson: 工控仿真场景常泄露 AES key base64；JSESSIONID + CUSTOMSESSID 双 cookie 是仿真平台特征；chenhua/chenhua@0813 是默认弱口令。
quality: medium
---

# 【云境】ThermalPower 工控仿真场景

## 概览
云境 ThermalPower 工控仿真场景 WP，AES-CBC 加密 + JSESSIONID cookie 重放。

## 关键信息

### AES 参数
```
algMode = CBC
key = QZYysgMYhG6/CzIJlVpR2g==
algName = AES
```

### 抓包信息
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
Cookie: JSESSIONID=8A365128F3FD7662310296AD67463C26;
        CUSTOMSESSID=8A365128F3FD7662310296AD67463C26
```

## 攻击链

### Stage 1: 抓包分析
- 抓取登录请求
- 发现 JSESSIONID 和 CUSTOMSESSID 两个 cookie

### Stage 2: 重放登录
- 弱口令 `chenhua/chenhua@0813`
- 替换 cookie 重放

### Stage 3: 拿 flag
- flag01: `flag{33565d1e-04e9-4efb-b1b9-f70641ae489c}`
- flag02: `flag{63cd8cd5-151f-4f29-bdc7-f80312888158}`

## 经验提炼
- 工控仿真场景常泄露 AES key base64
- JSESSIONID + CUSTOMSESSID 双 cookie 是仿真平台特征
- chenhua/chenhua@0813 是默认弱口令
- AES-CBC key 16/24/32 字节
- 工控场景常涉及热力、电力系统仿真
- 抓包重放是工控入门套路
- Cloud scenarios (云境) 是永信至诚的工控仿真平台
- ThermalPower = 热电力
- CUSTOMSESSID 是定制化会话 ID
- AES 加密 cookie 中数据需先 base64 解 key
