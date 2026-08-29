---
title: PARADIGM CTF 2022/Hint Finance
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type:
- logic
tags:
- 以太坊
- Solidity
- ERC777 重入
- ERC1820Registry 钩子
- 闪电贷
- 函数签名碰撞
- 0xcae9ca51
- approveAndCall
- 嵌套调用
attack_chain:
- 题目给 vault + factory + 3 个 token 合约（token1/3 是 ERC777，token2 是魔改 ERC20）
- 目标：让每个 vault 余额 < 初始 1%
- ERC777 通过 ERC1820Registry 注册 tokensReceived 钩子 → 跟经典重入一样
- withdraw 时已转账但 totalSupply 未更新 → 重新进入 deposit 增大份额占比
- 多次 withdraw+deposit 占据大部分份额后提走 → token1/3 解决
- token2（魔改 ERC20）有 approveAndCall 函数签名 (0xcae9ca51) 跟 flashloan 回调同签名
- 构造 data 双重满足 onHintFinanceFlashloan 和 approveAndCall
- 嵌套 approveAndCall → flashloan → approveAndCall 实现 vault 给攻击合约 approve
- 再 transferFrom 转走 token2
- 3 个 token 都被盗空 → 满足 vault < 1% 初始 → 拿 flag
key_payload: "register ERC1820 hook for from/to → withdraw → reenter deposit → loop"
one_liner: ERC777 重入 + 函数签名碰撞嵌套 approveAndCall 转走 vault 全部代币
lesson: 任何外部回调（不只是 ETH transfer）都可能造成重入；函数签名碰撞可用于跨合约调用伪装
quality: high
---

# PARADIGM CTF 2022/Hint Finance

**ERC777 重入 + 函数签名碰撞 + 嵌套 approveAndCall**

> PARADIGM CTF · 2022 · hard · logic · quality=high
> 思路: ERC777 通过 ERC1820Registry 注册 tokensReceived 钩子 → withdraw 时重入 deposit 增大份额 → 多次循环占多数 → withdraw token1/3 解决；token2 用 approveAndCall(0xcae9ca51) 跟 flashloan 回调同签名 → 构造 data 双重满足两个函数 → 嵌套调用盗空 token2
> 套路: 任何外部回调（不只是 ETH transfer）都可能造成重入；函数签名碰撞可用于跨合约调用伪装

**关键 payload**:
```solidity
register ERC1820 hook for from/to → withdraw → reenter deposit → loop
```
