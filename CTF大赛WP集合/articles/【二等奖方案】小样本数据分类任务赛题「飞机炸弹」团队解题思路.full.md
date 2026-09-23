---
title: CCF BDCI 2022 二等奖 - 小样本专利分类 飞机炸弹团队
contest: CCF BDCI 2022 (第十届CCF大数据与计算智能大赛)
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags:
- 小样本分类
- 专利分类
- RAKE
- 预训练
- MLM
- SimCSE
- 记忆网络
- R-Drop
- 标签平滑
- 伪标签
- 5折融合
- Mixup
- BERT-large
attack_chain: RAKE抽取关键短语 → 北大专利数据集MLM+SimCSE领域预训练 → 4个预训练模型(roberta-wwm/mengzi/nezha/bert-for-patents) → 5个Dropout+共享分类头 → MemoryBank对比Loss → R-Drop KL损失 → 5折融合 → 伪标签迭代+标签平滑
key_payload: RAKE关键词 + MLM+SimCSE预训练 + MemoryBank + R-Drop + Mixup + 5折融合
one_liner: 哈工大(深圳)研究生用RAKE+SimCSE+MemoryBank+R-Drop在小样本专利分类上A榜0.6371/B榜0.6023。
lesson: 长文本小样本场景先用RAKE降学习难度;MemoryBank+BCELoss+对比学习防过拟合;R-Drop利用Dropout机制构造正例;SimCSE同一句子两次前向作为正样本对;中翻英+bert-for-patents在英文域效果更好;Mixup在batch内折半翻转构造增强。
quality: high
full_path: 【二等奖方案】小样本数据分类任务赛题「飞机炸弹」团队解题思路.full.md
meta_path: 【二等奖方案】小样本数据分类任务赛题「飞机炸弹」团队解题思路.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: CCF BDCI 2022 二等奖 - 小样本专利分类 飞机炸弹团队。哈工大(深圳)研究生用RAKE+SimCSE+MemoryBank+R-Drop在小样本专利分类上A榜0.6371/B榜0.6023。。经验：长文本小样本场景先用RAKE降学习难度;MemoryBank+BCELoss+对比学习防过拟合;R-Drop利用Drop...
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/134878.html
reasoning_chain:
- 赛题：小样本专利分类 (每类 ~100 样本) → 触发点：长文本 (5000+ 字) + 类别不平衡
- 假设：长文本直接进 BERT 截断会丢关键 → 动作：RAKE 抽取关键短语 → 观察：长度从 5000 砍到 500
- 领域预训练数据用北大专利 → 动作：MLM (动态掩码) + SimCSE 对比预训练 → 观察：SimCSE 同句两次前向
- 假设：通用 bert-base 不够 → 动作：roberta-wwm + mengzi + nezha + bert-for-patents 4 模型并行
- 触发点：单模型过拟合 → 假设：MemoryBank 对比学习能拉同类样本距离
- 动作：MemoryBank + BCELoss + 对比 Loss → 观察：训练 loss 稳定下降
- R-Drop KL 损失 → 假设：两次 forward 一致性约束 → 动作：KL(p1 || p2) + KL(p2 || p1)
- Mixup 数据增强 → 触发点：样本太少 → 动作：batch 内两样本折半反转构造新样本
- 5 折交叉验证 + 融合 → 假设：5 折均值比单折稳 → 观察：A 榜 0.6371
- B 榜 0.6023 → 触发点：A→B 衰减 5.5% → 比通用 BERT 微调衰减小
failed_attempts:
- 试图直接用 bert-base 微调 → 失败：长文本截断丢关键 + 小样本过拟合
- 试图用对抗训练 FGM → 失败：与 R-Drop 同时使用冲突
- 试图用伪标签迭代 → 失败：B 榜衰减加剧 (噪声累积)
key_observations:
- RAKE 关键短语抽取能大幅降低长文本学习难度
- MemoryBank + BCELoss + 对比学习是小样本过拟合通用解法
- R-Drop 利用 Dropout 机制构造正例 (同一样本两次 forward) 比对抗训练温和
- SimCSE 同一句子两次前向作为正样本对 = 对比学习入门 trick
- 中翻英 + bert-for-patents 在英文域专利分类上效果比中文模型更好
prerequisites:
- BERT MLM 预训练 (HuggingFace Trainer)
- SimCSE 对比学习原理
- R-Drop / MemoryBank / Mixup 增强
- RAKE 关键短语抽取算法
---
# 【二等奖方案】小样本数据分类任务赛题「飞机炸弹」团队解题思路

> 原文: https://www.ctfiot.com/134878.html
> ID: 134878

2022 CCF BDCI

第十届CCF大数据与计算智能大赛

第十届CCF大数据与计算智能大赛（2022 CCF BDCI）已圆满结束。大赛官方竞赛平台DataFountain（简称DF平台）正在陆续释出各赛题获奖队伍的方案思路。
本方案为【小样本数据分类任务】赛题的二等奖获奖方案，赛题地址：

https://datafountain.cn/competitions/582（戳底部“阅读原文”可直达）

获奖团队简介

团队名称：飞机炸弹

团队成员：孙雅涵，哈尔滨工业大学(深圳)，研究生二年级在读。主要负责任务定义、数据处理和方案的设计。

张凌源，哈尔滨工业大学，研究生二年级在读。主要负责方案的实现和效果论证。

所获奖项：二等奖

摘要

创新是国家发展、民族复兴的不竭动力。近年来，随着政策扶植、国家工业化水平和国民教育水平提高，我国的专利申请量快速增长，专利检索、查新、管理等需求也不断增加。为了满足以上需求，提升专利服务质量，通常需要建立多个维度的专利分类体系。

比赛方公开958条专利数据，包括专利权人、专利标题、专利摘要和分类标签，其中分类标签经过脱敏处理，共36类。要求选手设计一套算法，完成测试数据的分类任务。本次赛题公布的训练数据量较小，属于基于小样本训练数据的分类任务。

本团队基于预训练语言模型，利用外部大规模无标签专利数据集做无监督领域继续预训练。通过使用Rake算法抽取专利摘要中的关键短语来降低长文本任务小样本场景下任务拟合难度。通过记忆网络、R-Drop以及标签平滑的方法解决小样本训练场景下模型容易过拟合问题。使用伪标签迭代训练的方法来扩增训练数据集，提升模型精度。最后利用模型5折融合的方法增强模型的泛化能力，提升模型精度。通过实验最终证明我们使用方法的有效性。最终在A榜得分0.6371，B榜得分0.6023。

关键词

小样本分类、专利分类、预训练语言模型

介绍

小样本分类任务作为近年来研究的热点问题，学界提出了远程监督、数据增强、预训练模型等一系列方案。专利分类体系中常见的有国际专利分类(IPC)、联合专利分类(CPC)、欧洲专利分类(ECLA)等，但是这些专业性极强的分类体系对非专利知识产权相关从业人员而言难以理解和使用。

智慧芽作为国际领先的知识产权SaaS平台，根据用户的搜索习惯等因素，为了提升用户的使用体验，构建了一种新的专利分类体系，为本赛题提供了真实标注的语料，要求利用算法进行训练预测完成专利数据的分类任务。

技术方案

2.1 数据预处理

本赛题数据集提供了具有36类分类标签的958条专利数据，每条数据包含专利权人、专利标题和专利摘要。训练集整体的数据量较小，我们首先对数据进行了简单统计，如图1所示。

图1：训练集各类别数量分布

比赛属于小样本领域，训练数据偏少，测试规模大。同时本次比赛中使用的文本摘要的长度过长，若直接利用长文本信息进行小样本训练，模型较难从长段信息中提取出有用的信息进行标签的分类，因此我们采用RAKE算法[1-2]对专利摘要抽取关键短语来降低模型学习摘要内容的难度。RAKE算法首先使用标点符号（如半角的句号、问号、感叹号、逗号等）将一篇文档分成若干分句，然后对于每一个分句，使用停用词作为分隔符将分句分为若干短语，这些短语作为最终提取出的关键词的候选词。最后，每个短语可以再通过空格分为若干个单词，可以通过给每个单词赋予一个得分，通过累加得到每个短语的得分。一个关键点在于将这个短语中每个单词的共现关系考虑进去。最终定义的公式如式(1)所示。

wordScore=wordDegree(w)/wordFrequency(w)

同时我们利用腾讯翻译API对训练集以及A榜测试集进行中翻英的处理，为了后续在英文预训练语言模型中使用以及后续A榜数据集伪标签迭代进行准备。

最后我们使用按照标签分层的方法将训练数据切成5折，保证每折内有近似标签分布。

2.2 领域预训练

我们使用北京大学开放研究数据平台-发明专利数据集[3]中的专利摘要进行无监督预训练。预训练任务包括MLM、SimCSE。其中MLM我们对于每个摘要随机mask掉15%的token，然后预测被MASK掉的词。而SimCSE预训练任务，利用预训练模型中的Dropout mask，对每一个句子进行两次前向传播，得到两个不同的embeddings向量，将同一个句子得到的向量对作为正样本对，对于每一个向量，选取其他句子产生的embeddings向量作为负样本，以此来训练模型。

其中本竞赛我们在3个不同的预训练语言模型上进行了上述领域预训练。包括hfl/chinese-roberta-wwm-ext、Langboat/mengzi-bert-base以及nezha-cn-base。每个预训练在外部无监督专利数据集上进行5轮，学习率为5e-5。而对于SimCSE版本的预训练任务，对比学习Loss的权重是50，MLM Loss的权重为1。

2.3 模型结构

2.3.1 中文模型

本次比赛中文模型使用的模型结构如图2所示。

图2：模型结构图

模型的输入是专利标题、专利申请人、专利摘要Rake算法关键短语提取结果以及专利摘要原文拼接而成。模型结构上使用的预训练语言模型有hfl/chinese-roberta-wwm-ext、Langboat/mengzi-bert-base以及nezha-cn-base。每类模型我们都会取第一个Token的表示分别过5个不同比例的Dropout层后过一个共享参数的分类头与原始标签计算交叉熵作为分类loss。同时我们还维护了一个记忆存储模块用来存储每个类别的平均表示，其表示结果采用指数平均的方式估计得到。最后我们将CLS的表示与记忆存储中各个分类的平均表示计算BCELoss，其中同类为1，不同类为0。由于该任务共36类，因此此处对比Loss我们还采用Focal Loss来增强对于正例的学习能力。

同时我们还使用R-Drop的方法来增强模型的鲁棒性，提升模型的精度。具体来说，模型经过两次前向后得到的分类表示间计算KL损失，其本质思想是利用Dropout随机丢弃部分神经元的机制构建正例，利用KL损失拉近与正例的距离。

2.3.2 英文模型

对于中翻英后的训练集，我们采用anferico/bert-for-patents预训练语言模型进行训练，该模型基于BERT-large在大规模美国专利摘要中预训练得到。相较于中文模型，在英文模型中我们还使用Mixup的方法来提升模型的精度。我们使用预训练语言模型最后一层CLS的表示进行Batch内的Mixup，具体融合对象我们采用折半翻转后折半内部再翻转的方式获得，例如[0,1,2,3,4,5]折半翻转为[3,4,5,0,1,2]再内部翻转得到[5,4,3,2,1,0]

2.4 后处理

对于上述4种不同的预训练语言模型，我们都在5折训练集上进行训练，训练一共20个模型。在各自折上进行简单的模型融合，融合策略采用分布加权平均的方法，由于本次竞赛为小样本，因此此处没有搜索加权的权重，直接使用默认权重1进行融合，在A榜测试集上按照折得到5个不同版本的伪标签。之所以不使用全量模型融合得到伪标签，是因为全量的操作会导致后续伪标签迭代训练验证集标签泄漏。

最后我们使用SimCSE版本的预训练模型在伪标签结果上进行微调，其中为了平衡真实训练集的比例，在每轮训练中我们复制了原始训练集12次与A榜测试集伪标签融合。同时，为了解决原始伪标签质量不高，可能导致模型混乱的情况，我们使用了标签平滑的方法防止模型过度拟合伪标数据。

外部数据集使用情况

我们使用北京大学开放研究数据平台2017年全年发明专利数据集。该数据集源自润桐网（www.rainpat.com），由国家信息中心合作企业北京国信宏数科技有限责任公司提供，包含申请时间为2017年的全国专利数据，数据总量为277万条。按照专利申请时间统计，时间跨度为2017年全年，地域覆盖全国。

本实验预训练语言模型分别使用哈工大-科大讯飞联合实验室开源预训练语言模型[4]hfl/chinese-roberta-wwm-ext；澜舟科技开源预训练语言模型[5]Langboat/mengzi-bert-base；华为开源预训练语言模型[6]nezha-cn-base；huggingface上开源英文专利领域预训练语言模型[7]anferico/bert-for-patents。

实验结果

实验结果在A榜测试集以及训练集五折平均上的表现如表1和图3所示。其中CV代表在训练集5折平均的分数，而LB代表在A榜测试集下的分数。

表1:
A榜测试集以及训练集五折平均实验结果

图3:
A榜测试集以及训练集五折平均实验结果图

实验结果显示在基础模型使用memory bank机制以及R-drop都可以在baseline的基础上稳定提点，使用领域预训练虽然在本地CV存在部分抖动，但是在大规模的测试集A榜上的表现有明显的提升。而使用Rake算法提取关键词作为输入降低模型学习难度不仅在CV上同时在LB上也取得了较大的提升。最后通过伪标签学习的方法虽然在CV上提升很多，但是在LB的表现只提升了0.8，不过之后如果使用标签平滑的方法，可以使得模型在CV的表现和LB的表现类似，降低了过拟合的风险。最后使用SimCSE版本的预训练模型在最终结果上也得到了一定的提升。

致谢

感谢中国计算机学会、智慧芽和DataFountain举办了本次比赛，提供了宝贵的竞赛数据，为我们提供了提升自我的机会。感谢团队成员的努力和付出。

参考

[1] Rose S, Engel D, Cramer N, et al. Automatic keyword extraction from individual documents[J]. Text mining: applications and theory, 2010: 1-20.

[2] Text mining: applications and theory[M]. John Wiley & Sons, 2010.

[3] 国家信息中心, 2017, “发明专利数据”, https://doi.org/10.18170/DVN/ASRTHL, 北京大学开放研究数据平台, V2.

[4] Cui Y, Che W, Liu T, et al. Pre-training with whole word masking for chinese bert[J]. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2021, 29: 3504-3514.

[5] Zhang Z, Zhang H, Chen K, et al. Mengzi: Towards lightweight yet ingenious pre-trained models for chinese[J]. arXiv preprint arXiv:
2110.06696, 2021.

[6] Wei J, Ren X, Li X, et al. Nezha: Neural contextualized representation for chinese language understanding[J]. arXiv preprint arXiv:
1909.00204, 2019.

[7] Srebrovic R, Yonamine J. Leveraging the BERT algorithm for Patents with TensorFlow and BigQuery[R]. Technical Report. Global Patents, Google https://services. google. com/fh/files/blogs/bert_for_patents_white_paper. pdf, 2020.

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
[图片已移除]
[图片已移除]