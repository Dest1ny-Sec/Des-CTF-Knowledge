---
title: 美团CTF-WriteUp
contest: 美团CTF
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags: [ChaMd5-Venom, PHP-OOP, call_user_func, phar-deserialize, file_put_contents, time-blind-sqli, RSA-low-bits, babyrop-pwn, brute-md5, AES-CBC]
attack_chain:
- Web PHP反序列化:abstract Users {db, verify_user, check_user_exist, add_user, eval} + User {func, param, eval: (func)(param)}
- phar.phar元数据反序列化触发eval
- payload:new User("call_user_func", array("Logs","log"))触发file_put_contents
- 用php://filter或base64前缀绕'<?php exit();'退出
- 时间盲注:b"#G.5~1s" + i + "aa",time.time()测时间15-12s=正确
- RSA低位爆破:n末18位+前18位+3位str(i,j,k)+factordb
- P=p拼接p+q,PP=P+Q,QQ=Q+P,n=PP*QQ
- babyrop ret2libc one_gadget
- AES-CBC解密
key_payload: PHP反序列化 + 时间盲注 + RSA低位爆破
one_liner: 美团CTF WriteUp,涵盖ChaMd5 Venom招新文+PHP OOP反序列化(Users/User/Welcome/File/Logs+call_user_func+phar触发)+时间盲注+RSA低位爆破+ret2libc babyrop。
lesson: PHP OOP反序列化是Web经典题型,phar元数据是稳定反序列化触发点;时间盲注+1字节差是密码攻击实用技术;RSA拼接+低位爆破是新型RSA攻击面。
quality: high
---
