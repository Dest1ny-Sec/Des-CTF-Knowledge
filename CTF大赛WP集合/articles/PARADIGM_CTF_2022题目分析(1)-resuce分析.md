# PARADIGM  CTF 2022题目分析(1)-resuce分析

> 原文: https://www.ctfiot.com/80208.html
> ID: 80208

今年的PARADIGM CTF比赛于北京时间2022年8月20日早晨8点开始至2022年8月22日早晨8时结束，共计两天时间。其中陆续总共给出了23道题，共有400多个队伍参加了这个比赛。是一个比较热闹并且具有挑战性的区块链安全CTF比赛，吸引了全球很多顶尖的区块链安全人员参加，因为其题目具有一定的难度，想拿到Flag也并非易事。

什么是CTF？

CTF是一种流行的信息安全竞赛形式，其英文名可直译为“夺得Flag”，也可意译为“夺旗赛”。其大致流程是，参赛团队之间通过进行攻防对抗、程序分析等形式，率先从主办方给出的比赛环境中得到一串具有一定格式的字符串或其他内容，并将其提交给主办方，从而夺得分数。为了方便称呼，我们把这样的内容称之为“Flag”.

NUMEN CYBER 实验室将就今年的比赛题目陆续推出分析文章，敬请期待。本文首先对其中rescue一题一起讨论一下题目分析，解题技巧和思路。

题目分析：

1. MasterChefHelper.sol合约

分析：这个合约可以外部调用的主要功能接口就只有swapTokenForPoolToken函数。

poolId：是查询MasterChef合约中pool对应的uniswap哪个pair地址。

tokenIn:
是转入合约中兑换代币的地址。

amountIn：是用户需要兑换的数量。

minAmountOut：获得lp的最小数量，可填0。

函数的主要功能是将用户转入代币的一半兑换成指定pair合约中的token0, 再将另一半兑换为token1,然后两者按比例一起添加到pair中获得流动性。

2. Setup.sol合约

分析：Setup合约在创建的时候先抵押了10ETH，获取了10 WETH并且将10个WETH转移到了mcHelper合约中。

题目的要求是怎么将mcHelper合约下的10个WETH转走。

解题分析：

想解开这道题，我们唯一可以调用的函数就只有MasterChefHelper.sol合约中的swapTokenForPoolToken函数，所以可以重点从这里寻找问题所在，我们发现在添加流动性的时候，会将合约下的两种币一起添加，当前合约下有10个WETH，我们可以想办法再获取另一种等比例的代币放到合约下来，是不是就可以解开此题。（注意，想要把这个函数调用成功，首先传入的tokenIn不能等于pair合约中对应的token0和token1）。

(1) 我们自己创建一个攻击合约，最开始我们的账户里面有一定数量的ETH，我们可以转一部分到攻击合约中，这时候调用uniswap的兑换函数去兑换与传入poolId对应pair中两种代币的不同的代币，这里小编兑换的是USDT。

(2) 因为mcHelper合约中存在10WETH，我们查询 poolId传入2后对应的pair中token0和token1分别是DAI和WETH,这时我们如果想把合约下的10个WETH一起添加走，我们就需要再兑换10个WETH对应的DAI转入mcHelper合约中，在这里小编换了20个，为了防止不够。

(3) 最后调用mcHelper合约中的swapTokenForPoolToken函数就可以解开此题，相当于10个ETH的USDT换了价值5ETH的WETH和价值5个ETH的DAI，再加上转入的20个ETH的DAI，就可以把合约下的之前的10个WETH一起按比例添加到pair中获得流动性，多余的DAI会留在合约中。

踩坑点：

①　第一次解题时，小编没有进行第二步操作，因为合约中添加流动性时是把合约下所有代币全部添加，小编以为直接就全部添加了，但uniswap的机制是按比例添加，WETH还是留在合约中。

②　你初始账户的ETH是可以灵活使用的，如果不去灵活兑换的话，也不容易解开此题。

Poc代码:

以下是小编本次poc主要的逻辑代码，如果有更好的解题方式，也希望大家能与NUMEN实验室进行交流，我们愿与大家一起努力。

总结：

本次CTF题目也是具有一定的难度和挑战性，NUMEN实验室也会继续对其进行研究和探索，守护区块链安全义不容辞，也希望能在每次研究和探索中进步和升华。

原文始发于微信公众号（Numen Cyber Labs）：PARADIGM CTF 2022题目分析(1)-resuce分析

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458230.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669458230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669458232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669458233.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669458233.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458233.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669458234.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669458235.png)