---
title: 首届"盘古石杯"全国电子数据取证大赛总决赛-数据分析
contest: 盘古石杯
year: 2023
difficulty: easy
vuln_type: forensic_disk
tags:
- 盘古石
- 数据分析
- SQL聚合
- SUM CASE WHEN
- NULLIF
- 银行卡交易取证
attack_chain: 1. copy *.csv Merged.csv 合并多个CSV|2. 转入对手去重统计+转出对手去重统计+特定卡号(6233542760791453)转入转出比|3. 全卡号按转出比排序DESC|4. 按转入成功总额排序
key_payload: copy *.csv Merged.csv|SELECT COUNT(DISTINCT 交易对手账卡号) FROM Merged WHERE 交易是否成功 = 1 AND 收付标志 = '进'|SELECT COUNT(DISTINCT 交易对手账卡号) FROM Merged WHERE 交易是否成功 = 1 AND 收付标志 = '出'|SELECT SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功, SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出成功, SUM(...)/SUM(...) AS 转出比 FROM Merged WHERE 交易卡号='6233542760791453';|SELECT 交易卡号, SUM(CASE WHEN 交易是否成功 = '01' AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功, ... SUM(...)/NULLIF(SUM(...), 0) AS 转出比 FROM Merged GROUP BY 交易卡号 ORDER BY 转出比 DESC|SELECT 交易卡号, SUM(CASE WHEN 收付标志 = '进' AND 交易是否成功 = '01' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功总额 FROM Merged GROUP BY 交易卡号 ORDER BY 转入成功总额 DESC
one_liner: 首届盘古石杯全国电子数据取证大赛总决赛-数据分析:copy *.csv Merged.csv+SQL SUM CASE WHEN+NULLIF+COUNT(DISTINCT)聚合查询银行卡交易(进/出/比/总额)
lesson: 1) 多个CSV合并:Windows copy *.csv Merged.csv;2) SQL聚合:COUNT(DISTINCT)去重+SUM(CASE WHEN条件聚合;3) NULLIF(SUM(...), 0)防除0;4) 转出比=SUM(出)/SUM(进);5) ORDER BY DESC排序
quality: medium
full_path: 首届“盘古石杯”全国电子数据取证大赛总决赛-数据分析.full.md
meta_path: 首届“盘古石杯”全国电子数据取证大赛总决赛-数据分析.meta.md
images_removed: true
images_removed_count: 7
schema_version: v3.0.0-P0
summary: 首届"盘古石杯"全国电子数据取证大赛总决赛-数据分析。首届盘古石杯全国电子数据取证大赛总决赛-数据分析:copy *.csv Merged.csv+SQL SUM CASE WHEN+NULLIF+COUNT(DISTINCT)聚合查询银行卡交易(进/出/比/总额)。经验：1) 多个CSV合并:Windows copy *.csv Merged.csv;2) SQL聚合:COUNT(DI...
category: forensic
subcategory: disk_forensics
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 7
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/122173.html
reasoning_chain:
- 多 CSV 散落目录 → 触发点：交易流水分散 → 假设：先合并再聚合
- 动作：copy *.csv Merged.csv → 观察：单表 Merged.csv
- Q1 转入对手去重 → 动作：SELECT COUNT(DISTINCT 交易对手账卡号) WHERE 成功=1 AND 进
- Q2 转出对手去重 → 同上 WHERE 出
- Q3 特定卡号 6233542760791453 → 假设：进/出/比 三角聚合
- 动作：SUM(CASE WHEN 成功=1 AND 进 THEN 金额 ELSE 0 END)/SUM(CASE WHEN ... 出)
- Q4 全卡号按转出比排序 → 假设：NULLIF 防除 0
- 动作：GROUP BY 卡号 ORDER BY 转出比 DESC
- Q5 转入成功总额排序 → 动作：SUM(CASE WHEN ... 进 AND 成功='01') ORDER BY DESC
failed_attempts:
- 试图单 CSV 分别聚合 → 失败：题目要求合并后聚合
- 试图不用 NULLIF 防除 0 → 失败：0 除返回 NULL
key_observations:
- 多 CSV 合并：Windows copy *.csv Merged.csv
- SQL 聚合：COUNT(DISTINCT) 去重 + SUM(CASE WHEN 条件聚合
- NULLIF(SUM(...), 0) 防除 0
- 转出比 = SUM(出)/SUM(进) + ORDER BY DESC 排序
prerequisites:
- Windows copy 合并文件
- SQL 聚合函数 COUNT/SUM/GROUP BY
- CASE WHEN 条件聚合 + NULLIF
- ORDER BY DESC 排序
---
# 首届“盘古石杯”全国电子数据取证大赛总决赛-数据分析

> 原文: https://www.ctfiot.com/122173.html
> ID: 122173

copy *.csv Merged.csv

SELECT COUNT(DISTINCT 交易对手账卡号) FROM Merged WHERE 交易是否成功 = 1 AND 收付标志 = '进'

SELECT COUNT(DISTINCT 交易对手账卡号) FROM Merged WHERE 交易是否成功 = 1 AND 收付标志 = '出'

SELECT
SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功,
SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出成功,
SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) / SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出比
FROM
Merged
WHERE
交易卡号='6233542760791453';

SELECT
交易卡号,
SUM(CASE WHEN 交易是否成功 = '01' AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功,
SUM(CASE WHEN 交易是否成功 = '01' AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出成功,
SUM(CASE WHEN (CASE WHEN 交易是否成功 = '01' THEN 1 ELSE 0 END) = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) / NULLIF(SUM(CASE WHEN (CASE WHEN 交易是否成功 = '01' THEN 1 ELSE 0 END) = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END), 0) AS 转出比
FROM
Merged
GROUP BY
交易卡号
ORDER BY
转出比
DESC

SELECT
交易卡号,
SUM(CASE WHEN 收付标志 = '进' AND (CASE WHEN 交易是否成功 = '01' THEN 1 ELSE 0 END) = 1 THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功总额
FROM
Merged
GROUP BY
交易卡号
ORDER BY
转入成功总额 DESC;


```
copy *.csv Merged.csv
SELECT COUNT(DISTINCT 交易对手账卡号) FROM Merged WHERE 交易是否成功 = 1 AND 收付标志 = '进'
SELECT COUNT(DISTINCT 交易对手账卡号) FROM Merged WHERE 交易是否成功 = 1 AND 收付标志 = '出'
SELECT
SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功,
SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出成功,
SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) / SUM(CASE WHEN 交易是否成功 = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出比
FROM
Merged
WHERE
交易卡号='6233542760791453';
SELECT
交易卡号,
SUM(CASE WHEN 交易是否成功 = '01' AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功,
SUM(CASE WHEN 交易是否成功 = '01' AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转出成功,
SUM(CASE WHEN (CASE WHEN 交易是否成功 = '01' THEN 1 ELSE 0 END) = 1 AND 收付标志 = '出' THEN CAST(交易金额 AS FLOAT) ELSE 0 END) / NULLIF(SUM(CASE WHEN (CASE WHEN 交易是否成功 = '01' THEN 1 ELSE 0 END) = 1 AND 收付标志 = '进' THEN CAST(交易金额 AS FLOAT) ELSE 0 END), 0) AS 转出比
FROM
Merged
GROUP BY
交易卡号
ORDER BY
转出比
DESC
SELECT
交易卡号,
SUM(CASE WHEN 收付标志 = '进' AND (CASE WHEN 交易是否成功 = '01' THEN 1 ELSE 0 END) = 1 THEN CAST(交易金额 AS FLOAT) ELSE 0 END) AS 转入成功总额
FROM
Merged
GROUP BY
交易卡号
ORDER BY
转入成功总额 DESC;
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]