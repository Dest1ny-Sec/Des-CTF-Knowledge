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
```



```
0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a
0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6
0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d
```



```
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
```



```
["0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a","0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6","0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d","0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e"]
[
["0x28cac318a86c8a0a6a9156c2dba2c8c2363677ba0514ef616592d81557e679b6", "0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486"],
["0x81376b9868b292a46a1c486d344e427a3088657fda629b5f4a647822d329cd6a","0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486"],
["0x804cd8981ad63027eb1d4a7e3ac449d0685f3660d6d8b1288eb12d345ca2331d","0x9b1a0a45cfdc60f45820808958c1895d44da61c8f804f5560020a373b23ad51e"],
["0x4a35f5bda2916fbfac6936f63313cee16979995b2409de59ceda0377bae8c486"]
]
[0,1,2,4]
```
