---
title: D^3CTF 2024 逆向 Writeup
contest: D3CTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [xtea-variant, ida-python, recur-func, rand-graph, dfa-attack]
attack_chain:
  - XTEA 变体 delta=0xE8017300
  - 32 轮减法 + 32 轮加法
  - 暴力逆向还原 fakeflag
  - 32 轮右移 1 位 + 0x84A6972F 异或
  - IDA Python recur 找函数关系
  - 提取 xor 推导下一函数
  - rand 关系图遍历
key_payload: XTEA 变体 + IDA 递归脚本
one_liner: D^3CTF 2024 逆向 2 道：XTEA 变体解密 + IDA Python 递归函数图。
lesson: XTEA 变体只需调整 delta 和轮数；IDA Python recur() 适合还原复杂调用图。
quality: high
---

D^3CTF 2024 逆向 2 道高质量 WP。

**题 1: XTEA 变体 + 32 轮减/加法**

```python
flag = [0x5406CBB1, 0xA4A41EA2, 0x34489AC5, 0x53D68797, 0xB8E0C06F, 0x259F2DB, 0x52E38D82, 0x595D5E1D]
k2 = 0xE8017300
k3 = 0xFF58F981
key = [0x5454, 0x4602, 0x4477, 0x5E5E, 0x33, 0x43, 0x54, 0x46]

for i in range(0, 7, 2):
    v6 = flag[i+1]
    v7 = flag[i]
    a2 = k2
    # 32 轮减法
    for _ in range(32):
        a2 = a2 + 0x100000000 - k3
        a2 &= 0xFFFFFFFF
    # 32 轮加法 + 减法
    for _ in range(32):
        a2 += k3; a2 &= 0xFFFFFFFF
        v6 -= ((v7 + ((v7 << 5) ^ (v7 >> 6))) ^ (key[(a2>>11)&3]+a2) ^ 0x33)
        v6 &= 0xFFFFFFFF
        v7 -= ((v6 + ((v6 << 4) ^ (v6 >> 5))) ^ (key[a2&3]+a2) ^ 0x44)
        v7 &= 0xFFFFFFFF
    flag[i+1] = v6; flag[i] = v7
print(''.join(f.to_bytes(4, "little").decode() for f in flag))
# fakeflag{Is_there_anywhere_else}
```

**题 2: 32 轮右移 1 位 + 0x84A6972F 异或**

```python
for _ in range(32):
    v0 = flag[i]
    if (v0 & 1) == 1:
        v0 ^= 0x84A6972F
        v0 = v0 >> 1
        v0 |= 0x80000000
    else:
        v0 = v0 >> 1
    flag[i] = v0
```

这是类似 XTEA 反馈移位 + 异或的扩散结构。

**IDA Python 递归函数图分析**

```python
import idc
import idaapi

start = 0x717F
funcs = {}
def recur(addr):
    if addr == 0x241A: return
    ea = addr
    value_dic = {}
    while True:
        ins = idc.generate_disasm_line(ea, 0)
        if ins.startswith("mov"):
            op0 = idc.print_operand(ea, 0)
            op1 = idc.print_operand(ea, 1)
            value_dic[op0] = op1
        if ins == "call _rand" and len(value_dic) >= 10:
            break
        ins_len = idc.create_insn(ea)
        ea += ins_len
    # xor 计算下一函数
    xor_ins = idc.print_operand(ea+0x36, 1)[:-1]
    xor = int(xor_ins, 16)
    nexts = []
    for i in ["60","58","50","48","40","38","30","28","20","18"]:
        nxt = ((int(value_dic[f"[rbp+var_{i}]"][:-1], 16) ^ xor) + addr) & 0xFFFFFFFFFFFFFFFF
        nexts.append(nxt)
    funcs[addr] = nexts
    for nxt in nexts:
        if nxt not in funcs:
            recur(nxt)
```

适合处理混淆代码"调用 rand 决定下一函数"的迷宫结构。
