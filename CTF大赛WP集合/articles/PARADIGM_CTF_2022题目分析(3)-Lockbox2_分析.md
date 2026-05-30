# PARADIGM CTF 2022题目分析(3)-Lockbox2 分析

> 原文: https://www.ctfiot.com/80187.html
> ID: 80187

首先其导入了一个合约，导入的lockbox2合约先暂时不管，然后setup的初始化函数是new了一个lockbox2合约，然后一个isSolved函数，这个函数view修饰，不上链，返回lockbox2合约的locked函数的返回值的非值，一个bool类型，看来拿到flag的前提是要让lockbox2的locked函数返回false。

进入lockbox2合约，如下图所示：

首先它定义了一个全局变量，bool类型locked，初始为true。然后是没有参数的solve函数。此函数首先声明了一个bool类型，长度为5的数组successes。下标从0到4分别对应5个返回值。继续看每一行，分别是调用当前合约的stage1-5函数，calldata数据为msg.data第4位开始。从第四位开始，也就是不算函数签名。然后把每个调用是否成功作为一个bool值赋给success数组。然后是一个循环遍历这个bool类型的数组，每个都是true的话，继续运行，把locked设置为false。只有solve这一个入口可以改变locked变量。看来关键问题就是solve函数的5个调用。

import randomfrom Crypto.Util.number import isPrime
from ecdsa import ecdsag = ecdsa.generator_secp256k1while True: private_key = random.randint(0, 1 << 256 - 1) public_key = private_key * g x = str(hex(public_key.x())[2:]) x = ("00" * 32 + x)[-32 * 2:] y = str(hex(public_key.y())[2:]) y = ("00" * 32 + y)[-32 * 2:]    public_key_hex = x + y if public_key_hex[:2] == "00": print(private_key, public_key_hex) break;

PUSH1 0x40DUP1PUSH1 0x06PUSH1 0x0CODECOPYPUSH1 0RETURN

emit log_bytes(: 0x890d6908)

000000000000000000000000000000000000000000000000000000000000006100000000000000000000000000000000000000000000000000000000000001010000000000000000000000000000000000000000000000000000000000000001

0000000000000000000000000000000000000000000000000000000000000061 000000000000000000000000000000000000000000000000000000000000000101 200000000000000000000000000000000000000000000000000000000000000001 400000000000000000000000000000000000000000000000000000000000000001 6000

409548


```
import randomfrom Crypto.Util.number import isPrime
from ecdsa import ecdsag = ecdsa.generator_secp256k1while True: private_key = random.randint(0, 1 << 256 - 1) public_key = private_key * g x = str(hex(public_key.x())[2:]) x = ("00" * 32 + x)[-32 * 2:] y = str(hex(public_key.y())[2:]) y = ("00" * 32 + y)[-32 * 2:]    public_key_hex = x + y if public_key_hex[:2] == "00": print(private_key, public_key_hex) break;
PUSH1 0x40DUP1PUSH1 0x06PUSH1 0x0CODECOPYPUSH1 0RETURN
emit log_bytes(: 0x890d6908)
000000000000000000000000000000000000000000000000000000000000006100000000000000000000000000000000000000000000000000000000000001010000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000061 000000000000000000000000000000000000000000000000000000000000000101 200000000000000000000000000000000000000000000000000000000000000001 400000000000000000000000000000000000000000000000000000000000000001 6000
409548
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669458194.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669458195.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669458196.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458196.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1669458197.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669458197.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669458198.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458198.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669458199.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669458199.png)