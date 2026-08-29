---
title: 【WriteUP·中篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛
contest: WIDC
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [车联网-APP, IPA-逆向, 命令执行双写%0截断, WPA-PSK-空口包, weak-password-123, base64-16进制解码]
attack_chain: 1. APP 远程控车 → 拿 IPA/2. 命令执行：双写加 %0 截断 ip=1.1.1.1%0acacatt flflagag.php/3. ssid=wifi + password=root12222 生成 PSK/4. Wireshark wpa-psk 工具生成 WPA PSK 解密空口 wifi 包/5. 弱口令 123 解压/6. Winhex base64 + 16 进制转字符串解码得 flag
key_payload: ip=1.1.1.1%0acacatt flflagag.php  PSK 生成 wireshark.org/tools/wpa-psk.html  flag{f7sgu2lsagbgfa90f63dc8b6e0e2Kg2lVW}
one_liner: 2024 WIDC 天融信杯中篇，车联网 APP 控车 + IPA 逆向 + 命令执行双写%0 截断 + WPA PSK 解密 + 弱口令 123。
lesson: 命令执行双写（flflagag.php 走 fl 跳 flag）+ %0a 截断；WPA PSK 用 ssid+password 算；Winhex 看 base64 后转 16 进制字符串。
quality: medium
---

# 【WriteUP·中篇】2024WIDC 世界智能驾驶挑战赛"天融信杯"信息安全攻防赛

## 概览
2024 WIDC 天融信杯中篇，车联网 APP 远程控车 + IPA 逆向 + 命令执行 + WPA PSK 解密。

## 题目背景
"一个带有智能汽车远程控制的 APP 应用程序，能够通过它来发动汽车"

## 攻击链

### Stage 1: 获取链接 + IPA
- 拿 APP 链接
- 拿 IPA（iOS 应用包）

### Stage 2: 命令执行双写 + %0 截断
```
ip=1.1.1.1%0acacatt flflagag.php
```
- 双写 `flflagag.php` → `fl` + `flag` 拼接 → `flag.php`
- `%0a` URL 编码换行符，截断前面 `ip=1.1.1.1`
- 等价于 `cacat flag.php` 命令注入

### Stage 3: WPA PSK 解密
- ssid: `wifi` 密码: `root12222`
- 生成 PSK：https://www.wireshark.org/tools/wpa-psk.html
- 解密空口 wifi 包内容

### Stage 4: 弱口令解压
- 压缩包口令：`123`
- 解压得文件

### Stage 5: Winhex + Base64 + 16 进制
- Winhex 分析发现 base64 编码
- 解码 base64：https://www.qqxiuzi.cn/bianma/base64.htm
- 16 进制转字符串：https://www.sojson.com/hexadecimal.html

## flag
`flag{f7sgu2lsagbgfa90f63dc8b6e0e2Kg2lVW}`

## 经验提炼
- 命令执行双写（flflagag.php 走 fl 跳 flag）+ %0a 截断
- WPA PSK 用 ssid+password 算
- Winhex 看 base64 后转 16 进制字符串
- 弱口令 123 是 CTF 入门级压缩包密码
- 双写绕过是 WAF 经典技巧
- `%0a` 是 URL 编码的换行符
- WPA-PSK 计算工具在 Wireshark 官方 tools 页面
- IPA 是 iOS 应用安装包
- APP 远程控车是车联网典型攻击场景
- Cacat 是 CAT 命令的"黑客"化变种
