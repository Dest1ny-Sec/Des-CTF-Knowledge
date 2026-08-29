---
title: 2023 数字网络安全人才挑战赛 WriteUp by Arr3stY0u
contest: 数字网络安全人才挑战赛 2023
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [SSRF, proc_net_arp, gopher协议, SQL盲注绕过滤, HNP格, 离散DH_CRT, TEA变种, pwn_起源, 山海关]
attack_chain:
  - easy_curl: file:///proc/net/arp 读内网 IP，绕过 127 关键字
  - gopher://127.1:80/ POST flag.php key=2730ea2fd4c40df0f8b7fdb6738221d6
  - 双重 URL 编码 gopher payload，hackbar 发包
  - Simple Message Board: 搜索 SQL 注入，禁 union 用 if 绕
  - 禁 substr/ascii 用 ord + left 绕，二分盲注
  - babysecret: 30 个 inputs 构造 HNP 格，sage LLL 求 x
  - factor(n-1) 多素数 p_i，discrete_log 各 p_i 模下解 ri，CRT 拼 x
  - game: 调试器改 dword_AEE880 = 0x280 改后续 XOR
  - easykernel: dev_write 函数，TEA 变种 -= 改 += 调顺序还原
  - pwn 起源: read 0x28 字节 + p32(0x100006F0) 大端跳转 ROP
  - one_gadget 配合 pwncli 一把梭
key_payload: 'POST /flag.php HTTP/1.1\r\nHost: 10.252.47.1\r\nContent-Length: 36\r\n\r\nkey=2730ea2fd4c40df0f8b7fdb6738221d6'
one_liner: 综合 6 题：SSRF+gopher+SQL 盲注绕过滤+HNP 格+DH CRT+TEA 变种+pwn 起源 ROP。
lesson: proc/net/arp 替代 127 关键字查内网；SQL 注入禁 union 用 if + 禁 substr 用 ord/left；HNP 用格攻击 + 离散 DH 用 CRT 拼。
quality: high
---

# 2023 数字网络安全人才挑战赛 WriteUp by Arr3stY0u

## 来源
- 原文：ctfiot.com/105328.html
- 团队：山海关安全团队 + Arr3stY0u 战队

## 6 道题详解

### WEB
1. **easy_curl**（SSRF + proc/net/arp）
   - file:///proc/net/arp 读内网 IP（绕过 127 关键字 ban）
   - gopher://127.1:80/ POST flag.php 带 key=...
   - 双重 URL 编码 gopher payload，hackbar 发包

2. **Simple Message Board**（SQL 盲注绕过滤）
   - 禁 union 用 `if(...,1,0)` 绕
   - 禁 substr/ascii 用 `ord(left(...,n))` 绕
   - 二分法盲注 flag 字符

### CRYPTO
3. **babysecret**（HNP 格 + 离散 DH + CRT）
   - 30 个 inputs 构造 HNP 格，sage LLL 求 x
   - `factor(n-1)` 多素数，discrete_log 各 p_i 模下解 ri
   - `crt(r_list, tmp_list)` 拼 x = secret
   - 参考《离散·DH·Elgamal》harry0597.com 博客

### REVERSE
4. **game**（调试器改内存）
   - dword_AEE880 的值后面去 XOR，改成 0x280 即可
   - 继续运行拿 flag

5. **easykernel**（TEA 变种）
   - dev_write 函数加密结构类似 TEA
   - `+=` 改 `-=`，调运算顺序
   - delta = 0x67616C66, sum = 0xD89114C8
   - 9 个 uint cipher 反向解

### PWN
6. **pwn 起源**（read 跳转）
   - `read(0, buf, 0x20)` 后 0x100006F0 跳转
   - payload: `cat f*;\x00...` + p32(0x100006F0) 大端
   - one_gadget 配合 pwncli

## 关键技巧
- **proc/net/arp**：替代被 ban 的 127 关键字查内网
- **if + ord + left**：SQL 注入经典过滤绕过组合
- **HNP**：构造格用 LLL 还原私钥分量
- **离散 DH + 多素数 + CRT**：n-1 多素数时分模数离散对数 + CRT 拼装
- **TEA 变种**：v25 索引数组做 (sum>>2)&3 ^ 1/2/5/6/7 选 key
- **pwn 起源**：read 后跳转 ROP 一把梭

## 适用场景
- SSRF + gopher
- SQL 注入盲注过滤绕过
- HNP 格 + DH CRT
- TEA 变种逆向
- pwncli 实战
