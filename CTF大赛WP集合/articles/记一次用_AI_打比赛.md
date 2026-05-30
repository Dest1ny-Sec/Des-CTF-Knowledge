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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815905-wxsync-2025-09-c3ccd184e1ee377edccd9fcdfc214312.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815907-wxsync-2025-09-619fa64d23319cc26632c96fc6a233de.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815909-wxsync-2025-09-26b8914267505e8067f6cdc7edfaefe9.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815911-wxsync-2025-09-e9644e76423ec14accbd3e35372c6ee7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815913-wxsync-2025-09-217457e76a6e476b3c1e980979933681.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815915-wxsync-2025-09-01a11dabf10b296af2b1c89df05969cb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815917-wxsync-2025-09-21a5c90826a1ed1afd7711ff92960fbe.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815920-wxsync-2025-09-7170b199f1812e197227fdb4b3cc4682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815922-wxsync-2025-09-a916ea4e319cb0f922650b8e74af6c0e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1756815924-wxsync-2025-09-b98e82224434f4961125d67bc837c07a.png)