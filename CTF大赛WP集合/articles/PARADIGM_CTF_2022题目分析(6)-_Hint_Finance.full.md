---
title: PARADIGM CTF 2022/Hint Finance
contest: PARADIGM CTF
year: 2022
difficulty: hard
vuln_type:
- logic
tags:
- 以太坊
- Solidity
- ERC777 重入
- ERC1820Registry 钩子
- 闪电贷
- 函数签名碰撞
- '0xcae9ca51'
- approveAndCall
- 嵌套调用
attack_chain:
- 题目给 vault + factory + 3 个 token 合约（token1/3 是 ERC777，token2 是魔改 ERC20）
- 目标：让每个 vault 余额 < 初始 1%
- ERC777 通过 ERC1820Registry 注册 tokensReceived 钩子 → 跟经典重入一样
- withdraw 时已转账但 totalSupply 未更新 → 重新进入 deposit 增大份额占比
- 多次 withdraw+deposit 占据大部分份额后提走 → token1/3 解决
- token2（魔改 ERC20）有 approveAndCall 函数签名 (0xcae9ca51) 跟 flashloan 回调同签名
- 构造 data 双重满足 onHintFinanceFlashloan 和 approveAndCall
- 嵌套 approveAndCall → flashloan → approveAndCall 实现 vault 给攻击合约 approve
- 再 transferFrom 转走 token2
- 3 个 token 都被盗空 → 满足 vault < 1% 初始 → 拿 flag
key_payload: register ERC1820 hook for from/to → withdraw → reenter deposit → loop
one_liner: ERC777 重入 + 函数签名碰撞嵌套 approveAndCall 转走 vault 全部代币
lesson: 任何外部回调（不只是 ETH transfer）都可能造成重入；函数签名碰撞可用于跨合约调用伪装
quality: high
full_path: PARADIGM_CTF_2022题目分析(6)-_Hint_Finance.full.md
meta_path: PARADIGM_CTF_2022题目分析(6)-_Hint_Finance.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: PARADIGM CTF 2022/Hint Finance。ERC777 重入 + 函数签名碰撞嵌套 approveAndCall 转走 vault 全部代币。关键路径：题目给 vault + factory + 3 个 token 合约（token1/3 是 ERC777，token2 是魔改 ERC20） → 目标：让每个 vault 余额 < 初始 1% → ERC777 通过 ER...
category: web
subcategory: logic
tools_used:
- Solidity
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/80234.html
reasoning_chain:
- 触发点:vault + factory + 3 个 token(token1/3 ERC777,token2 魔改 ERC20) → 假设:ERC777 钩子可重入
- 目标:vault 余额 < 初始 1% → 假设:必须把 vault 代币全部盗走
- ERC777 通过 ERC1820Registry 注册 tokensReceived 钩子 → 假设:跟经典 ETH 重入一样 → 动作:注册攻击合约实现 tokensToSend/tokensReceived
- withdraw 时已 transfer 但 totalSupply 未更新 → 重入 deposit 增大份额占比 → 多次 withdraw+deposit 占比接近 100% → 提取走光 token1/3
- token2 有 approveAndCall 0xcae9ca51 跟 flashloan 回调同签名 → 假设:函数签名碰撞可串联调用
- 动作:构造 data 同时满足 onHintFinanceFlashloan 和 approveAndCall → 嵌套 approveAndCall → flashloan → approveAndCall → vault 给攻击合约 approve
- 动作:transferFrom 转走 vault token2 余额 → 3 个 token 都耗光 → isSolved 返回 true
failed_attempts:
- 试图用普通 ERC20 transferFrom 转 token1/3 → 失败:ERC777 重入需要先注册 hooksToSend/hooksToReceive
- 试图直接调 flashloan 不签名碰撞 → 失败:回调签名 0xcae9ca51 与 approveAndCall 不兼容
- 试图只重入一次提走 → 失败:占比不够大,只能提走一部分
key_observations:
- ERC777 重入攻击面与 ETH transfer 一致,hooksToSend 在 transfer 前回调
- Solidity 函数签名碰撞:不同函数 keccak256(签名) 前 4 字节相同即可串联
- approveAndCall 0xcae9ca51 模式允许一个调用同时满足两个合约的预期
prerequisites:
- ERC777 与 ERC1820Registry 钩子机制
- Solidity 函数选择器 keccak256 计算
- DeFi 重入攻击与闪电贷原理
---
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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]