---
title: DownUnderCTF 2024——取证方向题解
contest: DownUnderCTF 2024
year: 2024
difficulty: medium
vuln_type: forensic_disk
tags: [forensics, nmap, wmi, mimikatz, domain-controller, emuc2, traffic-analysis]
attack_chain:
  - Baby's First Forensics: 流量分析识别扫描工具及版本
  - SAM I AM: WMI+域管理员密码 mimikatz
  - Bad Policies: 域控制器访问方法还原
  - emuc2: 模拟C2恶意软件流量分析
key_payload: nmap_7.25  # 类似格式
one_liner: DownUnderCTF 2024 取证4题：流量+域控WMI+Bad Policies+emuc2
lesson: 取证题常用流量分析+SMB事件+注册表+内存镜像组合
quality: medium
---

# DownUnderCTF 2024——取证方向题解

## 题目信息
- 比赛：DownUnderCTF 2024
- 方向：Forensics

## 关键攻击链
### 1. Baby's First Forensics
- 攻击者尝试入侵 → 捕获流量
- 工具识别：扫描器及版本
- 答案格式：`DUCTF{nmap_7.25}`

### 2. SAM I AM
- 攻击者通过 WMI 登录域控制器
- 转储 SAM 文件获取 Administrator 密码
- 答案格式：`DUCTF{password123!}`

### 3. Bad Policies
- 攻击者访问域控制器
- 从 Outpost 机器中提取 artifacts
- 还原访问方法

### 4. emuc2
- 攻击者获取自家 C2 源码反向利用
- 流量分析还原 C2 协议

## 评分
- quality: medium（4 道取证题目录式呈现，具体解法需看原 PDF/文档）
