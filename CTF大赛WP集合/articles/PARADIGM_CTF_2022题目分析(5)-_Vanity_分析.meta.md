---
title: PARADIGM CTF 2022 题目分析 (5) - Vanity (ECDSA 签名 + 16 字节 0x00)
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Solidity, isValidSignatureNow, ECDSA 签名, bestScore 0x00 字节计数, vanity 地址]
attack_chain: |
  1. 题目: challenge.bestScore() >= 16 拿 flag
  2. 三个 solve 函数:
     - solve() 无参: 读 msg.sender, 调内部 solve(msg.sender)
     - solve(address signer, bytes sig) 有参: 校验 isValidSignatureNow(hash, signer, sig) 返回 true 后调 solve(signer)
     - 内部 solve(address target): address 转 bytes20 遍历每个字节, 字节 == 0 时 score++, 每次 score > bestscore 时更新 bestscore
  3. 关键: 16 字节全 0x00 → bestscore >= 16
  4. vanity address: 生成 ECDSA 私钥 d → address = d * secp256k1 generator 末 20 字节
  5. ECDSA 签名 (r, s): sign(hash, d) → r, s
  6. 调 solve(signer_address, signature) 触发内部 solve
key_payload: |
  # 内部 solve:
  function _solve(address target) internal {
      bytes20 addr = bytes20(target);
      uint256 score;
      for (uint256 i = 0; i < 20; i++) {
          if (addr[i] == 0) score++;
      }
      if (score > bestScore) bestScore = score;
  }
  
  # 攻击:
  # 1. 找 16 字节全 0 的 vanity address (ECDSA 私钥爆破)
  # 2. 用私钥签 solve 选择子的 hash
  # 3. 调 solve(vanity_address, signature) → bestscore = 16
  # 4. challenge.bestScore() 返回 16 >= 16
one_liner: PARADIGM CTF 2022 Vanity: ECDSA 签名 vanity address (16 字节 0x00) + isValidSignatureNow 验证。
lesson: |
  - vanity address 是私钥的末 20 字节
  - 16 字节全 0x00 → 爆破 1/(2^16) = 1/65536 概率
  - ECDSA 签名 = sign(hash, d) → (r, s) 用私钥 d 签 hash
  - isValidSignatureNow(hash, signer, sig) 是 ecrecover 验证
  - Solidity bytes20 转换支持 address 类型
  - score 累加 → bestScore 持续更新
quality: high
---

# PARADIGM CTF 2022 题目分析 (5) - Vanity

> 来源: ctfiot.com 80219 - NUMEN Cyber Labs

## 题目分析

```solidity
function solve() external {
    _solve(msg.sender);
}

function solve(address signer, bytes memory sig) external {
    require(isValidSignatureNow(hash, signer, sig));
    _solve(signer);
}

function _solve(address target) internal {
    bytes20 addr = bytes20(target);
    uint256 score;
    for (uint256 i = 0; i < 20; i++) {
        if (addr[i] == 0) score++;
    }
    if (score > bestScore) bestScore = score;
}
```

**关键**：
- `isValidSignatureNow(hash, signer, sig)` ECDSA 签名验证
- `_solve(signer)` 把 address 转 bytes20 遍历
- 字节为 0 时 score++，score > bestScore 时更新
- 题目要求 `bestScore() >= 16`

## 攻击：Vanity Address 爆破

```python
import hashlib
from ecdsa import SigningKey, SECP256k1

# 1. 找 16 字节 0x00 的 vanity address
while True:
    d = SigningKey.generate(curve=SECP256k1).to_string()
    pub = SigningKey.from_string(d, curve=SECP256k1).get_verifying_key()
    addr = "0x" + pub.to_string()[-40:]  # 末 20 字节
    # 计算 address 16 进制字符串, 检查前 16 字节是否 0
    addr_bytes = bytes.fromhex(addr[2:])
    zero_bytes = sum(1 for b in addr_bytes if b == 0)
    if zero_bytes >= 16:
        print(f"Found: d={d.hex()}, addr={addr}")
        break

# 2. ECDSA 签名 solve hash
hash = hashlib.sha256(b"challenge.solve()").digest()
sig = SigningKey.from_string(d, curve=SECP256k1).sign_digest(hash)

# 3. 调用 solve(vanity_address, sig)
challenge.solve(vanity_address, sig)

# 4. challenge.bestScore() = 16 >= 16
```

## 评价

PARADIGM CTF 2022 Vanity ECDSA 签名 + vanity address 爆破：
- **vanity address** = 私钥末 20 字节
- **16 字节 0x00** 概率 1/65536
- **ECDSA 签名** (r, s) 用私钥签 hash
- **isValidSignatureNow** 是 OpenZeppelin ECDSA 库
- 内部 solve 把 address 转 bytes20 逐字节比对

适用读者：Solidity 合约 / ECDSA 密码学 / vanity 工具
