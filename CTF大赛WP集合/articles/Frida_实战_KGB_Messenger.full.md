---
title: Frida 实战 KGB Messenger
contest: KGB Messenger CTF App
year: 2024
difficulty: medium
vuln_type: reverse
tags:
- frida
- android
- kgb
- russia
- system-getProperty
- base64
- login
- ctf-app
attack_chain:
- '第1关: hook System.getProperty("user.home") 强制返回"Russia'
- '第2关: hook System.getenv(String) 返回"FLAG{57ERL1NG_4RCH3R}" base64'
- '解码: base64 -d "RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==" → FLAG{57ERL1NG_4RCH3R}'
- '第3关: 用户名codenameduchess登录'
- '第4关: hook LoginActivity.j() 强制true'
- '后续关卡: 算法反推+Frida hook'
key_payload: FLAG{57ERL1NG_4RCH3R}
one_liner: Frida闯关KGB Messenger：4关hook俄罗斯判断+base64密码+登录
lesson: Frida实战CTF App：System.getProperty/Environment反俄判断
quality: high
full_path: Frida_实战_KGB_Messenger.full.md
meta_path: Frida_实战_KGB_Messenger.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'Frida 实战 KGB Messenger。Frida闯关KGB Messenger：4关hook俄罗斯判断+base64密码+登录。关键路径：第1关: hook System.getProperty("user.home") 强制返回"Russia → 第2关: hook System.getenv(String) 返回"FLAG{57ERL1NG_4RCH3R}" base6...'
category: reverse
subcategory: reverse
tools_used:
- Frida
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/169480.html
reasoning_chain:
- 触发点：APP 启动提示 'This app can only run on Russian devices' → 假设：判断 user.home
- 动作：jadx 反编译 → 观察：System.getProperty('user.home')=='Russia' 判断
- 动作：Frida Java.use('java.lang.System').getProperty.overload('java.lang.String').implementation = function(s){ return 'Russia'; }
- 观察：第一关通过 → 第二关：getenv 判断 base64 密码 → 触发点：FLAG base64
- 假设：System.getenv 返回 base64 字符串 → 动作：base64 -d 'RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==' → 观察：FLAG{57ERL1NG_4RCH3R}
- 动作：Frida system.getenv.overload('java.lang.String').implementation = function(s){ return 'RkxBR3s1...'; } → 观察：第二关通过
- 第三关：登录界面 → 假设：R.string.username = codenameduchess → 动作：adb shell input text 'codenameduchess'
- 第四关：j() 函数 false → 假设：必须 true → 动作：Frida LoginActivity.j.implementation = function(){ return true; }
- 第五关：聊天消息 a(obj).equals(this.p) → 假设：a(str) 是 XOR+swap 算法 → 动作：写 Python 还原 a() → 观察：拿到正确输入
failed_attempts:
- 试图改 user.home 环境变量 → 失败：Android app 不读 env
- 试图 base64 解码 → 观察出 base64 但未用 Frida
- 试图修改 jadx 反编译 → 失败：必须重新签名重打包
key_observations:
- Frida hook System.getProperty / System.getenv 是 Android 通用绕过手法
- KGB Messenger 闯关式 CTF App，每关独立 hook 点
- XOR+swap 算法 a(str) 是 CTF 经典反推题型
- Frida implementation 替换返回值比修改 smali 快
- R.string.username 通过反编译可拿到硬编码用户
prerequisites:
- Frida Java hook 基础
- Android jadx 反编译
- Base64 编解码
- XOR 加密 + 字符串 swap 算法
---
# Frida 实战 KGB Messenger

> 原文: https://www.ctfiot.com/169480.html
> ID: 169480

一

前言

KGB Messenger是一个类似闯关的APP，有很多关卡，通过的方法有很多种，这里我们主要用frida进行闯关。中间有很多关于算法的实现和反推演的过程，其实对于新手还是很有挑战的，当然了对于我来说也是很有挑战的，接下分享下通关的思路和方法。

二

第一关

打开APP，映入眼前的就是 This app can only run on Russian devices.的提示报错，如果不解决这个，后面将无法进行，我们将APP拖入jadx进行分析。

搜索到目标代码，我们分析发现 System.getProperty(“user.home”) = Russia 即可满足条件进入下一关。

System.getProperty(String name)方法用于得到系统的属性.System是在lang包中的一个类，这个类中存在大量和系统打交道的实用方法，而且一般都是类方法，.getProperty(String key)就是其中一个比较常用的方法，用于返回系统参数文件中这个方法指定键所代表的值。

var system = Java.use("java.lang.System");
 system.getProperty.overload('java.lang.String').implementation = function (str) {
 var re = this.getProperty(str);
 return "Russia";
 }

三

第二关

var system = Java.use("java.lang.System");
 system.getenv.overload('java.lang.String').implementation = function (str) {
 console.log("system.getenv : ", str)
 var re = this.getenv(str);
 console.log("system.getenv.re : ", re)
 return "RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==";
 }

四

第三关

来到这一关是一个登录界面，随便输入账号密码，提示：User not recognized.，看来登录是有文章的，我们查看代码分析。

通过第二关的分析，我们很容容易找到了R.string.username = codenameduchess

adb shell input text 'codenameduchess'

五

第四关

随便输入密码 会提示 Incorrect password.，查看上面的图片我们可以知道，j()这函数是关键，满足true这个条件，即可跳入到下一关。

让结果强行改true.

var LoginActivity = Java.use("com.tlamb96.kgbmessenger.LoginActivity");
 LoginActivity["j"].implementation = function () {
 var ret = this.j();
 return true;
 };

六

第五关

来到这一关，我们进入到一个消息聊天界面，发送消息是没有反馈的，看代码：

this.o.add(new com.tlamb96.kgbmessenger.b.a(R.string.user, obj, j(), false));这个是发送消息的模板，true是对方发送的，flase代表我发发送的消息。当然了这段代码和解密无关，但是地了解它的发送逻辑，排除掉无关的代码。a(obj.toString()).equals(this.p)是闯关的关键。

p=”V@]EAASBu0012WZFu0012e,a$7(&am2(3.u0003″;输入的值经过a方法，返回值等于p值即可进入下一关。

a()：

private String a(String str) {
 char[] charArray = str.toCharArray();
 for (int i = 0; i < charArray.length / 2; i++) {
 char c = charArray[i];
 charArray[i] = (char) (charArray[(charArray.length - i) - 1] ^ '2');
 charArray[(charArray.length - i) - 1] = (char) (c ^ 'A');
 }
 return new String(charArray);
 }

这个a方法是一个算法，只要我们反推出这个算法，就知道应该输入什么值，遇到这样的问题，我觉得我们应该先还原算法，不要硬反推，应该这样很烧脑，很浪费时间，正向还原比反向推导要简单的多，我们安装他的逻辑进行编写即可。

再写算法之前，我们先了解下python的异或^运算。

chr()将数字（10进制）转化为中文

ord() 将中文转化为数字(10进制)

python a()还原：

def a(str_m):
 charArray2 = list(str_m)
 for ii in range(0, int(len(charArray2) / 2)):
 cc = charArray2[ii]
 print("ii ", ii, cc, " charArray2[ii] :", len(charArray2) - ii - 1, charArray2[len(charArray2) - ii - 1],
 chr(ord(charArray2[len(charArray2) - ii - 1]) ^ ord('2')), "charArray2[len(charArray2) - ii - 1] :",
 len(charArray2) - ii - 1, chr(ord(cc) ^ ord('A')))
 charArray2[ii] = chr(ord(charArray2[len(charArray2) - ii - 1]) ^ ord('2'))
 charArray2[len(charArray2) - ii - 1] = chr(ord(cc) ^ ord('A'))
 charArrayStr2 = "".join(charArray2)
 print("charArrayStr2:", charArrayStr2)
 return charArrayStr2

if __name__ == '__main__':
 str_m = "abcdef" # UTWd"
 # re = a(str_m)

“abcdef” 经过加密得到 #TWV”# ，当然了得必须验证下你得算法是否正确，万一写错误，不是陷入到了死胡同？所有hook a方法，输入 abcdef 看看打印的结果是不是TWV”#

var MessengerActivity = Java.use("com.tlamb96.kgbmessenger.MessengerActivity");
 MessengerActivity["a"].implementation = function (str) {
 console.log('a is called' + ', ' + 'str: ' + str);
 var ret = this.a(str);
 console.log('a ret value is ' + ret);
 return ret;
 };

结果：
a is called, str: abcdef
a ret value is TWV"#

得到了正向的加密，反推就简单多了，因为写了一遍，再反推和没写直接推演是不一样的。在这里我们要注意下 ^ 这个值的还原。记住这一点：当然也不一定对，欢迎批评指正，互相学习。

求y : x ^ '值' = y
 求x : y ^ '值' = x

反推算法：

def a_jie(str_m):
 str_m_fanzhuan = str_m[::-1]
 charArray2 = list(str_m_fanzhuan)
 for ii in range(0, int(len(charArray2) / 2)):
 cc = charArray2[ii]
 charArray2[ii] = chr(ord(charArray2[len(charArray2) - ii - 1]) ^ ord('2'))
 charArray2[len(charArray2) - ii - 1] = chr(ord(cc) ^ ord('A'))
 charArrayStr2 = "".join(charArray2)
 print("charArrayStr2:", charArrayStr2) # fedcba
 # 再反转：
 str_m_fanzhuan = charArrayStr2[::-1]
 print(str_m_fanzhuan)
 return str_m_fanzhuan

我们输入 TWV”# 得到值 ：abcedf 完全正确。这个时候我们再输入p值：

ss = "V@]EAASBu0012WZFu0012e,a$7(&am2(3.u0003"
re = a_jie(ss) # Boris, give me the password

返回结果：Boris, give me the password

输入 ：Boris, give me the password 即可进入到下一关。

七

第六关

第六关：

这一关的思路和第五关一样，他们的风控手段也是雷同的。主要是b(String str) = r = “u0000dslp}oQu0000 dks

b() 源码：

private String b(String str) {
 char[] charArray = str.toCharArray();
 for (int i = 0; i < charArray.length; i++) {
 charArray[i] = (char) ((charArray[i] >> (i % 8)) ^ charArray[i]);
 }
 for (int i2 = 0; i2 < charArray.length / 2; i2++) {
 char c = charArray[i2];
 charArray[i2] = charArray[(charArray.length - i2) - 1];
 charArray[(charArray.length - i2) - 1] = c;
 }
 return new String(charArray);
 }

b方法python正向还原：

def b(str_m):
 charArray = list(str_m)
 charArray2 = list(str_m)

 for i in range(len(charArray)):
 charArray[i] = chr((ord(charArray[i]) >> (i % 8)) ^ ord(charArray[i]))
 print(i,charArray2[i],charArray[i])
 print(charArray)
 for i2 in range(int(len(charArray) / 2)):
 c = charArray[i2]
 charArray[i2] = charArray[(len(charArray) - i2) - 1]
 charArray[(len(charArray) - i2) - 1] = c
 print(i2,c, charArray[i2], len(charArray) - i2 - 1,charArray[(len(charArray) - i2) - 1])
 print(charArray)
 charArrayStr2 = "".join(charArray)
 return charArrayStr2

我们发现以下代码是主要的加密位置，后面只是实现了一个倒序，只是他实现的过程比较复杂，如果用python 实现这个逻辑只要一行代码就行。废话不多说，只要实现以下代码的反推逻辑即可破解。

char[] charArray = str.toCharArray();
 for (int i = 0; i < charArray.length; i++) {
 charArray[i] = (char) ((charArray[i] >> (i % 8)) ^ charArray[i]);
 }

反推后的代码：

def b_jie(str_m):
 str_m = " 00dslp}oQ 00 dks$|M 00h +AYQg 00P*!M$gQ 00"
 charArray = list(str(str_m))
 print(str_m)
 charArray.reverse()
 print(charArray)
 for i in range(len(charArray)):
 if i % 8 == 0:
 print("_", end="")
 continue
 for ch in string.printable:
 final_ch = chr((ord(ch) >> (i % 8)) ^ ord(ch))
 if final_ch == charArray[i]:
 print(ch, end="")

结果：
['x00', 'Q', 'g', '$', 'M', '!', '*', 'P', 'x00', 'g', 'Q', 'Y', 'A', '+', ' ', 'h', 'x00', 'M', '|', '$', 's', 'k', 'd', ' ', 'x00', 'Q', 'o', '}', 'p', 'l', 's', 'd', 'x00']
_ay I *P_EASE* h_ve the _assword_

得到 ：补全单词：May I PLEASE  have the password

总体来说hook的逻辑还是简单的，代码相信大家都能看得懂，唯一的难度就是a和b方法的加密算法的还原。

看雪ID：西贝巴巴

https://bbs.kanxue.com/user-home-961239.htm

*本文为看雪论坛优秀文章，由 西贝巴巴 原创，转载请注明来自看雪社区

# 往期推荐

1、ELF文件脱壳纪事

2、Glibc-2.35下对tls_dtor_list的利用详解

3、对旅行APP的检测以及参数计算分析【Simplesign篇】

4、2023强网杯warmup题解

5、Directory Opus 13.2 逆向分析

6、Pwn-oneday题目解析

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
前言
二
第一关
var system = Java.use("java.lang.System");
 system.getProperty.overload('java.lang.String').implementation = function (str) {
 var re = this.getProperty(str);
 return "Russia";
 }
三
第二关
var system = Java.use("java.lang.System");
 system.getenv.overload('java.lang.String').implementation = function (str) {
 console.log("system.getenv : ", str)
 var re = this.getenv(str);
 console.log("system.getenv.re : ", re)
 return "RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==";
 }
四
第三关
adb shell input text 'codenameduchess'
五
第四关
var LoginActivity = Java.use("com.tlamb96.kgbmessenger.LoginActivity");
 LoginActivity["j"].implementation = function () {
 var ret = this.j();
 return true;
 };
六
第五关
private String a(String str) {
 char[] charArray = str.toCharArray();
 for (int i = 0; i < charArray.length / 2; i++) {
 char c = charArray[i];
 charArray[i] = (char) (charArray[(charArray.length - i) - 1] ^ '2');
 charArray[(charArray.length - i) - 1] = (char) (c ^ 'A');
 }
 return new String(charArray);
 }
chr()将数字（10进制）转化为中文

ord() 将中文转化为数字(10进制)
def a(str_m):
 charArray2 = list(str_m)
 for ii in range(0, int(len(charArray2) / 2)):
 cc = charArray2[ii]
 print("ii ", ii, cc, " charArray2[ii] :", len(charArray2) - ii - 1, charArray2[len(charArray2) - ii - 1],
 chr(ord(charArray2[len(charArray2) - ii - 1]) ^ ord('2')), "charArray2[len(charArray2) - ii - 1] :",
 len(charArray2) - ii - 1, chr(ord(cc) ^ ord('A')))
 charArray2[ii] = chr(ord(charArray2[len(charArray2) - ii - 1]) ^ ord('2'))
 charArray2[len(charArray2) - ii - 1] = chr(ord(cc) ^ ord('A'))
 charArrayStr2 = "".join(charArray2)
 print("charArrayStr2:", charArrayStr2)
 return charArrayStr2

if __name__ == '__main__':
 str_m = "abcdef" # UTWd"
 # re = a(str_m)
var MessengerActivity = Java.use("com.tlamb96.kgbmessenger.MessengerActivity");
 MessengerActivity["a"].implementation = function (str) {
 console.log('a is called' + ', ' + 'str: ' + str);
 var ret = this.a(str);
 console.log('a ret value is ' + ret);
 return ret;
 };

结果：
a is called, str: abcdef
a ret value is TWV"#
求y : x ^ '值' = y
 求x : y ^ '值' = x
def a_jie(str_m):
 str_m_fanzhuan = str_m[::-1]
 charArray2 = list(str_m_fanzhuan)
 for ii in range(0, int(len(charArray2) / 2)):
 cc = charArray2[ii]
 charArray2[ii] = chr(ord(charArray2[len(charArray2) - ii - 1]) ^ ord('2'))
 charArray2[len(charArray2) - ii - 1] = chr(ord(cc) ^ ord('A'))
 charArrayStr2 = "".join(charArray2)
 print("charArrayStr2:", charArrayStr2) # fedcba
 # 再反转：
 str_m_fanzhuan = charArrayStr2[::-1]
 print(str_m_fanzhuan)
 return str_m_fanzhuan
ss = "V@]EAASBu0012WZFu0012e,a$7(&am2(3.u0003"
re = a_jie(ss) # Boris, give me the password

返回结果：Boris, give me the password
七
第六关
private String b(String str) {
 char[] charArray = str.toCharArray();
 for (int i = 0; i < charArray.length; i++) {
 charArray[i] = (char) ((charArray[i] >> (i % 8)) ^ charArray[i]);
 }
 for (int i2 = 0; i2 < charArray.length / 2; i2++) {
 char c = charArray[i2];
 charArray[i2] = charArray[(charArray.length - i2) - 1];
 charArray[(charArray.length - i2) - 1] = c;
 }
 return new String(charArray);
 }
def b(str_m):
 charArray = list(str_m)
 charArray2 = list(str_m)

 for i in range(len(charArray)):
 charArray[i] = chr((ord(charArray[i]) >> (i % 8)) ^ ord(charArray[i]))
 print(i,charArray2[i],charArray[i])
 print(charArray)
 for i2 in range(int(len(charArray) / 2)):
 c = charArray[i2]
 charArray[i2] = charArray[(len(charArray) - i2) - 1]
 charArray[(len(charArray) - i2) - 1] = c
 print(i2,c, charArray[i2], len(charArray) - i2 - 1,charArray[(len(charArray) - i2) - 1])
 print(charArray)
 charArrayStr2 = "".join(charArray)
 return charArrayStr2
char[] charArray = str.toCharArray();
 for (int i = 0; i < charArray.length; i++) {
 charArray[i] = (char) ((charArray[i] >> (i % 8)) ^ charArray[i]);
 }
def b_jie(str_m):
 str_m = " 00dslp}oQ 00 dks$|M 00h +AYQg 00P*!M$gQ 00"
 charArray = list(str(str_m))
 print(str_m)
 charArray.reverse()
 print(charArray)
 for i in range(len(charArray)):
 if i % 8 == 0:
 print("_", end="")
 continue
 for ch in string.printable:
 final_ch = chr((ord(ch) >> (i % 8)) ^ ord(ch))
 if final_ch == charArray[i]:
 print(ch, end="")

结果：
['x00', 'Q', 'g', '$', 'M', '!', '*', 'P', 'x00', 'g', 'Q', 'Y', 'A', '+', ' ', 'h', 'x00', 'M', '|', '$', 's', 'k', 'd', ' ', 'x00', 'Q', 'o', '}', 'p', 'l', 's', 'd', 'x00']
_ay I *P_EASE* h_ve the _assword_
```


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