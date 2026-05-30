# 2024盘古石晋级赛IPA和apk部分

> 原文: https://www.ctfiot.com/183403.html
> ID: 183403

IPA取证

1.分析毛雪柳的手机检材，记账APP存储记账信息的数据库文件名称是：[答案格式：tmp.db，区分大小写][★★★★☆]

default.realm

找到记账APP为iCost，跳转到源文件，在Documents里面找到realm格式文件，realm是数据库文件

2.分析毛雪柳的手机检材，记账APP中，2月份总收入金额是多少：[答案格式：1234][★★★★★]

11957

使用realm studio查看数据库文件，type=1为收入，进行筛选

先转换出2月的时间，按照时间排列，在这个时间范围内只有2条，9600+2357=11957

3.分析毛雪柳的手机检材，手机中团队内部使用的即时通讯软件中，团队老板的邮箱账号是：[答案格式：abc@abc.com][★★★☆☆]

gxyt@163.com

分析得到gxyt为团队老板，可以从服务器查看

也可以从手机中数据库查看，在application.plist中看到了Mattermost的共享数据目录在/private/var/mobile/Containers/Shared/AppGroup/BBE0D501-AB0B-422E-9B4D-02E2D86130D4

分析聊天记录得到老板user_id为enf863dp1ifi3ffos7bpduynny

User中找到对应的email为gxyt@163.com，username为gxyt

4.接上题，该内部即时通讯软件中，毛雪柳和老板的私聊频道中，老板加入私聊频道的时间是：[答案格式：2024-01-01-04-05-06][★★★☆☆]

2024-04-24-11-59-28

结合聊天记录分析，yiyan频道是和yiyan的聊天频道，Off-Topic和Town Square都是群聊，发财是和gxyt的聊天频道，找到gxyt加入频道的记录，时间为1713931168391，转换为北京时间是2024-04-24 11:59:28

5.接上题，该私聊频道中，老板最后一次发送聊天内容的时间是：[答案格式：2024-01-01-04-05-06][★★★☆☆]

2024-04-25-10-24-50

找到gxyt最后一次发送的时间为1714011890182，转换为2024-04-25 10:24:50

APK分析

1.分析伏季雅的手机检材，手机中诈骗APP的包名是：[答案格式：abc.abc.abc，区分大小写][★☆☆☆☆]

w2a.W2Ah5.jsgjzfx.org.cn

找到诈骗app为威尼斯，从服务器等均可印证

2.分析伏季雅的手机检材，手机中诈骗APP连接的服务器地址是：[答案格式：127.0.0.1][★☆☆☆☆]

192.168.137.125

找到源文件base.apk（在data/app目录下），导出用雷电APP智能分析，服务器地址为192.168.137.125

3.分析伏季雅的手机检材，手机中诈骗APP的打包ID是：[答案格式：_abc_abc.abc，区分大小写][★☆☆☆☆]

__W2A__h5.jsgjzfx.org.cn

查看源文件内容，id为__W2A__h5.jsgjzfx.org.cn

4.分析伏季雅的手机检材，手机中诈骗APP的主启动项是：[答案格式：abc.abc.abc，区分大小写][★☆☆☆☆]

io.dcloud.PandoraEntry

5.分析义言的手机检材，分析团队内部使用的即时通讯软件，该软件连接服务器的地址是：[答案格式：127.0.0.1][★★☆☆☆]

192.168.137.97

从义言手机中找到mattermost的数据库app.db，找到服务器地址为192.168.137.97

6.接上题，该软件存储聊天信息的数据库文件名称是：[答案格式：abc.abc，区分大小写][★★☆☆☆]

aHR0cDovLzE5Mi4xNjguMTM3Ljk3OjgwNjU=.db

7.接上题，该即时通讯软件中，团队内部沟通群中，一共有多少个用户：[答案格式：1][★★☆☆☆]

6

从user中看到一共6个用户

8.接上题，该即时通讯应用的版本号是：[答案格式：1.1.1][★★☆☆☆]

2.15.0

9.接上题，该即时通讯应用中，团队内部沟通中曾发送了一个视频文件，该视频文件发送者的用户名是：[答案格式：abc][★★★★☆]

yiyan

可以从服务器中直接看到

也可以从数据库中找到，从file中看到mp4格式的视频文件，post_id为hctctn8bnbd7meywjpmk3z9dhh

按照id在聊天记录中找到了此条内容，对应user_id为jrmi9kx8pfg9drc7b9dczh7neo，返回user中找到其用户名为yiyan

10.接上题，分析该即时通讯的聊天记录，团队购买了一个高性能显卡，该显卡的显存大小是：[答案格式：20G][★★☆☆☆]

24G

从聊天记录中找到个地址https://item.jd.com/10091688812789.html

11.分析义言的手机检材，手机中装有一个具备隐藏功能的APP，该APP启动设置了密码，设置的密码长度是多少位：[答案格式：5][★★★★☆]

9

APP为计算器

经搜索查找到加密原理，可供参考，以下内容参照其进行。

https://theincidentalchewtoy.wordpress.com/2021/12/07/decrypting-the-calculator-apps/

根据上述链接得知图案密钥在“/data/data/com.hld.anzenbokusufake/shared_prefs”文件夹中的“share_privacy_safe.xml”中，得到图案密文为AF809945A92BC6EAF96B6FE5758AB660

加密模式为AES_CBC，加密密钥和IV均为Rny48Ni8aPjYCnUI，要将其转换为Hex格式

将图案的密文进行AES_CBC解密，得到图案设置密码为012467853，长度为9位

对应的图案为

12.接上题，分析上述隐藏功能的APP，一共隐藏了多少个应用：[答案格式：1][★★★★☆]

5

解法一：仿真查看

按照上述教程了解到，数据在/data/data/com.hld.anzenbokusufake中，媒体文件在/sdcard/.privacy_safe中，从火眼中导出这两类文件，使用MT管理器复制到模拟器的相同路径下（雷电模拟器电脑目录为Documentsleidian9Pictures，共享安卓目录为Pictures）

用得到的图案密码，在模拟器中打开app，长按计算器标题打开第二空间

按照上题中的密码解密，在应用隐藏选项中共隐藏了5个应用

解法二：查看数据库

数据库文件“privacy_safe.db”也使用加密密钥Rny48Ni8aPjYCnUI加密，使用DB Browser打开

应用隐藏是在HIDE_APP中，一共有5个

13.接上题，分析上述隐藏功能的APP，该APP一共加密了多少个文件：[答案格式：][★★★★☆]

5

在文件保险箱中，发现共有5个文件

文件隐藏是在FILE_INFO表中，一共有5个

14.接上题，分析上述隐藏功能的APP，该APP加密了一份含有公民隐私信息的文件，该文件的原始名称是：[答案格式：abc.txt][★★★★☆]

公民信息.xlsx

同上得到该文件原始名称为公民信息.xlsx

15.分析义言的手机检材，马伟的手机号码是：[答案格式：13012341234][★★★★☆]

18921286666

恢复公民信息.xlsx至原始路径

使用MT管理器导出至电脑进行分析，找到马伟的手机号为18921286666

根据数据库的表我们知道公民信息.xlsx加密后的文件为e-283a934b-7821-4af3-9301-2cd6bba15782+c1，我们可以用CyberChef解密，将文件以Raw上传，解密后以Raw下载

解压后重命名，打开即可

16.分析义言的手机检材，手机中存有一个BitLocker恢复密钥文件，文件已被加密，原始文件的MD5值是：[答案格式：小写字母和数字][★★★★☆]

497f308f66173dcd946e9b6a732cd194

同上题步骤，仿真导出和使用CyberChef解密下载得到的MD5值是一样的

原文始发于微信公众号（数据取证杂谈）：2024盘古石晋级赛IPA和apk部分

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716708729.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716708730.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1716708731.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716708733.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716708734.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716708735.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716708735.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716708736.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716708737.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716708739.png)