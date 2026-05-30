# 2022 祥云杯 Misc super_electric WriteUp

> 原文: https://www.ctfiot.com/68853.html
> ID: 68853

拿到题目，是个流量分析题，先看下流量分布。

可以看出来，IPv4-TCP-MMS几乎占了绝大部分，而其他的协议占比也没有超出合理范围，那么这个流量包是让分析MMS协议基本上是板上钉钉的事了。

> mms协议主要应用在工控领域，属于是专业对口了。

那就筛选一下mms。

发现从头到尾都有好多的confirmed-RequestPDU（这个消息类型的过滤器是mms.confirmedServiceRequest），而其他的几个消息类型又一般是没啥用的那种（用mms && !mms.confirmedServiceRequest过滤后可以看出确实没啥有用信息）。

> mms协议主要有initiate-RequestPDU、confirmed-RequestPDU、initiate-ResponsePDU、confirmed-ResponsePDU四种消息类型，其中confirmed-RequestPDU相对来说比较重要。

那就过滤一下mms.confirmedServiceRequest呗。

发现除了开头那条是LLN0$CO$FunEna1$SBOw，后续不是LLN0$CO$FunEna2$Oper就是LLN0$CO$FunEna1$Oper，那目标已经很明确了，肯定是后两者咯。

先是mms.itemId == “LLN0$CO$FunEna2$Oper”看了下，发现从头到尾一直在传同一个值：172.20.1.23。

所以LLN0$CO$FunEna2$Oper大概是没啥用了，那就去看LLN0$CO$FunEna1$Oper呗。

这熟悉的4d5a9000开头，这不exe吗？那就tshark提取一下呗（还是老老实实用cmd跑tshark比较好，pwsh不知道为啥一直会报tshark: “$” was unexpected in this context.）。

tshark -r .super_electric.pcapng -Y "mms.itemId == "LLN0$CO$FunEna1$Oper"" -T fields -e "mms.octet_string" &gt; data.txt

提取结果是hex的：

那么写个脚本输出成exe吧。

data = b""with open('data.txt', 'r') as f:    for line in f:        data += bytes.fromhex(line.strip())with open("test.exe", 'wb') as f:    f.write(data)

那就开始逆向呗。

打开发现有窗口，那就找一下文本先。

发现有反调试相关函数名，不过应该问题不大，先去看看crackme那块有啥调用吧。

应该是在创建窗口或者应用啥的，那么上面的sub_43CB50应该就是主函数了，跟过去看看。

有个aC96f278c370c43常量，好像上面看字符串的时候见过，跟回去看看附近还有没有啥。

有一堆不知道是啥的常量，直接A一下发现就是窗口上的各种文本和消息。（有些文本被ida解析成函数了，需要U一下然后A）

那就回去看看哪里触发了那个恭喜。

所以关键还是那个C96F278C370C43299F1EE98257CCBD8A，只不过这边dword_449CB0函数没解析出来是啥，过去看看定义发现应该是Win32 Api。

那就x32dbg调试一下看看，因为这玩意我记得能识别Win32 Api。

到调用点43ccbd看看，发现这个函数其实是memcmp。

那有没有可能，输入的就是这一串，因为上面没见到啥复杂的处理逻辑或者其他调用。

于是输入了看看，发现确实是。

但是点确定之后就退出了，有点离谱…

于是命令行启动看看，猜测会不会是在STDOUT输出了东西。

结果输入完点确定后发现，根本不是正常退出，是异常了…

去看了下系统日志，是VC14翻车了，啥情况啊。然后想起来之前打绿城杯线下有一题也是这个类似的情况（不过那题不是VC14翻的，但是都是最后环节过几秒钟异常）。

绿城杯那题是因为作者写了个按条件触发的自解压的壳，然后因为我电脑环境问题好像触发了空指针。这题也是触发了空指针，难道这题也是自己写的壳？结合上面pdb路径里面带了个upacker，感觉真有可能。

不过当时为了保险起见，这种出现了异常的情况，肯定是先问问赛务比较靠谱。

结果赛务这回答，当时刚开始觉得好有道理，然后管理员运行、兼容性运行都给试了一遍，还是问题依旧。

然后突然醒悟，这回答不是命令行逆向题的标准回答吗？把我当小白了…赛务果然不靠谱。

然后后来我又小怼了一下，看出来回复确实才变成出题人的回复了。

但是看这意思是，出题人觉得正常情况下，点完确认是可以到下一阶段开始命令行交互的，然后大概会有在STDOUT写东西然后马上关闭？

那我这属于是环境问题导致完全不知道有下一阶段呗…搁这耽误了快两个小时是真离谱。

算了算了，确认有壳就行，找脱壳点吧。回到上面那个恭喜逻辑。

相比于没输入正确，多了个调用，那就去x32dbg看看是啥函数的调用。

是个SendMessageA，然后消息是16，这不是WM_CLOSE嘛…

那看来这个窗口应该是没啥脱壳逻辑了，往上追调用堆栈看看后续有没有吧。

然后一路追直接到了start函数。

其中sub_43CD50是创建窗体的函数，那么下面还一堆内存处理的，咋看咋像脱壳，然后最后有个内存块当函数调用的，就更像是脱壳完后的入口地址了。

于是懒得看脱壳逻辑了，直接跑到最后这个调用点43d4a6然后Scylla一键脱了吧。

结果压根没跑到这个地方，触发啥异常了，应该是哪个地方有反调试插桩。那就从sub_43CD50的调用结束后下个断点然后单步跟呗。

结果连sub_43CD50还没结束就触发反调试了。

那就只能把这个异常给过滤掉了。

然后发现在调用43d2a0会触发另一个异常。

上ida一看，发现是个反调试，直接nop。

然后跟过去发现真有代码。

直接Scylla一把梭。

不过无论是dump后的还是修复后的都依旧跑不起来，感觉还是踩到那个环境问题了。

不过无所谓，ida直接找到了真实的main函数，这就方便多了。

似乎是需要输入什么东西然后异或0x89后和byte_42D624比较，但是这个输入的后续就没有使用了，而且咱们跑不起来，也就无所谓需要输入啥了，反正没地方输入。

然后下面开始循环异或下标，范围是[0, 717)，那就写个脚本看看这里解出来的结果是啥。

b = bytearray(bytes.fromhex("66736D6E2446747E787D65254F647E677563327A796579656C395B5E4F177772504E505704474F49495A494245274742405E4047145D574450555359365B4C502D612A2B2C652F2A3826383F6C2B222E375B332027302423783F363A3B06646A3D415F5E4442000B090E114C4C0C000B50171E12132E5B4642245A46415D5902A78BE9E6FDA5BBA7EAAEBEEFB5ECB9BFA0A1A3A3A0A6A1BDB2B3BD91F0BDA3BFCCC4CC8BCFC0DF8EA2C4CFD8DFCCC9CA908C92D193F1D997C1D6CF9BD9CBDBCDE0A7A7A6A8E9E6A1ADACA6EBBFA2EEBFB1A1B7A1F4A1BEBEB6F5FA97B5B6BBFF81C18A8C919683C7878FCA888D9F8A9CDCD1BD9D91D5949B978EDA9D8E9293DF6360746A6A62266E662E2A202C6F67617162717A7D3B6379707C6277757B67374840514B484C44095B414B19191B064455481B1D5C504E53515E5F48481517161B7B7373194F2F3168746A2D202C2914656B7F62095F3B322B2A3B3C397D637F0D041110050203474349081218081D47581D525E5419131950141F080F1C191AA9A1A7A3E8ACA6ADA8EAE2F9A4E1AEA2B0FDF7FDBCF8F3E4EBF8FDFEB5BDBBBFCC888E83C1CBC5C8CCC0C4CC8C908E88C5C5D49E8C929FBDD9DCC99B819DFFFA93EFACA6B3EDADA2B1E5EA8A899EE0829F95978C979795FBF8B0ACF2D6ADACB68E95CA818D8B87948B8083C58488968399978BDB959085D99D979989858D8AD76D6471706562632E21200028262724253A3B38393E3F3C3D32333031363734350A0B08090E0F0C0D02030001060704051A1B18191E1F1C1D12131011161714156A6B68696E6F6C6D62636061666764657A7B78797E7F7C7D72737071767774754A4B48494E4F4C4D42434041464744455A5B58595E5F5C5D5253505156575455AAABA8A9AEAFACADA2A3A0A1A6A7A4A5BABBB8B9BEBFBCBDB2B3B0B1B6B7B4B58A8B91C5C6C49093C9CD9DC99B95989886D4868580868F828980838F8E898D8FF2A3F0F2A6F7A4F6FFADA8F9C6"))for i in range(len(b)):    b[i] = 0xff & (b[i] ^ i)print(b)

发现蹦出来个python代码，这就是上面说的You Got it!nNow, try to resolve this crypto…n？这套娃…

这已知key高位，然后key又被sha256了一波扔到m结尾去了，然后message = message + bytes((l – len(message) % l) * chr(l – len(message) % l), encoding = ‘utf-8’)就是padding操作，最后flag当成iv用，加密结果只告诉了低位。

这就是ezAES这题改的。

所以咱就按照这个wp的思路来。

首先AES/CBC/PKCS7Padding的特性有：

1.分段加密，每段16字节，上一段的加密结果会当作下一段的iv去使用

2.用来填充的数据每字节内容和其长度相等，如01、0202、030303这种

那么咱们就可以将加密结果的最后16字节和倒数第二个16字节取出来，即78676e464395199424302b21b2b17db2和**********************3fba64ad7b。

然后将**********************3fba64ad7b当成iv去解密78676e464395199424302b21b2b17db2，至于key，爆破就完事。

至于爆破是否正确的判断，当然是利用padding特性了，根据题目的加密脚本我们可以知道m的长度是84+10=94，也就是说需要填充0202，那咱们拿上面wp里的脚本改改就行：

import binasciifrom Crypto.Cipher import AESdef decrypt(message, passphrase, iv):    aes = AES.new(passphrase, AES.MODE_CBC, iv)    return aes.decrypt(message)def find_key():    keytmp = '4d9a700010437{}{}{}'    for c1 in "0123456789abcdef":        for c2 in"0123456789abcdef":            for c3 in "0123456789abcdef":                tmp = decrypt(                    binascii.unhexlify('78676e464395199424302b21b2b17db2'),                    keytmp.format(c1, c2, c3).encode('utf8'),                    binascii.unhexlify('0' * 22 + '3fba64ad7b'),                )                if 2 == tmp[-1] == tmp[-2]:                    print(keytmp.format(c1, c2, c3))find_key()

所以key大概率就是4d9a7000104376fe了。

然后已知m和key求iv这个属于是密码学题目基本操作了，抄一下上面wp的脚本稍微改一下就行：

import binasciiimport hashlibfrom Crypto.Cipher import AESdef encrypt(message,passphrase,iv):    aes = AES.new(passphrase, AES.MODE_CBC, iv)    return aes.encrypt(message)def decrypt(message, passphrase, iv):    aes = AES.new(passphrase, AES.MODE_CBC, iv)    return aes.decrypt(message)key = b"4d9a7000104376fe"message = b"Do you ever feel, feel so paper thin, Like a house of cards, One blow from caving in"          + binascii.unhexlify(hashlib.sha256(key).hexdigest())[:10]          + b"x02x02"IV = b'yellow_submarine'arbitrary = binascii.hexlify(encrypt(message, key, IV))encrypted = '******************************************************************************************************************************************************3fba64ad7b78676e464395199424302b21b2b17db2'.replace('*', '0')encrypted = [encrypted[i:i+32] for i in range(0, len(encrypted), 32)]arbitrary = [arbitrary[i:i+32] for i in range(0, len(arbitrary), 32)]def guess_block(flag_block, correct_block, correct_iv):    c1 = decrypt(binascii.unhexlify(flag_block), key, binascii.unhexlify(b'0' * 32))    c2 = decrypt(binascii.unhexlify(correct_block), key, binascii.unhexlify(correct_iv))    result = b''    for i in range(16):        result += bytes([c1[i] ^ c2[i]])    return binascii.hexlify(result)for i in range(1, len(arbitrary) + 1):    if i == len(arbitrary):        e2 = binascii.hexlify(IV)    else:        e2 = arbitrary[-i - 1]    tmp = guess_block(encrypted[-i], arbitrary[-i], e2)    if i == len(arbitrary):        flag = binascii.unhexlify(tmp)    else:        encrypted[-i - 1] = tmpprint(flag.decode('utf8'))

所以最后flag就出来了。

> flag{72713126e9b90eab}

END


```
tshark -r .super_electric.pcapng -Y "mms.itemId == "LLN0$CO$FunEna1$Oper"" -T fields -e "mms.octet_string" &gt; data.txt
```



```
data = b""with open('data.txt', 'r') as f:    for line in f:        data += bytes.fromhex(line.strip())with open("test.exe", 'wb') as f:    f.write(data)
```



```
b = bytearray(bytes.fromhex("66736D6E2446747E787D65254F647E677563327A796579656C395B5E4F177772504E505704474F49495A494245274742405E4047145D574450555359365B4C502D612A2B2C652F2A3826383F6C2B222E375B332027302423783F363A3B06646A3D415F5E4442000B090E114C4C0C000B50171E12132E5B4642245A46415D5902A78BE9E6FDA5BBA7EAAEBEEFB5ECB9BFA0A1A3A3A0A6A1BDB2B3BD91F0BDA3BFCCC4CC8BCFC0DF8EA2C4CFD8DFCCC9CA908C92D193F1D997C1D6CF9BD9CBDBCDE0A7A7A6A8E9E6A1ADACA6EBBFA2EEBFB1A1B7A1F4A1BEBEB6F5FA97B5B6BBFF81C18A8C919683C7878FCA888D9F8A9CDCD1BD9D91D5949B978EDA9D8E9293DF6360746A6A62266E662E2A202C6F67617162717A7D3B6379707C6277757B67374840514B484C44095B414B19191B064455481B1D5C504E53515E5F48481517161B7B7373194F2F3168746A2D202C2914656B7F62095F3B322B2A3B3C397D637F0D041110050203474349081218081D47581D525E5419131950141F080F1C191AA9A1A7A3E8ACA6ADA8EAE2F9A4E1AEA2B0FDF7FDBCF8F3E4EBF8FDFEB5BDBBBFCC888E83C1CBC5C8CCC0C4CC8C908E88C5C5D49E8C929FBDD9DCC99B819DFFFA93EFACA6B3EDADA2B1E5EA8A899EE0829F95978C979795FBF8B0ACF2D6ADACB68E95CA818D8B87948B8083C58488968399978BDB959085D99D979989858D8AD76D6471706562632E21200028262724253A3B38393E3F3C3D32333031363734350A0B08090E0F0C0D02030001060704051A1B18191E1F1C1D12131011161714156A6B68696E6F6C6D62636061666764657A7B78797E7F7C7D72737071767774754A4B48494E4F4C4D42434041464744455A5B58595E5F5C5D5253505156575455AAABA8A9AEAFACADA2A3A0A1A6A7A4A5BABBB8B9BEBFBCBDB2B3B0B1B6B7B4B58A8B91C5C6C49093C9CD9DC99B95989886D4868580868F828980838F8E898D8FF2A3F0F2A6F7A4F6FFADA8F9C6"))for i in range(len(b)):    b[i] = 0xff & (b[i] ^ i)print(b)
```



```
import binasciifrom Crypto.Cipher import AESdef decrypt(message, passphrase, iv):    aes = AES.new(passphrase, AES.MODE_CBC, iv)    return aes.decrypt(message)def find_key():    keytmp = '4d9a700010437{}{}{}'    for c1 in "0123456789abcdef":        for c2 in"0123456789abcdef":            for c3 in "0123456789abcdef":                tmp = decrypt(                    binascii.unhexlify('78676e464395199424302b21b2b17db2'),                    keytmp.format(c1, c2, c3).encode('utf8'),                    binascii.unhexlify('0' * 22 + '3fba64ad7b'),                )                if 2 == tmp[-1] == tmp[-2]:                    print(keytmp.format(c1, c2, c3))find_key()
```



```
import binasciiimport hashlibfrom Crypto.Cipher import AESdef encrypt(message,passphrase,iv):    aes = AES.new(passphrase, AES.MODE_CBC, iv)    return aes.encrypt(message)def decrypt(message, passphrase, iv):    aes = AES.new(passphrase, AES.MODE_CBC, iv)    return aes.decrypt(message)key = b"4d9a7000104376fe"message = b"Do you ever feel, feel so paper thin, Like a house of cards, One blow from caving in"          + binascii.unhexlify(hashlib.sha256(key).hexdigest())[:10]          + b"x02x02"IV = b'yellow_submarine'arbitrary = binascii.hexlify(encrypt(message, key, IV))encrypted = '******************************************************************************************************************************************************3fba64ad7b78676e464395199424302b21b2b17db2'.replace('*', '0')encrypted = [encrypted[i:i+32] for i in range(0, len(encrypted), 32)]arbitrary = [arbitrary[i:i+32] for i in range(0, len(arbitrary), 32)]def guess_block(flag_block, correct_block, correct_iv):    c1 = decrypt(binascii.unhexlify(flag_block), key, binascii.unhexlify(b'0' * 32))    c2 = decrypt(binascii.unhexlify(correct_block), key, binascii.unhexlify(correct_iv))    result = b''    for i in range(16):        result += bytes([c1[i] ^ c2[i]])    return binascii.hexlify(result)for i in range(1, len(arbitrary) + 1):    if i == len(arbitrary):        e2 = binascii.hexlify(IV)    else:        e2 = arbitrary[-i - 1]    tmp = guess_block(encrypted[-i], arbitrary[-i], e2)    if i == len(arbitrary):        flag = binascii.unhexlify(tmp)    else:        encrypted[-i - 1] = tmpprint(flag.decode('utf8'))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667302242.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667302243.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1667302244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667302245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667302246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1667302248.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667302249.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667302249.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667302250.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1667302250.png)