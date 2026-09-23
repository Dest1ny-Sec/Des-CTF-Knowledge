---
title: NepnepxCATCTF CatPaw 题目详解 (Android 小米备份 + 触摸事件)
contest: NepnepxCATCTF
year: 2023
difficulty: hard
vuln_type: reverse
tags:
- Android 小米备份
- 7zip
- /dev/input/event1 触摸事件
- Frida hook LoginDataSource
- X/Y 03003500/03003600
attack_chain: '|'
key_payload: '|'
one_liner: 'NepnepxCATCTF CatPaw: Android 小米备份 + Frida hook 绕 login + /dev/input/event1 触摸事件还原画图。'
lesson: '|'
quality: high
full_path: NepnepxCATCTF-CatPaw题目详解.full.md
meta_path: NepnepxCATCTF-CatPaw题目详解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'NepnepxCATCTF CatPaw 题目详解 (Android 小米备份 + 触摸事件)。NepnepxCATCTF CatPaw: Android 小米备份 + Frida hook 绕 login + /dev/input/event1 触摸事件还原画图。。经验：|'
category: reverse
subcategory: reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/89529.html
reasoning_chain:
- CatPaw 题拿到小米备份文件 → 触发点：7zip 打开得到 apk
- 对 apk 分析 → 加密代码只需 md5 == 8b9b0ad9c324204fac87ae0fc2c630bd
- 假设：hook LoginDataSource.login 直接通过 → 动作：Frida 脚本
- 观察：hook 后显示通过但不给 flag → 假设：flag 不在 login 后
- so 中读取 /dev/input/event1 → 触发点：触摸事件保存到应用目录
- 动作：getevent -lt /dev/input/event1 抓数据 + cat 模拟输入 → 观察：得到 1666666666
- 假设：解析触摸事件坐标 → 动作：分析 16 进制 03003500/03003600 = X/Y
- 动作：写 Python 脚本提取 X/Y 坐标 → 观察：得到画图坐标序列
- 假设：坐标还原出图案 = flag → 动作：matplotlib 画图 → 观察：flag 图样
failed_attempts:
- 直接 Frida hook login 拿 flag → 失败：flag 在触摸图案非 login
- 用小米手机模拟输入 → 失败：非小米设备报错
- 不解 X/Y 方向只画单点 → 失败：必须 XY 配对
key_observations:
- 小米备份文件可 7zip 直接打开
- Frida hook 绕过 login 但 flag 不在 hook 后
- /dev/input/event1 是 Android 触摸事件设备
- X 事件码 03003500 / Y 事件码 03003600
- 触摸坐标还原图案是 Android 逆向常见思路
prerequisites:
- Android APK 反编译（jadx）
- Frida hook 脚本编写
- Linux input 子系统（/dev/input/event*）
- 7zip 解压与文件分离
---
# NepnepxCATCTF-CatPaw题目详解

> 原文: https://www.ctfiot.com/89529.html
> ID: 89529

CatPaw

小米备份文件，可以用7zip打开得到apk

对apk进行分析，跳转到加密代码，通过分析代码，发现只需要最后的md5值和8b9b0ad9c324204fac87ae0fc2c630bd相等即可

同时资源中又发现password必须大于5位

一开始的想法是hook上面的方法，认为通过验证后能拿到flag

脚本如下

setImmediate(function() {Java.perform(function() { var targetClass='nep.zxc.catpaw.data.LoginDataSource'; var methodName='login'; var gclass = Java.use(targetClass); gclass[methodName].overload("java.lang.String").implementation = function(arg0) { var loginUser = Java.use("nep.zxc.catpaw.data.model.LoggedInUser").$new("12345","admin"); //hook内部类 var resultClass = Java.use("nep.zxc.catpaw.data.Result$Success"); var ret = resultClass.$new(loginUser); return ret; }})})

hook之后是直接显示通过，并没有给出flag

之后在so中发现读取/dev/input/event1并保存在应用目录下

利用命令即可模拟输入

一次输入是CatC，大概是因为输入的时候报错了，我的手机并不是小米手机，只是刷了MIUI系统，可能是这个原因导致报错，没有全部输入完成

转换思路，通过阅读文章https://blog.seeflower.dev/archives/45/，发现可以分析文件指令，先通过命令getevent -lt /dev/input/event1和命令cat 1666666666 >> /dev/input/event1可以抓取文件未报错部分的信息

可以看到上图中按下的坐标值，根据坐标值搜索文件的16进制数据，可以发现两个指令，指令03003500代表X轴，指令03003600代表Y轴

依次写出脚本提取所有的坐标

def get_x(v): x = [] for i in range(4): tmp = str(hex(v[i+4]))[2:] if len(tmp) == 1: tmp = "0" + tmp     x.append(tmp) x.reverse() ret = "" for v in x:  ret += v return int(ret,16)def get_y(v):  y = []   for i in range(4):    tmp = str(hex(v[i+4]))[2:]    if len(tmp) == 1:    tmp = "0" + tmp    y.append(tmp)    y.reverse()    ret = ""    for v in y:    ret += v    return int(ret,16)def is_y(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x36 and v[3] == 0x00: return True return Falsedef is_x(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x35 and v[3] == 0x00: return True return Falsewith open("1666666666","rb") as fr: rd = fr.read()for i in range(16,len(rd),24): v = rd[i:i+8] x = 0 y = 0 if is_x(v): x = get_x(v) print(x,end=",") if is_y(v): y = get_y(v) print(y)
# 622,319
# 83,1901
# 472,1904
# 81,1892
# 133,1739
# 493,1603
# 62,1892
# 443,502,1601
# 450,1755
# 97,1903
# 107,2064
# 293,1622
# 487,1620
# 635,1751
# 271,1601
# 83,2086
# 1011,1626
# 65,1919
# 453,1913
# 386,1438
# 500,1588
# 84,2021
# 1015,1630
# 87,2074
# 465,1902
# 489,1446
# 90,2042
# 1028,1611
# 77,1897
# 417,1599
# 77,1903
# 286,1613
# 438,1912
# 1032,1491
# 388,1615
# 325,1758
# 804,1623
# 82,1895
# 765,1908
# 920,1464
# 76,2056
# 1016,1635
# 89,2060
# 769,1763
# 431,1912
# 385,1614
# 290,1435
# 1437
# 756,1933
# 95,2051
# 1021,1647
# 648,1906
# 593,1597
# 86,2069
# 1029,1649
# 817,1615
# 767,1899
# 83,1919
# 1043,1643
# 79,1909
# 715,1611
# 492,1625
# 89,2090
# 1040,1632
# 289,1607
# 542,1918
# 81,1935
# 292,1580
# 80,1909
# 756,1922
# 711,1466
# 83,2021
# 392,1605
# 587,781

提取的数据中出现两个问题，可以看到少了两条数据，443没有对应的Y轴，1437没有对应的X轴

干脆先把两者互补一下，都是443,1437，利用adb进行模拟点击

adb shell input tap 622 319adb shell input tap 83 1901adb shell input tap 472 1904adb shell input tap 81 1892adb shell input tap 133 1739adb shell input tap 493 1603adb shell input tap 62 1892adb shell input tap 443 1437adb shell input tap 502 1601adb shell input tap 450 1755adb shell input tap 97 1903adb shell input tap 107 2064adb shell input tap 293 1622adb shell input tap 487 1620adb shell input tap 635 1751adb shell input tap 271 1601adb shell input tap 83 2086adb shell input tap 1011 1626adb shell input tap 65 1919adb shell input tap 453 1913adb shell input tap 386 1438adb shell input tap 500 1588adb shell input tap 84 2021adb shell input tap 1015 1630adb shell input tap 87 2074adb shell input tap 465 1902adb shell input tap 489 1446adb shell input tap 90 2042adb shell input tap 1028 1611adb shell input tap 77 1897adb shell input tap 417 1599adb shell input tap 77 1903adb shell input tap 286 1613adb shell input tap 438 1912adb shell input tap 1032 1491adb shell input tap 388 1615adb shell input tap 325 1758adb shell input tap 804 1623adb shell input tap 82 1895adb shell input tap 765 1908adb shell input tap 920 1464adb shell input tap 76 2056adb shell input tap 1016 1635adb shell input tap 89 2060adb shell input tap 769 1763adb shell input tap 431 1912adb shell input tap 385 1614adb shell input tap 290 1435adb shell input tap 443 1437adb shell input tap 756 1933adb shell input tap 95 2051adb shell input tap 1021 1647adb shell input tap 648 1906adb shell input tap 593 1597adb shell input tap 86 2069adb shell input tap 1029 1649adb shell input tap 817 1615adb shell input tap 767 1899adb shell input tap 83 1919adb shell input tap 1043 1643adb shell input tap 79 1909adb shell input tap 715 1611adb shell input tap 492 1625adb shell input tap 89 2090adb shell input tap 1040 1632adb shell input tap 289 1607adb shell input tap 542 1918adb shell input tap 81 1935adb shell input tap 292 1580adb shell input tap 80 1909adb shell input tap 756 1922adb shell input tap 711 1466adb shell input tap 83 2021adb shell input tap 392 1605adb shell input tap 587 781

本次点击的效果如下，很明显不符合flag的形式，其次是443,1437，显示的是5，第一个5显而易见是C，将坐标改成C的坐标即可

然而即使CatCTF{thepC4T_!5_RecprdiN9_$cr35n”by”inLutpev{N7}，那也很奇怪了，并且md5校验不通过

通过打开安卓的触控指针位置并进行录屏，对每次点击的位置进行分析

利用PotPlayer对视频进行逐帧分析，发现每次点击都在键盘偏下的位置，因此需要减少Y轴的值，通过不断调试，发现减少25最为合适

同时注意到了1437这个没有X坐标的值，这个高度位于数字区，也就是说如果5不正确，最多再试9次，依旧能获得正确的值

修改后代码如下

def get_x(v): x = []  for i in range(4):   tmp = str(hex(v[i+4]))[2:] if len(tmp) == 1: tmp = "0" + tmp x.append(tmp) x.reverse() ret = "" for v in x: ret += v return int(ret,16)def get_y(v): y = [] for i in range(4): tmp = str(hex(v[i+4]))[2:] if len(tmp) == 1: tmp = "0" + tmp y.append(tmp) y.reverse() ret = "" for v in y: ret += v return int(ret,16)def is_y(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x36 and v[3] == 0x00: return True return False
def is_x(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x35 and v[3] == 0x00: return True return Falsewith open("1666666666","rb") as fr: rd = fr.read()for i in range(16,len(rd),24): v = rd[i:i+8] x = 0 y = 0 if is_x(v): x = get_x(v) print(x,end=",") if is_y(v): y = get_y(v) print(y-25)

修改后的脚本如下

adb shell input tap 622 294adb shell input tap 83 1876adb shell input tap 472 1879adb shell input tap 81 1867adb shell input tap 133 1714adb shell input tap 493 1578adb shell input tap 62 1867adb shell input tap 472 1879adb shell input tap 502 1576adb shell input tap 450 1730adb shell input tap 97 1878adb shell input tap 107 2039adb shell input tap 293 1597adb shell input tap 487 1595adb shell input tap 635 1726adb shell input tap 271 1576adb shell input tap 83 2061adb shell input tap 1011 1601adb shell input tap 65 1894adb shell input tap 453 1888adb shell input tap 386 1413adb shell input tap 500 1563adb shell input tap 84 1996adb shell input tap 1015 1605adb shell input tap 87 2049adb shell input tap 465 1877adb shell input tap 489 1421adb shell input tap 90 2017adb shell input tap 1028 1586adb shell input tap 77 1872adb shell input tap 417 1574adb shell input tap 77 1878adb shell input tap 286 1588adb shell input tap 438 1887adb shell input tap 1032 1466adb shell input tap 388 1590adb shell input tap 325 1733adb shell input tap 804 1598adb shell input tap 82 1870adb shell input tap 765 1883adb shell input tap 920 1439adb shell input tap 76 2031adb shell input tap 1016 1610adb shell input tap 89 2035adb shell input tap 769 1738adb shell input tap 431 1887adb shell input tap 385 1589adb shell input tap 290 1410adb shell input tap 443 1412adb shell input tap 756 1908adb shell input tap 95 2026adb shell input tap 1021 1622adb shell input tap 648 1881adb shell input tap 593 1572adb shell input tap 86 2044adb shell input tap 1029 1624adb shell input tap 817 1590adb shell input tap 767 1874adb shell input tap 83 1894adb shell input tap 1043 1618adb shell input tap 79 1884adb shell input tap 715 1586adb shell input tap 492 1600adb shell input tap 89 2065adb shell input tap 1040 1607adb shell input tap 289 1582adb shell input tap 542 1893adb shell input tap 81 1910adb shell input tap 292 1555adb shell input tap 80 1884adb shell input tap 756 1897adb shell input tap 711 1441adb shell input tap 83 1996adb shell input tap 392 1580adb shell input tap 587 756

本次运行效果如下，这次就有点像样了，不过这串的md5值还是不匹配

那很简单了，将$cr35n的5用其他数字进行替换，最终在替换为3时，md5值成功匹配

在app中进行验证，成功攻破

结果为CatCTF{the_C4T_!5_Rec0rdiN9_$cr33n_by_inPut_evEn7}

招新小广告

2023年招新计划(主力/NMEGREZ)

注：不限年龄与职业要求，只要不是纯小白(或者是初学者未参与过任何一场比赛的人)就有机会通过审核，天权信安对外长期招新，出色的师傅能够参与团队项目和竞赛项目建设。

PWN：要求技术中等偏上（曾参与过省级/国家级网安赛事荣获过奖项的师傅优先考虑）

REVERSE：要求技术中等（曾参与过省级/国家级网安赛事荣获过奖项的师傅优先考虑）

CRYPTO：要求技术中等偏上

WEB：要求技术中等偏上

取证：曾参与过省级网安取证赛事荣获过奖项的师傅

BLOCKCHAIN/IOT/工控/AI：要求技术中等

CTF竞赛靶场/TQCTF练习平台运维师傅：若干名，熟悉docker操作、动态题目部署、以及常规运维，还具备组网部署经验和Linux、Windows系统部署和日常维护，能使靶场平台在各种环境中正常运行。

 欢迎联系：

投递邮箱：megrez@megrezsec.cn（Evan师傅）

–天权信安网络安全团队–

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！


```
setImmediate(function() {Java.perform(function() { var targetClass='nep.zxc.catpaw.data.LoginDataSource'; var methodName='login'; var gclass = Java.use(targetClass); gclass[methodName].overload("java.lang.String").implementation = function(arg0) { var loginUser = Java.use("nep.zxc.catpaw.data.model.LoggedInUser").$new("12345","admin"); //hook内部类 var resultClass = Java.use("nep.zxc.catpaw.data.Result$Success"); var ret = resultClass.$new(loginUser); return ret; }})})
def get_x(v): x = [] for i in range(4): tmp = str(hex(v[i+4]))[2:] if len(tmp) == 1: tmp = "0" + tmp     x.append(tmp) x.reverse() ret = "" for v in x:  ret += v return int(ret,16)def get_y(v):  y = []   for i in range(4):    tmp = str(hex(v[i+4]))[2:]    if len(tmp) == 1:    tmp = "0" + tmp    y.append(tmp)    y.reverse()    ret = ""    for v in y:    ret += v    return int(ret,16)def is_y(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x36 and v[3] == 0x00: return True return Falsedef is_x(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x35 and v[3] == 0x00: return True return Falsewith open("1666666666","rb") as fr: rd = fr.read()for i in range(16,len(rd),24): v = rd[i:i+8] x = 0 y = 0 if is_x(v): x = get_x(v) print(x,end=",") if is_y(v): y = get_y(v) print(y)
# 622,319
# 83,1901
# 472,1904
# 81,1892
# 133,1739
# 493,1603
# 62,1892
# 443,502,1601
# 450,1755
# 97,1903
# 107,2064
# 293,1622
# 487,1620
# 635,1751
# 271,1601
# 83,2086
# 1011,1626
# 65,1919
# 453,1913
# 386,1438
# 500,1588
# 84,2021
# 1015,1630
# 87,2074
# 465,1902
# 489,1446
# 90,2042
# 1028,1611
# 77,1897
# 417,1599
# 77,1903
# 286,1613
# 438,1912
# 1032,1491
# 388,1615
# 325,1758
# 804,1623
# 82,1895
# 765,1908
# 920,1464
# 76,2056
# 1016,1635
# 89,2060
# 769,1763
# 431,1912
# 385,1614
# 290,1435
# 1437
# 756,1933
# 95,2051
# 1021,1647
# 648,1906
# 593,1597
# 86,2069
# 1029,1649
# 817,1615
# 767,1899
# 83,1919
# 1043,1643
# 79,1909
# 715,1611
# 492,1625
# 89,2090
# 1040,1632
# 289,1607
# 542,1918
# 81,1935
# 292,1580
# 80,1909
# 756,1922
# 711,1466
# 83,2021
# 392,1605
# 587,781
adb shell input tap 622 319adb shell input tap 83 1901adb shell input tap 472 1904adb shell input tap 81 1892adb shell input tap 133 1739adb shell input tap 493 1603adb shell input tap 62 1892adb shell input tap 443 1437adb shell input tap 502 1601adb shell input tap 450 1755adb shell input tap 97 1903adb shell input tap 107 2064adb shell input tap 293 1622adb shell input tap 487 1620adb shell input tap 635 1751adb shell input tap 271 1601adb shell input tap 83 2086adb shell input tap 1011 1626adb shell input tap 65 1919adb shell input tap 453 1913adb shell input tap 386 1438adb shell input tap 500 1588adb shell input tap 84 2021adb shell input tap 1015 1630adb shell input tap 87 2074adb shell input tap 465 1902adb shell input tap 489 1446adb shell input tap 90 2042adb shell input tap 1028 1611adb shell input tap 77 1897adb shell input tap 417 1599adb shell input tap 77 1903adb shell input tap 286 1613adb shell input tap 438 1912adb shell input tap 1032 1491adb shell input tap 388 1615adb shell input tap 325 1758adb shell input tap 804 1623adb shell input tap 82 1895adb shell input tap 765 1908adb shell input tap 920 1464adb shell input tap 76 2056adb shell input tap 1016 1635adb shell input tap 89 2060adb shell input tap 769 1763adb shell input tap 431 1912adb shell input tap 385 1614adb shell input tap 290 1435adb shell input tap 443 1437adb shell input tap 756 1933adb shell input tap 95 2051adb shell input tap 1021 1647adb shell input tap 648 1906adb shell input tap 593 1597adb shell input tap 86 2069adb shell input tap 1029 1649adb shell input tap 817 1615adb shell input tap 767 1899adb shell input tap 83 1919adb shell input tap 1043 1643adb shell input tap 79 1909adb shell input tap 715 1611adb shell input tap 492 1625adb shell input tap 89 2090adb shell input tap 1040 1632adb shell input tap 289 1607adb shell input tap 542 1918adb shell input tap 81 1935adb shell input tap 292 1580adb shell input tap 80 1909adb shell input tap 756 1922adb shell input tap 711 1466adb shell input tap 83 2021adb shell input tap 392 1605adb shell input tap 587 781
def get_x(v): x = []  for i in range(4):   tmp = str(hex(v[i+4]))[2:] if len(tmp) == 1: tmp = "0" + tmp x.append(tmp) x.reverse() ret = "" for v in x: ret += v return int(ret,16)def get_y(v): y = [] for i in range(4): tmp = str(hex(v[i+4]))[2:] if len(tmp) == 1: tmp = "0" + tmp y.append(tmp) y.reverse() ret = "" for v in y: ret += v return int(ret,16)def is_y(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x36 and v[3] == 0x00: return True return False
def is_x(v): if v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x35 and v[3] == 0x00: return True return Falsewith open("1666666666","rb") as fr: rd = fr.read()for i in range(16,len(rd),24): v = rd[i:i+8] x = 0 y = 0 if is_x(v): x = get_x(v) print(x,end=",") if is_y(v): y = get_y(v) print(y-25)
adb shell input tap 622 294adb shell input tap 83 1876adb shell input tap 472 1879adb shell input tap 81 1867adb shell input tap 133 1714adb shell input tap 493 1578adb shell input tap 62 1867adb shell input tap 472 1879adb shell input tap 502 1576adb shell input tap 450 1730adb shell input tap 97 1878adb shell input tap 107 2039adb shell input tap 293 1597adb shell input tap 487 1595adb shell input tap 635 1726adb shell input tap 271 1576adb shell input tap 83 2061adb shell input tap 1011 1601adb shell input tap 65 1894adb shell input tap 453 1888adb shell input tap 386 1413adb shell input tap 500 1563adb shell input tap 84 1996adb shell input tap 1015 1605adb shell input tap 87 2049adb shell input tap 465 1877adb shell input tap 489 1421adb shell input tap 90 2017adb shell input tap 1028 1586adb shell input tap 77 1872adb shell input tap 417 1574adb shell input tap 77 1878adb shell input tap 286 1588adb shell input tap 438 1887adb shell input tap 1032 1466adb shell input tap 388 1590adb shell input tap 325 1733adb shell input tap 804 1598adb shell input tap 82 1870adb shell input tap 765 1883adb shell input tap 920 1439adb shell input tap 76 2031adb shell input tap 1016 1610adb shell input tap 89 2035adb shell input tap 769 1738adb shell input tap 431 1887adb shell input tap 385 1589adb shell input tap 290 1410adb shell input tap 443 1412adb shell input tap 756 1908adb shell input tap 95 2026adb shell input tap 1021 1622adb shell input tap 648 1881adb shell input tap 593 1572adb shell input tap 86 2044adb shell input tap 1029 1624adb shell input tap 817 1590adb shell input tap 767 1874adb shell input tap 83 1894adb shell input tap 1043 1618adb shell input tap 79 1884adb shell input tap 715 1586adb shell input tap 492 1600adb shell input tap 89 2065adb shell input tap 1040 1607adb shell input tap 289 1582adb shell input tap 542 1893adb shell input tap 81 1910adb shell input tap 292 1555adb shell input tap 80 1884adb shell input tap 756 1897adb shell input tap 711 1441adb shell input tap 83 1996adb shell input tap 392 1580adb shell input tap 587 756
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