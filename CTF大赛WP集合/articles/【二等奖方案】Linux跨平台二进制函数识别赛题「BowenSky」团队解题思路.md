# 【二等奖方案】Linux跨平台二进制函数识别赛题「BowenSky」团队解题思路

> 原文: https://www.ctfiot.com/124838.html
> ID: 124838

2022 CCF BDCI

数字安全公开赛

赛题「Linux跨平台二进制函数识别」

地址：http://go.datafountain.cn/C9x

@BowenSky战队

获奖方案

团队简介

BowenSky战队来自上海交通大学NETSEC网络安全实验室团队。该实验室依托上海交通大学网络空间安全学院，信息内容分析技术国家工程研究中心，形成了一支成员合理，具有一定研究潜力的研究队伍。团队负责人是邹福泰高级工程师，主要研究方向为网络攻击检测及追踪溯源、系统软件安全。团队主持了多项国家重点研发、国家自然科学基金、国防预研等项目，已发表学术论文100多篇，获得国家发明专利授权40多项，出版了学术专著1本，教材3本。团队学生在国内外信息安全竞赛中多次取得优异成绩，获得过6项全国大学生信息安全竞赛一等奖。

摘要

近几年，跨平台二进制函数相似性检测在学术与工业界都广受关注，该技术可应用于软件成分分析、恶意代码同源分析、代码漏洞检测等方面。最近的基于深度学习的二进制函数相似性检测论文大都将研究重心放在设计一个能充分提取二进制函数语义、结构信息的模型，忽略了模型训练策略的重要性。大部分研究工作在模型训练时从训练集随机采样正、负样本对，这使得训练好的模型对于难样本对无法精准检测。

为了解决以上问题，本论文将二进制函数相似性检测问题视为度量学习问题。引入Multi-Similarity(MS)采样策略和MS损失函数，提高了模型的检测性能。此外，本论文采用指令标准化减少单词表规模，使用Bi-LSTM提取基本块指令序列语义特征，并使用GatedGCN-E提取控制流图结构特征。由此得到的二进制函数表征充分包含二进制语义与结构信息。本方案在赛题测试集上达到了0.922685 Mean Average Precision(MAP)分数，位列初赛榜第四名。

关键词

二进制函数相似性、图神经网络、度量学习

引言

随着开源代码社区的不断壮大，许多开源软件会被编译成不同形式的二进制文件，运行在不同平台。如果该软件源码存在安全漏洞，则漏洞会被扩散至所有从源码编译得到的二进制中，造成极大的安全隐患。二进制函数相似性检测技术可有效解决该问题，该技术旨在识别两段二进制函数代码的相似程度，如果二者由同一份源代码编译得到，则被认为是相似的，反之亦然。如果我们拥有一份有漏洞的二进制函数代码，就可以用其去匹配其他编译环境、指令集下的相似二进制函数，从而判断软件的安全性。除了代码漏洞检测，二进制函数相似性检测还可应用于软件成分分析、恶意代码同源判定等领域。

近几年，大部分二进制函数相似性检测的研究都将重心放在如何设计一个能充分建模二进制函数信息的神经网络模型上。Gemini[1]利用基于人工特征定义的Attributed CFG(ACFG)，采用图神经网络计算二进制函数嵌入，是第一个将图神经网络和孪生网络引入该方向的里程碑式工作，但其无法充分提取基本块内的指令序列信息。Asm2Vec[2]和SAFE[3]则将二进制函数视为指令序列，采用自然语言处理领域的模型进行二进制函数表征的提取，但此类模型无法学习二进制控制流的结构信息。OrderMatters[4]采用在四个子任务上预训练的BERT模型提取基本块语义特征，采用图神经网络提取结构特征，兼顾了二进制语义与结构两种信息。最近的jTrans[5]提出了基于Transformer的预训练模型，作者创新性地改进了Transformer的Position Embedding结构，使模型不仅能学习上下文信息，也能捕捉二进制控制流信息。该模型在二进制相似性检测任务上微调能达到目前最佳的检测性能，且在不微调的情况下进行Zero-shot推理也拥有可观的表现。

然而，目前大部分研究工作都忽视了模型训练策略的重要性。他们大都在数据集中随机采样正负样本对(或三元组)构成模型训练集，这会使得模型训练被无用的样本对或信息量较少的样本对主导，造成模型收敛慢甚至模型退化的现象[6]。jTrans[5]论文表明在目标函数池规模较大的情况下(如104)，现有模型的二进制函数搜索精度会急剧下降。本赛题测试集考察的也是模型在大规模目标函数中(104)的相似函数搜索能力。因此，我们希望通过引入更优的模型训练策略来提高模型的二进制函数相似性检测性能。

本文将二进制函数相似性检测问题视为度量学习问题。我们希望训练后的模型能对不相似样本计算出较大的距离，对相似样本计算出较小的距离。我们引入了度量学习领域的Multi-Similarity(MS)采样算法以及MS损失函数[6]。MS采样算法在每个小批量内采样有价值的样本对，MS损失函数则根据样本自相似度和相对相似度决定样本损失的权重。在二进制函数表征模型方面，考虑到训练、推理的内存开销，我们采用了相比Transformer更轻量化的模型。我们采用Bi-LSTM提取基本块内语义特征，采用GatedGCN-E提取控制流图结构特征。此外，考虑到汇编指令的复杂性，我们对指令进行了标准化处理来降低词表规模。本模型在赛题测试任务上达到了0.922685 Mean Average Precision(MAP)分数，位列初赛榜第四名。

模型与算法

2.1 指令标准化

对于每条指令，我们执行以下三步标准化操作：(1)去除ptr, offset, word, byte等缺乏语义信息的操作数；(2)将所有常量替换为CONST；(3)将保存栈指针和基指针的寄存器名替换为reg_stack_pointer和reg_base_pointer，其他寄存器名保持不变。我们把标准化后的指令的所有操作符和操作数视为单词，将训练集中出现三次及以上的单词构成单词表(词表大小为1,2532)。指令标准化有效降低了单词表规模，并统一了不同指令集架构下关键寄存器的名称。

2.2 数据预处理

图1：模型概览

我们设计了如图1(下半部分)所示的神经网络模型。对于输入的二进制函数控制流图，该模型能计算其表征向量。我们的模型由语义建模与结构建模两部分组成。

图2：语义信息表征模型

在语义建模方面，我们对控制流图中的每个基本块提取指令序列的上下文语义特征。具体地，我们对基本块内每个单词进行词嵌入，并加入指令架构嵌入、编译器嵌入和编译器优化选项嵌入，构成输入序列。接着，采用Bi-LSTM(双向LSTM)提取输入序列上下文信息，最终采用平均池化得到基本块语义表征向量。语义模型结构如图2所示。

图3：GatedGCN-E单层结构

在结构建模方面，我们采用图神经网络模型GatedGCN-E[7]。经过语义表征模型，输入的控制流图(CFG)已经转化成了属性控制流图(ACFG)，即图中每个基本块都是一个特征向量。我们将CFG中的边分为两类：控制流跳转和顺序执行(不满足跳转条件导致的顺序执行)。我们对两类边进行边嵌入得到边特征。至此，原始控制流图已转化为节点特征矩阵和边特征矩阵，可被图神经网络处理。我们采用的GatedGCN-E的单层网络结构如图3所示，在第层网络中，前向传播公式如下公式(1)所示。

其中h为节点特征，N(i)为节点的邻居节点集合。

A、B、C、D均为线性变换矩阵。eij为由节点i指向节点j的边特征。经过一层前向传播，每个节点都将其邻点和邻边的特征进行聚合，因此，经过t层计算，每个节点都能感知其跳节点内的信息。最终的图表征向量由公式(2)和(3)计算得到。

其中，n为控制流图节点个数，Hs为经过s层更新的节点特征矩阵，Go为线性变换矩阵，Pgate为线性变换矩阵，将转化为标量，g为最终表征向量。

2.3 模型训练策略

本方案的模型训练流程如图1(上半部分)所示，在小批量训练过程中，每个批次包含b=m x k个样本二进制函数。其中b为批量大小(batch size)，m为二进制函数组(由相同源代码编译得到的二进制函数属于同一组)的个数，k为每组中样本数量，从而保证每个小批量内一定存在正样本对与负样本对。将这些样本输入二进制函数表征模型，可得到b个样本的表征向量。

我们采用Multi-Similarity(MS)[6]采样算法(miner)，在小批量中选取信息量较大的正负样本对。对于样本xi，负样本对的选择取决于相似度最小的正样本对，正样本对的选择取决于相似度最大的负样本对。MS采样的负样本需满足公式(4)，采样的正样本需满足公式(5)。

其中sij为样本i和样本j的余弦相似度，y为样本所属类别，ε为常量。

模型的训练目标是对采样的正样本对计算出较大的相似度，对采样的负样本对计算出较小的相似度。我们采用Multi-Similarity(MS)损失函数来优化模型，如下公式所示。

其中n为一个批量内采样的正、负样本对个数，Pi为样本i对应的正样本集合，Ni为样本i对应的负样本集合。α、β、λ为超参数。基于MS损失函数，通过反向传播更新二进制表征模型参数。

性能评估

3.1 数据预处理

我们发现赛题数据集中有的样本控制流图包含较多(>2000)基本块，这会导致模型训练时显存开销过大。经统计，我们发现数据集中超过98%的样本的基本块数量小于96，因此，对于基本块数量大于96的样本，我们取其控制流图的前96个基本块的导出子图作为样本输入(测试集不做此操作)。此外，数据集中超过95%的基本块的词序列长度不超过64，因此我们将词序列小于64的基本块用0填充，大于64的基本块进行截断。

我们随机选择了95%函数组作为训练集，剩下5%函数组作为验证集，数据集划分如表1所示。

_

函数族

函数

训练集

66500

2156744

验证集

3500

114187

总计

70000

2270931

表1：数据集划分

3.2 超参数设置与实验配置

我们对Bi-LSTM和GatedGCN-E的层数和维度进行了调参数，并选择在验证集上MAP分数最高的模型作为最终参数选择。模型涉及的超参数如表2所示。

词嵌入维度

128

Bi-LSTM层数

2

Bi-LSTM隐藏层维度

128

GatedGCN-E层数

3

GatedGCN-E隐藏层维度

128

函数表征维度

2270931

表2：模型超参数

模型训练涉及的超参数如表3所示。

批量大小

82（21×4）

训练轮次

80

学习率

10-3在40、60轮

下降10倍

优化器

Adam

每轮参预训练

的样本数

400000

MS采样与损失

ε=0.1 α=2 β=50

表3：模型训练超参数

3.3 模型效果

本方案在赛题测试集上的MAP分数为0.922685，位列初赛榜第四名。表4展示了采用其他在线(批量内)采样算法与损失函数情况下达到的性能。我们对CodeCMR[8]提出的Norm weighted采样算法结合Triplet loss进行了测试，MAP分数为0.855586。将采样算法替换为MS算法，MAP分数提升到了0.883205，由此可见MS miner相比Norm weighted miner能采样到信息量更大的样本对，有效提升了模型二进制相似性搜索性能。本方案采用的MS minder结合MS loss进一步将测试MAP提升到了0.922685，可见MS loss相比Triplet loss能带来更好的性能。

Norm weighted miner

 + Tiplet loss

0.855586

MS miner

 + Triplet loss

0.883205

MS miner + MS loss

0.922685

表4：模型在赛题测试集上的性能

此外，我们还测试了本方案的推理效率。我们的实验环境CPU为8 x Xeon(R) Silver 4114 @ 2.20GHz，GPU为GeForce RTX 2080 Ti。测试结果如表5所示。对于单个样本，预处理约1.68ms。在CPU上，网络模型推理时间约123.69ms，在GPU上，网络模型推理时间约8ms。此外，本方案提出的神经网络模型参数量为 2.6 Million，模型文件大小为11MB，因此本方案在拥有较好的性能的同时，也具有轻量化的特点，具有良好的推理效率。

硬件

预处理

 (ms/样本)

模型推理 

(ms/样本)

CPU

1.6837

123.6908

GPU

8.0288

表5：方案推理效率

创新点与讨论

本文提出的跨平台二进制相似性检测模型的创新点在于：

(1) 提出了能同时提取控制流图语义与结构信息的模型；

(2) 模型轻量化，可训练参数为2.6Million，模型文件大小仅11MB；

(3) 引入了度量学习领域的MS采样与损失函数，提高模型性能。

本方案还有许多可改进之处：

(1) 在指令标准化策略中，本方案将操作符和操作数作为词，而许多操作数的结构依然很复杂，导致本方案的词表规模较大，且语义模型无法感知操作数内部结构，可参考PalmTree[9]将操作数切分成更细粒度的token，一方面能大幅度降低词表规模，另一方面能使语义模型感知操作数内部结构。

(2) 本方案采用的样本采样算法为在线采样，即在每个小批量内采样正负样本，其缺点是无法挖掘到批量外潜在的更有效的样本对。可参考XBM[10]和MOCO[11]提出的采用队列来存储过去批量特征的方法进行跨批量的采样。

致谢

感谢CCF BDCI组委会提供的竞赛机会与赛题数据，以及赛题负责老师的悉心答疑！

参考

[1] Xu X, Liu C, Feng Q, et al. Neural network-based graph embedding for cross-platform binary code similarity detection[C]//Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security. 2017: 363-376.

[2] Ding S H H, Fung B C M, Charland P. Asm2vec: Boosting static representation robustness for binary clone search against code obfuscation and compiler optimization[C]//2019 IEEE Symposium on Security and Privacy (SP). IEEE, 2019: 472-489.

[3] Massarelli L, Luna G A D, Petroni F, et al. Safe: Self-attentive function embeddings for binary similarity[C]//International Conference on Detection of Intrusions and Malware, and Vulnerability Assessment. Springer, Cham, 2019: 309-329.

[4] Yu Z, Cao R, Tang Q, et al. Order matters: semantic-aware neural networks for binary code similarity detection[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2020, 34(01): 1145-1152.

[5] Wang H, Qu W, Katz G, et al. jTrans: jump-aware transformer for binary code similarity detection[C]//Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and Analysis. 2022: 1-13.

[6] Wang X, Han X, Huang W, et al. Multi-similarity loss with general pair weighting for deep metric learning[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2019: 5022-5030.

[7] Bresson X, Laurent T. Residual gated graph convnets[J]. arXiv preprint arXiv:1711.07553, 2017.

[8] Yu Z, Zheng W, Wang J, et al. Codecmr: Cross-modal retrieval for function-level binary source code matching[J]. Advances in Neural Information Processing Systems, 2020, 33: 3872-3883.

[9] Li X, Qu Y, Yin H. Palmtree: learning an assembly language model for instruction embedding[C]//Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security. 2021: 3236-3251.

[10] Wang X, Zhang H, Huang W, et al. Cross-batch memory for embedding learning[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2020: 6388-6397.

[11] He K, Fan H, Wu Y, et al. Momentum contrast for unsupervised visual representation learning[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2020: 9729-9738.

—End—

戳“阅读原文”，速来参赛办赛~

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/7-1689163150.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/7-1689163151.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/6-1689163152.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/6-1689163152.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/8-1689163152.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/6-1689163153.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/4-1689163153.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/0-1689163153.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/4-1689163153.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/1-1689163153.jpeg)