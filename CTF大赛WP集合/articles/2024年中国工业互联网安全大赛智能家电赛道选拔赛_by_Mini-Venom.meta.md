---
title: 2024 年中国工业互联网安全大赛智能家电赛道选拔赛 by Mini-Venom
contest: 智能家电赛道
year: 2024
difficulty: medium
vuln_type: [crypto_rsa, web_unknown, rce, web_rce]
tags: [RSA rsa 库 256bit 小模数, p, q, d 已知 → 反向, XOR 12 + ASCII+1 反向, cmd 命令 base64 写入 flag.txt, modbus.reference_num 边界]
attack_chain: RSA 256bit 已知 n, e, c + p, q, d → rsa.decrypt → xor(12) → subtract_one_from_ascii → cmd 命令 → base64 -d > flag.txt
key_payload: rsa.PrivateKey(n, e, d, p, q) ; rsa.decrypt(c, privkey) → xor(12) → byte - 1 → cmd="cd /var/www/html;echo ZmxhZ3szOTA4NEVFRjJEMjhFOTQxRjUzRTRBMUFBMUZBNjc2Nn0K|base64 -d > ./flag.txt;..."; modbus.reference_num >= 212
one_liner: 256bit RSA 已知 p,q,d 还原 cmd 命令 + modbus 边界。
lesson: rsa 库默认 256bit 太小直接分解；private_key 已知时直接 decrypt。
quality: low
---
# 2024 年中国工业互联网安全大赛智能家电赛道选拔赛 by Mini-Venom

> 原文主体是招新广告，正文只有一段 RSA 还原脚本。

## RSA 还原 cmd 命令

```python
import rsa

def rsa_decode(c, pubkey):
    privkey = rsa.PrivateKey(pubkey.n, pubkey.e, pubkey.d, pubkey.p, pubkey.q)
    return rsa.decrypt(c, privkey)

def subtract_one_from_ascii(data):
    return bytes(b - 1 for b in data)

def xor_bytes(data, key):
    return bytes(b ^ key for b in data)

# 256-bit RSA 参数全公开
n = 71484438965393396388835335667806052411397994375702758854090697767967524655627
e = 65537
ciphertext = bytes.fromhex('515b50d7407f4f321ddea14d0d99e4134c285ee6b7b92b77f3ed65f32212a529')
pubkey = rsa.PublicKey(n, e)
p = 895534711824738922785094048763390663
q = 79823191688166851259736970548355545692829
d = 19619308233067290551077729872542647104506154812668367156272584280826183049209
privkey = rsa.PrivateKey(n, e, d, p, q)

# 解密 → XOR 12 → 减 1 还原 ASCII
decoded = rsa.decrypt(ciphertext, privkey)
decoded = xor_bytes(decoded, 12)
original = subtract_one_from_ascii(decoded)
print(original.decode())
```

还原命令：
```bash
cd "/var/www/html"; echo ZmxhZ3szOTA4NEVFRjJEMjhFOTQxRjUzRTRBMUFBMUZBNjc2Nn0K | base64 -d > ./flag.txt
```

`flag{39084EEF2D28E941F53E4A1AF1AF6A766}`

## 其他题目

- modbus.reference_num >= 212（212 是写入长度边界）
- zip 压缩包
- 5010 ... 49a6 ...（hex 流）
