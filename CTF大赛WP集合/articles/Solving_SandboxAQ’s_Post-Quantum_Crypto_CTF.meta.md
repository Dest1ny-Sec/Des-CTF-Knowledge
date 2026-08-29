---
title: Solving SandboxAQ's Post-Quantum Crypto CTF
contest: SandboxAQ
year: 2024
difficulty: hard
vuln_type: lattice
tags: [post-quantum, lwe, ring-lwe, module-lwe, kyber-768, x25519kyber768, prng-brute]
attack_chain:
- rotMatrix poly cyclotomic=True 构造 X^N+1 上的旋转矩阵
- module(polys, 2, 2) 拼装 2x2 块矩阵
- LWE 攻击：DBDD_predict 估计 δ=1.045280 β=2.00
- NTL ZZ_pX + OpenMP 并行爆破 s1, s2 ∈ {0,1}^16
- 找到 s1=RR([1,1,1,1,1,0,1,1,0,0,0,1,0,0,1,1]) s2=RR([1,0,0,0,1,0,1,1,1,0,0,1,0,1,1,1])
- 解密 v - s*u^T 再 decompress 还原 16 bit
- flag = [1,0,0,1,0,1,1,0,0,1,1,1,0,0,0,1]
- Kyber NIST KAT: entropy_input 24 bit 暴力枚举
- OQS_KEM_kyber_1024_keypair 对比 test_public_key
- 找到 seed 后复现 ECDH
- x25519 + Kyber768 混合 TLS 抓包解密
- wireshark 抓 pcap → pcap_processing → 解出 HTTP 响应
- /dir/.../server_secret.txt → My v0ice is my p@ssport.
- 54318...d90 = 真正的 flag
key_payload: OQS_randombytes_nist_kat_init_256bit(entropy_input, NULL)
one_liner: SandboxAQ 后量子密码 CTF：Module-LWE 攻击 + Kyber-1024 PRNG 爆破 + X25519+Kyber768 混合 TLS 解密。
lesson: 后量子密码实现若 PRNG 种子空间过小，仍可通过暴力枚举恢复 shared secret。
quality: high
---
# SandboxAQ Post-Quantum Crypto CTF

## 1. Module-LWE 解密
```python
# rotMatrix + module 拼装矩阵
K, N = 2, 16
q = 251
R.<x> = Zmod(q)[]
RR = R.quotient(x^N + 1)

# 公钥 A (2x2 矩阵)、密文 t (2 个多项式)
A1 = RR(195*x^15 + 229*x^14 + ... + 180)
# ... A2/A3/A4
t1 = RR(109*x^15 + 188*x^14 + ... + 9)
# ... t2

# 爆破 s1, s2 (每个 2^16)
s1 = RR([1,1,1,1,1,0,1,1,0,0,0,1,0,0,1,1])
s2 = RR([1,0,0,0,1,0,1,1,1,0,0,1,0,1,1,1])
s = matrix(RR, [s1, s2])

err = t.transpose() - A * s.transpose()  # error in -1,0,1
m_n = v - s * u.transpose()              # 解密
flag_bits = decompress(m_n)              # 解压
```

## 2. Kyber-1024 PRNG 爆破
```c
// 24 bit PRNG seed 暴力枚举
int rc, res;
struct AES_ctx ctx;
for (size_t i = 0; i < 16777216; i++) {
    for (size_t j = 0; j < 24; j++) {
        entropy_input[24+j] = (i >> j) & 1;
    }
    OQS_randombytes_nist_kat_init_256bit(entropy_input, NULL);
    rc = OQS_KEM_kyber_1024_keypair(public_key, secret_key);
    res = memcmp(public_key, test_public_key, OQS_KEM_kyber_1024_length_public_key);
    if (res == 0) {
        // 找到 seed
        break;
    }
}
OQS_KEM_kyber_1024_decaps(shared_secret, ciphertext, secret_key);
```

## 3. X25519+Kyber768 TLS 抓包
```python
# TLS 1.3 key_share "x25519kyber768draft00"
# calc_shared_key: x25519 私钥 + Kyber 私钥组合
S = x25519(private[:32], x25519_ps)
kb = kyber.Kyber(kyber.DEFAULT_PARAMETERS['kyber_768'])
skb = kb.dec(kyber_ps, private[32:])
return S + skb
```

## 4. 协议解析
- 客户端发 `client_secret.txt` (24 byte 标识)
- 服务端返回 800 字节响应
- 客户端 768 字节 ciphertext
- 服务端 16 字节 accept
- 客户端 48 字节二次认证
- 后续 368 字节 HTTP 响应

## 5. flag
解密 HTTP 响应得到：
```
The flag is: 5443184089537ac26d77f5605e1d0c8271597ca097ef1b40be77c7a7bbd62d90
```
