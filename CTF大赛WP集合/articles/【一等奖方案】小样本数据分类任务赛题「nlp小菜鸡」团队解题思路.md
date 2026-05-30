# 【一等奖方案】小样本数据分类任务赛题「nlp小菜鸡」团队解题思路

> 原文: https://www.ctfiot.com/133251.html
> ID: 133251

2022 CCF BDCI

第十届CCF大数据与计算智能大赛

第十届CCF大数据与计算智能大赛（2022 CCF BDCI）已圆满结束。大赛官方竞赛平台DataFountain（简称DF平台）将陆续释出各赛题获奖队伍的方案思路。本方案为【小样本数据分类任务】赛题的一等奖获奖方案，赛题地址：

https://datafountain.cn/competitions/582（戳底部“阅读原文”可直达）

获奖团队简介

团队名称：nlp小菜鸡

团队成员：本团队由具有丰富比赛经验及正在自然语言处理（NLP）专业领域从事实习的团队成员组成。团队成员包括：

朱金乘（队长），华南师范大学电子与信息工程学院，研二，主要研究方向为数据挖掘与自然语言处理、图像生成，曾带队在华为中国大学生ICT大赛2021创新赛全国总决赛中荣获二等奖，同时在2021年数据挖掘和人工智能建模大赛中荣获二等奖，在本次比赛中，主要负责初赛时期的各个模型的训练以及推理代码编写，调参，使用各种trick提分，英文数据翻译，模型融合以及伪标签生成和训练，复赛的方案制定与实施，复现时期的代码整理，复现文档编写，docker镜像的制作，决赛时期的说明论文编写等工作。

包刚林（队员），北京交通大学，研二，主要研究方向为自然语言处理，曾在阿里天池新冠疫情机器翻译挑战赛获得冠军，以及WMT2022 译文质量评测任务英德赛道获得亚军，在本次比赛中，主要负责初赛时期模型融合代码的编写，领域预训练代码的编写，伪标签分层抽样代码编写，英文数据翻译，复现时期的shell脚本的编写与复现代码调试，决赛时期的ppt制作与答辩等工作。

穆丽伟（指导老师），华南师范大学物理与电信工程学院，副教授，主要研究方向为机器学习、信息论、信道编码、无线通信。

所获奖项：一等奖

摘要

目前的人工智能技术日趋成熟，尤其在大数据处理的模型应用很成功，但当处理小数据集时，人工智能技术尚待完善。近年来，小样本学习被提出来解决这一问题。

随着政策扶植、国家工业化水平和国民教育水平提高，我国的专利申请量快速增长，专利检索、查新、管理等需求也不断增加。为了提升专利服务质量，通常需要建立多个维度的专利分类体系。多维度使得专利分类体系比较复杂，又因其专业性强，获取带有监督信息的专利分类标签需要较高的人工成本，故本参赛团队依据该背景，对专利数据进行处理，关注分类模型在小样本专利数据的分类效果，推动小样本学习技术在实际应用中的发展。

本团队将该任务转为自然语言处理中常见的多分类任务，采用通用预训练模型->领域预训练模型->领域微调的三阶段范式，主要选择使用了Nezha[1]、Ernie-Gram[2]、Ernie-3.0-xbase-zh[3]、Bert-for-patents、Chinese-roberta-wwm-ext-large[4]等最新的预训练模型。针对该赛题中训练样本数据较少这一难点，本团队使用了AWP[5]对抗训练、SWA[6]、分层学习率、Multi-Sample Dropout等技术增强模型的鲁棒性。最终通过集成不同优势的多个模型和伪标签学习，利用模型大小不到2g的模型推理，在小样本数据分类任务上，取得了较好的结果：复赛成绩0.61387745，排名第一。

关键词

文本分类、小样本分类、

领域预训练、预训练模型

赛题分析

1.1 数据集

本赛题训练集为958条专利数据，包括专利权人、专利标题、专利摘要和分类标签，其中分类标签经过脱敏处理，共36类，初赛测试集共20839条样本，复赛测试集包含20890条样本。

1.2 评价指标

本赛题需要输出测试集每条样本的标签类别。评价指标采用macro F1指标，计算公式如下：

其中Pi是第i个类别的Precition，Ri是第i个类别的Recall，n是类别总数。

1.3 数据分析

本团队主要从训练集的标签分布，文本长度分布进行分析。

图1：训练集title+assignee+abstract

拼接后的长度分布

图2：初赛测试集拼接title+assignee+abstract的长度分布

图3：复赛测试集拼接title+assignee+abstract的长度分布

图4：训练集标签分布

如图1，2，3所示，训练集将专利标题、专利申请人、专利摘要拼接后的文本长度最大值在657，测试集拼接后长度都未超过600。所以本赛题数据属于短文本数据。训练集标签分布如图4所示，可看到训练集标签分布呈现长尾分布，属于标签不平衡问题。

经过以上分析，本团队认为赛题任务的难点主要有四点：

一是训练集数据量太少，模型很容易过拟合；二是训练集标签分布不均衡，有些标签类别只有4，5条样本，而模型预测更倾向于样本数量多的标签类别；三是标签类别语义未知，很难通过分析badcase，做后处理以及提示学习；四是训练集数据量太少，线下指标并不能和线上指标达成一致，故只能通过线上指标来挑选模型，然而线上提交次数有限。

整体方案

本团队的最终解决方案，主要是由Nezha[1]模型方案、Ernie-Gram-zh[2]模型方案、Ernie-3.0-xbase-zh[3]模型方案、Bert-for-patents模型方案、Chinese-roberta-wwm-ext-large[4]模型方案通过加权平均集成，经过两阶段的伪标签学习，最后利用伪标签数据和训练集训练5折Ernie-Gram-zh[2]模型作为最后提交模型。整体流程如图5所示：

图5：整体方案流程图

2.1 Nezha-large模型

Nezha是一个华为诺亚方舟实验室在预训练模型上的实践总结，它在Bert的基础上加了很多当下有用的优化。本团队用初赛测试集对Nezha模型进行领域增量预训练，并设计了Nezha + Multi-Sample Dropout + Linear的结构。实验结果表明，经过领域预训练后的Nezha模型具有一定的泛化能力，单项指标达0.61。模型架构示意图如图6所示：

图6：Nezha+Multi-Sample Dropout+Linear

示意图

2.2 Roberta-large模型

Chinese-roberta-wwm-ext-large模型是支持中文的Roberta-like BERT模型，它采用Whole Word Masking技术；简单取消了Next Sentence Prediction loss；直接采用最大长度512进行训练。本团队简单使用了Roberta-large+linear的基础结构，并采用AWP[5]和SWA[6]技巧来增强模型的鲁棒性，单项指标达0.595。

2.3 Bert-for-patents模型

Bert for patents是谷歌基于Bert-large模型，在超过1亿项专利上训练的模型。本团队将比赛数据集翻译成英文数据，并将输入文本输入拆分title + assignee + head + body + tail 5个部分，其中head、body、tail是通过对abstract分句得到的，模型结构采用Bert-for-patents + MultiDropout + Linear的结构，同时采用SWA技巧来增强模型的鲁棒性，单项指标达0.605。

2.4 Ernie-gram-zh模型

Ernie-gram是百度的研究成果，它提出显式的n-gram掩码语言模型，通过引入多粒度语言知识增强预训练模型效果，在5项典型中文文本任务中领先。本团队在模型结构设计了Ernie-gram-zh + GRU + Multi-Sample Dropout +Linear的结构，同时采用SWA技巧来增强模型的鲁棒性，单项指标达0.597。模型架构示意图如图7所示：

图7：Ernie-gram-zh模型架构示意图

2.5 Ernie-3.0-xbase-zh模型

文心Ernie3.0相对于业界其他大模型来说，在各类任务场景和零样本、小样本学习中都取得了非常显著的提升。本模型结构采用和Ernie-gram-zh相同的模型结构，同时采用SWA技巧来增强模型的鲁棒性，单项指标达0.599。

优化方案

在训练、验证、测试阶段，为提高模型的泛化能力，我们做了以下优化：

(1) 领域预训练：预训练模型通常是在通用领域的大规模文本上进行训练的，本团队利用比赛测试集的无监督数据，领域增量预训练Nezha-large-wwm模型，从而提升我们下游任务的效果。

(2) AWP对抗训练：训练阶段同时对Embedding层上和模型上增加扰动，形成双扰动机制，使模型更具有泛化能力。

(3) SWA[6]：保存多个局部最优点进行集成。

(4) 加权平均融合：为综合各模型的不同优势，我们根据模型的多样性选择不同的融合权重，最后我们将Ernie-gram和Ernie-xbase模型的权重设置较小。

(5) 二阶段伪标签：由于我们训练集数据量较小，而测试集数据量较大，为了增强我们模型的泛化能力，我们采用了二阶段伪标签，其中第一阶段是由训练集训练出来各模型的集成生成的，而第二阶段则是由训练集、初赛测试集70%的伪标签、复赛测试集70%伪标签训练Nezha10折模型集成生成的。

3.1 其他尝试方案

(1) 尝试最新NLP范式[7]Prompt模型，使预训练任务和下游任务统一，该方案在小样本学习任务上具有优势，但由于我们比赛数据标签语义未知，未加入融合。

(2) 尝试对训练数据进行文本增强，通过简单的随机替换词语、交换、删除、回译等操作，该方法虽然能引入一些噪声，但对本次任务并无提升，未加入融合。

(3) TTA:
尝试在测试阶段，对测试集做不影响标签的数据增强，使预测结果更可靠，但对本次任务并无提升，未加入融合。

3.2 部分实验记录

表1：部分实验结果记录表

从表1中可以得出结论，通过加权融合综合不同模型的不同优势，通过伪标签增强数据量，可以极大提升指标。在比赛中，最终线上成绩为0.61387745，居第一。我们设计的模型方案模型大小并未超于2g，效果好，还具备泛化能力强，易于生产落地。

致谢

感谢本次大赛的所有工作人员！感谢指导老师的指导！感谢每位队友的辛苦付出！

参考

[1] Wei J ,Ren X ,Li X , et al. NEZHA: Neural ContextualizedRepresentation for Chinese Language Understanding[J]. 2019.

[2] D Xiao, Li Y K , Zhang H , et al. ERNIE-Gram: Pre-Training withExplicitly N-Gram Masked Language Modeling for NaturalLanguage Understanding[J]. 2020.

[3] Sun Y, Wang S, Feng S, et al. Ernie 3.0: Large-scale knowledge enhanced pre-training for language understanding and generation[J]. arXiv preprint arXiv:
2107.02137, 2021.

[4]  Liu Y ,  Ott M ,  Goyal N , et al. RoBERTa: A Robustly Optimized BERT Pretraining Approach[J].  2019.

[5]  Deng  Z ,  Dong Y ,  Pang T , et al. Adversarial Distributional Training for Robust Deep Learning[C]// 2020.

[6] Wang G ,Li W , Ourselin S , et al. Automatic Brain TumorSegmentation using Convolutional Neural Networks with Test-Time Augmentation[J]. Springer, Cham, 2018.

[7]  Liu P, Yuan W, Fu J, et al. Pre-train, prompt, and predict: Asystematic survey of prompting methods in natural languageprocessing[J]. 2021

—End—

戳“阅读原文”，速来参赛办赛~

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/2-1693742830.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742830.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/1-1693742831.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/7-1693742831.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693742831.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742831.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/6-1693742832.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/9-1693742832.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742832.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/10-1693742832.png)