---
title: CCF BDCI 2022 二等奖 - 数据湖流批一体性能优化 TT
contest: CCF BDCI 2022 (第十届CCF大数据与计算智能大赛)
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [数据湖, LakeSoul, Spark3.1.2, Scala, 自定义版本号, 并行upsert, MergeOperator, Iceberg, Hudi, 元数据, Future, 乱序]
attack_chain: 改LakeSoul源码增userDefinedTimestamp → Future并行upsert 11个parquet → 0号大文件repartition=8 → MOR表读时合并元数据(version=999) → 注册求和/非空/最后值MergeOperator → snappy压缩parquet输出
key_payload: 自定义Upsert版本号 + Future并行 + LakeSoul MOR表 + 读时合并
one_liner: 汤振东+樊秋轩双人在LakeSoul源码加自定义版本号使乱序upsert并行可行,数据湖性能优化拿二等奖。
lesson: LakeSoul等数据湖默认按系统时间戳决定合并顺序,无法乱序并行;改源码增userDefinedTimestamp使并行+乱序+补数场景都能正确merge;repartition应根据数据量+核数判断,小文件直接写入避免shuffle;MergeOperator注册支持字段级合并策略;COW/MOR选择对性能影响巨大。
quality: high
---
