---
title: Paradigm CTF 2021 - Lockbox
contest: Paradigm CTF 2021
year: 2021
difficulty: high
vuln_type: crypto_rsa
tags: [blockchain, ethereum, solidity, ecdsa, ecrecover, abi-encode, assembly, lockbox]
attack_chain:
  - Entrypoint 修饰符 _ 用 assembly 调 getSelector() 拿当前 stage 函数选择器
  - 把 calldata 原样透传给 Stage 合约
  - Stage 0: 猜 blockhash(block.number-1) 的前 4 字节
  - Stage 1: ecrecover(keccak("stage1")) 验证 v=28 + r=0x1f9c.. + s=0x6e95.. 还原地址
  - Stage 2: uint16 a+b<a 触发 uint16 溢出 (a=0xff1c, b=任意)
  - Stage 3: keys 数组 < lock 数组 + 升序 + 差值为偶数
  - Stage 4: choices[choice%6]==keccak256("choose")
  - Stage 5: msg.data.length<256 (8 个参数 + 4 字节 selector = 260 略超)
  - 单笔 calldata 串联所有 stage：先算 blockhash 前 4 字节 + 16 位溢出值 + r/s
  - abi.encodePacked 拼装 8 个 bytes32 + 1 个 uint
  - lockBoxExploit 用 assembly call gas() entry 0 size 0 触发整链路
key_payload: uint16(0xff1c) + bytes32(0x1f9c551056...) r + bytes32(0x6e95dc...) s + bytes32(keccak('choose')) + choice=4
one_liner: Paradigm 2021 Lockbox 通过 assembly 链式调用 6 个 stage 合约，分别用 blockhash、ecrecover、uint16 溢出、数组排序、keccak 选择、calldata 长度约束完成。
lesson: Ethereum assembly call 可以串联多个合约；ecrecover 私钥可控时 signHash 拿 v/r/s；uint16 加法溢出绕 (a>0 && b>0 && a+b<a)；msg.data 长度硬限制 <256。
quality: high
---
