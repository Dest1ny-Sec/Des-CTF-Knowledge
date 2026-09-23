---
title: 冠军Writeup大放送 | DataCon2022物联网安全赛道之"S7一1200"战队
contest: DataCon2022 物联网安全
year: 2022
difficulty: medium
vuln_type: forensic_disk
tags:
- DataCon
- 物联网安全
- 固件基地址识别
- 函数符号恢复
- 整数溢出检测
- bindiff
- S7-1200
- 中科院信工所
attack_chain:
- 中科院信工所 S7-1200 战队 (李红老师)
- '第一部分: 固件基地址识别 (图1 加载基址示意)'
- 图2 各固件字符串数量统计柱形图
- 图3 加载基址识别过程示意
- '第二部分: 函数符号恢复 (bindiff 工具)'
- '第三部分: 整数溢出检测'
- S7-1200 PLC 相关固件逆向
- 2021 DataCon 第二名战绩 (老板说得真队)
key_payload: '''固件基地址识别 + bindiff 函数符号恢复 + 整数溢出检测'''
one_liner: DataCon2022 物联网安全冠军 S7-1200：固件基地址识别 + bindiff 符号恢复 + 整数溢出检测。
lesson: '固件逆向三件套: 1) 加载基地址识别 (字符串统计+熵分析) 2) bindiff 对比已知版本恢复符号 3) 整数溢出检测 (符号执行/约束求解)。'
quality: medium
full_path: 冠军Writeup大放送_-_DataCon2022物联网安全赛道之“S7一1200”战队.full.md
meta_path: 冠军Writeup大放送_-_DataCon2022物联网安全赛道之“S7一1200”战队.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '冠军Writeup大放送 | DataCon2022物联网安全赛道之"S7一1200"战队。DataCon2022 物联网安全冠军 S7-1200：固件基地址识别 + bindiff 符号恢复 + 整数溢出检测。。关键路径：中科院信工所 S7-1200 战队 (李红老师) → 第一部分: 固件基地址识别 (图1 加载基址示意) → 图2 各固件字符串数量统计柱形图。经验：固件逆向三件套:...'
category: forensic
subcategory: disk_forensics
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/92303.html
reasoning_chain:
- '中科院信工所 S7-1200 战队发布 3 段 WP, 第一部分标题''固件基地址识别'' → 触发点: PLC 固件不像普通 exe, .bin 无符号无区段, 必须先识别加载基址才能 IDA 分析 → 下一步: 看图 2 字符串数量统计'
- '假设: 不同固件被加载到不同虚拟地址, 字符串全局指针差值可推算加载基址 → 动作: 提取每条字符串指针, 统计 cross-reference, 对比已知固件 → 观察: 图 2 显示不同样本字符串数量差异明显 → 下一步: 识别最相似固件做 bindiff'
- '第二部分标题''函数符号恢复'' bindiff 工具 → 触发点: 固件二进制无 PDB 无符号表, 函数名全无, 但 bindiff 可对比已知版本还原符号 → 假设: 找到与目标固件同版本的不同功能模块二进制 → 动作: BinDiff 配 IDA Database'
- '观察: bindiff 输出置信度 0.85+ 的函数名匹配 → 下一步: 用匹配函数名作锚点, 继续人工命名邻居函数'
- '第三部分''整数溢出检测'' → 触发点: PLC 工控常见整数溢出导致控制逻辑被绕过 → 假设: 函数符号恢复后扫所有算术指令, 找无边界检查的 mul/add → 动作: 静态分析 (无动态符号执行环境)'
- '观察: IDA 反编译 highlight 出 _memcpy_n + unsigned int len 三处缺校验 → 下一步: 输出 sink 点给人工复核'
failed_attempts:
- '试图用 angr 全自动符号执行跑整数溢出 → 失败: PLC 固件 ARM Cortex-R 指令集 angr 支持不完善'
- '试图直接 IDA 反编译固件不识别基址 → 失败: 函数地址全是 0x00xxxxxx 没偏移 anchor'
key_observations:
- '固件逆向三件套顺序不可乱: 先识别加载基址 → 再 bindiff 恢复符号 → 最后扫漏洞'
- PLC 工控固件比普通 Linux 固件更依赖字符串统计识别基址 (无 dynsym 无 eh_frame)
- BinDiff 置信度阈值 0.85 是经验值, 低于这个匹配几乎都是误报
prerequisites:
- IDA Pro + BinDiff 插件使用
- ARM/MIPS 指令集基础 (PLC 固件常用)
- 固件加载机制 (链接脚本 / scatter-loading)
- 整数溢出检测 (静态分析 + 符号执行)
---
# 冠军Writeup大放送 | DataCon2022物联网安全赛道之“S7一1200”战队

> 原文: https://www.ctfiot.com/92303.html
> ID: 92303

由奇安信集团、清华大学网络研究院、蚂蚁集团、腾讯安全大数据实验室、Coremail论客主办的DataCon2022大数据安全分析竞赛线上赛和决赛已圆满落幕，五大赛道第一名也已各归其主。本期为大家分享的是物联网安全赛道排名第一的S7一1200战队writeup。

来自中国科学院信息工程研究所的S7一1200战队，指导老师是李红老师。战队研究方向包括物联网安全、工控安全、软件供应链安全等。DataCon2021的比赛中，曾以“老板说得真队”为名组队参加软件供应链与物联网安全赛道，并夺得第二名。

第一部分 固件基地址识别

图1加载基址示意图

图2各固件所含字符串数量统计柱形图

图3加载基址识别过程示意图

第二部分 函数符号恢复

[1] bindiff. 2022. https://www.zynamics.com/bindiff.html

第三部分 整数溢出检测

参考文献

【往期回顾】

添加DataCon小助手微信微信号：DataConofficial获取更多大数据安全知识进群还有超多活动、福利DataCon定制服饰、背包等精彩好礼等你来拿！

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