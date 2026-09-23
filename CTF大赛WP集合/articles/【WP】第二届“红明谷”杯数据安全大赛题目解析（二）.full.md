---
title: 【WP】第二届"红明谷"杯数据安全大赛题目解析（二）
contest: 红明谷
year: 2022
difficulty: hard
vuln_type: forensic_memory
tags:
- SM2-Biased-nonce-attack
- HNP-lattice
- DPAPI-blob
- Master-Key
- volatility-imageinfo
- hashdump-getsids
- mftparser
- CVE-2022
attack_chain: '1. SM2: nonce 前 6 bits 永远 0 + 构造 HNP 格子解密钥 /2. MissingFile: volatility imageinfo + filescan + mftparser + hivelist + hashdump + getsids + dpapi masterkey 解 + dpapi blob 解得 flag{Hide_Behind_Windows}'
key_payload: dpapi masterkey  SID=S-1-5-21-206512979-2006505507-2644814589-1001  password=123456  flag{Hide_Behind_Windows}
one_liner: 第二届红明谷杯题解（二），SM2 biased nonce 攻击 + DPAPI masterkey/blob 内存取证解密。
lesson: SM2 nonce 偏差攻击用 HNP (Hidden Number Problem) 构造 LLL 格；DPAPI Master Key 用用户密码 + SID + 16 字节随机数加密；volatility mftparser + hivelist + hashdump 是 Windows 内存取证三件套。
quality: high
full_path: 【WP】第二届“红明谷”杯数据安全大赛题目解析（二）.full.md
meta_path: 【WP】第二届“红明谷”杯数据安全大赛题目解析（二）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WP】第二届"红明谷"杯数据安全大赛题目解析（二）。第二届红明谷杯题解（二），SM2 biased nonce 攻击 + DPAPI masterkey/blob 内存取证解密。。经验：SM2 nonce 偏差攻击用 HNP (Hidden Number Problem) 构造 LLL 格；DPAPI M...
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/32512.html
reasoning_chain:
- SM2 题：nonce 有 bias（前 6 bits 永为 0）→ 触发点：Biased nonce attack → 假设：可构造 HNP 格子
- 动作：Sage 构造 LLL 还原私钥 → 观察：拿到 d 后解 SM2 flag
- MissingFile 内存取证：volatility imageinfo → 触发点：Win7SP1x86 profile → 动作：filescan 找 Hacker 路径
- 动作：mftparser > mtfparser.txt 找可疑文件 → 观察：定位 dump_S3cret + master.key
- DPAPI 流程：hivelist 找 SYSTEM/SAM → hashdump 提 NTLM hash → getsids 提 SID
- 动作：masterkey /in:master.key /sid:S-1-5-21-... /password:123456 → 观察：得到 Master Key 092c42...
- 动作：dpapi blob /in:dump_S3cret /masterkey:092c... → 观察：得到 flag{Hide_Behind_Windows}
failed_attempts:
- 试图直接 vol.py filescan 拿 flag → 失败：flag 被 DPAPI 加密，必须 master key 解
- 试图爆破 DPAPI 密码 → 失败：密码已给 123456
- 试图不解 master key 直接解 blob → 失败：blob 必须 master key 才能解
key_observations:
- Biased nonce attack = HNP (Hidden Number Problem) + LLL 格还原私钥
- DPAPI Master Key = SID + 用户密码 + 16 字节随机数三重加密
- volatility mftparser + hivelist + hashdump 是 Windows 内存取证三件套
- SM2 nonce 偏差攻击与 ECDSA nonce 偏差是同一类 HNP 问题
- DPAPI 是 Windows 保护凭据的核心 API，CTF 内存取证必考
prerequisites:
- SM2 算法原理与 biased nonce 攻击
- Sage LLL 格子基础
- volatility 2.x 插件用法（imageinfo/filescan/mftparser/hashdump/getsids）
- DPAPI 加密体系（master key + blob 解密链）
---
# 【WP】第二届“红明谷”杯数据安全大赛题目解析（二）

> 原文: https://www.ctfiot.com/32512.html
> ID: 32512

SM2

题目知识点：

Biased nonce attack

观察代码发现 nonce 有一定 bias，前 6 bits 永远是 0，构造格子解 HNP 得到密钥，解密得到 flag。

poc链接：https://raw.githubusercontent.com/chunqiugame/cqb_writeups/master/2022hmgb/sm2_poc.sage

MissingFile

00 楔子

本意是为了考察选手对于MTF的一些认知，以及对于微软里面常见的一个API CryptProtectData加密获得的数据，也就是常说的 DPAPI Blob的一些了解程度的考察。但是为了方便出题（其实是自己折磨自己了），用了各种办法将数据读入内存，反而导致flag的泄露（疑似是flag也被存在了内存中，还没有被抹去），导致出现了非预期解，给各位师傅道歉了。

01 致知力行

题目描述: 某日Akira检查自己电脑时，发现机器好像中毒了！Akira试着抢救，但被病毒发现，只剩下了一份快照，这份快照能帮Akira找到病毒留下的秘密吗？

题目描述中提到了机器中毒，其实就是指这台电脑 已经被攻击过，暗示memory之中会残留一些攻击者利用过的数据。通常情况下，内存中残留的数据不足以进行数据恢复，但是在某些特定情况下，数据已被加载到内存中时，便有获取某一些特定数据的机会，这一题就是模拟此场景。同时提到了被病毒发现，其实这里是想表达病毒进行了自我数据删除，所以有数据残留。

加密数据发现

对于这类内存分析题，首先通过volatility调查当前内存的版本。

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群

Q群:
703460426


```
Biased nonce attack
.volatility_2.6_win64_standalone.exe -f memory imageinfo
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 filescan
UsersNewGuestDesktopHacker
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 mftparser > mtfparser.txt
DPAPI：
全称Data Protection Application Programming Interface

DPAPI blob：
一段密文，可使用Master Key对其解密

Master Key：
64字节，用于解密DPAPI blob，使用用户登录密码、SID和16字节随机数加密后保存在Master Key file中

Master Key file：
二进制文件，可使用用户登录密码对其解密，获得Master Key

这部分内容选自：https://3gstudent.github.io/%E6%B8%97%E9%80%8F%E6%8A%80%E5%B7%A7-%E5%88%A9%E7%94%A8Masterkey%E7%A6%BB%E7%BA%BF%E5%AF%BC%E5%87%BAChrome%E6%B5%8F%E8%A7%88%E5%99%A8%E4%B8%AD%E4%BF%9D%E5%AD%98%E7%9A%84%E5%AF%86%E7%A0%81
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 hivelist
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 hashdump
.volatility_2.6_win64_standalone.exe -f memory --profile=Win7SP1x86 getsids
dpapi::
masterkey /in:"master.key" /sid:S-1-5-21-206512979-2006505507-2644814589-1001 /password:
123456
dpapi::
blob /in:
dump_S3cret /masterkey:
092c4220064c30bc7f8b15d2d48957c4926af0632149b9c08cd87f34fc43aa1204d775bdc6ab429a0d4d0826fb80b08250b125d92913e2f7578cf778073bfe38
flag{Hide_Behind_Windows}
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