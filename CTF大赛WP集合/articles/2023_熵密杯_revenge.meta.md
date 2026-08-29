---
title: 2023 熵密杯 revenge
contest: 熵密杯 2023
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags: [openssl补丁, drbg_lib硬编码随机数, TLS预主密钥恢复, Wireshark解密, SM2临时密钥派生, SHA256(seed), 临时密钥恢复私钥]
attack_chain:
  - Gitea 检材发现 openssl crypto/rand/drbg_lib.c 修改
  - 原本 32 字节随机数被写死成 32 字节常量数组
  - rand0_32 = {0x67, 0xc6, 0x69, ..., 0x9a} 用于服务端私钥生成
  - 用 X25519PrivateKey.from_private_bytes(rand0_32) 拿服务端私钥
  - X25519 客户端公钥 + 服务端私钥 → shared_key
  - Wireshark 导入 PMS_CLIENT_RANDOM + 共享密钥解密 TLS 流量
  - 找到 SM2 数字签名系统账号密码 + 验签源码
  - 分析 Sign 函数发现 time_parse + derive_from_time
  - derive_from_time(seed) = SHA256(seed) || SHA256(seed+1) || ... 输出 32 字节
  - 计算 msg1 时间戳对应的临时密钥 k
  - 签名 r,s 经 FlipEndian 处理，逆序还原数值
  - sk = (k - s) * inverse(s + r, n) % n 恢复私钥
  - 用私钥给 msg2 签名，伪造合法签名
key_payload: 'rand0_32 = {0x67, 0xc6, 0x69, 0x73, 0x51, 0xff, 0x4a, 0xec, ...}'
one_liner: Gitea 检测 openssl 硬编码随机数 → TLS 解密 → SM2 临时密钥派生 → 恢复私钥。
lesson: openssl 改 drbg_lib.c 是经典后门；derive_from_time 用 SHA256(seed) 派生临时密钥可逆；SM2 签名 r,s 有字节序处理。
quality: high
---

# 2023 熵密杯 revenge

## 来源
- 原文：ctfiot.com/133267.html

## 题目详解

### 1. Gitea 检材 + openssl 补丁检测
- 出题人在 Gitea 仓库改 openssl 的 `crypto/rand/drbg_lib.c`
- 原本生成 32 字节随机数写死成常量数组
- 写死的数组：
  ```c
  uint8_t rand0_32[32] = {0x67, 0xc6, 0x69, 0x73, 0x51, 0xff, 0x4a, 0xec,
                          0x29, 0xcd, 0xba, 0xab, 0xf2, 0xfb, 0xe3, 0x46,
                          0x7c, 0xc2, 0x54, 0xf8, 0x1b, 0xe8, 0xe7, 0x8d,
                          0x76, 0x5a, 0x2e, 0x63, 0x33, 0x9f, 0xc9, 0x9a};
  ```
- 复现 `for(i=0;i<outlen;i++) out[i] = rand0_32[i % 32];`

### 2. TLS 预主密钥恢复
- 用 X25519PrivateKey.from_private_bytes(rand0_32) 拿服务端私钥
- X25519PublicKey.from_public_bytes(客户端公钥) 拿客户端公钥
- shared_key = privatekey.exchange(publickey)
- Wireshark 导入 `PMS_CLIENT_RANDOM <random> <shared_key>` 解密 TLS

### 3. SM2 数字签名系统破解
- 解密后流量中找到 SM2 签名系统（数字签名 + Socks 代理）
- 拿到 sign-verify.c 源码，分析 Sign 函数
- 发现 `derive_from_time(seed, randomScalar, 32)` 用时间戳派生临时密钥：
  ```c
  while (generatedLength < length) {
      SHA256((unsigned char*)&currentSeed, sizeof(currentSeed), shaOutput);
      memcpy(randomScalar + generatedLength, shaOutput, copyLength);
      generatedLength += copyLength;
      currentSeed++;
  }
  ```
- 时间戳 `2023-8-10 09:11:13` → i_time → SHA256 → 临时密钥 k
- k = 0xD2D569D2A7250B2B27DF909C9AFC1FD9E0A555AEC4BFB5D80CD71F70ADACF414

### 4. SM2 私钥恢复
- 签名 r, s 经 FlipEndian 处理，需 `bytes_to_long(long_to_bytes(r)[::-1])`
- 恢复私钥：`sk = (k - s) * inverse(s + r, n) % n`
- 私钥 = 104515905597970870556286963199400550747760654012576876144731059595513283165045

### 5. 伪造 msg2 签名
- 用还原的私钥签名 msg2
- 主函数改成 Sign_Prifile(message2, sig1) 即可

## 关键技巧
- **Gitea 提交历史**：git diff 看代码变更
- **openssl 源码阅读**：crypto/rand/drbg_lib.c 关键随机函数
- **X25519 shared_key**：用服务端私钥反算预主密钥
- **Wireshark TLS 解密**：PMS_CLIENT_RANDOM 文件导入
- **SM2 临时密钥派生**：time → mktime → SHA256 → 32 字节
- **FlipEndian 处理**：签名值 r, s 在网络传输时字节序翻转

## 适用场景
- openssl 后门检测
- TLS 流量解密
- SM2 签名 + 临时密钥派生
- 数字签名系统攻击
