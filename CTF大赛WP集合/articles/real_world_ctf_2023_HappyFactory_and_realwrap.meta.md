---
title: real world ctf 2023 HappyFactory and realwrap
contest: RWCTF
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [blockchain, solidity, uniswap-v2-fork, kp3r, reward-distribution, flashloan, impermanent-loss]
attack_chain:
  - 自定义 KonohaFactory/KonohaPair
  - 复刻 UniswapV2 接口
  - 提供 WETH/KP3R 流动性
  - 大量 addLiquidity 累积 LP
  - flashloan 借 KP3R 提流动性
  - swap 操纵价格
  - removeLiquidity 提 ETH + KP3R
  - repay flashloan
key_payload: 自定义 UniswapV2 复刻 + LP 累积攻击
one_liner: RWCTF 2023 HappyFactory 区块链题，自定义 UniswapV2 复刻的 LP 攻击。
lesson: 当 DEX 是 UniswapV2 复刻时，要特别留意 feeTo / feeToSetter 等管理函数是否可调用。
quality: high
---

Real World CTF 2023 HappyFactory + realwrap 题 WP（来源 ctfiot）。

**HappyFactory 题**
题目合约是 KonohaFactory + KonohaPair 完整复刻 UniswapV2，漏洞不在主流程，而是：
- `feeTo()` / `feeToSetter()` 公开可调
- `setFeeTo(address)` / `setFeeToSetter(address)` 公开
- 攻击者可以先调 setFeeToSetter 把自己设为 setter，再 setFeeTo(address) 收所有手续费

或者：
- `mintFee` 函数可重入触发
- `_update` 内部 K 值计算有 off-by-one

**realwrap 题**
经典 LP 提供/移除的"impermanent loss + flashloan 套利"：
1. 借 WETH/KP3R LP
2. 在 UniswapV2 上 swap 操纵价格
3. 在 KonohaPair 上 removeLiquidity 拿 ETH
4. repay flashloan + 利润

**核心 exploit 模式**：
- Flashloan 提供零成本大额借款
- 用借来的 token 操纵 DEX 价格
- 在另一处 DEX 套利
- repay flashloan

整篇是"DeFi 真实场景攻击"经典复现。
