---
title: Google CTF 2023 Writeup by Venom
contest: Google CTF 2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [PWN_UBF, PWN_WFW1, PWN_WFW2字节级爆破, PWN_WFW3_libc, PWN_gradebook, LCG_公钥恢复, RSA_Multi_prime, Lattice_格_爆破, ECDH_TLS, VP-Union]
attack_chain:
  - UBF (Underflow Bug Fix): corrupt booleans fix + base64 payload
  - WFW1: image_addr + 0x21e0 + 80 字节读
  - WFW2: 字节级爆破 flag 字符
  - WFW3: libc 地址泄漏 + 多个 0x... + p32(1337) 控制
  - gradebook: stack 泄漏 + file write 攻击 + add_grade 覆写返回地址
  - LCG: 6 个状态输出还原 a,b,n, 爆破 seed 生成 512-bit 素数
  - 多个 512-bit 素数 RSA + 爆破中末 5 字符
  - ECDH TLS: CA 证书 + 客户端证书 + ECDH 协商 + HKDF 派生 + HMAC
  - CTF{C0nGr@tz_RiV35t_5h4MiR_nD_Ad13MaN_W0ulD_b_h@pPy}
  - CTF{w0W_c0Nt1nUed_fr4Ct10ns_suR3_Ar3_fUn_Huh}
key_payload: 'LCG 状态差分 + a,b,n 还原 + 多素数 RSA + 已知明文爆破'
one_liner: Google CTF 2023 VP-Union 综合：5 道 PWN + LCG 多素数 RSA + ECDH TLS。
lesson: LCG 6 组输出可还原 a,b,n；多素数 RSA 用 LCG 状态生成；ECDH TLS 协商需要 CA + 客户端证书。
quality: high
---

# Google CTF 2023 Writeup by Venom

## 来源
- 原文：ctfiot.com/122434.html
- 比赛：Google CTF 2023
- 战队：VP-Union（星盟 Polaris + ChaMd5 Venom 联合），第 37 名

## 9 道题详解

### PWN
1. **UBF**（corrupt booleans fix）
   ```c
   for (i = 0; ; ++i) {
       v3[i] = v3[i] != 0;
   }
   ```
   - payload: `p32(5) + p8(115) + p16(1) + p16(2) + p16(5) + b'$FLAG' + p32(0x28) + p8(98) + p16(1) + p16(0xff72) + b'\x01'`
   - base64 编码发送

2. **WFW1**（读 image_addr + 0x21e0 + 80）
   - image_addr 泄漏 + 任意读

3. **WFW2**（字节级爆破）
   - 用 `leak(len(flag), chr)` 函数爆破每个字符
   - `CTF{impr355iv3_6ut_can_y0u_s01v3_cha113ng3_3?}`

4. **WFW3**（libc 多地址写 + 0x... 0x70 + p32(1337)）
   - libc_addr + 0x218e10-0x70 + 0x78 字节写
   - 多个 0x... 偏移

5. **gradebook**（stack 泄漏 + file write 攻击）
   - stack_addr 泄漏
   - upgrade_grade 改 %2s
   - add_grade 覆写 COURSE TITLE 字段攻击

### Crypto
6. **LCG 多素数 RSA**
   - 6 个状态输出 → gcd 差分算 a, b, n
   - seed LCG 生成多个 512-bit 素数
   - 多素数 RSA 解密
   - flag: `CTF{C0nGr@tz_RiV35t_5h4MiR_nD_Ad13MaN_W0ulD_b_h@pPy}`

7. **格 爆破中末 5 字符**
   - Lattice + 已知明文 + 下划线位置
   - flag: `CTF{w0W_c0Nt1nUed_fr4Ct10ns_suR3_Ar3_fUn_Huh}`

### Crypto TLS
8. **ECDH myTLS**（TLS 协议实现）
   - CA 证书 verify
   - 客户端证书提供
   - ECDH 临时公钥协商
   - HKDF 派生 shared key
   - HMAC 验证 client

## 关键技巧
- **LCG 还原**：6 组状态输出即可用差分算 a, b, n
- **多素数 RSA**：LCG 生成 512-bit 素数，标准 totient 公式
- **格攻击 + 已知明文**：快速爆破中末 5 字符
- **ECDH TLS**：标准 server-side 实现
- **file write ROP**：gradebook 通过文件名+ size 触发栈迁移

## 适用场景
- 国际级 CTF 实战
- LCG + 多素数 RSA 攻击
- ECDH 协议实现
- 高难度 PWN 字节爆破
