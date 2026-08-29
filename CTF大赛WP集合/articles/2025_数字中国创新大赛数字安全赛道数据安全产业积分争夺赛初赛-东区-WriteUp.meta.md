---
title: 2025 数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区 WP
contest: 2025 数字中国创新大赛数字安全赛道
year: 2025
difficulty: easy
vuln_type: [sqli, forensic_disk, misc_unknown]
tags: [数字中国 2025 数据安全东区, ez_upload 漏洞, 加密驱动器 BitLocker 解密, web 日志分析 awk 排序 uniq 统计, 溯源与取证, 数据社工 邮箱爆破, 数据跨境 语音通话还原, awk -F ' ' '{print $1}' 1.log]
attack_chain:
  - 数据安全 ez_upload: 文件上传漏洞利用
  - 服务器 web 日志 awk -F ' ' '{print $1}' 1.log | sort | uniq -c | sort -nr → 找黑客 IP
  - 加密驱动器 BitLocker 解密 → 拿 web 日志
  - 数据社工 邮箱爆破：员工.xlsx + mysql_data.txt 对比
  - 数据跨境 语音通话还原：流量文件 VoIP 提取（小写 26 字母）
key_payload: "awk -F ' ' '{print $1}' 1.log | sort | uniq -c | sort -nr"
one_liner: 2025 数字中国数据安全产业积分争夺赛：BitLocker 解密 + web 日志 awk 排序找黑客 IP + 邮箱对比 + VoIP 流量还原。
lesson: BitLocker 加密驱动器是数据安全赛常见考点；awk -F ' ' 取 IP + sort | uniq -c | sort -nr 是日志分析标准流程；VoIP 流量还原用 Wireshark + rtp 分析。
quality: medium
---

# 2025 数字中国创新大赛数字安全赛道数据安全产业积分争夺赛初赛-东区 WP

## 数据安全-ez_upload
文件上传漏洞利用，常见路径：`/upload` `Content-Type: image/png` + 突破后缀校验。

## 数据分析-溯源与取证

**Q2**：服务器网站遭到黑客攻击，但服务器的 web 日志文件被存放在了加密驱动器中，请解密获得该日志并将黑客 IP 作为答案提交。

```bash
awk -F ' ' '{print $1}' 1.log | sort | uniq -c | sort -nr
```
- 加密驱动器 → BitLocker 解密（密钥恢复或 TPM 旁路）
- 解密后挂载拿到 web 日志
- awk 切第一列（IP）→ sort 排序 → uniq -c 计数 → sort -nr 倒序 → 出现频率最高的 IP 即为黑客 IP

## 数据分析-数据社工
- 员工邮箱列表 vs 数据库泄露邮箱对比
- 高频工具：pandas.read_excel + set 比对
- 输出外泄邮箱地址

## 数据分析-数据跨境

**Q3**：请分析审计导出的流量文件，确认是否存在内部人员与外部人员之间的语音通话记录。鉴于信息泄露的风险，请提取并还原所有相关通话内容，并根据对话内容提交答案。本题的答案由小写的 26 个英文字母组成。

- Wireshark 打开 .pcap → Telephony → VoIP Calls
- 提取 RTP 流 → 解码 G.711 / G.729 → 还原音频
- 听音频写答案（小写 26 字母）

## 战队
- 鱼影安全社区
