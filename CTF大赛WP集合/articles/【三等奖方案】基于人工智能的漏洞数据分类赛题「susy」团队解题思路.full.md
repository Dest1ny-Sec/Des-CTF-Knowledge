---
title: CCF BDCI 2022 三等奖 - AI漏洞数据分类 susy战队
contest: CCF BDCI 2022 数字安全公开赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags:
- CVE
- 漏洞分类
- TF-IDF
- 词向量
- 集成模型
- LightGBM
- NLP
- privilege_required
- attack_vector
- impact
attack_chain: 加载数据 → TF-IDF构造词向量 → 降维 → 提取CVE编号特征 → 词向量+人工特征拼接 → 三个字段分别训练分类器 → 阈值调整 → 合并结果
key_payload: TF-IDF(降维) + LightGBM分类 + 三级标签分开训练
one_liner: 北工大硕士+中大博士用TF-IDF+集成学习做CVE漏洞三级分类,线上第3。
lesson: 漏洞分类三级标签分开训练比合并训练效果好;TF-IDF降维既降内存又加速训练;集成模型相对深度网络速度更快、性能更稳定;换榜后不易过拟合。
quality: high
full_path: 【三等奖方案】基于人工智能的漏洞数据分类赛题「susy」团队解题思路.full.md
meta_path: 【三等奖方案】基于人工智能的漏洞数据分类赛题「susy」团队解题思路.meta.md
images_removed: true
images_removed_count: 6
schema_version: v3.0.0-P0
summary: CCF BDCI 2022 三等奖 - AI漏洞数据分类 susy战队。北工大硕士+中大博士用TF-IDF+集成学习做CVE漏洞三级分类,线上第3。。经验：漏洞分类三级标签分开训练比合并训练效果好;TF-IDF降维既降内存又加速训练;集成模型相对深度网络速度更快、性能更稳定;...
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 6
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/125871.html
reasoning_chain:
- 赛题给 CVE 描述文本 + 三标签 (privilege_required/attack_vector/impact) → 触发点：NLP 分类任务 + 三级标签
- 假设：单模型硬塞 3 标签效果差 → 动作：分 3 个二/多分类器各训一字段
- 动作：sklearn TfidfVectorizer 构造漏洞描述词向量 → 观察：高维稀疏 + 内存爆
- 触发点：TF-IDF 维度过高 → 假设：降维可加速 → 动作：限制 max_features + 截断 SVD
- 动作：正则从 CVE 编号 (CVE-YYYY-NNNN) 提取年份+序号作为人工特征 → 观察：与分类相关
- 触发点：词向量稀疏 + 人工特征稠密 → 假设：需拼接后入模 → 动作：hstack 拼成统一特征
- 模型选 LightGBM 多分类 → 假设：树模型比深度网络更稳、训练快 → 观察：A 榜 impact F1=0.471
- 三级分开训练 vs 合并训练对比 → 假设：分开更准 → 动作：实测对比 → 观察：分开训练提 2-5%
- B 榜调阈值 (impact 多类分布不均) → 假设：默认 0.5 阈值不是最优 → 动作：grid 搜索 0.3-0.7
- 最终线上 0.4851 → 触发点：排名第 3，三等奖
failed_attempts:
- 试图用 BERT 微调做 3 标签 → 失败：线上数据量大、深度网络慢且过拟合
- 试图将三标签当一个多分类 (3^3=27 类) → 失败：长尾严重、训练不收敛
- 试图用整段 Description 不分词 → 失败：TF-IDF 词表过大、过拟合
key_observations:
- 三级标签 (privilege/attack_vector/impact) 各用独立分类器比合并多分类准
- TF-IDF + 截断 SVD 降维既能省内存又加速训练，树模型上效果稳定
- CVE 编号作为人工特征有判别力 (年份越老 + 序号越靠前 = 攻击向量越老)
- B 榜阈值调优对不均衡多分类提分明显 (默认 0.5 不是最优)
- LightGBM 比 BERT 在小数据 + 结构化文本场景更稳 (符合数据竞赛经验)
prerequisites:
- TF-IDF + 词向量原理 (sklearn TfidfVectorizer)
- LightGBM 多分类接口 (num_class + softmax)
- 特征工程 (正则提取 CVE 编号)
- 二/多分类阈值调优 (precision/recall/F1 trade-off)
---
# 【三等奖方案】基于人工智能的漏洞数据分类赛题「susy」团队解题思路

> 原文: https://www.ctfiot.com/125871.html
> ID: 125871

2022 CCF BDCI

数字安全公开赛

赛题「基于人工智能的漏洞数据分类」

地址：http://go.datafountain.cn/s57

@susy战队

获奖方案

团队简介

吴绍武，硕士毕业于北京工业大学理学部，主修专业数学；目前在中山大学就读博士研究生，网络空间安全专业。迄今为止，曾获2022年全国水下机器人大赛-水声通信赛优胜奖；2022年中国移动梧桐杯大数据应用创新大赛-数智交通赛优胜奖；2022年“移动云杯”算力网络应用创新大赛-双碳节能赛三等奖。

摘要

CVE平台的漏洞信息，由于数据量过大，人工无法及时对其进行分析归类。为了降低成本，提高效率，以便后续对漏洞信息的进一步研究，需要通过人工智能的方法对其进行学习分类。

本方案，通过自然语言处理的方法，对每条漏洞信息进行学习并预测。首先通过TF-IDF对漏洞描述构造词向量，并采用降维的方法进行降维；同时对CVE编号提取特征。最终是词向量特征与人工提取的特征进行拼接，喂给分类器模型进行训练和预测。由于漏洞标签涉及三个等级，故可采用分开训练或者合并训练的方式。经过线下的验证，本方案采用分开训练的方式，分别对三个字段进行学习训练与预测。

最终，模型在线下的效果为：针对privilege-required标签，准确率为0.8788，F1-score为0.7051；针对attack-vector标签，准确率为0.9710，F1-score为0.8125；针对impact标签，准确率为0.7976，F1-score为0.4710。最终模型在线上的得分为0.4851，排名第3名。

关键词

CVE平台、漏洞分类、词向量、人工智能

赛题背景

为及时跟踪国际信息安全趋势，需对国际公开的漏洞数据内容进行及时统计和梳理，例如CVE漏洞平台。CVE平台的漏洞信息包含有CVE编号、漏洞评分、漏洞描述等内容，其中漏洞描述含有对漏洞的利用条件、受影响的范围、漏洞可达到的效果（危害）等内容。为了更好地理解和持续研究，需将这些漏洞信息按照一定规则进行分类。而在此过程中，人工筛选分类效率较低，耗时耗力，利用人工智能，通过自然语言处理则可能更好地解决这一问题。

本次赛题的任务是，通过平台给出的A榜已标注数据、未标注的漏洞数据（未标注的漏洞数据请按照漏洞信息分类规则先进行分类标注），设计软件算法模型，对漏洞数据进行分类。

数据简介

数据总共包括五个字段，即CVE编号“CVE-Number”，漏洞描述“Description”，以及三个等级标签字段“Privilege-Required”，“Attack-Vector”，“Impact”。其中，在测试集中，只提供了前面两个字段，后面的三个字段需要训练模型进行预测。

三个等级标签的分类标准的详细说明如下：

● Privilege-Required：即漏洞利用所需要的权限，漏洞描述中若存在利用需要登录授权后才能利用，需要普通权限即为Nonprivileged、需要admin或者root权限即为admin/root、若是直接通过网络访问即可利用，则为access；若从描述中不能得该部分的信息即为unknown。

● Attack-Vector（攻击介质）：即为漏洞描述中的攻击方式，若是通过远程网络攻击即为remote，若是通过非远程方式的话（本地物理接触攻击）即为Non-remote。

● Impact：Impact（Impact-level1）即为描述中成功利用该漏洞的所产生的影响，根据漏洞类型而异，RCE、代码执行等可获取到权限Privilege-Gained（RCE），提权漏洞成功利用即可获得最高（root/admin）权限；DoS（denial of service）漏洞即为拒绝服务漏洞；access为可利用漏洞获取到访问权限；other即为不属于以上所列出的影响的其他影响；Impact（Impact-level2）为若Impact（Impact-level1）漏洞类型为Privilege-Gained（RCE），即为获取到的权限分类，普通权限Nonprivileged、最高权限admin/root以及不清楚unknown；根据描述内容即可确定；若Impact（Impact-level1）漏洞类型为信息泄漏，且能获取到本机的登录凭证，即为local（credit），若能获取到其他的非本机的凭证，即为other-target（credit），若描述中未说明是否获取到权限或者没有获取到即为other; Impact（Impact-level3）即为获取到的凭证的权限（一般非特权权限Nonprivileged、最高权限admin/root、unknown）。

数据预处理

主要包括对未标注数据的处理，以及对标签的处理。这里需要对未标注的数据进行提取，从而获得CVE编号、漏洞描述等信息；而对于标签，需要对其进行拼接得到新的标签，从而可以当作模型的标签进行使用。

方案框架

本方案总体框架如图所示。首先通过加载数据，并对数据进行探索，包括对未标注数据的提取、标签的处理、可视化等；然后对其进行特征提取，得到特征后带入分类器模型中进行学习训练，并且采用交叉验证的方式，对测试集进行预测。最后，是对预测结果阈值的调整，以及对生成结果的合并。

方案总框架图

方案效果

本方案主要采用准确率、F1-score、模型大小来衡量方案的性能。下面展示的是，模型分别对三个等级标签，即“Privilege-Required”，“Attack-Vector”，“Impact”的性能。性能如下表所示。

方案亮点

本方案的亮点主要在于以下方面：

1）训练目标上的不同，作品采用单独训练的方式，对三级标签单独训练模型，比拼接后再训练的方式效果性能更好；

2）在词向量的构造中，主要采用TF-IDF词向量，并做适当的降维处理，即可以降低内存，也可以加速模型训练的速度；

3）模型采用了性能、速度都占优势的集成模型，相对于深度网络模型，具有易实现，速度快，性能高等优势；

4）构造的特征以及采用的模型，效果性能稳定，在换榜后不易发生过拟合的现象。

致谢

此次赛题的顺利完成，非常地感谢主办方中国计算机学会、大数据协同安全技术国家工程研究中心、中国科学院信息工程研究所、360未来安全研究院工业互联网实验室；同时感谢参赛选手的积极交流与分享！

参考

[1] 中国计算机学会，CCF大数据与计算智能大赛，https://www.datafountain.cn/competitions/594/datasets

[2] 李航. 统计学习方法[M]. 清华大学出版社, 北京.

[3] Guolin K，Qi M，Thomas F,et al. LightGBM: A Highly Efficient Gradient Boosting Decision Tree [J]. Advances in Neural Information Processing Systems, 2017:
3149-3157.

[4] Friedman J H. Greedy Function Approximation: A Gradient Boosting Machine[J]. The Annals of Statistics . 2001.

—End—

戳“阅读原文”，速来参赛办赛~

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]