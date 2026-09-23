---
title: 2024 FIC 第四届全国网络空间取证竞赛 初赛 WP
contest: 第四届全国网络空间取证竞赛 (FIC 2024)
year: 2024
difficulty: hard
vuln_type:
- forensic_disk
- forensic_memory
- misc_unknown
tags:
- 杀猪盘
- ESXi
- vmdk
- Docker
- MySQL
- 若依
- RuoYi
- jar-反编译
- vmdk挂载
- 微信取证
- iStoreOS
- OpenWrt
- NasTools
- 鲁盒
attack_chain:
- 案：卢某被'杀猪盘'诈骗 → 查李某手机(检材1) + 服务器(检材2) + 赵某PC(检材3)
- ESXi vmdk esxcfg-volume -l 挂载
- 微信 wxid 提取 → 赌博群 URL http://www.honglian7001.com/down
- 服务器扫 192.168.110.110:8000/login + 密码 limoon890
- docker inspect 9b 看 MYSQL_ROOT_PASSWORD
- ruoyi-admin.jar 解压改 application-druid.yml 启动 /api/shopOrder
- iStoreOS OpenWrt NasTools PassWall2 → token 订阅地址
- TrueCrypt 卷密码 qwerasdfzxcv
- 火眼鲁盒 dst01.jpeg 镜像 0.85 缩放
key_payload: ruoyi-admin.jar BOOT-INF/classes/application-druid.yml → MYSQL_ROOT_PASSWORD=my-secret-pw
one_liner: 杀猪盘综合取证：手机+服务器+PC 三检材联动
lesson: 综合取证赛三大类：微信/QQ 聊天记录；ESXi/Docker 容器部署链路；加密卷密码与镜像；iStoreOS 软路由+订阅 token
quality: high
full_path: 2024FIC第四届全国网络空间取证竞赛线上初赛全解参考wp.full.md
meta_path: 2024FIC第四届全国网络空间取证竞赛线上初赛全解参考wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 FIC 第四届全国网络空间取证竞赛 初赛 WP。杀猪盘综合取证：手机+服务器+PC 三检材联动。关键路径：案：卢某被'杀猪盘'诈骗 → 查李某手机(检材1) + 服务器(检材2) + 赵某PC(检材3) → ESXi vmdk esxcfg-volume -l 挂载 → 微信 wxid 提取 → 赌博群 URL http://www.honglian7001.com/down。经验...
category: forensic
subcategory: disk_forensics
subcategories:
- disk_forensics
- memory_forensics
- misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/176442.html
reasoning_chain:
- 触发点：杀猪盘诈骗案 → 假设：检材1手机+检材2服务器+检材3PC 三联动 → 动作：分别挂载镜像取证
- 观察：检材1 是 ESXi vmdk → 假设：esxcfg-volume -l 看卷 → 动作：vmkfstools -i 挂载 vmdk
- 触发点：李某手机微信 wxid → 假设：赌博群聊天记录 → 动作：取证工具提取 wxid 数据库
- 观察：赌博群 URL http://www.honglian7001.com/down → 假设：访问群文件下载赌博 app → 动作：curl 下载取证
- 触发点：服务器 192.168.110.110:8000/login → 假设：弱口令 limoon890 → 动作：浏览器访问后台
- 观察：Docker 部署 → 假设：docker inspect 9b 看环境变量 → 动作：docker inspect <container_id>
- 触发点：MYSQL_ROOT_PASSWORD=my-secret-pw → 假设：数据库密码泄露 → 动作：mysql -uroot -pmy-secret-pw
- 观察：ruoyi-admin.jar → 假设：BOOT-INF/classes/application-druid.yml 含 DB 密码 → 动作：unzip jar 改 yml
- 触发点：iStoreOS OpenWrt NasTools PassWall2 → 假设：订阅 token 是关键 → 动作：cat /etc/nastools/config.yaml
- 观察：token 订阅地址 → 假设：解密订阅节点 → 动作：解密 base64 订阅 URL
- 触发点：TrueCrypt 卷 → 假设：密码 qwerasdfzxcv → 动作：truecrypt -m=nokernelcrypto -p=qwerasdfzxcv
- 观察：火眼鲁盒 dst01.jpeg 镜像 0.85 缩放 → 假设：缩放比例匹配 → 动作：python PIL 缩放对比
failed_attempts:
- 试图直接 docker exec 进容器 → 失败：需先拿到镜像 inspect 信息
- 试图爆破 TrueCrypt 密码 → 失败：必须找现场残留字典
- 试图不解 vmdk 直接读 ESXi 卷 → 失败：必须用 vmkfstools 挂载
- 试图不解订阅节点直接访问 → 失败：token 加密需解密
key_observations:
- 综合取证赛三大类：微信/QQ 聊天记录；ESXi/Docker 容器部署链路；加密卷密码与镜像
- ruoyi-admin.jar BOOT-INF/classes 路径是若依框架密码泄露固定位置
- iStoreOS OpenWrt NasTools PassWall2 订阅 token 是软路由取证常见入口
- TrueCrypt 卷密码常在嫌疑人电脑明文残留
- 火眼鲁盒 dst01.jpeg 镜像 0.85 缩放比是图像取证固定考点
prerequisites:
- ESXi vmdk 挂载（vmkfstools/esxcfg-volume）
- 微信 wxid 数据库提取与赌博群 URL 定位
- Docker inspect 环境变量读取
- 若依 RuoYi 框架 BOOT-INF/classes 路径
- TrueCrypt 卷解密（nokernelcrypto 模式）
---
# 2024FIC第四届全国网络空间取证竞赛线上初赛全解参考wp

> 原文: https://www.ctfiot.com/176442.html
> ID: 176442

“ 比赛的发挥不尽如人意，又是通宵复盘的一次比赛，很多时候其实题目不难，难的是自己比赛时无法从紧张的情绪中抽离出来冷静思考，花了很长时间，终于一个人完整复盘了一遍。”

检材链接：https://pan.baidu.com/share/init?surl=pJDwwNy14o-kAstHkndWPg&pwd=1234容器密码：2024Fic@杭州Powered~by~HL!

01

—

2024年4月，卢某报案至警方，声称自己疑似遭受了“杀猪盘”诈骗，大量钱财被骗走。卢某透露，在与某公司交流过程中结识了员工李某。李某私下诱导卢某参与赌博游戏，起初资金出入均属正常。但随后，李某称赌博平台为提升安全性，更换了地址和玩法，转为通过群聊抢红包形式进行赌博。随着赌资不断增加，卢某投入巨额资金后，发现无法再访问该网站，同时李某也失去联系，卢某遂意识到自己被骗。在经济压力下，卢某选择报警，并承认参与赌博活动，愿意承担相应法律后果。警方依据卢某提供的线索和手机数据，迅速锁定犯罪团伙，并在一藏匿地点成功抓获犯罪嫌疑人李某和赵某。警方对嫌疑人持有的物品进行了证据固定：李某手机被标记为检材1，窝点内服务器为检材2，赵某使用的计算机为检材3。 

接下来，请取证工作者根据案情和这些检材进行深入分析，并解答后续问题。

02

—

B

D

5aada11bc1b5

wxid_wnigmud8aj6j12

http://www.honglian7001.com/down

limoon890

B

C

wxid_06f01lnpavn722

192.168.110.110:
8000/login

03

—

6.7

A

65efb8a8-ddd817f6-04ff-000c297bd0e6

esxcfg-volume -l

192.168.8.112

4

192.168.8.89

qqqqqq

14131

/webapp

0

!@#qaaxcfvghhjllj788+)_)((

D

C

877

jar xf ruoyi-admin.jar BOOT-INF/classes/application-druid.yml

vim BOOT-INF/classes/application-druid.yml

jar uf ruoyi-admin.jar BOOT-INF/classes/application-druid.yml

java -jar ruoyi-admin.jar

sh start.sh start

3.8.2

/api/shopOrder

10044888

465222

10

7354468.56

my-secret-pw

docker inspect 9b | grep MYSQL_ROOT_PASSWORD

7.9.2009

1.13.1

9bf1cecec3957a5cd23c24c0915b7d3dd9be5238322ca5646e3d9e708371b765

66c0e7ca4921e941cbdbda9e92242f07fe37c2bcbbaac4af701b4934dfc41d8a

B

172.17.0.2

182.33.2.250

43.139.0.193

35821148.48

3

3000

admin@admin.com

5.0.24

104857600

B

vim /etc/ssh/sshd_config

http://172.16.80.47

35%

B

lao@su.com

iStoreOS

5.10.201

192.168.8.5

br-lan

20.10.22

/root/Configs/NasTools

PassWall2

54

1070

https://pqjc.site/api/v1/client/subscribe?token=243d7bf31ca985f8d496ce078333196a

04

—

FFD2777C0B966D5FC07F2BAED1DA5782F8DE5AD6

B25E2804B586394778C800D410ED7BCDC05A19C8

E6EB3D28C53E903A71880961ABB553EF09089007

qwerasdfzxcv

404052-011088-453090-291500-377751-349536-330429-257235

146794496

A

Zhao

www.585975.com

B

db.jpg

0.85

dst01.jpeg

http://hi.pcmoe.net/buddha.html

192.168.8.17

C

hl@7001

易有云

aa123456

28300

05

—

喜欢的看官还请多多点赞转发


```
检材链接：https://pan.baidu.com/share/init?surl=pJDwwNy14o-kAstHkndWPg&pwd=1234容器密码：2024Fic@杭州Powered~by~HL!
B
D
5aada11bc1b5
wxid_wnigmud8aj6j12
http://www.honglian7001.com/down
limoon890
B
C
wxid_06f01lnpavn722
192.168.110.110:
8000/login
6.7
A
65efb8a8-ddd817f6-04ff-000c297bd0e6
esxcfg-volume -l
192.168.8.112
4
192.168.8.89
qqqqqq
14131
/webapp
0
!@#qaaxcfvghhjllj788+)_)((
D
C
877
jar xf ruoyi-admin.jar BOOT-INF/classes/application-druid.yml
vim BOOT-INF/classes/application-druid.yml
jar uf ruoyi-admin.jar BOOT-INF/classes/application-druid.yml
java -jar ruoyi-admin.jar
sh start.sh start
3.8.2
/api/shopOrder
10044888
465222
10
7354468.56
my-secret-pw
docker inspect 9b | grep MYSQL_ROOT_PASSWORD
7.9.2009
1.13.1
9bf1cecec3957a5cd23c24c0915b7d3dd9be5238322ca5646e3d9e708371b765
66c0e7ca4921e941cbdbda9e92242f07fe37c2bcbbaac4af701b4934dfc41d8a
B
172.17.0.2
182.33.2.250
43.139.0.193
35821148.48
3
3000
admin@admin.com
5.0.24
104857600
B
vim /etc/ssh/sshd_config
http://172.16.80.47
35%
B
lao@su.com
iStoreOS
5.10.201
192.168.8.5
br-lan
20.10.22
/root/Configs/NasTools
PassWall2
54
1070
https://pqjc.site/api/v1/client/subscribe?token=243d7bf31ca985f8d496ce078333196a
FFD2777C0B966D5FC07F2BAED1DA5782F8DE5AD6
B25E2804B586394778C800D410ED7BCDC05A19C8
E6EB3D28C53E903A71880961ABB553EF09089007
qwerasdfzxcv
404052-011088-453090-291500-377751-349536-330429-257235
146794496
A
Zhao
www.585975.com
B
db.jpg
0.85
dst01.jpeg
http://hi.pcmoe.net/buddha.html
192.168.8.17
C
hl@7001
易有云
aa123456
28300
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]