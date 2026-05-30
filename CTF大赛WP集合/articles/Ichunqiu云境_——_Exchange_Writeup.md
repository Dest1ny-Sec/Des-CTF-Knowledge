# Ichunqiu云境 —— Exchange Writeup

> 原文: https://www.ctfiot.com/101057.html
> ID: 101057

Ichunqiu云境 —— Exchange Writeup

Author:小离-xiaoli

0x00 Intro

1. OSCP 渗透风格，脱离C2和MSF之类的工具

2. Box 难度不高

0x01 Info

• Tag: JDBC, Exchange, NTLM, Coerce Authentication, DCSync

0x02 Recon

1. Target external IP 39.98.179.149

2. Nmap results

3. 直接关注8000端口，前面我已经怼过80了，没东西直接过

4. 华夏ERP，有很多漏洞的，入口点卡了很久，后面看到JDBC，直接谷歌一搜就搜到大哥的文章了 Fastjson高版本的奇技淫巧 – Bmth (bmth666.cn)(http://www.bmth666.cn/bmth_blog/2022/10/19/Fastjson%E9%AB%98%E7%89%88%E6%9C%AC%E7%9A%84%E5%A5%87%E6%8A%80%E6%B7%AB%E5%B7%A7/#%E8%93%9D%E5%B8%BD%E6%9D%AF2022%E5%86%B3%E8%B5%9B-%E8%B5%8C%E6%80%AA)

5. 构造payload

6. Configure MySQL_Fake_Server

7. 未授权 + MySQL Connector JDBC反序列化组合拳直接RCE

8. RCE后直接获取 Flag01

0x03 入口点：172.22.3.12

1. SMB扫描内网主机，看到Exchange关键字 (EXC01)，尝试访问

2. 172.22.3.9 为 Exchange

3. Proxylogon 直接打死，获取system权限

4. flag02（后续凭据收集略过）

0x04 入口点：172.22.3.9

• 快进1：已经收集到了exchange机器账户的hash

• 快进2：同时收集到了一个域账户凭据：Zhangtong

1. 这边已经通过上面的操作收集到了exchange的机器账户hash，exchang的机器账户在域内对整个domain-object有writedacl权限，那我们直接使用dacledit.py给Zhangtong加dcsync权限（其实你也可以给自己加上dcsync）

2. Dcsync，获取到域管和用户lumia的hashes

3. 进入 172.22.3.2 获取flag04

0x05 Final：172.22.3.26

1. 172.22.3.26上面的Lumia用户文件夹里面有个secret.zip

2. 直接PTH Exchange导出Lumia mailbox里面的全部邮件以及附件

3. item-0.eml，提示密码是手机号

4. 刚好导出的附件里面有一个csv，里面全是手机号

5. 常规操作，转换成pkzip格式的hash再跑字典，跑出密码

6. flag03

0x06 Outro

1. Exchange 后渗透那，作者本意是想让我们用 NTLM Relay去完成DCSync提权，获取Exchange SYSTEM权限后，触发webdav回连中继到ldap，这里的话就不尝试了，有兴趣的话可以看我上一篇文章 Spoofing

2. Lumia用户登录exchange那，作者也是想让你改掉Lumia用户的密码，但是我就懒了，直接PTH

原文始发于微信公众号（Gcow安全团队）：Ichunqiu云境 —— Exchange Writeup

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/8-1677804098.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1677804099.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/4-1677804100.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1677804100.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1677804101.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1677804102.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1677804103.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1677804104.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/6-1677804104.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/4-1677804105.png)