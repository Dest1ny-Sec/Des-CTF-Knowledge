# 2025高校网络安全管理运维赛-电子取证分析师赛道-决赛WriteUp

> 原文: https://www.ctfiot.com/278549.html
> ID: 278549

点击上方蓝字·关注我们

前言：

本篇文章是赛后复现欢迎大家交流学习！

文章同步CSDN，感谢观看！

csdn主页：https://blog.csdn.net/Aluxian_?type=lately

签到题：

gif文件 分帧-组合-画图-拼接-扫码

谁真正的执行了命令？：

log日志文件 直接kali 使用awk 过滤 或者肉眼看

flag{b1bdef37df1a7acec711e97568c8e3b8}

网络流量中的巨兽踪迹god：

11cd6a875898416+6c37ac826a2a04bc#md5解密密钥:3c6e0b8a9c15224a

MISC-PACPdfir-pcap：

flag{redis}

flag{1234567qwerc}

flag{/usr/share/caddy/testinfo.php}

DFIR-archer：

flag{42DDE4A368FD17641E8B56017081A5B00CAB11B89FD88495E3FE2D684A9F3DC9}

2.给出用户账户“archer”的创建时间（格式：2001-12-21 05:23:15 精确到秒)

flag{2022-02-05 00:25:26}

解密这个keepss文件,找到ironbox.safe

flag{PqR$34%sTuVwX}

4.VeraCrypt加密卷中的最新的Excel中有一张热成像图片，计算该图片的SM3校验值（全大写）。

flag{ce4a2f20ebc2bcdce729885ae12fb3de0a7231e6c0a8dc1cc050605f9f8f1663}

flag{hereyouare}

DFIR-rensom：

1.恢复系统数据，给出主机用户的姓名全拼（全小写，例：zhangsan）

flag{maaiyu}

2.给出主机最近一次插过的U盘的厂商，全小写（例：barracuda）

flag{jetflash}

3.给出电脑的OEM厂商品牌名称，全小写（例：xiaomi）

DFIR-prx：

DFIR-RAID：

blkid ##命令，列出所有分区的 UUID、文件系统类型 lsblk -f ##参数可以树状图

systemctl list-unit-files | grep dlna #查找位置find / -name *dlna* #搜索全部路径，然后去路径查看版本即可cd/trim/var/mindlna /usr/trim/bin/minidlnad -V#执行命令 查看版本

lvscan#查看挂载的盘，发现有两个 新建两个进行挂载mkdirnewmkdirbackcd/newmount /dev/newnew/vol1cd/backmount /dev/newnew/back202510 diff -r back new #对比两个文件 -r 递归 -I 排除二进制

需要交流或者培训可以联系小编加群交流！

排版创作不宜如果对你有帮助，可以支持一下小编！

关注我们

欢迎关注鱼影安全社区,专注CTF,职业技能大赛中高职技能培训,信息安全评估高职组赛项,金砖一带一路诸暨技能大赛:企业信息安全赛道-攻防治理赛道-首届金砖虚拟网络建设赛道-创信大赛,世界技能大赛省选拔赛,企业赛,行业赛,电子取证和CTF系列培训,工控CTF系列，第二届网络安全行业职业技能大赛（电子取证师、渗透测试员、网络安全管理员、网络信息审核员）等。

鱼影安全团队招人啦,有感兴趣的师傅可以私信我

需要学习数据安全管理员和CTF安全培训,可以联系小编


```
11cd6a875898416+6c37ac826a2a04bc#md5解密密钥:3c6e0b8a9c15224a
```



```
blkid ##命令，列出所有分区的 UUID、文件系统类型 lsblk -f ##参数可以树状图
```



```
systemctl list-unit-files | grep dlna #查找位置find / -name *dlna* #搜索全部路径，然后去路径查看版本即可cd/trim/var/mindlna /usr/trim/bin/minidlnad -V#执行命令 查看版本
```



```
lvscan#查看挂载的盘，发现有两个 新建两个进行挂载mkdirnewmkdirbackcd/newmount /dev/newnew/vol1cd/backmount /dev/newnew/back202510 diff -r back new #对比两个文件 -r 递归 -I 排除二进制
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737434-wxsync-2025-11-f4dd000cea4bf9f74ed932731079694c.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737436-wxsync-2025-11-a8f45598cf1a3d1d063fee7dc3b7301b.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737437-wxsync-2025-11-ee68cea1bb4999cd7377be94137708cb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737439-wxsync-2025-11-82eabde481389790f640aed3fda2442d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737441-wxsync-2025-11-fc4760810a7de6e9e2faa6054f90dfc3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737444-wxsync-2025-11-c8bd4227793b2da23f4a70d680578c83.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737449-wxsync-2025-11-7cff5e8c99da61187a0cf266755e8317.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737457-wxsync-2025-11-7e3f617d4b7ca7bb9a10e4f956a8b9ab.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737459-wxsync-2025-11-69f10437e5f3bfbd78f3ced21029f0a0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737460-wxsync-2025-11-f11e060307f5bed6ae1c5580bba312c7.png)