---
title: WIZ Cloud Hunting Games 挑战赛 WP
contest: WIZ Cloud Hunting Games (云安全应急响应)
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [aws_cloudtrail, s3_getobject, lambda_listfunctions, mount_umount_var_log, bash_history_audit, crontab_persistence, postgresql_user_dir, findmnt_suspicious, pgsql_script_mislabeled]
attack_chain: 1) CloudTrail 查 S3 GetObject 命中 secret 文件 → 提交 arn / 2) 同上查凭证失陷 arn + 唯一扮演记录 + IP+上下文 / 3) EventName 筛 ListFunctions20150331 → Lambda 工作负载入侵 / 4) /var/log 攻击者留言 + .bash_history findmnt /tmp/.../ mount 覆盖 /var/log → umount 恢复 → auth.log 找 IP / 5) /var/spool/cron/crontabs 持久化 + pgsql 二进制实为 bash 脚本 → 攻击脚本 + curl VPS 回传 + 文件删除防泄漏
key_payload: aws s3api list-objects --bucket thebigiamchallenge-admin-storage-abf1321 --prefix 'files/' --no-sign-request / cat /home/user/postgresql-user/.bash_history / findmnt 显示 /tmp/.../ mount 在 /var_log
one_liner: WIZ Cloud Hunting Games 5 关 AWS 云安全应急响应，从 CloudTrail S3 入侵回溯到 Lambda 工作负载到 /var/log mount 隐藏到 crontab 持久化完整攻击链。
lesson: 攻击者常通过 mount tmpfs 覆盖 /var/log + .bash_history 隐藏痕迹；/var/spool/cron/crontabs 是 Debian/Ubuntu 的 cron 持久化位置（与 /etc/crontab 不同）。
quality: high
---
