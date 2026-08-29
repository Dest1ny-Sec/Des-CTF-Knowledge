---
title: UKFC2024 RCTF WP
contest: UKFC2024 RCTF (ctfiot)
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [regexp_blind_sql, jwt_forge, rc4, double_pinyin, usb_hid, code_block_loss]
attack_chain: SQL 注入 regexp 盲注爆破 flag → JWT 篡改 have_lovers=true 取 key2 → RC4 解密 (rot 6 隐藏+密钥 thisisyoursecretke) → 双拼解码 USB 流量键盘输入
key_payload: '||love_key regexp '^RCTF{ + username===my_lover.username + love_time===my_lover.love_time + 双拼 → 快来打夺旗赛吧
one_liner: 一个被严重破坏格式的 RCTF 杂项 WP，三个 key 拼出：regexp 盲注+JWT 假 lover+RC4+双拼 USB。
lesson: CTF 杂项拼盘类题目往往是"分别攻击 N 段"再拼接 flag，攻击链断点往往是社会工程（双拼解谜、双拼密码）。
quality: low
---
