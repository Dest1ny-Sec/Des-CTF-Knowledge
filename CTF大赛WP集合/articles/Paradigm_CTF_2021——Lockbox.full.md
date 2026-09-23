---
title: Paradigm CTF 2021 - Lockbox
contest: Paradigm CTF 2021
year: 2021
difficulty: hard
vuln_type: crypto_rsa
tags:
- blockchain
- ethereum
- solidity
- ecdsa
- ecrecover
- abi-encode
- assembly
- lockbox
attack_chain:
- Entrypoint 修饰符 _ 用 assembly 调 getSelector() 拿当前 stage 函数选择器
- 把 calldata 原样透传给 Stage 合约
- 'Stage 0: 猜 blockhash(block.number-1) 的前 4 字节'
- 'Stage 1: ecrecover(keccak("stage1")) 验证 v=28 + r=0x1f9c.. + s=0x6e95.. 还原地址'
- 'Stage 2: uint16 a+b<a 触发 uint16 溢出 (a=0xff1c, b=任意)'
- 'Stage 3: keys 数组 < lock 数组 + 升序 + 差值为偶数'
- 'Stage 4: choices[choice%6]==keccak256("choose")'
- 'Stage 5: msg.data.length<256 (8 个参数 + 4 字节 selector = 260 略超)'
- 单笔 calldata 串联所有 stage：先算 blockhash 前 4 字节 + 16 位溢出值 + r/s
- abi.encodePacked 拼装 8 个 bytes32 + 1 个 uint
- lockBoxExploit 用 assembly call gas() entry 0 size 0 触发整链路
key_payload: uint16(0xff1c) + bytes32(0x1f9c551056...) r + bytes32(0x6e95dc...) s + bytes32(keccak('choose')) + choice=4
one_liner: Paradigm 2021 Lockbox 通过 assembly 链式调用 6 个 stage 合约，分别用 blockhash、ecrecover、uint16 溢出、数组排序、keccak 选择、calldata 长度约束完成。
lesson: Ethereum assembly call 可以串联多个合约；ecrecover 私钥可控时 signHash 拿 v/r/s；uint16 加法溢出绕 (a>0 && b>0 && a+b<a)；msg.data 长度硬限制 <256。
quality: high
full_path: Paradigm_CTF_2021——Lockbox.full.md
meta_path: Paradigm_CTF_2021——Lockbox.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Paradigm CTF 2021 - Lockbox。Paradigm 2021 Lockbox 通过 assembly 链式调用 6 个 stage 合约，分别用 blockhash、ecrecover、uint16 溢出、数组排序、keccak 选择、calldata 长度约束完成。。关键路径：Entrypoint 修饰符 _ 用 assembly 调 getSelector() 拿当...
category: crypto
subcategory: rsa
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/141643.html
reasoning_chain:
- 触发点:entrypoint 修饰符 _ 用 assembly 调 getSelector() → 透传 calldata 给 Stage 合约 → 假设:链式调用多 stage
- Stage 0:猜 blockhash(block.number-1) 前 4 字节 → 假设:同区块内已知,直接读 on-chain blockhash
- Stage 1:ecrecover(keccak('stage1')) 还原 0x7E5F4552... → 假设:私钥可控可签任意 hash
- 动作:python eth_account.signHash(keccak('stage1'), private_key=0x...01) → 观察:得 v=0x1b r s
- Stage 2:uint16 a+b<a 触发溢出 → 假设:a=0xff1c + 任意 b 满足 a+b<a
- Stage 3:keys 数组 < lock 数组 + 升序 + 差值为偶数 → 假设:keys=lock-2k 即可
- Stage 4:choices[choice%6]==keccak256('choose') → 假设:choice=4 时 choices[4]=keccak256('choose')
- Stage 5:msg.data.length<256 → 假设:8 个 bytes32+1 个 uint=260 略超需精简
- 动作:abi.encodePacked 拼 8 bytes32+uint → assembly call gas() entry 触发整链路
failed_attempts:
- 试图分多笔交易分别调 stage → 失败:同 calldata 必须满足所有 stage
- 试图用默认私钥 0x01 → 失败:eth_account.signHash 需要 32 字节私钥,0x01 有效但要先验签
key_observations:
- Ethereum assembly call 可以串联多个合约(call gas()/to/value)
- ecrecover 私钥已知时 signHash 拿 v/r/s
- uint16 加法溢出绕 (a>0 && b>0 && a+b<a) 是经典绕过
prerequisites:
- EVM assembly 指令(mstore/call/calldatacopy)
- ecrecover 签名原理与 eth_account 库
- Solidity ABI encodePacked 与 calldata 长度限制
---
# Paradigm CTF 2021——Lockbox

> 原文: https://www.ctfiot.com/141643.html
> ID: 141643

modifier _() { _;
 assembly { //第一步：拿到全局变量Stage, 判断如果stage的值没有更新则返回 let next := sload(next_slot) if iszero(next) { return(0, 0) }
 //第二步：调用Stage上的getSelector()函数，将结果存储在内存中 // keccak(abi.encode("getSelector"))[0:
0x04] = 0x034899bc mstore(0x00, 0x034899bc00000000000000000000000000000000000000000000000000000000) pop(call(gas(), next, 0, 0, 0x04, 0x00, 0x04))
 //第三步：调用Stage合约，函数选择器为getSelector()函数的返回值，参数为CALLDATA[0x04:] calldatacopy(0x04, 0x04, sub(calldatasize(), 0x04)) switch call(gas(), next, 0, 0, calldatasize(), 0, 0) //第四步：如果调用失败，则REVERT case 0 { returndatacopy(0x00, 0x00, returndatasize()) revert(0x00, returndatasize()) } case 1 { returndatacopy(0x00, 0x00, returndatasize()) return(0x00, returndatasize()) } } }

从Entrypointto等到Stage1to Stage2，Stage5我们会将相同的 calldata 传递给所有调用。所以一个 calldata 解决题中的6个条件

function solve(bytes4 guess) public _ { require(guess == bytes4(blockhash(block.number - 1)), "do you feel lucky?");
 solved = true;}

function solve(uint8 v, bytes32 r, bytes32 s) public _ { require(ecrecover(keccak256("stage1"), v, r, s) == 0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf, "who are you?");}

from eth_account import Account, messagesfrom eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider
rpc = "https://mainnet.infura.io/v3/0aec7fd42e0a40f28dd6c1a185f7d3e6"web3 = Web3(HTTPProvider(rpc))
messageshash = web3.toHex(web3.sha3(text='stage1'))print(messageshash)private_key_hex = "0x0000000000000000000000000000000000000000000000000000000000000001"
signed_message = Account.signHash(message_hash=messageshash, private_key=private_key_hex)
print("signature =", signed_message)
print("r = ", web3.toHex(signed_message.r))print("s = ", web3.toHex(signed_message.s))print("v = ", web3.toHex(signed_message.v))

r = 0x370df20998cc15afb44c2879a3c162c92e703fc4194527fb6ccf30532ca1dd3bs = 0x35b3f2e2ff583fed98ff00813ddc7eb17a0ebfc282c011946e2ccbaa9cd3ee67v = 0x1b

const ethereumjs_util = require("ethereumjs-util");
const { randomBytes } = require('crypto');
const { ecdsaSign } = require('ethereum-cryptography/secp256k1')
const privateKeyStr = '0x0000000000000000000000000000000000000000000000000000000000000001';
const hashStr = '0x' + (ethereumjs_util.keccak(Buffer.from('stage1'), 256)).toString('hex');
const privateKey = Buffer.from(privateKeyStr.slice(2), "hex");
const hash = Buffer.from(hashStr.slice(2), "hex");
while (true) { // node_modules /@types/secp256k1/index.d.ts const { signature, recid } = ecdsaSign(hash, privateKey, { data: randomBytes(32) });
 v = recid + 27; r = Buffer.from(signature.slice(0, 32)) s = Buffer.from(signature.slice(32, 64))
 if (v != 28) { continue; }
 const rBN = '0x' + r.toString('hex'); const sBN = '0x' + s.toString('hex');
 // stage3 require: out of order if (sBN < rBN) { continue; }
 // // stage3 require: this is a bit odd if (sBN.slice(-2) % 2 != 0) { continue; }
 break;}
console.log('0x' + v.toString(16));console.log('0x' + r.toString('hex'));console.log('0x' + s.toString('hex'));

v = 0x1cr = 0x1f9c5510565172835329f4e0107b3af787bf46d1690f7e81aba39e47c9940d43s = 0x6e95dc6553997968a1be6cc8ae66dc1730cd1965f8b3e7114ca0f9df15fc3e98

function solve(uint16 a, uint16 b) public _ { require(a > 0 && b > 0 && a + b < a, "something doesn't add up");}

function solve(uint idx, uint[4] memory keys, uint[4] memory lock) public _ { require(keys[idx % 4] == lock[idx % 4], "key did not fit lock");
 for (uint i = 0; i < keys.length - 1; i++) { require(keys[i] < keys[i + 1], "out of order"); }
 for (uint j = 0; j < keys.length; j++) { require((keys[j] - lock[j]) % 2 == 0, "this is a bit odd"); }}

slot0 idx guess v slot1 keys[0] r slot2 keys[1] s slot3 keys[2] slot4 keys[3] slot5 lock[0]slot6 lock[1]

function solve(bytes32[6] choices, uint choice) public _ { require(choices[choice % 6] == keccak256(abi.encodePacked("choose")), "wrong choice!");}

function solve() public _ { require(msg.data.length < 256, "a little too long");}

import "./Setup.sol";
contract lockBoxExploit { Entrypoint public entrypoint; constructor(address _setup) public { entrypoint = lockBoxSetup(_setup).entrypoint(); } function exploit() public { bytes memory data = abi.encodePacked( entrypoint.solve.selector, uint(uint16(0xff1c) | (uint256(bytes32(bytes4(blockhash(block.number - 1))))), bytes32(0x1f9c5510565172835329f4e0107b3af787bf46d1690f7e81aba39e47c9940d43), //r bytes32(0x6e95dc6553997968a1be6cc8ae66dc1730cd1965f8b3e7114ca0f9df15fc3e98), //s bytes32(0x6e95dc6553997968a1be6cc8ae66dc1730cd1965f8b3e7114ca0f9df15fc3e9a), //满足差值偶数 bytes32(keccak256('choose')), bytes32(0x1f9c5510565172835329f4e0107b3af787bf46d1690f7e81aba39e47c9940d43), // =r bytes32(0x0000000000000000000000000000000000000000000000000000000000000004) //做的choice 也就是指向abi.encodePakced("choose")的指针 ); uint size = data.length; address entry = address(entrypoint); assembly{ switch call(gas(),entry,0,add(data,0x20),size,0,0) case 0 { returndatacopy(0x00,0x00,returndatasize()) revert(0, returndatasize()) } } }
}


```
modifier _() { _;
 assembly { //第一步：拿到全局变量Stage, 判断如果stage的值没有更新则返回 let next := sload(next_slot) if iszero(next) { return(0, 0) }
 //第二步：调用Stage上的getSelector()函数，将结果存储在内存中 // keccak(abi.encode("getSelector"))[0:
0x04] = 0x034899bc mstore(0x00, 0x034899bc00000000000000000000000000000000000000000000000000000000) pop(call(gas(), next, 0, 0, 0x04, 0x00, 0x04))
 //第三步：调用Stage合约，函数选择器为getSelector()函数的返回值，参数为CALLDATA[0x04:] calldatacopy(0x04, 0x04, sub(calldatasize(), 0x04)) switch call(gas(), next, 0, 0, calldatasize(), 0, 0) //第四步：如果调用失败，则REVERT case 0 { returndatacopy(0x00, 0x00, returndatasize()) revert(0x00, returndatasize()) } case 1 { returndatacopy(0x00, 0x00, returndatasize()) return(0x00, returndatasize()) } } }
function solve(bytes4 guess) public _ { require(guess == bytes4(blockhash(block.number - 1)), "do you feel lucky?");
 solved = true;}
function solve(uint8 v, bytes32 r, bytes32 s) public _ { require(ecrecover(keccak256("stage1"), v, r, s) == 0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf, "who are you?");}
from eth_account import Account, messagesfrom eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider
rpc = "https://mainnet.infura.io/v3/0aec7fd42e0a40f28dd6c1a185f7d3e6"web3 = Web3(HTTPProvider(rpc))
messageshash = web3.toHex(web3.sha3(text='stage1'))print(messageshash)private_key_hex = "0x0000000000000000000000000000000000000000000000000000000000000001"
signed_message = Account.signHash(message_hash=messageshash, private_key=private_key_hex)
print("signature =", signed_message)
print("r = ", web3.toHex(signed_message.r))print("s = ", web3.toHex(signed_message.s))print("v = ", web3.toHex(signed_message.v))
r = 0x370df20998cc15afb44c2879a3c162c92e703fc4194527fb6ccf30532ca1dd3bs = 0x35b3f2e2ff583fed98ff00813ddc7eb17a0ebfc282c011946e2ccbaa9cd3ee67v = 0x1b
const ethereumjs_util = require("ethereumjs-util");
const { randomBytes } = require('crypto');
const { ecdsaSign } = require('ethereum-cryptography/secp256k1')
const privateKeyStr = '0x0000000000000000000000000000000000000000000000000000000000000001';
const hashStr = '0x' + (ethereumjs_util.keccak(Buffer.from('stage1'), 256)).toString('hex');
const privateKey = Buffer.from(privateKeyStr.slice(2), "hex");
const hash = Buffer.from(hashStr.slice(2), "hex");
while (true) { // node_modules /@types/secp256k1/index.d.ts const { signature, recid } = ecdsaSign(hash, privateKey, { data: randomBytes(32) });
 v = recid + 27; r = Buffer.from(signature.slice(0, 32)) s = Buffer.from(signature.slice(32, 64))
 if (v != 28) { continue; }
 const rBN = '0x' + r.toString('hex'); const sBN = '0x' + s.toString('hex');
 // stage3 require: out of order if (sBN < rBN) { continue; }
 // // stage3 require: this is a bit odd if (sBN.slice(-2) % 2 != 0) { continue; }
 break;}
console.log('0x' + v.toString(16));console.log('0x' + r.toString('hex'));console.log('0x' + s.toString('hex'));
v = 0x1cr = 0x1f9c5510565172835329f4e0107b3af787bf46d1690f7e81aba39e47c9940d43s = 0x6e95dc6553997968a1be6cc8ae66dc1730cd1965f8b3e7114ca0f9df15fc3e98
function solve(uint16 a, uint16 b) public _ { require(a > 0 && b > 0 && a + b < a, "something doesn't add up");}
function solve(uint idx, uint[4] memory keys, uint[4] memory lock) public _ { require(keys[idx % 4] == lock[idx % 4], "key did not fit lock");
 for (uint i = 0; i < keys.length - 1; i++) { require(keys[i] < keys[i + 1], "out of order"); }
 for (uint j = 0; j < keys.length; j++) { require((keys[j] - lock[j]) % 2 == 0, "this is a bit odd"); }}
slot0 idx guess v slot1 keys[0] r slot2 keys[1] s slot3 keys[2] slot4 keys[3] slot5 lock[0]slot6 lock[1]
function solve(bytes32[6] choices, uint choice) public _ { require(choices[choice % 6] == keccak256(abi.encodePacked("choose")), "wrong choice!");}
function solve() public _ { require(msg.data.length < 256, "a little too long");}
import "./Setup.sol";
contract lockBoxExploit { Entrypoint public entrypoint; constructor(address _setup) public { entrypoint = lockBoxSetup(_setup).entrypoint(); } function exploit() public { bytes memory data = abi.encodePacked( entrypoint.solve.selector, uint(uint16(0xff1c) | (uint256(bytes32(bytes4(blockhash(block.number - 1))))), bytes32(0x1f9c5510565172835329f4e0107b3af787bf46d1690f7e81aba39e47c9940d43), //r bytes32(0x6e95dc6553997968a1be6cc8ae66dc1730cd1965f8b3e7114ca0f9df15fc3e98), //s bytes32(0x6e95dc6553997968a1be6cc8ae66dc1730cd1965f8b3e7114ca0f9df15fc3e9a), //满足差值偶数 bytes32(keccak256('choose')), bytes32(0x1f9c5510565172835329f4e0107b3af787bf46d1690f7e81aba39e47c9940d43), // =r bytes32(0x0000000000000000000000000000000000000000000000000000000000000004) //做的choice 也就是指向abi.encodePakced("choose")的指针 ); uint size = data.length; address entry = address(entrypoint); assembly{ switch call(gas(),entry,0,add(data,0x20),size,0,0) case 0 { returndatacopy(0x00,0x00,returndatasize()) revert(0, returndatasize()) } } }
}
```
