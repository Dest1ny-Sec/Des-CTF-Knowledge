---
title: 【WriteUP·中篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛
contest: WIDC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags:
- 车联网-APP
- IPA-逆向
- 命令执行双写%0截断
- WPA-PSK-空口包
- weak-password-123
- base64-16进制解码
attack_chain: 1. APP 远程控车 → 拿 IPA/2. 命令执行：双写加 %0 截断 ip=1.1.1.1%0acacatt flflagag.php/3. ssid=wifi + password=root12222 生成 PSK/4. Wireshark wpa-psk 工具生成 WPA PSK 解密空口 wifi 包/5. 弱口令 123 解压/6. Winhex base64 + 16 进制转字符串解码得 flag
key_payload: ip=1.1.1.1%0acacatt flflagag.php  PSK 生成 wireshark.org/tools/wpa-psk.html  flag{f7sgu2lsagbgfa90f63dc8b6e0e2Kg2lVW}
one_liner: 2024 WIDC 天融信杯中篇，车联网 APP 控车 + IPA 逆向 + 命令执行双写%0 截断 + WPA PSK 解密 + 弱口令 123。
lesson: 命令执行双写（flflagag.php 走 fl 跳 flag）+ %0a 截断；WPA PSK 用 ssid+password 算；Winhex 看 base64 后转 16 进制字符串。
quality: medium
full_path: 【WriteUP·中篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛.full.md
meta_path: 【WriteUP·中篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WriteUP·中篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛。2024 WIDC 天融信杯中篇，车联网 APP 控车 + IPA 逆向 + 命令执行双写%0 截断 + WPA PSK 解密 + 弱口令 123。。经验：命令执行双写（flflagag.php 走 fl 跳 flag）+ %0a 截断；WPA PSK 用 ssid+pass...
category: misc
subcategory: misc_other
tools_used:
- Wireshark
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/186393.html
reasoning_chain:
- 智能车控 APP → 触发点：远程控车接口 → 动作：抓包 + 反编译 IPA → 观察：拿到 API 端点
- 命令执行：双写 + %0a 截断 → 触发点：filter 过滤 fl 或 flag 但可双写绕过 → 动作：ip=1.1.1.1%0acacatt flflagag.php
- 观察：%0a 截断后 flflagag.php 经 fl 替回 flag → 服务器当 cat flag.php 解析 → 拿到 flag
- WPA 空口包破解 → 触发点：ssid=wifi + password=root12222 → 假设：可算 WPA PSK 解密 802.11
- 动作：用 wireshark.org/tools/wpa-psk.html 算 PSK → 观察：得到 32 字节 hex
- Wireshark 802.11 preferences 填 PSK → 触发点：解密 WPA data → 观察：解出明文 flag
- 弱口令 123 解压 zip → 触发点：zip 加密 → 动作：7z x -p123 → 观察：拿到内层文件
- Winhex 看 base64 → 触发点：内含字符串疑似 base64 → 动作：解码 + 转 16 进制字符串 → 观察：flag{f7sgu2lsagbgfa90f63dc8b6e0e2Kg2lVW}
failed_attempts:
- 试图直接 cat flag.php 绕双写 → 失败：filter 已拦 fl
- 试图手算 WPA PSK → 失败：用 wireshark.org 工具更稳
- 试图不解 PSK 直接看 WPA data → 失败：WPA 包是加密的，必须 PSK 才能解
key_observations:
- 命令执行双写（flflagag.php）+ %0a 截断是经典绕过滤招
- WPA PSK = PBKDF2(SSID + password) 算 32 字节，wireshark.org 提供在线计算
- APP 逆向 (IPA) 控车 API 是车联网题常见入口
- Wireshark 解 WPA 802.11 必须 Edit → Preferences → IEEE 802.11 → PSK
- 弱口令 123 是取证解压题高频密码
prerequisites:
- iOS IPA 反编译（class-dump / Hopper）
- Wireshark WPA 解密配置（PSK 计算 + 802.11 preferences）
- 命令注入双写 + %0a 截断手法
- base64 + 16 进制字符串互转
---
# 【WriteUP·中篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛

> 原文: https://www.ctfiot.com/186393.html
> ID: 186393

一个带有智能汽车远程控制的APP应用程序，能够通过它来发动汽车

（1）获取链接

（2）获取IPA

（3）简单的命令执行：双写加%0截断：ip=1.1.1.1%0acacatt flflagag.php

（6）由ssid：wifi和密码：root12222，生成PSK，用于解密空口wifi包内容（使用如下网址生成PSK https://www.wireshark.org/tools/wpa-psk.html）

（9）分析发现为压缩包文件，尝试打开，存在口令，此处为弱口令“123”解压出文件如下

（10）Winhex分析发现存在base64（url：https://www.qqxiuzi.cn/bianma/base64.htm）编码并再次16进制转字符串（url：https://www.sojson.com/hexadecimal.html），解码得flag

（6）flag{f7sgu2lsagbgfa90f63dc8b6e0e2Kg2lVW}

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