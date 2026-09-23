---
title: 2025 腾讯游戏安全技术竞赛 - 初赛 (有源码)
contest: 腾讯游戏安全
year: 2025
difficulty: medium
vuln_type: reverse
tags:
- R3反调试
- R0驱动加载阻断
- base58自定义字符集
- 异或sxx
- ACEDriverSDK
- FilterSendMessage
- '0x10D0'
- '0x1370'
- 重命名
attack_chain:
- windbg 调试 R3 检测 → patch 模块+0x10D0 为 C3 (ret) 阻断
- R0 驱动加载时直接结束程序 → patch 模块+0x1370 为 mov rax,1; ret
- 'R3 校验: 输入以 "ACE_" 开头'
- 解密 base58 自定义字符集 "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@+/" + 异或 key "sxx
- base58_encrypt + 倒序 + '@' 前缀
- XOR "sxx" 循环
- ACEDriverSDK::Communicate(+96) 走 FilterSendMessage 发到驱动
- 驱动侧校验密文
key_payload: '''patch 0x10D0=C3 / patch 0x1370=mov rax,1;ret / base58 表+key "sxx" / ACEDriverSDK::Communicate'''
one_liner: 腾讯游戏安全初赛 — R3 windbg 阻断 + R0 驱动加载阻断 + 自定义 base58 字符集 + XOR "sxx" + ACEDriverSDK::FilterSendMessage 通信。
lesson: R3+R0 双层反调试常见：模块+0x10D0 必为 ret；驱动加载前 sub_140001370 是阻断点；base58 自定义字符集在释放时是反推关键。
quality: medium
full_path: 2025腾讯游戏安全技术竞赛初赛-题解(有源码).full.md
meta_path: 2025腾讯游戏安全技术竞赛初赛-题解(有源码).meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2025 腾讯游戏安全技术竞赛 - 初赛 (有源码)。腾讯游戏安全初赛 — R3 windbg 阻断 + R0 驱动加载阻断 + 自定义 base58 字符集 + XOR "sxx" + ACEDriverSDK::FilterSendMessage 通信。。关键路径：windbg 调试 R3 检测 → patch 模块+0x10D0 为 C3 (ret) 阻断 → R0 驱动加载时直接...
category: reverse
subcategory: reverse
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/234759.html
reasoning_chain:
- 触发点：R3 反调试检测，模块+0x10D0 处 → 假设：JMP/CALL 检测 → 动作：windbg eb 模块地址+10D0 C3 (ret) 阻断
- 下一步：R0 驱动加载阻断 → 假设：模块+0x1370 是 sub_140001370 → 动作：eb 48 C7 C0 01 00 00 00 C3 (mov rax,1;ret) 阻断
- 触发点：R3 校验要求输入以 'ACE_' 开头 → 假设：base58 自定义字符集 → 观察：释放时 dump 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@+/'
- 下一步：base58_encrypt(text) → 倒序 → 头加 '@' → XOR 'sxx' 循环
- 触发点：ACEDriverSDK::Communicate(+96) FilterSendMessage 发到驱动 → 假设：R3→R0 IOCTL 通信
- 下一步：R0 驱动做最终密文校验 → flag 输出
- 动作：逆向已知 base58 表 + XOR 'sxx' + ACEDriverSDK 类调用流程
failed_attempts:
- 试图跳过 R0 校验直接看 flag → 失败：R0 缺校验 R3 输出也被禁止
- 试图用标准 base58 → 失败：自定义表 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@+/' 不是标准 base58
- 试图 patch R0 直接拿 flag → 失败：必须照路径走完整加密流程
key_observations:
- R3+R0 双层反调试常见：模块+0x10D0 必为 ret；驱动加载前 sub_140001370 是阻断点
- base58 自定义字符集在释放时是反推关键（dump 全局看 58 个字符）
- ACEDriverSDK::FilterSendMessage 是 R3→R0 IOCTL 通信标准封装
- XOR 'sxx' 循环 + 倒序 + 头加 '@' 标志检测这类易识别
- windbg eb 直接 patch 二进制是反调试常用手法
prerequisites:
- R3 反调试技巧（API hook / patch 二进制）
- R0 驱动加载与阻断
- Base58 自定义字符集逆向
- Windows 驱动 IOCTL 通信
---
# 2025腾讯游戏安全技术竞赛初赛-题解(有源码)

> 原文: https://www.ctfiot.com/234759.html
> ID: 234759

作者论坛账号：dejavusecure

windbg 调试程序无法正常执行

绕过 R3 调试检测后在驱动加载时对程序下断， 程序会直接被结束。
这里的做法是直接在 sub_140001370 处阻止驱动加载。

创建 ACEDriverSDK 类，其中包括 安装驱动 和 与驱动的通讯逻辑 。

校验输入字符串的头部和长度: 头部必须为 ACE_ 。
长度不满足的字符串无法通过校验，这里输入随机字符串”ACE_2580219509218592511″ ，可以通过R3校验最终传递到R0。

从代码释放 base58 自定义字符集
“abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@+/” 和异或密钥 “sxx” 。
动态分析得到的自定义字符集:

释放自定义字符集的函数:

释放异或密钥的代码:

调用设置了自定义字符集的 base58_encrypt 函数对用户输入进行编码，将编码结果加上符号 ‘@’ 后倒序排列。

用异或密钥 “sxx” 循环对编码后的结果执行异或， 得到异或后的结果。

调用 ACEDriverSDK::
Communicate(+96) 发送数据到内核，传递加密得到的密文，在驱动中对密文进行验证。

通讯时调用 ACEDriverSDK::
Handler(+64) ，最终调用 FilterSendMessage 实现与内核间的通讯。

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
eb 模块地址+10D0 C3
// ret 用于阻止R3反调试执行
eb 模块地址+1370 48 C7 C0 01 00 00 00 C3
// mov rax， 1
// ret 用于阻止R0驱动加载
复制代码 隐藏代码
B8 67C30E 4490 DA C9 EB 2D 6C DA C3C9 DD 887515 A0 32 B4 D01D 23748A 9E 4B 743E 5D D71287 AB EA 88 E8 04 E7 AC 311A E0 5C 20 AE EC 6774 BE A7 A352620C 4E EC EF 1A
44 ED 0D C4 CC 42C8C30E 0C 4A DE FC F3247C 01D0 B8 8F 6E 3E 15115C D10E 53114821F4 E0 17 B5 BE 3416 F9 63 A5 F8 964D C8 EA 23 FE DF 7A 602C 5C D843 CC 5B 6C 18 FF
A5 E1 638758 BD 87919B 06D1877B 8D 87D7686B 6E 833F C6 A0 55 B3 FD 79D9 EE 4D 523E 825C B3 7A 8D DA F4A24C BA 0817 E6 5306 71
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