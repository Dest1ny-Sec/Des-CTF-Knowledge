# 春秋云境Initial通关

> 原文: https://www.ctfiot.com/109744.html
> ID: 109744

前言

Initial是一套难度为简单的靶场环境，完成该挑战可以帮助玩家初步认识内网渗透的简单流程。该靶场只有一个flag，各部分位于不同的机器上。

步骤

入口处是一个电源管理系统，指纹识别可以得出是thinkphp框架，直接用工具扫描是否存在thinkphp漏洞。

确定有漏洞后就可以直接进行RCE。

getshell后拿的权限是www-data权限，这里可以使用sudo提权来读取flag1:(sudo mysql -e ‘! cat /root/flag/flag01.txt’)

拿下第一个flag后用frp带代理扫描内网机器，扫描结果如下：

172.22.1.2（域控）172.22.1.15（边界机）172.22.1.18（信呼协同办公系统）172.22.1.21（永恒之蓝）

总结

总结一下该靶场的相关流程：

首先使用thinkphp漏洞拿下边界机（flag1）→做代理利用ms17-010拿下域内机器→DCSync拿下域管理员权限（flag3）→使用域管理员权限读取flag2

END

• 往期精选

windows提权总结

一次SSH爆破攻击haiduc工具的应急响应

记一次艰难的SQL注入(过安全狗)

记一次溯源

下方点击关注发现更多精彩


```
172.22.1.2（域控）172.22.1.15（边界机）172.22.1.18（信呼协同办公系统）172.22.1.21（永恒之蓝）
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1681447010.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1681447010.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/4-1681447011.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681447011.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1681447011.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681447011.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1681447011.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1681447013.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681447013.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/4-1681447013.png)