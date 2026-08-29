---
title: CTF 逆向：基础 VM 的三大解法剖析
contest: CTF Reverse
year: 2024
difficulty: medium
vuln_type: reverse
tags: [VM字节码, opcode 0x01/0x04/0x05 add/sub/xor, target+value 操作数, IDA get_wide_byte 提取, z3 BitVec 8位约束, Frida hook onEnter 计数, encode/decode 对称, flag_enc 32字节密文]
attack_chain:
  - VM 字节码: opcode 0x01 加 / 0x04 减 / 0x05 异或
  - 操作数: (target, value) - flag[target] += value / -= value / ^= value
  - 解法 1: IDA Python idc.get_wide_byte(start+i) 提取 0x7A31D0 起 16*25 字节
  - 解法 2: deopcode 倒序遍历 (3字节一组) 还原 flag
  - 解法 3: z3 BitVec 8位 + solver 约束每字节 == flag_enc
  - 解法 4: Frida hook vm.exe + 0x197F onEnter 计数, send(number) 到 Python
  - flag_enc = [0x65, 0xE2, ..., 0xFD] 32 字节
key_payload: 'VM opcode 0x01/0x04/0x05 / (target, value) 操作 / IDA get_wide_byte / z3 BitVec 8位 / deopcode 倒序 / Frida Interceptor.attach onEnter'
one_liner: CTF VM 基础 — VM 字节码 0x01/0x04/0x05 (add/sub/xor) + IDA get_wide_byte 提取 + z3 BitVec 8 位约束 + deopcode 倒序遍历 + Frida hook onEnter 计数。
lesson: VM 逆向 3 大解法:① IDA 提取 opcode + 解释执行 / ② 倒序遍历反推 (因为加减异或操作可逆) / ③ z3 符号执行约束求解;VM 字节码通常 3 字节一组 (op, target, value)。
quality: high
---

# CTF 逆向：基础 VM 的三大解法剖析

## 速读
CTF 基础 VM 逆向 3 大解法 — IDA 提取 / 倒序反推 / z3 符号执行。

## VM 核心
```python
while i < len(opcode):
    if opcode[i] == 0x00:
        i += 1
    elif opcode[i] == 0x01:
        i += 2
    elif opcode[i] == 0x02:
        i += 3
```

## opcode 类型
| opcode | 含义 |
|--------|------|
| 0x01 | add (target, value) |
| 0x04 | sub (target, value) |
| 0x05 | xor (target, value) |

## 解法 1: IDA 提取
```python
import idaapi, idc
start_address = 0x7A31D0
data_length = 16 * 25
with open("dumpopcode.txt", "a") as f:
    for i in range(0, data_length):
        f.write(hex(idc.get_wide_byte(start_address + i)))
        f.write("\n")
```

## 解法 2: 倒序反推
```python
def deopcode(value, opcode, number):
    for i in range(len(opcode)-3, -1, -3):
        if opcode[i] == number:
            if opcode[i+1] == 1: value -= opcode[i+2]  # 减
            elif opcode[i+1] == 2: value += opcode[i+2]  # 加
            elif opcode[i+1] == 3: value ^= opcode[i+2]  # 异或
    return value & 0xff
```

## 解法 3: z3
```python
import z3
flag = [z3.BitVec(f'flag[{i}]', 8) for i in range(flag_size)]
encoded_flag = encode(flag, opcode)
for j in range(len(flag_enc)):
    solver.add(encoded_flag[j] == flag_enc[j])
```

## 解法 4: Frida hook
```javascript
var base = Module.findBaseAddress("vm.exe");
Interceptor.attach(base.add(0x197F), {
    onEnter: function(args) {
        number += 1;
    }
});
Interceptor.attach(base.add(0x19A2), {
    onEnter: function(args) {
        send(number);
    }
});
```

## flag_enc
```python
flag_enc = [0x65, 0xE2, 0x57, 0x60, 0xCE, 0x1E, 0xE1, 0x5C, 0x4B, 0x4B, ...]  # 32 字节
```
