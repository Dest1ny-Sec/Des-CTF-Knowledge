# DataCon2023软件安全赛道，冠军战队WP分享

> 原文: https://www.ctfiot.com/150561.html
> ID: 150561

由中国通信学会数据安全委员会指导，奇安信集团、清华大学网络研究院、北京市大数据中心、蚂蚁集团、腾讯安全大数据实验室、Coremail广东盈世、赛尔网络主办的DataCon大数据安全分析竞赛最终排名已揭晓。

清华大学TrickorTech战队、武汉大学N0nE429战队、中国科学院信息工程研究所404NOTFOUND战队、中国科学院信息工程研究所Hematopoiesisbshjdkvhbj战队、社会联合跃哥我真不会啊战队分别获得AI安全赛道、软件安全赛道、邮件安全赛道、互联网威胁溯源赛道、漏洞分析赛道冠军。本期N0nE429战队将为大家分享软件安全赛道解题思路。

一、Metasploit/CobaltStrike shellcode stager配置信息提取

Metasploit/CobaltStrike样本数据集，共200个样本，均为PE文件，架构为x86、x64。题目提供一个沙箱供选手分析和下载内存转储和衍生物文件。提交格式如下:

{ "xxxxxxxx":{"C2": "101.42.166.216:80", "Arch": "x86", "Encoder":"shikata_ga_nai:15"}, "xxxxxxxx":{"C2": "145.78.129.214:3000", "Arch": "x64", "Encoder":"null"} }

参考资料： Metasploit & CobaltStrike 的shellcode分析
(https://xz.aliyun.com/t/7996)

有6个样本加了upx壳, 直接使用https://github.com/upx/upx提供的程序就可以全部脱壳。

1. Metasploit

1.1 无Encoder

1.1.1 逆向分析

Metasploit 是一个开源框架, 可以直接通过查看源码来获取其shellcode信息。对于不使用Encoder的Metasploit shellcode样本来说, 其特征非常明显, 以block_bind_tcp.asm为例, 其函数调用是通过如下方式进行的:

push 0x006B8029 ; hash( "ws2_32.dll", "WSAStartup" ) call ebp ; WSAStartup( 0x0190, &WSAData );

先push一个特殊值, 再通过call ebp进行调用. 64位的调用也类似:

mov r10d, 0x006B8029 ; hash( "ws2_32.dll", "WSAStartup" ) call rbp ; WSAStartup( 0x0101, &WSAData );

因此我们可以通过搜索0x6B8029这个关键十六进制字节来确定shellcode的位置. 接下来需要知道这段shellcode是如何加载C2的ip和端口的。

通过观察源码和二进制文件, 我们可以确定, 在32位中其ip和端口的加载方式如下:

0x80BEA8C0 -> 0xC0A8BE80 -> C0 A8 BE 80 -> 192.168.190.128 0x33050002 -> 0x533 -> 1331

64位样本中IP和端口的加载方式也类似:

0x00000000 -> 0.0.0.0 0x5c110002 -> 0x115c -> 4444

具体实现时, 通过python调用ida脚本, 直接对代码段进行搜索得到shellcode位置

addr = ida_search.find_binary(0, 0xffffffffffffffff, '29 80 6B 00', 16, idc.SEARCH_DOWN)

得到shellcode位置后, 在按照上面的方法提取出IP/端口并转换为可读文本即可。有些样本中shellcode会被放在.text段中, 有些则会被放在.data段中。

1.2 shikata_ga_nai Encoder

对于使用了shikata_ga_nai encoder的样本来说, 其代码中总是包含xd9x74x24xf4, 即下文的fnstenv指令, 因此可以通过这个内存特征来筛选出相关样本。

1.2.1 逆向分析

shikata_ga_nai encoder是通过自修改/解密代码来实现隐藏的，可能有多轮，每一轮 smc 模式如下所示，具体指令顺序可能有所不同。

fcmovu st, st(1) ; opcode=DA,还有其他形式 fnstenv byte ptr [esp-0Ch] mov REG1, XORCONST pop REG2 sub ecx, ecx ; xor ecx, ecx mov cl, XORLEN loc_loop: xor [REG2+OFFSET], REG1 add REG2, 4 ; sub REG2, 0FFFFFFFCh add REG1, [REG2+OFF-4] loop loc_loop

• fnstenv 指令，常用于恶意代码shellcode实现中, 配合pop指令可以得到EIP地址. 在这段程序中通过 pop REG2 , 使得REG2的值为 fcmovu st, st(1)的地址(即上一条FPU指令所在地址)；
• 从地址 REG2+OFFSET 开始，每 4 字节为一个单位，与 XORCONST 进行异或，XORCONST 更新为加上异或结果的值；
• 循环次数为 XORLEN；
• 如果存在多轮加密, 那么每轮解密的结果仍然是一段解密代码；

样本解密后如下所示, 使用无Encoder的方法就可以搜索并提取到IP/端口。

2.CobaltStrike

2.1 无混淆

CobaltStrike的shellcode特征较为明显, 其回连C2的ip和port会被传入InternetConnectA, 即InternetConnectA(hInternet, serverIp, atoi(serverPort), NULL, NULL, 3, NULL, NULL)因此我们分析该函数的前后情况即可。以下图为例:

push 0C69F8957h 和 call ebp代表调用, 前面的几条汇编指令代表传参, 因此以push 0C69F8957h为基准, 减去一个偏移就可得到push端口的指令, 提取出操作数就是端口。

而ip的提取麻烦一些: 在调用InternetConnectA之前, 会首先调用InternetOpenA, InternetOpenA调用完成后, 会经历 jmp -> jmp ->call, 其中call的地址就是上面这段代码的开始地址, 根据x86(x64)的调用规则, call指令会将其下一条指令地址压栈, 如下图所示：

压栈的就是0x41A38D, 而其内容就是’39312e3133322e35392e313133′, 即 91.132.59.113, 而上面那段代码的开头会调用pop ebx, 此时ebx指向的就是这个ip地址了。

因此只要找到push 0C69F8957h, 就可以比较顺利找到这个样本对应的ip和port了。

2. 2 混淆

2.2.1 逆向分析

CobaltStrike的样本中存在一种比较简单的混淆。

从某个0x1000对齐的地址开始, 首先四个字节无用, 然后是四个字节表示shellcode长度, 紧接着的四个字节是用于解密shellcode的密钥, 然后跳过8个字节, 开始的就是shellcode，在代码中这段数据的解密方式为：

在本次比赛中, 沙箱的内存dump下载功能可以帮助我们直接获得解密后的样本, 因此这一部分不需要额外进行处理。

二、AgentTesla、Sliver家族配置信息提取

AgentTesla/Sliver样本数据集，共320个样本，其中AgentTesla为170个，Sliver为150个。题目提供一个沙箱供选手分析和下载内存转储和衍生物文件。

提交格式如下:

{ "xxxxxxxx": { "Family": "AgentTesla", "Protocol": "smtp", "Host": "smtp.powweb.com", "Port": "587", "Username": "imports@mastertraders.biz", "Password": "Naeem@68", "EmailTo": "jeanluois.rrms26@gmail.com" }, "xxxxxxxx":{ "Family": "AgentTesla", "Protocol": "ftp", "Host": "ftp://peruglobo.com", "Port": "21", "Username": "0n0w0phili@peruglobo.com", "Password": "Etd[WCRaH$sX" }, "xxxxxxxx":{ "Family": "Sliver", "Protocol": "mtls", "C2": "mtls://116.82.195.67:15903", "CA_Certificate": "-----BEGIN CERTIFICATE-----XXX-----END CERTIFICATE-----", "Certificate": "-----BEGIN CERTIFICATE-----XXX-----END CERTIFICATE-----", "PRIVATE_KEY": "-----BEGIN EC PRIVATE KEY-----XXX-----END EC PRIVATE KEY-----" }}

参考资料:

1, Decrypting XorStringsNET the easy way

2, AgentTesla v3

3, AGENT TESLA RAT DISGUISED AS NSIS INSTALLER

1.AgentTesla

我们针对AgentTesla主要研究了V3和V4版本

1.1 正则匹配

1.1.1 直接正则匹配邮箱

比如样本：
c2379132478fd4e404e95f02d8da64f7

可以直接从沙箱分析后的内存转储映像文件，即dmp文件中，根据邮箱的正则表达式进行匹配 b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}b

如下所示，分别为端口，Host、Username、password、emailto

由于内存转储文件中许多其他不相关字符，所以需要先用”x00x00x00”进行切割，并通过正则表达式[x20-x7E]{2,}$ 匹配长度至少为2的可见字符串。

最后对于匹配到的第一个邮箱，其他信息设置如下：

self.Port = str_data[index - 3] self.Host = str_data[index - 1] self.Username = data self.Password = str_data[index + 1] self.EmailTo = str_data[index + 2]

通过沙箱获取所有样本中间衍生物（反射加载得到的，文件名带有Reflective字样的），再通过沙箱获取衍生物的dmp文件，进一步通过上述方法获取，最后成功提取得到39个。

1.2 V3（IL提取）

1.2.1 分析

V3版本的特点是, 其关键字符串(包括我们所需的C2信息)都是通过某个内部类下面的方法获得的, 以0a11269d25419f79726cd9d3e95c7fbc为例:

而这些方法的实现依靠调用该类下的一个方法来切割字符串:

这个切割方法如下, 调用GetString获得目标字符串然后进行赋值:

而这个字符串86BE2B1B-20DF-4E6D-ACD5-3008899C7F6A.<> 是直接写入程序中的:

在解密开始前该字符串会被进行一个简单解密:

那么解题思路就很清晰:

1, 搜索这个解密算法, 确定V3的样本(样本内存dump)；

2, 获取这个字符串, 并手动对其进行解密；

3, 获取分割根据, 例如上面的(0, 0, 0), (1, 0, 2)；

4, 对解密的字符串进行分割；

5, 然后根据特定规律进行C2信息的提取。

1.2.2 实现

在实现上, 参考了大量参考资料2, 只需要对其代码进行调整即可

1, 搜索解密算法, 我们以解密方法的尾部字节为函数签名进行搜索

2, 获取字符串

复用参考资料2提供的脚本

3, 获取分割依据

复用参考资料2提供的脚本

4, 对解密的字符串进行分割

这些内存dump里的字节序列, 其和这些分割标记对不上. 通过动态调试发现, 在程序真正运行时, AgentTesla采集到的系统信息会被填充到这个字节序列里, 并抛弃了前面一部分字节.

通过观察发现几乎所有的字节序列都包含一个特殊的特征:

yyyy-MM-dd HH:mm:ssyyyy_MM_dd_HH_mm_ss

它们的长度分别为19, 19, 4, 4. 根据这个特征我们可以遍历得到yyyy-MM-dd HH:mm:ss对应的分割标记A1, 而我们可以直接检索到yyyy-MM-dd HH:mm:ss开始的index, 我们将这两个信息结合, 直接抛弃掉A1之前所有的分割标记, 抛弃掉这个字符串之前的所有字符串, 这样我们就可以用正确的标记对信息进行分割了

5, 按照特定规律提取C2信息

提取得到的字符串如下图所示:

我们观察到, 对于smtp协议来说, C2信息可能出现在两个位置, 一个是PW_x00后紧跟的3或4个字符串, 分别代表username, password, host(, emailto), 一个是application/x-www-form-urlencoded后紧跟的3或4个字符串, 分别代表username, password, host(, emailto):

emailto可能为空, 如果emailto为空, 那么emailto就是username

对于ftp协议, 其特征是ftp协议ftp://, 因此只需要检测是否以其开头, 如果是那么它就是host, 然后提取下面的username和password即可

1.3 V4（IL提取）

1.3.1 分析

以b49b452080b4822c8c1aac813609cb20为例, V4样本的特点是, 其关键变量的获取是通过调用某个函数并传入一个大整数实现的:

这个函数非常复杂, 不过参考资料1中已经给出了解密方法, 因此我们只需要识别出这个函数, 记录其Token即可:

识别到后我们使用命令

de4dot.exe {filepath} --strtyp delegate --strtok {token} -o {output_filepath}

即可得到解密后的文件, 再次打开就可以看到这些关键变量已经被赋予了正确的值

我们的思路如下

1, 扫描解密方法特征, 识别出所有的样本(样本内存dump)

2, 批量使用de4dot进行解密

3, 识别出包含这些字符串的类并进行字符串提取

4, 识别出IOC信息

1.3.2 实现

1, 扫描解密方法特征

这个同样采取了操作序列作为函数签名, 通过观察几个样本确定前面确定的字符序列和尾部确定的字符序列:

2, 批量使用de4dot进行解密

3, 识别出包含这些字符串的类并进行字符串提取

通过观察可以发现包含了关键信息的类中field非常多, 我们就以30个为界, 去识别这样的类, 然后将这个类中所有的赋值语句中涉及到的字符串给提取出来

4, 识别出IOC信息

识别得到的字符串序列非常有特点, 即这些信息所在的行数是固定的

对于ftp协议来说:

对于smtp协议来说:

emailto的部分和v3一样, 如果不存在则默认填写username

1.4 v4-反射提取

下面以b49a32215b6caeeee05cc2d994343c59为例进行定位与解密。

1.4.1 定位解密方法

先找到smtpClient（）的配置方法

在b中是密文

u.A显然应该是解密方法

在正常情况下，我们需要考虑提取该解密方法的Key、填充模式等信息，并重写该解密方法，但对于反射法来说，上述都不需要，我们会通过反射的方法加载该解密方法，完成自动化密文解密。

但所有方法和变量名都已经经过混淆，不能直接通过名字查找，因此可以通过特征逐步缩小范围，直 至可以成功定位。

观察其特征，发现以下特征：

• 该方法为public unsafe static string A(int A_0)
• 只有一个参数，且类型为int，代码实现时parametertype为Int32
• 该方法返回类型为string，代码实现时为String
• 该方法所在类有1个方法，判断时(0，2)

1.4.2 定位密文

观察类b，总结以下特征：

• 密文所在类b包含public static变量，且数量在35-37之间
• 类中包含public static方法，一般为1， 且数量在1-3之间

1.4.3 解密

成功拿到解密方法和加密数据后，需要用invoke调用解密方法解密加密数据：

// 使用invoke调用解密方法,参数为 //value_type = field.FieldType; value = field.GetValue(null) as string; //Console.WriteLine(i.ToString()); //Console.WriteLine(value);                             result = decryptMethod.Invoke(null, new object[] { value });

2. Sliver

2.1 提取准备

首先，将150个Sliver样本上传至天穹沙箱分析，分析选项为：

分析系统：Windows 10 x86-64

分析时间：10分钟

环境类型：Fast

分析环境：快速分析环境

2.2 提取C2服务器信息

首先选择几个样本，使用010 Editor的Find in Files功能，在内存Dump中进行初步的搜索。

使用正则表达式:d{2,5}搜索，然后人工查看，即可在很多样本中快速定位到C2服务器信息。

314d579e475de6222fa478f612b8dd7a：

而对于部分样本，通过这种方式无法找到C2服务器，例如样本
495D0D2353A62E7A43335449E81FA652

还发现一个现象：一些C2配置信息开头有形如mtls://的协议信息，例如mtls://28.143.36.90:51251，而另一些则没有，例如117.117.22.187:5000。并且，很多C2配置的开头和末尾都是x00字节。

基于上述观察，编写脚本进行C2配置信息的自动化提取, 流程如下:

然后，使用正则表达式搜索C2配置信息。正则表达式分为两类，一类确信度较高，如果使用这类正则表达式匹配到结果，那么很可能就是正确答案；一类确信度较低，如果使用这类正则表达式匹配到结果，那么很可能不是正确答案。

部分确信度较高的正则表达式包括：

([da-zA-Z.-]+).([a-z.]{2,6}):d{2,5}x00([da-zA-Z.-]+).([a-z.]{2,6}):d{2,5}x00mtls://([da-zA-Z.-]+).([a-z.]{2,6}):d{2,5}
((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?):d{2,5}x00((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?):d{2,5}x00mtls://((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?):d{2,5}

确信度较低的正则表达式包括：

((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?)([da-zA-Z.-]+).(xyz|com|cn|ru|uk|us|net|co|agency|top|org|best)

使用确信度较低的正则表达式提取，基本不可能提取到正确答案。

于是设计下面的算法：

首先，在C000Files中用确信度高的正则表达式搜索。

如果未搜索到结果，再在所有内存Dump文件中用确信度高的正则表达式搜索。

如果仍未搜索到结果，再在C000Files中用确信度低的正则表达式搜索。

如果依旧未搜索到结果，最后再在所有文件中用确信度低的正则表达式搜索。

假如最终结果是由确信度低的方法得到的，搜索到的结果里是没有端口号的，这种情况下，将提取的端口号设置为8888（mtls协议默认端口)

如果使用正则表达式没有找到C2的协议，那么使用下面的方法进一步判断协议：

在C000Files中依次搜索”mtls://”，”https://”等字符串，搜索到某个字符串，就将提取的C2协议设置为对应的协议。如果未搜索到字符串，那么再根据端口号进行判断，例如443端口认为是https协议，80端口认为是http协议。最后，如果仍未得到C2的协议，那么就认为C2是mtls协议。

根据人工辅助分析可以发现, 在匹配IP地址的时候，找到所有能匹配到的IP地址，并优先选择其中第一个字段最大的IP地址, 正确率更高一些。

2.3 提取证书和密钥信息

需要提取的证书和密钥均为PEM格式。

证书的格式为：

-----BEGIN CERTIFICATE-----XXXXXXXXX-----END CERTIFICATE-----

密钥的格式为：

-----BEGIN EC PRIVATE KEY-----XXXXXXXXX-----END EC PRIVATE KEY-----

在部分样本中，可以直接在内存Dump里搜索到符合上述格式的字符串。

例如，样本20820a18233a63bfaa9ec04f2049f0ad的内存Dump中搜索，可找到：

经过简单统计后，认为证书数据的字符数大约在450~750的范围，客户端私钥数据的字符数大约在100~300的范围。

在能提取到证书和私钥的样本中，通常可以提取两个证书和一个私钥。提取出的私钥即可认为是客户端私钥。而对于提取出的两个证书，可以用Python的cryptography库进一步判断是CA证书还是客户端证书。

【推荐阅读】


```
{ "xxxxxxxx":{"C2": "101.42.166.216:80", "Arch": "x86", "Encoder":"shikata_ga_nai:15"}, "xxxxxxxx":{"C2": "145.78.129.214:3000", "Arch": "x64", "Encoder":"null"} }
```



```
push 0x006B8029 ; hash( "ws2_32.dll", "WSAStartup" ) call ebp ; WSAStartup( 0x0190, &WSAData );
```



```
mov r10d, 0x006B8029 ; hash( "ws2_32.dll", "WSAStartup" ) call rbp ; WSAStartup( 0x0101, &WSAData );
```



```
0x80BEA8C0 -> 0xC0A8BE80 -> C0 A8 BE 80 -> 192.168.190.128 0x33050002 -> 0x533 -> 1331
```



```
0x00000000 -> 0.0.0.0 0x5c110002 -> 0x115c -> 4444
```



```
addr = ida_search.find_binary(0, 0xffffffffffffffff, '29 80 6B 00', 16, idc.SEARCH_DOWN)
```



```
fcmovu st, st(1) ; opcode=DA,还有其他形式 fnstenv byte ptr [esp-0Ch] mov REG1, XORCONST pop REG2 sub ecx, ecx ; xor ecx, ecx mov cl, XORLEN loc_loop: xor [REG2+OFFSET], REG1 add REG2, 4 ; sub REG2, 0FFFFFFFCh add REG1, [REG2+OFF-4] loop loc_loop
```



```
{ "xxxxxxxx": { "Family": "AgentTesla", "Protocol": "smtp", "Host": "smtp.powweb.com", "Port": "587", "Username": "imports@mastertraders.biz", "Password": "Naeem@68", "EmailTo": "jeanluois.rrms26@gmail.com" }, "xxxxxxxx":{ "Family": "AgentTesla", "Protocol": "ftp", "Host": "ftp://peruglobo.com", "Port": "21", "Username": "0n0w0phili@peruglobo.com", "Password": "Etd[WCRaH$sX" }, "xxxxxxxx":{ "Family": "Sliver", "Protocol": "mtls", "C2": "mtls://116.82.195.67:15903", "CA_Certificate": "-----BEGIN CERTIFICATE-----XXX-----END CERTIFICATE-----", "Certificate": "-----BEGIN CERTIFICATE-----XXX-----END CERTIFICATE-----", "PRIVATE_KEY": "-----BEGIN EC PRIVATE KEY-----XXX-----END EC PRIVATE KEY-----" }}
```



```
self.Port = str_data[index - 3] self.Host = str_data[index - 1] self.Username = data self.Password = str_data[index + 1] self.EmailTo = str_data[index + 2]
```



```
yyyy-MM-dd HH:mm:ssyyyy_MM_dd_HH_mm_ss
```



```
de4dot.exe {filepath} --strtyp delegate --strtok {token} -o {output_filepath}
```



```
// 使用invoke调用解密方法,参数为 //value_type = field.FieldType; value = field.GetValue(null) as string; //Console.WriteLine(i.ToString()); //Console.WriteLine(value);                             result = decryptMethod.Invoke(null, new object[] { value });
```



```
([da-zA-Z.-]+).([a-z.]{2,6}):d{2,5}x00([da-zA-Z.-]+).([a-z.]{2,6}):d{2,5}x00mtls://([da-zA-Z.-]+).([a-z.]{2,6}):d{2,5}
((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?):d{2,5}x00((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?):d{2,5}x00mtls://((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?):d{2,5}
```



```
((2[0-4]d|25[0-5]|[01]?dd?).){3}(2[0-4]d|25[0-5]|[01]?dd?)([da-zA-Z.-]+).(xyz|com|cn|ru|uk|us|net|co|agency|top|org|best)
```



```
-----BEGIN CERTIFICATE-----XXXXXXXXX-----END CERTIFICATE-----
```



```
-----BEGIN EC PRIVATE KEY-----XXXXXXXXX-----END EC PRIVATE KEY-----
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702114343.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1702114344.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1702114344.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/5-1702114345.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702114346.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702114347.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702114347.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702114348.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702114349.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1702114351.png)