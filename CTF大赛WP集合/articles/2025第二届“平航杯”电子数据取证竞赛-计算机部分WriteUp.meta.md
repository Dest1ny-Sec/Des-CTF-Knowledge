---
title: 2025 第二届"平航杯"电子数据取证竞赛-计算机部分 WriteUp
contest: 平航杯
year: 2025
difficulty: easy
vuln_type: forensic_disk
tags: [neo4j, Cypher, 助记词, 加密钱包, rednotebook, 取证入门]
attack_chain:
  - 解压容器得到 E:\neo4j-community-3.5.14\data\databases
  - 启动 neo4j 数据库
  - 浏览器登录 neo4j Web UI (http://localhost:7474)
  - 执行 Cypher 查询 MATCH(p:person) WHERE p.name STARTSWITH '白杰' RETURN p.mobile
  - 提取助记词 "flash treat wide divide type plug garlic draft infant broom desert useful" (12 词 BIP39)
key_payload: 'MATCH (p:person) WHERE p.name STARTSWITH ''白杰'' RETURN p.mobile'
one_liner: 入门级电子取证 — neo4j 数据库 Cypher 查询人员手机号 + 助记词还原加密钱包。
lesson: 当代取证常涉及图数据库 (neo4j) 和加密钱包助记词 (BIP39) 提取；rednotebook 是 Linux 常见日记工具，CTF 偶尔出题。
quality: low
---

# 2025 第二届"平航杯"电子数据取证竞赛 - 计算机部分

## 速读
作者 (csdn:Aluxian_) 入门级复盘，检材涉及 neo4j + rednotebook + 加密钱包。

## 关键步骤
- 检材密码: 早起王的爱恋日记
- 路径: `E:\neo4j-community-3.5.14\data\databases`
- Cypher 查询: `MATCH (p:person) WHERE p.name STARTSWITH '白杰' RETURN p.mobile`
- 助记词还原: 12 词 BIP39

## 评价
入门复盘 + 鱼影安全社区招新软广；技术深度有限，但作为 neo4j 取证 + 助记词识别的入门案例可参考。
