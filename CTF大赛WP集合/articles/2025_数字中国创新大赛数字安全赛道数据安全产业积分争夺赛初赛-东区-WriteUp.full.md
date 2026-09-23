---
title: 2025 数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区 WP
contest: 2025 数字中国创新大赛数字安全赛道
year: 2025
difficulty: easy
vuln_type:
- sqli
- forensic_disk
- misc_unknown
tags:
- 数字中国 2025 数据安全东区
- ez_upload 漏洞
- 加密驱动器 BitLocker 解密
- web 日志分析 awk 排序 uniq 统计
- 溯源与取证
- 数据社工 邮箱爆破
- 数据跨境 语音通话还原
- awk -F ' ' '{print $1}' 1.log
attack_chain:
- '数据安全 ez_upload: 文件上传漏洞利用'
- 服务器 web 日志 awk -F ' ' '{print $1}' 1.log | sort | uniq -c | sort -nr → 找黑客 IP
- 加密驱动器 BitLocker 解密 → 拿 web 日志
- 数据社工 邮箱爆破：员工.xlsx + mysql_data.txt 对比
- 数据跨境 语音通话还原：流量文件 VoIP 提取（小写 26 字母）
key_payload: awk -F ' ' '{print $1}' 1.log | sort | uniq -c | sort -nr
one_liner: 2025 数字中国数据安全产业积分争夺赛：BitLocker 解密 + web 日志 awk 排序找黑客 IP + 邮箱对比 + VoIP 流量还原。
lesson: BitLocker 加密驱动器是数据安全赛常见考点；awk -F ' ' 取 IP + sort | uniq -c | sort -nr 是日志分析标准流程；VoIP 流量还原用 Wireshark + rtp 分析。
quality: medium
full_path: 2025_数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区-WriteUp.full.md
meta_path: 2025_数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025 数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区 WP。2025 数字中国数据安全产业积分争夺赛：BitLocker 解密 + web 日志 awk 排序找黑客 IP + 邮箱对比 + VoIP 流量还原。。关键路径：数据安全 ez_upload: 文件上传漏洞利用 → 服务器 web 日志 awk -F '' '' ''{print $1}'' 1.log | sort | ...'
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- disk_forensics
- misc_other
tools_used:
- Wireshark
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/235930.html
reasoning_chain:
- '[触发点] BitLocker 加密驱动器 + 服务器 web 日志被加密 → 假设：必须先解密 BitLocker → [动作] 寻找恢复密钥 → [观察] 拿到解密驱动器 → [下一步] 取日志'
- '[触发点] web 日志分析找黑客 IP → 假设：awk 提取 IP + sort | uniq -c | sort -nr → [动作] awk -F '' '' ''{print $1}'' 1.log | sort | uniq -c | sort -nr → [观察] 拿到最多 IP'
- '[触发点] 邮箱对比（数据社工）→ 假设：从邮件服务器导出数据 → [动作] 比对邮箱账号 + 附件 → [观察] 拿到关联信息'
- '[触发点] VoIP 流量还原语音通话 → 假设：Wireshark + rtp 解析 → [动作] rtp 分析 → [观察] 还原通话内容 → [下一步] 字母排序'
failed_attempts:
- 试图直接 cat 解 BitLocker 加密驱动器 → 失败：必须解密
- 试图人工读日志找 IP → 失败：日志太大必须 awk
- 试图不解 VoIP 流量 → 失败：必须 rtp 还原
key_observations:
- BitLocker 加密驱动器是数据安全赛常见考点
- awk -F ' ' 取 IP + sort | uniq -c | sort -nr 是日志分析标准流程
- VoIP 流量还原用 Wireshark + rtp 分析
- 数据安全赛 = 取证 + 密码学 + Web 综合能力
prerequisites:
- BitLocker 加密驱动器解密
- awk/sort/uniq 日志分析三连
- Wireshark rtp 流量还原
- 数据社工基础
---
# 2025 数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区-WriteUp

> 原文: https://www.ctfiot.com/235930.html
> ID: 235930

点击上方蓝字·关注我们

前言：

随便参加着玩玩，记录一下，仅供参考！

文章同步CSDN，感谢大家观看，麻烦点个赞！

数据安全-ez_upload

数据分析-溯源与取证

2.服务器网站遭到了黑客攻击，但服务器的web日志文件被存放在了加密驱动器中，请解密获得该日志并将黑客ip作为答案提交。

awk -F " " '{print $1}' 1.log | sort | uniq -c | sort -nr

数据分析-数据社工

数据分析-数据跨境

3.请分析审计导出的流量文件，确认是否存在内部人员与外部人员之间的语音通话记录。鉴于信息泄露的风险，请提取并还原所有相关通话内容，并根据对话内容提交答案。本题的答案由小写的26个英文字母组成。

关注我们

欢迎关注鱼影安全社区,专注CTF,职业技能大赛中高职技能培训,金砖企业赛,世界技能大赛省选拔赛,企业赛,行业赛,电子取证和CTF系列培训。

鱼影安全团队招人啦,有感兴趣的师傅可以私信我

需要数据包流量分析 专项培训的 比如比赛等 可以联系小编  价格优惠！


```
awk -F " " '{print $1}' 1.log | sort | uniq -c | sort -nr
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