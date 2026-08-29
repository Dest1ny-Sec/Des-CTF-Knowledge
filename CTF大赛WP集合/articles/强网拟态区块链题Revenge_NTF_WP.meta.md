---
title: 强网拟态区块链 Revenge NTF - NFT Market CouponVerifierBeta ECDSA签名
contest: 第五届强网拟态防御国际精英挑战赛
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Solidity, NFT_Market, ERC721, ERC20, OpenZeppelin, CouponVerifierBeta, ECDSA, ecrecover, abi.encode, signed_coupon, fakeNFT, orderId_reuse, Airdrop, 0.8.16]
attack_chain: 部署CtfMarket+3个NFT(1/2/3)+CtfToken+CouponVerifierBeta → airdrop领5 token → 部署FakeNFT合约实现ownerOf返回market地址(绕过) → 部署Attacker合约实现onERC721Received返回正确selector → purchaseTest绕过:tested=true + createOrder(nftAddress,tokenId,price) + approve + purchaseOrder → purchaseWithCoupon:伪造SignedCoupon(orderId=0,newprice=1,issuer=market,user=attacker,reason) + ECDSA签名"because"+abi.encode("I, the issuer"+issuer+offer+user+order+at+newprice+because+reason) → win:要求ctfNFT.ownerOf(1/2/3)==msg.sender
key_payload: FakeNFT.ownerOf返回market地址 + purchaseTest+tested复用 + CouponVerifierBeta ECDSA ecrecover
one_liner: 强网拟态NFT Market Revenge:伪造NFT合约ownerOf返回market+purchaseTest绕过+CouponVerifierBeta ECDSA签名。
lesson: NFT Market常见漏洞:FakeNFT合约实现ownerOf返回指定地址绕过isNFTApprovedOrOwner;tested标志一次写入后可绕过purchaseTest复用;CtfMarket.deleted=orders[orderId]=orders[last]+pop但index 0被删后newOrderId=0;CouponVerifierBeta的abi.encode含"because"+reason字段可ECDSA签名伪造。
quality: high
---
