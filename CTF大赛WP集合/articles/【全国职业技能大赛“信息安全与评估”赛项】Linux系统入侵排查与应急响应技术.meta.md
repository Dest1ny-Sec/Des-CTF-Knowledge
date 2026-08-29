---
title: 【全国职业技能大赛"信息安全与评估"赛项】Linux系统入侵排查与应急响应技术
contest: 全国职业技能大赛
year: 2024
difficulty: easy
vuln_type: forensic_disk
tags: [应急响应, Linux-IR, lsof-process, /etc/passwd, cron-check, auth.log, SSH, init.d]
attack_chain: 1. 进程排查 lsof -p PID /2. 端口 ss/netstat /3. 历史命令 history /4. 恶意文件 find /tmp /dev/shm /5. 分析恶意程序 strings+objdump /6. Linux 账户 /etc/passwd uid=0 /etc/shadow /7. cron /etc/crontab /var/spool/cron/ /8. 系统日志 /var/log/cron/message/btmp/wtmp/secure /9. .ssh authorized_keys
key_payload: lsof -p  /etc/passwd uid=0  /var/log/secure  /etc/crontab  /var/spool/cron
one_liner: 全国职业技能大赛 Linux 应急响应技术，9 大模块：进程/端口/历史/恶意文件/恶意程序/账户/cron/系统日志/.ssh。
lesson: 应急响应 9 模块：lsof 进程 + 端口 + history + find + strings + /etc/passwd + cron + /var/log + .ssh。
quality: high
---

# 【全国职业技能大赛"信息安全与评估"赛项】Linux系统入侵排查与应急响应技术

## 概览
全国职业技能大赛 Linux 应急响应 9 大模块 WP，是 IR (Incident Response) 入门级参考。

## 0x1 进程
```bash
lsof -p <pid>
```

## 0x2 安全网关/监控系统
- 排查 Web 应用防火墙、IDS/IPS、HIDS

## 0x3 端口
```bash
ss -tlnp
netstat -anpt
```

## 0x4 历史命令
```bash
history
cat ~/.bash_history
```

## 0x5 恶意文件查找
```bash
find /tmp /dev/shm /var/tmp -type f -mtime -7
find / -name "*.php" -mtime -3
```

## 0x6 分析恶意程序
```bash
strings <binary>
objdump -d <binary>
```

## 0x7 Linux 账户安全
```bash
# 所有账号
cat /etc/passwd
# 特权用户 (uid=0)
grep :0: /etc/passwd
# 密码相关
cat /etc/shadow
# 登录时间
uptime
# 当前登录
who
# 进程
w
# 最近登录
lastlog
# 远程登录
tail /var/log/auth.log
tail /var/log/secure
# sudo
cat /etc/sudoers
# 禁用/删除
usermod -L user
userdel user
userdel -r user
```

## 0x8 系统日志
```bash
/var/log/cron       # 定时任务
/var/log/cups       # 打印
/var/log/dmesg      # 内核自检
/var/log/maillog    # 邮件
/var/log/messages   # 重要信息
/var/log/btmp       # 错误登录 (lastb)
/var/log/lastlog    # 最后登录 (lastlog)
/var/log/wtmp       # 永久登录 (last)
/var/log/utmp       # 当前登录 (w/who/users)
/var/log/secure     # SSH/su/sudo
```

## 0x9 .ssh
```bash
cat ~/.ssh/authorized_keys
cat /root/.ssh/id_rsa
```

## 经验提炼
- 应急响应 9 模块：lsof 进程 + 端口 + history + find + strings + /etc/passwd + cron + /var/log + .ssh
- `grep :0: /etc/passwd` 找特权用户
- `/var/log/secure` 看 SSH 登录
- `crontab -l` + 检查 `/etc/cron.d/`
- `lsof -p` 看进程打开的文件/网络
- `userdel -r` 删用户+家目录
- `lastb` 看错误登录尝试
- `find -mtime -7` 找最近 7 天修改文件
- `strings` 提取二进制中的可打印字符串
- `/var/spool/cron/` 查用户级 cron
- 应急响应顺序：进程 → 端口 → 文件 → 账户 → 日志
