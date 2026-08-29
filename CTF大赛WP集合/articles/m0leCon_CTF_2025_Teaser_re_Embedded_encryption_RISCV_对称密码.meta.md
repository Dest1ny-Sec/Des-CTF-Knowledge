---
title: m0leCon CTF 2025 Teaser re Embedded encryption RISCV 对称密码
contest: m0leCon
year: 2025
difficulty: hard
vuln_type: reverse
tags: [risc-v, mcu, metal-gpio, ip-permutation, p-box, row-column-sum, gpio-input-pin, custom-block-cipher]
attack_chain:
  - 识别 RISC-V 32 位固件
  - metal_gpio_get_input_pin 读 1 位随机种子
  - srand+rand 用内置库
  - var644[1604] 分四区: m32[32]/input[33]/m256[256]/output[256*4]
  - IP 置换表 (32 字节)
  - P 盒映射 (256 字节)
  - 重复 1337 轮
  - output[input[j]] = 1 << (31-j)
  - 行列和反推 input
  - 解密
key_payload: 1 位种子 + IP/P 盒 + 行列和反推
one_liner: m0leCon 2025 Teaser 嵌入式逆向，RISC-V 自定义分组密码 + 行列和反推 output。
lesson: 当 output 矩阵每行/列只有 1 位为 1 时，行列和反推是经典线性代数问题。
quality: high
---

m0leCon CTF 2025 Teaser re Embedded encryption RISCV 完整复盘（来源 ctfiot）。

**架构识别**
- RISC-V 32 位固件
- `metal_gpio_get_input_pin` 从针脚读 1 位值作为 seed
- `srand` + `rand` 用内置库（不同实现）

**关键数据结构**
```c
unsigned char var644[1604];
// 逻辑上分四区：
// _BYTE m32[32];       // &var644[0:32]   IP 置换表
// _BYTE input[33];     // &var644[32:64]  明文
// _BYTE m256[256];     // &var644[68:324] P 盒
// _DWORD output[256];  // &var644[580:1604] 密文
```

**加密流程**
1. **1337 轮** 自定义分组密码（标准对称密码结构）
2. **第二轮**：j: 0 → 31，将最后一轮结果映射到 output
3. **output 视为 16×16 矩阵**，输出每行/列和

**关键等价**：`output[input[j]] = 1 << (31 - j)`

**解密**（从行列和反推）
```python
def get_bit_idx(x):
    i, res = 0, []
    while x:
        if x & 1: res.append(i)
        i += 1; x >>= 1
    return res

rows, cols = [0]*32, [0]*32
for r in range(16):
    for a in get_bit_idx(row_sums[r]): rows[a] = r
for c in range(16):
    for a in get_bit_idx(col_sums[c]): cols[a] = c

output = [0]*256
for i in range(32):
    output[rows[i]*16 + cols[i]] |= 1 << i

# 然后由 output 还原最后一轮的 input
inputs = [0]*32
for i in range(256):
    for j in get_bit_idx(output[i]):
        inputs[31-j] = i
```

**关键洞察**：
- `output` 矩阵中不同两个元素不会在相同位同时为 1
- 行和为 `0x101` → 至少存在 0x100、0x1 或 0x101 三种组合
- 行列和位分解 → 反推元素位置

**嵌入式逆向技巧**：
- 硬件相关 API（metal_gpio_*）看名字猜功能
- IDA F5 美化后看等价的 C 代码
- 复杂结构体先看初始化推测语义

整篇适合作为"嵌入式固件逆向 + 自定义密码学"教学案例。
