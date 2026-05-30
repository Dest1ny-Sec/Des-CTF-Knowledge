# 逆向心法修炼之道 FLARE ON 9TH WRITEUP

> 原文: https://www.ctfiot.com/74040.html
> ID: 74040

背景：Mandiant 公司的 FLARE 团队会在每年九十月份举办一场侧重于 Windows 平台的逆向挑战赛 FlareOn CTF，旨在考验参赛选手在逆向分析领域上的技能水平。从 2014 年至今 FLARE 团队已经连续举办了 8 届比赛，而今年第 9 届 FlareOn Challenge 也是 Mandiant 被 Google 收购后所举办的第一场 FlareOn 挑战赛。尽管相比往年，本届比赛的开赛时间略微晚了一个月，但比赛时长和题目质量却并没有缩水。比赛时长仍旧是横跨 6 周，自北京时间 2022.10.01 08:00 开始到 2022.11.12 09:00 结束。比赛题目所涉及的内容与往年大同小异，基本涵盖了 C/C++、JavaScript、.Net、密码学、勒索、后门、网络流量等主题方向，另外还新增加了一个针对 68K Macintosh 架构的挑战题目。

对于大陆地区的小伙伴们来说，正好可以趁国庆假期在家刷刷题练练手，最后再在收到双十一快递包裹的喜悦中结束比赛。

一、Flaredle

1.1 writeup

第一题对输入内容的校验逻辑相对直白，通过与word.js中内置的一组硬编码值进行比对，若相符即验证通过：

二、Pixel Poker

2.1 writeup

根据计算逻辑，只要保证像素点的x，y坐标满足以下条件即可触发flag显示：

X == 0x52414C46 % 0x2E5

Y == 0x6E4F2D45 % 0x281

选取坐标(x,y )=(95,313），点击即可得到flag：

三、Magic 8 Ball

3.1 writeup

解题步骤（前2步可调换顺序）：

Star typing your question处输入gimme flag pls?

以L L U R U L D U L（即：左左上右上左下上左）顺序依次敲击键盘上的方向键

回车确认

经分析，程序关键的校验逻辑存在于函数0x4024E0中，其主要完成以下校验操作：

检查是否有用户输入，且输入内容是否与0x4021A1处硬编码字符串gimme flag pls?相同；

2. 用户是否按指定序列依次敲击了方向键；

若满足以上两个条件，程序随即进入flag解密分支：

四、darn_mice

4.1 writeup

程序需提供1个命令行参数，该命令行参数将被用作以下用途：

参与生成待执行的1字节shellcode（多组）

参与解密计算

由于代码中会执行v2(v2)操作，而此地址上填充的是str[i]+v5[i]的内容，即只有1字节。为了保证函数正常执行，那么大概率这1字节是一个ret指令，对应十六进制0xC3：

按此逻辑编写脚本反推输入内容：

将see three, C3 C3 C3 C3 C3 C3 C3! XD作为命令行参数，再次运行程序即可得到flag内容：

五、T8

5.1 writeup

入口处（0x4046E0）通过月相计算函数判断当前日期的月相值，经分析，程序只有在满月的日期运行时才能避免陷入长时间的休眠等待：

这里可通过修改系统日期来绕过sleep休眠。

接下来t8.exe作为网络请求客户端，向flare-on.com发起2次POS请求，其网络请求参数的构造方式如下：

srand(milliseconds since current hour)

randnum = rand()

key = wchar(

md5sum.hexdigest(

wchar(“FO9″+randnumOfDecimal)))

POST1 => wchar(

b64_encode(

rc4(key, wchar(“ahoy”))))

RESP1 => rc4(key, b64_decode(resp))

.split(wchar(“,”))

.forEach(calcMoonPhase).map(phase => {

alphabet[phase]

})

.join()

POST2 => rc4(md5sum(flag), “sce”)

而服务器则会将flag信息加密后放在第一次的响应应答中。根据该报文的构造方式，若要解密flag信息则需要知晓参与RC4加密的key参数。由于POST1和RESP1共用同一对rc4 key，且我们有双方的数据包流量，则可以通过枚举方式找出程序当时参与运算所使用的rc4 key。

根据分析结果，rc4 key的构造依赖于运行时的时间戳：

password = “FO9” + 自本小时开始所经过的毫秒数

key = md5sum(password)

报文中的时间戳信息可以将时间范围缩小到16:14:36前后，即srand函数的seed范围介于1000*(14*60+36)~ 1000*(14*60+36)+0xFFFF之间：

因此可构造最多65535组key，对应的password形如：

FO99870

FO99873

FO99876

FO99879

FO99883

…snip…

因为POST1的内容已知，即：y.d.N.8.B.X.q.1.6.R.E.=，则只需要逐个遍历找到正确的password即可。

编写测试脚本进行测试，当password为FO911950时，rc4(key, “ahoy”)的结果正好为ydN8BXq16RE=。

需注意，key的hexstream形式为：a5c6993299429aa7b900211d4a279848，而由于程序内部均使用wchar_t类型来存储字符串等内容，故真正参与计算的key实际是：61003500630036003900390033003200390039003400320039006100610037006200390030003000320031003100640034006100320037003900380034003800。

使用该key，对RESP1内容进行解密，即可得到解密后的内容：

rc4(array(“61003500630036003900390033003200390039003400320039006100610037006200390030003000320031003100640034006100320037003900380034003800”), b64decode(“F1KFlZbNGuKQxrTD/ORwudM8S8kKiL5F906YlR8TKd8XrKPeDYZ0HouiBamyQf9/Ns7u3C2UEMLoCA0B8EuZp1FpwnedVjPSdZFjkieYqWzKA7up+LYe9B4dmAUM2lYkmBSqPJYT6nEg27n3X656MMOxNIHt0HsOD0d+”))

得到的内容再经wchar(“,”)分割（0x40426A）后生成14组_SYSTEMTIME结构类型的存储数据（CyberChef recipe）：

e5 07 09 00 03 00 0f 00 0d 00 25 00 03 00 62 02

dc 07 0a 00 06 00 0d 00 0d 00 25 00 09 00 2a 03

e1 07 0c 00 04 00 07 00 0d 00 25 00 24 00 e5 00

e0 07 05 00 05 00 06 00 0d 00 25 00 0b 00 26 00

e2 07 0a 00 01 00 08 00 0d 00 25 00 1f 00 45 03

e6 07 03 00 02 00 01 00 0d 00 25 00 32 00 da 00

de 07 07 00 02 00 16 00 0d 00 25 00 36 00 d1 02

de 07 05 00 03 00 0e 00 0d 00 25 00 01 00 e8 00

da 07 04 00 01 00 05 00 0d 00 25 00 3a 00 0b 00

dd 07 0a 00 04 00 03 00 0d 00 25 00 16 00 16 03

de 07 01 00 02 00 0e 00 0d 00 25 00 10 00 c9 00

dc 07 0c 00 01 00 0a 00 0d 00 25 00 30 00 0c 02

e6 07 02 00 01 00 1c 00 0d 00 25 00 22 00 4b 01

e6 07 09 00 05 00 09 00 0d 00 25 00 21 00 6d 01

分别计算这14组日期参数对应的月相值，以月相值为下标索引，从内置的一个字符串编码表中取相应的字符进行拼接：

即可得到flag前缀：i_**。

在使用正确key的情况下，t8在拿到第二次响应RESP2后最终会生成一个提示窗：

六、àla mode

6.1 writeup

使用capa v4.0有注意到该文件具备mixed mode特征：

使用flass-floss v1.7.0发现存在xor解密后的\\.\pipe\FlareOn字符串：

floss.v1.7.0.exe -x -g –no-static-strings –no-stack-strings -q HowDoesThisWork.dll

其中一些函数操作及管道名称等跟dnSpy中看到的代码逻辑基本对应得上。

使用IDA加载HowDoesThisWork.dll文件，在Load config界面注意选择Portable executable for 80386(PE)[pe.dll]模式：

就可以看到native code内容：

由于此时的EP为0xD16C，故而DllEntryPoint定位到了0x1000D16C函数中，此处是CorDllMain的入口点。

根据经验，我们找到native code中真实的DllEntryPoint位置，为0x1000181A。修改PE文件的EP为0x181A后重新用IDA打开该文件即可看到熟悉的内容：

程序逻辑本身不复杂，首先使用xor方式动态解密一组函数符号，而后动态获取到这一组函数的加载地址便于后续调用，这一组待解析的函数符号正好出现在我们之前使用floss所获取到的那组字符串中。

随后native code通过\\.\pipe\FlareOn进行读操作，而写操作则由managed code完成。简单分析发现只有当managed code端传入正确的password之后，native code才能返回flag信息：

直接在调试器中进行硬编码测试，发现预置的密码为：MyV0ic3!。此时会调用0x10001187函数（flossv1.7.0也同样识别到了该解密函数）解密得到flag信息。

七、anode

7.1 writeup

程序是由nexe打包而来，根据nexe的打包特点，可在文件尾部提取出约321848字节长度的anode.js源文件：

其代码逻辑是对输入长度为44字节的字符串进行若干组组合变化，最后与预置的一组状态值进行比对，若相符则证明输入正确。

Tips:可直接修改exe文件尾部的源码，进行测试。

经测试发现该程序存在几个值得关注的地方：

使用随机数决定状态的下一跳，且只有当state= 185078700时才会退出while循环；

使用随机数参与数值的逻辑计算，但最终比对的target数组内容却是硬编码预置好的；

相同输入在原独立exe程序中的运行结果和通过node anode.js方式本地运行的结果不一致；

原程序中，if(1n)时无法进不到该条件分支，且存在其他类似条件检测与标准的逻辑boolean计算结果相悖的地方；

了解nexe的机制之后发现，nexe在打包nodejs文件的时候会嵌入一个node运行环境（再底层是Chrome v8 engine）。而这套node环境既可以来自于官方预编译好的标准版（可以理解为非阉割、非魔改的版本），亦可以经由开发者自行编译node.js源码进行嵌入。不妨推测一下，该程序底层所使用的v8运行环境可能经过了魔改，使得部分函数调用和逻辑检查有别于标准v8引擎实现。亦或者，程序对部分函数实现进行了hook。

跟着这个思路，接下来尝试先去解决Math.random随机数问题。由于程序的退出状态和检查结果是固定的，因此程序中各状态间的跳转顺序必然是固定的，随机数生成序列必然固定，即Math.random是个伪随机数。

在原程序中加入打印Math.random随机数的代码，若干轮测试发现，其生成序列固定，且开头的几组数值为：

0.9409662359975814

0.8785819538827613

0.5130407304372815

0.7256221596588996

0.17527533615471103

到这里，对于获取完整随机数序列的思路有2个：

找到初始化seed，而后枚举出后续生成序列

修改原程序，直接获取运行过程中所用到的随机数序列

沿着思路2走的话，共统计出1566次Math.random调用，完整的随机数生成序列详见文件：https://gist.github.com/renzhexigua/34f09dd09b6a5cba05b04fcbef7dea92#file-pseudorandom-standard-py

而在沿着思路1继续检索Math.random初始化种子相关的技术资料时，找到了PwnFunction/v8-randomness-predictor这个项目，在README的介绍中瞥到了一个1337常量的身影：

这个数字同样作为init state出现在了anode.js中：

这可能是出题者故意留下的一个线索，引导选手去发现有关v8 Math.random生成器可预测的相关研究。简单来说就是，该研究找到了v8中Math.random生成器的实现“瑕疵”，证明其并不是密码学安全的伪随机数生成器（CPRNG），也即，可根据Math.random过去的生成序列（需提供至少2组随机数前序序列值），预测出后续随机数生成序列。

Douglas Goddard最早在文章“Hacking the JavaScript Lottery”中介绍了Math.random伪随机性、可预测性的特点并公开了一个PoC工具XorShift128Plus。这套工具是Douglas Goddard为了玩LA Time的powerball网页模拟器游戏所开发的“作弊器（不是）助手”：

先前提到的PwnFunction/v8-randomness-predictor项目则完全是针对Math.random攻击的另外一套纯PoC工具。

实际上，早在Douglas Goddard写那篇文章之前（2016.05），v8.dev在2015.12就出过一篇关于Math.random的博客“There’s Math.random(), and then there’s Math.random()”，其中提到了现有的实现技术，也点出了其非CPRNG的特点。

有关这部分的技术参考资料，推荐阅读：

Hacking the JavaScript Lottery

https://blog.securityevaluators.com/hacking-the-javascript-lottery-80cc437e3b7f

2. There’s Math.random(), and then there’s Math.random()

https://v8.dev/blog/math-random

3. XorShift128Plus

https://github.com/TACIXAT/XorShift128Plus

4. PwnFunction/v8-randomness-predictor

https://github.com/PwnFunction/v8-randomness-predictor/

https://github.com/whokilleddb/v8-randomness-predictor/

5. [V8 Deep Dives] Random Thoughts on Math.random()

https://apechkurov.medium.com/v8-deep-dives-random-thoughts-on-math-random-fb155075e9e5

Anyway，如果想实现自动化，那么可以通过上面的线索或PoC开发自己的工具。一开始我是思路1和2并行尝试，后来发现思路2的结果已经可以满足当前的需求。

在这里需要提一点，若想通过思路1实现自动化的随机数预测，需要注意node会在每生成64组随机数后重置entry pool/state，而参与重置的参数因子又来自于另一个“随机数”。这也导致了，用思路1的方法可能并不那么容易就用自动化的方式生成这1566组随机数序列。尽管根据前面提到的PoC可以计算出初始state0和state1，进而生成完全相同的前64组随机数。但若继续沿用1~64的state0和state1产生余下序列值，则从第65组开始，后续的随机数都会跟原程序的实际运行结果出现出入。因此，必须在每生成64组随机数后，重置一次state0和state1。至于如何重置以及本道题目下是否有编程实现的可能，以达到跟实际运行程序所使用的随机数序列相一致的效果，留到后面继续研究。这一部分的细节内容，可参考以下章节：

[V8 Deep Dives] Random Thoughts on Math.random()：The Nitty-gritty Details

MathRandom  https://github.com/nodejs/node/blob/52f9aafeab02390ff78447a390651ec6ed94d166/deps/v8/src/builtins/math.tq#L435-L453

3. MathRandom::RefillCache

https://github.com/nodejs/node/blob/52f9aafeab02390ff78447a390651ec6ed94d166/deps/v8/src/numbers/math-random.cc#L35

解决了随机数使用的问题（这里，我直接使用思路2得到全随机数序列），那么接下来可以继续分析anode.js是否有逆向分析的可能。

因为输入项的44组值之间存在各种理不清的逻辑关系，而最终校验的逻辑也是按位进行预设值的比较：

首先想到的可能是z3求解器，那么接下来就需要进行js转Python代码的等价移植。这个过程中还存在一个悬而未决的问题：哪些if逻辑分支被patch/hook了？

如下面的分支片段中，if(63441291n)为真，但在实际运行中却走入了else分支：

还有类似的：

解决这个问题，可能有更优的方案，比如去分析底层魔改或hook的逻辑等。

我这里是通过比对移植后的运行中间状态与node版运行的中间状态（如state、b的变化），来人工确定“不合实际/不一致”的逻辑分支位置，而后手动进行patch，如直接将781285820改为False等。

经过移植，我得到了一个等价版的Python代码，伪随机数的部分我通过把Math.random改为自己实现的一个小函数来代替，使用的时候按序弹出一个固定序列的随机数：

from collections import deque

PSEUDO_RANDOMS = deque([

0.9409662359975814,

0.8785819538827613,

0.5130407304372815,

…snip…

]

class Random():

def __init__(self, q):

self.q = q

def random(self):

value = self.q.pop()

return value

R = Random(PSEUDO_RANDOMS)

# 使用

if (R.random() < 0.5):

b[10] += b[32] + b[1] + b[20] + b[30] + b[23] + b[9] + 115

b[10] &= 0xFF

else:

b[7] ^= (b[18] + b[14] + b[11] + b[25] + b[31] + b[21] + 19) & 0xFF

尽管得到了Python的替代版程序，但在测试z3的时候发现很难在较短时间内进行求解，即使将约束条件设置得很少，也需要很久才能计算出合适的数值。因为44组数据经过1000+的逻辑关系运算后，相互之间的关联关系变得也更加复杂和膨胀，所以z3可能并不适合在这里使用。

在弃用z3的方案之后，我开始评估程序本身是否有逆向运行的可能，即从最终状态往前运行，由已知结果去还原原始输入。

发现，anode.js中涉及字节操作的逻辑只有+=、-=、^=三种，而这三种恰好都是可逆运算，即，根据结果和其中一个操作数，可以反向求得另外一个操作数：

B[0] ^= B[1] + B[2]   =>   B[0] ^= B[1] + B[2]

B[0] += B[1] + B[2]   =>   B[0] -= B[1] + B[2]

B[0] -= B[1] + B[2]   =>   B[0] += B[1] + B[2]

与此同时还需要注意另外2个地方：

初始状态和结束状态需要由正向运行时的from1337 to 185078700变为from 185078700 to 1337；

随机数的生成顺序也需要逆序开始，从最后一个开始往前逐个使用；

而在具体实现的过程中还发现了第3个需要注意的地方，如下存在2处Math.random调用的state分支：

假设进入该state时，正向程序在调用random时所用的随机数序列是：

…

0.4929938026657028 # if (Math.random() < 0.5)

0.9419549483892964 # Math.random() * 256

…

在做逆向运行时，程序不能像其他地方一样粗暴地从先前定义PSEUDO_RANDOMS队列中从后往前取，这样会变成：

…

0.9419549483892964 # if (Math.random() < 0.5)

0.4929938026657028 # Math.random() * 256

…

这会使得程序走向错误的分支，参与逻辑运算的随机数也将由原本的0.9419549483892964变为0.4929938026657028。因此，针对这种在if语句中也调用了Math.random的分支逻辑，需要保证该分支下的随机数使用顺序和正向运行时的相同。即，仍然保证如下的调用顺序：

…

0.4929938026657028 # if (Math.random() < 0.5)

0.9419549483892964 # Math.random() * 256

…

这可以通过适当调整PSEUDO_RANDOMS中的部分随机数序列顺序实现。

至此，完全逆向运行从target得到input的方案就可以实施了：

完整代码详见：https://gist.github.com/renzhexigua/34f09dd09b6a5cba05b04fcbef7dea92

Anyway，尽管使用了这种方法解决了这道题，但或许存在更优的解决方法。

八、backdoor

8.1 writeup

这道题结合使用反射+动态生成方法+异常三种手段来增加调试和逆向难度，使得直接使用dnSpy工具既没法静态分析部分函数IL实现，亦无法对部分函数或IL指令进行动态调试。

最直观的表现就是当对某些函数进行反编译的时候会提示decompile error或IL不合法。原因在于，程序会在运行时通过flared_71和flared_67两组函数动态更新其他异常函数的IL指令从而恢复函数功能的正常运行，因此最好的办法是能在运行前就确认这些存在异常问题的函数最终运行时的IL指令代码，将其复原正确。

恢复的关键点则在于对DynamicILInfo.GetTokenFor函数的理解：

Gets a token, valid in the scope of the current DynamicILInfo, representing a string, field, method, type, or signature in the MSIL stream for the associated dynamic method.

以flared_71为例，通过GetTokenFor(value)求得的tokenFor值，其“作用域”仅在当前dynamicILInfo中可见：

倘若我们直接拿求得的tokenFor去patch程序，则因为该值在当前assemble下无意义，因此反编译得到的函数（如flared_70）可能会变成如下这种样子：

即，会出现依次调用flare_01/02/03/04…的情况。

而倘若我们是拿keyValuePair.Value的值去patch相应的字段，则恢复出来的函数（如flared_70）是下面这个样子：

以C#形式解释的话，则是：

这才是对于当前assemble而言正确的token映射关系。

注意到这一问题之后，接下来恢复程序就变得容易许多。恢复后的程序实际是通过DGA方式来实现后门程序的命令下发和执行结果回传。

其关键操作在于flared_56函数中，当程序接收到符合特定顺序的DNS响应后，会使用RC4解密名为5aeb2b97的section中的数据：

解密后的数据是一张gif图片，其中包含了flag信息：

符合其约束条件且能触发程序执行到解密gif操作的一组DNS响应序列为：

192.168.1.1

192.0.0.2

43.50.0.0

192.0.0.3

43.49.48.0

192.0.0.2

43.56.0.0

192.0.0.3

43.49.57.0

192.0.0.3

43.49.49.0

192.0.0.2

43.49.0.0

192.0.0.3

43.49.53.0

192.0.0.3

43.49.51.0

192.0.0.3

43.50.50.0

192.0.0.3

43.49.54.0

192.0.0.2

43.53.0.0

192.0.0.3

43.49.50.0

192.0.0.3

43.50.49.0

192.0.0.2

43.51.0.0

192.0.0.3

43.49.56.0

192.0.0.3

43.49.55.0

192.0.0.3

43.50.48.0

192.0.0.3

43.49.52.0

192.0.0.2

43.57.0.0

192.0.0.2

43.55.0.0

192.0.0.2

43.52.0.0

九、encryptor

9.1 writeup

程序使用RSA结合chacha20的方式实现文件加密，两者参与的阶段分别是：

0x4022A3：首先，随机生成用以进行chacha20对称加密的32字节key和12字节nonce（4字节block counter全0），而后对目标文件进行加密

0x 4016CC：接着，使用RSA的私钥(d, n)对上一步参与chacha20加密的key、counter、nonce进行加密，将加密后的密文、私钥(d,n)追加到文件末位

上述过程中，有别于RSA常见加密逻辑的地方在于此处是使用私钥进行加密：

且计算产生私钥d的时候亦使用的是默认推荐的e=65537（0x10001）值。如此一来，可以直接使用e=65537对密文进行解密：

c：0x5a04e95cd0e9bf0c8cdda2cbb0f50e7db8c89af791b4e88fd657237c1be4e6599bc4c80fd81bdb007e43743020a245d5f87df1c23c4d129b659f90ece2a5c22df1b60273741bf3694dd809d2c485030afdc6268431b2287c597239a8e922eb31174efcae47ea47104bc901cea0abb2cc9ef974d974f135ab1f4899946428184c

e：65537

n：0xdc425c720400e05a92eeb68d0313c84a978cbcf47474cbd9635eb353af864ea46221546a0f4d09aaa0885113e31db53b565c169c3606a241b569912a9bf95c91afbc04528431fdcee6044781fbc8629b06f99a11b99c05836e47638bbd07a232c658129aeb094ddaf4c3ad34563ee926a87123bc669f71eb6097e77c188b9bc9

使用pow(c, e, n)即可解密得到代表明文m的由key、counter、nonce组成的chacha20 initial state，内容如下：

65 78 70 61 6E 64 20 33 32 2D 62 79 74 65 20 6B expand 32-byte k

01 b0 97 a1 2a 39 fc 42 05 24 a2 e7 75 a7 43 c9

28 d5 a5 50 b1 87 9a a8 b4 15 57 1e 38 32 9b 98

00 00 00 00 02 49 fc 0f c8 33 40 fe 4d 92 8f 95

对位于SuspiciousFile.txt.Encrypted开头的73字节内容进行chacha20解密即可得到flag信息：

package main

import (

“fmt”

“golang.org/x/crypto/chacha20”

)

func main() {

key := []byte{

0x01, 0xb0, 0x97, 0xa1, 0x2a, 0x39, 0xfc, 0x42, 0x05, 0x24, 0xa2, 0xe7, 0x75, 0xa7, 0x43, 0xc9,

0x28, 0xd5, 0xa5, 0x50, 0xb1, 0x87, 0x9a, 0xa8, 0xb4, 0x15, 0x57, 0x1e, 0x38, 0x32, 0x9b, 0x98,

}

nonce := []byte{

0x02, 0x49, 0xfc, 0x0f, 0xc8, 0x33, 0x40, 0xfe, 0x4d, 0x92, 0x8f, 0x95,

}

ciphertext := []byte{

0x7F, 0x8A, 0xFA, 0x63, 0x65, 0x9C, 0x5E, 0xF6, 0x9E, 0xB9, 0xC3, 0xDC, 0x13, 0xE8, 0xB2, 0x31,

0x3A, 0x8F, 0xE3, 0x6D, 0x94, 0x86, 0x34, 0x21, 0x46, 0x2B, 0x6F, 0xE8, 0xAD, 0x30, 0x8D, 0x2A,

0x79, 0xE8, 0xEA, 0x7B, 0x66, 0x09, 0xD8, 0xD0, 0x58, 0x02, 0x3D, 0x97, 0x14, 0x6B, 0xF2, 0xAA,

0x60, 0x85, 0x06, 0x48, 0x4D, 0x97, 0x0E, 0x71, 0xEA, 0x82, 0x06, 0x35, 0xBA, 0x4B, 0xFC, 0x51,

0x8F, 0x06, 0xE4, 0xAD, 0x69, 0x2B, 0xE6, 0x25, 0x5B,

}

plaintext := make([]byte, len(ciphertext))

cipher, _ := chacha20.NewUnauthenticatedCipher(key, nonce)

cipher.XORKeyStream(plaintext, ciphertext)

fmt.Printf(“%s”, plaintext)

}

十、Nur geträumt

10.1 writeup

Mini vMac搭建部分可参考：知乎《使用 Mini vMac 搭建一个 System 7.0 虚拟机》

https://zhuanlan.zhihu.com/p/57342369

分析本题时所使用的环境信息如下：

Minivmac-36.04-wx64（Mini vMac.exe）

1986-03 – 4D1F8172 – MacPlus v3.ROM（128KB vMac.ROM）

需注意，Mini vMac可能会无法识别Nur geträumt.img文件名，因此可将img重命名后挂载。

根据简单的尝试，发现输出与输入存在某种异或关联。使用内置的Super ResEdit查看68K汇编指令，在Modules中同样发现相关端倪：

另外还看到一个名为Flag的资源：

Name中包含一个“99 Luftballons”的提示线索1。

而后在TEXT资源中找到另外一份提示线索2：

线索3则来自于题目名称本身，Nur geträumt。Nur geträumt和99 Luftballons均来自Nena这套专辑。

因为password与flag之间存在xor关系，而flag末尾格式已知，因此可以手动试验出末尾几位的password取值：

Hast du etwas Zeit所异或得到的flag内容为：dich@flare-on.com。这两个推导出来的内容均来自于99 Luftballons歌词：

由于最终flag内容应为可打印字符序列，因而可多加几次测试验证是否可进一步推出其他password内容。

经过几轮测试，发现这里实际采用的是循环异或编码，参与异或的password实为99 Luftballons第一句完整歌词的变形体：

但这里的flag内容中包含有德文，直接提交后提示错误。尝试将ü改为u后重新提交，服务器验证通过。

十一、The challenge that shall not be named.

11.1 writeup

11.exe运行后，从行为监控软件上观察到该程序会尝试通过本地的代理端口向www.evil.flare-on.com提交一段flag数据，内容如下：

因此解密的关键就在于要找到flag被加密前的内容是什么。

使用PE类检查工具发现文件11.exe是由PyInstaller打包生成的，故而可使用PyInstaller Extractor结合python-uncompyle6的常规方法对11.exe进行解包，得到11.py文件内容如下：

需注意，PyInstaller Extractor在解包时提示原程序是在Python 3.7运行环境下所创建的，因此尽量选择在同版本的Python环境下进行解包和反编译操作，否则可能会出现提取失败的问题：

11.py所引入的pytransform为开源的Python加固工具，其支持多种加密和保护模式。根据该线索在互联网上找到一篇早期的分析文章：SoderCTF – Rev6: Unpacking PyArmor（https://devilinside.me/blogs/unpacking-pyarmor），参考该文章中介绍的inspect方法（本体选择对socket.py进行修改），能直接在No.11栈帧中找到flag解密后的痕迹，如下图所示：

与此同时还能看到base64、RC4、PyArmor_Pr0tecteth_My_K3y等字样，推测编码逻辑为RC4加密后再进行base64编码。进一步测试后得到验证：

十二、结语

本届挑战赛共计11道题目，涵盖Windows、JavaScript、.Net、Python、68K Macintosh等不同领域的技术点，当所有的挑战通过后会提示如下：

每年Flare-On挑战赛的题目大都来源于厂商遇到的真实事件以及研究员们的最近研究成果，这些题目对于专注于漏洞研究、样本分析、应急响应、CTF等领域的专业人员或爱好者来说都是非常有价值的参考资料。通过不断的参与，不断发现自身需要提高的技能，并保持对所关注领域最新趋势热点及资讯的敏锐度和参与度，相信可以让自己的眼界和能力更上一层楼。

根据大家在 Twitter 上的反馈，今年比赛有挑战难度的 2 个题目是：8. backdoor 和 7.anode。前者是一道 .Net 程序额外增加了一些反静态分析和调试的技巧，而后者则是一道纯 JS 逆向题目。想要解出这两道题目可能都需要花些功夫，感兴趣的小伙伴们可以试试看。

期待下一年！

原文始发于绿盟科技：逆向心法修炼之道 FLARE ON 9TH WRITEUP

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c51ec2207.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c5361999c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c53dc304b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c54696632.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c54f27179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c559d512e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c56413878.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c56fe8c83.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c57ba705e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6371c583af073.png)