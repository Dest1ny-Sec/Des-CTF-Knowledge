---
title: Midnight Sun CTF 2023 Finals – Writeups – CTFするぞ
contest: Midnight Sun CTF
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags: [多素数 RSA, E 异常, 系统调用 system("$PROG '<arbitrary string>'")]
attack_chain: |
  1. RSA 多组数据: 不同的 (Public Exponent, Modulus, Ciphertext)
  2. 第一次: 22616 (stack canary 0x5858) / 20450 (func1 0x4fe2) / 10596 (skip 0x2964) / 65280 (arg1 0xff00) / 7330 (arg2 0x1ca2) / 20699 (func2 0x50db) / 464 (loop 0x1d0) / 0 (arg1 0x0) / 4628 (arg2 0x1214) / 6970 (arg3 0x1b3a)
  3. 第二次 + 第三次: N 相同 (105485909539302343682393765142198393869888400422595584344848080319220554344765142068633113057605072008120447995511459791164086717714452445525900872135444441922799547203637125587718326496756865379111734536835717969217501986460486866455030114291836448819270922526967276362623954616008938297593516881809069452459), e 不同 → 共模攻击
  4. system("$PROG '<arbitrary string>'"): 通过算术运算构造命令字符串执行
key_payload: |
  # 共模攻击 (相同 N, 不同 e):
  from functools import reduce
  from Crypto.Util.number import *
  
  N = 105485909539302343682393765142198393869888400422595584344848080319220554344765142068633113057605072008120447995511459791164086717714452445525900872135444441922799547203637125587718326496756865379111734536835717969217501986460486866455030114291836448819270922526967276362623954616008938297593516881809069452459
  e1 = 81527149853274967867330281122861369134002594020874386569175070591393763589124283222257680735360206160019714178475186119840676412580184783642914952823718854196285068193471576875760518418570508606597801241354462995303092313113267959493950020688558073609011113475992265891863855436963447737070556709073024059749
  e2 = 90051294818134602141342465972381725307723336343068630953802954374926328987011486242807231248352006000143918922842329124501936958773012452561039323344339325165614434298436842264587505847772729164638758139465380776251275917722434711009950711165155879895556773415263339750741308013278846283398286170778381488987
  c1, c2 = ..., ...
  
  def egcd(a, b):
      if a == 0: return b, 0, 1
      g, x, y = egcd(b % a, a)
      return g, y - (b // a) * x, x
  
  g, s1, s2 = egcd(e1, e2)
  m = (pow(c1, s1, N) * pow(c2, s2, N)) % N
one_liner: Midnight Sun CTF 2023 Finals 几道 reverse + crypto 综合题，多组 RSA + 共模攻击 + 整数算术 (a+b) 构造字符串执行。
lesson: |
  - Midnight Sun CTF 是瑞典 0xL4ugh CTF 团队组织的国际赛
  - 多组 RSA 数据可用共模攻击 (相同 N, 不同 e)
  - 整数算术 (a + b = ans) 题目可构造 system("$PROG '<input>'") → 用户可控输入
  - 0xff00 / 0x1d0 / 0x1214 / 0x1b3a 等 hex 常量是反汇编出来的指令
  - stack canary 0x5858 是程序自带弱 canary
quality: medium
---

# Midnight Sun CTF 2023 Finals – Writeups – CTFするぞ

> 来源: ctfiot.com 131988

## 题目分析

**第一组数据：**
```
22616 = stack canary (0x5858)
20450 = func1 (0x4fe2)
10596 = skip (0x2964)
65280 = arg1 (0xff00)
7330 = arg2 (0x1ca2)
20699 = func2 (0x50db)
464 = loop (0x1d0)
0 = arg1 (0x0)
4628 = arg2 (0x1214)
6970 = arg3 (0x1b3a)
```

`stack canary = 0x5858` 是程序自带的弱 canary。

## RSA 多组数据

**第二 + 第三组：**
- 相同 Modulus N = 10548590953930234...9452459 (512-bit)
- 不同 Public Exponent: e1 ≠ e2
- 同样长度的 Ciphertext

**→ 共模攻击（Common Modulus Attack）：**

```python
from functools import reduce
from Crypto.Util.number import *

def egcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = egcd(b % a, a)
    return g, y - (b // a) * x, x

g, s1, s2 = egcd(e1, e2)
m = (pow(c1, s1, N) * pow(c2, s2, N)) % N
long_to_bytes(m)
```

## system("$PROG '<arbitrary string>'")

题目类似 "a + b = ans" 的算术题：
- 用户输入两个数字 `a` 和 `b`
- 程序计算 `ans = a + b`
- 程序执行 `system("$PROG '<ans>'")`
- 如果能把 `ans` 构造为 shell 命令，就 RCE

## 评价

Midnight Sun CTF 2023 Finals 速查，亮点是：
- **共模攻击** 恢复多组 RSA
- **算术题 + system()** 形式 RCE
- **0x5858 弱 canary** 是入门 reverse 题标志

Midnight Sun CTF 是瑞典 0xL4ugh 团队组织的国际赛，参赛队伍以欧洲安全研究团队为主。
