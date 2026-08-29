---
title: 0CTF 2017 - zer0IIvm 题目分析
contest: 0CTF 2017
year: 2017
difficulty: insane
vuln_type: [reverse, crypto_rsa]
tags: [LLVM, obfuscation, OLLVM, AES, SBox, MixColumns, CRC32爆破, key-recovery, GF(2)-linear, sage, AES_PRECOMP_TE, PRNG]
attack_chain: ["IDA 看 main 是巨大的 switch state machine（OLLVM flatten 混淆）", "分析 lib0opsPass.so 找 Oops::CryptoUtils::prng_seed + scramble32", "crc32('FTC0', &key, 3) == 0xF9E319A6 爆破前 3 字节 = 179, 197, 140", "scramble32 = 4 轮 AES-like XorKey+SubBytes+MixColumn+XorKey", "用 AES_PRECOMP_TE[i](x) = MixColumns(SBox(x) << 8*i) 验证 = AES SBox", "key 用于 scramble plains[65806] 数组", "PRNG 是 8 位非线性 S-box TABLE + 线性 bit 累加，构造 GF(2) 线性系统", "Sage 解 128×16 线性方程组 → 16 字节 seed"]
key_payload: "flag{0llvm_<recovered 16 bytes>}"
one_liner: OLLVM flatten + AES-like scramble + CRC32 爆破前 3 字节 + GF(2) 线性方程恢复 PRNG seed
lesson: LLVM 混淆插件常用 CryptoUtils 做 PRNG；GF(2) 线性化是把非线性 S 盒转成线性系统求密钥的经典方法
quality: high
---

# 0CTF 2017 - zer0IIvm 题目分析

原文 https://www.ctfiot.com/44501.html （山石网科安全技术研究院）

## 题目
- 二进制 + LLVM 混淆插件 `lib0opsPass.so`
- 16 字节 seed → PRNG → AES 密钥 → 加密 plains[65806] 数组
- main 函数被 OLLVM `flatten()` 转成 switch state machine

## 解题
### Step 1: IDA 分析 main
```
state = 0x4E52BCE7
main_switch:
  switch(state) {
    case 0x8000DEEA: goto loc_728049;
    case 0x8001EACA: goto loc_73E38A;
    case 0x8003CC64: goto loc_5C0C95;
    ...
  }
loc_xxxxxx:
  // do something
  state = 0x8003CC64
  goto main_switch
```

### Step 2: lib0opsPass.so 找 CryptoUtils
- `Oops::CryptoUtils::prng_seed(cryptoutils, &seed_string)`
- `Oops::CryptoUtils::get_bytes(cryptoutils, &key, 16)`
- `Oops::CryptoUtils::scramble32(v35, plains0, &key)`

### Step 3: CRC32 爆破前 3 字节
```c
if (crc32('FTC0', &key, 3) != 0xF9E319A6) ...
```
- 用 `crc32(key_prefix + 'FTC0', bytes, 3)` 反查
- 前 3 字节 = **179, 197, 140**

### Step 4: AES 密钥恢复
scramble32 = 4 轮 AES-like (XorKey → SubBytes → MixColumn) + XorKey
```c
v3 = AES_PRECOMP_TE3[(x ^ key[3])] ^
     AES_PRECOMP_TE2[(BYTE1(x) ^ key[2])] ^
     AES_PRECOMP_TE1[((x >> 16) ^ key[1])] ^
     AES_PRECOMP_TE0[(BYTE3(x) ^ *key)];
```
- `AES_PRECOMP_TE[i](x) = MixColumns(SBox(x) << 8*i)` → 等价于 AES S-Box
- 已知前 3 字节 → 逐字节爆破剩余 13 字节

### Step 5: PRNG seed 恢复 (GF(2) 线性化)
encrypt 函数 = 8 轮循环，每次按 seed bit 选择是否 XOR buf
```c
for (j = 0; j <= 7; ++j) {
    if (seedbyte & 1) {
        for (k = 0; k <= 15; ++k) dst[k] ^= buf[k];
    }
    seedbyte >>= 1;
    for (l = 0; l <= 15; ++l) buf[l] = TABLE[buf[l]];
}
```
- TABLE 是 8 位非线性 S 盒
- 但每轮 buf 更新独立 → **buf 和 seed 在 GF(2) 上线性相关**
- 构造 128×128 矩阵（每列是一次 buf 状态）求线性系统

```python
from sage.all import *
from struct import pack

PRNG_OUT = [179, 197, 140, 9, 31, 61, 9, 48, 214, 74, 172, 159, 200, 11, 185, 236]
TABLE = [...]  # 256 字节 S 盒

nonce = pack("<QQ", 0xD7C59B4DFFD1E010, 0x21C7C17B250E019A)
cols = [map(ord, nonce)]
for i in range(127):
    v = [TABLE[c] for c in cols[-1]]
    cols.append(v)

cols = [vector(GF(2), tobinvec(v)) for v in cols]
target = vector(GF(2), tobinvec(PRNG_OUT))
m = matrix(GF(2), 128, len(cols))
for x, c in enumerate(cols):
    m.set_column(x, c)

sol = m.solve_right(target)
res = ""
for i in range(0, 128, 8):
    res += chr(frombin(sol[i:i+8][::-1]))
print(f"flag{{{res}}}")
```

## 考点
1. **C++ 逆向分析** — LLVM 混淆函数去 flatten
2. **LLVM 反混淆原理** — OLLVM pass 工作机制
3. **AES 密钥爆破** — CRC32 校验 + 已知明文攻击

## 教学价值
- 0CTF 顶级赛事经典题
- OLLVM flatten 是工业级混淆，理解 PRNG/CryptoUtils 是关键
- GF(2) 线性化是把非线性 S 盒转成线性方程的标准技巧（Side-channel 攻击同理）
- 配合 Sage / z3 的 CTF Crypto 工具链

## 工具
IDA + Python Sage + Python AES + GDB
