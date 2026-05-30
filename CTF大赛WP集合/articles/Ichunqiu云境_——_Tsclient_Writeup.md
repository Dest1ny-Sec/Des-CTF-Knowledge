# Ichunqiu云境 —— Tsclient Writeup

> 原文: https://www.ctfiot.com/85253.html
> ID: 85253

Ichunqiu云境 —— Tsclient Writeup

Author:小离-xiaoli

0x1 Info

• Tag: MSSQL，Privilege Escalation，Kerberos，域渗透，RDP

0x2 Recon

1. Target external ip 47.92.82.196

2. nmap

3. MSSQL 弱口令爆破，爆破出有效凭据，权限为服务账户权限（MSSQLSERVER） sa:
1qaz!QAZ

0x3 入口点 MSSQL – 172.22.8.18

• 前言，该机器不在域内

1. 直接MSSQL shell（这里做完了忘记截图了..）

2. 提权，这里直接获取Clsid暴力怼potato（前面几个clsid是用不了的）

修改GetClsid.ps1，添加执行potato

Potato和GetClsid.ps1

执行GetClsid.ps1

获取到有效clsid以及命令执行结果

3. 导出SAM，SYSTEM，Security

解出凭据，用administrator + psexec 139横向（外网没有开445）就能获取到 flag01 administrator 2caf35bb4c5059a3d50599844e2b9b1f

4. qwinsta和端口连接看到有机器rdp过来

5. 这边使用administrator psexec后上msf（system权限），使用incognito模块，模拟至john（本人实测，只有msf的incognito能完成后续操作，f-secure lab等其他的模拟令牌工具没成功）

6. 使用john的token执行 net use 看到 \tsclientC 共享

7. 直接获取 \tsclientC 下面的 credential.txt，同时提示 hijack image (镜像劫持) xiaorang.labAldrich:
Ald@rLMWuy7Z!#

• 快进，略过搭建代理过程

1. CME 扫描 172.22.8.0/24，有三个机器提示密码过期了

2. 测试一下 DC01 88端口是否开启（测是否域控），DC01为域控

3. smbpasswd.py 远程修改一下过期密码，改成111qqq…

4. ldapshell.py 验证，登录域成功

5. CME 枚举 RDP，显示能登录进入 172.22.8.46（用CME官方的RDP模块不会扫出有效RDP凭据，这边自己写了一个基于xfreerdp的CME模块） XiaoliChan/CrackMapExec-Extension

0x4 域渗透 – 入口 – 172.22.8.46

1. 登录进入，查看到 xiaorang.labAldrich 不是这台机器的管理员，只是普通用户

• 提权，两种方法

Priv-ESC1：镜像劫持提权（常规）

Get-ACL查看到任何用户都可以对注册表 “HKLM:
SOFTWAREMicrosoftWindows NTCurrentVersionImage File Execution Options” 进行写入，创建操作

创建一个劫持magnify.exe（放大镜）的注册表，执行CMD.exe

锁定用户

点击放大镜

提权至system

Priv-ESC2：krbrelayup提权

域普通权限用户在域内机器，直接带走（非常规，推荐）

5. 快进mimikatz，获取到当前机器的机器账户 win2016$

xiaorang.labWIN2016$ 4ba974f170ab0fe1a8a1eb0ed8f6fe1a

0x5 域渗透 – DC Takeover

• 两种方法

1. 观察 WIN2016$ 的组关系，发现处于 Domain Admins 组，直接使用 Dcsync 带走 DC01 （过程略）

2. 约束委派（非常规）

Bloodhound收集域信息，分析，发现存在约束委派

使用 getST.py 进行约束委派攻击

带走 DC01

0x6 Outro

• 个人比较手残，不懂C，incognito那个部分，按照作者解释来说，常规是要自己写一个impersonate token的工具（还是没脱离MSF.. TAT）

原文始发于微信公众号（Gcow安全团队）：Ichunqiu云境 —— Tsclient Writeup

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/7-1670809586.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1670809586.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1670809588.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1670809588.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1670809589.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1670809589.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1670809590.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1670809593.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1670809594.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1670809597.png)