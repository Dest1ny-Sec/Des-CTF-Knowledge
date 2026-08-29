---
title: PARADIGM CTF 2022 题目分析 (2) - Source Code (EVM bytecode 自构造)
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Solidity, EVM bytecode, safe 白名单, DUP1 + MSTORE, CODECOPY, PUSH32, RETURN]
attack_chain: |
  1. 题目: challenge.solve(bytes code) → 调 safe(code) 返回 true → new(code) 部署合约 → staticcall(code) 调用 → require(return == code 的 bytecode)
  2. safe(code) 遍历 code, 禁用 CODECOPY/CALLCODE/CALL 等操作码
  3. 关键: 合约的 bytecode 必须和 staticcall 的返回数据完全一致
  4. 攻击: 构造 32 字节指令:
     - PUSH32 0x80607f60005360015260215260416000f3... (32 字节, 7f 是 PUSH32 opcode)
     - DUP1 (复制栈顶, 准备执行)
     - PUSH1 0x7f + PUSH1 0x00 + MSTORE8 (存 0x7f 到 0 位置, 1 字节)
     - PUSH1 0x01 + MSTORE (存栈顶 32 字节到位置 1)
     - PUSH1 0x21 + MSTORE (存栈顶 32 字节到位置 33)
     - PUSH1 0x41 + PUSH1 0x00 + RETURN (从 0 返回 0x41 字节)
     - STOP (剩余填充)
  5. DUP1 复制 PUSH32 的内容, 既是 PUSH32 自身 (第一次执行) 也是 MSTORE 输入 (第二次)
  6. total code = 0x40 字节 (PUSH32) + 0x40 字节 (DUP1 + MSTORE*3 + RETURN) = 0x80 字节
key_payload: |
  PUSH32 0x80607f60005360015260215260416000f3000000000000000000000000000000
  DUP1
  PUSH1 0x7f
  PUSH1 0x00
  MSTORE8
  PUSH1 0x01
  MSTORE
  PUSH1 0x21
  MSTORE
  PUSH1 0x41
  PUSH1 0x00
  RETURN
  STOP (×N)
one_liner: PARADIGM CTF 2022 Source Code: 自构造 EVM bytecode (PUSH32 + DUP1 + MSTORE + RETURN) 让合约 bytecode == staticcall 返回。
lesson: |
  - Solidity safe() 函数禁用 CODECOPY/CALLCODE/CALL
  - 自构造 bytecode 让 code == staticcall return 是关键
  - DUP1 复制 PUSH32 内容, 既作 PUSH32 又作 MSTORE 输入
  - MSTORE8 (1 字节) + MSTORE (32 字节) 组合覆盖
  - EVM 操作码表: 7f=PUSH32, 80=DUP1, 7f=PUSH1, 52=MSTORE8, 53=MSTORE, 60=PUSH1, 00=STOP, f3=RETURN
  - total = 0x40 字节 (1 个 PUSH32) + 0x40 字节 (DUP1 + 9 个 PUSH1/MSTORE/RETURN) = 0x80 字节
quality: high
---

# PARADIGM CTF 2022 题目分析 (2) - Source Code

> 来源: ctfiot.com 80201 - NUMEN Cyber Labs

## 题目分析

```solidity
function solve(bytes memory code) external {
    require(code.length != 0);
    require(safe(code));
    address target;
    assembly {
        target := create(0, add(code, 0x20), mload(code))
    }
    require(target != address(0));
    (bool success, bytes memory result) = target.staticcall(msg.data);
    require(success && keccak256(result) == keccak256(code));
    solved = true;
}

function safe(bytes memory code) public pure returns (bool) {
    uint256 size = code.length;
    assembly {
        let success := 1
        let ptr := add(code, 0x20)
        for { let i := 0 } lt(i, size) { i := add(i, 1) } {
            let op := mload(add(ptr, i))
            if eq(op, 0x39) { success := 0 } // CODECOPY
            if eq(op, 0xF2) { success := 0 } // CALLCODE
            if eq(op, 0xF1) { success := 0 } // CALL
        }
    }
    return true;
}
```

**关键**：
- safe() 禁用 **CODECOPY** (0x39) / **CALLCODE** (0xF2) / **CALL** (0xF1)
- 合约 bytecode == staticcall return

## 攻击：自构造 EVM bytecode

```
PUSH32 0x80607f60005360015260215260416000f3000000000000000000000000000000
DUP1
PUSH1 0x7f
PUSH1 0x00
MSTORE8  // 存 0x7f 到 0 位置 (1 字节)
PUSH1 0x01
MSTORE   // 存栈顶 32 字节到位置 1
PUSH1 0x21
MSTORE   // 存栈顶 32 字节到位置 33 (0x01 + 0x20)
PUSH1 0x41
PUSH1 0x00
RETURN  // 从 0 返回 0x41 字节
STOP ×N
```

**关键 trick**：
- `DUP1` 复制 PUSH32 的内容，**既是 PUSH32 自身 (第一次执行) 也是 MSTORE 输入 (第二次)**
- 用 MSTORE8 (1 字节) + MSTORE (32 字节) 组合覆盖字节
- total = 0x40 字节 (PUSH32) + 0x40 字节 (DUP1 + 9 指令) = 0x80 字节
- 1 个 7f (0x7f=PUSH32) + 2 个 32 字节指令 = 0x41 字节返回 → RETURN

## 评价

PARADIGM CTF 2022 Source Code EVM bytecode 自构造题：
- **DUP1 复制** 是关键，省去 PUSH 操作
- **safe() 白名单** 限制操作码
- **bytecode == staticcall return** 是核心约束

适用读者：Solidity 合约安全 / EVM 字节码 / 高级 Web3
