---
title: SEKAICTF 2024 Writeup – Polaris战队
contest: SEKAICTF
year: 2024
team: Polaris
rank: 55
difficulty: medium
vuln_type: pwn_unknown
tags: [nolibc, custom-protocol, group-theory, randomness-recovery]
attack_chain:
- 构造大量 add chunk 触发 tcache 耗尽
- 通过 set bitmap attribute 翻转 EPROCESS 关键位完成 EoP
- 远程 nolibc 触发 show_win 弹出 flag
- 客户端通过 judge 二分位 + reseed 重置 PRNG 状态
- 利用 fight_bot 写任意 64-bit word 至 libssl 内部 FILE 结构
- hijack IO 改写 stdout vtable 调用 system
- CIPHER_SUITE randbelow 2^256 作为 random.seed 输入
- 构造 GSIZE=8209 阶群 G 与 GNUM=79 阶非交换积
- gexp(tuple(g)) 计算置换 g 的幂
- 已知明文 + 密文 + 公钥解 DLP 还原私钥
key_payload: judge(int('1'*bit+'0'*(64-bit), 2))  # PRNG 状态位判定
one_liner: 50+ 道 PWN/Crypto/Misc 联合战场，Polaris 靠 nolibc EoP + Group Theory DLP 攻破密码套件。
lesson: 自研协议常依赖「randbelow」类可种子化 PRNG；一旦能二分位恢复状态即等于控制输出流。
quality: high
---
# SEKAICTF 2024 – Polaris 第 55

## 1. PWN 1 - nolibc（EoP）
定制 register/login/add/del/show/save/load/quit 菜单。`save` + `load` 复用 stdio 路径触发 `getchar` 循环写死到 EPROCESS 关键偏移；`dele(0); load("/bin/sh")` 触发 shellcode；用 set bitmap attribute 翻转 token 字段完成 EoP。

## 2. PWN 2 - speedpwn
二进制 PRNG reseed 后用 fight_bot 输出 0/-1 决定每 bit 值。Stage 1 二分定位 bit_number；Stage 2 复用 leak 逐位恢复 libc；Stage 3 构造 fake FILE hijack IO 调 system 弹 shell。

## 3. PWN 3 - Life Simulator 2
C++ 模拟经营。`sell_company` 在 budget==0 时仍允许 UAF；`generate_profit` 用 pow() 溢出使 budget 归 0，触发 use-after-free 串联 fake_company_vector 改 worker 字段，最终控制 RIP。

## 4. Crypto - random CIPHER_SUITE
Alice/Bob 双向 ECDH-like 协议，CIPHER_SUITE = `randbelow(2**256)` 作为 `random.seed`。B1/A1/B2 三组置换间存在 DLP 关系；构造 8209 阶基础置换群 ×79 次幂形成乘法关系，用 `gexp` 还原 key 后 `key_replay` 拼接出 flag。

## 5. Misc - Miku vs Machine
贪心构造每个歌手演出时间 = m，每场换人 ≤1。fuzz 发现校验宽松，输出合法 schedule 即可。
