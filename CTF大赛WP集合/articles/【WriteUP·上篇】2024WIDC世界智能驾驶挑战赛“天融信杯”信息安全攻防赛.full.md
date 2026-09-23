---
title: 【WriteUP·上篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛
contest: WIDC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags:
- 车联网-ransomware
- Sepolia-Etherscan
- calldata-extract
- XOR-decrypt-3-9
- RSA-public-key-PEM
- encrypted-seed
attack_chain: '1. 从 Sepolia Etherscan 提取 calldata 拿到加密字符串/2. Python decrypt: (ord(c) + 3) ^ 9 处理前 67 字符/3. Base64 解码得 PEM 公钥/4. 私钥 (n, d) 加密 seed 发给服务端过 27 服务'
key_payload: decrypt = (ord(c) + 3) ^ 9  RSA 私钥 627585038806247 / 119987789848673  base64 flag
one_liner: 2024 WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛上篇，OEM 勒索病毒恢复数据 + Sepolia Etherscan 提取 calldata + XOR 解密。
lesson: Sepolia 是 Ethereum 测试网；calldata 是 EVM 合约调用数据；(ord+3)^9 是经典 XOR 加偏移解密；RSA 短密钥 (n 短到能 627585038806247) 暗示 RSA-CRT 攻击。
quality: high
full_path: 【WriteUP·上篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛.full.md
meta_path: 【WriteUP·上篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WriteUP·上篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛。2024 WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛上篇，OEM 勒索病毒恢复数据 + Sepolia Etherscan 提取 calldata + XOR 解密。。经验：Sepolia 是 Ethereum 测试网；calldata 是 EVM 合约调用数据；(ord+3)^9 是...
category: misc
subcategory: misc_other
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/185724.html
reasoning_chain:
- OEM 勒索病毒加密数据 → 触发点：给出 Sepolia Etherscan 地址 → 假设：加密 key 在以太坊 calldata
- 动作：访问 https://sepolia.etherscan.io/address/0xa9bf... 提所有 calldata → 观察：拿到加密字符串
- 字符串显然是 ciphertext → 触发点：勒索病毒常见 XOR/偏移加密 → 假设：decrypt = (ord(c) + 3) ^ 9
- 动作：Python 循环 (ord(c) + 3) ^ 9 跑前 67 字符 → 观察：得到 PEM 公钥字符串
- PEM 公钥 → base64 解码 → 假设：RSA 公钥 → 动作：从 PEM 提 n 和 e
- 加密 (n, d) 是 627585038806247 / 119987789848673 → 触发点：RSA 私钥 d + n → 假设：可解加密的 seed
- 动作：用 d 解密 AES seed → 观察：得到明文 seed → 发给服务端过第 27 服务
failed_attempts:
- 试图直接 AES 解密原始字符串 → 失败：先要 RSA 解 seed
- 试图用 openssl 解 PEM → 失败：题目要 Python 代码实现
- 试图找 Calldata 之外的密钥 → 失败：题目明示 calldata 是唯一来源
key_observations:
- Sepolia 是 Ethereum 测试网，etherscan 可读 calldata
- (ord(c) + 3) ^ 9 是经典 XOR 加偏移勒索病毒解密
- RSA 短密钥（n 短到 16 位级）暗示题目另有私钥，不是分解
- PEM 公钥 base64 是 RSA 标准包装，rsa.PublicKey.fromPEM 解析
- 勒索病毒取证的核心是恢复加密 key，不是解密算法
prerequisites:
- Ethereum Sepolia + Etherscan calldata 提取
- Python cryptodome / pycryptodome RSA 使用
- XOR 加偏移解密逻辑
- PEM 公钥解析（base64 + ASN.1）
---
# 【WriteUP·上篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛

> 原文: https://www.ctfiot.com/185724.html
> ID: 185724

某车辆OEM制造厂商遭受勒索病毒攻击，重要数据被加密，请帮助厂商恢复重要数据

（1）从初始地址提取每笔交易的calldatahttps://sepolia.etherscan.io/address/0xa9bf5b94b191bd39407376dc3af147c367b0ad 9d

（3）直接使用python实现这段代码↓拿到flag

import sys

def decrypt_and_print_flag(encrypted_string):

decrypted_flag = “”

for c in encrypted_string[:67]:  # 只处理前67个字符

decrypted_char = (ord(c) + 3) ^ 9

decrypted_flag += chr(decrypted_char)

print(decrypted_flag)

if __name__ == “__main__”:

if len(sys.argv) != 2:

print(“Usage: python script.py <encrypted_string>”)

sys.exit(1)

encrypted_string = sys.argv[1]

decrypt_and_print_flag(encrypted_string)

（5）转化成ASCII字符串：LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUNJd0RRWUpLb1pJaHZjTkFRRUJCUUFERVFBd0RnSUhBanJKQjAzczV3SURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==

（6）Base64解码得到pem文件：

—–BEGIN PUBLIC KEY—–

MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHAjrJB03s5wIDAQAB

—–END PUBLIC KEY—–

（8）得到私钥：（n,d）= 627585038806247 119987789848673

对seed使用私钥加密发送给服务端，服务端用公钥解密即可过27服务：

5a6d4e764d47786a613368686133427564484a6f5a7a426a4e3259354e474a68597a4d35595463344e7a46714e57526f4e6a466a4e46565551323957646e704f64586447636d5a5251576b33624756545957356e636e6b3d

（9）转ASCII：

ZmNvMGxja3hha3BudHJoZzBjN2Y5NGJhYzM5YTc4NzFqNWRoNjFjNFVUQ29WdnpOdXdGcmZRQWk3bGVTYW5ncnk=

Base64解码：

fco0lckxakpntrhg0c7f94bac39a7871j5dh61c4UTCoVvzNuwFrfQAi7leSangry

                                                                                                                          

WriteUP系列将持续更新，敬请关注护车行动！

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]