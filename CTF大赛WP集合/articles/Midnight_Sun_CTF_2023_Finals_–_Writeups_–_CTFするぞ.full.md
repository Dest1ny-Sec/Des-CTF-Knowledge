---
title: Midnight Sun CTF 2023 Finals – Writeups – CTFするぞ
contest: Midnight Sun CTF
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags:
- 多素数 RSA
- E 异常
- 系统调用 system("$PROG '<arbitrary string>'")
attack_chain: '|'
key_payload: '|'
one_liner: Midnight Sun CTF 2023 Finals 几道 reverse + crypto 综合题，多组 RSA + 共模攻击 + 整数算术 (a+b) 构造字符串执行。
lesson: '|'
quality: medium
full_path: Midnight_Sun_CTF_2023_Finals_–_Writeups_–_CTFするぞ.full.md
meta_path: Midnight_Sun_CTF_2023_Finals_–_Writeups_–_CTFするぞ.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Midnight Sun CTF 2023 Finals – Writeups – CTFするぞ。Midnight Sun CTF 2023 Finals 几道 reverse + crypto 综合题，多组 RSA + 共模攻击 + 整数算术 (a+b) 构造字符串执行。。经验：|
category: crypto
subcategory: oracle
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/131988.html
reasoning_chain:
- 触发点：多次 RSA 加密 + E 异常 (E=2 不是 RSA) + system("$PROG '<arbitrary string>'") → 假设：Rabin/Paillier 类变种 + 整数算术构造命令注入
- 第一组数据：22616 (stack canary 0x5858) / 20450 (func1 0x4fe2) / 10596 (skip 0x2964) / 65280 (arg1 0xff00) → 假设：常量来自反汇编
- 动作：观察第二组+第三组 N 相同但 e 不同 → 假设：共模攻击 → egcd(e1,e2) 求 s1+s2 = 1 → m = pow(c1,s1,N)*pow(c2,s2,N) % N
- 假设：多组 RSA 都用同一 N 不同 e → 动作：扩展欧几里得算法拼所有 e 的 CRT 解
- 触发点：system("$PROG '<input>'") 字符串 → 假设：用户可控 input 注入 → 动作：构造 system("$PROG 'a'+'b'") 类算术拼字符串
- 动作：用整数算术 (a + b = ans) 构造 'cat /flag' 字符串 → 假设：算式结果作为命令参数拼到 system()
- 观察：服务端读用户输入做 a+b 算术 + 拼命令执行 → 完成
failed_attempts:
- 试图按标准 RSA 解密（pow(c,d,n)） → 失败：N 不是 RSA modulus，是 Rabin 类（E=2）或多素数 N
- 试图单组 RSA 暴力分解 N → 失败：N 是大素数乘积，factordb 不可解，必须走共模攻击
- 试图直接拼接 shell 命令字符串 → 失败：题目只接受整数算术结果作为字符串，必须用 + 运算构造字符
key_observations:
- 共模攻击（相同 N + 不同 e）= egcd(e1,e2) + pow(c1,s1,N)*pow(c2,s2,N) % N 还原 m
- E=2 不是 RSA 是 Rabin 密码（CRT 4 个解），E=多个素数乘积也是 Rabin 变种
- system("$PROG '<input>'") + 整数算术 = 用户可控输入转命令注入（拼字符串而非直接注入）
- 0xff00 / 0x1d0 / 0x1214 等 hex 常量是反汇编出来的指令片段，可作为 flag 解密的种子
- Midnight Sun CTF 是瑞典 0xL4ugh CTF 团队组织的国际赛
prerequisites:
- RSA 数学基础（modular exponentiation / egcd / CRT）
- Rabin 密码（E=2 + CRT 4 个解 + sqrt mod p/q）
- Linux 命令注入（system() + 字符串拼接）
- pwntools / sage 数学工具
---
# Midnight Sun CTF 2023 Finals – Writeups – CTFするぞ

> 原文: https://www.ctfiot.com/131988.html
> ID: 131988


```
22616 = = = = = = = = = C ; stack canary (0x5858)
20450 = C ; func1 (0x4fe2)
10596 = C ; skip (0x2964)
65280 = C ; arg1 (0xff00)
7330 = C ; arg2 (0x1ca2)
20699 = C ; func2 (0x50db)
464 = C ; loop (0x1d0)
0 = C ; arg1 (0x0)
4628 = C ; arg2 (0x1214)
6970 = Q ; arg3 (0x1b3a)
Public Exponent: 65537
Modulus: 8183083614123980651512525726265039763297170592399337374069708919926046325913623412792726783191923340532116587489748386113782581259412232424196738634940809
Ciphertext: b'(\xa6\xc0\xee\xb5\x9d\xd2\xc8\xe6\xa1\xb1\xcf:\x8b\xdcgx\xef\xb4\t\x7fvM@\xc8\x98\xbd\x80\xad\x13\x11\xeb\x97\xef\xc84\xd6|\x93E@\xeb\xc9\xf9\x0b\x86\xc7\x8bpKV\xe8\xa1\xa4&X\x14\\\x1a\xe3\x13\x8d\x8d6'
Public Exponent: 81527149853274967867330281122861369134002594020874386569175070591393763589124283222257680735360206160019714178475186119840676412580184783642914952823718854196285068193471576875760518418570508606597801241354462995303092313113267959493950020688558073609011113475992265891863855436963447737070556709073024059749
Modulus: 105485909539302343682393765142198393869888400422595584344848080319220554344765142068633113057605072008120447995511459791164086717714452445525900872135444441922799547203637125587718326496756865379111734536835717969217501986460486866455030114291836448819270922526967276362623954616008938297593516881809069452459
Ciphertext: b"\x0c\x01\x8b\x84\x02P\x80_A\x1c|\x1f\xd7\xafP\xf7\x14\xb3\x1b\xb4\xcb\x90)\x1f\x1d/\xe0\\\x861Y]+7}\x97\xec\x9b^B\x1b\xc76\xc4 kb'\xaa\xda\xbf\x95\xeaP\x0b5\xb9Z\x7f\xe6C\xb2H.v\x18:ga\xee\xd7=}\xfb\xda\xbd\xee\xa8\x82\xf2\xc2\x1c6\\}\xd7\x005AW\xc0*hRNZ\x86\xfa\x80\xcb\t8\xbe9ad2}\x84\x82\xf2\x88h\x87\x85\xcb\x00E\xb4\xae\xb9\xd1\x15g\xbe\x18!\x8e"
Public Exponent: 90051294818134602141342465972381725307723336343068630953802954374926328987011486242807231248352006000143918922842329124501936958773012452561039323344339325165614434298436842264587505847772729164638758139465380776251275917722434711009950711165155879895556773415263339750741308013278846283398286170778381488987
Modulus: 105485909539302343682393765142198393869888400422595584344848080319220554344765142068633113057605072008120447995511459791164086717714452445525900872135444441922799547203637125587718326496756865379111734536835717969217501986460486866455030114291836448819270922526967276362623954616008938297593516881809069452459
Ciphertext: b'\x03[\xb4\xb0\x08\xde\x8b\xf9\xf4{\x04\xc8\x9c7\xc2\x84\x1f\x8e\xd4\xd0\x9f\xf4H\xe3(|\xbb\xf5N\xd9~\xbe\x13\xb8\xf5\x1a\xe8\xe21\xc2\xf2D\xb3D\x8a\n)\x14\xe2R\xad\x97\xbe\xcf\n\x1b\xf5I\xad\xf7s\x1d\xfbzq\x17\xa9\x80\xf0\xc6\xb0\x80y\xb9\x7f\xbe\xd0a~\xdf+:\xaa\x05=\xdb\x12"\xb5\x16\x1d\xb6\x12\xd5\xa5i\x9f\x19\xd3\xba\xc4\x11\x19\x9b\xd3\n\x81o\xc0\x9c\xcc\xebE{\xc5\x15\xdd\x92\xefq!h\xee\xb4\x16\x9a\xe4\xb5'
system("$PROG '<arbitrary string>'");
```
