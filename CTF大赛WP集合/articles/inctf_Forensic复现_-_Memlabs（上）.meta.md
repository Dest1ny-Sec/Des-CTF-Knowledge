---
title: inctf Forensic 复现 | Memlabs（上）
contest: inctf
year: 2019
difficulty: medium
vuln_type: forensic_memory
tags: [memory-forensics, volatility, hashdump, chrome-history, steghide, xor, base64]
attack_chain:
  - Lab1: volatility -f Lab1.raw --profile=Win7SP1x64 hashdump
  - NTLM hash crack (Administrator 31d6... = 空密码)
  - Lab2: chromehistory + desktop 文件
  - vip.txt 用 XOR 3 + base64 编码
  - 'am1gd2V4M20wXGs3b2U=' base64 + XOR 3 = "image of key"
  - steghide 隐写提取
key_payload: NTLM hashdump + chromehistory + steghide
one_liner: inctf Memlabs Lab 1-3 复现，volatility + NTLM 爆破 + steghide 综合。
lesson: 经典内存取证三件套：hashdump / chromehistory / filescan。
quality: high
---

inctf Memlabs Lab 1-3 复现（来源 ctfiot，作者 SanDieg0）。

**Lab1: NTLM Hashdump**
```bash
volatility.exe -f Lab1.raw --profile=Win7SP1x64 hashdump
# Administrator: 31d6cfe0d16ae931b73c59d7e0c089c0::: (空密码)
# SmartNet: 4943abb39473a6f32c11301f4987e7e0
# Alissa Simpson: f4ff64c8baac57d22f22edc681055ba6
```

**Lab2: Chrome History + Desktop 文件**
```bash
python2 vol.py --plugins=./volatility/plugins/ -f Lab2.raw --profile=Win7SP1x64 chromehistory
# 找到下载的 vip.txt
```

**vip.txt 解密**：
```python
import sys
def xor(s): return ''.join(chr(ord(i)^3) for i in s)
def encoder(x): return x.encode("base64")
f = open("C:\\Users\\hello\\Desktop\\vip.txt", "w")
f.write(encoder(xor(sys.argv[1])))
s = 'am1gd2V4M20wXGs3b2U='
d = s.decode('base64')
print ''.join(chr(ord(i)^3) for i in d)  # "image of key"
```

**Lab3: steghide 隐写**
```bash
steghide extract -sf image.png -p "image of key"
```

**核心工具链**：
1. `volatility --profile=Win7SP1x64 hashdump` - 提 NTLM
2. `volatility chromehistory` - 提 Chrome 浏览器历史
3. `volatility filescan | grep` - 提桌面文件
4. `steghide` - 隐写图提取
5. `XOR + base64` 编码还原

整篇适合作为"内存取证入门"教学案例。
