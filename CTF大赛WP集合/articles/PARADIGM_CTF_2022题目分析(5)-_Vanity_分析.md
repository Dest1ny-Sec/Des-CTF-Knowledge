# PARADIGM CTF 2022题目分析(5)- Vanity 分析

> 原文: https://www.ctfiot.com/80219.html
> ID: 80219

照例先看题目的setup合约：

创建了一个challenge合约，然后要拿到flag需要让challenge合约的bestScore这个方法的返回值大于等于16。

进入到challenge合约：

三个函数都是solve，函数可见性不一样。两个外部调用，一个private。先看第一个solve，没有参数，但是读取调用者地址(msg.sender)，然后调用内部的solve函数。内部的solve函数先暂时搁置，继续往下看第二个外部调用的solve。这个solve传入两个参数，一个地址，一个bytes字符串，这两个变量都外部可控，然后内部逻辑调用了一个库函数isValidSignatureNow，这个函数需要3个参数，两个是外部传入的变量，还有一个是hash常量。然后需要这个库函数返回true，才继续调用内部的solve。然后就是内部的solve，看到内部调用的solve函数只传入一个地址类型的数据，把这个地址转成 bytes20，然后遍历，如果当前字节是00，则score++，最后如果score>bestscore，则把score赋值给bestscore。看来关键点是这个判断，最后bestscore要>=16，即传入的这个地址的16个字节的内容都要是00。

首先排除第一个可以外部调用的solve，无法构造一个有16个字节都是0的地址并且让这个地址发起调用。所以主要就是第二个可外部调用的solve，这个函数的主要部分就是isValidSignatureNow，这个库函数的逻辑，由于篇幅问题，只粘贴可利用的代码部分。

进入到代码逻辑，参数是一个外部可控的地址，一个外部可控的bytes字符串，一个hash常量。

先把这个hash打出来：

bytes4 a= bytes4(keccak256("isValidSignature(bytes32,bytes)" ));

emit log_bytes4(tttt:
0x1626ba7e)

整个代码读完之后，有了大致的思路，因为其它函数调用经过分析都走不通，唯一这个staticcall的地方可以尝试。要一个地址有至少16个字节都是0，容易想到evm预编译。首先这个预编译合约它是不在链上的，这部分内容集成在每个节点上，因为调用频繁，所以不在链上计算，节约成本。 具体文档参照:
https://www.evm.codes/precompiled。首先这些个预编译合约的地址前面有很多0，满足条件，但是还需要找一个调用返回bytes32的。

dat=bytes.fromhex('1626ba7e'+ web3.codec.encode_abi(['bytes32','bytes' ],['19bb34e293bba96bf0xaeea54cdd3d2dad7fdf44cbea855173fa84534fcfb528', h]).hex())


```
bytes4 a= bytes4(keccak256("isValidSignature(bytes32,bytes)" ));
emit log_bytes4(tttt:
0x1626ba7e)
dat=bytes.fromhex('1626ba7e'+ web3.codec.encode_abi(['bytes32','bytes' ],['19bb34e293bba96bf0xaeea54cdd3d2dad7fdf44cbea855173fa84534fcfb528', h]).hex())
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1669458247.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669458248.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669458248.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669458250.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1669458250.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669458251.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1669458251.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669458252.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669458253.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669458254.png)