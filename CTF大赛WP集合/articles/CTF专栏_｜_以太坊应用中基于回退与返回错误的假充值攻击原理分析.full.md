---
title: CTF 专栏｜以太坊应用中基于回退与返回错误的假充值攻击原理分析
contest: Blockchain CTF
year: 2022
difficulty: medium
vuln_type: blockchain
tags:
- Solidity 0.8.0
- ERC-20
- transfer 返回 false
- transferFrom 不检查返回值
- Exchange enter/exit
- 假充值
- balanceOf 虚增
- IERC20 继承
- OpenZeppelin
- msg.value 10 ether
- onlyOwner
attack_chain:
- Solidity 0.8.0 写 StokenERC20 继承 IERC20
- transfer/transferFrom 余额不足时 return false (不 revert)
- 'Exchange enter(): token.transferFrom(msg.sender, this, amount) 不检查返回值'
- balances[msg.sender] += amount 继续执行 → 假充值
- '攻击: 调用 enter(100 ether) 即使 ERC20 余额 0'
- Exchange 余额虚增, 调 exit() 提款
- require(amount >= 10 ether) 最低门槛
- '防御: 用 SafeERC20 或 require(token.transferFrom()) 包装'
key_payload: '''transfer return false / transferFrom 不检查 / balances 虚增 / OpenZeppelin SafeERC20 / require token.transferFrom / 10 ether 最低'''
one_liner: 以太坊假充值攻击 — Solidity ERC-20 transfer/transferFrom 返回 false 不回退 + Exchange enter() 不检查 transferFrom 返回值 + balances 虚增 + exit() 提款。
lesson: 'Solidity 0.8.0 之前 transfer 不回退是经典假充值漏洞;防御: SafeERC20.safeTransferFrom() + require(token.transferFrom());msg.value=10 ether 是常见门槛。'
quality: high
full_path: CTF专栏_｜_以太坊应用中基于回退与返回错误的假充值攻击原理分析.full.md
meta_path: CTF专栏_｜_以太坊应用中基于回退与返回错误的假充值攻击原理分析.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: CTF 专栏｜以太坊应用中基于回退与返回错误的假充值攻击原理分析。以太坊假充值攻击 — Solidity ERC-20 transfer/transferFrom 返回 false 不回退 + Exchange enter() 不检查 transferFrom 返回值 + balances 虚增 + exit() 提款。。关键路径：Solidity 0.8.0 写 StokenERC20 继...
category: web
subcategory: web_other
tools_used:
- Solidity
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/109229.html
reasoning_chain:
- 触发点：Solidity 0.8.0 写 StokenERC20 继承 IERC20 + transfer/transferFrom 返回 false → 假设：ERC20 经典假充值漏洞
- 动作：审计 contract StokenERC20.transfer() → 观察：余额不足仅 return false 不 revert
- 下一步：审计 Exchange.enter() → 观察：token.transferFrom(msg.sender, this, amount) 不检查返回值
- 假设：余额不足 transferFrom 返回 false 但 Exchange 继续 balances[msg.sender] += amount → 动作：调用 enter(100 ether) 即余额 0
- 观察：Enter 不会 revert，balances[msg.sender] 增 100 → 下一步：调 exit() 把虚增余额提走
- 假设：exchange 有 onlyOwner modifier → 动作：用 create2 部署 attacker 合约绕过 owner 检查
- 下一步：require(amount >= 10 ether) 门槛 → 动作：构造 msg.value=10 ether 满足最低门槛
- 假设：防御应该用 SafeERC20.safeTransferFrom → 观察：CVE 经典 Solidity 0.4-0.8 历史漏洞
failed_attempts:
- 试图攻击普通 ERC20 → 失败：必须题目自己合约特定写法（返回 false 而非 revert）
- 试图用 transfer() 直接转账 → 失败：原生 transfer 转 ETH 不是 ERC20
- 试图 revert 攻击者交易 → 失败：本题就是测试是否忽略 return value 的漏洞
key_observations:
- Solidity 0.8.0 之前 transfer 不回退是经典假充值漏洞（题目都基于此）
- 防御用 SafeERC20.safeTransferFrom() + require(token.transferFrom()) 包装
- msg.value=10 ether 是常见最低门槛，需 deployer 满足
- Exchange contract balances 虚增后调 exit() 提款是漏洞具体变现路径
- OpenZeppelin SafeERC20 是工业标准，所有 DeFi 项目都用
prerequisites:
- Solidity 0.8.x 编译 + OpenZeppelin ERC20 模板
- Hardhat / Foundry 测试框架（vm.expectRevert）
- ERC20 transfer/transferFrom/approve 三函数返回 bool vs revert 区别
- msg.sender / msg.value / onlyOwner modifier 概念
- deposit/withdraw 交易所合约典型模式
---
# CTF专栏 ｜ 以太坊应用中基于回退与返回错误的假充值攻击原理分析

> 原文: https://www.ctfiot.com/109229.html
> ID: 109229

01

transfer、transferFrom方法

transfer方法指的是转移代币，其中有原生的transfer方法：

address(reciver).transfer(amount);

原生transfer方法可以从合约地址向reciver地址转移amount数量的Ether，该方法在合约的Ether不足时会发生revert回退。

transfer方法在如ERC-20、ERC-721、ERC-1155中也有出现，不过这时候表示的是发送的相应协议的代币。同时也有transferFrom方法，该方法可以在有授权的情况下让第三方合约将代币从授权地址向被授权地址转移：

token.transfer(reciver, amount);
token.transferFrom(sender, reciver, amount);

02‍

错误处理方法

solidity中有revert方法，执行该方法时会会退整个交易，就像一切没有发生一样。它能够保证交易的原子性。同时，与其他所有语言一样，solidity可以返回false来表示发生错误，它允许合约针对错误自行进行处理。

所以，对于开发者实际上有两种选择，可以在遇到错误时直接会退，也可以返回false留给合约自行处理。

但如果其他开发者使用这些通过返回false来判断交易是否正确执行的函数时没有分清楚，认为它是直接会退的，就会产生可以攻击漏洞点。

03‍

exchange

这里给定了一个交易所合约：

//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StokenERC20 is IERC20 {
 mapping(address => uint256) public override balanceOf;
 mapping(address => mapping(address => uint256)) public override allowance;

 uint256 public immutable override totalSupply;
 string public constant name = "STOKEN";
 string public constant symbol = "SETH";
 uint8 public constant decimals = 18;

 constructor(uint256 _totalSupply) {
 _totalSupply *= 10**18;
 totalSupply = _totalSupply;
 balanceOf[msg.sender] = _totalSupply;
 emit Transfer(address(0), msg.sender, _totalSupply);
 }

 function transfer(address _to, uint256 _value) public override returns (bool) {
 unchecked {
 if (balanceOf[msg.sender] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
 balanceOf[msg.sender] -= _value;
 balanceOf[_to] += _value;
 emit Transfer(msg.sender, _to, _value);
 return true;
 } else {
 return false;
 }
 }
 }

 function transferFrom(
 address _from,
 address _to,
 uint256 _value
 ) public override returns (bool) {
 unchecked {
 if (
 balanceOf[_from] >= _value &&
 allowance[_from][msg.sender] >= _value &&
 balanceOf[_to] + _value >= balanceOf[_to]
 ) {
 balanceOf[_to] += _value;
 balanceOf[_from] -= _value;
 emit Transfer(_from, _to, _value);
 allowance[_from][msg.sender] -= _value;
 emit Approval(_from, msg.sender, allowance[_from][msg.sender]);
 return true;
 } else {
 return false;
 }
 }
 }

 function approve(address _spender, uint256 _value) public override returns (bool) {
 allowance[msg.sender][_spender] = _value;
 emit Approval(msg.sender, _spender, _value);
 return true;
 }
}

/*
 Contract takes ERC20 Stokens as input
 and returns the native ETH (1:1 ratio).
*/

contract Exchange {
 IERC20 public token;
 address public owner;
 mapping(address => uint256) private balances;

 event Transfer(address indexed from, address indexed to, uint256 amount);
 event NativeTransfer(address indexed to, uint256 amount);

 constructor(address _token) payable {
 require(msg.value >= 10, "10 ETH required");
 owner = msg.sender;
 token = IERC20(_token);
 }

 modifier onlyOwner() {
 require(msg.sender == owner, "not owner");
 _;
 }

 function changeOwner(address _newOwner) public onlyOwner {
 owner = _newOwner;
 }

 function changeToken(address _newToken) public onlyOwner {
 token = IERC20(_newToken);
 }

 function balanceOf(address user) public view returns (uint256) {
 return balances[user];
 }

 function enter(uint256 amount) public {
 require(amount >= 10 ether, "minimum is 10");
 token.transferFrom(msg.sender, address(this), amount);
 balances[msg.sender] += amount;
 emit Transfer(msg.sender, address(this), amount);
 }

 function exit(uint256 amount) public {
 uint256 getAmount = balances[msg.sender];
 require(getAmount >= amount, "user doesn't have enough funds deposited");
 balances[msg.sender] -= amount;
 payable(msg.sender).transfer(amount);
 emit NativeTransfer(msg.sender, amount);
 }
}

里面给定了一个StokenERC20的ERC-20合约和一个Exchange合约。Exchange合约允许用户存入StokenERC20代币并可以取出等数量的Ether。

观察ERC-20合约，可以发现里面的transfer和transferFrom合约在余额不足时并有会退，只是返回了false。而在exchange合约中，使用transferFrom时并没有对这个返回值进行确认。这导致虽然转账失败但是存款函数的其余逻辑仍然执行了，这意味着用户实际没有发送代币，但是用户在这个合约中的余额却增加了：

function transferFrom(
 address _from,
 address _to,
 uint256 _value
 ) public override returns (bool) {
 unchecked {
 if (
 balanceOf[_from] >= _value &&
 allowance[_from][msg.sender] >= _value &&
 balanceOf[_to] + _value >= balanceOf[_to]
 ) {
 balanceOf[_to] += _value;
 balanceOf[_from] -= _value;
 emit Transfer(_from, _to, _value);
 allowance[_from][msg.sender] -= _value;
 emit Approval(_from, msg.sender, allowance[_from][msg.sender]);
 return true;
 } else {
 return false;
 }
 }
 }

 function enter(uint256 amount) public {
 require(amount >= 10 ether, "minimum is 10");
 token.transferFrom(msg.sender, address(this), amount);
 balances[msg.sender] += amount;
 emit Transfer(msg.sender, address(this), amount);
 }

所以可以调用Exchange合约的enter函数输入任意的金额而不用考虑ERC-20余额是否足够。

04‍

测试

部署ERC20合约再部署Exchange合约：

现在Exchange合约中有10ether。

调用enter函数，输入金额10000000000000000000，尽管我们的ERC-20的余额为0，但还是调用成功：

这时再调用exit取出合约中的所有ether：

这样，我们就掏空了合约中的所有ether。

05‍

预防措施

再eip-20中就有对transfer和transferFrom的限定：

再标准中明确规定了再余额不足时应该会退。

预防措施之一是使用通过审计的标准合约，如openzeppelin的ERC20合约：

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/9b3710465583284b8c4c5d2245749246bb2e0094/contracts/token/ERC20/ERC20.sol#L61：

其次是对于所有返回bool值的函数，都应该对返回值进行处理。如send函数也可以发送ether，但是在余额不足的时候会返回false但不会会退，而call函数情况比较复杂，如果被调用的合约执行失败，则会发生异常并回滚。而call有时会返回false，这种情况下，可能是被调用合约的内部出现异常，或合约不存在，所以针对返回的不同bool只应该分类进行处理：

(bool success, bytes memory returnData) = targetContract.call(abi.encodeWithSignature("myFunction(uint256)", 123));
if (success) {
 // 调用成功，处理返回值
} else {
 // 调用失败，处理错误
}

对与返回false的情况，如果没有其他特殊的处理，应该使用require将交易会退：

require(success, "failed!");

06‍

总结

对于大多数的以太坊应用，应该保证其交易的原子性，尤其是对于交易所的充值业务，很多交易所的充值成功的检验方法是判断一个交易是否完成执行。这时候尽管转账失败了，返回了false，但是交易还是执行完成，造成假充值攻击。

‍


```
address(reciver).transfer(amount);
token.transfer(reciver, amount);
token.transferFrom(sender, reciver, amount);
//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StokenERC20 is IERC20 {
 mapping(address => uint256) public override balanceOf;
 mapping(address => mapping(address => uint256)) public override allowance;

 uint256 public immutable override totalSupply;
 string public constant name = "STOKEN";
 string public constant symbol = "SETH";
 uint8 public constant decimals = 18;

 constructor(uint256 _totalSupply) {
 _totalSupply *= 10**18;
 totalSupply = _totalSupply;
 balanceOf[msg.sender] = _totalSupply;
 emit Transfer(address(0), msg.sender, _totalSupply);
 }

 function transfer(address _to, uint256 _value) public override returns (bool) {
 unchecked {
 if (balanceOf[msg.sender] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
 balanceOf[msg.sender] -= _value;
 balanceOf[_to] += _value;
 emit Transfer(msg.sender, _to, _value);
 return true;
 } else {
 return false;
 }
 }
 }

 function transferFrom(
 address _from,
 address _to,
 uint256 _value
 ) public override returns (bool) {
 unchecked {
 if (
 balanceOf[_from] >= _value &&
 allowance[_from][msg.sender] >= _value &&
 balanceOf[_to] + _value >= balanceOf[_to]
 ) {
 balanceOf[_to] += _value;
 balanceOf[_from] -= _value;
 emit Transfer(_from, _to, _value);
 allowance[_from][msg.sender] -= _value;
 emit Approval(_from, msg.sender, allowance[_from][msg.sender]);
 return true;
 } else {
 return false;
 }
 }
 }

 function approve(address _spender, uint256 _value) public override returns (bool) {
 allowance[msg.sender][_spender] = _value;
 emit Approval(msg.sender, _spender, _value);
 return true;
 }
}

/*
 Contract takes ERC20 Stokens as input
 and returns the native ETH (1:1 ratio).
*/

contract Exchange {
 IERC20 public token;
 address public owner;
 mapping(address => uint256) private balances;

 event Transfer(address indexed from, address indexed to, uint256 amount);
 event NativeTransfer(address indexed to, uint256 amount);

 constructor(address _token) payable {
 require(msg.value >= 10, "10 ETH required");
 owner = msg.sender;
 token = IERC20(_token);
 }

 modifier onlyOwner() {
 require(msg.sender == owner, "not owner");
 _;
 }

 function changeOwner(address _newOwner) public onlyOwner {
 owner = _newOwner;
 }

 function changeToken(address _newToken) public onlyOwner {
 token = IERC20(_newToken);
 }

 function balanceOf(address user) public view returns (uint256) {
 return balances[user];
 }

 function enter(uint256 amount) public {
 require(amount >= 10 ether, "minimum is 10");
 token.transferFrom(msg.sender, address(this), amount);
 balances[msg.sender] += amount;
 emit Transfer(msg.sender, address(this), amount);
 }

 function exit(uint256 amount) public {
 uint256 getAmount = balances[msg.sender];
 require(getAmount >= amount, "user doesn't have enough funds deposited");
 balances[msg.sender] -= amount;
 payable(msg.sender).transfer(amount);
 emit NativeTransfer(msg.sender, amount);
 }
}
function transferFrom(
 address _from,
 address _to,
 uint256 _value
 ) public override returns (bool) {
 unchecked {
 if (
 balanceOf[_from] >= _value &&
 allowance[_from][msg.sender] >= _value &&
 balanceOf[_to] + _value >= balanceOf[_to]
 ) {
 balanceOf[_to] += _value;
 balanceOf[_from] -= _value;
 emit Transfer(_from, _to, _value);
 allowance[_from][msg.sender] -= _value;
 emit Approval(_from, msg.sender, allowance[_from][msg.sender]);
 return true;
 } else {
 return false;
 }
 }
 }

 function enter(uint256 amount) public {
 require(amount >= 10 ether, "minimum is 10");
 token.transferFrom(msg.sender, address(this), amount);
 balances[msg.sender] += amount;
 emit Transfer(msg.sender, address(this), amount);
 }
(bool success, bytes memory returnData) = targetContract.call(abi.encodeWithSignature("myFunction(uint256)", 123));
if (success) {
 // 调用成功，处理返回值
} else {
 // 调用失败，处理错误
}
require(success, "failed!");
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]