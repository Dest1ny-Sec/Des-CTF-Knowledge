---
title: 2023 工业信息安全技能大赛鹏城锦标赛 WriteUp
contest: 2023 工业信息安全技能大赛鹏城锦标赛
year: 2023
difficulty: hard
vuln_type: forensic_disk
tags: [IEC_60870-5_104, CAN_15765, ICMP流量, SMC_TEA变种, AES_ECB, PEM手撕, Wiener攻击, factorDB, RsaCtfTool]
attack_chain:
  - 工控-Welcome: IEC 60870-5 流量追踪异常 base64 解密 flag{sign_in_successfully!}
  - 解 Hex0 + Base64 + 键盘密码
  - CAN 包 ISO 15765 解析 ID=730，拼接导出二进制
  - strings 找假 flag，反编译 pyc 反写 decode
  - 源码逆向，每条 ICMP data 长度转 ASCII（192.168.3.73 源）
  - 去除花指令 + SMC TEA 变种 (delta=0x11451419, 移位改了)
  - idapython 还原 sub_2DB7 AES+hex 加密
  - AES-ECB (key=rGzuwTc31NRH9tsT) 解密 flag
  - RSA: 手撕 PEM 拿 N，factorDB 分解找 p,q
  - RsaCtfTool issue #304 找 e，Wiener 攻击兜底
key_payload: 'key = rGzuwTc31NRH9tsT, n = 460657813884289609896372056585544172485318117026246263899744329237492701820627219556007788200590119136173895989001382151536006853823326382892363143604314518686388786002989248800814861248595075326277099645338694977097459168530898776007293695728101976069423971696524237755227187061418202849911479124793990722597'
one_liner: 工业信息安全综合：IEC104 + CAN + ICMP 隐写 + SMC TEA 变种 + AES + 手撕 PEM RSA。
lesson: PEM corrupt 时手撕结构体；SMC TEA 变种要看 delta 和移位；Wiener 攻击是大 e RSA 兜底。
quality: high
---

# 2023 工业信息安全技能大赛鹏城锦标赛 WriteUp

## 来源
- 原文：ctfiot.com/139444.html

## 7+ 道题详解

### 1. 工控-Welcome（IEC 60870-5 流量）
- 流追踪 IEC 60780-5 流量
- 异常部分 base64 解密
- flag: `flag{sign_in_successfully!}`

### 2. RSA（PEM 手撕）
- 解出来是 RSA PEM 公钥，Corrupt
- Crypto.PublicKey 解不出来
- 手撕 PEM 结构
- factorDB 分解 N
- RsaCtfTool issue #304 找 e
- Wiener 攻击兜底

### 3. CAN 流量（ISO 15765）
```python
# ISO 15765-2 PCI Type
# ID 730 数据，tp[0]='2' 连续帧拼接
```
- 取出 ID=730 数据
- 拼接导出二进制
- strings 找假 flag
- 反编译 pyc 反写 decode

### 4. ICMP 流量（data 长度隐写）
```python
cap = pyshark.FileCapture('easyping.pcap', display_filter="ip.src==192.168.3.73")
flag = []
for packet in cap:
    flag.append(len(bytes.fromhex(packet.icmp.data)))
flag = base64.b64decode(bytes(flag))
```
- 每条 ICMP data 长度转 ASCII
- 192.168.3.73 源报文
- base64 解码

### 5. SMC TEA 变种
- delta = 0x11451419
- 移位改了（`<<3` 替代 `<<4`，`>>6` 替代 `>>5`）
- idapython 还原 sub_2DB7 函数
- 32 轮解密

### 6. AES-ECB
```python
key = b'rGzuwTc31NRH9tsT'
aes = AES.new(key, AES.MODE_ECB)
print(aes.decrypt(bytes.fromhex(dst)))
# b'flag{hsOrB3IMqfoMUg0E}'
```

### 7. 键盘密码
- Base32 → XOR 37 → XOR 73 解密
- 还原键盘码

## 关键技巧
- **PEM 手撕**：Corrupt 时手撕 ASN.1 结构
- **factorDB + Wiener**：大 e RSA 兜底
- **ISO 15765 CAN 解析**：PCI 类型分帧
- **ICMP 长度隐写**：data 长度转 ASCII
- **SMC TEA 变种**：delta + 移位都改
- **AES-ECB**：key 直接读取

## 适用场景
- 工业控制协议（IEC104 / CAN / Modbus）
- 流量长度隐写
- SMC 自修改代码逆向
- 手撕 PEM 公钥
- Wiener 攻击
