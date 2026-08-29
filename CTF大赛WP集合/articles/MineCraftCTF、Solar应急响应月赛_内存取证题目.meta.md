---
title: MineCraftCTF + Solar 应急响应月赛 内存取证
contest: MineCraftCTF + Solar 月赛
year: 2025
difficulty: medium
vuln_type: forensic_memory
tags: [勒索病毒, Volatility 内存取证, webshell, 攻击者 IP, 外联 IP]
attack_chain: |
  1. 题目: Minecraft 服务器被勒索组织投放勒索病毒，文件被加密，服务器内存镜像打包排查
  2. 第 1 题: 攻击者 IP
     - 用 volatility 检查镜像 → 找 PHP webshell (shell.php)
     - 搜 index.php 日志 → 找 POST /uploads/shell.php 请求
     - REMOTE_ADDR: 10.10.0.1 → 攻击者 IP
  3. 第 2 题: 攻击者外联 IP 和端口
     - volatility imageinfo → profile=Win7SP1x64
     - volatility netscan → 找网络连接
     - 找到 wininit.exe (PID 372) 监听 49152 端口 → 外联 IP
  4. 第 6 题: 不会 (待定)
key_payload: |
  # 找攻击者 IP:
  # 搜日志 "index.php" → 找 POST /uploads/shell.php 请求
  # REMOTE_ADDR: 10.10.0.1
  POST /uploads/shell.php HTTP/1.1
  Host: 10.10.0.133
  User-Agent: Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 4901
  
  # volatility 内存取证:
  volatility_2.6_win64_standalone.exe -f memdump.mem imageinfo
  # Suggested Profile(s): Win7SP1x64
  
  # volatility netscan:
  volatility.exe -f memdump.mem --profile=Win7SP1x64 netscan
  # 0x3e176630  TCPv6  :::49152  LISTENING  372  wininit.exe
  # 0x3e1a4e60  TCPv4  0.0.0.0:49153  LISTENING  772  svchost.exe
one_liner: MineCraftCTF + Solar 月赛内存取证：搜日志找攻击者 IP (10.10.0.1) + netscan 找外联 IP + 端口。
lesson: |
  - 内存取证找攻击者 IP: 搜日志 + 找 REMOTE_ADDR
  - 找外联 IP: volatility netscan 找监听端口 + 进程
  - Win7SP1x64 镜像 profile 兼容性最好
  - 勒索病毒内存取证: 不仅找病毒文件，还需找病毒下载源 (C2 IP) 和传播路径
  - 真实环境勒索病毒取证需要隔离环境
quality: medium
---

# MineCraftCTF + Solar 应急响应月赛 内存取证

> 来源: ctfiot.com 265387

## 题目背景

Minecraft 多人服务器被勒索组织投放勒索病毒，文件被加密。技术把服务器内存镜像打包交给极安云科排查。

> 注意：本题涉及真实环境勒索病毒，需要隔离环境。

## 第 1 题：攻击者 IP

```http
POST /uploads/shell.php HTTP/1.1
Host: 10.10.0.133
User-Agent: Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Referer: http://10.10.0.133/index.php?msg=文件上传成功！文件名: shell.php, 大小: 0.03 KB&type=success
Content-Type: application/x-www-form-urlencoded
Content-Length: 4901
Connection: close

DOCUMENT_ROOT: C:/phpstudy_pro/WWW
SERVER_SOFTWARE: nginx/1.15.11
REMOTE_ADDR: 10.10.0.1
REMOTE_PORT: 59820
SERVER_ADDR: 10.10.0.133
```

**攻击者 IP = 10.10.0.1**

## 第 2 题：攻击者外联 IP 和端口

```bash
volatility_2.6_win64_standalone.exe -f memdump.mem imageinfo
# Suggested Profile(s): Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, ...

volatility.exe -f memdump.mem --profile=Win7SP1x64 netscan
# 0x3e176630  TCPv6  :::49152  LISTENING  372  wininit.exe
# 0x3e1797b0  TCPv4  0.0.0.0:49153  LISTENING  772  svchost.exe
# 0x3e1a4e60  TCPv4  0.0.0.0:49154  LISTENING  ...
```

## 第 6 题：不会

（待补充）

## 评价

MineCraftCTF + Solar 应急响应月赛内存取证题，亮点是：
- **真实勒索病毒** 内存镜像排查
- **PHP webshell** `shell.php` 通过文件上传进入服务器
- **REMOTE_ADDR 攻击者 IP** 是经典 web 日志取证
- **Win7SP1x64 镜像** 是取证最常见 profile

适合蓝队 / 应急响应工程师学习。
