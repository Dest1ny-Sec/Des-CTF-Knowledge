# 【工控Writeup】2022河南工业互联网安全大赛复赛

> 原文: https://www.ctfiot.com/78419.html
> ID: 78419

HNGK-流量分析

打开过滤mms，然后直接搜索flag发现有个列目录的返回结果。

再往下找有个fileOpen的操作。

继续往后找也是上面这俩个操作，那么就过滤一下fileOpen的操作去拿打开后的标识符然后看看用哪了。有4次打开操作。

那就过滤出这几个的返回包，拿到标识符。

不过有个返回包没解析出来，先不管，看看能不能用过滤出来的三个标识符找到其fileFead操作。

成功找到，那就看看这个请求的响应是什么。结果没过滤出来东西。

猜测是wireshark没解析成功，那就去掉过滤看看下一个包是什么，这个流量包里的请求和响应都是挨在一起的。

似乎是因为长度没解析对。反正看见base64格式的图片了，先提取出来。发现图片内容就是flag。

flag{ICS-mms104}

HNGK-MMS拿到流量包后发现打不开，扔到010发现其实是个压缩包，于是再解压一次。

遍历一遍mms，发现有两条请求的item比较奇怪。

而66正好是f的ascii。

所以猜测可能是有位移，但是十六进制的字母必然不可能有ij这种东西，所以猜测可能是先把字母往小移，但是不知道具体偏移是多少，那就一个一个试过去，然后移完之后解一下hex看看能出来啥。

先从偏移为4开始，因为至少要4才能让ij移到ef这种合理的hex。

import string
flag = bytearray(b"666i5250356j4249"b"616732557968356j")for i in range(len(flag)):    if flag[i] in string.ascii_lowercase.encode():        flag[i] -= 4print(flag)print(bytes.fromhex(flag.decode()))

但是好像没啥规律，继续尝试到偏移为6的时候发现fl和ag。

尝试将前后半段每两字节拼接，得到flagRP2U5myhBI5m，拼上括号提交发现正确。

flag{RP2U5myhBI5m}

HNGK-modbus

这题筛选modbus之后发现function是有规律循环的：17, 109, 65, 1, 1, 3, 3, 67。

于是尝试提取发送方所有的func_code和帧id，然后跑一轮看看有没有多了或者少了的。

tshark -r .modbus.pcap -Y "modbus && ip.src==172.31.14.123" -T fields -e "frame.number" -T fields -e "modbus.func_code" > data.txt

发现1648帧多了个1。

data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if i[1] != base[p % len(base)]:        print(i)    p += 1

过去看了下发现确实是多了个1，不过上下对比一下发现实际上多出来的是1642数据包，因为这个1541在其他地方没出现过。

而1642数据包在提取结果里是539条，直接忽略这条再跑一遍看看还有没有异常的。

data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if p == 539:        continue    if i[1] != base[p % len(base)]:        print(i)    p += 1

直接跑完没有异常。

尝试提交flag{1642}或者flag{1642+1643}但是都不对。

于是怀疑可能数据包异常点不是func而是其内容。

那么只能挨个func的数据筛选过去看看有没有异常了。

先把17给发送和返回过滤一遍：(modbus.func_code == 17) && !(!modbus.data) && !(modbus.data == 06:00:00)。

发现没有异常的，那就再看109的：((modbus.func_code == 109) && !(modbus.data == 54)) && !(modbus.data == 00)。

发现也没有，再看65的：((modbus.func_code == 65) && !(modbus.data == a8:b9:09:00:0c:01:06:02:06:03:06:04:06:05:06:06:06:07:06:00:06)) && !(modbus.data == 02:fe:00)。

还是没有，再看1的：((((modbus.func_code == 1) && !(modbus.reference_num == 0)) && !(modbus.reference_num == 1536)) && !(frame[63] == 00)) && !(frame[63] == fe)。

发现两对数据包有异常，比之前找的多了一对，所以实际上异常是多了一个和改了一个。

尝试提交flag{1642+5485}，发现正确。

flag{1642+5485}

HNGK-奇怪的工控协议

看了下协议分布，最主要的modbus，不过iec60870_104和iec60870_asdu也不算少。

在modbus里面翻了半天也没看到啥有用的东西，然后去iec60870_104翻了下直接发现了flag。

flag{sort__104}

点击在看，关注我们

END


```
import string
flag = bytearray(b"666i5250356j4249"b"616732557968356j")for i in range(len(flag)):    if flag[i] in string.ascii_lowercase.encode():        flag[i] -= 4print(flag)print(bytes.fromhex(flag.decode()))
tshark -r .modbus.pcap -Y "modbus && ip.src==172.31.14.123" -T fields -e "frame.number" -T fields -e "modbus.func_code" > data.txt
data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if i[1] != base[p % len(base)]:        print(i)    p += 1
data = []with open("data.txt", 'r') as f:    for line in f:        data.append(line.strip().split('t'))
base = ['17', '109', '65', '1', '1', '3', '3', '67']p = 0for i in data:    if p == 539:        continue    if i[1] != base[p % len(base)]:        print(i)    p += 1
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669171056.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669171056.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669171057.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1669171058.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1669171059.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1669171060.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669171061.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669171062.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669171063.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669171064.png)