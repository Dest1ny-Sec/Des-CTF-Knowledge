# ACTF flutter逆向学习

> 原文: https://www.ctfiot.com/169656.html
> ID: 169656

参考了许多大佬的博客，在此特别诚挚感谢oacia大佬和其他大佬的博客和指导！1.flutter和apk基础结构介绍

首先下载附件，是一个apk文件，用jadx打开

可以看见flutter字样，而flutter是一种目前比较流行的android框架，很多app都是用的该框架构建，而该原生框架是建立在app的native层。

Android的系统架构采用了分层架构的思想。从下往上依次分为Linux内核、硬件抽象层（HAL）、系统Native库和Android运行时环境、Java框架层以及应用层这5层架构，其中每一层都包含大量的子模块或子系统

而平时我们接触到的都是应用层和Java框架层，包括用Jadx对apk进行逆向时也只是在逆向Java层的逻辑。如果想要逆向native层，就需要对android进行解包

apk本身是一个包，压缩了运行时的依赖、配置文件以及native库，也就是.so，将apk文件后缀名修改成.zip后，即可解压查看这些文件

也可以使用androidkiller这个工具对apk进行分析、修改

最基础的app配置文件放在AndroidManifest.xml，这个文件里面存放的有app的很多配置，如该题的配置情况如下，可以在这个文件里面看到该应用的包名，名称、SDK的版本等等信息，这些信息在app取证里面很有用，对之后的动态调试SO层也有很大帮助。

<?xml version=”1.0″ encoding=”utf-8″ standalone=”no”?><manifest xmlns:android=”http://schemas.android.com/apk/res/android” android:compileSdkVersion=”33″ android:compileSdkVersionCodename=”13″ package=”com.example.flutter_application_1″ platformBuildVersionCode=”33″ platformBuildVersionName=”13″>

<application android:appComponentFactory=”androidx.core.app.CoreComponentFactory” android:icon=”@mipmap/ic_launcher” android:label=”flutter_application_1″ android:name=”android.app.Application”>

<activity android:configChanges=”density|fontScale|keyboard|keyboardHidden|layoutDirection|locale|orientation|screenLayout|screenSize|smallestScreenSize|uiMode” android:exported=”true” android:hardwareAccelerated=”true” android:launchMode=”singleTop” android:name=”com.example.flutter_application_1.MainActivity” android:theme=”@style/LaunchTheme” android:windowSoftInputMode=”adjustResize”>

<meta-data android:name=”io.flutter.embedding.android.NormalTheme” android:resource=”@style/NormalTheme”/>

<intent-filter>

<action android:name=”android.intent.action.MAIN”/>

<category android:name=”android.intent.category.LAUNCHER”/>

</intent-filter>

</activity>

<meta-data android:name=”flutterEmbedding” android:value=”2″/>

<uses-library android:name=”androidx.window.extensions” android:required=”false”/>

<uses-library android:name=”androidx.window.sidecar” android:required=”false”/>

</application>

</manifest>

至于其他的文件夹，大家可以自行查阅，这里就不一一说明。

而native层的.so文件就放在lib的几个文件夹里面

这三个文件夹分别代表了不同架构的.so文件。我们如果想用真机调试.so文件，那么就要用真机对应的架构，不能乱用。

2.blutter安装以及使用

接下来把lib文件进行解包，因为flutter使用的是dart语言，并且采用了dartVM的方法进行拍摄快照，所以我们现在要使用一些工具对.so文件进行快照解析，市面上对flutter的逆向工具都是这个原理。

但是有一个问题，dart快照是可以更改的，随着DartSdk版本的更新，reflutter和flutter逆向助手已经停止更新，这次的这个题flutterSDK过高，两个工具都无法破解，于是找到了blutter这个工具

官方地址：

https://github.com/worawit/blutter

用git把blutter.py拉进kali里面(如果拉不进就直接到GitHub上下zip解压就行)，然后安装依赖。

sudo apt install python3-pyelftools python3-requests git cmake ninja-build \

build-essential pkg-config libicu-dev libcapstone-dev

若报错如下

说明你该更新你的apt源了

sudo apt-get update

下载完成情况如图

接下来就可以用这个工具了，将解压后的app放进虚拟机，在blutter目录下运行.py文件，注意有两个参数，前一个参数是.so文件所在的其中一个目录，后一个参数是结果输出目录

若成功会解析稍微长一点的时间，耐心等待即可，如果有下图结果即为解析完成

完成后在输出目录会有五个文件和文件夹

按照作者的说法，分别对应的是

objs.txt：对象池中对象的完整（嵌套）转储，在这里我理解成对象池里面的方法和相应的偏移量

blutter_frida.js：这个是用于对该flutter程序hook的js代码，应用在frida这个工具里面(接下来会讲到)

ida_script：这个文件夹装的是.so文件的符号表还原脚本，因为dart语言是依靠偏移量识别函数的，所以也能依靠偏移量还原函数

asm：对dart语言的反编译结果，里面有很多dart源代码的对应偏移

3.动态调试flutter程序

接下来就是利用frida工具hook插桩以及动态调试破解该程序了

环境：具有python环境的win10系统、kali系统

设备：pixel3(需要root)

重点：必须是欧版，如果不是欧版OEM无法打开，不可能刷的了机

具体root过程参考https://sspai.com/post/76276

工具：adb调试桥、IDA7.7工具

3.1.下载adb

https://blog.csdn.net/x2584179909/article/details/108319973

3.2.运行IDA

注意，在此之前需要将chall.apk修改成可调试状态

具体方法为利用androidkiller打开程序->在AndroidManifest.xml里面第二行插入

android:debuggable=”true”

如果程序SDK版本比较老，这样就可以，但是这个程序的targetSdkVersion是33，是高版本，签名会出问题，所以在apktool.xml改成27或者28即可

两处改好后就可以进行编译，得到新的程序。

完成后即可安装到手机上

adb install chall_killer.apk

查看自己的手机是什么架构可以用下列代码

adb shell getprop ro.product.cpu.abi

在ida的下图文件夹内找到android_server64(我的真机架构是arm64位的)

连接手机(手机上打开USB调试)，打开终端，利用adb程序在手机上下载chall.apk，安装完成后把之前找到的server文件push到手机里执行

adb push android_server64 /data/local/tmp/as

adb shell

su #加载手机root权限

cd /data/local/tmp/

chmod 777 as #给server文件可读可写可执行权限

./as -p 12345 #用12345端口运行server

如果运行成功会有一个正在监听的提示，说明这个命令端已经成为了server端监听了

接下来重新开启一个命令行，adb转发端口

adb forward tcp:12345 tcp:12345

保持收发端口一致后启动ida，将libapp.so放进ida

用刚才blutter解析得到的addName.py还原符号表

得到了符号表之后，查看解析的asm里面的main.dart，查找主程序里面的函数

在flutter官网查找四个函数的含义均为dart的API

表单交互 (Forms)

https://flutter.cn/docs/cookbook/forms

或者可以在这篇博客上找到

Flutter基建 – 按钮全解析 – 掘金

https://juejin.cn/post/7300771357524885554

onChanged()：这个API在删除或插入文本的时候的回调函数

onSubmitted()：当用户完成文本输入并按下键盘上的“完成”按钮时的回调函数

onLongPressed()：在屏幕上保持了一段时间

onTap()：用户点击事件完成(点击提交按钮时)

现在查看我们的程序，可以看见这个程序的窗口组成，而最重要的应该是提交按钮，对应的也就是onTap()回调函数所做的

所以直接过滤器查找这个函数(也可以直接用之前在main.dart里面找到的函数地址)

回调函数在0xE03C4处

之后我们查看程序发现有256这个变量

再加上这里很明显的RC4加密流程

可以大概得知这是一个RC4加密。

3.3.frida工具hook key值

接下来需要用到frida工具，frida是一款基于python + java 的hook框架，可运行在android、ios、linux、win、osx等各平台，主要使用动态二进制插桩技术。

安装部分可以看这里

frida安装正确流程

https://www.yuque.com/fuxuqiannian/zrregp/kpmsyb4qu5ecn4so?singleDoc#

上面步骤中用blutter解析快照时，工具自动帮我们写了一个插桩脚本，叫做blutter_frida.js，只需要在下图所示部分修改成上面有RC4加密的函数地址，即可hook出密文

改完之后使用frida加载这个js脚本

frida -U -f com.example.flutter_application_1 -l blutter_frida.js

随便输入点什么执行程序即可hook得到密文

3.4.动态调试部分

现在可以调试一下我们的apk应用程序

首先打开应用debug模式，如果上面的androidkiller如果不行，可以用面具开，具体流程如下图

adb shell

su

magisk resetprop ro.secure 0

magisk resetprop ro.debuggable 1

getprop ro.debuggable #如果回显为1则已经开启

stop

start #上面两步重启手机

这个时候下载monitor(DDMS)用于观察程序进程是否开启(如果是真机可能不需要这一步)

此电脑

打开monitor.bat，可以看见设备上的进程

这个时候挂起程序

jdb -connect com.sun.jdi.SocketAttach:hostname=127.0.0.1,port=8639

运行结果如下图

如果有报错 致命错误:无法附加到目标 VM。

那可能是端口搞错了，这里要填写的是应用程序的端口，而不是adb运行server的端口。

运行成功的话monitor里面程序那行进程栏会显示为绿色

接下来进行调试，调试设置如下图

设置完成点击Attach to process…进行附加程序调试，附加我们的程序即可

现在先找密钥，而密钥是RC4加密的异或操作下的变量，我们把断点下在异或的指令上

f9断到这个地方之后可以看见X2变量是有赋值的，我们利用trace跟踪该变量，并将值都打印出来

import idc

print(idc.ger_reg_value(‘X2′),’,’,end=”)

此处点击运行直接跳过，跳过后发现手机上能够输入了，这个时候输入字符(字符个数可以往前看用frida工具hook出来的key数量)然后点√

感谢oacia师傅的提示，如果不点√就f9不会有输入，程序会一直卡在第一个异或的密钥上

这个是第一个异或的密钥，但是如果检查下来发现密文和这个密钥异或之后得不到输入，重新检查一下会发现还要异或一个0xff即可

addr = [14, 14, 68, 80, 29, 201, 241, 46, 197, 208, 123, 79, 187, 55, 234, 104, 40, 117, 133, 12, 67, 137, 91, 31, 136,

177, 64, 234, 24, 27, 26, 214, 122, 217]

key = [184,

132,

137,

215,

146,

65,

86,

157,

123,

100,

179,

131,

112,

170,

97,

210,

163,

179,

17,

171,

245,

30,

194,

144,

37,

41,

235,

121,

146,

210,

174,

92,

204,

22

]

flag = “”

for i in range(len(addr)):

flag += chr(addr[i] ^ 0xff ^ key[i])

print(flag)

4.本文知识点来源

https://bbs.kanxue.com/thread-279403.htm

https://www.jianshu.com/p/8db31a8f45cd

https://www.52pojie.cn/thread-1847985-1-1.html

https://sspai.com/post/76276

https://blog.csdn.net/x2584179909/article/details/108319973

https://www.yuque.com/fuxuqiannian/zrregp/kpmsyb4qu5ecn4so?singleDoc#

https://juejin.cn/post/7300771357524885554

https://flutter.cn/docs/cookbook/forms

原文始发于Marc Ilunga：ACTF flutter逆向学习

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a208f1bbac.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a2085d46a5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a2074900af.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a204cc2c1b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a2026c2be7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a1fc51734b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a1fabae458.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a1ee1312ba.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a1eabb22be.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/img_660a1e7e8a96f.png)