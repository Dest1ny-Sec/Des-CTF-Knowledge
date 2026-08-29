---
title: 贵阳大数据及网络安全精英对抗赛 Reverse EZRE_0 解题
contest: 贵阳大数据
year: 2023
difficulty: medium
vuln_type: reverse
tags: [TLS-callback, RC4, JT8U9ptt, multi-stage, param-control, encrypt-decrypt-flag, chence, key-extraction, debugger]
attack_chain:
  - 32 位 C++ 程序，无壳
  - 输入 flag{77e52c5b-b141-4f3b-92ec-aa680ca38} (38 字符)
  - 错位异或: x[i] ^= x[i+1]
  - TLS 回调函数: RC4 加密, 密码 JT8U9ptt
  - 第 3 阶段: 自定义变换函数, 第 5 个参数 0x65 = 加密, 0x64 = 解密
  - 5 次变换后比对
  - 解法: 拿最终正确值, 把变换函数参数 5 改成 0x64 解密, 再 RC4 解密, 再错位 XOR 逆
  - flag = flag{068d772e155448f0ba101abb62a2a837}
key_payload: 'JT8U9ptt (RC4 key) + 第 5 参数 0x64 解密 + 错位 XOR 逆 + flag{068d772e155448f0ba101abb62a2a837}'
one_liner: EZRE_0 Reverse：错位异或 + TLS 回调 RC4(JT8U9ptt) + 自定义变换（参数 0x65/0x64 切换加解密）+ 5 阶段。
lesson: TLS 回调函数是 RE 隐蔽执行点；自定义算法通过第 5 参数切换加解密是好出题思路。
quality: high
---

# 贵阳大数据及网络安全精英对抗赛 Reverse EZRE_0 解题

**来源**: ctfiot.com ID 115285
**作者**: 看雪 ID `chence`

## 题目结构
- 32 位 C++ 程序，无壳
- 5 阶段变换
- 输入: `flag{77e52c5b-b141-4f3b-92ec-aa680ca38}` (38 字符)

## 5 阶段算法

### 阶段 1: 错位异或
```c
x[i] ^= x[i+1];  // for i in range
```

### 阶段 2: TLS 回调函数 RC4
- RC4 密码: `JT8U9ptt`（调试器提取）
- TLS 回调函数是隐藏执行点（线程创建前后调用）

### 阶段 3: 自定义变换（关键）
- 第 5 个参数 `0x65` = 加密，`0x64` = 解密
- 通过 0x64/0x65 切换方向

### 阶段 4 & 5: 进一步变换
- 作者称"复杂但可逆"

## 解题步骤
1. 运行程序获取最终值（图 13）
2. 拿最终值，把变换函数第 5 参数改成 0x64
3. 重新执行，得到 3F D8 A0 03 BB 66 8C FC 94 AF A9 EA 83 28 31 59 82 83 C9 92 9D B5 73 A4 8D 4C 7B 96 2B 74 6A A8 AE C8 C0 AE B2 D4 00 00
4. RC4 解密 (key=JT8U9ptt)
5. 错位 XOR 逆

## flag
`flag{068d772e155448f0ba101abb62a2a837}`

## 关键技术
- **TLS 回调函数**：在 main 之前/之后执行，IDA 不直接显示
- **RC4 加密**：标准流密码
- **自定义变换**：第 5 参数控制加解密方向（0x65 加, 0x64 解）
- **错位异或**：x[i] ^= x[i+1] 是简单可逆变换
- **动态调试**：x32dbg + 硬件断点定位 TLS 回调
- **作者**: chence（看雪 ID）

## 评价
贵阳大数据 RE 实战：
- 错位异或 → TLS 回调 RC4 → 自定义变换 → 5 阶段
- 第 5 参数切换加解密是巧妙设计
- 调试器动态分析 + 静态算法识别
