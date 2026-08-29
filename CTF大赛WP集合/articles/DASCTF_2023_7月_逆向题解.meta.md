---
title: DASCTF 2023 7月 逆向题解
contest: DASCTF
year: 2023
difficulty: medium
vuln_type: reverse
tags: [controlflow-flatten, matrix-inverse, rsa-128bit, tea-decrypt, custom-vm, idct]
attack_chain:
  - controlflow: 数组 swap 还原
  - mod 3 + 加 i + XOR i*(i+1)
  - 减 i*i + XOR 0x401
  - webserver: 4x10 矩阵 P * Q.inv mod 251
  - TCP: 128 bit RSA p,q 已知
  - 60 字节密文解 phi 后 pow(.,phi,n)
  - TEA 32 轮 delta=0x9e3779b9
  - 12 字节指令头解析
  - seg4-7 拼装 flag
key_payload: 控制流平坦化还原 + 矩阵求逆 + RSA+TEA
one_liner: DASCTF 2023 7 月逆向 3 题：控制流平坦化/矩阵求逆解密/128 位 RSA+TEA 自定义 VM。
lesson: 控制流平坦化的逆向要点是把"被打散的 state 序列"用 Python 数组 ops 重新串起来执行。
quality: high
---

DASCTF 2023 7 月逆向 3 道题：controlflow / webserver / TCP。

**controlflow** — 40 元素数组 S 操作序列。逆向代码：
```python
for i in range(0, 20, 2):
    S[11 + i], S[10 + i] = S[10 + i], S[11 + i]  # 交换相邻对
for i in range(40):
    assert S[i] % 3 == 0
    S[i] //= 3; S[i] += i
for i in range(20):
    S[10 + i] ^= i * (i + 1)
for i in range(40):
    S[i] -= i * i; S[i] ^= 0x401
print(''.join(chr(s) for s in S))
```
整题核心是把"switch case state machine"反编译为线性数组操作。

**webserver** — 4×10 矩阵 P 与 10×10 矩阵 Q，已知 `F = P * Q^(-1) mod 251`，用 sympy 求逆得明文。

**TCP** — 自定义 TCP 协议 + 128 位 RSA + TEA 加密。
- n 是 128 bit，p=1152921504606848051 + q=2152921504606847269 已知
- e=0x00010001000000000000000000000000（超长 e，构造 phi 后 inverse 求 d）
- 60 字节密文分 6 段，每段 pow(c, phi, n) 解 8 字节 RSA
- 48 字节明文前 32 字节为 TEA key，后 16 字节为 XOR key
- TEA delta=0x9e3779b9，LIMIT=0xffffffffffffffff，从 s=0x13c6ef3720 减 32 次
- 12 字节指令头解析：a0 是 opcode（1=print/2=store/3=input/4=show/5=execute/0=end），a1 是段号，a2 是长度
- 解压后 4 段 seg4-7 各 400 字节交错拼装 flag

加密函数 `f(m, a, b)` 是 `__int128` 模乘：while b 循环累加 `(a^(b&1) * x) mod m`。
