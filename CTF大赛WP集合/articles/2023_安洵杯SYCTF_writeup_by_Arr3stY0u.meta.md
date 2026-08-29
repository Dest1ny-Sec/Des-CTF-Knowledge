---
title: 2023 安洵杯 SYCTF WriteUp by Arr3stY0u
contest: 安洵杯 SYCTF 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [数独游戏, pwntools, telnetlib, 贪吃蛇, ARC4, IDA, claripy符号执行, printfFSOP, House of Apple, RSA]
attack_chain:
  - Sudoku 数独游戏用 pwntools 连远程 + 回溯算法 5 秒内解 9x9
  - telnetlib 收数独 + 算解 + WASD 模拟键盘操作提交
  - librosa 音频 2*audio1 - audio2 = 还原信号
  - ez_cpp3 用 exitcode 字符爆破每一位 flag
  - IDA ida_bytes.get_dword 读 6 个 10x10 地图找跳关路径
  - ARC4 + srand(0x94307F97) + 361 步贪吃蛇 RC4 加密
  - claripy BVS 符号执行 enc1/enc2/enc3 还原 flag
  - fin/mul 数组除法 + XOR + 半字节交换还原 flag
  - printf $p 泄漏 heap/libc/stack 配合 _IO_wfile_jumps 劫持 FSOP
  - libc 2.35 House of Apple 2 fake io + setcontext+61 ORW
  - RSA p-q 已知 256-bit 用连分数 + is_prime 验证分解
  - Coppersmith + m^p*Q*R 同余分解 pqr 三素数
key_payload: 'SYC{I_h0pE_you_cAn_FInd_d4eam}'
one_liner: 综合 9 题：数独贪吃蛇符号执行 FSOP RSA-Coppersmith 全面覆盖。
lesson: 数独用回溯；贪吃蛇 RC4 用 srand+ARC4；claripy BVS 做符号执行；libc2.35 House of Apple 2 是 IO 攻击标配。
quality: high
---

# 2023 安洵杯 SYCTF WriteUp by Arr3stY0u

## 来源
- 原文：ctfiot.com/120089.html
- 作者：Arr3stY0u

## 9 道题详解

### 1. Sudoku 数独（pwn + 回溯）
- pwntools 连远程 + Python 回溯算法
- 5 秒内解 9x9 数独
- telnetlib 版本用 WASD 模拟键盘操作提交答案

### 2. 音频还原（librosa）
```python
import librosa
audio1, sr1 = librosa.load('2.wav', sr=None)
audio2, sr2 = librosa.load('3.wav', sr=None)
result = 2 * audio1 - audio2
sf.write('result.wav', result, sr1)
```

### 3. ez_cpp3（exitcode 爆破）
```python
for ch in table:
    flag = (theflag + ch).ljust(32, '#')
    exitcode = os.system(f"echo {flag} | ez_cpp3.exe 1>&0")
    if exitcode >= len(theflag) + 1: theflag += ch
```
- 用 exit code 当 oracle，32 字符爆破

### 4. 跳关地图（IDA 静态分析）
- `ida_bytes.get_dword(0x140005040 + ...)` 读 6 个 10x10 地图
- 找 level 0→1→2→3→4→5 的跳转路径，提取 flag
- 最终 path: `wddwwdddddDdwwwdddsdddddDwwWassaaaaaaaaAsssssssssSddwwdwwwwwWw`

### 5. 贪吃蛇（RC4 + 路径）
```python
srand(0x94307F97)
seed_list = [rand() for i in range(361)]
# 贪吃蛇路径 pos[i] = (y<<8 | x)
# RC4 key = srand(seed) → rand() 生成的随机字符串
data = enc(data, 3+i, pos)
```
- 361 步贪吃蛇用 srand + RC4 加密
- 还原路径 = srand seed sequence

### 6. ez_cpp（claripy 符号执行）
```python
from claripy import BVS
tmp_flag = [BVS(f'flag{i}', 8) for i in range(30)]
# enc1: 偶数轮 tmp_flag[i] = (unk + tmp_flag[i]) ^ 0x17
# enc2: 各位置 += -= ^=
# enc3: 奇数轮 15 个 swap
solve = Solver()
for i in range(4): enc1(); enc2(); enc3()
solve.add(enc_flag[i] == tmp_flag[i])
print(solve.eval(flag, 2))  # SYC{I_h0pE_you_cAn_FInd_d4eam}
```

### 7. fin/mul 数组还原
- `flag[i] = fin[i] / mul[i+18 mod 36]`
- 反向 XOR + 半字节交换还原 flag

### 8. pwn - printf FSOP + House of Apple
- `printf %p %11$llx %15$p` 泄漏 heap/libc/stack
- 篡改 printf_arginfo + printf_functable 触发 FSOP
- libc 2.35 House of Apple 2: `fake_io + setcontext+61` 走 ORW
- `shellcraft.open(fake_io_addr, 0) + sendfile(2, 3, 0, 0x50)`

### 9. crypto - RSA 连分数 + Coppersmith
- 数据 1.4287... 走 `continued_fraction` + `convergents`
- 找 a/b 都是 256-bit prime
- 解 p-q + Coppersmith 分解 pqr

## 关键技巧
- **数独回溯**：Python `is_valid + find_empty + solve` 5 秒内
- **贪吃蛇路径**：srand seed + 步长 + RC4 加密
- **claripy BVS**：逐字节 BVS 求解非线性方程
- **libc 2.35 FSOP**：House of Apple 2 + _IO_wfile_jumps + setcontext+61
- **连分数 RSA**：continued_fraction 找相邻素数 p,q

## 适用场景
- 数独 + 贪吃蛇 AI
- 符号执行入门
- libc 2.35 IO 攻击
- RSA 连分数分解
