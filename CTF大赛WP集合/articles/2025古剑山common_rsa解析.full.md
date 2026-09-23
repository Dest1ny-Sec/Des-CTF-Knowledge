---
title: 2025 古剑山 common_rsa 解析（RSA 共模攻击+扩展欧几里得）
contest: 2025 古剑山
year: 2025
difficulty: medium
vuln_type:
- crypto_rsa
- lattice
tags:
- 古剑山 2025 common_rsa 物不知数
- RSA 共模攻击 同一 m 不同 e
- c1=m^e1 mod N
- c2=m^e2 mod N
- gcd(e1
- e2)=1
- 扩展欧几里得 s*e1+t*e2=1
- m=c1^s * c2^t mod N
- c1_inv=invert(c1
- N) c1^(-1)^334
- part1+part2 mod N
- gmpy2.gcdext
attack_chain:
- 同 N 同 m 不同 e1, e2，e1=35422 e2=1033
- 扩展欧几里得 gcd(e1, e2)=1, s=-334, t=11453
- s*e1 + t*e2 = -334*35422 + 11453*1033 = 1
- c1^s = c1^(-334) = (c1^(-1))^334
- c1_inv = gmpy2.invert(c1, N)
- m = (c1_inv)^|s| * c2^t mod N = (c1^(-1))^334 * c2^11453 mod N
- flag = bytes.fromhex(hex(m)[2:])
key_payload: m = (c1_inv)^|s| * c2^t mod N
one_liner: 2025 古剑山 common_rsa 物不知数：同 N 同 m 不同 e1=35422, e2=1033 共模攻击，扩展欧几里得求 s, t，c1^(-1)^334 * c2^11453 mod N 还原 m。
lesson: RSA 共模攻击 = 同 N 同 m 不同 e，扩展欧几里得求 s*e1 + t*e2 = 1，m = c1^s * c2^t mod N；s 为负数时取模逆元 invert(c1, N)。
quality: high
full_path: 2025古剑山common_rsa解析.full.md
meta_path: 2025古剑山common_rsa解析.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 2025 古剑山 common_rsa 解析（RSA 共模攻击+扩展欧几里得）。2025 古剑山 common_rsa 物不知数：同 N 同 m 不同 e1=35422, e2=1033 共模攻击，扩展欧几里得求 s, t，c1^(-1)^334 * c2^11453 mod N 还原 m。。关键路径：同 N 同 m 不同 e1, e2，e1=35422 e2=1033 → 扩展欧几里得 g...
category: crypto
subcategory: rsa
subcategories:
- rsa
- lattice
tools_used:
- gmpy2
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/284446.html
reasoning_chain:
- 触发点：同 N 同 m 不同 e1=35422 / e2=1033 两个密文 → 假设：RSA 共模攻击
- 动作：扩展欧几里得 gcd(e1, e2)=1 → 假设：s*e1 + t*e2 = 1 必有 s,t → 观察：-334*35422 + 11453*1033 = 1 验证
- 下一步：s=-334 是负数 → 假设：取 c1 的模逆 c1_inv = invert(c1, N) → 动作：c1^(-1)^334 mod N
- 观察：m = (c1^(-1))^334 * c2^11453 mod N → 下一步：m^(e1*s + e2*t) = m^1 mod N
- 触发点：m 是长整数 → 假设：flag = bytes.fromhex(hex(m)[2:]) 还原字符串 → 动作：print(flag.decode('ascii'))
- 观察：拿到 flag → 总结：同 N 同 m 不同 e 共模攻击是 RSA 经典套路
failed_attempts:
- 试图用 e1*e2 互乘爆破解密 → 失败：单一 e 没逆元，必须 gcd=1 才有解
- 试图直接 pow(c1, -1, N) 得到 m → 失败：s 不是 -1，要 raise 到 abs(s)=334 才能抵消
- 试图对 (N, e1) 单独因式分解 → 失败：N 不含显式 p, q 泄露
key_observations:
- RSA 共模攻击 = 同 N 同 m 不同 e，gcd(e1,e2)=1 时扩展欧几里得求 s*e1+t*e2=1 还原 m
- s 为负数时取 c1 的模逆 invert(c1,N) → c1^|s| 才得到 c1^(-|s|)
- 古剑山 '物不知数' 类型题 = 数论经典，孙子定理/共模攻击变体
- gmpy2.gcdext 一步搞定扩展欧几里得不需要手写递归
prerequisites:
- 扩展欧几里得算法（exgcd/gcdext）
- RSA 共模攻击原理（同 N 同 m 不同 e）
- Python gmpy2 或 sympy 的模逆函数使用
- long_to_bytes / bytes.fromhex 整数与字节转换
---
# 2025古剑山common rsa解析

> 原文: https://www.ctfiot.com/284446.html
> ID: 284446

RSA共模攻击详解：物不知数

题目背景

在密码学竞赛中，我们遇到了一道名为”物不知数”的RSA加密题目。题目给出了如下信息：

ounter(lineounter(lineounter(lineounter(lineounter(lineN = 162178605357818616394571566923155907889899677780239882906511996614607940884142045197452389471499799373787832649318837814454679970724845203557871078001956378966434166323827984964942729898095347038272003371167123553368531662277059263517900162297903110415768403265100411543878859321181606008503516896600638590699e1 = 35422c1 = 153249315480380808558746807096025628082875635601515291525075274335055878390662930254941118045696231628008256877302589689883059616503108946971165183674522403835250738176157466145855833767128209866527507862726083268576304163200171600023472544755768741118904892489037291247455823396160705615280802805803254323033e2 = 1033c2 = 5823189490163315770684717059899864988806118565674660089157163486577056500243194221873916232616081138765317598078910078375360361118674333149663483360677725162911935082290640547407140413703664960164356579153623498735889314476063673352676918268911309402784919521792079943937126634436658784515914270266106683548

选择两个大素数p和q，计算N = p * q

计算欧拉函数φ(N) = (p-1)(q-1)

选择公钥指数e，满足gcd(e, φ(N)) = 1

计算私钥d，满足e * d ≡ 1 (mod φ(N))

加密：c = m^e mod N

解密：m = c^d mod N

同一条明文m

使用相同的模数N

使用不同的公钥指数e1和e2

得到两个密文c1和c2

ounter(lineounter(linec1 = m^e1 mod Nc2 = m^e2 mod N

ounter(lines * e1 + t * e2 = 1

ounter(linem = (c1^s * c2^t) mod N

ounter(lineounter(lineounter(lineounter(linec1^s * c2^t mod N= (m^e1)^s * (m^e2)^t mod N= m^(e1*s) * m^(e2*t) mod N= m^(e1*s + e2*t) mod N

ounter(linem^(e1*s + e2*t) mod N = m^1 mod N = m mod N

ounter(linegcd(a, b) = s * a + t * b

ounter(lines * e1 + t * e2 = 1

ounter(lineounter(lineounter(lineounter(line
def gcd(a, b): if b == 0: return a return gcd(b, a % b)

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
def extended_gcd(a, b): if b == 0: return a, 1, 0 gcd, x1, y1 = extended_gcd(b, a % b) x = y1 y = x1 - (a // b) * y1 return gcd, x, y

ounter(lineounter(linegcd = x1 * b + y1 * (a - (a // b) * b) = y1 * a + (x1 - (a // b) * y1) * b

ounter(lineounter(lines = y1t = x1 - (a // b) * y1

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport gmpy2e1 = 35422e2 = 1033gcd, s, t = gmpy2.gcdext(e1, e2)

ounter(lineounter(lineounter(linegcd(e1, e2) = 1s = -334t = 11453

ounter(line-334 * 35422 + 11453 * 1033 = -11830948 + 11830949 = 1

ounter(linea * b ≡ 1 (mod N)

ounter(linec1^s mod N = c1^(-334) mod N = (c1^(-1))^334 mod N

ounter(linec1_inv = gmpy2.invert(c1, N)

ounter(linem = (c1_inv)^|s| * c2^t mod N

ounter(lineounter(lineounter(linepart1 = pow(c1_inv, abs(s), N) # (c1^-1)^334 mod Npart2 = pow(c2, t, N) # c2^11453 mod Nm = (part1 * part2) % N

ounter(lineounter(lineflag = bytes.fromhex(hex(m)[2:])print(flag.decode('ascii'))

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport gmpy2N = 162178605357818616394571566923155907889899677780239882906511996614607940884142045197452389471499799373787832649318837814454679970724845203557871078001956378966434166323827984964942729898095347038272003371167123553368531662277059263517900162297903110415768403265100411543878859321181606008503516896600638590699e1 = 35422c1 = 153249315480380808558746807096025628082875635601515291525075274335055878390662930254941118045696231628008256877302589689883059616503108946971165183674522403835250738176157466145855833767128209866527507862726083268576304163200171600023472544755768741118904892489037291247455823396160705615280802805803254323033e2 = 1033c2 = 5823189490163315770684717059899864988806118565674660089157163486577056500243194221873916232616081138765317598078910078375360361118674333149663483360677725162911935082290640547407140413703664960164356579153623498735889314476063673352676918268911309402784919521792079943937126634436658784515914270266106683548
# 使用扩展欧几里得算法求解 gcd(e1, e2) = s*e1 + t*e2gcd, s, t = gmpy2.gcdext(e1, e2)print(f"gcd(e1, e2) = {gcd}")print(f"s = {s}, t = {t}")
# 求c1的模逆元c1_inv = gmpy2.invert(c1, N)
# 计算明文part1 = pow(c1_inv, abs(s), N)part2 = pow(c2, t, N)m = (part1 * part2) % N
# 转换为字符串flag = bytes.fromhex(hex(m)[2:])print(f"Flag: {flag.decode('ascii')}")

ounter(lineounter(lineounter(linegcd(e1, e2) = 1s = -334, t = 11453Flag: flag{A_RSA_c0mm0n_m0dulu5_4tt4ck}

gcd(e1, e2) = 1：两个公钥指数互质

相同的模数N：两次加密使用同一个N

相同的明文m：对同一条消息进行加密

获得两个密文：能够截获c1和c2

不要复用模数N：每次生成密钥对时，都应该重新生成新的N值

使用填充方案：即使使用相同的N，通过随机填充(如OAEP)，每次加密同一明文也会得到不同的结果

密钥管理规范：遵循密码学最佳实践，避免为了便利而牺牲安全性

密码学的安全性不仅取决于算法本身，还取决于使用方式

看似微小的实现缺陷可能导致整个系统的崩溃

数学理论在密码攻防中扮演着关键角色


```
ounter(lineounter(lineounter(lineounter(lineounter(lineN = 162178605357818616394571566923155907889899677780239882906511996614607940884142045197452389471499799373787832649318837814454679970724845203557871078001956378966434166323827984964942729898095347038272003371167123553368531662277059263517900162297903110415768403265100411543878859321181606008503516896600638590699e1 = 35422c1 = 153249315480380808558746807096025628082875635601515291525075274335055878390662930254941118045696231628008256877302589689883059616503108946971165183674522403835250738176157466145855833767128209866527507862726083268576304163200171600023472544755768741118904892489037291247455823396160705615280802805803254323033e2 = 1033c2 = 5823189490163315770684717059899864988806118565674660089157163486577056500243194221873916232616081138765317598078910078375360361118674333149663483360677725162911935082290640547407140413703664960164356579153623498735889314476063673352676918268911309402784919521792079943937126634436658784515914270266106683548
ounter(lineounter(linec1 = m^e1 mod Nc2 = m^e2 mod N
ounter(lines * e1 + t * e2 = 1
ounter(linem = (c1^s * c2^t) mod N
ounter(lineounter(lineounter(lineounter(linec1^s * c2^t mod N= (m^e1)^s * (m^e2)^t mod N= m^(e1*s) * m^(e2*t) mod N= m^(e1*s + e2*t) mod N
ounter(linem^(e1*s + e2*t) mod N = m^1 mod N = m mod N
ounter(linegcd(a, b) = s * a + t * b
ounter(lines * e1 + t * e2 = 1
ounter(lineounter(lineounter(lineounter(line
def gcd(a, b): if b == 0: return a return gcd(b, a % b)
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
def extended_gcd(a, b): if b == 0: return a, 1, 0 gcd, x1, y1 = extended_gcd(b, a % b) x = y1 y = x1 - (a // b) * y1 return gcd, x, y
ounter(lineounter(linegcd = x1 * b + y1 * (a - (a // b) * b) = y1 * a + (x1 - (a // b) * y1) * b
ounter(lineounter(lines = y1t = x1 - (a // b) * y1
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport gmpy2e1 = 35422e2 = 1033gcd, s, t = gmpy2.gcdext(e1, e2)
ounter(lineounter(lineounter(linegcd(e1, e2) = 1s = -334t = 11453
ounter(line-334 * 35422 + 11453 * 1033 = -11830948 + 11830949 = 1
ounter(linea * b ≡ 1 (mod N)
ounter(linec1^s mod N = c1^(-334) mod N = (c1^(-1))^334 mod N
ounter(linec1_inv = gmpy2.invert(c1, N)
ounter(linem = (c1_inv)^|s| * c2^t mod N
ounter(lineounter(lineounter(linepart1 = pow(c1_inv, abs(s), N) # (c1^-1)^334 mod Npart2 = pow(c2, t, N) # c2^11453 mod Nm = (part1 * part2) % N
ounter(lineounter(lineflag = bytes.fromhex(hex(m)[2:])print(flag.decode('ascii'))
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport gmpy2N = 162178605357818616394571566923155907889899677780239882906511996614607940884142045197452389471499799373787832649318837814454679970724845203557871078001956378966434166323827984964942729898095347038272003371167123553368531662277059263517900162297903110415768403265100411543878859321181606008503516896600638590699e1 = 35422c1 = 153249315480380808558746807096025628082875635601515291525075274335055878390662930254941118045696231628008256877302589689883059616503108946971165183674522403835250738176157466145855833767128209866527507862726083268576304163200171600023472544755768741118904892489037291247455823396160705615280802805803254323033e2 = 1033c2 = 5823189490163315770684717059899864988806118565674660089157163486577056500243194221873916232616081138765317598078910078375360361118674333149663483360677725162911935082290640547407140413703664960164356579153623498735889314476063673352676918268911309402784919521792079943937126634436658784515914270266106683548
# 使用扩展欧几里得算法求解 gcd(e1, e2) = s*e1 + t*e2gcd, s, t = gmpy2.gcdext(e1, e2)print(f"gcd(e1, e2) = {gcd}")print(f"s = {s}, t = {t}")
# 求c1的模逆元c1_inv = gmpy2.invert(c1, N)
# 计算明文part1 = pow(c1_inv, abs(s), N)part2 = pow(c2, t, N)m = (part1 * part2) % N
# 转换为字符串flag = bytes.fromhex(hex(m)[2:])print(f"Flag: {flag.decode('ascii')}")
ounter(lineounter(lineounter(linegcd(e1, e2) = 1s = -334, t = 11453Flag: flag{A_RSA_c0mm0n_m0dulu5_4tt4ck}
```
