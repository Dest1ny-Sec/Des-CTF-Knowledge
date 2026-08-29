---
title: 2025 春节 解题领红包所有题 writeup
contest: 春节活动
year: 2025
difficulty: mixed
vuln_type: crypto_unknown
tags: [XXTEA, SPN, AES-OFB, custom-VM, phoenixAES, XTEA, TEA, md5-bruteforce]
attack_chain: XXTEA 6+52/n 轮 + delta=0x9E3779B9 解密 SPN 密码 24 字节 S-box 拆位 (32 字节 16 字节) 查表/pheonixAES.crack_file AES OFB 已知 key=7E13141528AED2A6ABF7158809CF4F3C iv=0/AES mode=OFB/魔改 XTEA 12 轮 + delta=0xB979379E 加密 timestamp+uid+hash/VM 自定义指令 17 种操作 xor/neg/pop/or/nop/ret/cmpnz/swap/and/shl/div/add 栈机/flag 拼接 md5(uid) + "{}" 
key_payload: AES key=7E13141528AED2A6ABF7158809CF4F3C  魔改 XTEA delta=0xB979379E  12 轮  XXTEA key="my-xxtea-secret\x00"
one_liner: 2025 春节解题领红包全题 writeup，覆盖 XXTEA + 自定义 SPN + AES OFB + 魔改 XTEA + 自定义 VM 5 大密码学/逆向方向。
lesson: phoenixAES 用于 AES DPA 侧信道攻击或已知末轮密钥恢复；魔改 XTEA 把 delta 改成 0xB979379E 是非标准变种；XXTEA 的 6+52/n 轮数随 n 变化；自定义 VM 栈机 op>>3 区分操作 op&7 取立即数 7 表示后续字节为 16 位立即数。
quality: high
---

# 2025 春节 解题领红包所有题 writeup

## 概览
2025 春节 CTF 通杀榜第一 BMK 全题 writeup，覆盖 5+ 道密码学/逆向/VM 综合题。

## 题目1: XXTEA + 自定义 SPN
```python
# XXTEA 解密
def shift(z, y, x, k, p, e):
    return ((((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((x ^ y) + (k[(p & 3) ^ e] ^ z)))

def decrypt(v, k):
    delta = 0x9E3779B9
    n = len(v)
    rounds = 6 + 52 // n
    x = (rounds * delta) & 0xFFFFFFFF
    y = v[0]
    for i in range(rounds):
        e = (x >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - shift(z, y, x, k, p, e)) & 0xFFFFFFFF
            y = v[p]
        v[0] = (v[0] - shift(z, y, x, k, n-1, e)) & 0xFFFFFFFF
        x = (x - delta) & 0xFFFFFFFF
    return v

key = list(unpack("<4I", b"my-xxtea-secret\x00"))
enc = b64decode(b"hjyaQ8jNSdp+mZic7Kdtyw==")
pt = decrypt(enc, key)
```

## 题目2: 自定义 SPN 密码
- 32 字节 S-box 拆位 16 字节一组（每字节拆两位 4-bit）
- 16 轮重复使用 v12[i][24*j+offset][a][b] 查找
- 倒数用 `for ss in range(16)` 枚举每个字节初始值
- 输出 16 字节密文，匹配 16 行 trace

## 题目3: AES OFB 已知密钥
- 已知 key=`7E13141528AED2A6ABF7158809CF4F3C`，iv=`b'\x00'*16`
- mode=OFB，密文 `[0x48, 0x27, 0x8F, ...]`
- 答案拼接 md5(uid) 即 `flag{md5("19150922025")}`

## 题目4: 魔改 XTEA
- delta=`0xB979379E`（标准 0x9E3779B9 的变种）
- 12 轮，每轮 `v1 += ((v0<<4) + k0) ^ (v0 + sum) ^ ((v0>>5) + k1)`
- 解密 sum 初始值 0xB1AE9B68
- 三组 key：k1/k2/k3 分别加密 timestamp + uid + hash
- 输出 24 字节 hex

## 题目5: 自定义 VM
- vm_s 结构：`mem[16384]` + `pc` + `top` + `flag` + `field_10006` = 0x10008 字节
- 17 种操作码（op = opcodes[pc]>>3, imm = opcodes[pc]&7）：
  - 0/12/14/17/20/29: 终止，结果 = stack[top]
  - 1: XOR stack[top-1]
  - 2: NEG stack[top]
  - 3: pop imm
  - 4/26: NOP
  - 5: OR
  - 6: RET (jump to stack[top-1])
  - 7: cmpnz (compare not equal)
  - 8: swap
  - 9: AND
  - 10: shl/shr
  - 19: div
- 初始 stack = [0, 1915092, 0x1000, 0x2000] + [0]*0x1000
- top=3, pc=0

## 经验提炼
- XXTEA 6+52/n 轮数随 n 变化是标准实现
- phoenixAES 用于 AES 已知末轮密钥的破解（侧信道/DPA）
- 魔改 XTEA 通过改 delta 避免直接 known-plaintext 攻击
- 自定义 VM 栈机逆向先识别 17 种操作码的位拆分（op>>3 操作，op&7 立即数）
- 已知 iv+key 的 AES OFB 直接解密即可
