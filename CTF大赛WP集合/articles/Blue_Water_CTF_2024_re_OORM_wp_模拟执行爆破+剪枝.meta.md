---
title: Blue Water CTF 2024 re OORM wp 模拟执行爆破+剪枝
contest: Blue Water CTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [800 funcs, keyAs keyBs, 400 funcs_A + 400 funcs_B, 模拟执行 Unicorn, 20-bit 输入爆破, 剪枝, dfsA(20, key), x = input_bit | (key<<1), y = hashA(x), keyAs[20] = y, 看雪 wx_御史神风]
attack_chain:
  - main: 800 funcs (400 funcs_A + 400 funcs_B), do while times <= 799
  - funcs_A_i: x = input_bit | (key << 1), y = hashA(x), keyAs[20] = y
  - keyAs[0] 已知, keyBs[0] 已知
  - funcs_A_399: y == 21961 || y == 27098 → ++dwCheck
  - 模拟执行: Unicorn Uc(UC_ARCH_X86, UC_MODE_64)
  - 段映射: 0x6000 段 mem_map + mem_write
  - rva_to_offset 解析 ELF 段
  - dfsA(i, j, key) DFS 20-bit, j=19 末位剪枝
  - 剪枝: sim2(uc, i, j, key, 0/1) 结果 == 32766 接受
  - 关键: uc bug → j==3 重新创建 Uc
  - 输出: 20-bit 路径 + final key
key_payload: '800 funcs 链 / x = input_bit | (key<<1) / 模拟执行 Unicorn / dfsA(20, j) 剪枝 / uc bug j==3 重建 / final key 校验'
one_liner: Blue Water CTF 2024 re OORM — 800 个 funcs 链 20-bit 输入 + 模拟执行 Unicorn + DFS 剪枝爆破 (32766 阈值) + 末位 funcs_A_399 校验 (21961/27098)。
lesson: 模拟执行 + 剪枝是 OORM (Obscure Obfuscated Reversing Machine) 标准解法;Unicorn 跨函数模拟需重建 Uc 实例;rva_to_offset + 段映射是 ELF 操作基础。
quality: high
---

# Blue Water CTF 2024 re OORM wp 模拟执行爆破+剪枝

## 速读
Blue Water CTF 2024 reverse — OORM (Obscure Obfuscated Reversing Machine) 800 funcs 链。

## main 循环
```c
times = 0;
do {
    for (i = 0; i != 400; ++i) {
        keyA = keyAs_2135E0[i];
        if (runA) {
            ++times;
            funcs_A_211CA0[i](keyA, input_in_bits_A_214EE0[i]);
            keyAs_2135E0[i] = 0LL;
        }
        keyB = keyBs_212960[i];
        if (keyB) {
            ++times;
            funcs_B_211020[i](keyB, input_in_bits_B_214260[i]);
            keyBs_212960[i] = 0LL;
        }
    }
} while (times <= 799);
```

## funcs 模板
```c
void funcs_A_0(__int64 key, __int64 input_bit) {
    x = input_bit | (key << 1);
    y = hashA0(x);
    keyAs[20] = y;
}

void funcs_A_399(__int64 key, __int64 input_bit) {
    x = input_bit | (key << 1);
    y = hashA399(x);
    if (y == 21961 || y == 27098) ++dwCheck_212940;
}
```

## 模拟执行
```python
from capstone import *
from unicorn import *
from unicorn.x86_const import *
from elftools.elf.elffile import ELFFile

uc = Uc(UC_ARCH_X86, UC_MODE_64)

# 段映射
for segment in elff.iter_segments():
    if segment['p_vaddr'] == 0x6000:
        uc.mem_map(segment['p_vaddr'], segment['p_memsz']//0x1000*0x1000 + 0x1000)
        uc.mem_write(segment['p_vaddr'], segment.data())
```

## DFS 剪枝
```python
def dfsA(i, j, key) -> bool:
    global path, uc
    if j == 3:  # Unicorn bug 重建
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        # ... 重新映射
    
    if j == 19:  # 末位剪枝
        new_key, t0, t1 = sim2(uc, i, j, key, 0)
        if new_key == t0 or new_key == t1:
            print('path', path + [0], new_key)
        new_key, t0, t1 = sim2(uc, i, j, key, 1)
        if new_key == t0 or new_key == t1:
            print('path', path + [1], new_key)
    else:
        new_key, _, _ = sim2(uc, i, j, key, 0)
        path.append(0)
        dfsA(i, j + 1, new_key)
        path.pop()
        new_key, _, _ = sim2(uc, i, j, key, 1)
        path.append(1)
        dfsA(i, j + 1, new_key)
        path.pop()
```
