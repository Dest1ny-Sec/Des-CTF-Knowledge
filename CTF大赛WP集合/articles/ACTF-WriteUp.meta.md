---
title: ACTF WriteUp
contest: ACTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [XOR爆破, zstd循环解压, RSA e=-1,b=-2*n方程, sympy.solve, libc-2.27 64堆菜单, ret2csu ARM aarch64, 2048 qemu, Minimaxab AI, Process Hollowing, RunPE, FindResourceW, VirtualAllocEx, WriteProcessMemory, SetThreadContext, BigI 128进制, encrypt=add+mul+subabs多次轮, web3 6666链]
attack_chain:
  - Crypto1: a,b 两数组 XOR 27 字符
  - Crypto2: zstd/bunzip2 循环解压 10000 次出 flag ACTF{r0cK_4Nd_rolL_1n_C0mpr33s1Ng_aNd_uNCOmrEs5iNg}
  - Crypto3: RSA e=-1 方程 -m*x² + x - e*n = 0, sympy.solve 解出 m=46280, 求 p,q
  - Pwn1: libc-2.27 64 堆菜单 0/1/2/3/4 add/delete/edit/show/q, 多次 edit 改 size 字段 + unlink 拿 libc
  - Pwn2: aarch64 qemu 跑 2048 游戏, ret2csu 调 system 拿 shell
  - Reverse1: PE Process Hollowing (RunPE), FindResourceW/LoadResource/LockResource 读资源, VirtualAllocEx 申请空间, WriteProcessMemory 写入, SetThreadContext + ResumeThread
  - Reverse2: BigI 128 进制数, encrypt 8 轮: add+mul+subabs+add+mul+subabs+add+subabs+add+subabs+add+subabs, 已知 targ 反推
  - Web3: chainId=6666, bet 合约, nonce 推测 + pre_time 修正
key_payload: 'libc-2.27 64 堆菜单 / aarch64 ret2csu / 2048 Minimaxab AI / Process Hollowing RunPE / BigI 128 进制多项式加密 / chainId 6666 bet'
one_liner: ACTF 综合多题 — XOR爆破 + zstd循环解压 + RSA e=-1 方程 + libc-2.27 堆菜单 + aarch64 ret2csu 2048 AI + RunPE Process Hollowing + BigI 128 进制 + chainId 6666 bet。
lesson: ACTF 风格是把所有方向都做一遍；Process Hollowing 的关键是 FindResourceW 找 PE 资源；BigI 128 进制加密逆推可直接列线性方程组；2048 这类游戏可接 Minimax AI。
quality: high
---

# ACTF WriteUp

## 速读
ACTF 2022 全方向多题合集 — Crypto/Pwn/Reverse/Web3 都有。

## Crypto
1. **XOR**: 两数组 27 元素逐位 XOR
2. **zstd 套娃**: 循环解压 10000 次出 flag
3. **RSA e=-1**: 方程 `-m*x² + x - e*n = 0`, sympy.solve 解 m=46280, 求 p,q

## Pwn
1. **libc-2.27 64 堆菜单**: 0/1/2/3/4 add/delete/edit/show/q
   - 多次 edit 改 size 字段做 unlink
   - show 4,4 拿 heap_addr
   - libc.address = u64(...)-libc.symbols[...]
2. **aarch64 2048 qemu**: 64-bit qemu-aarch64 跑游戏
   - ret2csu 调 system
   - 4x4 棋盘走 w/s/a/d

## Reverse
1. **Process Hollowing (RunPE)**: PE 子进程注入
   - FindResourceW/LoadResource/LockResource 读嵌入 PE
   - VirtualAllocEx 申请远进程空间
   - WriteProcessMemory 写多段 (j 段 sections)
   - SetThreadContext + ResumeThread 启动
2. **BigI 128 进制**: j_bigIadd/mul/subabs 多轮加密
   - 8 轮 add+mul+subabs 链
   - 已知 targ 列表反推输入

## Web3
- chainId=6666 自定义链
- bet 合约, nonce 读 storage[2]
- pre_time 推测 (now_block-start_block)*30+start_time+offset
- Web3.keccak 算 guess_num % 12
- 调 bet() 函数
