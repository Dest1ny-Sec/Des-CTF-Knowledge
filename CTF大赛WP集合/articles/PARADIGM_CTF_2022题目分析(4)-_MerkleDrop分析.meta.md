---
title: PARADIGM CTF 2022 题目分析 (4) - MerkleDrop 分析
contest: PARADIGM CTF 2022
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [MerkleTree, 空投合约, uint256_index, address, uint96_amount, MerkleProof验证, ParadigmCTF]
attack_chain:
  - MerkleDrop 合约结构：node + index uint256 + account address + amount uint96 + MerkleProof
  - 通过验证 MerkleProof 领取空投
  - Solidity 合约结构题
key_payload: 'MerkleProof 验证链'
one_liner: Paradigm CTF 2022 MerkleDrop 分析：Merkle Tree 空投合约结构与验证。
lesson: MerkleDrop 合约三要素：index（uint256）+ account（address）+ amount（uint96）+ MerkleProof 验证。
quality: low
---

# PARADIGM CTF 2022 题目分析 (4) - MerkleDrop 分析

## 来源
- 原文：ctfiot.com/80171.html
- 比赛：Paradigm CTF 2022

## MerkleDrop 合约结构

```solidity
struct Node {
    uint256 index;        // 索引
    address account;      // 账户地址
    uint96 amount;        // 金额（uint96 节省空间）
    MerkleProof proof;    // Merkle 证明
}
```

## 关键字段
- **index uint256**：节点索引
- **account address**：用户地址
- **amount uint96**：96 位无符号整数，节省存储
- **MerkleProof**：Merkle Tree 路径证明

## 关键技巧
- **uint96 替代 uint256**：节省 Gas
- **MerkleProof 验证**：链上验证 path
- **Airdrop 标准模式**：Paradigm CTF 经典空投合约结构

## 适用场景
- 区块链空投合约分析
- Merkle Tree 应用
- Solidity 优化模式
