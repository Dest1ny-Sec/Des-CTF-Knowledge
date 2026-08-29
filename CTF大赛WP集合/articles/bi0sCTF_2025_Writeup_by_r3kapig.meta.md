---
title: bi0sCTF 2025 Writeup by r3kapig
contest: bi0sCTF
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [blockchain, solidity, transient-storage, oracle-manipulation, dex, amm, batchTransfer-overflow, evade-create2, eradicate2]
attack_chain:
  - Transient Heist: 借鉴 SIR.trading 瞬态存储漏洞
  - swapCallback 绕过 msg.sender 检查
  - 创建恶意代币 + SwapPair
  - Transient Heist Revenge: ERADICATE2 暴力 create2 salt
  - Empty Vessel: ERC4626 vault + INR batchTransfer 溢出
  - 兑换金额小 → 乘积溢出
  - The Time Travellers DEX: snapshot 漏洞价格操纵
  - 1 ETH 借 INR flashloan 压价
  - mint INR 拉价
  - 50000 ETH bonus 2
key_payload: 瞬态存储漏洞 + ERADICATE2 + vault 溢出 + DEX 价格操纵
one_liner: bi0sCTF 2025 r3kapig 战队 WP 4 道区块链：瞬态存储偷窃/vault 溢出/时间旅行 DEX。
lesson: 现代区块链 CTF 越来越像真实 DeFi 攻击复现（SIR.trading/Venus 等真实事件）。
quality: high
---

bi0sCTF 2025 r3kapig 战队第一名 WP（**CTFtime 暂居世界第一**），4 道区块链题。

**Transient Heist**
- 借鉴 SIR.trading 真实黑客事件
- swapCallback 回调将兑换金额存瞬态存储 slot 1
- 该值也用于检查 msg.sender == SwapPair
- 通过特定数量 swap 让 slot 1 == 恶意合约地址绕过检查
- 调 swapCallback 设 collateralDeposited
- 攻击合约 + Killer 合约 + Exploit 合约

**Transient Heist Revenge**
- 同样思路，但 depositCollateralThroughSwap 检查 _collateralToken
- 兑换金额有上限，需要暴力破解 create2 salt
- 使用 ERADICATE2 工具
- 预部署 Attacker → 用其地址生成恶意合约 → 调 attack()

**Empty Vessel**
- ERC4626 vault 存 100_000 ether INR
- 目标：赎回金额 < 75_000 ether
- convertToAssets 用 totalAssets() / totalSupply()
- 在 stakeINR 之前给 vault 转 INR → 拉低份额
- INR 合约汇编实现，batchTransfer 没乘法溢出检查
- 构造 `2^256-2` 乘积溢出 → 转移大量 INR

**The Time Travellers DEX**
- Finance: stake (ETH → INR) / withdraw (INR → ETH) 按当前价格
- Oracle 是带累计价格功能的 DEX
- snapshot 后第一笔交易的价格被采用
- 限制：DEX 6 次 swap、flashloan 1 次、withdraw 不能在 flashloan 中
- 1 ETH 借 INR flashloan → 卖 INR 压价 → mint INR → 拉高价格 → 高价 burn
- 5 笔交易获得 50000 ETH → bonus 2
- sim1/sim2 Python 脚本搜索最佳比例

**Solana 暂时没题，但 Ethereum 生态全面考察**：
- DEX AMM 数学
- vault 计算精度
- 瞬态存储
- oracle 操纵
