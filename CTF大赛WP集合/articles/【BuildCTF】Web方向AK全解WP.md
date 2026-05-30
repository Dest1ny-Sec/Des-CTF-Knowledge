# 【BuildCTF】Web方向AK全解WP

> 原文: https://www.ctfiot.com/212857.html
> ID: 212857

【find-the-id】

爆破数字，207时得到flag

【Tflock】

扫目录发现robots.txt

获得一个账号ctfer:123456

获得admin密码字典

在每次爆破admin密码前发送一个ctfer登录成功的请求

admin爆破成功

登录获得flag

【Babyupload】

上传.htaccess

再上传木马执行env命令即可

【ez!http】

按要求填写http headers即可

Date不用按标准格式填写，用点分隔就行

【我写的网站被rce了？】

读文件时候可以命令执行即可

【LovePopChain】

写反序列化链子，然后post传参rce即可

【RedFlag】

Flask ssti

https://www.freebuf.com/articles/web/323728.html

【Why_so_serials?】

利用replace长度的变化构造反序列化字符串，利用joker扩充把原来最后面的内容按长度挤出去就行了

【ez_md5】

md5 sql注入，输入ffifdyop加密得到’闭合构造sql注入

进入下一关/LnPkcKqy_levl2.php

提示了robots看到

爆破一下3e41f780146b6c246cd49dd296a3da28得到1145146803531

Md5弱等于，直接传数组即可

【eazyl0gin】

node在处理大小时候有漏洞

在Character.toUpperCase()函数中，字符ı会转变为I，字符ſ会变为S。

在Character.toLowerCase()函数中，字符İ会转变为i，字符K会转变为k。

密码md5解密得到012346

故使用BUıLDCTF和012346登录

【刮刮乐】

提示传入cmd并且修改Referer头

没有回显可能后面拼接了/dev/null，注释掉后面就行了

【sub】

注册admin

利用JWT_SECRET_KEY伪造token

可以读到文件之后构造命令执行闭合

【Cookie_Factory】

扫目录发现app.js

打开即可获得flag

【ez_waf】

前面添加8000个1绕过waf上传一句话木马

获取flag

【打包给你】

原题：https://blog.csdn.net/qq_46548764/article/details/141602431

上传文件后，后端会存储用户的文件并将其打包并提供压缩包下载功能，漏洞触发点，关键在于：

vps打开nc -lvvp 8080 监听

上传这三个文件并下载，触发tar命令的反弹shell

【fake_signin】

看到补签功能只有一次，但是存在如果30天同时并发可以达到同时补签30天的情况

再次刷新签到页面，发现30天都是已签到状态了，flag也出来了

原文始发于微信公众号（智佳网络安全）：【BuildCTF】Web方向AK全解WP

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1730380283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1730380283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1730380284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1730380285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1730380286.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1730380286.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1730380287.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1730380287.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1730380289.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1730380290.png)