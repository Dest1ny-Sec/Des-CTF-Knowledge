---
title: 【全国职业技能大赛"信息安全与评估"赛项】Linux系统入侵排查与应急响应技术
contest: 全国职业技能大赛
year: 2024
difficulty: easy
vuln_type: forensic_disk
tags:
- 应急响应
- Linux-IR
- lsof-process
- /etc/passwd
- cron-check
- auth.log
- SSH
- init.d
attack_chain: 1. 进程排查 lsof -p PID /2. 端口 ss/netstat /3. 历史命令 history /4. 恶意文件 find /tmp /dev/shm /5. 分析恶意程序 strings+objdump /6. Linux 账户 /etc/passwd uid=0 /etc/shadow /7. cron /etc/crontab /var/spool/cron/ /8. 系统日志 /var/log/cron/message/btmp/wtmp/secure /9. .ssh authorized_keys
key_payload: lsof -p  /etc/passwd uid=0  /var/log/secure  /etc/crontab  /var/spool/cron
one_liner: 全国职业技能大赛 Linux 应急响应技术，9 大模块：进程/端口/历史/恶意文件/恶意程序/账户/cron/系统日志/.ssh。
lesson: 应急响应 9 模块：lsof 进程 + 端口 + history + find + strings + /etc/passwd + cron + /var/log + .ssh。
quality: high
full_path: 【全国职业技能大赛“信息安全与评估”赛项】Linux系统入侵排查与应急响应技术.full.md
meta_path: 【全国职业技能大赛“信息安全与评估”赛项】Linux系统入侵排查与应急响应技术.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【全国职业技能大赛"信息安全与评估"赛项】Linux系统入侵排查与应急响应技术。全国职业技能大赛 Linux 应急响应技术，9 大模块：进程/端口/历史/恶意文件/恶意程序/账户/cron/系统日志/.ssh。。经验：应急响应 9 模块：lsof 进程 + 端口 + history + find + strings + /etc/pas...
category: forensic
subcategory: disk_forensics
tools_used:
- objdump
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/218471.html
reasoning_chain:
- 应急响应 9 大模块 → 触发点：进程/端口/历史/文件/账户/cron/日志/.ssh
- 步骤 1：进程排查 → 假设：恶意进程用 lsof 看打开文件 → 动作：lsof -p <pid>
- 步骤 2：端口排查 → 假设：恶意端口 → 动作：ss -tlnp / netstat -anpt → 观察：监听端口 + PID
- 步骤 3：历史命令 → 假设：操作痕迹 → 动作：history / cat ~/.bash_history
- 步骤 4：恶意文件查找 → 假设：临时目录藏木马 → 动作：find /tmp /dev/shm /var/tmp -mtime -7
- 步骤 5：恶意程序分析 → 假设：二进制含回连 IP → 动作：strings <bin> + objdump -d
- '步骤 6：账户安全 → 假设：新增 uid=0 提权账号 → 动作：grep :0: /etc/passwd + cat /etc/shadow'
- 步骤 7：cron 后门 → 假设：定时反弹 → 动作：cat /etc/crontab + /var/spool/cron/ + /etc/cron.d/
- 步骤 8：系统日志 → 假设：SSH 登录痕迹 → 动作：/var/log/secure + lastb + lastlog + wtmp
- 步骤 9：SSH 公钥 → 假设：攻击者写入免密登录 → 动作：cat ~/.ssh/authorized_keys + /root/.ssh/id_rsa
failed_attempts:
- 试图只看 top 进程 → 失败：恶意进程可能改名 (sshd) 隐藏
- 试图只看 /var/log/messages → 失败：SSH 登录在 /var/log/secure 不在 messages
- 试图只看 cron 主目录 → 失败：/etc/cron.d/ 单独目录有写权限
key_observations:
- 应急响应 9 模块顺序：进程 → 端口 → 文件 → 账户 → 日志
- 'grep :0: /etc/passwd 找特权用户 (uid=0) 是最快发现后门账号'
- /var/log/secure 是 SSH 登录日志 (RHEL 系)，/var/log/auth.log 是 Debian 系
- lsof -p <pid> 看进程打开的文件/网络连接能查回连 IP/木马上传
- crontab -l + /etc/cron.d/ + /var/spool/cron/ 三个目录都要查
prerequisites:
- Linux 进程/端口基础 (lsof, ss, netstat)
- find + mtime 文件时间筛选
- /etc/passwd /etc/shadow 用户系统
- Linux cron 计划任务目录结构
---
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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]