---
title: 从Google CTF Fluffy看Dart逆向
contest: Google CTF 2025
year: 2025
difficulty: hard
vuln_type: reverse
tags: [Dart, ARM64, DecompressPointer, HEAP, base62, rol1, ror1, 时间戳爆破, 多线程, 预计算]
attack_chain:
  - 静态分析 Dart AOT 编译产物（AArch64）识别 saveSecret/update_token_bytes/b62encode
  - 还原算法 saveSecret: pin 轮循环 rol1(byte + token_bytes[j%8], j&7) + memmove 循环
  - 还原 update_token_bytes: memmove 循环 + ror1(token_bytes[j], (pin^((round&3)+1))&7)
  - 还原 generate_token: gctf25_{ts} SHA1 前 8 字节 b62encode
  - 写 restoreSecretWithPrecomputed 逆算法 (ror1 - token_bytes)
  - 预计算 token_bytes_list 10000 项避免重复 update
  - 24 线程并行 bf_secret_thread 搜 timestamp 范围
  - 测 '}' 字符快速过滤可打印解密
  - 拼接 3 段 flag: Ok4y_h4v3_u_0ptim1zed + brUt3_f0rcE_0R_y0u_jUst + ...
key_payload: 'CTF{Ok4y_h4v3_u_0ptim1zed_brUt3_f0rcE_0R_y0u_jUst'
one_liner: Dart AOT ARM64 逆向 + 自定义 b62 编解码 + 时间戳爆破 token + 多线程预计算 pin 优化。
lesson: Dart AOT 没有标准运行时元数据，靠 DecompressPointer+HEAP 寻址对象；优化 pin 循环时预计算 token_bytes_list 把 update 提到 pin 循环外，多线程按时间分片爆破 ts 范围。
quality: high
---

# 从Google CTF Fluffy看Dart逆向

## 概览
- **来源**: 看雪 SleepAlone 原创 (ctfiot 261979)
- **目标**: 逆向 Google CTF 2025 Fluffy，Dart 编写的 AArch64 ELF
- **难度**: ⭐⭐⭐⭐

## Dart AOT 关键概念
- `DecompressPointer r2` = `add x2, x2, HEAP, lsl #32` 解压压缩指针
- 寄存器约定: `X27`=ObjectPool `X26`=Thread `X15`=SP
- 函数签名: `(_QWORD* pool@<X27>, Thread* thread@<X26>, stack*@<X15>, ...)`

## saveSecret 算法
```
for i in 0..pin:
  for j in 0..secret_len:
    res[j] = rol1(res[j] + token_bytes[j % 8], j & 7)
  tmp = res[last]; memmove(res+1, res, last); res[0] = tmp
  update_token_bytes(token_bytes, 8, pin, i)
```

## 还原/优化
- `restoreSecretWithPrecomputed` 用预计算 token_bytes_list 避免 pin 循环内重复 update
- `restoreSecretWithPrecomputedAt(idx, ...)` 只算一个字节判断末尾 '}' 快速过滤
- `bf_secret_thread` 24 线程按 ts 分片

## 三段 flag
- `CTF{Ok4y_h4v3_u_0ptim1zed_brUt3_f0rcE_0R_y0u_jUst`
- 3 个不同时间戳 + 不同 ciphertext 拼出完整 flag

## 工具
- gmp 大整数 + openssl SHA1
- pthread 多线程
