---
title: DataCon24供应链安全赛道亚军源码分享：MalNPMDetector NPM恶意软件包检测
contest: DataCon 2024 供应链安全赛道亚军
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags:
- npm
- supply-chain
- chatgpt
- static-rule
- taint-analysis
- dynamic-analysis
- malicious-package
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
full_path: DataCon24供应链安全赛道亚军源码分享：MalNPMDetector_NPM恶意软件包检测.full.md
meta_path: DataCon24供应链安全赛道亚军源码分享：MalNPMDetector_NPM恶意软件包检测.meta.md
images_removed: true
images_removed_count: 3
schema_version: v3.0.0-P0
summary: DataCon24供应链安全赛道亚军源码分享：MalNPMDetector NPM恶意软件包检测。DataCon24亚军 MalNPMDetector：静态规则+污点分析+ChatGPT+动态分析。关键路径：第一步：高效静态规则匹配大样本初步过滤可疑包 → 第二步：基于字符串的污点分析收缩范围 → 第三步：构造prompt提交ChatGPT验证恶意性。经验：供应链安全需4步漏斗：粗筛+精筛+...
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 3
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/233929.html
reasoning_chain:
- npm 大样本检测 → 触发点：恶意包 4 步漏斗
- 假设：先粗筛再精筛 → 动作：第一步静态规则匹配（敏感 API/网络/IP/eval）
- 观察：大量 false positive → 下一步：第二步字符串污点分析收缩范围
- 假设：LLM 验证可疑性 + 学习新恶意特征 → 动作：第三步 ChatGPT prompt 验证
- 观察：ChatGPT 输出恶意分类 + 新特征 → 下一步：反馈更新静态规则
- 假设：混淆包静态规则失效 → 动作：第四步动态分析（沙箱跑 install hook）
- 观察：动态捕获 postinstall payload → 完成检测
failed_attempts:
- 试图单步静态规则全检 → 失败：混淆包与新型变种绕过
- 试图纯 ChatGPT 全检 → 失败：成本太高，需先粗筛
key_observations:
- 供应链安全 4 步漏斗：粗筛 + 精筛 + LLM + 动态
- 静态规则 → 字符串污点 → LLM 验证 → 动态沙箱 = 高效漏斗
- ChatGPT prompt 可学习新恶意特征反向更新规则
- 混淆包必须靠动态分析确认
prerequisites:
- npm 包结构与 install 生命周期
- 静态规则 + 字符串污点分析
- ChatGPT 提示工程
- 动态沙箱分析（postinstall hook）
---
# DataCon24供应链安全赛道亚军源码分享：MalNPMDetector NPM恶意软件包检测

> 原文: https://www.ctfiot.com/233929.html
> ID: 233929

高效的静态规则匹配在大样本数据集中初步过滤出可疑恶意包及混淆软件包；

较为耗时的基于字符串的污点分析在规则匹配的可疑恶意包结果中进一步收缩范围；

将两步过滤结果的可疑样本通过构造的prompt提交给ChatGPT验证其恶意性，同时学习新的恶意特征更新已有的静态规则；

针对静态规则匹配检测出的混淆软件包，采用动态分析的方式确认其恶意性。本项目能够高效检测出npm软件包中的恶意包，误报率低、准确率高、能够检测新的攻击。

https://gitee.com/jenniedn/mal-npmdetector.git

此类恶意包通常结构简单，具有统一模板。安装后会自动执行恶意脚本，收集并回传系统和用户信息等敏感数据，如用户目录、用户名、DNS服务器，网卡信息和 passwd 文件内容等;

此类恶意包危害极大，成功攻击后，攻击者可获取目标机器当前用户权限，并进步尝试提权，以最高权限执行任意命令，全面控制受害设备;

此类恶意包在用户机器上下载或释放并执行已经精心制作好的后门木马;

此类恶意包以窃取计算资源为目的，将受害者的机器变为攻击者矿池的算力节点,为其持续提供算力。

此类恶意包会读取用户电脑上的重要目录文件内容，加密后再写回原文件，并留下勒索提示。

此类恶意包没有太多实际作用，但是大量充斥于NPM开源仓库，某些情形下容易造成NPM整个仓库不可用。

⭐ 给个 Star，支持我们的项目！

👀 Watch 关注项目，随时获取最新动态

🍴 Fork 仓库，进行二次开发或学习研究！

📝 提交 Issue 或 PR，共同优化软件供应链生态！

👉 访问 Gitee 仓库：https://gitee.com/jenniedn/mal-npmdetector.git

https://gitee.com/jenniedn/mal-npmdetector.git

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]