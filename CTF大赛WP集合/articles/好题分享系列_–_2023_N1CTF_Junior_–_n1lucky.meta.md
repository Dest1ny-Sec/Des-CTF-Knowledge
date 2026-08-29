---
title: 2023 N1CTF Junior n1lucky - LLL格密码恢复secret
contest: 2023 N1CTF Junior (Nu1L)
year: 2023
difficulty: hard
vuln_type: lattice
tags: [Nu1L, N1CTF, LLL, 格密码, CRT中国剩余定理, multi-prime, 30-bit_prime, 888-bit_prime, 4096-bit_secret, socketserver, POW, hashcash]
attack_chain: 解决sha256(XXXX+proof[4:]) POW → 20次交互拿20对(r_i*secret mod p_i) → 因secret 4096-bit远大于p_i 888-bit需5组CRT合并 → 因r_i仅30-bit prime造LLL格(Delta=2^(4096+30)+CRT项+prodp) → LLL规约首行提取r_i → GCD验证r_0∩r_1=r_2*r_3*r_4
key_payload: LLL(6×6) + Delta=2^(4096+30) + CRT合并 + GCD校验
one_liner: Nu1L 30-bit r乘4096-bit secret模888-bit p,20次机会用5组CRT+LLL恢复secret。
lesson: 30-bit与4096-bit数量级悬殊 → 30-bit部分可视为"短向量"通过LLL格密码规约恢复;secret远大于p所以必须多组CRT合并;每组res_i*Pi[i]*Qi[i]填最后一列+Delta=2^(4096+30)在对角+prodp末行末列,LLL后首行除Delta得所有r_i;GCD交叉验证r_0∩r_1=r_2*r_3*...*r_{n-1}。
quality: high
---
