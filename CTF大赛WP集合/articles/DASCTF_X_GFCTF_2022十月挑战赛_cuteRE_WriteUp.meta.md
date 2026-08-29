---
title: DASCTF X GFCTF 2022 十月挑战赛 cuteRE WriteUp
contest: DASCTF+GFCTF
year: 2022
difficulty: easy
vuln_type: reverse
tags: [base64-custom, rc4, dynamic-debug, swpu, szv, controlflow-obfuscation, deflat]
attack_chain:
  - IDA 主函数 4 子函数
  - 32 字符按奇偶分 2 部分
  - sub_405700 自定义 base64 表生成
  - sub_4059F0 控制流混淆 deflat
  - sub_406270 RC4
  - 动态调 sub_405700 后取 byte_609450 = 新 base64 表
  - 动态调 sub_4059F0 后取 byte_6090A0 = 'szv~'
  - base64 解密文 1
  - RC4(szv~) 解密文 2
  - 奇偶拼回
key_payload: 动态调试拿真实 key (szv~) + 自定义 base64 表
one_liner: cuteRE 入门逆向，动态调出运行时修改的 base64 表 + RC4 key。
lesson: 当 reverse 题 IDA 静态看不出真实 key，优先动态调试 print 实际写入的地址值。
quality: high
---

DASCTF X GFCTF 2022 十月挑战赛 cuteRE 复盘，作者 HU_Moon（看雪论坛）。

**信息搜集**
64 位程序无壳，IDA 找 main 函数。程序获取用户输入后判断长度 32 位，按奇偶分成 2 部分。

**4 子函数**：
- `sub_405700(byte_609450)`：BASE 编码表 + base 关键字 → 自定义 Base64
- `sub_4059F0(unk_609350, byte_6090A0='swpu', 4)`：控制流混淆（deflat 处理）
- `sub_406270(unk_609350, s2, len)`：RC4 加密
- `sub_400C10(v35, v33, len)`：Base64 编码

**解密密文 1**：`xlt0+V9PtVBKt0lEukZYug==`

直接 base64 解失败 → 加密时 `sub_405700` 已修改 `byte_609450` 地址的 Base64 表。

**动态调试**：
- 调 `sub_405700` 后查 `byte_609450` → 新表 `ghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef`
- 调 `sub_4059F0` 后查 `byte_6090A0` → 实际值 `szv~`（不是源代码里的 `swpu`）

**解密 1**：用新 base64 表解 → `DST{Wo7Xj5Ad8Nx8`
**解密 2**：用 `szv~` RC4 解 `\x72\xA7\xE5\xB1\xBF\xD1\x3A\xC9\x7E\x5D\x83\xA8\x21\x4F\x70\x90` → `ACFg0Gw1Jo5Ix9C}`

**奇偶拼回**：
- 偶数位：DST{Wo7Xj5Ad8Nx8
- 奇数位：ACFg0Gw1Jo5Ix9C}
- 交织：g, W, A, C, 0, F, g, 0, 7, G, w, 1, X, J, j, 5, 5, A, o, d, I, 5, 8, x, N, x, C, 8, x, C, 9, }
- flag = `DASCTF{gW0oG7wX1jJ5oA5dI8xN9xC8}`
