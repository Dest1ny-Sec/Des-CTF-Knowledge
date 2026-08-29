---
title: 从一道实例题目解析AI在CTF中的解题过程
contest: AI辅助CTF实例
year: 2025
difficulty: easy
vuln_type: crypto_oracle
tags: [变异凯撒, Base64, AI解题, caesar_decode, 偏移量反推]
attack_chain:
  - 加密流程: 变异凯撒 + Base64
  - 变异凯撒规则: 偏移量 = 位置序号 + 3 (位置从 0 开始)
  - cipher_text = aVRZM0x6QTJNVGt3Y0dGa1pTMXpOVEF3WldKa1pUQmliR2h2Y21sbmFXNWhiQzV1WkdWdWRHbG1hV05s
  - Step 1: base64.b64decode 得到中间密文
  - Step 2: caesar_decode(char, offset=i+3) 解密
  - AI 提示: { } 不参与偏移 + 偏移量修正为 i+2
  - 反推 flag{xxx} 全部小写
key_payload: 'aVRZM0x6QTJNVGt3Y0dGa1pTMXpOVEF3WldKa1pUQmliR2h2Y21sbmFXNWhiQzV1WkdWdWRHbG1hV05s'
one_liner: AI 解变异凯撒+Base64 混合加密，反推偏移量 +2 修正 + { } 不参与偏移。
lesson: AI 解密 CTF 题可以快速验证偏移量 + 字符集，但偏移量偏差需要根据 flag 格式 (全小写) 反推修正；caesar_decode 函数必须处理 { } 等非字母字符。
quality: low
---

# 从一道实例题目解析AI在CTF中的解题过程

## 概览
- **来源**: ctfiot 270682
- **类型**: 简单 Crypto + AI 辅助

## 加密规则
- 明文: `flag{xxx}` 仅大小写字母 + 数字 + 下划线
- Step 1: 变异凯撒加密
  - 偏移量 = 位置序号 + 3
  - 第 0 位偏移 3，第 1 位偏移 4，依次类推
- Step 2: Base64 编码

## 密文
```
aVRZM0x6QTJNVGt3Y0dGa1pTMXpOVEF3WldKa1pUQmliR2h2Y21sbmFXNWhiQzV1WkdWdWRHbG1hV05s
```

## 解密 (AI 生成)
```python
import base64

def caesar_decode(cipher, start_offset=3):
    plain = ""
    for i, char in enumerate(cipher):
        offset = i + start_offset
        if char.islower():
            decoded_ascii = (ord(char) - offset - 97) % 26 + 97
            plain += chr(decoded_ascii)
        elif char.isupper():
            decoded_ascii = (ord(char) - offset - 65) % 26 + 65
            plain += chr(decoded_ascii)
        elif char.isdigit():
            decoded_ascii = (ord(char) - offset - 48) % 10 + 48
            plain += chr(decoded_ascii)
        elif char == '_':
            plain += char
        else:
            plain += char
    return plain

cipher_text = "aVRZM0x6QTJNVGt3Y0dGa1pTMXpOVEF3WldKa1pUQmliR2h2Y21sbmFXNWhiQzV1WkdWdWRHbG1hV05s"
base64_decoded = base64.b64decode(cipher_text).decode('utf-8')
print(f"Base64 解密后: {base64_decoded}")
middle_cipher = "iTZ3LzA2MTKwcGFkZTNnzTAwWZKZTBibGhvcmxnaHVuZGVudGlm"
final_plain = caesar_decode(middle_cipher, start_offset=2)  # AI 修正偏移量
print(f"最终明文: {final_plain}")
```

## AI 修正
- 提示: "flag 通常为小写，可检查偏移量是否存在 ±1 误差"
- AI 反推: "偏移量 = 位置序号 + 2 更符合结果"
- { 和 } 不参与偏移
- LaG → lag 大小写问题
