---
title: 2023 年全国网络安全行业职业技能大赛 - 电子数据取证分析师（淘汰赛 C 卷）- WP
contest: 2023 全国网络安全行业职业技能大赛
year: 2023
difficulty: medium
vuln_type: forensic_memory
tags:
- 手机取证
- E01镜像
- 监控厂商
- 格式化时间
- 宝塔面板
- 远程登录IP
- 取证与溯源
attack_chain:
- 检材 1 ext4 文件系统，Asia/Shanghai 时区，IMEI 提取
- HL1sbetter WiFi 密码
- 检材 2 E01 镜像 SHA-1 计算
- 检材 3 远程登录 IP + 服务器关机时间
- 网站路径 + 数据库配置文件路径
- 检材 4 监控厂商识别 + 格式化时间
- 起始扇区 + 数据块大小
- 检材 5 系统版本号 + 命令历史第 11 条
- 第一次登录 IP + 宝塔面板密码
- 虚拟货币诈骗网站源码 + 联系人手机号
key_payload: '''检材 1: ext4 / Asia/Shanghai / HL1sbetter'''
one_liner: 取证淘汰赛 C 卷 5 检材：ext4+E01+监控+宝塔面板 综合 20 题。
lesson: 监控厂商识别靠字符串匹配；宝塔面板默认密码在 config.json；命令历史第 11 条要按序号精确定位。
quality: medium
full_path: 2023年全国网络安全行业职业技能大赛-电子数据取证分析师（淘汰赛C卷）-WP.full.md
meta_path: 2023年全国网络安全行业职业技能大赛-电子数据取证分析师（淘汰赛C卷）-WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2023 年全国网络安全行业职业技能大赛 - 电子数据取证分析师（淘汰赛 C 卷）- WP。取证淘汰赛 C 卷 5 检材：ext4+E01+监控+宝塔面板 综合 20 题。。关键路径：检材 1 ext4 文件系统，Asia/Shanghai 时区，IMEI 提取 → HL1sbetter WiFi 密码 → 检材 2 E01 镜像 SHA-1 计算。经验：监控厂商识别靠字符串匹配；宝塔面板默...
category: forensic
subcategory: memory_forensics
tools_used:
- C
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/155630.html
reasoning_chain:
- 触发点：检材 1 ext4 文件系统 → 假设取证识别 ext4 类型 → 动作：file 命令查文件类型
- 观察：ext4=flag → 操作系统 5.1 + 时区 Asia/Shanghai → 下一步：IMEI 提取
- 动作：HL1sbetter WiFi 密码 → 检材 2 E01 镜像 SHA-1 计算 → 假设哈希固定
- actor 检材 3 远程登录 IP + 服务器关机时间 → 假设 IIS/Apache 日志 → 动作：网站路径查询
- actor 数据库配置文件路径 → 假设宝塔面板默认 config.json → 观察：拿宝塔密码
- actor 检材 4 监控厂商识别 + 格式化时间 → 假设字符串匹配 Hikvision/Dahua
- 动作：起始扇区 + 数据块大小 → 检材 5 系统版本号 + 命令历史第 11 条
- actor 第一次登录 IP + 宝塔面板密码 → 假设虚拟货币诈骗网站源码 → 联系人手机号
failed_attempts:
- 试图直接 cat 看检材 → 失败：镜像需挂载或 E01 转 raw
- 试图命令历史按行统计 → 失败：第 11 条要按精确序号定位
key_observations:
- 监控厂商识别靠字符串匹配（hikvision/dahua 等）
- 宝塔面板默认密码在 /www/server/panel/config.json
- E01 镜像 SHA-1 计算要分块
- 命令历史第 11 条要按精确序号定位
prerequisites:
- E01 镜像挂载与 SHA-1 计算
- 宝塔面板目录结构
- ext4 文件系统识别
- 取证工具基础（FTK/X-Ways）
---
# 2023年全国网络安全行业职业技能大赛-电子数据取证分析师（淘汰赛C卷）-WP

> 原文: https://www.ctfiot.com/155630.html
> ID: 155630

【一个佬们都没去的比赛，一个小时随便做做，答案仅供参考】

【没有留言功能，各种勘误在首页】

任务目标

第一部分：电子数据提取与固定（30%）

总体要求：根据提供的检材，完成指定电子数据提取

任务 1：检材 1.rar 上的任务

1.提取检材的文件类型，并以此作为 flag 提交。(全小写)（3 分）

ext4

2.提取检材操作系统版本，并以此作为 flag 提交。(去除“_”，全小写)（3 分）

5.1

3.提取该检材时区，并以此作为 flag 提交。（全小写，如 utc+12:00）（7 分）

Asia/Shanghai

4.提取该手机的 IMEI 号，并以此作为 flag 提交。（7 分）

5.提取该手机连接 hlnet 的 wifi 密码，并以此作为 flag 提交。

HL1sbetter

任务 2:检材 2.e01 上的任务

1.计算检材的 SHA-1 值，以此作为 flag 提交。（4 分）

2.提取该检材中 index.rar 文件，并计算其 SHA-1 值，以此作为 flag 提交。（6 分）

第二部分：电子数据分析（30%）

任务 3:检材 3.rar 上的任务

1.分析检材，找出最近一次远程登录的 IP 地址，并以此作为 flag 提交。（3 分）

2.分析检材，找出最近以此服务器关机的时间，并以此作为 flag 提交。（格式为YYYY/MM/DDHH:MM:SS，如 2023/11/2114:37:25，去除空格）

3.分析检材中的网站路径，并以此作为 flag 提交(全小写)。（5 分）

4. 找出检材中的数据库配置文件路径，并以此作为 flag 提交（7 分）

任务 4:检材 4.e01 上的任务

1.恢复该监控镜像，找出监控厂商名，并以此作为 flag 提交。（全英文，大写）（13 分）

2.通过分析，该监控硬盘已被格式化，找出格式化时间，并以此作为 flag 提交。（格式为YYYY/MM/DDHH:MM:SS，如 2023/11/2114:37:25，去除空格）（11 分）

3. 该监控硬盘的起始扇区，并以此作为 flag 提交。（全阿拉伯数字）（6 分）

4. 该监控硬盘的数据块大小，并以此作为 flag 提交。（全阿拉伯数字）

任务 5：检材 5 上的任务

分析虚拟磁盘，通过技术手段找到信息。

1. 分析检材，找出服务器系统版本号，并以此作为 flag 提交。（3 分）

2、分析检材，查询服务器命令历史，找出第 11 条命令，并以此作为 flag 提交。（5 分）

3、分析检材，找出第一次登录服务器的 ip 地址，并以此作为 flag 提交。（3 分）

4、分析检材，找出宝塔面板的默认账号的密码，并以此作为 flag 提交。

5、分析检材，找出宝塔面板上涉及虚拟货币诈骗的网站源码存放位置，并以此作为 flag 提交。（7 分）

6、分析检材，查询宝塔面板绑定的联系人手机号，并以此作为 flag 提交。

原文始发于微信公众号（取证与溯源）：2023年全国网络安全行业职业技能大赛-电子数据取证分析师（淘汰赛C卷）-WP

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