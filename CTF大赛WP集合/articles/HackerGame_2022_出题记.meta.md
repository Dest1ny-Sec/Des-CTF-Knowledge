---
title: HackerGame 2022 出题记
contest: HackerGame 2022 (出题记)
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [crypto, aes-cbc, chosen-ciphertext, crc128, affine-crc, sagemath, gf2, writeup-design]
attack_chain:
  - AES-CBC chosen ciphertext attack
  - AES_CBC_chosen_ciphertext: pos指定位置插入
  - crc128 = (1<<128) - 1 多项式
  - poly=0x883ddfe55bba9af41f47bd6e0b0d8f8f
  - 等价仿射CRC: crc(x) = M*x + C (GF(2))
  - Affine_Matrix = []
  - target_bits = 8 * target_bytes
  - v2n + n2v 转换 GF(2) vector
  - matrix(GF(2), Affine_Matrix).transpose()
key_payload: crc(x) = M*x + C in GF(2)
one_liner: HackerGame 2022 出题记：AES-CBC chosen ciphertext+仿射CRC
lesson: CRC可表示为GF(2)上仿射变换；AES-CBC chosen ciphertext可构造任意块
quality: high
---

# HackerGame_2022_出题记

## 题目信息
- 比赛：HackerGame 2022
- 类型：出题记
- 类别：Crypto

## 关键攻击链
### 1. AES-CBC chosen ciphertext
```python
from Crypto.Util.number import *
from Crypto.Cipher import AES
import os

block_size = 16
key_size = 16

def pad(msg: bytes, block_size = 16):
    n = AES.block_size - len(msg) % AES.block_size
    return msg + bytes([n]) * n

def unpad(msg, block_size = 16):
    return msg[: -msg[-1]]

def xor(b1: bytes, b2: bytes):
    return bytes([x ^ y for x, y in zip(b1, b2)])

def split_block(text: bytes):
    return [text[i*block_size:(i+1)*block_size] for i in range(len(text)//block_size)]

def AES_CBC_chosen_ciphertext(AES_key: bytes, plaintext: bytes, chosen_ciphertext: bytes, pos=None):
    # pos = None: iv will be set as chosen ciphertext
    # pos = -1: last block will be set as ciphertext
    # pos = i: ith (from 0) block will be set as ciphertext
    if pos == None:
        iv = chosen_ciphertext
        aes_cbc = AES.new(AES_key, AES.MODE_CBC, iv)
        return iv, aes_cbc.encrypt(msg)
    
    iv = os.urandom(block_size)
    aes_cbc = AES.new(AES_key, AES.MODE_CBC, iv)
    aes_ecb = AES.new(AES_key, AES.MODE_ECB)
    cipher = aes_cbc.encrypt(msg)
    msg_blocks = split_block(msg)
    cipher_blocks = split_block(cipher)
    cipher_blocks[pos] = chosen_ciphertext
    
    for i in range(pos-1, -1, -1):
        cipher_blocks[i] = xor(aes_ecb.decrypt(cipher_blocks[i+1]), msg_blocks[i+1])
    
    iv = xor(aes_ecb.decrypt(cipher_blocks[0]), msg_blocks[0])
    
    for i in range(pos+1, len(cipher_blocks)):
        cipher_blocks[i] = aes_ecb.encrypt(xor(cipher_blocks[i-1], msg_blocks[i]))
    
    return iv, b"".join(cipher_blocks)
```

### 2. CRC128 仿射表示
```python
def crc128(data, poly=0x883ddfe55bba9af41f47bd6e0b0d8f8f):
    crc = (1 << 128) - 1
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (poly & -(crc & 1))
    return crc ^ ((1 << 128) - 1)

def equivalent_affine_crc(crc=crc128, crc_bits=128, target_bytes=16):
    zero_crc = crc(target_bytes * b"\x00")
    target_bits = 8 * target_bytes
    v2n = lambda v: int(''.join(map(str, v)), 2)
    n2v = lambda n: vector(GF(2), bin(n)[2:].zfill(crc_bits))
    Affine_Matrix = []
    for i in range(target_bits):
        v = vector(GF(2), (j == i for j in range(target_bits)))
        value = crc(long_to_bytes(v2n(v), target_bytes)) ^ zero_crc
        Affine_Matrix.append(n2v(value))
    return matrix(GF(2), Affine_Matrix).transpose(), n2v(zero_crc)
```

## 关键技术点
- AES-CBC chosen ciphertext attack
- CRC 表示为 GF(2) 上仿射变换 `crc(x) = M*x + C`
- 矩阵可逆性分析
- Sagemath 求解

## 评分
- quality: high（AES-CBC + CRC 仿射表示 + 出题思路）
