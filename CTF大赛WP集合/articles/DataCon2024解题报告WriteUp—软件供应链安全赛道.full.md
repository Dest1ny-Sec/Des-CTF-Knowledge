---
title: DataCon2024解题报告WriteUp—软件供应链安全赛道
contest: DataCon 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags:
- supply-chain
- npm
- pypi
- llm
- mphunter
- guarddog
- obs
- typosquatting
attack_chain:
- 第一章：赛题介绍
- 第二章：总体思路
- 第三章：解题详述
- MPHunter：恶意PyPI包聚类
- npm软件包文件结构分析
- LLM对NodeJS代码威胁评分
- OBS（Obfuscation）代码检测
- PyPI恶意包相似性匹配
- 基于多源规则拓展匹配
- 第四章：未标注新恶意包样本
- LLM 增强数据集 Maltracker
- guarddog规则+LLM辅助
- 高度相似依赖识别
key_payload: LLM 评分NodeJS代码+多源规则匹配+相似性聚类
one_liner: DataCon2024软件供应链：npm/PyPI恶意包检测+LLM辅助+MPHunter
lesson: LLM辅助+规则匹配+相似性聚类是供应链安全3大武器
quality: high
full_path: DataCon2024解题报告WriteUp—软件供应链安全赛道.full.md
meta_path: DataCon2024解题报告WriteUp—软件供应链安全赛道.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: DataCon2024解题报告WriteUp—软件供应链安全赛道。DataCon2024软件供应链：npm/PyPI恶意包检测+LLM辅助+MPHunter。关键路径：第一章：赛题介绍 → 第二章：总体思路 → 第三章：解题详述。经验：LLM辅助+规则匹配+相似性聚类是供应链安全3大武器
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/224419.html
reasoning_chain:
- npm/PyPI 恶意包识别 → 触发点：软件供应链安全综合题
- MPHunter：恶意 PyPI 包聚类 → 假设：包结构相似性聚类 → 动作：extract metadata+feature hash
- npm 包文件结构分析 → 假设：install hook / postinstall 注入是入口 → 动作：tree 文件树
- LLM 对 NodeJS 代码威胁评分 → 假设：LLM 语义理解识别混淆代码 → 动作：prompt = score(0-10)
- OBS Obfuscation 代码检测 → 假设：高度可疑变量名+字符串拼接 → 动作：LLM 判断
- PyPI 恶意包相似性匹配 → 假设：已知恶意包 hash 数据库 → 动作：相似度 SSDEEP/SDHash
- 高度相似依赖识别 → 假设：typosquatting（requests→requestts） → 动作：编辑距离匹配
failed_attempts:
- 试图仅靠静态签名 → 失败：新型混淆绕过
- 试图纯规则匹配 → 失败：必须 LLM 辅助语义判断
key_observations:
- LLM 辅助 + 规则匹配 + 相似性聚类 = 供应链安全 3 大武器
- install/postinstall hook 是 npm 恶意包标准入口
- MPHunter 通过聚类发现新型恶意包家族
- typosquatting 编辑距离 <3 是高风险信号
prerequisites:
- npm/PyPI 包结构与生命周期 hook
- LLM 提示工程威胁评分
- 代码相似性算法（SSDEEP/TLSH）
- typosquatting 命名检测
---
# DataCon2024解题报告WriteUp—软件供应链安全赛道

> 原文: https://www.ctfiot.com/224419.html
> ID: 224419

2024年11月28日，DataCon2024大数据安全分析竞赛落下帷幕。竞赛共设AI安全、软件供应链安全、网络基础设施安全、网络黑产分析和漏洞分析五大赛道。在706支战队、1556位专业选手激烈的角逐中，来自中国科学院软件研究所的“SecureNexusLab供应链安全”战队以总成绩第一斩获软件供应链安全赛道冠军，本期一起来看看冠军的解题报告。

第一章 赛题介绍

第二章 总体思路

图 2.1 整体工作流程

图2.2 MPHunter流程图

第三章 解题详述

图3.1 npm软件包文件结构

图3.2 使用LLM对NodeJS代码进行威胁评分

图3.3 LLM判断为OBS的代码截图

图3.5 星图实验室安全报告截图

图3.6 PyPI软件包文件结构

图3.7 PyPI恶意包相似性匹配流程

图3.8 大语言模型输出示例

图3.9 收集总结的部分恶意规则

图3.10 基于多源规则进行拓展匹配流程

第四章 未标注的新恶意软件包样本

图4.1 无意义的依赖包列表

图4.2 高度相似的依赖

图4.3 恶意代码片段

图4.4 恶意代码风险评估

第五章 致谢

参考文献

[1]Liang, Wentao, et al. “A Needle is an Outlier in a Haystack: Hunting Malicious PyPI Packages with Code Clustering.” the 38th IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE, 2023.

[2]https://github.com/DataDog/guarddog

[3]https://tongyi.aliyun.com/

[4]https://socket.dev/blog/2023-npm-retrospective

[5]https://www.theregister.com/2024/11/05/typosquatting_npm_campaign/

[6]https://www.theregister.com/2022/02/03/npm_malware_report/

[7]https://arstechnica.com/security/2024/11/javascript-developers-targeted-by-hundreds-of-malicious-code-libraries/

[8]Duan, Ruian, et al. “Towards measuring supply chain attacks on package managers for interpreted languages.” The Network and Distributed System Security (NDSS) Symposium, 2021.

[9]https://js-deobfuscator.vercel.app/

[10]Yu, Zeliang, et al. “Maltracker: A fine-grained npm malware tracker copiloted by llm-enhanced dataset.” Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis. 2024.

[11]Guo, Wenbo, et al. “An empirical study of malicious code in PyPI ecosystem.” 2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE, 2023.

[12]https://tianwen.qianxin.com/blog/2024/08/16/tea-npm-rubbish/

[13]https://www.virustotal.com/gui/home/url

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