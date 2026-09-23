---
title: Automotive CTF 2024 World Final Writeup
contest: Automotive CTF
year: 2024
difficulty: hard
vuln_type: forensic_traffic
tags:
- SWD协议
- SWCLK/SWDIO
- DEMCR 0xe000ed00
- RDBUFF
- CPU ID 0x410fd212
- CTRL/STAT 0xf0000040
- '0xe0042000'
- CAN总线 778帧
- I2C 0x63 0x00 0x00 0x01
- bh{INFAMOUS_REMAKE}
- ARM CoreSight
attack_chain:
- 'SWD 协议: SWCLK(1) SWDIO(2) 抓包'
- 0.594900000 起始时间戳
- '写入 AP4: W AP4 OK'
- '读 APc: 0xe000ed00 (DEMCR 调试异常监控控制寄存器)'
- '读 RDBUFF: 0x410fd212 (CPU ID = ARM Cortex-M3)'
- '读 CTRL/STAT: 0xf0000040'
- 写 AP4 0xe0042000 读 ROM 表
- 写 APc 0x00000000 + 状态机
- 'Python rev(s) 4 字节反序: s[6:]+s[4:6]+s[2:4]+s[:2]'
- 'I2C: SCL=PB10, SDA=PB11, 0x63 0x00 0x00 0x01 命令'
- 'CAN0 778 帧: 62 68 7B 49 4E 46 41 4D 4F 55 53 5F 52 45 4D 41 4B 45 7D = "bh{INFAMOUS_REMAKE}'
key_payload: '''SWD 0xe000ed00 DEMCR / RDBUFF 0x410fd212 CPU ID / 0xf0000040 CTRL/STAT / 0xe0042000 ROM 表 / I2C 0x63 0x00 0x00 0x01 / CAN 778 帧 bh{INFAMOUS_REMAKE}'''
one_liner: Automotive CTF 2024 World Final — SWD 协议抓包 (DEMCR 0xe000ed00 + RDBUFF 0x410fd212 CPU ID) + I2C 0x63 0x00 0x00 0x01 + CAN 778 帧解 bh{INFAMOUS_REMAKE}。
lesson: SWD 协议是 ARM 调试标准,3-wire (SWDIO/SWCLK/SWO) + 状态机 (W AP4/R APc/RDBUFF);I2C 起始 + 地址 0x63 + 控制 0x00 0x00 0x01;CAN ID 778 是 vehicle bus 经典帧。
quality: high
full_path: Automotive_CTF_2024_World_Final_Writeup.full.md
meta_path: Automotive_CTF_2024_World_Final_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Automotive CTF 2024 World Final Writeup。Automotive CTF 2024 World Final — SWD 协议抓包 (DEMCR 0xe000ed00 + RDBUFF 0x410fd212 CPU ID) + I2C 0x63 0x00 0x00 0x01 + CAN 778 帧解 bh{INFAMOUS_REMAKE}。。关键路径：SWD...
category: misc
subcategory: misc_other
tools_used:
- ARM
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/210738.html
reasoning_chain:
- '[触发点] 拿到 SWD 抓包数据 → 假设：ARM 调试协议 3-wire / [动作] 看起始 0.594900000 时间戳 + SWCLK/SWDIO 两通道 / [观察] 写入 AP4: W AP4 OK + 读 APc 0xe000ed00 (DEMCR) / [下一步] 看 RDBUFF'
- '[触发点] 读 RDBUFF 0x410fd212 → 假设：CPU ID = ARM Cortex-M3 / [动作] 读 CTRL/STAT 0xf0000040 + 写 AP4 0xe0042000 读 ROM 表 + 写 APc 0x00000000 + 状态机 / [观察] 完成 SWD 状态机初始化 / [下一步] 看 I2C 协议'
- '[触发点] I2C: SCL=PB10, SDA=PB11, 0x63 0x00 0x00 0x01 命令 → 假设：I2C 启动 + 地址 0x63 + 控制字节 / [动作] 用 Python rev(s) 4 字节反序: s[6:]+s[4:6]+s[2:4]+s[:2] / [观察] 拿到数据 / [下一步] 看 CAN 总线'
- '[触发点] CAN0 778 帧: 62 68 7B 49 4E 46 41 4D 4F 55 53 5F 52 45 4D 41 4B 45 7D → 假设：这是 ASCII 字符拼成 flag / [动作] hex to ASCII 转换 / [观察] 拿到 bh{INFAMOUS_REMAKE} / [下一步]'
failed_attempts:
- 试图从 SWD 直接读 flag → 失败：flag 在 CAN 帧
- 试图不解码 I2C → 失败：I2C 数据有端序问题
key_observations:
- SWD 协议是 ARM 调试标准，3-wire (SWDIO/SWCLK/SWO) + 状态机 (W AP4/R APc/RDBUFF)
- I2C 起始 + 地址 0x63 + 控制 0x00 0x00 0x01
- CAN ID 778 是 vehicle bus 经典帧
- 0x410fd212 = ARM Cortex-M3 CPU ID
prerequisites:
- ARM CoreSight 调试架构
- SWD 协议状态机
- I2C 总线协议
- CAN 总线协议
---
# Automotive CTF 2024 World Final Writeup

> 原文: https://www.ctfiot.com/210738.html
> ID: 210738


```
0x000007e0 05 31 01 40 44 ff 00 00
Time;CH 1 SWCLK;CH 2 SWDIO
0.000000000;1;1
0.594872000;0;1
0.594878000;1;1
0.594884000;0;1
0.594890000;1;1
0.594894000;0;0
0.594900000;1;0
…
1-15 SWD: : W AP4
18-22 SWD: : OK
28-90 SWD: : 0xe000ed00
94-108 SWD: : R APc
111-115 SWD: : OK
117-179 SWD: : 0x00000000
187-201 SWD: : RDBUFF
204-208 SWD: : OK
210-272 SWD: : 0x410fd212
280-294 SWD: : R CTRL/STAT
297-301 SWD: : OK
303-365 SWD: : 0xf0000040
372-386 SWD: : W AP4
389-393 SWD: : OK
399-461 SWD: : 0xe0042000
465-479 SWD: : R APc
482-486 SWD: : OK
488-550 SWD: : 0x00000000
…
res = {}

def rev(s):
 return s[6:] + s[4:6] + s[2:4] + s[:2]

with open("annon.txt") as fp:
 state = 0
 addr = ""
 buf = []
 for _line in fp.readlines():
 line = _line[:-1]
 if line.endswith("SWD: : W AP4"):
 assert state == 0
 state = 1
 elif state == 1 and line.endswith(" SWD: : OK"):
 state = 2
 elif state == 2:
 addr = line.split(':')[2]
 buf = []
 state = 3
 elif state == 3:
 if line.endswith("SWD: : RDBUFF"):
 res[addr] = buf
 state = 0
 elif "SWD: : 0x" in line:
 buf.append(rev(line.split(":")[2][3:]))

for addr,bufs in res.items():
 print(addr, bufs)
SCL -> PB10 ->14
SDA -> PB11 -> 15
I2C> [0x63 0x00 0x00 0x01]
(1729536865.698447) can0 778 [8] 62 68 7B 49 4E 46 41 4D 'bh{INFAM'
 (1729536865.700350) can0 778 [8] 4F 55 53 5F 52 45 4D 41 'OUS_REMA'
 (1729536865.708109) can0 778 [3] 4B 45 7D 'KE}'
```
