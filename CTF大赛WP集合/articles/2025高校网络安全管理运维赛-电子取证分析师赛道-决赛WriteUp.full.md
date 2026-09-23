---
title: 2025 高校网络安全管理运维赛-电子取证分析师赛道-决赛 WriteUp
contest: 2025 高校网络安全管理运维赛
year: 2025
difficulty: medium
vuln_type:
- forensic_disk
- forensic_memory
- misc_unknown
tags:
- 高校网络安全管理运维赛 2025 决赛
- 电子取证分析师
- 签到题 gif 分帧组合扫码
- log 日志 awk 过滤
- MD5 11cd6a875898416+6c37ac826a2a04bc
- 3c6e0b8a9c15224a 解密密钥
- pcap redis/1234567qwerc Caddy /usr/share/caddy/testinfo.php
- VeraCrypt 加密卷 SM3 校验
- Keepass ironbox.safe PqR$34%sTuVwX
- 用户名 maaiyu
- U 盘 jetflash
- RAID lvscan 挂载对比
attack_chain:
- '签到: gif 分帧-组合-画图-拼接-扫码'
- '谁真正执行命令: log awk 过滤'
- '网络流量 MD5 解密: 11cd6a875898416+6c37ac826a2a04bc → 3c6e0b8a9c15224a'
- 'PACPdfir-pcap: flag{redis}, flag{1234567qwerc}, flag{/usr/share/caddy/testinfo.php}'
- 'DFIR-archer: 账户创建时间 2022-02-05 00:25:26'
- Keepass ironbox.safe 密码 PqR$34%sTuVwX
- 'VeraCrypt SM3 校验: ce4a2f20ebc2bcdce729885ae12fb3de0a7231e6c0a8dc1cc050605f9f8f1663'
- 'DFIR-rensom: 用户 maaiyu, U 盘 jetflash'
- 'DFIR-RAID: lvscan + mount + diff -r back new'
key_payload: Keepass ironbox.safe → PqR$34%sTuVwX
one_liner: 2025 高校网络安全管理运维赛电子取证分析师决赛：签到 GIF + log awk + PACP pcap + Keepass + VeraCrypt + 勒索恢复 + RAID 对比。
lesson: 高校运维赛取证赛道覆盖签到/log/pcap/账户/Keepass/VeraCrypt/勒索/RAID 全栈；Keepass 主密码 PqR$34%sTuVwX 需 keepass2john + john 爆破；VeraCrypt SM3 是国密场景。
quality: medium
full_path: 2025高校网络安全管理运维赛-电子取证分析师赛道-决赛WriteUp.full.md
meta_path: 2025高校网络安全管理运维赛-电子取证分析师赛道-决赛WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025 高校网络安全管理运维赛-电子取证分析师赛道-决赛 WriteUp。2025 高校网络安全管理运维赛电子取证分析师决赛：签到 GIF + log awk + PACP pcap + Keepass + VeraCrypt + 勒索恢复 + RAID 对比。。关键路径：签到: gif 分帧-组合-画图-拼接-扫码 → 谁真正执行命令: log awk 过滤 → 网络流量 MD5 解密:...'
category: forensic
subcategory: disk_forensics
subcategories:
- disk_forensics
- memory_forensics
- misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/278549.html
reasoning_chain:
- 题面 9 道取证子题 → 触发点：覆盖签到/log/pcap/Keepass/VeraCrypt/RAID 全栈
- '签到: gif 文件 → 动作：ffmpeg 分帧 → 观察：每帧二分之一图'
- 假设：gif 分帧 - 拼接完整图 - 扫码 → 动作：组合拼图 → 观察：扫出 flag
- 谁真正执行命令：log 日志 → 动作：awk 过滤特定关键字 → 观察：b1bdef37df1a7acec711e97568c8e3b8
- 网络流量 MD5 解密：11cd6a875898416+6c37ac826a2a04bc → 动作：md5 在线查 → 观察：密钥 3c6e0b8a9c15224a
- 'PACP pcap: 协议分布 redis + http Caddy → 动作：strings 搜 1234567qwerc + /usr/share/caddy/testinfo.php'
- Keepass ironbox.safe → 假设：keepass2john + john 字典爆破 → 动作：执行 → 观察：主密码 PqR$34%sTuVwX
- VeraCrypt 加密卷 Excel 内嵌热成像图 → 动作：计算 SM3 哈希 → 观察：ce4a2f20ebc2bcdce729885ae12fb3de0a7231e6c0a8dc1cc050605f9f8f1663
- '勒索恢复: 用户 maaiyu + U 盘 jetflash → 动作：Windows 注册表 SAM 解析'
- 'RAID: lvscan + mount + diff -r back new → 动作：对比快照'
failed_attempts:
- 试图直接 cat log 找 flag → 失败：flag 不在原始日志，需 awk 过滤
- Keepass 直接 cat ironbox.safe → 失败：二进制加密文件，需 keepass2john 提 hash
- VeraCrypt 试 TrueCrypt 算法 → 失败：国密场景走 SM3
key_observations:
- Keepass 主密码爆破 = keepass2john + john 是标准链
- VeraCrypt SM3 = 国密取证场景（与传统 SHA-512 不同）
- RAID 取证 = lvscan 看卷组 + mount 挂载 + diff 对比
- 勒索恢复优先看 SAM/注册表 + U 盘插拔记录
- 网络流量取证先 strings 搜默认密码（1234567qwerc）+ 已知 web 路径
prerequisites:
- Linux 取证命令链（awk / grep / ffmpeg / strings）
- Keepass2john + John the Ripper 字典爆破
- VeraCrypt/TrueCrypt 加密卷挂载 + SM3 国密算法
- Windows 注册表 SAM 解析
---
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

11cd6a875898416+6c37ac826a2a04bc#md5解密密钥:
3c6e0b8a9c15224a

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

欢迎关注鱼影安全社区,专注CTF,职业技能大赛中高职技能培训,信息安全评估高职组赛项,金砖一带一路诸暨技能大赛:
企业信息安全赛道-攻防治理赛道-首届金砖虚拟网络建设赛道-创信大赛,世界技能大赛省选拔赛,企业赛,行业赛,电子取证和CTF系列培训,工控CTF系列，第二届网络安全行业职业技能大赛（电子取证师、渗透测试员、网络安全管理员、网络信息审核员）等。

鱼影安全团队招人啦,有感兴趣的师傅可以私信我

需要学习数据安全管理员和CTF安全培训,可以联系小编


```
11cd6a875898416+6c37ac826a2a04bc#md5解密密钥:
3c6e0b8a9c15224a
blkid ##命令，列出所有分区的 UUID、文件系统类型 lsblk -f ##参数可以树状图
systemctl list-unit-files | grep dlna #查找位置find / -name *dlna* #搜索全部路径，然后去路径查看版本即可cd/trim/var/mindlna /usr/trim/bin/minidlnad -V#执行命令 查看版本
lvscan#查看挂载的盘，发现有两个 新建两个进行挂载mkdirnewmkdirbackcd/newmount /dev/newnew/vol1cd/backmount /dev/newnew/back202510 diff -r back new #对比两个文件 -r 递归 -I 排除二进制
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