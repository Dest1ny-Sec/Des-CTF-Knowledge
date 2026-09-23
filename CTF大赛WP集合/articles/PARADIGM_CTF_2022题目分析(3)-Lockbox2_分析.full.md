---
title: PARADIGM CTF 2022 题目分析 (3) - Lockbox2 (5 stage calls + ECDSA)
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags:
- Solidity
- 5 stage calls
- ECDSA 私钥爆破
- secp256k1 特殊公钥
- log_bytes 事件
attack_chain: '|'
key_payload: '|'
one_liner: 'PARADIGM CTF 2022 Lockbox2: 5 stage 函数全部 call 成功 + secp256k1 ECDSA 私钥爆破 (公钥 0x00 开头)。'
lesson: '|'
quality: high
full_path: PARADIGM_CTF_2022题目分析(3)-Lockbox2_分析.full.md
meta_path: PARADIGM_CTF_2022题目分析(3)-Lockbox2_分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'PARADIGM CTF 2022 题目分析 (3) - Lockbox2 (5 stage calls + ECDSA)。PARADIGM CTF 2022 Lockbox2: 5 stage 函数全部 call 成功 + secp256k1 ECDSA 私钥爆破 (公钥 0x00 开头)。。经验：|'
category: web
subcategory: web_other
tools_used:
- Solidity
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/80187.html
reasoning_chain:
- 触发点:setup.isSolved() == !lockbox2.locked,locked 默认 true → 假设:必须调 solve 让 5 个 stage 调用都成功
- solve 内部用 msg.data[4:] 作为 calldata 调 stage1-5 → 假设:单笔 calldata 必须同时满足 5 个 stage
- stage3 要求 emit log_bytes(:0x890d6908) → 假设:需构造特定事件签名的 EVM bytecode
- 动作:用 PUSH1 0x40 + DUP1 + PUSH1 0x06 + PUSH1 0x00 + CODECOPY + PUSH1 0 + RETURN 构造 6 字节 runtime → 观察:能执行 log_bytes 事件
- stage1 要求公钥 x 坐标开头 0x00 → 假设:secp256k1 私钥可爆破出低 x 公钥 → 动作:Python 循环 random private_key 求 public_key 直到 x[:2]=='00'
- stage2/4/5 配合 stage1/3 拼接 calldata → 动作:把 5 个 stage 的 selector + 数据连成一笔 → 观察:全部 call 返回 success
failed_attempts:
- 试图用 Solidity 写 5 个独立函数调用 → 失败:solve 只传 msg.data[4:] 不分调用
- 试图用普通地址作为 stage1 输入 → 失败:必须公钥 x 坐标 0x00 开头才能匹配
key_observations:
- 单笔 calldata 串联多 stage 是 EVM CTF 经典模式,reducer/modifier 链式调用
- secp256k1 公钥 x 坐标首字节为 0 的概率约 1/256,爆破 256 次可命中
- PUSH1+DUP1+PUSH1+PUSH1+CODECOPY+RETURN 是最小可执行 runtime 模板
prerequisites:
- EVM 字节码最小构造(PUSH/MSTORE/RETURN/CODECOPY)
- secp256k1 公私钥对生成与 ecdsa 库
- Solidity ABI 编码与 calldata 拼接
---
# PARADIGM CTF 2022题目分析(3)-Lockbox2 分析

> 原文: https://www.ctfiot.com/80187.html
> ID: 80187

首先其导入了一个合约，导入的lockbox2合约先暂时不管，然后setup的初始化函数是new了一个lockbox2合约，然后一个isSolved函数，这个函数view修饰，不上链，返回lockbox2合约的locked函数的返回值的非值，一个bool类型，看来拿到flag的前提是要让lockbox2的locked函数返回false。

进入lockbox2合约，如下图所示：

首先它定义了一个全局变量，bool类型locked，初始为true。然后是没有参数的solve函数。此函数首先声明了一个bool类型，长度为5的数组successes。下标从0到4分别对应5个返回值。继续看每一行，分别是调用当前合约的stage1-5函数，calldata数据为msg.data第4位开始。从第四位开始，也就是不算函数签名。然后把每个调用是否成功作为一个bool值赋给success数组。然后是一个循环遍历这个bool类型的数组，每个都是true的话，继续运行，把locked设置为false。只有solve这一个入口可以改变locked变量。看来关键问题就是solve函数的5个调用。

import randomfrom Crypto.Util.number import isPrime
from ecdsa import ecdsag = ecdsa.generator_secp256k1while True: private_key = random.randint(0, 1 << 256 - 1) public_key = private_key * g x = str(hex(public_key.x())[2:]) x = ("00" * 32 + x)[-32 * 2:] y = str(hex(public_key.y())[2:]) y = ("00" * 32 + y)[-32 * 2:]    public_key_hex = x + y if public_key_hex[:2] == "00": print(private_key, public_key_hex) break;

PUSH1 0x40DUP1PUSH1 0x06PUSH1 0x0CODECOPYPUSH1 0RETURN

emit log_bytes(: 0x890d6908)

000000000000000000000000000000000000000000000000000000000000006100000000000000000000000000000000000000000000000000000000000001010000000000000000000000000000000000000000000000000000000000000001

0000000000000000000000000000000000000000000000000000000000000061 000000000000000000000000000000000000000000000000000000000000000101 200000000000000000000000000000000000000000000000000000000000000001 400000000000000000000000000000000000000000000000000000000000000001 6000

409548


```
import randomfrom Crypto.Util.number import isPrime
from ecdsa import ecdsag = ecdsa.generator_secp256k1while True: private_key = random.randint(0, 1 << 256 - 1) public_key = private_key * g x = str(hex(public_key.x())[2:]) x = ("00" * 32 + x)[-32 * 2:] y = str(hex(public_key.y())[2:]) y = ("00" * 32 + y)[-32 * 2:]    public_key_hex = x + y if public_key_hex[:2] == "00": print(private_key, public_key_hex) break;
PUSH1 0x40DUP1PUSH1 0x06PUSH1 0x0CODECOPYPUSH1 0RETURN
emit log_bytes(: 0x890d6908)
000000000000000000000000000000000000000000000000000000000000006100000000000000000000000000000000000000000000000000000000000001010000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000061 000000000000000000000000000000000000000000000000000000000000000101 200000000000000000000000000000000000000000000000000000000000000001 400000000000000000000000000000000000000000000000000000000000000001 6000
409548
```


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