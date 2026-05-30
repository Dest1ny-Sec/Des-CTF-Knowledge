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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736943311.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736943314.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/4-1736943315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736943315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736943316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736943317.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736943318.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736943318.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736943319.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736943319.jpeg)