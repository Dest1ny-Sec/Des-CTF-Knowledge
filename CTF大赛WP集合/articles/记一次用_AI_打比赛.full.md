---
title: 记一次用 AI 打比赛
contest: BlockHarbor 比赛
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags:
- AI-assisted
- CAN-bus
- UDS
- caringcaribou
- automotive-security
- RDBI-dump
- security-access
- seed-answer
- firmware-signing
- rockyou
attack_chain:
- '题目1AutoGraph: RAMN ECU B和C的caringcaribou UDS RDBI dump日志+签名固件,提示flag是十进制secret key'
- 用rockyou.txt爆破压缩包密码(字母+数字爆不出来)
- 从candump日志重建完整固件+识别Security Access算法
- ECU C给出seed 9A5ABF0C1CAAFDEB72761E909501D6E9,求answer(32位hex大写)
- '题目2ECU C: SecurityAccess算法逆向,seed→key计算'
- flag是十进制格式的secret key
key_payload: 32位hex大写answer
one_liner: BlockHarbor汽车安全比赛AI辅助WP,涵盖caringcaribou UDS RDBI dump+Security Access算法逆向+CAN日志固件重建+seed→key计算,rockyou.txt爆破压缩包密码。
lesson: 汽车安全比赛常考UDS(统一诊断服务)+CAN总线+caringcaribou工具;SecurityAccess算法(Seed→Key)需要逆向固件提取;rockyou.txt是国外比赛压缩包密码首选字典。
quality: medium
full_path: 记一次用_AI_打比赛.full.md
meta_path: 记一次用_AI_打比赛.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '记一次用 AI 打比赛。BlockHarbor汽车安全比赛AI辅助WP,涵盖caringcaribou UDS RDBI dump+Security Access算法逆向+CAN日志固件重建+seed→key计算,rockyou.txt爆破压缩包密码。。关键路径：题目1AutoGraph: RAMN ECU B和C的caringcaribou UDS RDBI dump日志+签名固件,提示f...'
category: misc
subcategory: misc_other
tools_used:
- C
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/267997.html
reasoning_chain:
- 题目1 AutoGraph：candump 日志 + RAMN ECU B/C RDBI dump + 签名固件 → 触发点：汽车安全（UDS+CAN）
- 提示 flag 是十进制 secret key → 假设：压缩包可能用 secret key 加密 → 动作：rockyou.txt 爆破压缩包密码
- 字母+数字字典爆破失败 → 下一步：从 candump 日志重建固件
- 动作：解析 candump 重建 ECU C 完整固件 → 观察：SecurityAccess 算法签名验证逻辑
- 假设：ECU C 给 seed=9A5ABF0C1CAAFDEB72761E909501D6E9 → 要求 32 位 hex 大写 answer
- 动作：逆向固件中 SecurityAccess seed→key 算法 → 编写计算脚本 → 观察：得到 answer
- 题目2 ECU C 同样逻辑 → flag 是十进制 secret key
- AI 辅助用途：自动化 candump 解析 + 算法逆向代码补全
failed_attempts:
- 试图用 rockyou.txt 纯字母数字爆破 → 失败：密码含特殊字符或超字典范围
- 试图直接拿 candump 数据当 flag → 失败：flag 是计算后的 secret key 不是 log 字符串
- 不重建固件直接猜 answer → 失败：SecurityAccess seed→key 不可猜
key_observations:
- UDS（统一诊断服务）+ CAN 是汽车安全比赛标配，caringcaribou 是首选工具
- SecurityAccess 子服务（0x27）的 seed→key 算法是 ECU 身份认证核心
- rockyou.txt 是国际比赛压缩包密码首选字典，但纯字母数字不够
- AI 适合自动化解析 CAN 日志和补全逆向算法代码（节省体力）
prerequisites:
- UDS（ISO 14229）协议与 SecurityAccess 子服务
- CAN 总线 candump 日志格式解析
- caringcaribou 工具使用（UDS RDBI / SecurityAccess）
- rockyou.txt 字典爆破与压缩包密码学
---
# 记一次用 AI 打比赛

> 原文: https://www.ctfiot.com/267997.html
> ID: 267997

无奖竞猜：封面打码的三个字是什么

前段时间刚写了篇文章说 blockharbor 平台没什么动静，结果人家最近就办了场比赛

这次比赛是个人赛，分了红队和蓝队两个方向各四道题目，蓝队有 TARA 分析、威胁情报分析溯源类题目，红队则是两道 candump 分析题、两道 UDS 模拟题

周末结合 AI，把 candump 分析的题目做了做，UDS 模拟的题目没 get 到出题人的想法，连诊断会话都无法切换，因此没有继续深入 Orz ，接下来，讲讲怎么结合 AI 做的题

题目1：AutoGraph [RAMN]

题目说明：

Participants are provided with signed firmware files and a diagnostic log file from a "caringcaribou" UDS RDBI dump, related to a secret over-the-air (OTA) firmware portal in development for RAMN's ECU B and C.
参与者将获得来自“caringcaribou”UDS RDBI 转储的签名固件文件和诊断日志文件，该文件与为 RAMN 的 ECU B 和 C 开发的秘密无线 (OTA) 固件门户有关。

This challenge invites you to delve into intricate vehicle communication data and sophisticated security mechanisms. Can you leverage this information to unlock the ability to sign your own firmware files? Success in this endeavor promises to enable you in learning more about firmware authentication.
这项挑战将带您深入探究复杂的车辆通信数据和精密的安全机制。您能否利用这些信息解锁签名您自己的固件文件的能力？成功完成这项挑战将使您能够深入了解固件身份验证。

Prompt: I downloaded a firmware update for RAMN’s ECU B and C from a secret OTA portal in development. Can you help me sign my own firmware files? I have attached a caringcaribou UDS RDBI dump log file, if that is any help. (Note: flag is secret key in decimal format – not hexadecimal. It is NOT the password for the .zip file).
提示： 我从一个正在开发中的秘密 OTA 门户网站下载了 RAMN ECU B 和 C 的固件更新。请问您能帮我签名我自己的固件文件吗？我附上了一个 caringcaribou UDS RDBI 转储日志文件，希望对您有所帮助。（注意：flag 是十进制格式的密钥，而不是十六进制格式。它不是 .zip 文件的密码）。

这道题给了两个附件，一个是 candump 日志文件，一个带密码的压缩包

一开始爆破压缩包密码的思路是字母加数字，跑了几分钟没结果，后来考虑到国外的比赛可能用 rockyou.txt 比较好

(时间戳)  can接口  CANID#CAN数据

This challenge dives into Universal Diagnostic Services (UDS) and firmware reverse engineering. You'll need to reconstruct a complete firmware image from a raw CAN log file.
本次挑战将深入探讨通用诊断服务 (UDS) 和固件逆向工程。您需要从原始 CAN 日志文件重建完整的固件映像。

The main goal is to identify and understand a new Security Access algorithm embedded within the firmware. This algorithm is common to other automotive security access algorithms, requiring meticulous binary analysis to extract. Success hinges on your UDS knowledge and reverse engineering skills.
本次测试的主要目标是识别并理解固件中嵌入的新型安全访问算法。该算法与其他汽车安全访问算法相同，需要进行细致的二进制分析才能提取。成功与否取决于您的 UDS 知识和逆向工程技能。

Prompt: I updated my RAMN with a new firmware for ECU C, but it seems like the Security Access algorithm has been updated and I can’t unlock it anymore.
提示： 我使用 ECU C 的新固件更新了我的 RAMN，但似乎安全访问算法已更新，我无法再解锁它。

ECU C just gave me the seed: 9A5ABF0C1CAAFDEB72761E909501D6E9.
ECU C 刚刚给了我种子：9A5ABF0C1CAAFDEB72761E909501D6E9。

What is the answer to that seed? (Note: flag is 32-character hexadecimal string, all caps).
那颗种子的答案是什么？（注意：标志是 32 个字符的十六进制字符串，全部大写）。


```
Participants are provided with signed firmware files and a diagnostic log file from a "caringcaribou" UDS RDBI dump, related to a secret over-the-air (OTA) firmware portal in development for RAMN's ECU B and C.
参与者将获得来自“caringcaribou”UDS RDBI 转储的签名固件文件和诊断日志文件，该文件与为 RAMN 的 ECU B 和 C 开发的秘密无线 (OTA) 固件门户有关。

This challenge invites you to delve into intricate vehicle communication data and sophisticated security mechanisms. Can you leverage this information to unlock the ability to sign your own firmware files? Success in this endeavor promises to enable you in learning more about firmware authentication.
这项挑战将带您深入探究复杂的车辆通信数据和精密的安全机制。您能否利用这些信息解锁签名您自己的固件文件的能力？成功完成这项挑战将使您能够深入了解固件身份验证。

Prompt: I downloaded a firmware update for RAMN’s ECU B and C from a secret OTA portal in development. Can you help me sign my own firmware files? I have attached a caringcaribou UDS RDBI dump log file, if that is any help. (Note: flag is secret key in decimal format – not hexadecimal. It is NOT the password for the .zip file).
提示： 我从一个正在开发中的秘密 OTA 门户网站下载了 RAMN ECU B 和 C 的固件更新。请问您能帮我签名我自己的固件文件吗？我附上了一个 caringcaribou UDS RDBI 转储日志文件，希望对您有所帮助。（注意：flag 是十进制格式的密钥，而不是十六进制格式。它不是 .zip 文件的密码）。
(时间戳)  can接口  CANID#CAN数据
This challenge dives into Universal Diagnostic Services (UDS) and firmware reverse engineering. You'll need to reconstruct a complete firmware image from a raw CAN log file.
本次挑战将深入探讨通用诊断服务 (UDS) 和固件逆向工程。您需要从原始 CAN 日志文件重建完整的固件映像。

The main goal is to identify and understand a new Security Access algorithm embedded within the firmware. This algorithm is common to other automotive security access algorithms, requiring meticulous binary analysis to extract. Success hinges on your UDS knowledge and reverse engineering skills.
本次测试的主要目标是识别并理解固件中嵌入的新型安全访问算法。该算法与其他汽车安全访问算法相同，需要进行细致的二进制分析才能提取。成功与否取决于您的 UDS 知识和逆向工程技能。

Prompt: I updated my RAMN with a new firmware for ECU C, but it seems like the Security Access algorithm has been updated and I can’t unlock it anymore.
提示： 我使用 ECU C 的新固件更新了我的 RAMN，但似乎安全访问算法已更新，我无法再解锁它。

ECU C just gave me the seed: 9A5ABF0C1CAAFDEB72761E909501D6E9.
ECU C 刚刚给了我种子：9A5ABF0C1CAAFDEB72761E909501D6E9。

What is the answer to that seed? (Note: flag is 32-character hexadecimal string, all caps).
那颗种子的答案是什么？（注意：标志是 32 个字符的十六进制字符串，全部大写）。
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