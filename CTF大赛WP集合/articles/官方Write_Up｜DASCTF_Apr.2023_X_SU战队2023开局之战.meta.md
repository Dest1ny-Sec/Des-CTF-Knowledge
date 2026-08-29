---
title: DASCTF Apr.2023 X SU战队2023开局之战官方WP
contest: DASCTF Apr.2023 X SU战队2023开局之战
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [区块链, Solidity, 闪电贷, ERC3156, FlashLoan, Vault, 预言机操纵, Intention签名, Conflux_eSpace, eSpace, tx.origin, block.timestamp, UnCrackableGame, 委托调用delegatecall, 重入]
attack_chain: 这必不可能是预言机:Hacker合约构造Intention+签名+闪电贷借999WETH → 兑换比1:1000 → 存1WETH换1000FLAG → 转给Challenge合约 → 链上Poseidon.Blockchain交互;到国链之光一游:Conflux eSpace Testnet水龙头领gas → block.timestamp+keccak256猜key → getFlag触发CaptureTheFlag事件;easyCoin:delegatecall存owner可改;Guess:Range+重入
key_payload: 闪电贷999WETH + Intention签名(Intention+r/s/v) + TrashOracle + Poseidon.Blockchain框架
one_liner: DASCTF Apr.2023 X SU战队开局之战BLOCKCHAIN 4题:闪电贷操纵预言机/Conflux eSpace签名/UnCrackableGame delegatecall/Guess Range重入。
lesson: 闪电贷借出大量代币操纵预言机兑换比例(1:1→1000:1)是经典DeFi攻击;构造特殊Intention结构+链下ECDSA签名(v,r,s)绕过_verifyIntention;Conflux eSpace Testnet需先领gas;block.timestamp+keccak256作key可预测;Solidity 0.8.19+IERC3156FlashBorrower接口;UnCrackableGame经典delegatecall+storage覆盖;Guess猜数字用Range约束+回退检查防重入。
quality: high
---
