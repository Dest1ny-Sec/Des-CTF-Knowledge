---
title: 强网杯2025 Qcalc 解析 - Android Content URI授权+历史.yml反序列化
contest: 强网杯2025
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [Android, ExploitActivity, deeplink, qiangcalc://, content://, history.yml, ContentResolver, openOutputStream, YAML反序列化, divide-by-zero异常, bridge_token, fallback Intent, Uri.encode, FLAG_ACTIVITY_CLEAR_TOP, Arahat0]
attack_chain: 构造deeplink qiangcalc://calculate?expression=Intent.toUri(带bridge_token) → 启动ExploitActivity存fallback → 延时1800ms触发1/0 divide-by-zero → 受害端进入BridgeActivity,授予content://.../history.yml读写并回调ExploitActivity → ExploitActivity写恶意YAML(覆盖包名+ExploitActivity) → 触发2+2让受害端loadHistory()->PingUtil读flag → 550ms后回调读grantedUri获取flag → nc外传
key_payload: content://history.yml ContentResolver授权 + YAML反序列化 + 1800ms divide-by-zero异常触发
one_liner: 强网杯2025 Qcalc:Android Content URI授权链(YAML history.yml)绕过读flag,核心在1800ms divide-by-zero触发BridgeActivity+550ms读grantedUri。
lesson: Android Content URI授权漏洞利用链:deeplink触发+fallback Intent存储+divide-by-zero异常进入BridgeActivity+ContentResolver.openOutputStream写恶意YAML+回调读grantedUri;关键时序1800ms触发+550ms读取窗口;YAML反序列化通过改包名+ExploitActivity实现;flag外传用nc 111.229.198.6 6666。
quality: high
---
