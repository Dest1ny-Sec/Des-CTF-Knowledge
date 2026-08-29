---
title: 0CTF/TCTF 2022 NFT Market (Solidity 0.8.15 calldata bug)
contest: 0CTF/TCTF 2022
year: 2022
difficulty: hard
vuln_type: [logic, web_unknown]
tags: [Solidity, 0.8.15, calldata-tuple-head-overflow, ERC721, ERC20, reentrancy, view-function, ABI-reencoding, Foundry]
attack_chain: ["目标：拿到 3 个 NFT（id=1, 2, 3）触发 win() emit SendFlag()", "Part 1: purchaseTest + approve 钩子 — 注册 FakeNFT，在 approve 回调里把 NFT 转给 USER，让 purchaseOrder 给 USER 转账", "Part 2: Solidity 0.8.15 calldata tuple head overflow bug — abi.encode 转发 SignedCoupon 时 orderId 被覆盖", "攻击者构造 orderId=1 的 coupon，但 verifyCoupon 内取 order[0]（自己控制的）", "Part 3: 综合：airdrop 5 → purchaseTest 拿 1337 → buy #2 → mint FakeNFT 上架 → buy #1 把 own 单变 order[0] → coupon 买 #3"]
key_payload: "abi.encode(\"I, the issuer\", issuer, \"offer a special discount for\", user, \"to buy\", order, \"at\", newprice, \"because\", reason)"
one_liner: Solidity 0.8.15 calldata tuple head overflow + 数组 swap 删除 + approve 钩子
lesson: Solidity 编译器 bug 是 web3 CTF 高级考点；upgradeable 数组 swap 删除要小心 order 变化被利用
quality: high
---

# 0CTF/TCTF 2022 NFT Market (Solidity 0.8.15 calldata bug)

原文 https://www.ctfiot.com/58223.html （rkm0959 原作 / GitHub）

## 目标
- 拿到 NFT id=1, 2, 3 → 触发 `win()` emit SendFlag
- NFT 1 = 1 token，NFT 2 = 1337 tokens，NFT 3 = 13333333337 tokens（天价）

## 关键漏洞

### Part 1: approve 钩子偷币
```solidity
function approve(address dest, uint256 tokenId) public override {
    if (approved == 0) {
        super.safeTransferFrom(msg.sender, USER, 1);  // 把 NFT 转给 USER
    } else {
        super.approve(dest, tokenId);
    }
    approved += 1;
}
```
- 注册 FakeNFT，mint 给 TctfMarket
- `purchaseTest(fakeNFT, 1, 1337)`：
  - createOrder → NFT 1 价格为 1337
  - approve 触发 → safeTransferFrom 把 NFT 转给 USER
  - purchaseOrder → 给 NFT 的 owner（现在是 USER）转 1337 tokens

### Part 2: Solidity 0.8.15 calldata tuple head overflow
- 博客：https://blog.soliditylang.org/2022/08/08/calldata-tuple-reencoding-head-overflow-bug/
- Bug 触发条件：
  1. 最后组件是静态大小数组（这里是 `bytes32[2]`）
  2. 有动态组件（这里是 `bytes`）
  3. 合约直接转发 calldata 到另一个 external call
- 攻击效果：`orderId` 字段被清零（偏移 32 字节）

```solidity
// SignedCoupon 直接转发到 verifyCoupon
function verifyCoupon(SignedCoupon calldata scoupon) public {
    // abi.encode 时 head overflow，orderId 实际为 0 而不是 1
}
```

### Part 3: 综合攻击
1. `token.airdrop()` 拿 5 tokens
2. `purchaseTest(fakeNFT, 1, 1337)` → 偷 1337 tokens（approve 钩子）
3. 用 1337 + 5 = 1342 tokens 买 NFT #2
4. mint FakeNFT #2 → 自己上架 1 token
5. 用 1 token 买 NFT #1（order 数组 [#1, #3] 变 [us, #3]）
6. 现在 order[0] = 自己控制的 NFT，可签 coupon
7. 构造 coupon orderId=1 newprice=1，**因 bug 实际生效 orderId=0**
8. 签自己的 coupon → purchaseWithCoupon → 拿 NFT #3
9. 调 `win()` 拿 flag

## 教学价值
- **Solidity 编译器 bug** 是 web3 CTF 高级考点（0.8.15 → 0.8.16 修复）
- **数组 swap 删除**（`orders[i] = orders[last]; pop()`）会让 order ID 不稳定，被攻击者利用
- **approve 回调** 在 ERC721 是可重入点，必须用 `isApprovedForAll` / `getApproved` 验证
- **view 函数** 也可能被 reentrancy 攻击（虽然 staticcall，但仍能在外部合约中改 storage）
- **Foundry** 是 web3 CTF 必会工具

## 参考
- rkm0959: https://github.com/rkm0959/I_will_never_forget_you/blob/main/0ctf2022/nftmarket.md
- Solidity bug blog: https://blog.soliditylang.org/2022/08/08/calldata-tuple-reencoding-head-overflow-bug/
