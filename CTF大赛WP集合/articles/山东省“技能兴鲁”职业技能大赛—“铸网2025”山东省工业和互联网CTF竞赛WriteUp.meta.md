---
title: 山东省技能兴鲁职业技能大赛—铸网 2025 工业和互联网 CTF WriteUp
contest: 技能兴鲁
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [ICS, force-control-PCZ, modbus-TCP-flow, CAN-bus-speed, OTA-AES-CBC, PKCS7-padding, UUID-validation, Industrial-CTF]
attack_chain:
  - ICS 失窃的工艺: test.PCZ 改后缀 .zip 解压 → 搜 flag 文本
  - ICS 工控协议分析: Wireshark 追踪 TCP 流 → flag 逐字符藏在流量中
  - Misc 总线流量分析: CAN ID 0x0000280 1 字节速度 (0x50≈80km/h)
  - 速度列表: [0x46, 0x48, 0x50, 0x50, 0x55, 0x58, 0x52, 0x5A, 0x58, 0x58, ...] (30 个)
  - 36 秒间隔，距离 = sum(v * 36 / 3600) * 1000 = 24470 米
  - Misc OTA 流量分析: device 发起 /api/v1/vehicle/handshake → server 返回 session_key (hex)
  - 后续用 session_key AES-CBC 解密固件包 (PKCS7 padding 校验)
  - k1 段: 三次 AES-CBC 解密 + PKCS7 校验 → 找到正确 k1
  - k0 段: 一次 AES-CBC + UUID 格式校验 → flag UUID
key_payload: 'PCZ→.zip 解压 + CAN 0x0000280 速度 36s 间隔 24470m + session_key AES-CBC PKCS7 UUID'
one_liner: 山东省铸网 2025 工控 4 题：PCZ 解压找 flag + TCP 流拼字符 + CAN 速度积分算距离 + OTA AES-CBC UUID 爆破。
lesson: 工控 OT/IT 融合题考察 OT 协议 (modbus/TCP/CAN) + 流量分析 + 加密协议 (AES-CBC) 综合能力。
quality: high
---

# 山东省"技能兴鲁"职业技能大赛—"铸网 2025"山东省工业和互联网 CTF 竞赛 WriteUp

**来源**: ctfiot.com ID 269821

## ICS

### 1. 失窃的工艺
- 文件 `test.PCZ`（力控软件工程文件）
- 无力控软件 → 改后缀 `.zip` 直接解压
- 搜索 `flag` 文本
- flag: `flag{D076-4D7E-92AC-A05ACB788292}`

### 2. 工控协议分析
- Wireshark 打开 pcap
- 追踪 TCP 流
- flag 逐字符藏在流量中
- 拼凑: `flag{c93650241853da240f9760531a79cbcf}`

## Misc

### 1. 总线流量分析（CAN 速度积分）
- 汽车测试报文，时间间隔 36s
- 找 1 字节变化的速度报文
- 找到 ID = 0x0000280 的报文，速度在 0x50 左右浮动（≈ 80 km/h）

```python
speeds_hex = ["46","48","50","50","55","58","52","5A","58","58",
              "56","54","55","4F","4F","4F","4D","4D","4D","4E",
              "4E","53","56","56","59","59","51","52","4F","46"]

speeds = [int(h, 16) for h in speeds_hex]
delta_t = 36

distance_km = 0
for v in speeds:
    distance_km += v * delta_t / 3600
distance_m = distance_km * 1000
print(distance_km, distance_m)
# 24.469999999999995 24469.999999999996
# flag{24470}
```

### 2. OTA 流量分析
- 车机/IOT 设备 OTA 流程
- 设备 → `/api/v1/vehicle/handshake` 带设备信息
- Server → `session_key` (hex)
- 后续用 `session_key` AES-CBC 解密固件包

#### 攻击
```python
import re, base64
from Crypto.Cipher import AES

# 1. 提取 session_key (hex)
def find_session_keys(text):
    keys = set()
    for m in re.finditer(r'"session_key"\s*:\s*"([0-9a-fA-F]{32,128})"', text):
        keys.add(m.group(1))
    return keys

# 2. 提取长 base64 段
def find_long_base64(text, min_len=80):
    found = set()
    for m in re.finditer(r'([A-Za-z0-9+/]{%d,}={0,2})' % min_len, text):
        found.add(m.group(1))
    return list(found)

# 3. AES-CBC 解密 + PKCS7 校验
# 爆 k1: 三次 AES-CBC 解密 + 补位校验
# 爆 k0: 一次 AES-CBC + UUID 格式校验
```

#### 优化
- k1 搜索空间大 → 多进程/批量加速
- PKCS7 校验 + UUID 校验作为快速剪枝
- 找到匹配 k0 → flag

## 评价
山东省铸网 2025 工控 4 题：
- ICS 失窃工艺（PCZ 改名解压）
- ICS TCP 流量分析
- Misc CAN 速度积分（数学+工控协议）
- Misc OTA AES-CBC UUID 爆破

考察工控 OT/IT 融合能力。
