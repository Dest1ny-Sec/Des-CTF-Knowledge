---
title: 2023 全国网络安全行业职业技能大赛 - 网络安全管理员 - 决赛 WP
contest: 2023 全国网络安全行业职业技能大赛
year: 2023
difficulty: easy
vuln_type: misc_unknown
tags:
- IDA_F5
- Linux后门
- 勒索程序
- RSA公钥提取
- .NET反编译
- 动态调试
- VBA宏
- XML外链
- 网络安全管理员
attack_chain:
- 题 7 恶意样本分析：丢进 ida f5 找字符串 flag{armtant_info.net}
- 题 8 Linux 后门分析：netstat -ano 看对外连接 IP flag{118.195.244.213}
- 题 9 勒索程序：F12 字符串找 .onion 网址 + RSA 公钥前 10 字符
- 题 10 PE 社工钓鱼：动态调试看连接 https://www.google.com
- 提取 16 字节密钥 0x264c7298bee40000...
- 反射加载 ArgenTINA.dll
- 题 11 文档类社工：解压 .docx + word/_rels/document.xml.rels 找恶意外链
- 提取外链 du.testjj.com
key_payload: '''armtant_info.net / 118.195.244.213 / royal2xthig3ou5hd7zsliqagy6yygk2cdelaxtni2fyad6dpmpxedid.onion'''
one_liner: 网络安全管理员职业技能 5 题：IDA 反编译 + Linux 后门 + 勒索 + .NET + 文档宏。
lesson: 取证题靠 IDA 字符串 + netstat + 反射加载 + .docx 解压看 _rels；RSA 公钥前 10 字符直接 F5 拿。
quality: medium
full_path: 2023全国网络安全行业职业技能大赛-网络安全管理员-决赛WP.full.md
meta_path: 2023全国网络安全行业职业技能大赛-网络安全管理员-决赛WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2023 全国网络安全行业职业技能大赛 - 网络安全管理员 - 决赛 WP。网络安全管理员职业技能 5 题：IDA 反编译 + Linux 后门 + 勒索 + .NET + 文档宏。。关键路径：题 7 恶意样本分析：丢进 ida f5 找字符串 flag{armtant_info.net} → 题 8 Linux 后门分析：netstat -ano 看对外连接 IP flag{118.195...
category: misc
subcategory: misc_other
tools_used:
- IDA
time_required: quick
difficulty_score: 2
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/155372.html
reasoning_chain:
- 触发点：题 7 恶意样本丢 IDA F5 → 假设字符串找 flag → 动作：F12 找 flag{armtant_info.net}
- 触发点：题 8 Linux 后门 netstat -ano → 假设外连 IP 是 flag → 观察：118.195.244.213
- actor 题 9 勒索程序 F12 找 .onion 网址 → 假设 RSA 公钥前 10 字符 → 动作：F5 找密钥
- 观察：http://royal2xthig3ou5hd7zsliqagy6yygk2cdelaxtni2fyad6dpmpxedid.onion + MIICCAKCAg → flag
- actor 题 10 PE 社工钓鱼 → 假设动态调试看外连 → 动作：https://www.google.com
- 动作：提取 16 字节密钥 0x264c7298bee40000 → 假设反射加载 → 观察：ArgenTINA.dll
- actor 题 11 文档类社工 → 假设解压 .docx 看 _rels → 动作：找恶意外链
- 观察：du.testjj.com →触发点：取证靠 IDA 字符串 + netstat + 反射加载 + .docx 解压
failed_attempts:
- 试图手工跟踪勒索程序加密逻辑 → 失败：解密需要受害私钥
- 试图静态分析 .NET 反射加载 → 失败：必须运行时拿 ArgenTINA.dll
key_observations:
- 取证题靠 IDA 字符串 + netstat + 反射加载 + .docx 解压看 _rels
- RSA 公钥前 10 字符直接 F5 拿
- 反射加载 ArgenTINA.dll 是 .NET 后门常见模式
- docx 解压看 _rels/document.xml.rels 找恶意外链
prerequisites:
- IDA Pro F5/F12 字符串搜索
- Linux netstat 命令与后门排查
- .NET 反射加载机制
- Office 文档结构（docx + rels）
---
# 2023全国网络安全行业职业技能大赛-网络安全管理员-决赛WP

> 原文: https://www.ctfiot.com/155372.html
> ID: 155372

2023全国网络安全行业职业技能大赛-网络安全管理员-决赛WP

前言

把最近参加的全国网络安全行业职业技能大赛决赛的第三部分：网络安全处置做的题（答案可能不对仅供参考） 进行记录下。

7. 恶意样本分析

丢进ida f5一下 flag{armtant_info.net}

8. Linux 后门分析

最简单的方法直接在linux虚拟机运行，然后netstat -ano查看对外连接ip即可。flag{118.195.244.213}

9.勒索程序分析

9-1 请问该网址是什么？

丢到ida f12查看字符串都能看到 。

flag{http://royal2xthig3ou5hd7zsliqagy6yygk2cdelaxtni2fyad6dpmpxedid.onion}

9-2 RSA 公钥的前10 个字符？

f5一下查看密钥就出来了。flag{MIICCAKCAg}

10 社工钓鱼分析（PE 类）

10-1 尝试连接一个 URL 来判断当前的网络连接状态该URL 是什么？

解压查看发现是一个.net程序并且进行了混淆，这里直接动态调试。

直接挂起动态调试，一眼就看出来对外连接地址https://www.google.com。

flag{https://www.google.com}

10-2 16 字节的密钥?

密钥就是当前面访问状态返回值为OK时候，进行循环，这里当num3>6的时候后续字节都为空，这边代码提取出来转hex一下就行。flag{0x264c7298bee400000000000000000000}

10-3 文件的文件名是什么?

根据之前密钥解密的字符串，通过分析后续代码是进行反射加载的。所以在反射加载之前将字节保存下来在丢进dnspy即可得到dll文件名。

flag{ArgenTINA.dll}

11 社工钓鱼分析（文档类）

根据题目和提供的附件猜测是关于Word类型病毒，其中类型主要有两种一种是创建VBA脚本，打开文档时执行恶意宏。另外一种嵌入在名为”word/rels/document.xml.rels”的XML文件中的外部链接。

直接修改后缀解压在word/_rels/document.xml.rels找到恶意外链地址。

flag{du.testjj.com}

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