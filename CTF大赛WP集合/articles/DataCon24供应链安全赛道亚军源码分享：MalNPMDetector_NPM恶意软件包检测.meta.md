---
title: DataCon24供应链安全赛道亚军源码分享：MalNPMDetector NPM恶意软件包检测
contest: DataCon 2024 供应链安全赛道亚军
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [npm, supply-chain, chatgpt, static-rule, taint-analysis, dynamic-analysis, malicious-package]
attack_chain:
  - 第一步：高效静态规则匹配大样本初步过滤可疑包
  - 第二步：基于字符串的污点分析收缩范围
  - 第三步：构造prompt提交ChatGPT验证恶意性
  - 学习新恶意特征更新静态规则
  - 针对混淆包采用动态分析确认
  - https://gitee.com/jenniedn/mal-npmdetector.git
key_payload: static_rule → taint_analysis → ChatGPT_verify → dynamic_analysis
one_liner: DataCon24亚军 MalNPMDetector：静态规则+污点分析+ChatGPT+动态分析
lesson: 供应链安全需4步漏斗：粗筛+精筛+LLM+动态
quality: high
---

# DataCon24供应链安全赛道亚军源码分享：MalNPMDetector NPM恶意软件包检测

## 题目信息
- 比赛：DataCon 2024
- 方向：供应链安全
- 成绩：亚军
- 项目：MalNPMDetector

## 关键攻击链
### 4 步检测流程
1. **静态规则匹配**：大样本数据集中初步过滤可疑恶意包+混淆软件包
2. **污点分析**：基于字符串的污点分析在规则匹配结果中收缩范围
3. **ChatGPT 验证**：将可疑样本通过 prompt 提交 ChatGPT 验证恶意性
4. **动态分析**：针对静态规则匹配出的混淆软件包确认其恶意性
5. **反馈循环**：学习新恶意特征 → 更新静态规则

### 恶意包类型
- **模板类**：自动执行恶意脚本，回传用户目录/用户名/DNS/网卡/passwd
- **提权类**：成功后获取当前用户权限 → 提权 → 任意命令
- **后门类**：下载或释放并执行后门木马
- **挖矿类**：变算力节点，连接矿池
- **勒索类**：加密重要文件并写回，留勒索提示
- **刷库类**：大量充斥仓库，造成 NPM 不可用

## 评分
- quality: high（4 步检测框架 + 6 类恶意包分类 + 开源仓库链接）
