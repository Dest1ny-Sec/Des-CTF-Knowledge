---
title: ASIS CTF Quals 2022
contest: ASIS CTF
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [BinomialExpansion, enc % pubkey^2 // pubkey, LatticeHashCollision, chaffymasking, fixed_p DLP, CRT Joye-Libert, EC离散对数smallfactor, EC Pohlig-Hellman+CRT, ratio nearby_rational, LSB_attack, openssl_pbkdf2, Xor256爆破]
attack_chain:
  - Binomial: enc % pubkey^2 // pubkey 得明文（(a+b)^2 拆解）
  - Lattice hash collision: chaffymasking 1024 bit salt 漏洞, masked_flag 直接 hex 解码
  - Fixed p DLP: p 已知, g 已知, send (1-p) 反推 x 满足 m*G = x*G
  - Joye-Libert CRT: 4 组 (n,s) + c, n>>268 拆 a+b, a*b, GF(2^134) 算 (F(c)^a / F(s)^a).log()
  - Nested EC DLP: y1=0, y2=i 控制曲线参数, Pohlig-Hellman small factor 走 CRT 拼 fullres
  - Nearby rational: (y-x)/n 取 2^64 逼近, 求 phi
  - LSB: 40 字符 8 个候选,逐位 discard 收窄到唯一解
  - Xor 256 爆破: wormrep.klr.enc1 字节 XOR
  - openssl aes-256-cbc -pbkdf2 -a -d -salt: U2FsdGVkX18 + 20字节 salt
key_payload: 'enc % n^2 // n / chaffymasking / 1-p DLP / Joye-Libert CRT / Pohlig-Hellman small factor CRT / nearby_rational 2^64 / LSB discard / openssl pbkdf2'
one_liner: ASIS CTF Quals 2022 — 8 道 Crypto 集锦：Binomial 展开 + Lattice 哈希碰撞 + Fixed p DLP + Joye-Libert CRT 还原 + 嵌套 EC Pohlig-Hellman + nearby_rational 求 phi + LSB discard 收窄 + openssl pbkdf2。
lesson: ASIS 风格是全覆盖所有方向的高质量 Crypto;Joye-Libert 是教科书方案;Pohlig-Hellman 小因子+CRT 拼是 EC DLP 标准法;nearby_rational(max_denominator=2^64) 是连分数在 phi 恢复的应用。
quality: high
---

# ASIS CTF Quals 2022

## 速读
ASIS 2022 Quals — 8 道 Crypto 集合 (从经典到高级全覆盖)。

## Crypto 题目列表

| # | 题目 | 技术 | flag |
|---|------|------|------|
| 1 | Binomial Expansion | (a+b)^2 拆解 | ASIS{8!N0miaL_3XpAn5iOn_Us4G3_1N_cRyp7o_9rApHy!} |
| 2 | Lattice hash collision | chaffymasking 漏洞 | ASIS{Lattice_based_hash_collision_it_was_sooooooooooooooo_easY!} |
| 3 | Fixed p DLP | 1-p 发送 | ASIS{fiX3d_pOIn7s_f0r_d!5Cret3_l0g4riThmS!} |
| 4 | Joye-Libert CRT | 4 组参数 | ASIS{N3w_CTF_nEw_Joye_Libert_CrYpt0_5} |
| 5 | Nested EC DLP | Pohlig-Hellman + CRT | ASIS{(e$l6LH_JfsJ:~<}1v&} |
| 6 | Nearby rational | 连分数 | ASIS{N3s7Ed_DLP_089823341e928d6d87f0e442245d5a765833b575} |
| 7 | LSB attack | 40字符 discard | ASIS{Pr!v4t3_5E7_iNTeRS3c710N_p4St_Or_Pr3sEnT} |
| 8 | Xor 256 | wormrep.klr.enc1 | ASIS{N07_@ll_v!ru535_@r3_AS_8@d_a5_cov!d} |
| 9 | openssl pbkdf2 | U2FsdGVkX18 salt | ASIS{pgm_1M4gE_f0Rma7_ManUpL4T!On!} |

## 关键技术

### Binomial Expansion
```python
print(long_to_bytes(enc % pubkey**2 // pubkey))
```

### Joye-Libert CRT
```python
def solve_bytes(n, s, c):
    k = 134
    pd = n >> (2*k)
    sm = (n >> k) % 2**k
    a, b = var('a b')
    soln = solve([a+b==sm, a*b==pd], a, b, solution_dict=True)[0]
    F = GF((int(soln[a]) << k) + 1)
    return long_to_bytes((F(c)**soln[a]).log(F(s)**soln[a]))
```

### Nested EC
```python
order = G.order()
small = factor_trial_division(order, 2**24)[-1][0]
mod = order // small
res = discrete_log(small * mG, small * G, mod, operation='+')
fullres = crt([res, fullres], [mod, fullmod])
```

### Nearby rational
```python
ratio = (Integer(y-x)/n).n().nearby_rational(max_denominator=2**64)
phi = int(2*n + (y-x)/ratio - 6) // 3
```
