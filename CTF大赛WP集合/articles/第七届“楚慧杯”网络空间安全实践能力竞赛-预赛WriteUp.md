# 第七届“楚慧杯”网络空间安全实践能力竞赛-预赛WriteUp

> 原文: https://www.ctfiot.com/106699.html
> ID: 106699

mobile

level_one

[B@15db9742flag{380605c6-7123-4f71-b573- 601 e8c4457b4}

level_up

aes解密

结果为

flag{6b1df900-1284-11ed-9fa7-5405dbe5e745}

misc

crypt

图⽚备注提示了 VeraCrypt 容器

找到jpg⽂件尾 FFD9 ，将后⾯的内容另存为vc容器⽂件使⽤ VeraCrypt 挂载容器

资源管理器打开看不到⽂件，因此使⽤ X-Ways 打开

结果为

flag{4ba7689c6dee7749403380b11c416de6}

secret

镜像内⼀个bitlocker加密卷，⼀个有图⽚

图⽚crc不正确

修改图⽚⾼度后拿到password1 OXi

stegsolve找到password2 ChaiYan

passware跑出密钥 

620224-121649-497585-220572-660704-152383-484957-174713 并⽣成解密后的镜像⽂件

或者取证⼤师使⽤密码 OXiChaiYan 直接解密

明⽂攻击

结果为

flag{b6aa5b40559fc9762918cd32f5f6bd0f}

pocky

将⽣成的hex⽤winhex写到新⽂件中

发现jpg尾部有压缩包数据

导出压缩包，⾥⾯有⼀张图和⼀个加密的压缩包

反转后补上⽂件头

拿到内容

签到

压缩包伪加密，直接⽤winzip⼀键修复即可

然后打开之后缩⼩，即可得到flag

结果为

 flag{b3b2cc1ffcaa12f61c6e61c519d1db2f}

web

python_easy

注册界⾯SSTI读config得到key

字节型直接⽤⽹上的项⽬改写⼀下，把key写死

伪造admin

修改cookie，访问flag

结果为

flag{3d12b41b-2c23-11ed-afc5-98fa9b8aee74}

sign

golang的ssti漏洞直接读flag name={{.FileRead “/tmp/flag”}}

结果为

flag{79d07778-2c32-11ed-b8ad-98fa9b8aee74}

⼩f的⽹站

Dir扫⼀下得到console

同时file存在绝对路径泄露

计算pin码 

同时存在任意⽂件读取

读取⽤户名

读取机器id

读取mac地址

输⼊进⼊console得到flag

结果为

flag{8229a22e014cb1fb9d349ec485cf2895}

ez_pop

第⼀层：php反序列化

绕md5强⽐较 

参考⽂章：

https://blog.csdn.net/LYJ20010728/article/details/114492485

shell.txt⽂件内容

shell.txt拖进fastcoll

⽣成两个⽂件内容不⼀样但md5值相同的⽂件，绕过if，进⼊include

构造pop链，本地跑

读到hint.php内容为⽂件上传的路径uploadkfc.php，访问/uploadkfc.php第⼆层：⽂件上传的绕过

利⽤之前反序列化⽂件包含的点读到有如下上传的限制：image/png类型检查和⽂件内容检查

Content-Type：image/pngfile_put_contents(shell.php,’xxx’)转base64绕过

结果为

flag{e0w91c4a-6e34-59fb-b8af-b1f9440b92b4}

crypto

RollingBase

爆破⼀下对于字典的旋转

结果为

flag{416d3b4a10a9925363a44275d8655c5d}

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1680226175.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1680226176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1680226179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1680226179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1680226179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1680226179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1680226180.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1680226180.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1680226180.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1680226181.png)