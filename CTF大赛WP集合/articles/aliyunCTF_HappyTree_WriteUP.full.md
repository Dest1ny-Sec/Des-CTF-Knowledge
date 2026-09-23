---
title: aliyunCTF HappyTree WriteUP
contest: aliyunCTF HappyTree
year: 2024
difficulty: hard
vuln_type: blockchain
tags:
- merkle_tree_verify
- solidity_smart_contract
- keccak256_abi_encodePacked
- leaf_used_replay
- merkle_proof_construction
- ethereum_blockchain
- function_b_verify
- leaf_used_mapping
- blockchain_ctf
attack_chain: Solidity Greeter 合约 + b(leafs[], proofs[], indexs[]) 函数 + verify(proof, leaf, index) Merkle 路径验证 (index%2==0 则 hash=keccak256(hash,proof) 否则 keccak256(proof,hash)) + used_leafs[leaf] 防止重放 + this.a(i, y) 调用 → 3 个 leaf (0x8137...cd6a, 0x28ca...79b6, 0x804c...31d) + 4 个 proofs + 4 个 indexs (0,1,2,4) + root 0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e
key_payload: leafs = [0x81376b..., 0x28cac3..., 0x804cd8..., 0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e] / proofs[i] for i in 4 / indexs = [0,1,2,4] / verify(proofs, leaf, index) keccak256 abi.encodePacked
one_liner: aliyunCTF HappyTree WriteUP：Solidity Merkle Tree 验证合约 b(leafs, proofs, indexs) 接收 3 个 leaf + 4 个 proof + 4 个 index，verify 通过 keccak256(abi.encodePacked(hash, proof)) 计算路径验证 == root。
lesson: Merkle Tree 在 CTF 区块链题中是验证批量 leaf 的标准结构；keccak256(abi.encodePacked(hash, proof)) 是按 index 奇偶交换参数的 Merkle 验证算法。
quality: high
full_path: aliyunCTF_HappyTree_WriteUP.full.md
meta_path: aliyunCTF_HappyTree_WriteUP.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: aliyunCTF HappyTree WriteUP。aliyunCTF HappyTree WriteUP：Solidity Merkle Tree 验证合约 b(leafs, proofs, indexs) 接收 3 个 leaf + 4 个 proof + 4 个 index，verify 通过 keccak256(abi.encodePacked(hash, proof)) 计算路...
category: web
subcategory: web_other
tools_used:
- Solidity
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/112421.html
reasoning_chain:
- 触发点:Solidity Greeter 合约 + b(leafs[], proofs[], indexs[]) 函数 → 假设:Merkle 路径验证 → 动作:分析 verify(proof, leaf, index)
- 动作:index%2==0 则 hash=keccak256(hash, proof) 否则 keccak256(proof, hash) → 观察:Merkle 验证算法
- 动作:used_leafs[leaf] 防止重放 + this.a(i, y) 调用 → 观察:防 replay 机制
- 动作:3 个 leaf (0x8137...cd6a, 0x28ca...79b6, 0x804c...31d) + 4 个 proofs + 4 个 indexs (0,1,2,4) + root 0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e → 观察:数据齐全
- 动作:verify(proofs, leaf, index) keccak256 abi.encodePacked 计算路径验证 == root → 观察:验证通过 → 完成
failed_attempts:
- 试图不解 Merkle Tree → 失败:必须 keccak256 abi.encodePacked 验证
- 试图用标准 Merkle → 失败:这题用 abi.encodePacked 不是标准 packed
- 试图重放 leaf → 失败:used_leafs 防重放
key_observations:
- Merkle Tree 在 CTF 区块链题中是验证批量 leaf 的标准结构
- keccak256(abi.encodePacked(hash, proof)) 是按 index 奇偶交换参数的 Merkle 验证算法
- used_leafs mapping 防重放是 Solidity 经典模式
- this.a(i, y) 调用 other contract 是 Solidity 跨合约调用
- Solidity 0.8.x 的 abi.encodePacked 不补 0 是细节
prerequisites:
- Solidity 智能合约基础 (mapping / require / keccak256)
- Merkle Tree 验证算法
- abi.encodePacked 编码规则
- Solidity 跨合约调用 (this.a())
---
# aliyunCTF HappyTree WriteUP

> 原文: https://www.ctfiot.com/112421.html
> ID: 112421


```
function b(
 bytes32[] calldata leafs,
 bytes32[][] calldata proofs,
 uint256[] calldata indexs
 ) public {
 require(leafs.length == proofs.length, "Greeter: length not equal");
 require(leafs.length == indexs.length, "Greeter: length not equal");

 for (uint256 i = 0; i < leafs.length; i++) {
 require(
 verify(proofs[i], leafs[i], indexs[i]),
 "Greeter: proof invalid"
 );
 require(used_leafs[leafs[i]] == false, "Greeter: leaf has be used");
 used_leafs[leafs[i]] = true;
 this.a(i, y);
 y++;
 }
 }
0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a
0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6
0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d
function verify(
 bytes32[] memory proof,
 bytes32 leaf,
 uint256 index
 ) internal view returns (bool) {
 bytes32 hash = leaf;

 for (uint256 i = 0; i < proof.length; i++) {
 bytes32 proofElement = proof[i];

 if (index % 2 == 0) {
 hash = keccak256(abi.encodePacked(hash, proofElement));
 } else {
 hash = keccak256(abi.encodePacked(proofElement, hash));
 }

 index = index / 2;
 }

 return hash == root;
 }
["0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a","0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6","0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d","0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e"]
[
["0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6", "0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486"],
["0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a","0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486"],
["0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d","0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e"],
["0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486"]
]
[0,1,2,4]
```
