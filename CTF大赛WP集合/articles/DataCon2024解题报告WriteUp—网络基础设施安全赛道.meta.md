---
title: DataCon2024解题报告WriteUp—网络基础设施安全赛道
contest: DataCon 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [dns, open-resolver, isc-bind, geoip2, libjson, features, attack]
attack_chain:
  - 题目1: DNS开放解析器识别+攻击利用
  - 9.16/9.18 Bind版本
  - 胶水缓存存在/弃用
  - 陈旧缓存开启/弃用
  - --disable-silent-rules（可选/不可选）
  - --enable-backtrace（可选/不可选）
  - --enable-shared
  - --enable-native-pkcs11
  - --with-geoip2 功能失效但可选
  - --with-libjson 功能失效但可选
key_payload: --with-geoip2 --with-libjson  # Bind 配置特征
one_liner: DataCon2024 DNS开放解析器识别：Bind编译选项+功能版本
lesson: Bind编译参数+版本特征可用于识别DNS开放解析器
quality: medium
---

# DataCon2024解题报告WriteUp—网络基础设施安全赛道

## 题目信息
- 比赛：DataCon 2024
- 方向：网络基础设施安全
- 冠军：中科院信工所"ddddns"战队

## 关键攻击链
### 题目 1：DNS 开放解析器识别与攻击利用
- Bind 版本：9.16 / 9.18
- 胶水缓存：存在/弃用
- 陈旧缓存：开启/弃用
- 编译选项对比表：
  - `--disable-silent-rules`（9.16 可选 → 9.18 不可选）
  - `--enable-backtrace`（可选 → 不可选）
  - `--enable-shared`（可选 → 不可选）
  - `--enable-native-pkcs11`（可选 → 不可选）
  - `--with-geoip2`（功能失效但可选 → 不可选）
  - `--with-libjson`（功能失效但可选 → 不可选）

## 评分
- quality: medium（157 行，主要是版本+功能对比表，缺具体攻击利用细节）
