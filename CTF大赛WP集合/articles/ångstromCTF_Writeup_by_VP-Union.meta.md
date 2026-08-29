---
title: ångstromCTF Writeup by VP-Union
contest: ångstromCTF
year: 2023
difficulty: mixed
vuln_type: crypto_rsa
tags: [caesar-shift, RSA-Leak-pmqm, RSA-homomorphic, fake_psi, one_encoding, zero_encoding, fmt-string, jinja2-SSTI, BEAM-bytecode]
attack_chain: Caesar 26 shift 爆破/ RSA 给 (p-2)(q-1) 和 (p-1)(q-2) 两个方程 z3 解出 p q 算 (p-1)(q-1) phi/RSA homomorphic 给 5-bit X prime 选 X 让 Y = c*X^e mod n 通过解密 oracle 拿到 Y^d = m*X mod n 枚举 i 让 (n*i + m*X) / X 含 actf/fake_psi + one_encoding/zero_encoding: x=1<<64 + 1 即 65 位 1 / y=1<<64 即 64 位 1 满足 one_encoding(x) ∩ zero_encoding(y) = ∅
key_payload: caesar: c = "rtkw{cf0bj_czbv_nv'cc_y4mv_kf_kip_re0kyvi_uivjj1ex_5vw89s3r44901831}" shift=12 → actf{lo0ks_like_we'll_h4ve_to_try_an0ther_dress1ng_5ef89b3a44901831}
one_liner: VP-Union ångstromCTF 2023 第二份 WP，crypto 比重更大，含 RSA 二方程解、homomorphic oracle、伪 set 交为空 trick。
lesson: RSA 二方程 (p-2)(q-1) + (p-1)(q-2) + n 可解 p q；homomorphic RSA 选 X prime 让 Y = c*X^e mod n 通过 oracle 拿到 m*X mod n；伪 set 交为空需要 one_encoding(x) 与 zero_encoding(y) 完全互斥。
quality: high
---

# ångstromCTF 2023 Writeup by VP-Union（第二份）

## 概览
VP-Union 战队另一份 2023 ångstromCTF WP，crypto 比重更高，覆盖 Caesar 爆破、RSA 二方程、RSA 同态、伪集合交集 trick。

## CRYPTO 类

### Caesar shift
```python
c = "rtkw{cf0bj_czbv_nv'cc_y4mv_kf_kip_re0kyvi_uivjj1ex_5vw89s3r44901831}"
for shift in range(26):
    plain = ''
    for i in c:
        if i in string.ascii_lowercase:
            plain += chr(((ord(i) - 97 - shift) % 26)+97)
        else:
            plain += i
# shift=12 → actf{lo0ks_like_we'll_h4ve_to_try_an0ther_dress1ng_5ef89b3a44901831}
```

### RSA 二方程 (p-2)(q-1) + (p-1)(q-2) 泄露
- 给出 n, e, c, A=(p-2)(q-1), B=(p-1)(q-2)
- z3 解 p, q：
  ```python
  S.add(p*q==n)
  S.add((p-2)*(q-1)==A)
  ```
- 拿到 p, q 后算 phi = (p-1)*(q-1)，`m = pow(c, gmpy2.invert(e, phi), n)` 解密
- flag: `actf{tw0_equ4ti0ns_in_tw0_unkn0wns_d62507431b7e7087}`

### RSA 同态 + 解密 oracle
- 加密后提供解密 oracle，但禁止 c=m 或 b"actf{" in plaintext
- 选 5-bit prime X，构造 `Y = c * X^e mod n`
- 通过 oracle 拿到 `Y^d = m*X mod n`
- 枚举 i 找 `(n*i + Y^d) / X` 含 "actf"
- flag: `actf{rs4_is_sorta_homom0rphic_50c8d344df58322b}`

### fake_psi + one_encoding/zero_encoding
- `fake_psi(a, b) = [i for i in a if i in b]`（伪 set 交集）
- `one_encoding(x, n)`: 提取 x 二进制中所有 1 位的值
- `zero_encoding(x, n)`: 提取 x 二进制中所有 0 位的 x | 1 值
- 条件：`fake_psi(one_encoding(x, 64), zero_encoding(y, 64)) == 0 and x > y and x > 0 and y > 0`
- 关键：x=65 位 1（即 `int('1'*65, 2)`），y=64 位 1
- flag: `actf{se3ms_pretty_p0ssible_t0_m3_7623fb7e33577b8a}`

## PWN/RE/WEB
与第一份相同：slack fmt 字符串 `%*c$hn` 改 rbp 跳 one_gadget，Bananas Elixir BEAM 反编译，brokenlogin jinja2 SSTI。

## 经验提炼
- 二方程解 RSA 比单方程 (p+q) 泄露更隐蔽，但同样可通过 z3 解
- RSA 同态：`E(m1) * E(m2) mod n = E(m1*m2 mod n)`，可用 oracle 反推明文
- `fake_psi` 用 list comprehension 模拟 set 交集，O(n²) 性能但故意隐藏语义
- one_encoding/zero_encoding 的"位权编码"设计巧妙，让 set 交集为空要求 x 是 y 的超集但相邻
- Caesar 26 爆破时若 flag 含 `'` 和 `_` 要保留原样
