---
title: ACTF 2026 WriteUp By F1ux
contest: ACTF
year: 2026
difficulty: hard
vuln_type: crypto_rsa
tags: [inverse pow, 128-bit定点扫描, Decimal高精度, pydoc.builtin不拦截, help('secret')泄flag, 低指数RSA广播, QuadraticField虚数域, max_order, decimal_part_of_sqrt, TenSEAL CKKS, 同态计算rank, Galois key旋转, sign近似, DOSEMU2, DJ64 loader, comcom64 stubless, STFLG1_NO32PL|SHM_EXCL|SHM_NEW_NS, VNC上傳hex+decoder, /usr/bin/cat SUID]
attack_chain:
  - Crypto1 inverse_pow: 128-bit 定点 C helper 扫描 + Decimal Python 复核
  - Crypto2 jail: eval 没禁 builtins, help('secret') 触发 pydoc DATA 区打印 secret.py FLAG
  - Crypto3 低指数 RSA 广播: Pand√ra 给 Sage, 反推 p ≡ 3 mod 4
  - Crypto4: QuadraticField(-p, 'w') + max_order OK, Oq = K.order([1, (Δq+q*K.gen())/2])
  - 输出 (A>>360, B, decimal_part_of_sqrt(p*q^2)) 反推 45 字节 token
  - Crypto5 Arrange in Ascending: TenSEAL CKKS 加密 128 元素 Base, 同态计算 rank
  - round(answer[i]) == sorted(Base).index(Base[i]) → 用 Galois key 旋转
  - rank = #j < i + (#j > i, sign 区分) - 1, 加法+密文乘密文+rescale
  - Misc Farthest2026: DOSEMU2 DOS 环境 cat 加 SUID, dos 不可直接读 /flag
  - 走 DJ64 loader: 构造 R.COM 调 int 0e6h al=60h ah=01h dx=0005h
  - 改 R.ELF 为 fake MZ 头 (0x86=STFLG1_NO32PL|SHM_EXCL|SHM_NEW_NS)
  - dj64init_once() 内 fork+execve /usr/bin/cat /flag 重定向到 /home/dos/.dosemu/drive_c/OUT.TXT
  - VNC 上传: copy con A.TXT (hex) + g.com decoder + R.ELF
key_payload: 'TenSEAL CKKS rank 同态 / QuadraticField + decimal sqrt 反推 / DJ64 STFLG1_NO32PL|SHM_EXCL|SHM_NEW_NS / SUID cat / DOSEMU2'
one_liner: ACTF 2026 — 5 道 Crypto (inverse_pow + jail help('secret') + 低指 RSA 广播 + QuadraticField+decimal sqrt + TenSEAL CKKS 同态 rank) + Misc Farthest2026 DOSEMU2 DJ64 loader + SUID cat。
lesson: pydoc DATA 区会打印模块源 (help('secret') 非预期读 flag);TenSEAL CKKS 即使无 secret key 也可同态计算（仅用 public+galois）;DOSEMU2 DJ64 loader 是非预期 host exec 入口;STFLG1_NO32PL+SHM_NEW_NS 组合是关键。
quality: high
---

# ACTF 2026 WriteUp By F1ux

## 速读
F1ux 战队 (4th place) — 5 道 Crypto + 1 道 Misc Farthest2026。

## Crypto

### inverse pow
- 128-bit 定点 C helper 扫描
- Python Decimal 高精度复核

### jail 非预期
- eval 没禁 builtins
- `help('secret')` 触发 pydoc DATA 区打印 `secret.py` 中 FLAG

### 低指数 RSA 广播
- `Pand√ra` Sage 脚本
- p ≡ 3 mod 4 条件过滤

### QuadraticField token 还原
- `K = QuadraticField(-p, 'w')`
- `Oq = K.order([1, (Δq+q*K.gen())/2])`
- 输出 `(A>>360, B, decimal_part_of_sqrt(p*q^2))` 反推 45 字节 token

### TenSEAL CKKS Arrange in Ascending
- `ctx.coeff_mod_bit_sizes=[50]+[40]*12+[50]`, `global_scale=2**40`
- 128 元素 Base 加密,需返回 `round(answer[i]) == sorted(Base).index(Base[i])`
- 用 public key + galois key 同态计算每个元素 rank
- rank = (#j<i) + sign 区分 (#j>i)

## Misc Farthest2026
- DOSEMU2 + DJ64 loader
- `/usr/bin/cat` 加 SUID, dos 用户不可直接读
- `unix /usr/bin/cat /flag` 被白名单挡
- 走 DJ64 loader: `R.COM` 调 `int 0e6h al=60h ah=01h dx=0005h`
- 改 R.ELF fake MZ 头 (0x86 = `STFLG1_NO32PL | SHM_EXCL | SHM_NEW_NS`)
- `dj64init_once()` 内 fork+execve `/usr/bin/cat /flag`
- VNC 上传: `copy con A.TXT` (hex) + `g.com` decoder
