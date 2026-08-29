---
title: HKCERT CTF 2022 Postmortem (II): Harder Crypto Challenges
contest: HKCERT CTF 2022
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [crypto, aes, batch-file, windows-aes, subbytes-shiftrows-mixcolumns, block-cipher, batch-attack]
attack_chain:
  - Windows批处理实现AES加密（aes.bat）
  - 已知明文+密文对
  - 红色 4czfHjwa9rl+Xds/1EbFuJioVRnYL0ym86UZ2WDMQPgBKGT5AN3Cqe7OShpvkxIt
  - 蓝色 4czIHjwaYd8F1St/xEb7rJioV0+RLnygf6UGZWDMQPuBClqKAX35Te9ONhsv2mkp
  - 红色+蓝色→flag
  - AES-128 SubBytes+ShiftRows+MixColumns
  - AES batch file完整实现
  - 加密已知明文ABCDEFGHIJKLMNOPQRSTUVWXYZ...+/
  - 调整密文+密文
key_payload: 已知明文+密文对+多密钥差异
one_liner: HKCERT 2022 Harder Crypto：Windows批处理AES+双密钥密文对比
lesson: 批处理文件实现AES是新颖密码学题形式
quality: high
---

# HKCERT CTF 2022 Postmortem (II): Harder Crypto Challenges

## 题目信息
- 比赛：HKCERT CTF 2022
- 作者：mystiz
- 类别：Crypto（Harder）

## 关键攻击链
### 1. Windows 批处理实现 AES
```batch
@echo off
aes.bat [REDACTED_KEY] 68656c6c6f20776f726c6421
```
- 输出：`2740f489df8449453fd87f075a648e94`

### 2. 红色密钥密文
```
Plaintext: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Ciphertext: 4czfHjwa9rl+Xds/1EbFuJioVRnYL0ym86UZ2WDMQPgBKGT5AN3Cqe7OShpvkxIt
```

### 3. 蓝色密钥密文
```
Plaintext: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Ciphertext: 4czIHjwaYd8F1St/xEb7rJioV0+RLnygf6UGZWDMQPuBClqKAX35Te9ONhsv2mkp
```

### 4. AES 批处理实现
```batch
:EncryptBlock
    set block_id=%1
    call :LoadState %block_id%
    set round_key=0
    call :AddRoundKey %round_key%
    for /l %%r in (1, 1, 9) do (
        set round_key=%%r
        call :SubBytes
        call :ShiftRows
        call :MixColumns
        call :AddRoundKey %round_key%
    )
    set round_key=10
    call :...
```

### 5. 攻击
- 已知明文+密文对
- 红色 + 蓝色密文组合 → flag

## 评分
- quality: high（Windows 批处理 AES 实现 + 双密钥密文对比）
