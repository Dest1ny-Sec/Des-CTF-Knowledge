---
title: CCF BDCI 2022 三等奖 - 数据湖流批一体性能优化 冀科数字
contest: CCF BDCI 2022 (第十届CCF大数据与计算智能大赛)
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags:
- 数据湖
- LakeSoul
- Spark3.1.2
- Scala
- 流批一体
- coalesce
- parquet
- S3
- AQE
- 并行调度
attack_chain: 11个parquet并行读 → spark SQL join流计算 → coalesce合并非空字段 → 写入LakeSoul湖仓 → 全量并行读出
key_payload: spark.sql.shuffle.partitions=20 + spark.default.parallelism=12 + coalesce合并
one_liner: 冀科数字团队用Spark+LakeSoul+coalesce在数据湖流批一体赛道上拿三等奖。
lesson: 流批一体场景中字段合并用coalesce可同时处理null字符串和空值,比RDD算子更清晰高效;并行11个parquet任务+DataFrame持久化避免重算;国产LakeSoul数据湖支持实时+批量统一写入;Spark 3.x比2.x性能提升2倍多。
quality: medium
full_path: 【三等奖方案】数据湖流批一体性能优化「冀科数字」团队思路.full.md
meta_path: 【三等奖方案】数据湖流批一体性能优化「冀科数字」团队思路.meta.md
images_removed: true
images_removed_count: 4
schema_version: v3.0.0-P0
summary: CCF BDCI 2022 三等奖 - 数据湖流批一体性能优化 冀科数字。冀科数字团队用Spark+LakeSoul+coalesce在数据湖流批一体赛道上拿三等奖。。经验：流批一体场景中字段合并用coalesce可同时处理null字符串和空值,比RDD算子更清晰高效;并行11个parquet...
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 4
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/135726.html
reasoning_chain:
- 赛题 11 个文件分别流批读写 → 触发点：流批一体性能瓶颈
- 假设：单 partition 顺序读会卡 → 动作：spark.sql.shuffle.partitions=20 + parallelism=12
- 11 个 parquet 并行读入 DataFrame → 动作：spark.read.parquet(path) + persist(StorageLevel.DISK_ONLY)
- 触发点：字段合并有 null 字符串和空值 → 假设：coalesce 比 RDD when/otherwise 更清
- 动作：df.na.fill("").coalesce(1) 写入 LakeSoul 湖仓 → 观察：避免产生小文件
- 数据湖写入要分批 upsert → 触发点：LakeSoul 默认系统时间戳 → 假设：实时+批量合并乱序会丢
- 动作：用 DataFrame.write.mode('append') + LakeSoul TableProvider 注册 → 观察：11 路并行写完
- 下游读取走 LakeSoul 全量并行 → 动作：df.write.partitionBy(...).parquet → 观察：输出 12 任务并行
- Spark 3.x AQE 自适应查询 → 假设：自动合并小 partition → 动作：spark.sql.adaptive.enabled=true
- 最终三等 → 触发点：性能对比 Spark 2.x 提升 2 倍多
failed_attempts:
- 试图直接 LakeSoul upsert 不加 coalesce → 失败：产生大量小文件、读时合并开销大
- 试图用 RDD API 手写字段合并 → 失败：null 字符串和空值混用时分支太多
- 试图不开 AQE → 失败：小 partition 过多 shuffle 拖慢
key_observations:
- coalesce 字段合并比 RDD when/otherwise 更清、性能更稳 (LakeSoul/Delta 通用)
- spark.sql.shuffle.partitions + parallelism 双参数要分别设置 (20 与 12 各自角色不同)
- Spark 3.x AQE (Adaptive Query Execution) 自动合并小 partition 是性能关键
- 国产数据湖 LakeSoul 支持流批一体，比 Iceberg/Hudi 国产化更友好
- DataFrame.persist 避免重复计算是流批一体场景的标配
prerequisites:
- Spark 3.x DataFrame API + SQL
- LakeSoul / Iceberg / Hudi 数据湖概念
- Shuffle / Partition / Parallelism 三参数调优
- 流批一体架构 (Lambda/Kappa)
---
# 【三等奖方案】数据湖流批一体性能优化「冀科数字」团队思路

> 原文: https://www.ctfiot.com/135726.html
> ID: 135726

2022 CCF BDCI

第十届CCF大数据与计算智能大赛

第十届CCF大数据与计算智能大赛（2022 CCF BDCI）已圆满结束，大赛官方竞赛平台DataFountain（简称DF平台）正陆续释出各赛题获奖队伍的方案思路，欢迎广大数据科学家交流讨论。

本方案为【数据湖流批一体性能优化】赛题的三等奖获奖方案，赛题地址：https://www.datafountain.cn/competitions/585（戳底部“阅读原文”可直达）

获奖团队简介

团队名称：冀科数字

团队成员：唐松（队长）、王志强、崔能西、檀改芳、张天亮

队长：唐松，目前天津大学博士在读。主要研究方向为区块链、大数据系统架构等。在比赛中负责spark算法实现。

队员：王志强，博士，毕业于浙江大学控制系。目前工作于河北省科学院应用数学研究所，主要研究方向为大数据分析等。在比赛中负责整体方案与并行算法设计。

队员：崔能西，大三就读于天津大学工科实验班。在比赛中负责数据处理与算法测试。

队员：檀改芳，本科，毕业于燕山大学测控技术与仪器专业。目前工作于河北省科学院应用数学研究所，主要研究方向为机器学习、知识图谱。在比赛中负责数据湖算法实现。

队员：张天亮，博士，毕业于中国农业大学。目前工作于河北省科学院应用数学研究所，主要研究方向为机器学习与数据分析等。在比赛中负责整体方案优化。

所获奖项：三等奖

摘   要

本方案最大的亮点读取每个parquet文件后，先进行流计算，调用spark SQL join函数，在字段合并时调用coalesce函数返回非空的字段，合并后结果，再流式存储到lakesoul。在从数据湖lakesoul读取全量数据时，分多个并行任务写入到存储中。

关 键 词

数据湖性能优化，spark优化，并行执行，多任务调度

1 赛题任务简介

1.1 数据计算要求

湖仓一体、流批一体已经成为大数据新一代架构范式。通过在数据湖存储上构建数仓表存储，并支持流批一体写入，能够大幅简化大数据架构、开发流程以及部署运维开销，降本增效。业内涌现出 DeltaLake、Iceberg、Hudi 等数据湖存储框架。湖仓存储框架的流批一体读写性能，是非常重要的指标，关系到数据能否快速、准确的摄入到湖仓之中，并做高效的数据处理分析。而数据湖通常使用计算存储分离的设计，并且需要支持多种计算框架、支持对象存储等，给读写性能优化带来很大的挑战。

在数据湖流批一体性能优化场景中，主要研究如何面对业务日志实时入湖分析，我们可以借助数据湖任务运行效率高、并行处理优化、可扩展性增强的特点，进行线上业务的各类指标数据处理，然后同步到湖仓中进行进一步分析，需要将这些数据通过流批一体的方式写入到湖仓中，能实现跨业务条线、跨系统的数据整合，为管理分析和业务决策提供统一的数据支持，处理后的数据可以用于 BI 报表分析展示或者 AI 模型训练。

本赛题通过模拟业务日志实时入湖分析分析场景，在线上业务中，通常会有各类指标数据需要同步到湖仓中进行进一步分析，例如用户的请求数、商品的点击购买次数等。为了能够快速分析线上各类指标数据，需要将这些数据通过流批一体的方式写入到湖仓中，在湖仓中会进行ETL加工处理，包括字段求和、特殊字符串处理等。对给定的数据，快速过滤并准确计算出满足条件的记录，以多个批次的方式模拟流式、并发写入，所有数据写入完毕后全量读取出来。

2 赛题分析

根据分析，本赛题要面对业务日志实时入湖分析场景，使用以下技术提升数据读写效率：

（1）计算框架方面，本课题限定了计算框架为Spark3.1.2。Spark 3.x比Spark 2.x的性能提高了2倍多，支持自适应查询执行、动态分区剪枝和其他优化，并且改进了Spark SQL引擎，从而提高了性能和ANSI兼容性，新的自适应查询执行(AQE)框架通过在运行时生成更好的执行计划来改进性能和简化调优，本赛题，我们团队使用Spark SQL API，来优化数据湖读写。

（2）语言环境方面，Spark通过与编程语言集成的方式暴露RDD的操作，每个数据集都表示为RDD对象，对数据集的操作就表示成对RDD对象的操作。Spark主要支持的编程语言是Scala、java、python。Spark是使用Scala语言开发的， 理论上使用Scala开发Spark程序运行效率会更高。Scala设计初衷是要整合面向对象编程和函数式编程的各种特性。Scala运行于Java平台（Java虚拟机），并兼容现有的Java程序。是一个兼顾开发效率和运行效率的语言，具有非常优秀的开发特性。本赛题，我们选用Scala语言开发程序，方便在Spark-Shell测试程序。

（3）数据湖框架选择，目前业用的较多的数据湖框架主要有DeltaLake、Iceberg、Hudi 、 LakeSoul 等，其中LakeSoul作为国产唯一的开源数据湖存储框架，在存储层面，统一支持实时和批量两种方式对湖仓中的数据进行更新写入和读取，可以允许我们不用分别开发两套不同的数据链路。这一方面大幅降低了开发成本，也消除了两套链路带来的数据口径不一致等问题，减少了维护时间成本。本课题，我们选用LakeSoul在数据湖上构建数据表，能够充分利用云原生架构下对计算资源和存储资源的弹性能力，支持数据的实时更新写入。湖仓一体化的方式简化了基础设施的使用门槛，并提升了资源利用效率和性能。

（4）内存管理方面，Scala有一套特别的内存管理机制。而且本方案测试数据规模庞大，进行大块的内存声明和回归，都有可能导致各种内存异常。因此，内存空间的复用和及时回收也是需要考虑的问题，同时在程序设计过程中，应可能减少大块数据频繁读取。

（5）Spark任务调度管理方面，现在的计算机通常都是多核CPU，充分利用多线程也是方案应该考虑的。将数据进行分块分线程异步并行读取，因此Spark参数调优也是本课题重要优化手段，正确的参数配置对提升Spark的使用效率具有极大助力。

3 模型构建

3.1 主体流程设计

本方案根据业务日志实时入湖分析的特点，在Spark计算引擎和LakeSoul读写优化的基础上，考虑数据快速载入、多任务并行计算、Spark调度优化等功能，建立本方案的主体流程：

（1）parquet格式文件的读取：base-0.parquet、base-1.parquet…base-10.parquet，11个parquet格式文件中的数据进行分析，业务需要版本号大的日志文件对版本号小的数据进行更新，因此读写和更新顺序非常重要，本课题，我们针对每个日志文件，分别利用spark.read.format并行11个任务读取数据，先进行流计算，此时一定要注意DataFrame的重用和持久化，避免后续需要，再次重新计算，提升效率。

（2）数据计算：

a) spark参数的确定：结合core 数统一为 4，每个 core 分配 4G 内存的运算环境，本课题我们设置spark参数如下：spark向S3写入大文件的最佳方法是设置”spark.hadoop.fs.s3a.fast.upload.buffer” = “bytebuffer”，”spark.hadoop.fs.s3a.multipart.size” = “167108864”，dataframe中shuffle partitions的数量是由spark.sql.shuffle.partitions控制，本课题我们设置”spark.sql.shuffle.partitions” = “20”，spark作业中，各个stage的task的数量，也就代表了spark作业在各个阶段stage的并行度，parallelism是指RDD任务的默认并行度，Spark中并行度是指RDD中的分区数，即RDD中的Task数，结合cpu个数为4，经验值为cpu个数的2-3倍，本课题我们设置”spark.default.parallelism” = “12”。

b)日志数据更新：调用spark SQL join函数，在字段合并时调用coalesce函数返回非空的字段，合并后结果，再流式存储到lakesoul，coalesce函数有个好处，可以允许传入多个值，会返回第一个非空，例如在join过程，对”requests”字段求和，可以直接这么写coalesce(df1(“requests”)+df2(“requests”), f1(“requests”), df2(“requests”)).alias(“requests”)，对于spark 的RDD算子，df1(“requests”)+df2(“requests”)求和时，一个字段为空，均返回null，对于本课题”requests”求和很符合，运用coalesce算子即提升了效率，又清晰可观。

（3）数据读过程：用于数据读取计算，从 S3 读取之前写入的数据，我们调用spark.read.format(“lakesoul”)，结合CPU个数4，分多个文件并行写入到存储中。

4 结语与展望

通过本次比赛，对数据湖流批一体性能优化有了一定的认识和理解，在相关算法设计方面有如下心得：

（1）合理制定spark任务执行流程，复用已经分配的内存空间，进行并行计算，尽量避免过多的中间变量生成。

（2）根据不同的应用场景和数据特点开发相应的算法，如字段值‘null’字符串与null存在很大的不同，在调用spark SQL join接口时，调用不同算子函数，或者自定义UDF函数。

（3）对于数据湖流批一体大数据场景，任务调度、算子优化、参数调优和数据湖底层架构的选择都将对整体效率产生重大影响。

（4）编程语言方面，尽量选用Scala。Scala设计初衷是要整合面向对象编程和函数式编程的各种特性，Spark是使用Scala语言开发的，方便修改spark底层源代码，自定义适配库函数。

由于团队成员均是在本次比赛中刚刚接触数据湖LakeSoul架构，对很多内容还处于学习摸索阶段，因此方案还有很大的提升空间。保守估计，我们方案的运行效率还有15%-25%的优化提升空间。

致  谢

感谢平台和主办方给了我们这次锻炼机会。感谢指导老师天津大学金志刚教授在spark内存模型调优、RDD的重用和持久化等方向给予的指导和帮助。感谢队友们的精诚合作，让我们能够一步步坚实地迈进决赛。

—End—

戳“阅读原文”，速来参赛办赛~

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]