---
title: TJCTF 部分 Crypto-wp
contest: TJCTF
year: 2025
difficulty: medium
vuln_type: crypto_rsa
tags: [baconian-cipher, case-encoding, custom-rc4, rsa-multi-prime, lcg-time-seed]
attack_chain:
- Baconian 加密 + 大小写编码
- chr(ord(c)-13) 减位 → 解码
- 大写/小写对应 1/0
- 5 字符一组映射回 Baconian 二进制 → 明文
- "tictf" 改为 "tjctf" 包裹花括号
- alchemist-recipe 自定义 RC4-like 加密 (SHA256 派生 key + 256 字节 S-box 初始化)
- deschuffle 排序还原 + XOR 还原 + S-box 逆映射
- 多模数 RSA 攻击：CRT 合并 C，iroot 求 e 次方根
- LCG 伪随机数 (m=2^32, a=157, c=1) seed=time.asctime()
- nc tjc.tf 31493 拿 ciphertext
- 2 小时时间窗口爆破 seed → AES-ECB 解密
key_payload: AES-ECB(key, ciphertext) where key = LCG.randbytes(32)
one_liner: TJCTF 2025 部分 Crypto：4 题 Baconian + 自定义 RC4 + 多模数 RSA + LCG 伪随机爆破。
lesson: 多模数 RSA 当 e 较小时 e 次方根可解；LCG 种子若用 time.asctime()，时间窗口可爆破。
quality: medium
---
# TJCTF 部分 Crypto-wp

## 1. Baconian 加密
加密方式：每个字符 → 5 位二进制 → 大写(1) / 小写(0)
再 `chr(ord(c)-13)` 写入 out.txt。

解密：
```python
baconian = {
    '00000': 'a', '00001': 'b', '00010': 'c', '00011': 'd', '00100': 'e',
    '00101': 'f', '00110': 'g', '00111': 'h', '01000': 'i', '01001': 'k',
    '01010': 'l', '01011': 'm', '01100': 'n', '01101': 'o', '01110': 'p',
    '01111': 'q', '10000': 'r', '10001': 's', '10010': 't', '10011': 'u',
    '10100': 'w', '10101': 'x', '10110': 'y', '10111': 'z',
}

with open("out.txt", "r") as f:
    encrypted = f.read().strip()

# chr(ord(c) + 13) 还原大小写
decoded = ''.join([chr(ord(c) + 13) for c in encrypted])

bits = []
for i in range(0, len(decoded), 5):
    group = decoded[i:i+5]
    bit_string = ''.join(['1' if c.isupper() else '0' for c in group])
    bits.append(bit_string)

plaintext = ''.join([baconian.get(b, '?') for b in bits])
# tictfoinkooinkoooinkooooink
# 改为 tjctf{...}
```

## 2. alchemist-recipe
SHA256 派生 key：
```python
SNEEZE_FORK = "AurumPotabileEtChymicumSecretum"
WUMBLE_BAG = 8
def glorbulate_sprockets_for_bamboozle(blorbo):
    yarp = hashlib.sha256(blorbo.encode()).digest()
    zing = {
        'flibber': list(yarp[:8]),  # 8 byte
        'twizzle': list(yarp[8:24]),  # 16 byte
    }
    glimbo = list(yarp[24:])  # 剩余
    snorb = list(range(256))
    sploop = 0
    for _ in range(256):
        for z in glimbo:
            wob = (sploop + z) % 256
            snorb[sploop], snorb[wob] = snorb[wob], snorb[sploop]
            sploop = (sploop + 1) % 256
    zing['drizzle'] = snorb
    return zing
```

解密 = 排序还原 + XOR 还原 + S-box 逆映射。

## 3. 多模数 RSA
```python
from sympy.ntheory.modular import crt
from gmpy2 import iroot
import re

with open("output.txt", "r") as f:
    data = f.read()

e = int(re.search(r"e\s*=\s*(\d+)", data).group(1))
pairs = re.findall(r"n\s*=\s*(\d+)\s+c\s*=\s*(\d+)", data)
n_list = [int(n) for n, _ in pairs]
c_list = [int(c) for _, c in pairs]

# CRT 合并
C, N = crt(n_list, c_list)
m_root, exact = iroot(C, e)
flag = long_to_bytes(m_root)
```

## 4. LCG 伪随机爆破
```python
class RandomGenerator:
    def __init__(self, seed, modulus=2**32, multiplier=157, increment=1):
        self.seed = int.from_bytes(seed.encode(), "big") if isinstance(seed, str) else seed
        self.m, self.a, self.c = modulus, multiplier, increment
    def randint(self, bits: int):
        self.seed = (self.a * self.seed + self.c) % self.m
        result = self.seed.to_bytes(4, "big")
        while len(result) < bits // 8:
            self.seed = (self.a * self.seed + self.c) % self.m
            result += self.seed.to_bytes(4, "big")
        return int.from_bytes(result, "big") % (2 ** bits)
    def randbytes(self, length: int):
        return self.randint(length * 8).to_bytes(length, "big")

# nc 拿 ciphertext，时间窗口 2h 爆破
from datetime import datetime, timedelta
import time
start = datetime(2025, 6, 7, 8, 0, 0)
end = datetime(2025, 6, 7, 10, 0, 0)
cur = start
while cur <= end:
    seed_str = time.asctime(cur.timetuple())
    rng = RandomGenerator(seed_str)
    key = rng.randbytes(32)
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        plain = unpad(cipher.decrypt(ciphertext), 16)
        if b'tjctf{' in plain:
            print(plain.decode()); break
    except: pass
    cur += timedelta(seconds=1)
```
