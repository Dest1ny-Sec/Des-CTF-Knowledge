---
title: DASCTF Apr.2023
contest: DASCTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [ecc-key-recover, coppersmith, carmichael-lll, file-overwrite, canary, pwn-stack]
attack_chain:
  - sign1n: RSA e=0x10001 + 特制 kphi 推导
  - ECC: 3 点曲线 y²=x³+ax+b 还原参数
  - babyhash: Carmichael 数 + LLL 矩阵
  - four: 文件菜单覆盖 flag
  - canary 栈溢出
  - ret2flag
key_payload: ECC 曲线还原 + LLL 还原 Carmichael
one_liner: DASCTF 2023 4 月 EDI 战队招新+4 题：ECC 还原/Carmichael LLL/file 覆盖 pwn。
lesson: 当 ECC 给出 3 个点 (x, y) 满足 y²=x³+ax+b mod n，可以列两个方程解 a, b mod n。
quality: high
---

DASCTF 2023 4 月 EDI 战队招新 + 4 道题 WP。

**MISC: Ge9ians_Girl** — Twitter Secret Messages 解密 + 手动补文件头 + 备注 our secret 解密。

**Crypto: sign1n** — RSA 特殊构造。`kphi = e^3 * (WHATF-3) - 1` + `k = kphi // n + 1` + `phi = kphi // k`，inverse 求 d。`m = pow(sign, e, n)` + `tt = pow(2, -e^2 - d^2, n)` 解密。

**Crypto: ECC?** — 3 点曲线还原 + xgcd 恢复。Mersenne 风格 gift 大数。`t1, s1 = C1[0], C1[1]^2 - C1[0]^3` 列方程：
- `kn = (t1-t2)*(s1-s3) - (t1-t3)*(s1-s2)`
- `n = GCD(kn, gift)`
- `a = (s1-s2) * inverse_mod(t1-t2, n) % n`
- `b = (s1 - t1*a) % n`
然后 `E = EllipticCurve(IntegerModRing(n), [a, b])`，`g, u, v = xgcd(e1, e3)`，`M = u*C1 + v*C3`，`M.xy()[0]` 取明文。

**Crypto: babyhash** — 给出 38 个 Carmichael 伪素数 n=1766847064778384329583297500742918515827483896875618958121606201292619891。构造 2x40 矩阵 LLL，M1=2^230, M2=2^145, M[i+2][i+2]=n, M[0][i+2]=gift[i+1], M[1][i+2]=gift[i]^3。LLL 还原 a，转二进制找第一个 0 即 key 长度。

**Pwn: four** — 文件菜单 + canary 栈溢出。
1. `choice(2) edit(0x5fef, './flag\x00\x00'*2*0x5fe)` 写 0x5fef 大小
2. `filee()` 输出到 `output.txt`（覆盖 flag）
3. `choice(3)` 子菜单 1/1/3/'kkk.../output.txt' 创建文件
4. `delete('~3:\x60\x21\x40>@\x70*')` 越界信息
5. `choice(5)` `recvuntil('strange overflow...')` + 0x118 字节 padding + `p64(0x602140)` 改返回地址

有 canary 但题目提示 canary 已知，ret2flag 一气呵成。
