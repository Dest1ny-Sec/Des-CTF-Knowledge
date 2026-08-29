---
title: 嘉新杯部分wp
contest: 恒安嘉新杯 / EasyAES + 失窃的工艺
year: 2025
difficulty: medium
vuln_type: crypto_oracle
tags: [EasyAES, 4层CBC, 双重爆破, SHA-256 key派生, OTA流量分析, 晨星安全团队, Zion_Cat]
attack_chain:
  - 题1 EasyAES: 4 层 AES-CBC 加密
  - c3 (密文 hex 192 字节) → 3 次 unpad + decrypt 得 c0
  - part2 (3 字符 ascii_letters+digits) SHA-256 派生 key1
  - 解 c3 → c2 → c1 → c0 (需要 valid_padding 检查)
  - part1 (3 字符) SHA-256 派生 key0, 解 c0 → flag (36 字符 + 4 横线)
  - flag 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  - 题2 失窃的工艺: OTA 流量分析
  - hello 消息找到 session_key + vehicle_type + 密文
  - session_key: b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90
  - ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg==
key_payload: '4 层 AES-CBC + part1+part2 SHA-256 派生 key + flag UUID 格式'
one_liner: 嘉新杯 2 题：EasyAES 4 层 CBC 双重爆破 + 失窃的工艺 OTA 流量分析 session_key 解密。
lesson: 多层 AES-CBC 加密需要 valid_padding 检查 + unpad 逐层验证; SHA-256 短 key 派生可爆破 (3 字符 62^3 = 238k); OTA 流量 first message 通常含 session_key。
quality: medium
---

# 嘉新杯部分wp

## 概览
- **来源**: ctfiot 271379
- **赛事**: 恒安嘉新杯
- **作者**: 晨星安全团队 Zion_Cat
- **难度**: ⭐⭐⭐

## 题1: EasyAES (4 层 CBC)

### 加密结构
```
c3 = AES-CBC(key1).encrypt(c2)
c2 = AES-CBC(key1).encrypt(c1)
c1 = AES-CBC(key1).encrypt(c0)
c0 = AES-CBC(key0).encrypt(flag)
```

### 爆破脚本
```python
from Crypto.Cipher import AES
from hashlib import sha256
import string, itertools

def valid_padding(s):
    n = s[-1]
    return 1 <= n <= 32 and len(s) >= n and all(s[-i] == n for i in range(1, n+1))

def unpad(s):
    return s[:-s[-1]]

def decrypt_with_key(enc, key):
    iv = enc[:16]
    return AES.new(key, AES.MODE_CBC, iv).decrypt(enc[16:])

# part2 爆破 (62^3 = 238k)
for part2 in itertools.product(string.ascii_letters + string.digits, repeat=3):
    key1 = sha256(''.join(part2).encode()).digest()
    dec3 = decrypt_with_key(c3, key1)
    if not valid_padding(dec3): continue
    c2 = unpad(dec3)
    # ... 同理解 c2 → c1 → c0
    candidates.append((part2, c0))

# part1 爆破 key0
for part2, c0 in candidates:
    for part1 in itertools.product(string.ascii_letters + string.digits, repeat=3):
        key0 = sha256(''.join(part1).encode()).digest()
        dec0 = decrypt_with_key(c0, key0)
        if not valid_padding(dec0): continue
        flag = unpad(dec0).decode('utf-8')
        if len(flag) == 36 and flag.count('-') == 4:
            # UUID 格式
            print(f"Flag: {flag}")
```

## 题2: 失窃的工艺 (OTA 流量)

### 流量提取
- `hello` 消息包含 session_key + 密文
```json
{
  "message": "handshake ok",
  "ok": true,
  "session_key": "b908232bfa70d5c3060dd2f96b36a7fc8199e18ef1b3c509efe4a86bf9339d90",
  "vehicle_type": "normal"
}
密文: "ALTaXk84WULvUwvHHoKpDlmW8PKnKIhyCZVl3kiI4Kca1NgiZDbUt6O6H1OAsZvUX7FyZsgjRJLolAEBnp0Lpg=="
```

## 教学
- 多层 AES-CBC 爆破: 每层 valid_padding + unpad 检查
- 短字符串 (3 字符) SHA-256 派生 key 可暴力 (238k)
- flag UUID 格式: 8-4-4-4-12 共 36 字符
- OTA 协议: hello 消息含 session_key 用于后续加密
