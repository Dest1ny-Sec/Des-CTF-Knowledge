---
title: 2025 强网杯 write up By Ginkgo
contest: 强网杯
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [Connection注入, X-User, The_Interrogation_Room, PoW暴力, 汉明码d=5, 校验矩阵P, GCD攻击, AES-CBC, MT19937-LLL, printf格式化, _IO_wfile_jumps, setcontext+61, ptrace-VM调试器, XXTEA, MMX编码]
attack_chain:
  - Web 题用 Connection: close,X-User 头部注入让服务端把 X-User 当 hop-by-hop
  - Java ProcessBuilder RCE 经 out0.setStringValue 弹结果
  - The_Interrogation_Room 25 轮，每轮 17 问（8位+9校验），暴力 4 位 PoW 后用汉明码 d=5 解码
  - Crypto 用 gcd(c,N) 拿 p,q 走 RSA-3 + AES-CBC(iv, key=long_to_bytes(c^d mod N)[:16])
  - MT19937 用 LLL 矩阵 (624 单 bit 状态) 还原 624*32 bit state
  - Pwn printf %hn 写 0x404090 改函数指针 + 二次 fmt 任意读
  - House of XXX 路径: 改 _IO_2_1_stdout_ 头 + setcontext+61 假 IO 触发 /bin/sh ORW (open/read/write flag)
  - Reverse: butterfly 二进制 MMX 编码 — XOR key8 → 16-bit 字内 swap → 64-bit ROL1 → 逐字节加 key8；解码逆向
  - Ptrace VM 调试器: int3→PEEKTEXT→int3_check→handler dispatch (RET/CALL/PUSH/JMP)
key_payload: 'Connection: close,X-User / 汉明码 d=5 校验矩阵 P / MT19937 LLL 矩阵爆破 / _IO_wfile_jumps+setcontext+61 假 IO 链 / MMX 编码逆向 (XOR→swap→ROL1→add) / ptrace int3 VM 调度'
one_liner: 强网杯 7 大题型混合集 — Web Connection 注入 + Crypto GCD/AES + MT19937 LLL + Pwn printf+House of XXX + Reverse MMX 编码 + ptrace VM 调度器。
lesson: 汉明码 d=5 校验矩阵 P 选满秩行可解码 2 个错；MT19937 单 bit 状态基底可建 GF(2) 上 LLL 还原；setcontext+61 配合 _IO_wfile_jumps-0x10 是 ORW RCE 经典链；MMX 编码是字节级流水线可完全逆向；ptrace int3 调度是 anti-RE 的 VM 形态。
quality: high
---

# 2025 强网杯 write up By Ginkgo

## 速读
ChaMd5 Ginkgo 团队风格 — 一篇覆盖 7 个完全不同方向的强网杯题型 EXP 大杂烩。

## 题型覆盖

### Web — X-User 信任
- 后端完全信任客户端 X-User 头
- 用 Connection 头注入把 X-User 标成 hop-by-hop 让服务端丢弃
- Flag: `flag{e5c09a17-be4a-4b68-a411-f93bb874b233}`

### Java — ProcessBuilder RCE
- `new ProcessBuilder("/bin/sh","-c","cat /flag")` 注入到 out0.setStringValue
- readLine 累加 + waitFor 拼 EXIT_CODE

### The_Interrogation_Room (Math/Pwn 混合)
- PoW: SHA256(XXXX+suffix) == target，遍历 4 字符组合
- 25 轮 × 17 问 = 8 基础位 + 9 校验位
- 校验矩阵 P 选满秩使最小汉明距 d=5
- 收到含 2 错回答后用汉明距最小化还原 8 位真实秘密
- flag{e5c09a17...} 来源

### Crypto — GCD Attack
- `gcd(c, N) == p`，直接得 p,q
- `key = long_to_bytes(pow(c, d, N))[:16]` 作 AES-CBC key
- iv 固定解出明文

### Crypto — MT19937 LLL
- 624 状态基底单 bit 启动 Random.setstate
- `build_row` 拿 NUM_ITER bits 作矩阵行
- `L.solve_left(R)` + `left_kernel().basis()` 得 1024 个候选
- `rng.shuffle(x) × 2025` 逆推原序找 flag 子串

### Pwn — printf + fmt + 整数溢出
- 选项 1 读 0x100 字节含 `%9$p` 泄 canary + `%12$hn` 改写 0x404090
- 选项 2 触发 -1 绕过边界，第二次 fmt `%12$s` 读 target
- target = leaked + 0x1e0 (返回地址) → system

### Pwn — House of XXX / setcontext+61
- 改 _IO_2_1_stdout_ 为 fake_file
- setcontext+61 + ucontext_t 触发 ORW ROP
- ROP: open /flag → read → write stdout
- `_IO_wfile_jumps + 0x10` 作 vtable

### Reverse — butterfly 二进制 MMX 编码
- 8 字节块编码: XOR key8 → 16-bit 字内 swap → 64-bit ROL1 → 逐字节加 key8
- 解码: 减 key8 → ROR1 → swap → XOR
- decode_mmx.py 提供完整实现

### Reverse — Ptrace VM 调试器
- 父进程 fork 子进程，子进程跑原 binary，父进程用 ptrace 调度
- int3 (0xCC) 触发 vm_debugger_loop
- PTRACE_GETREGS / PEEKTEXT / POKEDATA 读写寄存器+内存
- VM 指令：RET (handler 2) / CALL (3) / PUSH (4) / JMP (5)
- IDA Python 脚本映射 int3 → 原函数名 (puts/printf/memset/read/srand/setvbuf/rand)

## 评价
一篇 7 题 EXP 完整集合，密度极高，从 Web 头部 trick 到 VM 调度器逆向全覆盖。代码质量参差但思路骨架完整，是强网杯 2025 的多面手复盘。
