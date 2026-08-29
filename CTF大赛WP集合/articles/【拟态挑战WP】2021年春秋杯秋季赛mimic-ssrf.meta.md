---
title: 【拟态挑战WP】2021 春秋杯秋季赛 mimic-ssrf
contest: 春秋杯
year: 2021
difficulty: hard
vuln_type: ssrf
tags: [拟态防御-mimic-defense, 邬江兴-紫金山实验室, SSRF, file-protocol, /proc/PID/cmdline, XDebug-PHP, python-debugpy, Java-JDWP, 多异构体表决]
attack_chain: 1. SSRF file:///etc/passwd 读文件 /2. /proc/PID/cmdline 遍历进程找 3 个语言服务 (PHP/Python/Java) /3. PHP XDebug client_port 13000 → 反弹代码执行 /4. Python debugpy + Java JDWP 类似利用 /5. 三种异构体需同时返回一致结果（拟态表决）
key_payload: file:///etc/passwd  /proc/§1§/cmdline  client_port=13000  三个异构体同时执行
one_liner: 2021 春秋杯秋季赛 mimic-ssrf 拟态防御 + SSRF + XDebug/debugpy/JDWP 三语言 RCE 链。
lesson: 拟态防御（mimic defense）= 邬江兴院士 + 紫金山实验室；三语言异构体需一致响应通过表决；SSRF + XDebug 13000 端口是 PHP RCE 经典；debugpy/JDWP 是 Python/Java 对应端口。
quality: high
---

# 【拟态挑战WP】2021 春秋杯秋季赛 mimic-ssrf

## 概览
2021 春秋杯秋季赛 mimic-ssrf 题，春秋GAME 与紫金山实验室合作，基于邬江兴院士拟态防御理论。

## 题目背景
- 拟态 = mimic（多异构体表决）
- 三种开发语言 debug 调试器
- 攻击指令必须让 3 个异构体反馈一致结果，否则被表决失效

## 攻击链

### Stage 1: SSRF 入口
```
/ssrf?url=file:///etc/passwd
/ssrf?url=file:///proc/§1§/cmdline
```
- 找到 PHP/Python/Java 三个服务

### Stage 2: PHP XDebug RCE
- XDebug 扩展，client_port=13000
- 携带 `XDEBUG_SESSION_START=1` 触发反向连接
- VPS 监听 13000 端口
- 执行任意 PHP 代码

### Stage 3: Python debugpy
- 5678 端口默认
- debugpy 反向连接
- 执行 Python 代码

### Stage 4: Java JDWP
- 8000 端口默认
- JDWP 协议可执行 Java 代码
- jdb 工具连接

### Stage 5: 异构体表决
- 三个异构体同时执行相同命令
- 返回一致结果通过表决机制
- 不一致被判定为攻击并丢弃

## 经验提炼
- 拟态防御（mimic defense）= 邬江兴院士 + 紫金山实验室
- 三语言异构体需一致响应通过表决
- SSRF + XDebug 13000 端口是 PHP RCE 经典
- debugpy 5678 是 Python RCE 端口
- JDWP 8000 是 Java RCE 端口
- /proc/PID/cmdline 遍历进程
- X-Forwarded-For 头可指定反向连接目标
- 紫金山实验室是网络通信安全国家队
- 拟态表决 = 多数一致 + 异常丢弃
- mimic-ssrf 是经典 SSRF + 拟态防御复合题型
