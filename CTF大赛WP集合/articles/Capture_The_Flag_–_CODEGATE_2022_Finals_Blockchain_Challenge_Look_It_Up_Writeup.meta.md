---
title: Capture The Flag – CODEGATE 2022 Finals Blockchain Challenge Look It Up Writeup
contest: CODEGATE 2022 Finals
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [blockchain, solidity, foundry, paradigm-ctf, NTT, isPowerOf2, bn256]
attack_chain:
  - nc启动私有链+uuid+RPC+private key
  - Setup合约challenge=new Challenge()
  - Challenge合约含flag但query()需10000 ether
  - isPowerOf2验证n+1为2的幂
  - sanity_check: f.length==n + t/s1/s2.length==n+1
  - 三个子条件solved1/solved2/solved3全true后declareSolved
  - 题目核心是构造三个有效proof（f, t, s1, s2）
key_payload: web3.sha3(text="isSolved()")[:4] → solved() call
one_liner: CODEGATE 2022 Finals区块链题 Look It Up，3层proof验证
lesson: Paradigm CTF框架部署区块链题，需10000 ether绕过+构造f/t/s1/s2
quality: high
---

# Capture The Flag – CODEGATE 2022 Finals Blockchain Challenge Look It Up Writeup

## 题目信息
- 比赛：CODEGATE 2022 Finals
- 类别：Blockchain
- 部署：Paradigm CTF 2022 dockerfiles / foundry 默认设置

## 关键攻击链
1. **环境接入**：
   - `nc 3.34.81.192 31337`
   - ticket: `kaistgonbestteam`
   - 获得 uuid + RPC endpoint + private key + Setup 合约地址
2. **合约结构**：
   - `Setup.challenge = new Challenge()` 0.8.0
   - `Challenge` 私有 flag，`query()` 要 `msg.value >= 10000 ether`
   - `p = 21888242871839275222246405745257275088548364400416034343698204186575808495617`（BN254 素数）
3. **核心约束**：
   - `isPowerOf2(n+1)`：n+1 必须为 2 的幂
   - `f.length==n`，t/s1/s2.length==n+1
   - 元素均在 [0, p)
   - 三子条件 solved1/solved2/solved3 全 true 后 `declareSolved()`
4. **解题思路**：构造满足 sanity_check 的 (f, t, s1, s2) 三个 proof
5. **isSolved 检测**：
   ```python
   web3.sha3(text="isSolved()")[:4] → call
   result.hex() == "0x...01"
   ```

## 关键技术点
- Solidity 0.8.0 合约
- BN254 椭圆曲线素数 p（alt_bn128）
- Paradigm CTF 部署框架
- foundry 工具链
- 3 个子条件 + 1 个 declare 模式

## 评分
- quality: high（合约源码 + 交互流程 + 验证逻辑完整）
