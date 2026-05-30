# PARADIGM CTF 2022题目分析(6)- Hint Finance

> 原文: https://www.ctfiot.com/80234.html
> ID: 80234

题目分析

照例先看setup合约，声明了1个数组，长度为3，里面3个代币(pnt,sand,amp)。还有一个数组，长度为3，表示每个vault的初始底层资产余额。new了一个工厂合约。工厂合约主要用来创建vault合约。然后是初始化函数，声明了一个uniswap合约，并有一个swapExactETHForTokens接口。接下来是一个循环，遍历这3个代币，兑换路径分别是eth到这3个token，然后每个兑换价值为10eth的token，分别存到对应的vault合约，记录一下此时的vault合约余额，并保存在一个数组里。最后是solve函数，看到要使这个solve函数返回true，需要让每个vault合约当前的余额小于初始余额的百分之一。看来是需要找个方法把vault合约的钱搞走，题意大概明确了。

接下来开始细看vault合约和factory合约这两个。

Vault合约篇幅太长，只截取了关键函数。

factory没有利用空间，他的主要作用是传入一个底层资产并创建一个合约，然后就是vault合约。vault合约主要是存取和闪电贷功能，大致一看好像也是没啥利用空间。因为题目环境是fork以太坊的，题目给出的合约文件暂时没看出来问题，决定先看看题目给的这3个代币。了解到token1和token3是erc777代币，token2是erc20，但是有魔改。erc777有个特性，合约和普通地址都可以通过ERC1820Registry合约的setInterfaceImplementer注册一个方法。这个方法相当于一个钩子，本质上就是回调函数，当调用代币的转账功能时，它会回调调用者的tokensReceived函数。本质上和重入一样，猜测题目是不是想让利用重入。然后仔细分析一下deposit和withdraw函数。ERC777具体详见(https://eips.ethereum.org/EIPS/eip-777, https://eips.ethereum.org/EIPS/eip1820)。

关注这两行代码，首先bal是动态获取的。然后看到withdraw函数发生转账之后再计算totalSupply。有了思路，可以在withdraw的时候重入，重新调用deposit函数，此时bal变小，因为已经发生转账，而且bal是动态获取的，totalSupply由于发生在transfer之后，所以重入到deposit之后是没变的，所以totalSupply/bal变大，获得的份额会变大。思路可行，在withdraw的时候重入进入deposit，然后来回几次之后，就可以占据vault合约中大部分的份额，之后取出份额，提走相应的代币，token1和token3问题解决。token1和token3同理，只贴出一个代码。部分exp代码如下：

首先需要自定义hook函数，所以先去erc1820合约中去注册，传入from和to地址和函数hash，调用setinterfaceimplementer函数。这个函数设定from，to，在接收转账交易的时候去回调的函数，才可以完成在withdraw的时候重新进入在没改变totalsupply值的情况下进入deposit，这样来回几次之后，池子中攻击合约占用的份额变大，最终完成攻击。

还有一个部分是token2，token2是sand代币。这个代币是魔改的erc20，有了上边的思路，怀疑是不是需要用到代币合约的原生方法配合题目合约完成攻击。代币合约有一个approveAndCall函数，vault合约的flashloan函数里面的回调函数和onHintFinanceFlashloan具有相同的函数签名。可参照下面函数签名链接：

https://www.4byte.directory/signatures/?bytes4_signature=0xcae9ca51

有一个大致思路，能否让vault合约给攻击合约进行代币授权，即approve操作，然后调用transferfrom函数把vault合约的代币转走。首先需要伪造一个代币合约，在代币合约里面执行approveandcall：

这个函数有3个参数，并且有一个判断，doFirstParamEqualsAddress，这个函数要求从data里面取address，取的是除函数签名的第一个数据。要求msg.sender和取出来的地址一样。所以需要构造一个data数据。首先要明确谁给谁approve，最终目的是需要让vault合约给攻击合约approve，所以最后这个approveandcall的调用者是vault合约，传的参数是攻击合约地址。因为flashloan里的回调函数和approveandcall同函数签名，而且回调的调用者正是vault合约，满足所有条件。然后还需要构造外面的这个approveandcall，使用嵌套approveandcall的调用，因为approveandcall和闪电贷的回调函数具有相同的函数签名，所以第一层approveandcall进入之后，进入闪电贷的回调，实际是调用第二个approveandcall，这一层完成vault合约对攻击合约的代币授权。 然后看一下里面的这个回调函数，需要构造这个data。

因为approveandcall和上述函数具有相同的函数签名，所以这个回调就变成了去token3代币合约中调用approveandcall。因为这个data是透传过来的，而且需要让两个不同函数的参数经过abi编码之后都匹配，所以需要对data进行构造，即这个data要同时满足onHintFinanceFlashloan和approveAndCall。

注意一下data的偏移量并保证data数据合法就行，甚至可以空调用。(0xa0就是data的偏移量，要告诉函数calldata数据从内存的a0开始找，因为bytes不定长，所以先存个长度。)

如上述，就可以构造出一系列调用，通过aproveandcall进入flashloan，然后进入闪电贷的回调函数，实际是进入sand token的approveandcall(因为相同的函数签名，只需要构造同时符合两个函数的abi编码之后的参数)。再次进入approveandcall，这时调用者是vault，授权的对象是伪造的token，即攻击合约，之后调用transferfrom转走，完成对token2的攻击。

具体代码段：

最后打印一下3个函数调用之后，vault合约的余额变化。

前后余额已经发生改变，false已经变为true，已经具备拿到flag的条件。

总结

对于以太坊重入问题，必须要谨慎处理，虽然是erc类型代币，但对于不受控制的外部回调函数要格外注意，在逻辑允许的情况下，转账操作要放到所有计算的最后执行。本题运用了erc777的重入和函数签名的碰撞，完成攻击，要是考虑重入漏洞，不能只简单想到以太坊的经典重入，所有的外部回调在某些特定场景下同样能造成极大危害。

Numen 导航

Numen 官网

https://www.numencyber.com/

GitHub

https://github.com/NumenCyber

Twitter

https://twitter.com/@numencyber

Medium

https://medium.com/@numencyberlabs

LinkedIn

https://www.linkedin.com/company/numencyber/

原文始发于微信公众号（Numen Cyber Labs）：PARADIGM CTF 2022题目分析(6)- Hint Finance

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669458269.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669458271.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1669458273.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669458275.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669458275.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669458276.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1669458278.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669458279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1669458280.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669458280.png)