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
