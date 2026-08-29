---
title: EHAX CTF 2026 Writeup by Mini-Venom
contest: EHAX CTF 2026
year: 2026
difficulty: hard
vuln_type: web_unknown
tags: [pwn, slice-uaf, double-free, built-in-func-ptr-overwrite, bytecode-vm, aarch64, aarch64]
attack_chain:
  - Slice和Buffer共享data_ptr但GC不知道
  - Buffer被GC释放→Slice仍引用data_ptr
  - BUILTIN复用该chunk通过Slice PRINTB泄露func_ptr
  - Slice被GC再次释放同一data_ptr→double free
  - NEWBUF第二次获得同一chunk通过WRITEBUF覆写func_ptr
  - CALL builtin→跳转到execve("/bin/sh")
  - CrackMe: 8函数+32字节key约束z3求解
  - AES ghost key: key[:16] SHA256+AES-CBC key[16:] MD5 IV
  - 智能合约: EvilGov pwn() sstore(0,0) sstore(1,caller())
  - Python pyc: grid 10x10迷宫+N/S/E/W路径
key_payload: func_ptr overwrite → execve("/bin/sh")
one_liner: EHAX 2026 6题：Slice UAF+CrackMe AES+迷宫+智能合约+pyc
lesson: Slice-Buffer共享data_ptr是GC漏判导致double-free经典模式
quality: high
---

# EHAX CTF 2026 Writeup by Mini-Venom

## 题目信息
- 比赛：EHAX CTF 2026
- 战队：Mini-Venom（ChaMd5）
- 涵盖：PWN + Rev + Crypto + Blockchain + Misc

## 关键攻击链
### 1. SarcAsm（PWN）Slice UAF
- Slice 和 Buffer 共享 `data_ptr`，但 GC 不知道
- Buffer 被 GC 释放后 Slice 仍引用 `data_ptr` → dangling pointer
- BUILTIN 复用该 chunk，通过 Slice PRINTB 泄露 `func_ptr`
- Slice 被 GC 再次释放同一 `data_ptr` → double free
- NEWBUF 第二次获得同一 chunk → WRITEBUF 覆写 `func_ptr`
- CALL builtin → 跳转到 `execve("/bin/sh")`

### 2. CrackMe（REV）
- 8 函数约束：长度 32 + tag XOR + nibble + colsum + pairs + sbox + LFSR
- z3 求解 32 字节 key
- AES: `key[:16] SHA256` + `key[16:] MD5 IV`
- flag: `crackme{AES_gh0stk3y_r3v3rs3d!!}`

### 3. Maze（Misc）
- 10x10 网格 + N/S/E/W 路径
- 哈希 `h(path) = (73244475 * rol32(v^ch, 13)) & 0xFFFFFFFF`
- flag: `EHAX{2E3S2W6S8E2NE2S}`

### 4. Blockchain EvilGov
- `sstore(0, 0)` + `sstore(1, caller())` 覆写 Vault
- `setGovernance` + `execute` + `withdraw` 三步
- `sload(0) == 0 && sload(1) == player` 判定

### 5. ghost_8d3f4a91
- `0xCD9AADD8D9C9A989` mix64 生成 keystream
- 解：明文 `EH4X{fr3k7_fri3n5dly_1nt3rf4c35_0nc3_4g41n}`

### 6. ML 模型精准破坏
- 准确率 0.94 → 0.69（精确翻转 25% 样本）
- `np.argsort(confidence)[-n_flips:]` 选最自信样本
- 强行 flip label

## 评分
- quality: high（6 题完整 exp + z3 约束 + AES 密钥派生）
