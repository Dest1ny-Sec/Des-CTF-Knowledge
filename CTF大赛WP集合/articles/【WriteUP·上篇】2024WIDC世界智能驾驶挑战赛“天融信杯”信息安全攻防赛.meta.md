---
title: 【WriteUP·上篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛
contest: WIDC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [车联网-ransomware, Sepolia-Etherscan, calldata-extract, XOR-decrypt-3-9, RSA-public-key-PEM, encrypted-seed]
attack_chain: 1. 从 Sepolia Etherscan 提取 calldata 拿到加密字符串/2. Python decrypt: (ord(c) + 3) ^ 9 处理前 67 字符/3. Base64 解码得 PEM 公钥/4. 私钥 (n, d) 加密 seed 发给服务端过 27 服务
key_payload: decrypt = (ord(c) + 3) ^ 9  RSA 私钥 627585038806247 / 119987789848673  base64 flag
one_liner: 2024 WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛上篇，OEM 勒索病毒恢复数据 + Sepolia Etherscan 提取 calldata + XOR 解密。
lesson: Sepolia 是 Ethereum 测试网；calldata 是 EVM 合约调用数据；(ord+3)^9 是经典 XOR 加偏移解密；RSA 短密钥 (n 短到能 627585038806247) 暗示 RSA-CRT 攻击。
quality: high
---

# 【WriteUP·上篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛

## 概览
2024 WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛上篇，OEM 勒索病毒恢复 + 区块链数据提取。

## 题目背景
"某车辆 OEM 制造厂商遭受勒索病毒攻击，重要数据被加密，请帮助厂商恢复重要数据"

## 攻击链

### Stage 1: Sepolia Etherscan 提取 calldata
- 访问 https://sepolia.etherscan.io/address/0xa9bf5b94b191bd39407376dc3af147c367b0ad9d
- 从初始地址提取每笔交易的 calldata

### Stage 2: XOR 解密
```python
import sys

def decrypt_and_print_flag(encrypted_string):
    decrypted_flag = ""
    for c in encrypted_string[:67]:  # 只处理前67个字符
        decrypted_char = (ord(c) + 3) ^ 9
        decrypted_flag += chr(decrypted_char)
    print(decrypted_flag)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <encrypted_string>")
        sys.exit(1)
    encrypted_string = sys.argv[1]
    decrypt_and_print_flag(encrypted_string)
```

### Stage 3: Base64 → PEM
- 转 ASCII 字符串：`LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0...`
- Base64 解码：
  ```
  -----BEGIN PUBLIC KEY-----
  MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHAjrJB03s5wIDAQAB
  -----END PUBLIC KEY-----
  ```

### Stage 4: RSA 加密 seed
- 私钥 (n, d) = (627585038806247, 119987789848673)
- 加密 seed：`5a6d4e764d47786a613368686133427564484a6f5a7a426a4e3259354e474a68597a4d35595463344e7a46714e57526f4e6a466a4e46565551323957646e704f64586447636d5a5251576b33624756545957356e636e6b3d`
- 转 ASCII：`ZmNvMGxja3hha3BudHJoZzBjN2Y5NGJhYzM5YTc4NzFqNWRoNjFjNFVUQ29WdnpOdXdGcmZRQWk3bGVTYW5ncnk=`
- Base64 解码：`fco0lckxakpntrhg0c7f94bac39a7871j5dh61c4UTCoVvzNuwFrfQAi7leSangry`

## 经验提炼
- Sepolia 是 Ethereum 测试网，Etherscan 查 calldata
- calldata 是 EVM 合约调用数据
- (ord+3)^9 是经典 XOR 加偏移解密
- RSA 短密钥 (n 短到能 627585038806247) 暗示 RSA-CRT 攻击
- Base64 → PEM 公钥 → 配合 n 找 p q
- OEM 勒索病毒场景考察真实事件还原
- 短 n RSA 可直接质因数分解
- calldata 第一笔通常是合约构造或初始化
- XOR 9 加偏移 3 简单密码可爆破
- WIDC 是世界智能驾驶挑战赛，车联网场景
