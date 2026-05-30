# 【二等奖方案】数据湖流批一体性能优化「TT」团队思路

> 原文: https://www.ctfiot.com/135378.html
> ID: 135378

2022 CCF BDCI

第十届CCF大数据与计算智能大赛

第十届CCF大数据与计算智能大赛（2022 CCF BDCI）已圆满结束，大赛官方竞赛平台DataFountain（简称DF平台）将陆续释出各赛题获奖队伍的方案思路，欢迎广大数据科学家交流讨论。

本方案为【数据湖流批一体性能优化】赛题的二等奖获奖方案，赛题地址：https://www.datafountain.cn/competitions/585（戳底部“阅读原文”可直达）

获奖团队简介

团队名称：TT

团队成员：汤振东（队长）、樊秋轩

TT团队由汤振东、樊秋轩两人组成。成立的初衷是钻研新知识，互相帮助，交流开发经验。

汤振东，熟悉生物信息及数据挖掘，对Spark等分布式框架及数仓有浓厚兴趣，喜欢思考。作为本次比赛队长，积极推动比赛的进行，承担主要开发任务，与成员保持良好沟通，互相交流新的想法。

樊秋轩，拥有多年开发经验，对Java和Scala及各种分布式计算框架及调优都比较熟悉，作为参与成员为本次比赛提供代码指导。

所获奖项：二等奖

摘   要

随着近年来数据量的急剧膨胀，人们对读写性能要求也越来越高，我们见证了从数据湖概念的提出到一些优秀数据湖框架的出现及流行[1]。本文对2022 CCF BDCI 数据湖流批一体性能优化比赛参赛方案的内容、实验、结论进行概况总结。数据集为官方提供的11个parquet文件，任务的基本流程分为写任务和读任务两个模块，提出了一个基于Spark[2]和LakeSoul 数据湖框架的读写优化方案。通过对LakeSoul 源码的修改，我们可以在进行upsert操作时指定一个自定义版本号，在即使是乱序写入的场景，也可以根据自定义版本号正确合并。基于此功能，可以在写任务时进行乱序并行写入以提高并行度进而提升性能。我们使用Iceberg、Hudi、LakeSoul 三个数据湖框架进行了多次实验，通过耗时对比，可见本方案性能具有显著优越性。

关 键 词

数据湖，元数据，并发，乱序，读写性能，Spark

1 赛题背景

数据湖是大数据时代出现的概念之一。数据湖的最初想法源于商业领域而不是学术领域。由于数据湖是一个具有革命性概念的新构思，因此它的采用带来了许多挑战。然而，改变数据格局的潜力提高了使数据湖的研究价值[3]。业内涌现出 DeltaLake、Iceberg、Hudi 等数据湖存储框架。而 LakeSoul 作为国产唯一湖仓表存储框架，在元数据扩展性、并发性和数据实时更新能力上有着全新的设计实现和性能优势，也吸引了业内的广泛关注。

湖仓存储框架的流批一体读写性能，是非常重要的指标，关系到数据能否快速、准确的摄入到湖仓之中，并做高效的数据处理分析。而数据湖通常使用计算存储分离的设计，给读写性能优化带来很大的挑战。

1.1 数据集

数据集为官方提供的11个parquet文件，每个文件中有相同的字段，uuid（String)、ip（String）、hostname（String）、requests（Long）、name（String）、city（String）、job（String）、phonenum（String）。所有文件均未压缩，base-0文件900MB大小、1000,0000条记录，其余base-1~base-10文件均为179MB大小，200,0000条记录。所有文件uuid的pv值为3000,0000，uv值为2000,0000，requests字段求和的最大值为6240。只有name字段的值存在“null”字符串，且所有字段值均无null。

1.2 基本流程

主要分为写表任务和读表任务。

1.2.1 写任务

a. 创建lakeSoul的MOR表。主键：uuid，分区数量：4，合并方式：读时合并(MOR)。

b. 所有文件的读取及upsert操作封装成多个Future对象并行执行。

c. Await所有Future任务完成 。

写任务的流程图如图1。

图 1:
写任务流程图

1.2.2 读任务

a. 注册MergeOperator，分别为求和Operator、最后一个非null值Operator、最后一个值Operator。

b. 按version合并元数据表partition_info中的多次upsert的快照集合。

c. 根据Operator进行读时合并，未指定Operator的采用默认DefaultMergeOp，合并规则为取最后一个。

d. 合并结果写入本地磁盘，文件格式为parquet，压缩格式为snappy。

1.3 关键源码修改点

对lakeSoul框架源码的部分关键修改提要。

1.3.1 LakeSoulTable

executeUpsert方法中LakeSoulUpsert对象提供一个额外userDefinedTimestamp成员。

1.3.2 UpsertCommand

a. 在canUseDeltaFile时，增加是否通过repartition增加write的并行度的判断，由于本方案已并行并充分利用CPU核数， 故仅对0号900MB大文件依据uuid进行repartition，通过实验，分成8个分区得到较稳定结果。其余1-10号文件均直接写入即可，节省shuffle时间。

b. 给写文件的返回值Seq[DataFileInfo]设置自定义时间戳作为partition_info的元数据commit

1.3.3 TransactionCommit

变更元数据表写入内容：commit方法新增传参userDefinedTimestamp，默认值为-1。由传入的自定义时间戳替代原来系统时间时间戳。

1.3.4 DBManager

修改DBManager的commitData方法，提交模式为MergeCommit时，使得一次提交的元数据仅保留当前快照号，不再继承之前的所有快照构成集合。使得提交的version不再是自增值，而是使用curPartitionInfo在TransactionCommit时设置的自定义时间戳（版本号）。

1.3.5 MergePartitionInfoTable

a. 合并元数据表partition_info中的多次upsert的快照列表

b. 根据table_id读表partition_info

c. 根据version升序排序

d. 按照排序顺序合并多次upsert的快照成一个集合

e. 将合并结果写入partition_info表 version=999

2 实验

2.1 实验环境

Spark版本为3.1.2，Java 版本为 OpenJDK 11，操作系统版本为 Ubuntu 20.04

core 数统一为 4，每个 core 分配 4G 内存

硬件环境为AWS r5a.xlarge，磁盘为gp2

PostgreSQL (作为 LakeSoul 元数据服务存储)

MinIO (用以本地模拟 S3 存储)

LakeSoul 2.1.0

2.1 并行优化

由于赛题指定环境仅有4个核，故要充分利用所有核数。但由于单个文件只有一个row group，使得在读取时仅1核在工作读取该文件全部数据，如图2，造成性能浪费。解决方法：由于指定了upsert时自定义version，无需再考虑多线程执行时完成先后顺序的问题，直接通过scala的Future操作并行执行读数据及upsert，如图3。经实验，可带来总耗时约40s的提升。

图 2:
串行时序图

图 3:
并行时序图

2.2 元数据变更

对元数据表partition_info提交修改，以适配乱序写入。

2.2.1 初始状态

每次upsert时会存入一个自增version及snapshot。存入的snapshot是继承自上一个version的snapshot加上本次upsert的snapshot的集合。元数据表partition_info记录见图3。

图 4:
原始元数据

2.2.1 本方案修改

本方案Upsert时所提交信息变更为，version为用户在upsert时自行指定的版本号而不再是自增数。snapshot仅保存当前快照ID。新的元数据表partition_info记录见图4。

图 5:
本方案元数据

2.2.1 读表时Merge元数据逻辑

在读表时，先对partition_info表进行merge操作，merge规则为新增一条记录version为999，snapshot为之前提交的所有记录的snapshot为多次提交的version大小升序排序的集合。此时在读表的时候便能根据该条记录进行符合预期的合并操作。实验结果如图5，在version=999的记录中，snapshot集合符合预期。

图 6:
元数据合并结果

2.3 重分区

LakeSoul源码在写时repartition可以提高单个文件写入时的并行度及解决数据倾斜问题，但本赛题每个文件读取结果仅有一个分区，且通过线程池并行执行多个读写任务，故并行度充足且不需要考虑数据倾斜问题。本方案采用仅对大文件（base-0.parquet）进行重分区，而其他任务均直接写入以避免shuffle耗费。我们采用sort-shuffle的bypass模式进行实验。实验结果Spark UI如图6，可见仅对900MB目标大文件进行了Shuffle，而其他10个178MB小文件Job均没有进行Shuffle过程，结果符合预期。

图 7:
Spark UI

2.4 实验结果及结论

表1:
各方案实验结果

通过对IceBerge、Hudi、LakeSoul及本文新提出的方案分别在COW/MOR模式下采用10次实验取平均值的方法，得到读写耗时，如表1。可见本方案在读写性能上具有显著优越性，较各方案写表耗时和总耗时均有大幅度提升。

3 核心创新点

3.1创新点

在lakeSoul数据湖源码的基础上，提供自定义Upsert版本号接口，使得即使在upsert操作没有在既定的顺序执行的情况下，依然可以在读表的时候（MOR)根据自定义的版本号进行符合预期的merge。

对于所读取文件是否需要进行重分区以提高并行度给予用户自行选择的接口。在某些场景，核数已充分利用或者CPU资源不敏感的情况下，关闭此步repartition操作以节约shuffle的时间。

3.2价值

脱离了UPSERT需要固定执行顺序的束缚后，我们可以解决很多场景问题，例如：

并行场景。用户可以轻易的使用并行同步执行UPSERT而不用考虑多线程情况下执行顺序混乱的问题，以进行性能调优（即本方案需要解决的问题）

补数场景。对于有需要按顺序merge的一批数据源，在数据不全时可以先行upsert已有数据源而不用等待全部数据源再按顺序依次upsert，之后再进行补数。如已经有1，2，3，6，7号的数据源，在4与5号缺失的情况写可以先对已有的数据源进行upsert，等到拥有4，5数据源时再进行upsert补充，读时依然可以merge到预期结果，提高了写表时机的灵活性。

致  谢

首先感谢DataFountain平台以及数元灵科技提供这次学习机会让我们对数据湖框架有了更深入的了解。其次感谢队友的鼎力相助，解决了许多工程实践上的难题。最后感恩家人的陪伴！

参  考

[1] Fang, and Huang. “Managing data lakes in big data era: What’s a data lake and why has it became popular in data management ecosystem.” IEEE International Conference on Cyber Technology in Automation IEEE, 2015:
820-824.

[2] Matei Zaharia, and Mosharaf Chowdhury . “Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing”NSDI’12 Proceedings of the 9th USENIX conference on Networked Systems Design and Implementation, Pages 2-2 .

[3]  Khine, P. P. , and  S. W. Zhao . “Data lake: a new ideology in big data era.” International Conference on Computer Science & Applications 2018.

—End—

戳“阅读原文”，速来报名参会~

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/10-1694607890.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/3-1694607890.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694607891.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/2-1694607891.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694607891.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/2-1694607892.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/7-1694607892.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/6-1694607892.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1694607893.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1694607893.png)