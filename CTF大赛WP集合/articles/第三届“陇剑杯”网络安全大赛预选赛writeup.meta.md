---
title: 第三届"陇剑杯"网络安全大赛预选赛writeup
contest: 第三届陇剑杯预选赛
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [陇剑杯预选赛, RC5-32/12/b, Z3多约束, popcount, XXTEA, pickle反序列化, Wazuh应急, PTH哈希传递, PSEXESVC]
attack_chain: RC5-32/12/b→Z3约束求解(22字节flag+popcount)→XXTEA解密→pickle反序列化CHIKAWA→Wazuh日志分析
key_payload: "flag{7ac1d3e59f0b2468};flag{cbee3251-9cff-4542-bf15-337bb8df7f3f};RC5-32/12/b;Z3多约束+popcount;XXTEA;PSEXESVC"
one_liner: 第三届陇剑杯预选赛（另一版writeup）：RC5+Z3+XXTEA+pickle+Wazuh（与同篇WP同主题重复）
lesson: 同一比赛不同作者写的writeup会有不同侧重点，可互为补充
quality: medium
---

# 第三届"陇剑杯"网络安全大赛预选赛writeup

**赛事**：第三届陇剑杯预选赛（2025，另一版writeup）

**与同篇WP主题重复**：
- RC5-32/12/b 完整实现
- Z3约束求解
- XXTEA解密
- pickle反序列化CHIKAWA
- Wazuh应急响应分析

**两个flag**：
- `flag{7ac1d3e59f0b2468}`
- `flag{cbee3251-9cff-4542-bf15-337bb8df7f3f}`

**质量评估**：中（与同篇WP主题重复，可互为补充）
