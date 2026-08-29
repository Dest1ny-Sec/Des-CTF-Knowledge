---
title: 矩阵杯 2024 战队攻防对抗赛初赛 Writeup
contest: 矩阵杯
year: 2024
difficulty: medium
vuln_type: reverse
tags: [packpy, UPX, pyinstaller, pycdc, base58, zlib, marshal, IDEA, mod-65537, keyExpend, pyd, Python-3.10]
attack_chain:
  - 1.1 packpy: UPX 加壳修复 (.upxrecoverytool.py) + pyinstaller 解包 + pycdc 反编译
  - 内部含 base58 + zlib + marshal 编码的 scrambled_code_string
  - zlib.decompress 后是缺文件头的 pyc，补 550D0D0A 头 → wtf.pyc
  - wtf.pyc 反编译: random.seed(len(flag)) + key[byte] ^ 95 加密
  - 写 decrypt: inv_key = {x: i for i, x in enumerate(key)} 还原
  - 256 seed 全部爆破（len(flag) <= 256）
  - 1.2 ccc: Python 3.10 pyd 逆向 + IDEA 算法 mod 0x10001
  - keyExpend 52 位，8 轮加密每轮 6 步 + 最后一轮 4 步
  - 函数 sub_3BA0 是 IDEA 加密核心
  - 复用开源 IDEA 实现 razvanalex/IDEA-encryption-algorithm 还原
key_payload: 'wft.pyc 头部 550D0D0A000000000000000000000000 + 加密公式 key[byte]^95'
one_liner: 矩阵杯 2024 Reverse：UPX 修复脱壳 + pycdc 反编译 wtf.pyc + IDEA 算法 pyd 逆向复用开源实现。
lesson: Python 字节码保护（base58+zlib+marshal 编码 + 缺文件头）是常见混淆；IDEA 是经典 mod 65537 块密码。
quality: high
---

# 矩阵杯 2024 战队攻防对抗赛初赛 Writeup

**来源**: ctfiot.com ID 185241
**覆盖**: 闯关赛除 rhttpd / unsafevm / domaingogogo 外全部 + 漏洞挖掘 1 题

## 1.1 packpy（Python 字节码 + UPX）

### 步骤
1. **UPX 修复脱壳**：
   ```bash
   python .upxrecoverytool.py -i D:\xxx\packpy -o D:\xxx\packpy2
   ```
2. **pyinstaller 解包** → 内部 Python 字节码
3. **反编译**：
   ```python
   import base58
   import zlib
   import marshal
   
   scrambled_code_string = b'X1XehTQeZCsb4WSLBJBYZMjovD1x1E5wj...'
   exec(marshal.loads(zlib.decompress(base58.b58decode(scrambled_code_string))))
   ```
4. **zlib.decompress 缺 pyc 头**，补上：
   ```python
   HEAD = bytes.fromhex('550D0D0A000000000000000000000000')
   a = zlib.decompress(base58.b58decode(scrambled_code_string))
   with open('wtf.pyc', 'wb') as f:
       f.write(HEAD + a)
   ```
5. **pycdc 反编译 wtf.pyc**：

```python
import random
encdata = b'\x18\xfa\xad\xed\xab\xad\x9d\xe5\xc0\xad\xfa\xf9\x0b\xef\xe5\xad\xe6\xf9\xfd\x88\xf9\x9d\xe5\x9c\xe5\x9d\xe3))\x0f\xff'

def generate_key(seed_value):
    key = list(range(256))
    random.seed(seed_value)
    random.shuffle(key)
    return bytes(key)

def encrypt(data, key):
    encrypted = bytearray()
    for byte in data:
        encrypted.append(key[byte] ^ 95)
    return bytes(encrypted)

def decrypt(data, key):
    m = bytearray()
    inv_key = {x: i for i, x in enumerate(key)}
    for ci in data:
        m.append(inv_key[ci ^ 95])
    return bytes(m)

for seed_value in range(256):
    key = generate_key(seed_value)
    data = decrypt(encdata, key)
    print(data)
```

爆破 `len(flag)` ∈ [1, 256]，找到含 `flag{` 的输出。

## 1.2 ccc（Python 3.10 .pyd + IDEA）

### 算法识别
- 密文 48 字节，key 16 字节，keyExpend 52 位
- 函数 sub_3BA0 是 IDEA 加密核心
- 加密形状：
  ```
  每次 8 字节分组，每组 2 字节 × 4
  8 轮: t1 = a1 * keyExpend[i*6+0] % 0x10001
        t2 = a2 + keyExpend[i*6+1]
        t3 = a3 + keyExpend[i*6+2]
        t4 = a4 * keyExpend[i*6+3] % 0x10001
        t5 = t1 ^ t3; t6 = t2 ^ t4
        t8 = t5 * keyExpend[i*6+4] % 0x10001
        t9 = t8 + t6
        t10 = t9 * keyExpend[i*6+5] % 0x10001
        t11 = t8 + t10
        t12 = t1 ^ t10
        t13 = t4 ^ t11
        t14 = t2 ^ t11
        t15 = t3 ^ t10
        a1 = t12; a2 = t15; a3 = t14; a4 = t13
  最后一轮: a1 *= keyExpend[48+0] % 0x10001
            a2 += keyExpend[48+1]
            a3 += keyExpend[48+2]
            a4 *= keyExpend[48+3] % 0x10001
  ```
- `mod 0x10001` + 52 位 keyExpend = **IDEA 加密算法**

### 复现
```c
// https://github.com/razvanalex/IDEA-encryption-algorithm
#include <stdio.h>
#include <string.h>

typedef __uint32_t uint32_t;
typedef __int32_t int32_t;
typedef __uint16_t uint16_t;
typedef void (*idea_gen_key)(uint16_t[52], uint16_t[8]);

uint16_t mulMod65537(uint16_t a, uint16_t b) {
    uint32_t c;
    uint16_t hi, lo;
    if (a == 0) return -b + 1;
    if (b == 0) return -a + 1;
    c = (uint32_t)a * (uint32_t)b;
    hi = c >> 16;
    lo = c;
    if (lo > hi) return lo - hi;
    return lo - hi + 1;
}
```

复用开源 IDEA 实现，传入密文 + key + keyExpend → 明文。

## 评价
矩阵杯 2024 闯关赛初赛 Reverse 双题。packpy 考察 Python 字节码混淆（base58+zlib+marshal+缺头）+ UPX 加壳修复；ccc 考察 .pyd 逆向 + IDEA 块密码识别。都是中级 Reverse 必会技能。
