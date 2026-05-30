# 破译APK口令，解锁知识宝藏：大狗Unlock活动优质经验分享

> 原文: https://www.ctfiot.com/223172.html
> ID: 223172

<大狗unlock>

“大狗Unlock：输入口令解锁豪华大奖！”活动圆满落幕。在此次活动中，参与者通过解密特定的APK，获取隐藏在其中的flag口令，深入信息的海洋，抽丝剥茧，从看似混乱的数据中挖掘隐秘的真相。不仅赢得了丰厚的奖励，还收获了满满的知识与经验。

在后续的经验分享阶段，知察社区共出现了来自 6 名用户的 8 份精彩经验分享贴。感谢所有参与者的热情支持，特别是10***9、dd***m、dyy01***9、13***0、mumuzi 和 Ra*****n 这 6 位用户的用心分享，让整个活动更加丰富多彩。

接下来，我们将分享 mumuzi 用户撰写的经验贴。他针对此次活动中的 5 个APK题目进行了全面而详细的分析与讲解，提供了实用的解题思路和操作步骤。让我们一起交流学习吧！

大狗Unlock 1-5题全题解

静态题解 + 动态题解

大狗的真机平台挺好用的，特别是在用frida的时候方便了许多。

题目一

静态解题

将APK拖入jadx打开，我们找到资源文件中的Androidmanifest.xml文件，通过定位android.intent.category.LAUNCHER找出启动后的位置是在com.nosugar.dagou_challenge_01.MainActivity。

AndroidManifest.xml是 Android应用的核心配置文件，用来描述应用的基本信息、权限、组件及其相互关系。

通过定位到该类后，找到与flag输出有关的函数，图上我对函数都进行了解释。

那么我们可以自己写一个脚本来运行它，这里的python脚本。

1def transform_string(): 2    original_string = "Yvbjp{Pigjf_CJJF_0s1}" 3    transformed_string = [] 4 5    for char in original_string: 6        if char < 'a' or char > 'z':  # 非小写字母 7            if 'A' <= char <= 'Z':  # 大写字母 8                char = chr(ord(char) - 21) 9                if char < 'A':  # 超出范围则补偿 2610                    char = chr(ord(char) + 26)11            # 非字母直接加入结果12            transformed_string.append(char)13        else:  # 小写字母14            char = chr(ord(char) - 21)15            if char < 'a':  # 超出范围则补偿 2616                char = chr(ord(char) + 26)17            transformed_string.append(char)1819    result = ''.join(transformed_string)20    print(result)2122transform_string()23#运行得到结果Dagou{Unlok_HOOK_0x1}

动态解题

静态分析很简单，但是我们需要学会用frida等工具来尝试动态解题，这里我们使用大狗平台-云真机加载该APK，编写frida。

我们打开jadx，找到get_random函数，右键点击复制为frida片段。

接着我们把脚本写入大狗平台的脚本里，并启动软件，点击加载脚本后，勾选重启APP。

我们就可以得到随机数值，接着计算i*2+4即可得到我们的输入i2，提交得到flag。

题目二

静态解题

同样的，我们找到Androidmanifest.xml文件，定位android.intent.category.LAUNCHER。

找到该类后，查看静态代码。

知道了key和密文以及加密算法之后，就可以直接解密，我们使用cyberchef（赛博厨子），即可直接得到flag。

动态解题

同样的，我们也要学习动态解题的方法，依旧是在我们的云真机操作台上运行该软件。然后查看代码，能够发现需要验证code。

右击Checker.code，选择复制为frida片段，复制下来的内容是这样的：

1let Checker = Java.use("com.nosugar.dagou_challenge_03.Checker");2code = Checker.code.value;

但是我们要他的值是512，就需要自己赋值，改成以下内容：

1let Checker = Java.use("com.nosugar.dagou_challenge_03.Checker");2Checker.code.value=512;

运行该frida脚本并重启APP后，点击软件里面的 Click me! 即可获得flag。

题目三

静态解题

通过上面两个题目的练习，相信大家已经了解了如何定位找到主函数、如何使用frida进行简单的解题。

仔细分析MainActivity类，发现该类只是做了一个界面布局，让我们运行软件看看，确实只有一个Hello Hackers，其他什么都没有。

接着我们还发现他还定义了一个Check类，里面有个get_flag函数。

根据逻辑，我们直接进行异或就可以得到flag，这里也是使用的cyberchef。

动态解题

由于该APK中并没有自身去调用Check类的，因此我们在写frida脚本的时候需要自己去进行调用，首先我们先复制Check这里为frida片段。

得到的内容是：

1let Check = Java.use("com.nosugar.dagou_challenge_04.Check");

然后我们创建他的实例：

1let checkInstance = Check.$new();

接着传入值并输出：

1let result = checkInstance.get_flag(1337);2console.log(result);

综合起来的代码如下：

1// 获取目标类2let Check = Java.use("com.nosugar.dagou_challenge_04.Check");3// 创建目标类的实例4let checkInstance = Check.$new();5// 调用目标方法并传入参数 13376let result = checkInstance.get_flag(1337);7// 输出返回的结果8console.log(result);

题目四

静态解题

和之前的解题方式相同，先找到入口。

跳转过去之后直接就能找到flag验证部分。

如果满足则自动解这段AES获取flag，我们手动解密即可获取，注意key选UTF-8，输入为原始输入，模式是ECB。

动态解题

我们使用大狗的云真机操作台，启动之后看看。

就是一个什么都没有的hello world，我们之前找到了get_flag，我们全局搜一下这个，看看其他地方是否有他的调用。

能够发现只有他自己进行了定义，但是没有进行调用，与我们昨天的题目类似，但是num的定义是在Check类里面，我们这里一步步来。

首先，假设我们直接写一个调用的脚本，如下：

1Java.perform(function() { 2  var Checker = Java.use('com.nosugar.dagou_challenge_06.Checker'); 3  var MainActivity = Java.use('com.nosugar.dagou_challenge_06.MainActivity'); 4  MainActivity.get_flag.overload('com.nosugar.dagou_challenge_06.Checker').implementation = function(checker) { 5    checker.num1.value = 1234; 6    checker.num2.value = 4321; 7    this.get_flag(checker); 8  }; 910  var checker = Checker.$new();1112  checker.num1.value = 1234;13  checker.num2.value = 4321;14  var activity = MainActivity.$new();15  activity.get_flag(checker);16});

运行之后会发现报错：Error: java.lang.RuntimeException: Can’t create handler inside thread Thread[Thread-2,10,main] that has not called Looper.prepare()这是由于在 Android 开发中，UI 操作必须在主线程（也称为 UI 线程）上执行。我们的get_flag方法里面最后一句是this.f163t1.setText，他涉及到了对TextView的更新，是典型的UI操作，那么就必须在UI线程上进行，如果在非主线程上运行，就会遇到上面的报错。因此我们可以写出这个脚本：

1Java.perform(function () { 2  var Checker = Java.use("com.nosugar.dagou_challenge_06.Checker"); 3 4  Java.choose("com.nosugar.dagou_challenge_06.MainActivity", { 5    onMatch: function (instance) { 6      var checker = Checker.$new(); 7      checker.num1.value = 1234; 8      checker.num2.value = 4321; 910      Java.scheduleOnMainThread(function () {11        instance.get_flag(checker);12      });13    }14  });15});

首先，开头的：

1Java.perform(function ()

为了确保脚本与应用的 Java 环境同步，避免出现报错：ClassNotFoundException:
com.nosugar.dagou_challenge_06.MainActivity，接着使用了Java.use，确保脚本中可用。

1var Checker = Java.use("com.nosugar.dagou_challenge_06.Checker");

接下来，使用了onMatch。

1var checker = Checker.$new();2checker.num1.value = 1234;3checker.num2.value = 4321;

这段的作用是查找并枚举应用中所有com.nosugar.dagou_challenge_06.MainActivity类的实例。

接着的checker就是修改值。

1var checker = Checker.$new();2checker.num1.value = 1234;3checker.num2.value = 4321;

最关键的Java.scheduleOnMainThread(function ()的作用就是让其在UI线程（主线程）上运行。

1Java.scheduleOnMainThread(function () {2  instance.get_flag(checker);3});

总结：

获取 Checker 类：通过 Java.use 获取 Checker 类的引用，以便创建和修改其实例。

查找 MainActivity 实例：使用 Java.choose 查找并枚举所有 MainActivity 实例。

修改 Checker 实例： 

● 创建 Checker 类的新实例。

● 设置 num1 和 num2 为满足条件的值（1234 和 4321）。

调用 get_flag 方法：

● 使用 Java.scheduleOnMainThread 将 get_flag 方法的调用调度到主线程上，确保 UI 操作的线程安全性。

● 传递修改后的 Checker 实例给 get_flag，触发逻辑判断并显示 flag。

题目五

这里静态分析没有做出来，虽然找到一个APP_ID的点并且要解AES，但是那个貌似和题目无关。

然后呢如果单纯是说为了得到flag而得，可以不用做题，直接看报告，这一点呢平台没考虑到位。

编者注：这里题目设计的时候，第一位用户使用云真机提取出APP_ID之前，报告里还没有记录，mumuzi 老师分析的时候，由于当天已经有用户做出来，平台收录之后，才会出现的答案。

然后有一部分人找到的__UNI__*******实际是APP_KEY，并不是APP_ID。能够在内置脚本中找到一个常见的SDK分析，试了之后发现软件显示没有网络连接，加入不了房间。

在本地用模拟器我进去也显示网络链接失败。

根据在社区里面搜索，发现大狗在7月份发布过该云会议的文章，因此进行学习：nosugar://apps/NsKnowledgeBaseAnswer/index.html#/questions/10010000000003024。

我们需要使用在线的js解混淆网站，这里我使用的不是文章里面的那个网站，我用的是：https://deobfuscatejavascript.com/#

将assetsapps__UNI__942333Ewwwapp-service.js的文件进行解混淆，然后找到isTrueVersion。

注意到这里的date要等于version，而version是20240921，因此我们需要在真机里面修改时间到20240921。

能够成功进入，但是现在无法找到会议室，我们假设输入一个12345。

通过搜索，定位到：

发现房间号是5位纯数字或者6位纯数字，接着分析，发现定义了一个参数 m。

再根据下面的内容：

发现实际是这样的：

字符替换：

● mixStr 和 _keyStr 是提供的字符集，在 Python 中建立了一个映射 mix_to_key_map 来执行字符替换。

● 在 decode64 函数中，我们遍历输入的字符串，并使用映射表将每个字符从 mixStr 转换为 _keyStr 中对应的字符。

Base64 解码：

● 使用 base64.b64decode 进行标准的 Base64 解码。解码后的数据会以字节形式返回。

UTF-8 编码转换：

● 解码后的字节数据通过 .decode(‘utf-8’) 转换成原始的字符串。

我们可以得到这个脚本：

1import base64 2 3
# 自定义字符集 4_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" 5mixStr = "嵝飬麾斡闇灓楼鲰陙真尡灑崐轜戾皽樓傠鑮扌稌陹渀圂脙攪漇媧蓨脶鯃憭唺勌閍低譽椻踂憘啚溬侇€騅繖聍紌萁蝊郝囓莻犠■倕氬蚻熘齥挎捒饊襪" 6 7
# 创建字符替换的映射字典 8mix_to_key_map = {mixStr[i]: _keyStr[i] for i in range(len(mixStr))} 910def decode64(input_str):11
# 替换自定义字符集12replaced_str = ''.join([mix_to_key_map.get(ch, ch) for ch in input_str])1314
# Base64 解码15decoded_bytes = base64.b64decode(replaced_str)1617
# 将解码后的字节转换为 UTF-8 字符串18return decoded_bytes.decode('utf-8')1920
# 测试解密 m 对象中的数据21m = {22    1: "崐犠陙郝戾楼脙倕崐踂崐■脙低陙郝轜楼灓譽攪扌勌踂崐斡蓨倕戾扌稌蝊脙郝飬勌戾渀崐紌崐扌勌齥憭鲰紌萁崐楼崐紌脙犠轜譽轜渀稌郝戾扌稌囓崐楼樓郝脙低飬踂崐郝闇紌轜低勌椻攪楼崐莻攪扌椻踂轜唺襪襪",23    2: "轜渀樓萁脙渀闇氬崐渀真椻轜犠稌萁轜斡陙萁攪渀真椻攪低蓨囓攪渀闇犠攪低蓨紌轜低灓低攪斡飬齥憭鲰紌郝攪斡真閍崐渀闇■轜渀陙倕攪斡脙囓攪低譽犠戾扌闇倕脙扌真勌攪斡闇郝崐扌崐倕攪扌陹椻崐紌襪襪",24    3: "崐楼闇蝊崐犠稌萁轜犠樓倕戾斡蓨犠轜楼陙囓轜踂闇郝轜斡蓨郝脙低蓨氬脙犠脙莻崐渀稌倕脙扌轜齥憭鲰紌蝊攪踂崐萁轜郝唺紌崐渀轜閍攪低陙囓攪斡嵝蝊脙渀脙氬戾斡稌蝊戾楼陙萁戾扌譽蝊戾斡攪閍攪唺襪襪",25    4: "轜渀樓囓轜踂攪踂崐郝飬椻脙踂闇萁轜斡嵝倕攪踂真踂轜斡譽紌戾楼脙囓戾斡蓨蝊轜犠闇犠戾斡灓齥憭鲰萁勌攪扌勌椻攪斡崐倕轜低唺犠攪扌嵝囓轜低唺萁脙踂陹譽轜斡嵝倕崐斡蓨■攪斡脶勌崐扌脙萁轜嵝襪襪",26    5: "轜扌樓■崐踂稌犠轜楼崐紌轜扌稌萁轜楼闇萁攪扌譽犠脙渀崐犠脙踂脙倕崐踂陙蝊戾斡譽囓戾楼灓齥憭鲰紌萁崐郝唺莻脙犠樓囓脙郝唺萁戾楼崐囓崐扌闇郝戾斡灓閍脙低崐倕戾楼陙蝊戾楼崐萁轜犠崐■攪嵝襪襪",27}2829
# 测试解密30for key in m:
31decrypted = decode64(m[key])32print(f"Decrypted m[{key}] = {decrypted}")

👇点击阅读原文，即可下载无糖浏览器


```
1def transform_string(): 2    original_string = "Yvbjp{Pigjf_CJJF_0s1}" 3    transformed_string = [] 4 5    for char in original_string: 6        if char < 'a' or char > 'z':  # 非小写字母 7            if 'A' <= char <= 'Z':  # 大写字母 8                char = chr(ord(char) - 21) 9                if char < 'A':  # 超出范围则补偿 2610                    char = chr(ord(char) + 26)11            # 非字母直接加入结果12            transformed_string.append(char)13        else:  # 小写字母14            char = chr(ord(char) - 21)15            if char < 'a':  # 超出范围则补偿 2616                char = chr(ord(char) + 26)17            transformed_string.append(char)1819    result = ''.join(transformed_string)20    print(result)2122transform_string()23#运行得到结果Dagou{Unlok_HOOK_0x1}
1let Checker = Java.use("com.nosugar.dagou_challenge_03.Checker");2code = Checker.code.value;
1let Checker = Java.use("com.nosugar.dagou_challenge_03.Checker");2Checker.code.value=512;
1let Check = Java.use("com.nosugar.dagou_challenge_04.Check");
1let checkInstance = Check.$new();
1let result = checkInstance.get_flag(1337);2console.log(result);
1// 获取目标类2let Check = Java.use("com.nosugar.dagou_challenge_04.Check");3// 创建目标类的实例4let checkInstance = Check.$new();5// 调用目标方法并传入参数 13376let result = checkInstance.get_flag(1337);7// 输出返回的结果8console.log(result);
1Java.perform(function() { 2  var Checker = Java.use('com.nosugar.dagou_challenge_06.Checker'); 3  var MainActivity = Java.use('com.nosugar.dagou_challenge_06.MainActivity'); 4  MainActivity.get_flag.overload('com.nosugar.dagou_challenge_06.Checker').implementation = function(checker) { 5    checker.num1.value = 1234; 6    checker.num2.value = 4321; 7    this.get_flag(checker); 8  }; 910  var checker = Checker.$new();1112  checker.num1.value = 1234;13  checker.num2.value = 4321;14  var activity = MainActivity.$new();15  activity.get_flag(checker);16});
1Java.perform(function () { 2  var Checker = Java.use("com.nosugar.dagou_challenge_06.Checker"); 3 4  Java.choose("com.nosugar.dagou_challenge_06.MainActivity", { 5    onMatch: function (instance) { 6      var checker = Checker.$new(); 7      checker.num1.value = 1234; 8      checker.num2.value = 4321; 910      Java.scheduleOnMainThread(function () {11        instance.get_flag(checker);12      });13    }14  });15});
1Java.perform(function ()
1var Checker = Java.use("com.nosugar.dagou_challenge_06.Checker");
1var checker = Checker.$new();2checker.num1.value = 1234;3checker.num2.value = 4321;
1var checker = Checker.$new();2checker.num1.value = 1234;3checker.num2.value = 4321;
1Java.scheduleOnMainThread(function () {2  instance.get_flag(checker);3});
1import base64 2 3
# 自定义字符集 4_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" 5mixStr = "嵝飬麾斡闇灓楼鲰陙真尡灑崐轜戾皽樓傠鑮扌稌陹渀圂脙攪漇媧蓨脶鯃憭唺勌閍低譽椻踂憘啚溬侇€騅繖聍紌萁蝊郝囓莻犠■倕氬蚻熘齥挎捒饊襪" 6 7
# 创建字符替换的映射字典 8mix_to_key_map = {mixStr[i]: _keyStr[i] for i in range(len(mixStr))} 910def decode64(input_str):11
# 替换自定义字符集12replaced_str = ''.join([mix_to_key_map.get(ch, ch) for ch in input_str])1314
# Base64 解码15decoded_bytes = base64.b64decode(replaced_str)1617
# 将解码后的字节转换为 UTF-8 字符串18return decoded_bytes.decode('utf-8')1920
# 测试解密 m 对象中的数据21m = {22    1: "崐犠陙郝戾楼脙倕崐踂崐■脙低陙郝轜楼灓譽攪扌勌踂崐斡蓨倕戾扌稌蝊脙郝飬勌戾渀崐紌崐扌勌齥憭鲰紌萁崐楼崐紌脙犠轜譽轜渀稌郝戾扌稌囓崐楼樓郝脙低飬踂崐郝闇紌轜低勌椻攪楼崐莻攪扌椻踂轜唺襪襪",23    2: "轜渀樓萁脙渀闇氬崐渀真椻轜犠稌萁轜斡陙萁攪渀真椻攪低蓨囓攪渀闇犠攪低蓨紌轜低灓低攪斡飬齥憭鲰紌郝攪斡真閍崐渀闇■轜渀陙倕攪斡脙囓攪低譽犠戾扌闇倕脙扌真勌攪斡闇郝崐扌崐倕攪扌陹椻崐紌襪襪",24    3: "崐楼闇蝊崐犠稌萁轜犠樓倕戾斡蓨犠轜楼陙囓轜踂闇郝轜斡蓨郝脙低蓨氬脙犠脙莻崐渀稌倕脙扌轜齥憭鲰紌蝊攪踂崐萁轜郝唺紌崐渀轜閍攪低陙囓攪斡嵝蝊脙渀脙氬戾斡稌蝊戾楼陙萁戾扌譽蝊戾斡攪閍攪唺襪襪",25    4: "轜渀樓囓轜踂攪踂崐郝飬椻脙踂闇萁轜斡嵝倕攪踂真踂轜斡譽紌戾楼脙囓戾斡蓨蝊轜犠闇犠戾斡灓齥憭鲰萁勌攪扌勌椻攪斡崐倕轜低唺犠攪扌嵝囓轜低唺萁脙踂陹譽轜斡嵝倕崐斡蓨■攪斡脶勌崐扌脙萁轜嵝襪襪",26    5: "轜扌樓■崐踂稌犠轜楼崐紌轜扌稌萁轜楼闇萁攪扌譽犠脙渀崐犠脙踂脙倕崐踂陙蝊戾斡譽囓戾楼灓齥憭鲰紌萁崐郝唺莻脙犠樓囓脙郝唺萁戾楼崐囓崐扌闇郝戾斡灓閍脙低崐倕戾楼陙蝊戾楼崐萁轜犠崐■攪嵝襪襪",27}2829
# 测试解密30for key in m:
31decrypted = decode64(m[key])32print(f"Decrypted m[{key}] = {decrypted}")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736339418.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736339420.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736339422.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736339424.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/3-1736339425.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736339426.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736339428.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736339430.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736339432.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/3-1736339433.png)