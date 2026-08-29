---
title: WMCTF WriteUp (ChaMd5 Venom)
contest: WMCTF
year: 2021
difficulty: hard
vuln_type: crypto_oracle
tags: [aes_cbc, ocb_mode, arbitrary_encrypt, pmac_forgery, lattice_lll, bkz_22, sage_small_roots, rabin_chain, lwe_qary, knapsack_cvp, ocb_oracle]
attack_chain: v2x_misc.conf AES-CBC 16 字节密码 ljust\x00 → OCB 模式 Arbitrary_encrypt oracle 重放 + my_pmac 标签伪造 (xor_block(tag, pmac_admin)) → 32 元子集和问题 BKZ-22 求最短向量 → RSA p^5 Coppersmith small_roots X=2^369 → Rabin 链 c^(1/2^i) mod p 穷举 2^13 候选 → LWE q=2^24 格密码 to_mat 16 维 + Matrix(F).solve_left 求解向量
key_payload: pmac_admin = my_pmac(bytearray(b'from admin')) / M = matrix(ZZ, m); v = M.BKZ(blocksize=22) / sympy.root(x, 2) 取整数
one_liner: WMCTF 早期 ChaMd5 Venom 战队杂烩 WP，AES-CBC 密码爆破 + OCB 模式 oracle 标签伪造 + 32 元子集和 + Rabin 链解 e=4096 + LWE 格密码，多道密码学题经典攻击模板。
lesson: OCB 模式 arbitrary_encrypt oracle 可直接伪造 PMAC 标签；子集和+super-increasing+前几位已知可用 BKZ-22 而非 LLL。
quality: high
---
