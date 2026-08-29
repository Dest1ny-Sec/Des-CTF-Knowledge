---
title: PARADIGM CTF 2022 题目分析 (3) - Lockbox2 (5 stage calls + ECDSA)
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Solidity, 5 stage calls, ECDSA 私钥爆破, secp256k1 特殊公钥, log_bytes 事件]
attack_chain: |
  1. 题目: lockbox2.solve() → 调 stage1-5 (msg.data[4:]) → 5 个 call 全部 success → locked = false
  2. solve 内部:
     - bool successes[5]
     - for i in 0..4: successes[i] = address(this).call(abi.encodeWithSignature("stage1", msg.data[4:]))
     - if all true: locked = false
  3. 关键: 5 个 stage 函数返回什么才能让 call success?
  4. 推测: stage1-5 校验某种加密签名, 需要恢复 secp256k1 私钥
  5. ECDSA 私钥爆破 (00 开头公钥):
     - secp256k1 曲线 256-bit 私钥
     - 公钥 x,y 拼成 64 hex 字节, 开头是 0x00 的概率 1/256
     - 循环 256 次找公钥开头 00 的私钥
  6. emit log_bytes(: 0x890d6908) 事件触发 log
key_payload: |
  # ECDSA 私钥爆破 (开头 00 公钥):
  import random
  from Crypto.Util.number import isPrime
  from ecdsa import ecdsa
  g = ecdsa.generator_secp256k1
  while True:
      private_key = random.randint(0, 1 << 256 - 1)
      public_key = private_key * g
      x = str(hex(public_key.x())[2:]).zfill(64)
      y = str(hex(public_key.y())[2:]).zfill(64)
      public_key_hex = x + y
      if public_key_hex[:2] == "00":
          print(private_key, public_key_hex)
          break
  
  # Lockbox2 solve 关键:
  bool successes[5];
  for (uint i = 0; i < 5; i++) {
      successes[i] = address(this).call(
          abi.encodeWithSignature("stage"+(i+1), msg.data[4:])
      );
  }
  if (all true) locked = false;
one_liner: PARADIGM CTF 2022 Lockbox2: 5 stage 函数全部 call 成功 + secp256k1 ECDSA 私钥爆破 (公钥 0x00 开头)。
lesson: |
  - 5 stage call 链是经典 Solidity 攻防套路
  - 全部 success 需 ECDSA 签名恢复私钥
  - secp256k1 公钥开头 00 的概率 1/256, 平均 256 次循环找
  - 私钥 d 是 uint256, 公钥是 d * G (G 是 secp256k1 generator)
  - emit log_bytes 事件可能泄露部分信息
quality: high
---

# PARADIGM CTF 2022 题目分析 (3) - Lockbox2

> 来源: ctfiot.com 80187 - NUMEN Cyber Labs

## 题目分析

```solidity
function solve() public {
    bool[5] memory successes;
    for (uint256 i = 0; i < 5; i++) {
        successes[i] = address(this).call(
            abi.encodeWithSignature(
                string(abi.encodePacked("stage", i+1)),
                msg.data[4:]
            )
        );
    }
    for (uint256 i = 0; i < 5; i++) {
        if (!successes[i]) return;
    }
    locked = false;
}
```

**关键**：
- 5 个 stage 函数必须 call 成功
- `msg.data[4:]` 是 calldata 后面部分
- locked = false 才能 isSolved() == true 拿 flag

## 攻击：ECDSA 私钥爆破

```python
import random
from ecdsa import ecdsa
g = ecdsa.generator_secp256k1
while True:
    private_key = random.randint(0, 1 << 256 - 1)
    public_key = private_key * g
    x = str(hex(public_key.x())[2:]).zfill(64)
    y = str(hex(public_key.y())[2:]).zfill(64)
    public_key_hex = x + y
    if public_key_hex[:2] == "00":
        print(private_key, public_key_hex)
        break
```

**为什么开头 0x00？**
- secp256k1 私钥 d 是 256-bit
- 公钥 = d * G (G 是 generator)
- 公钥 (x, y) 各 32 字节，拼成 64 字节 hex
- x 或 y 开头 0x00 的概率是 1/256
- 平均循环 256 次能找到一个

## emit log_bytes 事件

```solidity
emit log_bytes(: 0x890d6908);
```

事件中可能泄露 stage 函数的部分信息。

## 评价

PARADIGM CTF 2022 Lockbox2 多阶段调用题：
- **5 stage call 链** 必须全部 success
- **secp256k1 ECDSA** 私钥爆破 (公钥 0x00 开头)
- **emit log_bytes 事件** 可能泄露部分信息
- **all() 验证** 必须 5 个 successes 都 true

适用读者：Solidity 多阶段攻击 / ECDSA 密码学 / 私钥恢复
