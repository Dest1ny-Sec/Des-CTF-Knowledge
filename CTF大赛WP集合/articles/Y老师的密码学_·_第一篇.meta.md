---
title: Y 老师的密码学 · 第一篇 (狼组)
contest: corctf 2022 (狼组复现)
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [rsa_fizzbuzz_oracle, chosen_ciphertext_blinding, multivariate_quadratic_secret_sharing, gf_matrix_equation, vigenere_with_pt_plus_key, lsbit_oracle_extended, binary_search_padding, wiener_attack, dbdh, half_gcd_2k_bit]
attack_chain: fizzbuzz100:RSA + FizzBuzz oracle (Fizz % 3 / Buzz % 5) → 选择密文盲化 X=907 → Y = c * X^e mod n → 盲化解密 + Fizz/Buzz 判断 / eyes:Multivariate Quadratic Secret Sharing conv(1..7) → fn(x)=x.T*A*x + B.T*x + C → 7 个 L 值代数化简求 c / cbc:维吉尼亚 CBC padding X (klen=16) → ct 拆 16 字节块 + sub_key(prev_block) → 把 pt+key 当维吉尼亚密文在线破解 / fizzbuzz101:RSA + LSB oracle 101 版本（无回显）→ binary_search(k//2, k) + 迭代乘 5 反向 binary_search 收敛
key_payload: flag = ct * inverse(w, n) % n (w=907 prime 10-bit) / c = (L[6]-(L[2]+L[4]+L[5]-2*(L[0]+L[1]+L[3]))-(L[0]+L[1]+L[3])) % p / corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}
one_liner: 狼组出品的 corctf 4 道密码学复现：fizzbuzz100/101 RSA + 改进 LSB oracle 盲注 + 多元二次 Secret Sharing 代数化简 + 维吉尼亚 CBC 拆 key 在线破解。
lesson: FizzBuzz 模 3/5 oracle + 选择密文盲化是 RSA 经典侧信道；Multivariate Quadratic Secret Sharing 在 conv 矩阵下用 7 个点就能代数化简求常数 c。
quality: high
---
