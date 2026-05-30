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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1722648385.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1722648385.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1722648386.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1722648387.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1722648388.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722648389.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1722648390.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1722648391.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1722648392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1722648392.png)