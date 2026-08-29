---
title: paradigm 2022 ctf — Rescue
contest: paradigm
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [blockchain, solidity, uniswap-v2, sushiswap, masterchef, addliquidity, slipstream]
attack_chain:
  - MasterChefHelper 调 masterchef.poolInfo
  - UniswapV2RouterLike 调 swapExactTokensForTokens
  - addLiquidity 拿 LP
  - 漏洞：addLiquidity 不检查 amountOut
  - 用 0 minAmountOut 调 addLiquidity
  - 实际拿 token1 调 addLiquidity
  - 重入 swapTokenForPoolToken
  - 提空 Setup
key_payload: addLiquidity 不检查 amountOut + 重入
one_liner: paradigm 2022 Rescue 区块链题，SushiSwap LP 池重入。
lesson: 'addLiquidity 的 minAmountOut 不检查 = 任何人都能抽干 LP 池。'
quality: high
---

paradigm 2022 CTF Rescue 完整 WP（来源 ctfiot）。

**题目合约**
```solidity
// Setup: WETH 10 ether + 转给 MasterChefHelper
// MasterChefHelper.swapTokenForPoolToken(poolId, tokenIn, amountIn, minAmountOut)
//   - masterchef.poolInfo(poolId) 拿 LP
//   - token0/1 调 addLiquidity
//   - router.addLiquidity(token0, token1, balance, balance, 0, 0, msg.sender, now)
//   - require(amountOut >= minAmountOut)
```

**漏洞**：
`addLiquidity` 的 `minAmountOut=0`，不检查实际 amountOut。结果：
1. 攻击合约给 `swapTokenForPoolToken` 转 WETH
2. MasterChefHelper 切 WETH 换 token0/1
3. 调 addLiquidity 拿 LP 给攻击者
4. **重入**：用 `swapTokenForPoolToken` 再次进入
5. 第二次 addLiquidity 用 `balanceOf(this)` 但 balance 已为 0
6. 拿空 Setup

**测试结果**：
- pair_id 0: WETH/USDT (0x06da0fd433C1A5d7a4faa01111c044910A184553)
- pair_id 1: USDC/WETH (0x397FF1542f962076d0BFE58eA045FfA2d347ACa0)
- pair_id 9: ...

**关键洞**：`addLiquidity(token0, token1, balanceOf(this), balanceOf(this), 0, 0, msg.sender, block.timestamp)` 把余额 0 当 input → 拿到 0 LP，但调用仍然成功！

```solidity
function _addLiquidity(address token0, address token1, uint256 minAmountOut) internal {
    (,, uint256 amountOut) = router.addLiquidity(
        token0, token1,
        ERC20Like(token0).balanceOf(address(this)),  // 漏洞：第二次为 0
        ERC20Like(token1).balanceOf(address(this)),  // 漏洞：第二次为 0
        0, 0,  // minAmountOut = 0
        msg.sender, block.timestamp
    );
    require(amountOut >= minAmountOut);  // 0 >= 0 永远 true
}
```

**质量**：经典"amountOut 不检查"漏洞，参考 2021 PolyNetwork 攻击事件。
