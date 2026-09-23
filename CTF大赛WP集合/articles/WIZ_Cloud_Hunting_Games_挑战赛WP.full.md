---
title: WIZ Cloud Hunting Games 挑战赛 WP
contest: WIZ Cloud Hunting Games (云安全应急响应)
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- aws_cloudtrail
- s3_getobject
- lambda_listfunctions
- mount_umount_var_log
- bash_history_audit
- crontab_persistence
- postgresql_user_dir
- findmnt_suspicious
- pgsql_script_mislabeled
attack_chain: 1) CloudTrail 查 S3 GetObject 命中 secret 文件 → 提交 arn / 2) 同上查凭证失陷 arn + 唯一扮演记录 + IP+上下文 / 3) EventName 筛 ListFunctions20150331 → Lambda 工作负载入侵 / 4) /var/log 攻击者留言 + .bash_history findmnt /tmp/.../ mount 覆盖 /var/log → umount 恢复 → auth.log 找 IP / 5) /var/spool/cron/crontabs 持久化 + pgsql 二进制实为 bash 脚本 → 攻击脚本 + curl VPS 回传 + 文件删除防泄漏
key_payload: aws s3api list-objects --bucket thebigiamchallenge-admin-storage-abf1321 --prefix 'files/' --no-sign-request / cat /home/user/postgresql-user/.bash_history / findmnt 显示 /tmp/.../ mount 在 /var_log
one_liner: WIZ Cloud Hunting Games 5 关 AWS 云安全应急响应，从 CloudTrail S3 入侵回溯到 Lambda 工作负载到 /var/log mount 隐藏到 crontab 持久化完整攻击链。
lesson: 攻击者常通过 mount tmpfs 覆盖 /var/log + .bash_history 隐藏痕迹；/var/spool/cron/crontabs 是 Debian/Ubuntu 的 cron 持久化位置（与 /etc/crontab 不同）。
quality: high
full_path: WIZ_Cloud_Hunting_Games_挑战赛WP.full.md
meta_path: WIZ_Cloud_Hunting_Games_挑战赛WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: WIZ Cloud Hunting Games 挑战赛 WP。WIZ Cloud Hunting Games 5 关 AWS 云安全应急响应，从 CloudTrail S3 入侵回溯到 Lambda 工作负载到 /var/log mount 隐藏到 crontab 持久化完整攻击链。。经验：攻击者常通过 mount tmpfs 覆盖 /var/log + .bash_history 隐藏痕迹...
category: web
subcategory: web_other
tools_used:
- curl
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/247131.html
reasoning_chain:
- 触发点：5 关 AWS 云安全应急响应 → 假设：CloudTrail 日志 + S3 入侵回溯
- 任务 1：CloudTrail 查 S3 GetObject 命中 secret 文件 → 动作：aws s3api list-objects --bucket thebigiamchallenge-admin-storage-abf1321 --prefix 'files/' --no-sign-request → 提交 arn
- 任务 2：凭证失陷 arn + 唯一扮演记录 + IP+上下文 → aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole
- 任务 3：EventName 筛 ListFunctions20150331 → Lambda 工作负载入侵 → aws lambda list-functions
- 任务 4：/var/log 攻击者留言 + .bash_history findmnt /tmp/.../ mount 覆盖 /var/log → 动作：umount 恢复 → 假设：auth.log 找 IP
- 动作：mount tmpfs /var/log + 隐藏日志 → 攻击者用 mount tmpfs 覆盖 /var/log 隐藏痕迹
- 任务 5：/var/spool/cron/crontabs 持久化 + pgsql 二进制实为 bash 脚本 → 动作：cat /var/spool/cron/crontabs/* + file /usr/bin/postgres
- 假设：pgsql 是 bash 脚本伪装 + curl VPS 回传 + rm 删除文件防泄漏 → 假设：必须恢复并审计
- 观察：5 关 flag 完整覆盖 AWS IAM + Lambda + S3 + crontab + 持久化攻击链
failed_attempts:
- 任务 1 试图直接登录 S3 GetObject → 失败：必须用 --no-sign-request 公共桶访问
- 任务 4 试图 cat /var/log/auth.log → 失败：被 tmpfs mount 覆盖
- 任务 5 试图用 ps 看 postgres 进程 → 失败：pgsql 二进制实为 bash 脚本伪装，需要 file / cat 审计
key_observations:
- 攻击者常通过 mount tmpfs 覆盖 /var/log + .bash_history 隐藏痕迹；umount 恢复 + 历史审计是关键
- /var/spool/cron/crontabs 是 Debian/Ubuntu 的 cron 持久化位置（与 /etc/crontab 不同）
- AWS CloudTrail 是云应急响应的核心数据源（事件名 + 角色 + IP 上下文）
- ListFunctions + Lambda GetFunction 是 AWS 工作负载入侵常见审计触发
- 二进制伪装 pgsql → 实为 bash 脚本是 Linux 持久化的高级手法
prerequisites:
- AWS CLI（s3api / cloudtrail / lambda）
- Linux 文件系统（mount / findmnt / umount）
- Linux 持久化机制（crontab / pgsql 伪装）
- 云应急响应流程（CloudTrail → S3 → Lambda）
- bash 脚本审计（curl VPS 回传 / 文件删除）
---
# WIZ Cloud Hunting Games 挑战赛WP

> 原文: https://www.ctfiot.com/247131.html
> ID: 247131

点击蓝字

关注我们

声明

本文作者：shadowabi
本文字数：3029字

阅读时长：约8分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

Cloud Hunting Games 是 WIZ 最新推出的一个新的 CTF 挑战赛，这一次是从云安全应急响应的维度来进行挑战。
挑战赛入口：https://www.cloudhuntinggames.com

背景

❝

ExfilCola 是一家很有前途的初创公司，拥有可以打破可乐巨头双头垄断的革命性苏打水配方，它收到了一封来自名为“FizzShadows”的威胁组织的数据勒索电子邮件，声称已经破坏了他们的系统。

如果秘方被盗，公司的未来将面临直接风险。作为选定的专家，您必须防止公式被泄露在为时已晚之前。

Challenge 1

这一关其实就是去调查取证，找到秘密配方被窃取的证据，并提供当时被调用的身份凭证 arn 号。

查询语句官方已经默认给好了，直接点 RUN Query 即可

然后点 Columns，筛选我们需要的关键信息。

很显然，根据线索的提示，这是 S3 存储桶内的文件窃取，那么我们需要筛选出，GetObject 事件，访问的 object 需要和 secret 相关，以及 arn 号

那么就是这三列

可以选择 Download as CSV，在 excel 表格里筛选

也可以用 search 功能来搜

拉到最下面，可以发现，这个 txt 是比较可疑的，提交对应的 arn 号即可

Challenge 2

在挑战 1 中，我们找到了 arn 号，接下来就需要去溯源这个身份凭证是什么时候被失陷的。

和上面一样的方法，这里给出最佳解法：

这个  Moe.Jito 并不是常见的调用用户，而且仅有一次扮演记录，很可疑。也可以综合 IP 和上下文调用记录、凭证失陷时间来判断。

Challenge 3

这个挑战就是继续深挖，攻击者是否有横向移动的痕迹。

直接下载整个 CSV，我的办法是筛选 EventName，看日志中是否有和服务器相关的，然后再结合上下文判断

EventName 中有一个 ListFunctions20150331 事件，查看发现是和云函数相关的，并且根据后续的行动，可推断该函数和获取凭证相关，且后续有攻击者使用痕迹

此时可证明，该云函数工作负载已遭到攻击者入侵

Challenge 4

第四关应该是最难的一关，非常容易想太多。

第四关是找，攻击者是怎么入侵该云函数的工作负载的。

已经提示了机器不出网，所以可以排除和网络连接相关的入侵手法。

很显然，找攻击者什么时候入侵机器，第一想法是找 ssh 登录日志

last 提示文件不存在。去 /var/log 里找，发现有攻击者的留言。

有可能日志被删了，或者被隐藏了

回到最开始的地方，我们并不是在 /root 目录中，而是在 /home/user 中，这也是一个提示

当前目录下没文件，但是返回 home 目录，会发现有一个 postgresql-user 目录

两个python文件很显然是用来获取凭证的，而 .bash_history 则揭示了攻击者所使用的手法。

由于 history 文件内容多，这里用 head 即可

先去跟 /tmp/…/ 目录，因为这很显然是一个隐藏目录，正常程序不会这样写

可以发现，这里的内容和 /var/log 一致，再结合 .bash_history 中的 findmnt，大概率，攻击者是用这里的文件夹 mount 了 /var/log

在 findmnt 中也是这样的

直接 umount /var/log 即可

然后进入 /var/log，发现有个 auth.log，head auth.log 能得到攻击者 ip

Challenge 5

这一关相对简单，提示攻击者做了持久化，要反打攻击者。

做持久化，最明显就是 crontab 定时任务。直接用 crontab -l 或者 找 /etc/crontab/ 是没东西的。

这里我差点就错过关键线索，在群友的提醒下，/var/spool/cron/crontabs 也是可以放的，我之前一直以为这是 centos 才会放这。

第二个坑点来了，这里看起来是某个 pgsql 的二进制文件，但仔细看参数，他是用 bash 执行的，也就是说，他必然是一个 sh 脚本。

这里把 sh 脚本解开会得到攻击者的完整攻击脚本。

这里我们只需要关注攻击者怎么将结果回传到他的 VPS 上即可

这里就很明显了，结果是通过 curl 回传到他的服务器上的，直接把攻击脚本前面的变量拼接进来就可以了

根据任务提示，我们需要去删除掉泄漏的秘密。恰好他的文件管理系统是有删除功能的，直接删就过关了。

通关凭证

shadowabi 和 他的小伙伴们组团上分，是国内第一批打完这个挑战赛的。

作者

shadowabi

自强不息

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec

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