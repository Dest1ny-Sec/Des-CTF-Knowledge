---
title: WIZ IAM 挑战赛 Writeup (The Big IAM Challenge)
contest: WIZ The Big IAM Challenge
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [aws_iam_policy, s3_listbucket, sqs_receivemessage, sns_subscribe_endpoint, cognito_identity_pool, sts_assume_role_web_identity, public_principal_star, condition_bypass, s3_x1000]
attack_chain: 1) S3 thebigiamchallenge-storage-9979f4b Principal=* 公共桶 GetObject+ListBucket / 2) SQS wiz-tbic-analytics-sqs-queue-ca7a1b2 SendMessage+ReceiveMessage → aws sqs receive-message 读消息 / 3) SNS TBICWizPushNotifications Subscribe with @tbic.wiz.io 条件 → nc -lvk 80 接收订阅确认 / 4) thebigiamchallenge-admin-storage-abf1321 + ForAllValues:StringLike aws:PrincipalArn=arn:iam::133713371337:user/admin 条件 + 133713371337 = leet → 套星号条件 + no-sign-request 列桶 / 5) Cognito Identity Pool + mobileanalytics + cognito-sync + s3:GetObject+ListBucket wiz-privatefiles → get-id + get-open-id-token + assume-role-with-web-identity → 临时凭证 → s3 ls → flag2.txt in wiz-privatefiles-x1000
key_payload: aws sqs receive-message --queue-url https://queue.amazonaws.com/092297851374/wiz-tbic-analytics-sqs-queue-ca7a1b2 / aws cognito-identity get-id --identity-pool-id us-east-1:b73cb2d2-0d00-4e77-8e80-f99d9c13da3b / aws sts assume-role-with-web-identity --role-arn arn:aws:iam::092297851374:role/Cognito_s3accessAuth_Role
one_liner: WIZ The Big IAM Challenge 5 关 AWS IAM 策略误配置利用：公共 S3 桶+SQS ReceiveMessage+SNS 订阅+PrincipalArn 条件绕过+ Cognito Identity Pool 临时凭证链。
lesson: AWS IAM 策略中 "Principal": "*" + 弱条件 StringLike 是 CTF 经典 5 连击；Cognito Identity Pool 是 AWS 临时凭证颁发的低门槛入口。
quality: high
---
