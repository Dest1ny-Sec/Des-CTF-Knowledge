---
title: Automotive CTF 2024 World Final Writeup
contest: Automotive CTF
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [SWD协议, SWCLK/SWDIO, DEMCR 0xe000ed00, RDBUFF, CPU ID 0x410fd212, CTRL/STAT 0xf0000040, 0xe0042000, CAN总线 778帧, I2C 0x63 0x00 0x00 0x01, bh{INFAMOUS_REMAKE}, ARM CoreSight]
attack_chain:
  - SWD 协议: SWCLK(1) SWDIO(2) 抓包
  - 0.594900000 起始时间戳
  - 写入 AP4: W AP4 OK
  - 读 APc: 0xe000ed00 (DEMCR 调试异常监控控制寄存器)
  - 读 RDBUFF: 0x410fd212 (CPU ID = ARM Cortex-M3)
  - 读 CTRL/STAT: 0xf0000040
  - 写 AP4 0xe0042000 读 ROM 表
  - 写 APc 0x00000000 + 状态机
  - Python rev(s) 4 字节反序: s[6:]+s[4:6]+s[2:4]+s[:2]
  - I2C: SCL=PB10, SDA=PB11, 0x63 0x00 0x00 0x01 命令
  - CAN0 778 帧: 62 68 7B 49 4E 46 41 4D 4F 55 53 5F 52 45 4D 41 4B 45 7D = "bh{INFAMOUS_REMAKE}"
key_payload: 'SWD 0xe000ed00 DEMCR / RDBUFF 0x410fd212 CPU ID / 0xf0000040 CTRL/STAT / 0xe0042000 ROM 表 / I2C 0x63 0x00 0x00 0x01 / CAN 778 帧 bh{INFAMOUS_REMAKE}'
one_liner: Automotive CTF 2024 World Final — SWD 协议抓包 (DEMCR 0xe000ed00 + RDBUFF 0x410fd212 CPU ID) + I2C 0x63 0x00 0x00 0x01 + CAN 778 帧解 bh{INFAMOUS_REMAKE}。
lesson: SWD 协议是 ARM 调试标准,3-wire (SWDIO/SWCLK/SWO) + 状态机 (W AP4/R APc/RDBUFF);I2C 起始 + 地址 0x63 + 控制 0x00 0x00 0x01;CAN ID 778 是 vehicle bus 经典帧。
quality: high
---

# Automotive CTF 2024 World Final Writeup

## 速读
Automotive CTF 2024 World Final — 车联网逆向综合题。

## SWD 协议抓包
```
Time;CH 1 SWCLK;CH 2 SWDIO
0.594900000;1;0
0.594906000;1;1
0.594910000;0;1
```

## SWD 状态机解析
```
W AP4 → OK → 0xe000ed00 (DEMCR)
R APc → OK → 0x00000000
RDBUFF → OK → 0x410fd212 (CPU ID)
R CTRL/STAT → OK → 0xf0000040
W AP4 → OK → 0xe0042000
R APc → OK → 0x00000000
```

## Python 解析
```python
def rev(s):
    return s[6:] + s[4:6] + s[2:4] + s[:2]

# 状态机
state = 0
addr = ""
buf = []
for line in fp.readlines():
    line = line[:-1]
    if line.endswith("SWD: : W AP4"):
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
```

## I2C
```
SCL -> PB10 -> 14
SDA -> PB11 -> 15
I2C> [0x63 0x00 0x00 0x01]
```

## CAN 总线
```
(1729536865.698447) can0 778 [8] 62 68 7B 49 4E 46 41 4D 'bh{INFAM'
(1729536865.700350) can0 778 [8] 4F 55 53 5F 52 45 4D 41 'OUS_REMA'
(1729536865.708109) can0 778 [3] 4B 45 7D 'KE}'
```

## Flag
`bh{INFAMOUS_REMAKE}`
