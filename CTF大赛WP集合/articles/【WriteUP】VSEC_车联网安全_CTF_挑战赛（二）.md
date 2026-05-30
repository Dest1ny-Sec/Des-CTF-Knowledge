# 【WriteUP】VSEC 车联网安全 CTF 挑战赛（二）

> 原文: https://www.ctfiot.com/194326.html
> ID: 194326

第一季赛事结束后，Block Harbor 通过其平台VSEC公开了50个独特的汽车挑战，并提供了5000美元的奖金，激发了更广泛的参与和社区建设。

第二季赛事预计将在2024年8月24日至9月8日举行，奖金池增至10万美元（From Garage to Glory: The Rise of a $100K Automotive Capture the Flag Challenge – Block Harbor）

继第一部分WriteUP发出后，收到很多师傅关注，也有很多师傅动手做了起来

欢迎大家与我们交流，继续第二弹

再次感谢yichen投稿，yichen yyds

题目描述：Please download https://github.com/zombieCraig/ICSim and read the instructions to compile/run. Once setup, set the seed value -s 10000 for both the ./controls and ./icsim. Next Answer the following questions. Use any tool you would like in order to arrive at the answers.What is the arbitration id for door unlocks?NOTE: Submit in the format 0xARBID翻译：请下载 https://github.com/zombieCraig/ICSim 并阅读编译/运行说明。设置完成后，为 ./controls 和 ./icsim 设置种子值 -s 10000。下一步回答以下问题。使用任何您想要的工具来获得答案。门解锁的仲裁 ID 是什么？注意：以 0xARBID 格式提交

# 导入所需的库from collections import defaultdictimport reimport sys
def count_can_ids(log_file_path): # 创建一个字典来存储CAN ID及其出现次数 can_id_count = defaultdict(int)
 # 尝试打开并读取candump日志文件 try: with open(log_file_path, 'r') as file: for line in file: # 使用正则表达式提取CAN ID match = re.search(r'(d+.d+)s+vcan0s+(w+)#', line) if match: # 将匹配到的CAN ID添加到字典中，并增加其计数 can_id = match.group(1) can_id_count[can_id] += 1 except FileNotFoundError: print(f"Error: The file '{log_file_path}' does not exist.") sys.exit(1) except Exception as e: print(f"An error occurred: {e}") sys.exit(1)
 # 打印统计结果 for can_id, count in sorted(can_id_count.items()): print(f"CAN ID {can_id} appears {count} times.")
# 从命令行参数获取日志文件路径if len(sys.argv) != 2: print("Usage: python script.py <path_to_candump_log_file>") sys.exit(1)
log_file_path = sys.argv[1]count_can_ids(log_file_path)

题目描述：Please download https://github.com/zombieCraig/ICSim and read the instructions to compile/run. Once setup, set the seed value -s 10000 for both the ./controls and ./icsim. Next Answer the following questions. Use any tool you would like in order to arrive at the answers.What is the abritration id for the speedometor display?翻译：请下载 https://github.com/zombieCraig/ICSim 并阅读编译/运行说明。设置完成后，为 ./controls 和 ./icsim 设置种子值 -s 10000。下一步回答以下问题。使用任何您想要的工具来获得答案。速度计显示屏的 ID 是什么？

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.Retrieve the VIN of the simulation using UDS.翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。使用 UDS 检索模拟的 VIN。

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.It seems the simulation broadcasts some diagnostic information on arbitration ID 0x7DF when booting up, what does this message say? (in ASCII)HINT: How can you get an ECU to restart?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。似乎模拟在启动时广播了一些有关仲裁 ID 0x7DF 的诊断信息，这条消息说了什么？（ASCII 格式）提示：如何让 ECU 重新启动？

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.The simulation's engine light is on, can you read the diagnostic code?Check out our youtube walkthrough if you get stuck: https://www.youtube.com/watch?v=IaUL0dA4Z_YThe format of the DTC is Pxxxx-xx. Example answer: P1234-01翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。模拟的发动机灯亮了，你能读出诊断代码吗？如果你遇到困难，请查看我们的 YouTube 演示：https://www.youtube.com/watch?v=IaUL0dA4Z_YDTC 的格式为 Pxxxx-xx。示例答案：P1234-01

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.It seems the simulation allows access to only some off-chip sections of memory, are there any secrets in the visible memory?The memory region starts at 0xC3F80000 and the flag is in the format flag{...}.翻译：这项挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。似乎模拟只允许访问一些片外内存部分，可见内存中有什么秘密吗？内存区域从 0xC3F80000 开始，标志的格式为 flag{...}。

import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])recvdata = "[DATA]:"for hex_value in range(0xC3F83000, 0xc3f87000, 0xFF): byte1 = (hex_value >> 24) & 0xFF byte2 = (hex_value >> 16) & 0xFF byte3 = (hex_value >> 8) & 0xFF byte4 = hex_value & 0xFF candata=[0x07, 0x23, 0x14, byte1, byte2, byte3, byte4, 0xFF] message = can.Message(arbitration_id=0x7DF, is_extended_id=False, dlc=8, data=[0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() message = can.Message(arbitration_id=0x7DF, is_extended_id=False, dlc=8, data=candata) bus.send(message, timeout=0.2) msg = bus.recv() recvdata += binascii.hexlify(msg.data).decode('utf-8')[6:] message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) temp = 0 while temp < 36: msg = bus.recv() tempdata = binascii.hexlify(msg.data).decode('utf-8')[2:] if tempdata != "00000000000000": recvdata += tempdata temp = temp + 1print("n========== READMEM ==========")print(recvdata)print("========== READMEM ==========n")
bus.shutdown()

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.The simulation is implementing service 0x27 Security Access Level 3 using MAAATH. Can you find the key and break in?The flag is the key to unlock with seed 1337 in hex (example a5a5)Unlock Hint for 0 pointsflag is the two bytes of key you send (example: 55aa)翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。模拟正在使用 MAAATH 实现服务 0x27 安全访问级别 3。你能找到钥匙并闯入吗？标志是使用十六进制种子 1337 解锁的钥匙（例如 a5a5）解锁提示 0 分标志是您发送的两个字节的密钥（例如：55aa）

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.Level 3 provides access to a new diagnostic session and some new memory at 0x1A000, but we still don't have full control of the module. Can you provide a valid key for security access level 1?The flag is the key to unlock with seed 7D0E1A5C in hex (example 12345678)翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。级别 3 提供对新诊断会话和 0x1A000 处的一些新内存的访问，但我们仍然无法完全控制该模块。您能为安全访问级别 1 提供有效的密钥吗？该标志是使用十六进制种子 7D0E1A5C（例如 12345678）解锁的密钥


```
题目描述：Please download https://github.com/zombieCraig/ICSim and read the instructions to compile/run. Once setup, set the seed value -s 10000 for both the ./controls and ./icsim. Next Answer the following questions. Use any tool you would like in order to arrive at the answers.What is the arbitration id for door unlocks?NOTE: Submit in the format 0xARBID翻译：请下载 https://github.com/zombieCraig/ICSim 并阅读编译/运行说明。设置完成后，为 ./controls 和 ./icsim 设置种子值 -s 10000。下一步回答以下问题。使用任何您想要的工具来获得答案。门解锁的仲裁 ID 是什么？注意：以 0xARBID 格式提交
```



```
/icsim vcan0 -s 10000
./controls vcan0 -s 10000
```



```
# 导入所需的库from collections import defaultdictimport reimport sys
def count_can_ids(log_file_path): # 创建一个字典来存储CAN ID及其出现次数 can_id_count = defaultdict(int)
 # 尝试打开并读取candump日志文件 try: with open(log_file_path, 'r') as file: for line in file: # 使用正则表达式提取CAN ID match = re.search(r'(d+.d+)s+vcan0s+(w+)#', line) if match: # 将匹配到的CAN ID添加到字典中，并增加其计数 can_id = match.group(1) can_id_count[can_id] += 1 except FileNotFoundError: print(f"Error: The file '{log_file_path}' does not exist.") sys.exit(1) except Exception as e: print(f"An error occurred: {e}") sys.exit(1)
 # 打印统计结果 for can_id, count in sorted(can_id_count.items()): print(f"CAN ID {can_id} appears {count} times.")
# 从命令行参数获取日志文件路径if len(sys.argv) != 2: print("Usage: python script.py <path_to_candump_log_file>") sys.exit(1)
log_file_path = sys.argv[1]count_can_ids(log_file_path)
```



```
题目描述：Please download https://github.com/zombieCraig/ICSim and read the instructions to compile/run. Once setup, set the seed value -s 10000 for both the ./controls and ./icsim. Next Answer the following questions. Use any tool you would like in order to arrive at the answers.What is the abritration id for the speedometor display?翻译：请下载 https://github.com/zombieCraig/ICSim 并阅读编译/运行说明。设置完成后，为 ./controls 和 ./icsim 设置种子值 -s 10000。下一步回答以下问题。使用任何您想要的工具来获得答案。速度计显示屏的 ID 是什么？
```



```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.Retrieve the VIN of the simulation using UDS.翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。使用 UDS 检索模拟的 VIN。
```



```
cansend vcan0 7df#0322f190
cansend vcan0 7E0#3000000000000000
```



```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.It seems the simulation broadcasts some diagnostic information on arbitration ID 0x7DF when booting up, what does this message say? (in ASCII)HINT: How can you get an ECU to restart?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。似乎模拟在启动时广播了一些有关仲裁 ID 0x7DF 的诊断信息，这条消息说了什么？（ASCII 格式）提示：如何让 ECU 重新启动？
```



```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.The simulation's engine light is on, can you read the diagnostic code?Check out our youtube walkthrough if you get stuck: https://www.youtube.com/watch?v=IaUL0dA4Z_YThe format of the DTC is Pxxxx-xx. Example answer: P1234-01翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。模拟的发动机灯亮了，你能读出诊断代码吗？如果你遇到困难，请查看我们的 YouTube 演示：https://www.youtube.com/watch?v=IaUL0dA4Z_YDTC 的格式为 Pxxxx-xx。示例答案：P1234-01
```



```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.It seems the simulation allows access to only some off-chip sections of memory, are there any secrets in the visible memory?The memory region starts at 0xC3F80000 and the flag is in the format flag{...}.翻译：这项挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。似乎模拟只允许访问一些片外内存部分，可见内存中有什么秘密吗？内存区域从 0xC3F80000 开始，标志的格式为 flag{...}。
```



```
import canimport timeimport binascii
bus = can.Bus(interface='socketcan', channel='vcan0')bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])recvdata = "[DATA]:"for hex_value in range(0xC3F83000, 0xc3f87000, 0xFF): byte1 = (hex_value >> 24) & 0xFF byte2 = (hex_value >> 16) & 0xFF byte3 = (hex_value >> 8) & 0xFF byte4 = hex_value & 0xFF candata=[0x07, 0x23, 0x14, byte1, byte2, byte3, byte4, 0xFF] message = can.Message(arbitration_id=0x7DF, is_extended_id=False, dlc=8, data=[0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) msg = bus.recv() message = can.Message(arbitration_id=0x7DF, is_extended_id=False, dlc=8, data=candata) bus.send(message, timeout=0.2) msg = bus.recv() recvdata += binascii.hexlify(msg.data).decode('utf-8')[6:] message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) bus.send(message, timeout=0.2) temp = 0 while temp < 36: msg = bus.recv() tempdata = binascii.hexlify(msg.data).decode('utf-8')[2:] if tempdata != "00000000000000": recvdata += tempdata temp = temp + 1print("n========== READMEM ==========")print(recvdata)print("========== READMEM ==========n")
bus.shutdown()
```



```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.The simulation is implementing service 0x27 Security Access Level 3 using MAAATH. Can you find the key and break in?The flag is the key to unlock with seed 1337 in hex (example a5a5)Unlock Hint for 0 pointsflag is the two bytes of key you send (example: 55aa)翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。模拟正在使用 MAAATH 实现服务 0x27 安全访问级别 3。你能找到钥匙并闯入吗？标志是使用十六进制种子 1337 解锁的钥匙（例如 a5a5）解锁提示 0 分标志是您发送的两个字节的密钥（例如：55aa）
```



```
0x1337 = 0001001100110111
按位取反
 1110110011001000
最终得到 ecc8 也就是 flag
```



```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.Level 3 provides access to a new diagnostic session and some new memory at 0x1A000, but we still don't have full control of the module. Can you provide a valid key for security access level 1?The flag is the key to unlock with seed 7D0E1A5C in hex (example 12345678)翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器内进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。级别 3 提供对新诊断会话和 0x1A000 处的一些新内存的访问，但我们仍然无法完全控制该模块。您能为安全访问级别 1 提供有效的密钥吗？该标志是使用十六进制种子 7D0E1A5C（例如 12345678）解锁的密钥
```



```
9102870c c43b2d1b
d64217a8 837bbdbf
241adbeb 712371fc
9bb26411 ce8bce06
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721349006.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721349006.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721349006.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721349007.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1721349008.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721349008.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721349009.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1721349009.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1721349009.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1721349009.png)