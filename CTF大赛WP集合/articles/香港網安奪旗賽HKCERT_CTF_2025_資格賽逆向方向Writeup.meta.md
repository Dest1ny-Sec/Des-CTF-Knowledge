---
title: 香港網安奪旗賽HKCERT CTF 2025 資格賽逆向方向Writeup
contest: HKCERT CTF 2025 資格賽
year: 2025
difficulty: hard
vuln_type: reverse
tags: [SM4, custom-SBOX, XXTEA, modified-TEA, AES-custom, custom-Base64, rsa, key-schedule, cipher-reversal]
attack_chain:
- 题目1SM4魔改: 重新派生SBOX_P=SBOX[(i^167)&255]再rotl8(val, i&3),tau函数4字节替换+T=tau^rotl^rotl^rotl^rotl,expand_key 32轮派生rk
- 题目2魔改AES+自定义Base64: 32字节KEY_SEED+256字节SBOX+32字节CIPHERTEXT打包,密钥扩展10轮(每轮f=17+1~10)
- 题目3魔改XXTEA: sum从DELTA*32开始倒推,key=[0x3C2D1E0F,0x78695A4B,0xB4A59687,0xF0E1D2C3],解密逆向v3/v4
- 题目4 srand随机+alloca栈帧: time(0)^getpid()%20作为srand seed,生成36字节cipherXOR,爆破seed
- 题目5混淆比较: 主函数将s[j]^rand()与cipher比较,绕混淆爆破随机种子
key_payload: hkcert25{...}
one_liner: HKCERT 2025资格赛逆向方向5题,涵盖魔改SM4+自定义SBOX+魔改AES+魔改XXTEA+随机种子爆破,密码学逆向全方向深度。
lesson: 魔改对称加密的破题关键是先识别原算法(SM4/AES/XXTEA),再识别SBOX/常量/DELTA/key的修改,逐项还原。随机数种子爆破:time^pid取低20位是常见弱种子。
quality: high
---

## 题目列表

5道逆向题,涵盖:
1. 魔改SM4 (SBOX重派生+tau函数)
2. 魔改AES (自定义SBOX+10轮key schedule)
3. 魔改XXTEA (sum倒序+key定制)
4. srand+alloca栈帧随机数异或
5. 混合加密+自定义Base64

## 关键考点

### 题目1: 魔改SM4
- CK/FK数组直接从Java代码提取(非标准SM4 CK)
- SBOX_SIGNED用负数表示需`x & 0xFF`转无符号
- SBOX_P = SBOX[(i^167)&255] 后 rotl8(val, i&3)
- tau函数4字节分别sbox_transform((byte^60)&0xFF)
- T = tau ^ rotl(tau,2) ^ rotl(tau,10) ^ rotl(tau,18) ^ rotl(tau,24)
- expand_key 32轮派生rk
- 密文21c2692a4775c413356a31fc55c38f6218bed9d46c45bd0eb777be9334c999d7
- 种子"happ" → derive_key公式`val = (seed_bytes[i%len] + i*17 + 35) & 0xFF`

### 题目2: 魔改AES+自定义Base64
- raw_data_str = 混合普通字符+`\xx`十六进制编码
- data_bytes[0:32] = KEY_SEED(32字节),[32:288] = SBOX(256字节),[288:320] = CIPHERTEXT(32字节)
- f_c(a, b, c) = (c * -23 + (a ^ b)) & 0xFF
- generate_initial_key: 16字节来自f_c(seed[d], seed[d+16], d)
- key_expansion: 11组,每轮e=f*17,新key[a] = (e ^ prev_key[a]) ^ a
- AES标准InvShiftRows+InvSubBytes+InvMixColumns,11轮解密

### 题目3: 魔改XXTEA
- sum = DELTA * 32 倒序开始
- idx = (sum >> 2) & 3
- 加密term1 = ((v3>>5)^(v3<<2)) + ((v3>>3)^(v3<<4))
- term2 = (sum ^ v3) + (v3 ^ k[idx^1])
- v4 += term1 ^ term2
- 已知条件(v3 ^ 0x6421ACBE | (v4 ^ 0xFA7CB432)) == 0 求v3/v4
- key=[0x3C2D1E0F,0x78695A4B,0xB4A59687,0xF0E1D2C3]

### 题目4: srand+alloca混淆
- srand((time(0) ^ getpid()) % 0x14) - 时间+pid低20位爆破
- v13 = v8[0..35] (alloca 48字节栈帧)
- 输入s[j] ^ rand() 与 cipher 36字节比较
- 爆破srand种子恢复rand()序列

### 题目5: 混合加密+自定义Base64
- pack_string_le_with_len: 字符串LE打包后追加长度字段
- xxtea_encrypt_like_402980: sum递减版本(DELTA = 0x9E3779B9)
- B64 alphabet = "ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$"
- 索引顺序v18, v19, i_idx, v21对应4个6-bit索引
- flag{cd00b4953fe9a109148f350427ceddbd} (已给出验证)

## 实战价值
- 魔改SM4/AES/XXTEA是2024-2025 CTF密码学逆向常见题
- 识别原算法的关键:常量数组(0x9E3779B9, 0x10001)、SBOX结构、轮函数
- 弱srand种子爆破在PWN中也是常见漏洞(time+pid组合)
