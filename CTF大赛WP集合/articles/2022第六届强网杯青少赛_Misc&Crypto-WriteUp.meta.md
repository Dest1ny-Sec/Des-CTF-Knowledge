---
title: 2022 第六届强网杯青少赛 Misc & Crypto WriteUp
contest: 强网杯青少赛 2022
year: 2022
difficulty: easy
vuln_type: crypto_oracle
tags: [base64, 奇偶分离, 异或32, 大小写偏移, NGC660安全实验室, 入门]
attack_chain:
  - 读 chuyinweilai.png 文件 Base64 decode
  - 字节奇偶分离交换 + zfill(2) 重组 PNG
  - XOR 32 还原 FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]
  - 大写字母 -31 / 小写字母 -32 解密
  - 大写字母 -32 解密反向偏移
key_payload: 'cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"; res = chr(ord(i)^32)'
one_liner: 入门：Base64 + 字节奇偶互换 + XOR 32 + 大小写 -31/-32 偏移。
lesson: PNG 字节奇偶互换 + zfill(2) 重组是常见 stego 套路；大小写偏移 -31/-32 区分大小写。
quality: medium
---

# 2022 第六届强网杯青少赛 Misc & Crypto WriteUp

## 来源
- 原文：ctfiot.com/71039.html
- 团队：NGC660 安全实验室

## 题目详解

### 1. chuyinweilai.png（Base64 + 奇偶分离）
- 原 PNG 文件内容被 Base64 编码存储
- 解码后字节流做**奇偶分离交换**（高位 / 低位互换）
- 重组 PNG

```python
import base64, binascii
f = open('chuyinweilai.png','r')
content = base64.b64decode(f.read())
r = ""
for i in range(0, len(content), 2):
    r += str(hex(content[i+1]))[2:].zfill(2)  # 偶位
    r += str(hex(content[i]))[2:].zfill(2)    # 奇位
content = binascii.unhexlify(r)
with open('new.png','wb') as f:
    f.write(content)
```

### 2. FLAG[] XOR 32
```python
cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"
res = ""
for i in cryher:
    res += chr(ord(i) ^ 32)
```
- 大小写切换：A ↔ a, [...] 保持不变

### 3. 大小写 -31 / -32 偏移
```python
content = "VXPSdQceLWWOcLSOcOLWPUVLQfVVfRPOPbSS"
res = "flag{"
for i in content:
    if i.isupper():
        res += chr(ord(i) - 31)  # 大写 -31
    else:
        res += chr(ord(i) - 32)  # 小写 -32
res += "}"
print(res.lower())
```
- ROT 类移位密码的变种，区分大小写分别偏移

## 关键技巧
- **PNG 字节奇偶互换**：常见 stego 套路，配合 zfill(2) 防止前导 0 丢失
- **XOR 32**：第 6 位翻转，大小写互换
- **大小写偏移**：ROT 类的细化版本

## 适用场景
- Misc 入门
- Crypto 基础编码
- 青少年赛训练
