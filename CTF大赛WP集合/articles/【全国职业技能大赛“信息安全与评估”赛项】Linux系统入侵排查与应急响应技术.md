# 【全国职业技能大赛“信息安全与评估”赛项】Linux系统入侵排查与应急响应技术

> 原文: https://www.ctfiot.com/218471.html
> ID: 218471

扫码领资料

获网安教程

0x1 进程

lsof -p 

0x2 查看安全网关或监控系统

0x3 端口

0x4 历史命令

0x5 恶意文件查找

0x6 分析恶意程序

0x7 检查Linux账户安全

##查看所有账号cat /etc/passwd##查看特权用户（uid为0）grep :0: /etc/passwd##查看账号密码相关信息cat /etc/shadow##查看用户登录时间uptime##查询utmp文件并报告当前登录的每一个用户who##查询utmp文件并显示当前系统中每个用户和它队形的进程w##列出所有用户最近的登录报告lastlog##查看远程SSH和telnet登录tail /var/log/auth.logtail /var/log/secure##查看sudo用户列表cat /etc/sudoers##多可以账号进行禁用或删除usermod -L user //禁用user账号userdel user //删除user账号userdel -r user //删除user账号，并将/home目录下的user目录一并删除

##列出当前用户cron服务详细内容crontab -l //文件保存在/var/spool/cron/user##查看以下目录中是否存在恶意脚本cat /etc/crontab/etc/crontab/etc/cron.d//etc/cron.daily//etc/cron.hourly//etc/cron.monthly//etc/cron.weekly//etc/anacrontab/var/spool/cron//var/spool/anacron/

检查可疑服务

查看开机自启动  
遍历/etc/目录下 init 开头、rc 开头的目录及文件

/etc/init.da





查询开机自启动的服务

service–status-all

0x8 检查系统日志

/var/log/cron 记录了系统定时任务相关的日志/var/log/cups 记录打印信息的日志/var/log/dmesg 记录了系统在开机时内核自检的信息/var/log/mailog 记录邮件信息/var/log/message 记录系统重要信息的日志/var/log/btmp 记录错误登录日志。 要使用lastb命令查看/var/log/lastlog 记录系统中所有用户最后一次登录时间的日志。 要使用lastlog命令查看/var/log/wtmp 永久记录所有用户的登录、注销信息，同时记录系统的启动、重启、关机事件。 要使用last命令查看/var/log/utmp 记录当前已经登录的用户信息。要使用w,who,users命令查看/var/log/secure 记录验证和授权方面的信息，比如SSH登录，su切换用户，sudo授权其他web中间件日志，如apache、mysql、ngnix

0x9 排查.ssh

查看/root/.ssh/known_hosts文件中的ssh公钥，查看本机通过ssh连接那一部分主机

0x10 结尾

内部圈子介绍

1、维护更新src专项漏洞知识库，包含原理、挖掘技巧、实战案例2、分享src优质视频课程3、分享src挖掘技巧tips4、微信小群一起挖洞5、不定期有众测、渗透测试项目

申明：本公众号所分享内容仅用于网络安全技术讨论，切勿用于违法途径，
所有渗透都需获取授权，违者后果自行承担，与本号及作者无关，请谨记守法.

欢迎加入星球一起交流，券后价仅40元！！！ 即将满150人涨价

长期更新，更多的0day/1day漏洞POC/EXP


```
lsof -p 
##查看所有账号cat /etc/passwd##查看特权用户（uid为0）grep :0: /etc/passwd##查看账号密码相关信息cat /etc/shadow##查看用户登录时间uptime##查询utmp文件并报告当前登录的每一个用户who##查询utmp文件并显示当前系统中每个用户和它队形的进程w##列出所有用户最近的登录报告lastlog##查看远程SSH和telnet登录tail /var/log/auth.logtail /var/log/secure##查看sudo用户列表cat /etc/sudoers##多可以账号进行禁用或删除usermod -L user //禁用user账号userdel user //删除user账号userdel -r user //删除user账号，并将/home目录下的user目录一并删除
##列出当前用户cron服务详细内容crontab -l //文件保存在/var/spool/cron/user##查看以下目录中是否存在恶意脚本cat /etc/crontab/etc/crontab/etc/cron.d//etc/cron.daily//etc/cron.hourly//etc/cron.monthly//etc/cron.weekly//etc/anacrontab/var/spool/cron//var/spool/anacron/
/var/log/cron 记录了系统定时任务相关的日志/var/log/cups 记录打印信息的日志/var/log/dmesg 记录了系统在开机时内核自检的信息/var/log/mailog 记录邮件信息/var/log/message 记录系统重要信息的日志/var/log/btmp 记录错误登录日志。 要使用lastb命令查看/var/log/lastlog 记录系统中所有用户最后一次登录时间的日志。 要使用lastlog命令查看/var/log/wtmp 永久记录所有用户的登录、注销信息，同时记录系统的启动、重启、关机事件。 要使用last命令查看/var/log/utmp 记录当前已经登录的用户信息。要使用w,who,users命令查看/var/log/secure 记录验证和授权方面的信息，比如SSH登录，su切换用户，sudo授权其他web中间件日志，如apache、mysql、ngnix
1、维护更新src专项漏洞知识库，包含原理、挖掘技巧、实战案例2、分享src优质视频课程3、分享src挖掘技巧tips4、微信小群一起挖洞5、不定期有众测、渗透测试项目
申明：本公众号所分享内容仅用于网络安全技术讨论，切勿用于违法途径，
所有渗透都需获取授权，违者后果自行承担，与本号及作者无关，请谨记守法.
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1733360779.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1733360780.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1733360780.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1733360781.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/9-1733360781.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1733360782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/9-1733360782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733360782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1733360783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1733360784.png)