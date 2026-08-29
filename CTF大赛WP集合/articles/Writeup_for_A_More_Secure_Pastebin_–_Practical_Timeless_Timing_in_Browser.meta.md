---
title: Writeup for A More Secure Pastebin – Practical Timeless Timing in Browser
contest: TQLCTF (More Secure Pastebin)
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [mongo_regex_search, timing_side_channel, network_measurement, date_now_ms_diff, fetch_parallel_race, cors_proxy, pastebin_blind_search, dns_amplification, regex_perf_amplify]
attack_chain: 目标 /admin/searchword?word= 用 MongoDB RegExp 大小写不敏感搜索 + 5 条 .limit 排序 + 后端 fetch 速度反映匹配数 → 攻击者 fetch 两路径 word=flag{aa 与 word=flag{ab 用 Promise.all 看哪个先返回 (Date.now() ms 差) → 多次迭代差分聚合 (timing) 字符爆破 → 浏览器用 script Date.now() 测量 → fetch+report XHR vps 收集 → CORS proxy 443 + 1443 双端口绕过
key_payload: word=flag{aa / word=flag{ab / Date.now() 测量 fetch ms / Promise.all([p1,p2]).then(1/-1) / timing() 循环 30 次 sleep(50)
one_liner: TQLCTF More Secure Pastebin 实战时间盲注绕过，用浏览器 fetch + Date.now() 测 MongoDB RegExp 搜索响应差，通过 Promise.all 加速盲注爆破 flag{...}。
lesson: MongoDB RegExp 是无锁时间盲注的放大器；浏览器 Date.now() 微秒级精度足够做字符级爆破；fetch race (Promise.all([p1,p2])) 是 network measurement 的标配。
quality: high
---
