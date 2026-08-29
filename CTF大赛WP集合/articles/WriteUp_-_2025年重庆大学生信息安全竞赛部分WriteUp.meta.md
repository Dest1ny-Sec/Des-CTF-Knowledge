---
title: WriteUp | 2025年重庆大学生信息安全竞赛部分 WriteUp
contest: 2025 重庆大学生信息安全竞赛
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [php_include_png, base64_path_concat, strstr_filter_bypass, xor_static, ctf_newbie, classic_crypto_xor, file_param_truncation]
attack_chain: 题 1 (WEB):$_GET['file']=base64_decode → strstr 过滤 "./" → include 'upload/'.$file.'.png' → 通过 file= 截断加 .png 路径 → flag{th1s1sf14g} / 题 2 (RE):C 字符串 "cjfor~c=~?|v &ti" → a[i]=b[i]^(i+5) for i in range(15) → puts(a) 解明文
key_payload: php://filter/../upload/ + base64(file) 触发 include 'upload/...png' / xor 密钥 (i+5) 起始 5
one_liner: 2025 重庆大学生信息安全竞赛入门题 2 道：PHP include base64 路径拼接 + strstr 黑名单 + .png 后缀；C 字符串 15 字节异或 (i+5) 还原明文。
lesson: 入门级题：strstr 单次匹配可双写 (././)、大小写、URL 编码绕过；C 字符数组 XOR 密钥是动态 (i+k) 而非常数。
quality: low
---
