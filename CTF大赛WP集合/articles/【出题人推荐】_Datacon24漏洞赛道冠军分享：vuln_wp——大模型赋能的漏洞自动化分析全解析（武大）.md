# 【出题人推荐】 Datacon24漏洞赛道冠军分享：vuln_wp——大模型赋能的漏洞自动化分析全解析（武大）

> 原文: https://www.ctfiot.com/233200.html
> ID: 233200

出题人推荐

由于其复杂的性质，漏洞识别与定位一直是一个具有挑战性的难题。在Datacon2024漏洞分析赛道中，冠军团队——武汉大学0817 IOTG，针对性的对不同类型漏洞采用大模型方法以及与其匹配的分析模式，取得了卓越的成绩。该团队不仅证实了AI驱动漏洞挖掘的可行性，还为智能漏洞挖掘技术的实际应用提供了重要参考，推动了这一领域的工程化进程。这种方法展示了在处理复杂漏洞识别和定位任务时，结合先进技术和创新分析策略的巨大潜力。

https://github.com/123f321/datacon24_vuln_wp

https://www.datacon.org.cn/competition/competitions/91/introduction

https://github.com/123f321/datacon24_vuln_wp

在网络安全和漏洞挖掘领域，海量漏洞分析文章和庞大的代码库常常让传统人工和静态分析方法捉襟见肘。datacon24_vuln_wp 正是为了解决这一问题而设计，利用大模型的深度语义理解能力，实现自动化、智能化的漏洞检测与信息提取。

项目基于赛道冠军战队 0817iotg 的完整解题框架，融合了最新的提示工程方法和多轮大模型调用机制，旨在降低误报、提高漏洞识别的准确率和效率。

利用 BeautifulSoup4 对 HTML 进行解析，精准过滤图片等无关内容。

采用精细化的提示工程方法，将信息拆分成多个输出维度，使用两次大模型调用分别判定，确保提取结果准确且具备多角度分析。

内置投票机制，对多轮大模型输出进行校验，自动剔除不合理或低置信度结果。

扩展功能：除基础信息外，还能识别版本信息、修复建议，并从文章中提取 POC/EXP 代码和图像内容。（详见 task1_source_code 中的 test.py、appendix.py 及 pic_expand.py）

先对待分析文件进行大小排序、类型过滤，再依据编程语言进行函数级别的切分，确保每个代码片段都能单独分析。

利用提示工程进行初步筛查，提取可能包含漏洞的种子函数；对种子函数内容进行深度解析，针对不同漏洞类型（如 race condition、SQL 注入、double-fetch、buff_overflow、command_injection 等）采用不同分析策略。

部分复杂漏洞类型引入 RAG 技术，结合多轮提示与结果投票，有效降低误报，并输出最有可能的漏洞函数供后续手工验证或自动修复。

利用最新大模型技术和提示工程，实现高效、精准的信息提取与漏洞定位。

通过多次调用大模型和投票比对，显著降低输出不确定性，提高漏洞检测准确率。

提供完整的 Docker 压缩包，无需复杂环境配置，支持快速部署和现场测试。

代码结构清晰、模块化设计，方便开发者二次开发、扩展与定制。

内置针对多种漏洞类型的示例与测试数据，为新手和资深安全研究者提供了宝贵的实战参考。

访问 GitHub 仓库 https://github.com/123f321/datacon24_vuln_wp 下载源代码和 Docker 镜像。

欢迎 Star ⭐、Fork 🍴、Watch 👀，关注项目动态；提出 Issue 或提交 PR，大家一起完善自动化漏洞分析工具。

利用该框架进行漏洞挖掘与安全审计，将实战经验分享到社区，共同推动安全技术的进步。

https://github.com/123f321/datacon24_vuln_wp

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-b0533deebcd60183de7f193d5461b388.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-a04e1ef10354091372e5ba6083d0a018.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-c14f8aa6a67534515a18a2ab3e0e890c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-e5c640ce013fd2e40f52661a323eefbe.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-cb3d3c483fc65562fe574863eed551e8.png)