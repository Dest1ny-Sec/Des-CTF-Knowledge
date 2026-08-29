---
title: CTF 专栏｜以太坊应用中基于回退与返回错误的假充值攻击原理分析
contest: Blockchain CTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [Solidity 0.8.0, ERC-20, transfer 返回 false, transferFrom 不检查返回值, Exchange enter/exit, 假充值, balanceOf 虚增, IERC20 继承, OpenZeppelin, msg.value 10 ether, onlyOwner]
attack_chain:
  - Solidity 0.8.0 写 StokenERC20 继承 IERC20
  - transfer/transferFrom 余额不足时 return false (不 revert)
  - Exchange enter(): token.transferFrom(msg.sender, this, amount) 不检查返回值
  - balances[msg.sender] += amount 继续执行 → 假充值
  - 攻击: 调用 enter(100 ether) 即使 ERC20 余额 0
  - Exchange 余额虚增, 调 exit() 提款
  - require(amount >= 10 ether) 最低门槛
  - 防御: 用 SafeERC20 或 require(token.transferFrom()) 包装
key_payload: 'transfer return false / transferFrom 不检查 / balances 虚增 / OpenZeppelin SafeERC20 / require token.transferFrom / 10 ether 最低'
one_liner: 以太坊假充值攻击 — Solidity ERC-20 transfer/transferFrom 返回 false 不回退 + Exchange enter() 不检查 transferFrom 返回值 + balances 虚增 + exit() 提款。
lesson: Solidity 0.8.0 之前 transfer 不回退是经典假充值漏洞;防御: SafeERC20.safeTransferFrom() + require(token.transferFrom());msg.value=10 ether 是常见门槛。
quality: high
---

# CTF 专栏｜以太坊应用中基于回退与返回错误的假充值攻击原理分析

## 速读
以太坊假充值攻击原理 — Solidity ERC-20 transfer/transferFrom 返回 false 不回退。

## 漏洞合约

### StokenERC20
```solidity
function transfer(address _to, uint256 _value) public override returns (bool) {
    if (balanceOf[msg.sender] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        return true;
    } else {
        return false;  // 余额不足时返回 false, 不 revert
    }
}

function transferFrom(address _from, address _to, uint256 _value) public override returns (bool) {
    if (balanceOf[_from] >= _value && allowance[_from][msg.sender] >= _value && ...) {
        // 转账成功
        return true;
    } else {
        return false;  // 不 revert
    }
}
```

### Exchange
```solidity
function enter(uint256 amount) public {
    require(amount >= 10 ether, "minimum is 10");
    token.transferFrom(msg.sender, address(this), amount);  // 不检查返回值!
    balances[msg.sender] += amount;  // 虚增
}

function exit(uint256 amount) public {
    require(balances[msg.sender] >= amount, "user doesn't have enough funds");
    balances[msg.sender] -= amount;
    payable(msg.sender).transfer(amount);  // 提款
}
```

## 攻击
1. 用户 ERC-20 余额 0
2. `Exchange.enter(100 ether)` 
3. `token.transferFrom` 返回 false (因为没余额/allowance)
4. **但** `balances[user] += 100 ether` 仍执行
5. `Exchange.exit(100 ether)` 提到真钱

## 防御
```solidity
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

using SafeERC20 for IERC20;

function enter(uint256 amount) public {
    require(amount >= 10 ether);
    token.safeTransferFrom(msg.sender, address(this), amount);  // 会 revert
    balances[msg.sender] += amount;
}
```

或手动检查:
```solidity
require(token.transferFrom(msg.sender, address(this), amount), "transfer failed");
```
