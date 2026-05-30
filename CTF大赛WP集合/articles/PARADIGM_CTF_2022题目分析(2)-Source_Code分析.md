# PARADIGM CTF 2022题目分析(2)-Source Code分析

> 原文: https://www.ctfiot.com/80201.html
> ID: 80201

紧接上篇关于resuce的分析， 本文我们一起来探讨一下source code。

先分析setup，如图1，拿到flag的前提是isSolved返回true。然后分析challenge合约，challenge合约主要有两个函数 solve和safe，如图2所示。先看solve函数，我们想让setup合约的isSolved函数返回true，我们就必须更改变量solved，更改solved的唯一方法就是调用solve函数，继续分析solve函数。solve函数传入一个bytes类型的变量，首先校验长度不为0，然后调用safe函数，我们看到safe函数的参数是solve函数传入的code，然后safe函数会返回一个bool，我们要想继续运行，必须使safe函数返回true。safe函数内容等会再分析，继续往下看，用传入的code作为参数，直接new一个新合约，new的时候会调用这个合约的初始化函数(constructor)。然后staticcall(静态调用)这个新合约，两个返回值，一个bool表示是否调用成功，一个bytes类型的result，表示返回数据。最后一个判断，要求staticcall调用成功并且返回数据(无论怎么call,evm都是这个返回)和合约的bytecode一致。

以上判断通过之后，solved变为true。看到这儿，感觉想让合约的bytecode和调用返回一样有很多方法，但是应该不会这么简单，中间有一个关键的safe函数，如图3所示：

跟进safe的逻辑，safe函数通过遍历传入的bytes类型的字符串，禁用一些操作码，如果匹配到禁用的操作码，直接返回false。如果要safe函数返回true，我们传入的操作码必须要在safe函数定义的“白名单”中。之后，用code作为参数new一个合约，最后一个判断，要求合约的bytecode和对这个合约任意调用的返回结果(无论怎么call,evm都是这个返回)一致。完成以上所有require判断，即可更改solved，拿到falg。要求合约的sourcecode和合约的调用返回值一致。

其实我们有很多方式满足这一条件，CODECOPY，CALLCODE，CALL很多方式都能实现合约代码和调用返回一致，但是这些操作码都在safe合约的“黑名单”中。所以要思考别的途径。大致思路是我们尝试构造一系列操作执行指令，然后我们push这个数据，然后执行这个数据的指令，这个数据的指令内容就是利用dup1，mstore，return这些来操作栈里的内容，并返回(我们第一步已经把一系列操作指令当作参数入栈)，关键操作就是dup1，需要把操作指令当参数push一次，代码中并要执行一次，所以调用的返回中需要出现两次，所以要用dup1进行复制一次。针对mstore类型指令，只有mstore8和mstore,一个是存1字节，一个是存32字节。1字节肯定不够用，32可能用不完，我们可以后面补0(利用stop)，所以一开始push的指令长度必须要32字节，如果短的话mstore存储之后会在高位补0，到时候肯定会影响return的返回。

PUSH32 0x80607f60005360015260215260416000f3000000000000000000000000000000DUP1PUSH1 0x7fPUSH1 0x00MSTORE8PUSH1 0x01MSTOREPUSH1 0x21MSTOREPUSH1 0x41PUSH1 0x00RETURNSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOP

把一个32字节的内容入栈，并且复制一次(取栈顶的数据复制)，所以栈内2个元素，都是指令数据的内容。DUP1很关键，我们需要复制指令数据的内容做输出。 初始指令PUSH32，对应bytecode是7f，所以构造7f。把7f入栈，存00位置，占用1字节，只能使用mstore8，前面提到过如果使用mstore，它会高位补0，补齐32位，影响return返回。剩余都是指令数据中的操作。这时栈里还有两个元素都是指令数据的内容，把栈顶的存到位置01，一个数据占用32字节，然后还剩1个，把这个存到位置21(32字节，所以01+20=21，16进制)。最后return，从0开始返回，一个1字节的数据和两个32字节的数据，一共长度0x41，stop对应补0。所以返回了1个7f和两个指令数据的内容，达到和代码的内容一致(代码：push了一个32字节数据，把指令数据当参数硬编码了一次，然后执行了指令数据的内容，所以也是1个7f和两个指令数据的内容)。

灵活运用dup，这个问题的关键点在于dup，这个操作码有dup1-16。分别是从栈顶开始数，复制当前位置的元素。正是使用dup操作，省去了push操作，才能做到使合约的bytecode和合约的调用返回一致。


```
PUSH32 0x80607f60005360015260215260416000f3000000000000000000000000000000DUP1PUSH1 0x7fPUSH1 0x00MSTORE8PUSH1 0x01MSTOREPUSH1 0x21MSTOREPUSH1 0x41PUSH1 0x00RETURNSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOPSTOP
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669458213.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669458215.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458217.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1669458219.png)